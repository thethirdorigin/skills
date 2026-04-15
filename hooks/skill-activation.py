#!/usr/bin/env python3
"""
Skill auto-activation hook for Claude Code (UserPromptSubmit).

Auto-discovers SKILL.md files from plugin directories, parses their YAML
frontmatter for triggers and dependencies, matches the user prompt, resolves
dependency chains, and injects Skill tool invocation instructions.

No manual skill-rules.json needed — SKILL.md frontmatter is the single source
of truth. A cached manifest is rebuilt when any SKILL.md changes.
"""

import json
import os
import re
import sys
from collections import deque
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HOME = Path.home()
CACHE_DIR = HOME / ".claude" / "hooks" / ".cache"
MANIFEST_PATH = CACHE_DIR / "skill-manifest.json"

# Directories to scan for SKILL.md files.
# Override with SKILL_DIRS env var (colon-separated paths).
DEFAULT_SKILL_DIRS = [
    HOME / ".claude" / "skills",
    HOME / ".claude" / "plugins",
]


def get_skill_dirs():
    """Return the list of directories to scan for SKILL.md files."""
    env = os.environ.get("SKILL_DIRS")
    if env:
        return [Path(p) for p in env.split(":") if p]
    return DEFAULT_SKILL_DIRS


# ---------------------------------------------------------------------------
# Frontmatter parser (no PyYAML dependency)
# ---------------------------------------------------------------------------

def parse_frontmatter(path: Path) -> dict | None:
    """Parse YAML frontmatter between --- delimiters from a SKILL.md file.

    Returns a dict with keys: name, triggers, dependencies, file_patterns, path.
    Returns None if the file cannot be read or has no valid frontmatter.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    # Frontmatter must start at line 1
    if not text.startswith("---"):
        return None

    end = text.find("\n---", 3)
    if end == -1:
        return None

    fm_block = text[4:end]  # skip opening ---\n

    result = {
        "name": "",
        "triggers": [],
        "dependencies": [],
        "file_patterns": [],
        "path": str(path),
    }

    current_key = None
    for line in fm_block.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Detect list item under current key
        if stripped.startswith("- ") and current_key:
            value = stripped[2:].strip().strip("'\"")
            if current_key == "triggers":
                result["triggers"].append(value)
            elif current_key == "dependencies":
                result["dependencies"].append(value)
            elif current_key in ("file-patterns", "file_patterns"):
                result["file_patterns"].append(value)
            continue

        # Detect key: value or key:
        m = re.match(r"^([a-zA-Z_-]+)\s*:\s*(.*)", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip().strip("'\"")
            if key == "name":
                result["name"] = value
                current_key = None
            elif key == "triggers":
                current_key = "triggers"
            elif key == "dependencies":
                current_key = "dependencies"
            elif key in ("file-patterns", "file_patterns"):
                current_key = "file_patterns"
            elif key == "description":
                # Multi-line description — skip until next key
                current_key = "description"
            else:
                current_key = key  # track for other multi-line fields
        elif current_key == "description":
            # continuation of description, skip
            continue

    if not result["name"]:
        return None

    return result


# ---------------------------------------------------------------------------
# Discovery and caching
# ---------------------------------------------------------------------------

def find_skill_files(dirs: list[Path]) -> list[Path]:
    """Recursively find all SKILL.md files under the given directories.

    Uses os.walk with followlinks=True to traverse symlinked skill directories
    (e.g. ~/.claude/skills/audit -> ../../.agents/skills/audit).
    """
    results = []
    seen = set()
    for d in dirs:
        if not d.exists():
            continue
        for root, _dirs, files in os.walk(str(d), followlinks=True):
            for f in files:
                if f == "SKILL.md":
                    p = Path(root) / f
                    # Resolve to avoid counting the same file via different symlink paths
                    resolved = p.resolve()
                    if resolved not in seen:
                        seen.add(resolved)
                        results.append(p)
    return results


def build_manifest(dirs: list[Path]) -> dict:
    """Scan SKILL.md files and build a manifest dict keyed by skill name."""
    manifest = {"skills": {}, "file_mtimes": {}}
    for path in find_skill_files(dirs):
        fm = parse_frontmatter(path)
        if fm and fm["name"]:
            manifest["skills"][fm["name"]] = fm
            manifest["file_mtimes"][str(path)] = os.path.getmtime(path)
    return manifest


def load_or_rebuild_manifest(dirs: list[Path]) -> dict:
    """Load cached manifest if fresh, otherwise rebuild."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if MANIFEST_PATH.exists():
        try:
            cached = json.loads(MANIFEST_PATH.read_text())
            # Check if any SKILL.md has been modified since cache was written
            stale = False
            current_files = find_skill_files(dirs)
            cached_mtimes = cached.get("file_mtimes", {})

            # Check for new or modified files
            for path in current_files:
                key = str(path)
                if key not in cached_mtimes:
                    stale = True
                    break
                if os.path.getmtime(path) > cached_mtimes[key]:
                    stale = True
                    break

            # Check for removed files
            if not stale:
                current_set = {str(p) for p in current_files}
                for key in cached_mtimes:
                    if key not in current_set:
                        stale = True
                        break

            if not stale:
                return cached
        except (json.JSONDecodeError, OSError):
            pass

    manifest = build_manifest(dirs)
    try:
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    except OSError:
        pass  # cache write failure is non-fatal
    return manifest


