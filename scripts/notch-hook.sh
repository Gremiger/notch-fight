#!/usr/bin/env bash
# Claude Code hook: keeps NotchFight up while at least one Claude session is working.
#   notch-hook.sh start <path/to/NotchFight.app>   (UserPromptSubmit)
#   notch-hook.sh stop                              (Stop, StopFailure, SessionEnd)
# Each working session leaves a marker in ~/.config/notch-fight/sessions/<session_id> holding the
# PID of its `claude` process. Stop removes it; the panel retracts only when no live marker is left.
# The app also prunes markers of dead PIDs (a closed terminal never fires Stop) and retracts itself.
set -u
DIR="$HOME/.config/notch-fight/sessions"; LOCK="$HOME/.config/notch-fight/.lock"
mkdir -p "$DIR"

sid="$(python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("session_id",""))
except Exception: pass' 2>/dev/null)"
sid="${sid//[^A-Za-z0-9_-]/}"

# The `claude` process that ran this hook: walk up the process tree.
claude_pid() {
  local p=$PPID
  while [[ -n "$p" && "$p" -gt 1 ]]; do
    [[ "$(basename "$(ps -o comm= -p "$p" 2>/dev/null)")" == claude ]] && { echo "$p"; return; }
    p="$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')"
  done
}

# Serialize start/stop so a stop can't kill the app right as another session starts it.
for _ in $(seq 50); do mkdir "$LOCK" 2>/dev/null && break; sleep 0.05; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

case "${1:-}" in
  start)
    [[ -n "$sid" ]] && echo "$(claude_pid)" > "$DIR/$sid"
    open -g "$2" >/dev/null 2>&1 || true
    ;;
  stop)
    [[ -n "$sid" ]] && rm -f "$DIR/$sid"
    for f in "$DIR"/*; do
      [[ -e "$f" ]] || continue
      pid="$(cat "$f" 2>/dev/null)"
      if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then exit 0; fi   # someone still working
      # no PID recorded (process tree lookup failed): trust the marker for 2 h
      if [[ -z "$pid" && -n "$(find "$f" -mmin -120 2>/dev/null)" ]]; then exit 0; fi
      rm -f "$f"
    done
    pkill -x NotchFight >/dev/null 2>&1 || true
    ;;
esac
exit 0
