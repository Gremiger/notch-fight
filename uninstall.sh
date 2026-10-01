#!/usr/bin/env bash
# Removes the Notch Fight Claude Code hooks and stops the app. --purge also deletes
# ~/.config/notch-fight (first-clip config) and the build/ folder.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
pkill -x NotchFight 2>/dev/null || true
python3 "$ROOT/scripts/hooks.py" uninstall
[[ -L "$HOME/.local/bin/nf" && "$(readlink "$HOME/.local/bin/nf")" == "$ROOT/nf" ]] && rm "$HOME/.local/bin/nf" && echo "removed ~/.local/bin/nf"
rm -f "$HOME/.config/notch-fight/paused"
if [[ "${1:-}" == "--purge" ]]; then
  rm -rf "$HOME/.config/notch-fight" "$ROOT/build"; echo "purged config + build/"
fi
echo "Notch Fight uninstalled."
