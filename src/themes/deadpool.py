"""Deadpool: Claude as Deadpool vs Wolverine, in the Void (Deadpool & Wolverine).
SNIKT. Katanas vs claws; an arm pops off and a tiny one grows back. Then Deadpool turns to us, in his
yellow boxes: A NOTCH? SERIOUSLY? — and knocks on the top edge of the panel. Close-up: MAXIMUM EFFORT.
He offers a chimichanga; Wolverine takes it and leaves: BUB."""
from engine import *

THEME = 'deadpool'
N_ = 376

RED, RED_D = (196,30,40), (128,16,26)
BOX, INK = (250,220,70), (20,16,16)
# Deadpool: red suit, black patches round white eyes, katana hilts over the shoulders
DPAL = {'r':RED, 'R':RED_D, 'x':(18,16,18), 'e':(250,250,250), 'h':(120,120,130)}
# Wolverine (Deadpool & Wolverine): yellow suit, blue, the mask's black wings
WPAL = {'y':(236,196,40), 'b':(44,74,160), 'P':(226,182,140), 'W':(250,250,250)}

EYES = {                     # which of the 2x2 eye pixels are white, per expression (top row, bottom row)
    'normal':  ('11','11'),
    'happy':   ('11','00'),
    'angry':   ('01','11'),  # the inner top pixel goes dark: a frown (mirrored for the other eye)
    'squint':  ('00','11'),
}

def _deadpool(spr, mood='normal'):
    g=[list(r) for r in overlay(spr,["h.......h"],0,0)]            # katana hilts over the shoulders
    ks=sorted((x,y) for y,row in enumerate(g) for x,c in enumerate(row) if c=='K')
    for y,row in enumerate(g):
        for x,c in enumerate(row):
            if c=='O': g[y][x]='r'
            elif c=='o': g[y][x]='R'
    if ks:
        cols=sorted({x for x,_ in ks}); y0=min(y for _,y in ks)
        top,bot=EYES[mood]
        for i,cx in enumerate(cols):                                # one eye per K column
            for dy in (-1,0,1,2):                                   # the black patch
                for dx in (-1,0,1):
                    yy,xx=y0+dy,cx+dx
                    if 0<=yy<len(g) and 0<=xx<len(g[0]) and g[yy][xx] in 'rR': g[yy][xx]='x'
            t=top if i==0 else top[::-1]
            g[y0][cx]='e' if t[0]=='1' else 'x'
            g[y0+1][cx]='e' if bot[0]=='1' else 'x'
    return S([''.join(r) for r in g])
DP={mood:variant(lambda s,m=mood: _deadpool(s,m)) for mood in EYES}

def _no_arm(spr):
    """The guard pose with the raised arm gone (it popped off)."""
    g=[list(r) for r in spr]; w=len(g[0])
    for y in range(len(g)):
        for x in range(w-4,w):
            if g[y][x]=='R': g[y][x]='.'
    return S([''.join(r) for r in g])
ARMLESS={mood:_no_arm(DP[mood]['guard']) for mood in EYES}

WOLV=poses(S([
"..bb.......bb...","..bbb.....bbb...","...bbyyyyybb....","....ykWkWky.....","....yPPPPPy.....",
".....PPPPP......","......PkP.......","...bbyyyyybb....","..bbbyyyyybbb...","..PbyyyyyyybP...",
"..PyyybbbyyyP...","..P.yyybyyy.P...","....yyyyyyy.....","....bbbbbbb.....","....bb...bb.....",
"....bb...bb.....","....bb...bb.....","...kkk...kkk....",]),9,'P',4)

