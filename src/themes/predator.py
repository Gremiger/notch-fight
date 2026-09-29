"""Predator: Claude (an 80s jungle commando: red bandana, olive fatigues) vs the Yautja hunter in a
night jungle. Three red laser dots crawl onto Claude, a cloaked shimmer moves through the trees —
close-up in the hunter's THERMAL vision, Claude glowing hot. He covers himself in mud and goes cold:
the reticle loses him. The Predator decloaks in blue sparks and pulls his mask off (close-up of the
mandibles, roar), a brawl, Claude drops the log trap on him. Beaten, he arms the wrist bomb (red alien
countdown, laughter), Claude runs, the jungle goes up in a mushroom flash — and a shimmer is back in
the trees for the loop."""
from engine import *

THEME = 'predator'
N_ = 348

# ---- colours (per-actor pal: no PAL.update) --------------------------------------------------
CPAL={'1':(78,98,50),'2':(46,60,32),'3':(186,40,34),'4':(34,28,22),'q':(66,44,28)}
LASER=(255,36,24)
ZAP=(110,180,255)

def _mix(a,b,k): return tuple(int(lerp(a[i],b[i],k)) for i in range(3))
def _lum(c): return (c[0]*3+c[1]*6+c[2])/10/255
_CL_KEYS={**{k:PAL[k] for k in 'OoK'},**CPAL}
def cpal(mud=0.0):
    """Claude's palette, pulled towards grey-brown mud (0..1); the eyes stay dark."""
    if mud<=0: return CPAL
    return {ch:(c if ch=='K' else _mix(c,_mix((60,52,40),(128,114,90),_lum(c)*1.4),mud)) for ch,c in _CL_KEYS.items()}

# ---- Claude: the commando ---------------------------------------------------------------------
def _commando(x,y,t,l,r,c,h):
    if c=='.': return None
    inside=l<=x<=r
    if y>=h-2: return '4' if y==h-1 else '1'                        # fatigues + boots
    if inside and y==t: return 'q'                                  # hair
    if inside and y==t+1: return '3'                                # the bandana
    if inside and y==t+8: return '4'                                # belt
    if inside and y>=t+5: return '2' if (x*3+y*5)%7==0 else '1'     # camo shirt
    return None                                                     # face 'O', bare arms 'o'
def _cm(s):
    h=len(s); s=recolor_rows(s,lambda x,y,t,l,r,c: _commando(x,y,t,l,r,c,h))
    t,l,_=body_box(s)
    return paint(s,[(l-2,t+1,'33'),(l-2,t+2,'3.')],grow=True)      # bandana tails behind the head
CM={k:_cm(v) for k,v in CL.items()}

# ---- the Predator (drawn facing right; flip=True faces Claude) --------------------------------
YPAL={'l':(30,26,20),'L':(150,126,64),'m':(176,170,150),'e':(22,22,26),'a':(146,146,84),'A':(78,80,46),
      'd':(66,62,60),'D':(132,102,58),'c':(86,88,96),'C':(150,152,162),'w':(118,96,60),'B':(226,230,238),
      'x':(52,44,34),'r':(255,36,24)}
UNMASK={**YPAL,'m':(128,126,72),'e':(236,180,40)}                   # no mask: skin + yellow eyes
_Y_RAW=[
".....llll...........",
"....lmmmmm..........",
"...lmmmmmmm.........",
"..llmmmmmmmm........",
"..lLmeemmeem..cCC...",
".ll.mmmmmmmm.ccc....",
".l.llmmmmmm.cc......",
".L.l.lmmmm.dd.......",
".l.l.aaaaaDDD.......",
"...dDddddddddD......",
"..DdaAaAaAaddDa.....",
"..aaAaAaAaAa.aa.....",
"..aa.aAaAaAa..aa....",
"..aa.ddddddd..aww...",
"..aa.aAaAaAa...wwBBB",
"..ww.aaaaaaa....BBB.",
"..aa.xxxxxxx........",
".....xxxxxxxx.......",
".....aaa..aaa.......",
".....aAa..aAa.......",
".....aa....aa.......",
".....aa....aa.......",
".....dd....dd.......",
"....ddd....ddd......",
]
def _sway(rows):
    """Idle 2: the dreadlocks swing one pixel back."""
    out=[]
    for i,r in enumerate(rows):
        if 5<=i<=8: r=('.'+r[:3]+r[4:]) if r[0]!='.' or i>5 else r
        out.append(r)
    return out
