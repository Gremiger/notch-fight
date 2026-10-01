"""Renders every clip of every theme + all theme-to-theme transitions into the cwd:
clips/<theme>__<clip>/NNN.png, transitions/<a>__<b>/NNN.png, sheet_<theme>_<clip>.png.

ONLY=<theme|theme__clip>[,...] renders just those clips and the transitions to and from their themes,
leaving the rest of the cwd as it is (it needs a full build first). Either way `.built` lists the clips
rendered by this run (build.sh makes GIFs for those)."""
import os, random, shutil, sys, zlib
from engine import *
from themes import load_themes
from transitions import transition

def selected(themes, only):
    """(theme, clip) pairs named by ONLY; exits listing the known names on a typo."""
    known={f'{t}__{c[0]}' for t,items in themes.items() for c in items}
    picked=[]
    for name in only:
        hits=[(t,c) for t,items in themes.items() for c in items if name in (t,f'{t}__{c[0]}')]
        if not hits: sys.exit(f"unknown theme or clip '{name}'. Known: {', '.join(sorted(known|set(themes)))}")
        picked+=[h for h in hits if h not in picked]
    return picked

def render_clip(theme, name, n, frame_fn, off):
    random.seed(zlib.crc32(name.encode()))
    frames=[frame_fn(f) for f in range(n)]
    dd=f'clips/{theme}__{name}'; shutil.rmtree(dd,ignore_errors=True); os.makedirs(dd)
    for i,fr in enumerate(frames): fr.save(f'{dd}/{i:03d}.png')
    if off: open(f'{dd}/.default-off','w').close()   # shipped off: ./clips.sh and the app read this
    big=[fr.resize((W*2,H*2),Image.NEAREST) for fr in frames]
    sh=Image.new('RGB',(W*4,H*12)); pick=[int(i*(n-1)/11) for i in range(12)]
    for j,i in enumerate(pick): sh.paste(big[i],((j%2)*W*2,(j//2)*H*2))
    sh.save(f'sheet_{theme}_{name}.png'); print(theme,name,n)
    return frames[0]

if __name__=='__main__':
    THEMES=load_themes()
    only=[n for n in os.environ.get('ONLY','').split(',') if n]
    if only and not os.path.isdir('clips'): sys.exit('ONLY needs an existing build: run a full build first (./build.sh)')
    todo=selected(THEMES,only) if only else [(t,c) for t,items in THEMES.items() for c in items]
    if not only: shutil.rmtree('clips',ignore_errors=True); shutil.rmtree('transitions',ignore_errors=True)
    first={}
    for theme,(name,n,frame_fn,off) in todo:
        fr=render_clip(theme,name,n,frame_fn,off)
        if name==THEMES[theme][0][0]: first[theme]=fr          # a theme's keyframe: its first clip's first frame
    rebuilt={t for t,_ in todo}
    for theme,items in THEMES.items():                           # the other themes' keyframes, from the last build
        if theme not in first:
            path=f'clips/{theme}__{items[0][0]}/000.png'
            if not os.path.exists(path): sys.exit(f'{path} is missing: run a full build first (./build.sh)')
            first[theme]=Image.open(path).convert('RGB')
    for a in first:
        for b in first:
            if a==b or not ({a,b}&rebuilt): continue
            dd=f'transitions/{a}__{b}'; shutil.rmtree(dd,ignore_errors=True); os.makedirs(dd)
            for i,fr in enumerate(transition(first[a],first[b])): fr.save(f'{dd}/{i:03d}.png')
    open('.built','w').write('\n'.join(f'{t}__{c[0]}' for t,c in todo)+'\n')
    print('transitions ok')
