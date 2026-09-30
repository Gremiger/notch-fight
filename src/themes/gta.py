"""GTA San Andreas: Claude (CJ in a Grove green tank top) on Grove Street at sunset, next to his
green low-poly Greenwood. AH SHIT HERE WE GO AGAIN... he jumps in and pulls out; the wanted stars
fill up and a police cruiser (lights flashing) chases him down the street. The cop rams him, Claude
pulls a handbrake donut, the cruiser clips his tail, barrel-rolls and explodes. MISSION PASSED!
RESPECT + — then he cruises back, parks in the same spot and gets out.

The cars are real low-poly 3D: a tiny flat-shaded software renderer (below) projects each mesh
into the pixel scene, so they can turn, drift, spin and flip."""
from engine import *

THEME = 'gta'
N_ = 288

# ---- a tiny flat-shaded 3D renderer ---------------------------------------------------------
# World: x right, y up, z away from the camera (world x = screen x - W/2, the road plane is y=0).
# The camera looks down TILT onto the street from FOC units in front of z=0.
TILT, FOC = math.radians(22), 240
CAM = (0.0, 0.0, -FOC)
AMB, DIF = 0.5, 0.62

def _sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def _dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def _cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def _unit(a): l=math.sqrt(_dot(a,a)) or 1.0; return (a[0]/l,a[1]/l,a[2]/l)
def _avg(ps): n=len(ps); return (sum(p[0] for p in ps)/n,sum(p[1] for p in ps)/n,sum(p[2] for p in ps)/n)
LIGHT = _unit((0.5,0.8,-0.45))       # the low sun on the right, a bit toward the camera
GLOW = {'head','tailL','barR','barB'}  # emissive: never shaded

PIVOT = 6   # roll/pitch pivot height (mid-body), so a flip turns about the car's centre

def _xf(p,yaw,pitch,roll,pos):
    """Local mesh point -> camera space: roll (long axis), pitch (nose up), yaw (nose toward the
    camera when > 0), translate, then the camera tilt."""
    x,y,z=p; y-=PIVOT
    c,s=math.cos(roll),math.sin(roll); y,z=y*c-z*s,y*s+z*c
    c,s=math.cos(pitch),math.sin(pitch); x,y=x*c-y*s,x*s+y*c
    y+=PIVOT
    c,s=math.cos(yaw),math.sin(yaw); x,z=x*c+z*s,-x*s+z*c
    x,y,z=x+pos[0],y+pos[1],z+pos[2]
    c,s=math.cos(TILT),math.sin(TILT)
    return (x,y*c+z*s,z*c-y*s)

def _proj(p):
    k=FOC/(FOC+p[2]); return (W/2+p[0]*k, GROUND-p[1]*k)

def _shade(c,n,key=None):
    if key in GLOW: return c
    k=AMB+DIF*max(0.0,_dot(n,LIGHT)); return tuple(min(255,int(v*k)) for v in c)

def draw_mesh(im,parts,pal,yaw=0,pitch=0,roll=0,pos=(0,0,0)):
    """Back-face culled, painter-sorted, Lambert flat-shaded polygons with a 1px dark outline
    around the silhouette. parts = [(rank, verts, faces)], faces = [(idx, colour key, details)];
    every part is convex, so culling + a depth sort inside it is exact; parts are ordered by rank
    (wheels, body, cabin, roof bar), reversed when the car is upside down."""
    up=_sub(_xf((0,1,0),yaw,pitch,roll,(0,0,0)),_xf((0,0,0),yaw,pitch,roll,(0,0,0)))
    flip=up[1]<0
    xf=lambda p: _xf(p,yaw,pitch,roll,pos)
    drawn=[]
    for rank,verts,faces in parts:
        vs=[xf(v) for v in verts]; ctr=_avg(vs)
        polys=[]
        for fi,(idx,key,details) in enumerate(faces):
            ps=[vs[i] for i in idx]; c=_avg(ps)
            n=_unit(_cross(_sub(ps[1],ps[0]),_sub(ps[2],ps[0])))
            if _dot(n,_sub(c,ctr))<0: n=(-n[0],-n[1],-n[2])          # outward
            if _dot(n,_sub(c,CAM))>=0: continue                       # back face
            polys.append((-math.dist(c,CAM),fi,ps,key,n,details))
        polys.sort(key=lambda t:(t[0],t[1]))
        drawn.append(((-rank if flip else rank), -math.dist(ctr,CAM), polys))
    drawn.sort(key=lambda t:(t[0],t[1]))
    lay=Image.new('RGB',(W,H)); mask=Image.new('L',(W,H),0)
    dl,dm=ImageDraw.Draw(lay),ImageDraw.Draw(mask)
    for _,_,polys in drawn:
        for _,_,ps,key,n,details in polys:
            pts=[_proj(p) for p in ps]
            dl.polygon(pts,fill=_shade(pal[key],n,key)); dm.polygon(pts,fill=255)
            for dpts,dkey in details:
                dl.polygon([_proj(xf(p)) for p in dpts],fill=_shade(pal[dkey],n,dkey))
    im.paste(OUT,(0,0),mask.filter(ImageFilter.MaxFilter(3)))
    im.paste(lay,(0,0),mask)
    return lambda p: _proj(xf(p))          # local point -> screen, for glows / smoke / sparks

