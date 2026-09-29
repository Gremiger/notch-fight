"""Terraria: Claude (the Terrarian: brown hair, blue shirt) vs the Eye of Cthulhu, at night.
EYE OF CTHULHU HAS AWOKEN! It charges twice and sends Servants; close-up: it spins, the iris
shatters, the mouth comes out (phase 2); faster charges; HAS BEEN DEFEATED!, coins rain.
Two clips on the same scene and choreography of the Eye:
  melee    — Claude swings the Terra Blade and its green beams.
  summoner — Claude raises a staff, a Stardust Dragon coils around the Eye; a whip tags it."""
import zlib
from engine import *

THEME = 'terraria'
N_ = 264

PURPLE = (175,75,255)                  # boss messages
DMG, CRIT = (255,150,40), (255,70,40)  # damage numbers
TERRA, TERRA_HI = (60,200,90), (170,255,170)
STAR, STAR_HI = (70,150,240), (190,235,255)
# the Terrarian: brown hair, blue shirt
TPAL = {'l':(104,64,38), 'f':(72,42,24), 'a':(62,112,196), 'i':(44,84,160)}
HAIR = ["..llllllll..", ".llllllllll.", "lfllllllfll."]

def _terrarian(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(top+5,min(top+9,len(g))):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='a' if y<top+8 else 'i'
    return S([''.join(x) for x in g])
TERR=variant(_terrarian)

def _heart(d,x,y,c):
    d.point((x-1,y),fill=c); d.point((x+1,y),fill=c); d.line([x-2,y+1,x+2,y+1],fill=c)
    d.line([x-1,y+2,x+1,y+2],fill=c); d.point((x,y+3),fill=c)

def _night(d):
    """Surface at night: stars, the moon, tree silhouettes, grass + dirt blocks, the life hearts."""
    rr=random.Random(3311)
    for _ in range(40):
        x,y=rr.randint(0,W-1),rr.randint(0,40); v=rr.randint(50,120); d.point((x,y),fill=(v,v,v+30))
    d.ellipse([60,4,70,14],fill=(226,226,200)); d.ellipse([63,6,66,9],fill=(200,200,176))
    for tx,th in ((100,26),(172,32),(8,20)):
        d.rectangle([tx-1,GROUND-th,tx+1,GROUND],fill=(18,26,20))
        d.ellipse([tx-7,GROUND-th-8,tx+7,GROUND-th+6],fill=(16,30,20))
    d.rectangle([0,GROUND+1,W,GROUND+1],fill=(58,140,52))
    d.rectangle([0,GROUND+2,W,H],fill=(72,48,30))
    for x in range(0,W,4): d.line([x,GROUND+2,x,H],fill=(58,38,24))
    for i in range(5): _heart(d,162+i*5,2,(230,40,50))
register_bg(THEME, lambda v: (v//3,v,v//3), decor=_night)

# ---------------------------------------------------------------- the Eye (shared by both clips)
HOVER=(145,24); HOVER2=(140,26)
LOW=(10,GROUND-9)                                    # where a charge ends, skimming the grass
CLAUDE=(30,GROUND-6)
DASHES=((58,66,HOVER,(66,76)),(80,86,HOVER,(86,96)),(144,150,HOVER2,(150,158)),(160,166,HOVER2,(166,174)))
JUMPS=((58,72),(78,92),(142,156),(158,172))           # each peaks as the Eye passes x=30
SERVANTS=(76,82)                                       # spawn frames; they reach Claude 12 frames later
DEATH=196

def _bez(p0,p1,p2,t): return tuple((1-t)**2*p0[i]+2*(1-t)*t*p1[i]+t*t*p2[i] for i in range(2))

def eye_at(f):
    """(x, y, angle, phase, spin) of the Eye, or None when it is not on screen."""
    if f<14 or f>=DEATH or 100<=f<140: return None
    phase=1 if f<100 else 2
    home=HOVER if phase==1 else HOVER2
    bob=math.sin(f*0.2)*2
    pos=(home[0],home[1]+bob); motion=None
    if f<50: pos=(ez(200,HOVER[0],(f-14)/36),ez(-16,HOVER[1],(f-14)/36))
    for a,b,h,(r0,r1) in DASHES:
        if a-6<=f<a: pos=(h[0]+3*(a-f)/6*(1 if f%2 else -1)+4*(f-a+6)/6,h[1])        # wind-up: backs off, trembles
        if a<=f<b:
            p=((f-a)/(b-a))**1.5; pos=(lerp(h[0]+4,LOW[0],p),lerp(h[1],LOW[1],p)); motion=(-1,(LOW[1]-h[1])/(h[0]-LOW[0]))
        if r0<=f<r1: pos=_bez(LOW,(18,0),(h[0],h[1]),ease((f-r0)/(r1-r0)))
    if motion: ang=math.atan2(motion[1],motion[0])
    else: ang=math.atan2(CLAUDE[1]-pos[1],CLAUDE[0]-pos[0])
    spin=0
    if 94<=f<100: spin=((f-94)/6)**2*12
    return pos[0],pos[1],ang+spin,phase,spin

@fx('tr_eye')
def _fx_eye(d,im,e,f):
    """The Eye of Cthulhu looking along ang: trailing veins, white sclera, blue iris (phase 1) or a toothed mouth (2)."""
    _,x,y,ang,phase,tint,*r=e; R=r[0] if r else 10
    c,s=math.cos(ang),math.sin(ang)
    for k in range(4):                                         # tendrils trailing behind
        off=(k-1.5)*3; wig=math.sin(f*0.5+k*1.7)*2
        x0,y0=x-c*R*0.8-s*off,y-s*R*0.8+c*off
        x1,y1=x-c*(R+8+k%2*3)-s*(off*1.6+wig),y-s*(R+8+k%2*3)+c*(off*1.6+wig)
        d.line([x0,y0,x1,y1],fill=(170,36,40)); d.point((x1,y1),fill=(110,20,24))
    body=tint or (236,232,226)
    d.ellipse([x-R,y-R,x+R,y+R],fill=body,outline=(120,30,30))
    for k in range(6):                                         # veins across the white
        a=ang+math.pi+(k-2.5)*0.45
        d.line([x+math.cos(a)*R,y+math.sin(a)*R,x+math.cos(a)*R*0.45,y+math.sin(a)*R*0.45],fill=(200,70,70))
    if phase==1:
        ix,iy=x+c*R*0.45,y+s*R*0.45; ir=R*0.42
        d.ellipse([ix-ir,iy-ir,ix+ir,iy+ir],fill=(60,110,200)); d.ellipse([ix-ir/2,iy-ir/2,ix+ir/2,iy+ir/2],fill=(10,10,16))
        d.point((ix-ir/2,iy-ir/2),fill=(255,255,255))
    else:
        mx,my=x+c*R*0.35,y+s*R*0.35; mr=R*0.62
        d.ellipse([mx-mr,my-mr,mx+mr,my+mr],fill=(90,10,14))
        for k in range(8):
            a=k*math.pi/4+f*0.05; ex,ey=mx+math.cos(a)*mr,my+math.sin(a)*mr
            d.line([ex,ey,mx+math.cos(a)*mr*0.55,my+math.sin(a)*mr*0.55],fill=(250,246,230))

@fx('tr_servant')
def _fx_servant(d,im,e,f):
    _,x,y,ang=e; c,s=math.cos(ang),math.sin(ang)
    d.line([x,y,x-c*7,y-s*7],fill=(170,36,40))
    d.ellipse([x-3,y-3,x+3,y+3],fill=(236,232,226),outline=(120,30,30)); d.point((x+c*1.5,y+s*1.5),fill=(40,60,140))

def servant_at(f,s0):
    """A Servant of Cthulhu flying from the Eye to Claude; killed on arrival (None after)."""
    if not (s0<=f<s0+12): return None
    ex=eye_at(s0) or (HOVER[0],HOVER[1],0,1,0)
    p=(f-s0)/12; x=lerp(ex[0]-8,48,p); y=lerp(ex[1]+6,GROUND-10,p)+math.sin(p*9)*3
    return x,y,math.atan2(GROUND-10-ex[1],48-ex[0])

@fx('tr_bossbar')
def _fx_bossbar(d,im,e,f):
    """Boss life bar on the dirt strip, with a tiny eye icon."""
    _,hp=e; x0,x1,y=66,126,H-4
    d.rectangle([x0,y,x1,y+2],fill=(30,14,14),outline=(90,70,60))
    if hp>0: d.rectangle([x0+1,y+1,x0+1+int((x1-x0-2)*hp),y+1],fill=(220,40,40))
    d.ellipse([x0-7,y-1,x0-3,y+3],fill=(236,232,226)); d.point((x0-5,y+1),fill=(60,110,200))

@fx('tr_dmg')
def _fx_dmg(d,im,e,f):
    """Terraria damage number popping up: orange, crits bigger and red."""
    _,txt,x,y,k,crit=e; y=int(y-k*0.9)
    if crit is True: FX['big'](d,im,('big',txt,y-4,CRIT,int(x)),f)
    else: FX['dmg'](d,im,('dmg',txt,int(x)-len(txt)*2,y,crit or DMG),f)

@fx('tr_gore')
def _fx_gore(d,im,e,f):
    """The Eye bursting: ballistic chunks of white and red, bouncing off the grass."""
    _,x0,y0,k=e; rr=random.Random(9021)
    for i in range(22):
        vx=rr.uniform(-3,3); vy=rr.uniform(-3.5,0.5); t=k
        x=x0+vx*t; y=y0+vy*t+0.2*t*t
        if y>GROUND: y=GROUND
        c=(236,232,226) if i%3==0 else ((170,36,40) if i%3==1 else (60,110,200))
        d.rectangle([x,y,x+(1 if i%2 else 0),y+1],fill=c)

def coin_at(i,k,x0,y0):
    """Coin i, k frames after the death: burst, fall, bounce, rest on the grass."""
    rr=random.Random(700+i); vx=rr.uniform(-2.2,2.2); vy=rr.uniform(-3.2,-1.2)
    x=x0+vx*min(k,24); y=y0+vy*k+0.22*k*k
    if y>=GROUND-1:
        tl=k-(-vy+math.sqrt(vy*vy+0.88*(GROUND-1-y0)))/0.44     # frames since it touched down
        y=GROUND-1-max(0,3*math.sin(min(math.pi,tl*0.4)))*(1 if tl<8 else 0)
    return x,y

@fx('tr_coin')
def _fx_coin(d,im,e,f):
    _,x,y,i=e; x,y=int(x),int(y); gold=(250,200,50) if i%3 else (210,210,220)
    d.rectangle([x,y-1,x+1,y],fill=gold)
    if (f+i*3)%10<2: d.point((x+2,y-2),fill=(255,255,255))

def hits_before(f,hits): return sum(1 for h in hits if h<=f)

def hp_at(f,p1,p2):
    """Boss life from the hit lists: phase 1 hits take it to half, phase 2 hits to zero."""
    if f<30: return 1
    return max(0,1-0.5*hits_before(f,p1)/len(p1)-0.5*hits_before(f,p2)/len(p2))

def dmg_value(f,base,crit=False):
    v=base+zlib.crc32(f'{f}'.encode())%(base//3+1); return str(v*2 if crit else v)

def closeup_phase2(t,f):
    """Primer plano: the Eye spins faster and faster, the iris shatters, the mouth comes out."""
    im=Image.new('RGB',(W,H),(4,4,12)); d=ImageDraw.Draw(im)
    rr=random.Random(4400+f)
    for _ in range(20): d.point((rr.randint(0,W-1),rr.randint(0,H-1)),fill=(60,60,90))
    sx,sy=(rr.randint(-2,2),rr.randint(-1,1)) if t>0.4 else (0,0)
    cx,cy,R=W//2+sx,32+sy,27
    for k in range(10):                                        # veins/tendrils around the rim
        a=k*0.63+t*t*30; L=R+6+3*math.sin(f*0.6+k)
        d.line([cx+math.cos(a)*R,cy+math.sin(a)*R,cx+math.cos(a)*L,cy+math.sin(a)*L],fill=(170,36,40))
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=(236,232,226),outline=(120,30,30))
    for k in range(12):
        a=k*0.52+t*t*30; d.line([cx+math.cos(a)*R,cy+math.sin(a)*R,cx+math.cos(a)*R*0.55,cy+math.sin(a)*R*0.55],fill=(200,70,70))
    if t<0.45:                                                  # iris spinning faster and faster
        a=(t/0.45)**2*28; ix,iy=cx+math.cos(a)*9,cy+math.sin(a)*9
        d.ellipse([ix-11,iy-11,ix+11,iy+11],fill=(60,110,200)); d.ellipse([ix-5,iy-5,ix+5,iy+5],fill=(10,10,16))
        d.point((ix-4,iy-4),fill=(255,255,255))
    elif t<0.58:                                                # the iris shatters
        k=(t-0.45)/0.13
        for i in range(16):
            a=i*0.39; L=k*40
            d.rectangle([cx+math.cos(a)*L,cy+math.sin(a)*L,cx+math.cos(a)*L+2,cy+math.sin(a)*L+2],fill=(60,110,200) if i%2 else (170,36,40))
        if k<0.3:
            for i in range(10): a=i*0.63; d.line([cx,cy,cx+math.cos(a)*120,cy+math.sin(a)*60],fill=(255,255,255))
    else:                                                       # phase 2: the mouth
        d.ellipse([cx-17,cy-17,cx+17,cy+17],fill=(90,10,14))
        for k in range(12):
            a=k*math.pi/6+f*0.04
            p1=(cx+math.cos(a-0.12)*17,cy+math.sin(a-0.12)*17); p2=(cx+math.cos(a+0.12)*17,cy+math.sin(a+0.12)*17)
            d.polygon([p1,p2,(cx+math.cos(a)*9,cy+math.sin(a)*9)],fill=(250,246,230))
        d.ellipse([cx-7,cy-7,cx+7,cy+7],fill=(40,4,6))
    return im

def jump_y(f):
    for a,b in JUMPS:
        if a<=f<b: return GROUND-20*math.sin(math.pi*(f-a)/(b-a))
    return GROUND

def scene_base(f,p1,p2):
    """Everything both clips share: the Eye, its Servants, messages, boss bar, the death, the coins.
    Returns (scene, hand target for the coins' flight)."""
    s=scene(f,THEME)
    e=eye_at(f)
    if e: s['under'].append(('tr_eye',e[0],e[1],e[2],e[3],(255,160,160) if any(h<=f<h+2 for h in p1+p2) else None))
    for s0 in SERVANTS:
        sv=servant_at(f,s0)
        if sv: s['under'].append(('tr_servant',)+sv)
    if 18<=f<62: callout(s,"EYE OF CTHULHU HAS AWOKEN!",c=PURPLE)
    if 30<=f<DEATH+6: s['fx'].append(('tr_bossbar',hp_at(f,p1,p2)))
    last=max(p2)
    for i,h in enumerate(p1+p2):                               # damage numbers (only the killing blow is big)
        if h<=f<h+12:
            ex=eye_at(h) or (HOVER2[0],HOVER2[1])
            crit=h>=180; txt=dmg_value(h,24 if h<100 else 60,crit=crit)
            if h==last: s['fx'].append(('tr_dmg',txt,ex[0],ex[1]-14,f-h,True))
            else: s['fx'].append(('tr_dmg',txt,ex[0]+((i*7)%5-2)*7,ex[1]-12-(i%2)*6,f-h,CRIT if crit else False))
    dx,dy=eye_at(DEATH-1)[:2]
    if DEATH<=f<DEATH+24:
        k=f-DEATH; s['fx'].append(('tr_gore',dx,dy,k))
        if k<3: s['flash']=0.45-0.12*k; s['fc']=(int(dx),int(dy)); s['flashc']=(255,220,220)
        if k<8: s['shake']=rshake(2 if k<4 else 1)
    if DEATH+4<=f<DEATH+36: callout(s,"EYE OF CTHULHU HAS BEEN DEFEATED!",c=PURPLE)
    if DEATH<=f<244:                                           # coins: burst, rest, then fly to Claude
        for i in range(8):
            x,y=coin_at(i,min(f,228)-DEATH,dx,dy)
            if f>=228:
                p=ease((f-228-i)/10)
                if p>=1: continue
                x,y=lerp(x,34,p),lerp(y,GROUND-8,p)
            s['fx'].append(('tr_coin',x,y,i))
    return s

# ---------------------------------------------------------------- clip 1: melee (Terra Blade)
SWINGS1=(70,75,88,93); SWINGS2=(174,178,182,186,190)
TRAVEL=5
M_HITS1=tuple(a+TRAVEL for a in SWINGS1); M_HITS2=tuple(a+TRAVEL for a in SWINGS2)

@fx('tr_blade')
def _fx_blade(d,im,e,f):
    """The Terra Blade from the hand at angle a (degrees): green blade, bright edge, gold guard."""
    _,hx,hy,a,swing=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a)); L=12
    if swing:                                                   # arc trail of the swing
        for k in range(1,4):
            a2=math.radians(a-k*22); d.line([hx+c*4,hy+s*4,hx+math.cos(a2)*L,hy+math.sin(a2)*L],fill=(40,120,60))
    d.line([hx-c*2,hy-s*2,hx,hy],fill=(110,70,40))
    d.line([hx+2*c-2*s,hy+2*s+2*c,hx+2*c+2*s,hy+2*s-2*c],fill=(250,210,60))
    d.line([hx+3*c,hy+3*s,hx+L*c,hy+L*s],fill=TERRA); d.line([hx+3*c-s*0.8,hy+3*s+c*0.8,hx+L*c-s*0.8,hy+L*s+c*0.8],fill=TERRA_HI)

@fx('tr_beam')
def _fx_beam(d,im,e,f):
    """Terra Blade projectile: a green crescent with a fading trail."""
    _,x,y,ang=e; c,s=math.cos(ang),math.sin(ang)
    for k in range(5): d.point((x-c*k*2,y-s*k*2),fill=(40,120+k*10,60) if k else TERRA_HI)
    d.arc([x-5,y-5,x+5,y+5],math.degrees(ang)-70,math.degrees(ang)+70,fill=TERRA,width=2)

GRIP = {'guard':(13,4,-60), 'guard2':(13,4,-60), 'punch':(16,5,0), 'armsup':(12,0,-90), 'charge':(15,5,-30)}
def hand_of(pose,x,y):
    col,row,ang=GRIP[pose]; w=len(TERR[pose][0]); return int(round(x-w/2))+col, y-(11-row), ang

def clip_melee(f):
    s=scene_base(f,M_HITS1,M_HITS2)
    x,y=30,jump_y(f); pose=guard_pose(f)
    armed=16<=f<250
    if f in (16,17,248,249): s['fx'].append(('twinkle',40,GROUND-12,2))
    swinging=None
    for a in SWINGS1+SWINGS2:
        if a<=f<a+4: swinging=a
    if swinging is not None: pose='punch'
    if 36<=f<44: pose='charge'
    if armed:
        hx,hy,ang=hand_of(pose,x,y)
        if swinging is not None: ang=-80+(f-swinging)*30
        s['fx'].append(('tr_blade',hx,hy,ang,swinging is not None))
    for a in SWINGS1+SWINGS2:                                   # beams flying to where the Eye will be
        if a<=f<a+TRAVEL:
            tgt=eye_at(a+TRAVEL) or (HOVER2[0],HOVER2[1])
            hx,hy,_=hand_of('punch',30,jump_y(a)); p=(f-a)/TRAVEL
            s['fx'].append(('tr_beam',lerp(hx,tgt[0],p),lerp(hy,tgt[1],p),math.atan2(tgt[1]-hy,tgt[0]-hx)))
    for s0 in SERVANTS:                                         # servants cut down on arrival
        if s0+12<=f<s0+16: s['fx'].append(('spark',46,GROUND-10,4))
        if s0+12<=f<s0+24: s['fx'].append(('tr_dmg','12',44+SERVANTS.index(s0)*10,GROUND-22,f-s0-12,False))
    if 94<=f<100 or 140<=f<146: s['shake']=rshake(1)
    if 100<=f<140: s['image']=closeup_phase2((f-100)/40,f); return s
    if 244<=f<250: pose='armsup'
    s['actors']=[actor(TERR[pose],x,y,pal=TPAL)]
    return s

# ---------------------------------------------------------------- clip 2: summoner (Stardust Dragon)
PORTAL=(58,28)
BITES1=tuple(range(56,98,6)); BITES2=tuple(range(144,194,7))
WHIPS=(64,84,160)
S_HITS1=tuple(sorted(BITES1+WHIPS[:2])); S_HITS2=tuple(sorted(BITES2+WHIPS[2:]))

def dragon_head(t):
    """Where the Stardust Dragon's head is at (fractional) frame t: out of the portal, circling Claude,
    then orbiting the Eye (and coiling tight before the kill), then back home."""
    home=(46+math.cos(t*0.16)*20,30+math.sin(t*0.16)*12)
    if t<24: return PORTAL
    if t<34: return (lerp(PORTAL[0],home[0],(t-24)/10),lerp(PORTAL[1],home[1],(t-24)/10))
    e=eye_at(int(t))
    if e is None: e=eye_at(99) if 100<=t<140 else (eye_at(DEATH-1) if t>=DEATH else HOVER)
    r=18 if t<186 else lerp(18,7,(t-186)/10)
    if t>=DEATH: r=lerp(7,18,(t-DEATH)/10)
    orbit=(e[0]+math.cos(t*0.17)*r,e[1]+math.sin(t*0.17)*r*0.7)
    w=ease((t-46)/10)                                            # home -> orbit around the Eye
    if t>=DEATH+14: w=1-ease((t-DEATH-14)/14)                    # orbit -> home once it is dead
    return (lerp(home[0],orbit[0],w),lerp(home[1],orbit[1],w))

@fx('tr_dragon')
def _fx_dragon(d,im,e,f):
    """Stardust Dragon: pts from head to tail; blue plated body with a starry core, bright head with horns."""
    _,pts,keep=e
    for i in range(len(pts)-1,-1,-1):
        if ((i*37)%97)/97>=keep: continue
        x,y=pts[i]; r=4 if i==0 else (3 if i<len(pts)-4 else 2)
        d.ellipse([x-r,y-r,x+r,y+r],fill=STAR if i%2 else (50,110,210),outline=(20,40,110))
        d.point((x,y),fill=STAR_HI)
        if i==0:
            hx,hy=pts[1] if len(pts)>1 else (x-1,y); a=math.atan2(y-hy,x-hx)
            d.ellipse([x-2,y-2,x+2,y+2],fill=STAR_HI)
            d.point((x+math.cos(a)*3-math.sin(a)*2,y+math.sin(a)*3+math.cos(a)*2),fill=(255,255,255))
            for sgn in (-1,1): d.line([x-math.cos(a)*2,y-math.sin(a)*2,x-math.cos(a)*6+sgn*math.sin(a)*3,y-math.sin(a)*6-sgn*math.cos(a)*3],fill=STAR_HI)
    for i in range(0,len(pts),3):                                # twinkles along the body
        if (f+i)%6<2: x,y=pts[i]; d.point((x+2,y-3),fill=(255,255,255))

@fx('tr_portal')
def _fx_portal(d,im,e,f):
    _,x,y,k=e; r=min(8,k)
    for j in range(3):
        a=f*0.3+j*2.1; d.arc([x-r,y-r*0.7,x+r,y+r*0.7],math.degrees(a),math.degrees(a)+140,fill=STAR if j else STAR_HI)

@fx('tr_staff')
def _fx_staff(d,im,e,f):
    _,hx,hy=e; d.line([hx,hy+5,hx,hy-8],fill=(120,80,50)); d.ellipse([hx-2,hy-11,hx+2,hy-7],fill=STAR); d.point((hx,hy-9),fill=STAR_HI)

@fx('tr_whip')
def _fx_whip(d,im,e,f):
    """A whip lash from the hand to the target: a wavy line, the tip cracks with a tag mark."""
    _,x0,y0,x1,y1,k=e; p=min(1,k/3); pts=[]
    for i in range(13):
        t=i/12*p; pts.append((lerp(x0,x1,t),lerp(y0,y1,t)+math.sin(t*9+k)*3*(1-t)))
    d.line(pts,fill=(170,120,70))
    if p>=1: spark(d,int(x1),int(y1),3,STAR_HI)

def clip_summoner(f):
    s=scene_base(f,S_HITS1,S_HITS2)
    x,y=30,jump_y(f); pose=guard_pose(f)
    if 14<=f<30: pose='armsup'
    hx,hy,_=hand_of(pose,x,y)
    whip=next((w for w in WHIPS if w<=f<w+6),None)
    if whip is not None:
        pose='punch'; hx,hy,_=hand_of(pose,x,y); tgt=eye_at(whip+3) or (HOVER2[0],HOVER2[1])
        s['fx'].append(('tr_whip',hx,hy,tgt[0],tgt[1],f-whip))
    elif 14<=f<250: s['fx'].append(('tr_staff',hx,hy))
    if 18<=f<34: s['under'].append(('tr_portal',PORTAL[0],PORTAL[1],f-18))
    if 24<=f<252:                                                # the dragon: grows, bites, coils, fades to stars
        n=min(16,1+(f-24)//2) if f<140 else min(22,16+(f-140)//6)
        pts=tuple(dragon_head(f-i*0.8) for i in range(n))
        keep=1 if f<236 else max(0,1-(f-236)/14)
        s['fx'].append(('tr_dragon',pts,keep))
        if f>=236:
            for i in range(0,n,2):
                if (f+i)%3==0: s['fx'].append(('twinkle',pts[i][0],pts[i][1],1))
    for b in BITES1+BITES2:
        if b<=f<b+2:
            e=eye_at(b)
            if e: s['fx'].append(('spark',e[0]+math.cos(b*0.17)*8,e[1]+math.sin(b*0.17)*6,3))
    for s0 in SERVANTS:                                          # the dragon snaps up the servants
        if s0+12<=f<s0+16: s['fx'].append(('spark',46,GROUND-10,4))
        if s0+12<=f<s0+24: s['fx'].append(('tr_dmg','12',44+SERVANTS.index(s0)*10,GROUND-22,f-s0-12,False))
    if 94<=f<100 or 140<=f<146: s['shake']=rshake(1)
    if 100<=f<140: s['image']=closeup_phase2((f-100)/40,f); return s
    if 244<=f<250: pose='armsup'
    s['actors']=[actor(TERR[pose],x,y,pal=TPAL)]
    return s

CLIPS = [clip('melee', N_, clip_melee), clip('summoner', N_, clip_summoner)]
