"""Alien: Claude (a warrant-officer survivor: curly hair, olive tank top, cargo pants, a pulse rifle)
vs the Xenomorph, aboard a dark industrial spaceship hangar. Something lurks in the ceiling vent.
The MOTION TRACKER: beep... beep-beep, the range drops to zero — IN THE ROOM. It drops from the
vent; the rifle can't stop it; close-up of the glossy head, the inner jaw shoots out at the camera.
Claude climbs into the POWER LOADER — GET AWAY FROM HER! — two hydraulic punches, acid blood
sizzles through the floor; a claw slams the airlock button: AIRLOCK OPEN, decompression, the
Xenomorph clings to the door frame, lets go and is blown into space. The door shuts, the loader
walks back to its dock... and the next one is already watching from the vent."""
from engine import *

THEME = 'alien'
N_ = 348
CX = 32            # Claude's neutral spot (the loader dock is on the left)
DOCK = 20          # loader centre when parked
VENT = (94,110)    # the ceiling vent's x span
DOOR = (160,183)   # airlock opening x span
DOOR_Y = 16        # top of the airlock opening
PANEL = (124,36)   # airlock button on the wall

# Theme colours live in each actor's `pal` (no PAL.update: other themes are added in parallel).
RIP_PAL={'1':(66,42,30),'2':(134,128,86),'3':(78,84,62),'4':(36,32,30)}
XENO_PAL={'k':(20,20,28),'r':(56,62,80),'h':(116,128,156),'H':(210,218,234),'T':(222,226,214),'m':(110,28,36)}
XENO_LIT=dict(XENO_PAL,k=(34,36,50),r=(86,94,120),h=(150,164,196))    # rim-lit by the planet outside
LOAD_BASE={'Y':(236,178,36),'y':(160,110,22),'z':(34,28,22),'g':(84,86,96),'c':(136,140,152),'w':(214,218,226)}
ACID=(200,244,40); ACID2=(120,190,20)
AMBER=(255,160,30)
GREEN=(70,255,110)

def load_pal(beacon=0.0):
    p=dict(LOAD_BASE); k=max(0,min(1,beacon))
    p['a']=tuple(int(lerp(a,b,k)) for a,b in zip((90,50,16),(255,190,60)))
    return p

# ---- Claude: the survivor ---------------------------------------------------------------------
def _ripley(spr):
    spr=overlay(spr,[".1.11.1.","11111111"],0,0)                        # curly hair
    g=[list(r) for r in spr]; h=len(g); top,l,r=body_box(spr)
    for y in range(h):
        for x,c in enumerate(g[y]):
            if c=='.': continue
            inside=l<=x<=r
            if y>=h-1: g[y][x]='4'                                        # boots
            elif y>=h-3: g[y][x]='3'                                      # cargo pants
            elif inside and y-top>=5: g[y][x]='2'                         # tank top
            elif inside and y==top: g[y][x]='1'
            elif inside and x==l and y-top in (1,2): g[y][x]='1'          # hair at the back
    return S([''.join(r) for r in g])
RIP=variant(_ripley)
_HAND={'charge':(15,5),'guard':(13,4),'guard2':(13,5)}

# ---- the Xenomorph (built from a skeleton, native facing right) --------------------------------
XW,XH=48,28
_CH={1:'k',2:'r',3:'h',4:'H',5:'T',6:'m'}
def _rot(p,a): x,y=p; return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))
def _add(a,b): return (a[0]+b[0],a[1]+b[1])

