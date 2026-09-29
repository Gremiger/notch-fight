"""Jujutsu Kaisen sub-theme "jjk-maki": Claude as Maki Zen'in, awakened, vs the Zen'in clan.
The estate catches fire and three clansmen close in. Close-up: her glasses crack and fall, the eyes
sharpen — I WILL DESTROY IT ALL. She cuts through them in a blur of afterimages, crosses swords
twice with her father Ogi and cuts him down, then walks back as the flames die; the glasses return."""
from engine import *

THEME = 'jjk-maki'
N_ = 264

FIRE, FIRE_HI = (255,140,40), (255,236,160)
RED = (255,80,70)
# Maki: dark green hair with a ponytail, glasses, navy Jujutsu High uniform
MPAL = {'l':(46,92,64), 'f':(30,64,44), 'a':(44,50,84), 'i':(34,38,66), 'z':(110,110,124)}
# Zen'in clansmen: dark kimono, red sash; Ogi: grey kimono, beard
ZPAL = {'c':(66,58,76), 'x':(150,40,40)}
OPAL = {'c':(96,92,104), 'x':(150,40,40), 'u':(40,34,32)}

HAIR = ["..llllllll..", ".llllllllll.", "llflllllfll."]

def _maki(spr, glasses=True):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(top,top+4):                                     # ponytail down the back
        if l-1>=0 and g[y][l-1]=='.': g[y][l-1]='l'
    if top+4<len(g) and l-2>=0 and g[top+4][l-2]=='.': g[top+4][l-2]='f'
    ks=[(x,y) for y,row in enumerate(g) for x,c in enumerate(row) if c=='K']
    if glasses and ks:
        x0=min(x for x,_ in ks); x1=max(x for x,_ in ks); y0=min(y for _,y in ks)
        for x in range(x0-1,x1+2):
            if g[y0-1][x] in 'Oo': g[y0-1][x]='z'                  # the frame over the eyes
        for x in (x0-1,x1+1):
            if g[y0][x] in 'Oo': g[y0][x]='z'
    for y in range(top+5,min(top+9,len(g))):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='a' if y<top+8 else 'i'
    return S([''.join(x) for x in g])
MAKI=variant(_maki)
MAKI_BARE=variant(lambda s: _maki(s,glasses=False))

ZENIN=poses(S([
".....kkk......","....kkkkk.....","....kPPPk.....","....PkPkP.....","....PPPPP.....",
".....PPP......","...cccccccc...","..cccPcccccc..","..ccccPcccccc.","..PcccccccccP.",
"..P.xxxxxx.P..","....cccccc....","....cccccc....","...cccccccc...","...cccccccc...",
"...cc....cc...","...cc....cc...","..kkk....kkk..",]),9,'P',4)
OGI=poses(S([
".....kkkkk......","....kkkkkkk.....","....kPPPPPk.....","....PkPPPkP.....","....PPPPPPP.....",
"....uPPPPPu.....","....uuuuuuu.....",".....uuuuu......","...ccccccccc....","..cccccPccccc...",
"..ccccccPcccc...","..PcccccccccP...","..P.xxxxxxx.P...","....ccccccc.....","....ccccccc.....",
"...ccccccccc....","...ccccccccc....","...cc.....cc....","...cc.....cc....","..kkk.....kkk...",]),11,'P',4)

def _estate(d):
    """The Zen'in estate at night: shoji walls with a wooden frame, a roof edge."""
    d.rectangle([0,6,W,8],fill=(34,22,18))
    for x0 in range(4,W,36):
        d.rectangle([x0,12,x0+30,GROUND-6],outline=(46,32,24))
        for x in range(x0+6,x0+30,6): d.line([x,12,x,GROUND-6],fill=(30,22,18))
        for y in range(18,GROUND-6,8): d.line([x0,y,x0+30,y],fill=(30,22,18))
    d.line([0,GROUND-5,W,GROUND-5],fill=(50,34,26))
