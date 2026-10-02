"""Sprite-grid transforms and sprite geometry (same maths as core.draw)."""
from .core import *

def rotate90(spr,k=1,trim=False):
    """Rotate a sprite grid 90 degrees clockwise k times (k=3: counter-clockwise).
    trim=True first drops fully empty columns (so the rotated sprite has no empty rows)."""
    if trim:
        cols=[i for i in range(len(spr[0])) if any(r[i]!='.' for r in spr)]
        spr=[''.join(r[i] for i in cols) for r in spr]
    g=[list(r) for r in spr]
    for _ in range(k%4): g=[list(r) for r in zip(*g[::-1])]
    return S([''.join(r) for r in g])

def paint(spr,items,top=0,right=0,bottom=0,left=0,grow=False):
    """Pad a sprite grid and paint items=[(x,y,chars)] (chars: a string, '.' = keep) in the ORIGINAL
    coordinates. grow=True computes the padding: rows on top for negative y, and the same number
    of columns on both sides for x past the right edge (so the sprite stays centred)."""
    if grow:
        top=max(0,-min(y for _,y,_ in items))
        right=left=max(0,max(x+len(ch)-1 for x,_,ch in items)-(len(spr[0])-1))
    w=len(spr[0])+right; row=lambda r: list('.'*left+r.ljust(w,'.'))
    g=[row('') for _ in range(top)]+[row(r) for r in spr]+[row('') for _ in range(bottom)]
    for x,y,chars in items:
        for i,ch in enumerate(chars):
            if ch!='.': g[y+top][x+left+i]=ch
    return S([''.join(r) for r in g])

def origin(spr,cx,feet=GROUND):
    """Top-left world position where draw() puts spr (flip does not move it)."""
    return int(round(cx-len(spr[0])/2)),int(round(feet-len(spr)))

def hand_at(spr,cx,feet,flip,hx,hy,h=None):
    """World position of sprite cell (hx,hy), mirrored when flip. h = the pose's original height
    when the sprite was padded on top (y is measured from the feet). y is NOT rounded (pass int feet)."""
    w=len(spr[0]); h=h or len(spr); ox=int(round(cx-w/2))
    return (ox+(w-1-hx) if flip else ox+hx), feet-h+hy

def sprite_img(spr, pal, scale=1):
    """The sprite (with the same 1px dark outline core.draw gives it) as an RGBA image, for the
    cards and close-ups that scale or rotate it. Chars missing from pal fall back to PAL."""
    m, w, h = mask_of(spr, False)
    im = Image.new('RGBA', (w+2, h+2), (0,0,0,0)); px = im.load()
    for x, y in dilate(set(m), 1): px[x+1, y+1] = OUT+(255,)
    for (x, y), ch in m.items(): px[x+1, y+1] = ((pal or {}).get(ch) or PAL[ch])+(255,)
    return im.resize((im.width*scale, im.height*scale), Image.NEAREST) if scale > 1 else im

def paste_feet(im, spr_im, cx, feet):
    """Paste a sprite_img centred at cx with its bottom row on feet."""
    im.paste(spr_im, (int(cx-spr_im.width/2), int(feet-spr_im.height)), spr_im)