def _void(d):
    """The Void: dusty orange sky, dunes, a giant half-buried skull and wreckage."""
    for y in range(0,GROUND):
        v=int(34+30*y/GROUND); d.line([0,y,W,y],fill=(v+24,v,v//2))
    d.polygon([(0,GROUND),(0,48),(30,44),(70,50),(110,42),(150,48),(185,44),(185,GROUND)],fill=(92,62,40))
    d.ellipse([88,22,124,52],fill=(120,100,80)); d.rectangle([94,40,118,50],fill=(120,100,80))   # the skull
    d.ellipse([96,30,104,38],fill=(50,34,24)); d.ellipse([108,30,116,38],fill=(50,34,24))
    for x in range(98,116,4): d.rectangle([x,46,x+2,50],fill=(80,64,50))
    d.polygon([(150,48),(156,30),(160,31),(156,48)],fill=(70,60,56))                             # wreckage
    d.line([20,44,26,34],fill=(80,70,62)); d.line([26,34,34,36],fill=(80,70,62))
register_bg(THEME, lambda v: (v+20,v*2//3+10,v//3+6), decor=_void)

@fx('dp_box')
def _fx_box(d,im,e,f):
    """Deadpool's yellow caption boxes (one or more lines), centred at x."""
    _,lines,cx,y=e
    lines=[lines] if isinstance(lines,str) else lines
    w=max(len(l) for l in lines)*4+5; h=len(lines)*7+3; x=int(cx-w/2)
    x=max(1,min(W-w-1,x))
    d.rectangle([x,y,x+w,y+h],fill=BOX,outline=INK)
    for i,l in enumerate(lines): text(d,l,x+3,y+2+i*7,INK,shadow=None)

@fx('dp_bubble')
def _fx_bubble(d,im,e,f):
    """A white speech balloon (Wolverine), tail down towards the speaker."""
    _,txt,cx,y=e; w=len(txt)*4+5; x=max(1,min(W-w-2,int(cx-w/2))); cx=max(x+3,min(x+w-3,cx))
    d.rectangle([x,y,x+w,y+9],fill=(250,250,250),outline=INK); d.polygon([(cx-2,y+9),(cx+2,y+9),(cx+3,y+13)],fill=(250,250,250))
    text(d,txt,x+3,y+2,INK,shadow=None)

@fx('dp_katana')
def _fx_katana(d,im,e,f):
    _,hx,hy,a=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
    d.line([hx-c*2,hy-s*2,hx,hy],fill=(40,40,44))
    d.line([hx+c,hy+s,hx+13*c,hy+13*s],fill=(214,220,236)); d.point((hx+13*c,hy+13*s),fill=(255,255,255))

@fx('dp_claws')
def _fx_claws(d,im,e,f):
    """Three adamantium claws out of the fist (pointing left: Wolverine faces left)."""
    _,x,y,L=e
    for k in (-2,0,2): d.line([x,y+k,x-L,y+k-1],fill=(200,206,220))

@fx('dp_arm')
def _fx_arm(d,im,e,f):
    """The arm that popped off, tumbling."""
    _,x,y,k=e; a=k*0.8; c,s=math.cos(a)*3,math.sin(a)*3
    d.line([x-c,y-s,x+c,y+s],fill=RED_D); d.point((x+c,y+s),fill=RED)

@fx('dp_tinyarm')
def _fx_tinyarm(d,im,e,f):
    _,x,y=e; d.point((x,y),fill=RED_D); d.point((x+1,y-1),fill=RED)

@fx('dp_chimi')
def _fx_chimi(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.rectangle([x,y-1,x+5,y+1],fill=(214,164,90)); d.line([x+1,y-1,x+4,y-1],fill=(240,200,130))

@fx('dp_dust')
def _fx_dust(d,im,e,f):
    """Dust falling from the top edge of the panel where Deadpool knocked."""
    _,x,k=e; rr=random.Random(515)
    for i in range(14):
        px=x+rr.uniform(-14,14); py=k*rr.uniform(0.8,1.6)+rr.uniform(0,3)
        if py<GROUND: d.point((int(px),int(py)),fill=(200,180,150) if i%2 else (150,130,110))

GRIP = {'punch':(16,5), 'dash':(16,5), 'charge':(15,5)}

def closeup_effort(t,f):
    """Primer plano: the mask; the eyes narrow; MAXIMUM / EFFORT."""
    im=Image.new('RGB',(W,H),(30,18,14)); d=ImageDraw.Draw(im)
    for i in range(0,64,4): d.line([0,i,W,i],fill=(40,24,18))
    d.rectangle([22,6,86,64],fill=RED); d.rectangle([80,6,86,64],fill=RED_D)
    d.line([54,6,54,64],fill=RED_D)                                           # the mask's seam
    sq=ease((t-0.25)/0.3)                                                     # the eyes narrow
    for x0,flip in ((30,False),(58,True)):
        d.polygon([(x0-2,20),(x0+22,20),(x0+20,42),(x0,42)],fill=(18,16,18))
        top=24+int(9*sq); bot=37
        if flip: d.polygon([(x0+3,top+3),(x0+17,top),(x0+17,bot),(x0+3,bot)],fill=(250,250,250))
        else:    d.polygon([(x0+3,top),(x0+17,top+3),(x0+17,bot),(x0+3,bot)],fill=(250,250,250))
    for j,w in enumerate(("MAXIMUM","EFFORT")):
        if t>=0.45+j*0.15: FX['big'](d,im,('big',w,14+j*18,(250,250,250) if j==0 else BOX,138),f)
    if t<0.06: zoom_lines(d)
    return im

WX=150

def clip_bub(f):
    """Text holds follow ~1 s + 0.3 s per word (min 1.5 s at 20 fps), so every line can be read."""
    s=scene(f,THEME)
    x,y,pose,mood,flip=30,GROUND,guard_pose(f),'normal',False
    wx,wpose,claws=None,'idle',0
    armless=False
    # 1) Wolverine walks in; SNIKT
    if 14<=f<338: wx=ez(210,WX,(f-14)/20) if f<34 else WX
    if 30<=f<54: callout(s,"SNIKT",c=(236,236,244)); mood='angry'
    if f>=32: claws=min(8,(f-32)*2)
    # 2) the fight; the arm pops off, a tiny one grows back
    if 40<=f<48: pose,x,mood='dash',ez(30,124,(f-40)/8),'angry'
    if 48<=f<66:
        x,mood=124,'angry'; k=(f-48)%8; pose='punch' if k<4 else 'guard'; wpose='attack' if 3<=k<7 else 'idle'
        if k in (2,3): s['fx'].append(('spark',136,GROUND-7,3+k))
    if 66<=f<72: x,pose,mood=124,'hurt','normal'
    if 66<=f<86: callout(s,"POP!",c=BOX)
    if 66<=f<110:
        k=min(14,f-66); p=k/14
        s['fx'].append(('dp_arm',lerp(128,70,p),GROUND-8-18*math.sin(p*math.pi) if f<80 else GROUND-2,k))
    if 72<=f<110:
        x,armless,mood=124,True,'squint'
        s['fx'].append(('dp_tinyarm',127,GROUND-7))
        if 76<=f<106: s['fx'].append(('dp_box','OH COME ON.',x,4))                       # 1.5 s
    if 106<=f<110: s['fx'].append(('twinkle',128,GROUND-8,2))
    # 3) the fourth wall
    if 110<=f<118: pose,x,flip=guard_pose(f),ez(124,70,(f-110)/8),True
    if 118<=f<228: x,mood=70,'happy'
    if 118<=f<158: s['fx'].append(('dp_box',["A NOTCH?","SERIOUSLY?"],x,4))                 # 2 s
    if 158<=f<168:
        p=(f-158)/10; pose='armsup'; y=GROUND-int(40*math.sin(p*math.pi)); mood='angry'
        if 162<=f<166: s['shake']=rshake(2); s['fx'].append(('spark',70,1,3))
    if 162<=f<182: s['fx'].append(('dp_dust',70,f-162))
    if 168<=f<228: s['fx'].append(('dp_box',["I AM LITERALLY","CLAUDE. IN A NOTCH."],x,4))   # 3 s
    if 118<=f<228 and wx is not None: s['fx'].append(('dp_bubble','...',WX,12))
    # 4) close-up
    if 228<=f<268: s['image']=closeup_effort((f-228)/40,f); return s
    # 5) two more blows, the chimichanga, BUB.
    if 268<=f<276: pose,x,mood='dash',ez(70,124,(f-268)/8),'angry'
    for c0 in (278,284):
        if c0<=f<c0+4:
            pose,x,wpose='punch',124,'attack'
            if f<c0+2: s['fx'].append(('spark',136,GROUND-7,4))
    if 276<=f<290 and pose not in ('punch','dash'): x,pose=124,guard_pose(f)
    chimi=None
    if 290<=f<322:
        x,pose,mood=124,'punch','happy'
        hx,hy=hand_at(DP[mood]['punch'],x,GROUND,False,16,5,h=11); chimi=(hx,hy-1)
        if f<320: s['fx'].append(('dp_box','CHIMICHANGA?',x,4))                           # 1.5 s
    if 322<=f<352:
        wx=ez(WX,215,(f-322)/24); wpose='idle'; chimi=(wx-10,GROUND-10)
        s['fx'].append(('dp_bubble','BUB.',wx,12))                                # 1.5 s
        x,pose,mood=124,guard_pose(f),'squint'
    if chimi: s['fx'].append(('dp_chimi',*chimi))
    # 6) wave, back to the neutral pose
    if 352<=f<364: x,flip,pose,mood=ez(124,30,(f-352)/12),True,guard_pose(f),'happy'
    if 364<=f<370: x,pose,mood,flip=30,'armsup','happy',False
    if f>=370: x,flip=30,False
    acts=[]
    if wx is not None and wx<W+10:
        acts.append(actor(WOLV[wpose],wx,flip=True,pal=WPAL))
        if claws: s['fx'].append(('dp_claws',wx-8-(4 if wpose=='attack' else 0),GROUND-9,claws))
    spr=ARMLESS[mood] if armless else DP[mood][pose]
    acts.append(actor(spr,x,y,flip=flip,pal=DPAL))
    if pose in GRIP and not armless and chimi is None:
        hx,hy=hand_at(DP[mood][pose],x,int(y),flip,*GRIP[pose],h=11)
        s['fx'].append(('dp_katana',hx,hy,180 if flip else 0))
    s['actors']=acts
    return s

CLIPS = [clip('bub', N_, clip_bub)]
