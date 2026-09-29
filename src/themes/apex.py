"""Apex Legends: Claude (a jump-pack Legend with an antenna) vs Wraith, with the Apex HUD (shield
and health bottom-left, the enemy's bar over her head, ring and squads up top). Claude redeploys,
the dropship passes and he dives back in on a jumpmaster trail; he cracks Wraith's shield, she
phases INTO THE VOID and slashes his shield off, opens a DIMENSIONAL RIFT, he GRAPPLEs after her
and knocks her. Close-up of Claude's Legend banner as KILL LEADER, the finisher leaves a death
box, YOU ARE THE CHAMPION — then the dropship respawns her through the beacon beam for the loop."""
from engine import *

THEME = 'apex'
N_ = 288

def _legend(x,y,t,l,r,c):
    inside=l<=x<=r
    if c=='.':
        if l-2<=x<=l-1 and t+1<=y<=t+4: return 'r' if y==t+4 else 'd'   # jump pack on the back
        return None
    if inside and t+5<=y<=t+7: return 'L'                                   # blue armour vest
    if inside and y==t+8: return 'Y' if x==(l+r)//2 else 'k'                # belt + buckle
    return None
LEGEND=variant(lambda s: recolor_rows(overlay(s,["Y","k"],6,0),_legend))

W_ROWS=[
"...111..........","..11111111......",".1111111111.....",".11ssssss11.....","..1s2ss2s1......",
"..1ssssss1......","...ssssss.......","....ssss........","..33333333......",".3334333343.....",
".ss.333333.ss...",".ss.3VVV33.ss...",".44.333333.44...","....444444......","....33..33......",
"....33..33......","....33..33......","....44..44......","...444..444.....",]
WRAITH=poses(S(W_ROWS),10,'W',3)                                           # the attack holds the kunai
WRAITH['knock']=hurt(S(W_ROWS[:13]+["...33333333.....","..444444444....."]))
WPAL={'1':(78,66,96),'2':(210,130,255),'3':(70,62,92),'4':(46,40,62)}
VOID=(160,90,255)

SHIP=S(["......HHHHHH..........","..HHHHDDDDDDHHHHHH....","HHDDDDkkkDDDDDDDDDHHH.",
        "DDDDDDdddddddddDDDDDDD",".ddddd..........ddddd."])
BOX=S(["YYYYYYYYYY","YqqqqqqqqY","YqYYqqYYqY","YqqqqqqqqY","YqqqqqqqqY","YYYYYYYYYY"])
SHIELD=(170,80,255)   # purple (evo) shields on both

def _stage(d):
    d.polygon([(0,GROUND),(20,40),(34,46),(52,32),(76,GROUND)],fill=(18,18,28))
    d.polygon([(96,GROUND),(122,36),(138,44),(150,30),(174,GROUND)],fill=(16,16,26))
    d.rectangle([60,26,62,GROUND],fill=(24,22,34)); d.rectangle([56,24,66,25],fill=(34,30,46))   # a jump tower
