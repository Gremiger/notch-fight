"""The Matrix: Claude (Neo, long black coat, tiny sunglasses) vs Agent Smith on a rooftop under the
digital rain. "MR. ANDERSON..." — Smith fires, bullet time: the rounds crawl through the air with
ripple rings — close-up of Neo's sunglasses reflecting them, then the world turns to code (HE IS
THE ONE) — the limbo dodge, one grazes him, the clones join in (ME TOO), a second volley — "NO." —
the bullets stop and drop, Smith turns to green code, Neo dives into him and he bursts into light.
Neo re-forms on his ledge and an Agent takes over a passer-by: Smith is back for the loop."""
from engine import *

THEME = 'matrix'
N_ = 288

# Theme colours live in each actor's `pal` (no PAL.update: other themes are added in parallel).
NEO_PAL={'C':(60,62,74),'Q':(6,6,8)}                       # coat, sunglasses
SMITH_PAL={'C':(58,60,70),'Q':(6,6,8),'t':(20,20,26)}      # suit, sunglasses, tie
BY_PAL={'c':(120,110,96),'u':(70,86,120)}                  # passer-by: jacket, jeans
GREEN=(90,230,120); DGREEN=(20,110,44)

# --- sprites ---------------------------------------------------------------------------------
def _neo(spr):
    """Sunglasses over both eyes (+ bridge, one glint), coat over the torso, a coat tail behind."""
    g=grid(spr); top,l,r=body_box(spr); w=len(g[0])
    eyes=[x for x in range(w) if g[top+2][x]=='K']
    for ex in eyes:
        for y in (top+2,top+3):
            for x in (ex-1,ex):
                if g[y][x]!='.': g[y][x]='Q'
    if len(eyes)>=2:
        for x in range(eyes[0],eyes[-1]): g[top+2][x]='Q'
        g[top+2][eyes[0]-1]='W'
    for y in range(top+5,min(top+9,len(g))):
        for x in range(l,r+1):
            if g[y][x] in 'Oo': g[y][x]='C'
    for y in range(top+9,len(g)):                          # the long coat hangs to the knees
        for x in (l,l+1,r-1,r):
            if 0<=x<w and g[y][x]=='.' and y<top+10: g[y][x]='C'
    return ungrid(g)
NEO={k:_neo(v) for k,v in CL.items()}
_g=grid(NEO['punch']); _g[4][15]=_g[4][16]=_g[3][16]='O'   # "NO." — palm up, fingers raised
NEO['stop']=ungrid(_g)
def _shear(spr,k):
    """Lean the upper body backwards (away from the facing direction) by k px per row."""
    out=[]
    for i,r in enumerate(spr):
        n=int(round(max(0,8-i)*k)); out.append(r[n:]+'.'*n)
    return S(out)
NEO['lean']=_shear(S(['...'+r for r in NEO['guard']]),0.35)
NEO['limbo']=S([                                           # bent over backwards, head nearly on the floor
"oo...................",
".oo..................",
"..oOOOO..............",
".OQQOQQOOOC..........",
".OOOOOOOCCCCC........",
"..OOOCCCCCCCCo.......",
".CC..CCCCCCCooo......",
"CC........oo...oo....",
"..........oo....oo...",])

SMITH_IDLE=S([
"....qqqqqq........","...qqqqqqqq.......","...qsssssss.......","...sQQQsQQQ.......","..HssssssssK......",
"..h.ssssss........","..h..ssss.........","..hCCWtWCCC.......",".CCCCWtWCCCC......",".CCCCCtCCCCC......",
".CC.CCCCCC.CC.....",".CC.CCCCCC.CC.....",".ss.CCCCCC.ss.....","....CCCCCC........","....CC..CC........",
"....CC..CC........","....CC..CC........","...kkk..kkk.......",])
_a=[r for r in SMITH_IDLE]
_a[10]=".CC.CCCCCCCCCsdddd"; _a[11]=".CC.CCCCCC...sd..."; _a[12]=".ss.CCCCCC........"   # handgun raised
SMITH={'idle':SMITH_IDLE,'attack':S(_a),'hurt':hurt(SMITH_IDLE)}
BARREL=(9,GROUND-8)   # muzzle offset from Smith's x (flipped: x-9)

