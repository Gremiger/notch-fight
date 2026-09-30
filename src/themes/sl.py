"""Solo Leveling: Claude (Sung Jinwoo, the Shadow Monarch: dark hooded coat, glowing blue eyes,
twin daggers) vs Igris, the Blood-Red Knight, in the dim throne room. The System pops up —
[QUEST] DEFEAT IGRIS — then a fast sword duel: parries, dodges, Claude's eyes flare and he cuts
Igris down. Close-up: ARISE! Black smoke rises, the shadow army stands up and Igris returns as a
shadow to kneel behind his Monarch. LEVEL UP! The shadows sink and the knight is back in red."""
from engine import *

THEME = 'sl'
N_ = 288

# ---- sprites ---------------------------------------------------------------------------------
def _jinwoo(x,y,t,l,r,c):
    if c=='.': return None
    inside=l<=x<=r
    if inside and y in (t,t+1): return 'k'                          # the hood
    if c=='K': return 'E'                                           # glowing eyes
    if inside and y==t+4 and x in (l,r): return 'k'                 # hood sides framing the face
    if inside and y>=t+5: return 'p' if y==t+5 and l+3<=x<=r-3 else 'N'   # coat, purple collar
    if c=='o': return 'N'                                           # sleeves and boots
    return None

# a dagger in each pose's front hand (blade 'H', guard 'D')
_DAGGER={
 'guard':  lambda s: paint(s,[(13,0,'H'),(13,1,'H'),(13,2,'D')],top=1),
 'guard2': lambda s: paint(s,[(13,1,'H'),(13,2,'D')]),
 'punch':  lambda s: paint(s,[(17,5,'DHHH'),(17,6,'.hh')],right=4),
 'dash':   lambda s: paint(s,[(17,5,'DHHH'),(17,6,'.hh')],right=4),
 'charge': lambda s: paint(s,[(16,5,'DHHH'),(16,6,'.hh')],right=4),
 'armsup': lambda s: paint(s,[(1,-3,'H'),(1,-2,'H'),(1,-1,'D'),(12,-3,'H'),(12,-2,'H'),(12,-1,'D')],top=3),
}
def _jw(name,s):
    s=recolor_rows(s,_jinwoo)
    s=overlay(s,["...kk....",".kkkkkkk."],0,0)                    # hood peak
    return _DAGGER.get(name,lambda z: z)(s)
JW={k:_jw(k,v) for k,v in CL.items()}
JWPAL={'N':(40,38,62),'p':(96,56,170),'k':(22,18,32),'E':(140,210,255),'H':(226,232,255),'h':(140,150,190),'D':(120,110,150)}

_IG=S([
"..rr.................",
".rrrr.RRRRR..........",
"rr..rRRRRRRR.........",
"r...RRRRRRRRR........",
"....RRkkkkkWR........",
"....RRRRRRRRR........",
".....RRRRRRR.........",
"..cYYRRRRRRRYY.......",
".ccRRRRrRRrRRRR......",
".ccRR.RRRRRR.RR......",
".ccRR.RRRRRR.RR......",
"cccRR.YYYYYY.RR......",
"ccc...RRRRRR.YDY.....",
"ccc...RRRRRR..H......",
"cccc..RRRRRR..H......",
"cccc..RR..RR..H......",
"cccc..RR..RR..H......",
"ccc...RR..RR..H......",
"......RR..RR..h......",
".....RRR..RRR........",])
_IG2=S([(r[:2].replace('r','.')+'r'+r[3:] if i<3 else r) for i,r in enumerate(_IG)])   # plume sway
# the long sword thrust forward
_IG_ATK=S([r for r in _IG[:8]]+
          [".ccRRRRrRRrRRRRRRY.........",
           ".ccRR.RRRRRR...RRDHHHHHHHHH",
           ".ccRR.RRRRRR.....Y.........",
           "cccRR.YYYYYY................"]+
          [r[:12] for r in _IG[12:]])
# the sword raised overhead, ready to cleave
_IG_RAISE=S(["...................H..",
             "..................H...",
             ".................H....",
             "................H.....",
             "..rr...........H......",
             ".rrrr.RRRRR..YDY......",
             "rr..rRRRRRRR.RR.......",
             "r...RRRRRRRRRRR.......",
             "....RRkkkkkWRR........",
             "....RRRRRRRRR.........",
             ".....RRRRRRR..........",
             "..cYYRRRRRRRYY........",
             ".ccRRRRrRRrRR.........",
             ".ccRR.RRRRRR..........",
             ".ccRR.RRRRRR..........",
             "cccRR.YYYYYY.........."]+[r[:12] for r in _IG[12:]])
