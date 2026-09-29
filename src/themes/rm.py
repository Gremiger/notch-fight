"""Rick and Morty: Claude (Rick: spiky blue-grey hair, unibrow, lab coat, portal gun) vs a
Cromulon, the giant floating head in the sky. "SHOW ME WHAT YOU GOT!" — Claude portal-hops
into the middle of the stage and gets schwifty; close-up of the Cromulon: "DISQUALIFIED!" Its
planet-killer beam goes into Claude's portal and comes out of another one right behind the
head. WUBBA LUBBA DUB DUB! The Cromulon floats off dazed, Claude portals home, the head
drifts back down for the loop."""
from engine import *

THEME = 'rm'
N_ = 288

RICK_PAL={'v':(150,200,228)}      # Rick's hair / unibrow (light blue-grey)
GREEN=((60,200,60),(170,255,130))   # portal fluid: rim, glow

def _rick(spr):
    spr=overlay(spr,["v...v..v....","vv.vvv.vv.v.",".vvvvvvvvvv."],-2,0)
    w=len(spr[0])
    def fn(x,y,t,l,r,c):
        if c=='.': return None
        if y==t+1 and c=='O' and x>=l+3: return 'v'                       # the unibrow
        if t+4<=y<=t+8 and c=='O' and (x<=l+1 or x>=r-1) and l<=x<=r: return 'W'   # lab coat panels
        if t+3<=y<=t+6 and (x<l or x>r):
            if x>=w-2 and c=='O': return 'D'                               # portal gun in the hand
            return 'W'                                                     # coat sleeves
        if y>=t+9: return 'q'                                              # brown pants
        return None
    return recolor_rows(spr,fn)
RICK=variant(_rick)

def gun_tip(x,pose,feet=GROUND):
    spr=RICK[pose]; w,h=len(spr[0]),len(spr)
    return int(round(x-w/2))+w, int(round(feet-h))+h-5

def _sky(d):
    rr=random.Random(51)
    for _ in range(26):
        x,y=rr.randint(0,W-1),rr.randint(1,GROUND-10); c=rr.choice([(60,60,80),(90,90,120),(50,80,60)])
        d.point((x,y),fill=c)
    d.ellipse([66,17,74,25],fill=(40,70,50)); d.arc([62,19,78,23],0,360,fill=(70,110,80))   # a ringed planet
