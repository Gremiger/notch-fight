#!/usr/bin/env bash
# Choose which clips play: a checklist (in a real terminal), or list / enable / disable / mode.
# See scripts/clips.py for the details.
exec python3 "$(cd "$(dirname "$0")" && pwd)/scripts/clips.py" "$@"
