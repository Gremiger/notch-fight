"""Breaking Bad: Claude (Heisenberg: pork-pie hat, sunglasses, goatee) vs Tuco Salamanca.
Tuco screams TIGHT TIGHT TIGHT! and pulls a gun; Claude calmly shows a bag of blue crystals —
THIS IS NOT METH. — and throws one: fulminated mercury, the office windows blow out. Close-up:
SAY MY NAME. ...CLAUDENBERG. YOU ARE GODDAMN RIGHT. Tuco gets back up, the lights come back on."""
from engine import *

THEME = 'bb'
N_ = 276

BLUE, BLUE_HI = (70,170,255), (170,230,255)
GOLD = (250,210,60)
# Heisenberg's own colours: a hat crown, its band, the lenses, the goatee
HPAL = {'a':(66,66,74), 'c':(26,26,30), 'z':(14,14,18), 'x':(150,160,180), 'u':(74,42,26)}
# Tuco: tan skin, dark jeans (the rest comes from PAL)
TPAL = {'s':(198,142,102), 'L':(52,66,112), 'd':(150,150,160)}

HAT = ["..aaaaaa..", "..cccccc..", "aaaaaaaaaa"]

def _heisenberg(spr):
    """Hat over the body, sunglasses across the eye rows, a goatee under them."""
    g=[list(r) for r in overlay(spr,HAT,-1,0)]
    ks=[(x,y) for y,r in enumerate(g) for x,c in enumerate(r) if c=='K']
    if not ks: return S([''.join(r) for r in g])
    y0=min(y for _,y in ks); x0=min(x for x,_ in ks); x1=max(x for x,_ in ks)
    for y in {y for _,y in ks}:
        for x in range(x0-1,x1+1):
            if g[y][x] in 'OoK': g[y][x]='z'
    g[y0][x0]='x'                                              # glint on the lens
    mid=(x0+x1)//2
    for y in (y0+3,y0+4):
        for x in (mid,mid+1):
            if y<len(g) and g[y][x] in 'Oo': g[y][x]='u'
    return S([''.join(r) for r in g])
HEIS=variant(_heisenberg)

TUCO=poses(S([
"....ssss......","...ssssss.....","..ssssssss....","..skksskks....","..sKssssKs....",
"..ssssssss....","..skYYYYks....","...skkkks.....","....ssss......","..HHHHHHHH....",
".sHHHHHHHHs...",".sHHHHHHHHs...","ssHHHYYHHHss..","ss.HHYYHH.ss..","ss.HHHHHH.ss..",
"...HHHHHH.....","...LLLLLL.....","...LLLLLL.....","...LL..LL.....","...LL..LL.....",
"...LL..LL.....","..kkk..kkk....",]),12,'ss',4)
def _gun(spr):
    g=[r for r in spr]
    g[11]=g[11].rstrip('.')+'.ddd'
    g[12]=g[12].rstrip('.')+'dddd'; g[13]=g[13][:len(g[12])-4]+'..dd'
    return S(g)
TUCO['gun']=_gun(attack(TUCO['idle'],12,2,'ss'))
TUCO['yell']=S([r.replace('YYYY','YkkY') if i==6 else r for i,r in enumerate(TUCO['attack'])])

def _desert(d):
    rr=random.Random(5303)
    for _ in range(26):
        x,y=rr.randint(0,W-1),rr.randint(0,30); v=rr.randint(40,90); d.point((x,y),fill=(v,v,v+14))
    d.polygon([(0,GROUND),(0,44),(12,40),(30,40),(40,46),(58,46),(64,GROUND)],fill=(16,12,22))   # mesa
    d.rectangle([62,46,100,GROUND-1],fill=(34,32,30))                                          # the RV
    d.rectangle([64,44,92,45],fill=(34,32,30)); d.line([62,51,100,51],fill=(60,48,30))
    d.rectangle([90,48,96,50],fill=(46,44,40)); d.rectangle([68,48,72,50],fill=(46,44,40))
    for x in (68,92): d.ellipse([x-2,GROUND-3,x+2,GROUND+1],fill=(14,12,12))
    d.rectangle([116,28,184,GROUND],fill=(24,19,22)); d.line([116,28,184,28],fill=(44,36,38))  # Tuco's office