_Y_ATK=[r[:14]+'......' for r in _Y_RAW[:13]]+[
"..aa.ddddddd.aaaww..",
"..aa.aAaAaAa....wwBBBB",
"..ww.aaaaaaa......BBBB",
]+[r for r in _Y_RAW[16:]]
YA={'idle':S(_Y_RAW),'idle2':S(_sway(_Y_RAW)),'attack':S(_Y_ATK)}
YA['hurt']=hurt(YA['idle'])
YA['down']=rotate90(YA['hurt'],3,trim=True)
def y_idle(f): return YA['idle'] if (f//6)%2==0 else YA['idle2']

def cell_at(spr,cx,feet,flip,ch):
    """World position of the first cell holding ch (None when absent)."""
    ox,oy=origin(spr,cx,feet); w=len(spr[0])
    for y,row in enumerate(spr):
        if ch in row:
            x=row.index(ch); return (ox+(w-1-x) if flip else ox+x), oy+y
    return None

# ---- background: the jungle at night -----------------------------------------------------------
TREES=((8,6),(56,4),(98,5),(138,7),(176,5))
MUD=(14,46)
def _jungle(d):
    for y in range(GROUND+1):                                        # night sky, deeper at the top
        v=y/GROUND; d.line([0,y,W,y],fill=(int(4+6*v),int(8+12*v),int(10+10*v)))
    d.ellipse([150,3,158,11],fill=(40,52,56)); d.ellipse([152,3,159,10],fill=(10,16,20))   # thin moon
    for x0,w in TREES:                                               # trunks, with a lit edge
        d.rectangle([x0-w//2,0,x0+w//2,GROUND],fill=(14,20,16))
        d.line([x0+w//2,0,x0+w//2,GROUND],fill=(24,34,26))
        for y in range(6,GROUND,9): d.line([x0-w//2,y,x0-w//2+2,y+2],fill=(10,14,12))
    rr=random.Random(58)
    for i in range(70):                                              # canopy
        x=rr.randint(-6,W+6); y=rr.randint(-6,10); r=rr.randint(4,9)
        d.ellipse([x-r,y-r//2,x+r,y+r//2],fill=(12,26,16) if i%3 else (18,36,22))
    for x in (30,78,118,160):                                        # hanging vines
        ln=rr.randint(16,30)
        for y in range(4,ln): d.point((x+int(math.sin(y*0.4)*1.5),y),fill=(20,40,24))
    for i in range(34):                                              # ferns along the ground
        x=rr.randint(0,W); h=rr.randint(3,7); c=(16,38,20) if i%2 else (22,50,26)
        d.line([x,GROUND,x-3,GROUND-h],fill=c); d.line([x,GROUND,x+3,GROUND-h+1],fill=c); d.line([x,GROUND,x,GROUND-h-1],fill=c)
    d.ellipse([MUD[0],GROUND-1,MUD[1],GROUND+3],fill=(46,36,26)); d.line([MUD[0]+5,GROUND,MUD[1]-6,GROUND],fill=(62,50,36))
register_bg(THEME, lambda v: (v//3,v,v//2), decor=_jungle)

# ---- effects ------------------------------------------------------------------------------------
@fx('pred_flies')
def _fx_flies(d,im,e,f):
    """Fireflies drifting between the trunks (periods 58/87: loop-safe over 348 frames)."""
    for i in range(7):
        a=2*math.pi*(f%87/87+i/7); b=2*math.pi*(f%58/58+i*0.3)
        x=(i*29+17)%W+math.sin(a)*8; y=24+(i*7)%20+math.cos(b)*4
        if math.sin(b*2+i)>-0.3: d.point((int(x),int(y)),fill=(170,220,90) if i%2 else (120,170,70))

def cloak(im,spr,cx,feet,flip,k,f,edge=0.4):
    """Active camouflage: the body refracts the jungle behind it (sampled a few px off) with a faint
    glassy rim. k = strength 0..1."""
    if k<=0: return
    m,w,h=mask_of(spr,flip); ox,oy=int(round(cx-w/2)),int(round(feet-h))
    src=im.copy().load(); px=im.load(); pts=set(m)
    for (x,y) in pts:
        X,Y=ox+x,oy+y
        dx=2 if math.sin(Y*0.8+2*math.pi*f/12)>0 else -2
        sx=min(W-1,max(0,X+dx)); c=src[sx,Y] if 0<=Y<H else (0,0,0)
        blend(px,X,Y,tuple(min(255,int(v*1.35+8)) for v in c),k)
    for (x,y) in dilate(pts,1)-pts:
        if (x+y+f//2)%3: blend(px,ox+x,oy+y,(150,200,190),edge*k)

@fx('pred_cloak')
def _fx_cloak(d,im,e,f):
    _,spr,x,feet,flip,k=e; cloak(im,spr,x,feet,flip,k,f)

@fx('pred_zap')
def _fx_zap(d,im,e,f):
    """Decloaking: blue electric crackles jumping over the sprite's outline (n arcs)."""
    _,spr,cx,feet,flip,n=e
    m,w,h=mask_of(spr,flip); ox,oy=int(round(cx-w/2)),int(round(feet-h))
    edge=sorted(dilate(set(m),1)-set(m))
    for _ in range(int(n)):
        x,y=random.choice(edge); X,Y=ox+x,oy+y
        pts=[(X,Y)]
        for _ in range(3): X+=random.choice((-2,-1,1,2)); Y+=random.choice((-2,-1,1)); pts.append((X,Y))
        d.line(pts,fill=ZAP); d.point(pts[0],fill=(240,250,255))

def dots(d,im,x,y,k=1.0):
    """The plasma caster's triple laser sight: three red dots in a triangle, with a soft halo."""
    px=im.load()
    for (dx,dy) in ((0,-2),(-2,1),(2,1)):
        X,Y=int(x+dx),int(y+dy)
        for ax,ay in ((1,0),(-1,0),(0,1),(0,-1)): blend(px,X+ax,Y+ay,LASER,0.4*k)
        blend(px,X,Y,(255,200,190),k)
@fx('pred_dots')
def _fx_dots(d,im,e,f):
    _,x,y,*k=e; dots(d,im,x,y,k[0] if k else 1.0)

@fx('pred_mud')
def _fx_mud(d,im,e,f):
    """A clod of mud: a 2x2 grey-brown splat."""
    _,x,y=e; d.rectangle([int(x),int(y),int(x)+1,int(y)+1],fill=(84,70,52))

@fx('pred_rope')
def _fx_rope(d,im,e,f):
    """The trap's vine: from Claude's hand up to a branch, along the canopy, down to the log."""
    _,pts=e; d.line(pts,fill=(86,112,58))

@fx('pred_log')
def _fx_log(d,im,e,f):
    """The deadfall log: a bark cylinder with cut rings at both ends."""
    _,x,y=e; x,y=int(x),int(y)
    d.rectangle([x-13,y-3,x+13,y+3],fill=(92,62,36)); d.line([x-12,y-2,x+12,y-2],fill=(128,90,54))
    for k in range(-10,11,5): d.line([x+k,y+1,x+k+3,y+1],fill=(62,40,24))
    for ex in (x-14,x+14): d.ellipse([ex-2,y-3,ex+2,y+3],fill=(170,130,80)); d.point((ex,y),fill=(110,76,44))

@fx('pred_blink')
def _fx_blink(d,im,e,f):
    """The wrist bomb blinking red, faster as the countdown runs (period p)."""
    _,x,y,p=e; px=im.load()
    if (f//max(1,p))%2: return
    for dx in range(-3,4):
        for dy in range(-3,4):
            r=abs(dx)+abs(dy)
            if r<=3: blend(px,x+dx,y+dy,(255,30,20),0.9 if r==0 else 0.5/r)

@fx('pred_nuke')
def _fx_nuke(d,im,e,f):
    """The self-destruct: white-out, a fireball that climbs into a mushroom cap on a stem, and a
    ground shockwave; the whole jungle lit orange, then smoke."""
    _,x,age=e; base=im.copy()
    heat=max(0,1-age/22)
    im.paste(fade_to(im,(255,140,50),0.55*heat)); d=ImageDraw.Draw(im)
    sw=10+age*9                                                      # shockwave along the ground
    if age<14: d.ellipse([x-sw,GROUND-3,x+sw,GROUND+3],outline=_mix((120,60,30),(255,230,160),heat))
    r=min(20,5+age*2.2); cy=max(20,GROUND-6-age*2.6)
    cols=[(255,255,236),(255,226,110),(255,140,40),(200,60,24),(80,50,40)]
    k=min(4,age/5)
    shade=lambda i: _mix(cols[min(4,int(k)+i)],cols[min(4,int(k)+i+1)],k-int(k))
    sw2=max(3,int(r*0.35))                                           # the stem
    d.polygon([(x-sw2,cy),(x+sw2,cy),(x+sw2+4,GROUND),(x-sw2-4,GROUND)],fill=shade(1))
    d.rectangle([x-sw2//2,cy,x+sw2//2,GROUND],fill=shade(0))
    d.ellipse([x-r*1.6,GROUND-r*0.5,x+r*1.6,GROUND+2],fill=shade(1))   # base surge
    d.ellipse([x-r*1.45,cy-r*0.75,x+r*1.45,cy+r*0.55],fill=shade(2))    # the cap
    d.ellipse([x-r*1.2,cy-r*0.7,x+r*1.2,cy+r*0.35],fill=shade(1))
    d.ellipse([x-r*0.7,cy-r*0.5,x+r*0.7,cy+r*0.1],fill=shade(0))
    for i in range(7):                                               # the rolling rim below the cap
        a=math.pi*(i/6); rx=x+math.cos(a)*r*1.3; ry=cy+r*0.4+math.sin(a)*2
        d.ellipse([rx-3,ry-2,rx+3,ry+2],fill=shade(2))
    if age<5: im.paste(fade_to(im,(255,255,255),1-age/5))
    if age>16: im.paste(Image.blend(base,im,max(0,1-(age-16)/11)))    # the cloud thins away

@fx('pred_smolder')
def _fx_smolder(d,im,e,f):
    """What is left: a scorched crater, embers and a rising smoke column, fading by k."""
    _,x,k=e; px=im.load()
    for dx in range(-26,27):
        for dy in range(-1,3): blend(px,x+dx,GROUND+dy,(10,8,6),0.8*k*(1-abs(dx)/27))
    rr=random.Random(f//2)
    for i in range(int(20*k)):
        yy=GROUND-rr.uniform(0,40)*k; xx=x+rr.uniform(-6,6)+math.sin(yy*0.2)*3; r=rr.randint(2,4)
        d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=_mix((20,24,20),(70,66,60),k*rr.random()))
    for i in range(int(10*k)):
        d.point((x+rr.randint(-18,18),GROUND-rr.randint(0,3)),fill=(255,120,40) if i%2 else (200,60,20))

# ---- the 3x5 alien glyphs (the Predator's numerals) ------------------------------------------
AG=["100110111110100","001011111011001","111000111000111","101101111000010",
    "010111010111010","100010001010100","111101010101111","001010100010001"]
def glyph(d,x,y,g,c,sc=1):
    for j,b in enumerate(g):
        if b=='1': d.rectangle([x+(j%3)*sc,y+(j//3)*sc,x+(j%3)*sc+sc-1,y+(j//3)*sc+sc-1],fill=c)

# ---- close-up 1: THERMAL vision --------------------------------------------------------------
HEAT={'O':235,'o':212,'K':150,'3':196,'q':170,'1':150,'2':138,'4':80}
_LUT=[(0,(0,0,40)),(50,(10,20,150)),(95,(0,160,200)),(135,(40,210,70)),(175,(240,230,20)),
      (215,(255,90,10)),(255,(255,255,230))]
def _thermal_rgb(v):
    for (a,ca),(b,cb) in zip(_LUT,_LUT[1:]):
        if v<=b: return _mix(ca,cb,(v-a)/(b-a))
    return _LUT[-1][1]
_TH=[_thermal_rgb(v) for v in range(256)]
def _thermal(L):
    """Map a heat image (L) to the blue -> green -> yellow -> red palette."""
    return Image.merge('RGB',[L.point([c[i] for c in _TH]) for i in range(3)])

def closeup_thermal(t,f,mud=False):
    """Primer plano through the hunter's eyes: the jungle cold blue, Claude burning bright, the
    triangle of red dots locking on his head. mud=True: Claude is as cold as the trees, the reticle
    wanders and loses him."""
    L=Image.new('L',(W,H),30); d=ImageDraw.Draw(L); rr=random.Random(7)
    for i in range(40):                                              # cold foliage + trunks
        x=rr.randint(0,W); y=rr.randint(0,H); r=rr.randint(4,10); d.ellipse([x-r,y-r//2,x+r,y+r//2],fill=rr.randint(36,52))
    for x in (12,150,176): d.rectangle([x-5,0,x+5,H],fill=20)
    spr=CM[guard_pose(f)]; sc=5; ox=76-len(spr[0])*sc//2; oy=H-len(spr)*sc
    for y,row in enumerate(spr):
        for x,ch in enumerate(row):
            if ch=='.': continue
            v=HEAT.get(ch,120)
            if mud: v=20 if ch!='K' else 40
            d.rectangle([ox+x*sc,oy+y*sc,ox+x*sc+sc-1,oy+y*sc+sc-1],fill=v)
    L=L.filter(ImageFilter.GaussianBlur(1.6 if not mud else 3))
    im=_thermal(L); d=ImageDraw.Draw(im)
    px=im.load()
    for y in range(0,H,3):                                           # scan lines
        for x in range(W): blend(px,x,y,(0,0,30),0.35)
    ky=next(y for y,r in enumerate(spr) if 'K' in r); kx=spr[ky].index('K')
    hx,hy=ox+kx*sc+6,oy+ky*sc+2
    if not mud:
        lock=ease(t/0.45); x=lerp(160,hx,lock); y=lerp(52,hy,lock); r=int(lerp(16,7,ease((t-0.4)/0.25)))
    else:
        x=hx+math.sin(f*0.35)*34+14; y=26+math.cos(f*0.5)*12; r=12
    red=(255,40,24) if not mud or (f//3)%2 else (150,20,14)
    tri=[(x,y-r),(x-r*0.87,y+r/2),(x+r*0.87,y+r/2)]
    d.polygon(tri,outline=(200,20,16))
    for (px_,py_) in tri: d.rectangle([px_-1,py_-1,px_+1,py_+1],fill=red)
    for i in range(6):                                               # alien readout, right edge
        g=AG[(i*3+f//4)%len(AG)] if not mud else AG[(i+f//2)%len(AG)]
        glyph(d,172,3+i*7,g,(255,40,24) if i%2 or not mud else (120,20,14))
    if not mud and t>0.55 and (f//3)%2: glyph(d,int(x)+r+3,int(y)-6,AG[0],(255,60,40),2)
    if mud and (f//4)%2: text(d,"?",int(x)-1,int(y)-2,(255,60,40),shadow=None)
    if t<0.08: zoom_lines(d,(255,120,90))
    return im

# ---- close-up 2: the mask comes off --------------------------------------------------------------
SKIN=(146,146,84); SKIN_D=(98,100,56)
def _dreads(d,f,sway):
    for i in range(9):
        for side in (-1,1):
            x0=92+side*(20+i*2.2); a=math.sin(2*math.pi*f/12+i)*0.8*sway
            pts=[(x0+side*j*0.25+a*j/12,6+i*2+j) for j in range(0,60,4)]
            d.line(pts,fill=(34,28,20),width=3)
            for j in range(2,len(pts),4): d.point(pts[j],fill=(164,138,70))
def _face(d,o,f):
    """The Yautja face: crested brow, small yellow eyes, four mandibles spread by o (0..1)."""
    d.ellipse([66,2,118,62],fill=SKIN)
    for i in range(5): d.arc([72+i*2,2+i*3,112-i*2,40+i*2],200,340,fill=SKIN_D)           # crest ridges
    rr=random.Random(3)
    for _ in range(26):
        x,y=rr.randint(70,114),rr.randint(6,52); d.point((x,y),fill=(90,92,50))
    d.polygon([(74,26),(90,30),(92,34),(76,32)],fill=SKIN_D); d.polygon([(110,26),(94,30),(92,34),(108,32)],fill=SKIN_D)
    for ex in (82,102): d.ellipse([ex-3,30,ex+3,35],fill=(20,14,8)); d.point((ex,32),fill=(250,190,40)); d.point((ex+1,32),fill=(250,190,40))
    cx,cy=92,50
    d.ellipse([cx-4-10*o,cy-6-6*o,cx+4+10*o,cy+6+8*o],fill=(96,26,34))                  # the mouth
    if o>0.3:
        d.ellipse([cx-3-6*o,cy-3-3*o,cx+3+6*o,cy+3+5*o],fill=(60,12,20))
        for k in range(-3,4): d.point((cx+k*2,cy-4-5*o),fill=(236,230,210))              # teeth
    for sx in (-1,1):
        for up in (True,False):
            # hinged at the mouth corners: closed they fold over the mouth, open they splay outward
            bx,by=cx+sx*9,(cy-5 if up else cy+7)
            tx=lerp(cx+sx*2,cx+sx*24,o); ty=lerp(cy-1 if up else cy+3,cy-12 if up else cy+10,o)
            mx,my=(bx+tx)/2+sx*3*o,(by+ty)/2+(-3 if up else 3)*(1-o)
            d.line([(bx,by),(mx,my),(tx,ty)],fill=(40,34,20),width=6)
            d.line([(bx,by),(mx,my),(tx,ty)],fill=(176,150,104),width=4)
            d.polygon([(tx-1,ty-1),(tx+1,ty+1),(tx-sx*3,ty+(4 if up else -4))],fill=(236,230,210))  # tusk

def _mask(d,dy):
    y=dy
    d.polygon([(68,6+y),(116,6+y),(118,34+y),(108,56+y),(92,62+y),(76,56+y),(66,34+y)],fill=(176,170,150))
    d.polygon([(70,8+y),(92,8+y),(92,60+y),(78,54+y),(68,34+y)],fill=(196,190,170))
    d.line([92,6+y,92,60+y],fill=(130,124,108))
    d.polygon([(74,24+y),(90,30+y),(88,36+y),(74,31+y)],fill=(22,22,26))
    d.polygon([(110,24+y),(94,30+y),(96,36+y),(110,31+y)],fill=(22,22,26))
    d.point((78,27+y),fill=(120,150,160)); d.point((106,27+y),fill=(120,150,160))
    for x0 in (80,104): d.line([x0,44+y,x0+(4 if x0<92 else -4),52+y],fill=(130,124,108))
def _hands(d,dy,spread):
    for sx in (-1,1):
        x=92+sx*(28+spread); y=34+dy
        d.polygon([(x,y-10),(x+sx*14,y-6),(x+sx*18,y+30),(x+sx*2,y+30)],fill=SKIN)
        for k in range(4): d.line([x,y-8+k*5,x+sx*14,y-4+k*5],fill=(78,80,46))   # the net
        d.rectangle([min(x+sx*2,x+sx*18),y+18,max(x+sx*2,x+sx*18),y+26],fill=(118,96,60))  # bracers
        for k in range(3): d.polygon([(x,y-8+k*6),(x-sx*6,y-6+k*6),(x,y-4+k*6)],fill=(24,20,14))  # claws

def closeup_unmask(t,f):
    im=Image.new('RGB',(W,H),(6,14,10)); d=ImageDraw.Draw(im)
    _dreads(d,f,1.0)
    o=0 if t<0.62 else ease((t-0.62)/0.12)*(0.9+0.1*math.sin(f*1.7))
    lift=0 if t<0.4 else ease((t-0.4)/0.18)*72
    _face(d,o,f)
    if lift<70: _mask(d,lift)
    if 0.12<t<0.6: _hands(d,lift,int(lerp(14,0,ease((t-0.12)/0.14))))
    if 0.3<=t<0.46:                                                  # the hoses pop: steam
        rr=random.Random(f)
        for sx in (-1,1):
            for _ in range(10):
                u=rr.random(); x=92+sx*(26+u*22); y=30-u*18+rr.uniform(-3,3)
                d.ellipse([x-2,y-2,x+2,y+2],fill=(200,210,206) if rr.random()<0.6 else (140,150,146))
    if t>=0.64:
        big_text(im,"RAAARGH!",4,(255,200,60),outline=(120,30,10))
    if t<0.06: zoom_lines(d)
    if t>=0.62:
        dx,dy=rshake(1); im2=Image.new('RGB',(W,H),(6,14,10)); im2.paste(im,(dx,dy)); im=im2
    return im

# ---- close-up 3: the wrist bomb --------------------------------------------------------------------
def closeup_bomb(t,f):
    im=Image.new('RGB',(W,H),(6,12,8)); d=ImageDraw.Draw(im)
    d.polygon([(0,20),(W,14),(W,52),(0,58)],fill=SKIN)                 # the forearm across the frame
    for x in range(-30,W,9): d.line([x,58,x+30,14],fill=(116,118,66))    # net mesh
    for x in range(-30,W,9): d.line([x,14,x+30,58],fill=(116,118,66))
    d.rectangle([54,12,134,58],fill=(118,96,60),outline=(70,56,34))     # the gauntlet
    for x,y in ((58,16),(130,16),(58,54),(130,54)): d.point((x,y),fill=(200,170,110))
    lid=ease(t/0.15)
    glow=0.5+0.5*math.sin(f*(0.6+t*1.4))
    d.rectangle([70,20,118,48],fill=_mix((40,6,6),(110,14,10),glow))
    n=int(t*40); digits=[AG[(n*3+i*5)%len(AG)] for i in range(3)]
    if t<0.18: digits=[AG[i] for i in (0,3,6)]
    for i,g in enumerate(digits): glyph(d,76+i*14,24,g,(255,60,40),3)
    if lid<1: d.rectangle([70,20,118,20+int(28*(1-lid))],fill=(96,78,48),outline=(70,56,34))
    if 0.18<t<0.44:                                                   # a claw punches the keys
        press=abs(math.sin((t-0.18)*40)); y=-8+press*16
        d.polygon([(96,y-20),(108,y-20),(106,y+4),(98,y+4)],fill=SKIN)
        d.polygon([(98,y+4),(106,y+4),(102,y+10)],fill=(24,20,14))
    for i in range(5): d.rectangle([124,22+i*5,128,24+i*5],fill=(255,50,30) if (i+f//2)%5==0 else (80,20,14))
    if t>0.45:
        big_text(im,"HAHAHA",2 if (f//2)%2 else 3,(255,70,50),outline=(60,6,4))
    if t<0.06: zoom_lines(d)
    return im

# ---- the clip ---------------------------------------------------------------------------------------
PX=150         # the cloaked hunter's post in the trees (loop keyframe)
DX=122         # where he decloaks
LX=74          # the deadfall
# laser dots: down the tree trunk, across the ferns, up onto Claude's chest, then his forehead
DOT_PATH=[(24,(140,20)),(34,(138,50)),(44,(60,55)),(50,(40,55)),(56,(34,53)),(64,(33,49))]
def dot_pos(f):
    if f<=DOT_PATH[0][0]: return DOT_PATH[0][1]
    for (a,pa),(b,pb) in zip(DOT_PATH,DOT_PATH[1:]):
        if f<=b: u=ease((f-a)/(b-a)); return lerp(pa[0],pb[0],u),lerp(pa[1],pb[1],u)
    return DOT_PATH[-1][1]

def clip_hunt(f):
    s=scene(f,THEME); s['under'].append(('pred_flies',))
    cl=actor(CM[guard_pose(f)],30,pal=CPAL); pr=actor(y_idle(f),PX,flip=True,pal=YPAL,vis=False)
    cloaked=(PX,1.0)           # (x, strength) of the shimmer, None when visible or gone
    mud=0.0
    # 1) the laser dots crawl in (24-84); the shimmer slides between the trunks (60-84)
    if 24<=f<84:
        x,y=dot_pos(f); jit=(f%5==0)
        s['fx'].append(('pred_dots',x+(1 if jit else 0),y))
        if 56<=f<74 and (f//3)%2: s['fx'].append(('dmg',"!",31,38,(255,255,255)))
    if 60<=f<84: cloaked=(ez(PX,DX,(f-60)/22),1.0)
    if 84<=f<168: cloaked=(DX,1.0)
    # 2) primer plano: THERMAL vision
    if 84<=f<132: s['image']=closeup_thermal((f-84)/48,f); return s
    # 3) Claude smears himself with mud and goes cold
    if 132<=f<168:
        mud=ease((f-136)/14)
        if f<152: cl['spr']=CM['armsup'] if (f//3)%2 else CM['guard2']
        if f<150 and f%2==0:
            for k in range(3):
                u=((f+k*5)%8)/8; s['fx'].append(('pred_mud',22+k*6+u*2,GROUND-1-u*12,))
        if f<146: s['fx'].append(('pred_dots',33,49))
        else:
            u=(f-146)/10; s['fx'].append(('pred_dots',33+math.sin(u*5)*30+u*30,46-u*6+math.cos(u*7)*6))
    if 156<=f<168: s['image']=closeup_thermal((f-156)/12,f,mud=True); return s
    if f>=136: mud=max(mud,ease((f-136)/14))
    if f>=302: mud=0
    # 4) he decloaks in blue sparks (168-192)
    if 168<=f<192:
        p=ease((f-174)/12); cloaked=(DX,1-p) if p<1 else None
        pr.update(vis=p>0,x=DX,alpha=p)
        if 170<=f<190: s['fx'].append(('pred_zap',pr['spr'],DX,GROUND,True,6 if f<186 else 2))
    # 5) primer plano: the mask comes off, the roar (192-228)
    if 192<=f<228: s['image']=closeup_unmask((f-192)/36,f); return s
    # 6) the brawl (228-258)
    if 228<=f<258:
        cloaked=None; pr.update(vis=True,pal=UNMASK)
        if f<238: pr.update(x=ez(DX,56,(f-228)/10),y=GROUND-((f//2)%2))
        elif f<246:
            pr.update(x=56,spr=YA['attack'] if f<243 else YA['idle'])
            if f==240: s['fx'].append(('arc',44,46,8,150,260,(230,236,246),1))
            if 240<=f<246: cl.update(spr=CM['hurt'],x=ez(30,24,(f-240)/4))
            if f==240: s['shake']=rshake(1); s['fx'].append(('spark',38,46,4))
        else:
            cl['x']=24
            if 247<=f<251: cl.update(spr=CM['punch'],x=ez(24,34,(f-247)/2)); pr['x']=ez(56,64,(f-248)/3)
            elif 251<=f<256: cl.update(spr=CM['punch'],x=ez(28,38,(f-251)/2)); pr['x']=ez(64,LX,(f-252)/3)
            else: cl.update(x=ez(38,26,(f-256)/2))
            if f in (248,252): s['fx'].append(('spark',int(pr['x'])-6,40,5)); s['shake']=rshake(1)
            if 248<=f<251 or 252<=f<256: pr['spr']=YA['hurt']
            elif f>=256: pr.update(x=LX,spr=YA['idle'])
    # 7) the log trap (258-270)
    if 258<=f<302:
        cloaked=None; pr.update(vis=True,x=LX,pal=UNMASK)
    if 258<=f<270:
        cl.update(spr=CM['armsup'],x=26,y=GROUND-(1 if f<262 else 0))
        lx,ly=cell_at(CM['armsup'],26,GROUND,False,'o')
        ytop=ez(-8,GROUND-26,(f-260)/4) if f>=260 else -8
        s['fx'].append(('pred_rope',[(lx,ly),(46,4),(LX,4),(LX,int(ytop)-3)] if f<264 else [(lx,ly),(46,4)]))
        s['fx'].append(('pred_log',LX,ytop if f<264 else min(GROUND-4,GROUND-26+(f-264)*6)))
        if f<264: pr['spr']=y_idle(f)
        else: pr['spr']=YA['hurt'] if f<266 else YA['down']
        if f==264: s['shake']=rshake(2); s['fx']+=[('spark',LX,GROUND-26,6),('dmg',"THUD",LX-7,20,(255,230,150))]
    # 8) the wrist bomb: close-up (270-288), then he laughs while Claude runs (288-302)
    if 270<=f<288: s['image']=closeup_bomb((f-270)/18,f); return s
    if 266<=f<302:
        pr['spr']=YA['down']
        if f>=270: s['fx'].append(('pred_log',LX+4,GROUND-4))
        w=cell_at(YA['down'],LX,GROUND,True,'w')
        if w and f>=288: s['fx'].append(('pred_blink',w[0],w[1],max(1,4-(f-288)//4)))
        if f>=288: s['fx'].append(('big',"HAHAHA",4,(255,70,50)))
    if 288<=f<302:
        cl.update(spr=CM['dash'],flip=True,x=ez(30,-22,(f-290)/10) if f>=290 else 30)
    # 9) the mushroom flash (302-326), then the jungle again, a new shimmer in the trees (326-348)
    if f>=302:
        pr['vis']=False; cloaked=None; cl['vis']=False
        if f<328: s['fx'].append(('pred_nuke',LX,f-302))
        if f>=316: s['under'].append(('pred_smolder',LX,max(0,1-(f-316)/22)))
        if f>=322:
            cloaked=(PX,ease((f-324)/14))
            cl.update(vis=True,flip=False,x=ez(-12,30,(f-322)/16),spr=CM['guard' if (f//3)%2 else 'guard2'])
            if f>=338: cl['spr']=CM[guard_pose(f)]
        if f<312: s['flash']=max(0,1-(f-302)/10); s['fc']=(LX,40); s['flashc']=(255,240,200)
        if 302<=f<314: s['shake']=rshake(2 if f<308 else 1)
    cl['pal']=cpal(mud)
    if cloaked and cloaked[1]>0: s['under'].append(('pred_cloak',y_idle(f),cloaked[0],GROUND,True,cloaked[1]))
    s['actors']=[pr,cl]
    return s

CLIPS = [clip('hunt', N_, clip_hunt)]
