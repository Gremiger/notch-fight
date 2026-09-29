"""Minecraft: Claude (Steve-style: brown hair, cyan shirt, blue trousers, diamond sword) in the End.
A Creeper walks up and hisses — close-up of its face right behind Claude's shoulder — and blows a
blocky crater out of the ground. The Ender Dragon flies in, healed by the End Crystals: Claude
pillars up, shoots both crystals, survives the purple breath, jumps down and slashes the perched
dragon's head. It dies in the classic burst of light beams, dissolving into XP orbs over the exit
portal — THE END — and the whole island respawns for the loop."""
from engine import *

THEME = 'mc'
N_ = 300

# Steve colours ride on the actor's own palette (no PAL keys added).
MCP = {'a':(84,54,30),'c':(0,168,168),'t':(52,58,170),'u':(34,36,110),'z':(90,90,96),
       'l':(140,98,52),'i':(80,220,210),'I':(190,255,245),'x':(30,90,96)}

def _paint(spr, pts):
    """Paint (x,y,ch) pixels in the sprite's own coords; grows up / sideways (symmetric, so the
    sprite stays centred on the same x) when a pixel falls outside."""
    g=[list(r) for r in spr]; w=len(g[0])
    padt=max(0,-min(y for _,y,_ in pts)); padr=max(0,max(x for x,_,_ in pts)-(w-1))
    g=[['.']*w for _ in range(padt)]+g
    g=[['.']*padr+r+['.']*padr for r in g]
    for x,y,c in pts: g[y+padt][x+padr]=c
    return S([''.join(r) for r in g])

def _steveify(spr):
    """Flat-top hair, cyan shirt below the eyes, blue trousers, dark legs and grey shoes."""
    spr=overlay(spr,["aaaaaaaa"],0,0)
    g=[list(r) for r in spr]; h=len(g)
    t=next(y for y,r in enumerate(spr) if r.count('O')>=6)
    xs=[x for x,c in enumerate(spr[t]) if c=='O']; l,r=min(xs),max(xs)
    e=next(y for y,r in enumerate(spr) if 'K' in r)
    lb=max(y for y,row in enumerate(spr) if 'O' in row[l:r+1])
    body=list(range(e+2,lb+1)); trou=body[-2:] if len(body)>=4 else body[-1:]
    for y in range(h):
        for x in range(len(g[0])):
            c=g[y][x]
            if c not in 'Oo': continue
            inside=l<=x<=r
            if y==t and inside and x<=l+1: g[y][x]='a'
            elif y==t+1 and x==l: g[y][x]='a'
            elif y in trou and inside: g[y][x]='t'
            elif y in body and inside: g[y][x]='c'
            elif y>lb: g[y][x]='z' if y==h-1 else 'u'
    return S([''.join(r) for r in g])

_SW_UP=[(13,2,'l'),(12,1,'x'),(13,1,'x'),(14,1,'x')]+[(13,y,'i') for y in range(-3,1)]+[(14,y,'I') for y in range(-3,1)]+[(13,-4,'I')]
_SW_FWD=[(17,5,'l'),(17,6,'l')]+[(18,y,'x') for y in (4,5,6,7)]+[(x,5,'I') for x in range(19,25)]+[(x,6,'i') for x in range(19,25)]+[(25,5,'I')]
_BOW=[(16,5,'l'),(16,6,'l'),(16,4,'l'),(16,7,'l'),(15,3,'l'),(15,8,'l'),(14,2,'l'),(14,9,'l'),(13,3,'D'),(13,4,'D'),(13,7,'D'),(13,8,'D')]
_ARMED={'guard':_SW_UP,'guard2':_SW_UP,'punch':_SW_FWD,'dash':_SW_FWD,'charge':_BOW}
STEVE0={k:_steveify(v) for k,v in CL.items()}                                   # unarmed (close-up)
STEVE={k:_steveify(_paint(v,_ARMED[k]) if k in _ARMED else v) for k,v in CL.items()}