def _xeno(hip,sh,tilt=0.0,jaw=0,tongue=0,elbow=None,hand=None,hand2=None,tail=((-10,8),(-19,-6)),
          legs='crouch'):
    im=Image.new('L',(XW,XH),0); d=ImageDraw.Draw(im)
    hx,hy=hip
    # tail: a quadratic curve from the hip, thick then thin, segmented, with a blade tip
    p0=(hx-2,hy+1); p1=_add(hip,tail[0]); p2=_add(hip,tail[1]); pts=[]
    for i in range(17):
        s=i/16; pts.append(((1-s)**2*p0[0]+2*(1-s)*s*p1[0]+s*s*p2[0],(1-s)**2*p0[1]+2*(1-s)*s*p1[1]+s*s*p2[1]))
    for i in range(16): d.line([pts[i],pts[i+1]],fill=1,width=2 if i<7 else 1)
    for i in range(2,16,3): d.point(pts[i],fill=2)
    dx,dy=p2[0]-p1[0],p2[1]-p1[1]; L=math.hypot(dx,dy) or 1; ux,uy=dx/L,dy/L
    d.polygon([(p2[0]+ux*4,p2[1]+uy*4),(p2[0]-uy*1.5,p2[1]+ux*1.5),(p2[0]+uy*1.5,p2[1]-ux*1.5)],fill=3)
    # legs: digitigrade (thigh forward, shin back, toe forward); the far one in shade
    if legs=='crouch':
        LG=[(2,(hx-2,hy+4),(hx-5,hy+8),(hx-2,XH-1)),(1,(hx+5,hy+4),(hx+1,hy+8),(hx+5,XH-1))]
    elif legs=='stride':
        LG=[(2,(hx-4,hy+4),(hx-9,hy+7),(hx-7,XH-1)),(1,(hx+6,hy+3),(hx+4,hy+8),(hx+8,XH-1))]
    else:                                                                # streaming (cling / fall)
        LG=[(2,(hx-6,hy+1),(hx-12,hy+3),(hx-15,hy+2)),(1,(hx-5,hy+3),(hx-11,hy+5),(hx-14,hy+5))]
    for c,knee,ank,toe in LG:
        d.line([hip,knee],fill=c,width=3); d.line([knee,ank],fill=c,width=2); d.line([ank,toe],fill=c,width=1)
    # far arm
    if hand2: d.line([_add(sh,(-1,1)),_add(sh,(1,6)),hand2],fill=2,width=1)
    # torso + ribs + dorsal tubes
    d.line([hip,sh],fill=1,width=5)
    vx,vy=sh[0]-hip[0],sh[1]-hip[1]; vl=math.hypot(vx,vy) or 1; nx,ny=-vy/vl,vx/vl    # n points to the belly
    if ny<0: nx,ny=-nx,-ny
    for t in (0.25,0.45,0.65):
        p=(hip[0]+vx*t,hip[1]+vy*t); d.line([(p[0]+nx,p[1]+ny),(p[0]+nx*2.5,p[1]+ny*2.5)],fill=2)
        d.point((p[0]-nx*0.5+vx/vl,p[1]-ny*0.5+vy/vl),fill=2)
    for t in (0.5,0.72,0.92):
        p=(hip[0]+vx*t-nx*2,hip[1]+vy*t-ny*2); e=(p[0]-nx*3-vx/vl*2,p[1]-ny*3-vy/vl*2)
        d.line([p,e],fill=1,width=1); d.point(e,fill=3)
    # legs' highlight
    d.point((hx+2,hy+1),fill=3)
    # neck + head (a long glossy dome swept back, jaws at the front)
    nk=_add(sh,(3,-1)); d.line([sh,nk],fill=1,width=3)
    P=lambda q: _add(nk,_rot(q,tilt))
    dome=[(8,0),(7,2),(3,3),(-1,2),(-4,0),(-9,-4),(-13,-8),(-14,-10),(-11,-10),(-6,-7),(-1,-4),(4,-2)]
    d.polygon([P(q) for q in dome],fill=1)
    if jaw:
        d.polygon([P(q) for q in ((-1,2),(6,2+jaw),(6,3+jaw),(1,4+jaw))],fill=1)
        d.polygon([P(q) for q in ((1,2),(7,2),(6,2+jaw),(1,3))],fill=6)
        for x in (2,4,6): d.point(P((x,2)),fill=5); d.point(P((x-1,2+jaw)),fill=5)
    else:
        for x in (3,5,7): d.point(P((x,2)),fill=5)
    if tongue:
        y0=2+jaw/2; d.line([P((3,y0)),P((6+tongue,y0))],fill=2,width=1)
        d.point(P((7+tongue,y0-1)),fill=5); d.point(P((7+tongue,y0+1)),fill=5)
    d.line([P(q) for q in ((-12,-9),(-7,-7),(-2,-4),(3,-2))],fill=3)
    d.point(P((-8,-7)),fill=4); d.point(P((-7,-7)),fill=4)
    # near arm with claws
    elbow=elbow or _add(sh,(2,6)); hand=hand or _add(sh,(5,10))
    d.line([sh,elbow],fill=1,width=2); d.line([elbow,hand],fill=1,width=1)
    for c in ((1,1),(2,0),(1,2)): d.point(_add(hand,c),fill=3)
    return S([''.join(_CH.get(im.getpixel((x,y)),'.') for x in range(XW)) for y in range(XH)])

XE={
 'idle':  _xeno((18,17),(28,12)),
 'idle2': _xeno((18,17),(28,11),tail=((-10,9),(-19,-3))),
 'hiss':  _xeno((18,17),(28,10),tilt=0.3,jaw=2,hand=(35,14),elbow=(32,12),hand2=(33,12),tail=((-10,6),(-18,-9))),
 'hiss2': _xeno((18,17),(28,10),tilt=0.3,jaw=2,tongue=3,hand=(35,14),elbow=(32,12),hand2=(33,12),tail=((-10,6),(-17,-10))),
 'lunge': _xeno((20,16),(32,11),tilt=-0.05,jaw=2,tongue=2,hand=(43,11),elbow=(37,12),hand2=(41,10),legs='stride',
                tail=((-12,4),(-20,0))),
 'hurt':  _xeno((17,17),(25,11),tilt=0.6,jaw=2,hand=(26,4),elbow=(27,6),hand2=(22,5),tail=((-8,8),(-17,2))),
 'fall':  _xeno((18,15),(28,10),tilt=0.15,jaw=1,hand=(33,4),elbow=(30,6),hand2=(24,5),legs='stream',
                tail=((-8,-6),(-16,-10))),
 'cling': _xeno((20,12),(31,11),tilt=0.05,jaw=2,hand=(46,9),elbow=(38,9),hand2=(44,12),legs='stream',
                tail=((-10,-2),(-19,3))),
 'cling2':_xeno((20,13),(31,11),tilt=0.1,jaw=2,tongue=2,hand=(46,9),elbow=(38,10),hand2=(44,12),legs='stream',
                tail=((-10,4),(-19,-3))),
}
XE['tumble']=[XE['fall'],rotate90(XE['fall'],1),rotate90(XE['fall'],2),rotate90(XE['fall'],3)]

