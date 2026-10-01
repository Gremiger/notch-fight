"""nf: one command to manage Notch Fight from anywhere (install.sh links it into ~/.local/bin).

    nf clips [...]                 which clips play (same as ./clips.sh: checklist, list, enable, ...)
    nf pause [15m|30m|1h|4h|8h|forever|<minutes>|<N>m|<N>h]
                                   stop showing the panel for a while (a menu when no time is given)
    nf resume                      show it again (right away if a Claude session is working)
    nf status                      paused?, quiet hours, screen sharing, clips, scale, hooks, sessions
    nf preview <clip|theme>...     play those clips in the notch now, then close (no focus change)
    nf quiet [HH:MM-HH:MM [all|weekdays] | off]
                                   never show it in that window, every day or Monday to Friday
    nf share [on|off]              hide it while you share your screen (Zoom, macOS screen recording)

Whether the panel may show right now is decided in one place, `gate()`, which the Claude Code hook
(scripts/notch-hook.sh) and the app (every few seconds while it is up) both ask: `nf gate` exits 0
when it may show, 1 when it may not, and prints why.
State: ~/.config/notch-fight/paused ({"until": <epoch> | null}) and, in config.json, "quiet" and
"pauseOnShare". NOTCH_FIGHT_CONFIG moves config.json, and the paused file next to it (tests/dev).
"""
import datetime, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import clips as clipsmod                                              # noqa: E402

CONFIG = clipsmod.CONFIG
STATE_DIR = os.path.dirname(CONFIG)
PAUSED = os.path.join(STATE_DIR, 'paused')
SESSIONS = os.path.expanduser('~/.config/notch-fight/sessions')
APP = os.path.join(ROOT, 'build', 'NotchFight.app')
PRESETS = [('15 minutes', 15), ('30 minutes', 30), ('1 hour', 60), ('4 hours', 240), ('8 hours', 480), ('until I resume', None)]
# Processes that only run while the screen is being shared or recorded. Zoom starts CptHost to share;
# screencaptureui is macOS's own capture (Cmd-Shift-5). Browser-based calls (Meet, Teams on the web)
# cannot be told apart from a process list: add your own names under "shareProcesses" in config.json.
SHARE_PROCESSES = ['CptHost', 'screencaptureui']

class NfError(Exception): pass

# ---- state -------------------------------------------------------------------------------------------
def load_cfg(): return clipsmod.load(CONFIG)

def save_cfg(cfg):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = CONFIG + '.tmp'
    with open(tmp, 'w') as fh: json.dump(cfg, fh, indent=2); fh.write('\n')
    os.replace(tmp, CONFIG)

def paused_until(now=None):
    """None: not paused; float('inf'): until resumed; else the epoch it ends (expired pauses are cleared)."""
    now = time.time() if now is None else now
    try:
        with open(PAUSED) as fh: until = json.load(fh).get('until')
    except (OSError, ValueError): return None
    if until is None: return float('inf')
    if until <= now:
        try: os.remove(PAUSED)
        except OSError: pass
        return None
    return float(until)

def set_pause(minutes, now=None):
    now = time.time() if now is None else now
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(PAUSED, 'w') as fh: json.dump({'until': None if minutes is None else now + minutes * 60}, fh)

def parse_duration(s):
    """'15m' / '1h' / '90' (minutes) / '1h30m' / 'forever' -> minutes (None = until resumed)."""
    s = s.strip().lower()
    if s in ('forever', 'off', 'indef', 'indefinitely', 'until-resume', 'inf'): return None
    if re.fullmatch(r'\d+', s): return int(s)
    m = re.fullmatch(r'(?:(\d+)h)?\s*(?:(\d+)m(?:in)?)?', s)
    if not m or not (m.group(1) or m.group(2)): raise NfError(f"can't read '{s}' as a time: try 15m, 1h, 90 or forever")
    return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)

def parse_quiet(span):
    m = re.fullmatch(r'(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})', span)
    if not m: raise NfError(f"can't read '{span}': use HH:MM-HH:MM, e.g. 22:00-08:00")
    h1, m1, h2, m2 = map(int, m.groups())
    if not (h1 < 24 and h2 < 24 and m1 < 60 and m2 < 60): raise NfError(f"'{span}' is not a time of day")
    return f'{h1:02d}:{m1:02d}', f'{h2:02d}:{m2:02d}'

