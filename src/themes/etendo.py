"""Etendo rebrand: Claude walks up to the old Etendo logo (yellow square, navy E-X glyph), grabs it,
lifts it and spins it; close-up of the morph — the yellow melts into lime while the navy strokes
break apart and fly back together as the new four-pointed star. NEW ETENDO! Claude ships it
(it rockets off the top) and the next old logo drops onto the stand for the loop."""
from engine import *

THEME = 'etendo'
N_ = 288
SZ = 28                     # logo side (art px)
STAND = 150                 # x of the display stand
REST = GROUND-10            # logo bottom when it rests on the stand
HELD = GROUND-11            # logo bottom when Claude holds it overhead (armsup top row)

OLD_TOP, OLD_BOT, NAVY = (255,228,85), (250,215,30), (32,36,82)
LIME, LIME_DK, INK = (190,240,80), (150,206,50), (22,22,22)
NEW_R = 6                   # corner radius of the new rounded square

def _supersample(inside, k=6):
    """Pixels of the SZ x SZ grid whose sub-samples fall inside(u,v) (u,v in 0..1) at least half the time."""
    pts=set()
    for y in range(SZ):
        for x in range(SZ):
            n=sum(inside((x+(i+.5)/k)/SZ,(y+(j+.5)/k)/SZ) for i in range(k) for j in range(k))
            if n*2>=k*k: pts.add((x,y))
    return pts

def _seg_dist(px,py,ax,ay,bx,by):
    dx,dy=bx-ax,by-ay; t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)))
    return math.hypot(px-ax-t*dx,py-ay-t*dy)

# Old glyph: centerlines in the source's 1080 units (box + two crossing diagonals ending in short
# bars), scaled up around the centre so the strokes survive at 28 px.
_OLD_LINES=[[(261,265),(261,815)],[(261,265),(810,265)],[(261,815),(810,815)],
            [(810,265),(605,540),(520,617),(410,617)],[(410,455),(520,455),(605,540),(810,815)]]
def _old_inside(u,v,grow=1.25,stroke=75):
    x=540+(u*1080-540)/grow; y=540+(v*1080-540)/grow
    for line in _OLD_LINES:
        for (ax,ay),(bx,by) in zip(line,line[1:]):
            if _seg_dist(x,y,ax,ay,bx,by)<=stroke/2: return True
    return False

# New glyph: a band between two concave curves on each side ("{ }" facing in), split by a thin
# vertical gap; the lime left between them is the four-pointed star.
def _new_inside(u,v,a=0.36,b=0.32):
    x=(u-0.5)/a; y=(v-0.5)/b                        # glyph box -> -1..1
    if abs(x)>1 or abs(y)>1 or abs(x)<0.10: return False
    ax,ay=abs(x),abs(y)
    if ((ax-1)/0.5)**2+((ay-1)/0.75)**2<1: return False              # outer concave corners
    if ax<0.58 and not ((ax-0.58)/0.58)**2+(ay-1)**2<1: return False  # the star
    return True

GLYPH={}
def glyph(kind):
    if kind not in GLYPH: GLYPH[kind]=_supersample(_old_inside if kind=='old' else _new_inside)
    return GLYPH[kind]

def _square(d,x0,y0,melt=0.0,radius=0):
    """The logo's square, yellow gradient melting into lime top-down as melt goes 0 -> 1."""
    m=Image.new('L',(SZ,SZ),0); ImageDraw.Draw(m).rounded_rectangle([0,0,SZ-1,SZ-1],radius=radius,fill=255)
    for y in range(SZ):
        old=tuple(int(lerp(OLD_TOP[i],OLD_BOT[i],y/(SZ-1))) for i in range(3))
        new=LIME if y<SZ-3 else LIME_DK
        for x in range(SZ):
            if not m.getpixel((x,y)): continue
            k=max(0,min(1,melt*1.7-(y/SZ)*0.7+0.06*math.sin(x*1.3)))      # drips down the columns
            d.point((x0+x,y0+y),fill=tuple(int(lerp(old[i],new[i],k)) for i in range(3)))