register_bg(THEME, lambda v: (v//2,v+6,v//2+6), decor=_sky)

@fx('rm_portal')
def _fx_portal(d,im,e,f):
    """A green portal at (x,y) opened to k (0..1); vertical (standing) or horizontal (in the sky)."""
    _,x,y,k,horiz=e
    if k<=0: return
    a,b=(int(10*k)+1,int(3*k)+1) if horiz else (int(3*k)+1,int(9*k)+1)
    rim,glow=GREEN
    d.ellipse([x-a-1,y-b-1,x+a+1,y+b+1],fill=(20,90,20)); d.ellipse([x-a,y-b,x+a,y+b],fill=rim)
    d.ellipse([x-a*0.6,y-b*0.6,x+a*0.6,y+b*0.6],fill=glow)
    for j in range(6):      # the swirl
        ang=f*0.5+j*1.05; px,py=x+math.cos(ang)*a*0.8,y+math.sin(ang)*b*0.8
        d.point((px,py),fill=(230,255,210))
    if k<1:
        for j in range(4): ang=f*0.9+j*1.57; d.point((x+math.cos(ang)*(a+3),y+math.sin(ang)*(b+3)),fill=rim)

@fx('rm_glow')
def _fx_glow(d,im,e,f):
    """Portal gun muzzle glow."""
    _,x,y=e; r=1+(f%2)
    d.ellipse([x-r,y-r,x+r,y+r],fill=GREEN[1]); d.point((x,y),fill=(255,255,255))

@fx('rm_blob')
def _fx_blob(d,im,e,f):
    _,x,y=e; d.ellipse([x-2,y-2,x+2,y+2],fill=GREEN[0]); d.ellipse([x-1,y-1,x+1,y+1],fill=GREEN[1])
    d.line([x-6,y,x-3,y],fill=(40,140,40))

@fx('rm_note')
def _fx_note(d,im,e,f):
    """A music note (eighth note)."""
    _,x,y,c=e; x,y=int(x),int(y)
    d.rectangle([x,y+3,x+1,y+4],fill=c); d.line([x+1,y-1,x+1,y+3],fill=c); d.line([x+2,y-1,x+3,y],fill=c)

@fx('rm_ray')
def _fx_ray(d,im,e,f):
    """The Cromulon's planet-killer beam, at any angle (x0,y0)->(x1,y1)."""
    _,x0,y0,x1,y1=e; wob=f%2
    d.line([x0,y0,x1,y1],fill=(200,40,140),width=7+wob)
    d.line([x0,y0,x1,y1],fill=(255,140,220),width=4)
    d.line([x0,y0,x1,y1],fill=(255,255,255),width=2)
    d.ellipse([x1-3-wob,y1-3-wob,x1+3+wob,y1+3+wob],fill=(255,200,240))

SKIN,SHADE,LINE=(236,188,158),(196,142,116),(70,34,30)

@fx('rm_crom')
def _fx_crom(d,im,e,f):
    """The Cromulon head at (cx,cy). mouth 0..1 open; mood 'n' (neutral), 'talk', 'hurt'."""
    _,cx,cy,mouth,mood=e; cx,cy=int(cx),int(cy)
    d.ellipse([cx-24,cy-6,cx-16,cy+6],fill=SHADE,outline=LINE); d.ellipse([cx+16,cy-6,cx+24,cy+6],fill=SHADE,outline=LINE)  # ears
    d.ellipse([cx-19,cy-24,cx+19,cy+14],fill=SKIN,outline=LINE)          # cranium
    d.rounded_rectangle([cx-15,cy-2,cx+15,cy+23],radius=9,fill=SKIN,outline=LINE)   # the long jaw
    d.rectangle([cx-14,cy-2,cx+14,cy+8],fill=SKIN)
    d.line([cx-16,cy+4,cx-12,cy+14],fill=SHADE); d.line([cx+16,cy+4,cx+12,cy+14],fill=SHADE)   # cheekbones
    for ex in (cx-8,cx+8):
        if mood=='hurt':
            d.line([ex-3,cy-8,ex+3,cy-3],fill=LINE,width=2); d.line([ex-3,cy-3,ex+3,cy-8],fill=LINE,width=2)
        else:
            d.ellipse([ex-5,cy-9,ex+5,cy-2],fill=(250,250,250),outline=LINE)
            d.rectangle([ex-3,cy-6,ex-2,cy-5],fill=(20,14,12))                 # looking down-left at Claude
        d.line([ex-6,cy-12,ex+5,cy-10+(2 if ex<cx else 0)] if mood!='n' else [ex-6,cy-11,ex+5,cy-11],fill=LINE,width=2)  # brows
    d.line([cx,cy-4,cx-2,cy+5],fill=SHADE); d.line([cx-2,cy+5,cx+2,cy+5],fill=LINE)  # nose
    my=cy+13; m=max(0.0,min(1.0,mouth))
    if m<0.1: d.line([cx-8,my,cx+8,my],fill=LINE)
    else:
        hh=int(1+6*m); d.ellipse([cx-8,my-hh,cx+8,my+hh],fill=(60,10,20),outline=LINE)
        d.rectangle([cx-6,my-hh+1,cx+6,my-hh+2],fill=(240,240,230))           # teeth
    if mood=='hurt':
        for k in range(3): a=f*0.4+k*2.1; d.point((cx+math.cos(a)*16,cy-24+math.sin(a)*3),fill=(255,230,90))

def crom_pos(f):
    """Hovering bob (period 48 divides N_ so the loop is seamless)."""
    return 146, 28+round(2*math.sin(2*math.pi*f/48))

def closeup_crom(t,f):
    """Primer plano: the Cromulon's face fills the sky. 'DISQUALIFIED!'"""
    im=Image.new('RGB',(W,H),SKIN); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,H],fill=SKIN)
    for x0 in (0,W-14): d.rectangle([x0,0,x0+13,H],fill=SHADE)
    for ex in (52,133):
        d.ellipse([ex-24,20,ex+24,36],fill=(250,250,250),outline=LINE,width=2)
        px=ex-8+int(3*math.sin(f*0.3)) if t<0.45 else ex-10
        d.ellipse([px-4,24,px+4,32],fill=(20,14,12)); d.point((px-1,26),fill=(255,255,255))
        d.polygon([(ex-28,17),(ex+26,13),(ex+26,18),(ex-28,21)] if ex<W//2 else [(ex-26,13),(ex+28,17),(ex+28,21),(ex-26,18)],fill=LINE)  # angry brows
    d.line([92,30,86,46],fill=SHADE,width=2); d.line([84,47,100,47],fill=LINE,width=2)   # nose
    talk=t>0.3 and (f//3)%2==0
    mh=2 if t<0.3 else (8 if talk else 4)
    d.ellipse([60,56-mh,124,56+mh],fill=(60,10,20),outline=LINE,width=2)
    if mh>3: d.rectangle([66,56-mh+2,118,56-mh+3],fill=(240,240,230))
    if t>=0.3: big_text(im,"DISQUALIFIED!",2,(220,30,40))
    if t<0.06:
        zoom_lines(d)
    return im

def portal(s,x,y,f,t0,t1,horiz=False,layer='under'):
    """Open over 5 frames from t0, stay, close over 5 frames before t1."""
    if t0<=f<t1:
        k=min(1,(f-t0+1)/5,(t1-f)/5); s[layer].append(('rm_portal',x,y,k,horiz))

def clip_schwifty(f):
    s=scene(f,THEME)
    cl=actor(RICK[guard_pose(f)],30,pal=RICK_PAL)
    cx,cy=crom_pos(f); mouth=0.0; mood='n'
    # 1) SHOW ME WHAT YOU GOT!
    if 12<=f<40:
        s['fx'].append(('dmg',"SHOW ME WHAT YOU GOT!",36,2,(255,200,120))); mood='talk'; mouth=0.8 if (f//3)%2 else 0.3
    # 2) portal hop into the middle of the stage
    if 40<=f<56: cl['spr']=RICK['charge']
    if 42<=f<48: s['fx'].append(('rm_glow',*gun_tip(30,'charge')))
    if 46<=f<52: s['fx'].append(('rm_blob',lerp(46,62,(f-46)/6),GROUND-5))
    portal(s,64,GROUND-9,f,50,70)
    if 56<=f<62: cl.update(spr=RICK['dash'],x=ez(30,60,(f-56)/6))
    if 62<=f<66: cl['vis']=False
    portal(s,96,10,f,58,78,horiz=True,layer='fx')
    if 64<=f<72:
        cl.update(spr=RICK['hurt'] if f<68 else RICK['guard'],x=96,y=int(ez(24,GROUND,(f-64)/7)))
    if f>=64: cl['x']=96
    if f==71:
        for k in range(4): s['fx'].append(('dust',96+(k-2)*5,GROUND-1))
    # 3) GET SCHWIFTY
    if 74<=f<112:
        ph=(f-74)//5; cl.update(spr=RICK['armsup'] if ph%2 else RICK['guard2'],x=96+(1 if ph%4<2 else -1))
        callout(s,"GET SCHWIFTY!",c=(170,255,130))
        for k in range(3):
            u=((f-74)*1.5+k*14)%42; s['fx'].append(('rm_note',84+k*12+2*math.sin(u*0.3),50-u,[(170,255,130),(255,200,120),(150,200,228)][k]))
    if 100<=f<112: mood='talk'; mouth=0.2; cy+=1
    # 4) close-up: DISQUALIFIED!
    if 112<=f<152: s['image']=closeup_crom((f-112)/40,f); return s
    # 5) the planet-killer beam — through Claude's portals and back into the head
    if 152<=f<200: mood='talk'
    mx,my_=cx-6,cy+13
    if 152<=f<166:
        mouth=ez(0.3,1,(f-152)/8); s['fx'].append(('orbc',mx,my_,1+(f-152)//4,((200,40,140),(255,140,220))))
        s['shake']=rshake(1) if f%2 else (0,0)
    if 152<=f<164: cl['spr']=RICK['charge']
    if 154<=f<160: s['fx'].append(('rm_glow',*gun_tip(96,'charge')))
    if 156<=f<162: s['fx'].append(('rm_blob',lerp(112,120,(f-156)/6),GROUND-6))
    portal(s,118,GROUND-14,f,158,202,layer='fx')
    portal(s,178,cy-4,f,162,202,layer='fx')
    if 164<=f<194:
        mouth=1.0; x1=lerp(mx,120,min(1,(f-164)/4)); y1=lerp(my_,GROUND-14,min(1,(f-164)/4))
        s['fx'].append(('rm_ray',mx,my_,x1,y1))
        if f>=168:
            xb=lerp(176,cx+20,min(1,(f-168)/3)); s['fx'].append(('rm_ray',176,cy-4,xb,cy-4))
        if f>=171:
            mood='hurt'; s['fx'].append(('boom',cx+17,cy-4,3+(f%3))); s['shake']=rshake(2)
            if f==171: s['flash']=1.0; s['fc']=(cx+10,cy); s['flashc']=(255,190,240)
            if f%3==0: s['fx'].append(('spark',cx+random.randint(-14,18),cy+random.randint(-20,16),4))
    if 164<=f<200: cl['spr']=RICK['armsup'] if f>=172 else RICK['guard']
    if 174<=f<204: s['fx'].append(('dmg',"WUBBA LUBBA DUB DUB!",36,2,(170,255,130)))
    if 194<=f<200: mood='hurt'; mouth=0.6
    # 6) the Cromulon floats off dazed; Claude portals home
    if 200<=f<226: mood='hurt'; mouth=0.5; cy=int(ez(cy,-40,(f-200)/24)); cx+=int(3*math.sin(f*0.6))
    if 226<=f<238: cy=-60
    if 200<=f<216: cl['spr']=RICK['charge']
    if 202<=f<208: s['fx'].append(('rm_glow',*gun_tip(96,'charge')))
    if 206<=f<212: s['fx'].append(('rm_blob',lerp(112,118,(f-206)/6),GROUND-5))
    portal(s,120,GROUND-9,f,210,230)
    if 216<=f<222: cl.update(spr=RICK['dash'],x=ez(96,118,(f-216)/6))
    if 222<=f<226: cl['vis']=False
    portal(s,30,10,f,218,238,horiz=True,layer='fx')
    if 226<=f<234: cl.update(spr=RICK['hurt'] if f<230 else RICK['guard'],x=30,y=int(ez(24,GROUND,(f-226)/7)))
    if f>=226: cl['x']=30
    if f==233:
        for k in range(4): s['fx'].append(('dust',30+(k-2)*5,GROUND-1))
    # 7) the head drifts back down into place for the loop
    if 238<=f<264: cy=int(ez(-40,cy,(f-238)/24)); mood='n'
    if cy>-30: s['under'].append(('rm_crom',cx,cy,mouth,mood))
    s['actors']=[cl]
    return s

CLIPS = [clip('schwifty', N_, clip_schwifty)]
