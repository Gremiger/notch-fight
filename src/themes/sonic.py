"""Sonic the Hedgehog: Claude (Sonic: blue quills, white gloves, red sneakers) vs Dr. Eggman in
his Egg Mobile, in Green Hill Zone. Claude dashes through a line of rings (RINGS counter HUD),
revs a spin dash that Eggman dodges and blasts off-screen - cut to a full-speed run around the
loop-de-loop. Back in the arena Eggman lowers the checkered wrecking ball and swats Claude out of
the air: the classic ring loss, RINGS 0 flashing red. The 7 Chaos Emeralds circle him, SUPER
CLAUDE turns gold and smashes the Egg Mobile; the "CLAUDE GOT THROUGH ACT 1" tally card, then a
new act: rings back, Eggman back, neutral."""
from engine import *

THEME = 'sonic'
N_ = 324

# --- Claude as Sonic: blue body, white eyes, peach muzzle + belly, quills, gloves, red sneakers ---
SONIC_PAL={'L':(34,72,214),'N':(20,40,150),'W':(248,248,252),'s':(242,200,160),'r':(224,36,36),'H':(250,250,250)}
SUPER_PAL={'L':(250,212,70),'N':(236,168,30),'W':(255,255,235),'s':(255,226,170),'r':(224,36,36),'H':(250,250,250),
           'K':(190,30,30)}
QUILLS=[(-4,0,"NNNL"),(-2,1,"LL"),(-4,2,"NNNL"),(-2,3,"LL"),(-3,4,"NNL")]

def _sonic_dress(spr):
    ks=[(x,y) for y,row in enumerate(spr) for x,ch in enumerate(row) if ch=='K']
    ky0=min(y for _,y in ks); ky1=max(y for _,y in ks); kx0=min(x for x,_ in ks); kx1=max(x for x,_ in ks)
    h=len(spr); top,l,r=body_box(spr)
    def fn(x,y,t,l,r,c):
        if c=='.' or c=='K': return None
        if ky0<=y<=ky1 and kx0-1<=x<=kx1: return 'W'                        # the big white eyes
        if y==ky1+1 and kx0<=x<=r: return 's'                                # muzzle
        if y>=h-2 and c=='o': return 'H' if (y==h-2 and (x+1<len(spr[0]) and spr[y][x+1]=='.')) else 'r'
        if c=='o': return 'L' if (y>=h-3) else 'W'                          # gloves / legs
        if t+5<=y<=t+7 and l+3<=x<=r-2: return 's'                          # belly
        return 'L'
    s=recolor_rows(spr,fn)
    s=paint(s,[(l+dx,top+dy,ch) for dx,dy,ch in QUILLS],left=4,right=4)    # symmetric pad: stays centred
    return overlay(s,["NN.......",".NNLL...."],2,0)                            # crest sweeping back
SONIC=variant(_sonic_dress)

# --- Dr. Eggman in the Egg Mobile (front view): bald head, goggles, glasses, huge moustache ---
EGG=S([
"........sssssss........",
".......sssssssss.......",
"......kEEkkkkkEEk......",
"......sssssssssss......",
"......sEEsssssEEs......",
".....sssssssssssss.....",
"..qqqqqqqsssssqqqqqqq..",
".qqqqqqqqqsssqqqqqqqqq.",
"..qq..rrrrrrrrrrr..qq..",
".....rrrrrrYrrrrrr.....",
"WW..rrrrrrrrrrrrrrr..WW",
"DDDDDDDDDDDDDDDDDDDDDDD",
"dHHDDDDDDDDDDDDDDDDDDDd",
".dDDDDDDDDDYYDDDDDDDDd.",
"..dDDDDDDDDDDDDDDDDDd..",
"...ddDDDDDDDDDDDDDdd...",
".....ddddddddddddd.....",])
_egg_laugh=list(EGG); _egg_laugh[8]="..qq..rrrkkkkkrrr..qq.."
EGGS={'idle':EGG,'laugh':S(_egg_laugh),'hurt':hurt(EGG)}
EGG_PAL={'s':(248,196,168),'q':(200,100,40),'k':(30,26,34),'E':(120,200,255),'r':(220,44,40),
         'Y':(250,210,60),'W':(248,248,252),'D':(186,190,204),'d':(110,112,128),'H':(250,250,255)}
