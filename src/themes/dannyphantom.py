"""Danny Phantom: Claude is Danny Fenton (messy black hair, white tee with the red circle, jeans)
in Amity Park at night, Fenton Works and its op-centre on the skyline, the green portal swirling at
its door. A blue wisp out of his mouth: the ghost sense. Skulker, the armoured ghost hunter with the
flaming mohawk: "I'LL HAVE YOUR PELT, WHELP!" Close-up: GOIN' GHOST! — two white rings sweep the
body into the black-and-white jumpsuit, white hair, green eyes. He floats; the shoulder launcher
fires, he goes intangible and the missiles fly right through him; a green ecto-blast. Close-up: the
Ghostly Wail, the shockwaves fill the screen and blow Skulker across the street. The Fenton Thermos
sucks him in a spinning vortex; the rings take Danny back to human. The thermos rattles, the lid
pops: Skulker reforms on his spot. "I'LL BE BACK, WHELP!" """
import zlib
from engine import *

THEME = 'dannyphantom'
N_ = 280
CX, VX = 30, 150                                                   # the neutral pose: Danny (human), Skulker
HOLD = 274                                                         # the last frames hold frame 0, for the loop
ECTO = (90,255,140)
ECTO_D = (30,170,80)
RING = (250,250,255)

# ---- Danny: the human form and the ghost form share their grid, so the rings can swap rows ----
def _danny(spr, ghost):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y])                  # the body's last row
    shirt=max(bot-3,max(y for y in range(h) if 'K' in spr[y])+2)   # below the eyes
    m=(l+r)//2
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='K' and ghost: g[y][x]='e'                                     # green eyes
            elif c=='O' and not inside: g[y][x]='W' if ghost else 'O'           # a fist: glove / skin
            elif c=='O' and y>=shirt:
                if ghost: g[y][x]='W' if (y==shirt and x in (m,m+1)) else 'k'    # the DP on the chest
                else: g[y][x]='r' if (y in (shirt,shirt+1) and x in (m,m+1)) else 'W'   # the red circle
            elif c=='o' and y>bot:                                               # legs, the last row the boots
                g[y][x]=('W' if y==h-1 else 'k') if ghost else ('k' if y==h-1 else 'J')
            elif c=='o' and y==bot and inside: g[y][x]='W' if ghost else 'J'    # belt / jeans
            elif c=='o': g[y][x]='W' if ghost else 'o'                          # gloves / arms
    hair='H' if ghost else 'k'
    pat=["..{0}{0}.{0}{0}{0}...".format(hair),".{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}".format(hair)]
    return overlay(ungrid(g),pat,-1,0,bangs=f"{hair}{hair}{hair}.{hair}{hair}.{hair}")
HUMAN={k:_danny(v,False) for k,v in CL.items()}
GHOST={k:_danny(v,True) for k,v in CL.items()}
DPAL={'W':(240,240,246),'r':(220,40,40),'J':(60,90,170),'k':(22,22,30),'H':(244,246,255),
      'e':ECTO,'o':(168,80,54)}

def mix(pose,prog,to_ghost=True):
    """The transformation: two rings start at the waist and sweep apart (prog 0..1); the rows
    between them have changed. Returns the sprite and the rings' rows (top, bottom)."""
    a,b=(HUMAN,GHOST) if to_ghost else (GHOST,HUMAN)
    sa,sb=a[pose],b[pose]; h=len(sa); mid=h*0.6; span=prog*(h*0.6+1)
    top,bottom=mid-span,mid+span*0.7
    rows=[sb[y] if top<=y<=bottom else sa[y] for y in range(h)]
    return S(rows),(int(top),int(bottom))

# ---- Skulker -------------------------------------------------------------------------------------
_SK=S([
".....GgG..........",
"....gGgGg.........",
"....GgGgG.........",
"...dddddd.........",
"..dDDDDDDd........",
"..dDeDDeDd........",
"..dDDDDDDd........",
"...dkWkWd.........",
"...dkkkkd...SSSSSS",
"..ddddddddddSSSSSs",
".dDDDDDDDDDDdSSSS.",
".dDDDdDDDdDDDd....",
".dDD.DDDDD.DDDd...",
".dDD.DDDDD.DDDd...",
".dDD.DDDDD.ddd....",
"..dd.DDDDD........",
".....ddddd........",
"....dDd.dDd.......",
"....dDd.dDd.......",
"....dDd.dDd.......",
"...ddDd.dDdd......",
"...dddd.dddd......",])
_SK2=S([r.translate(str.maketrans('Gg','gG')) if i<3 else r for i,r in enumerate(_SK)])   # the flame flickers
SK=poses(_SK,12,'D',3)
SK.update(idle2=_SK2,down=rotate90(hurt(_SK),3,trim=True))
SKPAL={'D':(112,134,124),'d':(58,72,68),'G':(60,200,100),'g':(150,255,170),'e':(255,70,60),
       'k':(20,24,24),'W':(230,230,230),'S':(146,146,158),'s':(40,40,46)}
