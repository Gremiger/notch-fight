"""Harry Potter: Claude as Harry (black messy hair, round glasses, the lightning scar, the Gryffindor scarf, the
black school robe, his wand) in the graveyard at Little Hangleton by night: the leaning headstones, the yew,
the statue of Death with its scythe, the mist on the ground. That is the neutral pose every clip starts and
ends on.
- priori: Voldemort rises out of the mist (chalk-white, no nose, red slit eyes, the bone wand). Close-ups of
  each face shouting its spell, EXPELLIARMUS against AVADA KEDAVRA: the red and green beams lock, the bead of
  light slides between them, the golden cage rises. Inside it, PRIORI INCANTATEM, the silver shades of
  Cedric, James and Lily come out of the wand. Harry pushes the bead home, breaks the link, runs for the cup
  and Cedric's body, and the blue Portkey flash swallows him.
- patronus: the mist freezes, dementors glide down, the frost spreads, Harry sinks to a knee, "EXPECTO
  PATRONUM!", the silver stag gallops out and the dementors scatter in a white blast.
- horrocrux: the diary on a headstone glows, young Tom Riddle rises out of its pages; Harry stabs it with the
  basilisk fang, ink gushes and Riddle cracks with light and dissolves.
- basilisco: the Chamber of Secrets: the basilisk rears up, Fawkes drops the Sorting Hat, the sword of
  Gryffindor comes out of it (close-up, rubies glinting), the lunge, the sword up through the roof of its mouth."""
from engine import *

THEME = 'hp'
N_ = 432                                                            # a multiple of 12 and of 48 (the mist)
HX, VX = 40, 146
INK = (10,10,16)
RED, GREEN, GOLD = (255,60,50), (80,255,110), (255,214,90)
ICE = (222,240,255)
SILVER = (205,220,236)

# ---- people, built from a pose --------------------------------------------------------------------------
POSES = {   # (back elbow, back hand, front elbow, front hand, lean, legs), from (C, shoulder row)
 'stand':  ((-1,4),(-1,8),(3,4),(5,6),0,'stand'),
 'walk1':  ((-2,4),(-3,8),(3,4),(4,8),0,'stance'),
 'walk2':  ((-1,4),(0,8),(3,4),(2,8),0,'stand'),
 'cast':   ((-2,4),(-4,6),(6,1),(12,0),1,'stance'),
 'strain': ((-3,4),(-5,5),(6,2),(12,1),-1,'stance'),
 'run1':   ((-4,2),(-7,4),(4,3),(8,1),1,'run1'),
 'run2':   ((-1,3),(1,6),(3,3),(2,6),1,'run2'),
 'reach':  ((-2,4),(-3,7),(6,2),(11,4),1,'lunge'),
 'kneel':  ((-1,4),(1,8),(3,4),(5,6),0,'kneel'),
 'kneelup':((-1,4),(1,8),(5,1),(9,-3),0,'kneel'),
 'cringe': ((-2,3),(-3,6),(4,1),(4,-3),-2,'stance'),
 'lift':   ((-2,4),(-4,5),(3,0),(4,-7),0,'stance'),
 'stab':   ((-1,4),(-2,8),(7,2),(10,0),1,'stance'),
 'crouch': ((-1,4),(2,8),(4,4),(9,10),1,'crouch'),
 'thrust': ((-2,3),(-3,1),(5,0),(9,-6),1,'lunge'),
 'hurt':   ((-3,4),(-6,2),(1,5),(4,7),-2,'reel'),
 'point':  ((-1,4),(-1,8),(6,1),(11,0),0,'stance'),
 'swing':  ((-1,4),(-3,6),(6,0),(9,-3),1,'stance'),
}
WANDV = {'stand':(3,2),'walk1':(3,2),'walk2':(3,2),'cast':(4,0),'strain':(4,-1),'kneel':(3,2),'kneelup':(2,-4),'point':(4,0),
         'reach':(4,0)}

def _robe_h(g, at):                                                 # the school robe, to the knees
    c, hip = at['c'], at['hip']
    for t in range(7):
        w = 4 + t // 3
        for x in range(c - w - 1, c + w): put(g, x + at['sh'](hip), hip + t, 'j' if (x + t) % 4 else 'J')
def _scarf(g, at):                                                  # scarlet and gold, the end hanging down the back
    c, ty, sh = at['c'], at['ty'], at['sh']
    for y in range(ty, ty + 3):
        for x in range(c - 4 + sh(y), c + 4 + sh(y)): put(g, x, y, 'r' if (x + y) % 3 else 'y')
    for t in range(3, 9):
        for x in (c - 5, c - 4): put(g, x + sh(ty + t), ty + t, 'r' if (t + x) % 2 else 'y')
    put(g, c - 5 + sh(ty + 9), ty + 9, 'y')
HFACE = [".hhhhh.",
         "hhhhhhh",
         "hhhsshs",
         "hssszss",
         "GGGsGGG",
         "GKGsGKG",
         "sssssss",
         "sssnsss",
         "ssmmmss"]
def _harry_face(g, at):                                             # hair, scar, round glasses, a shout
    c, hy, o = at['c'], at['hy'], at['sh'](at['hy'])
    for i, row in enumerate(HFACE):
        for j, ch in enumerate(row):
            if ch != '.': put(g, c - 3 + o + j, hy + i, ch)
