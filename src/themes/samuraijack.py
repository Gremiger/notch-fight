"""Samurai Jack: Claude is Jack (black topknot, white gi, geta, the katana) in the desert at sunset,
Aku's futuristic city on the horizon. LONG AGO, IN A DISTANT LAND... Aku (black, flame eyebrows,
green eyes, horns) laughs HA HA HA and drops three beetle robots. Genndy-style split screen: one
panel per robot creeping in, the last one Jack's hand on the hilt. Close-up: Jack's eyes narrow,
the gleam runs down the blade. One cut, silence, and all three robots slide apart leaking black
oil. ENOUGH! Aku melts into a giant hand that slams down; Jack leaps clear, then up, and takes a
finger off. Aku dissolves in smoke (CURSE YOU, SAMURAI!), Jack sheathes slowly; Aku reforms."""
import zlib
from engine import *

THEME = 'samuraijack'
N_ = 280
CX, VX = 30, 150                                                   # the neutral pose: Jack, Aku

# ---- Claude as Jack ----------------------------------------------------------------------------
def _jack(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y])
    m=(l+r)//2
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='O' and inside and y>=t+5: g[y][x]='O' if (y==t+5 and x in (m,m+1)) else 'W'   # the gi, a V of skin
            elif c=='o' and y>bot: g[y][x]='q' if y==h-1 else 'W'                              # hakama, geta
            elif c=='o': g[y][x]='W'                                                           # sleeves
    for x in range(l,r+1):
        if t+7<h and g[t+7][x]=='W': g[t+7][x]='v'                                             # the sash
    return overlay(ungrid(g),["...kkk....","...kkk....","....k.....",".kkkkkkkk."],-1,0,bangs="kkkkkkkk")
JACK=variant(_jack)
JACKPAL={'W':(238,234,222),'v':(190,184,170),'q':(120,84,50),'k':(18,16,20)}
HAND={'punch':(16,5),'dash':(16,5),'charge':(15,5)}                # the front hand, in CL coordinates
def hand(pose,x,feet,flip=False):
    hx,hy=HAND[pose]; return hand_at(JACK[pose],x,feet,flip,hx,hy,h=len(CL[pose]))

# ---- Aku ---------------------------------------------------------------------------------------
_AKU=[
".h..................h.",
".hh................hh.",
"..hh..............hh..",
"...hh...ffffff...hh...",
"....hhffFFyyFFffhh....",
".....kfFFyyyyFFfk.....",
"....kkkffFFFFffkkk....",
"...kkkGGGkkkkGGGkkk...",
"...kkkGEGkkkkGEGkkk...",
"...kkkkkkkkkkkkkkkk...",
"....kkkkrrrrrrkkkk....",
"....kkkkkrrrrkkkkk....",
".....kkkkkkkkkkkk.....",
"....mkkkkkkkkkkkkm....",
"..mmkkkkkkkkkkkkkkmm..",
".mkkk.kkkkkkkkkk.kkkm.",
".kkk..kkkkkkkkkk..kkk.",
".kk...kkkkkkkkkk...kk.",
".kk...kkkkkkkkkk...kk.",
".hh..mkkkkkkkkkkm..hh.",
"....mkkkkkkkkkkkkm....",
"...mkkkkkkkkkkkkkkm...",
"...kkkkkk....kkkkkk...",
"..kkkkkk......kkkkkk..",
"..kkkkk........kkkkk..",
".kkkkkk........kkkkkk.",]
_AKU2=[r.replace('ffFFyyFFff','fFFyyyyFFf') if i==4 else r for i,r in enumerate(_AKU)]   # the flames flicker
_LAUGH=_AKU[:7]+["...kkkGGGkkkkGGGkkk...","...kkkkkkkkkkkkkkkk...","...kkkkrrrrrrrrkkkk...",
                 "....kkkrrHHHHrrkkk....","....kkkkrrrrrrkkkk...."]+_AKU[12:]
def _arms_up(rows):
    g=[list(r) for r in rows]
    for y in range(15,20):
        for x in (1,2,3,18,19,20): g[y][x]='.'
    top=[list('.'*22) for _ in range(0)]
    for y in range(9,15):
        for x in (1,2,19,20): g[y][x]='k'
    for x in (1,2,19,20): g[8][x]='h'
    return S([''.join(r) for r in g])
AKU={'idle':S(_AKU),'idle2':S(_AKU2),'laugh':_arms_up(_LAUGH),'laugh2':_arms_up(_LAUGH[:4]+[_AKU2[4]]+_LAUGH[5:])}
AKU['hurt']=hurt(AKU['idle'])
AKUPAL={'h':(84,76,92),'f':(230,70,30),'F':(255,150,40),'y':(255,236,140),'k':(26,22,32),'m':(56,48,70),
        'G':(60,230,90),'E':(220,255,220),'r':(200,30,40),'H':(250,250,250)}