register_bg(THEME, lambda v: (v,v*3//4,v//2), decor=_estate)

@fx('maki_red')
def _fx_red(d,im,e,f):
    _,a=e; im.paste(fade_to(im,(90,20,8),min(1,max(0,a))))

@fx('maki_katana')
def _fx_katana(d,im,e,f):
    """Split Soul Katana from the hand at angle a (degrees): long pale blade, gold tsuba, wrapped hilt."""
    _,hx,hy,a,L=e; c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
    d.line([hx-c*3,hy-s*3,hx,hy],fill=(60,40,60))
    d.line([hx+c-s*1.5,hy+s+c*1.5,hx+c+s*1.5,hy+s-c*1.5],fill=(230,190,60))
    d.line([hx+2*c,hy+2*s,hx+L*c,hy+L*s],fill=(214,220,236)); d.point((hx+L*c,hy+L*s),fill=(255,255,255))

@fx('maki_cut')
def _fx_cut(d,im,e,f):
    """A clean diagonal cut through a target, fading over k."""
    _,x,y,k=e; L=12-k
    if L>0: d.line([x-L,y+L*0.7,x+L,y-L*0.7],fill=(255,255,255)); d.line([x-L+1,y+L*0.7,x+L+1,y-L*0.7],fill=RED)

GRIP = {'guard':(13,4,-60), 'guard2':(13,4,-60), 'punch':(16,5,0), 'charge':(15,5,-30), 'dash':(16,5,10)}
def katana_fx(s,pose,x,y,flip):
    if pose not in GRIP: return
    col,row,ang=GRIP[pose]; hx,hy=hand_at(MAKI[pose],x,y,flip,col,row,h=11)
    s['fx'].append(('maki_katana',hx,hy,(180-ang) if flip else ang,14))

def closeup_glasses(t,f):
    """Primer plano: the glasses crack and fall, the eyes sharpen, the burns show; I WILL / DESTROY / IT ALL."""
    im=Image.new('RGB',(W,H),(14,4,4)); d=ImageDraw.Draw(im)
    rr=random.Random(6611+f)
    for _ in range(14):                                                    # embers
        x=rr.randint(0,96); y=(rr.randint(0,H)-f*2)%H; d.point((x,y),fill=FIRE if rr.random()<0.5 else FIRE_HI)
    O,o=(217,119,87),(168,80,54)
    d.rectangle([22,12,82,64],fill=O); d.rectangle([76,12,82,64],fill=o)
    d.rectangle([18,2,86,14],fill=MPAL['l']); d.rectangle([14,6,20,40],fill=MPAL['l'])      # hair + ponytail side
    for x in range(20,86,8): d.polygon([(x,14),(x+8,14),(x+4,20)],fill=MPAL['l'])
    d.rectangle([56,36,70,42],fill=(190,90,70)); d.line([58,38,68,38],fill=(160,70,56))     # the burn
    sharp=t>=0.4
    for x0 in (32,56):
        if sharp: d.polygon([(x0,30),(x0+14,27),(x0+14,32),(x0,32)],fill=(24,14,12)); d.rectangle([x0+6,29,x0+8,31],fill=(200,170,60))
        else: d.rectangle([x0,27,x0+14,33],fill=(24,14,12)); d.point((x0+4,29),fill=(255,255,255))
    d.line([40,50,64,50],fill=(60,20,20))
    if t<0.4:                                                              # the glasses: intact, then cracking
        for x0 in (30,54):
            d.rectangle([x0,24,x0+18,36],outline=(110,110,124)); d.line([x0+2,26,x0+6,26],fill=(160,190,210))
        d.line([48,28,54,28],fill=(110,110,124))
        if t>=0.15:
            for x0 in (30,54):
                d.line([x0+4,24,x0+10,31],fill=(230,240,255)); d.line([x0+10,31,x0+7,36],fill=(230,240,255)); d.line([x0+10,31,x0+17,28],fill=(230,240,255))
    elif t<0.6:                                                            # falling shards
        k=(t-0.4)/0.2
        for i in range(10):
            x=34+i*4+math.sin(i)*3; y=30+k*40+i%3*3; d.line([x,y,x+1,y+2],fill=(200,220,240))
    for j,w in enumerate(("I WILL","DESTROY","IT ALL")):
        if t>=0.45+j*0.14: FX['big'](d,im,('big',w,6+j*18,RED if j==1 else (236,236,244),138),f)
    if t<0.06: zoom_lines(d)
    return im

FOES=((112,14),(134,18),(156,22))           # (spot, frame they finish walking in by +)
CUTS=((100,106,112),(112,118,134),(124,130,156))   # (dash start, cut frame, foe x)

def clip_zenin(f):
    s=scene(f,THEME)
    mx,mflip,mpose=30,False,guard_pose(f)
    bare=52<=f<250
    burn=0
    if 14<=f<200: burn=min(0.45,(f-14)/26*0.45)
    if 200<=f<246: burn=0.45*(1-(f-200)/46)
    if burn: s['under'].append(('maki_red',burn))
    if 14<=f<246:                                                         # the estate burns
        k=1 if (f<30 or f>=230) else 2
        for j,x in enumerate((4,72,180)):
            s['under'].append(('fire',x,GROUND,k+(f+j)%3))
    acts=[]
    # 1) three clansmen walk in
    for i,(fx_,_) in enumerate(FOES):
        start,cut,_x=CUTS[i]
        if f<18 or f>=cut+14: continue
        x=ez(200+i*10,fx_,(f-18-i*4)/20)
        z=actor(ZENIN['idle'],x,flip=True,pal=ZPAL)
        if f>=cut:
            k=f-cut; z.update(spr=ZENIN['hurt'],alpha=max(0,1-k/14))
            s['fx'].append(('maki_cut',x,GROUND-10,k))
        acts.append(z)
    if 22<=f<44: callout(s,"ZENIN CLAN",c=RED)
    # 2) close-up
    if 52<=f<100: s['image']=closeup_glasses((f-52)/48,f); return s
    # 3) the blur: dash, cut, dash, cut
    prev=30
    for start,cut,foe_x in CUTS:                                          # each cut ends where the next dash starts
        if start<=f<cut: mpose,mx='dash',ez(prev,foe_x-12,(f-start)/(cut-start))
        if cut<=f<cut+6: mpose,mx='punch',foe_x-12
        prev=foe_x-12
    if mpose=='dash' and 100<=f<136:                                      # afterimages
        for j in (1,2,3): acts.append(actor(MAKI_BARE['dash'],mx-j*7,pal=MPAL,alpha=0.5-j*0.12,tint=(90,210,130)))
    if 136<=f<168: mx,mpose=prev,guard_pose(f)
    # 4) Ogi: two clashes, then the cut
    ox,opose=None,'idle'
    if 146<=f<204:
        ox=ez(210,166,(f-146)/14)
        if 150<=f<168: callout(s,"OGI ZENIN",c=(236,236,244))
    for c0 in (168,180):
        if c0-4<=f<c0: mpose,mx='dash',ez(144,150,(f-c0+4)/4); opose='attack'
        if c0<=f<c0+6:
            mpose,mx,opose='punch',150,'attack'
            if f<c0+3: s['fx'].append(('spark',158,GROUND-10,4+(f-c0))); s['shake']=rshake(2)
        if c0+6<=f<c0+10: mpose,mx='guard',ez(150,140,(f-c0-6)/4)
    if 186<=f<192: mpose,mx='dash',ez(140,180,(f-186)/6)
    if 192<=f<204:
        mpose,mx='punch',180; opose='hurt'
        if f<196: s['flash']=0.6; s['fc']=(166,GROUND-10); s['flashc']=(255,200,180)
        s['fx'].append(('maki_cut',166,GROUND-12,f-192))
    if 188<=f<200:
        for j in (1,2,3): acts.append(actor(MAKI_BARE['dash'],min(mx,180)-j*9,pal=MPAL,alpha=0.45-j*0.1,tint=(90,210,130)))
    if ox is not None:
        o=actor(OGI[opose],ox,flip=True,pal=OPAL)
        if f>=196: o.update(spr=OGI['hurt'],alpha=max(0,1-(f-196)/8))
        acts.append(o)
    # 5) she walks back through the dying flames; the glasses come back
    if 204<=f<250: mx,mflip,mpose=ez(180,30,(f-204)/40),True,guard_pose(f)
    if f>=250: mx,mflip=30,False
    if 250<=f<256: s['fx'].append(('twinkle',30,GROUND-15,2))
    spr=(MAKI_BARE if bare else MAKI)[mpose]
    acts.append(actor(spr,mx,flip=mflip,pal=MPAL))
    katana_fx(s,mpose,mx,GROUND,mflip)
    s['actors']=acts
    return s

CLIPS = [clip('zenin', N_, clip_zenin)]