def in_quiet(q, now):
    """Is `now` (a datetime) inside the quiet window q = {"from","to","days"}? Wraps past midnight; with
    "weekdays" the window belongs to the day it starts on (Friday night yes, Saturday night no)."""
    if not q: return False
    f = [int(x) for x in q['from'].split(':')]; t = [int(x) for x in q['to'].split(':')]
    mins, start, end = now.hour * 60 + now.minute, f[0] * 60 + f[1], t[0] * 60 + t[1]
    if start == end: return False
    weekdays = q.get('days') == 'weekdays'
    if start < end:
        return start <= mins < end and (not weekdays or now.weekday() < 5)
    if mins >= start: return not weekdays or now.weekday() < 5                    # tonight
    if mins < end: return not weekdays or (now - datetime.timedelta(days=1)).weekday() < 5   # since last night
    return False

def sharing(cfg):
    """A screen-sharing / recording process that is running, or None."""
    for name in cfg.get('shareProcesses', SHARE_PROCESSES):
        if subprocess.run(['pgrep', '-x', name], capture_output=True).returncode == 0: return name
    return None

def gate(cfg=None, now=None):
    """(may_show, reason)."""
    cfg = load_cfg() if cfg is None else cfg
    now_ts = time.time() if now is None else now.timestamp()
    until = paused_until(now_ts)
    if until is not None:
        return False, 'paused until resumed' if until == float('inf') else f'paused until {fmt_time(until)}'
    q = cfg.get('quiet')
    if in_quiet(q, now or datetime.datetime.now()): return False, f"quiet hours ({q['from']}-{q['to']}{', weekdays' if q.get('days') == 'weekdays' else ''})"
    if cfg.get('pauseOnShare', True):
        who = sharing(cfg)
        if who: return False, f'screen sharing ({who})'
    return True, 'showing'

def fmt_time(ts): return time.strftime('%H:%M', time.localtime(ts))
def fmt_left(secs):
    m = int(round(secs / 60)); return f'{m} min' if m < 60 else f'{m // 60} h {m % 60:02d} min'

def live_sessions():
    n = 0
    for f in (os.listdir(SESSIONS) if os.path.isdir(SESSIONS) else []):
        if f.startswith('.'): continue
        try: pid = int(open(os.path.join(SESSIONS, f)).read().strip() or 0)
        except (OSError, ValueError): pid = 0
        if pid:
            try: os.kill(pid, 0); n += 1
            except PermissionError: n += 1
            except OSError: pass
        elif time.time() - os.path.getmtime(os.path.join(SESSIONS, f)) < 7200: n += 1
    return n

def app_running(): return subprocess.run(['pgrep', '-x', 'NotchFight'], capture_output=True).returncode == 0
def hide_app(): subprocess.run(['pkill', '-x', 'NotchFight'], capture_output=True)
def show_app(*args): subprocess.run(['open', '-g', APP, *(['--args', *args] if args else [])], capture_output=True)

# ---- commands ----------------------------------------------------------------------------------------
def cmd_pause(args):
    if args: minutes = parse_duration(' '.join(args))
    elif sys.stdin.isatty() and sys.stdout.isatty():
        for i, (label, _) in enumerate(PRESETS, 1): print(f'  {i}. {label}')
        print(f'  {len(PRESETS) + 1}. other (minutes)')
        pick = input('Pause for: ').strip()
        if not pick.isdigit() or not 1 <= int(pick) <= len(PRESETS) + 1: raise NfError('nothing paused')
        minutes = PRESETS[int(pick) - 1][1] if int(pick) <= len(PRESETS) else parse_duration(input('Minutes: '))
    else: raise NfError('how long? e.g. nf pause 30m (15m, 30m, 1h, 4h, 8h, forever, or minutes)')
    if minutes is not None and minutes <= 0: raise NfError('the pause has to last at least a minute')
    set_pause(minutes); hide_app()
    print('Paused until you run: nf resume' if minutes is None else f'Paused for {fmt_left(minutes * 60)}, until {fmt_time(time.time() + minutes * 60)}')

def cmd_resume(args):
    was = paused_until()
    try: os.remove(PAUSED)
    except OSError: pass
    ok, why = gate()
    if not ok: print(f'Resumed, but not showing yet: {why}'); return
    if live_sessions() and not app_running(): show_app(); print('Resumed: a Claude session is working, here it comes')
    else: print('Resumed' if was is not None else 'Not paused')

