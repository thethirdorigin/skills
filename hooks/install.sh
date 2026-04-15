#!/bin/bash
# Install skill hooks for Claude Code.
#
# Symlinks the hooks from this repository to ~/.claude/hooks/ and registers
# them in ~/.claude/settings.json. Safe to run multiple times (idempotent).
#
# Usage:
#   ./hooks/install.sh            # from the repo root
#   bash hooks/install.sh         # or explicitly

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOKS_DIR="$HOME/.claude/hooks"
SETTINGS_FILE="$HOME/.claude/settings.json"
CACHE_DIR="$HOOKS_DIR/.cache"

echo "=== Claude Code Hooks Installer ==="
echo ""

# -----------------------------------------------------------------------
# 1. Create directories
# -----------------------------------------------------------------------
mkdir -p "$HOOKS_DIR"
mkdir -p "$CACHE_DIR"

# -----------------------------------------------------------------------
# 2. Symlink hook scripts
# -----------------------------------------------------------------------
HOOKS=(
  "skill-activation.py"
  "file-tracker.py"
)

for hook in "${HOOKS[@]}"; do
  src="$SCRIPT_DIR/$hook"
  dst="$HOOKS_DIR/$hook"

  if [ ! -f "$src" ]; then
    echo "WARNING: $src not found, skipping"
    continue
  fi

  if [ -L "$dst" ]; then
    current_target="$(readlink "$dst")"
    if [ "$current_target" = "$src" ]; then
      echo "OK: $hook already linked"
      continue
    fi
    echo "UPDATE: $hook symlink target changed, relinking"
    rm "$dst"
  elif [ -f "$dst" ]; then
    # Back up existing non-symlink file
    backup="$dst.backup.$(date +%Y%m%d%H%M%S)"
    echo "BACKUP: $hook -> $backup"
    mv "$dst" "$backup"
  fi

  ln -s "$src" "$dst"
  echo "LINKED: $hook -> $dst"
done

# Make scripts executable
chmod +x "$SCRIPT_DIR/skill-activation.py" "$SCRIPT_DIR/file-tracker.py" 2>/dev/null || true

# -----------------------------------------------------------------------
# 3. Register hooks in settings.json
# -----------------------------------------------------------------------
register_hooks() {
  # Build the desired hooks configuration
  local activation_cmd="python3 $HOOKS_DIR/skill-activation.py"
  local tracker_cmd="python3 $HOOKS_DIR/file-tracker.py"

  if [ ! -f "$SETTINGS_FILE" ]; then
    # Create settings.json from scratch
    cat > "$SETTINGS_FILE" <<SETTINGS
{
  "\$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$activation_cmd"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$tracker_cmd"
          }
        ]
      }
    ]
  }
}
SETTINGS
    echo "CREATED: $SETTINGS_FILE with hook registration"
    return
  fi

  # Check if hooks are already registered (look for our Python scripts)
  if grep -q "skill-activation.py" "$SETTINGS_FILE" 2>/dev/null; then
    echo "OK: Hooks already registered in settings.json"
    return
  fi

  # Settings file exists but doesn't have our hooks — use jq if available
  if command -v jq &>/dev/null; then
    local tmp="$(mktemp)"
    jq --arg acmd "$activation_cmd" --arg tcmd "$tracker_cmd" '
      .hooks.UserPromptSubmit = [
        {
          "hooks": [
            {
              "type": "command",
              "command": $acmd
            }
          ]
        }
      ] |
      .hooks.PostToolUse = [
        {
          "matcher": "Edit|MultiEdit|Write",
          "hooks": [
            {
              "type": "command",
              "command": $tcmd
            }
          ]
        }
      ]
    ' "$SETTINGS_FILE" > "$tmp" && mv "$tmp" "$SETTINGS_FILE"
    echo "UPDATED: settings.json with hook registration"
  else
    echo ""
    echo "WARNING: jq not found. Please manually add hooks to $SETTINGS_FILE:"
    echo ""
    echo '  "hooks": {'
    echo '    "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "'"$activation_cmd"'"}]}],'
    echo '    "PostToolUse": [{"matcher": "Edit|MultiEdit|Write", "hooks": [{"type": "command", "command": "'"$tracker_cmd"'"}]}]'
    echo '  }'
    echo ""
  fi
}

register_hooks

# -----------------------------------------------------------------------
# 4. Clear stale cache so manifest rebuilds on next prompt
# -----------------------------------------------------------------------
rm -f "$CACHE_DIR/skill-manifest.json" 2>/dev/null || true
echo "CLEARED: Skill manifest cache (will rebuild on next prompt)"

# -----------------------------------------------------------------------
# Done
# -----------------------------------------------------------------------
echo ""
echo "Installation complete. Hooks will activate on your next Claude Code session."
echo ""
echo "To verify: start a new session and type 'audit this codebase' — you should"
echo "see additional context suggesting both audit and codegraph skills."
