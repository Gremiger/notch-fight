"""Claude vs Clippy — DEATH MATCH, on a Windows 98 / Office 97 desktop (teal wallpaper, a grey
Word window full of code, the Recycle Bin, the taskbar). Clippy pops up on his yellow notepad:
IT LOOKS LIKE YOU ARE WRITING CODE. NEED HELP? [YES] [NO]. Claude punches NO. He comes back
angrier (ARE YOU SURE? [YES] [YES]), Claude smashes the balloon and Clippy grows HUGE. He throws
error dialogs, shape-shifts (a bicycle, a bell, a question mark — he really did that), spams
NEED HELP? all over the screen. Close-up on his crazy googly eyes. Claude combos him back to size,
hits END TASK on CLIPPY.EXE IS NOT RESPONDING, bends him straight and drops him in the Recycle
Bin, which rattles one last HELP? before Claude empties it. Back to guard on a quiet desktop."""
from engine import *

THEME = 'clippy'
N_ = 360
CX = 30                                                            # Claude's spot in the neutral pose

# ---- background: the Win98 desktop ------------------------------------------------------------
TEAL=(0,128,128); GREY=(192,192,192); DGREY=(128,128,128); NAVY=(0,0,128); WHITE=(255,255,255); INK=(0,0,0)
WIN=(46,3,134,44)                                                  # the Word window behind the fight

def bevel(d,x0,y0,x1,y1,fill=GREY,sunken=False):
    """A Win98 3D box: light top-left, dark bottom-right (swapped when sunken)."""
    lt,dk=(DGREY,WHITE) if sunken else (WHITE,DGREY)
    d.rectangle([x0,y0,x1,y1],fill=fill)
    d.line([x0,y0,x1,y0],fill=lt); d.line([x0,y0,x0,y1],fill=lt)
    d.line([x0,y1,x1,y1],fill=dk); d.line([x1,y0,x1,y1],fill=dk)

def window(d,x0,y0,x1,y1,title,title_c=NAVY,body=GREY):
    """A Win98 window frame: bevel, blue title bar with its caption and the [x] box."""
    bevel(d,x0,y0,x1,y1,fill=body)
    d.rectangle([x0+1,y0+1,x1-1,y0+7],fill=title_c)
    text(d,title,x0+3,y0+2,WHITE,shadow=None)
    bevel(d,x1-7,y0+2,x1-2,y0+6)
    d.point((x1-5,y0+4),fill=INK); d.point((x1-4,y0+4),fill=INK)

def _desk(d):
    d.rectangle([0,0,W,H],fill=TEAL)
    x0,y0,x1,y1=WIN
    window(d,x0,y0,x1,y1,"CODE.DOC - WORD")
    d.line([x0+2,y0+9,x1-2,y0+9],fill=DGREY)                        # the toolbar
    for i,c in enumerate(((0,0,160),(160,0,0),(0,120,0),(120,120,0),(0,0,0),(128,0,128))):
        d.rectangle([x0+3+i*5,y0+10,x0+5+i*5,y0+12],fill=c)
    d.rectangle([x0+3,y0+14,x1-3,y1-2],fill=WHITE)                  # the page, with code on it
    rr=random.Random(98); cols=((0,0,170),(0,120,0),(150,0,120),(90,90,90),(170,60,0))
    for j in range(8):
        y=y0+16+j*3; x=x0+5+(rr.randint(0,3) if j%3 else 0)*3
        while x<x1-8 and y<y1-3:
            w=rr.randint(2,9); d.line([x,y,min(x+w,x1-6),y],fill=rr.choice(cols)); x+=w+2
    d.rectangle([0,GROUND+1,W,H],fill=GREY); d.line([0,GROUND+1,W,GROUND+1],fill=WHITE)   # taskbar
    bevel(d,1,GROUND+2,24,H-1)
    for (dx,dy),c in zip(((0,0),(2,0),(0,2),(2,2)),((230,40,20),(40,180,40),(30,90,230),(250,210,20))):
        d.rectangle([3+dx,GROUND+2+dy,4+dx,GROUND+3+dy],fill=c)     # the flag
    text(d,"START",8,GROUND+2,INK,shadow=None)
    bevel(d,W-20,GROUND+2,W-2,H-1,sunken=True); text(d,"4:20",W-18,GROUND+2,INK,shadow=None)
