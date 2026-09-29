"""Naruto sub-theme "naruto-zabuza": Claude (Kakashi) vs Zabuza on the mist-covered lake. Close-up
of the headband lifting off the Sharingan; both weave the same hand seals and two Water Dragons
collide; then Kakashi casts first — the Great Waterfall sweeps Zabuza away. He resurfaces for the loop."""
from engine import *

THEME = 'naruto-zabuza'

def _kakashi(sharingan):
    def fn(x,y,t,l,r,c):
        if c=='.' or not (l<=x<=r): return None
        if y==t: return 'D' if l+2<=x<=l+4 else 'N'                  # headband + plate
        if c=='K' and x<=(l+r)//2: return 'r' if sharingan else 'N'   # left eye: covered / Sharingan
        if t+4<=y<=t+5: return 'N'                                     # mask
        if t+6<=y<=t+8: return 'w'                                     # jonin flak vest
        return None
    return fn
HAIR=[".....H.H.H..","...HHHHHHHH.","..HHHHHHHHHH","HHHHHHHHHHH."]
KAKASHI=variant(lambda s: recolor_rows(overlay(s,HAIR,-2,0),_kakashi(False)))
KAKASHI_SH=variant(lambda s: recolor_rows(overlay(s,HAIR,-2,0),_kakashi(True)))

ZABUZA=poses(S([
"....kkkkkk......","...kkkkkkkk.....","...DDDDDDDD.....","...ssKsssKs.....","...HHHHHHHH.....",
"...HhHhHhHH.....","....HHHHHH......","..ssssssssss....",".sssskssssss....",".ss.sskssss.ss..",
".ss.ssskss..ss..",".hh.kkkkkk..hh..","....vvvvvv......","....vvvvvv......","....vv..vv......",
"....vv..vv......","....hh..hh......","...kkk..kkk.....",]),9,'ss',3)

WATER,FOAM,DEEP=(60,140,230),(200,232,255),(30,80,170)

def _mist(d):
    for i,(y,x0,L) in enumerate([(16,10,40),(22,70,56),(28,130,40),(34,20,30),(40,96,48),(46,150,30)]):
        d.line([x0,y,x0+L,y],fill=(16,20,26))
