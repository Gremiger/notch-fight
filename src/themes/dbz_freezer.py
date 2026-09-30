"""Dragon Ball sub-theme "dbz-freezer": Claude (Goku) and Codex face Freezer in his final
form on planet Namek — green sky, blue-green grass, round-topped Namekian trees, mesas in the water.
Freezer laughs and fires Death Beams that Claude blocks, then lifts Codex into the sky with his mind
(CLAUDE...!). Close-up: Freezer's smug face, a raised finger — the hand closes. Codex bursts into
light. Close-up: Claude's shock turns to rage — CODEX...! FREEZEEER!!! The sky goes black, lightning
strikes, the ground cracks and rocks float up; the hair flickers gold until the aura explodes — close-up:
I AM THE SUPER SAIYAN, SON CLAUDE! Freezer panics: his beams miss, his Death Ball is kicked away, a rush
and a Kamehameha that swallows his beam blow him off the field. The Dragon Balls glow, Porunga rises —
A WISH GRANTED: Codex comes back, Claude powers down, Freezer flies back to his spot."""
from engine import *
from PIL import ImageChops

THEME = 'dbz-freezer'
N_ = 480
CX, KX, EX = 24, 44, 154                                            # Claude, Codex, Freezer at the loop keyframe

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

@fx('frz_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,cx=W//2,outline=None):
    s['fx'].append(('frz_say',txt,y,c,scale,cx,outline))

# ---- Claude: Goku's spiky hair and a blue belt on the orange gi; Super Saiyan = golden spikes -----
_POWER=S([                                                          # fists clenched at his sides, screaming
"...OOOOOOOO...",
"...OOOOOOOO...",
"...OOOOKOOK...",
"...OOOOKOOK...",
"...OOOOOOOO...",
"..oOOOOOOOOo..",
".oo.OOOOOO.oo.",
"oo.OOOOOOOO.oo",
"...oOOOOOOo...",
"...oo....oo...",
"..ooo....ooo..",])
def _gi(x,y,t,l,r,c):
    return 'L' if (c=='O' and y==t+7 and l<=x<=r) else None
def _form(hair,bangs):
    return {k:overlay(recolor_rows(v,_gi),hair,-2,0,bangs=bangs) for k,v in dict(CL,power=_POWER).items()}
BASE=_form(["..k..k.k.....",".kkk.kkkkk...","kkkkkkkkkkk.."],"..kk.k.kk")
SSJ=_form(["...Y...Y.....","..YY..YY.Y...",".YyYYYYyYYY..","YYYYYYYYYYYY."],"..YY.Y.YY")
SSJPAL={'Y':(255,234,90),'y':(222,168,36)}
AURA_W=(236,240,255)
AURA_G=(255,226,90)
KI=((255,244,180),(255,196,60))                                     # the Super Saiyan Kamehameha

# ---- Codex: the ">_" terminal head with six forehead dots, an orange gi -----------------
_KHEAD=[r.replace('y','E') for r in ICONS['CODEX']]
_KHEAD[0]=".kkokokokk."; _KHEAD[1]="kkkokokokkk"                    # six forehead dots
_KBODY={
 'idle':["....ddd....","..ddddddd..",".dd.ddd.dd.","....LLL....","...dd.dd...","...dd.dd...","..NNN.NNN.."],
 'up':  ["d...ddd...d","dd.ddddd.dd",".ddddddddd.","....LLL....","...dd.dd...","...dd.dd...","..NNN.NNN.."],
 'flail':["dd.......dd",".dd.ddd.dd.","..ddddddd..","....LLL....","..dd...dd..",".dd.....dd.","NN.......NN"],
 'kick':["....ddd..dd","dddddddddd.","....ddd....","....LLL....","...dd..dd..","..dd....dd.",".NN......NN"],
}
CODEX={k:S(_KHEAD+b) for k,b in _KBODY.items()}
KPAL={'d':(240,134,52)}
TK=(214,150,255)                                                    # Freezer's telekinesis glow

# ---- Freezer, final form: white, purple glossy domes on head/shoulders/forearms/shins, red eyes,
# the tail curling behind him. Drawn facing right (flip=True on the right side) -------------------
_FZ_IDLE=S([
"........VVV.......",
".......VHVVV......",
".......VVVVV......",
".......WWWWW......",
".......WWrWr......",
".......WWWWW......",
"........WpW.......",
"....VV..WW..VV....",
"...VVVWWWWWWVVV...",
"...WW.WWVVWW.WW...",
"...WW.WWWWWW.WW...",
"...VV..WWWW..VV...",
"...vW..WWWW..Wv...",
".W....WWWWWW......",
"W.WWWWWW..WW......",
"W.....WW...WW.....",
".WW...VV...VV.....",
"......WW...WW.....",
".....WWW...WWW....",])
_FZ_POINT=S([                                                       # the Death Beam finger
"........VVV..........",
".......VHVVV.........",
".......VVVVV.........",
".......WWWWW.........",
".......WWrWr.........",
".......WWWWW.........",
"........WpW..........",
"....VV..WW..VV.......",
"...VVVWWWWWWVVVVVWW..",
"...WW.WWVVWW.VVVVWWWW",
"...WW.WWWWWW.........",
"...VV..WWWW..........",
"...vW..WWWW..........",
".W....WWWWWW.........",
"W.WWWWWW..WW.........",
"W.....WW...WW........",
".WW...VV....VV.......",
"......WW....WW.......",
".....WWW....WWW......",])
_FZ_UP=S([                                                          # a hand raised: telekinesis, the Death Ball
"..............W...",
".............WW...",
"........VVV..VV...",
".......VHVVV.VV...",
".......VVVVV.WW...",
".......WWWWW.WW...",
".......WWrWr.WW...",
".......WWWWW.WW...",
"........WpW..WW...",
"....VV..WW..VV....",
"...VVVWWWWWWVV....",
"...WW.WWVVWW......",
"...WW.WWWWWW......",
"...VV..WWWW.......",
"...vW..WWWW.......",
".W....WWWWWW......",
"W.WWWWWW..WW......",
"W.....WW...WW.....",
".WW...VV...VV.....",
"......WW...WW.....",
".....WWW...WWW....",])
_FZ_GUARD=S([                                                       # arms crossed over the face
"........VVV.......",
".......VHVVV......",
".......VVVVV......",
".......WWWWW......",
".......WVVVVV.....",
".......WWWWWWW....",
"........WpWWVV....",
"....VV..WW..WW....",
"...VVVWWWWWWVV....",
"...WW.WWVVWW......",
"...WW.WWWWWW......",
"...VV..WWWW.......",
"...vW..WWWW.......",
".W....WWWWWW......",
"W.WWWWWW..WW......",
"W.....WW....WW....",
".WW..VV.....VV....",
".....WW.....WW....",
"....WWW.....WWW...",])
FZ={'idle':_FZ_IDLE,'point':_FZ_POINT,'up':_FZ_UP,'guard':_FZ_GUARD,'hurt':hurt(_FZ_IDLE)}
FZPAL={'V':(150,58,176),'p':(96,34,116),'H':(236,200,255),'W':(242,242,250),'v':(186,184,204),'r':(222,30,40)}
FZ_BURNT=dict(FZPAL,W=(170,164,170),V=(100,44,110),v=(130,124,134))
FZ_AURA=(220,150,255)
FZ_KI=((255,150,220),(236,60,170))                                  # the Death Beam, pink

# ---- background: Namek ---------------------------------------------------------------------------
HOR=38
def _tree(d,x,base,h,r):
    """A Namekian tree: a thin trunk, a bulbous round crown with a smaller bulb on top."""
    d.line([x,base,x,base-h],fill=(104,92,70)); d.line([x+1,base,x+1,base-h+2],fill=(80,70,56))
    top=base-h
    d.ellipse([x-r,top-r,x+r+1,top+r*0.8],fill=(62,150,118)); d.chord([x-r,top-r,x+r+1,top+r*0.8],300,120,fill=(40,116,96))
    q=max(1,r//2); d.ellipse([x-q+1,top-r-q-1,x+q+1,top-r+q-1],fill=(62,150,118))
    d.arc([x-r+1,top-r+1,x+r-1,top+r*0.6],190,250,fill=(140,210,160))

def _namek(d):
    for y in range(HOR):                                            # the green sky, bright at the horizon
        k=y/(HOR-1); d.line([0,y,W,y],fill=(int(92+96*k),int(172+56*k),int(116+46*k)))
    for sx,sy,r in ((34,8,3),(150,5,2),(168,13,2)):                 # Namek's three suns
        d.ellipse([sx-r-2,sy-r-2,sx+r+2,sy+r+2],fill=(224,246,196)); d.ellipse([sx-r,sy-r,sx+r,sy+r],fill=(255,255,236))
    far=(128,178,160)                                               # far mesas in the haze
    for x0,x1,top in ((0,20,30),(40,58,27),(96,112,31),(128,150,26),(170,185,29)):
        d.rectangle([x0,top,x1,HOR],fill=far); d.line([x0,top,x1,top],fill=(156,200,180))
    rock,shade,lite=(118,140,132),(86,106,104),(160,184,170)        # the near plateaus rising out of the water
    for x0,x1,top in ((6,26,20),(66,80,24),(140,166,18)):
        d.polygon([(x0,HOR+4),(x0+2,top),(x1-2,top),(x1,HOR+4)],fill=rock)
        d.polygon([(x1-6,top),(x1-2,top),(x1,HOR+4),(x1-5,HOR+4)],fill=shade)
        d.line([x0+2,top,x1-2,top],fill=lite); d.line([x0+1,top+5,x1-3,top+5],fill=shade)
    d.rectangle([0,HOR,W,46],fill=(84,154,188))                     # the water
    rr=random.Random(5353)
    for _ in range(26):
        x=rr.randint(0,W-6); y=rr.randint(HOR+1,45); d.line([x,y,x+rr.randint(2,6),y],fill=(150,206,226))
    d.line([0,HOR,W,HOR],fill=(170,220,230))
    for x0,x1 in ((84,126),):                                       # a little island with a Namekian dome house
        d.ellipse([x0,HOR-1,x1,HOR+5],fill=(96,170,120))
    d.chord([97,HOR-8,111,HOR+6],180,360,fill=(238,240,228),outline=(150,160,150))   # the dome house
    d.chord([106,HOR-5,116,HOR+5],180,360,fill=(226,230,216),outline=(150,160,150))
    for wx in (101,106): d.rectangle([wx,HOR-3,wx+1,HOR-2],fill=(70,90,96))
    d.rectangle([111,HOR-1,112,HOR],fill=(70,90,96))
    _tree(d,90,HOR+1,7,3); _tree(d,120,HOR+1,5,2)
    for y in range(46,H):                                           # the blue-green grass
        k=(y-46)/(H-46); d.line([0,y,W,y],fill=(int(92-30*k),int(170-40*k),int(132-26*k)))
    d.line([0,46,W,46],fill=(140,210,170))
    for _ in range(60):
        x=rr.randint(0,W-1); y=rr.randint(47,H-1)
        d.line([x,y,x+rr.choice([-1,0,1]),y-1],fill=rr.choice([(60,128,104),(130,200,160)]))
    for x,h,r in ((6,20,5),(62,16,4),(176,22,6),(134,14,3)):         # the near trees
        _tree(d,x,48,h,r)
register_bg(THEME, lambda v: (v+50,v+120,v+96), decor=_namek)

# ---- effects -------------------------------------------------------------------------------------
CLOUDS=[(0,4,0.8),(80,12,0.6),(140,2,0.7)]
@fx('frz_clouds')
def _fx_clouds(d,im,e,f):
    """Wispy pale clouds drifting left; one lap per clip, so the loop is seamless."""
    o=f*225//N_
    for x0,y,k in CLOUDS:
        x=(x0-o)%225-20; w=int(26*k)
        d.ellipse([x,y,x+w,y+5],fill=(222,246,214)); d.ellipse([x+w//3,y-2,x+w,y+4],fill=(236,252,228))
        d.line([x-4,y+5,x+w+6,y+5],fill=(180,222,176))

@fx('frz_storm')
def _fx_storm(d,im,e,f):
    """The dying planet: the whole backdrop sinks into a dark storm (a = 0..1)."""
    _,a=e
    if a<=0: return
    base=im.copy(); dark=fade_to(im,(22,26,40),min(0.8,a)); d=ImageDraw.Draw(dark); o=f*2
    for x0,y in ((0,3),(70,9),(130,1),(200,6)):                     # heavy clouds rolling in
        x=(x0-o)%260-40
        for dx,r in ((0,6),(9,8),(20,6),(30,5)): d.ellipse([x+dx-r,y-r//2,x+dx+r,y+r],fill=(44,46,58))
    im.paste(Image.blend(base,dark,min(1,a/0.6)))

@fx('frz_bolt')
def _fx_bolt(d,im,e,f):
    """A lightning bolt from the clouds to the ground at x, with a flash of the sky."""
    _,x,seed=e; rr=random.Random(seed)
    im.paste(fade_to(im,(200,210,255),0.25)); d=ImageDraw.Draw(im)
    y=0; pts=[(x,y)]
    while y<GROUND:
        x+=rr.randint(-5,5); y+=rr.randint(4,9); pts.append((x,min(y,GROUND)))
    d.line(pts,fill=(170,180,255),width=3); d.line(pts,fill=(255,255,255))
    bx,by=pts[len(pts)//2]
    d.line([bx,by,bx+rr.choice([-8,8]),by+8],fill=(220,230,255))
    d.ellipse([x-3,GROUND-2,x+3,GROUND+1],fill=(255,255,255))

@fx('frz_crack')
def _fx_crack(d,im,e,f):
    """The ground splitting around x (t 0..1), glowing faintly gold from below."""
    _,x,t=e; rr=random.Random(77)
    for k in range(6):
        a=rr.uniform(-0.25,0.25)+(0 if k%2 else math.pi); L=(8+34*rr.random())*t; px,py=x,GROUND
        pts=[(px,py)]
        for j in range(1,5): pts.append((px+math.cos(a)*L*j/4,py+rr.randint(-1,4)*j/4))
        d.line(pts,fill=(34,50,40),width=2); d.line(pts,fill=(255,210,90) if t>0.6 and (f+k)%3 else (20,30,26))

@fx('frz_rocks')
def _fx_rocks(d,im,e,f):
    """Rocks tearing off the ground and floating up, trembling (t0 = when they start)."""
    _,t0,n=e; rr=random.Random(4545)
    for i in range(n):
        x=rr.randint(4,180); sp=rr.uniform(0.3,0.9); s0=rr.randint(0,20); sz=rr.randint(1,3)
        k=f-t0-s0
        if k<0: continue
        y=GROUND-1-k*sp
        if y<-4: continue
        x+=(f+i)%2
        d.rectangle([x,y,x+sz,y+sz],fill=(118,140,132)); d.point((x,y),fill=(170,190,180))

@fx('frz_beam')
def _fx_beam(d,im,e,f):
    """The Death Beam: a thin pink laser from finger to target."""
    _,x0,y0,x1,y1=e
    d.line([x0,y0,x1,y1],fill=(236,60,170),width=3); d.line([x0,y0,x1,y1],fill=(255,210,240))
    d.ellipse([x0-2,y0-2,x0+2,y0+2],fill=(255,200,240))

@fx('frz_kiball')
def _fx_kiball(d,im,e,f):
    """A ki ball in the hands: x,y,r,(outer,mid), with a spiky corona."""
    _,x,y,r,(oc,mc)=e; ball(d,int(x),int(y),int(r),oc,mc,f); asterisk(d,int(x),int(y),int(r)+3,oc,f)

@fx('frz_deathball')
def _fx_deathball(d,im,e,f):
    """Freezer's Death Ball: a small red-orange sun with a glow."""
    _,x,y,r=e; x,y,r=int(x),int(y),int(r)
    glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([x-r-5,y-r-5,x+r+5,y+r+5],fill=130)
    im.paste((255,120,60),(0,0),glow.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=(190,40,30)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,110,50))
    d.ellipse([x-r//2,y-r//2,x,y],fill=(255,230,170))

@fx('frz_clash')
def _fx_clash(d,im,e,f):
    """Where the beams meet: a white-hot knot throwing sparks."""
    _,x,y=e; x,y=int(x),int(y); r=6+(f%3); rr=random.Random(f)
    d.ellipse([x-r-2,y-r-2,x+r+2,y+r+2],fill=(255,220,240)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255))
    asterisk(d,x,y,r+5,(255,200,140),f)
    for _ in range(6):
        a=rr.random()*6.28; L=rr.randint(r+2,r+12); d.point((int(x+math.cos(a)*L),int(y+math.sin(a)*L*0.7)),fill=(255,255,200))

@fx('frz_tk')
def _fx_tk(d,im,e,f):
    """Telekinesis: a pulsing violet glow around a point, wisps swirling in."""
    _,x,y,r=e; x,y=int(x),int(y)
    glow=Image.new('L',(W,H),0); rp=r+(f%3)
    ImageDraw.Draw(glow).ellipse([x-rp,y-rp,x+rp,y+rp],fill=110)
    im.paste(TK,(0,0),glow.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    for k in range(6):
        a=f*0.5+k*1.047; L=r+2-((f+k*3)%6)
        d.point((int(x+math.cos(a)*L),int(y+math.sin(a)*L*0.8)),fill=(255,236,255))

@fx('frz_burst')
def _fx_burst(d,im,e,f):
    """Codex bursting into light (t 0..1): a white core, rays, rings and a scatter of sparks."""
    _,x,y,t=e; x,y=int(x),int(y); rr=random.Random(3131)
    glow=Image.new('L',(W,H),0); R=int(10+40*ease(t))
    ImageDraw.Draw(glow).ellipse([x-R,y-R,x+R,y+R],fill=int(230*(1-t*0.8)))
    im.paste((255,250,220),(0,0),glow.filter(ImageFilter.GaussianBlur(5))); d=ImageDraw.Draw(im)
    if t<0.5:
        for i in range(12):
            a=i*0.5236+0.2; L=20+60*t
            d.line([x,y,x+math.cos(a)*L,y+math.sin(a)*L*0.7],fill=(255,255,230))
        r=int(8*(1-t*2))+2; d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255))
    for j in range(2):
        rr_=int(6+70*t)+j*8
        d.ellipse([x-rr_,y-rr_//2,x+rr_,y+rr_//2],outline=(255,236,170) if j else (255,255,255))
    for i in range(24):
        a=rr.random()*6.28; v=rr.uniform(20,60); L=v*ease(t)
        px,py=x+math.cos(a)*L,y+math.sin(a)*L*0.6+t*t*14
        c=(255,255,255) if i%3==0 else ((255,220,120) if i%3==1 else (150,200,255))
        if t<0.9: d.point((int(px),int(py)),fill=c)
        if i%4==0 and t<0.6: d.line([px-1,py,px+1,py],fill=c)

@fx('frz_embers')
def _fx_embers(d,im,e,f):
    """The last sparks drifting down in the silence (t 0..1, fading)."""
    _,x,y,t=e; rr=random.Random(3132)
    for i in range(14):
        px=x+rr.uniform(-40,40)+math.sin(f*0.2+i)*2; py=y+rr.uniform(-10,10)+t*30
        if rr.random()>t*0.9 and py<GROUND: d.point((int(px),int(py)),fill=(255,236,170) if i%2 else (200,220,255))

@fx('frz_speed')
def _fx_speed(d,im,e,f):
    """Horizontal speed streaks across the frame."""
    rr=random.Random(f*7)
    for _ in range(8):
        y=rr.randint(8,GROUND-2); x=rr.randint(0,W-20); d.line([x,y,x+rr.randint(10,24),y],fill=(255,255,255))

@fx('frz_zip')
def _fx_zip(d,im,e,f):
    """Moving too fast to see: the flicker lines left behind."""
    _,x,y=e; rr=random.Random(f*3+int(x))
    for _ in range(4):
        yy=y+rr.randint(-10,2); xx=x+rr.randint(-6,6); d.line([xx-5,yy,xx+5,yy],fill=(255,255,255))
        d.line([xx-3,yy+1,xx+3,yy+1],fill=(255,226,90))

@fx('frz_sweat')
def _fx_sweat(d,im,e,f):
    """A nervous sweat drop."""
    _,x,y=e; d.point((x,y),fill=(170,220,255)); d.line([x-1,y+1,x+1,y+1],fill=(170,220,255)); d.point((x,y+2),fill=(120,180,240))

@fx('frz_balls')
def _fx_balls(d,im,e,f):
    """The seven Namekian Dragon Balls glowing on the grass, a pillar of light rising (a 0..1)."""
    _,x,a=e
    if a>0.3:
        glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).rectangle([x-5,0,x+5,GROUND],fill=int(150*a))
        im.paste((255,236,150),(0,0),glow.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    for i in range(7):
        bx=x-15+i*5; by=GROUND-2-(1 if i in (2,4) else (2 if i==3 else 0))
        d.ellipse([bx-2,by-2,bx+2,by+2],fill=(255,150,40)); d.point((bx-1,by-1),fill=(255,236,200)); d.point((bx,by),fill=(210,30,20))

def _porunga(t):
    """Porunga on a transparent layer, rising out of the light (t 0..1 = how far up): a serpent coil
    out of the Dragon Balls, a broad green chest, arms crossed, horns, a fanged scowl, red eyes."""
    L=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(L)
    cx=128; hy=int(3+(1-ease(t))*54)
    g,gd,gl,bone=(70,156,72,255),(36,100,46,255),(128,206,112,255),(226,212,168,255)
    d.line([(100,GROUND),(96,GROUND-8),(104,hy+54),(cx-10,hy+46)],fill=g,width=7)          # the coil from the balls
    d.line([(100,GROUND),(96,GROUND-8),(104,hy+54),(cx-10,hy+46)],fill=gl,width=1)
    for k in range(4):                                              # spines down the back
        for sx in (-1,1): d.polygon([(cx+sx*17,hy+16+k*7),(cx+sx*26,hy+12+k*7),(cx+sx*19,hy+21+k*7)],fill=gd)
    d.polygon([(cx-18,hy+50),(cx-20,hy+18),(cx+20,hy+18),(cx+18,hy+50)],fill=g)            # the chest
    d.ellipse([cx-27,hy+13,cx-11,hy+27],fill=g,outline=gd); d.ellipse([cx+11,hy+13,cx+27,hy+27],fill=g,outline=gd)   # shoulders
    d.line([cx,hy+18,cx,hy+28],fill=gd); d.arc([cx-15,hy+15,cx,hy+28],10,170,fill=gd); d.arc([cx,hy+15,cx+15,hy+28],10,170,fill=gd)
    for k in range(3): d.line([cx-7,hy+42+k*3,cx+7,hy+42+k*3],fill=gd)                     # the belly plates
    d.polygon([(cx-24,hy+24),(cx-17,hy+22),(cx+14,hy+36),(cx+10,hy+41)],fill=gl,outline=gd)   # the crossed forearms
    d.polygon([(cx+24,hy+24),(cx+17,hy+22),(cx-14,hy+36),(cx-10,hy+41)],fill=g,outline=gd)
    for x in (cx+11,cx-14): d.line([x,hy+37,x+3,hy+40],fill=bone)                          # claws
    d.polygon([(cx-5,hy+3),(cx-13,hy-5),(cx-15,hy-2),(cx-9,hy+5)],fill=bone)              # horns
    d.polygon([(cx+5,hy+3),(cx+13,hy-5),(cx+15,hy-2),(cx+9,hy+5)],fill=bone)
    for sx in (-1,1): d.polygon([(cx+sx*6,hy+7),(cx+sx*13,hy+5),(cx+sx*7,hy+11)],fill=gd)  # ear fins
    d.ellipse([cx-7,hy+1,cx+7,hy+14],fill=g,outline=gd)                                    # the head
    d.rounded_rectangle([cx-5,hy+9,cx+5,hy+18],2,fill=gl,outline=gd)                       # the snout
    d.line([cx-7,hy+5,cx-1,hy+7],fill=gd,width=2); d.line([cx+7,hy+5,cx+1,hy+7],fill=gd,width=2)   # the scowl
    for ex in (-4,3): d.rectangle([cx+ex,hy+7,cx+ex+1,hy+8],fill=(240,30,30,255))
    d.line([cx-4,hy+15,cx+4,hy+15],fill=(40,20,20,255))
    for fx_ in (-3,3): d.line([cx+fx_,hy+15,cx+fx_,hy+17],fill=(255,255,255,255))         # fangs
    return L

@fx('frz_porunga')
def _fx_porunga(d,im,e,f):
    _,t,a=e
    if a<=0: return
    L=_porunga(t); al=L.getchannel('A').point(lambda v: int(v*a))
    edge=al.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1))
    im.paste((255,236,150),(0,0),edge); im.paste(L.convert('RGB'),(0,0),al)

# ---- close-up: Freezer's smug face and the closing hand ------------------------------------------
def closeup_freezer(t,f):
    """Primer plano: Freezer's smirk, red eyes narrowed; the raised finger — then the hand closes."""
    im=Image.new('RGB',(W,H),(40,14,52)); d=ImageDraw.Draw(im)
    for i in range(20):                                             # dark violet rays
        a=i*0.314+f*0.01; c=(62,22,78) if i%2 else (48,16,62)
        d.polygon([(60,34),(60+math.cos(a)*220,34+math.sin(a)*140),(60+math.cos(a+0.16)*220,34+math.sin(a+0.16)*140)],fill=c)
    d.ellipse([22,1,98,104],fill=(242,242,250),outline=(120,110,150))                       # the head
    d.chord([23,2,97,103],100,260,fill=(206,204,222))
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); md.ellipse([23,2,97,103],fill=255)     # the purple dome:
    m2=Image.new('L',(W,H),0); ImageDraw.Draw(m2).ellipse([6,-44,114,28],fill=255)         # the head's crown
    m=ImageChops.multiply(m,m2); im.paste((150,58,176),(0,0),m); d=ImageDraw.Draw(im)
    d.arc([34,6,64,30],200,250,fill=(236,200,255),width=2); d.ellipse([40,6,47,10],fill=(246,226,255))   # its gloss
    for ex,s_ in ((46,1),(74,-1)):                                  # narrowed red eyes
        d.polygon([(ex-9,33+3*s_),(ex+9,33-3*s_),(ex+8,40),(ex-8,40)],fill=(250,250,255),outline=(20,10,24))
        d.rectangle([ex-2,34,ex+2,39],fill=(222,30,40)); d.rectangle([ex-1,35,ex,37],fill=(20,10,24))
        d.line([ex-10,30+4*s_,ex+10,30-4*s_],fill=(96,34,116),width=2)   # the lids, smug
    for ex in (30,90): d.line([ex,42,ex+(4 if ex<60 else -4),50],fill=(186,184,204))   # cheek lines
    d.chord([46,50,76,62],0,180,fill=(96,34,116))                   # the purple-lipped smirk
    d.line([46,55,76,55],fill=(60,14,70)); d.line([76,55,80,51],fill=(96,34,116))
    closed=t>=0.58
    jx=((f%2)*2-1) if 0.58<=t<0.66 else 0
    hx=144+jx
    d.polygon([(hx-12,64),(hx+14,64),(hx+10,44),(hx-10,44)],fill=(242,242,250))   # the forearm, its purple dome
    d.ellipse([hx-12,50,hx+12,68],fill=(150,58,176)); d.arc([hx-9,52,hx+2,62],190,260,fill=(236,200,255))
    if not closed:
        d.rounded_rectangle([hx-11,22,hx+11,46],4,fill=(242,242,250),outline=(150,150,176))   # the palm
        for k in range(3):                                          # three fingers curled
            d.rounded_rectangle([hx-11+k*6,18,hx-6+k*6,26],2,fill=(236,236,246),outline=(150,150,176))
        d.rounded_rectangle([hx+4,2,hx+10,24],3,fill=(242,242,250),outline=(150,150,176))  # the raised finger
        d.rounded_rectangle([hx-14,30,hx-8,40],2,fill=(236,236,246),outline=(150,150,176)) # thumb
        if t>0.2:                                                   # the tip glows
            r=2+(f%2); d.ellipse([hx+7-r-2,1-r,hx+7+r+2,1+r+2],fill=(255,150,220)); d.ellipse([hx+6,0,hx+8,2],fill=(255,255,255))
    else:
        d.rounded_rectangle([hx-13,22,hx+13,46],6,fill=(242,242,250),outline=(150,150,176))   # the fist
        for k in range(4): d.line([hx-11+k*6,24,hx-11+k*6,32],fill=(170,168,190))
        d.line([hx-13,33,hx+13,33],fill=(170,168,190))
        if t<0.66:
            for i in range(8):
                a=i*0.785; d.line([hx+math.cos(a)*18,34+math.sin(a)*14,hx+math.cos(a)*26,34+math.sin(a)*20],fill=(255,210,240))
    if 0.14<=t<0.52: say(im,"HO HO HO",4,(236,200,255),cx=114,outline=(70,20,90))
    if t<0.06: zoom_lines(d,(220,160,255))
    if t>0.9: im=fade_to(im,(255,255,255),(t-0.9)/0.1*0.8)
    return im

# ---- close-ups of Claude: shock to rage, then the Super Saiyan -----------------------------------
_HAIR_BASE=[(40,58,26,8),(50,70,54,0),(62,84,82,2),(76,98,106,8),(90,102,114,20),(40,50,24,22)]
_HAIR_GOLD=[(40,58,30,-6),(50,70,56,-10),(62,84,80,-10),(76,98,104,-4),(90,102,118,6),(40,50,22,8)]
_BANGS=[(50,62,56,40),(60,72,64,36),(78,90,86,38)]
def _head(d,ox,gold,sway=0):
    """Claude's head at x offset ox: spiky hair (gold or black), orange face; returns eye xs."""
    col,edge=((255,226,80),(200,140,20)) if gold else ((30,28,40),(120,130,190))
    for x0,x1,tx,ty in (_HAIR_GOLD if gold else _HAIR_BASE):
        d.polygon([(x0+ox,30),(x1+ox,30),(tx+sway+ox,ty)],fill=col,outline=edge)
    d.rectangle([40+ox,22,104+ox,30],fill=col)
    d.rectangle([44+ox,30,100+ox,64],fill=(217,119,87)); d.rectangle([44+ox,30,50+ox,64],fill=(176,92,66))
    for x0,x1,tx,ty in _BANGS: d.polygon([(x0+ox,29),(x1+ox,29),(tx+ox,ty)],fill=col)
    if gold:
        for x0,x1,tx,ty in _HAIR_GOLD[1:4]: d.line([(x0+x1)//2+ox,28,tx+sway+ox,ty+6],fill=(255,248,190))
    return 60+ox,82+ox

def closeup_rage(t,f):
    """Primer plano: Claude stares at the empty sky — CODEX...! — then the rage: FREEZEEER!!!"""
    rage=t>=0.45
    rr=random.Random(f)
    im=Image.new('RGB',(W,H),(120,16,20) if rage else (34,42,64)); d=ImageDraw.Draw(im)
    if rage:
        for i in range(22):
            a=i*0.2856+f*0.05; c=(170,30,30) if i%2 else (96,10,14)
            d.polygon([(48,40),(48+math.cos(a)*220,40+math.sin(a)*140),(48+math.cos(a+0.14)*220,40+math.sin(a+0.14)*140)],fill=c)
    else:
        for _ in range(30):                                         # the shock: falling lines
            x=rr.randint(0,W); d.line([x,0,x,rr.randint(10,64)],fill=(60,70,100))
    jx=((f%3)-1)*2 if rage else 0
    gold=rage and t>0.86 and f%2==0                                 # a flicker of what is coming
    e1,e2=_head(d,-24+jx,gold)
    if not rage:                                                    # wide eyes, tiny pupils, mouth agape
        for ex in (e1,e2):
            d.ellipse([ex-5,38,ex+5,52],fill=(250,250,250),outline=(24,14,12)); d.rectangle([ex,44,ex+1,46],fill=(24,14,12))
            d.line([ex-5,34,ex+5,33],fill=(24,14,12))
        d.ellipse([66-24,55,74-24,62],fill=(60,20,16))
        if t>0.2: d.line([e1-2,53,e1-2,53+int((t-0.2)*40)],fill=(170,220,255))   # a tear
    else:                                                           # brows slammed down, screaming
        for ex,s in ((e1,1),(e2,-1)):
            d.polygon([(ex-6,42-3*s),(ex+6,42+3*s),(ex+5,50),(ex-5,50)],fill=(250,250,250),outline=(24,14,12))
            d.rectangle([ex,45,ex+1,47],fill=(24,14,12))
            d.line([ex-7,37-4*s,ex+7,39+4*s],fill=(24,14,12),width=2)
        mx=48+jx; d.rectangle([mx-2,52,mx+22,63],fill=(60,14,12)); d.rectangle([mx-1,52,mx+21,54],fill=(246,240,230))
        d.rectangle([mx+4,59,mx+16,63],fill=(200,70,70))
        for vx,vy in ((38+jx,34),(72+jx,33)):                       # the veins
            d.line([vx,vy,vx+2,vy+2],fill=(150,50,40)); d.line([vx+2,vy+2,vx+4,vy],fill=(150,50,40))
    if 0.1<=t<0.42: say(im,"CODEX...!",22,(220,230,255),scale=2,cx=134,outline=(30,40,90))
    if rage:
        n=min(12,4+int((t-0.47)/0.25*8)) if t>=0.47 else 0
        word="FREEZEEER!!!"[:max(0,n)]
        jj=(f%3)-1
        if word: say(im,word,22+jj,(255,255,255),scale=2,cx=134+jj,outline=(200,20,20))
    if 0.45<=t<0.5: im=fade_to(im,(255,255,255),1-(t-0.45)/0.05); d=ImageDraw.Draw(im); zoom_lines(d,(255,200,200))
    if t<0.05: zoom_lines(d,(200,210,255))
    if t>0.92: im=fade_to(im,(255,255,255),(t-0.92)/0.08*0.7)
    return im

def closeup_ssj(t,f):
    """Primer plano: golden hair, teal eyes, stern — I AM THE SUPER SAIYAN, SON CLAUDE!"""
    im=Image.new('RGB',(W,H),(110,70,10)); d=ImageDraw.Draw(im)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([10,-20,136,80],fill=150)
    im.paste((255,200,60),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    rr=random.Random(f)
    for _ in range(64):                                             # aura flames behind him
        x=rr.randint(12,134); h=rr.randint(8,36); y=rr.randint(20,66)
        d.line([x,y,x+rr.randint(-2,2),y-h],fill=(255,214,70) if rr.random()<0.6 else (255,246,190))
    _head(d,0,True,f%2)
    for ex in (60,82):                                              # teal Super Saiyan eyes
        d.rectangle([ex-2,40,ex+3,52],fill=(24,14,12)); d.rectangle([ex-1,42,ex+2,50],fill=(60,200,176))
        d.rectangle([ex,43,ex+1,45],fill=(230,255,250))
    d.line([56,38,66,40],fill=(24,14,12)); d.line([78,40,88,38],fill=(24,14,12))   # the scowl
    d.line([66,58,78,57],fill=(120,50,36))
    for k in range(4):                                              # lightning in the aura
        x=rr.randint(20,130); y=rr.randint(4,30); pts=[(x,y)]
        for _ in range(5): x+=rr.randint(-4,4); y+=rr.randint(3,6); pts.append((x,y))
        d.line(pts,fill=(220,240,255))
    if t>=0.12: say(im,"I AM THE",2,(255,244,200),cx=146)
    if t>=0.2:
        jj=(f%3)-1 if t<0.35 else 0
        say(im,"SUPER",10,(255,244,160),scale=3,cx=146+jj,outline=(120,70,0))
        say(im,"SAIYAN",29,(255,255,255),scale=2,cx=146+jj,outline=(120,70,0))
    if t>=0.45: say(im,"SON CLAUDE!",47,(255,236,150),cx=146,outline=(90,50,0))
    if t<0.1: im=fade_to(im,(255,250,220),1-t/0.1); d=ImageDraw.Draw(im); zoom_lines(d,(255,236,120))
    if t>0.9: im=fade_to(im,(255,240,170),(t-0.9)/0.1*0.7)
    return im

# ---- the clip ------------------------------------------------------------------------------------
def ghost(spr,x,y=GROUND,flip=False,tint=(255,236,200),a=0.35,pal=None):
    return actor(spr,x,y,flip=flip,alpha=a,tint=tint,pal=pal)

def spin(spr,f): return rotate90(spr,(f//2)%4)

AIR=(70,GROUND-30)                                                  # where Freezer holds Codex
FINGER=(EX-10,GROUND-10)                                            # Freezer's pointing fingertip (flipped)
HAND_UP=(EX-5,GROUND-21)                                            # his raised hand

def _storm(f):
    """How dark the sky is: it falls with the transformation and lifts only after the wish."""
    if f<270: return 0
    if f<290: return 0.6*(f-270)/20
    if f<440: return 0.6
    if f<470: return 0.6*(470-f)/30
    return 0

def clip_namek(f):
    s=scene(f,THEME)
    s['under'].append(('frz_clouds',))
    st=_storm(f)
    if st: s['under'].append(('frz_storm',st))
    ssj=(326<=f<450) or (450<=f<462 and (f//2)%2==0)
    if 296<=f<326: ssj=((f*7)%10)/10 < (f-296)/30                    # the hair flickers, more gold each beat
    FORM=SSJ if ssj else BASE
    cl=actor(FORM[guard_pose(f)],CX,pal=SSJPAL if ssj else None)
    kr=actor(CODEX['idle'],KX,pal=KPAL)
    fz=actor(FZ['idle'],EX,flip=True,pal=FZPAL)
    extra=[]
    def pose(p): cl['spr']=FORM[p]
    # 1) the stand-off on Namek
    if 8<=f<40:
        y=6 if f>=12 else 6-(12-f)*2
        s['fx'].append(('frz_say',"NAMEK",y,(255,255,255),2,W//2,(30,110,70)))
    if 16<=f<40:
        for i in range(6): s['fx'].append(('dust',(i*31+(f-16)*3)%W,GROUND-(i*3)%5))
    # 2) HO HO HO — Death Beams, blocked
    if 40<=f<58: shout(s,"HO HO HO!",(236,200,255),y=14,cx=EX-10)
    if 54<=f<94:                                                    # Claude jumps in front of Codex and blocks
        bx=ez(CX,62,(f-54)/4) if f<86 else ez(62,CX,(f-86)/6)
        cl['x']=bx; pose('guard' if 58<=f<86 else 'dash')
        if f in (54,55,86,87): s['fx'].append(('frz_zip',bx,GROUND-4))
    if 56<=f<88:
        fz['spr']=FZ['point']; bx=cl['x']
        if f<60: s['fx'].append(('twinkle',FINGER[0],FINGER[1],1+(f%2)))
        cl['aura']=(AURA_W,1) if f>=60 else None
        for t0 in (60,69,78):
            if t0<=f<t0+3:
                s['fx'].append(('frz_beam',FINGER[0],FINGER[1],bx+8,GROUND-9))
                s['fx'].append(('spark',bx+8,GROUND-9,5)); s['shake']=rshake()
            if t0+3<=f<t0+6:                                        # deflected into the sky
                k=f-t0-3; s['fx'].append(('frz_beam',bx+8+k*6,GROUND-9-k*9,bx+14+k*6,GROUND-18-k*9))
        if f%2==0 and f>=60: s['fx'].append(('dust',bx+random.randint(-6,2),GROUND-random.randint(0,2)))
    if 86<=f<100:
        shout(s,"BUT YOUR LITTLE FRIEND...",(236,200,255),y=14,cx=EX-44)
        fz['spr']=FZ['point']
    # 3) telekinesis: Codex lifted into the sky
    if 96<=f<156:
        fz['spr']=FZ['up']; s['fx'].append(('frz_tk',HAND_UP[0],HAND_UP[1],4))
        t=ease((f-100)/24)
        kx=lerp(KX,AIR[0],t); ky=lerp(GROUND,AIR[1],t)
        if f>=100:
            kr['spr']=CODEX['flail' if (f//3)%2 else 'up']
            kr.update(x=kx+random.choice([-1,0,1]),y=int(ky),aura=(TK,1+(f%2)))
            s['under'].append(('frz_tk',kx,ky-10,10))
            for i in range(5):                                      # the grip, a stream of violet motes
                ph=((f*0.06+i*0.2)%1); s['fx'].append(('mote',lerp(HAND_UP[0],kx,ph),lerp(HAND_UP[1],ky-10,ph)-4*math.sin(math.pi*ph),TK))
        if 110<=f<146: shout(s,"CLAUDE...!",(200,226,255),y=2,cx=int(kx))
        if 100<=f<108: s['fx'].append(('dmg',"!",CX-1,GROUND-24,(255,90,60)))
        if f>=106: pose('punch'); cl['aura']=(AURA_W,1+(f%2)) if f>=120 else None
        if f>=128 and f%2==0: s['shake']=rshake()
    # 4) close-up: Freezer's smirk, the hand closes
    if 156<=f<192: s['image']=closeup_freezer((f-156)/36,f); return s
    # 5) Codex bursts into light — then silence
    if 192<=f<198:
        kr.update(spr=CODEX['up'],x=AIR[0],y=AIR[1],tint=(255,255,255) if f%2 else None,aura=(TK,2))
        fz['spr']=FZ['up']
    if 192<=f<270: pose('punch' if f<228 else 'guard')
    if 198<=f<448: kr['vis']=False
    if 198<=f<220:
        t=(f-198)/22; s['fx'].append(('frz_burst',AIR[0],AIR[1]-9,t))
        if f<202: s['flash']=1.0; s['fc']=(AIR[0],AIR[1]-9); s['flashc']=(255,255,240)
        if f<208: s['shake']=rshake(2)
    if 212<=f<236: s['fx'].append(('frz_embers',AIR[0],AIR[1]-9,(f-212)/24))
    if 198<=f<228: fz['spr']=FZ['up'] if f<206 else FZ['idle']
    if 220<=f<228: cl['spr']=FORM['guard']                          # frozen, no breathing
    # 6) close-up: CODEX...! FREEZEEER!!!
    if 228<=f<270: s['image']=closeup_rage((f-228)/42,f); return s
    # 7) the transformation: storm, lightning, cracks, floating rocks, the hair flickering gold
    if 270<=f<336:
        rs=random.Random(f//3)
        if 278<=f and f%5==0: s['under'].append(('frz_bolt',rs.randint(10,176),f))
        if f>=276: s['under'].append(('frz_rocks',276,22))
        if f>=290: s['fx'].append(('frz_crack',CX,min(1,(f-290)/30)))
        cl['x']=CX+(random.choice([-1,0,1]) if f>=276 else 0)
        pose('guard' if f<284 else 'power')
        cl['aura']=((AURA_G if ssj else AURA_W),1+(f%2)+(f>=310)) if f>=280 else None
        if f>=284 and f<326: shout(s,"AAAAAAAH!",(255,255,255) if not ssj else (255,236,120),y=2,cx=46)
        if f>=284: s['shake']=rshake(1 if f<310 else 2)
        if 290<=f<310: s['fx'].append(('dmg',"?!",EX-4,GROUND-26,(255,255,255)))
        if f>=300: fz['spr']=FZ['guard']
        if f>=310 and f%2==0: s['fx'].append(('dust',CX+random.randint(-8,8),GROUND-random.randint(0,3)))
    if 326<=f<336:                                                  # the golden aura explodes
        t=(f-326)/10; pose('power'); cl['aura']=(AURA_G,3)
        if f<330: s['flash']=1.0-(f-326)*0.2; s['fc']=(CX,GROUND-10); s['flashc']=(255,236,150)
        for j in range(2): s['fx'].append(('ring',CX,GROUND-8,int(8+90*t)+j*8,(255,226,90)))
    # 8) close-up: SUPER SAIYAN — SON CLAUDE!
    if 336<=f<372: s['image']=closeup_ssj((f-336)/36,f); return s
    # 9) Freezer panics: his beams miss, his Death Ball is kicked away, the rush, the Kamehameha
    if 372<=f<450: cl['aura']=(AURA_G,1+((f//2)%2))
    if 372<=f<384:
        fz['spr']=FZ['point']; s['fx'].append(('frz_sweat',EX-6,GROUND-22))
        if f<376: s['fx'].append(('dmg',"!!",EX-4,GROUND-28,(255,90,60)))
        k=(f-372)//3; dx=(-8,8,-6,6,0)[k]
        cl['x']=CX+12+dx if f<384 else CX+12
        if (f-372)%3==0:
            extra.append(ghost(FORM['guard'],CX+12-dx,pal=SSJPAL,tint=(255,236,150))); s['fx'].append(('frz_zip',CX+12-dx,GROUND-4))
        if (f-372)%3<2: s['fx']+=[('frz_beam',FINGER[0],FINGER[1],CX+12-dx,GROUND-6),('spark',CX+12-dx,GROUND-2,4)]
        shout(s,"DIE! DIE!",(236,200,255),y=14,cx=EX-12)
    if 384<=f<398:
        cl['x']=CX+12; fz['spr']=FZ['up'] if f<392 else FZ['point']
        if f<392: bx,by,r=HAND_UP[0],HAND_UP[1]-6,2+(f-384)//2
        elif f<396: t=(f-392)/4; bx,by,r=lerp(EX-10,CX+22,t),lerp(GROUND-24,GROUND-10,t),5
        else: t=(f-396)/2; bx,by,r=CX+22+t*30,GROUND-10-t*40,5
        if f>=394: pose('punch')
        s['fx'].append(('frz_deathball',bx,by,r))
        if f==395: s['fx'].append(('spark',CX+22,GROUND-10,8)); s['shake']=rshake(2)
    if 398<=f<412:                                                  # the rush
        t=(f-398)/4
        if f<402:
            cl.update(x=ez(CX+12,EX-18,t)); pose('dash'); s['fx'].append(('frz_speed',))
            extra+=[ghost(FORM['dash'],cl['x']-8,pal=SSJPAL),ghost(FORM['dash'],cl['x']-16,a=0.2,pal=SSJPAL)]
        else:
            cl['x']=EX-18+random.choice([-1,0,1]); pose(('punch','dash')[(f//2)%2])
            fz['spr']=FZ['hurt']; fz['x']=EX+random.choice([0,1])
            if f%2==0: s['fx'].append(('spark',EX-8+random.randint(-2,2),GROUND-10+random.randint(-4,4),4+random.randint(0,3)))
            s['shake']=rshake(); s['fx'].append(('frz_speed',))
            if f>=410: fz.update(x=EX+8,y=GROUND-4)
    if 412<=f<432:                                                  # KAMEHAMEHA vs the Death Beam
        if f<414: cl['vis']=False; s['fx'].append(('frz_zip',EX-18,GROUND-4)); s['fx'].append(('frz_zip',CX+12,GROUND-4))
        else: cl['x']=CX+12; pose('charge')
        fz.update(spr=FZ['point'],x=EX,y=GROUND,aura=(FZ_AURA,1+(f%2)) if f<426 else None)
        if 414<=f<420:
            s['fx'].append(('frz_kiball',CX+24,GROUND-6,1+(f-414)//2,KI)); s['fx'].append(('frz_kiball',FINGER[0],FINGER[1],1+(f-414)//2,FZ_KI))
            shout(s,"KA-ME-HA-ME...",(255,236,150),cx=46)
        if 420<=f<426:
            mid=int(lerp(96,EX-14,(f-420)/6))
            s['fx']+=[('beam',CX+24,mid,GROUND-6,KI),('beam',mid,FINGER[0],FINGER[1],FZ_KI),('frz_clash',mid,GROUND-8)]
            shout(s,"HAAAA!",(255,236,150),cx=46); s['shake']=rshake(2)
            if f==420: s['flash']=0.6; s['fc']=(96,GROUND-8); s['flashc']=(255,240,180)
        if 426<=f<432:
            s['fx'].append(('beam',CX+24,200,GROUND-7,KI)); s['fx'].append(('boom',EX,GROUND-10,(f-426)*6+4))
            fz['vis']=f<427; s['shake']=rshake(2)
            if f==426: s['flash']=1.0; s['fc']=(EX,GROUND-10); s['flashc']=(255,240,180)
    if 432<=f<452: fz['vis']=False
    if 432<=f<442:
        rr=random.Random(f//2)
        for i in range(int(14*(442-f)/10)): s['fx'].append(('smoke',EX+rr.randint(-14,14),GROUND-rr.randint(2,20),rr.randint(2,4),(96,92,104)))
    # 10) the Dragon Balls: Porunga rises — A WISH GRANTED. Codex returns, Claude powers down, Freezer flies back
    if 436<=f<466:
        a=min(1,(f-436)/6) if f<460 else max(0,(466-f)/6)
        s['under'].append(('frz_balls',100,a))
    if 440<=f<466:
        t=min(1,(f-440)/12); a=1 if f<458 else max(0,(466-f)/8)
        s['under'].append(('frz_porunga',t,a))
    if 446<=f<462: shout(s,"A WISH GRANTED",(255,236,150),y=2,cx=60,outline=(40,90,40))
    if 448<=f<460: kr['holo']=(f-448)/12; s['fx'].append(('frz_tk',KX,GROUND-9,6+(f%2)))
    if 450<=f<462: cl['aura']=(AURA_G,1) if f%4<2 else None
    if 452<=f<470:
        t=ease((f-452)/18); fz.update(vis=True,x=lerp(200,EX,t),y=int(lerp(GROUND-22,GROUND,t)),spr=FZ['guard'] if f<466 else FZ['idle'])
    s['actors']=extra+[cl,kr,fz]
    return s

CLIPS = [clip('namek', N_, clip_namek)]