LOGO={}
def logo(kind):
    """RGBA SZ x SZ picture of the old or new logo."""
    if kind not in LOGO:
        im=Image.new('RGBA',(SZ,SZ),(0,0,0,0)); d=ImageDraw.Draw(im)
        _square(d,0,0,0.0 if kind=='old' else 1.0,0 if kind=='old' else NEW_R)
        for p in glyph(kind): d.point(p,fill=NAVY if kind=='old' else INK)
        LOGO[kind]=im
    return LOGO[kind]

def paste_logo(im,kind,cx,bottom,sx=1.0):
    """Paste a logo centred at cx with its bottom row just above `bottom`; sx<1 squeezes it (spin)."""
    lg=logo(kind) if isinstance(kind,str) else kind
    w=max(1,int(round(SZ*abs(sx))))
    if w!=SZ: lg=lg.resize((w,SZ),Image.NEAREST)
    if sx<0: lg=lg.transpose(Image.FLIP_LEFT_RIGHT)
    im.paste(lg,(int(round(cx-w/2)),int(bottom)-SZ),lg)

@fx('etendo_logo')
def _fx_logo(d,im,e,f):
    _,kind,cx,bottom,*rest=e; paste_logo(im,kind,cx,bottom,rest[0] if rest else 1.0)

def _studio(d):
    for x in range(0,W,23): d.line([x,0,x,GROUND-14],fill=(14,16,26))                   # wall panels
    d.line([0,GROUND-14,W,GROUND-14],fill=(22,24,36))
    d.rectangle([54,6,110,30],fill=(18,20,32),outline=(40,44,62))                          # whiteboard
    for k,(x,h) in enumerate(((60,6),(68,10),(76,8),(84,14),(92,12),(100,18))):
        d.rectangle([x,27-h,x+4,27],fill=(34,56,40) if k<5 else (60,90,40))               # a growth chart
    d.rectangle([4,GROUND-8,10,GROUND],fill=(60,40,32)); d.ellipse([1,GROUND-18,13,GROUND-7],fill=(26,52,30))  # plant
    d.rectangle([STAND-2,REST,STAND+2,GROUND],fill=(58,60,74)); d.rectangle([STAND-8,GROUND-1,STAND+8,GROUND],fill=(78,80,96))  # stand
    d.line([STAND-1,REST,STAND-1,GROUND-2],fill=(84,86,104))
register_bg(THEME, lambda v: (v,v,v+8), decor=_studio)

@fx('etendo_confetti')
def _fx_confetti(d,im,e,f):
    """Confetti falling since frame t0 (fixed trajectories)."""
    _,t0=e; k=f-t0; cols=(LIME,OLD_TOP,(255,255,255),(217,119,87),(120,200,255))
    for i in range(36):
        rr=random.Random(4200+i); x0=rr.uniform(10,W-10); v=rr.uniform(0.5,1.2); y=-rr.uniform(0,30)+k*v
        if 0<=y<GROUND:
            x=x0+math.sin(k*0.2+i)*3; c=cols[i%len(cols)]
            d.point((x,y),fill=c)
            if (k+i)%4<2: d.point((x+1,y),fill=c)

@fx('etendo_glow')
def _fx_glow(d,im,e,f):
    """Pulsing lime glow around a logo centred at (cx, cy)."""
    _,cx,cy=e; r=SZ//2+3+(f//3)%2
    d.rounded_rectangle([cx-r,cy-r,cx+r,cy+r],radius=NEW_R+3,outline=LIME)
    for k in range(4):
        a=f*0.25+k*math.pi/2; d.point((cx+math.cos(a)*(r+4),cy+math.sin(a)*(r+4)),fill=(230,255,180))