register_bg(THEME, lambda v: (v,v*2//3,v//2), decor=_desert)

WINDOWS=((124,33),(164,33))
@fx('bb_windows')
def _fx_windows(d,im,e,f):
    """Office windows: lit, or blown out (dark with jagged glass left in the frame)."""
    _,lit=e
    for x,y in WINDOWS:
        d.rectangle([x,y,x+12,y+9],fill=(84,68,32) if lit else (6,6,8),outline=(50,42,40))
        if lit: d.line([x+6,y,x+6,y+9],fill=(50,42,40)); d.line([x,y+4,x+12,y+4],fill=(50,42,40))
        else:
            d.polygon([(x+1,y+1),(x+5,y+1),(x+2,y+4)],fill=(90,120,140))
            d.polygon([(x+11,y+8),(x+11,y+3),(x+8,y+8)],fill=(90,120,140))

@fx('bb_bag')
def _fx_bag(d,im,e,f):
    """The zip bag of blue crystals held up in Claude's hand."""
    _,x,y=e
    d.rectangle([x,y-7,x+6,y],fill=(40,44,52),outline=(150,160,176))
    for i,(cx,cy) in enumerate(((1,-2),(3,-3),(5,-2),(2,-1),(4,-1),(3,-5))): d.point((x+cx,y+cy),fill=BLUE_HI if (i+f//3)%3==0 else BLUE)
    d.line([x,y-7,x+6,y-7],fill=(210,60,60))

@fx('bb_crystal')
def _fx_crystal(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y)
    d.rectangle([x-1,y-1,x+1,y+1],fill=BLUE); d.point((x,y),fill=(255,255,255))
    if f%2: d.point((x-2,y),fill=BLUE_HI); d.point((x+2,y),fill=BLUE_HI)
    else: d.point((x,y-2),fill=BLUE_HI); d.point((x,y+2),fill=BLUE_HI)

@fx('bb_sparkle')
def _fx_sparkle(d,im,e,f):
    """Blue crystal twinkle (the signature accent): a small cross that grows then shrinks."""
    _,x,y,k=e; s=(0,1,2,1)[k%4]
    d.line([x-s-1,y,x+s+1,y],fill=BLUE); d.line([x,y-s,x,y+s],fill=BLUE); d.point((x,y),fill=(230,245,255))

@fx('bb_blast')
def _fx_blast(d,im,e,f):
    """Fulminated mercury: white core, orange fireball, a thin shock ring; fades out with k."""
    _,x,y,k=e; rr=random.Random(f*31)
    if k<10:
        r=4+k*2
        for _ in range(14):
            a=rr.random()*6.28; dd=rr.random()*r; rb=max(1,int((r-dd)/3)+1)
            px,py=x+math.cos(a)*dd,y+math.sin(a)*dd*0.7
            d.ellipse([px-rb,py-rb,px+rb,py+rb],fill=(255,240,180) if dd<r*0.35 else ((255,150,40) if dd<r*0.7 else (200,60,20)))
    if k<14: rr2=6+k*5; d.ellipse([x-rr2,y-rr2//2,x+rr2,y+rr2//2],outline=(255,200,120) if k<7 else (140,90,60))

@fx('bb_glass')
def _fx_glass(d,im,e,f):
    """Glass shards thrown out of the blast and the windows: ballistic, deterministic."""
    _,k=e; rr=random.Random(4422)
    srcs=[(140,GROUND-10)]*14+[(x+6,y+4) for x,y in WINDOWS for _ in range(8)]
    for sx,sy in srcs:
        vx=rr.uniform(-3.2,3.2); vy=rr.uniform(-3.4,-0.6); t=k
        px=sx+vx*t; py=sy+vy*t+0.18*t*t
        if 0<=px<W and py<GROUND: d.point((int(px),int(py)),fill=(180,225,245) if rr.random()<0.6 else (255,255,255))

@fx('bb_gunfly')
def _fx_gunfly(d,im,e,f):
    _,k=e; x=lerp(128,176,k/14); y=GROUND-14-12*math.sin(min(1,k/14)*math.pi)
    d.rectangle([x-2,y,x+2,y+1],fill=(150,150,160)); d.point((x-2,y+2),fill=(150,150,160))

@fx('bb_dizzy')
def _fx_dizzy(d,im,e,f):
    _,x,y=e
    for k in range(3): a=f*0.4+k*2.1; d.point((x+math.cos(a)*6,y+math.sin(a)*2),fill=GOLD)

def closeup_name(t,f):
    """Primer plano: Heisenberg's face; SAY MY NAME. / ...CLAUDENBERG. / YOU ARE GODDAMN RIGHT."""
    im=Image.new('RGB',(W,H),(6,6,10)); d=ImageDraw.Draw(im)
    for i in range(0,64,4): d.line([0,i,96,i],fill=(10,12,20))                  # faint blue haze
    O,o=(217,119,87),(168,80,54)
    d.rectangle([22,12,82,64],fill=O); d.rectangle([76,12,82,64],fill=o)        # the block head
    d.rectangle([22,14,82,18],fill=o)                                            # brim shadow
    d.rectangle([28,0,76,9],fill=(52,52,60)); d.line([28,0,76,0],fill=(84,84,96))  # crown
    d.rectangle([28,6,76,9],fill=(24,24,28))                                     # band
    d.rectangle([10,10,94,13],fill=(52,52,60)); d.line([10,10,94,10],fill=(84,84,96))  # brim
    for x0 in (32,56):
        d.rectangle([x0,24,x0+18,32],fill=(14,14,18),outline=(58,58,68))       # sunglasses
    d.line([50,26,56,26],fill=(58,58,68))
    g=int((t*3%1)*26)                                                            # a glint sweeping the lenses
    if g<18: d.line([32+g,25,32+g+3,31],fill=(120,130,150)); d.line([56+g,25,56+g+3,31],fill=(90,100,120))
    speaking=(0.08<t<0.34 or 0.62<t<0.95) and (f//3)%2
    d.rectangle([42,44,68,46],fill=(74,42,26))                                   # moustache
    d.rectangle([47,47,63,49],fill=(24,10,10) if speaking else O)                # mouth
    d.rectangle([48,50,62,60],fill=(74,42,26)); d.rectangle([51,60,59,63],fill=(74,42,26))  # goatee
    if 0.08<=t<0.34:
        FX['big'](d,im,('big',"SAY MY",14,(236,236,244),138),f)
        FX['big'](d,im,('big',"NAME.",30,(236,236,244),138),f)
    elif 0.38<=t<0.6:
        text(d,"TUCO:" if t>=0.42 else "...",100,12,(160,130,60))
        if t>=0.44: FX['big'](d,im,('big',"CLAUDENBERG.",26,GOLD,137),f)
        else: text(d,"...",120,30,GOLD)
    elif 0.62<=t:
        for j,w in enumerate(("YOU ARE","GODDAMN","RIGHT.")): FX['big'](d,im,('big',w,18+j*15,BLUE_HI if j<2 else BLUE,138),f)
    for i,(x,y) in enumerate(((12,30),(90,52),(16,56),(96,22))):
        if (f//2+i*3)%8<4: _fx_sparkle(d,im,('bb_sparkle',x,y,f//2+i),f)
    if t<0.06:
        zoom_lines(d)
    return im

HAND=(39,GROUND-6)   # the end of Claude's extended arm ('punch' pose at x=30)
TX,TY=140,GROUND-10  # where the crystal lands, at Tuco's feet

def clip_saymyname(f):
    s=scene(f,THEME)
    cl=actor(HEIS[guard_pose(f)],30,pal=HPAL); tu=actor(TUCO['idle'],150,flip=True,pal=TPAL)
    s['under'].append(('bb_windows', not (110<=f<252 and not (246<=f<252 and f%2))))
    # signature: a crystal glint near Claude's hat now and then (period 69 divides the clip)
    if f%69<8: s['fx'].append(('bb_sparkle',22,GROUND-15,(f%69)//2))
    # 1) Tuco loses it: TIGHT TIGHT TIGHT!
    if 20<=f<64:
        k=(f-20)//5; tu['spr']=TUCO['yell'] if k%2 else TUCO['attack']
        if k%2: s['shake']=rshake(1)
        callout(s,"TIGHT TIGHT TIGHT!",c=GOLD)
    # 2) the gun; Claude shows the bag
    if 64<=f<112: tu['spr']=TUCO['gun']
    if 70<=f<104:
        cl['spr']=HEIS['punch']; s['fx'].append(('bb_bag',HAND[0],HAND[1]))
        if f>=74: callout(s,"THIS IS NOT METH.",c=BLUE_HI)
    # 3) one crystal, thrown
    if 104<=f<110:
        cl['spr']=HEIS['dash'] if f<106 else HEIS['punch']; p=(f-104)/6
        s['fx'].append(('bb_crystal',lerp(HAND[0],TX,p),HAND[1]-4-14*math.sin(p*math.pi)))
    # 4) fulminated mercury
    if 110<=f<148:
        k=f-110
        s['fx'].append(('bb_blast',TX,TY,k)); s['fx'].append(('bb_glass',k))
        if k<14: s['fx'].append(('bb_gunfly',k))
        if k<6: s['shake']=rshake(2 if k<3 else 1)
        if k<2: s['flash']=0.4-0.15*k; s['fc']=(TX,TY); s['flashc']=(255,190,110)
        for j in range(3): s['fx'].append(('smoke',TX-8+j*8,TY-k*0.6-j,2+min(k,24)//4,(40,36,40)))
        if 2<=k<16: s['fx'].append(('big',"BOOM!",4,(255,170,60)))
        tu.update(spr=TUCO['hurt'],x=ez(150,174,k/8),y=GROUND-int(6*math.sin(min(1,k/8)*math.pi)))
        if k>=16: s['fx'].append(('bb_dizzy',174,GROUND-24))
    # 5) close-up: SAY MY NAME.
    if 148<=f<232: s['image']=closeup_name((f-148)/84,f); return s
    # 6) Tuco comes to, gets up, walks back; the office lights return
    if 232<=f<248: tu.update(spr=TUCO['hurt'],x=174); s['fx'].append(('bb_dizzy',174,GROUND-24))
    if 248<=f<262: tu.update(spr=TUCO['idle'],x=ez(174,150,(f-248)/14),y=GROUND-(1 if (f//3)%2 else 0))
    if 232<=f<244: s['fx'].append(('dmg',"CLAUDENBERG...",112,4,(160,130,60)))
    s['actors']=[cl,tu]
    return s

CLIPS = [clip('saymyname', N_, clip_saymyname)]