def _robe_v(g, at):                                                 # sweeping to the ground, tattered at the hem
    c, hip, L = at['c'], at['hip'], at['L']
    for t in range(L):
        w = 4 + (t * 5) // L
        for x in range(c - w, c + w + 1):
            if t == L - 1 and (x + c) % 3 == 0: continue
            put(g, x + at['sh'](hip), hip + t, 'j' if (x + t // 2) % 5 else 'J')
VFACE = [".sssss.",
         "sssssss",
         "sbbsbbs",
         "seesees",
         "sssssss",
         "ssnsnss",
         "ssnnnss",
         ".sssss."]
def _vold_face(g, at):                                              # bald, chalk-white, red slit eyes, no nose
    c, hy, o = at['c'], at['hy'], at['sh'](at['hy'])
    for i, row in enumerate(VFACE):
        for j, ch in enumerate(row):
            if ch != '.': put(g, c - 3 + o + j, hy + i, ch)
RFACE = [".hhhhh.",
         "hhhhhhh",
         "hhhhhss",
         "sssssss",
         "sKsssKs",
         "sssssss",
         "sssnsss",
         "sssmmss",
         ".sssss."]
def _riddle_face(g, at):                                            # neat side-parted hair, pale, a smirk
    c, hy, o = at['c'], at['hy'], at['sh'](at['hy'])
    for i, row in enumerate(RFACE):
        for j, ch in enumerate(row):
            if ch != '.': put(g, c - 3 + o + j, hy + i, ch)
def _tie(g, at):                                                    # the green and silver tie
    c, ty, sh = at['c'], at['ty'], at['sh']
    put(g, c - 1 + sh(ty), ty, 'W'); put(g, c + 1 + sh(ty), ty, 'W')
    for t in range(1, 7): put(g, c + sh(ty + t), ty + t, 'X' if t % 2 else 'D')

_ARM = dict(shoulders=((-3,1),(3,1)), sleeve='j', back_sleeve='J', fore='j', back_fore='J')
HARRY = dict(name='harry', w=30, h=33, c=14, legs=12, torso=9, head=9, torso_cols=(-4,4), arm=_ARM,
             leg=dict(toe=False, bend=False, boot_rows=2), paint={'legs': [_robe_h], 'body': [_scarf], 'face': [_harry_face]})
VOLDEMORT = dict(name='voldemort', w=34, h=40, c=16, legs=15, torso=10, head=8, torso_cols=(-4,4), arm=_ARM, eye='e',
                 leg=dict(color='j', boot='j', toe=False), paint={'legs': [_robe_v], 'face': [_vold_face]})
RIDDLE = dict(name='riddle', w=28, h=31, c=13, legs=11, torso=8, head=9, torso_cols=(-4,4), arm=_ARM,
              leg=dict(toe=False, bend=False), paint={'body': [_tie], 'face': [_riddle_face]})

HPAL = {'s':(238,202,172),'K':(30,60,40),'G':(92,94,116),'z':(210,50,50),'h':(20,16,20),'j':(36,34,46),'J':(24,22,32),
        'r':(176,28,36),'y':(226,150,64),'p':(36,36,46),'k':(22,18,20),'n':(206,150,124),'m':(130,40,44)}
VPAL = {'s':(226,232,224),'e':(235,30,30),'n':(120,130,120),'b':(110,120,110),'j':(14,12,18),'J':(32,28,38),'p':(14,12,18),'k':(10,10,12)}
RPAL = {'s':(214,226,214),'K':(20,20,26),'h':(34,38,46),'j':(52,70,66),'J':(38,52,50),'p':(48,64,60),'k':(24,30,30),
        'n':(176,190,176),'m':(150,90,100),'W':(230,236,230),'X':(40,150,95),'D':(190,196,206)}

def build(who, pose):
    return figure({'harry': HARRY, 'voldemort': VOLDEMORT, 'riddle': RIDDLE}[who], POSES[pose])

def hand(spec, pose, x, flip=False):
    """Where the front hand is on screen (a person standing on the ground at x)."""
    return figure_point(spec, POSES[pose], 'hand', x, GROUND, flip)

def wand_tip(x, feet, pose, flip=False, spec=None):
    hx, hy = figure_point(spec or HARRY, POSES[pose], 'hand', x, feet, flip)
    dx, dy = WANDV.get(pose, (4, 0)); return hx + (-dx if flip else dx), hy + dy

def put_wand(s, spec, pose, x, flip=False, col=(130,90,56)):
    """The wand in the front hand; returns its tip."""
    hx, hy = hand(spec, pose, x, flip); tx, ty = wand_tip(x, GROUND, pose, flip, spec)
    s['fx'].append(('hp_wand', hx, hy, tx, ty, col)); return tx, ty

def glow(im, x, y, r, c, a=0.5):
    """A soft glow of radius r (blurred, only the box around it)."""
    r = int(r); x, y = int(x), int(y); b = max(1, r // 3); pad = 3 * b + 2; n = 2 * (r + pad)
    m = Image.new('L', (n, n), 0); ImageDraw.Draw(m).ellipse([pad, pad, n - pad, n - pad], fill=int(255 * min(1, a)))
    m = m.filter(ImageFilter.GaussianBlur(b))
    im.paste(c, (x - n // 2, y - n // 2, x - n // 2 + n, y - n // 2 + n), m)

def comp(im, layer, a=1.0, tint=None, k=0.0):
    """Lay a RGBA layer over im at opacity a (tinted towards a colour by k)."""
    rgb = layer.convert('RGB'); al = layer.getchannel('A')
    if tint and k: rgb = Image.blend(rgb, Image.new('RGB', rgb.size, tint), k)
    if a < 1: al = al.point(lambda v: int(v * a))
    im.paste(rgb, (0, 0), al)

# ---- the graveyard --------------------------------------------------------------------------------------
GRAVES = ((10,10,-1),(60,8,1),(118,12,0),(172,9,-1),(132,7,1),(74,6,0))   # x, height, lean
def _graveyard(d):
    for y in range(H): k=y/H; d.line([0,y,W,y],fill=(int(lerp(10,26,k)),int(lerp(14,30,k)),int(lerp(30,38,k))))
    rr=random.Random(39)
    for _ in range(40): d.point((rr.randint(0,W-1),rr.randint(0,24)),fill=(180,190,220))
    d.ellipse([150,3,164,17],fill=(220,224,210)); d.ellipse([154,3,168,15],fill=(14,18,34))   # a thin moon
    d.polygon([(0,40),(20,30),(46,36),(70,26),(100,34),(130,28),(160,36),(185,30),(185,46),(0,46)],fill=(22,26,30))   # the hill
    x=92                                                             # the statue of Death, with its scythe
    d.polygon([(x-6,GROUND-2),(x-4,22),(x,16),(x+4,22),(x+6,GROUND-2)],fill=(70,74,80)); d.ellipse([x-3,14,x+3,22],fill=(60,64,70))
    d.line([x+4,24,x+10,6],fill=(80,84,90)); d.arc([x+2,2,x+20,14],180,300,fill=(110,114,120),width=2)
    d.rectangle([x-9,GROUND-3,x+9,GROUND],fill=(80,84,88))
    d.line([20,GROUND,24,20],fill=(30,26,24),width=3)                 # the old yew
    for k in range(8): a=k*0.8; d.line([24,22,24+math.cos(a)*12,20+math.sin(a)*6],fill=(30,40,30),width=2)
    for x,h,tilt in GRAVES:                                          # leaning headstones
        d.polygon([(x-3,GROUND),(x-3+tilt,GROUND-h),(x+3+tilt,GROUND-h),(x+3,GROUND)],fill=(96,100,104),outline=(56,58,62))
        d.pieslice([x-3+tilt,GROUND-h-3,x+3+tilt,GROUND-h+3],180,360,fill=(96,100,104))
    d.rectangle([0,GROUND,W,H],fill=(26,32,26))
    for _ in range(50): d.point((rr.randint(0,W-1),rr.randint(GROUND,H-1)),fill=(40,50,36))
register_bg(THEME, lambda v: (v+20,v+26,v+20), decor=_graveyard)

def _chamber(d):
    """The Chamber of Secrets: a long dark hall, snake pillars, Slytherin's stone face at the back, green gloom."""
    for y in range(H): k=y/H; d.line([0,y,W,y],fill=(int(lerp(4,10,k)),int(lerp(12,30,k)),int(lerp(10,24,k))))
    d.rectangle([44,0,141,44],fill=(16,34,28))                          # the back wall, in blocks
    for y in range(0,44,7):
        d.line([44,y,141,y],fill=(10,24,20))
        for x in range(44+(y//7%2)*6,141,12): d.line([x,y,x,y+7],fill=(10,24,20))
    cx=92                                                            # the giant face of Slytherin
    d.polygon([(cx-18,0),(cx+18,0),(cx+17,18),(cx+11,34),(cx+4,46),(cx-4,46),(cx-11,34),(cx-17,18)],fill=(52,80,66))
    d.polygon([(cx-18,0),(cx-6,0),(cx-4,16),(cx-11,34),(cx-17,18)],fill=(40,64,52))
    d.rectangle([cx-17,0,cx+17,4],fill=(36,58,48))                      # the brow of his headdress
    for sx in (-9,9):
        d.polygon([(cx+sx-5,12),(cx+sx+5,12),(cx+sx+3,17),(cx+sx-3,17)],fill=(6,14,12))   # eye sockets
        d.rectangle([cx+sx-1,13,cx+sx+1,15],fill=(70,200,110))
    d.polygon([(cx-2,14),(cx+2,14),(cx+3,26),(cx-3,26)],fill=(40,64,52))   # the long nose
    d.polygon([(cx-8,31),(cx+8,31),(cx+6,40),(cx-6,40)],fill=(3,8,7))      # the open mouth, the way in
    for x in range(cx-6,cx+7,3): d.line([x,31,x,34],fill=(150,180,160))
    for k in range(-4,5): d.line([cx+k*2,40,cx+k*2+(k//2),50],fill=(46,72,60))   # the beard
    for sx,half,w in ((6,13,16),(40,7,7),(57,4,4)):                  # pillars carved with snakes, both sides
        for side in (0,1):
            x0=sx if side==0 else W-sx-w
            d.rectangle([x0,0,x0+w,46],fill=(26,50,42)); d.rectangle([x0,0,x0+w//4,46],fill=(36,66,54))
            d.rectangle([x0+w-w//5,0,x0+w,46],fill=(14,30,26))
            for y in range(0,46):                                      # the serpent winding round it
                xx=x0+w/2+math.sin(y*0.45+sx)*(w/2-1)
                d.point((int(xx),y),fill=(88,140,108)); d.point((int(xx)+(1 if w>6 else 0),y),fill=(60,104,82))
            d.rectangle([x0-1,42,x0+w+1,46],fill=(34,62,50))
    d.rectangle([0,45,W,H],fill=(8,24,22))                              # the flooded floor
    for y in range(46,H,2): d.line([0,y,W,y],fill=(10,30+(y%4)*3,26))
register_bg('hp_chamber', lambda v:(v//2,v+8,v//2+4), decor=_chamber)

@fx('hp_mist')
def _fx_mist(d,im,e,f):
    """Mist along the ground, drifting (a loop every 48 frames); thick: how much; mf: the frame it drifts on."""
    thick=e[1]; mf=e[2] if len(e)>2 else f; m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for i in range(10):
        x=(i*24+(mf%48)*24/48)%(W+40)-20; y=GROUND-2+(i%3)
        md.ellipse([x-20,y-4-thick*6,x+20,y+5],fill=int(70+60*thick))
    im.paste((150,160,170),(0,0),m.filter(ImageFilter.GaussianBlur(3)))

@fx('hp_wand')
def _fx_wand(d,im,e,f):
    _,x0,y0,x1,y1,c=e; d.line([x0,y0,x1,y1],fill=c); d.point((x1,y1),fill=(255,250,220))

@fx('hp_beam')
def _fx_beam(d,im,e,f):
    """A spell's beam from (x0,y0) to (x1,y1), wavering, with its glow."""
    _,x0,y0,x1,y1,c,w=e
    g=Image.new('L',(W,H),0); gd=ImageDraw.Draw(g)
    n=12; pts=[(lerp(x0,x1,i/n),lerp(y0,y1,i/n)+(math.sin(f*0.9+i*1.3)*1.2 if 0<i<n else 0)) for i in range(n+1)]
    gd.line(pts,fill=160,width=w+4); im.paste(c,(0,0),g.filter(ImageFilter.GaussianBlur(2)))
    d=ImageDraw.Draw(im); d.line(pts,fill=c,width=w); d.line(pts,fill=(255,255,255),width=1)

@fx('hp_bead')
def _fx_bead(d,im,e,f):
    """Where the two meet: the bead of light, the sparks."""
    _,x,y=e; r=3+(f%4)//2
    glow(im,x,y,r+6,GOLD,0.8)
    d=ImageDraw.Draw(im); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,250,220))
    rr=random.Random(f)
    for _ in range(5): a=rr.uniform(0,2*math.pi); L=rr.uniform(3,8); d.line([x,y,x+math.cos(a)*L,y+math.sin(a)*L],fill=GOLD)

@fx('hp_cage')
def _fx_cage(d,im,e,f):
    """The golden dome over the two of them (a: how far it has risen)."""
    _,a=e
    if a<=0: return
    cx=(HX+VX)/2; rx=(VX-HX)/2+14; top=GROUND-48*a
    for k in range(9):
        t=k/8; ph=math.sin(f*0.3+k)*2
        d.arc([cx-rx*abs(1-2*t)-1,top+ph,cx+rx*abs(1-2*t)+1,GROUND*2-top],180,360,fill=(220,180,70))
    d.arc([cx-rx,top,cx+rx,GROUND*2-top],180,360,fill=GOLD,width=2)

@fx('hp_cup')
def _fx_cup(d,im,e,f):
    """The Triwizard Cup, the Portkey, glinting on the grass (lift: how high it has been picked up)."""
    _,x,glow_,lift=e; y=GROUND-lift
    c,o=(150,200,230),(90,130,160)
    d.polygon([(x-4,y-9),(x+4,y-9),(x+2,y-4),(x-2,y-4)],fill=c,outline=o)
    d.rectangle([x-1,y-4,x+1,y-2],fill=c); d.rectangle([x-3,y-2,x+3,y],fill=c,outline=o)
    for s in (-1,1): d.arc([x+s*4-3,y-9,x+s*4+3,y-4],90 if s>0 else 270,270 if s>0 else 90,fill=c)
    if glow_>0:
        glow(im,x,y-5,10,(120,190,255),0.6*glow_)
        if (f//2)%2: ImageDraw.Draw(im).ellipse([x-8,y-14,x+8,y+2],outline=(200,240,255))

@fx('hp_cedric')
def _fx_cedric(d,im,e,f):
    """Cedric's body lying on the grass, feet to the right (a: how much of him the mist shows; lift: raised)."""
    _,x,a,lift=e
    if a<=0: return
    y=GROUND-1-lift; L=Image.new('RGBA',(W,H),(0,0,0,0)); ld=ImageDraw.Draw(L)
    ld.polygon([(x-2,y-6),(x+16,y-5),(x+22,y-4),(x+22,y),(x-2,y)],fill=(34,32,40))        # the robe
    ld.rectangle([x+4,y-6,x+8,y-4],fill=(226,176,40)); ld.rectangle([x+8,y-6,x+10,y-4],fill=(30,26,24))   # Hufflepuff scarf
    ld.ellipse([x-8,y-7,x-1,y],fill=(224,186,160)); ld.rectangle([x-9,y-7,x-4,y-5],fill=(70,50,36))        # the head, the hair
    ld.rectangle([x+22,y-3,x+26,y],fill=(20,18,22))                                           # the boots
    ld.line([x+8,y-1,x+14,y-3],fill=(224,186,160))                                            # a hand
    comp(im,L,a)

@fx('hp_text')
def _fx_text(d,im,e,f):
    _,txt,cx,y,c=e; big_text(im,txt,y,c,scale=1,cx=cx,shadow=INK)

# ---- big faces for the close-ups ------------------------------------------------------------------------
def _P(cx,y0,sc): return lambda *pts: [(cx+a*sc,y0+b*sc) for a,b in pts]

def harry_face(im,cx,y0,sc=1.0,mouth=1.0,eye=(0,0)):
    """Harry from the front, at close range: hair, scar, round glasses, a furrowed brow, the scarf, a shout."""
    d=ImageDraw.Draw(im); P=_P(cx,y0,sc); w=max(1,int(round(2*sc)))
    d.polygon(P((-40,70),(-32,46),(-14,42),(14,42),(32,46),(40,70)),fill=(26,24,34))
    d.rectangle([cx-5*sc,y0+34*sc,cx+5*sc,y0+44*sc],fill=(206,160,132))
    d.polygon(P((-17,37),(17,37),(20,50),(-20,50)),fill=(176,28,36))                  # the scarf
    for k in range(-4,5): d.line(P((-18+k*5,37),(-15+k*5,50)),fill=(226,150,64) if k%2 else (150,22,30),width=w)
    d.ellipse([cx-15*sc,y0+2*sc,cx+15*sc,y0+39*sc],fill=(240,206,176),outline=(150,100,80))
    for s_ in (-1,1): d.ellipse([cx+s_*15*sc-2*sc,y0+17*sc,cx+s_*15*sc+2*sc,y0+25*sc],fill=(226,184,154))   # ears
    d.polygon(P((-16,22),(-17,8),(-11,0),(-8,-5),(-3,-1),(2,-6),(6,-1),(12,-3),(14,2),(17,10),(16,22),(12,13),(7,10),(2,12),(-4,9),(-10,13)),fill=(18,14,16))
    d.line(P((3,10),(1,13),(5,13),(2,18)),fill=(210,40,44),width=w)                    # the scar
    for s_ in (-1,1):
        ex=s_*7; d.ellipse([cx+(ex-6.5)*sc,y0+(23-6.5)*sc,cx+(ex+6.5)*sc,y0+(23+6.5)*sc],fill=(212,226,236),outline=(20,20,26),width=w)
        d.ellipse([cx+(ex-3)*sc,y0+(23-2.5)*sc,cx+(ex+3)*sc,y0+(23+2.5)*sc],fill=(250,250,250))
        d.ellipse([cx+(ex+eye[0]-1.6)*sc,y0+(23+eye[1]-1.6)*sc,cx+(ex+eye[0]+1.6)*sc,y0+(23+eye[1]+1.6)*sc],fill=(50,120,70))
    d.line(P((-1,22),(1,22)),fill=(20,20,26),width=w)
    d.line(P((-14,15),(-4,19)),fill=(18,14,16),width=w); d.line(P((4,19),(14,15)),fill=(18,14,16),width=w)   # the brow
    d.line(P((0,25),(-1,30),(2,30)),fill=(190,140,115),width=1)
    ry=(1.5+5*mouth)*sc; my=y0+35*sc
    d.ellipse([cx-6*sc,my-ry/2,cx+6*sc,my+ry],fill=(96,20,28))
    d.line([cx-5*sc,my-ry/2+1,cx+5*sc,my-ry/2+1],fill=(250,250,245),width=max(1,int(sc)))
    if mouth>0.4: d.ellipse([cx-3*sc,my+ry*0.3,cx+3*sc,my+ry],fill=(200,90,100))

def voldemort_face(im,cx,y0,sc=1.0,mouth=1.0):
    """Voldemort from the front: bald, chalk-white, red slit eyes, two slits for a nose, the black collar."""
    d=ImageDraw.Draw(im); P=_P(cx,y0,sc); w=max(1,int(round(2*sc)))
    d.polygon(P((-42,70),(-34,44),(-16,34),(16,34),(34,44),(42,70)),fill=(12,10,16))
    d.polygon(P((-20,32),(20,32),(26,50),(-26,50)),fill=(26,22,32))
    d.rectangle([cx-6*sc,y0+30*sc,cx+6*sc,y0+42*sc],fill=(196,204,194))
    d.ellipse([cx-14*sc,y0-4*sc,cx+14*sc,y0+40*sc],fill=(226,232,224),outline=(110,122,112))
    d.ellipse([cx+2*sc,y0-1*sc,cx+13*sc,y0+36*sc],fill=(206,214,206))                  # shade on one side
    for s_ in (-1,1):
        ex=s_*7; glow(im,cx+ex*sc,y0+18*sc,int(7*sc),(255,40,40),0.5); d=ImageDraw.Draw(im)
        d.polygon(P((ex-5,16.5+(-1 if s_<0 else 1)),(ex+5,16.5+(1 if s_<0 else -1)),(ex+4,20),(ex-4,20)),fill=(240,24,24),outline=(70,10,16))
        d.line(P((ex,16),(ex,20)),fill=(10,0,0),width=1)
        d.line(P((ex-6,12+(2 if s_<0 else -2)),(ex+6,12+(-2 if s_<0 else 2))),fill=(110,120,110),width=w)   # the cruel brow
    d.line(P((-3,26),(-2,31)),fill=(80,92,80),width=w); d.line(P((3,26),(2,31)),fill=(80,92,80),width=w)   # nostril slits
    ry=(1+5*mouth)*sc; my=y0+34*sc
    d.polygon([(cx-7*sc,my),(cx+7*sc,my),(cx+5*sc,my+ry),(cx-5*sc,my+ry)],fill=(60,10,16))
    d.line([cx-7*sc,my,cx+7*sc,my],fill=(150,130,130),width=w)
    if mouth>0.4: d.line([cx-4*sc,my+1,cx+4*sc,my+1],fill=(190,190,170),width=1)

def riddle_face(im,cx,y0,sc=1.0,smirk=1.0):
    """Young Tom Riddle from the front, smug: neat side-parted hair, a raised brow, a crooked smile, the tie."""
    d=ImageDraw.Draw(im); P=_P(cx,y0,sc); w=max(1,int(round(2*sc)))
    d.polygon(P((-40,70),(-32,46),(-12,40),(12,40),(32,46),(40,70)),fill=(24,24,32))
    d.polygon(P((-12,40),(0,48),(12,40),(8,38),(-8,38)),fill=(232,238,232))            # the white collar
    d.polygon(P((-3,44),(3,44),(5,70),(-5,70)),fill=(40,150,95))                       # the tie
    for k in range(5): d.line(P((-4,46+k*5),(4,50+k*5)),fill=(190,196,206),width=1)
    d.rectangle([cx-5*sc,y0+32*sc,cx+5*sc,y0+42*sc],fill=(200,212,200))
    d.ellipse([cx-12*sc,y0,cx+12*sc,y0+38*sc],fill=(222,232,222),outline=(120,140,120))
    d.polygon(P((-13,16),(-13,4),(-6,-2),(5,-2),(13,5),(13,15),(10,8),(2,5),(-4,6),(-5,12)),fill=(22,20,28))   # the hair
    d.line(P((-4,-1),(-5,10)),fill=(70,66,80),width=1)                                  # the parting
    for s_,dy in ((-1,0),(1,-2)):
        ex=s_*6; d.ellipse([cx+(ex-3)*sc,y0+(18+dy)*sc,cx+(ex+3)*sc,y0+(21+dy)*sc],fill=(250,250,250))
        d.ellipse([cx+(ex-1.5)*sc,y0+(18.5+dy)*sc,cx+(ex+1.5)*sc,y0+(21+dy)*sc],fill=(20,20,26))
        d.line(P((ex-4,15+dy+(1 if s_<0 else -2)),(ex+4,15+dy+(-1 if s_<0 else 0))),fill=(22,20,28),width=w)   # one brow up
    d.line(P((0,22),(-1,28),(2,28)),fill=(172,184,172),width=1)
    d.line(P((-5,32),(1,33.5),(6,31-2*smirk)),fill=(120,70,80),width=w)                 # the smirk
    d.point((cx+7*sc,y0+(30-2*smirk)*sc),fill=(120,70,80))

def shade_fig(L,who,cx,base,h):
    """A silver shade (on an RGBA layer): Cedric, James or Lily, h tall, feet-wisp at base."""
    d=ImageDraw.Draw(L); s=h/44; top=base-h; hr=5*s; hy=top+hr+1*s
    body=(206,220,236,255); line=(100,124,150,255); hair=(120,140,166,255)
    if who=='lily':
        d.polygon([(cx-hr-2*s,hy-1*s),(cx+hr+2*s,hy-1*s),(cx+hr+4*s,top+26*s),(cx-hr-4*s,top+26*s)],fill=hair)   # the long hair
    d.polygon([(cx-7*s,top+11*s),(cx+7*s,top+11*s),(cx+11*s,base-3*s),(cx+5*s,base),(cx,base-2*s),(cx-5*s,base),(cx-11*s,base-3*s)],fill=body)
    d.line([cx-7*s,top+13*s,cx-10*s,top+27*s],fill=body,width=max(1,int(3*s))); d.line([cx+7*s,top+13*s,cx+10*s,top+27*s],fill=body,width=max(1,int(3*s)))
    d.rectangle([cx-2*s,top+9*s,cx+2*s,top+12*s],fill=body)
    d.ellipse([cx-hr,hy-hr,cx+hr,hy+hr],fill=body)
    if who=='cedric':
        d.pieslice([cx-hr-1,hy-hr-1*s,cx+hr+1,hy+hr],180,360,fill=hair)                # short neat hair
        d.rectangle([cx-7*s,top+11*s,cx+7*s,top+14*s],fill=(240,214,80,255)); d.rectangle([cx-3*s,top+11*s,cx-1*s,top+14*s],fill=(40,36,30,255))
    if who=='james':
        for k in range(-2,3): d.line([cx+k*2*s,hy-hr+1*s,cx+k*2.6*s,hy-hr-4*s],fill=hair,width=max(1,int(2*s)))   # messy hair
        d.pieslice([cx-hr-1,hy-hr-1*s,cx+hr+1,hy+hr],180,360,fill=hair)
        for ex in (-2.4,2.4): d.ellipse([cx+(ex-1.8)*s,hy-1.5*s,cx+(ex+1.8)*s,hy+1.8*s],outline=line,width=1)   # round glasses
    if who=='lily': d.pieslice([cx-hr-1,hy-hr-1*s,cx+hr+1,hy+hr*0.4],180,360,fill=hair)
    for ex in (-2,2): d.point((int(cx+ex*s),int(hy)),fill=line)

def shade_layer(shades):
    """[(who, cx, base, h, alpha)] as one RGBA layer, and its glow."""
    L=Image.new('RGBA',(W,H),(0,0,0,0))
    for who,cx,base,h,a in shades:
        one=Image.new('RGBA',(W,H),(0,0,0,0)); shade_fig(one,who,cx,base,h)
        one.putalpha(one.getchannel('A').point(lambda v: int(v*0.62*a))); L=Image.alpha_composite(L,one)
    return L

# ---- the neutral pose, and what every clip shares ---------------------------------------------------------
def neutral(f, thick=0.3, mf=None):
    """The graveyard, Harry standing with his wand: the frame every clip starts and ends on."""
    s=scene(f,THEME); s['actors']=[actor(build('harry','stand'),HX,pal=HPAL)]
    put_wand(s,HARRY,'stand',HX)
    s['fx'].append(('hp_mist',thick,f if mf is None else mf)); return s

def finish(s,f,thick=0.3,mf=None):
    """The mist goes over everything that stands on the ground."""
    s['fx'].append(('hp_mist',thick,f if mf is None else mf)); return s

def flash_to(s,f,c,a):
    """The frame of s washed towards c by a (a Portkey, a blast); a>0 turns it into a finished image."""
    s['image']=fade_to(render(s,f),c,max(0,min(1,a))); return s

# ---- close-ups --------------------------------------------------------------------------------------------
def closeup_spell(t,f,who):
    """A face shouting its spell, the beam leaving the wand: Harry (red) or Voldemort (green)."""
    harry=who=='harry'; col=RED if harry else GREEN; txt='EXPELLIARMUS!' if harry else 'AVADA KEDAVRA!'
    def draw(im,d,t,f):
        glow(im,92,40,60,col,0.35)
        mouth=0.5+0.5*abs(math.sin(f*0.9))
        if harry: harry_face(im,56,16,0.95,mouth,(1,0))
        else: voldemort_face(im,128,14,1.0,mouth)
        d=ImageDraw.Draw(im)
        wx=100 if harry else 84; tx=W+2 if harry else -2; sgn=1 if harry else -1
        d.line([wx-sgn*10,58,wx,46],fill=(120,80,50) if harry else (236,232,214),width=2)   # the arm, the wand
        d.line([wx,46,wx+sgn*12,40],fill=(120,80,50) if harry else (236,232,214),width=1)
        bx=wx+sgn*12; by=40
        glow(im,bx,by,12,col,0.9); d=ImageDraw.Draw(im); d.ellipse([bx-3,by-3,bx+3,by+3],fill=(255,255,255))
        L=int(t*70)+12
        pts=[(bx+sgn*i*5,by-(i*0.6)+math.sin(f+i)*1.2) for i in range(L//5+1)]
        if len(pts)>1 and 0.35<=t: d.line(pts,fill=col,width=3); d.line(pts,fill=(255,255,255),width=1)
        rr=random.Random(f)
        for _ in range(8): a=rr.uniform(0,2*math.pi); r_=rr.uniform(4,12); d.line([bx,by,bx+math.cos(a)*r_,by+math.sin(a)*r_*0.7],fill=col)
    return closeup(t,f,bg=(18,8,10) if harry else (6,16,10),draw=draw,txt=txt,box=(2,2,W-2,24),text_from=0,
                   color=col,outline=INK,max_scale=3,zoom=col)

def closeup_priori(t,f):
    """Inside the golden cage: the threads of light humming, the bead between the wands, and the shades of
    the dead coming out of Voldemort's wand: Cedric, then James and Lily, silver and see-through."""
    im=Image.new('RGB',(W,H),(14,12,6)); d=ImageDraw.Draw(im)
    for k in range(14):                                              # the cage's threads, arching over
        a=k/13; ph=math.sin(f*0.25+k)*3
        d.arc([-20+a*40,-30+ph,W+20-a*40,H+70],180,360,fill=(int(150+100*a),int(110+80*a),40))
    glow(im,92,50,70,GOLD,0.25)
    d=ImageDraw.Draw(im)
    d.line([0,44,W,44],fill=GOLD,width=3); d.line([0,44,W,44],fill=(255,255,240))   # the link between them
    d.ellipse([86,39,98,49],fill=(255,250,220))
    sh=[]
    for who,fx_,start in (('cedric',52,0.08),('james',90,0.32),('lily',128,0.56)):
        a=max(0,min(1,(t-start)/0.28))
        if a<=0: continue
        x=lerp(176,fx_,ez(0,1,a)); h=lerp(16,46,ez(0,1,a))
        sh.append((who,x,lerp(46,63,ez(0,1,a)),h,min(1,a*2))); glow(im,x,63-h*0.5,int(h*0.7),(150,190,230),0.28*a)
    comp(im,shade_layer(sh))
    d=ImageDraw.Draw(im)
    d.rectangle([168,40,W,48],fill=(236,232,214)); d.rectangle([0,40,18,48],fill=(120,80,50))   # the two wands
    d.rectangle([168,41,W,42],fill=(255,255,245)); d.rectangle([0,41,18,42],fill=(160,110,70))
    for who,fx_ in (('CEDRIC',52),('JAMES',90),('LILY',128)):
        if t>0.88: text(d,who,fx_-len(who)*2+1,58,(226,236,248))
    big_text(im,"PRIORI INCANTATEM",2,GOLD,scale=2,shadow=INK)
    if t<0.05: zoom_lines(d,GOLD)
    return im

# ---- priori -----------------------------------------------------------------------------------------------
def clip_priori(f):
    if 56<=f<76: s=scene(f,THEME); s['image']=closeup_spell((f-56)/20,f,'harry'); return s
    if 76<=f<96: s=scene(f,THEME); s['image']=closeup_spell((f-76)/20,f,'volde'); return s
    if 212<=f<282: s=scene(f,THEME); s['image']=closeup_priori((f-212)/70,f); return s
    s=scene(f,THEME)
    hpose,vpose,vvis,valpha='stand','stand',False,1.0
    hx=HX; thick=0.3; cage=0.0; hvis=True; vrise=0; body=0.0; cuplift=0; cupglow=0; gone=False
    if 14<=f<372:                                                    # Voldemort rises out of the mist, with Cedric and the cup
        vvis=True; valpha=min(1,(f-14)/30) if f<44 else 1.0; vrise=int(8*(1-min(1,(f-14)/30))) if f<44 else 0
        body=min(1,(f-14)/30)
    if 14<=f<50: thick=0.3+0.7*math.sin(min(1,(f-14)/36)*math.pi)
    tips=None
    if 96<=f<336:                                                    # the duel: the two spells, the lock, the bead going back and forth
        hpose='cast' if f<140 else 'strain'; vpose='cast'
        x0,y0=wand_tip(HX,GROUND,hpose); x1,y1=wand_tip(VX,GROUND,vpose,True,VOLDEMORT)
        if f<108: t=(f-96)/12; mx=lerp(x0,(x0+x1)/2,t); my=lerp(y0,(y0+y1)/2,t); mx2=lerp(x1,(x0+x1)/2,t)
        else:
            mid=(x0+x1)/2+[-0,-8,6,-4,10,18,26][min(6,(f-108)//18)]+3*math.sin(f*0.4)
            if f>=294: mid=lerp(mid,x1-4,(f-294)/24)                 # Harry pushes it home
            mx=mx2=mid; my=(y0+y1)/2
        s['fx'].append(('hp_beam',x0,y0,mx,my,RED,2)); s['fx'].append(('hp_beam',x1,y1,mx2,my,GREEN,2))
        if f>=108: s['fx'].append(('hp_bead',mx,my)); s['shake']=rshake(1) if f%9==0 else (0,0)
        if f<100: s['flash']=1-(f-96)/4; s['fc']=((x0+x1)/2,y0); s['flashc']=(255,255,235)
    if 152<=f<336: cage=min(1,(f-152)/40)
    if 316<=f<336: cage=max(0,cage-(f-316)/20)
    if 336<=f<344: s['flash']=1-(f-336)/8; s['fc']=(VX-10,GROUND-14); vpose='stand'   # the link breaks
    if 336<=f<372:                                                   # he runs for the cup and Cedric, and takes both
        t=(f-336)/26; hx=lerp(HX,90,ez(0,1,t)); hpose='run1' if (f//4)%2 else 'run2'
        if f>=362: hpose='reach'; cupglow=min(1,(f-362)/6)
        if f>=366: cuplift=min(5,(f-366)); body=1.0
    lift=(max(0,min(3,(f-366)//2)) if f>=366 else 0)
    if 372<=f<384: hvis=hvis and f<380
    if 384<=f<404:                                                   # the Portkey has taken him; the graveyard comes back
        s=neutral(f); return flash_to(s,f,(210,235,255),1-(f-384)/20)
    if f>=404: return neutral(f)
    s['under'].append(('hp_cage',cage))
    if body>0: s['under'].append(('hp_cedric',112,body,lift if hvis else 0)); s['under'].append(('hp_cup',102,cupglow,cuplift if hvis else 0))
    if f>=380: s['under']=[e for e in s['under'] if e[0] not in ('hp_cedric','hp_cup')]
    acts=[]
    if vvis: acts.append(actor(build('voldemort',vpose),VX,y=GROUND+vrise,flip=True,pal=VPAL,alpha=valpha))
    if hvis: acts.append(actor(build('harry',hpose),hx,pal=HPAL))
    s['actors']=acts
    if hvis and hpose in ('stand','cast','strain','reach'): put_wand(s,HARRY,hpose,hx)
    if vvis and valpha>0.5: put_wand(s,VOLDEMORT,vpose,VX,True,(236,232,214))
    if 372<=f<384: s['fx'].append(('hp_portkey',hx if f<380 else 96,GROUND-14,(f-372)/12))
    finish(s,f,thick)
    if 372<=f<384: flash_to(s,f,(210,235,255),(f-372)/12)
    return s

@fx('hp_portkey')
def _fx_portkey(d,im,e,f):
    """The Portkey's blue pull: streaks swirling round a point."""
    _,x,y,t=e; rr=random.Random(f)
    for k in range(14):
        a=k*0.45+f*0.7; r0=24*(1-t)+4; r1=r0+8+rr.random()*6
        d.line([x+math.cos(a)*r0,y+math.sin(a)*r0*0.7,x+math.cos(a+0.5)*r1,y+math.sin(a+0.5)*r1*0.7],fill=(150,210,255))
    glow(im,x,y,20,(130,200,255),0.7)


# ---- patronus ---------------------------------------------------------------------------------------------
DEM = ((78,10),(104,17),(130,8),(158,15))                            # the dementors' x and the top of the hood

def dementor(d,x,y,h,f,k=0):
    """A dementor: a hood with darkness inside, a cloak that tapers into tatters, one grey skeletal hand."""
    sw=math.sin(2*math.pi*loop.phase(f,24)+k*1.7); rim=(58,54,88); cl=(10,8,14)
    d.polygon([(x-6,y+9),(x+6,y+9),(x+9+sw*2,y+h*0.6)]+[(x+11+sw*2-i*3.7,y+h-(i%2)*6+math.sin(f*0.3+i)*1.5) for i in range(7)]+[(x-9-sw*2,y+h*0.6)],fill=cl,outline=rim)
    for i in range(8):
        sx=x-8+i*2.3; d.line([sx,y+h*0.5,sx-2+i*0.5+sw*(1+i*0.15)*1.6,y+h+2+(i%3)*2],fill=cl)
    d.ellipse([x-6,y,x+6,y+13],fill=cl,outline=rim); d.ellipse([x-4,y+3,x+4,y+11],fill=(1,1,3))
    hx_,hy_=x+15+sw,y+20
    d.line([x+6,y+13,hx_,hy_],fill=(26,22,36),width=2)
    for i in range(3): d.line([hx_,hy_,hx_+1+i,hy_+4],fill=(150,150,158))
    d.point((hx_,hy_),fill=(180,180,188))

@fx('hp_dementor')
def _fx_dementor(d,im,e,f):
    _,x,y,h,k=e; dementor(d,x,y,h,f,k)

@fx('hp_dark')
def _fx_dark(d,im,e,f):
    """The sky darkening: a deep blue laid over everything (a: 0..1)."""
    im.paste((6,10,26),(0,0),Image.new('L',(W,H),int(150*e[1])))

@fx('hp_glow')
def _fx_glow(d,im,e,f):
    _,x,y,r,c,a=e; glow(im,x,y,r,c,a)

@fx('hp_frost')
def _fx_frost(d,im,e,f):
    """White frost spreading over the grass and the headstones from the right (a: 0..1)."""
    a=e[1]
    if a<=0: return
    front=W+10-a*(W+30); m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    if front<W: md.rectangle([max(0,front),GROUND-2,W,H],fill=90)
    for x,h,t in GRAVES:
        if x>front: md.polygon([(x-3,GROUND),(x-3+t,GROUND-h),(x+3+t,GROUND-h),(x+3,GROUND)],fill=170)
    im.paste(ICE,(0,0),m); rr=random.Random(5)
    for i in range(120):
        x=rr.randint(0,W-1); y=rr.randint(GROUND-1,H-2); hg=rr.randint(2,5)
        if x>front:
            hh=int(hg*min(1,(x-front)/25)); d.line([x,y,x,y-hh],fill=(240,249,255))
            if hh>2: d.point((x+1,y-hh+1),fill=(190,222,247))
    for x,h,t in GRAVES:
        if x>front:
            for k in range(6): xx=x-3+k*1.4+t; d.line([xx,GROUND-h,xx+(k-2.5)*0.7,GROUND-h-2-(k%3)],fill=(240,250,255))

@fx('hp_stag')
def _fx_stag(d,im,e,f):
    """The silver-white stag, galloping (ph: the stride), glowing, with big antlers; sc its size."""
    _,x,y,sc,ph,a=e
    L=Image.new('RGBA',(W,H),(0,0,0,0)); ld=ImageDraw.Draw(L)
    body=(236,247,255,255); mid=(176,212,244,255); w=max(1,int(2*sc))
    def P(*pts): return [(x+px*sc,y+py*sc) for px,py in pts]
    def box(x0,y0,x1,y1): return [x+x0*sc,y+y0*sc,x+x1*sc,y+y1*sc]
    for k,(lx,off) in enumerate(((-12,0),(-8,math.pi),(9,0.6),(13,math.pi+0.6))):   # hind legs, front legs
        sw=math.sin(ph+off); hip=(lx,-14); foot=(lx+sw*9,-1-max(0,math.cos(ph+off))*5)
        knee=((hip[0]+foot[0])/2+(-2 if k<2 else 2),-8); ld.line(P(hip,knee,foot),fill=mid if k%2 else body,width=w)
    ld.ellipse(box(-17,-27,10,-12),fill=body); ld.ellipse(box(1,-28,14,-12),fill=body)
    ld.polygon(P((8,-24),(15,-35),(19,-32),(14,-17)),fill=body)                       # the neck
    ld.polygon(P((15,-37),(26,-34),(24,-29),(17,-30)),fill=body)                      # the head
    ld.polygon(P((16,-37),(13,-42),(18,-38)),fill=mid)                               # an ear
    ld.polygon(P((-16,-24),(-22,-27),(-18,-20)),fill=body)                           # the tail
    ld.line(P((-6,-14),(14,-14)),fill=mid,width=w)                                   # the belly shade
    ld.point(P((21,-34))[0],fill=(60,100,160,255))
    for dx,col in ((-3,mid),(0,body)):                                               # the antlers, far one first
        ld.line(P((17+dx,-37),(14+dx,-44),(9+dx,-51),(6+dx,-58)),fill=col,width=w)
        for (a0,b0,a1,b1) in ((14,-44,19,-48),(11,-48,15,-54),(9,-51,3,-53),(7,-55,11,-60)): ld.line(P((a0+dx,b0),(a1+dx,b1)),fill=col,width=max(1,int(sc)))
    halo=L.getchannel('A').filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v*0.55*a))
    im.paste((130,190,255),(0,0),halo); comp(im,L,a)
    rr=random.Random(int(f)*3+1)
    for _ in range(6):
        sx=x+rr.uniform(-30,16)*sc; sy=y+rr.uniform(-55,0)*sc; d.line([sx-1,sy,sx+1,sy],fill=(255,255,255)); d.line([sx,sy-1,sx,sy+1],fill=(255,255,255))

def closeup_patronus(t,f):
    """Harry shouting EXPECTO PATRONUM!, the wand's tip alight with silver, the cold all round."""
    def draw(im,d,t,f):
        glow(im,150,40,50,(140,190,255),0.35+0.2*t)
        rr=random.Random(f)
        for _ in range(30): d.point((rr.randint(0,W-1),rr.randint(24,H-1)),fill=(190,215,240))     # frost drifting
        harry_face(im,56,16,0.95,0.5+0.5*abs(math.sin(f*0.8)),(1,0))
        d=ImageDraw.Draw(im); d.line([92,58,106,46],fill=(120,80,50),width=2); d.line([106,46,120,41],fill=(120,80,50))
        r_=5+int(6*t); glow(im,122,41,r_+8,(190,225,255),0.9); d=ImageDraw.Draw(im); d.ellipse([119,38,125,44],fill=(255,255,255))
        for i in range(14):
            sx=124+i*4+rr.uniform(-1,1); sy=41+math.sin(i*0.9+f*0.5)*(2+i*0.4)-i*0.3
            d.point((sx,sy),fill=(235,248,255))
    return closeup(t,f,bg=(6,10,28),draw=draw,txt="EXPECTO PATRONUM!",box=(2,2,W-2,24),text_from=0,color=(220,240,255),outline=INK,max_scale=3,zoom=(200,225,255))

def clip_patronus(f):
    if 112<=f<138: s=scene(f,THEME); s['image']=closeup_patronus((f-112)/26,f); return s
    if f>=212: return neutral(f)
    s=scene(f,THEME); frozen=16<=f<176; mf=16 if frozen else f
    dark=ez(0,0.9,(f-16)/24) if f<176 else ez(0,0.9,1-(f-176)/34) if f<210 else 0
    if f<16: dark=0
    frost=ez(0,1,(f-56)/50) if f<176 else ez(0,1,1-(f-176)/36)
    pose='stand'
    if 56<=f<76: pose='cast'
    if 76<=f<96: pose='kneel'
    if 96<=f<190: pose='kneelup'
    if f>=190: pose='stand'
    thick=0.3
    s['fx'].append(('hp_dark',dark)); s['fx'].append(('hp_frost',frost))
    s['actors']=[actor(build('harry',pose),HX,pal=HPAL)]
    tip=put_wand(s,HARRY,pose,HX)
    if 56<=f<176 and pose!='stand':                                  # the wand light flickers
        rr=random.Random(f); a=0.25+0.6*rr.random()*(1 if f<144 else 1.5)
        if f<144 or f<150: s['fx'].append(('hp_glow',tip[0],tip[1],4+rr.randint(0,3),(190,225,255),a))
    for i,(dx,top) in enumerate(DEM):                                # the dementors glide down, then scatter
        t0=24+i*5; a=ez(0,1,(f-t0)/46); y=lerp(-44,top,a); x=dx+10*(1-a)
        ts=149+i*7
        if f>=ts: u=f-ts; x+=u*(1.3+0.5*i)*(1 if i%2 else 0.7); y-=u*u*0.22+u*1.2
        if f>=t0 and y>-50: s['fx'].append(('hp_dementor',x,y,38,i))
        if ts<=f<ts+8: s['fx'].append(('hp_glow',dx,top+16,10+(f-ts)*5,(235,248,255),0.9-(f-ts)*0.1))
    if 144<=f<200:                                                   # the stag bursts out of the wand and gallops
        u=f-144; x=tip[0]+u*3.8; sc=min(1,0.35+u/14*0.65); y=lerp(tip[1]+10,GROUND-1,min(1,u/14))-abs(math.sin(u*0.9))*3
        s['fx'].append(('hp_stag',x,y,sc*0.85,u*0.9,1.0))
        if u<8: s['flash']=1-u/8; s['fc']=(tip[0],tip[1]); s['flashc']=(235,248,255)
    if 150<=f<182 and f%11<2: s['flash']=0.6; s['fc']=(DEM[min(3,(f-150)//8)][0],28); s['flashc']=(235,248,255)
    finish(s,f,thick,mf)
    return s


# ---- horrocrux --------------------------------------------------------------------------------------------
DX, DY = 118, 44                                                     # the diary, on top of that headstone
FANG_UP, FANG_SWING, FANG_STAB = -math.pi/2 - 0.15, -0.5, math.pi/2 - 0.15
GHOST_GREEN = (150,255,190)

def _ang_tip(x,y,ang,L): return x+math.cos(ang)*L, y+math.sin(ang)*L

@fx('hp_fang')
def _fx_fang(d,im,e,f):
    """The basilisk's fang: long, curved, ivory, a base wider than its point (ang: where it points)."""
    _,x,y,ang,L=e; pts=[]; a=ang; cx_,cy_=x,y; left=[]; right=[]
    for i in range(int(L)+1):
        wd=2.2*(1-i/L)+0.4
        nx,ny=-math.sin(a),math.cos(a); left.append((cx_+nx*wd,cy_+ny*wd)); right.append((cx_-nx*wd,cy_-ny*wd))
        cx_+=math.cos(a); cy_+=math.sin(a); a+=0.07
    d.polygon(left+right[::-1],fill=(244,236,208),outline=(150,140,110)); d.line(left[:int(L*0.7)],fill=(255,252,238))

@fx('hp_diary')
def _fx_diary(d,im,e,f):
    """The little black leather diary, T. M. RIDDLE in gold on it (open: the pages, a flutter)."""
    _,x,y,mode,a=e
    if a<=0: return
    if mode==0:
        d.rectangle([x-4,y-4,x+4,y],fill=(16,14,20),outline=(70,66,76)); d.rectangle([x-2,y-3,x+2,y-2],fill=(232,190,70))
        d.point((x,y-1),fill=(232,190,70))
    else:
        fl=int(2*math.sin(f*0.9))
        d.polygon([(x-9,y-1),(x,y-2+fl),(x,y),(x-9,y+1)],fill=(236,234,214),outline=(120,110,90))
        d.polygon([(x+9,y-1),(x,y-2-fl),(x,y),(x+9,y+1)],fill=(236,234,214),outline=(120,110,90))
        d.line([x-8,y-1,x-2,y-2+fl],fill=(150,140,120)); d.line([x+8,y-1,x+2,y-2-fl],fill=(150,140,120))
        d.rectangle([x-10,y+1,x+10,y+2],fill=(16,14,20))

@fx('hp_diarylight')
def _fx_diarylight(d,im,e,f):
    """Pale green light pouring out of the open pages (a: its strength)."""
    _,x,y,a=e
    glow(im,x,y-6,16,GHOST_GREEN,0.55*a)
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for k in range(5):
        sx=x+(k-2)*3; md.polygon([(sx-1,y-2),(sx+1,y-2),(sx+(k-2)*6+2,y-44-k*3),(sx+(k-2)*6-2,y-44-k*3)],fill=int(70*a*(0.6+0.4*math.sin(f*0.5+k))))
    im.paste(GHOST_GREEN,(0,0),m.filter(ImageFilter.GaussianBlur(1)))

@fx('hp_ink')
def _fx_ink(d,im,e,f):
    """Black ink gushing out of the diary from t0, flying in arcs, splashing on the ground and the stone."""
    _,x0,y0,t0,a=e
    if f<t0 or a<=0: return
    L=Image.new('RGBA',(W,H),(0,0,0,0)); ld=ImageDraw.Draw(L); u0=f-t0
    ld.ellipse([x0-5-u0*0.12,y0-3,x0+5+u0*0.12,y0+2],fill=(8,5,14,255))
    for k in range(70):
        rr=random.Random(k+11); ts=rr.uniform(0,34)
        if u0<ts: continue
        u=u0-ts; sp=rr.uniform(2.6,5.8); ang=rr.uniform(-2.6,-0.55)
        x=x0+math.cos(ang)*sp*u; y=y0+math.sin(ang)*sp*u+0.17*u*u; r=rr.choice((1,1,2))
        if y>=GROUND-1:
            y=GROUND-1; ld.ellipse([x-r-1,y-1,x+r+1,y],fill=(8,5,14,255)); continue
        ld.ellipse([x-r,y-r,x+r,y+r],fill=(8,5,14,255)); ld.point((x-r*0.4,y-r*0.4),fill=(70,60,100,255))
    ld.polygon([(x0-4,y0),(x0+4,y0),(x0+3,y0+min(10,u0*0.3)),(x0-3,y0+min(7,u0*0.2))],fill=(8,5,14,255))   # running down the stone
    comp(im,L,a)

@fx('hp_motes')
def _fx_motes(d,im,e,f):
    """Pale green specks rising off whatever is dissolving: x, y (its middle), t0, a."""
    _,x,y,t0,a=e
    if f<t0 or a<=0: return
    u0=f-t0
    for k in range(40):
        rr=random.Random(k+3); ts=rr.uniform(0,26)
        if u0<ts: continue
        u=u0-ts; px=x+rr.uniform(-6,6)+math.sin(u*0.3+k)*1.5; py=y+rr.uniform(-10,12)-u*rr.uniform(0.5,1.4)
        if py>0: d.point((int(px),int(py)),fill=(200,255,220) if k%2 else (120,230,170))

@fx('hp_cracks')
def _fx_cracks(d,im,e,f):
    """Beams of light bursting through Riddle (x, y: his middle; a: their strength)."""
    _,x,y,a=e; rr=random.Random(f*7)
    for k in range(7):
        ang=rr.uniform(0,2*math.pi); L_=rr.uniform(14,34)*a; x1,y1=x+math.cos(ang)*L_,y+math.sin(ang)*L_
        d.line([x,y,x1,y1],fill=(190,255,215)); d.line([x,y,x+(x1-x)*0.5,y+(y1-y)*0.5],fill=(255,255,255))
    glow(im,x,y,12,(210,255,225),0.5*a)

def closeup_riddle(t,f):
    """Young Tom Riddle out of the diary: pale green, smug."""
    def draw(im,d,t,f):
        glow(im,62,34,44,GHOST_GREEN,0.35)
        L=Image.new('RGBA',(W,H),(0,0,0,0)); riddle_face(L,62,14,0.95,1.0); comp(im,L,0.9,GHOST_GREEN,0.28)
        d=ImageDraw.Draw(im); y=56
        for k in range(3): d.line([112+k*3,y,100+k*14,10],fill=(20,70,50))
        glow(im,140,y-3,22,GHOST_GREEN,0.6); d=ImageDraw.Draw(im)
        d.polygon([(118,y-2),(140,y-6+int(2*math.sin(f*0.6))),(140,y+1),(118,y+3)],fill=(236,234,214),outline=(120,110,90))
        d.polygon([(162,y-2),(140,y-6-int(2*math.sin(f*0.6))),(140,y+1),(162,y+3)],fill=(236,234,214),outline=(120,110,90))
        rr=random.Random(f)
        for _ in range(12): d.point((rr.randint(100,180),rr.randint(8,50)),fill=(190,255,215))
    return closeup(t,f,bg=(4,16,12),draw=draw,txt="HELLO, HARRY.",box=(2,2,W-2,24),text_from=0,color=(210,255,225),outline=INK,max_scale=3,zoom=GHOST_GREEN)

def clip_horrocrux(f):
    if 128<=f<154: s=scene(f,THEME); s['image']=closeup_riddle((f-128)/26,f); return s
    if f>=282: return neutral(f)
    s=scene(f,THEME)
    hpx,_=hand(HARRY,'stab',0); XS=int(round(DX-1-(hpx+math.cos(FANG_STAB)*10)))   # where Harry stands to stab it
    x=HX; pose='stand'; flip=False; fang=None
    if 16<=f<54: x=lerp(HX,XS,ez(0,1,(f-16)/38)); pose='walk1' if (f//5)%2 else 'walk2'
    if 54<=f<190: x=XS
    if 54<=f<76: pose='point'
    if 76<=f<154: pose='stand'
    if 154<=f<188: pose='lift'; fang=(FANG_UP,10)
    if 188<=f<192: pose='swing'; fang=(FANG_SWING,10)
    if 192<=f<216: pose='stab'; fang=(FANG_STAB,10)
    if 216<=f<240: x=XS; pose='stand'
    if 240<=f<282: x=lerp(XS,HX,ez(0,1,(f-240)/42)); pose='walk1' if (f//5)%2 else 'walk2'; flip=True
    if f>=282: x=HX; flip=False; pose='stand'
    s['actors']=[actor(build('harry',pose),x,flip=flip,pal=HPAL)]
    if fang: hx_,hy_=hand(HARRY,pose,x,flip); s['fx'].append(('hp_fang',hx_,hy_,fang[0],fang[1]))
    elif pose!='lift': put_wand(s,HARRY,pose,x,flip)
    dfade=1.0 if f<252 else max(0,1-(f-252)/20)
    if 16<=f<22: s['fx'].append(('spark',DX,DY-5,3))
    opened=60<=f<256
    if 16<=f<272: s['fx'].append(('hp_diary',DX,DY,1 if opened else 0,min(1,(f-16)/6)*dfade))
    if opened and f<260: s['fx'].append(('hp_diarylight',DX,DY,min(1,(f-60)/16)*(1 if f<198 else max(0,1-(f-198)/50))))
    if f>=196: s['fx'].append(('hp_ink',DX,DY-2,196,dfade))
    if 194<=f<198: s['shake']=rshake(2)
    if 196<=f<199: s['flash']=0.4-(f-196)*0.12; s['fc']=(DX,DY); s['flashc']=(255,255,240)
    finish(s,f)
    base=render(s,f)
    r=ez(0,1,(f-84)/44) if f<84+44 else 1.0
    if 84<=f<262:                                                    # Riddle rises out of the pages, cracks, dissolves
        a=0.88*(min(1,(f-84)/16)) if f<226 else 0.88*max(0,1-(f-226)/32)
        rp='hurt' if 198<=f<236 else 'stand'; rx=DX+(random.Random(f).choice((-1,0,1)) if 198<=f<236 else 0)
        feet=DY+(1-r)*34; tmp=base.copy()
        draw(tmp,build('riddle',rp),rx,feet,True,aura=(GHOST_GREEN,1),alpha=a,pal=RPAL,f=f)
        base.paste(tmp.crop((0,0,W,DY)),(0,0)); d=ImageDraw.Draw(base)
        if 198<=f<246: draw_fx(d,base,('hp_cracks',rx,feet-14,min(1,(f-198)/10)*(1 if f<226 else max(0,1-(f-226)/20))),f)
        if 214<=f<262: draw_fx(d,base,('hp_motes',DX,DY-14,214,1),f)
    s['image']=base
    return s


# ---- basilisco --------------------------------------------------------------------------------------------
EMER, EMER_D, EMER_L = (30,140,74), (12,70,40), (80,205,120)

def _bez(p0,p1,p2,p3,n=36):
    out=[]
    for i in range(n+1):
        t=i/n; u=1-t
        out.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return out

def _rot(pts,ang,s,ox,oy):
    c,sn=math.cos(ang),math.sin(ang); return [(ox+(x*c-y*sn)*s,oy+(x*sn+y*c)*s) for x,y in pts]

def head_roof(ox,oy,ang,s): return _rot([(-22,5)],ang,s,ox,oy)[0]

def basilisk(d,im,ox,oy,ang,op,s,f,dead=False):
    """The basilisk: a huge emerald serpent coiling up from the right, a wedge head facing left (ox, oy: the
    back of its skull; ang: tilted down; op: jaw open, radians; s: size), yellow lamp eyes, fangs."""
    for path,r0,r1 in ((_bez((W+40,GROUND+2),(W-10,44),(W-70,72),(W-110,GROUND-6),30),11,9),
                       (_bez((W+50,GROUND+6),(W+60,24),(ox+70,oy+50),(ox+4,oy+4),40),17,13)):
        for k,(x,y) in enumerate(path):
            r=lerp(r0,r1,k/len(path))*(s if path[-1][0]==ox+4 else 1)**0.5
            d.ellipse([x-r,y-r,x+r,y+r],fill=EMER_D)
        for k,(x,y) in enumerate(path):
            r=lerp(r0,r1,k/len(path))*(s if path[-1][0]==ox+4 else 1)**0.5
            d.ellipse([x-r+2,y-r+1,x+r-2,y+r-3],fill=EMER if k%4 else (22,112,60))
            if k%3==0: d.ellipse([x-r*0.5,y-r*0.7,x+r*0.2,y-r*0.2],fill=EMER_L)
    R=lambda pts: _rot(pts,ang,s,ox,oy)
    pivot=(-2,6); jaw=[(-2,6),(-30,6),(-42,3),(-40,9),(-30,12),(-8,14),(2,10)]
    jr=_rot([(x-pivot[0],y-pivot[1]) for x,y in jaw],-op,1,pivot[0],pivot[1]); jw=R(jr)
    up=R([(0,-14),(-12,-19),(-26,-14),(-42,-4),(-46,2),(-30,5),(-10,6),(2,5)])
    d.polygon(R([(2,5),(-46,2)])+R(_rot([(-42,3),(-30,6)],-op,1,-2,6)[::-1] if False else [])+jw[1:3][::-1] if False else up,fill=EMER)
    inner=R([(2,5),(-44,2)])+[jw[2],jw[1]]
    d.polygon(inner,fill=(120,18,30))
    d.polygon(jw,fill=EMER_D,outline=(8,40,24))
    d.polygon(up,fill=EMER,outline=(8,40,24))
    d.polygon(R([(-6,-15),(-22,-14),(-36,-5),(-30,0),(-10,0)]),fill=EMER_L)
    for cx_ in (-6,-14,-22): d.polygon(R([(cx_,-17),(cx_-3,-17),(cx_-1,-24)]),fill=(180,200,60))   # the crest
    fg=R([(-37,4),(-33,4),(-35,4+8+op*8)]); d.polygon(fg,fill=(250,248,232),outline=(150,150,130))
    fg2=_rot([(-37,8),(-33,8),(-35,8-9-op*5)],-op,1,-2,6); d.polygon(R(fg2),fill=(250,248,232))
    ex,ey=R([(-14,-8)])[0]; er=5*s
    if dead:
        d.line([ex-er,ey-er,ex+er,ey+er],fill=(10,30,20),width=2); d.line([ex-er,ey+er,ex+er,ey-er],fill=(10,30,20),width=2)
    else:
        glow(im,ex,ey,int(er*2),(255,230,60),0.55); d.ellipse([ex-er,ey-er*0.7,ex+er,ey+er*0.7],fill=(255,232,40),outline=(150,110,10))
        d.line([ex,ey-er*0.7,ex,ey+er*0.7],fill=(0,0,0),width=max(1,int(s))); d.point((ex-er*0.4,ey-er*0.3),fill=(255,255,200))
    nx,ny=R([(-40,-1)])[0]; d.point((nx,ny),fill=(0,30,16))

@fx('hp_basilisk')
def _fx_basilisk(d,im,e,f):
    _,ox,oy,ang,op,s,dead=e; basilisk(d,im,ox,oy,ang,op,s,f,dead)

@fx('hp_ripple')
def _fx_ripple(d,im,e,f):
    """Ripples on the flooded floor, and a drip from the roof (a loop)."""
    ph=loop.phase(f,48); rr=random.Random(4)
    for i in range(14):
        y=47+rr.randint(0,15); x=(rr.randint(0,W)+ph*W*(1 if i%2 else -1))%W; l=rr.randint(6,16)
        d.line([x,y,x+l,y],fill=(60,120,100) if (i+int(ph*8))%3 else (110,170,140))
    dx=(40+int(ph*3)*0)%W
    dy=(ph*3%1)*GROUND; d.point((30,int(dy)),fill=(150,210,190))

def fawkes(d,x,y,sc,f,hat=False):
    """Fawkes in flight, facing left: scarlet and gold, long tail, wings beating; carries the Sorting Hat."""
    fl=math.sin(f*0.9); S_=lambda v: v*sc
    for k,(ty,col) in enumerate(((0,(255,190,60)),(3,(230,60,30)),(-3,(240,120,40)))):          # the long tail
        pts=[(x+S_(8+i*3),y+S_(3+ty+math.sin(i*0.5+f*0.3)*1.5+i*0.6)) for i in range(9)]; d.line(pts,fill=col,width=max(1,int(sc*1.5)))
    for sgn in (-1,1):                                                                           # the wings
        up=y-S_(6)+sgn*0; tipy=y+S_(-16*fl*(1 if sgn>0 else 0.6)-4)
        d.polygon([(x+S_(-2),y-S_(2)),(x+S_(8),y-S_(2)),(x+S_(18),tipy),(x+S_(4),tipy+S_(2)),(x-S_(6),tipy+S_(4))] if sgn>0 else
                  [(x-S_(1),y),(x+S_(6),y),(x+S_(10),tipy-S_(4)),(x-S_(2),tipy-S_(2))],fill=(232,70,36) if sgn>0 else (190,40,28),outline=(255,196,70))
    d.ellipse([x-S_(8),y-S_(5),x+S_(9),y+S_(5)],fill=(236,80,40)); d.ellipse([x-S_(5),y,x+S_(7),y+S_(5)],fill=(255,184,70))
    d.ellipse([x-S_(13),y-S_(7),x-S_(5),y+S_(1)],fill=(240,90,44))                                # the head
    d.polygon([(x-S_(13),y-S_(4)),(x-S_(18),y-S_(2)),(x-S_(13),y-S_(1))],fill=(255,210,80))      # the beak
    d.point((x-S_(10),y-S_(4)),fill=(10,10,10)); d.line([x-S_(9),y-S_(7),x-S_(5),y-S_(10)],fill=(255,190,60))
    if hat: hat_fx(d,x-S_(2),y+S_(14),sc*0.8); d.line([x-S_(2),y+S_(4),x-S_(2),y+S_(8)],fill=(255,190,60))

def hat_fx(d,x,y,sc=1.0):
    """The Sorting Hat: battered, patched, pointed, the tip bent over (y: its base)."""
    S_=lambda v: v*sc
    d.polygon([(x-S_(8),y),(x+S_(8),y),(x+S_(4),y-S_(9)),(x+S_(7),y-S_(15)),(x+S_(1),y-S_(13)),(x-S_(4),y-S_(8))],fill=(126,92,56),outline=(70,48,30))
    d.ellipse([x-S_(10),y-S_(2),x+S_(10),y+S_(2)],fill=(110,78,46),outline=(70,48,30))
    d.rectangle([x-S_(3),y-S_(6),x+S_(1),y-S_(3)],fill=(166,130,78)); d.line([x-S_(6),y-S_(3),x+S_(5),y-S_(4)],fill=(80,56,34))
    d.point((x-S_(2),y-S_(1)),fill=(20,10,6)); d.line([x+S_(2),y-S_(2),x+S_(5),y-S_(3)],fill=(60,40,24))

@fx('hp_fawkes')
def _fx_fawkes(d,im,e,f):
    _,x,y,sc,hat=e; fawkes(d,x,y,sc,f,hat)

@fx('hp_hat')
def _fx_hat(d,im,e,f): _,x,y=e; hat_fx(d,x,y)

@fx('hp_sword')
def _fx_sword(d,im,e,f):
    """The sword of Gryffindor from the hand at (x, y) towards ang: silver blade, gold guard, rubies."""
    _,x,y,ang,L=e
    if L<=0: return
    c,sn=math.cos(ang),math.sin(ang); nx,ny=-sn,c
    p=lambda t,o=0: (x+c*t+nx*o,y+sn*t+ny*o)
    d.line([p(-2),p(3)],fill=(120,70,40),width=2)
    d.line([p(3,-3),p(3,3)],fill=(236,190,70),width=2)
    d.point(p(3,0),fill=(220,30,50)); d.point(p(3,-3),fill=(220,30,50)); d.point(p(3,3),fill=(220,30,50))
    d.polygon([p(4,-1.4),p(4+L,0),p(4,1.4)],fill=(214,226,240),outline=(150,164,184)); d.line([p(5),p(L)],fill=(255,255,255))

def closeup_sword(t,f):
    """The sword of Gryffindor close up: silver blade, a gold hilt, the rubies glinting."""
    def draw(im,d,t,f):
        glow(im,100,40,60,(60,170,110),0.25); d=ImageDraw.Draw(im)
        for k in range(3): d.line([20+k*30,0,60+k*30,64],fill=(14,40,32))
        d.polygon([(54,38),(W+4,41),(W+4,45),(54,48)],fill=(206,220,238),outline=(120,136,160))
        d.line([54,43,W,43],fill=(150,166,190)); d.line([56,40,W,42],fill=(255,255,255))
        sx=int(lerp(40,W,(t*1.5)%1)); d.polygon([(sx,39),(sx+6,40),(sx+2,47),(sx-4,47)],fill=(255,255,255))      # the shine sweeping
        d.rectangle([22,41,50,46],fill=(110,66,40)); [d.line([x_,41,x_,46],fill=(70,40,24)) for x_ in range(25,50,4)]   # the grip
        d.rectangle([48,26,54,60],fill=(236,190,70),outline=(150,110,30))                                   # the guard
        d.ellipse([8,38,22,50],fill=(236,190,70),outline=(150,110,30))                                      # the pommel
        for rx,ry,rr_ in ((51,43,3),(51,29,2),(51,57,2),(15,44,3)):
            d.ellipse([rx-rr_,ry-rr_,rx+rr_,ry+rr_],fill=(220,24,50),outline=(110,10,24)); d.point((rx-1,ry-1),fill=(255,170,170))
        for k,(rx,ry) in enumerate(((51,43),(15,44),(51,29),(51,57))):
            ph=(f*0.25+k*0.8)%3
            if ph<1.2:
                q=int(3+ph*3); d.line([rx-q,ry,rx+q,ry],fill=(255,255,255)); d.line([rx,ry-q,rx,ry+q],fill=(255,255,255))
    return closeup(t,f,bg=(4,12,10),draw=draw,txt="GODRIC GRYFFINDOR",box=(2,2,W-2,22),text_from=0,color=(236,226,200),outline=INK,max_scale=3,zoom=(200,255,220))

def chamber_scene(f):
    s=scene(f,'hp_chamber'); s['under'].append(('fog',{'dens':0.45,'y0':30,'y1':62,'color':(40,120,84)})); s['under'].append(('hp_ripple',)); return s

def clip_basilisco(f):
    if 124<=f<152: s=scene(f,THEME); s['image']=closeup_sword((f-124)/28,f); return s
    if f>=244: return neutral(f)
    if f<20:
        s=neutral(f); return flash_to(s,f,(30,110,70),(f-16)/4) if f>=16 else s
    s=chamber_scene(f); hx=40; hp='stand'; sword=None
    ox,oy,ang,op,s_,dead=128,18,0.15,0.1,1.0,False
    tip_x=48; hand_p=hand(HARRY,'thrust',tip_x); C=_ang_tip(hand_p[0],hand_p[1],-1.25,22+4)
    if f<60: u=ez(0,1,(f-24)/36); oy=lerp(54,18,u); ang=lerp(0.6,0.15,u); ox=lerp(150,128,u)
    if 24<=f<72: hp='cringe'
    if f<24: oy=54; ox=150; ang=0.6
    if 60<=f<100:                                                    # Fawkes brings the hat
        u=(f-60)/36
        if f<89: s['fx'].append(('hp_fawkes',lerp(100,48,ez(0,1,u)),lerp(14,10,u),lerp(0.5,1.1,u),True))
        elif f<114:
            uu=(f-89)/25; s['fx'].append(('hp_fawkes',lerp(48,-10,uu),lerp(10,-14,uu),1.1,False))
    if 89<=f<124:
        hy_=min(GROUND-1,lerp(24,GROUND-1,((f-89)/10)**2)); s['fx'].append(('hp_hat',50,hy_))
    if 100<=f<124: hp='crouch'; hand_c=hand(HARRY,'crouch',hx); sword=(hand_c[0],hand_c[1]-3,-1.1,lerp(0,22,ez(0,1,(f-104)/18)))
    if f>=152:
        hp='lift' if f<168 else 'thrust'; hx=tip_x if hp=='thrust' else 40+8*ez(0,1,(f-152)/16)
        hh=hand(HARRY,hp,hx); sword=(hh[0],hh[1],-1.25 if hp=='thrust' else -1.45,22)
    lungeu=ez(0,1,(f-152)/24)
    if f>=152:
        ox_,oy_=C[0]+0,C[1]; ang=lerp(0.15,0.55,lungeu); s_=lerp(1.0,1.3,lungeu); op=lerp(0.1,0.75,lungeu)
        r0=head_roof(0,0,ang,s_); ox=lerp(128,C[0]-r0[0],lungeu); oy=lerp(18,C[1]-r0[1],lungeu)
    if f>=176:
        if f<180: s['flash']=0.5; s['fc']=C; s['flashc']=(255,240,200)
        if f<190: ox+=random.Random(f).choice((-1,0,1)); oy+=random.Random(f+9).choice((-1,0,1)); dead=f>=180
        if f<190: s['shake']=rshake(1)
        else:
            u=ez(0,1,(f-190)/34); dead=True; ox=lerp(ox,ox-4,u); oy=lerp(oy,50,u); ang=lerp(ang,0.95,u); op=lerp(op,0.3,u)
            if f>=190: sword=None
        for k in range(3):
            if f<236: s['fx'].append(('mote',C[0]-8+k*5,C[1]+10+((f*2+k*7)%30),(150,20,30)))
    s['under'].append(('hp_basilisk',ox,oy,ang,op,s_,dead))
    if f>=180 and f<190 and sword is None: sword=None
    s['actors']=[actor(build('harry',hp),hx,pal=HPAL)]
    if sword: s['fx'].append(('hp_sword',)+sword)
    elif hp not in ('crouch',): put_wand(s,HARRY,hp if hp in POSES else 'stand',hx)
    if f<28: return flash_to(s,f,(30,110,70),1-(f-20)/8)
    if f>=232: return flash_to(s,f,(200,255,220),(f-232)/12) if f<244 else s
    return s

CLIPS = [clip('priori', N_, clip_priori), clip('patronus', 288, clip_patronus), clip('horrocrux', 288, clip_horrocrux), clip('basilisco', 288, clip_basilisco)]