def sk_idle(f): return SK['idle'] if (f//4)%2==0 else SK['idle2']
MUZZLE=hand_at(_SK,VX,GROUND,True,17,9)                            # the launcher, Skulker facing left

# ---- background: Amity Park at night ---------------------------------------------------------------
PORTAL=(118,GROUND-8)
def _amity(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(8+10*k),int(12+14*k),int(30+18*k)))
    rr=random.Random(zlib.crc32(b'amity-park'))
    for _ in range(30): d.point((rr.randint(0,W-1),rr.randint(0,30)),fill=rr.choice([(120,140,180),(80,100,140)]))
    d.ellipse([20,5,30,15],fill=(210,226,214))                    # the moon
    for x,w,h in ((0,18,20),(20,16,14),(38,14,24),(150,14,18),(166,19,26)):
        d.rectangle([x,GROUND-h,x+w,GROUND],fill=(18,22,40))
        for wy in range(GROUND-h+3,GROUND-3,4):
            for wx in range(x+2,x+w-1,4):
                if rr.random()<0.35: d.point((wx,wy),fill=(240,210,120))
    d.rectangle([98,GROUND-26,138,GROUND],fill=(28,34,52))        # Fenton Works
    for wy in (GROUND-21,GROUND-14):
        for wx in (102,112,126):
            d.rectangle([wx,wy,wx+4,wy+3],fill=(70,90,110))
    d.rectangle([102,GROUND-31,134,GROUND-27],fill=(40,48,70))   # the sign
    text(d,"FENTON",106,GROUND-31,(120,255,160),shadow=None)
    d.rectangle([110,GROUND-38,126,GROUND-32],fill=(44,52,76))   # the op-centre
    d.pieslice([108,GROUND-46,128,GROUND-30],180,360,fill=(60,70,96))
    d.line([118,GROUND-46,118,GROUND-52],fill=(150,160,180)); d.point((118,GROUND-53),fill=(255,80,80))
    d.ellipse([111,GROUND-14,125,GROUND-1],fill=(10,30,20))      # the portal's door
    d.rectangle([0,GROUND-1,W,GROUND],fill=(24,28,40))