# ---- the power loader (native facing right; Claude stands in the cage) -------------------------
LW,LH=56,30
def _loader(ext=0,claw=1,step=0,fold=False):
    im=Image.new('L',(LW,LH),0); d=ImageDraw.Draw(im)
    V={'Y':1,'y':2,'z':3,'g':4,'c':5,'w':6,'a':7}
    b=1
    fu=(-2,1) if step==1 else (0,0); bu=(-2,1) if step==3 else (0,0)    # (lift, forward) per foot
    # far arm (behind the cage)
    fw=(b+27,19) if fold else (b+32+ext,10)
    d.line([(b+20,8),(b+26,13),fw],fill=V['y'],width=2)
    # engine block, hazard stripes
    d.rectangle([b,7,b+5,19],fill=V['Y'])
    for y in (9,11,13): d.line([b+1,y,b+4,y],fill=V['z'])
    for x in range(b,b+6,2): d.line([x,17,x+1,19],fill=V['z'])
    # back leg (shade), front leg
    for c,x0,(lift,fwd) in ((V['y'],b+8,bu),(V['Y'],b+15,fu)):
        x0+=fwd
        d.rectangle([x0,20+lift,x0+4,24+lift],fill=c); d.rectangle([x0+1,24+lift,x0+4,27+lift],fill=c)
        d.line([x0+5,21+lift,x0+5,26+lift],fill=V['c'])                  # knee piston
        d.rectangle([x0-2,27+lift,x0+6,29+lift],fill=V['g']); d.line([x0-2,29+lift,x0+6,29+lift],fill=V['z'])
    d.rectangle([b+7,19,b+21,21],fill=V['y'])
    # cage: roof, posts, floor plate, beacon
    d.rectangle([b+5,4,b+23,5],fill=V['Y']); d.line([b+6,5,b+6,19],fill=V['Y']); d.line([b+22,5,b+22,17],fill=V['Y'])
    d.line([b+6,5,b+22,5],fill=V['y'])
    d.rectangle([b+5,18,b+23,19],fill=V['g'])
    d.rectangle([b+12,2,b+14,3],fill=V['a'])
    # near arm: hydraulic upper arm, forearm, claw
    if fold: el,wr=(b+25,13),(b+26,19)
    else: el,wr=(b+27,14),(b+33+ext,12)
    d.line([(b+21,9),el],fill=V['Y'],width=3); d.line([(b+22,11),(el[0]-1,el[1]+1)],fill=V['c'])
    d.line([el,wr],fill=V['Y'],width=3)
    d.rectangle([wr[0]-1,wr[1]-1,wr[0]+1,wr[1]+1],fill=V['g'])
    if fold:
        d.line([(wr[0]-1,wr[1]+1),(wr[0]-2,wr[1]+4)],fill=V['c']); d.line([(wr[0]+1,wr[1]+1),(wr[0]+2,wr[1]+4)],fill=V['c'])
    else:
        wx,wy=wr
        d.line([(wx+1,wy-1),(wx+5,wy-3-claw),(wx+8,wy-1-claw)],fill=V['c'],width=1)
        d.line([(wx+1,wy+1),(wx+5,wy+3+claw),(wx+8,wy+1+claw)],fill=V['c'],width=1)
        d.point((wx+8,wy-1-claw),fill=V['w']); d.point((wx+8,wy+1+claw),fill=V['w'])
    inv={v:k for k,v in V.items()}
    return S([''.join(inv.get(im.getpixel((x,y)),'.') for x in range(LW)) for y in range(LH)])

LD_PARK=_loader(fold=True)
LD_WALK=[_loader(step=i) for i in range(4)]
LD_PUNCH={e:_loader(ext=e,claw=0 if e>6 else 1) for e in range(0,13)}
def cage_of(X,feet=GROUND):
    """Where Claude stands inside the loader centred at X: (x, feet)."""
    return X-13,feet-12

# ---- background --------------------------------------------------------------------------------
def _hazard(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(200,140,24))
    for x in range(x0-(y1-y0),x1,4): d.line([x,y1,x+(y1-y0),y0],fill=(26,22,16)); d.line([x+1,y1,x+1+(y1-y0),y0],fill=(26,22,16))
    d.rectangle([x0-3,y0,x0-1,y1],fill=(26,28,34))

def _hangar(d):
    d.rectangle([0,0,W,GROUND],fill=(24,28,34))
    for x in range(0,W,22): d.line([x,8,x,GROUND],fill=(17,19,24))          # wall panel seams
    d.line([0,21,W,21],fill=(38,42,50)); d.line([0,22,W,22],fill=(16,18,22))
    for x in range(2,W,3): d.line([x,46,x,GROUND-1],fill=(20,23,28))         # ribbed lower wall
    d.line([0,45,W,45],fill=(36,40,48))
    d.rectangle([0,0,W,6],fill=(12,13,16))                                   # ceiling + pipes
    d.line([0,2,W,2],fill=(46,50,56)); d.line([0,3,W,3],fill=(30,32,36))
    d.line([0,6,W,6],fill=(52,56,62)); d.line([0,7,W,7],fill=(28,30,34))
    for x in range(8,W,30): d.rectangle([x,1,x+2,8],fill=(60,64,70))
    d.rectangle([VENT[0],0,VENT[1],7],fill=(3,3,4))                          # the vent: a black hole
    _hazard(d,VENT[0]-3,7,VENT[1]+3,8)
    d.line([58,8,58,GROUND],fill=(52,56,62)); d.line([59,8,59,GROUND],fill=(34,36,42))   # a pipe
    d.rectangle([56,30,61,33],fill=(120,40,30))                              # its valve wheel
    d.line([148,8,148,GROUND],fill=(44,48,54))
    # airlock frame
    d.rectangle([DOOR[0]-4,DOOR_Y-4,W,GROUND],fill=(54,58,66))
    _hazard(d,DOOR[0]-1,DOOR_Y-3,W,DOOR_Y-1)
    d.rectangle([DOOR[0],DOOR_Y,DOOR[1],GROUND],fill=(10,10,14))
    # the control panel
    px,py=PANEL
    d.rectangle([px-3,py-4,px+3,py+5],fill=(40,44,50),outline=(70,74,82))
    d.rectangle([px-2,py+2,px+2,py+4],fill=(20,60,30))
    # loader dock: hazard floor + a gantry
    _hazard(d,3,GROUND-1,40,GROUND)
    d.rectangle([0,9,1,GROUND],fill=(40,44,50)); d.line([0,9,26,9],fill=(40,44,50))