# ---- meshes ---------------------------------------------------------------------------------
def _prism(profile,z0,z1,keys,side,details=None):
    """Extrude a convex x-y profile between z0 and z1: one quad per profile edge (keys[i]) plus
    the two side caps. details = {face index: [(points, key)]} (side caps: len(profile)+0/1)."""
    n=len(profile); v=[(x,y,z0) for x,y in profile]+[(x,y,z1) for x,y in profile]
    faces=[([i,(i+1)%n,(i+1)%n+n,i+n],keys[i],[]) for i in range(n)]
    faces+=[(list(range(n)),side,[]),(list(range(2*n-1,n-1,-1)),side,[])]
    for k,ds in (details or {}).items(): faces[k][2].extend(ds)
    return v,faces

def _loft(bot,top,keys,roof,details=None):
    """A frustum between two quads (the cabin / the light bar): side faces keys[i] + the top."""
    n=len(bot); v=bot+top
    faces=[([i,(i+1)%n,(i+1)%n+n,i+n],keys[i],[]) for i in range(n)]+[(list(range(n,2*n)),roof,[])]
    for k,ds in (details or {}).items(): faces[k][2].extend(ds)
    return v,faces

WR = 3.7   # wheel radius
def _wheel(cx,z0,z1,spin):
    ring=[(cx+WR*math.cos(spin+k*math.pi/4),WR+WR*math.sin(spin+k*math.pi/4)) for k in range(8)]
    v,faces=_prism(ring,z0,z1,['tire']*8,'tire')
    hub=lambda z:[(cx+1.6*math.cos(spin+k*math.pi/2),WR+1.6*math.sin(spin+k*math.pi/2),z) for k in range(4)]
    faces[8][2].append((hub(z0),'hub')); faces[9][2].append((hub(z1),'hub'))
    return v,faces

def _quad(x0,x1,y0,y1,z): return [(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)]
def _fq(x,y0,y1,z0,z1): return [(x,y0,z0),(x,y0,z1),(x,y1,z1),(x,y1,z0)]    # a quad on a x=const face

