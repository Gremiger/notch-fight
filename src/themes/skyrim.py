"""The Elder Scrolls V: Skyrim. Claude as the Dragonborn (the horned iron helmet, the fur armour, a round
wooden shield, a steel sword) at night in the snowy mountains, the aurora rippling over a ruined stone
watchtower, the compass across the top. Clip `fusrodah`: a dragon comes in over the peaks, lands on the
tower and breathes fire (YOL TOOR SHUL) — Claude takes it on his shield; the combat bars come up.
Close-up: the helmet, the mouth — FUS... RO... DAH! The shout's wave knocks the dragon off the tower;
it crashes, its flesh burns away to bone, and its soul streams into Claude: DRAGON SOUL ABSORBED."""
from engine import *

THEME = 'skyrim'
N_ = 384                                                            # a multiple of 12, 48 and 64
CX, TOWER = 34, 156                                                 # Claude; the watchtower
PERCH = (150, 36)                                                   # where the dragon lands (its feet)
TOP = 38                                                            # the top of the tower
SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(30,26,30)
IRON, IRON_D = (150,152,162), (96,98,110)
SOUL = ((255,170,70),(255,230,170))
# the Dragonborn: horned iron helmet, fur armour with a pale trim, leather on the arms, dark trousers
DPAL = {'1':IRON,'2':IRON_D,'3':(120,88,56),'4':(196,176,140),'5':(90,64,44),'6':(52,48,52),'7':(226,216,190),'8':(70,46,30),'9':(200,170,80)}
HELM = ["7..........7","77........77",".7........7.",".1111111111.","221111111111"]

def _dovah(spr):
    g=[list(r) for r in overlay(spr,HELM,-1,0,bangs="2222222222")]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(h):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y==top+1 and x>=l+2: g[y][x]='2'               # the helmet's brow
            elif c=='O' and top+2<=y<=top+3 and x==r-2: g[y][x]='1'     # the nose guard
            elif c=='O' and y==top+5: g[y][x]='4'                       # the fur at the collar
            elif c=='O' and y==top+7: g[y][x]='9' if x==(l+r)//2 else '8'   # the belt and its buckle
            elif c=='O' and y>top+5: g[y][x]='3'
            elif c=='o' and y<top+8: g[y][x]='5'
            elif c=='o' and y==h-1: g[y][x]='4'                         # fur boots
            elif c=='o': g[y][x]='6'
    return S([''.join(x) for x in g])
DOVAH=variant(_dovah)

