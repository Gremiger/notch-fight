"""Fortnite: Claude (Jonesy hair, backpack, pickaxe) vs Geno on the island — Tilted Towers on the
skyline, the Battle Bus overhead, the purple storm wall closing in from both edges. Geno opens up
with an AR, Claude cranks 90s: wall, ramp, wall, ramp, up to high ground. Geno's rocket blows the
top wall off, Claude leaps down and pickaxes through Geno's wall — close-up: a wood EDIT, the window
opens on Geno's face, pump shotgun, 200 HEADSHOT. Geno is eliminated into cubes; the #1 VICTORY
ROYALE card with the crown dropping on Claude's head, the default dance, and a new match: the bus
comes round again and Geno glides back down to his spot."""
from engine import *

THEME = 'fn'
N_ = 336
CX, EX = 28, 152                                                    # the loop keyframe positions

PAL.update({'A':(26,24,32),'Q':(212,170,60),'F':(150,96,52)})
def _jones(s):
    s=recolor_rows(s,lambda x,y,t,l,r,c: ('F' if x==l-1 else 'k') if (t+1<=y<=t+6 and l-2<=x<=l-1 and c in '.o') else None)
    return overlay(s,["..FF.F...","FFFFFFFF."],0,0)                  # Jonesy's brown hair tuft
JONES=variant(_jones)
GENO=poses(S([
".....kkkk.......","....kkHkkk......","....kkHkss......","....kssEsE......","....ksssss......",".....ssss.......",
"...AAAQAAAA.....","..AAAArQAAAA....","..AQAArrAAQA....","..AA.AQQAA.AA...","..AA.ArrA..AA...","..AA.AAAA..sA...",
"..ss.AQQA.......",".....AAAA.......","....AA..AA......","....AQ..QA......","....AA..AA......","....Ar..rA......",
"....AA..AA......","...AAA..AAA.....",]),9,'As',4)
GENO_PAL={'r':(200,30,40)}

# ---- local glyphs: a wider M and W (the 3x5 font's read as H) and a '#' --------------------------
_GLYPH={'M':(5,"10001"+"11011"+"10101"+"10001"+"10001"),'W':(5,"10001"+"10001"+"10101"+"11011"+"10001"),
        '#':(5,"01010"+"11111"+"01010"+"11111"+"01010")}

