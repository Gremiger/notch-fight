"""Shingeki no Kyojin sub-theme "snk-colosal": lightning, and the Colossal Titan rises behind the
Wall (eye close-up). Its arm sweeps the rampart; Claude rides the ODM gear through the steam and
cuts its nape."""
from engine import *
from themes.snk import SCOUT   # same franchise: Claude in Survey Corps gear (+ 'wire', 'blades' fx)

THEME = 'snk-colosal'
WALL_TOP = 30
MUSCLE,STRIA,TOOTH = (170,52,42),(118,30,26),(232,222,202)

def wall(d):
    for y in range(WALL_TOP,GROUND+1):
        for x in range(W):
            mortar=(y-WALL_TOP)%5==0 or (x+((y-WALL_TOP)//5)*4)%9==0
            d.point((x,y),fill=(34,31,29) if mortar else (52,48,44))
    d.line([0,WALL_TOP,W,WALL_TOP],fill=(84,78,70))
    for x in range(0,W,6): d.rectangle([x,WALL_TOP-2,x+2,WALL_TOP-1],fill=(64,60,54))

register_bg(THEME, lambda v: (v,v-6,v-12), decor=wall)

def head(d,x,top,rise):
    """The skinless giant head; the Wall is redrawn over its lower half afterwards."""
    d.ellipse([x-22,top,x+22,top+46],fill=MUSCLE)
    for i in range(-18,19,4): d.line([x+i,top+4,x+int(i*0.8),top+42],fill=STRIA)
    d.line([x-18,top+13,x+18,top+13],fill=STRIA,width=2)
    for ex in (x-10,x+10):
        d.ellipse([ex-5,top+15,ex+5,top+21],fill=TOOTH); d.rectangle([ex-1,top+17,ex,top+19],fill=(30,40,30))
    d.point((x-2,top+25),fill=(40,0,0)); d.point((x+2,top+25),fill=(40,0,0))
    d.rectangle([x-12,top+29,x+12,top+36],fill=TOOTH)
    for tx in range(x-12,x+13,3): d.line([tx,top+29,tx,top+36],fill=(150,120,110))
    d.line([x-12,top+32,x+12,top+32],fill=(120,30,26))

@fx('colossal')
def _fx_colossal(d,im,e,f):
    _,x,rise,hands=e; top=int(WALL_TOP+6-rise*40)
    head(d,x,top,rise); wall(d)
    im.paste(bg_for(THEME).crop((0,GROUND+1,W,H)),(0,GROUND+1))   # keep the head out of the floor
    if rise>0.8:   # fingers gripping the rampart
        for hx,on in zip((x-38,x+30),hands):
            if not on: continue
            for k in range(4): d.rectangle([hx+k*3,WALL_TOP-3,hx+k*3+1,WALL_TOP+4],fill=MUSCLE); d.point((hx+k*3,WALL_TOP+4),fill=TOOTH)

@fx('lightning')
def _fx_lightning(d,im,e,f):
    _,x=e; rr=random.Random(f); pts=[(x,0)]; px=x
    for y in range(4,WALL_TOP+1,4): px+=rr.randint(-4,4); pts.append((px,y))
    d.line(pts,fill=(255,236,140),width=3); d.line(pts,fill=(255,255,255),width=1)

@fx('sweep')
def _fx_sweep(d,im,e,f):
    """The Colossal's forearm dragging along the top of the Wall, right to left."""
    _,hx=e; hx=int(hx)
    if hx+10<W: d.rectangle([hx+10,WALL_TOP-9,W+4,WALL_TOP-2],fill=MUSCLE)
    for x in range(hx+12,W,5): d.line([x,WALL_TOP-9,x+2,WALL_TOP-2],fill=STRIA)
    d.ellipse([hx-2,WALL_TOP-12,hx+16,WALL_TOP],fill=MUSCLE); d.line([hx,WALL_TOP-6,hx+12,WALL_TOP-6],fill=STRIA)

def steam(s,x,y,t,n=10,spread=24,seed=0):
    rr=random.Random(seed+t//2)
    for j in range(n):
        s['fx'].append(('smoke',x+rr.randint(-spread,spread),y-rr.randint(0,spread//2)-t//2,rr.randint(2,5),(236,236,240) if j%2 else (196,196,204)))

def closeup_eye(t,f):
    """Primer plano: one enormous eye in raw muscle; the pupil snaps onto Claude (reflected in it)."""
    im=Image.new('RGB',(W,H),MUSCLE); d=ImageDraw.Draw(im)
    for x in range(-10,W+10,4): d.line([x,0,x+int(6*math.sin(x*0.3)),H],fill=STRIA)
    for x in range(-10,W+10,9): d.line([x+2,0,x+4,H],fill=(196,76,62))
    cx,cy=92,32
    d.ellipse([cx-58,cy-22,cx+58,cy+22],fill=(24,6,4)); d.ellipse([cx-55,cy-20,cx+55,cy+20],fill=(234,226,212))
    rr=random.Random(4)
    for _ in range(14):   # veins
        a=rr.random()*6.28; x0,y0=cx+math.cos(a)*54,cy+math.sin(a)*19
        d.line([x0,y0,x0-math.cos(a)*rr.randint(8,20),y0-math.sin(a)*rr.randint(3,8)],fill=(210,90,80))
    look=ease((t-0.2)/0.2); ix=int(cx+10-14*look)
    d.ellipse([ix-17,cy-17,ix+17,cy+17],fill=(70,86,66)); d.ellipse([ix-13,cy-13,ix+13,cy+13],fill=(96,116,88))
    pr=int(10-6*ease((t-0.4)/0.15)); d.ellipse([ix-pr,cy-pr,ix+pr,cy+pr],fill=(6,4,4))
    d.ellipse([ix-10,cy-11,ix-6,cy-7],fill=(255,255,255))
    if t>0.55:   # tiny Claude in the iris
        d.rectangle([ix+5,cy+4,ix+8,cy+7],fill=(217,119,87)); d.point((ix+6,cy+5),fill=(24,14,12)); d.point((ix+8,cy+5),fill=(24,14,12))
    for k in range(6):   # steam wisps
        y=int(H-((f*1.5+k*23)%(H+20))); x=(k*37+f)%W
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([x-10,y-5,x+10,y+5],fill=90)
        im.paste((236,236,240),(0,0),m)
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,(255,255,255),0.6*(t-0.9)/0.1)
    return im

TX=128   # the Colossal's head, behind the Wall
def clip_colossal(f):
    s=scene(f,THEME)
    cl=actor(SCOUT[guard_pose(f)],30); pos=(30,GROUND); pose=None; flip=False; wire=None
    # 1) lightning, and the head rises
    if 12<=f<24:
        s['under'].append(('lightning',TX)); s['shake']=rshake(2)
        if f<16: s['flash']=0.9; s['fc']=(TX,WALL_TOP); s['flashc']=(255,240,160)
    rise=0
    if 20<=f<60: rise=ease((f-20)/34)
    elif 60<=f<176: rise=1
    elif 176<=f<210: rise=1-ease((f-176)/34)
    if rise>0: s['under'].append(('colossal',TX,rise,(True,not 104<=f<134)))   # the right hand leaves the Wall to sweep it
    if 18<=f<60: steam(s,TX,WALL_TOP,f-18,n=8,spread=26,seed=1)
    if 24<=f<56 and f%4==0: s['shake']=rshake()
    # 2) eye close-up
    if 60<=f<104: s['image']=closeup_eye((f-60)/44,f); return s
    # 3) the arm sweeps the rampart; rubble rains down, Claude sidesteps
    if 104<=f<132:
        hx=lerp(200,-30,(f-104)/28); s['fx'].append(('sweep',hx))
        rr=random.Random(7)
        for j in range(22):
            x0=rr.randint(0,W); t0=104+int((200-x0)/230*28)
            if t0<=f<t0+14: k=f-t0; s['fx'].append(('rock',x0+rr.randint(-2,2),WALL_TOP-2+k*k*0.2))
        if f%3==0: s['shake']=rshake()
    if 114<=f<130:
        t=(f-114)/16; pos=(ez(30,12,t*2) if t<0.5 else ez(12,30,(t-0.5)*2),GROUND); pose='dash' if t<0.5 else 'guard'; flip=t<0.5
    # 4) ODM gear: up the Wall, a first pass blown back by steam, then the nape
    if 132<=f<142: t=(f-132)/10; pos=(lerp(30,70,ease(t)),lerp(GROUND,WALL_TOP,ease(t))-6*math.sin(math.pi*t)); pose='dash'; wire=(70,WALL_TOP)
    if 142<=f<150: pos=(70,WALL_TOP)
    if 146<=f<176: callout(s,"SASAGEYO!",c=(230,230,240))
    if 150<=f<158: t=(f-150)/8; pos=(lerp(70,112,ease(t)),lerp(WALL_TOP,10,ease(t))); pose='dash'; wire=(TX-6,-2)
    if 156<=f<168:
        steam(s,TX-8,20,f-156,n=16,spread=20,seed=3)
        if f>=158: t=(f-158)/10; pos=(lerp(112,84,t),lerp(10,20,t)); pose='hurt'
    if 168<=f<176: t=(f-168)/8; pos=(lerp(84,TX+16,ease(t)),lerp(20,6,ease(t))); pose='dash'; wire=(TX+22,-2); s['fx'].append(('circle',pos[0],pos[1]-6,8,(240,240,255)))
    if 176<=f<182:
        pos=(TX+16,6); pose='punch'; flip=f%2==0
        if f==176: s['fx'].append(('spark',TX+14,4,8)); s['flash']=0.8; s['fc']=(TX+14,6); s['shake']=rshake(2)
        s['fx'].append(('shard',TX+12+random.randint(-4,4),6+random.randint(-3,5),(230,60,50)))
    # 5) it falls back behind the Wall in a cloud of steam; Claude drops down
    if 176<=f<232: steam(s,TX,WALL_TOP,f-176,n=max(2,int(16*(1-(f-176)/56))),spread=30,seed=5)
    if 182<=f<200: t=(f-182)/18; pos=(lerp(TX+16,92,t),lerp(6,GROUND,t*t)); pose='guard'
    if 200<=f<226: pos=(ez(92,30,(f-200)/26),GROUND)
    cl.update(x=pos[0],y=pos[1],flip=flip)
    if pose: cl['spr']=SCOUT[pose]
    if wire: s['fx'].append(('wire',pos[0],pos[1]-5,*wire))
    s['fx'].append(('blades',cl['x'],cl['y'],flip))
    s['actors']=[cl]
    return s

CLIPS = [clip('colossal', 264, clip_colossal)]