register_bg(THEME, lambda v: (v//2+6,v+6,v//2+20), decor=_amity)

# ---- effects ----------------------------------------------------------------------------------------
@fx('dp_portal')
def _fx_portal(d,im,e,f):
    """The Fenton portal's green swirl."""
    x,y=PORTAL; f=0 if f>=HOLD else f
    for k in range(3):
        r=5-k*1.5; a=f*0.4+k*2
        d.ellipse([x-r-1,y-r,x+r+1,y+r],outline=[ECTO_D,ECTO,(200,255,220)][k])
        d.point((int(x+math.cos(a)*r),int(y+math.sin(a)*r)),fill=(220,255,230))

@fx('dp_sense')
def _fx_sense(d,im,e,f):
    """The ghost sense: a blue wisp out of the mouth, t frames old."""
    _,x,y,t=e
    for i in range(min(t,12)):
        px=x+i*0.9+math.sin(i*0.9)*1.5; py=y-i*0.8
        d.point((int(px),int(py)),fill=(150,210,255) if i<t-6 else (90,150,230))

@fx('dp_rings')
def _fx_rings(d,im,e,f):
    """The transformation rings around a sprite at world rows y0, y1."""
    _,x,y0,y1,w=e
    for y in (y0,y1):
        d.ellipse([x-w,y-1,x+w,y+1],outline=RING); d.line([x-w+1,y,x+w-1,y],fill=(200,230,255))

@fx('dp_missile')
def _fx_missile(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y)
    d.line([x+3,y,x+7,y],fill=(255,170,60)); d.point((x+8,y),fill=(255,240,140))
    d.rectangle([x-3,y-1,x+3,y+1],fill=(150,150,160)); d.point((x-4,y),fill=(220,40,40))

@fx('dp_thermos')
def _fx_thermos(d,im,e,f):
    """The Fenton Thermos on its side or standing: x, feet, lid open, shake."""
    _,x,y,open_,sh=e; x=int(x)+sh
    d.rectangle([x-2,y-8,x+2,y-1],fill=(230,232,238),outline=(90,94,104))
    d.rectangle([x-2,y-5,x+2,y-4],fill=ECTO_D)
    if open_: d.rectangle([x-4,y-12,x-1,y-10],fill=(110,120,130))
    else: d.rectangle([x-2,y-10,x+2,y-9],fill=(110,120,130))

@fx('dp_vortex')
def _fx_vortex(d,im,e,f):
    """The thermos's pull: a spiral cone from (x0,y0) out to (x1,y1)."""
    _,x0,y0,x1,y1=e
    for i in range(16):
        k=i/15; cx=lerp(x0,x1,k); cy=lerp(y0,y1,k); r=1+k*8; a=f*0.7-i*0.8
        d.point((int(cx+math.cos(a)*r*0.4),int(cy+math.sin(a)*r)),fill=(170,220,255))
        d.point((int(cx-math.cos(a)*r*0.4),int(cy-math.sin(a)*r)),fill=(90,150,255))
    d.line([x0,y0,x1,y1],fill=(200,235,255))

_SKIMG=sprite_img(_SK,SKPAL)
@fx('dp_sucked')
def _fx_sucked(d,im,e,f):
    """Skulker shrinking and spinning into the thermos: centre, scale, angle."""
    _,x,y,s,a=e
    if s<=0.05: return
    sp=_SKIMG.resize((max(1,int(_SKIMG.width*s)),max(1,int(_SKIMG.height*s))),Image.NEAREST).rotate(a,expand=True)
    im.paste(sp,(int(x-sp.width/2),int(y-sp.height/2)),sp)

@fx('dp_wave')
def _fx_wave(d,im,e,f):
    """The Ghostly Wail's shockwaves out of (x,y), t frames old."""
    _,x,y,t=e
    for j in range(4):
        r=t*9-j*10
        if r>2: d.ellipse([x-r,y-r*0.55,x+r,y+r*0.55],outline=[(220,255,235),ECTO,ECTO_D,(150,200,255)][j],width=2 if j<2 else 1)

@fx('dp_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline,cx=e; big_text(im,txt,y,c,scale=scale,outline=outline,cx=cx)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))
def banner(s,txt,y,c,scale=2,outline=None,cx=W//2): s['fx'].append(('dp_say',txt,y,c,scale,outline,cx))

# ---- close-ups --------------------------------------------------------------------------------------
def _bg_close(f,c=(8,14,34)):
    im=Image.new('RGB',(W,H),c); d=ImageDraw.Draw(im)
    for i in range(14):
        a=i*math.tau/14+f*0.03
        d.line([50,32,50+math.cos(a)*200,32+math.sin(a)*120],fill=(14,40,40))
    return im,d

def closeup_goin(t,f):
    """GOIN' GHOST!: the rings sweep the body, scaled up."""
    im,d=_bg_close(f)
    prog=ease((t-0.15)/0.5)
    spr,(r0,r1)=mix('armsup',prog)
    sc=4; img=sprite_img(spr,DPAL,scale=sc)
    ox,oy=50-img.width//2,62-img.height
    if 0.15<=t<0.68:                                              # the glow between the rings
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).rectangle([ox,oy+(r0+1)*sc,ox+img.width,oy+(r1+1)*sc],fill=110)
        im.paste((200,255,220),(0,0),g.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    im.paste(img,(ox,oy),img); d=ImageDraw.Draw(im)
    if 0.15<=t<0.7:
        for ry in (r0,r1):
            y=oy+(ry+1)*sc+2
            d.ellipse([ox-6,y-3,ox+img.width+6,y+3],outline=RING,width=2)
    if t>=0.5:
        jx=(f%3)-1 if t<0.6 else 0
        big_text(im,"GOIN'",12,(255,255,255),scale=2,cx=128+jx,outline=(20,110,60))
        big_text(im,"GHOST!",30,(255,255,255),scale=3,cx=128+jx,outline=(20,110,60))
    if t<0.06: zoom_lines(d,ECTO)
    return im

def closeup_wail(t,f):
    """The Ghostly Wail: the face, the mouth wide open, shockwaves filling the screen."""
    im,d=_bg_close(f,(4,10,24))
    head=S([r[:11] for r in GHOST['guard'][:7]]+["...OOOOOOOO"]*2)  # the face, a chin added for the mouth
    img=sprite_img(head,DPAL,scale=5)
    sh=(f%3-1)*2 if t>=0.3 else 0
    ox,oy=60-img.width//2+sh,4
    mx,my=ox+int(8.5*5),oy+8*5+2
    if t>=0.3:                                                    # the waves out of the mouth
        for j in range(6):
            r=((t-0.3)*260+j*16)%110
            d.ellipse([mx-r,my-r*0.6,mx+r,my+r*0.6],outline=[(220,255,235),ECTO,ECTO_D][j%3],width=3 if j%3==0 else 2)
    im.paste(img,(ox,oy),img); d=ImageDraw.Draw(im)
    o=int(lerp(1,5,ease((t-0.2)/0.12)))                            # the mouth opens
    d.ellipse([mx-6,my-o,mx+6,my+o],fill=(10,10,14))
    if t>=0.3:
        txt="A"*min(7,int((t-0.3)*30)+3)+"!"
        big_text(im,txt,26,(220,255,235),scale=2,cx=142+sh,outline=(20,110,60))
    if t>=0.85: im=fade_to(im,(220,255,235),(t-0.85)/0.15*0.8)
    if t<0.06: zoom_lines(d,ECTO)
    return im

# ---- the clip -----------------------------------------------------------------------------------------
FLY=(46,GROUND-10)                                                # where the ghost floats
def clip_ghost(f):
    if f>=HOLD: f=0
    s=scene(f,THEME); s['under'].append(('dp_portal',))
    cl=actor(HUMAN[guard_pose(f)],CX,pal=DPAL)
    sk=actor(sk_idle(f),VX,flip=True,pal=SKPAL)
    # 1) the ghost sense; Skulker
    if 8<=f<26:
        s['fx'].append(('dp_sense',CX+3,GROUND-7,f-8))
        if f>=12: s['fx'].append(('dmg','!',CX+1,GROUND-22,(150,210,255)))
    if 22<=f<42: shout(s,"I'LL HAVE YOUR PELT, WHELP!",(150,255,170))
    # 2) GOIN' GHOST!
    if 42<=f<74: s['image']=closeup_goin((f-42)/32,f); return s
    # 3) up in the air
    bob=(f//5)%2
    if 74<=f<82: cl.update(spr=GHOST['armsup'],x=ez(CX,FLY[0],(f-74)/8),y=int(ez(GROUND,FLY[1],(f-74)/8)))
    if 82<=f<206 and not (120<=f<200): cl.update(spr=GHOST[guard_pose(f)],x=FLY[0],y=FLY[1]+bob)
    # 4) the missiles go right through
    for k,f0 in enumerate((84,96,108)):
        if f0<=f<f0+16:
            t=(f-f0)/16; x=lerp(MUZZLE[0],-12,t); y=lerp(MUZZLE[1],FLY[1]-6+k*2,min(1,t*1.6))
            s['fx'].append(('dp_missile',x,y))
            for j in range(3): s['fx'].append(('mote',x+9+j*3,y+random.randint(-1,1),(200,200,210)))
        if f==f0: s['fx'].append(('spark',MUZZLE[0],MUZZLE[1],3))
        if f==f0+15: s['fx'].append(('boom',4,FLY[1]-4+k*2,2))
    if 80<=f<122: sk['spr']=SK['attack'] if (f-84)%12<4 else sk_idle(f)
    if 88<=f<120: cl.update(alpha=0.45+0.15*((f//2)%2),tint=(170,220,255))           # intangible
    if 108<=f<122: shout(s,"MISSED ME!",(240,240,246))
    # 5) the ecto-blast
    if 122<=f<132:
        cl.update(spr=GHOST['punch'],x=FLY[0],y=FLY[1])
        hx,hy=hand_at(GHOST['punch'],FLY[0],FLY[1],False,len(GHOST['punch'][0])-1,len(GHOST['punch'])-6)
        if f>=124: s['fx'].append(('beam',hx+1,VX-8,hy,(ECTO_D,ECTO)))
    if 120<=f<122: cl.update(spr=GHOST['charge'],x=FLY[0],y=FLY[1]); s['fx'].append(('orbc',FLY[0]+8,FLY[1]-5,2,(ECTO_D,ECTO)))
    if f==128: s['fx'].append(('spark',VX-6,GROUND-14,7)); s['shake']=rshake(2)
    if 126<=f<146:
        sk.update(spr=SK['hurt'],x=ez(VX,VX+6,(f-126)/4))
        s['fx'].append(('dmg','40',VX-4,GROUND-34-(f-126)//3,ECTO))
    if 146<=f<152: sk.update(spr=SK['attack'],x=VX+6)
    if 132<=f<152: shout(s,"WHY YOU LITTLE...",(150,255,170))
    if 132<=f<152: cl.update(spr=GHOST[guard_pose(f)],x=FLY[0],y=FLY[1]+bob)
    # 6) the Ghostly Wail
    if 152<=f<184: s['image']=closeup_wail((f-152)/32,f); return s
    if 184<=f<200:
        t=f-184; cl.update(spr=GHOST['armsup'],x=FLY[0],y=FLY[1])
        s['fx'].append(('dp_wave',FLY[0]+5,FLY[1]-8,t+6)); s['shake']=rshake(2 if t<8 else 1)
        sk.update(spr=SK['hurt'],x=ez(VX+6,168,t/10),y=GROUND-int(8*math.sin(math.pi*min(1,t/10))))
        if t%3==0: s['fx'].append(('spark',sk['x']-4,GROUND-12+t%5,4))
    if 194<=f<214: sk.update(spr=SK['down'],x=168,y=GROUND)
    # 7) the Fenton Thermos
    TX=86
    if 200<=f<206: cl.update(spr=GHOST['guard'],x=ez(FLY[0],TX-10,(f-200)/6),y=int(ez(FLY[1],GROUND,(f-200)/6)))
    if 206<=f<232:
        cl.update(spr=GHOST['charge'],x=TX-10,y=GROUND)
        s['fx'].append(('dp_thermos',TX,GROUND-3,True,0))
    if 206<=f<226:
        t=(f-206)/20; sx=lerp(168,TX+2,ease(t)); sy=lerp(GROUND-10,GROUND-13,t)
        s['fx'].append(('dp_vortex',TX+2,GROUND-13,int(lerp(168,TX+8,ease(t))),GROUND-10))
        s['fx'].append(('dp_sucked',sx,sy,max(0,1-ease(t)*1.05),(f-206)*40))
        sk['vis']=False
        if f>=210: shout(s,"GOTCHA!",(240,240,246))
    if 226<=f<264: sk['vis']=False
    # 8) back to human; the thermos rattles and pops; Skulker reforms
    if 232<=f<246:
        spr,(r0,r1)=mix(guard_pose(f),ease((f-232)/12),to_ghost=False)
        cl.update(spr=spr,x=TX-10,y=GROUND)
        ox,oy=origin(spr,TX-10)
        if f<244: s['fx'].append(('dp_rings',TX-10,oy+r0,oy+r1,9))
    if 232<=f<254: s['fx'].append(('dp_thermos',TX+4,GROUND,False,(f%2)*(1 if f>=244 else 0)))
    if 246<=f<270: cl.update(spr=HUMAN[guard_pose(f)],x=ez(TX-10,CX,(f-246)/20),flip=f<266)
    if f==254:
        s['flash']=0.5; s['fc']=(TX+4,GROUND-8); s['flashc']=(170,255,200); s['shake']=rshake(2)
    if 254<=f<258: s['fx'].append(('dp_thermos',TX+4,GROUND,True,0)); s['fx'].append(('spark',TX+2,GROUND-10,5))
    if 254<=f<264:
        t=(f-254)/10; s['fx'].append(('dp_vortex',int(lerp(TX+4,VX,t)),GROUND-int(14+10*math.sin(math.pi*t)),int(lerp(TX+4,VX,t))+2,GROUND-12))
    if 262<=f<274: sk.update(vis=True,holo=min(1,(f-262)/8))
    if 258<=f<274: shout(s,"I'LL BE BACK, WHELP!",(150,255,170))
    s['actors']=[sk,cl]
    return s

CLIPS = [clip('ghost', N_, clip_ghost)]