# ---------------------------------------------------------------------------
# Matching and dependency resolution
# ---------------------------------------------------------------------------

def match_triggers(manifest: dict, prompt: str) -> list[str]:
    """Return skill names whose triggers match the prompt (case-insensitive)."""
    prompt_lower = prompt.lower()
    matched = []
    for name, skill in manifest.get("skills", {}).items():
        for trigger in skill.get("triggers", []):
            if trigger.lower() in prompt_lower:
                matched.append(name)
                break
    return matched


def resolve_dependencies(manifest: dict, matched: list[str]) -> list[tuple[str, str]]:
    """Resolve transitive dependencies for matched skills.

    Returns a list of (skill_name, reason) tuples in dependency-first order.
    Reason is 'matched' for directly matched skills or 'dependency of X' for deps.
    """
    skills = manifest.get("skills", {})
    result = []
    resolved = set()  # skills already added to result
    in_queue = set()   # cycle detection
    queue = deque()

    # Seed with matched skills
    for name in matched:
        queue.append((name, "matched"))
        in_queue.add(name)

    while queue:
        name, reason = queue.popleft()
        if name in resolved:
            continue

        # Resolve this skill's dependencies first (depth-first via re-queuing)
        skill = skills.get(name, {})
        deps = skill.get("dependencies", [])
        unresolved_deps = [d for d in deps if d not in resolved and d not in in_queue]

        if unresolved_deps:
            # Re-queue current skill after its deps
            queue.appendleft((name, reason))
            for dep in reversed(unresolved_deps):
                queue.appendleft((dep, f"dependency of {name}"))
                in_queue.add(dep)
        else:
            resolved.add(name)
            result.append((name, reason))

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, OSError):
        print("{}")
        return

    user_prompt = input_data.get("userMessage", "")
    if not user_prompt:
        print("{}")
        return

    dirs = get_skill_dirs()
    manifest = load_or_rebuild_manifest(dirs)
    matched = match_triggers(manifest, user_prompt)

    if not matched:
        print("{}")
        return

    resolved = resolve_dependencies(manifest, matched)

    if not resolved:
        print("{}")
        return

    # Build injection text
    lines = [
        "Based on your prompt, the following skills are relevant. "
        "Load them by invoking the Skill tool for each, in this order:\n"
    ]
    for i, (name, reason) in enumerate(resolved, 1):
        lines.append(f'{i}. Invoke the Skill tool with `skill="{name}"` ({reason})')

    lines.append(
        "\nLoad dependency skills before the skills that need them. "
        "Do not skip dependency loading — sub-skills are NOT automatically in context."
    )

    context = "\n".join(lines)
    print(json.dumps({"additional_context": context}))


if __name__ == "__main__":
    main()