HW = 8      # half width
def car_mesh(police=False,spin=0.0):
    # lower hull, side profile (convex): bumper, nose, hood/trunk deck, tail
    prof=[(-18,3.2),(18,3.2),(18.5,6.2),(16,8.2),(-16.5,8.2),(-18.5,6.6)]
    keys=['under','chrome','nose','deck','tail','chrome']
    side='door' if police else 'body'
    sdet=[]
    for z in (-HW,HW):
        if police:   # black fenders on the white doors
            sdet+= [(_quad(9,18.5,3.2,8.2,z),'body'),(_quad(-18.5,-10,3.2,8.2,z),'body')]
        sdet+= [(_quad(-17,17,5.4,5.9,z),'trim')]
    det={6:[d for d in sdet if d[0][0][2]==-HW],7:[d for d in sdet if d[0][0][2]==HW],
         1:[(_fq(18.3,4.2,5.8,-7,-3.5),'head'),(_fq(18.3,4.2,5.8,3.5,7),'head'),(_fq(18.3,4.4,5.6,-2.5,2.5),'grille')],
         5:[(_fq(-18.3,4.2,6,-7,-4),'tailL'),(_fq(-18.3,4.2,6,4,7),'tailL')]}
    hull=_prism(prof,-HW,HW,keys,side,det)
    # cabin: glass sides with a body-colour pillar, windshield, rear window, roof
    b=[(-10,8.2,-7),(6,8.2,-7),(6,8.2,7),(-10,8.2,7)]
    t=[(-7.5,13,-5.8),(2,13,-5.8),(2,13,5.8),(-7.5,13,5.8)]
    pil=lambda z0,zt:[(-2.2,8.2,z0),(-0.8,8.2,z0),(-1.6,13,zt),(-3.0,13,zt)]
    cab=_loft(b,t,['glass','glass','glass','glass'],'roofc' if police else 'body',
              {0:[(pil(-7,-5.8),'roofc' if police else 'body')],2:[(pil(7,5.8),'roofc' if police else 'body')]})
    parts=[(0,*_wheel(x,z0,z1,spin)) for x in (-11,11) for z0,z1 in ((-HW-1,-HW+2.2),(HW-2.2,HW+1))]
    parts+=[(1,*hull),(2,*cab)]
    if police:
        bb=[(-3.5,13,-4),(-1.5,13,-4),(-1.5,13,4),(-3.5,13,4)]
        bt=[(-3.4,14.4,-3.8),(-1.6,14.4,-3.8),(-1.6,14.4,3.8),(-3.4,14.4,3.8)]
        parts.append((3,*_loft(bb,bt,['barR','chrome','barB','chrome'],'barT')))
    return parts

GREEN = {'body':(40,132,56),'under':(26,40,30),'chrome':(196,196,204),'nose':(40,132,56),'deck':(40,132,56),
         'tail':(40,132,56),'trim':(22,70,32),'glass':(40,56,80),'tire':(26,24,28),'hub':(170,170,180),
         'head':(255,244,200),'grille':(30,32,36),'tailL':(220,40,40)}
COP = dict(GREEN, body=(24,24,30),nose=(24,24,30),deck=(24,24,30),tail=(24,24,30),door=(236,236,240),
           roofc=(236,236,240),trim=(90,90,100),barT=(60,60,70))
BURNT = {k:tuple(int(c*0.28)+14 for c in v) for k,v in COP.items()}