_BY=["....qqqqq.........","...qqqqqqq........","...qsssssq........","...sssKssK........","...sssssss........",
     "....sssss.........",".....sss..........","...ccccccc........","..ccccccccc.......","..cc.cccc.cc......",
     "..cc.cccc.cc......","..ss.cccc.ss......","....ccccc.........","....uuuuu.........","....uu.uu.........",
     "....uu.uu........."]
BYSTANDER=[S(_BY+["...uu...uu........","...kk...kk........"]),S(_BY+["....uu.uu.........","....kk.kk........."])]

# --- background: rooftop at night, faint skyline ----------------------------------------------
def _roof(d):
    for x0,x1,top in ((0,22,30),(26,44,38),(50,70,24),(112,130,34),(136,160,28),(164,185,36)):
        d.rectangle([x0,top,x1,GROUND],fill=(7,11,9))
        for y in range(top+3,GROUND-2,4):
            for x in range(x0+2,x1-1,4):
                if (x*7+y*3)%5==0: d.point((x,y),fill=(18,34,22))
    d.rectangle([80,40,100,GROUND],fill=(9,12,10)); d.rectangle([84,34,96,40],fill=(9,12,10))   # water tower
    d.line([86,40,84,GROUND],fill=(12,16,13)); d.line([94,40,96,GROUND],fill=(12,16,13))
    d.rectangle([0,GROUND+2,W,H],fill=(12,14,14))                                            # the ledge
