import math, random
from PIL import Image, ImageDraw
W,H,FPS,N = 185,64,20,200   # 185pt = MacBookPro18,3 notch width; 1 art px = 1pt = 2 device px
GROUND = 58
random.seed(7)

PAL = {
 'O':(217,119,87),'o':(168,80,54),'K':(24,14,12),
 'G':(112,192,84),'g':(52,118,44),'S':(24,34,24),'P':(236,226,206),'U':(146,72,168),
 'B':(38,32,48),'e':(236,64,128),'w':(78,150,66),
}
OUT = (18,12,16)

def S(rows): 
    w = max(len(r) for r in rows); return [r.ljust(w,'.') for r in rows]

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
CE = {
'idle':S([
"......g.g.......",
".....gGgGg......",
"....gGSGGSg.....",
"....GGGGGGG.....",
"....GPPPPPG.....",
"....GPPePPe.....",
"....UPPPPPU.....",
".....PPPPP......",
".w..GGSGGSGG....",
"ww.GGGBBBBGGG...",
"wwGGgGGGGGGgGG..",
"wwGGPPGGGGPPGG..",
".wG.BBBBBBBB.G..",
".w...BBGGBB.....",
"..w..GGGGGG.....",
".....SGGSGG.....",
".....GG..GG.....",
".....BB..BB.....",
".....BB..BB.....",
".....GS..GS.....",
".....GG...GG....",
"....PPP...PPP...",]),
'guard':S([
"......g.g.......",
".....gGgGg......",
"....gGSGGSg.....",
"....GGGGGGG.PP..",
"....GPPPPPG.GG..",
"....GPPePPe.GG..",
"....UPPPPPU.G...",
".....PPPPP.GG...",
".w..GGSGGSGG....",
"ww.GGGBBBBGG....",
"wwGGgBBBBBB.....",
"wwGG.BBBBBB.....",
".wGG.BBGGBB.....",
".wPP.BBBBBB.....",
"..w..GGGGGG.....",
".....SGGSGG.....",
".....GG..GG.....",
"....BB....BB....",
"....BB....BB....",
"...GS......GS...",
"...GG......GG...",
"..PPP......PPP..",]),
'punch':S([
"......g.g...........",
".....gGgGg..........",
"....gGSGGSg.........",
"....GGGGGGG.........",
"....GPPPPPG.........",
"....GPPePPe.........",
"....UPPPPPU.........",
".....PPPPP..........",
".w..GGSGGSGG........",
"ww.GGGBBBBGGGGGGGPP.",
"wwGGgBBBBBBgGGGGGPP.",
"wwGG.BBBBBB.........",
".wGG.BBGGBB.........",
".wPP.BBBBBB.........",
"..w..GGGGGG.........",
".....SGGSGG.........",
"....GG....GG........",
"...BB......BB.......",
"..BB........BB......",
"..GS........GS......",
".GG..........GG.....",
"PPP...........PPP...",]),
'hurt':S([
"...g.g..........",
"..gGgGg.........",
".gGSGGSg........",
".GGGGGGG........",
".GPPPPPG........",
".GPKKPKK........",
".UPPPPPU...PP...",
"..PPPPP...GG....",
".w.GGSGGSGG.....",
"wwGGGBBBBGGG....",
"wwGgBBBBBBgG....",
"wwG.BBBBBB......",
".w..BBGGBB......",
".w..BBBBBB......",
"..w.GGGGGG......",
"....SGGSGG......",
".....GG..GG.....",
".....BB...BB....",
"....BB.....BB...",
"....GS.....GS...",
"...GG.......GG..",
"..PPP.......PPP.",]),
'charge':S([
"......g.g.........",
".....gGgGg........",
"....gGSGGSg.......",
"....GGGGGGG.......",
"....GPPPPPG.......",
"....GPPePPe.......",
"....UPPPPPU.......",
".....PPPPP........",
".w..GGSGGSGG......",
"ww.GGGBBBBGGGG....",
"wwGGgBBBBBBgGGGPP.",
"wwGG.BBBBBB..GGPP.",
".wGG.BBGGBB.......",
".w...BBBBBB.......",
"..w..GGGGGG.......",
".....SGGSGG.......",
"....GG....GG......",
"...BB......BB.....",
"..BB........BB....",
"..GS........GS....",
".GG..........GG...",
"PPP...........PPP.",]),
}

