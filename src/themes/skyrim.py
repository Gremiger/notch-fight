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
DPAL = {'1':IRON,'2':IRON_D,'3':(120,88,56),'4':(196,176,140),'5':(90,64,44),'6':(52,48,52)}
HELM = ["1.........1.","1.........1.",".1.......1..",".11111111111","22111111111."]

def _dovah(spr):
    g=[list(r) for r in overlay(spr,HELM,-1,0,bangs="2222222222")]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(h):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y==top+1 and x>=l+2: g[y][x]='2'               # the helmet's brow
            elif c=='O' and y==top+5: g[y][x]='4'                       # the fur at the collar
            elif c=='O' and y>top+5: g[y][x]='3'
            elif c=='o' and y<top+8: g[y][x]='5'
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
    _,x,y,front=e; x,y=int(x),int(y); r=5 if front else 4
    d.ellipse([x-r,y-r,x+r,y+r],fill=(130,90,50),outline=IRON_D); d.ellipse([x-1,y-1,x+1,y+1],fill=IRON)
    d.line([x-r+1,y,x+r-1,y],fill=(100,70,40))

@fx('sk_sword')
def _fx_sword(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.line([x,y,x+8,y-3],fill=(210,214,224)); d.line([x-1,y-1,x+1,y+1],fill=(120,90,50))

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
SCALE_C, BELLY, WING = (96,104,84), (160,150,116), (110,86,74)
def dragon(d,x,y,f,state='perch',jaw=0.0,tilt=0.0,burn=0.0):
    """The dragon, facing left. state: fly (wings beating) | perch (feet at y, wings folded up) |
    tumble (spinning off, tilt radians) | dead (lying on the ground) | bones (burnt away)."""
    x,y=int(x),int(y)
    if state in ('dead','bones'):
        body=SCALE_C if state=='dead' else (230,226,210)
        if state=='dead':
            d.polygon([(x-6,y-4),(x+6,y-14),(x+30,y-4),(x+16,y-1)],fill=WING,outline=INK)     # a flat wing
            d.ellipse([x-14,y-7,x+14,y],fill=body,outline=INK)
            d.line([x-14,y-3,x-26,y-1],fill=body,width=3); d.ellipse([x-32,y-5,x-24,y],fill=body,outline=INK)
            d.line([x+14,y-3,x+34,y-1],fill=body,width=2)
            if burn>0:                                                # the flesh burning away
                rr=random.Random(f//2)
                for _ in range(int(20*burn)): d.point((x+rr.randint(-14,30),y-rr.randint(0,10)),fill=rr.choice(SOUL))
        else:
            d.line([x-14,y-3,x+14,y-3],fill=body); d.line([x-14,y-3,x-28,y-2],fill=body); d.line([x+14,y-3,x+34,y-1],fill=body)
            for k in range(6): d.arc([x-12+k*4,y-9,x-6+k*4,y+1],180,360,fill=body)            # the ribs
            d.ellipse([x-33,y-5,x-25,y],outline=body); d.point((x-31,y-3),fill=INK)
        return
    s=math.sin(tilt); c=math.cos(tilt)
    P=lambda u,v: (x+u*c-v*s, y+u*s+v*c)                              # body coordinates -> screen
    if state=='fly':
        flap=math.sin(f*0.5)*8
        for side,dx in ((-1,0),(1,4)):
            d.polygon([P(-2+dx,-14),P(6+dx,-34-flap*side*0.5),P(26+dx,-26-flap*0.6),P(18+dx,-12)],fill=WING,outline=INK)
    elif state in ('perch','tumble'):
        d.polygon([P(-2,-14),P(4,-36),P(22,-30),P(16,-14)],fill=WING,outline=INK)               # folded up
    d.line([P(14,-10),P(34,-6),P(42,-14)],fill=SCALE_C,width=3)                               # the tail
    d.polygon([P(-14,-13),P(-6,-19),P(8,-20),P(16,-13),P(8,-6),P(-6,-6)],fill=SCALE_C,outline=INK)   # the body
    d.line([P(-6,-8),P(10,-8)],fill=BELLY)
    if state=='perch':
        for lx in (-6,8): d.line([P(lx,-8),P(lx-2,0)],fill=SCALE_C,width=2)
    d.line([P(-12,-16),P(-20,-24),P(-24,-26)],fill=SCALE_C,width=4)                              # the neck
    hx,hy=P(-30,-26)
    d.polygon([(hx-6,hy-2),(hx+4,hy-4),(hx+6,hy+1),(hx-4,hy+2)],fill=SCALE_C,outline=INK)       # the head
    o=int(4*jaw); d.polygon([(hx-6,hy+2),(hx+4,hy+2),(hx-4,hy+3+o)],fill=(70,40,40),outline=INK)   # the jaw
    for hk in (0,3): d.line([hx+2+hk,hy-4,hx+6+hk,hy-9],fill=(220,210,180))                     # horns
    d.point((int(hx-1),int(hy-1)),fill=(255,200,60))
    return hx-6,hy+1                                                   # the mouth

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
    if 200<=f<330: dstate,dx,dy,hp='dead' if f<280 else 'bones',150,GROUND+1,0.85
    if 220<=f<280: burn=(f-220)/60
    if 240<=f<300:
        pose='armsup'; s['fx'].append(('sk_souls',150,GROUND-6,CX,GROUND-8,(f-240)/60))
    if 262<=f<300: s['fx'].append(('big',"DRAGON SOUL ABSORBED",44,(255,220,170)))
    if 320<=f<330: dstate=None
    # draw
    if dstate: s['under' if dstate in ('dead','bones') else 'fx'].append(('sk_dragon',dx,dy,dstate,jaw,tilt,burn))
    mouth=None
    if dstate=='perch':
        mouth=(PERCH[0]-36,PERCH[1]-25)
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
