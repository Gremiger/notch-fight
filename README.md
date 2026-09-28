# Notch Fight

Pixel-art anime fights that drop out of the MacBook Pro notch while Claude Code is working.
Claude (the orange asterisk mascot) is always the protagonist.

![DBZ beam](media/clips/dbz__beam.gif)

## How it works

- `NotchFight.app` hangs a black panel from the notch's bottom edge (width = notch width,
  detected at runtime via `NSScreen.auxiliaryTopLeftArea/RightArea`) and plays the clips.
- Clicking the panel, or `SIGTERM` (`pkill -x NotchFight`), retracts it into the notch and quits.
- Claude Code hooks in `~/.claude/settings.json` drive it:
  - `UserPromptSubmit` → `open -g ~/Workspace/notch-fight/build/NotchFight.app`
  - `Stop` / `StopFailure` → `pkill -x NotchFight`

## Themes and loop keyframes

Each theme has its own neutral pose (the "loop keyframe"). Every clip of a theme starts and
ends on it, so clips of the same theme chain seamlessly. Switching theme plays a
pre-rendered asterisk-iris transition (`transitions/<from>__<to>`).

| Theme | Claude as | Opponent | Clips |
|---|---|---|---|
| `dbz` | Claude | Cell | beam, teleport, barrage, super, genki, standoff |
| `ygo` | Yugi-style duelist | Kaiba | duel |
| `kny` | Tanjiro-style swordsman | Akaza | breath |
| `jjk` | Gojo-style sorcerer | Sukuna | infinity |

Playback: pick a random theme, play up to 2 of its clips (shuffle bag, no immediate
repeat), transition to another random theme, repeat.

## Layout

- `src/clips.py` — sprite engine + DBZ clips.
- `src/themes.py` — YGO/KNY/JJK themes, transitions and the frame export (entry point).
- `src/single_clip.py` — the original standalone 10 s clip (`--black` for the notch version).
- `app/main.swift`, `app/Info.plist` — the notch app.
- `media/` — rendered previews.

## Build

```bash
./build.sh           # frames + app into build/
GIFS=1 ./build.sh    # also refresh media/clips/*.gif
```

Canvas is 185×64 art pixels = 185×64 pt on a 14" MacBook Pro (1 art px = 2 device px).

## Adding a clip

Write a `clip_<name>(f)` in `src/themes.py` (or `src/clips.py` for DBZ) that starts and ends on
the theme's neutral pose, register it in `THEMES`, rebuild. A new theme needs its own
neutral pose; transitions to/from it are generated automatically.