def bg():
    im = Image.new('RGB',(W,H)); px = im.load()
    for y in range(H):
        for x in range(W):
            if y < 46:
                t = y/46; c = (int(96+100*t),int(150+75*t),int(222+18*t))
                # dither band
                if (x+y)%2==0 and int(t*8)!=int((y+1)/46*8): c=tuple(v+6 for v in c)
                px[x,y]=c
            else:
                t=(y-46)/18; c=(int(206-30*t),int(172-30*t),int(118-26*t))
                if (x*7+y*13)%23==0: c=(150,120,84)
                px[x,y]=c
    d = ImageDraw.Draw(im)
    # clouds
    for cx,cy,r in [(20,8,5),(27,7,6),(34,9,4),(120,5,4),(127,4,6),(135,6,4),(160,14,3),(165,13,4)]:
        d.ellipse([cx-r,cy-r//2,cx+r,cy+r//2],fill=(236,244,250))
    # mesas
    for x0,x1,top,col in [(-5,30,30,(172,128,100)),(40,62,36,(160,118,92)),(95,130,28,(172,128,100)),(150,190,34,(160,118,92)),(70,85,40,(150,110,86))]:
        d.rectangle([x0,top,x1,47],fill=col); d.rectangle([x0,top,x1,top],fill=(196,152,120))
        d.rectangle([x0+2,top+4,x0+3,47],fill=tuple(v-20 for v in col))
    d.rectangle([0,46,W,46],fill=(150,112,80))
    for x,y in [(12,52),(60,55),(110,51),(170,54),(88,61)]:
        d.rectangle([x,y,x+3,y+1],fill=(140,108,76)); d.point((x+1,y-1),fill=(170,136,100))
    return im
import sys
BLACK = True
def bg_black():
    im = Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    for x in range(0,W,2):
        a=1-abs(x-W/2)/(W/2)
        v=int(10+26*a); d.point((x,GROUND+1),fill=(v,v,v+4))
    return im
BG = bg_black() if BLACK else bg()

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

CL_OR=((255,196,140),(232,120,80))   # claude beam outer/mid
CE_BL=((140,210,255),(60,140,255))   # cell kamehameha

def lerp(a,b,t): return a+(b-a)*max(0,min(1,t))
def ease(t): t=max(0,min(1,t)); return t*t*(3-2*t)

def frame(f):
    im=BG.copy(); d=ImageDraw.Draw(im)
    shake=(0,0); flash=0.0
    clx,cly,clp = 30,GROUND,'guard'
    cex,cey,cep = 150,GROUND,'idle'
    claura=ceaura=None; after=[]; fx=[]
    bob = 1 if (f//6)%2 else 0
    AUR_C=(255,210,90); AUR_E=(190,255,150)
    if f<30:                       # stare-down / power-up
        clp='guard' if bob==0 else 'guard2'
        if f>=12: claura=(AUR_C,1 if f<22 else 2); ceaura=(AUR_E,1 if f<22 else 2)
        if f>=20: cep='guard'
    elif f<40:                     # dash
        t=ease((f-30)/10); clx=lerp(30,82,t); cex=lerp(150,104,t)
        clp='dash'; cep='punch'; claura=(AUR_C,2); ceaura=(AUR_E,2)
        after=[('cl',clx-6,clp),('cl',clx-12,clp),('ce',cex+7,cep),('ce',cex+14,cep)]
        for i in range(6):
            y=random.randint(30,60); x=random.randint(0,W-20); d.line([x,y,x+random.randint(8,20),y],fill=(250,250,250))
    elif f<90:                     # flurry, partly airborne
        k=(f-40)
        air = 0
        if 52<=f<80: air = int(14*math.sin(math.pi*(f-52)/28))
        clx=82+random.choice([-1,0,1]); cex=104+random.choice([-1,0,1])
        cly=cey=GROUND-air
        ph=(k//3)%4
        clp=['punch','guard','hurt','punch'][ph]; cep=['hurt','punch','punch','guard'][ph]
        if ph==2: cex-=2
        claura=(AUR_C,1+(f%2)); ceaura=(AUR_E,1+(f%2))
        if k%3==0:
            sy=cly-6+random.randint(-3,3); sx=93+random.randint(-2,2)
            fx.append(('spark',sx,sy,4+random.randint(0,2))); shake=(random.choice([-1,1]),random.choice([-1,0,1]))
        if f==40: flash=0.7; boomx=93; fx.append(('spark',93,GROUND-8,8))
    elif f<104:                    # Cell knocks Claude back
        t=ease((f-90)/10)
        clx=lerp(82,32,t); clp='hurt'; cep='punch' if f<96 else 'guard'
        cex=lerp(104,150,ease((f-94)/10)); cly=GROUND-int(6*math.sin(math.pi*min(1,(f-90)/10)))
        ceaura=(AUR_E,2)
        if f==90: fx.append(('spark',92,GROUND-8,9)); shake=(2,1); flash=0.4; boomx=92
        if f>=97: 
            for i in range(3): fx.append(('dust',clx-6+random.randint(-3,3),GROUND-random.randint(0,3)))
        after=[('cl',clx+6,'hurt')] if f<100 else []
    elif f<130:                    # charge beams
        t=(f-104)/26
        clx,cex=32,150; clp='charge'; cep='charge'
        claura=(AUR_C,2+(f%3==0)); ceaura=(AUR_E,2+(f%3==0))
        r=int(1+4*t)
        fx.append(('clball',clx+9,GROUND-6,r)); fx.append(('ceball',cex-10,GROUND-11,r))
        if f%4==0:
            for i in range(2): fx.append(('rock',random.randint(10,175),GROUND-random.randint(0,int(20*t))))
        if f>=118: shake=(random.choice([-1,0,1]),0)
    elif f<172:                    # beam struggle
        clx,cex=32,150; clp='charge'; cep='charge'
        claura=(AUR_C,3); ceaura=(AUR_E,3)
        t=(f-130)
        mid = 92 + 10*math.sin(t*0.35) + (lerp(0,26,(f-158)/12) if f>158 else 0)
        mid=int(mid)
        fx.append(('beam',clx+9,mid,GROUND-6,CL_OR,f,True))
        fx.append(('beam',mid,cex-10,GROUND-11,CE_BL,f,False))
        fx.append(('clash',mid,GROUND-8,f))
        shake=(random.choice([-2,-1,1,2]),random.choice([-1,0,1]))
        if f%2==0: fx.append(('rock',random.randint(mid-30,mid+30),GROUND-random.randint(0,25)))
    elif f<182:                    # explosion
        t=(f-172)/10
        clx,cex=32,150; clp='charge'; cep='charge'
        fx.append(('boom',120,GROUND-10,int(6+70*t)))
        boomx=120; flash = 1.0 if f<177 else lerp(1,0.35,(f-177)/5)
        shake=(random.choice([-2,2]),random.choice([-1,1]))
    else:                          # reset to stare-down (loops into f=0)
        t=(f-182)/18
        clp='guard' if bob==0 else 'guard2'; cep='guard' if f<190 else 'idle'
        boomx=120; flash = lerp(0.35,0,t*2)
        if f<192:
            for i in range(2): fx.append(('dust',random.randint(80,150),GROUND-random.randint(0,6)))

    # afterimages
    for who,x,p in after:
        if who=='cl': draw(im,CL[p],x,cly,False,alpha=0.35,tint=(255,220,190))
        else: draw(im,CE[p],x,cey,True,alpha=0.35,tint=(210,255,200))
    # beams under characters' hands
    for e in fx:
        if e[0]=='beam':
            _,x0,x1,y,(oc,mc),ff,isc = e
            wob=(ff%2)
            d.rectangle([x0,y-3-wob,x1,y+3+wob],fill=oc); d.rectangle([x0,y-2,x1,y+2],fill=mc); d.rectangle([x0,y-1+wob,x1,y],fill=(255,255,255))
            for i in range(3):
                xx=random.randint(min(x0,x1),max(x0,x1)); d.point((xx,y-4-wob),fill=oc); d.point((xx,y+4+wob),fill=oc)
    draw(im,CL[clp],clx,cly,False,aura=claura,f=f)
    draw(im,CE[cep],cex,cey,True,aura=ceaura,f=f)
    for e in fx:
        k=e[0]
        if k=='spark': spark(d,e[1],e[2],e[3])
        elif k=='dust': d.rectangle([e[1],e[2],e[1]+1,e[2]+1],fill=(222,196,150))
        elif k=='rock': d.rectangle([e[1],e[2],e[1]+1,e[2]+1],fill=(120,92,66))
        elif k=='clball': ball(d,e[1],e[2],e[3],*CL_OR,f); asterisk(d,e[1],e[2],e[3]+3,(255,150,100),f)
        elif k=='ceball': ball(d,e[1],e[2],e[3],*CE_BL,f)
        elif k=='clash':
            x,y,ff=e[1],e[2],e[3]; r=6+(ff%3)
            d.ellipse([x-r-2,y-r-2,x+r+2,y+r+2],fill=(255,236,170)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255))
            asterisk(d,x,y,r+5,(255,200,120),ff)
            for i in range(4):
                a=random.random()*6.28; L=random.randint(r+2,r+10); d.point((int(x+math.cos(a)*L),int(y+math.sin(a)*L)),fill=(255,255,200))
        elif k=='boom':
            x,y,r=e[1],e[2],e[3]
            d.ellipse([x-r-3,y-r-3,x+r+3,y+r+3],outline=(255,210,120),width=3)
            d.ellipse([x-r//2,y-r//2,x+r//2,y+r//2],fill=(255,255,255))
    if shake!=(0,0):
        im2=Image.new('RGB',(W,H),(0,0,0)); im2.paste(im,shake); 
        # fill exposed edge with original to avoid black bars
        base=im.copy(); base.paste(im2.crop((0,0,W,H)),(0,0)); im=im2
        px=im.load(); src=BG.load()
        for x in range(W):
            for y in range(H):
                if px[x,y]==(0,0,0): px[x,y]=src[x,y]
    if flash>0:
        if BLACK:
            from PIL import ImageFilter
            m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); r=int(20+90*flash)
            cx=boomx if 'boomx' in dir() else 93
            md.ellipse([cx-r,GROUND-10-r//2,cx+r,GROUND-10+r//2],fill=int(255*flash))
            m=m.filter(ImageFilter.GaussianBlur(8))
            im=Image.composite(Image.new('RGB',(W,H),(255,250,235)),im,m)
        else:
            im=Image.blend(im,Image.new('RGB',(W,H),(255,255,255)),flash)
    return im


# ---------------------------------------------------------------------------
# Multi-clip system. Every clip starts AND ends in the NEUTRAL stance
# (Claude guard at x=30, Cell arms-crossed at x=150, no aura, no fx), so any
# clip can follow any other seamlessly and the app can shuffle them.
# ---------------------------------------------------------------------------
AUR_C=(255,210,90); AUR_E=(190,255,150)
GOLD={'O':(255,214,90),'o':(210,156,40)}
GOLD_AURA=(255,244,150)

def base(f):
    cl=dict(x=30,y=GROUND,pose='guard' if (f//6)%2==0 else 'guard2',flip=False,aura=None,pal=None,vis=True)
    ce=dict(x=150,y=GROUND,pose='idle',flip=True,aura=None,pal=None,vis=True)
    return dict(cl=cl,ce=ce,after=[],under=[],fx=[],shake=(0,0),flash=0.0,fc=(93,GROUND-10))

def rshake(n=1): return (random.choice([-n,n]),random.choice([-1,0,1]))
def ez(a,b,t): return lerp(a,b,ease(t))

def render(s,f):
    im=BG.copy(); d=ImageDraw.Draw(im)
    for who,x,y,p,fl,tint in s['after']:
        draw(im,(CL if who=='cl' else CE)[p],x,y,fl,alpha=0.35,tint=tint)
    for e in s['under']: fxdraw(d,e,f)
    for who in ('cl','ce'):
        c=s[who]
        if c['vis']: draw(im,(CL if who=='cl' else CE)[c['pose']],c['x'],c['y'],c['flip'],aura=c['aura'],f=f,pal=c['pal'])
    for e in s['fx']: fxdraw(d,e,f)
    if s['shake']!=(0,0):
        im2=BG.copy(); im2.paste(im,s['shake']); im=im2
    if s['flash']>0:
        from PIL import ImageFilter
        m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); r=int(20+90*s['flash']); cx,cy=s['fc']
        md.ellipse([cx-r,cy-r//2,cx+r,cy+r//2],fill=int(255*min(1,s['flash'])))
        m=m.filter(ImageFilter.GaussianBlur(8))
        im=Image.composite(Image.new('RGB',(W,H),(255,250,235)),im,m)
    return im

def fxdraw(d,e,f):
    k=e[0]
    if k=='spark': spark(d,int(e[1]),int(e[2]),e[3])
    elif k=='dust': d.rectangle([e[1],e[2],e[1]+1,e[2]+1],fill=(150,130,100))
    elif k=='rock': d.rectangle([e[1],e[2],e[1]+1,e[2]+1],fill=(120,92,66))
    elif k=='zip':
        x,y=int(e[1]),int(e[2])
        for i in range(3):
            yy=y+random.randint(-8,2); xx=x+random.randint(-6,6); d.line([xx-4,yy,xx+4,yy],fill=(235,235,255))
    elif k=='orb':   # small ki blast
        x,y,c=int(e[1]),int(e[2]),e[3]
        d.ellipse([x-2,y-2,x+2,y+2],fill=c[0]); d.rectangle([x-1,y-1,x,y],fill=(255,255,255))
        d.line([x-6*e[4],y,x-2*e[4],y],fill=c[1])
    elif k=='ring':
        x,y,r,c=int(e[1]),int(e[2]),int(e[3]),e[4]
        d.ellipse([x-r,y-r//2,x+r,y+r//2],outline=c,width=1)
        if r<5: d.ellipse([x-2,y-2,x+2,y+1],fill=(255,240,200))
    elif k=='smoke':
        x,y,r,c=int(e[1]),int(e[2]),int(e[3]),e[4]
        d.ellipse([x-r,y-r,x+r,y+r],fill=c)
    elif k=='bolt':
        x,y=e[1],e[2]; pts=[(x,y)]
        for i in range(4): x+=random.randint(-3,3); y+=random.randint(2,4); pts.append((x,y))
        d.line(pts,fill=(210,245,255)); d.line(pts[:2],fill=(255,255,255))
    elif k=='mote': d.point((int(e[1]),int(e[2])),fill=e[3])
    elif k=='clball': ball(d,int(e[1]),int(e[2]),int(e[3]),*CL_OR,f); asterisk(d,int(e[1]),int(e[2]),int(e[3])+3,(255,150,100),f)
    elif k=='ceball': ball(d,int(e[1]),int(e[2]),int(e[3]),*CE_BL,f)
    elif k=='genki':
        x,y,r=int(e[1]),int(e[2]),int(e[3])
        d.ellipse([x-r-2,y-r-2,x+r+2,y+r+2],fill=(255,170,110)); d.ellipse([x-r,y-r,x+r,y+r],fill=(240,130,85))
        d.ellipse([x-r+2,y-r+2,x+r//2,y+r//2],fill=(255,210,160)); d.ellipse([x-r//3-1,y-r//3-1,x,y],fill=(255,255,255))
        asterisk(d,x,y,r+6,(255,190,130),f)
    elif k=='beam':
        _,x0,x1,y,(oc,mc)=e; x0,x1,y=int(x0),int(x1),int(y); wob=f%2
        d.rectangle([x0,y-3-wob,x1,y+3+wob],fill=oc); d.rectangle([x0,y-2,x1,y+2],fill=mc); d.rectangle([x0,y-1+wob,x1,y],fill=(255,255,255))
    elif k=='boom':
        x,y,r=int(e[1]),int(e[2]),int(e[3])
        d.ellipse([x-r-3,y-r-3,x+r+3,y+r+3],outline=(255,210,120),width=3); d.ellipse([x-r//2,y-r//2,x+r//2,y+r//2],fill=(255,255,255))
    elif k=='twinkle':
        x,y,s=int(e[1]),int(e[2]),e[3]; d.line([x-s,y,x+s,y],fill=(255,255,255)); d.line([x,y-s,x,y+s],fill=(255,255,255))

def calm_aura(s,f,t0,t1,who=('cl','ce')):
    """Aura on between t0..t1, so clip edges stay aura-free."""
    if t0<=f<t1:
        if 'cl' in who: s['cl']['aura']=(AUR_C,1+(f%2))
        if 'ce' in who: s['ce']['aura']=(AUR_E,1+(f%2))

# --- clip: instant-transmission zig-zag across the sky ---------------------
SPOTS=[(62,40,0),(128,28,1),(96,50,0),(44,26,1),(146,44,0),(100,32,1)]
def clip_teleport(f):
    s=base(f); cl,ce=s['cl'],s['ce']; calm_aura(s,f,8,110)
    if 12<=f<18:
        cl['vis']=ce['vis']=(f%2==0 and f<16)
        if f>=14: s['fx']+= [('zip',30,GROUND-4),('zip',150,GROUND-10)]
    elif 18<=f<84:
        i=(f-18)//11; k=(f-18)%11; x,y,side=SPOTS[i]
        if k<2 or k>=9:
            cl['vis']=ce['vis']=False; s['fx'].append(('zip',x,y))
        else:
            cl.update(x=x-8 if side==0 else x+8,y=y,flip=(side==1))
            ce.update(x=x+10 if side==0 else x-10,y=y+6,flip=(side==0))
            if k<5: cl['pose'],ce['pose']='punch','hurt'
            elif k<7: cl['pose'],ce['pose']='hurt','punch'
            else: cl['pose'],ce['pose']='punch','punch'
            if k in (3,5,7): s['fx'].append(('spark',x+random.randint(-1,1),y-7,5)); s['shake']=rshake()
    elif 84<=f<96:
        k=f-84
        if k<3:
            cl.update(x=84,pose='punch'); ce.update(x=102,pose='punch')
            if k==0: s['fx'].append(('spark',93,GROUND-8,9)); s['flash']=0.5; s['fc']=(93,GROUND-8)
            s['shake']=rshake(2)
        else:
            t=(k-3)/9; cl.update(x=ez(84,30,t),pose='hurt'); ce.update(x=ez(102,150,t),pose='hurt')
            for _ in range(2): s['fx'].append(('dust',cl['x']+random.randint(2,8),GROUND-random.randint(0,3))); s['fx'].append(('dust',ce['x']-random.randint(2,8),GROUND-random.randint(0,3)))
    elif 96<=f<112: ce['pose']='guard'
    return s

# --- clip: ki barrage, Cell shrugs it off and returns one ------------------
def clip_barrage(f):
    s=base(f); cl,ce=s['cl'],s['ce']; calm_aura(s,f,10,70,('cl',)); calm_aura(s,f,20,120,('ce',))
    if 12<=f<72: cl['pose']='charge' if f<24 else ('punch' if (f//2)%2 else 'charge')
    if 24<=f<72: ce['pose']='guard'
    HIT=138
    for k in range(16):
        t0=24+3*k
        if f<t0: continue
        x=40+6*(f-t0)
        if x<HIT: s['fx'].append(('orb',x,GROUND-6,CL_OR,1))
        else:
            dt=f-t0-(HIT-40)//6
            if dt<2: s['fx'].append(('spark',HIT,GROUND-8+random.randint(-3,3),3))
            gx=HIT+8+(k*29)%34
            if 1<=dt<7: s['fx'].append(('ring',gx,GROUND,dt*2,(255,200,120)))
            if dt==1: s['shake']=rshake()
    if 40<=f<96:   # smoke builds over Cell, then clears
        dens=min(1,(f-40)/12)*(1 if f<80 else max(0,(96-f)/16))
        rr=random.Random(f//2)
        for i in range(int(18*dens)):
            px=150+rr.randint(-16,18); py=GROUND-4-rr.randint(0,18)
            c=(70,68,72) if i%2 else (110,106,108)
            s['fx'].append(('smoke',px,py,rr.randint(2,5),c))
    if 72<=f<96: ce['pose']='idle'
    if 96<=f<102:
        ce['pose']='charge'; s['fx'].append(('ceball',140,GROUND-11,1+(f-96)//2))
    if 100<=f<117:
        ce['pose']='charge' if f<104 else 'idle'
        x=140-6*(f-100); s['fx'].append(('ceball',x,GROUND-10,3))
    if 112<=f<120: cl['pose']='punch'
    if f==116: s['fx'].append(('spark',46,GROUND-9,7)); s['shake']=rshake(2)
    if 116<=f<126: dt=f-116; s['fx'].append(('ceball',44+3*dt,GROUND-10-6*dt,3))
    if 128<=f<134: s['fx'].append(('twinkle',78,3,1+(f-128)%3))
    return s

# --- clip: Solar Flare, then Claude goes Super -----------------------------
def clip_super(f):
    s=base(f); cl,ce=s['cl'],s['ce']
    if 12<=f<22:
        ce['pose']='guard'
        if f>=17: s['fx'].append(('spark',146,GROUND-17,2+(f%2)))
    if 22<=f<30: s['flash']=max(0,1-(f-22)/8); s['fc']=(146,GROUND-17)
    if 26<=f<48:
        cl['pose']='hurt'; cl['x']=30+random.choice([-1,0,1])
    if 28<=f<36: ce.update(x=ez(150,46,(f-28)/8),pose='punch'); s['after'].append(('ce',ce['x']+8,GROUND,'punch',True,(210,255,200)))
    if 36<=f<48:
        ce.update(x=46,pose='punch' if (f//2)%2 else 'guard'); cl['x']=ez(30,24,(f-36)/12)
        if f%2==0: s['fx'].append(('spark',38,GROUND-7+random.randint(-2,2),4)); s['shake']=rshake()
    if 48<=f<60:
        t=(f-48)/12; ce.update(x=ez(46,112,t),y=GROUND-int(8*math.sin(math.pi*t)),pose='guard')
    if 60<=f<120: ce.update(x=112,pose='idle')
    if 48<=f<60: cl.update(x=24,pose='guard')
    if 60<=f<72:
        cl.update(x=ez(24,30,(f-60)/12)); cl['aura']=(AUR_C,1+(f-60)//6); s['shake']=rshake() if f%3==0 else (0,0)
        if f%2==0: s['fx'].append(('rock',random.randint(14,48),GROUND-random.randint(0,(f-60)*2)))
    if 72<=f<120:
        cl['pal']=GOLD; cl['aura']=(GOLD_AURA,3 if f<108 else 2)
        if f==72: s['flash']=0.6; s['fc']=(30,GROUND-6)
        if f<100:
            s['fx']+= [('bolt',random.randint(20,40),GROUND-18)]; s['shake']=rshake() if f%2 else (0,0)
            s['fx'].append(('rock',random.randint(10,52),GROUND-random.randint(0,30)))
    if 96<=f<104:
        t=(f-96)/8; cl.update(x=ez(30,100,t),pose='dash')
        s['after']+= [('cl',cl['x']-7,GROUND,'dash',False,(255,236,150)),('cl',cl['x']-14,GROUND,'dash',False,(255,236,150))]
    if 104<=f<108: cl.update(x=100,pose='punch')
    if f==104: s['fx'].append(('spark',108,GROUND-8,10)); s['shake']=rshake(2); s['flash']=0.4; s['fc']=(108,GROUND-8)
    if 104<=f<116:
        t=(f-104)/12; ce.update(x=ez(112,170,t),y=GROUND-int(7*math.sin(math.pi*t)),pose='hurt')
        if f>=112: s['fx'].append(('dust',ce['x']-5+random.randint(-3,3),GROUND-random.randint(0,4)))
    if 116<=f<140: ce.update(x=ez(170,150,(f-116)/20),pose='guard')
    if 108<=f<120: cl.update(x=ez(100,30,(f-108)/12),y=GROUND-int(6*math.sin(math.pi*(f-108)/12)),pose='guard')
    if 120<=f<132:
        cl['pal']=GOLD if f%2==0 and f<128 else None; cl['aura']=(GOLD_AURA,1) if f<126 else None
    return s

# --- clip: Spirit Bomb (Claude's giant asterisk) vs Kamehameha -------------
def clip_genki(f):
    s=base(f); cl,ce=s['cl'],s['ce']
    C=(30,12)
    if 12<=f<84:
        cl['pose']='armsup'; cl['aura']=(AUR_C,1)
        r=2+10*(f-12)/72; s['under'].append(('genki',C[0],C[1],r))
        for i in range(14):
            a=i*2.39996; ph=((f*0.035+i*0.137)%1)
            L=(1-ph)*140
            s['fx'].append(('mote',C[0]+math.cos(a)*L,C[1]+math.sin(a)*L*0.45,(255,200,150) if i%2 else (255,240,210)))
        if f>60 and f%3==0: s['shake']=rshake()
    if 40<=f<96:
        ce.update(pose='charge'); ce['aura']=(AUR_E,2); s['fx'].append(('ceball',140,GROUND-11,min(4,1+(f-40)//10)))
    if 84<=f<96:
        t=(f-84)/12; cl['pose']='charge'
        bx=lerp(30,96,t); by=lerp(12,GROUND-14,t)-10*math.sin(math.pi*t)
        s['under'].append(('genki',bx,by,12))
    if 96<=f<144:
        cl['pose']='charge'; cl['aura']=(AUR_C,2); ce['pose']='charge'; ce['aura']=(AUR_E,3)
        bx=96+6*math.sin((f-96)*0.3)
        s['under'].append(('beam',bx+12,140,GROUND-11,CE_BL)); s['under'].append(('genki',bx,GROUND-14,12+(f%2)))
        s['fx'].append(('spark',bx+13,GROUND-11+random.randint(-4,4),4)); s['shake']=rshake()
        if f%2==0: s['fx'].append(('rock',random.randint(70,130),GROUND-random.randint(0,20)))
    if 144<=f<152:
        t=(f-144)/8; bx=lerp(96,146,t); cl['pose']='charge'; ce['pose']='hurt'
        s['under'].append(('beam',bx+12,140,GROUND-11,CE_BL)) if bx+12<140 else None
        s['under'].append(('genki',bx,GROUND-14,12)); s['shake']=rshake(2)
    if 152<=f<166:
        t=(f-152)/14; ce['vis']=False
        s['fx'].append(('boom',150,GROUND-12,int(6+60*t))); s['flash']=1.0 if f<157 else max(0,1-(f-157)/9); s['fc']=(150,GROUND-12); s['shake']=rshake(2)
    if 166<=f<192:
        ce['pose']='hurt' if f<176 else ('guard' if f<184 else 'idle')
        if f<182:
            rr=random.Random(f//2)
            for i in range(int(10*(182-f)/16)): s['fx'].append(('smoke',150+rr.randint(-14,14),GROUND-rr.randint(2,20),rr.randint(2,4),(80,76,80)))
    return s

# --- clip: short standoff / taunt (breathing room between big fights) ------
def clip_standoff(f):
    s=base(f); cl,ce=s['cl'],s['ce']
    for i in range(10): s['fx'].append(('dust',(i*41-f*3)%W,GROUND-(i*7)%5))
    if 20<=f<52: ce['pose']='guard'
    if 28<=f<60:
        cl['pose']='guard' if (f//3)%2 else 'guard2'; cl['aura']=(AUR_C,1+(f%2)) if 32<=f<56 else None
    if 40<=f<56: ce['aura']=(AUR_E,1)
    return s

CLIPS={'teleport':(clip_teleport,132),'barrage':(clip_barrage,156),'super':(clip_super,168),
       'genki':(clip_genki,192),'standoff':(clip_standoff,84)}

if __name__=='__main__':
    import os, shutil, subprocess
    shutil.rmtree('clips',ignore_errors=True)
    all_names=['beam']+list(CLIPS)
    for name in all_names:
        os.makedirs(f'clips/{name}',exist_ok=True); random.seed(hash(name)%1000)
        if name=='beam': frames=[frame(f) for f in range(200)]
        else:
            fn,n=CLIPS[name]; frames=[render(fn(f),f) for f in range(n)]
        for i,fr in enumerate(frames): fr.save(f'clips/{name}/{i:03d}.png')
        big=[fr.resize((W*2,H*2),Image.NEAREST) for fr in frames]
        sh=Image.new('RGB',(W*2*2,H*2*6)); pick=[int(i*(len(big)-1)/11) for i in range(12)]
        for j,i in enumerate(pick): sh.paste(big[i],((j%2)*W*2,(j//2)*H*2))
        sh.save(f'sheet_{name}.png')
        print(name,len(frames),'frames',len(frames)/FPS,'s')
