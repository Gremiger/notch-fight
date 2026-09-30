"""Choose which clips Notch Fight plays. Writes ~/.config/notch-fight/config.json:

    {"newClips": "enabled",  "disabled": [...]}   everything plays except these; new clips play
    {"newClips": "disabled", "enabled":  [...]}   only these play; new clips are ignored

    ./clips.sh                     checklist (needs a real terminal)
    ./clips.sh list                on/off per clip, the mode, the forced first clips
    ./clips.sh enable  <clip|theme>...
    ./clips.sh disable <clip|theme>...
    ./clips.sh mode enabled|disabled   what happens to NEW clips (the current selection is kept)

Names are clip folders under build/clips (<theme>__<clip>); a theme name means all its clips.
Clips forced with "first" still play once at launch. NOTCH_FIGHT_CONFIG overrides the config path
(tests/dev: the app only sees it when its binary is run directly, not through `open`).
"""
import difflib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.environ.get('NOTCH_FIGHT_CONFIG') or os.path.expanduser('~/.config/notch-fight/config.json')
CLIPS_DIR = os.path.join(ROOT, 'build', 'clips')
MODES = ('enabled', 'disabled')

class ClipsError(Exception): pass

def theme_of(name): return name.split('__', 1)[0]

def clip_names(clips_dir):
    if not os.path.isdir(clips_dir): raise ClipsError(f'no clips in {clips_dir}: run ./build.sh first')
    return sorted(n for n in os.listdir(clips_dir) if '__' in n and not n.startswith('.'))

def load(path):
    if not os.path.exists(path): return {}
    try:
        with open(path) as fh: return json.load(fh)
    except json.JSONDecodeError as e:
        raise ClipsError(f'{path} is not valid JSON (line {e.lineno}, column {e.colno}: {e.msg}); fix it first')

def mode_of(cfg): return 'disabled' if cfg.get('newClips') == 'disabled' else 'enabled'

def active(cfg, clips):
    """The clips that play in the rotation."""
    if mode_of(cfg) == 'disabled': return set(clips) & set(cfg.get('enabled', []))
    return set(clips) - set(cfg.get('disabled', []))

def updates(cfg, clips, on, mode):
    """Config keys to write for this selection (and the key to drop). Names that are not current
    clips are kept when the mode does not change (a rename or a partial build loses nothing)."""
    same = mode_of(cfg) == mode
    if mode == 'enabled':
        kept = [n for n in cfg.get('disabled', []) if n not in clips] if same else []
        return {'newClips': 'enabled', 'disabled': sorted(set(clips) - set(on)) + kept}, {'enabled'}
    kept = [n for n in cfg.get('enabled', []) if n not in clips] if same else []
    return {'newClips': 'disabled', 'enabled': sorted(set(on) & set(clips)) + kept}, {'disabled'}

def expand(names, clips):
    """Clip or theme names -> clip names; unknown names fail with the closest matches."""
    out = []
    themes = sorted({theme_of(c) for c in clips})
    for n in names:
        if n in clips: out.append(n)
        elif n in themes: out += [c for c in clips if theme_of(c) == n]
        else:
            close = difflib.get_close_matches(n, clips + themes, n=3)
            raise ClipsError(f"unknown clip or theme '{n}'" + (f" (did you mean: {', '.join(close)}?)" if close else ''))
    return out

def save(path, up, drop):
    """Re-read the config (another process may have changed it), apply our keys, write atomically."""
    cfg = load(path)
    for k in drop: cfg.pop(k, None)
    cfg.update(up)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh: json.dump(cfg, fh, indent=2); fh.write('\n')
    os.replace(tmp, path)


class Checklist:
    """The checklist's state: which clips are on, the mode, the forced first clips."""
    def __init__(self, clips, cfg):
        self.clips, self.mode = clips, mode_of(cfg)
        self.on = active(cfg, clips)
        self.first = list(cfg.get('first', [])) if isinstance(cfg.get('first'), list) else \
                     ([cfg['first']] if cfg.get('first') else [])
        self.first_cleared = False

    def themes(self): return sorted({theme_of(c) for c in self.clips})

    def rows(self):
        out = []
        for t in self.themes():
            out.append(('theme', t))
            out += [('clip', c) for c in self.clips if theme_of(c) == t]
        return out

    def members(self, name): return [c for c in self.clips if theme_of(c) == name] if '__' not in name else [name]

    def mark(self, name):
        m = self.members(name); n = sum(c in self.on for c in m)
        return 'x' if n == len(m) else ('~' if n else ' ')

    def toggle(self, name):
        m = self.members(name)
        if self.mark(name) == 'x': self.on -= set(m)
        else: self.on |= set(m)

    def set_all(self, value): self.on = set(self.clips) if value else set()
    def switch_mode(self): self.mode = 'disabled' if self.mode == 'enabled' else 'enabled'
    def clear_first(self): self.first, self.first_cleared = [], True

    def result(self, cfg):
        up, drop = updates(cfg, self.clips, self.on, self.mode)
        if self.first_cleared: up['first'] = []
        return up, drop