_CR_TOP=["GjGGgGjG","GGgGGGGg","GKKGGKKG","gKKgGKKG","GGGKKGGg","GjKKKKGG","GGKGGKGj","gGKGGKGG",
         "..GgGj..","..jGGG..","..GGgG..","..gGGj..","..GjGG..","..GGgG.."]
CREEPER=[S(_CR_TOP+["GgG..GjG","GGg..gGG","ggg..ggg"]),S(_CR_TOP+[".GgGGjG.",".gGGGgG.",".gggggg."])]

CRYS=((64,26),(164,20))      # obsidian pillar tops carrying the End Crystals
CRATER=(38,62)

def _island(d):
    rr=random.Random(4)
    for _ in range(26): d.point((rr.randint(0,W-1),rr.randint(12,50)),fill=(34,22,48))
    for x0,top,w,dim in ((10,30,5,True),(118,34,5,True),(59,26,11,False),(159,20,11,False)):
        oc=(12,8,20) if dim else (20,12,32)
        d.rectangle([x0,top,x0+w-1,GROUND],fill=oc,outline=(28,18,42) if dim else (42,26,64))
        for _ in range(w*3): d.point((rr.randint(x0+1,x0+w-2),rr.randint(top+1,GROUND-1)),fill=(54,32,84) if not dim else (26,16,40))
        if not dim: d.rectangle([x0+2,top-3,x0+w-3,top-1],fill=(64,64,64),outline=(90,90,90))
    for x in range(0,W,6):
        d.rectangle([x,GROUND+1,x+5,H-1],fill=(58,56,38) if (x//6)%2 else (66,64,44))
        d.line([x,GROUND+1,x+5,GROUND+1],fill=(92,90,60))
        for _ in range(2): d.point((x+rr.randint(0,5),rr.randint(GROUND+2,H-1)),fill=(44,42,28))
register_bg(THEME, lambda v: (v,v,v*2//3), decor=_island)

# ---------------- HUD ----------------
_HEART=["rr.rr","rrrrr",".rrr.","..r.."]
_DRUM=["..mm.",".mmm.","mmm..","b...."]
_ICONS=[  # 5x4 hotbar icons
 (["...iI","..ii.","xli..","l.x.."],{'i':(80,220,210),'I':(190,255,245),'x':(30,90,96),'l':(140,98,52)}),
 (["iiii.","...l.","..l..",".l..."],{'i':(80,220,210),'l':(140,98,52)}),
 ([".ll.s","l..s.","l.s..",".s..."],{'l':(140,98,52),'s':(200,200,200)}),
 (["...dd","..ld.",".l...","f...."],{'d':(170,170,180),'l':(140,98,52),'f':(230,230,230)}),
 (["ggGgg","gGggG","GggGg","ggGgg"],{'g':(110,110,110),'G':(70,70,70)}),
 ([".pp..","pPPp.","pPPp.",".pp.."],{'p':(20,90,80),'P':(60,200,170)}),
 ([".y...","yYYy.","yYYy.",".yy.."],{'y':(200,160,20),'Y':(255,230,90)}),
 (["bbbbb","bBbBb","bbbbb","....."],{'b':(150,100,40),'B':(200,150,70)}),
 (["d...d","dwwwd","dwwwd",".ddd."],{'d':(150,150,160),'w':(50,90,230)}),
]

def _pat(d,x,y,rows,cols,alpha_im=None):
    for j,row in enumerate(rows):
        for i,ch in enumerate(row):
            if ch!='.': d.point((x+i,y+j),fill=cols[ch])

@fx('mc_hud')
def _fx_hud(d,im,e,f):
    """Hearts (half-heart units) top-left, hunger top-right, XP bar + 9-slot hotbar at the bottom."""
    _,hp,blink,xp,lvl,sel=e
    low=hp<=8
    for i in range(10):
        x=2+i*6; y=2+(((f//2+i*3)%3==0) if low else 0)
        _pat(d,x,y,_HEART,{'r':(70,16,16)})
        v=hp-i*2
        if v>0:
            col=(240,240,240) if blink and f%2==0 else (220,30,30)
            rows=_HEART if v>=2 else [r[:3] for r in _HEART]
            _pat(d,x,y,rows,{'r':col}); d.point((x,y),fill=(255,170,170))
    for i in range(10): _pat(d,124+i*6,2,_DRUM,{'m':(170,100,50),'b':(230,220,200)})
    x0=60
    d.line([x0+1,GROUND-1,x0+62,GROUND-1],fill=(16,36,8))
    if xp>0: d.line([x0+1,GROUND-1,x0+1+int(61*min(1,xp)),GROUND-1],fill=(120,230,40))
    if lvl>0: s=str(lvl); text(d,s,x0+32-len(s)*2,GROUND-8,(128,255,32))
    for i in range(9):
        x=x0+i*7; d.rectangle([x,GROUND,x+7,H-1],fill=(22,22,22),outline=(70,70,70))
        _pat(d,x+2,GROUND+1,*_ICONS[i])
    x=x0+sel*7; d.rectangle([x,GROUND,x+7,H-1],outline=(230,230,230))

@fx('mc_boss')
def _fx_boss(d,im,e,f):
    _,v=e; name="ENDER DRAGON"
    text(d,name,W//2-len(name)*2,1,(230,230,230))
    d.rectangle([W//2-30,7,W//2+30,8],fill=(60,10,50))
    if v>0: d.rectangle([W//2-30,7,W//2-30+int(60*v),8],fill=(230,60,200))

# ---------------- world fx ----------------
@fx('mc_crystal')
def _fx_crystal(d,im,e,f):
    """End Crystal floating over its bedrock: a spinning cube (square <-> diamond), pink core, flame."""
    _,x,top,a=e
    def c(rgb): return tuple(int(v*a) for v in rgb)
    y=top-9+(1 if (f//6)%2 else 0)
    if (f//5)%2: d.rectangle([x-3,y-3,x+3,y+3],outline=c((200,120,230)))
    else: d.polygon([(x,y-4),(x+4,y),(x,y+4),(x-4,y)],outline=c((200,120,230)))
    d.rectangle([x-1,y-1,x+1,y+1],fill=c((255,140,255))); d.point((x,y),fill=c((255,230,255)))
    d.point((x-1+(f%3),top-4),fill=c((255,140,60)))

@fx('mc_heal')
def _fx_heal(d,im,e,f):
    """The crystal's healing beam feeding the dragon (flickering dashes)."""
    _,x0,y0,x1,y1=e; n=max(1,int(math.hypot(x1-x0,y1-y0)))
    for k in range(0,n,1):
        if (k+f)%4==0: continue
        t=k/n; d.point((lerp(x0,x1,t),lerp(y0,y1,t)),fill=(255,170,255) if (k+f)%4==1 else (190,90,230))

@fx('mc_block')
def _fx_block(d,im,e,f):
    """A placed cobblestone block (8x6), bottom at y."""
    _,x,y=e; rr=random.Random(int(y))
    d.rectangle([x-4,y-6,x+3,y-1],fill=(110,110,110),outline=(62,62,62))
    for _ in range(5): d.point((x-3+rr.randint(0,5),y-5+rr.randint(0,3)),fill=(76,76,76))

@fx('mc_crater')
def _fx_crater(d,im,e,f):
    """The creeper's hole: end-stone blocks missing from the ground, a scorched stepped rim."""
    _,x0,x1,k=e     # k: 0..1 how much of it is still missing (respawn refills it)
    cols=[x for x in range(x0,x1,6)]
    n=int(round(len(cols)*k))
    mid=(x0+x1)/2
    for x in sorted(cols,key=lambda c: abs(c+3-mid))[:n]:
        deep=abs(x+3-mid)<(x1-x0)/3
        d.rectangle([x,GROUND+1 if deep else GROUND+3,x+5,H-1],fill=(4,2,6))
        d.line([x,GROUND+1,x+5,GROUND+1],fill=(34,28,22))

@fx('mc_debris')
def _fx_debris(d,im,e,f):
    """Blocky debris thrown up by an explosion, falling with gravity: x,y,t(frames),seed,count,colors."""
    _,x,y,t,seed,n,cols=e; rr=random.Random(seed)
    for k in range(n):
        vx=rr.uniform(-2.4,2.4); vy=rr.uniform(-3.4,-1.0); c=rr.choice(cols); s=rr.choice((1,2,2))
        px=x+vx*t; py=y+vy*t+0.22*t*t
        px,py=int(px),int(py)
        if py<GROUND: d.rectangle([px,py,px+s-1,py+s-1],fill=c)

@fx('mc_puff')
def _fx_puff(d,im,e,f):
    """Explosion smoke: square grey puffs that spread and shrink."""
    _,x,y,t,seed=e; rr=random.Random(seed)
    for k in range(12):
        a=rr.uniform(0,6.28); sp=rr.uniform(0.6,1.6); life=rr.uniform(10,18)
        if t>life: continue
        u=t/life; px=x+math.cos(a)*sp*t*1.6; py=y+math.sin(a)*sp*t*0.8-t*0.4
        s=max(1,int(5*(1-u))); g=int(lerp(200,70,u)); px,py=int(px),int(py)
        d.rectangle([px-s,py-s,px+s,py+s],fill=(g,g,g))

@fx('mc_arrow')
def _fx_arrow(d,im,e,f):
    """An arrow along a quadratic arc, at progress p (0..1)."""
    _,x0,y0,x1,y1,lift,p=e
    def at(u): return (lerp(x0,x1,u), lerp(y0,y1,u)-lift*4*u*(1-u))
    hx,hy=at(p); tx,ty=at(max(0,p-0.12))
    d.line([tx,ty,hx,hy],fill=(140,98,52)); d.point((hx,hy),fill=(200,200,210)); d.point((tx,ty),fill=(240,240,240))

@fx('mc_breath')
def _fx_breath(d,im,e,f):
    """Dragon's breath: a stream of purple blocky particles from the jaws to the target, pooling there."""
    _,x0,y0,x1,y1,p=e; rr=random.Random(f)
    for k in range(int(26*p)):
        u=rr.random()*p; x=lerp(x0,x1,u)+rr.randint(-3,3); y=lerp(y0,y1,u)+rr.randint(-3,3)
        c=rr.choice(((180,60,220),(230,140,255),(110,30,160))); s=rr.choice((1,1,2)); x,y=int(x),int(y)
        d.rectangle([x,y,x+s-1,y+s-1],fill=c)

@fx('mc_cloud')
def _fx_cloud(d,im,e,f):
    """The lingering purple breath cloud around a point."""
    _,x,y,r=e; rr=random.Random(f*3)
    for _ in range(int(r*3)):
        px=x+rr.randint(-r,r); py=y+rr.randint(-r//2,r//2)
        d.point((px,py),fill=rr.choice(((180,60,220),(230,140,255),(90,24,130))))

@fx('mc_crit')
def _fx_crit(d,im,e,f):
    """Critical-hit stars flying out of a hit."""
    _,x,y,t=e; rr=random.Random(int(x*7+y))
    for k in range(7):
        a=rr.uniform(0,6.28); r=2+t*2.2
        px,py=int(x+math.cos(a)*r),int(y+math.sin(a)*r*0.7)
        d.point((px,py),fill=(255,250,200)); d.point((px+1,py),fill=(250,210,90))

@fx('mc_dragon')
def _fx_dragon(d,im,e,f):
    """The Ender Dragon (drawn facing left): black scales, purple eyes, flapping wings, spiked tail.
    tint blends the whole body (red hurt flash); keep<1 dissolves it pixel by pixel."""
    _,cx,cy,tint,keep=e; cx,cy=int(cx),int(cy)
    L=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(L)
    dark,edge,spine,eye=(28,24,36,255),(96,84,114,255),(140,128,150,255),(220,100,255,255)
    def R(x0,y0,x1,y1,c=dark,o=edge): dd.rectangle([cx+x0,cy+y0,cx+x1,cy+y1],fill=c,outline=o)
    s=math.sin(f*0.45)
    def wing(dx,col,out,sc):
        pts=[(cx-4+dx,cy-3),(cx-12+dx,cy-4-int(12*s*sc)),(cx+3+dx,cy-4-int(17*s*sc)),(cx+18+dx,cy-4-int(12*s*sc)),(cx+10+dx,cy-2)]
        dd.polygon(pts,fill=col,outline=out)
        for p in pts[1:4]: dd.line([cx+2+dx,cy-3,p[0],p[1]],fill=out)
    wing(4,(24,20,32,255),(64,56,78,255),0.8)                       # far wing
    for i in range(6):                                              # tail
        x=10+i*4; w=int(2*math.sin(f*0.2+i*0.8))
        if i<3: R(x,-2+w,x+4,1+w)
        else: R(x,-1+w,x+4,0+w)
        if i%2==0: dd.rectangle([cx+x+1,cy-4+w,cx+x+2,cy-3+w],fill=spine)
    R(-8,3,-6,8); R(6,3,8,8)                                        # legs
    dd.rectangle([cx-9,cy+8,cx-6,cy+8],fill=spine); dd.rectangle([cx+5,cy+8,cx+8,cy+8],fill=spine)
    R(-10,-3,10,3)                                                  # body
    for i in range(-8,9,4): dd.rectangle([cx+i,cy-5,cx+i+1,cy-4],fill=spine)
    R(-20,-4,-9,0)                                                  # neck
    for i in (-18,-14): dd.rectangle([cx+i,cy-6,cx+i+1,cy-5],fill=spine)
    R(-30,-8,-20,0); R(-36,-6,-29,-2); R(-36,-1,-24,1)              # head, snout, jaw
    dd.rectangle([cx-23,cy-10,cx-22,cy-9],fill=spine); dd.rectangle([cx-27,cy-10,cx-26,cy-9],fill=spine)
    dd.rectangle([cx-28,cy-6,cx-25,cy-5],fill=eye); dd.point((cx-35,cy-5),fill=spine)
    wing(0,(46,40,58,255),(110,100,126,255),1.0)                    # near wing
    if tint:
        rgb=Image.blend(L.convert('RGB'),Image.new('RGB',(W,H),tint),0.55); rgb.putalpha(L.getchannel('A')); L=rgb
    if keep<1:
        a=L.getchannel('A'); pa=a.load()
        for y in range(H):
            for x in range(W):
                if pa[x,y] and ((x*37+y*91)%97)/97>=keep: pa[x,y]=0
        L.putalpha(a)
    im.paste(L,(0,0),L)

@fx('mc_beams')
def _fx_beams(d,im,e,f):
    """The dragon's death: purple/white light beams bursting out of the body and slowly turning."""
    _,cx,cy,t=e
    L=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(L)
    for k in range(12):
        a=k*math.pi/6+f*0.04+(k%3)*0.2; ln=10+min(64,t*110)*(0.6+0.4*((k*5)%3)/2); hw=0.035+0.015*(k%2)
        p=[(cx,cy),(cx+math.cos(a-hw)*ln,cy+math.sin(a-hw)*ln*0.8),(cx+math.cos(a+hw)*ln,cy+math.sin(a+hw)*ln*0.8)]
        dd.polygon(p,fill=(245,225,255,90) if k%2 else (190,100,255,110))
    r=2+int(3*t)+(f%2); dd.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(255,240,255,200))
    im.paste(L,(0,0),L)

@fx('mc_xp')
def _fx_xp(d,im,e,f):
    """XP orbs bursting out of (x0,y0) and homing onto (x1,y1); t 0..1."""
    _,x0,y0,x1,y1,t=e; rr=random.Random(33)
    for k in range(18):
        s0=k*0.035; u=(t-s0)/0.45
        if not 0<u<1: continue
        a=rr.uniform(0,6.28); mx,my=x0+math.cos(a)*30,y0+math.sin(a)*16
        x=(1-u)**2*x0+2*(1-u)*u*mx+u*u*x1; y=(1-u)**2*y0+2*(1-u)*u*my+u*u*y1
        c=(200,255,60) if (f+k)%4<2 else (120,210,30); x,y=int(x),int(y)
        d.rectangle([x-1,y-1,x,y],fill=c); d.point((x-1,y-1),fill=(240,255,170))

@fx('mc_portal')
def _fx_portal(d,im,e,f):
    """The exit portal: a bedrock rim around a black, starry End-portal surface."""
    _,cx,a=e; rr=random.Random(f//2)
    def c(rgb): return tuple(int(v*a) for v in rgb)
    d.rectangle([cx-15,GROUND-4,cx+15,GROUND],fill=c((58,58,58)),outline=c((86,86,86)))
    d.rectangle([cx-12,GROUND-3,cx+12,GROUND-1],fill=(4,6,10))
    for _ in range(6): d.point((cx+rr.randint(-11,11),GROUND-rr.randint(1,3)),fill=c(rr.choice(((40,150,130),(170,255,230),(90,60,160)))))
    d.rectangle([cx-1,GROUND-9,cx+1,GROUND-4],fill=c((58,58,58)),outline=c((86,86,86)))

# ---------------- close-up ----------------
_FACE=_CR_TOP[:8]
def _big_sprite(spr,flip,k):
    tmp=Image.new('RGB',(W,H),(6,4,10)); ox,oy,w,h=draw(tmp,spr,40,40,flip,pal=MCP)
    return tmp.crop((ox-1,oy-1,ox+w+1,oy+h+1)).resize(((w+2)*k,(h+2)*k),Image.NEAREST)

def closeup_creeper(t,f):
    """Primer plano: Claude looks away, the Creeper's face slides in right behind his shoulder — SSSS —
    flashing as it swells; at the last moment Claude turns round and sees it."""
    im=Image.new('RGB',(W,H),(6,4,10)); d=ImageDraw.Draw(im)
    fx0=int(ez(W+2,80,(t-0.05)/0.4)); k=8; rr=random.Random(5)
    flash=t>0.45 and (f//3)%2==0
    for j,row in enumerate(_FACE):
        for i,ch in enumerate(row):
            base=PAL[ch]; v=rr.uniform(0.82,1.12); c=tuple(min(255,int(b*v)) for b in base)
            if flash and ch!='K': c=tuple(int(lerp(a,225,0.3)) for a in c)
            x,y=fx0+i*k,j*k; d.rectangle([x,y,x+k-1,y+k-1],fill=c)
            if ch!='K':
                for _ in range(2):
                    px,py=x+rr.randint(0,k-3),y+rr.randint(0,k-3); d.rectangle([px,py,px+1,py+1],fill=tuple(int(a*0.8) for a in c))
    turned=t>=0.8
    big=_big_sprite(STEVE0['guard'],not turned,5)
    im.paste(big,(2,12))
    n=1+int(min(1,t/0.7)*6)
    FX['big'](d,im,('big',"S"*n+("..." if t>0.7 else ""),3,(210,255,210),128),f)
    if turned: FX['big'](d,im,('big',"!",3,(255,226,90),44),f)
    if t<0.06:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    return im

# ---------------- the clip ----------------
def _hearts(f):
    v=20
    if f>=100: v=12
    if f>=198: v=6
    if f>=276: v=int(round(lerp(6,20,(f-276)/16)))
    return v

def _dragon_pos(f):
    if f<140: return ez(230,122,(f-118)/22), ez(6,16,(f-118)/22)
    if f<190: return 122,16+2*math.sin(f*0.2)
    if f<200: return ez(122,70,(f-190)/10), ez(16,30,(f-190)/10)
    if f<214: return ez(70,120,(f-200)/14), ez(30,51,(f-200)/14)
    if f<240: return 120,51
    return 120, ez(51,24,(f-240)/22)

def clip_enderdragon(f):
    s=scene(f,THEME)
    cl=actor(STEVE[guard_pose(f)],30,pal=MCP)
    cr=actor(CREEPER[0],150,flip=True)
    sel=0; xp=0.0; lvl=0; blink=(100<=f<106) or (198<=f<204)
    # -- world: pillars' crystals, crater, placed blocks
    alive=[f<168 or f>=280, f<184 or f>=284]
    for (x,top),ok,t0 in zip(CRYS,alive,(280,284)):
        if ok: s['under'].append(('mc_crystal',x,top,min(1,(f-t0)/8) if f>=t0 else 1))
    if 100<=f<288: s['under'].append(('mc_crater',*CRATER,1 if f<280 else 1-(f-280)/8))
    nblk=0
    if 140<=f<276: nblk=min(3,(f-140)//6+(1 if (f-140)%6>=3 else 0))
    elif 276<=f<282: nblk=max(0,3-(f-276)//2)
    for k in range(nblk): s['under'].append(('mc_block',30,GROUND-6*k))
    if 276<=f<282 and (f-276)%2==0: s['fx'].append(('mc_debris',30,GROUND-6*nblk-3,2,f,6,((110,110,110),(76,76,76))))
    # -- 1) the creeper walks up and hisses
    if 20<=f<50: cr.update(spr=CREEPER[(f//4)%2],x=ez(150,50,(f-20)/30))
    if 50<=f<100: cr['x']=50
    if 50<=f<62 or 94<=f<100:
        fast=f>=94
        if (f//(1 if fast else 3))%2: cr['tint']=(225,250,225)
        callout(s,"SSSSS..."[:min(8,3+(f-50)//2)] if f<62 else "SSSSS...",y=13,c=(170,240,160))
        if fast: cr['x']=50+rshake(1)[0]
    if 62<=f<94: s['image']=closeup_creeper((f-62)/32,f); return s
    # -- 2) BOOM: crater, debris, Claude knocked back, hearts lost
    if f>=100 and f<284: cr['vis']=False
    if 100<=f<103: s['flash']=0.3*(1-(f-100)/3); s['fc']=(50,48); s['flashc']=(255,236,210)
    if 100<=f<104: s['fx'].append(('boom',50,48,6+(f-100)*4)); s['shake']=rshake(2)
    if 100<=f<126:
        s['fx'].append(('mc_puff',50,48,f-100,11))
        s['fx'].append(('mc_debris',50,52,f-100,12,20,((66,64,44),(92,90,60),(112,192,84),(52,118,44))))
    if 100<=f<110:
        u=(f-100)/10; cl.update(spr=STEVE['hurt'],x=ez(30,16,u),y=GROUND-int(6*math.sin(math.pi*u)),tint=(255,90,90) if f%2==0 and f<106 else None)
    if 110<=f<126: cl['x']=ez(16,30,(f-110)/16)
    # -- 3) the Ender Dragon; pillar up; arrows at the crystals
    dx,dy=_dragon_pos(f)
    dragon=118<=f<272
    if 122<=f<240: s['fx'].append(('mc_boss',1 if f<218 else (0.66 if f<226 else (0.33 if f<234 else 0))))
    if 118<=f<190:
        for (x,top),ok in zip(CRYS,alive):
            if ok and dx<W: s['under'].append(('mc_heal',x,top-9,dx,dy))
    if 140<=f<158:
        k=(f-140)//6; ph=(f-140)%6; sel=4
        cl.update(spr=STEVE['armsup'],y=GROUND-6*k-int(6*min(1,ph/3)))
    if 158<=f<206: cl['y']=GROUND-18
    if 158<=f<190:
        sel=2; cl['spr']=STEVE['charge']
        if 160<=f<168: s['fx'].append(('mc_arrow',40,33,64,17,4,(f-160)/8))
        if 174<=f<184: s['fx'].append(('mc_arrow',40,33,164,11,14,(f-174)/10))
    for x,top,t0 in ((64,26,168),(164,20,184)):
        if t0<=f<t0+14:
            u=f-t0; s['fx'].append(('mc_debris',x,top-9,u,t0,14,((255,140,255),(200,120,230),(255,230,255))))
            if u<4: s['fx'].append(('boom',x,top-9,3+u*3)); s['shake']=rshake(1)
            if u<2: s['flash']=0.2*(1-u/2); s['fc']=(x,top-9); s['flashc']=(240,170,255)
    # -- dragon swoop + purple breath
    if 192<=f<204: s['fx'].append(('mc_breath',dx-34,dy,34,32,min(1,(f-192)/6)))
    if 196<=f<214: s['fx'].append(('mc_cloud',32,33,8))
    if 198<=f<206: cl.update(spr=STEVE['hurt'],tint=(255,90,90) if f%2==0 else None)
    # -- jump down, three slashes on the perched dragon's head
    if 206<=f<216:
        u=(f-206)/10; cl.update(spr=STEVE['dash'],x=lerp(30,70,u),y=int(lerp(GROUND-18,GROUND,u))-int(10*math.sin(math.pi*u)))
    hit=None
    if 216<=f<240:
        k=(f-216)//8; ph=(f-216)%8
        cl.update(spr=STEVE['punch' if 2<=ph<5 else guard_pose(f)],x=70+(1 if 2<=ph<5 else 0))
        if ph>=2: hit=(k,ph-2)
        if ph==2: s['shake']=rshake(1)
    if hit and hit[1]<5: s['fx'].append(('mc_crit',87,48,hit[1]))
    if 240<=f<274: cl.update(x=70)
    # -- 4) death: light beams, dissolve, XP, exit portal, THE END
    if dragon:
        tint=(255,60,60) if hit and hit[1]<2 else None
        keep=1 if f<244 else max(0,1-(f-244)/26)
        if keep>0: s['under'].append(('mc_dragon',dx,dy,tint,keep))
    if 240<=f<272: s['fx'].append(('mc_beams',dx-4,dy,(f-240)/32))
    if 250<=f<280: s['under'].append(('mc_portal',120,1 if f<274 else 1-(f-274)/6))
    if 248<=f<274:
        s['fx'].append(('mc_xp',dx,dy,70,50,(f-248)/26))
        xp=((ez(0,1,(f-252)/22)*30)%1); lvl=int(ez(0,30,(f-252)/22))
    if 274<=f<284: lvl=int(lerp(30,0,(f-274)/8)); xp=0
    if 260<=f<276: s['fx'].append(('big',"THE END",16,(225,200,255)))
    # -- 5) respawn: Claude walks back, the creeper and crystals fade back in
    if 274<=f<292: cl.update(x=ez(70,30,(f-274)/18))
    if 284<=f<296: cr.update(vis=True,alpha=max(0.05,(f-284)/12))
    s['fx'].append(('mc_hud',_hearts(f),blink,xp,lvl,sel))
    s['actors']=[cr,cl]
    return s

CLIPS = [clip('enderdragon', N_, clip_enderdragon)]
