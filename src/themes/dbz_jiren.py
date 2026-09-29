"""Dragon Ball sub-theme "dbz-jiren": Claude vs Jiren at the Tournament of Power — the broken stone
arena floating in the purple void, rubble drifting past, the Grand Priest watching from afar. Claude
rushes in and is swatted away; close-up of Jiren's red glare (YOU ARE WEAK.). Claude gets up, the
silver motes gather — close-up: the eyes open silver, ULTRA INSTINCT. Jiren's barrage only ever hits
afterimages, his point-blank blast too. Claude is behind him; a beat of silence; then instant hits
from everywhere at once, a last palm strike knocks Jiren clean off the arena. He leaps back in."""
from engine import *

THEME = 'dbz-jiren'
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

@fx('jiren_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,cx=W//2,outline=None):
    s['fx'].append(('jiren_say',txt,y,c,scale,cx,outline))

# ---- Jiren: the big grey head, black eyes, red and black Pride Trooper suit -----------------------
JIREN=poses(S([
"....DDDDDDD.......","...DDDDDDDDD......","..DDDDDDDDDDD.....","..DDKKKDKKKDD.....","..DDKKKDKKKDD.....",
"..DDDDDDDDDDD.....","...DDDdddDDD......","....DDDDDDD.......",".RRRRRRRRRRRRR....","RRRRRkkkkRRRRRR...",
"RRR.RRkkRR.RRRR...","RRR.RRkkRR.RRR....","DDD.RRkkRR.DDD....","HHH.kkkkkk.HHH....","....kkkkkk........",
"....kkk.kkk.......","....kkk.kkk.......","....kkk.kkk.......","....RR...RR.......","...RRR...RRR......",]),10,'RR',3)
JI_AURA=(255,70,60)
JI_KI=((255,160,160),(230,50,50))

# ---- Claude: Goku's spiky hair; Ultra Instinct = silver spikes and a silver aura -----------------
BASE=variant(lambda s: overlay(s,["..k..k.k.....",".kkk.kkkkk...","kkkkkkkkkkk.."],-2,0,bangs="..kk.k.kk"))
UI=variant(lambda s: overlay(s,["..H..H.H.....",".HvH.HHvHH...","HHHHHHHHHHH.."],-2,0,bangs="..HH.H.HH"))
UI_AURA=(210,222,255)
AURA_W=(236,240,255)
GHOST=(190,205,255)

# ---- background: the Tournament of Power -------------------------------------------------------
TOP=46                                                              # back edge of the arena
def _void(d):
    for y in range(TOP):                                            # the World of Void: violet dark
        k=y/(TOP-1); d.line([0,y,W,y],fill=(int(14+46*k),int(10+18*k),int(40+56*k)))
    for cx,cy,rx,ry,c in ((40,14,40,9,(40,24,78)),(40,14,24,5,(62,36,104)),(40,14,10,2,(96,66,150)),   # nebulae
                          (150,26,46,10,(36,34,86)),(150,26,26,5,(48,60,116)),(150,26,10,2,(80,110,170))):
        d.ellipse([cx-rx,cy-ry,cx+rx,cy+ry],fill=c)
    rr=random.Random(909)
    for _ in range(60): d.point((rr.randint(0,W-1),rr.randint(0,TOP-8)),fill=rr.choice([(200,200,240),(150,150,210),(255,255,255)]))
    # the Grand Priest's pillar in the far distance
    d.polygon([(86,40),(98,40),(96,20),(88,20)],fill=(70,64,110)); d.rectangle([84,18,100,20],fill=(96,90,140))
    d.rectangle([91,11,93,17],fill=(30,26,60)); d.rectangle([91,9,93,10],fill=(120,190,230)); d.point((92,8),fill=(240,240,255))
    d.ellipse([40,26,54,34],fill=(64,58,96)); d.ellipse([136,30,146,36],fill=(58,52,90))   # far floating rocks
    # the arena: pale stone tiles in perspective, a chunk broken off the right edge
    x0b,x1b,x0f,x1f=10,176,0,185
    d.polygon([(x0b,TOP),(x1b,TOP),(x1f,GROUND+1),(x0f,GROUND+1)],fill=(196,196,206))
    for y in (49,53): d.line([lerp(x0b,x0f,(y-TOP)/13),y,lerp(x1b,x1f,(y-TOP)/13),y],fill=(160,160,176))
    for i in range(-8,9): d.line([92+i*10,TOP,92+i*11.4,GROUND],fill=(160,160,176))
    d.polygon([(150,TOP),(176,TOP),(185,GROUND+1),(172,GROUND+1),(166,53),(158,50)],fill=(40,26,70))   # the gap
    for x,y in ((158,50),(166,53),(172,GROUND+1)): d.point((x,y),fill=(230,230,238))
    for pts in (((40,50),(46,53),(44,56),(52,58)),((110,48),(104,52),(112,55)),((130,54),(138,57))):   # cracks
        d.line(pts,fill=(110,110,128))
    d.line([x0b,TOP,150,TOP],fill=(236,236,244))
    d.rectangle([x0f,GROUND+1,171,H],fill=(126,124,146))           # front face, jagged underside
    d.line([x0f,GROUND+1,171,GROUND+1],fill=(226,226,236))
    for x in range(8,171,16): d.line([x,GROUND+2,x,H],fill=(96,94,116))
    for x,y in ((20,62),(44,61),(76,63),(120,61),(150,62)): d.point((x,y),fill=(70,60,96))
    d.polygon([(171,GROUND+1),(176,GROUND+1),(171,H)],fill=(40,26,70))
register_bg(THEME, lambda v: (v+140,v+140,v+160), decor=_void)

# ---- effects ------------------------------------------------------------------------------------
RUBBLE=[(10,12,4),(52,30,3),(96,6,2),(128,20,5),(170,36,3),(200,10,4),(66,40,2)]   # (x, y, size)
@fx('jiren_rubble')
def _fx_rubble(d,im,e,f):
    """Broken arena chunks floating through the void: one 225px lap per clip, bobbing."""
    o=f*225//N_
    for i,(x0,y,s) in enumerate(RUBBLE):
        x=(x0+o*(1 if i%2 else -1))%225-20; y=y+int(math.sin(f*6.2832*2/N_+i)*2)
        d.polygon([(x,y),(x+s*2,y-1),(x+s*3,y+s//2+1),(x+s,y+s+1),(x-1,y+s//2)],fill=(150,146,170))
        d.line([x,y,x+s*2,y-1],fill=(214,212,228)); d.line([x+s,y+s+1,x+s*3,y+s//2+1],fill=(90,86,112))

@fx('jiren_stars')
def _fx_stars(d,im,e,f):
    """A few stars twinkling in the void."""
    rr=random.Random(77)
    for i in range(12):
        x=rr.randint(0,W-1); y=rr.randint(0,34)
        if (f//4+i)%6==0: d.line([x-1,y,x+1,y],fill=(255,255,255)); d.line([x,y-1,x,y+1],fill=(255,255,255))   # 84 steps: loops

@fx('jiren_speed')
def _fx_speed(d,im,e,f):
    """Speed lines converging on a point."""
    _,x,y=e; rr=random.Random(f)
    for _ in range(10):
        a=rr.random()*6.28; r0=rr.randint(14,22); r1=r0+rr.randint(8,20)
        d.line([x+math.cos(a)*r0,y+math.sin(a)*r0*0.6,x+math.cos(a)*r1,y+math.sin(a)*r1*0.6],fill=(220,228,255))

@fx('jiren_streak')
def _fx_streak(d,im,e,f):
    """Horizontal speed streaks across the frame."""
    rr=random.Random(f*7)
    for _ in range(8):
        y=rr.randint(10,GROUND-2); x=rr.randint(0,W-20); d.line([x,y,x+rr.randint(10,24),y],fill=(255,255,255))

@fx('jiren_zip')
def _fx_zip(d,im,e,f):
    """A silver flicker where Claude just was."""
    _,x,y=e; rr=random.Random(f*3+int(x))
    for _ in range(4):
        yy=y+rr.randint(-10,2); xx=x+rr.randint(-6,6); d.line([xx-5,yy,xx+5,yy],fill=(255,255,255))
        d.line([xx-3,yy+1,xx+3,yy+1],fill=(170,190,255))

@fx('jiren_kiball')
def _fx_kiball(d,im,e,f):
    """A ki ball: x,y,r,(outer,mid), with a spiky corona."""
    _,x,y,r,(oc,mc)=e; ball(d,int(x),int(y),int(r),oc,mc,f); asterisk(d,int(x),int(y),int(r)+3,oc,f)

@fx('jiren_crack')
def _fx_crack(d,im,e,f):
    """Cracks spidering out of the arena floor around x (t 0..1)."""
    _,x,t=e; rr=random.Random(int(x)*5)
    for k in range(6):
        a=rr.uniform(-0.3,0.3)+(0 if k%2 else math.pi); L=int(4+22*t*rr.uniform(0.5,1)); px,py=x,GROUND-1
        pts=[(px,py)]
        for j in range(1,4): pts.append((px+math.cos(a)*L*j/3,py-rr.randint(0,3)*j/3))
        d.line(pts,fill=(90,86,110))

# ---- close-up: Jiren's glare --------------------------------------------------------------------
def closeup_jiren(t,f):
    """Primer plano: Jiren's grey face in a roaring red aura, the black eyes flaring red."""
    im=Image.new('RGB',(W,H),(40,6,8)); d=ImageDraw.Draw(im)
    rr=random.Random(f)
    for _ in range(60):
        x=rr.randint(0,140); h=rr.randint(8,40); y=rr.randint(16,70)
        d.line([x,y,x+rr.randint(-2,2),y-h],fill=(220,40,30) if rr.random()<0.6 else (255,130,90))
    d.ellipse([22,0,118,88],fill=(255,80,60))                       # the aura's rim light
    d.ellipse([24,2,116,90],fill=(170,170,184)); d.chord([24,2,116,90],110,250,fill=(140,140,156))   # the head
    d.line([42,21,68,29],fill=(110,110,124),width=2); d.line([100,21,74,29],fill=(110,110,124),width=2)        # heavy brow
    g=ease((t-0.25)/0.2)
    for ex,pts in ((56,((-12,27),(11,33),(9,44),(-10,42))),(86,((-11,33),(12,27),(10,42),(-9,44)))):   # huge black eyes, glaring
        d.polygon([(ex+x,y) for x,y in pts],fill=(10,8,12))
        if g>0:
            glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([ex-6,30,ex+6,42],fill=int(220*g))
            im.paste((255,40,30),(0,0),glow.filter(ImageFilter.GaussianBlur(2))); d=ImageDraw.Draw(im)
            d.rectangle([ex-1,35,ex+1,37],fill=(255,230,220))
    d.line([62,56,80,56],fill=(90,90,104))                          # a flat, unimpressed mouth
    d.rectangle([20,60,122,64],fill=(160,30,30)); d.rectangle([60,60,82,64],fill=(24,20,28))   # suit collar
    jx=((f%2)*2-1) if 0.25<t<0.5 else 0
    if t>0.35:
        say(im,"YOU ARE",14,(255,210,200),scale=2,cx=156+jx,outline=(120,10,10))
        say(im,"WEAK.",32,(255,255,255),scale=3,cx=156+jx,outline=(120,10,10))
    if t<0.06: zoom_lines(d,(255,120,100))
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

# ---- close-up: the eyes of Ultra Instinct -------------------------------------------------------
_HAIR=[(40,58,26,8),(50,70,52,-2),(62,84,80,-4),(76,98,106,4),(90,102,116,20),(40,50,24,22)]
_BANGS=[(50,62,56,40),(60,72,64,36),(78,90,86,38)]
def closeup_ui(t,f):
    """Primer plano: calm, eyes shut in a silver aura; they open silver — ULTRA INSTINCT."""
    awake=t>=0.35
    im=Image.new('RGB',(W,H),(30,34,70) if awake else (16,18,40)); d=ImageDraw.Draw(im)
    if awake:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([14,-20,130,84],fill=130)
        im.paste((180,196,255),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    rr=random.Random(f)
    for _ in range(60 if awake else 20):                            # silver flames, drifting slow
        x=rr.randint(10,136); h=rr.randint(6,30); y=rr.randint(18,66)
        c=(230,236,255) if rr.random()<0.5 else ((150,170,240) if awake else (70,80,140))
        d.line([x,y,x+rr.randint(-1,1),y-h],fill=c)
    col,edge=((226,230,244),(140,150,200)) if awake else ((30,28,40),(90,100,150))
    for x0,x1,tx,ty in _HAIR: d.polygon([(x0,30),(x1,30),(tx,ty)],fill=col,outline=edge)
    d.rectangle([40,22,104,30],fill=col)
    d.rectangle([44,30,100,64],fill=(217,119,87)); d.rectangle([44,30,50,64],fill=(176,92,66))
    for x0,x1,tx,ty in _BANGS: d.polygon([(x0,29),(x1,29),(tx,ty)],fill=col)
    if not awake:                                                   # eyes closed, serene
        for ex in (60,82): d.line([ex-4,47,ex+4,47],fill=(24,14,12)); d.point((ex-4,46),fill=(24,14,12))
    else:
        for ex in (60,82):                                          # silver irises, a white glint
            d.rectangle([ex-3,40,ex+4,52],fill=(24,14,12)); d.rectangle([ex-2,42,ex+3,50],fill=(196,206,230))
            d.rectangle([ex-1,43,ex+2,49],fill=(236,240,252)); d.rectangle([ex+1,43,ex+2,44],fill=(255,255,255))
        d.line([55,37,66,38],fill=(24,14,12)); d.line([78,38,89,37],fill=(24,14,12))   # level brows
    d.line([66,58,78,58],fill=(120,50,36))                          # a calm closed mouth
    if 0.35<=t<0.42:
        im=fade_to(im,(236,240,255),1-(t-0.35)/0.07); d=ImageDraw.Draw(im); zoom_lines(d,(220,228,255))
    if t>=0.44:
        say(im,"ULTRA",6,(236,240,255),scale=3,cx=148,outline=(60,70,140))
        say(im,"INSTINCT",28,(190,206,255),scale=2,cx=148,outline=(40,50,110))
        say(im,"MIGATTE NO GOKUI",46,(160,170,220),cx=148)
    if t<0.06: zoom_lines(d,(200,210,255))
    if t>0.9: im=fade_to(im,(230,236,255),(t-0.9)/0.1*0.6)
    return im

# ---- the clip -----------------------------------------------------------------------------------
def ghost(x,spr,flip=False,a=0.35,tint=GHOST,y=GROUND):
    return actor(spr,x,y,flip=flip,alpha=a,tint=tint)

def spin(spr,f): return rotate90(spr,(f//2)%4)

def clip_ultra(f):
    s=scene(f,THEME)
    s['under']+=[('jiren_stars',),('jiren_rubble',)]
    ui=128<=f<312 or (312<=f<324 and (f//2)%2==0)                   # powers down with a flicker
    FORM=UI if ui else BASE
    cl=actor(FORM[guard_pose(f)],CX,aura=(UI_AURA,1+((f//2)%2)) if ui else None)
    ji=actor(JIREN['idle'],EX,flip=True); extra=[]
    def pose(p): cl['spr']=FORM[p]
    # 1) the Tournament of Power
    if 8<=f<40:
        y=4 if f>=12 else 4-(12-f)*2
        s['fx'].append(('jiren_say',"TOURNAMENT",y,(255,255,255),2,W//2,(70,40,130)))
        if f>=16: shout(s,"OF POWER",(210,190,255),y=y+15)
    # 2) Jiren's aura flares; Claude rushes him and is swatted away
    if 36<=f<60:
        ji['aura']=(JI_AURA,1+(f%2)+(f>=44)); s['fx'].append(('jiren_crack',EX,min(1,(f-36)/14)))
        if f>=44 and f%2==0: s['shake']=rshake()
        if f%3==0: s['fx'].append(('rock',EX+random.randint(-20,20),GROUND-random.randint(0,14)))
    if 48<=f<58:
        t=(f-48)/10; cl.update(x=ez(CX,132,t),aura=(AURA_W,2)); pose('dash')
        extra+=[ghost(cl['x']-8,BASE['dash'],tint=(255,236,200)),ghost(cl['x']-16,BASE['dash'],a=0.2,tint=(255,236,200))]
        s['fx'].append(('jiren_streak',))
    if 58<=f<64:
        cl.update(x=132); pose('punch'); ji['aura']=(JI_AURA,2)
        if f==58: s['flash']=0.6; s['fc']=(141,GROUND-8)
        s['fx'].append(('ring',141,GROUND-8,(f-58)*5+3,(255,255,255))); s['shake']=rshake(2)
        s['fx'].append(('dmg',"...",EX-6,GROUND-28,(255,255,255)))
    if 64<=f<68: cl.update(x=132); pose('punch'); ji['spr']=JIREN['attack']
    if 66<=f<84:
        ji['spr']=JIREN['attack'] if f<72 else JIREN['idle']
        t=(f-66)/14; cl.update(x=ez(132,14,t),y=GROUND-int(12*math.sin(math.pi*min(1,t))),aura=None)
        cl['spr']=spin(BASE['hurt'],f) if f<78 else BASE['hurt']
        if f==66: s['flash']=0.8; s['fc']=(138,GROUND-8); s['flashc']=(255,200,190); s['fx'].append(('spark',138,GROUND-8,10))
        if f<70: s['shake']=rshake(2)
        if f>=78:
            for _ in range(2): s['fx'].append(('dust',cl['x']+random.randint(0,8),GROUND-random.randint(0,3)))
    if 84<=f<90: cl.update(x=14,spr=BASE['hurt'])
    # 3) close-up: Jiren's glare
    if 90<=f<114: s['image']=closeup_jiren((f-90)/24,f); return s
    # 4) Claude gets up; the silver motes gather — the awakening
    if 114<=f<128:
        cl.update(x=ez(14,CX,(f-118)/10),spr=BASE['hurt'] if f<120 else BASE['guard'])
        t=(f-114)/14
        for i in range(12):
            a=i*0.52+f*0.12; L=(1-t)*40+4
            s['fx'].append(('mote',cl['x']+math.cos(a)*L,GROUND-6+math.sin(a)*L*0.5,UI_AURA if i%2 else (150,180,255)))
        if f>=120: s['under'].append(('dim',0.3*(f-120)/8))
    if f==128: s['flash']=1.0; s['fc']=(CX,GROUND-8); s['flashc']=(225,232,255)
    if 128<=f<136:
        s['fx'].append(('ring',CX,GROUND-4,(f-128)*6,UI_AURA)); s['fx'].append(('ring',CX,GROUND-4,(f-128)*4,(255,255,255))); s['shake']=rshake()
    # 5) close-up: the eyes open silver
    if 136<=f<168: s['image']=closeup_ui((f-136)/32,f); return s
    if ui and f%3==0: s['fx'].append(('mote',cl['x']+random.randint(-8,8),cl['y']-random.randint(10,18),(170,200,255)))
    if 168<=f<180:
        ji.update(aura=(JI_AURA,2+(f%2))); shout(s,"HMPH.",(255,160,150),cx=EX-10)
    # 6) the barrage: every punch lands on an afterimage
    SW=[30,20,38,24,36,18,32]
    if 180<=f<186:
        ji.update(spr=JIREN['attack'],x=ez(EX,58,(f-180)/6),aura=(JI_AURA,2))
        extra.append(ghost(ji['x']+10,JIREN['attack'],flip=True,tint=(255,150,140))); s['fx'].append(('jiren_streak',))
    if 186<=f<228:
        k=min(6,(f-186)//6); ph=(f-186)%6
        ji.update(spr=JIREN['attack'] if ph<3 else JIREN['idle'],x=58+(1 if ph<3 else 0),aura=(JI_AURA,1+(f%2)))
        prev,nxt=SW[k],SW[(k+1)%7]
        cl['x']=nxt if ph>=1 else prev
        if ph<3: extra.append(ghost(prev,UI['guard'],a=0.5-ph*0.12))
        if ph==1:
            s['fx'].append(('mote',46,GROUND-7,(255,255,255))); s['fx'].append(('ring',46,GROUND-8,5,(255,190,180)))
        if ph<4: s['fx'].append(('dmg',"MISS",36+(k%3)*4,GROUND-26-ph,(200,210,240)))
        if f%6==0: s['shake']=rshake()
    if 186<=f<228 and f>=200: shout(s,"TOO SLOW",(220,228,255),cx=46,y=10)
    # the point-blank blast
    if 228<=f<238:
        ji.update(spr=JIREN['attack'],x=58,aura=(JI_AURA,2))
        s['fx'].append(('jiren_kiball',lerp(46,-10,(f-228)/10),GROUND-8,4,JI_KI))
        if f==230: s['flash']=0.5; s['fc']=(40,GROUND-8); s['flashc']=(255,200,190)
        cl['x']=32; cl['vis']=f<232 and f%2==0
        if f>=230: extra.append(ghost(32,UI['guard'],a=0.5)); s['fx'].append(('jiren_zip',32,GROUND-4))
    # 7) gone — Jiren searches — and Claude is behind him. A beat of silence.
    if 238<=f<256:
        cl['vis']=False; ji.update(spr=JIREN['idle'],x=58,flip=not(244<=f<250))
        if f>=242: s['fx'].append(('dmg',"?",57,GROUND-30,(255,255,255)))
    if 250<=f<256: s['fx'].append(('twinkle',80,GROUND-8,1+(f%2)))
    if 256<=f<270:
        cl.update(vis=True,x=80,flip=True); pose('guard'); ji.update(x=58,flip=f<264)
        s['under'].append(('dim',0.35)); s['fx'].append(('dmg',"!",57,GROUND-30,(255,255,255)))
    # 8) instant hits from everywhere
    if 270<=f<300:
        rr=random.Random(f*5); lift=int(6*ease((f-270)/20))
        ji.update(spr=JIREN['hurt'],x=58+rr.randint(-1,1),y=GROUND-lift-rr.randint(0,1),flip=True)
        cl['vis']=False
        for j in range(4):
            gx=58+rr.choice([-20,-15,15,20]); gy=GROUND-lift+rr.choice([0,0,-8,-14])
            extra.append(ghost(gx,UI[rr.choice(['punch','dash'])],flip=gx>58,a=0.55,tint=None,y=gy))
        for j in range(3): s['fx'].append(('spark',58+rr.randint(-8,8),GROUND-lift-rr.randint(4,18),rr.randint(2,4)))
        s['fx'].append(('jiren_speed',58,GROUND-lift-10))
        if f%4==0: s['fx'].append(('ring',58,GROUND-lift-10,6+(f%8),UI_AURA)); s['shake']=rshake(2)
        s['fx'].append(('dmg',str((f-270)*61+17),118,GROUND-32,(230,236,255)))
    # the last palm strike: off the arena
    if 300<=f<312:
        cl.update(vis=True,x=42,flip=False); pose('punch')
        ji.update(spr=JIREN['hurt'],x=lerp(58,210,(f-300)/10),y=GROUND-6-(f-300))
        if f==300: s['flash']=1.0; s['fc']=(54,GROUND-10); s['flashc']=(225,232,255); s['fx'].append(('boom',56,GROUND-10,10))
        if f<306: s['shake']=rshake(2)
        for j in range(3): s['fx'].append(('tracer',ji['x']-30-j*6,ji['x']-8,ji['y']-10+j*3))
        shout(s,"HAA!",(220,228,255),cx=42,y=20)
    # 9) Ultra Instinct fades; Jiren leaps back onto the arena
    if 312<=f<330: cl.update(x=ez(42,CX,(f-312)/16)); pose('guard' if f<318 else guard_pose(f))
    if 312<=f<320: ji['vis']=False
    if 320<=f<332:
        t=(f-320)/10; ji.update(spr=JIREN['idle'],x=ez(200,EX,t),y=int(min(GROUND,lerp(GROUND-30,GROUND,t)-14*math.sin(math.pi*min(1,t)))))
        if f==330:
            for j in range(4): s['fx'].append(('dust',EX+random.randint(-8,8),GROUND-random.randint(0,3)))
    s['actors']=extra+[cl,ji]
    return s

CLIPS = [clip('ultra', N_, clip_ultra)]
