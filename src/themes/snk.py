"""Shingeki no Kyojin: Claude, a Survey Corps scout, vs a grinning Titan in the streets of Trost —
red roofs, the church spire and the huge Wall behind. Thuds, the birds scatter; the Titan's face
rises over the rooftops (close-up: the grin, the tiny pupils). It crashes through a roof and grabs
for Claude, who fires the ODM gear into the spire and swings clear. Close-up: the blades cross —
SHINZOU WO SASAGEYO! Claude zips in, cuts off the swatting hand, swings over its head off the Wall,
dives spinning onto the nape: one slash, a burst of steam. The Titan topples into the street and
evaporates; Claude walks back through the steam."""
from engine import *

THEME = 'snk'
N_ = 336
CX = 30                                                             # the loop keyframe position

PAL.update({'t':(232,186,160),'T':(194,146,122),'z':(208,174,112),'a':(132,100,62)})
# Claude in Survey Corps gear: green cloak behind, brown belt, grey ODM boxes on the hips.
SCOUT=variant(lambda s: recolor_rows(s,
    lambda x,y,t,l,r,c: ('X' if c in '.o' and x<l else None) if (t+1<=y<=t+8 and l-2<=x<l) else
                        ('q' if (y==t+6 and l<=x<=r and c=='O') else ('D' if (y==t+7 and x in (l,r)) else None))))

# ---- local glyphs: a wider W and M (the 3x5 font's read as H) ------------------------------------
_GLYPH = {'M':(5,"10001"+"11011"+"10101"+"10001"+"10001"), 'W':(5,"10001"+"10001"+"10101"+"11011"+"10001"),
          'N':(4,"1001"+"1101"+"1011"+"1001"+"1001")}