def cop_pal(f,burnt=False):
    if burnt: return dict(BURNT,barR=BURNT['body'],barB=BURNT['body'])
    ph=(f//3)%2
    return dict(COP,barR=(255,40,40) if ph else (90,20,24),barB=(40,90,255) if not ph else (20,24,90))

@fx('gta_car')
def _fx_car(d,im,e,f):
    """('gta_car', dict(x=screen x, z=depth, yaw, roll, pitch, lift, spin, police, burnt))"""
    _,c=e; police=c.get('police',False); burnt=c.get('burnt',False)
    pal=cop_pal(f,burnt) if police else GREEN
    at=draw_mesh(im,car_mesh(police,c.get('spin',0.0)),pal,c.get('yaw',0),c.get('pitch',0),c.get('roll',0),
                 (c['x']-W/2,c.get('lift',0),c['z']))
    if police and not burnt and not c.get('roll'):
        x,y=at((-2.5,15,0)); col=(255,60,60) if (f//3)%2 else (70,110,255); px=im.load()
        for dx in range(-7,8):
            for dy in range(-3,4):
                a=0.45*(1-abs(dx)/8)*(1-abs(dy)/4)
                if a>0: blend(px,int(x+dx),int(y+dy),col,a)

# ---- the street -----------------------------------------------------------------------------
SKY_ROWS=[(0,(40,20,70)),(14,(120,46,110)),(28,(220,96,90)),(40,(255,170,80))]
def _sky():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(42):
        for (y0,c0),(y1,c1) in zip(SKY_ROWS,SKY_ROWS[1:]):
            if y0<=y<=y1: t=(y-y0)/(y1-y0); d.line([0,y,W,y],fill=tuple(int(lerp(a,b,t)) for a,b in zip(c0,c1)))
    for r,c in ((12,(255,190,90)),(9,(255,214,120)),(6,(255,236,170))):     # the low sun
        d.ellipse([138-r,32-r,138+r,32+r],fill=c)
    for y in range(24,36,3): d.line([126,y,150,y],fill=(250,160,90))        # sunset bands over it
    far=(150,70,110)                                                         # downtown Los Santos
    for x0,w,h in ((18,6,16),(25,5,22),(31,7,13),(40,4,19),(60,6,10),(88,5,15),(94,4,11)):
        d.rectangle([x0,40-h,x0+w,40],fill=far)
    d.line([27,16,27,18],fill=far)
    return im

def _strip(period,draw_fn,seed):
    im=Image.new('RGB',(period,H)); m=Image.new('L',(period,H),0)
    draw_fn(ImageDraw.Draw(im),ImageDraw.Draw(m),random.Random(seed)); return im,m

HOUSE=(58,30,62); HOUSE2=(76,40,72); LIT=(250,196,110)
def _houses(d,m,rr):
    x=0
    while x<240:
        w=rr.randint(26,40); h=rr.randint(9,14); x1=min(239,x+w)
        for dd,fill in ((d,HOUSE if rr.random()<0.5 else HOUSE2),(m,255)):
            dd.rectangle([x,40-h,x1-2,40],fill=fill)
            dd.polygon([(x-2,40-h),(x+(x1-x)//2-1,40-h-6),(x1,40-h)],fill=fill)    # pitched roof
        for wx in range(x+4,x1-5,8):
            if rr.random()<0.55: d.rectangle([wx,40-h+3,wx+2,40-h+5],fill=LIT)
        d.rectangle([x+(x1-x)//2-2,34,x+(x1-x)//2,40],fill=(34,18,38))        # the door
        x=x1+rr.randint(2,6)
    d.line([0,37,239,37],fill=(40,22,44)); m.line([0,37,239,37],fill=255)     # low fence rail
    for fx_ in range(0,240,4): d.line([fx_,37,fx_,40],fill=(40,22,44)); m.line([fx_,37,fx_,40],fill=255)

PALM=(34,16,40)
def _palms(d,m,rr):
    for bx,top,lean in ((22,6,6),(66,14,-4)):
        pts=[(bx+lean*(t/10)**2,41-(41-top)*t/10) for t in range(11)]
        for dd,fill in ((d,PALM),(m,255)):
            dd.line(pts,fill=fill,width=2)
            tx,ty=pts[-1]
            for a in (-2.8,-2.3,-1.7,-1.2,-0.4,0.1,0.6):
                ex,ey=tx+math.cos(a)*11,ty+math.sin(a)*4+5
                dd.line([(tx,ty),(tx+math.cos(a)*6,ty+math.sin(a)*3),(ex,ey)],fill=fill,width=1)
            dd.ellipse([tx-2,ty-1,tx+2,ty+2],fill=fill)

SKY=None; HOUSES=None; PALMS=None
def _layers():
    global SKY,HOUSES,PALMS
    if SKY is None: SKY=_sky(); HOUSES=_strip(240,_houses,11); PALMS=_strip(90,_palms,12)

def _tile(im,layer,off,period):
    lim,lm=layer; x=-int(off)%period-period
    while x<W: im.paste(lim,(x,0),lm); x+=period

def draw_street(im,off):
    _layers(); im.paste(SKY); d=ImageDraw.Draw(im)
    _tile(im,HOUSES,off*0.5,240)
    d.rectangle([0,40,W,42],fill=(150,112,112)); d.line([0,42,W,42],fill=(96,70,84))   # far sidewalk
    _tile(im,PALMS,off*0.75,90)
    d.rectangle([0,43,W,55],fill=(62,54,72))                                          # asphalt
    for y in (45,51): d.line([0,y,W,y],fill=(66,58,76))
    o=int(off)%16
    for x in range(-o,W,16): d.line([x,49,x+7,49],fill=(214,176,70))                  # centre dashes
    d.line([0,55,W,55],fill=(196,176,164)); d.rectangle([0,56,W,H],fill=(128,108,112))  # curb + sidewalk
    for x in range(-o,W,16): d.line([x+4,57,x+2,63],fill=(104,88,94))
    d.line([0,56,W,56],fill=(100,82,90))

register_bg(THEME, lambda v: (v,v,v), decor=lambda d: draw_street(d._image,0))

@fx('gta_street')
def _fx_street(d,im,e,f): draw_street(im,e[1])

# ---- HUD ------------------------------------------------------------------------------------
STAR=["...#...","..###..","#######",".#####.","..###..",".##.##.","##...##"]
@fx('gta_stars')
def _fx_stars(d,im,e,f):
    """The wanted level, top right: 6 slots, filled stars gold; a fresh star blinks."""
    _,n,blink=e
    for k in range(6):
        x0=W-8-(k*8)-6
        lit=k<n and not (blink and k==n-1 and (f//2)%2)
        for j,row in enumerate(STAR):
            for i,ch in enumerate(row):
                if ch=='#':
                    for ox,oy in ((1,0),(-1,0),(0,1),(0,-1)): d.point((x0+i+ox,2+j+oy),fill=(0,0,0))
        for j,row in enumerate(STAR):
            for i,ch in enumerate(row):
                if ch=='#': d.point((x0+i,2+j),fill=(250,196,40) if lit else (70,64,56))

@fx('gta_radar')
def _fx_radar(d,im,e,f):
    """The San Andreas radar, bottom left: the street, CJ's arrow, the cop blip."""
    _,cop,off=e; cx,cy,r=11,52,9; px=im.load()
    for x in range(cx-r,cx+r+1):
        for y in range(cy-r,cy+r+1):
            if (x-cx)**2+(y-cy)**2<=r*r: blend(px,x,y,(30,40,30),0.8)
    d.line([cx-r+1,cy+2,cx+r-1,cy+2],fill=(150,150,150))
    for k in range(-2,3):
        x=cx+k*5-int(off/4)%5
        if abs(x-cx)<r-1: d.line([x,cy-r+3,x,cy+2],fill=(90,100,90))
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(0,0,0))
    d.polygon([(cx,cy-1),(cx+3,cy+2),(cx-3,cy+2)],fill=(255,255,255))
    if cop is not None and (f//3)%2: d.rectangle([cx+cop-1,cy+1,cx+cop+1,cy+3],fill=(255,50,50) if (f//6)%2 else (60,100,255))

@fx('gta_passed')
def _fx_passed(d,im,e,f):
    """MISSION PASSED! in orange-gold with a black outline, RESPECT + underneath."""
    _,t=e
    if t<=0: return
    big_text(im,"MISSION PASSED!",int(lerp(-14,12,t*3)),(240,160,40),outline=(0,0,0))
    if t>0.35:
        text(d,"RESPECT",W//2-19,30,(240,240,240))
        x,y=W//2+15,32
        for dx,dy in ((0,0),(1,1)):
            c=(0,0,0) if dx else (240,240,240)
            d.line([x-2+dx,y+dy,x+2+dx,y+dy],fill=c); d.line([x+dx,y-2+dy,x+dx,y+2+dy],fill=c)

@fx('gta_puff')
def _fx_puff(d,im,e,f):
    """A soft, see-through smoke puff (tyre smoke, exhaust, the burning wreck)."""
    _,x,y,r,c,a=e; px=im.load(); r=max(1,r)
    for yy in range(int(y-r),int(y+r)+1):
        for xx in range(int(x-r),int(x+r)+1):
            q=((xx-x)**2+(yy-y)**2)/(r*r)
            if q<=1: blend(px,xx,yy,c,a*(1-q*0.6))

@fx('gta_boom')
def _fx_boom(d,im,e,f):
    """Car explosion: a cluster of fireballs swelling and darkening into smoke, flying debris."""
    _,x,y,t=e; rr=random.Random(77); px=im.load()
    for k in range(7):
        ox,oy,sz=rr.uniform(-12,12),rr.uniform(-8,4),rr.uniform(0.6,1.0)
        r=(3+13*ease(t*1.8))*sz; cx,cy=x+ox*ease(t*2),y+oy*ease(t*2)-10*t*t
        heat=max(0,1-t*1.2-k*0.05)
        col=(tuple(int(lerp(a,b,(heat-0.5)*2)) for a,b in zip((240,110,30),(255,214,110))) if heat>0.5 else
             tuple(int(lerp(a,b,heat*2)) for a,b in zip((46,40,48),(240,110,30))))
        for yy in range(int(cy-r),int(cy+r)+1):
            for xx in range(int(cx-r),int(cx+r)+1):
                q=((xx-cx)**2+(yy-cy)**2)/(r*r)
                if q<=1: blend(px,xx,yy,col if q>0.35*heat else (255,236,150),min(1,1.6-t)*(1-q*0.3))
    for _ in range(14):
        a=rr.uniform(math.pi*1.05,math.pi*1.95); sp=rr.uniform(16,40)
        qx,qy=x+math.cos(a)*sp*t,y+math.sin(a)*sp*t+30*t*t
        d.rectangle([qx,qy,qx+1,qy+1],fill=(30,26,30) if rr.random()<0.5 else (255,190,70))

# ---- Claude as CJ -----------------------------------------------------------------------------
def _cj(x,y,t,l,r,c):
    if c=='.': return None
    inside=l<=x<=r
    if inside and t+5<=y<=t+7: return 'X'                            # Grove green tank top
    if y>=t+8: return 'N'                                             # jeans
    return None
CJ=variant(lambda s: recolor_rows(s,_cj))

# ---- choreography -----------------------------------------------------------------------------
def _speed(f):
    """Camera (scroll) speed profile, 0..1."""
    if f<60: return 0
    if f<84: return (f-60)/24
    if f<146: return 1
    if f<160: return 1-(f-146)/14
    if f<236: return 0
    if f<248: return (f-236)/12
    if f<256: return 1
    if f<268: return 1-(f-256)/12
    return 0
_acc=[0.0]
for _f in range(N_): _acc.append(_acc[-1]+_speed(_f))
SCROLL_TOTAL=960           # a multiple of every layer's period / parallax: 16 (road), 90/0.75, 240/0.5
SCROLL=[round(v*SCROLL_TOTAL/_acc[-1],6) for v in _acc]
WHEEL_TURNS=round(SCROLL_TOTAL/(2*math.pi*WR))
def scroll(f): return SCROLL[min(f,N_)]
def wheel_spin(f): return -scroll(f)*WHEEL_TURNS*2*math.pi/SCROLL_TOTAL   # whole turns over the loop

def keys(f,ks):
    """Ease between keyframes [(frame, (x, z, yaw)), ...]."""
    if f<=ks[0][0]: return ks[0][1]
    for (f0,a),(f1,b) in zip(ks,ks[1:]):
        if f0<=f<f1: t=ease((f-f0)/(f1-f0)); return tuple(lerp(u,v,t) for u,v in zip(a,b))
    return ks[-1][1]

PARK=(100,12,0.32)
TAU=2*math.pi
CAR_K=[(0,PARK),(60,PARK),(72,(106,19,-0.45)),(86,(116,30,0.0)),(146,(116,30,0.0)),
       (180,(112,28,TAU))]
CAR_K2=[(180,(112,28,0.0)),(236,(112,28,0.0)),(245,(114,21,0.4)),(252,(116,16,0.0)),(260,(110,14,0.18)),(268,PARK)]
COP_K=[(84,(-40,14,0.0)),(100,(44,14,0.0)),(128,(82,14,0.0)),(138,(98,21,-0.3)),(148,(70,18,0.1)),
       (160,(86,24,-0.25))]

def car_state(f):
    x,z,yaw=keys(f,CAR_K if f<180 else CAR_K2)
    if 92<=f<146:                                      # weaving through traffic
        env=math.sin(math.pi*(f-92)/54); ph=TAU*(f-92)/27
        z+=4*env*math.sin(ph); yaw-=0.28*env*math.cos(ph)
    return dict(x=x,z=z,yaw=yaw,spin=wheel_spin(f))

CRASH=184
def cop_state(f):
    if f<84 or f>=262: return None
    if f<160:
        x,z,yaw=keys(f,COP_K)
        if 104<=f<130:
            env=math.sin(math.pi*(f-104)/26); ph=TAU*(f-104)/26+1.6
            z+=3*env*math.sin(ph); yaw-=0.22*env*math.cos(ph)
        return dict(x=x,z=z,yaw=yaw,spin=wheel_spin(f)*1.1,police=True)
    if f<CRASH:                                        # clipped by the donut: barrel roll
        t=(f-160)/(CRASH-160)
        return dict(x=lerp(86,160,t),z=lerp(24,36,t),yaw=lerp(-0.25,0.5,t),roll=-3*math.pi*ease(t),
                    lift=30*math.sin(math.pi*t),spin=f*0.7,police=True)
    return dict(x=160-(scroll(f)-scroll(CRASH)),z=36,yaw=0.5,roll=-3*math.pi,police=True,burnt=f>=CRASH+3)

def stars(f):
    if f<84: return 0,False
    if f>=236: return (4 if (f//3)%2 else 0) if f<250 else 0,False
    for t0,n in ((186,4),(124,3),(104,2),(84,1)):
        if f>=t0: return n,f<t0+14
    return 0,False

def clip_grove(f):
    s=scene(f,THEME)
    s['under'].append(('gta_street',scroll(f)))
    cl=actor(CJ[guard_pose(f)],40)
    car=car_state(f); cop=cop_state(f)
    # 1) AH SHIT, HERE WE GO AGAIN... he walks to the car and gets in
    if 14<=f<46: callout(s,"AH SHIT HERE WE GO AGAIN...",c=(240,240,240))
    if 22<=f<44: cl['x']=ez(40,90,(f-22)/20)
    if 44<=f<272: cl['vis']=False
    if 44<=f<48: s['fx'].append(('gta_puff',92,GROUND-7,3,(200,190,200),0.5))            # the door slam
    if 48<=f<60:                                                                # engine start
        car['pitch']=0.03*math.sin(f*2.1)
        if f%3==0: s['fx'].append(('gta_puff',car['x']-22,GROUND-7-(f-48)//3,1+(f-48)//4,(150,140,150),0.6))
    # 2) pull out, the cops show up
    wreck=[]
    if cop and f>=CRASH+8:                                                     # the wreck burns
        wreck=[('fire',cop['x']+4,GROUND-14,3+(f%3==0)),('fire',cop['x']-6,GROUND-13,2)]
        for k in range(3):                                                     # the smoke column
            u=((f+k*8)%24)/24
            s['under'].insert(1,('gta_puff',cop['x']+2+u*8,GROUND-20-u*20,3+u*5,(40,34,44),0.7*(1-u)))
    cars=[(car['z'],[('gta_car',car)])]+([(cop['z'],[('gta_car',cop)]+wreck)] if cop else [])
    for _,items in sorted(cars,key=lambda t:-t[0]): s['under'].extend(items)   # far to near
    if 62<=f<90 and f%2==0:
        s['fx'].append(('gta_puff',car['x']-24+random.randint(-2,2),GROUND-9,2+random.randint(0,1),(160,150,160),0.5))
    # 3) the ram: sparks between the two cars
    if 136<=f<148 and f%2==0:
        s['fx'].append(('spark',random.randint(96,110),GROUND-14+random.randint(-2,2),3)); s['shake']=rshake()
    if 132<=f<148: callout(s,"BUSTED? NOT TODAY",c=(120,200,255))
    # 4) handbrake donut: tyre smoke; the cruiser clips the tail and flips
    if 148<=f<182:
        for k in range(2):
            a=car['yaw']+math.pi+random.uniform(-0.4,0.4); rr_=random.randint(4,8)
            s['fx'].append(('gta_puff',car['x']+math.cos(a)*16,GROUND-12-math.sin(a)*4+random.randint(-1,1),
                            rr_,(200,190,200) if k else (150,140,156),0.45))
    if 150<=f<168: callout(s,"HANDBRAKE!",c=(250,210,60))
    if 158<=f<164:
        s['fx'].append(('spark',96,GROUND-14,5)); s['flash']=0.25 if f==158 else 0; s['fc']=(96,GROUND-14)
        if f<162: s['shake']=rshake(2)
    if CRASH<=f<CRASH+16:
        t=(f-CRASH)/16; s['fx'].append(('gta_boom',cop['x']+2,GROUND-22,t))
        if f<CRASH+3: s['flash']=0.8; s['fc']=(cop['x'],GROUND-18); s['flashc']=(255,220,160)
        if f<CRASH+8: s['shake']=rshake(2)
    # 5) MISSION PASSED! RESPECT +
    if 196<=f<238: s['fx'].append(('gta_passed',(f-196)/42))
    # HUD
    n,blink=stars(f)
    if 60<=f<272:
        cx=None
        if cop and f<CRASH+4: cx=max(-7,min(7,int((cop['x']-car['x'])/12)))
        s['fx'].append(('gta_radar',cx,scroll(f)))
    if 84<=f<250: s['fx'].append(('gta_stars',n,blink))
    # 6) back home: he gets out and walks back to his spot
    if 272<=f<286: cl.update(vis=True,x=ez(90,40,(f-272)/14))
    s['actors']=[cl]
    return s

CLIPS = [clip('grove', N_, clip_grove)]
