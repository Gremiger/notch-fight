# Notch Fight — rules for agents

- **Claude is always the protagonist** of every clip.
- **Every clip starts and ends on its theme's neutral pose** (the loop keyframe). Same-theme
  clips chain seamlessly; a new theme needs its own neutral pose (transitions are automatic).
- **After creating a clip, make it play first** so the dev sees it immediately.
  `./build.sh` does this automatically for any clip that was not in the previous build
  (writes `~/.config/notch-fight/config.json` → `{"first": "<theme>__<clip>"}`).
  To force one: `FIRST=<theme>__<clip> ./build.sh`. Tell the dev which clip was set first.
- Regenerate previews with `GIFS=1 ./build.sh` and commit `media/clips/*.gif` with the change.
- Builds must stay reproducible: seed randomness with `zlib.crc32`, never `hash()`.