register_bg(THEME, lambda v: (v//3,v//2+4,v+16), decor=_mist, clip_ground=True)   # Zabuza surfaces from the lake

@fx('ripple')
def _fx_ripple(d,im,e,f):
    _,x=e; r=6+(f//3)%4; d.ellipse([x-r,GROUND,x+r,GROUND+2],outline=(70,130,200))

@fx('cleaver')
def _fx_cleaver(d,im,e,f):
    """Kubikiribocho slung across Zabuza's back: wide blade, round hole near the tip, half-moon notch."""
    _,x,y=e; ux,uy=math.cos(-1.05),math.sin(-1.05); nx,ny=-uy,ux     # blade axis (up-right) and its normal
    bx,by=x-5,y-10                                                    # hilt, behind his hip
    P=lambda a,b: (bx+ux*a+nx*b, by+uy*a+ny*b)
    d.line([P(-5,0),P(0,0)],fill=(90,60,40),width=2)
    d.polygon([P(0,-4),P(30,-4),P(33,0),P(33,5),P(0,5)],fill=(190,196,210),outline=(110,114,130))
    hx,hy=P(27,1); d.ellipse([hx-2,hy-2,hx+2,hy+2],fill=(0,0,0))
    nx_,ny_=P(18,5); d.ellipse([nx_-2,ny_-2,nx_+2,ny_+2],fill=(0,0,0))

@fx('dragon')
def _fx_dragon(d,im,e,f):
    """A Water Dragon rising out of the lake along an arc; prog 0..1 = how far the head has come."""
    _,x0,dr,prog=e
    if prog<=0: return
    pts=[]
    for i in range(int(prog*40)+1):
        s=i/40; pts.append((x0+dr*s*48, GROUND-44*math.sin(math.pi*s*0.75)+2*math.sin(s*12-f*0.5), 5-2.5*s))
    for x,y,r in pts: d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=FOAM)
    for x,y,r in pts: d.ellipse([x-r,y-r,x+r,y+r],fill=WATER)
    for x,y,r in pts[::4]: d.point((x,y-r+1),fill=(255,255,255))
    hx,hy,_=pts[-1]
    d.ellipse([hx-6,hy-4,hx+6,hy+4],fill=WATER,outline=FOAM)
    d.polygon([(hx+dr*4,hy),(hx+dr*11,hy-3),(hx+dr*11,hy+3)],fill=DEEP)          # open jaws
    d.line([hx-dr*2,hy-4,hx-dr*6,hy-9],fill=FOAM); d.line([hx,hy-4,hx-dr*3,hy-10],fill=FOAM)   # horns
    d.point((hx+dr*2,hy-2),fill=(255,255,255))

@fx('droplet')
def _fx_drop(d,im,e,f):
    _,x,y=e; d.line([x,y,x,y+1],fill=FOAM)

@fx('waterfall')
def _fx_wave(d,im,e,f):
    """Daibakufu: a wall of water from x0 to its curling front."""
    _,x0,front,h=e
    if front<=x0 or h<=0: return
    top=[(x,GROUND-h*min(1,(x-x0)/40)-2*math.sin(x*0.3+f*0.6)) for x in range(int(x0),int(front)+1,3)]
    d.polygon([(x0,GROUND+2)]+top+[(front,GROUND+2)],fill=WATER)
    for x,y in top[::2]: d.line([x,y,x+2,y+1],fill=FOAM)
    fy=GROUND-h; d.arc([front-12,fy-4,front+6,fy+14],200,40,fill=FOAM,width=3)
    for k in range(6): d.point((front+random.randint(0,6),fy+random.randint(0,int(h))),fill=FOAM)

def drops(s,cx,cy,t,n=30,seed=0):
    rr=random.Random(seed)
    for _ in range(n):
        vx=rr.uniform(-3,3); vy=rr.uniform(-3.5,0)
        x=cx+vx*t; y=cy+vy*t+0.18*t*t
        if y<GROUND: s['fx'].append(('droplet',x,y))

def closeup_sharingan(t,f):
    """Primer plano: Kakashi pushes the headband up — scar, and the Sharingan's tomoe start to spin."""
    im=Image.new('RGB',(W,H),(217,119,87)); d=ImageDraw.Draw(im)
    d.rectangle([0,40,W,H],fill=(44,44,96))                                   # mask
    for x in range(0,W,5): d.line([x,40,x+2,H],fill=(36,36,80))
    for i,x in enumerate(range(-6,W+6,10)): d.polygon([(x,0),(x+14,0),(x+10+(i%3)*2,9)],fill=(242,242,250))
    d.rectangle([0,0,W,5],fill=(242,242,250))
    for ex in (70,120):
        d.rounded_rectangle([ex-7,14,ex+7,36],radius=4,fill=(24,14,12))
    ex=70; up=ease((t-0.18)/0.3)
    if up>0:   # the Sharingan
        d.rounded_rectangle([ex-6,15,ex+6,35],radius=4,fill=(210,20,34))
        spin=f*0.4*(0.3+t)
        for k in range(3):
            a=spin+k*2.094; tx,ty=ex+math.cos(a)*4,25+math.sin(a)*6
            d.ellipse([tx-1.5,ty-1.5,tx+1.5,ty+1.5],fill=(10,6,8))
        d.ellipse([ex-2,23,ex+2,27],fill=(10,6,8)); d.point((ex-3,17),fill=(255,255,255))
        d.line([ex-2,8,ex+3,42],fill=(150,60,40))                                # the scar
    by=int(8-40*up)   # headband sliding up off the left eye
    d.polygon([(0,by+4),(W,by-2),(W,by+14),(0,by+20)],fill=(44,44,96))
    d.rectangle([ex-16,by+2,ex+16,by+17],fill=(186,186,206),outline=(110,110,126))
    d.arc([ex-6,by+4,ex+6,by+15],30,330,fill=(110,110,126)); d.line([ex+2,by+9,ex+8,by+6],fill=(110,110,126))
    if t>0.55: text(d,"SHARINGAN",W//2-18,56,(255,90,90))
    if t<0.06:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    if t>0.9: im=Image.blend(im,Image.new('RGB',(W,H),(200,0,20)),0.5*(t-0.9)/0.1)
    return im

SEALS=['armsup','charge','guard','punch']
def clip_waterdragon(f):
    s=scene(f,THEME)
    cl=actor(KAKASHI[guard_pose(f)],30); zb=actor(ZABUZA['idle'],150,flip=True)
    sh=44<=f<232
    if sh: cl['spr']=KAKASHI_SH[guard_pose(f)]
    # 0) close-up: the Sharingan
    if 12<=f<44: s['image']=closeup_sharingan((f-12)/32,f); return s
    # 1) the same hand seals, frame for frame
    if 48<=f<80 or 124<=f<146:
        k=(f//3)%4
        cl['spr']=KAKASHI_SH[SEALS[k]]; zb['spr']=ZABUZA['attack' if k%2 else 'idle']
        s['fx'].append(('mote',38+random.randint(-2,2),GROUND-8,(170,210,255)))
    if 52<=f<80: callout(s,"SUITON: SUIRYUDAN NO JUTSU!",c=(150,200,255))
    if 70<=f<82:
        for x in (44,136): drops(s,x,GROUND,(f-70)%6+2,n=8,seed=x+f//6)
    # 2) two Water Dragons, and the clash
    if 80<=f<112:
        p=ease((f-80)/28); s['fx'].append(('dragon',44,1,p)); s['fx'].append(('dragon',136,-1,p))
        cl['spr']=KAKASHI_SH['armsup']; zb['spr']=ZABUZA['attack']
        if f%3==0: s['shake']=rshake()
    if f==110: s['flash']=1.0; s['fc']=(90,GROUND-30); s['flashc']=(200,230,255)
    if 110<=f<146:
        drops(s,90,GROUND-30,f-110,n=44,seed=2)
        if f<118: s['fx'].append(('ring',90,GROUND-30,(f-110)*5,FOAM)); s['shake']=rshake(2)
    # 3) Zabuza can't believe it: Kakashi is ahead of him
    if 124<=f<150: s['fx'].append(('dmg',"!?",zb['x']-4,GROUND-28,(255,255,255)))
    if 146<=f<170: callout(s,"SUITON: DAIBAKUFU NO JUTSU!",c=(150,200,255)); cl['spr']=KAKASHI_SH['armsup']
    if 146<=f<176: zb['spr']=ZABUZA['hurt'] if f>=164 else ZABUZA['idle']
    # 4) the Great Waterfall
    if 156<=f<214:
        if f<196: front=lerp(44,240,ease((f-156)/36)); h=lerp(8,42,min(1,(f-156)/14))
        else: front=240; h=lerp(42,0,(f-196)/18)
        s['under'].append(('waterfall',40,front,h))   # under: Zabuza tumbles on top of it
        if f%2==0: s['shake']=rshake()
        if front>=144:
            zb['vis']=False
            tx=min(front-6,230); s['fx'].append(('mote',tx,GROUND-h+4,(255,255,255)))
            if front<236: zb2=actor(ZABUZA['hurt'],tx,y=GROUND-int(h*0.6),flip=True); s.setdefault('extra',[]).append(zb2)
    # 5) he surfaces again; the headband comes down
    if 176<=f<214: zb['vis']=False
    if 214<=f<240:
        t=(f-214)/20; zb.update(vis=True,spr=ZABUZA['hurt'] if t<1 else ZABUZA['idle'],y=GROUND+int(22*(1-ease(t))))
        if f<226: drops(s,150,GROUND-2,(f-214)%8+1,n=6,seed=f//8)
    if 228<=f<232: s['fx'].append(('mote',34,GROUND-9,(255,255,255)))
    for a in (cl,zb):
        if a['vis'] and a['y']<=GROUND: s['under'].append(('ripple',a['x']))
    if zb['vis']: s['under'].append(('cleaver',zb['x'],zb['y']))
    s['actors']=s.pop('extra',[])+[cl,zb]
    return s

CLIPS = [clip('waterdragon', 264, clip_waterdragon)]