# on one knee, head bowed, the sword planted in front
_IG_KNEEL=S([
"....................",
".rr.................",
"rrrr.RRRRR..........",
"r..rRRRRRRR.........",
"...RRRRRRRRR....Y...",
"...RRkkkkkWR...YDY..",
"..cYRRRRRRRYY...H...",
".ccRRRRrRRrRRRRRH...",
".ccRR.RRRRRRR.RRH...",
"cccRR.RRRRRR....H...",
"cccRR.YYYYYY....H...",
"cccc..RRRRRRRRRRH...",
"cccc.RRR.....RR.H...",
"cccc.RR......RR.H...",
"ccc.RRRRRR...RR.h...",])
IG={'idle':_IG,'idle2':_IG2,'attack':_IG_ATK,'raise':_IG_RAISE,'kneel':_IG_KNEEL,'hurt':hurt(_IG)}
IG['down']=rotate90(IG['hurt'],3,trim=True)
def ig_idle(f): return IG['idle'] if (f//6)%2==0 else IG['idle2']
IGPAL={'R':(170,30,36),'r':(236,70,56),'c':(100,14,24),'Y':(214,168,70),'k':(22,10,12),'W':(255,120,90),
       'H':(222,226,238),'h':(150,154,174),'D':(120,100,60)}
SHPAL={'R':(60,36,94),'r':(104,60,158),'c':(34,18,56),'Y':(112,78,176),'k':(8,4,14),'W':(214,150,255),
       'H':(124,104,176),'h':(84,68,124),'D':(70,54,110)}
SH_AURA=((92,40,160),1)

SOLDIER=S([
"...kkkk...",
"..kkkkkk..",
"..kWkkWk..",
"..kkkkkk..",
"...kkkk...",
".kkkkkkkk.",
"kk.kkkk.kk",
"kk.kkkk.kk",
"...kkkk...",
"...kk.kk..",
"...kk.kk..",
"..kkk.kkk.",])
SOLDIER2=S([(r if i!=2 else "..kkkkkk..") for i,r in enumerate(SOLDIER)])   # a blink
SOLPAL={'k':(26,16,40),'W':(200,130,255)}

# ---- background ------------------------------------------------------------------------------
TORCHES=(22,163)
def _throne_room(d):
    for y in range(8,GROUND,6):                                     # the stone wall, barely visible
        off=3 if (y//6)%2 else 0
        for x in range(off,W,12): d.line([x,y,x,y+5],fill=(14,14,21))
        d.line([0,y,W,y],fill=(13,13,20))
    for x in (8,52,128,172):                                        # pillars
        d.rectangle([x,6,x+6,GROUND],fill=(24,24,36)); d.rectangle([x-1,4,x+7,6],fill=(32,32,46))
        d.rectangle([x-1,GROUND-2,x+7,GROUND],fill=(32,32,46)); d.line([x+1,7,x+1,GROUND-3],fill=(30,30,44))
    d.rectangle([83,14,103,GROUND],fill=(22,20,32))                 # the throne, far in the back
    d.polygon([(83,14),(93,6),(103,14)],fill=(22,20,32))
    d.rectangle([80,34,106,GROUND],fill=(26,24,38)); d.rectangle([86,18,100,34],fill=(18,16,26))
    for x in TORCHES: d.rectangle([x-1,26,x+1,30],fill=(40,36,50))
register_bg(THEME, lambda v: (v//2+6,v//2+6,v+14), decor=_throne_room, clip_ground=True)

# ---- effects ---------------------------------------------------------------------------------
@fx('sl_torch')
def _fx_torch(d,im,e,f):
    """Blue flames on the wall sconces (flicker on a 12-frame cycle: loop-safe)."""
    rr=random.Random(f%12)
    for x in TORCHES:
        h=4+rr.randint(0,2); d.polygon([(x-2,25),(x+2,25),(x+rr.randint(-1,1),25-h)],fill=(70,130,230))
        d.line([x,24,x,25-h+2],fill=(200,230,255))

def _brackets(d,x,y,w,c):
    for bx,dx in ((x-3,1),(x+w+1,-1)):
        d.line([bx,y-1,bx,y+5],fill=c); d.point((bx+dx,y-1),fill=c); d.point((bx+dx,y+5),fill=c)

@fx('sl_system')
def _fx_system(d,im,e,f):
    """The System window: a translucent blue panel with a light border, opened by prog 0..1
    (unfolds from a line), text once fully open. Lines: [(text, colour, bracketed)]."""
    _,cx,y0,lines,prog=e
    if prog<=0: return
    w=max(len(t) for t,_,_ in lines)*4+14; h=len(lines)*8+6
    x0=int(cx-w//2); k=ease(min(1,prog)); hh=max(1,int(h*k)); yc=y0+h//2; top=yc-hh//2
    box=(x0,top,x0+w,top+hh)
    im.paste(Image.blend(im.crop(box),Image.new('RGB',(w,hh),(14,40,110)),0.72),box[:2])
    d.rectangle([x0,top,x0+w-1,top+hh-1],outline=(150,210,255))
    if hh>4: d.rectangle([x0+2,top+2,x0+w-3,top+hh-3],outline=(50,100,190))
    if prog<1: return
    for i,(t,c,br) in enumerate(lines):
        tx=int(cx-len(t)*2); ty=y0+4+i*8
        text(d,t,tx,ty,c,shadow=(6,16,50))
        if br: _brackets(d,tx,ty,len(t)*4-1,c)
    for x,y in ((x0,top),(x0+w-1,top),(x0,top+hh-1),(x0+w-1,top+hh-1)): d.point((x,y),fill=(255,255,255))

@fx('sl_smoke')
def _fx_smoke(d,im,e,f):
    """Black-purple shadow smoke rising from the ground around x (spread), strength a 0..1."""
    _,x,spread,a,seed=e
    if a<=0: return
    rr=random.Random(seed)
    for i in range(int(26*a)):
        bx=x+rr.uniform(-spread,spread); life=rr.randint(14,26); ph=(f+rr.randint(0,life))%life; k=ph/life
        yy=GROUND+1-k*rr.uniform(16,30); xx=bx+math.sin(k*4+i)*2; r=max(1,int((1-k)*3)+rr.randint(0,1))
        c=(34,14,52) if i%3 else (72,34,120)
        d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=c)
        if i%5==0 and k<0.7: d.point((int(xx),int(yy)-r-1),fill=(170,110,255))

@fx('sl_eyes')
def _fx_eyes(d,im,e,f):
    """Eye flare: a glowing streak trailing back from each of the sprite's 'E' cells."""
    _,spr,cx,feet,flip,L=e
    ox,oy=origin(spr,cx,feet); w=len(spr[0]); dirn=-1 if not flip else 1
    for y,row in enumerate(spr):
        for x,ch in enumerate(row):
            if ch!='E': continue
            X=ox+((w-1-x) if flip else x); Y=oy+y
            for k in range(1,L+1): blend(im.load(),X+dirn*k,Y-k//3,(120,90,255),0.9*(1-k/(L+1)))
            d.point((X,Y),fill=(255,255,255))

@fx('sl_slash')
def _fx_slash(d,im,e,f):
    """A sword arc: centre, radius, start/end angle, colour (bright core + dark trail)."""
    _,x,y,r,a0,a1,c=e
    d.arc([x-r,y-r,x+r,y+r],a0,a1,fill=tuple(v//2 for v in c),width=3)
    d.arc([x-r,y-r,x+r,y+r],a0,a1,fill=c,width=1)

@fx('sl_cut')
def _fx_cut(d,im,e,f):
    """The decisive dash: a long blue-white cut line with a purple fringe."""
    _,x0,x1,y=e
    for k,c in ((-1,(90,50,170)),(1,(90,50,170)),(0,(210,236,255))): d.line([x0,y+k,x1,y+k],fill=c)

@fx('sl_after')
def _fx_after(d,im,e,f):
    """A translucent afterimage of a sprite (Claude's dodge)."""
    _,spr,x,y,flip,a=e; draw(im,spr,x,y,flip,alpha=a,tint=(90,60,170),f=f)

# ---- close-up --------------------------------------------------------------------------------
def closeup_arise(t,f):
    """Primer plano: the hooded Monarch in a purple aura, eyes blazing blue — ARISE!"""
    im=Image.new('RGB',(W,H),(8,4,16)); d=ImageDraw.Draw(im)
    rr=random.Random(f)
    aura=ease(t/0.3)
    for _ in range(int(40*aura)):                                   # aura flames behind the hood
        x=rr.randint(18,122); h=rr.randint(8,30); y=rr.randint(18,64)
        d.line([x,y,x+rr.randint(-2,2),y-h],fill=(70,30,130) if rr.random()<0.7 else (140,80,230))
    d.polygon([(26,64),(30,26),(46,6),(70,0),(94,6),(110,26),(114,64)],fill=(20,16,30))   # hood
    d.polygon([(34,64),(38,30),(52,14),(70,10),(88,14),(102,30),(106,64)],fill=(12,10,20))
    d.rectangle([44,22,96,64],fill=(217,119,87))                    # Claude's face
    d.rectangle([44,22,50,64],fill=(176,92,66))
    d.polygon([(40,20),(100,20),(96,30),(70,26),(44,30)],fill=(12,10,20))   # the hood's shadow
    g=ease((t-0.15)/0.15)
    for ex in (62,82):
        glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([ex-9,26,ex+12,50],fill=int(200*g))
        im.paste((110,80,255),(0,0),glow.filter(ImageFilter.GaussianBlur(3)))
        d=ImageDraw.Draw(im)
        d.rectangle([ex-2,32,ex+3,45],fill=tuple(int(lerp(24,v,g)) for v in (140,210,255)))
        d.rectangle([ex,34,ex+1,43],fill=tuple(int(lerp(24,v,g)) for v in (240,250,255)))
        if g>=1:                                                    # the flare trailing back
            for k in range(1,26): d.point((ex+3+k,36-k//4),fill=tuple(int(v*(1-k/26)) for v in (150,120,255)))
    if t>0.4:
        jx=(f%3)-1 if t<0.55 else 0
        big_text(im,"ARISE!",22,(214,190,255),scale=3,cx=150+jx,outline=(70,30,140))
    if t<0.06: zoom_lines(d,(160,140,255))
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

# ---- the clip --------------------------------------------------------------------------------
QUEST=[("QUEST",(255,255,255),True),("DEFEAT IGRIS",(200,230,255),False)]
LEVEL=[("SYSTEM",(255,255,255),True),("LEVEL UP!",(255,230,120),False),("IGRIS ARISEN",(200,180,255),False)]
ARMY=[(98,6),(118,0),(142,4),(160,10),(178,2),(108,14)]            # (x, rise delay) of the soldiers
FALL_X=124

def clip_arise(f):
    s=scene(f,THEME)
    cl=actor(JW[guard_pose(f)],30,pal=JWPAL); ig=actor(ig_idle(f),150,flip=True,pal=IGPAL)
    s['under'].append(('sl_torch',))
    eyes=0
    # 1) the System: a quest
    if 20<=f<56:
        p=(f-20)/6 if f<50 else 1-(f-50)/6
        s['fx'].append(('sl_system',W//2,12,QUEST,p if f<50 else max(0,p)))
    # 2) the duel: Igris charges, Claude meets him
    if 56<=f<64:
        t=(f-56)/8; ig.update(spr=IG['attack'] if f>=60 else ig_idle(f),x=ez(150,82,t)); cl.update(spr=JW['dash'],x=ez(30,50,t))
        s['fx'].append(('dust',ig['x']+10,GROUND-1))
    if 64<=f<112:
        k=(f-64)//12; ph=(f-64)%12
        cl['x']=50; ig['x']=82
        if ph<5: ig['spr']=IG['raise']
        elif ph<9: ig['spr']=IG['attack']
        if 5<=ph<8: s['fx'].append(('sl_slash',78,GROUND-8,15,190,275,(255,110,90)))
        if k%2==0:                                                   # parry: dagger meets sword
            if 4<=ph<9: cl['spr']=JW['punch']
            if ph==5: s['fx'].append(('spark',64,GROUND-8,4)); s['shake']=rshake()
            if 5<=ph<8: s['fx'].append(('twinkle',66,GROUND-9,2))
        else:                                                        # dodge back, then step in
            if 4<=ph<10:
                cl.update(spr=JW['dash'],x=50-8*math.sin(math.pi*(ph-4)/6),y=GROUND-int(5*math.sin(math.pi*(ph-4)/6)))
                if ph<8: s['fx'].append(('sl_after',JW['dash'],50,GROUND,False,0.35))
    # 3) Claude's eyes flare, the decisive cut
    if 112<=f<122:
        ig.update(spr=IG['raise'],x=82); cl.update(x=50,aura=((100,50,200),1+(f%2))); eyes=4+(f-112)
        if f<116: s['shake']=rshake()
    if 122<=f<128:
        t=(f-122)/3; cl.update(spr=JW['dash'],x=ez(50,70,t),aura=((100,50,200),1)); eyes=10
        if f<124: s['fx'].append(('sl_cut',48,ez(50,96,t),GROUND-7))
        if f==124: s['flash']=0.45; s['fc']=(80,GROUND-10); s['flashc']=(190,200,255); s['shake']=rshake(2)
        if f<124: ig.update(spr=IG['raise'],x=82)
    if 124<=f<150:
        t=(f-124)/12; ig.update(spr=IG['hurt'] if f<136 else IG['down'],x=ez(82,FALL_X,t),y=GROUND-int(10*math.sin(math.pi*min(1,t))))
        if 124<=f<130:
            for j in range(3): s['fx'].append(('shard',84+random.randint(-4,6),GROUND-random.randint(4,18),(220,40,40) if j else (255,220,200)))
        if f==136: s['fx'].append(('dust',FALL_X-8,GROUND-1)); s['fx'].append(('dust',FALL_X+8,GROUND-1)); s['shake']=rshake(1)
    if 128<=f<190: cl.update(spr=JW['punch'] if f<136 else JW[guard_pose(f)],x=70)
    # 4) close-up: ARISE!
    if 150<=f<190: s['image']=closeup_arise((f-150)/40,f); return s
    # 5) shadow extraction
    shadows=[]
    if 190<=f<262:
        cl['x']=70
        if f<204: cl['spr']=JW['armsup']; eyes=6
        smk=min(1,(f-190)/8)
        if f<236: s['under'].append(('sl_smoke',FALL_X,12,smk,11))
        for i,(x,dl) in enumerate(ARMY):                             # the army rises out of the ground
            t=(f-196-dl)/16
            if t<=0: continue
            s['under'].append(('sl_smoke',x,5,max(0,1-t/2)*0.6,20+i))
            shadows.append(actor(SOLDIER2 if (f+i*5)%40<2 else SOLDIER,x,GROUND+int(14*(1-ease(t))),flip=True,pal=SOLPAL,aura=SH_AURA))
    sig=None                                                         # Igris as a shadow
    if 190<=f<206: ig.update(spr=IG['down'],x=FALL_X,alpha=1-(f-190)/16)   # the body turns to smoke
    if 206<=f<268: ig['vis']=False
    if 206<=f<220:                                                   # Igris stands up as a shadow
        t=(f-206)/10; sig=actor(IG['idle'],FALL_X,GROUND+int(20*(1-ease(t))),flip=True,pal=SHPAL,aura=SH_AURA)
    if 220<=f<226:                                                   # ...melts, crosses to his Monarch
        sig=actor(IG['idle'],FALL_X,flip=True,pal=SHPAL,alpha=1-(f-220)/6)
        s['under'].append(('sl_smoke',FALL_X,8,1-(f-220)/6,31))
    if 222<=f<262:
        a=min(1,(f-222)/6)
        sig=actor(IG['kneel'],44,pal=SHPAL,aura=SH_AURA if a>=1 else None,alpha=a)
        if f<234: s['under'].append(('sl_smoke',44,9,1-(f-222)/12,37))
    # 6) LEVEL UP!
    if 232<=f<262:
        p=(f-232)/6 if f<256 else 1-(f-256)/6
        s['fx'].append(('sl_system',W//2,6,LEVEL,max(0,p)))
    # 7) the shadows sink, Igris is back in red on his side
    if 262<=f<280:
        t=(f-262)/12
        if t<1:
            sig=actor(IG['kneel'],44,GROUND+int(18*ease(t)),pal=SHPAL,aura=SH_AURA)
            s['under'].append(('sl_smoke',44,9,1-t,37))
            for i,(x,dl) in enumerate(ARMY):
                shadows.append(actor(SOLDIER,x,GROUND+int(14*ease(t)),flip=True,pal=SOLPAL,aura=SH_AURA))
                s['under'].append(('sl_smoke',x,5,(1-t)*0.5,20+i))
        cl.update(spr=JW[guard_pose(f)],x=ez(70,30,(f-262)/16))
    if 268<=f<282:
        t=(f-268)/12
        ig.update(vis=True,spr=ig_idle(f),x=150,flip=True,pal=IGPAL,y=GROUND,alpha=min(1,t),aura=None)
        s['under'].append(('sl_smoke',150,8,max(0,1-t)*0.8,41))
    s['actors']=shadows+([sig] if sig else [])+[cl,ig]
    if eyes: s['fx'].append(('sl_eyes',cl['spr'],cl['x'],cl['y'],cl['flip'],eyes))
    return s

CLIPS = [clip('arise', N_, clip_arise)]
