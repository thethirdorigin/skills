#!/usr/bin/env python3
"""
File change tracker hook for Claude Code (PostToolUse).

Auto-discovers SKILL.md files from plugin directories, parses their YAML
frontmatter for file-patterns, matches the edited file path, and suggests
relevant skills.

No manual skill-rules.json needed — SKILL.md frontmatter is the single source
of truth. Shares the cached manifest with skill-activation.py.
"""

import json
import os
import sys
from pathlib import Path

# Import shared logic from skill-activation.py
# Both hooks live in the same directory; import directly.
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from importlib import util as importlib_util

def _load_activation_module():
    """Load skill-activation.py as a module to reuse its functions."""
    spec = importlib_util.spec_from_file_location(
        "skill_activation",
        SCRIPT_DIR / "skill-activation.py"
    )
    mod = importlib_util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_activation = _load_activation_module()

HOME = Path.home()
CACHE_DIR = HOME / ".claude" / "hooks" / ".cache"
TRACKED_FILES = CACHE_DIR / "tracked-files.txt"


def extract_file_path(input_data: dict) -> str:
    """Extract the file path from the tool input."""
    tool_input = input_data.get("tool_input", {})
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except json.JSONDecodeError:
            return ""
    return tool_input.get("file_path", "") or tool_input.get("path", "")


def match_file_patterns(manifest: dict, file_path: str) -> list[str]:
    """Return skill names whose file-patterns match the given file path."""
    matched = []
    for name, skill in manifest.get("skills", {}).items():
        patterns = skill.get("file_patterns", [])
        if not patterns:
            continue
        for pattern in patterns:
            if pattern.startswith("."):
                # Extension match: file must end with this extension
                if file_path.endswith(pattern):
                    matched.append(name)
                    break
            else:
                # Directory/path substring match
                if pattern in file_path:
                    matched.append(name)
                    break
    return matched


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, OSError):
        print("{}")
        return

    tool_name = input_data.get("tool_name", "")
    if tool_name not in ("Edit", "Write", "MultiEdit", "StrReplace"):
        print("{}")
        return

    file_path = extract_file_path(input_data)
    if not file_path:
        print("{}")
        return

    # Track the file
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(TRACKED_FILES, "a") as f:
            f.write(file_path + "\n")
    except OSError:
        pass

    # Load manifest (shared with skill-activation.py)
    dirs = _activation.get_skill_dirs()
    manifest = _activation.load_or_rebuild_manifest(dirs)

    matched = match_file_patterns(manifest, file_path)
    if not matched:
        print("{}")
        return

    # Resolve dependencies for matched skills
    resolved = _activation.resolve_dependencies(manifest, matched)

    lines = [
        "You are editing files that match skill patterns. "
        "If you haven't already, consider loading these skills:\n"
    ]
    for name, reason in resolved:
        lines.append(f'- Invoke the Skill tool with `skill="{name}"` ({reason})')

    context = "\n".join(lines)
    print(json.dumps({"additional_context": context}))


if __name__ == "__main__":
    main()
