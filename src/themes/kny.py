"""Kimetsu no Yaiba: Claude (Tanjiro: checkered haori, hanafuda earrings) vs Akaza, Upper Moon Three,
on the roof of the Mugen Train racing through a moonlit forest. Akaza opens his kanji eyes and lays
down the Compass Needle, a punch barrage drives Claude back — close-up: WATER BREATHING, TENTH FORM,
CONSTANT FLUX, the ukiyo-e water dragon rides the slash into him. Akaza answers with DESTRUCTIVE
DEATH: DISORDER and floors Claude — close-up: HINOKAMI KAGURA, the eyes and the scar catch fire.
A flaming leap, one cut through the neck: the head flies and the demon crumbles to ash on the wind.
Claude hops back, and another Akaza drops onto the roof."""
from engine import *
from PIL import ImageChops

THEME = 'kny'
N_ = 336
CX, EX = 30, 150                                                    # the loop keyframe positions

# ---- local glyphs: a wider M and W (the 3x5 font's read as H) ------------------------------------
_GLYPH = {'M':(5,"10001"+"11011"+"10101"+"10001"+"10001"), 'W':(5,"10001"+"10001"+"10101"+"11011"+"10001")}

def _mask(txt):
    gl=[_GLYPH.get(ch) or (3,''.join(FONT.get(ch,FONT[' '])[j*3:j*3+3] for j in range(5))) for ch in txt]
    m=Image.new('L',(sum(w+1 for w,_ in gl)-1,5),0); md=ImageDraw.Draw(m); x=0
    for w,bits in gl:
        for j,b in enumerate(bits):
            if b=='1': md.point((x+j%w,j//w),fill=255)
        x+=w+1
    return m

def say(im,txt,y,c,scale=1,cx=W//2,outline=None,shadow=(0,0,0)):
    """Like big_text, with the local glyphs; scale=1 gives a normal callout."""
    m=_mask(txt); m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        if shadow is not None: im.paste(shadow,(x+2,y+2),m)
    elif shadow is not None: im.paste(shadow,(x+1,y+1),m)
    im.paste(c,(x,y),m)

@fx('kny_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,cx=W//2,outline=None):
    s['fx'].append(('kny_say',txt,y,c,scale,cx,outline))

# ---- Claude as Tanjiro: dark-red hair, hanafuda earring, green/black checkered haori --------------
def _tanjiro(spr):
    spr=overlay(spr,["..RR.RR.R.",".RRRRRRRRR"],-1,0)
    def rows(x,y,t,l,r,c):
        if t+5<=y<=t+8 and c in 'Oo' and l<=x<=r: return 'X' if (x+y)%2 else 'Z'
        if x==l-1 and y in (t+2,t+3) and c=='.': return 'H' if y==t+2 else 'r'   # the earring
        return None
    return recolor_rows(spr,rows)
TANJ={k:_tanjiro(v) for k,v in CL.items()}

# ---- Akaza: pink hair, blue tattoo lines, the head comes off for the finish ------------------------
AKAZA=poses(S([
".....nnnn.......","....nnnnnn......","...nnPPPPn......","....PLyPyL......","....PPPPPP......",".....PLLP.......",
"...NNPLLPNN.....","..NNNPPPPNNN....","..PLNPLLPNLP....","..PL.PPPP.LP....","..PP.PLLP.PP....","..LP.PPPP.PL....",
".....WWWW.......",".....WWWW.......","....WW..WW......","....WW..WW......","....WW..WW......","....LP..PL......",
"....PP..PP......","...PPP..PPP.....",]),8,'PL',4)
AK_HEADLESS=S(['.'*16]*6+AKAZA['idle'][6:])
AK_HEAD=rotate90(rotate90(S(AKAZA['idle'][:6]),1,trim=True),3)

# ---- background: the Mugen Train roof under the full moon -----------------------------------------
def _train(d):
    for y in range(GROUND):                                         # night sky, indigo to moonlit haze
        k=y/(GROUND-1); d.line([0,y,W,y],fill=(int(10+30*k),int(14+38*k),int(40+56*k)))
    rr=random.Random(2024)
    for _ in range(34):
        x,y=rr.randint(0,W-1),rr.randint(0,30); d.point((x,y),fill=rr.choice([(200,210,240),(140,150,200),(255,255,255)]))
    mx,my=148,13                                                    # the full moon with its halo
    for r,c in ((15,(34,44,86)),(12,(52,64,112)),(10,(90,98,140))): d.ellipse([mx-r,my-r,mx+r,my+r],fill=c)
    d.ellipse([mx-8,my-8,mx+8,my+8],fill=(244,238,208)); d.ellipse([mx-4,my-5,mx,my-1],fill=(222,214,184))
    d.ellipse([mx+2,my+1,mx+5,my+4],fill=(226,218,188))
    d.polygon([(0,40),(16,30),(28,34),(44,24),(62,33),(80,28),(104,36),(126,26),(146,34),(166,28),(185,33),(185,46),(0,46)],fill=(30,40,70))
    d.polygon([(0,44),(22,37),(40,41),(70,35),(96,42),(120,37),(150,42),(172,36),(185,40),(185,50),(0,50)],fill=(22,30,54))
    # the carriage: curved roof, walkway plates, green side with lit windows
    d.rectangle([0,GROUND,W,H],fill=(34,34,40))
    d.line([0,GROUND,W,GROUND],fill=(120,124,140)); d.line([0,GROUND+1,W,GROUND+1],fill=(70,72,84))
    for x in range(6,W,16): d.line([x,GROUND+1,x+5,GROUND+1],fill=(96,98,112))
    d.rectangle([0,GROUND+3,W,H],fill=(22,54,40)); d.line([0,GROUND+3,W,GROUND+3],fill=(186,150,70))
    for x in range(4,W,12): d.rectangle([x,GROUND+4,x+6,GROUND+5],fill=(250,214,120))
    for x in (60,124): d.rectangle([x,GROUND,x+1,H],fill=(10,10,14))   # carriage joints
register_bg(THEME, lambda v: (v+30,v+30,v+40), decor=_train)

# ---- scenery rushing past (every layer laps a whole number of times per clip: a seamless loop) ----
PINES=[(0,14),(13,20),(22,11),(38,17),(49,23),(63,13),(77,19),(88,15),(104,22),(117,12),(129,18),(146,21),
       (158,13),(171,17),(186,24),(199,14),(211,19)]
@fx('kny_scenery')
def _fx_scenery(d,im,e,f):
    """Pine forest (2px/frame, period 224) and telegraph poles (4px/frame) scrolling left."""
    o=(f*2)%224
    for x0,h in PINES:
        x=(x0-o)%224-20
        for k in range(h//3):                                       # stacked tiers of a pine
            w=2+k*2; y=GROUND-h+k*3
            d.polygon([(x,y),(x-w,y+4),(x+w,y+4)],fill=(14,24,26))
        d.line([x-1,GROUND-h+1,x-(h//3)*2+1,GROUND-h+(h//3)*3+1],fill=(62,84,100))   # moonlit edge
        d.rectangle([x-1,GROUND-3,x,GROUND-1],fill=(18,14,14))
    o2=(f*4)%224
    for x0 in (30,142):
        x=(x0-o2)%224-20
        d.rectangle([x,14,x+1,GROUND-1],fill=(10,10,14)); d.line([x-4,17,x+5,17],fill=(10,10,14))
        d.point((x-4,16),fill=(120,120,130)); d.point((x+5,16),fill=(120,120,130))
    for yy in (16,19): d.line([0,yy+1,W,yy+1],fill=(26,30,46))       # the wires

@fx('kny_steam')
def _fx_steam(d,im,e,f):
    """Locomotive smoke puffs drifting back over the roof (4/3 px per frame, period 224)."""
    o=(f*4)//3
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for i,(x0,y,r) in enumerate(((10,6,7),(50,10,6),(96,4,8),(140,9,5),(186,5,7))):
        x=(x0-o)%224-20
        for dx,dy,k in ((0,0,1.0),(6,2,0.7),(-5,3,0.6)): md.ellipse([x+dx-r*k,y+dy-r*k*0.7,x+dx+r*k,y+dy+r*k*0.7],fill=70)
    im.paste((150,150,170),(0,0),m)

@fx('kny_wind')
def _fx_wind(d,im,e,f):
    rr=random.Random((f%N_)*5)
    for _ in range(4):
        y=rr.randint(20,GROUND-3); x=rr.randint(0,W-10); d.line([x,y,x+rr.randint(6,14),y],fill=(90,104,140))

# ---- effects -----------------------------------------------------------------------------------
@fx('katana')
def _fx_katana(d,im,e,f):
    _,x0,y0,x1,y1,glow=e
    if glow: d.line([x0,y0,x1,y1],fill=glow,width=3)
    d.line([x0,y0,x1,y1],fill=(222,224,238))
    d.line([x0,y0,x0+(x1-x0)*0.18,y0+(y1-y0)*0.18],fill=(40,30,30),width=2)

def katana_for(pose,x,y,flip,glow=None):
    s=-1 if flip else 1
    if pose in ('guard','guard2'): return ('katana',x+5*s,y-6,x+11*s,y-16,glow)
    if pose=='hurt': return ('katana',x+4*s,y-8,x-3*s,y-14,glow)
    if pose=='armsup': return ('katana',x,y-11,x-2*s,y-24,glow)
    return ('katana',x+8*s,y-5,x+20*s,y-7,glow)

@fx('kny_compass')
def _fx_compass(d,im,e,f):
    """Akaza's Compass Needle: a snowflake of light spreading on the roof."""
    _,x,r,a=e
    c=tuple(int(40+(v-40)*a) for v in (140,230,255))
    for i in range(12):
        ang=i/12*6.283; L=r if i%2==0 else r*0.6
        ex,ey=x+math.cos(ang)*L,GROUND+math.sin(ang)*L*0.25
        d.line([x,GROUND,ex,ey],fill=c)
        if i%2==0: d.point((int(x+math.cos(ang)*L*0.7),int(GROUND+math.sin(ang)*L*0.18)-1),fill=(255,255,255))
    d.ellipse([x-r,GROUND-r*0.25,x+r,GROUND+r*0.25],outline=c)

@fx('kny_shock')
def _fx_shock(d,im,e,f):
    """An air-type punch shockwave flying left: a fist-sized crescent with a white core."""
    _,x,y,r=e
    d.arc([x-r,y-r,x+r,y+r],110,250,fill=(140,220,255),width=2); d.arc([x-r+2,y-r+1,x+r-2,y+r-1],120,240,fill=(255,255,255))

@fx('kny_dragon')
def _fx_dragon(d,im,e,f):
    """The water dragon: a scaled blue body snaking from the tail x0 to the head at hx."""
    _,x0,hx,yb,amp=e
    pts=[]
    n=max(2,int((hx-x0)/2))
    for i in range(n+1):
        x=x0+(hx-x0)*i/n; y=yb+amp*math.sin(x*0.09-f*0.6)*(i/n)**0.5
        pts.append((x,y))
    for i,(x,y) in enumerate(pts):                                  # tail thin, neck thick
        r=1+int(3.5*(i/len(pts))**0.7)
        d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=(30,80,180))
    for i,(x,y) in enumerate(pts):
        r=1+int(3.5*(i/len(pts))**0.7)
        d.ellipse([x-r,y-r,x+r,y+r],fill=(70,150,240))
        if i%3==0: d.point((int(x),int(y-r+1)),fill=(200,236,255))
        if i%4==2 and r>2: d.point((int(x),int(y+r-1)),fill=(240,250,255))
    x,y=pts[-1]                                                     # head: snout, jaw, horns, eye
    d.polygon([(x-3,y-5),(x+7,y-3),(x+9,y),(x+2,y+1)],fill=(90,170,250),outline=(30,80,180))
    d.polygon([(x-2,y+1),(x+7,y+2),(x+1,y+5)],fill=(60,130,220),outline=(30,80,180))
    d.line([x-2,y-5,x-7,y-10],fill=(220,240,255)); d.line([x+1,y-5,x-2,y-11],fill=(220,240,255))
    d.point((x+3,y-3),fill=(255,255,255)); d.point((x+4,y-3),fill=(20,30,60))
    d.line([x+8,y+1,x+13,y+5],fill=(200,236,255)); d.line([x+8,y-1,x+13,y-4],fill=(200,236,255))
    rr=random.Random(f)
    for _ in range(8):                                              # spray off the body
        px,py=rr.choice(pts); d.point((int(px+rr.randint(-6,6)),int(py+rr.randint(-7,7))),fill=(210,240,255))

@fx('kny_warc')
def _fx_warc(d,im,e,f):
    """A water slash: layered blue crescent with foam curls at the tips."""
    _,x,y,r,a0,a1=e
    d.arc([x-r-1,y-r-1,x+r+1,y+r+1],a0,a1,fill=(30,80,180),width=4)
    d.arc([x-r,y-r,x+r,y+r],a0,a1,fill=(80,160,245),width=3)
    d.arc([x-r+1,y-r+1,x+r-1,y+r-1],a0,a1,fill=(230,246,255),width=1)
    for a in (a0,a1):
        cx,cy=x+math.cos(math.radians(a))*r,y+math.sin(math.radians(a))*r
        d.arc([cx-3,cy-3,cx+3,cy+3],0,270,fill=(230,246,255))

@fx('kny_farc')
def _fx_farc(d,im,e,f):
    """A Hinokami Kagura slash: a flame crescent (ry: flattened) with licking tongues and embers."""
    _,x,y,r,a0,a1,*ry=e; ry=ry[0] if ry else r
    box=lambda k: [x-r-k,y-ry-k,x+r+k,y+ry+k]
    d.arc(box(1),a0,a1,fill=(200,40,20),width=5 if ry>6 else 3)
    d.arc(box(0),a0,a1,fill=(255,130,30),width=3 if ry>6 else 2)
    d.arc(box(-1),a0,a1,fill=(255,240,160),width=1)
    rr=random.Random(f*3+int(x))
    for _ in range(10):
        a=math.radians(rr.uniform(a0,a1)); k=rr.randint(1,5)
        px,py=x+math.cos(a)*(r+k),y+math.sin(a)*(ry+k*ry/r)
        d.line([px,py,px+rr.randint(-1,1),py-rr.randint(1,4)],fill=rr.choice([(255,190,60),(255,110,30),(255,240,160)]))

@fx('kny_ember')
def _fx_ember(d,im,e,f):
    _,x,y=e; d.point((int(x),int(y)),fill=random.choice([(255,140,40),(255,210,80),(230,70,30)]))

@fx('kny_splash')
def _fx_splash(d,im,e,f):
    """Water droplets bursting out from x,y (t 0..1), falling back."""
    _,x,y,t=e; rr=random.Random(77)
    for _ in range(22):
        vx=rr.uniform(-2.5,2.5); vy=rr.uniform(-3,-0.5); k=t*12
        px,py=x+vx*k,y+vy*k+0.25*k*k
        if py<GROUND: d.point((int(px),int(py)),fill=rr.choice([(120,190,255),(230,246,255),(70,150,240)]))

def _pixels(spr,cx,feet,flip):
    m,w,h=mask_of(spr,flip); ox,oy=origin(spr,cx,feet)
    return [(ox+x,oy+y,ch) for (x,y),ch in m.items()],h,oy

@fx('kny_crumble')
def _fx_crumble(d,im,e,f):
    """A demon turning to ash from the top down, blown back along the train (t 0..1)."""
    _,spr,cx,feet,flip,t=e
    pix,h,oy=_pixels(spr,cx,feet,flip); rr=random.Random(33)
    keep=[]
    for (x,y,ch) in pix:
        delay=(y-oy)/h*0.55+rr.random()*0.25; vx=rr.uniform(1.2,2.6); vy=rr.uniform(-0.8,0.2); ph=rr.random()*6.28
        if t<delay: keep.append((x,y,ch)); continue
        age=(t-delay)*40
        if age>22: continue
        px=x-vx*age-0.04*age*age; py=y+vy*age+math.sin(ph+age*0.4)*1.5
        c=(255,150,60) if age<3 else ((140,120,120) if age<12 else (80,70,76))
        d.point((int(px),int(py)),fill=c)
    if keep:
        g=[['.']*len(spr[0]) for _ in spr]
        ox,_=origin(spr,cx,feet); w=len(spr[0])
        for x,y,ch in keep:
            gx=x-ox; g[y-oy][(w-1-gx) if flip else gx]=ch
        draw(im,S([''.join(r) for r in g]),cx,feet,flip,f=f)
        for x,y,ch in keep:                                         # glowing cracks where it breaks
            if rr.random()<0.12: d.point((x,y),fill=(255,170,80))

# ---- close-ups ---------------------------------------------------------------------------------
_KANJI={'up':["...#...","...#...","...###.","...#...","...#...","...#...","#######"],
        'three':["...#...","..#..#.",".#####.","...#...","#######","..#.#..",".#.#.#.","#..#..#","..#...."]}

def closeup_akaza(t,f):
    """Primer plano: Upper Moon Three opens his eyes — the kanji carved into the irises."""
    im=Image.new('RGB',(W,H),(232,206,196)); d=ImageDraw.Draw(im)
    for y0 in (4,40):                                               # the blue tattoo lines across the face
        for k in range(3): d.line([0,y0+k*3,W,y0+k*3+4],fill=(60,90,220))
    for i in range(0,W,14): d.polygon([(i,0),(i+16,0),(i+8,10+(i//14)%3*2)],fill=(240,120,170))   # fringe
    d.rectangle([0,0,W,3],fill=(240,120,170))
    op=ease(min(1,t/0.25))
    jx=((f%3)-1) if 0.2<t<0.32 else 0
    for n,ex in enumerate((52,133)):
        ex+=jx; hh=int(12*op)
        d.polygon([(ex-26,26),(ex,26-hh-2),(ex+26,26),(ex,26+hh+2)],fill=(20,14,24))      # lashes
        if hh>0:
            d.polygon([(ex-23,26),(ex,26-hh),(ex+23,26),(ex,26+hh)],fill=(150,210,240))  # sclera
            m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon([(ex-23,26),(ex,26-hh),(ex+23,26),(ex,26+hh)],fill=255)
            ir=Image.new('RGB',(W,H),(0,0,0)); di=ImageDraw.Draw(ir)
            di.ellipse([ex-11,15,ex+11,37],fill=(90,60,20)); di.ellipse([ex-10,16,ex+10,36],fill=(250,206,60))
            di.ellipse([ex-6,20,ex+6,32],fill=(255,236,140))
            km=_KANJI['up' if n==0 else 'three']; ky=26-len(km)//2
            for j,row in enumerate(km):
                for i,ch in enumerate(row):
                    if ch=='#': di.point((ex-3+i,ky+j),fill=(40,20,40))
            di.point((ex+6,19),fill=(255,255,255)); di.point((ex+7,20),fill=(255,255,255))
            im2=Image.new('L',(W,H),0); ImageDraw.Draw(im2).ellipse([ex-11,15,ex+11,37],fill=255)
            im.paste(ir,(0,0),ImageChops.multiply(m,im2))
            d=ImageDraw.Draw(im)
        d.line([ex-28,10,ex+20,6] if n==0 else [ex-20,6,ex+28,10],fill=(150,60,90),width=2)   # brows
    if t<0.08: zoom_lines(d,(255,255,255))
    if t>=0.3:
        d.rectangle([0,45,W,H],fill=(16,10,20))
        jj=(f%3)-1 if t<0.4 else 0
        say(im,"UPPER MOON THREE",49,(236,90,150),scale=2,cx=W//2+jj,outline=(60,20,50))
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

def _tanjiro_face(im,d,fire,f,breath):
    """Claude's face, zoomed: burgundy hair, the scar, hanafuda earrings, checkered collar."""
    hair,edge=((150,40,30),(255,150,60)) if fire else ((96,28,28),(150,60,50))
    for x0,x1,tx,ty in ((8,24,6,4),(18,36,26,0),(30,50,42,2),(44,62,58,0),(56,74,76,6),(66,78,84,16)):
        d.polygon([(x0,24),(x1,24),(tx,ty)],fill=hair,outline=edge)
    d.rectangle([10,16,74,24],fill=hair)
    d.rectangle([12,22,72,64],fill=(217,119,87)); d.rectangle([12,22,17,64],fill=(176,92,66))
    for x0,x1,tx in ((16,28,20),(30,42,34),(48,60,54)): d.polygon([(x0,21),(x1,21),(tx,31)],fill=hair)
    if fire:                                                        # the scar flares into a flame mark
        d.polygon([(56,24),(66,24),(68,34),(62,30),(58,35),(55,29)],fill=(255,110,30),outline=(200,40,20))
        d.line([61,25,62,30],fill=(255,230,140))
    else: d.polygon([(57,24),(65,24),(66,31),(60,29),(56,31)],fill=(160,50,40))
    for ex in (30,54):
        d.rectangle([ex-3,36,ex+3,48],fill=(24,14,12))
        d.rectangle([ex-2,38,ex+2,47],fill=(255,140,40) if fire else (150,40,40))
        d.rectangle([ex-1,39,ex,41],fill=(255,250,220))
        if fire and f%2: d.line([ex-3,35,ex+3,33],fill=(255,200,80))
    d.line([24,33,34,34],fill=(60,20,20)); d.line([50,34,60,33],fill=(60,20,20))
    if breath: d.ellipse([39,53,46,58],fill=(40,14,12))             # breathing through the mouth
    else: d.line([38,55,47,55],fill=(110,44,32))
    for x in (6,74):                                                # the hanafuda earrings
        d.line([x+3,42,x+3,45],fill=(40,30,30))
        d.rectangle([x,45,x+6,56],fill=(244,240,228),outline=(40,30,30))
        d.ellipse([x+1,46,x+5,50],fill=(214,40,40)); d.line([x+1,53,x+5,53],fill=(40,30,30)); d.line([x+1,55,x+5,55],fill=(40,30,30))
    for x in range(0,90,4):                                         # the checkered haori collar
        for y in (57,60,63):
            d.rectangle([x,y,x+3,y+2],fill=(40,150,95) if (x//4+y//3)%2 else (22,22,26))

def closeup_water(t,f):
    """Primer plano: WATER BREATHING, TENTH FORM: CONSTANT FLUX — the ukiyo-e water dragon coils past."""
    im=Image.new('RGB',(W,H),(14,34,84)); d=ImageDraw.Draw(im)
    for k,yb in enumerate((40,50,58)):                              # Hokusai waves with foam claws
        for x in range(-16,W+16,22):
            xx=x+((f*(k+1))%22)*(1 if k%2 else -1); c=[(30,70,150),(40,100,190),(60,130,220)][k]
            d.pieslice([xx-12,yb-10,xx+12,yb+10],180,360,fill=c)
            d.arc([xx-12,yb-10,xx+12,yb+10],200,300,fill=(230,246,255))
            d.arc([xx+4,yb-10,xx+12,yb-3],90,300,fill=(230,246,255))
    hx=lerp(-30,230,t)
    _fx_dragon(d,im,('',hx-220,hx,24,12),f)
    breath=t<0.5
    _tanjiro_face(im,d,False,f,breath)
    d=ImageDraw.Draw(im)
    if breath:                                                      # the breath: a cold mist
        rr=random.Random(f//2)
        for i in range(10):
            px=48+i*5+rr.randint(0,3); py=56-i*0.6+math.sin(i+f*0.5)*2; d.point((int(px),int(py)),fill=(220,236,255))
        if t<0.35: say(im,"HAAA",46,(200,230,255),scale=1,cx=100)
    if t>=0.12: say(im,"WATER BREATHING",4,(200,230,255),cx=134,outline=(20,40,90))
    if t>=0.28: say(im,"TENTH FORM",13,(200,230,255),cx=134,outline=(20,40,90))
    if t>=0.45:
        jj=(f%3)-1 if t<0.55 else 0
        say(im,"CONSTANT",23,(255,255,255),scale=2,cx=134+jj,outline=(20,60,150))
        say(im,"FLUX",36,(160,220,255),scale=3,cx=134+jj,outline=(20,60,150))
    if t<0.06: zoom_lines(d,(200,230,255))
    if t>0.9: im=fade_to(im,(230,246,255),(t-0.9)/0.1*0.7)
    return im

def closeup_fire(t,f):
    """Primer plano: HINOKAMI KAGURA — the eyes and the scar catch fire."""
    lit=t>=0.3 or (0.22<=t<0.3 and f%2==0)
    im=Image.new('RGB',(W,H),(60,14,8) if lit else (20,10,14)); d=ImageDraw.Draw(im)
    if lit:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([-10,-10,100,80],fill=160)
        im.paste((255,120,30),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
        for x in range(0,W,12): _fx_fire_col(d,x+(f*3)%12,H+2,4+(x*7)%4,f)
    rr=random.Random(f)
    for _ in range(30 if lit else 6):
        d.point((rr.randint(0,W-1),rr.randint(0,H-1)),fill=rr.choice([(255,140,40),(255,210,80),(230,70,30)]))
    _tanjiro_face(im,d,lit,f,not lit)
    if lit and t<0.36:
        im=fade_to(im,(255,230,170),1-(t-0.3)/0.06); d=ImageDraw.Draw(im); zoom_lines(d,(255,200,90))
    if t<0.2: say(im,"KOOO",40,(255,190,120),cx=110)
    if t>=0.4:
        jj=(f%3)-1 if t<0.5 else 0
        say(im,"HINOKAMI",10,(255,236,160),scale=2,cx=136+jj,outline=(140,30,0))
        say(im,"KAGURA",26,(255,255,255),scale=3,cx=136+jj,outline=(140,30,0))
        if t>=0.55: say(im,"SUN BREATHING",50,(255,190,100),cx=136)
    if t<0.06: zoom_lines(d,(255,160,80))
    if t>0.9: im=fade_to(im,(255,200,120),(t-0.9)/0.1*0.7)
    return im

def _fx_fire_col(d,x,feet,sz,f):
    rr=random.Random(f*13+int(x))
    for j in range(int(10+sz*3)):
        up=rr.random()**0.7; yy=feet-up*sz*5; xx=x+rr.uniform(-1,1)*sz*(1-up*0.6); r=max(1,int(sz*(1-up)*0.8+rr.randint(0,2)))
        c=(255,245,170) if up<0.25 else ((255,160,40) if up<0.6 else (220,60,20))
        d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=c)

# ---- the clip ----------------------------------------------------------------------------------
def ghost(spr,x,y=GROUND,flip=False,tint=(170,220,255),a=0.35):
    return actor(spr,x,y,flip=flip,alpha=a,tint=tint)

def clip_breath(f):
    s=scene(f,THEME)
    s['under']+=[('kny_scenery',),('kny_steam',)]
    if f%3==0: s['fx'].append(('kny_wind',))
    cl=actor(TANJ[guard_pose(f)],CX); ak=actor(AKAZA['idle'],EX,flip=True)
    pose='guard'; glow=None; extra=[]; blade=True
    # 1) the stand-off on the roof: MUGEN TRAIN, Akaza lays down the Compass Needle
    if 6<=f<36:
        yy=4 if f>=10 else 4-(10-f)
        shout(s,"MUGEN TRAIN",(255,236,200),y=yy,scale=2,outline=(80,30,40))
    if 18<=f<36:
        s['under'].append(('kny_compass',EX,4+(f-18)*1.2,min(1,(f-18)/6)))
        ak['aura']=((140,220,255),1) if f%4<2 else None
    # 2) close-up: the kanji eyes
    if 36<=f<64: s['image']=closeup_akaza((f-36)/28,f); return s
    # 3) Akaza closes in and hammers: AIR TYPE
    if 64<=f<76:
        t=(f-64)/12; ak.update(x=ez(EX,50,t),spr=AKAZA['attack'])
        extra+=[ghost(AKAZA['attack'],ak['x']+8,flip=True,tint=(255,170,210)),ghost(AKAZA['attack'],ak['x']+16,flip=True,tint=(255,170,210),a=0.2)]
        s['under'].append(('kny_compass',EX,26,max(0,1-(f-64)/6)))
    if 76<=f<100:
        k=f-76; hit=k%4<2
        ak.update(x=50+(0 if hit else 2),spr=AKAZA['attack'] if hit else AKAZA['idle'])
        cl['x']=CX-(k//8)
        if k%4==0:
            s['fx'].append(('spark',cl['x']+10+random.randint(-1,1),GROUND-14+random.randint(-4,4),4+random.randint(0,2))); s['shake']=rshake()
            s['fx'].append(('ring',cl['x']+11,GROUND-12,6,(200,236,255)))
        s['fx'].append(('kny_shock',cl['x']+4-(k%4)*3,GROUND-10-(k%8),5))
        shout(s,"AIR TYPE!",(255,150,200),cx=110)
    if 100<=f<114:                                                  # the last punch lands
        t=(f-100)/10; cl.update(x=ez(CX-3,14,t),y=GROUND-int(6*math.sin(math.pi*min(1,t)))); pose='hurt'
        ak.update(x=50,spr=AKAZA['attack'] if f<104 else AKAZA['idle'])
        if f==100: s['flash']=0.6; s['fc']=(38,GROUND-12); s['flashc']=(220,240,255); s['shake']=rshake(2)
        if f<104: s['fx'].append(('spark',36,GROUND-12,8-(f-100)))
        if f>=106: s['fx'].append(('dust',cl['x']+4,GROUND-random.randint(0,2)))
    if 104<=f<116:
        t=(f-104)/12; ak.update(x=ez(50,EX,t),y=GROUND-int(14*math.sin(math.pi*t)),spr=AKAZA['idle'])
    # 4) close-up: WATER BREATHING, TENTH FORM, CONSTANT FLUX
    if 116<=f<160: s['image']=closeup_water((f-116)/44,f); return s
    # 5) the water dragon rides the slash into Akaza
    if 160<=f<176:
        t=(f-160)/16; cl['x']=ez(14,124,t); pose='dash'; glow=(70,150,255)
        s['under'].append(('kny_dragon',max(-20,cl['x']-90),cl['x']+8,GROUND-12,5))
        extra+=[ghost(TANJ['dash'],cl['x']-8),ghost(TANJ['dash'],cl['x']-16,a=0.2)]
    if 176<=f<190:
        cl['x']=124; pose='punch'; glow=(70,150,255) if f<184 else None
        ak.update(spr=AKAZA['hurt'],x=ez(EX,164,(f-176)/8))
        if f<184:
            s['fx'].append(('kny_warc',146,GROUND-11,12,200+(f-176)*20,420+(f-176)*20))
            if f>=179: s['fx'].append(('kny_warc',150,GROUND-9,9,20,200))
        s['fx'].append(('kny_splash',148,GROUND-12,(f-176)/14))
        if f==176: s['flash']=0.6; s['fc']=(146,GROUND-10); s['flashc']=(200,236,255)
        if f<182: s['shake']=rshake(2)
    # 6) DESTRUCTIVE DEATH: DISORDER
    if 190<=f<200:
        cl['x']=124; ak.update(x=164,spr=AKAZA['idle'],aura=((255,120,180),1+(f%2)))
        s['under'].append(('kny_compass',164,6+(f-190)*2,1))
    if 190<=f<214: shout(s,"DESTRUCTIVE DEATH: DISORDER",(255,150,200))
    if 200<=f<214:
        k=f-200; ak.update(x=164,spr=AKAZA['attack'] if k%2==0 else AKAZA['idle'],aura=((255,120,180),2))
        for j in range(4): s['fx'].append(('kny_shock',160-((k*6+j*11)%40),GROUND-8-((j*5+k)%12),4+j%2))
        t=(f-200)/14; cl.update(x=ez(124,40,t),y=GROUND-int(10*math.sin(math.pi*t))); pose='hurt'
        if k%3==0: s['fx'].append(('spark',cl['x']+6,GROUND-12+random.randint(-4,4),5)); s['shake']=rshake(2)
        if f==200: s['flash']=0.5; s['fc']=(124,GROUND-10); s['flashc']=(255,200,230)
    if 214<=f<220:
        cl['x']=40; pose='hurt'; ak.update(x=ez(164,EX,(f-214)/6),spr=AKAZA['idle'])
    # 7) close-up: HINOKAMI KAGURA
    if 220<=f<260: s['image']=closeup_fire((f-220)/40,f); return s
    # 8) the flaming leap, one cut through the neck
    if 260<=f<278:                                                  # over him, cutting as he passes
        t=(f-260)/18; cl.update(x=ez(40,176,t),y=GROUND-int(24*math.sin(math.pi*t))); pose='dash'; glow=(255,120,40)
        s['fx'].append(('kny_farc',cl['x'],cl['y']-6,10,(f*40)%360,(f*40)%360+260))
        for i in range(3): s['fx'].append(('kny_ember',cl['x']-random.randint(4,18),cl['y']-random.randint(0,12)))
        ak['spr']=AKAZA['attack'] if f>=264 else AKAZA['idle']
    if 270<=f<278:
        s['fx'].append(('kny_farc',EX,GROUND-13,30,180,360,5))
        s['fx'].append(('kny_farc',EX,GROUND-14,22,190,350,3))
        if f==270: s['flash']=0.7; s['fc']=(EX,GROUND-14); s['flashc']=(255,200,120)
        if f<276: s['shake']=rshake(2)
    HEAD_T=lambda f: (f-272)/16
    if 278<=f<304:                                                  # Claude lands behind him, blade out
        cl.update(x=176,y=GROUND,flip=True); pose='punch' if f<292 else 'guard'; glow=(255,120,40) if f<286 else None
    if 272<=f<306:
        ak['vis']=False
        if f<284: s['fx'].append(('kny_crumble',AK_HEADLESS,EX,GROUND,True,0))
        else: s['fx'].append(('kny_crumble',AK_HEADLESS,EX,GROUND,True,(f-284)/22))
        ht=min(1,HEAD_T(f)); hx=EX-ht*22; hy=GROUND-16-20*math.sin(math.pi*ht)+ht*14
        hspr=rotate90(AK_HEAD,(f//3)%4) if ht<1 else rotate90(AK_HEAD,1)
        if f<290: extra.append(actor(hspr,hx,int(hy)+len(hspr)//2,flip=True))
        else: s['fx'].append(('kny_crumble',rotate90(AK_HEAD,1),EX-22,GROUND,True,(f-290)/16))
        if f<282: s['fx'].append(('kny_ember',EX+random.randint(-3,3),GROUND-14))
    # 9) Claude hops back home; another Akaza drops onto the roof
    if 304<=f<320:
        t=(f-304)/16; cl.update(x=ez(176,CX,t),flip=False,y=GROUND-int(12*math.sin(math.pi*t))); pose='guard'
    if 272<=f<314: ak['vis']=False
    if 314<=f<322:
        t=(f-314)/8; ak.update(vis=True,x=EX,y=int(lerp(-4,GROUND,t*t)),spr=AKAZA['hurt'] if t<1 else AKAZA['idle'])
    if 322<=f<330:
        ak.update(vis=True,x=EX,y=GROUND+(1 if f<325 else 0))
        s['fx'].append(('ring',EX,GROUND,(f-322)*4+3,(160,170,200)))
        for j in range(2): s['fx'].append(('dust',EX+random.randint(-12,12),GROUND-random.randint(0,3)))
        if f<325: s['shake']=rshake()
    if pose not in ('guard','guard2'): cl['spr']=TANJ[pose]
    if blade: s['fx'].append(katana_for(pose if pose!='guard' else 'guard',cl['x'],cl['y'],cl['flip'],glow))
    s['actors']=extra+[cl,ak]
    return s

CLIPS = [clip('breath', N_, clip_breath)]
