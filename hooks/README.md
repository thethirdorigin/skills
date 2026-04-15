# Skill Hooks for Claude Code

Generic hooks that auto-discover skills from SKILL.md frontmatter. No manual
configuration file needed — adding a new skill with the right frontmatter is
all that's required.

## How It Works

### skill-activation.py (UserPromptSubmit)

Fires on every user prompt. Scans all SKILL.md files, matches trigger phrases
against the prompt, resolves dependency chains, and injects Skill tool
invocation instructions into Claude's context.

**Example**: User types "audit this codebase" → hook matches `audit` →
resolves dependency `codegraph` → injects:

```
1. Invoke the Skill tool with skill="codegraph" (dependency of audit)
2. Invoke the Skill tool with skill="audit" (matched)
```

### file-tracker.py (PostToolUse on Edit/Write)

Fires after file edits. Matches the edited file path against skills'
`file-patterns` and suggests relevant skills.

**Example**: Editing a `.tsx` file → suggests `react-best-practises`.

## SKILL.md Frontmatter

The hooks read these fields from SKILL.md YAML frontmatter:

```yaml
---
name: my-skill            # Required — skill identifier
triggers:                 # Optional — prompt phrases that activate this skill
  - audit this codebase
  - find code smells
dependencies:             # Optional — skills to load before this one
  - codegraph
file-patterns:            # Optional — file patterns that suggest this skill
  - .tsx
  - frontend/
---
```

| Field | Used By | Purpose |
|-------|---------|---------|
| `name` | Both | Skill identifier |
| `triggers` | skill-activation.py | Case-insensitive substring match against user prompt |
| `dependencies` | Both | Transitive dependency resolution (BFS, cycle-safe) |
| `file-patterns` | file-tracker.py | Extension (`.tsx`) or directory (`frontend/`) match |

## Adding a New Skill

Just create a SKILL.md with the appropriate frontmatter fields. The hooks
auto-discover it on the next prompt (the cached manifest refreshes when any
SKILL.md file changes).

No config files to update. No registration step.

## Installation

```bash
./hooks/install.sh
```

This will:
1. Symlink hook scripts to `~/.claude/hooks/`
2. Register hooks in `~/.claude/settings.json`
3. Clear the manifest cache (rebuilds on next prompt)

Safe to run multiple times. Backs up existing hooks before overwriting.

### Custom skill directories

Set `SKILL_DIRS` to scan additional directories:

```bash
export SKILL_DIRS="$HOME/.claude/skills:$HOME/.claude/plugins:/path/to/more/skills"
```

Default: `~/.claude/skills` and `~/.claude/plugins`.

## Cache

A manifest cache at `~/.claude/hooks/.cache/skill-manifest.json` avoids
re-scanning SKILL.md files on every prompt. It auto-refreshes when any
SKILL.md is added, removed, or modified (checked via mtime comparison).

To force a rebuild: `rm ~/.claude/hooks/.cache/skill-manifest.json`