# ---- background: night in the mountains, the watchtower --------------------------------------------------
def _mountains(d):
    for y in range(46):
        k=y/45; d.line([0,y,W,y],fill=(int(10+20*k),int(14+26*k),int(34+30*k)))
    rr=random.Random(1111)
    for _ in range(50): d.point((rr.randint(0,W-1),rr.randint(0,30)),fill=rr.choice([(200,210,230),(150,160,190)]))
    for pts,c,snow in (([(0,40),(24,22),(46,34),(70,18),(96,30),(120,16),(150,28),(185,20),(185,46),(0,46)],(54,62,80),(220,228,240)),
                       ([(0,46),(30,34),(60,42),(90,32),(118,40),(150,34),(185,40),(185,48),(0,48)],(70,78,94),(236,240,248))):
        d.polygon(pts,fill=c)
        for i in range(1,len(pts)-3):                                # snow on the peaks
            x,y=pts[i]
            if pts[i-1][1]>y<pts[i+1][1]: d.polygon([(x-5,y+4),(x,y),(x+5,y+4),(x+2,y+3),(x-2,y+3)],fill=snow)
    x=TOWER                                                            # the ruined watchtower
    d.polygon([(x-14,GROUND),(x-11,TOP),(x+11,TOP),(x+14,GROUND)],fill=(110,106,104),outline=(60,58,60))
    for y in range(TOP+3,GROUND-2,6):
        for bx in range(x-12,x+12,6): d.rectangle([bx+(y//6)%2*3,y,bx+5+(y//6)%2*3,y+5],outline=(84,82,84))
    for i,bx in enumerate(range(x-12,x+12,5)):                         # broken battlements
        if i%2==0: d.rectangle([bx,TOP-4+(i%3),bx+3,TOP],fill=(110,106,104),outline=(60,58,60))
    d.rectangle([x-3,GROUND-8,x+3,GROUND],fill=(30,26,24))             # the door
    d.rectangle([0,GROUND-1,W,H],fill=(220,226,236))                   # snow on the ground
    for _ in range(40): d.point((rr.randint(0,W-1),rr.randint(GROUND,H-1)),fill=(190,198,214))
    for tx in (12,62,96):                                              # pines
        d.polygon([(tx,GROUND-14),(tx-5,GROUND-1),(tx+5,GROUND-1)],fill=(30,54,44)); d.polygon([(tx,GROUND-14),(tx-2,GROUND-10),(tx+2,GROUND-10)],fill=(230,236,244))
register_bg(THEME, lambda v: (v+150,v+156,v+170), decor=_mountains)

@fx('sk_aurora')
def _fx_aurora(d,im,e,f):
    """The aurora, rippling (one cycle per 64 frames: the clip loops on it)."""
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for band,(y0,amp,a) in enumerate(((6,4,90),(12,3,60))):
        pts=[(x,y0+amp*math.sin(2*math.pi*((f%64)/64)+x*0.05+band)) for x in range(0,W+1,4)]
        for k in range(6): md.line([(x,y+k) for x,y in pts],fill=int(a*(1-k/6)))
    im.paste((90,230,160),(0,0),m.filter(ImageFilter.GaussianBlur(2)))

@fx('sk_compass')
def _fx_compass(d,im,e,f):
    """The compass across the top, a red marker when the dragon is about (dx: its bearing, -1..1)."""
    _,dx=e; x0,x1=52,134
    d.rectangle([x0,1,x1,7],fill=(20,20,24)); d.line([x0,7,x1,7],fill=(150,150,160))
    for i,c in enumerate("W  N  E"):
        if c!=' ': text(d,c,x0+8+i*11,2,(220,220,220),shadow=None)
    if dx is not None:
        mx=int(lerp(x0+4,x1-4,(dx+1)/2)); d.polygon([(mx-2,2),(mx+2,2),(mx,6)],fill=(220,40,40))

@fx('sk_bars')
def _fx_bars(d,im,e,f):
    """Health (centre), magicka (left) and stamina (right), the way the game shows them in a fight."""
    _,hp,a=e
    if a<=0: return
    for (x0,w,c,v) in ((10,34,(60,90,220),1.0),(72,40,(200,40,40),hp),(140,34,(60,170,70),1.0)):
        d.rectangle([x0-1,60,x0+w+1,63],fill=(20,20,24)); d.rectangle([x0,61,x0+int(w*v),62],fill=tuple(int(cc*a+20*(1-a)) for cc in c))

@fx('sk_shield')
def _fx_shield(d,im,e,f):
    """The round wooden shield, on the back arm (or held up in front, blocking)."""
    _,x,y,front=e; x,y=int(x),int(y); r=6 if front else 5
    d.ellipse([x-r,y-r,x+r,y+r],fill=(140,96,54),outline=INK)                  # planks
    for k in (-2,1): d.line([x+k,y-r+1,x+k,y+r-1],fill=(108,72,40))
    d.ellipse([x-r+1,y-r+1,x+r-1,y+r-1],outline=IRON_D)                       # the iron rim
    d.ellipse([x-2,y-2,x+2,y+2],fill=IRON,outline=IRON_D); d.point((x-1,y-1),fill=(220,222,230))   # the boss

@fx('sk_sword')
def _fx_sword(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y)
    d.line([x+1,y,x+10,y-4],fill=(210,214,224)); d.point((x+10,y-4),fill=(255,255,255))       # the blade
    d.line([x,y-2,x+2,y+2],fill=(120,90,50)); d.line([x-2,y+1,x,y],fill=(80,56,36))           # guard, grip

@fx('sk_fire')
def _fx_fire(d,im,e,f):
    """Dragon fire: a cone from the mouth to where it stops (the shield)."""
    _,x0,y0,x1,y1=e; rr=random.Random(f)
    for i in range(36):
        t=rr.random(); spread=2+t*8
        x=lerp(x0,x1,t)+rr.uniform(-2,2); y=lerp(y0,y1,t)+rr.uniform(-spread,spread)
        r=1+int(t*3); c=rr.choice([(255,220,90),(255,150,40),(230,70,20)])
        d.ellipse([x-r,y-r,x+r,y+r],fill=c)
    for _ in range(6): d.point((int(x1+rr.randint(-3,6)),int(y1+rr.randint(-8,8))),fill=(255,230,150))

@fx('sk_wave')
def _fx_wave(d,im,e,f):
    """The Thu'um: rings of force rolling out from his mouth (k frames since)."""
    _,x,y,k=e
    for j in range(4):
        r=k*6-j*10
        if r<=0: continue
        a=max(0,1-r/170); c=tuple(int(v*a+(1-a)*40) for v in (200,220,255))
        d.arc([x-r*0.3,y-r*0.5,x+r,y+r*0.5],-60,60,fill=c,width=2)

@fx('sk_souls')
def _fx_souls(d,im,e,f):
    """The dragon's soul streaming into him: spirals of orange light from the body (k 0..1)."""
    _,x0,y0,x1,y1,k=e
    for i in range(14):
        p=(k*1.6+i/14)%1
        x=lerp(x0,x1,p)+math.sin(p*9+i)*8*(1-p); y=lerp(y0,y1,p)+math.cos(p*9+i)*6*(1-p)-14*math.sin(p*math.pi)
        d.line([x,y,x-3,y+1],fill=SOUL[i%2]); d.point((int(x),int(y)),fill=(255,255,255))

# ---- the dragon ---------------------------------------------------------------------------------------
SCALE_C, SCALE_D, BELLY = (104,108,88), (70,74,62), (176,164,128)
WING, WING_D, BONE = (120,88,70), (86,60,48), (226,216,190)
def dragon(d,x,y,f,state='perch',jaw=0.0,tilt=0.0,burn=0.0):
    """The dragon, facing left, feet at (x,y). state: fly (wings beating) | perch (wings folded) | tumble
    (spinning off, tilt radians) | dead (on its side on the ground, burn 0..1 for the flesh burning away)
    | bones (only the skeleton left). Returns the mouth."""
    x,y=int(x),int(y)
    if state in ('dead','bones'): tilt=-0.32                           # slumped, the head down in the snow
    s_,c_=math.sin(tilt),math.cos(tilt)
    P=lambda u,v: (x+u*c_-v*s_, y+u*s_+v*c_)
    bones=state=='bones'
    def poly(pts,fill,outline=INK):
        q=[P(u,v) for u,v in pts]
        if bones: d.polygon(q,outline=BONE)
        else: d.polygon(q,fill=fill,outline=outline)
    def line(pts,fill,width=1): d.line([P(u,v) for u,v in pts],fill=BONE if bones else fill,width=width)
    flap=math.sin(f*0.5) if state=='fly' else 0
    def wing(near):
        """A wing: the arm (shoulder, elbow, wrist), the finger bones fanning out, the membrane between."""
        if state=='fly':
            up=-10*flap; o=0 if near else 5                              # the far wing sits a little behind
            sh,el,wr=(2+o,-16),(6+o,-28+up*0.5),(14+o,-40+up)
            tips=[(30+o,-36+up*0.8),(32+o,-26+up*0.4),(24+o,-16),(12+o,-13)]
        else:
            sh,el,wr=(2,-16),(6,-30),(16,-36)
            tips=[(26,-30),(26,-20),(20,-14),(12,-13)]
        mem=[sh,el,wr]+tips
        poly(mem,WING if near else WING_D)
        line([sh,el,wr],SCALE_D,2)
        for t in tips[:3]: line([wr,t],SCALE_D)                         # the finger bones
        for t in tips[:3]:                                             # a tattered edge
            tx,ty=P(*t); d.point((int(tx),int(ty)+1),fill=(40,36,40) if not bones else BONE)
    if state in ('fly',): wing(False)
    # the tail, tapering, with spikes along it
    tail=[(14,-12),(24,-10),(32,-12),(38,-17),(42,-22)]
    poly([(14,-15),(24,-13),(32,-15),(38,-20),(43,-25),(40,-18),(32,-9),(24,-7),(14,-7)],SCALE_C)
    for u,v in tail[1:]: poly([(u-1,v-2),(u+1,v-5),(u+2,v-2)],BONE,SCALE_D)
    # legs and claws
    if state!='fly':
        poly([(8,-10),(13,-12),(14,-5),(12,0),(9,0),(10,-5)],SCALE_D)             # the hind leg
        poly([(-8,-10),(-4,-10),(-5,-4),(-6,0),(-9,0),(-8,-4)],SCALE_D)            # the foreleg
        for cx in (-10,-7,8,11): line([(cx,0),(cx-1,1)],BONE)
    # the body, the belly plates, the spines
    poly([(-12,-11),(-8,-17),(4,-19),(14,-16),(18,-11),(12,-6),(0,-5),(-10,-6)],SCALE_C)
    poly([(-10,-7),(0,-6),(12,-7),(10,-9),(0,-8),(-9,-9)],BELLY,SCALE_D)
    for u in range(-6,14,4): line([(u,-9),(u,-6)],SCALE_D)
    for u,v in ((-6,-18),(0,-20),(6,-19),(12,-17)): poly([(u-2,v),(u,v-3),(u+2,v)],BONE,SCALE_D)
    if state!='fly': wing(True)
    # the neck, rising to the head
    poly([(-8,-16),(-14,-22),(-20,-27),(-24,-29),(-22,-24),(-17,-19),(-11,-11)],SCALE_C)
    line([(-12,-14),(-17,-19),(-21,-24)],BELLY)
    for u,v in ((-12,-20),(-17,-25)): poly([(u-1,v),(u,v-3),(u+2,v)],BONE,SCALE_D)
    # the head: a long snout, horns swept back, the jaw (open with jaw 0..1), a glowing eye
    o=4*jaw
    poly([(-24,-29),(-28,-32),(-34,-31),(-40,-28),(-40,-26),(-30,-26),(-22,-25)],SCALE_C)   # skull and snout
    poly([(-22,-25),(-30,-25),(-39,-25+o),(-36,-23+o),(-26,-22)],SCALE_D)                  # the jaw
    if jaw>0.3: line([(-38,-26),(-32,-25+o*0.6)],(200,60,40))
    for k in range(3): line([(-36+k*3,-26),(-36+k*3,-25)],BONE)                           # teeth
    line([(-26,-31),(-20,-36),(-16,-37)],BONE,2); line([(-28,-31),(-24,-37)],BONE)        # the horns
    if not bones:
        ex,ey=P(-30,-29); d.point((int(ex),int(ey)),fill=(255,210,60) if state!='dead' else INK)   # the eye, dark once dead
        nx,ny=P(-39,-27); d.point((int(nx),int(ny)),fill=INK)
    if state=='fly': wing(True)
    if state=='dead' and burn>0:                                      # the flesh burning away, embers rising
        rr=random.Random(f//2)
        for _ in range(int(26*burn)):
            u,v=rr.uniform(-38,40),rr.uniform(-30,-4); px,py=P(u,v)
            d.point((int(px),int(py-rr.randint(0,6))),fill=rr.choice(SOUL))
    mx,my=P(-39,-25); return mx,my

@fx('sk_dragon')
def _fx_dragon(d,im,e,f):
    _,x,y,state,jaw,tilt,burn=e; dragon(d,x,y,f,state,jaw,tilt,burn)

# ---- close-up -----------------------------------------------------------------------------------------
def closeup_shout(t,f):
    """Primer plano: the helmet and the mouth — FUS... RO... DAH! — the air shuddering with each word."""
    im=Image.new('RGB',(W,H),(18,22,40)); d=ImageDraw.Draw(im)
    words=[(0.08,"FUS..."),(0.36,"RO..."),(0.64,"DAH!")]
    n=sum(1 for t0,_ in words if t>=t0)
    for j in range(n):                                               # rings for each word spoken
        r=(t-words[j][0])*400
        d.arc([60-r*0.4,32-r*0.5,60+r,32+r*0.5],-50,50,fill=(120,150,220),width=2)
    ox=8
    d.rectangle([ox,14,ox+56,H],fill=SKIN,outline=INK); d.rectangle([ox+50,14,ox+56,H],fill=SKIN_D)
    d.rectangle([ox-2,4,ox+58,16],fill=IRON,outline=INK); d.rectangle([ox-2,14,ox+58,18],fill=IRON_D)   # the helmet
    for hx,sgn in ((ox-2,-1),(ox+58,1)):                              # the horns
        d.polygon([(hx,10),(hx+sgn*10,2),(hx+sgn*14,-8),(hx+sgn*6,4)],fill=(220,210,180),outline=INK)
    d.rectangle([ox,18,ox+6,H],fill=IRON_D,outline=INK); d.rectangle([ox+50,18,ox+56,H],fill=IRON_D,outline=INK)   # cheek guards
    for ex in (ox+18,ox+38): d.rectangle([ex-3,26,ex+3,31],fill=(24,14,12))
    d.line([ox+12,24,ox+24,25],fill=INK,width=2); d.line([ox+32,25,ox+44,24],fill=INK,width=2)
    mo=[2,6,10,14][n]                                                # the mouth opens wider each word
    d.ellipse([ox+20,44-mo//2,ox+36,44+mo//2],fill=(60,20,20),outline=INK)
    for j in range(n):
        size=3 if j==2 else 2
        big_text(im,words[j][1],6+j*18,(220,230,255) if j<2 else (255,255,255),scale=size if j==2 else 2,cx=136,outline=(20,30,80))
    if n==3 and (f%4)<2: im=fade_to(im,(200,220,255),0.15)
    if t<0.05: zoom_lines(d)
    return im

# ---- the clip -----------------------------------------------------------------------------------------
GRIP={'guard':(13,4),'guard2':(13,4),'punch':(16,5),'charge':(15,5),'armsup':(12,0)}
def clip_fusrodah(f):
    s=scene(f,THEME)
    s['under'].append(('sk_aurora',))
    pose=guard_pose(f); hp=1.0; bars=0.0; marker=None
    dstate,dx,dy,jaw,tilt,burn=None,0,0,0.0,0.0,0.0
    # 1) the dragon comes in over the peaks and lands on the tower
    if 14<=f<60:
        p=(f-14)/46; dstate='fly'; dx=lerp(-40,PERCH[0],ease(p)); dy=lerp(44,PERCH[1],ease(p))-6*math.sin(p*math.pi)
        marker=lerp(-1,0.8,p)
    if 40<=f<330: bars=min(1,(f-40)/10) if f<300 else max(0,1-(f-300)/30)
    # 2) fire: YOL TOOR SHUL; he takes it on the shield
    if 60<=f<100:
        dstate,dx,dy,marker='perch',PERCH[0],PERCH[1],0.8; jaw=1.0 if f>=64 else (f-60)/4
        pose='charge'; hp=1.0-0.15*(f-64)/36 if f>=64 else 1.0
        s['fx'].append(('big',"YOL TOOR SHUL",14,(255,190,120)))
    # 3) close-up: FUS RO DAH
    if 100<=f<160: s['image']=closeup_shout((f-100)/60,f); return s
    # 4) the wave knocks it off the tower; it crashes
    if 160<=f<200:
        k=f-160; pose='punch'; hp=0.85
        s['fx'].append(('sk_wave',CX+8,GROUND-8,k))
        p=min(1,max(0,(k-6)/34)); dstate='tumble'; dx=lerp(PERCH[0],150,p); dy=lerp(PERCH[1],GROUND+2,p*p)-10*math.sin(p*math.pi); tilt=p*2.4
        marker=0.9
        if f==196: s['shake']=rshake(3)
    if 196<=f<206: s['shake']=rshake(2); s['fx']+= [('dust',170+random.randint(-14,14),GROUND-random.randint(0,6)) for _ in range(3)]
    # 5) it burns away; its soul streams into him
    if 200<=f<330: dstate,dx,dy,hp='dead' if f<280 else 'bones',140,GROUND+2,0.85
    if 220<=f<280: burn=(f-220)/60
    if 240<=f<300:
        pose='armsup'; s['fx'].append(('sk_souls',140,GROUND-8,CX,GROUND-8,(f-240)/60))
    if 262<=f<300: s['fx'].append(('big',"DRAGON SOUL ABSORBED",44,(255,220,170)))
    if 320<=f<330: dstate=None
    # draw
    if dstate: s['under' if dstate in ('dead','bones') else 'fx'].append(('sk_dragon',dx,dy,dstate,jaw,tilt,burn))
    mouth=None
    if dstate=='perch':
        mouth=(PERCH[0]-39,PERCH[1]-24)
        if f>=64: s['fx'].append(('sk_fire',mouth[0],mouth[1],CX+12,GROUND-8))
    hx,hy=hand_at(DOVAH[pose],CX,GROUND,False,*GRIP.get(pose,(13,4)),h=11)
    ox,oy=origin(DOVAH[pose],CX); top,l,r=body_box(DOVAH[pose])
    front=pose=='charge'
    if not front: s['under'].append(('sk_shield',ox+l-1,oy+top+7,False))
    s['actors']=[actor(DOVAH[pose],CX,pal=DPAL,aura=((255,190,90),1) if 240<=f<300 else None)]
    if front: s['fx'].append(('sk_shield',hx+2,hy-2,True))
    elif pose!='armsup': s['fx'].append(('sk_sword',hx,hy))
    s['fx'].append(('sk_compass',marker))
    s['fx'].append(('sk_bars',hp,bars))
    return s

CLIPS = [clip('fusrodah', N_, clip_fusrodah)]