def _mask(txt):
    gl=[_GLYPH.get(ch) or (3,''.join(FONT.get(ch,FONT[' '])[j*3:j*3+3] for j in range(5))) for ch in txt]
    m=Image.new('L',(sum(w+1 for w,_ in gl)-1,5),0); md=ImageDraw.Draw(m); x=0
    for w,bits in gl:
        for j,b in enumerate(bits):
            if b=='1': md.point((x+j%w,j//w),fill=255)
        x+=w+1
    return m

def say(im,txt,y,c,scale=2,cx=W//2,outline=None):
    """big_text with the local glyphs (outline + drop shadow)."""
    m=_mask(txt); m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        im.paste((0,0,0),(x+2,y+2),m)
    im.paste(c,(x,y),m)

@fx('snk_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,cx=W//2,outline=(40,30,20)):
    s['fx'].append(('snk_say',txt,y,c,scale,cx,outline))

# ---- background: Trost district — the Wall, the church spire, red-roofed houses -----------------
SKY_TOP,SKY_LOW=(92,124,178),(242,192,144)
WALL_TOP=13
CHURCH=64                                                           # the spire tip: (CHURCH, 2)
TIMBER=(108,72,50)
# (x0, width, facade top, gable?, wall colour, roof colour)
HOUSES=[(0,18,42,1,(232,220,196),(176,62,44)),(19,15,37,0,(220,204,176),(158,52,40)),
        (35,17,44,0,(236,226,204),(190,84,52)),(73,17,40,1,(226,212,186),(170,58,42)),
        (91,17,44,0,(214,200,174),(186,78,50)),(109,18,38,1,(234,222,198),(156,50,38)),
        (128,18,42,0,(222,208,182),(180,66,46)),(147,19,37,1,(232,218,192),(166,56,40)),
        (167,18,41,0,(218,204,178),(188,80,50))]

def _shade(c,k): return tuple(int(v*k) for v in c)

def _sky(d):
    for y in range(47):
        k=y/46; d.line([0,y,W,y],fill=tuple(int(a+(b-a)*k) for a,b in zip(SKY_TOP,SKY_LOW)))

def _wall(d):
    stone,course,lit=(170,160,148),(148,138,126),(204,194,178)
    d.rectangle([0,WALL_TOP,W,47],fill=stone)
    for i,y in enumerate(range(WALL_TOP+3,47,4)):
        d.line([0,y,W,y],fill=course)
        for x in range((i%2)*6,W,12): d.line([x,y+1,x,y+3],fill=course)
    rr=random.Random(515)
    for _ in range(22):                                             # weathering streaks
        x=rr.randint(0,W); y=rr.randint(WALL_TOP+3,40); d.line([x,y,x,y+rr.randint(2,6)],fill=(140,128,112))
    d.line([0,WALL_TOP,W,WALL_TOP],fill=lit)
    for x in range(0,W,7):                                          # the battlements
        d.rectangle([x,WALL_TOP-3,x+3,WALL_TOP-1],fill=stone); d.line([x,WALL_TOP-3,x+3,WALL_TOP-3],fill=lit)
    far=(170,112,96)                                                # distant roofs, lost in the haze
    for i,x in enumerate(range(-6,W,11)):
        h=5+(i*7)%5; d.polygon([(x,47),(x+5,47-h),(x+11,47)],fill=far)
        d.rectangle([x+2,47-h+3,x+9,47],fill=(196,170,150) if i%2 else (186,160,142))
        d.polygon([(x,47-h+3),(x+5,47-h-1),(x+11,47-h+3)],fill=far)

def _spire(d):
    x=CHURCH
    d.polygon([(x-6,20),(x+6,20),(x,3)],fill=(76,108,100)); d.polygon([(x,3),(x+6,20),(x,20)],fill=(56,82,78))
    d.line([x,0,x,3],fill=(222,196,120)); d.line([x-1,1,x+1,1],fill=(222,196,120))

def _church(d):
    x=CHURCH
    d.rectangle([x-5,20,x+5,56],fill=(214,202,180)); d.rectangle([x+3,20,x+5,56],fill=(180,168,148))
    d.rectangle([x-6,20,x+6,21],fill=(190,178,158))
    d.rectangle([x-2,24,x+1,29],fill=(54,46,52)); d.point((x-2,24),fill=(214,202,180)); d.point((x+1,24),fill=(214,202,180))
    d.ellipse([x-3,32,x+3,38],fill=(238,232,214),outline=(126,114,100)); d.line([x,35,x,33],fill=(40,34,30)); d.line([x,35,x+2,35],fill=(40,34,30))
    d.rectangle([x-2,49,x+1,56],fill=(96,62,42)); d.line([x-6,44,x+6,44],fill=(190,178,158))
    _spire(d)

def _house(d,x0,w,top,gable,wc,rc):
    x1=x0+w-1; dark=_shade(rc,0.78)
    d.rectangle([x0,top,x1,56],fill=wc)
    for x in (x0,x1): d.line([x,top,x,56],fill=TIMBER)
    d.line([x0,top+7,x1,top+7],fill=TIMBER)
    if gable:
        rh=w//2; peak=top-rh
        d.polygon([(x0-1,top),(x1+1,top),((x0+x1)//2,peak)],fill=rc)
        for y in range(peak+2,top,2):
            hw=(y-peak)/rh*(w/2); d.line([(x0+x1)/2-hw+1,y,(x0+x1)/2+hw-1,y],fill=dark)
        d.rectangle([(x0+x1)//2-1,top-4,(x0+x1)//2,top-3],fill=(58,50,60))   # attic window
    else:
        d.polygon([(x0-1,top),(x1+1,top),(x1-3,top-7),(x0+3,top-7)],fill=rc)
        for y in range(top-5,top,2): d.line([x0+1,y,x1-1,y],fill=dark)
        d.rectangle([x1-5,top-10,x1-3,top-6],fill=(150,96,72))       # chimney
    d.line([x0-1,top,x1+1,top],fill=_shade(rc,0.6))
    for wx in range(x0+3,x1-2,5):
        for wy in (top+2,top+9):
            if wy+3<56: d.rectangle([wx,wy,wx+1,wy+2],fill=(58,50,62)); d.point((wx,wy),fill=(250,214,140))
    dx=(x0+x1)//2-1; d.rectangle([dx,52,dx+2,56],fill=(98,62,42))

def roof_peak(x):
    """Top of the roofline at x (for the Titan's hands gripping it)."""
    for x0,w,top,gable,_,_ in HOUSES:
        if x0<=x<x0+w: return top-(w//2 if gable else 7)
    return 40

def _street(d,x0=0,x1=W):
    d.rectangle([x0,56,x1,57],fill=(132,120,108)); d.line([x0,58,x1,58],fill=(150,138,124))
    d.rectangle([x0,59,x1,H],fill=(80,72,68))
    for x in range(x0-x0%6,x1+1,6):
        for y,o in ((59,0),(61,3),(63,0)): d.line([x+o,y,x+o+3,y],fill=(104,94,86))
        d.point((x+2,57),fill=(104,94,86))

def _houses(d,xmin=-99):
    d.rectangle([max(0,xmin-1),47,W,56],fill=(112,98,90))           # the shadowed back alleys
    for h in HOUSES:
        if h[0]>=xmin: _house(d,*h)
    _street(d,max(0,xmin-1))

def _trost(d):
    _sky(d); _wall(d); _church(d); _houses(d)

register_bg(THEME, lambda v: (v,v-4,v-10), decor=_trost)

# ---- the Titan: a grinning, naked giant, drawn on its own layer (so it can topple over) ----------
SKIN,SKIN_SH,SKIN_DK=(232,186,160),(198,148,122),(150,100,82)
HAIR,MOUTH,TEETH=(96,62,40),(104,28,32),(248,240,224)
TL_W,TL_H,TL_PX,TL_PY=150,110,92,104                                # layer size, feet pivot
REST,GRAB,SWAT=(-12,-16),(-38,-6),(-30,-42)                         # front hand, relative to the feet
_TIT={}

def titan_layer(step=0,hand=REST,jaw=0,look=-1,cut=False):
    key=(step,hand,jaw,look,cut)
    if key in _TIT: return _TIT[key]
    im=Image.new('RGBA',(TL_W,TL_H),(0,0,0,0)); d=ImageDraw.Draw(im)
    cx,fy=TL_PX,TL_PY; top=fy-56; st=step/4
    d.line([(cx+9,top+21),(cx+13,top+31),(cx+12-st,top+40)],fill=SKIN_SH,width=4,joint='curve')   # back arm
    d.ellipse([cx+9-st,top+38,cx+14-st,top+43],fill=SKIN_SH)
    for side,col in ((1,SKIN_SH),(-1,SKIN)):                        # legs: back one first
        ft=cx+side*4+st*side*5; kn=(cx+side*4+st*side*2-1,top+46)
        d.line([(cx+side*3,top+36),kn,(ft,fy-2)],fill=col,width=5,joint='curve')
        d.ellipse([ft-5,fy-3,ft+2,fy],fill=col)
    d.polygon([(cx-10,top+20),(cx+10,top+20),(cx+8,top+38),(cx-8,top+38)],fill=SKIN)   # torso
    d.polygon([(cx+5,top+20),(cx+10,top+20),(cx+8,top+38),(cx+4,top+38)],fill=SKIN_SH)
    d.line([cx-7,top+26,cx-2,top+27],fill=SKIN_DK); d.line([cx+1,top+27,cx+5,top+26],fill=SKIN_DK)
    for y in (29,31): d.line([cx-6,top+y,cx-4,top+y],fill=SKIN_SH)
    d.point((cx-1,top+33),fill=SKIN_DK); d.line([cx-7,top+37,cx+6,top+37],fill=SKIN_SH)
    d.rectangle([cx-3,top+16,cx+3,top+21],fill=SKIN); d.line([cx+2,top+16,cx+2,top+21],fill=SKIN_SH)   # neck
    hx=cx-2                                                         # head, turned to the left
    d.ellipse([hx-9,top,hx+8,top+19],fill=SKIN); d.ellipse([hx+6,top+8,hx+9,top+12],fill=SKIN_SH)
    d.chord([hx-9,top-1,hx+8,top+13],180,360,fill=HAIR)
    d.polygon([(hx+8,top+5),(hx+10,top+14),(hx+5,top+9)],fill=HAIR)
    for bx in (hx-8,hx-4,hx):                                       # bangs
        d.polygon([(bx,top+5),(bx+4,top+5),(bx+1,top+8)],fill=HAIR)
    for ex in (hx-7,hx-1):                                          # the wide, staring eyes
        d.ellipse([ex,top+7,ex+4,top+11],fill=(246,242,232),outline=(60,36,30))
        d.point((ex+2+look,top+9),fill=(16,10,10))
    d.line([hx-4,top+11,hx-4,top+12],fill=SKIN_DK)
    my=top+14; mh=1+jaw                                             # the grin
    d.rectangle([hx-7,my,hx+4,my+mh+1],fill=MOUTH)
    d.line([hx-7,my,hx+4,my],fill=TEETH); d.line([hx-7,my+mh+1,hx+4,my+mh+1],fill=TEETH)
    for tx in range(hx-6,hx+4,2): d.point((tx,my),fill=(180,160,150))
    d.point((hx-8,my-1),fill=SKIN_DK); d.point((hx+5,my-1),fill=SKIN_DK)
    sh=(cx-9,top+21); hand_=(cx+hand[0],fy+hand[1])                 # front arm
    el=((sh[0]+hand_[0])/2-4,(sh[1]+hand_[1])/2+3)
    if cut:
        k=0.55; hand_=(el[0]+(hand_[0]-el[0])*k,el[1]+(hand_[1]-el[1])*k)
        d.line([sh,el,hand_],fill=SKIN,width=4,joint='curve')
        d.ellipse([hand_[0]-2,hand_[1]-2,hand_[0]+2,hand_[1]+2],fill=(200,50,44))
    else:
        d.line([sh,el,hand_],fill=SKIN,width=4,joint='curve')
        hx_,hy_=hand_; d.ellipse([hx_-3,hy_-3,hx_+3,hy_+3],fill=SKIN)
        for k in (-2,0,2): d.line([hx_-3,hy_+k,hx_-5,hy_+k+1],fill=SKIN)
    a=im.split()[3].filter(ImageFilter.MaxFilter(3))                # dark outline
    out=Image.new('RGBA',(TL_W,TL_H),(0,0,0,0)); out.paste((34,18,16,255),(0,0),a); out.alpha_composite(im)
    _TIT[key]=out; return out

def nape_of(x,feet=GROUND): return x+4, feet-38

def stump_of(x,hand,feet=GROUND):
    """World position of the cut forearm's end (same maths as titan_layer)."""
    sh=(-9,-35); el=((sh[0]+hand[0])/2-4,(sh[1]+hand[1])/2+3)
    return x+el[0]+(hand[0]-el[0])*0.55, feet+el[1]+(hand[1]-el[1])*0.55

@fx('snk_titan')
def _fx_titan(d,im,e,f):
    """('snk_titan', x, feet, angle, alpha, white, step, hand, jaw, look, cut): angle>0 falls to the left."""
    _,x,feet,angle,alpha,white,*p=e
    lay=titan_layer(*p)
    if angle: lay=lay.rotate(angle,resample=Image.NEAREST,center=(TL_PX,TL_PY))
    a=lay.split()[3]
    if alpha<1: a=a.point(lambda v: int(v*alpha))
    pos=(int(x)-TL_PX,int(feet)-TL_PY)
    im.paste((255,255,255) if white else lay.convert('RGB'),pos,a)

def titan(s,x,feet=GROUND,angle=0,alpha=1,white=False,step=0,hand=REST,jaw=0,look=-1,cut=False,under=True):
    hand=(int(round(hand[0])),int(round(hand[1])))
    (s['under'] if under else s['fx']).append(('snk_titan',x,feet,angle,alpha,white,step,hand,jaw,look,cut))

def walk_step(f): return int(round(4*math.sin(f*0.39)))

@fx('snk_front')
def _fx_front(d,im,e,f):
    """The houses from x0 on (and the street) redrawn over the Titan; hands grip the roofs."""
    _,x0,hands=e; _houses(d,x0)
    for hx in hands:
        y=roof_peak(hx)+1
        d.ellipse([hx-5,y-3,hx+4,y+2],fill=(34,18,16)); d.ellipse([hx-4,y-2,hx+3,y+1],fill=SKIN)
        for k in (-3,-1,1,3): d.line([hx+k,y+1,hx+k,y+3],fill=SKIN); d.point((hx+k,y+4),fill=(34,18,16))

# ---- effects -----------------------------------------------------------------------------------
@fx('wire')
def _fx_wire(d,im,e,f):
    """An ODM gear cable from Claude's hip to the anchor, with the hook glinting."""
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(120,120,134)); d.line([x0,y0-1,x1,y1-1],fill=(196,198,210))
    d.point((int(x1),int(y1)),fill=(255,255,255))

@fx('blades')
def _fx_blades(d,im,e,f):
    _,x,y,fl=e; s_=-1 if fl else 1
    d.line([x+6*s_,y-5,x+14*s_,y-8],fill=(220,224,238)); d.line([x+5*s_,y-3,x+13*s_,y-3],fill=(200,206,222))

CLOUDS=[(0,4,1.0),(62,8,0.7),(118,2,0.85),(176,6,0.6)]             # (x, y, size) — a 225px loop
@fx('snk_clouds')
def _fx_clouds(d,im,e,f):
    """Clouds drifting right, one lap per clip (seamless loop); the spire stays in front."""
    o=f*225//N_
    for x0,y,k in CLOUDS:
        x=(x0+o)%225-20
        for dx,dy,r in ((0,2,3),(5,0,4),(11,1,3),(16,2,2)):
            rr_=max(1,int(r*k)); c=x+dx*k; d.ellipse([c-rr_,y+dy-rr_,c+rr_,y+dy+rr_//2],fill=(252,236,220))
        d.line([x-2,y+3,x+int(18*k),y+3],fill=(236,196,176))
    _spire(d)

@fx('snk_birds')
def _fx_birds(d,im,e,f):
    """A flock scattering from the spire, wings flapping."""
    _,t=e; rr=random.Random(33)
    for i in range(8):
        vx,vy=rr.uniform(-2.2,-0.6),rr.uniform(-1.1,-0.3); x=CHURCH+rr.randint(-4,4)+vx*t; y=12+rr.randint(-3,5)+vy*t+0.004*t*t
        if -3<x<W and y>-3:
            up=(f+i)%4<2; c=(40,34,40)
            d.point((int(x),int(y)),fill=c)
            d.point((int(x)-1,int(y)-(1 if up else 0)),fill=c); d.point((int(x)+1,int(y)-(1 if up else 0)),fill=c)

@fx('snk_steam')
def _fx_steam(d,im,e,f):
    """Titan steam: soft white puffs [(x,y,r)] with a grey underside, alpha a."""
    _,puffs,a=e
    for off,c,k in ((1,(178,170,176),0.8),(0,(246,244,240),1.0)):
        m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
        for x,y,r in puffs: md.ellipse([x-r+off,y-r+off,x+r+off,y+r+off],fill=int(255*a*k))
        im.paste(c,(0,0),m)

def steam(s,x,y,t,n=10,spread=10,rise=0.8,size=1.0,a=0.85,seed=0,fade=1.0):
    """A column of steam rising from (x,y): puffs cycle so it keeps flowing while t advances."""
    rr=random.Random(seed); puffs=[]
    for j in range(n):
        ox,ph,L=rr.uniform(-spread,spread),rr.uniform(0,30),rr.randint(22,34)
        age=(t+ph)%L; yy=y-age*rise*(0.7+0.3*(j%3)); r=(1.5+age*0.22)*size*(1-0.5*age/L)
        if t+ph>=L*0 and r>=1: puffs.append((x+ox+age*0.15*(1 if j%2 else -1),yy,r))
    if puffs and fade>0: s['fx'].append(('snk_steam',puffs,a*fade))

@fx('snk_slash')
def _fx_slash(d,im,e,f):
    """Twin blade arcs: a white crescent with a cold blue edge."""
    _,x,y,r,a0,a1=e
    d.arc([x-r-1,y-r-1,x+r+1,y+r+1],a0,a1,fill=(140,190,255),width=3)
    d.arc([x-r,y-r,x+r,y+r],a0,a1,fill=(255,255,255),width=2)
    d.arc([x-r+4,y-r+4,x+r-4,y+r-4],a0+10,a1-10,fill=(220,236,255),width=1)

@fx('snk_gas')
def _fx_gas(d,im,e,f):
    """ODM gas puffs left behind along the flight path."""
    _,pts=e
    for i,(x,y) in enumerate(pts):
        r=1+i//3; d.ellipse([x-r,y-r,x+r,y+r],fill=(236,236,240) if i%2 else (200,202,210))

@fx('snk_hand')
def _fx_hand(d,im,e,f):
    """The severed hand, tumbling."""
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-4,y-4,x+4,y+4],fill=(34,18,16)); d.ellipse([x-3,y-3,x+3,y+3],fill=SKIN)
    d.rectangle([x+2,y-1,x+4,y+1],fill=(200,50,44))

@fx('snk_chunk')
def _fx_chunk(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.rectangle([x-2,y-1,x+2,y+1],fill=(34,18,16)); d.rectangle([x-1,y,x+1,y],fill=(210,70,60))

@fx('snk_speed')
def _fx_speed(d,im,e,f):
    """Speed lines converging on a point (the dive)."""
    _,cx,cy=e; rr=random.Random(f*5)
    for _ in range(14):
        a=rr.random()*6.283; r0=rr.randint(26,40)
        d.line([cx+math.cos(a)*r0,cy+math.sin(a)*r0*0.6,cx+math.cos(a)*(r0+60),cy+math.sin(a)*(r0+60)*0.6],fill=(255,255,255))

@fx('snk_tiles')
def _fx_tiles(d,im,e,f):
    """Roof tiles and dust blown off by the Titan crashing through (t frames since)."""
    _,x,y,t=e; rr=random.Random(71)
    for i in range(14):
        vx,vy=rr.uniform(-2.4,2.4),rr.uniform(-3.4,-1.2); px=x+vx*t; py=y+vy*t+0.28*t*t
        if py<GROUND: d.rectangle([px,py,px+1,py],fill=(176,62,44) if i%3 else (150,138,124))

# ---- close-up 1: the Titan's grin over the rooftops ----------------------------------------------
def closeup_titan(t,f):
    """Primer plano: the huge grinning face slowly pushes in, the tiny pupils lock onto Claude."""
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im); _sky(d)
    k=1+0.14*ease(t); cx,cy=92,30
    P=lambda x,y:(cx+(x-cx)*k,cy+(y-cy)*k)
    E=lambda x0,y0,x1,y1:[*P(x0,y0),*P(x1,y1)]
    d.ellipse(E(16,-40,168,112),fill=(34,18,16)); d.ellipse(E(18,-38,166,110),fill=SKIN_SH)
    d.ellipse(E(18,-38,152,110),fill=SKIN)
    d.ellipse(E(8,-64,176,12),fill=HAIR)                            # hair and bangs
    for bx in range(24,160,16): d.polygon([P(bx,6),P(bx+18,6),P(bx+7,16)],fill=HAIR)
    rr=random.Random(9)
    for _ in range(10):
        x=rr.randint(20,164); d.line([P(x,-6),P(x+rr.randint(-4,4),8)],fill=(70,44,28))
    look=ease((t-0.25)/0.2); pr=3-ease((t-0.45)/0.2)                # pupils snap left, then shrink
    for ex in (62,120):
        d.ellipse(E(ex-17,17,ex+17,35),fill=(60,36,30)); d.ellipse(E(ex-15,19,ex+15,33),fill=(246,242,232))
        for vx in (-12,11): d.line([P(ex+vx,24),P(ex+vx-2*(1 if vx>0 else -1),28)],fill=(226,150,140))
        px,py=P(ex+2-9*look,27); r=pr*k+0.5
        d.ellipse([px-r,py-r,px+r,py+r],fill=(16,10,10))
        d.arc(E(ex-16,30,ex+16,40),20,160,fill=SKIN_DK)             # the bags under the eyes
        d.line([P(ex-14,14),P(ex+12,12)],fill=SKIN_DK)
    d.point(P(86,43),fill=(90,50,40)); d.point(P(98,43),fill=(90,50,40)); d.line([P(92,34),P(90,41)],fill=SKIN_SH)
    jaw=4*ease((t-0.6)/0.2)                                         # the grin (it opens a little)
    def lip(x,up): return (47-8*((x-92)/50)**2) if up else (55+jaw-5*((x-92)/50)**2)
    xs=list(range(42,143,4))
    d.polygon([P(x,lip(x,1)) for x in xs]+[P(x,lip(x,0)) for x in reversed(xs)],fill=MOUTH)
    for x in range(44,140,7):                                       # upper and lower teeth
        tu=lip(x+3,1); tl=lip(x+3,0)
        d.rectangle(E(x+1,tu,x+6,tu+4+jaw*0.2),fill=TEETH); d.rectangle(E(x+1,tl-4,x+6,tl),fill=(236,226,208))
    d.line([P(x,lip(x,1)-1) for x in xs],fill=SKIN_DK)
    d.line([P(x,lip(x,0)+1) for x in xs],fill=SKIN_DK)
    for sx in (38,146): d.arc(E(sx-6,36,sx+6,52),(300 if sx<92 else 120),(60 if sx<92 else 240),fill=SKIN_DK)
    if jaw>1: steam_puffs=[(92+24*math.sin(i*1.7+f*0.2),52+jaw-((f*1.2+i*9)%24),3+i%3) for i in range(6)]; _fx_steam(d,im,('',steam_puffs,0.55),f)
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.8)
    return im

# ---- close-up 2: the blades cross — SHINZOU WO SASAGEYO! ------------------------------------------
def _blade(d,x0,y0,x1,y1,glint):
    dx,dy=x1-x0,y1-y0; L=math.hypot(dx,dy); nx,ny=-dy/L,dx/L
    d.polygon([(x0,y0),(x1,y1),(x1+nx*3,y1+ny*3),(x0+nx*4,y0+ny*4)],fill=(206,212,226))
    d.line([x0+nx*4,y0+ny*4,x1+nx*3,y1+ny*3],fill=(150,156,172)); d.line([x0,y0,x1,y1],fill=(252,252,255))
    for s_ in range(14,int(L),14):                                  # the segmented blade's snap lines
        px,py=x0+dx*s_/L,y0+dy*s_/L; d.line([px,py,px+nx*4,py+ny*4],fill=(150,156,172))
    if 0<=glint<=1:
        gx,gy=x0+dx*glint,y0+dy*glint; d.ellipse([gx-2,gy-2,gx+2,gy+2],fill=(255,255,255))
    d.rectangle([x0-5,y0-3,x0+3,y0+3],fill=(34,18,16)); d.rectangle([x0-4,y0-2,x0+2,y0+2],fill=(120,122,134))
    d.ellipse([x0-6,y0-4,x0,y0+3],fill=(217,119,87),outline=(34,18,16))

def closeup_scout(t,f):
    """Primer plano: Claude's narrowed eyes, the blades slide in and cross; the battle cry."""
    im=Image.new('RGB',(W,H),(22,52,56)); d=ImageDraw.Draw(im)
    for i in range(-4,24):                                          # diagonal speed stripes
        x=i*10+(f*3)%10; d.line([x,0,x-24,H],fill=(30,70,72))
    jx=((f%3)-1) if 0.28<=t<0.6 else 0
    ox=10+jx
    d.rectangle([ox+16,6,ox+72,H],fill=(217,119,87)); d.rectangle([ox+16,6,ox+21,H],fill=(176,92,66))
    for ex in (ox+34,ox+54):                                        # narrowed, determined eyes
        d.rectangle([ex,24,ex+4,34],fill=(24,14,12)); d.point((ex+1,26),fill=(255,255,255))
    d.polygon([(ox+32,22),(ox+40,22),(ox+40,27)],fill=(217,119,87)); d.polygon([(ox+60,22),(ox+52,22),(ox+52,27)],fill=(217,119,87))
    d.line([ox+31,21,ox+40,26],fill=(24,14,12)); d.line([ox+61,21,ox+52,26],fill=(24,14,12))
    d.polygon([(ox+8,H),(ox+20,52),(ox+44,58),(ox+68,52),(ox+80,H)],fill=(40,150,95))   # cloak collar
    d.polygon([(ox+36,H),(ox+44,58),(ox+52,H)],fill=(236,230,214)); d.line([ox+28,56,ox+24,H],fill=(112,72,42))
    slide=1-ease(t/0.18)                                            # the blades slide in and cross
    ga=(t-0.22)/0.25; gb=(t-0.3)/0.25
    _blade(d,4-40*slide,62+10*slide,100-40*slide,20+10*slide,ga)
    _blade(d,116+40*slide,62+10*slide,20+40*slide,20+10*slide,gb)
    if 0.17<=t<0.24:                                                # the SHING at the crossing
        spark(d,60,41,8,(200,230,255)); zoom_lines(d,(200,230,255))
    if t>=0.28: say(im,"SHINZOU WO",10,(255,255,255),scale=2,cx=138+jx,outline=(20,60,50))
    if t>=0.46: say(im,"SASAGEYO!",32,(255,226,120),scale=2,cx=138+jx,outline=(90,50,10))
    if t<0.05: zoom_lines(d)
    if t>0.9: im=fade_to(im,(255,255,255),(t-0.9)/0.1*0.7)
    return im

# ---- the clip ----------------------------------------------------------------------------------
TXP,TXS=154,112                                                     # the Titan: peeking, in the street
def swing(a,b,t,lift):
    """Flight between two points along an arc bowed upward by `lift` px."""
    e=ease(t); return (lerp(a[0],b[0],e),lerp(a[1],b[1],e)-lift*math.sin(math.pi*e))

def clip_survey(f):
    s=scene(f,THEME); s['under'].append(('snk_clouds',))
    pos=(CX,GROUND); pose=None; flip=False; blades=True; spr=None; hooks=[]; gas=None
    # 1) Trost at dusk: thuds, the birds scatter from the spire
    if f in (14,26,38,50): s['shake']=rshake()
    if 14<=f<96: s['under'].append(('snk_birds',f-14))
    if 30<=f<48: shout(s,"!",(255,230,90),y=GROUND-26-(1 if f<33 else 0),scale=2,cx=CX+1)
    # 2) the Titan's face rises over the rooftops, hands on the roofs
    if 40<=f<76:
        k=ease((f-40)/20); titan(s,TXP,GROUND+62-44*k,look=-1 if f>=56 else 0)
        s['under'].append(('snk_front',128,(136,176) if f>=58 else ()))
        if f==58: s['shake']=rshake()
    if 56<=f<76: pose='charge'
    # 3) close-up: the grin
    if 76<=f<112: s['image']=closeup_titan((f-76)/36,f); return s
    # 4) it crashes through a roof and grabs; Claude fires into the spire and swings clear
    hand=REST; jaw=0; cut=False; tx=None; feet=GROUND; step=0; angle=0; alpha=1; white=False; look=-1
    if 112<=f<124:
        tx=lerp(TXP,146,(f-112)/12); feet=lerp(GROUND+18,GROUND,ease((f-112)/12)); step=walk_step(f)
        s['under'].append(('snk_front',109,()))
    if 124<=f<140:
        tx=lerp(146,TXS,(f-124)/16); step=walk_step(f)
        if f%8==0: s['shake']=rshake()
    if 124<=f<146: s['under'].append(('snk_tiles',136,40,f-124))
    if f==124: s['shake']=rshake(2)
    if 140<=f<192:
        tx=TXS
        if f<148: hand=(lerp(REST[0],GRAB[0],ease((f-140)/8)),lerp(REST[1],GRAB[1],ease((f-140)/8)))
        else: hand=GRAB
    if f==148:
        s['shake']=rshake(2)
    if 148<=f<160:
        rr=random.Random(f)
        for j in range(8): s['fx'].append(('smoke',TXS-38+rr.randint(-8,8),GROUND-rr.randint(0,5)-(f-148)//3,rr.randint(1,3),(170,150,124) if j%2 else (200,184,160)))
    if 116<=f<132: pos=(ez(CX,72,(f-116)/16),GROUND)
    if 132<=f<144: pos=(72,GROUND); pose='charge'
    if 144<=f<156:                                                  # the pendulum swing off the spire
        t=(f-144)/12; a=lerp(0.14,-1.1,ease(t)); r=lerp(55,34,ease(t*1.4))
        pos=(CHURCH+r*math.sin(a),2+r*math.cos(a)); pose='dash'; flip=True; hooks=[(CHURCH,4),(CHURCH-1,6)]
        gas=[(pos[0]+4+i*2,pos[1]-5+i) for i in range(6)]
    # 5) close-up: the blades cross
    if 156<=f<192: s['image']=closeup_scout((f-156)/36,f); return s
    # 6) ODM assault: zip in, the swatting hand is cut off, over its head off the Wall
    nx,ny=nape_of(TXS)
    if 192<=f<246: tx=TXS
    if 192<=f<204:
        t=(f-192)/12; pos=swing((20,32),(TXS-24,20),t,10); pose='dash'; hooks=[(TXS-9,GROUND-35)]
        gas=[(pos[0]-4-i*2,pos[1]-5+i) for i in range(6)]
        hand=(lerp(GRAB[0],SWAT[0],ease(t)),lerp(GRAB[1],SWAT[1],ease(t)))
    if 204<=f<210:
        pos=(TXS-24,20); pose='punch'; hand=SWAT; cut=f>=205; flip=f%2==1
        if f==205:
            s['flash']=0.7; s['fc']=(TXS-30,GROUND-42); s['shake']=rshake(2)
        if f<209: s['fx'].append(('snk_slash',TXS-30,GROUND-44,9,200,340))
    if f>=205 and 192<=f<246: cut=True; hand=SWAT if f<214 else (lerp(SWAT[0],REST[0],ease((f-214)/10)),lerp(SWAT[1],REST[1],ease((f-214)/10)))
    if 205<=f<219:                                                  # the hand drops into the street
        k=f-205; s['fx'].append(('snk_hand',TXS-30-k*0.8,GROUND-42+0.2*k*k+k*0.2))
        for j in range(3): s['fx'].append(('shard',TXS-28+random.randint(-3,3),GROUND-40+random.randint(0,k),(210,60,50)))
    if f==219: s['shake']=rshake(2)
    if 219<=f<228:
        rr=random.Random(f)
        for j in range(6): s['fx'].append(('smoke',TXS-41+rr.randint(-6,6),GROUND-rr.randint(0,4)-(f-219)//2,rr.randint(1,3),(170,150,124) if j%2 else (200,184,160)))
    if 205<=f<226: jaw=min(3,(f-205)//2); s['shake']=s['shake'] if f in (205,219) else (rshake() if f%3==0 else (0,0))
    if 210<=f<226:
        t=(f-210)/16; pos=swing((TXS-24,20),(152,8),t,14); pose='dash'; hooks=[(158,WALL_TOP)]
        gas=[(pos[0]-4-i*2,pos[1]-4+i) for i in range(6)]; look=1 if t>0.5 else -1
    if 226<=f<234:
        pos=(152,8); pose='charge'; flip=True; hooks=[(158,WALL_TOP)]; look=1
    # 7) the dive, spinning, onto the nape — one slash, the steam bursts
    if 234<=f<244:
        t=(f-234)/10; pos=(lerp(152,nx+6,t*t),lerp(8,ny+4,t*t)); spr=rotate90(SCOUT['dash'],3-(f//2)%4); flip=True
        hooks=[(nx,ny)]; s['fx'].append(('snk_speed',pos[0],pos[1]-5)); look=1
        s['fx'].append(('circle',pos[0],pos[1]-5,8,(240,244,255)))
    if 226<=f<246: shout(s,"THE NAPE!",(255,236,140),y=3)
    if 244<=f<248:                                                  # hit-stop
        pos=(nx+6,ny+4); pose='punch'; flip=True; white=f<246
        s['fx'].append(('snk_slash',nx,ny,8,110,290)); s['fx'].append(('snk_slash',nx+1,ny+3,6,120,280))
        if f<246: s['flash']=0.55 if f==244 else 0.3; s['fc']=(nx,ny); s['flashc']=(255,255,255)
        s['shake']=rshake(2)
    if 244<=f<262:
        k=f-244; s['fx'].append(('snk_chunk',nx+4+k*2.2,ny-3-k*2.4+0.22*k*k))
    if 248<=f<262:                                                  # a backflip away, landing behind
        t=(f-248)/14; pos=(lerp(nx+6,140,t),lerp(ny+4,GROUND,t*t)-16*math.sin(math.pi*t))
        spr=rotate90(SCOUT['guard'],(f//2)%4) if t<0.8 else None; flip=True; blades=t>=0.8
    if 244<=f<310:
        steam(s,nx,ny,f-244,n=18,spread=6,rise=1.1,size=1.5,a=0.9,seed=3,fade=1-max(0,(f-290)/20))
    # 8) it topples into the street and evaporates
    if 248<=f<336:
        k=ease(min(1,(f-248)/22)**1.4) if f<270 else 1
        angle=84*k-(3*math.sin((f-270)*0.9)*max(0,1-(f-270)/8) if f>=270 else 0)
        tx=TXS-6*k; feet=GROUND-9*k; jaw=2
        if f>=280: alpha=max(0,1-(f-280)/34)
    if f==270: s['shake']=(0,2)
    if 270<=f<280 and f%2==0: s['shake']=rshake(2)
    if 270<=f<300:
        rr=random.Random(f)
        for j in range(12): s['fx'].append(('smoke',rr.randint(40,112),GROUND-rr.randint(0,6)-(f-270)//3,rr.randint(1,4),(170,150,124) if j%2 else (206,190,166)))
        if f<276:
            for j in range(6): s['fx'].append(('rock',rr.randint(40,110),GROUND-rr.randint(4,16)+(f-270)*2))
    if 272<=f<324:
        fade=min(1,(f-272)/8)*max(0,1-(f-306)/18)
        for i,xx in enumerate(range(56,112,9)): steam(s,xx,GROUND-6,f-272,n=5,spread=5,rise=0.9,size=1.3,a=0.85,seed=20+i,fade=fade)
    if 262<=f<292: pos=(140,GROUND); flip=True
    if 292<=f<324:
        pos=(ez(140,CX,(f-292)/32),GROUND); flip=True
    if tx is not None:
        titan(s,tx,feet,angle,alpha,white,step,hand,jaw,look,cut)
        if cut and 205<=f<290:                                      # steam from the stump
            sx,sy=stump_of(TXS,hand); steam(s,sx,sy,f-205,n=6,spread=2,rise=0.9,size=0.9,a=0.8,seed=11)
    cl=actor(spr or SCOUT[pose or guard_pose(f)],pos[0],y=pos[1],flip=flip)
    if white: cl['tint']=(255,255,255)
    for hk in hooks: s['fx'].append(('wire',pos[0],pos[1]-5,*hk))
    if gas: s['fx'].append(('snk_gas',gas))
    if blades and spr is None: s['fx'].append(('blades',cl['x'],cl['y'],flip))
    s['actors']=[cl]
    return s

CLIPS = [clip('survey', N_, clip_survey)]
