"""Canvas constants and low-level pixel drawing (sprites with auto outline + aura, sparks, orbs)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter
from .palette import PAL

W,H,FPS,N = 185,64,20,200   # 185pt = MacBookPro18,3 notch width; 1 art px = 1pt = 2 device px
GROUND = 58
random.seed(7)
OUT = (18,12,16)

def S(rows): 
    w = max(len(r) for r in rows); return [r.ljust(w,'.') for r in rows]

def mask_of(spr,flip):
    h=len(spr); w=len(spr[0]); out={}
    for y,row in enumerate(spr):
        for x,ch in enumerate(row):
            if ch!='.': out[((w-1-x) if flip else x, y)] = ch
    return out,w,h

def dilate(pts,r):
    s=set()
    for (x,y) in pts:
        for dx in range(-r,r+1):
            for dy in range(-r,r+1):
                if abs(dx)+abs(dy)<=r+ (1 if r>1 else 0): s.add((x+dx,y+dy))
    return s

def blend(px,x,y,c,a):
    if 0<=x<W and 0<=y<H:
        o=px[x,y]; px[x,y]=tuple(int(o[i]*(1-a)+c[i]*a) for i in range(3))

def draw(im,spr,cx,feet,flip,aura=None,alpha=1.0,tint=None,f=0,pal=None):
    px=im.load(); m,w,h=mask_of(spr,flip)
    ox=int(round(cx-w/2)); oy=int(round(feet-h))
    pts=set(m)
    if aura:
        col,r=aura
        ring=dilate(pts,r)-pts
        for (x,y) in ring:
            if (x*3+y*5+f)%4!=0 or r<=1:
                a=0.55 if (x+y+f)%3 else 0.85
                blend(px,ox+x,oy+y,col,a)
        # flame tips upward
        for (x,y) in list(ring):
            if (x*7+f*3)%5==0: 
                for k in range(1,3+(f+x)%3): blend(px,ox+x,oy+y-k-r,col,0.5)
    for (x,y) in dilate(pts,1)-pts:
        blend(px,ox+x,oy+y,OUT if not tint else tint,alpha)
    for (x,y),ch in m.items():
        c=(pal or {}).get(ch) or PAL[ch]
        if tint: c=tint
        blend(px,ox+x,oy+y,c,alpha)
    return ox,oy,w,h

def spark(d,x,y,s,c=(255,240,120)):
    d.line([x-s,y,x+s,y],fill=c); d.line([x,y-s,x,y+s],fill=c)
    d.line([x-s//2,y-s//2,x+s//2,y+s//2],fill=(255,255,255)); d.line([x-s//2,y+s//2,x+s//2,y-s//2],fill=(255,255,255))
    d.rectangle([x-1,y-1,x+1,y+1],fill=(255,255,255))

def ball(d,x,y,r,outer,mid,f):
    r2 = r + (f%2)
    d.ellipse([x-r2-1,y-r2-1,x+r2+1,y+r2+1],fill=outer)
    d.ellipse([x-r2,y-r2,x+r2,y+r2],fill=mid)
    rc=max(1,r2//2); d.ellipse([x-rc,y-rc,x+rc,y+rc],fill=(255,255,255))

def asterisk(d,x,y,r,c,f):
    for k in range(8):
        a=k*math.pi/4 + f*0.15
        L = r if k%2==0 else r*0.6
        d.line([x,y,x+math.cos(a)*L,y+math.sin(a)*L],fill=c)

def lerp(a,b,t): return a+(b-a)*max(0,min(1,t))
def ease(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def rshake(n=1): return (random.choice([-n,n]),random.choice([-1,0,1]))
def ez(a,b,t): return lerp(a,b,ease(t))
