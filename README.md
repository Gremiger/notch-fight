# Notch Fight

Pixel-art anime fights that drop out of the MacBook Pro notch while Claude Code is working.
Claude (the orange asterisk mascot) is always the protagonist.

![DBZ Cell Games](media/clips/dbz__cellgames.gif)

## Install

Requirements: **macOS** (ideally a MacBook with a notch), Xcode Command Line Tools (`swiftc`),
`python3`. Pillow is installed automatically if missing; `ffmpeg` is optional (GIF previews).

```bash
git clone <this repo> && cd notch-fight
./install.sh        # checks requirements, builds, registers the Claude Code hooks (idempotent)
./uninstall.sh      # removes the hooks and stops the app (--purge also deletes build/ + config)
nf clips            # choose which clips play (see "Choosing clips"); install.sh links `nf` into ~/.local/bin
nf pause 1h         # and the rest of the controls (see "The nf command")
# several Claude profiles? NOTCH_FIGHT_CLAUDE_DIRS=~/.claude-work:~/.claude-personal ./install.sh (same for uninstall)
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
- Claude Code hooks in `$CLAUDE_CONFIG_DIR/settings.json` (default `~/.claude`; for several profiles: `NOTCH_FIGHT_CLAUDE_DIRS=~/.claude-work:~/.claude-personal ./install.sh`) drive it:
  - `UserPromptSubmit` → `scripts/notch-hook.sh start` (marks the session as working, opens the app)
  - `Stop` / `StopFailure` / `SessionEnd` → `scripts/notch-hook.sh stop`
- Several sessions can work at once (even across profiles): each one leaves a marker in
  `~/.config/notch-fight/sessions/` with its `claude` PID, and the panel retracts only when the
  last one stops. The app also drops markers of dead PIDs (e.g. a closed terminal never fires
  `Stop`). An interrupted turn (Esc) doesn't fire `Stop` either: the panel stays until that
  session's next turn ends, or click it.

## Themes and loop keyframes

Each theme has its own neutral pose (the "loop keyframe"). Every clip of a theme starts and
ends on it. Switching theme plays a
pre-rendered asterisk-iris transition (`transitions/<from>__<to>`).

| Theme | Claude as | Opponent | Clips |
|---|---|---|---|
| `dbz` | Claude (goes Super Saiyan) | Perfect Cell, on the Cell Games ring | cellgames |
| `ygo` | Yugi-style duelist (D-D-D-DUEL and Heart of the Cards close-ups, Dark Magician card reveal, Mirror Force) | Kaiba + Blue-Eyes White Dragon hologram, in the Kaiba Corp stadium (life points 8000 to 0) | duel |
| `kny` | Tanjiro-style swordsman (Water Breathing dragon and Hinokami Kagura close-ups) | Akaza (kanji-eye close-up), on the Mugen Train roof; beheaded, crumbles to ash | breath |
| `jjk` | Gojo at the Shibuya crossing on 10.31 (Infinity stops Dismantle and the lunge — MUGEN, blindfold-off SIX EYES close-up, Blue, Red, HOLLOW PURPLE close-up erases the street) | Sukuna (Dismantle slashes, blown into the 109 tower, reforms from cursed motes) | infinity |
| `fn` | Jonesy with a pickaxe (cranks 90s to high ground, wood-edit shotgun close-up — 200 HEADSHOT, #1 VICTORY ROYALE crown card, default dance) | Geno, on the island (Tilted Towers skyline, Battle Bus overhead, the storm wall closing in; AR, rocket, eliminated into cubes) | royale |
| `pkm` | Claude in Ash's cap on a GBA battle screen (FIGHT menu, HP/EXP boxes; Quick Attack, Shadow Ball — SUPER EFFECTIVE close-up, levels up, YOU WIN!, Poke Ball GO! close-up) | Mewtwo on the far platform (Psychic warps the screen, faints, a wild one appears) | psychic |
| `snk` | Survey Corps scout (ODM gear) | a grinning Titan in Trost (red roofs, church spire, the Wall; grin + crossed-blades close-ups, SHINZOU WO SASAGEYO!, nape slash, steam) | survey |
| `nrt` | Naruto in the Hidden Leaf under the Hokage faces (hand-seal close-up, shadow clones, leaps the Great Fireball, Rasengan close-up) | Madara (gunbai swats the clones, Sharingan close-up, Katon) | shadowclone |
| `naruto-edo` | Naruto on the Fourth Great Ninja War battlefield (clones, Rasengan, Sage Mode close-up, Rasenshuriken wind dome) | Kabuto + Edo Tensei'd Codex, OpenCode, Grok (coffin close-up, paper-dust regeneration) | edotensei |
| `naruto-shikamaru` | Shikamaru in the Nara clan forest: hops the scythe, the thinking-pose close-up (WHAT A DRAG...), Kagemane catches Hidan mid-run and he copies every move, Asuma's lighter in close-up (FOR ASUMA.), the tags go up: CHECKMATE. | Hidan (FOR JASHIN!, I CANT MOVE!, climbs out of the pit: I AM IMMORTAL!) | kagemane |
| `naruto-zabuza` | Kakashi (Sharingan close-up, copied jutsu) | Zabuza on the lake (Water Dragons clash, Great Waterfall) | waterdragon |
| `dbz-buu` | Claude, then Clodex (fusion dance with Codex, FU-SION-HA! close-up, goes blue for the Final Kamehameha) on the Supreme Kai's world | Kid Buu (grin close-up, planet-destroying ball, regenerates) | fusion |
| `jjk-sukuna` | Gojo in ruined Shibuya under a red moon (hand-sign close-up with one Six Eye, Unlimited Void swallows the shrine, four Black Flashes) | Sukuna (grin close-up with four eyes, Malevolent Shrine, Dismantle + Cleave storm) | domain |
| `hxh` | Gon (fishing rod, adult form close-up) | Neferpitou (Terpsichora) | jajanken |
| `fma` | Colonel Mustang (glove snap close-up, flame alchemy) | Envy (disguised as Claude, burned to his true form) | flame |
| `dbz-jiren` | Claude in Ultra Instinct (silver-eyes close-up, dodges everything, instant hits from everywhere) at the Tournament of Power | Jiren (red glare close-up, knocked off the arena) | ultra |
| `dbz-freezer` | Claude as Goku with Codex on planet Namek (Codex lifted and blown into light, CODEX...! FREEZEEER!!! rage close-up, storm and lightning, first SUPER SAIYAN close-up, Kamehameha) | Freezer, final form (smug close-up closing his hand, Death Beams, Death Ball; Porunga revives Codex) | namek |
| `mk` | Claudepion (Scorpion: spear, Toasty fatality) | Sub-Zero, with the arcade HUD | fatality |
| `apex` | a Legend with jump pack and grapple (kill-leader banner close-up) | Wraith (Into the Void, Dimensional Rift) | champion |
| `cs` | Counter-Terrorist (AWP scope close-up, defuse) | Phoenix Terrorist, with the 1.6 HUD | defuse |
| `hl` | Gordon Freeman in the HEV suit (crowbar, Gravity Gun) | headcrabs + a Combine soldier (G-Man close-up) | lambda |
| `rm` | Rick with the portal gun | a Cromulon (SHOW ME WHAT YOU GOT!) | schwifty |
| `inv` | Invincible (Mark) | Omni-Man: the train, then PIENSA CLAUDE! (close-up) and the beatdown | train |
| `sf` | Ryu (Hadouken, Shoryuken, Shinku Hadouken close-up) | M. Bison, with the SF2 HUD | hadouken |
| `mario` | Mario (? blocks, Super Star close-up, the axe) | Bowser on the castle bridge | castle |
| `mc` | Steve (pillar, bow, diamond sword) | a Creeper (close-up) and the Ender Dragon | enderdragon |
| `ds` | a Sun knight (roll, Estus, PRAISE THE SUN, fake YOU DIED) | Malenia | felled |
| `sw` | a Jedi | Darth Vader (I AM YOUR FATHER close-up) | father |
| `matrix` | Neo (bullet time, NO.) | Agent Smith and his clones | bullettime |
| `term` | the T-800 (red HUD close-up) | the T-1000 (frozen and shattered) | judgment |
| `bb` | Heisenberg (SAY MY NAME: CLAUDENBERG) | Tuco | saymyname |
| `snk-colosal` | Survey Corps scout (ODM gear) | the Colossal Titan behind the Wall (eye close-up) | colossal |
| `jojo` | Jotaro-style Stand user (ORA ORA barrage, moves in stopped time) | DIO and The World (ZA WARUDO, clock close-up) | theworld |
| `etendo` | Claude the brand designer | the old Etendo logo (grabbed, spun, morphed into the new star in a close-up — NEW ETENDO!) | rebrand |
| `sl` | Sung Jinwoo, the Shadow Monarch (twin daggers, ARISE! close-up, shadow army) | Igris the Blood-Red Knight, extracted as a shadow (System windows) | arise |
| `memes` | Claude on a vaporwave stage (hug, uppercut, blast, deal-with-it shades) | a meme boss rush: Forever Alone, Tung Tung Tung Sahur, then the FINAL BOSS "6 7" (close-up, weighing-gesture attacks) | bossrush |
| `ben10` | Ben Tennyson with the Omnitrix (HERO TIME close-up, Heatblast, Four Arms, XLR8, the watch times out, Diamondhead) | Vilgax in the desert at night | hero |
| `sonic` | Claude as a blue hedgehog in Green Hill (rings, spin dash, loop-de-loop, ring loss, 7 Chaos Emeralds, SUPER CLAUDE) | Dr. Eggman in the Egg Mobile with the wrecking ball (GOT THROUGH ACT 1 tally) | greenhill |
| `tetris` | Claude in an ushanka (punches and kicks the falling pieces into place, FINALLY! I-piece close-up, TETRIS!) | the falling tetrominoes on an NES/Game Boy playfield in front of the Kremlin (4-line clear, Game Boy rocket ending) | tetris |
| `clippy` | Claude on a Windows 98 desktop (clicks NO, punches error dialogs, END TASK, bends him straight into the Recycle Bin) | Clippy in a DEATH MATCH (NEED HELP? spam, grows huge, turns into a bicycle/bell/question mark, crazy-eyes close-up) | deathmatch |
| `predator` | an 80s jungle commando (laser triple-dot, thermal-vision close-up, mud camouflage, log trap) | the Predator (decloaks, unmasks with a RAAARGH!, wrist self-destruct and mushroom blast) | hunt |
| `alien` | a warrant-officer survivor with a pulse rifle, then in the yellow power loader (motion-tracker and inner-jaw close-ups, GET AWAY FROM HER!) | the Xenomorph (acid blood that eats the deck, blown out of the airlock) | nostromo |
| `avp` | Claude caught between them in the Antarctic pyramid (WHOEVER WINS... WE LOSE., clan-mark close-up, alien-head shield + spear, back-to-back close-up) | a Xenomorph, the Predator and the Queen (buried under the collapsing pyramid) | pyramid |
| `gta` | CJ on Grove Street (AH SHIT HERE WE GO AGAIN..., wanted stars, handbrake donut, MISSION PASSED!) | a low-poly 3D police cruiser (flat-shaded software renderer: chase, barrel roll, explosion) | grove |
| `simpsons` | a Sector 7G worker (D'OH!, stomps the uranium rod back in, MMM... ROSQUILLAS) | Mr. Burns and his hounds in the nuclear plant (EXCELENTE... close-up) | meltdown |
| `portal` | the test subject with the Portal Gun in an Aperture test chamber (drops through blue/orange portals, turns the turret fire back through them, shoots a portal at the MOON; THIS WAS A TRIUMPH card, the cake is a lie) | GLaDOS on her ceiling arm (turrets, neurotoxin, yellow-to-red eye close-up — YOU MONSTER; her cores pop off, Wheatley babbles, SPAAACE!; sucked out into space) | triumph |
| `amongus` | an orange crewmate with Codex in The Skeld cafeteria (fix-wiring close-up, spots Codex venting ?!, lights out, DEAD BODY REPORTED, CODEX VENTED! meeting, VICTORY) | Codex, the impostor (I WAS IN ELECTRICAL, sweating close-up, voted off: CODEX WAS THE IMPOSTOR.) | impostor |
| `jjk-toji` | Toji (Inventory curse, Inverted Spear of Heaven, SORCERER KILLER close-up) | young Gojo: the spear shatters his Infinity | sakahoko |
| `jjk-maki` | Maki, awakened (glasses crack close-up, afterimage cuts) | the Zen'in clan, then her father Ogi | zenin |
| `meshi` | Laios (sword, I WONDER HOW IT TASTES... close-up) | the Red Dragon, then Senshi cooks it: DRAGON STEW | dragonstew |
| `terraria` | the Terrarian: Terra Blade beams, or a staff + whip with a Stardust Dragon | the Eye of Cthulhu (servants, phase 2 close-up, coins) | melee, summoner |
| `mist` | Vin, Mistborn (mistcloak, Steel Pushes on coins, ATIUM close-up with her future shadows) | a Steel Inquisitor in Luthadel's mists and ash (she Pulls the spike from his back); off by default | inquisitor |
| `mist-kelsier` | Kelsier, the Survivor of Hathsin, in Fountain Square under the red sun (sub-theme of `mist`, off by default): hops the axe, Steel-Pushes coins, a pewter punch; the spear, and the smile in close-up (THERES ALWAYS ANOTHER SECRET); the skaa raise their hands, the mists roll in and he stands up out of them | a Steel Inquisitor, then the Lord Ruler | survivor |
| `deadpool` | Deadpool (katanas, the arm pops off and a tiny one grows back, talks to us in yellow boxes and knocks on the notch, MAXIMUM EFFORT close-up); `notchverse`: a TVA door into the other themes (steals Madara's gunbai, tells the Cyclops he is NOBODY, OH NO. close-up before Cell's Kamehameha, comes home charred: WORTH IT.); `webcam`: finds the MacBook camera (fisheye close-up: HI MOM!), pushes the panel's edges, waits on Claude (STILL THINKING?) and dozes off as the panel closes (HEY! NOT YET!) | Wolverine in the Void (SNIKT, takes the chimichanga: BUB.); Madara, Polyphemus, Cell | bub, notchverse, webcam |
| `spidey` | Miles Morales, on twos with magenta/cyan rim light (camouflage split into comic panels, A LEAP OF FAITH close-up, the city turns upside down with streaking lights, THWIP, webs, venom blast ZZAKT!) | the Prowler in Brooklyn (webbed to a wall, police lights) | leap |
| `xmen-nightcrawler` | Nightcrawler (X-Men '97) on a New York rooftop at dusk: BAMF out of the crossfire, pops up behind each drone in a puff of indigo smoke, the yellow-eyed grin in close-up (BAMF!), teleports the last one into the sky (AUF WIEDERSEHEN!) | four Sentinel drones (MUTANT DETECTED) | bamf |
| `xmen-gambit` | Gambit (X-Men '97) in the French Quarter at night: a charged card for each drone (BONJOUR MES AMIS), vaults the giant hand on his staff, the ace of spades in close-up (CHARGED), blows the Sentinel apart and walks out of the smoke (DEALER WINS.) | three Sentinel drones, then a giant Sentinel (SURRENDER MUTANT) | charged |
| `coraline` | Coraline in stop-motion (the little door and the tunnel, NO., the seeing stone close-up with the ghost children's eyes, the escape with the cat, the button key: CLICK.) | the Other Mother: WE ONLY WANT YOU TO STAY., then her spider form with needle fingers | buttons |
| `odyssey` | Odysseus in a Corinthian helmet in the Cyclops' cave (Homer, book 9): gives him wine, the MY NAME IS NOBODY close-up, the olive stake heated in the fire and driven into the eye (close-up, TSSSS), rides out under the ram | Polyphemus (WHO ARE YOU?, MORE WINE!, NOBODY IS HURTING ME!; the other Cyclopes: NOBODY? THEN HUSH!) | nobody |
| `dnd` | A wizard (pointed hat, starry robe, beard, crystal staff), the DM narrating in parchment boxes: `nat20` (ROLL INITIATIVE, Shield against the eye rays, the d20 close-up lands NAT 20!, Fireball: CRITICAL HIT!) and `nat1` (the d20 lands NAT 1., the fireball comes down on his own hat: CRITICAL FAIL, PRESTIDIGITATION to clean up) | a Beholder (crashes and dreams another Beholder; laughs at the NAT 1) | nat20, nat1 |
| `ghibli-totoro` | Satsuki at the bus stop in the rain, no fight (fireflies, the lamp, lends Totoro the spare umbrella, grin close-up, the Catbus's headlight eyes, a bundle of acorns) | Totoro and the Catbus | busstop |
| `phm` | Ryland Grace in the Hail Mary's lab, no fight: `rocky` (the Blip-A, the xenonite tunnel, chords that become AMAZE AMAZE AMAZE, FIST MY BUMP close-up) and `astrophage` (the star dims, the bench, Taumoeba under the microscope, IT WORKS!); off by default | Rocky, a friend; Astrophage, the problem | rocky, astrophage |
| `arg` | the albiceleste number 10 in the 2022 World Cup final (Dibu's leg on Kolo Muani at 123 in close-up, PENALES with the TV scoreboard, GOL, Montiel's last penalty, CAMPEONES DEL MUNDO, the Cup and the third star) | France | final |
| `arg-86` | Diego at the Azteca, 1986 (sub-theme of `arg`), with the TV scoreboard: `mano` (the one-two with Valdano, Hodge's loop, up against the taller Shilton, the fist in close-up, the English round the referee, LA MANO DE DIOS) and `siglo` (the spin in his own half, the camera following his run past a slide, two lunges and the keeper, Butcher from behind; TA TA TA TA, GOLAZO, BARRILETE COSMICO, DE QUE PLANETA VINISTE) | England | mano, siglo |
| `arg-mate` | No fight: a ronda de mate in a patio under the parra, the flag with the Sol de Mayo on the wall: the first one for the cebador (EL PRIMERO ES DEL CEBADOR), the mate going round with facturas (RRRP), the yerba in close-up until ESTA LAVADO, a GRACIAS, the golden hour | three friends | ronda |
| `arg-colapinto` | Franco Colapinto, number 43, in the dark-blue Williams: the five red lights (AND AWAY WE GO!), four cars passed as the TV tower takes COL from P12 to P8, team radio (GOOD JOB FRANCO. P8. POINTS.), the chequered flag, the helmet in close-up with the stands in its visor (VAMOS FRANCO), a lap of honour under the flags | the rest of the grid | debut |
| `cai` | Independiente, the Rojo (red shirt, blue shorts), in the clasico de Avellaneda at the Libertadores de America: past three Racing defenders (OLE!: a nutmeg, a lob, a feint), the strike in close-up, top corner (GOL DEL ROJO, red flares), the trophy cabinet in close-up as the seven Libertadores light up: REY DE COPAS | Racing | clasico |
| `eternauta` | Juan Salvo in the home-made insulated suit (El Eternauta), on a street in Vicente Lopez under the deadly snowfall: the bullets spark off the shell (PAC! PAC! PAC!), a Mano at its console in close-up driving the beetles, Favalli, Lucas and Polsky come out of the snow and fire together (FUEGO!), four visors in close-up: NADIE SE SALVA SOLO | a cascarudo, the giant beetle (the snow buries it) | nevada |

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

## The nf command

`install.sh` links `nf` into `~/.local/bin` (it leaves an existing `nf` that isn't ours alone), so it
works from any folder:

```bash
nf clips [...]              # which clips play: the checklist, list, enable, disable, mode (= ./clips.sh)
nf pause                    # a menu: 15 min, 30 min, 1 h, 4 h, 8 h, until resumed, or N minutes
nf pause 45m                # or straight away: 15m, 1h, 1h30m, 90 (minutes), forever
nf resume                   # show it again (right away if a Claude session is working)
nf status                   # paused?, quiet hours, screen sharing, clips, scale, hooks, sessions, app
nf preview odyssey          # play a clip or a whole theme in the notch now, then close (no focus change)
nf quiet 22:00-08:00        # never show it in that window (add `weekdays` for Monday to Friday; `off`)
nf share on|off             # hide it while sharing the screen (on by default)
```

Whether the panel may show is decided in one place, `nf gate` (`scripts/nf.py`): the Claude Code hook
asks before opening it, and the app asks every few seconds while it is up, so a pause, quiet hours or a
screen share hides a panel that is already out. Sessions keep being tracked meanwhile. The pause lives
in `~/.config/notch-fight/paused`; quiet hours and `pauseOnShare` in `config.json`.

Screen sharing is detected by process: Zoom runs `CptHost` while sharing and macOS runs
`screencaptureui` while recording. A share from a browser tab (Meet, Teams on the web) looks like any
other tab from outside, so it isn't caught: list your own process names in `"shareProcesses"` in
`config.json`, or `nf pause` for the call.

## Choosing clips

```bash
./clips.sh                         # checklist (in a real terminal): space toggles, m mode, enter saves
./clips.sh list                    # on/off per clip
./clips.sh disable jjk-sukuna       # a clip (<theme>__<clip>) or a whole theme
./clips.sh enable sw__father
./clips.sh mode disabled           # what happens to NEW clips; the current selection is kept
```

Two modes, stored in `~/.config/notch-fight/config.json` (`install.sh` offers the checklist too):

| `newClips` | List | New clips |
|---|---|---|
| `"enabled"` (default) | `"disabled": [...]`: everything plays except these | play until you turn them off |
| `"disabled"` | `"enabled": [...]`: only these play | ignored until you turn them on |

- Clips forced with `first` (or `--first`) still play once at launch, even when turned off. The
  checklist shows them; `f` clears the list (`./build.sh` puts each new clip there).
- Enabling a theme in `"disabled"` mode enables the clips it has now, not ones added later.
- Some clips ship **off by default** (niche ones, see "Adding a clip"): they are listed as
  `(off by default)` and only play once you turn them on. In `"enabled"` mode those go in an
  `"enabled"` list next to `"disabled"`.
- With nothing selected the panel does not show at all. Changes apply from the next launch.
- `NOTCH_FIGHT_CONFIG=/path/config.json` points the app and `clips.sh` at another config (tests and
  dev only: the app sees it when its binary is run directly, not through `open`).
- To check what would play without opening the panel:
  `build/NotchFight.app/Contents/MacOS/NotchFight --print-selection` (the active count, forced clips, and
  whether the panel would show).
- Tests: `python3 -m unittest discover tests` (the app tests need `./build.sh`). They use `--print-selection`,
  so no panel shows and the focused window keeps focus. `NOTCH_FIGHT_TEST_PANEL=1` adds real launches
  (in the background with `open -g`: the panel shows, focus stays).

## Panel shape

The panel takes its size and position from the real notch of each Mac. Two looks can be tuned in
`~/.config/notch-fight/config.json` (defaults shown; `./build.sh` only rewrites `"first"`):

| Key | Default | Effect |
|---|---|---|
| `fillet` | `0` | Concave flare (pt) where the panel meets the notch. `8` gives the rounded "grows out of the notch" look; on some Macs it sticks out as a ledge. |
| `stretch` | `true` | Stretch the art to the notch width. `false` keeps square pixels, centred at 185pt (the black margins blend in). |
| `scale` | `1` | Make the panel bigger than the notch (e.g. `1.5`), keeping the art's proportions and staying centred under it. `install.sh` sets `1.5` when Vorssaint is installed (its bar is wider than the notch), unless you already chose a scale. |
| `widthTweak` | per model | Width correction (pt) when the panel overhangs by a hair. Built-in: `Mac14,2` → `-1`. |

```json
{ "fillet": 8, "stretch": false }
```

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
│   ├── dbz.py  ygo.py  kny.py  jjk.py  fn.py  pkm.py  snk.py  nrt.py  hxh.py  fma.py  mk.py  jojo.py  apex.py  cs.py  hl.py  rm.py  inv.py  phm.py  arg.py  odyssey.py  dnd.py  eternauta.py  cai.py
│   ├── sf.py  mario.py  mc.py  ds.py  sw.py  matrix.py  term.py  bb.py
│   ├── naruto_edo.py  naruto_zabuza.py  dbz_buu.py  dbz_jiren.py  jjk_sukuna.py  ghibli_totoro.py  snk_colosal.py  arg_86.py  naruto_shikamaru.py  mist_kelsier.py  xmen_nightcrawler.py  xmen_gambit.py  arg_mate.py  arg_colapinto.py   # sub-themes
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
ONLY=sonic GIFS=1 ./build.sh      # just one theme (or theme__clip, comma-separated) on top of the last build
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
- **Off by default:** for a clip most people may not want (a football club, a brand), ship it off so
  users opt in: `DEFAULT_OFF = True` in the theme file turns off all its clips, and
  `clip('<name>', <frames>, clip_<name>, off=True)` (or `off=False` to override the theme) does it per clip.
  `build.py` marks them in the build (`build/clips/<clip>/.default-off`); the app and `./clips.sh` read it.
  `./build.sh` still puts a new clip first, so you see it while you make it.