register_bg(THEME, lambda v: (v//2+4,v//2+2,v), decor=_stage)

@fx('apex_ring')
def _fx_ring(d,im,e,f):
    """The ring wall shimmering at the right edge."""
    px=im.load()
    for x in range(177,W):
        for y in range(0,GROUND+1):
            if (x+y*3+f//3)%4<2: blend(px,x,y,(210,60,90),0.12+0.05*(x-177))

@fx('apex_hud')
def _fx_hud(d,im,e,f):
    """Bottom-left: segmented shield over health. Top-left: ring. Top-right: squads left."""
    _,sh,hp,closing,squads=e
    for k in range(4):
        x0=4+k*12; fill=max(0,min(1,sh*4-k)); d.rectangle([x0,60,x0+10,61],fill=(40,30,56))
        if fill>0: d.rectangle([x0,60,x0+int(10*fill),61],fill=SHIELD)
    d.rectangle([4,62,50,63],fill=(70,24,24))
    if hp>0: d.rectangle([4,62,4+int(46*hp),63],fill=(232,232,238))
    col=(240,70,90) if closing else (200,200,210)
    d.ellipse([3,2,9,8],outline=col); d.point((6,5),fill=col)
    if not closing: text(d,"RING 2",12,3,col)
    elif (f//4)%2: text(d,"RING CLOSING",12,3,col)
    t="SQUADS "+str(squads); text(d,t,W-4-len(t)*4,3,(200,200,210))

@fx('apex_ebar')
def _fx_ebar(d,im,e,f):
    """The enemy's shield/health bar floating over her head."""
    _,x,y,sh,hp=e; x=int(x)-10
    for k in range(4):
        x0=x+k*5; fill=max(0,min(1,sh*4-k)); d.rectangle([x0,y,x0+3,y],fill=(40,30,56))
        if fill>0: d.rectangle([x0,y,x0+int(3*fill),y],fill=SHIELD)
    d.rectangle([x,y+2,x+18,y+2],fill=(70,24,24))
    if hp>0: d.rectangle([x,y+2,x+int(18*hp),y+2],fill=(232,232,238))

@fx('apex_ship')
def _fx_ship(d,im,e,f):
    _,x,y=e
    draw(im,SHIP,x,y,False)
    for k in range(2): d.point((int(x)-12-k,int(y)-2+(f%2)),fill=(120,200,255))

@fx('apex_trail')
def _fx_trail(d,im,e,f):
    """Jumpmaster trail: an orange ribbon along the dive path, fading at the tail."""
    _,pts=e
    for i,(x,y) in enumerate(pts):
        a=(i+1)/len(pts); c=(int(255*a),int(150*a),int(40*a))
        d.rectangle([x,y,x+1,y+1],fill=c)

@fx('apex_crack')
def _fx_crack(d,im,e,f):
    """Shield break: purple shards bursting outward from a point, t in 0..1."""
    _,x,y,t,seed=e; rr=random.Random(seed)
    for _ in range(14):
        a=rr.random()*6.28; sp=rr.uniform(6,16); px,py=x+math.cos(a)*sp*t,y+math.sin(a)*sp*t*0.7
        c=(230,200,255) if rr.random()<0.4 else SHIELD
        d.polygon([(px,py-1),(px+1,py),(px,py+1)],fill=c)
    if t<0.3: d.ellipse([x-6,y-8,x+6,y+8],outline=(230,200,255))

@fx('apex_portal')
def _fx_portal(d,im,e,f):
    _,x,o=e
    if o<=0: return
    w,h=max(1,int(4*o)),max(1,int(11*o)); y=GROUND-11
    d.ellipse([x-w-1,y-h-1,x+w+1,y+h+1],fill=(80,30,150)); d.ellipse([x-w,y-h,x+w,y+h],fill=(14,0,30))
    d.ellipse([x-w,y-h,x+w,y+h],outline=VOID)
    for k in range(4):
        a=f*0.5+k*1.57; d.point((x+math.cos(a)*(w+3),y+math.sin(a)*(h+2)),fill=(220,180,255))

@fx('apex_void')
def _fx_void(d,im,e,f):
    """Streaks left behind while phasing."""
    _,x0,x1=e; rr=random.Random(f)
    for _ in range(6):
        y=GROUND-rr.randint(2,18); xa=rr.uniform(min(x0,x1),max(x0,x1)); d.line([xa,y,xa+rr.randint(3,8),y],fill=VOID)

@fx('apex_grapple')
def _fx_grapple(d,im,e,f):
    _,x0,y0,x1,y1=e
    d.line([x0,y0,x1,y1],fill=(170,176,196))
    d.line([x1,y1-2,x1+2,y1],fill=(250,210,60)); d.line([x1,y1+2,x1+2,y1],fill=(250,210,60))

@fx('apex_kshield')
def _fx_kshield(d,im,e,f):
    """Knockdown shield: a red arc held in front of the knocked Legend."""
    _,x,y=e
    d.arc([x-6,y-9,x+6,y+9],110,250,fill=(230,50,50),width=2)

@fx('apex_beam')
def _fx_beam(d,im,e,f):
    """Respawn light column from the dropship down to the beacon."""
    _,x,y0,a=e; px=im.load()
    for yy in range(int(y0),GROUND+1):
        for xx in range(int(x)-6,int(x)+7):
            k=1-abs(xx-x)/7; blend(px,xx,yy,(110,210,255),a*k*(0.5+0.2*((yy+f)%3==0)))
    d.rectangle([x-5,GROUND-1,x+5,GROUND],fill=(80,170,255))

@fx('apex_band')
def _fx_band(d,im,e,f):
    """The CHAMPION banner: a dark red slanted band that slides in from the left."""
    _,a=e
    if a<=0: return
    px=im.load(); w=int(W*a)
    for y in range(16,42):
        for x in range(0,min(W,w+(41-y)//2)):
            c=(130,16,22) if 18<=y<=39 else (230,60,50)
            blend(px,x,y,c,0.9)
    if a>=1:
        text(d,"YOU ARE THE",W//2-22,19,(240,240,240))
        FX['big'](d,im,('big',"CHAMPION",26,(255,214,90)),f)

def holo(spr,prog,f):
    """draw_holo() without its pal-less draw: reveal from the feet up with scanline flicker."""
    cut=int(len(spr)*(1-prog)); full=prog>=1
    return S([r if (i>=cut and (full or (i+f)%3)) else '.'*len(r) for i,r in enumerate(spr)])

def track(f,marks,refill=(256,276)):
    """A bar value from (frame, value) drops, each draining over 4 frames; refills for the loop."""
    v=1.0
    for t0,val in marks:
        if f>=t0: v=lerp(v,val,(f-t0)/4)
    if f>=refill[0]: v=lerp(v,1.0,(f-refill[0])/(refill[1]-refill[0]))
    return v
SH_C=[(100,0.5),(104,0.0)]; HP_C=[(108,0.62)]
SH_W=[(64,0.75),(68,0.5),(72,0.25),(76,0.0)]; HP_W=[(142,0.35),(146,0.0)]

def pop(s,f,t0,txt,x,y,c):
    if t0<=f<t0+10: s['fx'].append(('dmg',txt,x,y-(f-t0)//2,c))

def closeup_banner(t,f):
    """Primer plano: Claude's Legend banner — the face, antenna, KILL LEADER crown and stats."""
    im=Image.new('RGB',(W,H),(16,8,10)); d=ImageDraw.Draw(im)
    for k in range(-2,8): x=k*18; d.polygon([(x,64),(x+8,64),(x+30,0),(x+22,0)],fill=(40,12,16))
    d.polygon([(0,0),(84,0),(74,64),(0,64)],fill=(26,10,14)); d.line([(84,0),(74,64)],fill=(210,40,40))
    # the face
    fx0=96; d.rectangle([fx0,14,fx0+64,64],fill=(217,119,87)); d.rectangle([fx0,50,fx0+64,64],fill=(60,90,220))
    d.rectangle([fx0-10,26,fx0-1,46],fill=(110,110,126)); d.rectangle([fx0-10,44,fx0-1,46],fill=(220,40,40))
    blink=(f%24)<2
    for ex in (fx0+34,fx0+52):
        if blink: d.rectangle([ex-3,30,ex+3,31],fill=(24,14,12))
        else: d.rectangle([ex-3,24,ex+3,37],fill=(24,14,12))
    d.rectangle([fx0+44,4,fx0+45,14],fill=(30,28,40)); d.rectangle([fx0+43,1,fx0+46,4],fill=(250,210,60))
    # the kill leader crown drops onto his head
    cy=int(ez(-14,4,(t-0.2)/0.2))
    if t>0.2:
        cx=fx0+22; col=(250,200,60)
        d.polygon([(cx-9,cy+8),(cx-9,cy),(cx-5,cy+4),(cx,cy-2),(cx+5,cy+4),(cx+9,cy),(cx+9,cy+8)],fill=col)
        d.rectangle([cx-9,cy+7,cx+9,cy+9],fill=(200,140,30)); d.point((cx,cy+5),fill=(220,40,40))
    FX['big'](d,im,('big',"CLAUDE",6,(240,240,240),40),f)
    if t>0.4 and (t>0.5 or (f//2)%2): text(d,"KILL LEADER",18,22,(240,70,70))
    k=ease((t-0.5)/0.35)
    if t>0.5:
        text(d,"KILLS "+str(int(20*k)),6,36,(250,210,60))
        text(d,"DAMAGE "+str(int(4012*k)),6,46,(200,200,210))
    if t>0.4 and t<0.5: spark(d,fx0+22,4,6)
    if t<0.06:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    return im

HAND_Y=GROUND-6
def clip_champion(f):
    s=scene(f,THEME)
    cl=actor(LEGEND[guard_pose(f)],30); wr=actor(WRAITH['idle'],150,flip=True,pal=WPAL)
    s['under'].append(('apex_ring',))
    closing=12<=f<60; squads=1 if 222<=f<270 else 2
    ebar=True
    # 1) redeploy: crouch, the jump pack fires, he shoots off the top
    if 12<=f<18: cl['spr']=LEGEND['charge']; cl['y']=GROUND+1
    if 16<=f<20: s['fx'].append(('smoke',30,GROUND-1,3+(f-16),(120,120,130)))
    if 18<=f<28:
        k=(f-18)/10; cl.update(spr=LEGEND['armsup'],y=int(lerp(GROUND,-8,ease(k)*1.1)))
        for j in range(3): s['fx'].append(('mote',30+random.randint(-2,2),cl['y']+j*2+1,(255,160,40)))
    if 28<=f<38: cl['vis']=False
    if 20<=f<56: s['under'].append(('apex_ship',lerp(-20,208,(f-20)/36),12))
    if 30<=f<50: callout(s,"DROPPING IN",y=14,c=(255,170,60))
    # 2) the dive on the jumpmaster trail
    if 38<=f<58:
        path=lambda u:(lerp(14,56,u),lerp(-6,GROUND,u))
        u=ease((f-38)/20); x,y=path(u)
        cl.update(spr=LEGEND['dash'],x=x,y=y)
        s['under'].append(('apex_trail',[tuple(int(v) for v in path(u*i/14)) for i in range(15)]))
    if 58<=f<62: cl.update(x=56); s['fx'].append(('ring',56,GROUND,4+(f-58)*3,(200,200,210)))
    if f==58: s['shake']=rshake(2)
    if 58<=f<116: cl['x']=56
    # 3) crack her shield
    if 62<=f<80:
        cl['spr']=LEGEND['punch']
        if f%2==0: s['fx'].append(('tracer',66,142,HAND_Y))
        if f%4==0: s['fx'].append(('spark',143,HAND_Y,2))
    for i,t0 in enumerate((64,68,72,76)): pop(s,f,t0,"25",134+i*7,30-i*2,SHIELD)
    if 76<=f<84: wr['spr']=WRAITH['hurt']; s['fx'].append(('apex_crack',150,GROUND-12,(f-76)/8,76))
    if 76<=f<88: callout(s,"SHIELD BROKEN",y=14,c=(220,190,255))
    # 4) INTO THE VOID: she phases across to Claude
    if 84<=f<88: wr['aura']=(VOID,1)
    if 86<=f<98:
        x=ez(150,80,(f-86)/12); wr.update(x=x,tint=(150,90,255),alpha=0.45); ebar=False
        s['under'].append(('apex_void',x,150))
    if 88<=f<104: callout(s,"INTO THE VOID",y=14,c=(200,150,255))
    # 5) she comes out slashing: Claude's shield breaks
    if 98<=f<112:
        wr.update(x=80,tint=None,alpha=1.0); ph=(f-98)%4
        wr['spr']=WRAITH['attack'] if ph<2 else WRAITH['idle']
    if f in (100,104,108): s['fx'].append(('spark',64,HAND_Y-2,4)); s['shake']=rshake()
    if 100<=f<112: cl['spr']=LEGEND['hurt']
    if 104<=f<112: s['fx'].append(('apex_crack',56,GROUND-8,(f-104)/8,104))
    pop(s,f,100,"38",40,34,SHIELD); pop(s,f,104,"37",58,30,SHIELD); pop(s,f,108,"28",74,34,(240,240,240))
    if 108<=f<116: cl['x']=ez(56,44,(f-108)/6)
    if 116<=f<132: cl['x']=44
    # 6) DIMENSIONAL RIFT: portal at her feet, out the other end
    po=0
    if 112<=f<140: po=min(1,(f-112)/5) if f<134 else 1-(f-134)/6
    s['under'].append(('apex_portal',94,po)); s['under'].append(('apex_portal',160,po))
    if 112<=f<122: wr.update(spr=WRAITH['idle'],x=ez(80,94,(f-112)/8))
    if 118<=f<122: wr['alpha']=1-(f-118)/4
    if 122<=f<126: wr['vis']=False; ebar=False
    if 126<=f<142: wr.update(x=160,alpha=min(1,(f-126)/4))
    if 112<=f<130: callout(s,"DIMENSIONAL RIFT",y=14,c=(200,150,255))
    # 7) GRAPPLE! Claude reels himself onto her and knocks her
    if 124<=f<130: cl['spr']=LEGEND['charge']
    if 128<=f<132: s['fx'].append(('apex_grapple',52,HAND_Y,lerp(52,150,(f-128)/4),GROUND-14))
    if 132<=f<142:
        x=ez(44,140,(f-132)/10); cl.update(spr=LEGEND['dash'],x=x,y=GROUND-int(8*math.sin(math.pi*(f-132)/10)))
        s['fx'].append(('apex_grapple',x+8,cl['y']-6,150,GROUND-14))
    if 130<=f<146: callout(s,"GRAPPLE!",y=14,c=(250,210,60))
    if 142<=f<150: cl.update(spr=LEGEND['punch'],x=140,y=GROUND); wr['spr']=WRAITH['hurt']
    if f in (142,146):
        s['fx'].append(('spark',152,HAND_Y-2,6)); s['shake']=rshake(2); s['flash']=0.35; s['fc']=(152,GROUND-10)
    pop(s,f,142,"52",150,30,(240,240,240)); pop(s,f,146,"36",164,20,(240,240,240))
    if 150<=f<164: cl.update(spr=LEGEND[guard_pose(f)],x=ez(140,126,(f-150)/8))
    if 148<=f<222:
        wr.update(spr=WRAITH['knock'],x=160-(1 if (f//6)%2 else 0),alpha=1.0); ebar=False
        s['fx'].append(('apex_kshield',151,GROUND-8))
    if 148<=f<164: s['fx'].append(('big',"KNOCKED",24,(240,60,60)))
    # 8) close-up: the Legend banner, KILL LEADER
    if 164<=f<204: s['image']=closeup_banner((f-164)/40,f); return s
    # 9) the finisher, a death box, CHAMPION
    if 204<=f<212: cl.update(spr=LEGEND[guard_pose(f)],x=ez(126,140,(f-204)/8))
    if 212<=f<218: cl.update(spr=LEGEND['armsup'],x=140,y=GROUND-int(6*math.sin(math.pi*(f-212)/6)))
    if 218<=f<250: cl.update(spr=LEGEND['punch'] if f<226 else LEGEND[guard_pose(f)],x=140)
    if f==220: s['flash']=0.6; s['fc']=(158,GROUND-8); s['shake']=rshake(2); s['fx'].append(('boom',158,GROUND-8,5))
    if 220<=f<226: s['fx'].append(('smoke',160,GROUND-5,4,(90,70,120)))
    if 222<=f<258:
        wr.update(spr=BOX,x=160,pal=None,aura=((250,210,60),1),alpha=1.0 if f<252 else 1-(f-252)/6); ebar=False
    if 226<=f<254: s['fx'].append(('apex_band',min(1,(f-226)/6)))
    # 10) the dropship respawns her through the beacon beam; Claude walks home
    if 248<=f<276:
        k=(f-248)/28
        sx=ez(-20,150,k/0.36) if k<0.36 else (150 if k<0.78 else ez(150,210,(k-0.78)/0.22))
        s['under'].append(('apex_ship',sx,10))
    if 258<=f<272:
        s['under'].append(('apex_beam',150,11,min(1,(f-258)/3,(272-f)/3)))
        wr.update(spr=holo(WRAITH['idle'],min(1,(f-258)/10),f),x=150,pal=WPAL,aura=None,alpha=0.85 if f<268 else 1.0); ebar=f>=268
    if 250<=f<272: cl.update(spr=LEGEND[guard_pose(f)],x=ez(140,30,(f-250)/20),y=GROUND)
    if ebar and wr['vis']:
        s['fx'].append(('apex_ebar',wr['x'],GROUND-len(WRAITH['idle'])-5,track(f,SH_W),track(f,HP_W)))
    s['fx'].append(('apex_hud',track(f,SH_C),track(f,HP_C),closing,squads))
    s['actors']=[wr,cl]
    return s

CLIPS = [clip('champion', N_, clip_champion)]