def aku_idle(f): return AKU['idle'] if (f//4)%2==0 else AKU['idle2']

# ---- the beetle robots -------------------------------------------------------------------------
_BOT=[
"....bbbbbb....",
"..bbBBBBBBbb..",
".bBBBBbbBBBBb.",
"bBBBBBbbBBBBBb",
"bBBBBBbbBBBBBb",
".bbbbbbbbbbbb.",
"rrkkkkkkkkkkkk",
".kkkkkkkkkkkk.",
".k.k..k..k.k..",
"k..k..k..k..k.",
"k...k.k.k...k.",]
_BOT2=_BOT[:8]+[".k.k..k..k.k..",".k..k.k.k..k..","k...k....k..k."]
BOT={'a':S(_BOT),'b':S(_BOT2),'top':S(_BOT[:6]),'bottom':S(_BOT[6:])}
BOTPAL={'b':(40,60,64),'B':(70,104,108),'k':(36,38,44),'r':(255,40,40)}
R0=[88,104,120]; R1=[66,84,102]                                    # robots: where they land, where they stop

# ---- background: the desert at sunset, Aku's city on the horizon --------------------------------
def _desert(d):
    for y in range(GROUND):
        k=y/GROUND
        c=(int(lerp(70,250,k)),int(lerp(20,120,k*k)),int(lerp(60,40,k)))
        d.line([0,y,W,y],fill=c)
    d.ellipse([22,22,58,58],fill=(255,210,120)); d.ellipse([26,26,54,54],fill=(255,236,170))   # the sun
    for x,w,h,sp in ((112,8,26,4),(122,6,34,6),(130,10,22,0),(142,5,40,8),(149,9,28,3),(160,7,32,5),(169,10,20,0)):
        d.rectangle([x,GROUND-h,x+w,GROUND],fill=(44,20,40))        # Aku's city: towers and spires
        if sp: d.polygon([(x,GROUND-h),(x+w,GROUND-h),(x+w//2,GROUND-h-sp)],fill=(44,20,40))
        for wy in range(GROUND-h+3,GROUND-2,4):
            for wx in range(x+1,x+w-1,3):
                if (wx*7+wy*3)%5==0: d.point((wx,wy),fill=(90,255,120))
    d.polygon([(0,GROUND),(0,GROUND-6),(30,GROUND-9),(70,GROUND-4),(110,GROUND-7),(150,GROUND-3),(W,GROUND-6),(W,GROUND)],
              fill=(150,70,40))                                    # dunes
    d.polygon([(0,GROUND),(40,GROUND-3),(90,GROUND-1),(140,GROUND-4),(W,GROUND-2),(W,GROUND)],fill=(118,52,34))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(96,42,30))
register_bg(THEME, lambda v: (v+40,v//2+10,v//3+6), decor=_desert)

# ---- effects -----------------------------------------------------------------------------------
@fx('sj_blade')
def _fx_blade(d,im,e,f):
    """The katana from the hand: guard, steel, a white edge."""
    _,x0,y0,x1,y1=e
    d.line([x0,y0,x1,y1],fill=(196,204,216),width=1)
    if abs(x1-x0)>2: d.point((x1,y1),fill=(255,255,255))
    d.line([x0,y0-1,x0,y0+1],fill=(220,180,60))

@fx('sj_slash')
def _fx_slash(d,im,e,f):
    _,x0,x1,y,a=e
    d.line([x0,y,x1,y],fill=(255,255,255),width=2 if a>0.5 else 1)
    if a>0.5: d.line([x0+10,y-1,x1-10,y-1],fill=(255,240,200))

@fx('sj_oil')
def _fx_oil(d,im,e,f):
    _,x,r=e; r=int(r)
    if r>0: d.ellipse([x-r,GROUND-1,x+r,GROUND+1],fill=(10,8,12))

@fx('sj_drip')
def _fx_drip(d,im,e,f):
    _,x,y=e; d.line([x,y,x,y+1],fill=(10,8,12))

@fx('sj_smoke')
def _fx_smoke(d,im,e,f):
    """Aku coming apart (or together): dark puffs around (x,y), spread s, size r."""
    _,x,y,s,r,seed=e; rr=random.Random(seed)
    for j in range(16):
        px=x+rr.uniform(-1,1)*s; py=y+rr.uniform(-1,1)*s*0.8-rr.random()*s*0.5
        rj=max(1,int(r*rr.uniform(0.5,1.2)))
        d.ellipse([px-rj,py-rj,px+rj,py+rj],fill=[(30,24,38),(48,36,60),(70,40,60)][j%3])

@fx('sj_hand')
def _fx_hand(d,im,e,f):
    """Aku's giant hand, fingers down: centre x, fingertips at y; cut=True drops the left finger."""
    _,x,y,cut=e; x=int(x); y=int(y); c=(26,22,32); o=(120,24,30)
    d.rectangle([x-12,min(-4,y-30),x+12,y-26],fill=c,outline=o)       # the arm, from the sky
    d.rounded_rectangle([x-17,y-30,x+17,y-12],radius=4,fill=c,outline=o)   # the palm
    for i,fx_ in enumerate((-14,-6,2,10)):
        if cut and i==0: continue
        top=y-14; ln=0 if i in (1,2) else 3
        d.rectangle([x+fx_,top,x+fx_+5,y-ln],fill=c,outline=o)
        d.polygon([(x+fx_,y-ln),(x+fx_+5,y-ln),(x+fx_+2,y-ln+3)],fill=(180,180,190))   # claws
    d.polygon([(x+17,y-26),(x+24,y-16),(x+22,y-10),(x+16,y-16)],fill=c,outline=o)    # the thumb
    d.ellipse([x-6,y-26,x-2,y-22],fill=(60,230,90)); d.ellipse([x+2,y-26,x+6,y-22],fill=(60,230,90))  # Aku's eyes on it

@fx('sj_finger')
def _fx_finger(d,im,e,f):
    _,x,y,t=e
    a=t*0.5; pts=[(0,0),(5,0),(5,12),(0,12)]
    ca,sa=math.cos(a),math.sin(a)
    d.polygon([(x+px*ca-py*sa,y+px*sa+py*ca) for px,py in pts],fill=(26,22,32),outline=(120,24,30))

@fx('sj_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))
def banner(s,txt,y,c,scale=2,outline=None): s['fx'].append(('sj_say',txt,y,c,scale,outline))

# ---- close-up: the eyes, the blade -------------------------------------------------------------
def closeup_jack(t,f):
    im=Image.new('RGB',(W,H),(20,6,10)); d=ImageDraw.Draw(im)
    if t<0.5:                                                       # the eyes
        u=t/0.5
        d.rectangle([0,0,W,16],fill=(18,16,20))                     # hair
        d.rectangle([0,16,W,50],fill=(217,119,87)); d.rectangle([0,50,W,H],fill=(196,100,72))
        nar=int(lerp(6,2,ease((u-0.3)/0.4)))                        # the eyes narrow
        for cx in (58,127):
            d.polygon([(cx-20,30),(cx+20,30-2),(cx+18,30+nar+2),(cx-18,30+nar)],fill=(250,246,236))
            d.ellipse([cx-4,30-1,cx+4,30+nar+1],fill=(24,14,12))
            d.line([cx-22,24-(cx>90)*0,cx+20,22+(cx>90)*0],fill=(18,16,20),width=3)   # brows
        d.line([92,34,92,48],fill=(176,92,66)); d.line([88,48,96,48],fill=(176,92,66))
        if u<0.12: zoom_lines(d,(255,230,200))
    else:                                                           # the blade, the gleam
        u=(t-0.5)/0.5
        for y in range(H): d.line([0,y,W,y],fill=(int(30+20*y/H),8,12))
        d.rectangle([4,29,40,35],fill=(20,18,24))                   # the hilt, the wrap
        for x in range(6,40,5): d.polygon([(x,29),(x+2,32),(x,35),(x-2,32)],fill=(200,170,70))
        d.rectangle([40,25,44,39],fill=(210,170,60))                # the tsuba
        d.polygon([(44,29),(176,29),(184,32),(176,35),(44,35)],fill=(190,198,212))
        d.line([44,29,176,29],fill=(250,252,255)); d.line([44,33,180,33],fill=(150,158,172))
        gx=int(lerp(44,182,ease(u/0.7)))
        if u<0.85:
            for k in range(-6,7): d.point((gx+k,30+(k%2)),fill=(255,255,255))
            spark(d,gx,31,4+(f%2),(255,255,255))
    return im

# ---- the clip ----------------------------------------------------------------------------------
def robots(s,f):
    """The three beetles: drop in, creep forward, get cut, slide apart; the hand crushes the pieces."""
    out=[]
    for i in range(3):
        d0=56+i*5
        if f<d0 or f>=202: continue
        if f<d0+8:
            y=int(ez(-14,GROUND,(f-d0)/8)); out.append(actor(BOT['a'],R0[i],y,pal=BOTPAL)); continue
        if f==d0+8: s['fx'].append(('dust',R0[i]-4,GROUND-1)); s['fx'].append(('dust',R0[i]+4,GROUND-1))
        x=R0[i] if f<76 else lerp(R0[i],R1[i],(f-76)/36)
        if f<158:
            spr=BOT['b'] if 76<=f<112 and (f//3)%2 else BOT['a']
            out.append(actor(spr,x,pal=BOTPAL))
        else:                                                       # the cut lands: the top slides off
            t=f-158-i*2
            if t<0: out.append(actor(BOT['a'],x,pal=BOTPAL)); continue
            out.append(actor(BOT['bottom'],x,pal=BOTPAL))
            dx=min(t,12)*0.6; dy=int(min(5,t*t*0.08))
            out.append(actor(BOT['top'],x+dx,GROUND-5+dy,pal=BOTPAL))
            s['under'].append(('sj_oil',x,min(9,t*0.5)))
            if t<20 and t%3==0: s['fx'].append(('sj_drip',int(x-2),GROUND-6+t%5))
    return out

def base(f):
    s=scene(f,THEME)
    cl=actor(JACK[guard_pose(f)],CX,pal=JACKPAL)
    ak=actor(aku_idle(f),VX,flip=True,pal=AKUPAL)
    bots=robots(s,f)
    s['actors']=[ak]+bots+[cl]
    return s,cl,ak

def panels(f):
    """Genndy split screen: one panel per robot creeping in, then Jack's hand on the hilt."""
    s,cl,ak=base(f)
    if f>=100: cl['spr']=JACK['charge']
    im=render(s,f); out=Image.new('RGB',(W,H),(0,0,0)); pw=43
    targets=[(lerp(R0[i],R1[i],(f-76)/36),GROUND-12) for i in range(3)]+[(CX+3,GROUND-10)]
    for i,(tx,ty) in enumerate(targets):
        if f<76+i*7: continue
        cw=pw/2; box=(int(tx-cw/2),int(ty-16),int(tx-cw/2)+int(cw)+1,int(ty+16))
        p=im.crop(box).resize((int(cw+1)*2,64),Image.NEAREST).crop((0,0,pw,H-4))
        x0=1+i*(pw+3); out.paste(p,(x0,2))
        ImageDraw.Draw(out).rectangle([x0-1,1,x0+pw,H-2],outline=(230,220,200))
    return out

def clip_aku(f):
    if 76<=f<112:
        s=scene(f,THEME); s['image']=panels(f); return s
    if 112<=f<140:
        s=scene(f,THEME); s['image']=closeup_jack((f-112)/28,f); return s
    s,cl,ak=base(f)
    fronts=[]
    # 1) the narration, Aku laughs, the robots drop
    if 6<=f<34: shout(s,"LONG AGO, IN A DISTANT LAND...",(255,236,200))
    if 34<=f<60:
        ak['spr']=AKU['laugh'] if (f//3)%2 else AKU['laugh2']; ak['x']=VX+(f//2)%2
        banner(s,"HA HA HA!",4,(90,255,120),2,(20,40,20))
    # 2) the cut: Jack dashes through all three
    if 140<=f<146:
        t=(f-140)/6; x=lerp(CX,128,t); cl.update(spr=JACK['dash'],x=x)
        hx,hy=hand('dash',x,GROUND); s['fx'].append(('sj_blade',hx,hy,hx+9,hy-1))
        for k in range(3): s['fx'].append(('mote',x-6-k*4,GROUND-6+k,(255,255,255)))
    if 144<=f<150: s['fx'].append(('sj_slash',40,132,GROUND-6,1-(f-144)/6))
    if f==144: s['flash']=0.4; s['fc']=(90,GROUND-6); s['flashc']=(255,255,255)
    if 146<=f<182:                                                  # frozen in the follow-through: silence
        cl.update(spr=JACK['charge'],x=128)
        hx,hy=hand('charge',128,GROUND); s['fx'].append(('sj_blade',hx,hy,hx+10,hy+4))
    # 3) ENOUGH!: Aku melts into a giant hand
    if 164<=f<180:
        ak.update(spr=AKU['laugh'],x=VX+((f//2)%2)*2-1); banner(s,"ENOUGH!",4,(255,90,60),2,(60,10,10))
    if 180<=f<188:
        t=(f-180)/8; ak['alpha']=1-t
        s['fx'].append(('sj_smoke',VX,GROUND-14,6+t*10,3,zlib.crc32(b'melt')+f))
    if 188<=f<224: ak['vis']=False
    HX=124
    if 184<=f<196: s['fx'].append(('sj_hand',HX,int(ez(-6,GROUND-22,(f-184)/12)),False))
    if 182<=f<196:                                                  # Jack leaps clear
        t=(f-182)/14; cl.update(spr=JACK['armsup'],x=lerp(128,70,t),y=GROUND-int(14*math.sin(math.pi*t)),flip=True)
    if 196<=f<200: s['fx'].append(('sj_hand',HX,int(lerp(GROUND-22,GROUND,(f-196)/4)),False))
    if f==200:
        s['shake']=rshake(3)
        for k in range(6): s['fx'].append(('dust',HX-18+k*7,GROUND-1))
    if 200<=f<214: s['fx'].append(('sj_hand',HX,GROUND,f>=210))
    if 196<=f<204: cl.update(spr=JACK[guard_pose(f)],x=70,flip=False)
    # 4) up onto it, a finger off
    if 204<=f<210:
        t=(f-204)/6; cl.update(spr=JACK['armsup'],x=lerp(70,HX-20,t),y=GROUND-int(22*math.sin(math.pi*t*0.5)))
    if 210<=f<216:
        cl.update(spr=JACK['punch'],x=HX-20,y=GROUND-22+int((f-210)*3.6))
        hx,hy=hand('punch',HX-20,cl['y']); s['fx'].append(('sj_blade',hx,hy,hx+10,hy+3))
    if f==210: s['fx'].append(('spark',HX-12,GROUND-8,7)); s['shake']=rshake(2); s['flash']=0.35; s['fc']=(HX-12,GROUND-8); s['flashc']=(170,255,170)
    if 210<=f<228:
        t=f-210; s['fx'].append(('sj_finger',HX-14-t*2,GROUND-14-int(10*math.sin(min(1,t/12)*math.pi))+max(0,t-12)*2,t))
    if 214<=f<224:
        t=(f-214)/10; s['fx'].append(('sj_hand',HX,int(lerp(GROUND,-20,ease(t))),True))
        s['fx'].append(('sj_smoke',HX,GROUND-20,10,3,zlib.crc32(b'hand')+f))
    if 216<=f<222: cl.update(spr=JACK['hurt'] if f<218 else JACK[guard_pose(f)],x=HX-20)
    # 5) Aku reforms, curses, dissolves; Jack walks back and sheathes slowly
    if 224<=f<232:
        ak.update(vis=True,spr=AKU['hurt'],alpha=(f-224)/8)
        s['fx'].append(('sj_smoke',VX,GROUND-14,14-(f-224),3,zlib.crc32(b'form')+f))
    if 232<=f<248: ak.update(vis=True,spr=AKU['hurt'] if f<238 else AKU['laugh'],alpha=1)
    if 232<=f<252: shout(s,"CURSE YOU, SAMURAI!",(90,255,120))
    if 248<=f<258:
        t=(f-248)/10; ak.update(vis=True,spr=AKU['hurt'],alpha=1-t)
        s['fx'].append(('sj_smoke',VX,GROUND-14,6+t*14,3,zlib.crc32(b'gone')+f))
    if 258<=f<262: ak['vis']=False
    if 262<=f<272:
        t=(f-262)/10; ak.update(vis=True,spr=aku_idle(f),alpha=t)
        s['fx'].append(('sj_smoke',VX,GROUND-14,14-t*12,max(1,int(3-t*2)),zlib.crc32(b'back')+f))
    if 222<=f<244:
        t=(f-222)/22; cl.update(spr=JACK[guard_pose(f)],x=lerp(HX-20,CX,t),flip=True,y=GROUND)
    if 244<=f<268:                                                  # the slow sheathe
        t=(f-244)/20; cl.update(spr=JACK['charge'],x=CX,flip=False,y=GROUND)
        hx,hy=hand('charge',CX,GROUND); ln=int(lerp(11,0,ease(t)))
        if ln>0: s['fx'].append(('sj_blade',hx,hy,hx+ln,hy+1))
    if f==264: s['fx'].append(('spark',CX+6,GROUND-5,2))
    if 264<=f<268: shout(s,"CLICK.",(255,255,255),y=GROUND-26)
    if f>=N_-8:                                                     # hold the exact loop keyframe
        cl.update(spr=JACK['guard'],x=CX,y=GROUND,flip=False); ak.update(vis=True,spr=AKU['idle'],alpha=1,x=VX)
    s['actors']=[a for a in s['actors']]+fronts
    return s

CLIPS = [clip('aku', N_, clip_aku)]
