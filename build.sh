#!/usr/bin/env bash
# Generates every clip + transition frame and builds NotchFight.app into build/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/build"; APP="$OUT/NotchFight.app"
mkdir -p "$OUT"
(cd "$OUT" && python3 "$ROOT/src/themes.py")

rm -rf "$APP"; mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$ROOT/app/Info.plist" "$APP/Contents/"
cp -R "$OUT/clips" "$OUT/transitions" "$APP/Contents/Resources/"
swiftc -O "$ROOT/app/main.swift" -o "$APP/Contents/MacOS/NotchFight"
codesign -s - --force "$APP" >/dev/null 2>&1

if [[ "${GIFS:-0}" == "1" ]]; then   # GIFS=1 ./build.sh refreshes media/clips previews
  for d in "$OUT"/clips/*/; do n=$(basename "$d")
    ffmpeg -y -loglevel error -framerate 20 -i "$d%03d.png" \
      -vf "scale=iw*2:ih*2:flags=neighbor,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=none" \
      -loop 0 "$ROOT/media/clips/$n.gif"
  done
fi
echo "Built $APP"
