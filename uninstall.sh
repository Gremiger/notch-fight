#!/usr/bin/env bash
# Removes the Notch Fight Claude Code hooks and stops the app. --purge also deletes
# ~/.config/notch-fight (first-clip config) and the build/ folder.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
pkill -x NotchFight 2>/dev/null || true
python3 "$ROOT/scripts/hooks.py" uninstall
if [[ "${1:-}" == "--purge" ]]; then
  rm -rf "$HOME/.config/notch-fight" "$ROOT/build"; echo "purged config + build/"
fi
echo "Notch Fight uninstalled."
