#!/usr/bin/env bash
# Generates every clip + transition frame and builds NotchFight.app into build/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/build"; APP="$OUT/NotchFight.app"
mkdir -p "$OUT"
before="$(ls "$OUT/clips" 2>/dev/null || true)"
(cd "$OUT" && python3 "$ROOT/src/build.py")

# Rule: a newly created clip plays FIRST so the dev sees it right away.
# All new clips are queued first, in order. FIRST=a__x,b__y ./build.sh forces a list; FIRST=none skips.
new="$(comm -13 <(echo "$before" | sort) <(ls "$OUT/clips" | sort) | paste -sd, -)"
[[ -z "$before" ]] && new=""          # first build ever: everything is "new", pick nothing
FIRST="${FIRST:-$new}"
if [[ -n "$FIRST" && "$FIRST" != "none" ]]; then
  mkdir -p "$HOME/.config/notch-fight"
  # update only "first": the panel-shape keys (fillet, stretch, widthTweak) are the user's
  python3 - "$FIRST" "$HOME/.config/notch-fight/config.json" <<'PY'
import json, sys, os
names, path = sys.argv[1].split(','), sys.argv[2]
cfg = json.load(open(path)) if os.path.exists(path) else {}
cfg['first'] = names
open(path, 'w').write(json.dumps(cfg, indent=2) + '\n')
PY
  echo "First clip set to $FIRST (~/.config/notch-fight/config.json)"
fi

rm -rf "$APP"; mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$ROOT/app/Info.plist" "$APP/Contents/"
cp -R "$OUT/clips" "$OUT/transitions" "$APP/Contents/Resources/"
# pin the deployment target: some toolchains default to a macOS newer than the running one (LaunchServices error -10825)
swiftc -O -target "$(uname -m)-apple-macos13.0" "$ROOT/app/main.swift" -o "$APP/Contents/MacOS/NotchFight"
codesign -s - --force "$APP" >/dev/null 2>&1

if [[ "${GIFS:-0}" == "1" ]]; then   # GIFS=1 ./build.sh refreshes media/clips previews
  for d in "$OUT"/clips/*/; do n=$(basename "$d")
    ffmpeg -y -loglevel error -framerate 20 -i "$d%03d.png" \
      -vf "scale=iw*2:ih*2:flags=neighbor,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=none" \
      -loop 0 "$ROOT/media/clips/$n.gif"
  done
fi
echo "Built $APP"
