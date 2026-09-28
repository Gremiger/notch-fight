"""Add/remove the Notch Fight hooks in ~/.claude/settings.json (idempotent, keeps a backup).

    python3 scripts/hooks.py install <path/to/NotchFight.app>
    python3 scripts/hooks.py uninstall
"""
import json, os, shlex, shutil, sys, time

SETTINGS = os.path.expanduser('~/.claude/settings.json')
MARK = 'NotchFight'   # every hook command we own mentions the app name

def load():
    if not os.path.exists(SETTINGS): return {}
    with open(SETTINGS) as fh: return json.load(fh)

def strip(settings):
    """Remove every hook entry that references NotchFight; drop groups left empty."""
    hooks = settings.get('hooks', {})
    for event in list(hooks):
        groups = []
        for g in hooks[event]:
            kept = [h for h in g.get('hooks', []) if MARK not in h.get('command', '')]
            if kept: groups.append(dict(g, hooks=kept))
        if groups: hooks[event] = groups
        else: del hooks[event]
    return settings

def save(settings):
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    if os.path.exists(SETTINGS):
        backup = f'{SETTINGS}.bak-notchfight-{time.strftime("%Y%m%d-%H%M%S")}'
        shutil.copy2(SETTINGS, backup); print(f'backup: {backup}')
    tmp = SETTINGS + '.tmp'
    with open(tmp, 'w') as fh: json.dump(settings, fh, indent=2); fh.write('\n')
    os.replace(tmp, SETTINGS)

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('install', 'uninstall'): sys.exit(__doc__)
    settings = strip(load())
    if sys.argv[1] == 'install':
        app = os.path.abspath(sys.argv[2])
        start = f'open -g {shlex.quote(app)} >/dev/null 2>&1 || true'
        stop = 'pkill -x NotchFight >/dev/null 2>&1 || true'
        hooks = settings.setdefault('hooks', {})
        hooks.setdefault('UserPromptSubmit', []).append({'hooks': [{'type': 'command', 'command': start, 'timeout': 5}]})
        for ev in ('Stop', 'StopFailure'):
            hooks.setdefault(ev, []).append({'hooks': [{'type': 'command', 'command': stop, 'timeout': 5}]})
        print(f'hooks installed -> {app}')
    else:
        print('hooks removed')
    save(settings)

if __name__ == '__main__':
    main()