HELP = "↑↓/jk move · space toggle · a all · n none · m new-clips mode · f clear forced · enter save · q quit"

def run_checklist(clips, path):
    import curses
    cfg = load(path); m = Checklist(clips, cfg); rows = m.rows()

    def ui(scr):
        curses.curs_set(0); pos, top, warn = 0, 0, ''
        while True:
            scr.erase(); h, w = scr.getmaxyx()
            new = 'new clips PLAY (until you turn them off)' if m.mode == 'enabled' else 'new clips are IGNORED (until you turn them on)'
            head = [f'Notch Fight: clips ({len(m.on)}/{len(clips)} on)', f'Mode [m]: {new}']
            if m.first: head.append(f"Forced first at every launch [f clears]: {', '.join(m.first)}")
            head.append(HELP)
            for i, line in enumerate(head): scr.addnstr(i, 0, line, w - 1, curses.A_BOLD if i == 0 else 0)
            body = h - len(head) - 2
            if pos < top: top = pos
            if pos >= top + body: top = pos - body + 1
            for i, (kind, name) in enumerate(rows[top:top + body]):
                indent = '' if kind == 'theme' else '    '
                line = f"{'>' if top + i == pos else ' '} {indent}[{m.mark(name)}] {name}"
                scr.addnstr(len(head) + 1 + i, 0, line, w - 1, curses.A_REVERSE if top + i == pos else 0)
            if warn: scr.addnstr(h - 1, 0, warn, w - 1, curses.A_BOLD)
            k = scr.getch(); warn = ''
            if k in (curses.KEY_UP, ord('k')): pos = max(0, pos - 1)
            elif k in (curses.KEY_DOWN, ord('j')): pos = min(len(rows) - 1, pos + 1)
            elif k == ord(' '): m.toggle(rows[pos][1])
            elif k == ord('a'): m.set_all(True)
            elif k == ord('n'): m.set_all(False)
            elif k == ord('m'): m.switch_mode()
            elif k == ord('f'): m.clear_first()
            elif k in (ord('q'), 27): return False
            elif k in (10, 13, curses.KEY_ENTER):
                if not m.on and not warn:
                    warn = 'Nothing selected: the panel will not show at all. Enter again to save anyway.'
                    scr.addnstr(h - 1, 0, warn, w - 1, curses.A_BOLD)
                    if scr.getch() not in (10, 13, curses.KEY_ENTER): warn = ''; continue
                return True

    if curses.wrapper(ui):
        save(path, *m.result(cfg)); print(f'saved {path}: {len(m.on)}/{len(clips)} clips on, new clips {m.mode}')
    else: print('not saved')

def cmd_list(clips, cfg):
    on = active(cfg, clips)
    print(f"new clips: {mode_of(cfg)} ({'they play' if mode_of(cfg) == 'enabled' else 'ignored until enabled'})")
    for c in clips: print(f"  {'on ' if c in on else 'off'}  {c}")
    first = cfg.get('first')
    if first: print(f"forced first (plays once at every launch): {first}")

def main(argv):
    try:
        clips = clip_names(CLIPS_DIR)
        cfg = load(CONFIG)
        if not argv:
            if not (sys.stdin.isatty() and sys.stdout.isatty()):
                print('The checklist needs a real terminal (not `!` inside Claude Code). Open one and run ./clips.sh,')
                print('or use the commands:'); print(__doc__.split('\n\n')[2]); return 1
            try: import curses  # noqa: F401
            except ImportError: print('this python3 has no curses; use the commands:'); print(__doc__); return 1
            run_checklist(clips, CONFIG); return 0
        cmd, args = argv[0], argv[1:]
        if cmd == 'list': cmd_list(clips, cfg); return 0
        if cmd in ('enable', 'disable') and args:
            on = active(cfg, clips); names = set(expand(args, clips))
            on = on | names if cmd == 'enable' else on - names
            save(CONFIG, *updates(cfg, clips, on, mode_of(cfg)))
            print(f"{cmd}d: {', '.join(sorted(names))}"); return 0
        if cmd == 'mode' and len(args) == 1 and args[0] in MODES:
            save(CONFIG, *updates(cfg, clips, active(cfg, clips), args[0]))
            print(f'new clips: {args[0]} (the current selection is kept)'); return 0
        print(__doc__); return 2
    except ClipsError as e:
        print(f'error: {e}', file=sys.stderr); return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
