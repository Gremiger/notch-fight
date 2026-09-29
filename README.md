# Notch Fight

Pixel-art anime fights that drop out of the MacBook Pro notch while Claude Code is working.
Claude (the orange asterisk mascot) is always the protagonist.

![DBZ beam](media/clips/dbz__beam.gif)

## Install

Requirements: **macOS** (ideally a MacBook with a notch), Xcode Command Line Tools (`swiftc`),
`python3`. Pillow is installed automatically if missing; `ffmpeg` is optional (GIF previews).

```bash
git clone <this repo> && cd notch-fight
./install.sh        # checks requirements, builds, registers the Claude Code hooks (idempotent)
./uninstall.sh      # removes the hooks and stops the app (--purge also deletes build/ + config)
```

Or just ask Claude Code in this repo: *"install this"* — `CLAUDE.md` tells it what to do.

**Platforms:** the app is macOS-only (Swift/AppKit + the notch API). The clip generator
(`src/`, Python + Pillow) runs anywhere. On a Mac without a notch the panel hangs from the top
centre with the default 185 pt width. A Linux port would only need a new player (e.g. a GTK
always-on-top borderless window) reading the same `build/clips` PNGs.

## How it works

- `NotchFight.app` hangs a black panel from the notch's bottom edge (width = notch width,
  detected at runtime via `NSScreen.auxiliaryTopLeftArea/RightArea`) and plays the clips.
- Clicking the panel, or `SIGTERM` (`pkill -x NotchFight`), retracts it into the notch and quits.
- Claude Code hooks in `~/.claude/settings.json` (added by `./install.sh`) drive it:
  - `UserPromptSubmit` → `open -g <repo>/build/NotchFight.app`
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
| `fn` | Fortnite default with pickaxe | Geno | royale |
| `pkm` | Pokémon with Ash's cap | Mewtwo | psychic |
| `snk` | Survey Corps scout (ODM gear) | 5 titans + the Armored Titan | survey |
| `nrt` | Naruto (headband, shadow clones, Rasengan) | Madara (Sharingan close-up) | shadowclone |
| `naruto-edo` | Naruto (clones, Rasengan, Rasenshuriken) | Kabuto + Edo Tensei'd Codex, OpenCode, Grok (coffin close-up) | edotensei |
| `dbz-buu` | Claude, then Clodex (fusion dance with Codex) | Kid Buu (regenerates) | fusion |
| `jjk-sukuna` | Gojo-style sorcerer (Unlimited Void, eye close-up, Black Flash) | Sukuna (Malevolent Shrine) | domain |
| `hxh` | Gon (fishing rod, adult form close-up) | Neferpitou (Terpsichora) | jajanken |
| `fma` | Colonel Mustang (glove snap close-up, flame alchemy) | Envy (disguised as Claude, burned to his true form) | flame |
| `dbz-jiren` | Claude in Ultra Instinct (silver hair, afterimages) | Jiren (instant hits from behind) | ultra |
| `mk` | Claudepion (Scorpion: spear, Toasty fatality) | Sub-Zero, with the arcade HUD | fatality |
| `snk-colosal` | Survey Corps scout (ODM gear) | the Colossal Titan behind the Wall (eye close-up) | colossal |

Playback (per launch): forced clips first, then every other clip in random order — no clip
repeats until all of them have played, then a new round starts. Clips are grouped up to 2 per
theme visit to keep transitions few.

## Forcing the first clip

Useful to test a new clip or to show one off. Value is a clip (`<theme>__<clip>`, e.g.
`fn__royale`), a whole theme (e.g. `ygo`), or a comma-separated list / JSON array of them,
played in order. After the forced clips, playback continues normally.

```bash
open -g build/NotchFight.app --args --first fn__royale     # one-off
open -g build/NotchFight.app --args --first pkm__psychic,snk__survey
NOTCH_FIGHT_FIRST=jjk ./build/NotchFight.app/Contents/MacOS/NotchFight
```

Or persistently (also applies to the Claude Code hook launches):

```bash
mkdir -p ~/.config/notch-fight && cp config.example.json ~/.config/notch-fight/config.json
```

Priority: `--first` arg > `NOTCH_FIGHT_FIRST` env > config file. An unknown name is logged
(with the list of valid names) and ignored. Clip names = folder names under `build/clips/`.

## Layout

```
src/
├── engine/            # shared by every theme
│   ├── core.py        # canvas constants, sprite drawing (auto outline + aura), sparks, orbs, easing
│   ├── palette.py     # one char per colour for sprite grids (themes add their own)
│   ├── claude.py      # Claude's base sprites + tools to dress him up / derive poses
│   ├── text.py        # 3x5 pixel font
│   ├── fx.py          # effect registry (@fx('name')) + effects used by several themes
│   ├── logos.py       # pixel logos of other coding agents (Codex, OpenCode, Grok) + stick body
│   └── render.py      # scene/actor model, backgrounds, render(), callout(), clip()
├── themes/            # one file per theme: sprites, its own effects, its clips, CLIPS = [...]
│   ├── dbz.py  ygo.py  kny.py  jjk.py  fn.py  pkm.py  snk.py  nrt.py  hxh.py  fma.py  mk.py
│   ├── naruto_edo.py  dbz_buu.py  dbz_jiren.py  jjk_sukuna.py  snk_colosal.py   # sub-themes
│   └── __init__.py    # auto-discovers every theme module
├── transitions.py     # asterisk-iris transition between themes
├── build.py           # entry point used by build.sh
└── legacy/single_clip.py   # the original standalone 10 s clip (--black for the notch version)
app/main.swift, app/Info.plist   # the notch app
media/                           # rendered previews
```

## Build

```bash
./build.sh           # frames + app into build/
GIFS=1 ./build.sh    # also refresh media/clips/*.gif
```

Canvas is 185×64 art pixels = 185×64 pt on a 14" MacBook Pro (1 art px = 2 device px).

## Adding a clip

See `CLAUDE.md` for the rules (a new clip is auto-set to play first).

- **New clip in an existing theme:** add a `clip_<name>(f)` returning a scene to that theme's file
  and append `clip('<name>', <frames>, clip_<name>)` to its `CLIPS`. It must start and end on the
  theme's neutral pose.
- **New theme:** create `src/themes/<id>.py` with `from engine import *`, `THEME = '<id>'`,
  `register_bg(THEME, ...)`, its sprites/effects (`@fx('name')`) and `CLIPS`. Nothing else to
  touch: themes are auto-discovered and transitions to/from it are generated.