register_bg(THEME, lambda v: GREY, decor=_desk)

# ---- Clippy -----------------------------------------------------------------------------------
# Sprites are drawn with PIL shapes on an index image, then turned into a char grid for draw().
_IDX='.cCWkYyrgGbB'
CLPAL={'c':(222,226,236),'C':(128,134,152),'W':(255,255,255),'k':(12,12,16),'Y':(252,236,120),'y':(206,176,64),
       'r':(230,30,30),'g':(242,196,56),'G':(170,120,20),'b':(120,120,120),'B':(70,70,70)}
def _grid(w,h,fn):
    m=Image.new('L',(w,h),0); fn(ImageDraw.Draw(m),lambda ch: _IDX.index(ch))
    return S([''.join(_IDX[m.getpixel((x,y))] for x in range(w)) for y in range(h)])

def _eyes(d,I,cx,y,look=(0,0),mood='idle',sep=4,r=3,blink=False):
    """The googly eyes (two white discs, black pupils looking `look`) and the eyebrows:
    idle = raised arches, angry = a V, crazy = pupils rolling apart, red rims."""
    for k,ex in enumerate((cx-sep,cx+sep)):
        if blink: d.line([ex-r,y,ex+r,y],fill=I('k')); continue
        d.ellipse([ex-r,y-r,ex+r,y+r],fill=I('W'),outline=I('r') if mood=='crazy' else I('k'))
        lx,ly=look if mood!='crazy' else ((-1,-1),(1,1))[k]
        px,py=ex+lx*(r-2),y+ly*(r-2); d.rectangle([px-1+(k==0),py-1,px+(k==0),py],fill=I('k')) if r<4 else \
            d.ellipse([px-r//2,py-r//2,px+r//2,py+r//2],fill=I('k'))
        by=y-r-2; o=-1 if k==0 else 1
        if mood=='idle': d.line([ex-2,by+1,ex,by-1,ex+2,by+1],fill=I('k'))
        else: d.line([ex-2*o,by-1,ex+2*o,by+2],fill=I('k'))        # the angry V over the nose

def _clippy_raw(look=(0,0),mood='idle',blink=False,straight=0.0):
    """Clippy on his notepad, 17x30. straight 0..1 bends the wire into a straight rod (the finisher)."""
    def fn(d,I):
        d.polygon([(1,26),(15,26),(16,29),(0,29)],fill=I('Y'))      # the yellow notepad
        d.line([2,27,14,27],fill=I('y')); d.line([1,28,15,28],fill=I('y'))
        if straight<=0:
            d.rounded_rectangle([3,5,13,26],radius=5,outline=I('C'),width=2)     # outer loop
            d.rounded_rectangle([5,9,11,23],radius=3,outline=I('c'),width=2)     # inner loop
            d.line([5,9,5,14],fill=I('.')); d.line([6,9,6,14],fill=I('.'))       # the open end
            d.rounded_rectangle([4,6,12,25],radius=4,outline=I('c'),width=1)
        else:                                                   # bent open: loops unroll to a rod
            h=int(lerp(21,24,straight)); a=int(lerp(4,0,straight))
            d.line([8-a,26,8,26-h],fill=I('c'),width=2); d.line([8+a,26,8,26-h+4],fill=I('C'),width=2)
        _eyes(d,I,8,8,look,mood,blink=blink)
    return _grid(17,30,fn)

def scale2(spr): return S([''.join(c*2 for c in r) for r in spr for _ in (0,1)])

# ---- his other shapes (he really did turn into these), googly eyes always on -------------------
def _bike():
    def fn(d,I):
        for hx in (5,21): d.ellipse([hx-5,11,hx+5,21],outline=I('c'))                  # the wheels
        d.line([5,16,13,16,11,9,5,16],fill=I('C')); d.line([11,9,20,9,13,16],fill=I('C'))
        d.line([20,9,21,16],fill=I('c')); d.line([19,7,23,7],fill=I('c')); d.line([10,8,12,8],fill=I('k'))
        _eyes(d,I,15,6,(-1,0),'angry',sep=4,r=3)
    return _grid(27,22,fn)
def _bell(ang=0):
    def fn(d,I):
        d.ellipse([8,1,11,4],fill=I('G')); d.pieslice([3,3,16,20],180,360,fill=I('g'))
        d.polygon([(3,11),(16,11),(18,18),(1,18)],fill=I('g')); d.line([1,18,18,18],fill=I('G'))
        d.line([2,17,17,17],fill=I('G')); d.ellipse([7,19,11,22],fill=I('G'))              # rim, clapper
        _eyes(d,I,9,11,(-1,0),'angry',sep=4,r=3)
    m=Image.new('L',(20,24),0); fn(ImageDraw.Draw(m),lambda ch: _IDX.index(ch))
    m=m.rotate(ang,resample=Image.NEAREST,center=(9,2))
    return S([''.join(_IDX[m.getpixel((x,y))] for x in range(20)) for y in range(24)])
def _qmark(dot=True):
    def fn(d,I):
        d.arc([1,3,15,17],180,90,fill=I('c'),width=2); d.line([8,17,8,23],fill=I('c'),width=2)
        d.line([9,18,9,23],fill=I('C'))
        if dot: d.ellipse([6,26,10,30],fill=I('c'),outline=I('C'))
        _eyes(d,I,8,8,(-1,0),'angry',sep=4,r=3)
    return _grid(17,31,fn)
BIKE=_bike(); BELL=[scale2(_bell(a)) for a in (-14,0,14,0)]; QM=scale2(_qmark()); QM0=scale2(_qmark(False))

# ---- text with a real M (the 3x5 font's M reads as H) -----------------------------------------
_M5=["10001","11011","10101","10001","10001"]
def _mask(txt):
    w=sum(6 if ch=='M' else 4 for ch in txt); m=Image.new('L',(max(1,w),6),0); x=0
    for ch in txt:
        if ch=='M':
            for j,r in enumerate(_M5):
                for i,b in enumerate(r):
                    if b=='1': m.putpixel((x+i,j),255)
            x+=6; continue
        for j,b in enumerate(FONT.get(ch,FONT[' '])):
            if b=='1': m.putpixel((x+j%3,j//3),255)
        x+=4
    return m
def big(im,txt,y,c,scale=2,cx=W//2,ol=(20,10,30)):
    m=_mask(txt).resize((_mask(txt).width*scale,6*scale),Image.NEAREST); x=int(cx-m.width//2); y=int(y)
    for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1),(2,2)): im.paste(ol,(x+dx,y+dy),m)
    im.paste(c,(x,y),m)

# ---- effects ---------------------------------------------------------------------------------
BALLOON=(255,255,204)
def _button(d,x0,y0,label,pressed=False):
    w=len(label)*4+5; bevel(d,x0,y0,x0+w,y0+8,sunken=pressed)
    if not pressed: d.line([x0+1,y0+7,x0+w-1,y0+7],fill=DGREY)
    text(d,label,x0+3+pressed,y0+2+pressed,INK,shadow=None); return x0+w

@fx('clippy_balloon')
def _fx_balloon(d,im,e,f):
    """The pale-yellow help balloon: lines typed out up to n chars, buttons, tail to Clippy. grow 0..1."""
    _,lines,n,buttons,pressed,grow=e
    x0,y0,x1,y1=58,12,141,47
    if grow<1:
        cx,cy=x1,y1; x0,y0=int(lerp(cx,x0,grow)),int(lerp(cy,y0,grow))
        if grow<=0: return
    d.polygon([(x1-10,y1),(x1-2,y1),(x1+7,y1+(GROUND-y1)//2-3)],fill=BALLOON,outline=INK)
    d.rounded_rectangle([x0,y0,x1,y1],radius=4,fill=BALLOON,outline=INK); d.line([x1-9,y1,x1-3,y1],fill=BALLOON)
    if grow<1: return
    for j,ln in enumerate(lines):
        k=max(0,min(len(ln),n)); n-=len(ln); text(d,ln[:k],x0+5,y0+4+j*6,INK,shadow=None)
    if buttons:
        x=x0+8
        for i,b in enumerate(buttons): x=_button(d,x,y1-11,b,pressed==i)+6

@fx('clippy_bin')
def _fx_bin(d,im,e,f):
    """The Recycle Bin (a grey wire-mesh basket with a green arrow), rattling by `shake` px."""
    _,x,sh=e; x=int(x)+(random.choice((-sh,sh)) if sh else 0); y1=GROUND; y0=y1-14
    d.polygon([(x-7,y0),(x+7,y0),(x+5,y1),(x-5,y1)],fill=(150,150,160),outline=INK)
    for k in range(-4,5,2): d.line([x+k,y0+2,x+round(k*0.75),y1-1],fill=(95,95,108))
    for yy in (y0+5,y0+9): d.line([x-6,yy,x+6,yy],fill=(95,95,108))
    d.rectangle([x-8,y0-2,x+8,y0],fill=(205,205,215),outline=INK)
    d.polygon([(x-2,y0+8),(x+2,y0+8),(x,y0+4)],fill=(40,180,60))

@fx('clippy_err')
def _fx_err(d,im,e,f):
    """A flying error dialog (Clippy's projectile): tiny window, red X icon, speed lines behind."""
    _,x,y=e; x,y=int(x),int(y)
    for k in (4,8,12): d.line([x+9+k,y-2+k%3*2,x+13+k*2,y-2+k%3*2],fill=(200,230,230))
    bevel(d,x-9,y-6,x+9,y+6); d.rectangle([x-8,y-5,x+8,y-3],fill=NAVY)
    d.ellipse([x-7,y-2,x-1,y+4],fill=(220,20,20),outline=(110,0,0))
    d.line([x-5,y,x-3,y+2],fill=WHITE); d.line([x-5,y+2,x-3,y],fill=WHITE)
    d.line([x+1,y-1,x+7,y-1],fill=INK); d.line([x+1,y+2,x+5,y+2],fill=INK)

@fx('clippy_help')
def _fx_help(d,im,e,f):
    """One of the NEED HELP? spam balloons."""
    _,x,y=e; x,y=int(x),int(y)
    d.polygon([(x+12,y+9),(x+17,y+9),(x+19,y+13)],fill=BALLOON,outline=INK)
    d.rectangle([x,y,x+42,y+9],fill=BALLOON,outline=INK); d.line([x+13,y+9,x+16,y+9],fill=BALLOON)
    text(d,"NEED HELP?",x+2,y+2,INK,shadow=None)

@fx('clippy_hp')
def _fx_hp(d,im,e,f):
    """Clippy's health as a Win98 progress bar (navy blocks), top-left."""
    _,hp=e
    text(d,"CLIPPY.EXE",4,2,WHITE,shadow=(0,60,60)); bevel(d,3,8,45,13,fill=WHITE,sunken=True)
    for k in range(int(round(10*max(0,min(1,hp))))): d.rectangle([5+k*4,10,7+k*4,11],fill=NAVY)

@fx('clippy_task')
def _fx_task(d,im,e,f):
    """The NOT RESPONDING dialog with its [END TASK] button."""
    _,pressed,grow=e
    x0,y0,x1,y1=46,10,128,44
    if grow<1:
        cx,cy=(x0+x1)//2,(y0+y1)//2; hw,hh=int((x1-x0)/2*grow),int((y1-y0)/2*grow)
        if hw>2: bevel(d,cx-hw,cy-hh,cx+hw,cy+hh)
        return
    window(d,x0,y0,x1,y1,"CLIPPY.EXE")
    d.ellipse([x0+4,y0+11,x0+10,y0+17],fill=(250,210,20),outline=INK); text(d,"!",x0+6,y0+12,INK,shadow=None)
    text(d,"IS NOT",x0+14,y0+11,INK,shadow=None); text(d,"RESPONDING.",x0+14,y0+17,INK,shadow=None)
    x=_button(d,x0+5,y1-11,"END TASK",pressed); _button(d,x+6,y1-11,"WAIT")

@fx('clippy_big')
def _fx_big(d,im,e,f):
    _,txt,y,c,scale,cx,ol=e; big(im,txt,y,c,scale,cx,ol)

@fx('clippy_rod')
def _fx_rod(d,im,e,f):
    """Straightened Clippy flying to the bin: a spinning silver rod with his eyes."""
    _,x,y,a=e
    dx,dy=math.cos(a)*11,math.sin(a)*11
    d.line([x-dx,y-dy,x+dx,y+dy],fill=INK,width=4); d.line([x-dx,y-dy,x+dx,y+dy],fill=CLPAL['c'],width=2)
    for s in (-1,1): d.ellipse([x+dx*0.6*s-2,y+dy*0.6*s-2,x+dx*0.6*s+2,y+dy*0.6*s+2],fill=WHITE,outline=INK)

# ---- close-up: the crazy googly eyes ----------------------------------------------------------
def closeup_eyes(t,f):
    im=Image.new('RGB',(W,H),(0,70,70)); d=ImageDraw.Draw(im)
    for i in range(16):                                             # a red burst
        a=i*2*math.pi/16+f*0.04; d.polygon([(W//2,H//2),(W//2+math.cos(a)*150,H//2+math.sin(a)*90),
                                           (W//2+math.cos(a+0.18)*150,H//2+math.sin(a+0.18)*90)],fill=(90,10,20))
    z=0.55+0.45*ease(t/0.15); jx=random.choice((-1,0,1)) if t>0.3 else 0
    cy=int(40-6*(1-z)); r=int(24*z); wire=CLPAL['c']
    d.arc([W//2-58*z,cy-34*z,W//2+58*z,cy+80*z],180,360,fill=INK,width=int(10*z)+2)     # the wire's top loop
    d.arc([W//2-57*z,cy-33*z,W//2+57*z,cy+79*z],180,360,fill=wire,width=int(8*z))
    rr=random.Random(f//2)
    for k,ex in enumerate((W//2-31*z+jx,W//2+31*z+jx)):
        d.ellipse([ex-r-2,cy-r-2,ex+r+2,cy+r+2],fill=INK); d.ellipse([ex-r,cy-r,ex+r,cy+r],fill=WHITE)
        for v in range(7):                                          # bloodshot veins
            a=rr.uniform(0,2*math.pi); L=rr.uniform(0.35,0.7)
            p0=(ex+math.cos(a)*r,cy+math.sin(a)*r); p1=(ex+math.cos(a+0.2)*r*(1-L),cy+math.sin(a+0.2)*r*(1-L))
            d.line([p0,p1],fill=(220,40,40))
        d.ellipse([ex-r,cy-r,ex+r,cy+r],outline=(200,30,30))
        a=f*(0.7 if k else -0.55); pr=int(5*z)                      # the pupils spin in opposite directions
        px,py=ex+math.cos(a)*(r-pr-3),cy+math.sin(a)*(r-pr-3); d.ellipse([px-pr,py-pr,px+pr,py+pr],fill=INK)
        d.point((int(px-pr//2),int(py-pr//2)),fill=WHITE)
        by=cy-r-6+(f%3==0)*2; o=1 if k==0 else -1                   # twitching angry brows
        d.line([ex-12*o,by-5,ex+10*o,by+3],fill=INK,width=int(5*z))
    if t<0.06: zoom_lines(d,(255,90,90))
    if t>0.35: big(im,"NEED",3+(f%2),(255,255,204),3,cx=36,ol=(90,0,10))
    if t>0.5: big(im,"HELP?",3+((f+1)%2),(255,255,204),3,cx=W-40,ol=(90,0,10))
    if t>0.92: im=fade_to(im,(0,0,0),(t-0.92)/0.08*0.6)
    return im

# ---- the clip --------------------------------------------------------------------------------
def pop(s,txt,y,c,scale=2,cx=W//2,ol=(20,10,30)): s['fx'].append(('clippy_big',txt,y,c,scale,cx,ol))
def jump(t,h): return GROUND-int(h*math.sin(math.pi*max(0,min(1,t))))
def poof(s,x,y,f,t0):
    """The shape-shift puff: a white ring and twinkles around (x,y) for 6 frames after t0."""
    if 0<=f-t0<6:
        s['fx'].append(('circle',x,y,4+(f-t0)*4,WHITE))
        for k in range(4): s['fx'].append(('twinkle',x+random.randint(-18,18),y+random.randint(-18,14),2))

CLX,BINX=152,175
MSG1=["IT LOOKS LIKE YOU","ARE WRITING CODE.","NEED HELP?"]; MSG2=["ARE YOU SURE?","","","",""]
HP=[(128,0.9),(144,0.8),(220,0.65),(282,0.45),(288,0.25),(294,0.1),(310,0.0)]
ERRS=[118,126,134,142]                                              # error dialogs thrown at t0, land t0+10
SPAM=[(random.Random(k*7+1).randint(2,140),random.Random(k*13+3).randint(0,46)) for k in range(16)]

def clip_deathmatch(f):
    s=scene(f,THEME)
    cl=actor(CL[guard_pose(f)],CX); cp=None; binsh=0
    look=(-1,0)
    # ======== the offer ===========================================================================
    if 10<=f<60:
        cp=actor(_clippy_raw(look,blink=36<=f<38),CLX,pal=CLPAL)
        if f<18: cp['y']=int(lerp(-2,GROUND,ease((f-10)/8)))
        elif f<22: cp['y']=GROUND-int(3*math.sin(math.pi*(f-18)/4))
        if 18<=f<54: s['under'].append(('clippy_balloon',MSG1,(f-20)*3,["YES","NO"] if f>=34 else None,1 if 48<=f<54 else -1,1))
        if 54<=f<58: s['under'].append(('clippy_balloon',MSG1,99,None,-1,1-(f-54)/4))
        if 40<=f<48: cl.update(spr=CL['dash'],x=ez(CX,84,(f-40)/7),y=jump((f-40)/16,14))
        if 48<=f<52: cl.update(spr=CL['punch'],x=84,y=jump((f-40)/16,14))
        if f==48: s['fx'].append(('spark',98,41,4)); s['shake']=rshake()
        if 48<=f<56: pop(s,"CLICK!",1,WHITE,1,cx=100,ol=INK)
        if 52<=f<62: cl.update(spr=CL[guard_pose(f)],x=ez(84,CX,(f-52)/10),y=jump((f-40)/16,14) if f<56 else GROUND)
        if 54<=f<60:
            cp['alpha']=1-(f-54)/6
            for k in range(2): s['fx'].append(('twinkle',CLX+random.randint(-8,8),GROUND-random.randint(4,28),1))
    # ======== he comes back ======================================================================
    if 62<=f<96:
        cp=actor(_clippy_raw(look,'angry'),CLX,pal=CLPAL)
        if f<70: cp['y']=int(lerp(-2,GROUND,ease((f-62)/8)))
        if 66<=f<76: s['fx'].append(('dmg',"?!",CLX-4,14,(255,60,60)))
        if 70<=f<88: s['under'].append(('clippy_balloon',MSG2,(f-70)*2,["YES","YES"] if f>=78 else None,-1,1))
        if 80<=f<86: cl.update(spr=CL['dash'],x=ez(CX,92,(f-80)/6),y=jump((f-80)/12,16))
        if 86<=f<90: cl.update(spr=CL['punch'],x=92,y=jump((f-80)/12,16))
        if f==88: s['shake']=rshake(2); s['flash']=0.4; s['fc']=(104,36)
        if 88<=f<100:
            rr=random.Random(f)
            for j in range(10): s['fx'].append(('shard',lerp(58,141,rr.random())+rr.uniform(-1,1)*(f-88)*3,
                                                 lerp(12,47,rr.random())+(f-88)**2*0.3,BALLOON if j%3 else INK))
        if 90<=f<102: cl.update(spr=CL[guard_pose(f)],x=ez(92,CX,(f-90)/12),y=jump((f-80)/12,16) if f<92 else GROUND)
    # ======== rage: he grows HUGE ================================================================
    if 96<=f<158:
        big_=f>=104 or (f//2)%2==1
        spr=_clippy_raw(look,'angry'); cp=actor(scale2(spr) if big_ else spr,CLX-2,pal=CLPAL)
        if f<108: s['shake']=rshake(2 if f>=104 else 1)
        if f==104: s['flash']=0.7; s['fc']=(CLX,30); s['flashc']=(255,80,80)
        if 104<=f<120: pop(s,"DEATH MATCH",22,(255,60,60),cx=70,ol=(60,0,0))
        # the error dialogs
        for i,t0 in enumerate(ERRS):
            if t0<=f<t0+10+(i==1)*6:
                t=(f-t0)/10; s['fx'].append(('clippy_err',lerp(CLX-18,36,t),lerp(26,GROUND-8,t)-12*math.sin(math.pi*min(1,t))))
            if f==t0: cp['spr']=scale2(_clippy_raw(look,'crazy'))
        for t0 in (ERRS[0],ERRS[2]):                                   # punched out of the air
            if t0+8<=f<t0+12: cl.update(spr=CL['punch'])
            if f==t0+10: s['fx'].append(('spark',44,GROUND-7,5)); s['shake']=rshake()
            if t0+10<=f<t0+16:
                for j in range(5): s['fx'].append(('shard',44+random.randint(-8,8)+(f-t0-10)*2,GROUND-8+random.randint(-6,6),(GREY,NAVY,(220,20,20))[j%3]))
        if 130<=f<142: cl.update(spr=CL['guard2'],y=jump((f-130)/12,22))          # hops the 2nd one
        if 152<=f<158: cl.update(spr=CL['hurt'],x=CX-3)                             # the 4th lands
        if f==152: s['fx'].append(('spark',34,GROUND-9,6)); s['shake']=rshake(2)
        if 152<=f<160: s['fx'].append(('dmg',"ERROR",20,GROUND-24,(255,70,70)))
        if f>=154: poof(s,CLX,36,f,156)
    # ======== the shape-shifts ===================================================================
    if 158<=f<180:                                                    # a bicycle
        cp=actor(BIKE,lerp(CLX,-30,(f-160)/18) if f>=160 else CLX,pal=CLPAL)
        if 158<=f<170: pop(s,"BICYCLE?!",2,BALLOON,1,cx=CLX,ol=INK)
        for k in range(3): s['fx'].append(('dust',cp['x']+14+k*4+random.randint(0,2),GROUND-1))
        if 166<=f<178: cl.update(spr=CL['guard2'],y=jump((f-166)/12,22))
        if f>=178: cp['vis']=False
    if 180<=f<198:                                                    # a bell
        cp=actor(BELL[(f//3)%4],CLX,pal=CLPAL); poof(s,CLX,30,f,180)
        if f>=184:
            for k in range(2):
                r=((f-184)*4+k*12)%28; s['fx'].append(('arc',CLX-6,24,6+r,120,240,(255,240,160),1))
            pop(s,"DING! DING!",18,(255,230,100),cx=80,ol=(90,50,0))
        if 188<=f<198: cl.update(spr=CL['hurt'],x=CX-2+(f%2)); s['fx'].append(('dizzy',CX,GROUND-14))
    if 198<=f<224:                                                    # a question mark
        cp=actor(QM if f<206 else QM0,CLX,pal=CLPAL); poof(s,CLX,30,f,198)
        if 204<=f<212: s['fx'].append(('dmg',"???",CLX-6,0,(255,255,204)))
        if 206<=f<212: s['fx'].append(('orbc',lerp(CLX,48,(f-206)/5),lerp(GROUND-4,GROUND-9,(f-206)/5),3,(CLPAL['C'],CLPAL['c'])))
        if 209<=f<213: cl.update(spr=CL['punch'])
        if f==211: s['fx'].append(('spark',46,GROUND-8,5)); s['shake']=rshake()
        if 212<=f<220: s['fx'].append(('orbc',lerp(48,CLX,(f-212)/7),lerp(GROUND-9,GROUND-20,(f-212)/7),3,(CLPAL['C'],CLPAL['c'])))
        if f==219: s['fx'].append(('spark',CLX,GROUND-20,7)); s['shake']=rshake(2)
        if f>=219: cp['tint']=WHITE if f%2 else None
        if f>=220: poof(s,CLX,36,f,220)
    # ======== NEED HELP? spam ====================================================================
    if 224<=f<248:
        cp=actor(scale2(_clippy_raw(look,'crazy' if f%4<2 else 'angry')),CLX-2,pal=CLPAL)
        n=min(len(SPAM),(f-224)//1)
        for x,y in SPAM[:n]: s['under'].append(('clippy_help',x,y))
        if 236<=f<248: cl.update(spr=CL['charge'],aura=((255,210,90),1+(f%2)))
        if f==247: s['flash']=0.9; s['fc']=(CX+10,GROUND-8)
    if 247<=f<254:
        rr=random.Random(f)
        for x,y in SPAM:
            t=(f-247)/6
            for j in range(2): s['fx'].append(('shard',x+21+(x+21-CX)*t*0.5+rr.randint(-6,6),y+5+(y-50)*t*0.3+rr.randint(-3,3),BALLOON if j else INK))
        cp=actor(scale2(_clippy_raw(look,'angry')),CLX-2,pal=CLPAL); cl.update(spr=CL['charge'])
    # ======== close-up ===========================================================================
    if 254<=f<280: s['image']=closeup_eyes((f-254)/26,f); return s
    # ======== the beatdown and the finisher =====================================================
    if 280<=f<302:
        small=f>=296; cp=actor(_clippy_raw((0,0),'crazy') if small else scale2(_clippy_raw(look,'angry')),CLX-(0 if small else 2),pal=CLPAL)
        if f<284: cl.update(spr=CL['dash'],x=ez(CX,122,(f-280)/4),aura=((255,210,90),1))
        elif f<296:
            k=(f-284)//4; ph=(f-284)%4
            cl.update(spr=CL['punch' if ph<2 else 'guard'],x=122+k*2,aura=((255,210,90),1))
            if ph==0: s['fx'].append(('spark',134,GROUND-10-k*8,6)); s['shake']=rshake(2); cp['tint']=WHITE
        else: cl.update(spr=CL['armsup'],x=128)
        if f==294: s['flash']=0.6; s['fc']=(CLX,30)
        if 294<=f<298: poof(s,CLX,36,f,294)
        if small: s['fx'].append(('dizzy',CLX,GROUND-30))
    if 302<=f<326:                                                    # END TASK
        cp=actor(_clippy_raw((0,0),'crazy'),CLX,pal=CLPAL); s['fx'].append(('dizzy',CLX,GROUND-30))
        s['under'].append(('clippy_task',1 if 314<=f<320 else 0,min(1,(f-302)/4) if f<320 else 1-(f-320)/6))
        if f<308: cl.update(spr=CL[guard_pose(f)],x=ez(128,50,(f-302)/6))
        elif f<314: cl.update(spr=CL['dash'],x=50,y=jump((f-308)/12,14))
        elif f<318: cl.update(spr=CL['punch'],x=50,y=jump((f-308)/12,14))
        else: cl.update(spr=CL['dash'],x=ez(50,136,(f-318)/6),y=jump((f-308)/12,14) if f<320 else GROUND)
        if f==314: s['fx'].append(('spark',64,43,4)); s['shake']=rshake()
        if 314<=f<322: pop(s,"TERMINATED",48,(255,80,80),1,cx=88,ol=INK)
    if 326<=f<336:                                                    # bent straight
        t=(f-326)/7; cp=actor(_clippy_raw((0,0),'crazy',straight=min(1,t)),CLX,pal=CLPAL)
        cl.update(spr=CL['punch' if (f//2)%2 else 'armsup'],x=138)
        if f%3==0: s['fx'].append(('spark',CLX,GROUND-10-(f-326)*2,3))
        if 328<=f<336: pop(s,"STRAIGHTENED",18,BALLOON,1,cx=CLX-44,ol=INK)
    if 336<=f<342:                                                    # into the bin
        t=(f-336)/5; cl.update(spr=CL['armsup'],x=138)
        s['fx'].append(('clippy_rod',lerp(CLX,BINX,t),GROUND-18-18*math.sin(math.pi*t),t*5))
    if 341<=f<354: binsh=2 if f<348 else 1
    if 342<=f<354: pop(s,"DELETED",20,(255,80,80),ol=(60,0,0))
    if 348<=f<354: pop(s,"HELP?",GROUND-26,BALLOON,1,cx=BINX-8,ol=INK)
    if 336<=f<360 and f>=342: cl.update(spr=CL[guard_pose(f)],x=ez(138,CX,(f-342)/14))
    s['under'].insert(0,('clippy_bin',BINX,binsh))
    if cp: s['actors'].append(cp)
    if 118<=f<312: s['fx'].append(('clippy_hp',track(f,HP,refill=None)))
    s['actors'].append(cl)
    return s

CLIPS = [clip('deathmatch', N_, clip_deathmatch)]
