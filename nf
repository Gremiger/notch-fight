#!/usr/bin/env bash
# nf: manage Notch Fight from anywhere (install.sh links it into ~/.local/bin). See scripts/nf.py.
SELF="$0"; while [[ -L "$SELF" ]]; do t="$(readlink "$SELF")"; [[ "$t" = /* ]] && SELF="$t" || SELF="$(dirname "$SELF")/$t"; done
exec python3 "$(cd "$(dirname "$SELF")" && pwd)/scripts/nf.py" "$@"
