"""Renders every clip of every theme + all theme-to-theme transitions into the cwd:
clips/<theme>__<clip>/NNN.png, transitions/<a>__<b>/NNN.png, sheet_<theme>_<clip>.png."""
import os, random, shutil, zlib
from engine import *
from themes import load_themes
from transitions import transition

if __name__=='__main__':
    THEMES=load_themes()
    shutil.rmtree('clips',ignore_errors=True); shutil.rmtree('transitions',ignore_errors=True)
    first={}
    for theme,items in THEMES.items():
        for name,n,frame_fn in items:
            random.seed(zlib.crc32(name.encode()))
            frames=[frame_fn(f) for f in range(n)]
            dd=f'clips/{theme}__{name}'; os.makedirs(dd)
            for i,fr in enumerate(frames): fr.save(f'{dd}/{i:03d}.png')
            first.setdefault(theme,frames[0])
            big=[fr.resize((W*2,H*2),Image.NEAREST) for fr in frames]
            sh=Image.new('RGB',(W*4,H*12)); pick=[int(i*(n-1)/11) for i in range(12)]
            for j,i in enumerate(pick): sh.paste(big[i],((j%2)*W*2,(j//2)*H*2))
            sh.save(f'sheet_{theme}_{name}.png'); print(theme,name,n)
    for a in first:
        for b in first:
            if a==b: continue
            dd=f'transitions/{a}__{b}'; os.makedirs(dd)
            for i,fr in enumerate(transition(first[a],first[b])): fr.save(f'{dd}/{i:03d}.png')
    print('transitions ok')