EX,EY=148,40                                       # Egg Mobile home spot (pod bottom)
def egg_bob(f): return EY+round(1.5*math.sin(2*math.pi*f/36))

# --- small text with a real 5-wide M (the 3x5 font's M reads as H) -----------------------------
_M5=["10001","11011","10101","10001","10001"]
def stext(d,txt,x,y,c,shadow=(0,0,0)):
    for ch in txt:
        if ch=='M':
            for j,row in enumerate(_M5):
                for i,b in enumerate(row):
                    if b=='1':
                        if shadow: d.point((x+i+1,y+j+1),fill=shadow)
                        d.point((x+i,y+j),fill=c)
            x+=6
        else: text(d,ch,x,y,c,shadow=shadow); x+=4

# --- Green Hill Zone ----------------------------------------------------------------------------
register_bg(THEME, lambda v: (0,0,0))
PALMS=(18,112,172)

def _palm(d,x,h):
    for k in range(h):                                             # banded trunk leaning right
        xx=x+int(k*k/(h*5)); c=(150,90,40) if (k//2)%2 else (104,60,24)
        d.line([xx,GROUND-k,xx+1,GROUND-k],fill=c)
    tx,ty=x+int(h/5),GROUND-h
    for dx,dy in ((-7,3),(-5,5),(6,3),(5,5),(0,-2),(-3,-1),(3,-1)):
        d.line([tx,ty,tx+dx,ty+dy],fill=(40,150,40)); d.point((tx+dx,ty+dy+1),fill=(24,100,30))
    d.rectangle([tx-1,ty,tx+1,ty+1],fill=(60,190,50))

@fx('sonic_stage')
def _fx_stage(d,im,e,f):
    """Sky, clouds, the shimmering sea, hills, palm trees, grass and checkered soil; off = scroll."""
    _,off=e; off=int(off)
    for y in range(0,27):
        k=y/26; d.line([0,y,W,y],fill=(int(lerp(40,110,k)),int(lerp(90,170,k)),int(lerp(210,250,k))))
    co=off//4
    for cx,cy,w in ((20,16,22),(78,10,16),(130,19,26),(176,12,14)):
        x=(cx-co)%(W+30)-15
        d.ellipse([x,cy,x+w,cy+4],fill=(236,242,255)); d.line([x+3,cy+4,x+w-3,cy+4],fill=(180,200,240))
    d.rectangle([0,27,W,40],fill=(40,110,220))
    for y in range(28,40,3):                                       # sea shimmer
        for x0 in range(-((off//2+f*2//3+y*7)%24),W,24): d.line([x0,y,x0+5+(y%4),y],fill=(150,200,255))
    ho=off//2
    for x in range(W):                                             # rolling hills (2 layers)
        y1=int(34+4*math.sin((x+ho)*0.06)+2*math.sin((x+ho)*0.17)); d.line([x,y1,x,GROUND],fill=(34,120,44))
        d.point((x,y1),fill=(80,180,70))
        y2=int(44+3*math.sin((x+off*3//4)*0.09+1)); d.line([x,y2,x,GROUND],fill=(26,96,36))
        if ((x+off*3//4)//6)%2==0: d.point((x,y2+2),fill=(46,130,52))
    for px in PALMS:
        x=(px-off)%(W+40)-20; _palm(d,x,18 if px!=112 else 14)
    for x in range(W):                                             # grass lip + checkered soil
        d.point((x,GROUND),fill=(96,210,60)); d.point((x,GROUND+1),fill=(40,150,40) if (x+off)%3 else (96,210,60))
        for y in range(GROUND+2,H):
            d.point((x,y),fill=(180,100,36) if (((x+off)//4)+((y-GROUND-2)//3))%2 else (112,56,20))

@fx('sonic_ring')
def _fx_ring(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); w=int(round(abs(math.cos(f*math.pi/6+x*0.2))*2.4))
    d.ellipse([x-w-1,y-3,x+w+1,y+3],outline=(250,210,40)); d.point((x-w,y-2),fill=(255,250,200))
    if w==0: d.line([x,y-3,x,y+3],fill=(250,210,40))

@fx('sonic_hud')
def _fx_hud(d,im,e,f):
    _,score,t,rings=e; ylw=(250,210,60)
    stext(d,"SCORE",3,1,ylw); stext(d,"TIME",3,7,ylw)
    stext(d,"RINGS",3,13,(236,40,40) if (rings==0 and (f//6)%2) else ylw)
    w=(248,248,252); text(d,f"{score:6d}",26,1,w); text(d,f"{t//60}:{t%60:02d}",34,7,w); text(d,f"{rings:3d}",30,13,w)

@fx('sonic_ball')
def _fx_ball(d,im,e,f):
    """The spin ball: a disc with quill arcs spinning at `spin` rad/frame."""
    _,x,y,r,spin,pal=e; x,y=int(x),int(y); body,dark=pal['L'],pal['N']
    d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=OUT); d.ellipse([x-r,y-r,x+r,y+r],fill=body)
    for k in range(3):
        a=f*spin+k*2.09; a0=math.degrees(a)
        d.arc([x-r+1,y-r+1,x+r-1,y+r-1],a0,a0+60,fill=dark)
        d.point((int(x+math.cos(a)*(r-2)),int(y+math.sin(a)*(r-2))),fill=pal['s'])
    d.point((x-r//2,y-r//2),fill=(255,255,255))

@fx('sonic_dust')
def _fx_dust(d,im,e,f):
    """Spin-dash dust kicked back (left) from x, strength 0..1."""
    _,x,a=e; rr=random.Random(f%12)
    for i in range(int(7*a)+2):
        k=rr.random(); xx=x-4-k*14; yy=GROUND-1-rr.random()*5*k; r=1+int(k*2)
        d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=(236,230,220) if i%2 else (200,190,176))

@fx('sonic_speed')
def _fx_speed(d,im,e,f):
    """Horizontal speed lines behind a runner going `dirn` (1 = right)."""
    _,x,y0,y1,dirn=e; rr=random.Random(f)
    for _ in range(5):
        yy=rr.randint(int(y0),int(y1)); L=rr.randint(6,16); xx=x-dirn*rr.randint(4,10)
        d.line([xx,yy,xx-dirn*L,yy],fill=(236,242,255))

@fx('sonic_wrecker')
def _fx_wrecker(d,im,e,f):
    """The checkered wrecking ball on its chain from the pod's pivot (px,py)."""
    _,px,py,bx,by=e; n=8
    for k in range(1,n):
        cx,cy=lerp(px,bx,k/n),lerp(py,by,k/n); d.point((int(cx),int(cy)),fill=(210,210,220) if k%2 else (120,120,134))
    r=5; bx,by=int(bx),int(by)
    d.ellipse([bx-r-1,by-r-1,bx+r+1,by+r+1],fill=OUT)
    for yy in range(by-r,by+r+1):
        for xx in range(bx-r,bx+r+1):
            if (xx-bx)**2+(yy-by)**2<=r*r+1:
                d.point((xx,yy),fill=(240,240,246) if ((xx-bx+8)//3+(yy-by+8)//3)%2 else (30,30,40))
    d.point((bx-2,by-3),fill=(255,255,255))

EMERALDS=[(40,200,80),(230,40,40),(50,110,250),(250,220,40),(60,230,230),(190,70,230),(230,230,240)]
@fx('sonic_emerald')
def _fx_emerald(d,im,e,f):
    _,x,y,c=e; x,y=int(x),int(y)
    d.polygon([(x,y-3),(x+3,y),(x,y+3),(x-3,y)],fill=c,outline=OUT)
    d.point((x-1,y-1),fill=(255,255,255))

def closeup_loop(t,f):
    """Full-speed cut: Claude streaks in from the left, spins round the loop-de-loop, exits right."""
    s=scene(f,THEME); s['under'].append(('sonic_stage',f*6))
    im=render(s,f); d=ImageDraw.Draw(im)
    cx,cy,R0,R1=92,35,23,28
    for yy in range(cy-R1,GROUND+1):                               # the checkered loop track
        for xx in range(cx-R1,cx+R1+1):
            q=(xx-cx)**2+(yy-cy)**2
            if R0*R0<=q<=R1*R1:
                d.point((xx,yy),fill=(96,210,60) if q<(R0+1.3)**2 else ((180,100,36) if ((xx//3)+(yy//3))%2 else (112,56,20)))
    d.rectangle([0,GROUND,W,GROUND+1],fill=(96,210,60))
    pr=R0-5; run=lambda x: ('dash' if (f//2)%2 else 'punch')
    if t<0.3:                                                       # the approach
        x=lerp(-12,cx,t/0.3)
        for k in (3,2,1): draw(im,SONIC['dash'],x-k*7,GROUND,False,alpha=0.12*(4-k),tint=(90,150,255))
        draw(im,SONIC[run(0)],x,GROUND,False,pal=SONIC_PAL); FX['sonic_speed'](d,im,('sonic_speed',x-6,GROUND-10,GROUND-2,1),f)
    elif t<0.7:                                                     # round the loop as a ball
        ph=(t-0.3)/0.4*2*math.pi
        for k in range(6,0,-1):
            p=ph-k*0.22
            if p<0: continue
            bx,by=cx+pr*math.sin(p),cy+pr*math.cos(p)
            r=5-k//2; d.ellipse([bx-r,by-r,bx+r,by+r],fill=tuple(int(lerp(c,255,k/8)) for c in (60,110,240)))
        FX['sonic_ball'](d,im,('sonic_ball',cx+pr*math.sin(ph),cy+pr*math.cos(ph),5,0.9,SONIC_PAL),f)
    else:                                                           # out the other side
        x=lerp(cx,W+16,(t-0.7)/0.3)
        for k in (3,2,1): draw(im,SONIC['dash'],x-k*7,GROUND,False,alpha=0.12*(4-k),tint=(90,150,255))
        draw(im,SONIC[run(0)],x,GROUND,False,pal=SONIC_PAL); FX['sonic_speed'](d,im,('sonic_speed',x-6,GROUND-10,GROUND-2,1),f)
    if t<0.05: zoom_lines(d)
    _fx_hud(d,im,('sonic_hud',*_hud(f)),f)
    return im

# --- timeline -----------------------------------------------------------------------------------
RINGS=[(50+i*7,46-int(3*math.sin(i*0.9))) for i in range(8)]
RUN0,RUN1=12,40                                    # ring dash: x 30 -> 100
def run_x(f): return lerp(30,100,(f-RUN0)/(RUN1-RUN0))
def collected(f):
    if f<RUN0 or f>=306: return 0
    return sum(1 for x,_ in RINGS if f>=RUN1 or run_x(f)+4>=x)
HIT=190; SUPER=244; BOOM=266; CARD=284; RESET=306

def _hud(f):
    if f>=RESET: return 0,0,0
    rings=collected(f) if f<HIT else (0 if f<226 else min(50,int((f-226)*50/18)))
    score=100*min(collected(f),8)*(f<HIT)+800*(f>=HIT)+1000*(f>=BOOM)
    if f>=CARD+8: score+=int(lerp(0,55000,(f-CARD-8)/10))
    return score,f//20,rings

def swing(f):
    """Wrecking-ball angle (rad, + = to the right) and chain length."""
    L=0 if f<156 else min(20,(f-156)*20/10)
    amp=0 if f<166 else min(1.15,(f-166)*1.15/14)
    return amp*math.sin((f-166)*2*math.pi/24+math.pi/2)*(-1 if f>=166 else 0),L

def wreck_at(f,px,py):
    ang,L=swing(f); return px+L*math.sin(ang),py+L*math.cos(ang)+5
_HB=wreck_at(HIT,EX,egg_bob(HIT)-1)
TGT=(int(_HB[0])-8,int(_HB[1])-3)                  # where Claude's spin jump meets the ball

def clip_green(f):
    s=scene(f,THEME); s['under'].append(('sonic_stage',0))
    cl=actor(SONIC[guard_pose(f)],30,pal=SONIC_PAL)
    ex,ey=EX,egg_bob(f); eg=actor(EGGS['idle'],ex,ey,pal=EGG_PAL)
    ball=None; wreck=None
    if 96<=f<144: s['image']=closeup_loop((f-96)/48,f); return s

    # 1) the ring dash
    for i,(rx,ry) in enumerate(RINGS):
        got=RUN0<=f<RESET and (f>=RUN1 or run_x(f)+4>=rx)
        if not got and not (RESET<=f<318 and (f//2)%2): s['fx'].append(('sonic_ring',rx,ry))
        if RUN0<=f<RUN1+4 and got and run_x(min(f,RUN1-1))-rx<12: s['fx'].append(('twinkle',rx,ry,2))
    if RUN0<=f<RUN1:
        x=run_x(f); cl.update(spr=SONIC['dash' if (f//2)%2 else 'punch'],x=x)
        s['under'].append(('sonic_speed',x-4,GROUND-10,GROUND-2,1))
    if RUN1<=f<48: cl.update(x=100,spr=SONIC['charge']); s['fx'].append(('dust',100-6+(f-RUN1),GROUND-2))
    if RUN1<=f<96: cl['x']=100
    # 2) spin dash: rev x3, release; Eggman hops up out of the way
    if 48<=f<84:
        cl['vis']=False; rev=(f-48)%12<3
        ball=(100,GROUND-5-(1 if rev else 0),5+(1 if rev else 0),0.5+(f-48)*0.03)
        s['fx'].append(('sonic_dust',100,1.0 if rev else 0.4))
        if rev: s['fx'].append(('sonic_speed',106,GROUND-9,GROUND-2,-1))
    if 84<=f<96:
        cl['vis']=False; bxx=lerp(100,196,(f-84)/10); ball=(bxx,GROUND-5,5,1.4)
        s['fx'].append(('sonic_speed',bxx-6,GROUND-9,GROUND-2,1))
    if 78<=f<156:
        up=ease((f-78)/8) if f<120 else 1-ease((f-144)/10)
        eg['y']=ey-int(22*up)
    # 3) back from the loop: Claude skids in from the left
    if 144<=f<156:
        t=(f-144)/12; cl.update(x=ez(-10,44,t*1.3),spr=SONIC['dash'] if t<0.7 else SONIC['charge'])
        if t>=0.7: s['fx'].append(('dust',cl['x']-6,GROUND-2))
    if 156<=f<HIT: cl['x']=44
    # 4) the wrecking ball: Claude spin-jumps at Eggman and gets swatted
    if 156<=f<CARD:
        ang,L=swing(f)
        if f>=HIT: ang,L=swing(HIT)[0]*max(0,1-(f-HIT)/12),(20 if f<226 else max(0,20-(f-226)*2))
        if L>0:
            px,py=eg['x'],eg['y']-1; wreck=(px,py,px+L*math.sin(ang),py+L*math.cos(ang)+5)
    if 176<=f<HIT:
        t=(f-176)/(HIT-176); cl['vis']=False
        ball=(lerp(44,TGT[0],t),lerp(GROUND-5,TGT[1],t)-16*math.sin(math.pi*t),5,0.9)
    if f==HIT or f==HIT+1: s['fx'].append(('spark',TGT[0]+4,TGT[1],5)); s['shake']=rshake(1)
    if HIT<=f<214:
        t=min(1,(f-HIT)/18); cl.update(spr=SONIC['hurt'],x=lerp(TGT[0],44,t),y=int(min(GROUND,lerp(TGT[1]+6,GROUND,t)-14*math.sin(math.pi*t))))
        for k in range(8):                                         # the rings scatter
            a=math.pi*(0.15+0.7*k/7); v=2.2+0.4*(k%3); tt=f-HIT
            rx=TGT[0]+math.cos(a)*v*tt*(1 if k%2 else -1); ry=TGT[1]-math.sin(a)*v*1.2*tt+0.12*tt*tt
            if ry>GROUND-3: ry=GROUND-3-abs(math.sin(tt*0.4))*6
            if tt<16 or (f//2)%2: s['fx'].append(('sonic_ring',rx,ry))
    if 200<=f<222:
        eg['spr']=EGGS['laugh']
        if (f//4)%2: s['fx'].append(('dmg',"HO HO HO!",eg['x']-18,eg['y']-26,(248,248,252)))
    if 214<=f<222: cl.update(x=44,spr=SONIC['hurt'] if f<218 else SONIC['guard'])
    # 5) the Chaos Emeralds -> SUPER CLAUDE
    if 222<=f<SUPER:
        cl.update(x=44,spr=SONIC['armsup']); t=(f-222)/(SUPER-222); rad=lerp(40,6,ease(t))
        for k,c in enumerate(EMERALDS):
            a=k*2*math.pi/7+t*7; s['fx'].append(('sonic_emerald',44+math.cos(a)*rad,GROUND-8+math.sin(a)*rad*0.55,c))
    if SUPER-4<=f<SUPER+2: s['flash']=1.0-abs(f-SUPER+1)/4; s['fc']=(44,GROUND-8); s['flashc']=(255,248,200)
    sup=SUPER<=f<CARD+2
    if sup:
        cl.update(pal=SUPER_PAL,aura=((255,226,90),1))
        if f%2==0: s['fx'].append(('twinkle',cl['x']+((f*7)%15)-7,GROUND-6-((f*5)%16),1))
    if SUPER<=f<258:
        cl.update(x=44,spr=SONIC['armsup'] if f<250 else SONIC['charge'])
        s['fx'].append(('big',"SUPER CLAUDE",4,(255,226,90),116))
    # 6) Super dash into the Egg Mobile, it explodes and flees
    if 258<=f<BOOM:
        t=(f-258)/(BOOM-258); x=lerp(44,eg['x']-12,t); y=lerp(GROUND,eg['y']-2,t)
        for k in (3,2,1): s['under'].append(('sonic_speed',x-6,y-12,y-2,1))
        cl.update(spr=SONIC['dash'],x=x,y=int(y))
    if BOOM<=f<CARD: cl.update(spr=SONIC['punch'],x=eg['x']-14,y=eg['y']-2)
    if BOOM<=f<CARD:
        t=f-BOOM; eg['spr']=EGGS['hurt']; eg['x']=ex+t*t*0.25; eg['y']=eg['y']-int(t*t*0.12)
        if t<2: s['shake']=rshake(2); s['flash']=0.8; s['fc']=(ex,eg['y']-8)
        rr=random.Random(t//2)
        for k in range(4): s['fx'].append(('smoke',eg['x']-8-k*6,eg['y']-6+k-(t%3),2+k,(70,70,80) if k%2 else (110,110,120)))
        if t<14:
            for j in range(2): s['fx'].append(('boom',eg['x']+rr.randint(-11,11),eg['y']-rr.randint(0,16),3+(t+j)%4))
        if t%3==0: s['fx'].append(('spark',eg['x']+rr.randint(-8,8),eg['y']-rr.randint(2,12),3))
    if BOOM<=f<BOOM+14: s['fx'].append(('dmg',"1000",ex-30,int(lerp(18,10,(f-BOOM)/14)),(248,248,252)))
    if BOOM<=f<RESET+10: eg['vis']=BOOM<=f<CARD and eg['x']<W+14
    # 7) the tally card: Claude lands, back to normal, arms up
    if CARD<=f<RESET:
        t=(f-CARD)/6; cl.update(spr=SONIC['armsup'] if t>=1 else SONIC['guard'],x=lerp(134,40,min(1,t)),
                               y=int(lerp(38,GROUND,min(1,t))) if t<1 else GROUND)
        if f<CARD+2: s['flash']=0.8; s['fc']=(cl['x'],GROUND-8); s['flashc']=(255,248,200)
        k=min(1,(f-CARD)/6)
        s['fx'].append(('big',"CLAUDE GOT",int(lerp(-12,4,k)),(248,248,252),118))
        s['fx'].append(('big',"THROUGH ACT 1",int(lerp(70,18,k)),(250,210,60),118))
        if f>=CARD+8:
            tb=int(lerp(50000,0,(f-CARD-8)/10)); rb=int(lerp(5000,0,(f-CARD-8)/10))
            s['fx'].append(('sonic_tally',tb,rb))
    # 8) new act: Claude jogs back, Eggman flies back in, rings reappear
    if RESET<=f<316:
        t=(f-RESET)/10; cl.update(spr=SONIC['dash' if (f//2)%2 else 'punch'],x=lerp(40,30,t),flip=True)
    if RESET<=f<318:
        t=ease((f-RESET)/12); eg.update(vis=True,x=lerp(W+16,EX,t),y=int(lerp(4,ey,t)))
    if f==316 or f==317: cl.update(spr=SONIC['charge'],x=30,flip=False)

    s['actors']=[eg,cl]
    if wreck: s['fx'].insert(0,('sonic_wrecker',*wreck))
    if ball:
        pal=SUPER_PAL if sup else SONIC_PAL
        s['fx'].append(('sonic_ball',ball[0],ball[1],ball[2],ball[3],pal))
    s['fx'].append(('sonic_hud',*_hud(f)))
    return s

@fx('sonic_tally')
def _fx_tally(d,im,e,f):
    _,tb,rb=e; ylw=(250,210,60); w=(248,248,252)
    stext(d,"TIME BONUS",80,37,ylw); text(d,f"{tb:5d}",140,37,w)
    stext(d,"RING BONUS",80,45,ylw); text(d,f"{rb:5d}",140,45,w)

CLIPS = [clip('greenhill', N_, clip_green)]
