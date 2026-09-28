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
BLACK = '--black' in sys.argv
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

def draw(im,spr,cx,feet,flip,aura=None,alpha=1.0,tint=None,f=0):
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
        c=PAL[ch]
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

frames=[frame(f) for f in range(N)]
import os; FD='frames_black' if BLACK else 'frames'; os.makedirs(FD,exist_ok=True)
for i,fr in enumerate(frames): fr.resize((W*2,H*2),Image.NEAREST).save(f'{FD}/{i:03d}.png')
sheet=Image.new('RGB',(W*4,H*8))
for j,i in enumerate(range(0,200,25)):
    pass
for j,i in enumerate([5,25,35,45,60,70,92,100,115,140,150,165,174,185,195,199]):
    sheet.paste(frames[i].resize((W*2,H*2),Image.NEAREST),((j%2)*W*2,(j//2)*H*2)) if j<16 else None
sheet=Image.new('RGB',(W*2*2,H*2*8))
for j,i in enumerate([5,25,35,45,60,70,92,100,115,140,150,165,174,185,195,199]):
    sheet.paste(frames[i].resize((W*2,H*2),Image.NEAREST),((j%2)*W*2,(j//2)*H*2))
sheet.save('sheet_black.png' if BLACK else 'sheet.png')
