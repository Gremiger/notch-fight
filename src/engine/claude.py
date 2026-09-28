"""Claude (the protagonist) base sprites + the sprite tools every theme uses to dress him up
(overlay hair/hats, recolour rows) and to derive attack/hurt poses for opponents."""
from .core import *

CL = {
'guard':S([
"...OOOOOOOO....",
"...OOOOOOOO....",
"...OOOOKOOK....",
"...OOOOKOOK.oo.",
"...OOOOOOOOooo.",
".ooOOOOOOOO.oo.",
"ooOOOOOOOOO....",
"...OOOOOOOO....",
"...oOOOOOOo....",
"..oo.....oo....",
".oo.......oo...",]),
'guard2':S([
"...............",
"...OOOOOOOO....",
"...OOOOOOOO....",
"...OOOOKOOK.oo.",
"...OOOOKOOKooo.",
".ooOOOOOOOO.oo.",
"ooOOOOOOOOO....",
"...OOOOOOOO....",
"...oOOOOOOo....",
"..oo.....oo....",
".oo.......oo...",]),
'punch':S([
"...OOOOOOOO......",
"...OOOOOOOO......",
"...OOOOKOOK......",
"...OOOOKOOK......",
"...OOOOOOOO......",
".ooOOOOOOOOooooOO",
"ooOOOOOOOOOooooOO",
"...OOOOOOOO......",
"...oOOOOOOo......",
"..oo.....oo......",
".oo........oo....",]),
'dash':S([
"....OOOOOOOO.....",
"....OOOOOOOO.....",
"...OOOOOKOOK.....",
"...OOOOOKOOK.....",
"...OOOOOOOO......",
"ooOOOOOOOOOooooOO",
".ooOOOOOOOOooooOO",
"...OOOOOOOO......",
"..oOOOOOOo.......",
"oooo..oo.........",
"......oo.........",]),
'hurt':S([
"oo...............",
".oo.OOOOOOOO..oo.",
"...OOOOOOOO..oo..",
"...OKKOOKKOOOo...",
"...OOOOOOOO......",
"...OOOOOOOO......",
"...OOOOOOOO......",
"...OOOOOOOO......",
"...oOOOOOOo......",
"....oo..oo.......",
"...oo....oo......",]),
'armsup':S([
".oo........oo.",
".oo........oo.",
"..oOOOOOOOOo..",
"...OOOOOOOO...",
"...OOOOKOOK...",
"...OOOOKOOK...",
"...OOOOOOOO...",
"...OOOOOOOO...",
"...oOOOOOOo...",
"...oo....oo...",
"..ooo....ooo..",]),
'charge':S([
"...OOOOOOOO.....",
"...OOOOOOOO.....",
"...OOOOKOOK.....",
"...OOOOKOOK.....",
"...OOOOOOOO.....",
"...OOOOOOOOooooo",
"...OOOOOOOOooooo",
"...OOOOOOOO.....",
"...oOOOOOOo.....",
"..oo......oo....",
".oo........oo...",]),
}

def grid(spr): return [list(r) for r in spr]
def ungrid(g): return S([''.join(r) for r in g])

def body_box(spr):
    """Top row + column span of Claude's body (first row with >=6 'O')."""
    for y,r in enumerate(spr):
        if r.count('O')>=6:
            xs=[x for x,c in enumerate(r) if c=='O']; return y,min(xs),max(xs)
    return 0,3,10

def overlay(spr, pat, dx, dy_bottom, bangs=None):
    """Paint `pat` so its last row sits just above the body top (padding upward)."""
    top,l,r=body_box(spr); g=grid(spr); w=len(g[0])
    y0=top-len(pat)
    pad=max(0,-y0)
    if pad: g=[['.']*w for _ in range(pad)]+g; top+=pad; y0+=pad
    for j,row in enumerate(pat):
        for i,ch in enumerate(row):
            x=l+dx+i
            if ch!='.' and 0<=x<w: g[y0+j][x]=ch
    if bangs:
        for i,ch in enumerate(bangs):
            x=l+dx+i
            if ch!='.' and 0<=x<w and g[top][x]!='.': g[top][x]=ch
    return ungrid(g)

def recolor_rows(spr, rows_fn):
    g=grid(spr); top,l,r=body_box(spr)
    for y in range(len(g)):
        for x in range(len(g[0])):
            n=rows_fn(x,y,top,l,r,g[y][x])
            if n: g[y][x]=n
    return ungrid(g)

def variant(fn): return {k:fn(v) for k,v in CL.items()}

def attack(spr,row,ext,col):
    g=[r for r in spr]
    for rr in (row,row+1):
        L=max(i for i,c in enumerate(g[rr]) if c!='.')
        g[rr]=g[rr][:L+1]+col*ext
    return S(g)
def hurt(spr):
    h=len(spr); out=[]
    for i,r in enumerate(spr):
        s=round((h-1-i)/(h-1)*2); out.append(r[s:]+'.'*s)
    return S(out)
def poses(idle,row,col,ext=4):
    return {'idle':idle,'attack':attack(idle,row,ext,col),'hurt':hurt(idle)}

def guard_pose(f): return 'guard' if (f//6)%2==0 else 'guard2'