def cmd_status(args):
    cfg = load_cfg(); ok, why = gate(cfg)
    until = paused_until()
    pause = 'no' if until is None else ('until you resume' if until == float('inf') else f'until {fmt_time(until)} ({fmt_left(until - time.time())} left)')
    q = cfg.get('quiet')
    quiet = 'off' if not q else f"{q['from']}-{q['to']} {'(weekdays)' if q.get('days') == 'weekdays' else '(every day)'}"
    share = 'off' if not cfg.get('pauseOnShare', True) else ('on, sharing now' if sharing(cfg) else 'on')
    try:
        names = clipsmod.clip_names(clipsmod.CLIPS_DIR); off = clipsmod.default_off(clipsmod.CLIPS_DIR)
        act = clipsmod.active(cfg, names, off); clip_line = f'{len(act)}/{len(names)} active ({clipsmod.mode_of(cfg)} mode for new clips)'
    except clipsmod.ClipsError as e: clip_line = str(e)
    from hooks import claude_dirs
    def has_hook(d):
        try: return 'notch-hook.sh' in open(os.path.join(d, 'settings.json')).read()
        except OSError: return False
    import glob
    dirs = sorted(set(claude_dirs()) | set(glob.glob(os.path.expanduser('~/.claude*'))))   # every profile on this Mac
    hooked = [d for d in dirs if os.path.isdir(d) and has_hook(d)]
    rows = [('now', 'may show' if ok else f'hidden: {why}'), ('paused', pause), ('quiet hours', quiet),
            ('screen sharing', share), ('clips', clip_line), ('scale', str(cfg.get('scale', 1))),
            ('hooks', ', '.join(d.replace(os.path.expanduser('~'), '~') for d in hooked) or 'not installed (./install.sh)'),
            ('sessions', f'{live_sessions()} working'), ('app', ('running' if app_running() else 'built') if os.path.isdir(APP) else 'not built (./build.sh)')]
    for k, v in rows: print(f'  {k:<15}{v}')

def cmd_preview(args):
    if not args: raise NfError('which clip or theme? e.g. nf preview odyssey')
    names = clipsmod.clip_names(clipsmod.CLIPS_DIR)
    todo = clipsmod.expand(args, names)
    was_up = app_running()
    if was_up: hide_app(); time.sleep(0.6)
    show_app('--first', ','.join(todo), '--only')
    # once the preview is over, bring the normal panel back if a Claude session is still working
    subprocess.Popen(['/bin/bash', '-c', f'sleep 2; while pgrep -x NotchFight >/dev/null; do sleep 1; done; '
                      f'exec python3 {__file__!r} _after_preview'], start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Playing {len(todo)} clip{'s' if len(todo) != 1 else ''}: {', '.join(todo)}")

def cmd_after_preview(args):
    if gate()[0] and live_sessions() and not app_running(): show_app()

def cmd_quiet(args):
    cfg = load_cfg()
    if not args:
        q = cfg.get('quiet'); print('Quiet hours: off' if not q else f"Quiet hours: {q['from']}-{q['to']} ({q.get('days', 'all')})"); return
    if args[0] == 'off': cfg.pop('quiet', None); save_cfg(cfg); print('Quiet hours: off'); return
    f, t = parse_quiet(args[0]); days = args[1] if len(args) > 1 else 'all'
    if days not in ('all', 'weekdays'): raise NfError("days: 'all' or 'weekdays'")
    cfg['quiet'] = {'from': f, 'to': t, 'days': days}; save_cfg(cfg)
    print(f"Quiet hours: {f}-{t}, {'Monday to Friday' if days == 'weekdays' else 'every day'}")
    if not gate(cfg)[0]: hide_app()

def cmd_share(args):
    cfg = load_cfg()
    if not args: print(f"Hide while sharing the screen: {'on' if cfg.get('pauseOnShare', True) else 'off'}"); return
    if args[0] not in ('on', 'off'): raise NfError("nf share on|off")
    cfg['pauseOnShare'] = args[0] == 'on'; save_cfg(cfg); print(f'Hide while sharing the screen: {args[0]}')

def cmd_gate(args):
    ok, why = gate(); print(why); sys.exit(0 if ok else 1)

COMMANDS = {'pause': cmd_pause, 'resume': cmd_resume, 'status': cmd_status, 'preview': cmd_preview,
            'quiet': cmd_quiet, 'share': cmd_share, 'gate': cmd_gate, '_after_preview': cmd_after_preview}

def main(argv):
    if not argv or argv[0] in ('-h', '--help', 'help'): print(__doc__.split('\n\nWhether')[0]); return 0
    cmd, args = argv[0], argv[1:]
    if cmd == 'clips': return clipsmod.main(args)
    if cmd not in COMMANDS: print(f"nf: unknown command '{cmd}' (nf help)", file=sys.stderr); return 2
    try: COMMANDS[cmd](args)
    except (NfError, clipsmod.ClipsError) as e: print(f'nf: {e}', file=sys.stderr); return 1
    except (KeyboardInterrupt, EOFError): print(); return 1
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