register_bg(THEME, lambda v: (v//3,v,v//2), decor=_roof)

# --- time warp: the rain slows to a crawl in bullet time, and still loops ------------------------
def _speed(f): return 0.12 if 34<=f<206 else 1.0
_CUM=[0.0]
for _f in range(N_): _CUM.append(_CUM[-1]+_speed(_f))
def tau(f): return N_*_CUM[f]/_CUM[N_]    # tau(0)=0, tau(N)=N: every column period divides N

_GLYPHS=[(0,0),(1,0),(0,1),(1,1)]
@fx('matrix_rain')
def _fx_rain(d,im,e,f):
    """Digital rain: columns of dim glyphs falling; heads brighter. bright scales everything."""
    _,t,bright=e; px=im.load()
    for i,x in enumerate(range(1,W,5)):
        rr=random.Random(i*977+13); k=rr.randint(2,5); off=rr.randint(0,95); L=rr.randint(4,9)
        head=(off+t*k/3)%96-20
        for j in range(L):
            y=int(head)-j*3
            if not (0<=y<GROUND-1): continue
            a=(1-j/L)*bright; gi=(i*5+j*3+int(t/4))%4
            c=(int(80*a),int(190*a),int(100*a)) if j==0 else (0,int(80*a),int(28*a))
            for gx,gy in ((0,0),_GLYPHS[gi]):
                if 0<=x+gx<W and 0<=y+gy<H:
                    o=px[x+gx,y+gy]; px[x+gx,y+gy]=tuple(max(o[q],c[q]) for q in range(3))

# --- green-code figure: a sprite seen as the Matrix sees it ------------------------------------
@fx('matrix_code')
def _fx_code(d,im,e,f):
    """Draw spr's silhouette as falling green code. keep: fraction of pixels shown; glow 0..1 whitens."""
    _,spr,cx,feet,flip,keep,glow=e; m,w,h=mask_of(spr,flip)
    ox=int(round(cx-w/2)); oy=int(round(feet-h)); px=im.load()
    for (x,y) in m:
        if ((x*37+y*61+f*3)%100)/100>=keep: continue
        ph=(y-f//2+(x*7)%5)%5
        c=(170,255,180) if ph==0 else (GREEN if ph<3 else DGREEN)
        c=tuple(int(lerp(c[q],255 if q!=0 else 230,glow)) for q in range(3))
        if 0<=ox+x<W and 0<=oy+y<H: px[ox+x,oy+y]=c

@fx('matrix_crack')
def _fx_crack(d,im,e,f):
    """Beams of green light breaking out of a body (Smith about to burst)."""
    _,x,y,n,L=e
    for k in range(n):
        a=k*2*math.pi/n+0.4; l=L*(0.6+0.4*((k*7)%3)/2)
        d.line([x,y,x+math.cos(a)*l,y+math.sin(a)*l*0.6],fill=(170,255,180))

@fx('matrix_burst')
def _fx_burst(d,im,e,f):
    _,x,y,r=e; rr=random.Random(f*5)
    d.ellipse([x-r,y-r//2,x+r,y+r//2],outline=GREEN); d.ellipse([x-r+3,y-r//2+2,x+r-3,y+r//2-2],outline=DGREEN)
    for _ in range(18):
        a=rr.random()*6.28; q=rr.uniform(0.3,1.1)*r
        d.point((x+math.cos(a)*q,y+math.sin(a)*q*0.5),fill=(200,255,210) if rr.random()<0.4 else GREEN)

# --- bullets ---------------------------------------------------------------------------------
@fx('matrix_bullet')
def _fx_bullet(d,im,e,f):
    """A slow bullet flying left: brass slug, a dim trail behind and air-ripple rings along it."""
    _,x,y,rings=e; x,y=int(x),int(y)
    d.line([x+3,y,x+16,y],fill=(34,40,38))
    if rings:
        for n,(dx,r) in enumerate(((5,2),(10,3),(16,4))):
            c=(110-n*28,140-n*30,130-n*30)
            d.ellipse([x+dx-1,y-r,x+dx+1,y+r],outline=c)
    d.line([x,y,x+2,y],fill=(220,190,110)); d.point((x,y),fill=(255,250,220))

@fx('matrix_slug')
def _fx_slug(d,im,e,f):
    """A stopped/falling bullet, turned upright."""
    _,x,y=e; d.line([int(x),int(y)-1,int(x),int(y)],fill=(220,190,110)); d.point((int(x),int(y)-1),fill=(255,250,220))

def _muzzle(s,x,y):
    s['fx'].append(('spark',x,y,3)); s['fx'].append(('ring',x-3,y,2,(255,220,140)))

# volley 1: (fired at, start x, start y, target y at Claude). Smith's muzzle: 150-9=141.
V1=[(34,141,GROUND-8,GROUND-11),(38,141,GROUND-8,GROUND-9),(42,141,GROUND-8,GROUND-8)]
V1_SPEED=1.3
def v1_pos(f,b):
    t0,x0,y0,yt=b; x=x0-V1_SPEED*(f-t0)
    return x,lerp(y0,yt,(x0-x)/(x0-30))
# volley 2: Smith + two clones fire, the rounds stop in mid-air at "NO."
V2=[(152,109,GROUND-8),(154,141,GROUND-8),(156,167,GROUND-8)]
V2_SPEED,STOP,DROP=1.5,186,202
def v2_pos(f,b,k):
    t0,x0,y0=b
    d=V2_SPEED*(min(f,STOP)-t0)
    if f>STOP: u=min(1,(f-STOP)/6); d+=V2_SPEED*3*u*(2-u)       # brake to a halt
    x=x0-d; y=y0+(k-1)*2
    if f>=DROP:                                                  # gravity takes them
        tt=f-DROP; y=min(GROUND,y+0.12*tt*tt); x-=tt*0.1*(k-1)
    return x,y

# --- close-up ---------------------------------------------------------------------------------
LENSES=((22,12,86,40),(100,12,164,40))
def closeup_glasses(t,f):
    """Primer plano: Neo's sunglasses reflect the incoming bullets, then the world as green code."""
    im=Image.new('RGB',(W,H),(186,98,70)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,5],fill=(140,66,46))
    for x in range(8): d.line([x,0,x,H],fill=(20+x*20,10+x*11,8+x*8)); d.line([W-1-x,0,W-1-x,H],fill=(20+x*20,10+x*11,8+x*8))
    d.line([0,18,22,18],fill=(6,6,8),width=2); d.line([164,18,W,18],fill=(6,6,8),width=2)     # temples
    d.line([86,17,100,17],fill=(6,6,8),width=2)                                                # bridge
    code=t>=0.55
    for i,(x0,y0,x1,y1) in enumerate(LENSES):
        lw,lh=x1-x0,y1-y0
        lens=Image.new('RGB',(lw,lh),(8,10,12)); ld=ImageDraw.Draw(lens)
        if not code:
            for k in range(3):   # three rounds growing as they approach, rings rippling out
                g=ease(t/0.55)*0.8+k*0.1
                cx=lw//2+int((k-1)*(10-6*g)); cy=lh//2+int((k-1)*3*(1-g))
                r=1+int(g*5)
                for q in range(3):
                    rq=r+2+q*3+int(f%3); cc=(50-q*12,80-q*20,74-q*18)
                    ld.ellipse([cx-rq,cy-rq,cx+rq,cy+rq],outline=cc)
                ld.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(200,170,100)); ld.point((cx-r//2,cy-r//2),fill=(255,250,220))
        else:
            for x in range(1,lw,4):   # the lenses fill with code
                rr=random.Random(x*31+i); k=rr.randint(1,3); L=rr.randint(3,6)
                head=(rr.randint(0,40)+f*k)%(lh+20)
                for j in range(L):
                    y=head-j*3
                    if 0<=y<lh:
                        c=(150,255,170) if j==0 else (0,int(200*(1-j/L)),int(60*(1-j/L)))
                        ld.point((x,y),fill=c); ld.point((x+(j%2),y+1),fill=c)
        ld.line([3,lh-4,lw//3,3],fill=(34,36,44))   # glint
        m=Image.new('L',(lw,lh),0); ImageDraw.Draw(m).rounded_rectangle([0,0,lw-1,lh-1],radius=8,fill=255)
        im.paste(lens,(x0,y0),m)
        d.rounded_rectangle([x0,y0,x1-1,y1-1],radius=8,outline=(6,6,8))
    if code: FX['big'](d,im,('big',"HE IS THE ONE",47,(120,255,150)),f)
    else: d.line([80,54,106,54],fill=(140,62,40))   # mouth
    if t<0.06:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(200,255,210))
    return im

# --- the clip ---------------------------------------------------------------------------------
def neo(pose,x=30,**kw): return actor(NEO[pose],x,pal=NEO_PAL,**kw)
def smith(pose,x=150,**kw): return actor(SMITH[pose],x,flip=True,pal=SMITH_PAL,**kw)

def clip_bullettime(f):
    s=scene(f,THEME)
    code_vis=206<=f<240
    bright=0.55+(0.35*(1-abs(f-222)/18) if code_vis else 0)
    s['under'].append(('matrix_rain',tau(f),bright))
    cl=neo(guard_pose(f)); sm=smith('idle')
    clones=[]
    # 1) MR. ANDERSON... Smith raises his gun and fires: bullet time
    if 8<=f<30: callout(s,"MR. ANDERSON...",c=(150,255,170))
    if 28<=f<52: sm['spr']=SMITH['attack']
    for t0,*_ in V1:
        if t0<=f<t0+2: _muzzle(s,141,GROUND-8); s['shake']=rshake(1) if f==t0 else (0,0)
    if 72<=f<108: s['image']=closeup_glasses((f-72)/36,f); return s
    for b in V1:
        if f>=b[0]:
            x,y=v1_pos(f,b)
            if x>-18: s['fx'].append(('matrix_bullet',x,y,True))
    # 2) the limbo dodge; the last round grazes him
    if 60<=f<72: cl['spr']=NEO['lean']
    if 108<=f<111 or 150<=f<156: cl['spr']=NEO['lean']
    if 111<=f<150: cl.update(spr=NEO['limbo'],x=26)
    if 127<=f<131:
        x,y=v1_pos(f,V1[2]); s['fx'].append(('spark',int(x)+1,int(y),2))
        if f==127: s['shake']=rshake(1)
    # clones step out of thin air, the second volley
    if 122<=f<232:
        for cx in (116,176):
            if f<136: s['fx'].append(('matrix_code',SMITH['idle'],cx,GROUND,True,(f-122)/12,0.4*(1-(f-122)/14)))
            else: clones.append(smith('attack' if 148<=f<172 else 'idle',cx))
    if 134<=f<146: s['fx'].append(('dmg',"ME TOO",104,20,(150,255,170)))
    if 140<=f<152: s['fx'].append(('dmg',"ME TOO",158,20,(150,255,170)))
    if 148<=f<172: sm['spr']=SMITH['attack']
    for b in V2:
        if b[0]<=f<b[0]+2: _muzzle(s,b[1],GROUND-8)
    # 3) "NO." — the bullets stop in mid-air and drop
    if 174<=f<206: cl['spr']=NEO['stop']
    if 180<=f<200: s['fx'].append(('big',"NO.",4,(200,255,210)))
    if f<232:
        for k,b in enumerate(V2):
            if f<b[0]: continue
            x,y=v2_pos(f,b,k)
            if f<STOP+4: s['under'].append(('matrix_bullet',x,y,f<STOP))   # behind the Agents in the line of fire
            else:
                jit=(1 if (f+k)%2 else 0) if f<DROP else 0
                s['fx'].append(('matrix_slug',x+jit,y))
                if y>=GROUND and f<DROP+14 and (f+k)%3==0: s['fx'].append(('mote',x+1,GROUND-1,(255,240,180)))
    # 4) Smith seen as code; Neo dives into him; Smith bursts into light
    agents=[sm]+clones
    if code_vis and f<234:
        keep_c=1.0 if f<222 else max(0,1-(f-222)/10)
        for a in agents:
            k=1.0 if a is sm else keep_c
            glow=0 if f<222 or a is not sm else (f-222)/12
            if k>0: s['fx'].append(('matrix_code',a['spr'],a['x'],a['y'],True,k,glow))
            a['vis']=False
    if 214<=f<222: cl.update(spr=NEO['dash'],x=ez(30,146,(f-214)/7),aura=(GREEN,1))
    if 222<=f<234:
        cl['vis']=False; s['fx'].append(('matrix_crack',150,GROUND-9,6+(f-222)//2,4+(f-222)*2))
        s['shake']=rshake(1)
    if 232<=f<236: s['flash']=0.6-(f-232)*0.14; s['fc']=(150,GROUND-9); s['flashc']=(140,255,170)
    if 232<=f<244: s['fx'].append(('matrix_burst',150,GROUND-9,6+(f-232)*4))
    if 234<=f<266: sm['vis']=False
    # Neo stands where Smith was, dissolves into code and re-forms on his ledge
    if 234<=f<242: cl.update(vis=True,spr=NEO[guard_pose(f)],x=150,aura=(GREEN,1) if f<238 else None)
    if 242<=f<248: cl['vis']=False; s['fx'].append(('matrix_code',NEO[guard_pose(f)],150,GROUND,False,1-(f-242)/6,0))
    if 246<=f<256:
        cl['vis']=False; s['fx'].append(('matrix_code',NEO[guard_pose(f)],30,GROUND,False,(f-246)/10,0))
    # 5) an Agent takes over a passer-by: Smith is back
    if 240<=f<262:
        bx=ez(200,150,(f-240)/18) if f<258 else 150
        s['actors'].append(actor(BYSTANDER[(f//4)%2 if f<258 else 1],bx,flip=True,pal=BY_PAL))
    if 258<=f<262 and f%2: s['actors'].pop(); s['fx'].append(('matrix_code',BYSTANDER[1],150,GROUND,True,1,0))
    if 262<=f<268: s['fx'].append(('matrix_code',SMITH['idle'],150,GROUND,True,1,0.3*(268-f)/6))
    if 262<=f<266: s['fx'].append(('ring',150,GROUND-9,4+(f-262)*3,GREEN))
    s['actors']=[cl]+s['actors']+[sm]+clones
    return s

CLIPS = [clip('bullettime', N_, clip_bullettime)]