def _mask(txt):
    gl=[_GLYPH.get(ch) or (3,FONT.get(ch,FONT[' '])) for ch in txt]
    m=Image.new('L',(sum(w+1 for w,_ in gl)-1,5),0); md=ImageDraw.Draw(m); x=0
    for w,bits in gl:
        for j,b in enumerate(bits):
            if b=='1': md.point((x+j%w,j//w),fill=255)
        x+=w+1
    return m

def say(im,txt,y,c,scale=1,cx=W//2,outline=None,shadow=(0,0,0)):
    """big_text with the local glyphs; scale=1 is a normal callout."""
    m=_mask(txt); m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        if shadow is not None: im.paste(shadow,(x+2,y+2),m)
    elif shadow is not None: im.paste(shadow,(x+1,y+1),m)
    im.paste(c,(x,y),m)

@fx('fn_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,cx=W//2,outline=None):
    s['fx'].append(('fn_say',txt,y,c,scale,cx,outline))

# ---- the island: Tilted Towers on the skyline, trees, grass and a dirt road ----------------------
WOOD,WOOD_D,WOOD_L=(176,118,60),(120,76,36),(214,160,92)
HOLO,HOLO_L=(70,150,255),(170,215,255)

def _pine(d,x,y,h):
    d.line([x,y,x,y-3],fill=(96,62,34))
    for k in range(3):
        w=h//2-k*2; yy=y-3-k*(h//4)
        d.polygon([(x-w,yy),(x+w,yy),(x,yy-h//3)],fill=(34,110,56) if k%2 else (44,134,64))

def _oak(d,x,y,r):
    d.line([x,y,x,y-r],fill=(104,66,36))
    d.ellipse([x-r,y-r*2-2,x+r,y-r+1],fill=(52,140,58)); d.ellipse([x-r+2,y-r*2-1,x+r-3,y-r-3],fill=(84,172,70))

def _island(d):
    for y in range(GROUND+1):                                       # bright Fortnite sky
        k=y/GROUND; d.line([0,y,W,y],fill=(int(lerp(70,170,k)),int(lerp(150,220,k)),int(lerp(245,255,k))))
    for cx,cy,w in ((14,14,20),(54,8,14),(150,12,24),(116,20,12)):
        d.ellipse([cx,cy,cx+w,cy+5],fill=(250,252,255)); d.line([cx+3,cy+5,cx+w-3,cy+5],fill=(200,220,245))
    for x in range(W):                                              # far hills
        y=int(40+3*math.sin(x*0.05)+2*math.sin(x*0.13+1)); d.line([x,y,x,GROUND],fill=(110,176,120))
    # Tilted Towers: a tight block of towers and the clock tower in the middle distance
    towers=[(60,26,12,(170,160,150)),(71,20,10,(196,120,84)),(80,30,9,(150,150,164)),(98,24,11,(186,176,156)),
            (108,18,9,(176,104,76)),(116,28,12,(160,160,172))]
    for x,top,w,c in towers:
        dk=tuple(int(v*0.72) for v in c)
        d.rectangle([x,top,x+w,GROUND-6],fill=c); d.line([x+w,top,x+w,GROUND-6],fill=dk)
        d.line([x,top,x+w,top],fill=tuple(min(255,v+30) for v in c))
        for wy in range(top+3,GROUND-8,4):
            for wx in range(x+2,x+w-1,3): d.point((wx,wy),fill=(250,236,160) if (wx*3+wy)%7==0 else (70,86,110))
    d.rectangle([89,12,96,GROUND-6],fill=(204,190,160)); d.line([96,12,96,GROUND-6],fill=(150,138,114))   # clock tower
    d.polygon([(88,12),(97,12),(92,6)],fill=(150,70,50)); d.ellipse([90,15,95,20],fill=(250,248,236),outline=(80,70,60))
    d.line([92,17,92,15],fill=(40,30,30)); d.line([92,17,94,17],fill=(40,30,30))
    for x in range(W):                                              # near hill + grass
        y=int(50+2*math.sin(x*0.09+2)); d.line([x,y,x,GROUND],fill=(76,162,70))
        if x%5==0: d.point((x,y),fill=(120,200,96))
    for x,h in ((6,20),(18,16),(170,22),(181,15),(132,14)): _pine(d,x,GROUND,h)
    for x,r in ((46,5),(146,6),(158,4)): _oak(d,x,GROUND,r)
    rr=random.Random(5151)
    for x in range(W):                                              # grass lip and the dirt road
        d.point((x,GROUND),fill=(96,196,74))
        for y in range(GROUND+1,H):
            road=abs(x-92)<60+(y-GROUND)*6
            c=(150,120,80) if road else (72,150,60)
            if rr.random()<0.18: c=(128,100,64) if road else (58,128,50)
            d.point((x,y),fill=c)
register_bg(THEME, lambda v: (96,196,74), decor=_island)

# ---- effects -----------------------------------------------------------------------------------
@fx('pickaxe')
def _fx_pickaxe(d,im,e,f):
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(150,96,52))
    dx,dy=x1-x0,y1-y0; L=max(1,math.hypot(dx,dy)); nx,ny=-dy/L,dx/L
    d.line([x1-nx*3,y1-ny*3,x1+nx*3,y1+ny*3],fill=(190,200,215),width=2)

@fx('fn_piece')
def _fx_piece(d,im,e,f):
    """A build piece in side view: kind wall|ramp|cone, x, level (16px cells), prog 0..1 (the blue
    blueprint filling up), window (an edited hole in a wall)."""
    _,kind,x,lv,prog,win=e; x=int(x); base=GROUND-16*lv; px=im.load()
    if kind in ('wall','cone'):
        h=16 if kind=='wall' else 12; top=base-h
        if prog<1:
            d.rectangle([x,top,x+3,base],outline=HOLO_L)
            for yy in range(int(base-h*prog),base+1):
                for xx in range(x,x+4): blend(px,xx,yy,HOLO,0.7)
            return
        d.rectangle([x-1,top-1,x+4,base],outline=OUT)
        d.rectangle([x,top,x+3,base],fill=WOOD); d.line([x,top,x,base],fill=WOOD_L); d.line([x+3,top,x+3,base],fill=WOOD_D)
        for yy in range(top+3,base,4): d.line([x,yy,x+3,yy],fill=WOOD_D)
        if win: d.rectangle([x,top+5,x+3,top+10],fill=(150,200,250))
    else:                                                           # ramp: rises 16 over 16 to the right
        L=int(16*prog) if prog<1 else 16
        for i in range(L+1):
            yy=base-i
            if prog<1:
                blend(px,x+i,yy,HOLO,0.8); blend(px,x+i,yy+1,HOLO,0.6); blend(px,x+i,yy+2,HOLO_L,0.5)
            else:
                d.point((x+i,yy-1),fill=OUT); d.point((x+i,yy+4),fill=OUT)
                d.line([x+i,yy,x+i,yy+3],fill=WOOD_D if i%4==0 else WOOD); d.point((x+i,yy),fill=WOOD_L)
        if prog>=1:                                                 # the support frame underneath
            d.line([x+15,base-13,x+15,base],fill=WOOD_D); d.line([x+8,base-6,x+8,base],fill=WOOD_D)

@fx('fn_bus')
def _fx_bus(d,im,e,f):
    """The Battle Bus under its hot-air balloon."""
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-7,y-12,x+7,y],fill=(70,140,240))
    for k in (-4,0,4): d.line([x+k,y-11,x+k*1.2,y-1],fill=(230,240,255))
    d.line([x-5,y-1,x-6,y+4],fill=(200,200,210)); d.line([x+5,y-1,x+6,y+4],fill=(200,200,210))
    d.rectangle([x-10,y+4,x+10,y+10],fill=(40,110,220),outline=(20,40,90))
    for wx in range(x-8,x+8,4): d.rectangle([wx,y+5,wx+2,y+7],fill=(200,236,255))
    d.line([x-10,y+9,x+10,y+9],fill=(250,210,60))
    d.point((x-7,y+11),fill=(30,30,30)); d.point((x+7,y+11),fill=(30,30,30))
    for k in range(3): d.point((x-12-k-(f%2),y+7),fill=(255,190-k*40,60))    # thruster

@fx('glider')
def _fx_glider(d,im,e,f):
    _,x,y=e; d.arc([x-8,y-6,x+8,y+4],180,360,fill=(250,210,60),width=2); d.line([x-6,y-1,x,y+6],fill=(200,200,210)); d.line([x+6,y-1,x,y+6],fill=(200,200,210))

@fx('fn_storm')
def _fx_storm(d,im,e,f):
    """The storm wall closing in from both edges, sw px deep, with a bright crackling front."""
    _,sw=e; sw=int(sw); px=im.load(); f%=N_; rr=random.Random(f//2)
    for x in list(range(0,sw))+list(range(W-sw,W)):
        k=min(x,W-1-x)/max(1,sw)
        for y in range(H): blend(px,x,y,(130,50,210),0.52-0.22*k+0.06*math.sin(y*0.4+f*0.5+x*0.2))
    for ex in (sw,W-1-sw):
        for y in range(H):
            if (y+f)%5: blend(px,ex,y,(214,150,255),0.8)
        if rr.random()<0.4:                                         # lightning inside the wall
            bx=ex-rr.randint(2,6) if ex<W//2 else ex+rr.randint(2,6); by=rr.randint(0,20); pts=[(bx,by)]
            for _ in range(4): bx+=rr.randint(-2,2); by+=rr.randint(4,8); pts.append((bx,by))
            d.line(pts,fill=(240,220,255))

@fx('fn_hud')
def _fx_hud(d,im,e,f):
    """Claude's shield + health bars, and the minimap with the storm circle and players left."""
    _,sh,hp,r,alive=e
    for y,v,c in ((2,sh,(60,160,255)),(8,hp,(70,220,90))):
        d.rectangle([3,y,33,y+2],fill=(20,24,40));
        if v>0: d.rectangle([3,y,3+int(30*v),y+2],fill=c); d.line([3,y,3+int(30*v),y],fill=tuple(min(255,k+70) for k in c))
        text(d,str(int(round(v*100))),36,y-1,(255,255,255))
    x0,y0=167,2; d.rectangle([x0,y0,x0+15,y0+13],fill=(130,50,200),outline=(250,250,255))
    d.ellipse([x0+8-r,y0+7-r,x0+8+r,y0+7+r],fill=(90,170,90),outline=(255,255,255))
    d.point((x0+6,y0+8),fill=(250,210,60))
    text(d,str(alive),x0-6,y0+4,(255,255,255))

@fx('fn_tracer')
def _fx_tracer(d,im,e,f):
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(255,240,150)); d.point((int(x1),int(y1)),fill=(255,255,255))

@fx('fn_rocket')
def _fx_rocket(d,im,e,f):
    _,x,y,dx,dy=e; L=max(1,math.hypot(dx,dy)); ux,uy=dx/L,dy/L
    d.line([x,y,x-ux*5,y-uy*5],fill=(90,110,90),width=2); d.point((int(x+ux),int(y+uy)),fill=(230,60,40))
    for k in range(4): d.point((int(x-ux*(6+k)),int(y-uy*(6+k))),fill=(255,200-k*40,60))

@fx('fn_rifle')
def _fx_rifle(d,im,e,f):
    _,x,y,flip=e; s_=-1 if flip else 1
    d.line([x,y,x+9*s_,y],fill=(60,60,70),width=2); d.point((x+2*s_,y+2),fill=(40,40,50)); d.point((x+9*s_,y-1),fill=(90,90,100))

@fx('fn_shotgun')
def _fx_shotgun(d,im,e,f):
    _,x,y=e; d.line([x,y,x+10,y],fill=(70,70,80),width=2); d.line([x-2,y+1,x+2,y+1],fill=(150,96,52),width=2)

@fx('fn_crown')
def _fx_crown(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y)
    d.polygon([(x-4,y),(x-4,y-4),(x-2,y-2),(x,y-5),(x+2,y-2),(x+4,y-4),(x+4,y)],fill=(250,210,60),outline=(170,110,20))
    d.point((x,y-1),fill=(230,40,60));
    if (f//4)%3==0: d.point((x+3,y-5),fill=(255,255,255))

@fx('fn_confetti')
def _fx_confetti(d,im,e,f):
    _,t0=e; rr=random.Random(77); k=f-t0
    for _ in range(40):
        x=rr.randint(0,W); y=(rr.randint(-60,0)+k*rr.uniform(0.8,1.6))
        if 0<=y<GROUND:
            c=rr.choice([(250,210,60),(90,170,255),(240,90,170),(120,230,120),(255,255,255)])
            xx=x+2*math.sin(k*0.3+x); d.point((int(xx),int(y)),fill=c); d.point((int(xx)+(k//3)%2,int(y)+1),fill=c)

@fx('fn_note')
def _fx_note(d,im,e,f):
    _,x,y,c=e; x,y=int(x),int(y)
    d.rectangle([x,y+3,x+1,y+4],fill=c); d.line([x+1,y,x+1,y+3],fill=c); d.point((x+2,y),fill=c)

@fx('fn_cubes')
def _fx_cubes(d,im,e,f):
    """Eliminated: the body breaks into little glowing cubes that float up (t frames in)."""
    _,x0,t=e; rr=random.Random(3); spr=GENO['hurt']
    for j,row in enumerate(spr):
        for i,c in enumerate(row):
            if c=='.' or rr.random()<0.55: continue
            x=x0-len(row)/2+(len(row)-1-i)+rr.uniform(-1,1)*t*0.6; y=GROUND-len(spr)+j-t*rr.uniform(0.6,2.0)
            if rr.random()>t/22:
                col=(120,200,255) if (i+j+f)%3 else (255,255,255); d.rectangle([x,y,x+1,y+1],fill=col)

# ---- close-up 1: the wood EDIT, 200 headshot -----------------------------------------------------
def _geno_face(d,cx,cy,shock,hit):
    skin=(255,170,150) if hit else (240,200,160)
    d.rectangle([cx-11,cy-6,cx+11,cy+14],fill=skin)
    d.rectangle([cx-12,cy-14,cx+12,cy-4],fill=(30,28,40)); d.rectangle([cx-3,cy-14,cx,cy-5],fill=(242,242,250))  # hair + streak
    d.rectangle([cx-12,cy-6,cx-10,cy+4],fill=(30,28,40))
    for ex in (cx-5,cx+5):
        if hit: d.line([ex-2,cy-1,ex+2,cy+3],fill=(30,20,20)); d.line([ex-2,cy+3,ex+2,cy-1],fill=(30,20,20))
        else:
            d.rectangle([ex-2,cy-2,ex+2,cy+3],fill=(255,255,255)); d.rectangle([ex-1 if shock else ex,cy,ex+ (0 if shock else 1),cy+2],fill=(40,110,220))
    if shock or hit: d.ellipse([cx-3,cy+7,cx+3,cy+12],fill=(90,30,30))
    else: d.line([cx-3,cy+9,cx+3,cy+9],fill=(120,60,50))
    d.rectangle([cx-14,cy+14,cx+14,cy+30],fill=(26,24,32)); d.polygon([(cx-3,cy+14),(cx+3,cy+14),(cx,cy+22)],fill=(200,30,40))

def closeup_edit(t,f):
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    for y in range(H):
        k=y/H; d.line([0,y,W,y],fill=(int(lerp(150,210,k)),int(lerp(110,160,k)),int(lerp(240,255,k))))
    for x in range(W):                                              # the storm light bleeding in
        a=max(0,1-min(x,W-1-x)/40)*0.5
        for y in range(0,H,1): blend(im.load(),x,y,(130,50,210),a)
    hit=t>=0.58; shock=t>=0.42
    jx=((f%3)-1)*2 if 0.58<=t<0.7 else 0
    _geno_face(d,92+jx+(4 if hit else 0),32-(2 if hit else 0),shock,hit)
    X0,Y0,C=62,2,20                                                 # the wall: a 3x3 edit grid of 20px tiles
    hole=t>=0.32; editing=0.12<=t<0.32; px=im.load()
    for j in range(3):
        for i in range(3):
            if hole and (i,j)==(1,1): continue
            x0,y0=X0+i*C,Y0+j*C
            d.rectangle([x0,y0,x0+C-1,y0+C-1],fill=WOOD)
            for yy in range(y0+4,y0+C,5): d.line([x0,yy,x0+C-1,yy],fill=WOOD_D)
            for yy in range(y0,y0+C,5):
                sx=x0+(7 if (yy//5)%2 else 13); d.line([sx,yy,sx,yy+3],fill=WOOD_D)
                d.line([x0,yy,x0+C-1,yy],fill=WOOD_L)
            d.point((x0+2,y0+2),fill=(80,70,70)); d.point((x0+C-3,y0+C-3),fill=(80,70,70))
    d.rectangle([X0-1,Y0-1,X0+3*C,Y0+3*C],outline=WOOD_D)
    if editing:                                                     # edit mode: blue blueprint + grid
        for yy in range(Y0,Y0+3*C):
            for xx in range(X0,X0+3*C): blend(px,xx,yy,HOLO,0.55)
        for k in range(4): d.line([X0+k*C,Y0,X0+k*C,Y0+3*C],fill=HOLO_L); d.line([X0,Y0+k*C,X0+3*C,Y0+k*C],fill=HOLO_L)
        if t>=0.2:
            x0,y0=X0+C,Y0+C
            for yy in range(y0,y0+C):
                for xx in range(x0,x0+C): blend(px,xx,yy,(210,236,255),0.6)
            d.rectangle([x0,y0,x0+C,y0+C],outline=(255,255,255))
        say(im,"EDIT",54,HOLO_L,cx=30,outline=(20,40,90))
    if 0.32<=t<0.36: d.rectangle([X0+C,Y0+C,X0+2*C,Y0+2*C],outline=(255,255,255))
    if 0.42<=t<0.58: say(im,"!",8,(255,80,60),scale=3,cx=134,outline=(80,20,10))
    if t>=0.46:                                                     # the pump shotgun swings up into the window
        o=int(ez(30,0,(t-0.46)/0.1))
        bx,by=104+o,40+o//2
        d.polygon([(bx-2,by-5),(bx+4,by-1),(bx+66,by+30),(bx+56,by+40)],fill=(20,20,26))
        d.polygon([(bx-1,by-3),(bx+3,by),(bx+64,by+30),(bx+56,by+38)],fill=(90,92,104))
        d.line([bx,by-3,bx+63,by+28],fill=(160,162,176)); d.line([bx+2,by+2,bx+56,by+36],fill=(60,60,70))
        d.polygon([(bx+12,by+6),(bx+28,by+13),(bx+24,by+21),(bx+8,by+13)],fill=(20,20,26))
        d.polygon([(bx+13,by+7),(bx+27,by+13),(bx+24,by+19),(bx+10,by+13)],fill=(170,110,60))
        for k in range(3): d.line([bx+15+k*4,by+9+k*2,bx+13+k*4,by+14+k*2],fill=(110,70,36))
        d.polygon([(bx+40,by+22),(bx+74,by+36),(bx+64,by+46),(bx+34,by+30)],fill=(126,80,42),outline=(20,20,26))
        if 0.58<=t<0.64:                                            # BOOM
            asterisk(d,bx-2,by-2,10+(f%2)*2,(255,240,150),f); d.ellipse([bx-6,by-6,bx+2,by+2],fill=(255,255,220))
            for k in range(8): d.point((bx-8-k*2,by-4+((k*5)%9)-4),fill=(255,230,120))
    if t>=0.6:
        y=int(ez(30,10,(t-0.6)/0.1)); jj=(f%2) if t<0.7 else 0
        say(im,"200",y,(255,226,70),scale=3,cx=150+jj,outline=(90,50,0))
        if t>=0.68: say(im,"HEADSHOT",y+18,(255,255,255),cx=150,outline=(90,50,0))
    if 0.58<=t<0.62: im=fade_to(im,(255,250,230),0.6); d=ImageDraw.Draw(im)
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,(255,255,255),(t-0.9)/0.1*0.7)
    return im

# ---- close-up 2: #1 VICTORY ROYALE ---------------------------------------------------------------
def closeup_victory(t,f):
    im=Image.new('RGB',(W,H),(24,50,150)); d=ImageDraw.Draw(im)
    cx,cy=34,40; a0=f*0.02
    for k in range(16):                                             # rotating light rays
        a=a0+k*math.pi/8
        d.polygon([(cx,cy),(cx+math.cos(a)*260,cy+math.sin(a)*260),(cx+math.cos(a+0.2)*260,cy+math.sin(a+0.2)*260)],
                  fill=(50,110,236) if k%2 else (36,80,200))
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([cx-40,cy-40,cx+40,cy+40],fill=120)
    im.paste((150,200,255),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    # Claude, big: orange head, brown Jonesy hair, happy eyes
    hx=14
    d.rectangle([hx,26,hx+40,H],fill=(217,119,87)); d.rectangle([hx,26,hx+5,H],fill=(176,92,66))
    d.rectangle([hx-2,20,hx+42,27],fill=(150,96,52)); d.rectangle([hx+6,16,hx+18,20],fill=(150,96,52)); d.rectangle([hx+22,17,hx+30,20],fill=(150,96,52))
    for ex in (hx+19,hx+31):
        d.arc([ex-4,34,ex+4,44],200,340,fill=(24,14,12),width=2)    # ^ ^ happy eyes
    d.chord([hx+17,46,hx+35,58],0,180,fill=(24,14,12)); d.chord([hx+19,47,hx+33,54],0,180,fill=(240,90,90))
    # the crown drops on and bounces
    if t>=0.14:
        k=(t-0.14)/0.16
        yb=lerp(-14,8,k) if k<1 else 8-3*abs(math.sin((t-0.3)*20))*max(0,1-(t-0.3)*6)
        x0,y0=hx+8,int(yb)
        d.polygon([(x0,y0+12),(x0,y0),(x0+6,y0+6),(x0+12,y0-2),(x0+18,y0+6),(x0+24,y0),(x0+24,y0+12)],fill=(250,210,60),outline=(170,110,20))
        d.rectangle([x0,y0+9,x0+24,y0+12],fill=(222,168,36))
        for gx,gc in ((x0+6,(230,40,60)),(x0+12,(60,160,255)),(x0+18,(230,40,60))): d.rectangle([gx-1,y0+9,gx+1,y0+11],fill=gc)
        if k>=1 and (f//3)%2: asterisk(d,x0+24,y0,4,(255,255,220),f)
    TX=124; oc=(20,30,100); gold=(255,226,90)
    if t>=0.08:
        jj=((f%3)-1) if t<0.2 else 0
        say(im,"#1",2+jj,(255,255,255),scale=4,cx=TX,outline=oc)
    if t>=0.3: say(im,"VICTORY",int(lerp(28,26,(t-0.3)*10)),gold,scale=2,cx=int(lerp(220,TX,(t-0.3)/0.06)),outline=oc)
    if t>=0.38: say(im,"ROYALE",int(lerp(42,40,(t-0.38)*10)),gold,scale=2,cx=int(lerp(220,TX,(t-0.38)/0.06)),outline=oc)
    FX['fn_confetti'](d,im,('fn_confetti',-20),f)
    if 0.3<=t<0.34: im=fade_to(im,(255,255,255),0.5); d=ImageDraw.Draw(im)
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,(255,255,255),(t-0.9)/0.1*0.6)
    return im

# ---- the clip ----------------------------------------------------------------------------------
# build pieces: (kind, x, level, built at, destroyed at)
PIECES=[('wall',58,0,24,None),('ramp',42,0,38,None),('wall',74,1,48,None),('ramp',58,1,50,None),
        ('cone',77,2,60,76),('wall',140,0,52,90),('wall',140,0,92,None)]
EDIT=96; ELIM=132; CARD=160; DANCE=204

def storm_w(f): return 3 if (f<8 or f>=CARD) else int(ez(3,24,(f-8)/150))

def dmg(s,f,t0,txt,x,y,c,dur=14):
    if t0<=f<t0+dur: s['fx'].append(('dmg',txt,x,y-(f-t0)*0.7,c))

def on_ramp(x0,lv,x): return GROUND-16*lv-int(max(0,min(16,x-x0)))

def clip_royale(f):
    s=scene(f,THEME)
    if EDIT<=f<ELIM: s['image']=closeup_edit((f-EDIT)/(ELIM-EDIT),f); return s
    if CARD<=f<DANCE: s['image']=closeup_victory((f-CARD)/(DANCE-CARD),f); return s
    cl=actor(JONES[guard_pose(f)],CX); gn=actor(GENO['idle'],EX,flip=True,pal=GENO_PAL)
    sh,hp=1.0,1.0; alive=2; tool='pick'; gtool=None; pose=None
    # the build pieces standing (they only exist during the fight)
    if f<CARD:
        for kind,x,lv,t0,t1 in PIECES:
            if f>=t0 and (t1 is None or f<t1):
                s['under'].append(('fn_piece',kind,x,lv,min(1,(f-t0+1)/4),kind=='wall' and x==140 and t0==92 and f>=ELIM))
    # 1) the Battle Bus flies over, the storm starts closing
    if f<64: s['under'].append(('fn_bus',lerp(-24,W+24,f/64),10+round(math.sin(f*0.2))))
    if 10<=f<38: shout(s,"STORM EYE SHRINKING",(236,170,255),y=26,outline=(60,20,90))
    # 2) Geno opens up with his AR; Claude walls up
    if 16<=f<48:
        gn['spr']=GENO['attack']; gtool='rifle'
        if f%3==0:
            if f<24: tx,ty=CX+4,GROUND-6; s['fx'].append(('spark',tx,ty,2))
            else: tx,ty=60,GROUND-4-(f*5)%12; s['fx'].append(('spark',tx,ty,2)); s['fx'].append(('shard',tx-1,ty+1,WOOD_L))
            s['fx'].append(('fn_tracer',EX-12,GROUND-11,tx,ty))
    dmg(s,f,18,"24",CX-4,GROUND-18,(90,170,255)); dmg(s,f,21,"24",CX+2,GROUND-22,(90,170,255))
    if 18<=f<CARD: sh=0.76
    if 21<=f<CARD: sh=0.52
    if 16<=f<CARD: tool=None                                         # build mode: hands free
    # 3) 90s: ramp, wall, ramp — up to high ground
    if 30<=f<40: cl['x']=ez(CX,42,(f-30)/10); pose='dash'
    if 40<=f<50:
        x=lerp(42,58,(f-40)/10); cl.update(x=x,y=on_ramp(42,0,x)); pose='dash'
    if 50<=f<60:
        x=lerp(58,72,(f-50)/10); cl.update(x=x,y=on_ramp(58,1,x)); pose='dash'
    if 60<=f<80: cl.update(x=72,y=GROUND-30); pose='guard' if f<70 else 'charge'
    if f in (24,38,48,50,60): s['fx'].append(('ring',{24:59,38:50,48:75,50:66,60:78}[f],GROUND-8-8*(f>=48)-12*(f>=60),5,HOLO_L))
    if 44<=f<64 and f%4==0:                                         # Geno shoots up at the tower
        ty=GROUND-20-(f%12); s['fx'].append(('fn_tracer',EX-12,GROUND-11,76,ty)); s['fx'].append(('spark',76,ty,2))
    if 52<=f<60: gn['spr']=GENO['idle']; gtool=None
    # 4) the rocket takes the top wall off
    if 62<=f<76:
        gn['spr']=GENO['attack']
        t=(f-62)/14; x=lerp(EX-12,79,t); y=lerp(GROUND-12,GROUND-38,t)
        s['fx'].append(('fn_rocket',x,y,-1,-0.35))
        for k in range(1,5): s['fx'].append(('smoke',x+k*5,y+k*1.8,1+k//2,(200,200,200) if k%2 else (160,160,160)))
        if f<68: shout(s,"ROCKET!",(255,120,80),y=24,cx=EX-22,outline=(80,20,10))
    if 76<=f<84:
        t=f-76; s['fx'].append(('boom',78,GROUND-38,t*3+2)); s['shake']=rshake(2)
        if f==76: s['flash']=0.7; s['fc']=(78,GROUND-38)
        for k in range(4): s['fx'].append(('shard',78+random.randint(-10,10),GROUND-38+random.randint(-8,8)+t,WOOD))
        cl['spr']=JONES['hurt']; pose='hurt'
    # 5) Claude drops on Geno's wall with the pickaxe
    if 84<=f<92:
        t=(f-84)/8; cl.update(x=lerp(72,128,t),y=int(lerp(GROUND-30,GROUND,t*t)-10*math.sin(math.pi*t))); pose='armsup'
        tool='pick'
    if 90<=f<96:
        cl.update(x=128,y=GROUND); pose='punch'; tool='pick'
        if f==90:
            s['flash']=0.6; s['fc']=(140,GROUND-8); s['shake']=rshake(2)
        if f<94:
            for k in range(6): s['fx'].append(('shard',140+random.randint(-4,8),GROUND-random.randint(0,16),WOOD if k%2 else WOOD_L))
            s['fx'].append(('spark',139,GROUND-10,5))
        gn['spr']=GENO['hurt']
    # 6) (close-up) — then Geno is eliminated
    if ELIM<=f<CARD:
        cl.update(x=128,y=GROUND); pose='punch'; tool='shotgun'; alive=1
        t=f-ELIM
        if t<4: gn.update(spr=GENO['hurt'],x=EX+t*2,tint=(255,120,120))
        else: gn['vis']=False; s['fx'].append(('fn_cubes',EX+8,t))
        dmg(s,f,ELIM,"200",EX-8,GROUND-30,(255,226,70),dur=20)
        if f>=ELIM+4: shout(s,"CLAUDE ELIMINATED GENO",(255,255,255),y=12,outline=(20,30,80))
        s['fx'].append(('fn_crown',EX+8,GROUND-12-min(t,16))) if t>=12 else None
    # 7) after the card: the default dance with the crown
    if DANCE<=f<252:
        k=f-DANCE; gn['vis']=False; alive=1
        cl['x']=92; pose=['armsup','punch','guard','dash','armsup','charge'][(k//4)%6]; cl['flip']=(k//8)%2==1
        cl['y']=GROUND-(1 if (k//2)%2 else 0); tool=None
        s['fx'].append(('fn_crown',92,cl['y']-14))
        s['fx'].append(('fn_confetti',DANCE))
        for j in range(3):
            ph=((k+j*8)%24)/24; s['fx'].append(('fn_note',92-14+j*12+int(4*math.sin(ph*6)),GROUND-16-ph*18,
                                                   [(250,210,60),(90,170,255),(240,90,170)][j]))
        if k<16: shout(s,"#1",(250,210,60),y=14,scale=2,outline=(20,30,100))
    # 8) new match: Claude runs home, the bus comes round, Geno glides back in
    if 252<=f<276:
        t=(f-252)/24; cl['x']=ez(92,CX,t); cl['flip']=True if t<0.9 else False; pose='dash' if t<0.9 else None
        if f<256: s['fx'].append(('twinkle',92,GROUND-16,2))
    if 236<=f<300: s['under'].append(('fn_bus',lerp(-24,W+24,(f-236)/64),10+round(math.sin(f*0.2))))
    if DANCE<=f<262: gn['vis']=False; alive=1
    if 262<=f<312:
        t=(f-262)/50; x=lerp(100,EX,t); y=lerp(22,GROUND,t)
        gn.update(vis=True,x=x,y=int(y),spr=GENO['hurt'] if f<270 else GENO['idle'])
        if 270<=f<310: s['fx'].append(('glider',x,y-22))
    if pose: cl['spr']=JONES[pose]
    p=pose or 'guard'
    if tool=='pick':
        sx=-1 if cl['flip'] else 1
        if p in ('guard','guard2'): s['fx'].append(('pickaxe',cl['x']+5*sx,cl['y']-5,cl['x']+9*sx,cl['y']-15))
        elif p=='armsup': s['fx'].append(('pickaxe',cl['x']+2,cl['y']-10,cl['x']-2,cl['y']-20))
        else: s['fx'].append(('pickaxe',cl['x']+8*sx,cl['y']-5,cl['x']+17*sx,cl['y']-9))
    elif tool=='shotgun': s['fx'].append(('fn_shotgun',cl['x']+6,cl['y']-6))
    if gtool=='rifle' and gn['vis']: s['fx'].append(('fn_rifle',int(gn['x'])-6,GROUND-11,True))
    s['fx'].insert(0,('fn_storm',storm_w(f)))
    rr=int(ez(6,3,(f-8)/150)) if 8<=f<CARD else 6
    s['fx'].append(('fn_hud',sh,hp,rr,alive))
    s['actors']=[cl,gn]
    return s

CLIPS = [clip('royale', N_, clip_royale)]