@fx('etendo_orbit')
def _fx_orbit(d,im,e,f):
    """Sparks spinning around the logo while Claude spins it."""
    _,cx,cy,r,n=e
    for k in range(n):
        a=f*0.5+k*2*math.pi/n; x,y=cx+math.cos(a)*r,cy+math.sin(a)*r*0.6
        d.point((x,y),fill=(255,255,255)); d.point((x-math.cos(a+1.6)*2,y-math.sin(a+1.6)),fill=(255,230,120))

@fx('etendo_trail')
def _fx_trail(d,im,e,f):
    _,cx,y0,y1=e; rr=random.Random(f)
    for _ in range(14):
        y=rr.uniform(y0,y1); d.point((cx+rr.randint(-SZ//2+2,SZ//2-2),y),fill=LIME if rr.random()<0.6 else (255,255,255))

# --- the morph close-up -------------------------------------------------------------------------
def _pairs():
    """Each old stroke pixel paired with a new one, both sorted by angle around the centre."""
    c=(SZ-1)/2; key=lambda p: (math.atan2(p[1]-c,p[0]-c),math.hypot(p[0]-c,p[1]-c))
    a=sorted(glyph('old'),key=key); b=sorted(glyph('new'),key=key); n=max(len(a),len(b)); rr=random.Random(77)
    return [(a[i*len(a)//n],b[i*len(b)//n],rr.random(),rr.uniform(4,12)) for i in range(n)]
PAIRS=[]

def closeup_morph(t,f):
    """Primer plano: the logo at 2x; the strokes fly apart and re-assemble into the star."""
    if not PAIRS: PAIRS.extend(_pairs())
    sm=Image.new('RGB',(W//2+1,H//2),(8,10,18)); d=ImageDraw.Draw(sm)
    cx,cy=W//4,H//4; x0,y0=cx-SZ//2,cy-SZ//2
    tt=ease((t-0.12)/0.62)
    for k in range(12):                                             # rotating light rays
        a=k*math.pi/6+f*0.04; c=tuple(int(lerp(a_,b_,tt)) for a_,b_ in zip((40,34,14),(26,44,16)))
        d.line([cx,cy,cx+math.cos(a)*80,cy+math.sin(a)*80],fill=c)
    jx,jy=(rshake(1) if t<0.14 else (0,0))
    squash=1-0.18*math.sin(math.pi*tt)
    _square(d,x0+jx,y0+jy,tt,int(round(NEW_R*tt)))
    if tt<=0:
        for p in glyph('old'): d.point((x0+p[0]+jx,y0+p[1]+jy),fill=NAVY)
    else:
        c=(SZ-1)/2
        for (ax,ay),(bx,by),dl,amp in PAIRS:
            k=ease((tt-dl*0.35)/0.65)
            x=lerp(ax,bx,k); y=lerp(ay,by,k); burst=math.sin(math.pi*k)
            ang=math.atan2(ay-c,ax-c)+burst*1.1; rad=math.hypot(ax-c,ay-c)*0.2+amp
            x+=math.cos(ang)*rad*burst; y+=math.sin(ang)*rad*burst*squash
            col=tuple(int(lerp(lerp(NAVY[i],INK[i],k),255,burst*0.7)) for i in range(3))
            d.point((x0+round(x),y0+round(y)),fill=col)
    im=sm.resize((sm.width*2,sm.height*2),Image.NEAREST).crop((0,0,W,H)); d=ImageDraw.Draw(im)
    if 0.14<=t<0.8:
        for _ in range(3): spark(d,random.randint(40,145),random.randint(4,60),random.choice((2,3)),LIME)
    if t>=0.8:                                                      # it clicks into place
        r=int((t-0.8)/0.2*80)+30; d.ellipse([W//2-r,H//2-r//2,W//2+r,H//2+r//2],outline=LIME,width=2)
    if 0.78<=t<0.86: im=fade_to(im,(255,255,240),1-abs(t-0.82)/0.04)
    if t<0.06: zoom_lines(ImageDraw.Draw(im),LIME)
    return im

# --- the clip -------------------------------------------------------------------------------------
def clip_rebrand(f):
    s=scene(f,THEME)
    cl=actor(CL[guard_pose(f)],30)
    lg=('old',STAND,REST)                                           # (kind, cx, bottom)
    sx=1.0
    # 1) Claude walks up to the old logo and studies it
    if 12<=f<44: cl['x']=lerp(30,126,(f-12)/32)
    if 44<=f<70: cl['x']=126
    if 46<=f<56: s['fx'].append(('dmg',"?",125,GROUND-19,(255,226,90)))
    if 56<=f<66: s['fx'].append(('dmg',"...",120,GROUND-19,(230,230,240)))
    # 2) grabs it and lifts it overhead
    if 64<=f<70: cl.update(spr=CL['punch'],x=128); lg=('old',STAND+(f%2),REST)
    if 70<=f<86:
        t=ease((f-70)/16); cl.update(spr=CL['armsup'],x=126)
        lg=('old',lerp(STAND,126,t),int(lerp(REST,HELD,t)-10*math.sin(math.pi*t)))
    if 86<=f<104:
        x=ez(126,92,(f-86)/16); cl.update(spr=CL['armsup'],x=x,flip=True)
        lg=('old',x,HELD-((f//3)%2))
    # 3) he spins it faster and faster
    if 104<=f<140:
        k=f-104; cl.update(spr=CL['armsup'],x=92,aura=((190,240,80),1) if k>12 else None)
        sx=math.cos(k*k*0.012); lg=('old',92,HELD)
        s['fx'].append(('etendo_orbit',92,HELD-SZ//2,SZ//2+4+k//6,3+k//8))
        if k>20: s['shake']=rshake(1)
        if k>=32: s['flash']=(k-31)/4; s['fc']=(92,HELD-SZ//2); s['flashc']=(240,255,200)
    if 108<=f<140 and (f//4)%4: callout(s,"REBRANDING...",c=(255,226,90))
    # 4) close-up: the morph
    if 140<=f<184: s['image']=closeup_morph((f-140)/44,f); return s
    # 5) the reveal
    if 184<=f<248:
        cl.update(spr=CL['armsup'],x=92); lg=('new',92,HELD-(1 if 190<=f<232 and (f//4)%2 else 0))
        s['fx'].append(('etendo_confetti',184))
        if f<232: s['under'].append(('etendo_glow',92,HELD-SZ//2))
        if f<190: s['flash']=1-(f-184)/6; s['fc']=(92,HELD-SZ//2); s['flashc']=(240,255,200)
        if 188<=f<230: s['fx'].append(('big',"NEW ETENDO!",2,LIME))
        if f%3==0: s['fx'].append(('twinkle',92+random.randint(-22,22),HELD-random.randint(2,SZ+4),random.choice((1,2))))
    # 6) ship it: it rockets off the top, and the next old logo drops onto the stand
    if 232<=f<248:
        t=(f-232)/14; b=HELD-70*t*t; lg=('new',92,b)
        s['fx'].append(('etendo_trail',92,b,min(HELD,b+18)))
        if f<236: s['shake']=rshake(1)
    if 236<=f<256: s['fx'].append(('dmg',"SHIP IT!",96,GROUND-22,LIME))
    if 246<=f<252: lg=None
    if 248<=f<278:
        cl.update(spr=CL[guard_pose(f)],x=ez(92,30,(f-248)/28),flip=f<276)
    if 252<=f<272:
        k=f-252
        if k<12: b=int(lerp(-2,REST,(k/12)**2))
        else: b=REST-int(3*math.sin(math.pi*(k-12)/8))
        lg=('old',STAND,b)
        if k==12:
            s['shake']=rshake(2)
            for j in range(4): s['fx'].append(('dust',STAND-10+j*6,GROUND-2))
    if lg and 70<=f<252: s['fx'].insert(0,('etendo_logo',*lg,sx))   # carried: over Claude
    elif lg: s['under'].append(('etendo_logo',*lg))                     # on the stand
    s['actors']=[cl]
    return s

CLIPS = [clip('rebrand', N_, clip_rebrand)]