register_bg(THEME, lambda v: (v*3//4,v*3//4,v//2), decor=_hangar)

# ---- effects -----------------------------------------------------------------------------------
@fx('alien_beacons')
def _fx_beacons(d,im,e,f):
    """Rotating amber warning lights in the ceiling: a slow sweep (period 58, loop-safe: 348=6*58); `alarm`
    turns them red-amber and fast."""
    _,alarm=e; px=im.load()
    for bx in (30,140):
        per=8 if alarm else 58
        a=((f%per)/per)*2*math.pi
        k=max(0,math.cos(a))**3
        col=(255,70,30) if alarm and (f//4)%2 else AMBER
        if k>0.05:
            cx=bx+int(math.sin(a)*40)
            for x in range(cx-10,cx+11):
                for y in range(9,GROUND,1):
                    w=1-abs(x-cx)/11
                    if w>0 and (x+y)%2==0: blend(px,x,y,col,0.18*k*w*(1.2 if alarm else 1))
        d.rectangle([bx-2,6,bx+2,8],fill=tuple(int(lerp(60,v,0.3+0.7*k)) for v in col))
        d.point((bx,9),fill=(255,240,200) if k>0.6 else col)

@fx('alien_steam')
def _fx_steam(d,im,e,f):
    """Steam leaking from the pipe valve (period 29, divides the clip)."""
    _,x,y,a=e; rr=random.Random(5)
    for i in range(10):
        ph=((f+i*3)%29)/29; xx=x+ph*14+rr.uniform(-1,1); yy=y-ph*10+math.sin(ph*6+i)
        r=1+int(ph*3); v=int(90*(1-ph)*a)+30
        if (1-ph)*a>0.15: d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=(v,v+4,v+8))

@fx('alien_drips')
def _fx_drips(d,im,e,f):
    """Slime dripping from the vent: n drips on staggered 58-frame cycles (loop-safe)."""
    _,n=e
    for i in range(n):
        x=VENT[0]+3+(i*7)%13; ph=(f+i*23)%58
        if ph<14: d.line([x,8,x,8+ph//4],fill=(150,170,130))
        else:
            y=10+(ph-14)**1.6*0.35
            if y<GROUND: d.line([x,y,x,y+1],fill=(170,190,150))
            elif ph-14<30: d.point((x-1,GROUND),fill=(120,140,100)); d.point((x+1,GROUND),fill=(120,140,100))

@fx('alien_lurk')
def _fx_lurk(d,im,e,f):
    """A head peeking down out of the vent: p=0 hidden, 1 = the glossy dome hanging below the ceiling,
    teeth glinting, a string of drool."""
    _,p=e
    if p<=0: return
    y=int(lerp(-8,8,p)); x=VENT[0]+3
    d.polygon([(x,0),(x+11,0),(x+12,y-2),(x+10,y+3),(x+7,y+6),(x+4,y+6),(x+2,y+3),(x+1,y-1)],fill=(18,18,26))
    d.line([(x+11,max(0,y-7)),(x+11,y-1),(x+9,y+3)],fill=(116,128,156)); d.point((x+11,y-4),fill=(210,218,234))
    d.line([(x+3,y+2),(x+9,y+2)],fill=(50,10,16))
    for tx in (x+3,x+5,x+7,x+9): d.point((tx,y+3),fill=(222,226,214)); d.point((tx+1,y+1),fill=(222,226,214))
    d.line([x+6,y+6,x+6,y+8+(f//6)%2],fill=(160,180,140))                  # drool

@fx('alien_rifle')
def _fx_rifle(d,im,e,f):
    """The pulse rifle held at a hand pivot, angle a (0 = pointing right)."""
    _,x,y,a=e; ca,sa=math.cos(a),math.sin(a)
    P=lambda u,v: (x+ca*u-sa*v, y+sa*u+ca*v)
    d.line([P(-5,0),P(-1,0)],fill=(40,42,40)); d.line([P(-5,1),P(-3,1)],fill=(40,42,40))
    d.line([P(-1,0),P(8,0)],fill=(78,88,74)); d.line([P(-1,1),P(8,1)],fill=(58,66,56))
    d.line([P(2,2),P(7,2)],fill=(48,54,46)); d.point(P(1,-1),fill=(255,120,40))    # grenade tube, ammo counter
    d.line([P(8,0),P(12,0)],fill=(100,104,100))

@fx('alien_muzzle')
def _fx_muzzle(d,im,e,f):
    _,x,y,a=e; ca,sa=math.cos(a),math.sin(a)
    for k,c in ((4,(255,170,60)),(2,(255,245,200))):
        d.polygon([(x-sa*k/2,y+ca*k/2),(x+ca*k*1.6,y+sa*k*1.6),(x+sa*k/2,y-ca*k/2)],fill=c)

@fx('alien_line')
def _fx_line(d,im,e,f):
    _,x0,y0,x1,y1,c=e; d.line([x0,y0,x1,y1],fill=c)

@fx('alien_acid')
def _fx_acid(d,im,e,f):
    _,x,y=e; d.point((int(x),int(y)),fill=ACID); d.point((int(x),int(y)+1),fill=ACID2)

@fx('alien_burst')
def _fx_burst(d,im,e,f):
    """Acid blood bursting from a hit: radial green-yellow streaks."""
    _,x,y,age=e
    for k in range(9):
        a=k*0.7+0.3; r0=2+age*3; r1=r0+4-age
        d.line([x+math.cos(a)*r0,y+math.sin(a)*r0*0.7,x+math.cos(a)*r1,y+math.sin(a)*r1*0.7],fill=ACID if k%2 else ACID2)

@fx('alien_hole')
def _fx_hole(d,im,e,f):
    """Acid eating through the deck: a glowing, widening pit, bubbles, green smoke; k fades it."""
    _,x,age,k=e; x=int(x)
    if k<=0: return
    r=min(3,1+age//6); px=im.load()
    d.ellipse([x-r-1,GROUND-1,x+r+1,GROUND+2],fill=(20,24,12))
    d.ellipse([x-r,GROUND,x+r,GROUND+1+min(2,age//10)],fill=(4,6,2))
    for dx in range(-r-2,r+3):
        blend(px,x+dx,GROUND-1,ACID,0.6*k*(1-abs(dx)/(r+3)))
    if (f+x)%3: d.point((x+((f+x)%(2*r+1))-r,GROUND),fill=ACID)
    rr=random.Random(x*7)
    for i in range(3):
        ph=((f+i*5+rr.randint(0,11))%18)/18; yy=GROUND-2-ph*12; xx=x+math.sin(ph*5+i)*2
        if ph<0.85*k: blend(px,int(xx),int(yy),(150,190,90),0.6*(1-ph)); blend(px,int(xx)+1,int(yy),(120,150,80),0.4*(1-ph))

@fx('alien_door')
def _fx_door(d,im,e,f):
    """The airlock: open 0 = shut, 1 = the panel fully up, space behind it."""
    _,op=e; x0,x1=DOOR; y0=DOOR_Y
    sp=Image.new('RGB',(x1-x0+1,GROUND-y0+1),(8,10,26)); sd=ImageDraw.Draw(sp)
    rr=random.Random(77)
    for _ in range(18): sd.point((rr.randint(0,sp.width-1),rr.randint(0,sp.height-1)),fill=(200,200,230) if rr.random()<0.4 else (90,90,120))
    pb=[-30,sp.height-14,sp.width+40,sp.height+60]                        # a planet below, lighting the doorway
    sd.ellipse(pb,fill=(40,70,120)); sd.arc(pb,180,300,fill=(120,170,230))
    im.paste(sp,(x0,y0))
    bot=int(lerp(GROUND,y0-1,ease(op)))
    if bot>y0:
        d.rectangle([x0,y0,x1,bot],fill=(70,74,84)); d.line([x0,y0,x0,bot],fill=(96,100,110))
        for y in range(y0+5,bot,9): d.line([x0+1,y,x1,y],fill=(56,60,68))
        _hazard(d,x0+3,max(y0,bot-3),x1,bot)
        wy=bot-22
        if wy>y0: d.rectangle([x0+6,wy,x1-6,wy+5],fill=(10,14,24)); d.point((x1-8,wy+1),fill=(120,140,170))

@fx('alien_panel')
def _fx_panel(d,im,e,f):
    """The airlock button: amber, or red + blinking once pressed."""
    _,pressed=e; px,py=PANEL
    c=((255,60,40) if (f//3)%2 else (130,20,16)) if pressed else (220,150,30)
    d.rectangle([px-1,py-2,px+1,py],fill=c)

@fx('alien_debris')
def _fx_debris(d,im,e,f):
    """Decompression: bits of trash, papers and dust streaking into the airlock, k = strength."""
    _,k=e; rr=random.Random(33)
    for i in range(int(34*k)):
        y=rr.randint(12,GROUND-1); spd=rr.uniform(6,11); off=rr.randint(0,200)
        x=(f*spd+off)%200-10
        if x>DOOR[1]: continue
        y2=y+(DOOR_Y+20-y)*max(0,(x-100)/80)*0.6
        L=int(spd*0.5); c=(180,180,170) if i%3 else (230,226,200)
        d.line([x-L,y2,x,y2],fill=(70,72,70)); d.point((int(x),int(y2)),fill=c)

@fx('alien_say')
def _fx_say(d,im,e,f):
    """2x shout with a local wide M (the font's M looks like an H)."""
    _,txt,y,c,*rest=e; say(im,txt,y,c,cx=rest[0] if rest else W//2)

WIDE={"M":["10001","11011","10101","10001","10001"],"W":["10001","10001","10101","10101","01010"]}
def say(im,txt,y,c,scale=2,cx=W//2,outline=(0,0,0)):
    widths=[5 if ch in WIDE else 3 for ch in txt]; tw=sum(w+1 for w in widths)
    m=Image.new('L',(tw,6),0); md=ImageDraw.Draw(m); x=0
    for ch,w in zip(txt,widths):
        if ch in WIDE:
            for j,row in enumerate(WIDE[ch]):
                for i,b in enumerate(row):
                    if b=='1': md.point((x+i,j),fill=255)
        else: text(md,ch,x,0,255,shadow=None)
        x+=w+1
    m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x0=int(cx-m.width//2)
    for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1),(2,2)): im.paste(outline,(x0+dx,y+dy),m)
    im.paste(c,(x0,y),m)

def small(d,txt,x,y,c,shadow=None):
    """3x5 text with the local wide M and W."""
    for ch in txt:
        if ch in WIDE:
            for j,row in enumerate(WIDE[ch]):
                for i,b in enumerate(row):
                    if b=='1': d.point((x+i,y+j),fill=c)
            x+=6
        else: text(d,ch,x,y,c,shadow=shadow); x+=4

# acid spray: droplets on fixed ballistic paths; each one leaves a hole where it lands
def _spray(x0,y0,seed,n=9):
    rr=random.Random(seed); out=[]
    for _ in range(n):
        vx=rr.uniform(-1.6,1.2); vy=rr.uniform(-2.4,-0.3); x,y=x0,y0; path=[]
        while y<GROUND and len(path)<40:
            path.append((x,y)); x+=vx; y+=vy; vy+=0.35
        out.append((path,int(x)))
    return out
SPLASH=[(106,_spray(106,GROUND-17,11,4)),(217,_spray(92,GROUND-18,21,12)),(241,_spray(98,GROUND-18,31,12))]
def splash_fx(s,f):
    for f0,drops in SPLASH:
        for path,lx in drops:
            a=f-f0
            if 0<=a<len(path): s['fx'].append(('alien_acid',*path[a]))
            elif a>=len(path) and f<336:
                k=1.0 if f<300 else max(0,1-(f-300)/30)
                s['under'].append(('alien_hole',lx,a-len(path),k))
                if a-len(path)<10 and path is drops[0][0]: s['fx'].append(('dmg',"TSSS",lx-7,GROUND-10-(a-len(path))//2,ACID))

# ---- close-up 1: the motion tracker ------------------------------------------------------------
def _beeps():
    out=[]; t=0; g=13
    while t<50: out.append(t); t+=max(3,int(g)); g*=0.86
    return out
BEEPS=_beeps()
def closeup_tracker(fr,f):
    """The motion tracker: a green fan, pulse rings, a blip closing in, the range dropping to 0."""
    im=Image.new('RGB',(W,H),(8,10,8)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([2,0,122,63],radius=6,fill=(46,50,44),outline=(80,86,76))
    d.rectangle([6,3,118,61],fill=(4,16,6))
    cx,cy=62,60
    for r in (14,28,42,56): d.arc([cx-r,cy-r,cx+r,cy+r],180,360,fill=(18,70,26))
    for a in (210,240,270,300,330):
        d.line([cx,cy,cx+math.cos(math.radians(a))*56,cy+math.sin(math.radians(a))*56],fill=(12,46,18))
    dist=max(0.0,20*(1-fr/50))
    for b in BEEPS:
        if 0<=fr-b<10:
            r=(fr-b)*6; k=1-(fr-b)/10
            d.arc([cx-r,cy-r,cx+r,cy+r],180,360,fill=tuple(int(v*k) for v in GREEN))
    blips=[(dist,270+22*math.sin(fr*0.07))]
    if fr>=34: blips+=[(dist+3,236),(dist+5,300)]
    for bd,ang in blips:
        rb=3+bd/20*50; bx=cx+math.cos(math.radians(ang))*rb; by=cy+math.sin(math.radians(ang))*rb
        lit=0
        for b in BEEPS:
            hit=b+rb/6
            if fr>=hit: lit=max(lit,1-(fr-hit)/9)
        if lit>0:
            c=tuple(int(v*lit) for v in (150,255,160))
            d.ellipse([bx-5,by-3,bx+5,by+3],fill=tuple(int(v*lit*0.45) for v in GREEN)); d.ellipse([bx-2,by-2,bx+2,by+2],fill=c)
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for y in range(3,62,2): md.line([6,y,118,y],fill=70)
    im=Image.composite(Image.new('RGB',(W,H),(0,0,0)),im,m); d=ImageDraw.Draw(im)
    near=dist<5
    col=(255,80,60) if near and (f//3)%2 else (110,255,140)
    small(d,"RANGE",132,4,(80,190,100))
    num=f"{int(round(dist)):02d}"
    big_text(im,num,14,col,scale=3,cx=150,shadow=(0,40,10))
    small(d,"M",170,28,col)
    if any(0<=fr-b<3 for b in BEEPS): small(d,"BEEP",138,40,(160,255,170))
    if fr>=46 and (f//2)%3: small(d,"IN THE ROOM",130,52,(255,90,70))
    if fr<3: zoom_lines(d,(120,255,140))
    if fr>=56: im=fade_to(im,(0,0,0),(fr-55)/5)
    return im

# ---- close-up 2: the head, the inner jaw -------------------------------------------------------
def closeup_head(fr,f):
    """Primer plano: the glossy elongated head in profile against the steam, lips peel back, drool —
    and the inner jaw shoots out, straight into the camera."""
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    strobe=max(0,math.cos(fr*0.45))**3
    for y in range(H):
        for x in range(0,W,1):
            k=max(0,1-math.hypot((x-150)/120,(y-10)/70))
            v=(int(18+60*k+30*k*strobe),int(14+40*k+14*k*strobe),int(12+20*k))
            if x%1==0: d.point((x,y),fill=v)
    rr=random.Random(3)
    for i in range(8):                                                   # steam drifting behind
        ph=((fr+i*4)%32)/32; x=130+rr.randint(-40,50)+ph*20; y=60-ph*50-rr.randint(0,10); r=4+int(ph*8)
        blend_c=(90,80,70)
        for dx in range(-r,r+1,2):
            for dy in range(-r//2,r//2+1,2): blend(im.load(),int(x+dx),int(y+dy),blend_c,0.12*(1-ph))
    jx=((f%2)*2-1) if 3<=fr<15 else 0
    jo=int(ease((fr-2)/8)*11)
    my=38                                                                # the lip line
    top=[(-20,-4),(20,-1),(60,5),(96,13),(124,22),(146,31),(154,my-2)]
    T=lambda pts: [(x+jx,y) for x,y in pts]
    d.polygon(T(top+[(154,my+1),(116,my+2),(100,50),(84,64),(-20,64)]),fill=(12,12,18))
    for x0 in range(58,120,10): d.arc(T([(x0-12,10),(x0+12,46)]),205,300,fill=(34,36,48))   # skull ridges under the dome
    d.line(T([(x,y+2) for x,y in top[:-1]]),fill=(70,78,104),width=2)
    d.line(T(top),fill=(150,160,190) if strobe<0.4 else (230,190,120))             # rim light
    d.line(T([(30,2),(62,7)]),fill=(200,210,232),width=2); d.line(T([(128,24),(140,29)]),fill=(170,180,206))
    jaw=[(114,my+1+jo*0.5),(154,my+1+jo),(150,my+7+jo),(128,my+10+jo),(104,54),(90,64)]
    d.polygon(T([(116,my+2)]+jaw),fill=(14,14,20)); d.line(T(jaw[1:4]),fill=(64,70,90))        # lower jaw
    if jo>0:
        d.polygon(T([(116,my+1),(153,my),(153,my+jo),(116,my+1+jo*0.5)]),fill=(56,10,16))    # the mouth
    for x in range(118,153,4):                                           # upper and lower teeth
        d.rectangle(T([(x,my-1),(x+1,my+3)]),fill=(222,226,214)); d.point((x+jx,my+3),fill=(160,164,156))
        yb=my+1+int(jo*(0.5+0.5*(x-116)/37))
        d.rectangle(T([(x+1,yb-3),(x+2,yb)]),fill=(222,226,214))
    for i,x in enumerate((124,136,146)):                                 # drool strings
        if jo>=3: d.line(T([(x,my+3),(x+(1 if (f+i)%4<2 else 0),my+jo)]),fill=(160,184,160))
    d.line(T([(140,my+8+jo),(140,my+10+jo+(fr%5))]),fill=(160,184,160))
    for x in range(30,96,6): d.line([(x,64-(x-30)//5),(x+4,64)],fill=(34,38,50))            # neck tubes
    if fr>=12:
        L=max(10,ease((fr-12)/3)*52); y=my+1+jo//2; x0=120+jx; tip=x0+L
        d.rectangle([x0,y-2,tip-7,y+2],fill=(120,104,116)); d.line([x0,y-2,tip-7,y-2],fill=(190,172,184))
        o=2 if (fr//2)%2 else 1                                          # the little jaws snap
        d.rectangle([tip-8,y-6,tip,y-o],fill=(130,112,124)); d.rectangle([tip-8,y+o,tip,y+6],fill=(110,94,106))
        d.rectangle([tip-7,y-o+1,tip,y+o-1],fill=(60,10,16))
        for dy in (-o-1,-o-3,o+1,o+3):
            d.rectangle([tip+1,y+dy-(1 if dy<0 else 0),tip+2,y+dy],fill=(236,238,228))
        d.line([(tip-3,y+6),(tip-3,y+10+fr%3)],fill=(160,184,160))
        if fr>=17:
            s=1+ease((fr-17)/6)*3.0; cw,ch=W/s,H/s; cx0=min(W-cw,max(0,tip-cw*0.55)); cy0=min(H-ch,max(0,y-ch/2))
            im=im.crop((int(cx0),int(cy0),int(cx0+cw),int(cy0+ch))).resize((W,H),Image.NEAREST); d=ImageDraw.Draw(im)
    if fr<2: zoom_lines(d)
    if fr>=24: im=fade_to(Image.new('RGB',(W,H),(255,255,255)),(0,0,0),min(1,(fr-24)/5))
    return im

# ---- the clip ----------------------------------------------------------------------------------
def rifle_at(pose,cx,a=0.0,feet=GROUND):
    ox,oy=origin(RIP[pose],cx,feet); hx,hy=_HAND[pose]; return ('alien_rifle',ox+hx-1,oy+hy,a)
def muzzle(g):
    _,x,y,a=g; return x+math.cos(a)*13,y+math.sin(a)*13

def loader_walk(X0,X1,t0,t1,f):
    t=(f-t0)/(t1-t0); X=lerp(X0,X1,t); ph=int((f-t0)//4)%4
    return X,LD_WALK[ph],((f-t0)%8==0 and f>t0)

def clip_nostromo(f):
    s=scene(f,THEME)
    alarm=266<=f<304
    s['under']+=[('alien_beacons',alarm),('alien_steam',60,31,1.0),('alien_panel',alarm)]
    cl=actor(RIP[guard_pose(f)],CX,pal=RIP_PAL)
    xe=actor(XE['idle'],120,flip=True,pal=XENO_PAL,vis=False)
    LX=DOCK; lspr=LD_PARK; beacon=0.0; lfeet=GROUND
    rifle=0.0; show_rifle=True; lurk=0.0; drips=2; door=0.0
    # 1) neutral: the head in the vent, it withdraws
    if f<16: lurk=1-ease((f-8)/8)
    # 2) the motion tracker
    if 18<=f<78: s['image']=closeup_tracker(f-18,f); return s
    # 3) it drops from the vent; the rifle can't stop it
    if 78<=f<118:
        rifle=-0.7 if f<96 else -0.05
        if f<86: drips=5; lurk=ease((f-78)/6)*1.3
        if 86<=f<94:
            t=(f-86)/8; xe.update(vis=True,spr=XE['fall'],x=104,y=int(lerp(12,GROUND,t*t)))
        if f==94: s['shake']=rshake(2); s['fx']+=[('dust',92,GROUND-1),('dust',116,GROUND-1)]
        if 94<=f<104: xe.update(vis=True,spr=XE['hiss'] if f<99 else XE['hiss2'],x=104)
        if 104<=f<114: xe.update(vis=True,spr=XE['idle'] if (f//3)%2 else XE['idle2'],x=ez(104,74,(f-104)/10),y=GROUND)
        if 114<=f<118: xe.update(vis=True,spr=XE['lunge'],x=ez(74,58,(f-114)/4))
        if 98<=f<116 and f%2==0:
            cl['x']=CX-1; g=rifle_at(guard_pose(f),cl['x'],rifle); mx,my=muzzle(g)
            s['fx']+=[('alien_muzzle',int(mx),int(my),rifle),('alien_line',int(mx)+4,int(my),int(xe['x'])-8,GROUND-12+(f%3),(255,236,150))]
            s['fx'].append(('spark',int(xe['x'])-10+(f%4),GROUND-13,2))
    # 4) primer plano: the inner jaw
    if 118<=f<150: s['image']=closeup_head(f-118,f); return s
    # 5) into the power loader (Claude dove to the dock)
    if 150<=f<176:
        show_rifle=f<154
        xe.update(vis=True,spr=XE['lunge'] if f<154 else (XE['hiss'] if (f//5)%2 else XE['hiss2']),
                  x=ez(56,112,(f-152)/20))
        if f<156: cl.update(spr=RIP['hurt'],x=ez(26,12,(f-150)/6))
        elif f<164:
            t=(f-156)/8; cx,cy=cage_of(DOCK); cl.update(spr=RIP['armsup'],x=lerp(12,cx,t),y=int(lerp(GROUND,cy,t)-4*math.sin(math.pi*t)))
        else:
            cx,cy=cage_of(DOCK); cl.update(spr=RIP['charge'],x=cx,y=cy)
            beacon=0.5+0.5*math.sin(f*0.8); lspr=LD_PUNCH[0] if f>=168 else LD_PARK
            if f in (164,165): s['shake']=rshake(1)
            s['fx'].append(('alien_steam',DOCK-16,GROUND-30,max(0,1-(f-164)/12)))
    # 6) the loader stomps in: GET AWAY FROM HER!
    if 176<=f<208:
        show_rifle=False; LX,lspr,stomp=loader_walk(DOCK,64,176,208,f); beacon=0.5+0.5*math.sin(f*0.8)
        if stomp: s['shake']=(0,1); s['fx'].append(('dust',int(LX)-6,GROUND-1))
        xe.update(vis=True,spr=XE['hiss'] if (f//4)%2 else XE['hiss2'],x=112)
    if 180<=f<214: s['fx'].append(('alien_say',"GET AWAY FROM HER!",3,(255,214,80)))
    # 7) two hydraulic punches, acid blood
    if 208<=f<252:
        show_rifle=False; LX=64; beacon=0.5+0.5*math.sin(f*0.8); ext=0
        if f<214: xe.update(vis=True,spr=XE['lunge'],x=ez(112,96,(f-208)/6))
        elif f<226:
            ext=int(ez(0,12,(f-214)/3)) if f<220 else int(ez(12,0,(f-220)/6))
            xe.update(vis=True,spr=XE['hurt'] if f>=217 else XE['lunge'],x=96 if f<217 else ez(96,122,(f-217)/7))
        elif f<234: xe.update(vis=True,spr=XE['hiss2'] if (f//3)%2 else XE['hiss'],x=122)
        elif f<238: xe.update(vis=True,spr=XE['lunge'],x=ez(122,102,(f-234)/4))
        else:
            ext=int(ez(0,12,(f-238)/3)) if f<244 else int(ez(12,0,(f-244)/8))
            xe.update(vis=True,spr=XE['hurt'] if f>=241 else XE['lunge'],x=102 if f<241 else ez(102,150,(f-241)/10),
                      y=GROUND-int(6*math.sin(math.pi*min(1,(f-241)/10))) if f>=241 else GROUND)
        lspr=LD_PUNCH[max(0,min(12,ext))]
        if f in (217,241): s['shake']=rshake(2); s['flash']=0.2; s['fc']=(int(xe['x'])-14,GROUND-16); s['flashc']=ACID
        for hf,hx in ((217,92),(241,98)):
            if 0<=f-hf<4: s['fx']+=[('alien_burst',hx,GROUND-18,f-hf),('spark',hx-2,GROUND-18,4-(f-hf))]
    # 8) the airlock
    if 252<=f<304:
        show_rifle=False; beacon=0.5+0.5*math.sin(f*0.8)
        if f<262:
            LX,lspr,stomp=loader_walk(64,96,252,262,f)
            if stomp: s['shake']=(0,1)
        else:
            LX=96; ext=int(ez(0,12,(f-262)/4)) if f<270 else int(ez(12,0,(f-270)/6))
            lspr=LD_PUNCH[ext] if f<276 else LD_WALK[0]
            if f==265: s['fx'].append(('spark',PANEL[0],PANEL[1]-1,3))
        door=ease((f-268)/8) if f<292 else 1-ease((f-292)/8)
        if f<266: xe.update(vis=True,spr=XE['hurt'] if f<258 else XE['idle'],x=150)
        elif f<272: xe.update(vis=True,spr=XE['hiss'],x=ez(150,152,(f-266)/6))
        elif f<280: xe.update(vis=True,spr=XE['cling'],x=ez(152,178,(f-272)/8),y=GROUND-8,pal=XENO_LIT)
        elif f<290:
            xe.update(vis=True,spr=XE['cling'] if (f//2)%2 else XE['cling2'],x=178+((f%3)-1),y=GROUND-8+((f//2)%2),pal=XENO_LIT)
        elif f<298:
            k=f-290; xe.update(vis=True,spr=XE['tumble'][(k//2)%4],x=178+k*k*1.4,y=GROUND-8-k,pal=XENO_LIT)
        if 270<=f<296:
            s['fx'].append(('alien_debris',min(1,(f-270)/4)*(1 if f<290 else (296-f)/6)))
            if f%3==0: s['fx']+=[('mote',int(LX)-10+(f%5),GROUND-2,(255,200,90)),('mote',int(LX)-2-(f%4),GROUND-1,(255,150,50))]
            s['shake']=(random.choice([-1,0,1]),0)
    if alarm and (f//4)%3: s['fx'].append(('alien_say',"AIRLOCK OPEN",3,(255,90,50)))
    # 9) back to the dock, hop out, the next one in the vent
    if 304<=f<330:
        show_rifle=False; LX,lspr,stomp=loader_walk(96,DOCK,304,330,f); beacon=max(0,1-(f-322)/8)*(0.5+0.5*math.sin(f*0.8))
        if stomp: s['fx'].append(('dust',int(LX)-6,GROUND-1))
    if 330<=f<342:
        LX=DOCK; lspr=LD_PARK if f>=334 else LD_WALK[0]; show_rifle=f>=336
        t=(f-330)/6
        if f<336:
            cx,cy=cage_of(DOCK); cl.update(spr=RIP['armsup'],x=lerp(cx,20,t),y=int(lerp(cy,GROUND,t)-5*math.sin(math.pi*t)))
        else: cl.update(x=ez(20,CX,(f-336)/6))
    if f>=332: lurk=ease((f-332)/15)
    # composition
    if door>0 or 252<=f<304: s['under'].append(('alien_door',door))
    else: s['under'].append(('alien_door',0))
    s['under'].append(('alien_drips',drips))
    s['under'].append(('alien_lurk',lurk))
    splash_fx(s,f)
    if 164<=f<330 and not (150<=f<164): cx,cy=cage_of(LX); cl.update(spr=RIP['charge'] if lspr is not LD_PARK else RIP['guard'],x=cx,y=cy)
    ld=actor(lspr,LX,pal=load_pal(beacon))
    if show_rifle and cl['spr'] in (RIP['guard'],RIP['guard2']) and cl['y']==GROUND:
        s['fx'].insert(0,rifle_at('guard' if cl['spr'] is RIP['guard'] else 'guard2',cl['x'],rifle))
    inside=164<=f<336 and cl['y']<GROUND
    s['actors']=[xe,cl,ld] if inside else [xe,ld,cl]
    return s

CLIPS = [clip('nostromo', N_, clip_nostromo)]
