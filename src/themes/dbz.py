"""Dragon Ball Z: Claude vs Perfect Cell at the Cell Games, on the white tiled ring in the rocky
wasteland. The stare-down, a clash that shakes the ring, a rush barrage that blinks up into the sky
and back, Cell's knee — Instant Transmission: Claude vanishes and slams down on Cell from above.
KAMEHAMEHA vs KAMEHAMEHA: the beam struggle goes Cell's way until the close-up — Claude screams and
goes SUPER SAIYAN, the golden beam blows straight through. Cell crawls out of the smoke (I AM
PERFECT!), Claude raises the GENKI DAMA and buries him with it. Cell regenerates from a scrap,
Claude powers down, back to the stare-down."""
from engine import *

THEME = 'dbz'
N_ = 456
CX, EX = 30, 150                                                    # the loop keyframe positions

# ---- local glyphs: a wider M and W (the 3x5 font's read as H) ------------------------------------
_GLYPH = {'M':(5,"10001"+"11011"+"10101"+"10001"+"10001"), 'W':(5,"10001"+"10001"+"10101"+"11011"+"10001")}

def _mask(txt):
    gl=[_GLYPH.get(ch) or (3,''.join(FONT.get(ch,FONT[' '])[j*3:j*3+3] for j in range(5))) for ch in txt]
    m=Image.new('L',(sum(w+1 for w,_ in gl)-1,5),0); md=ImageDraw.Draw(m); x=0
    for w,bits in gl:
        for j,b in enumerate(bits):
            if b=='1': md.point((x+j%w,j//w),fill=255)
        x+=w+1
    return m

def say(im,txt,y,c,scale=1,cx=W//2,outline=None,shadow=(0,0,0)):
    """Like big_text, with the local glyphs; scale=1 gives a normal callout."""
    m=_mask(txt); m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        if shadow is not None: im.paste(shadow,(x+2,y+2),m)
    elif shadow is not None: im.paste(shadow,(x+1,y+1),m)
    im.paste(c,(x,y),m)

@fx('dbzc_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,cx=W//2,outline=None):
    s['fx'].append(('dbzc_say',txt,y,c,scale,cx,outline))

# ---- Claude: Goku's spiky hair and a blue belt on the orange gi; Super Saiyan = golden spikes -----
def _gi(x,y,t,l,r,c):
    return 'L' if (c=='O' and y==t+7 and l<=x<=r) else None
BASE=variant(lambda s: overlay(recolor_rows(s,_gi),["..k..k.k.....",".kkk.kkkkk...","kkkkkkkkkkk.."],-2,0,
                               bangs="..kk.k.kk"))
SSJ=variant(lambda s: overlay(recolor_rows(s,_gi),["...Y...Y.....","..YY..YY.Y...",".YyYYYYyYYY..","YYYYYYYYYYYY."],-2,0,
                              bangs="..YY.Y.YY"))
SSJPAL={'Y':(255,234,90),'y':(222,168,36)}
AURA_W=(236,240,255)                                                # base-form ki: white
AURA_G=(255,226,90)                                                 # Super Saiyan: gold
KI=((255,196,140),(232,120,80))                                     # Claude's Kamehameha
KI_SSJ=((255,244,180),(255,196,60))
CELL_KI=((140,210,255),(60,140,255))
CELL_AURA=(190,255,150)

def spin(spr,f): return rotate90(spr,(f//2)%4)                      # a backflip, 2 frames per quarter

# ---- Perfect Cell: green armour, black spots, pale face with the pink cheek marks, wings, crown ---
_CE_IDLE=S([
"......g.g.......",
".....gGgGg......",
"....gGSGGSg.....",
"....GGGGGGG.....",
"....GPPPPPG.....",
"....GPPePPe.....",
"....UPPPPPU.....",
".....PPPPP......",
".w..GGSGGSGG....",
"ww.GGGBBBBGGG...",
"wwGGgGGGGGGgGG..",
"wwGGPPGGGGPPGG..",
".wG.BBBBBBBB.G..",
".w...BBGGBB.....",
"..w..GGGGGG.....",
".....SGGSGG.....",
".....GG..GG.....",
".....BB..BB.....",
".....BB..BB.....",
".....GS..GS.....",
".....GG...GG....",
"....PPP...PPP...",])
_CE_GUARD=S([
"......g.g.......",
".....gGgGg......",
"....gGSGGSg.....",
"....GGGGGGG.PP..",
"....GPPPPPG.GG..",
"....GPPePPe.GG..",
"....UPPPPPU.G...",
".....PPPPP.GG...",
".w..GGSGGSGG....",
"ww.GGGBBBBGG....",
"wwGGgBBBBBB.....",
"wwGG.BBBBBB.....",
".wGG.BBGGBB.....",
".wPP.BBBBBB.....",
"..w..GGGGGG.....",
".....SGGSGG.....",
".....GG..GG.....",
"....BB....BB....",
"....BB....BB....",
"...GS......GS...",
"...GG......GG...",
"..PPP......PPP..",])
_CE_PUNCH=S([
"......g.g...........",
".....gGgGg..........",
"....gGSGGSg.........",
"....GGGGGGG.........",
"....GPPPPPG.........",
"....GPPePPe.........",
"....UPPPPPU.........",
".....PPPPP..........",
".w..GGSGGSGG........",
"ww.GGGBBBBGGGGGGGPP.",
"wwGGgBBBBBBgGGGGGPP.",
"wwGG.BBBBBB.........",
".wGG.BBGGBB.........",
".wPP.BBBBBB.........",
"..w..GGGGGG.........",
".....SGGSGG.........",
"....GG....GG........",
"...BB......BB.......",
"..BB........BB......",
"..GS........GS......",
".GG..........GG.....",
"PPP...........PPP...",])
_CE_HURT=S([
"...g.g..........",
"..gGgGg.........",
".gGSGGSg........",
".GGGGGGG........",
".GPPPPPG........",
".GPKKPKK........",
".UPPPPPU...PP...",
"..PPPPP...GG....",
".w.GGSGGSGG.....",
"wwGGGBBBBGGG....",
"wwGgBBBBBBgG....",
"wwG.BBBBBB......",
".w..BBGGBB......",
".w..BBBBBB......",
"..w.GGGGGG......",
"....SGGSGG......",
".....GG..GG.....",
".....BB...BB....",
"....BB.....BB...",
"....GS.....GS...",
"...GG.......GG..",
"..PPP.......PPP.",])
_CE_CHARGE=S([
"......g.g.........",
".....gGgGg........",
"....gGSGGSg.......",
"....GGGGGGG.......",
"....GPPPPPG.......",
"....GPPePPe.......",
"....UPPPPPU.......",
".....PPPPP........",
".w..GGSGGSGG......",
"ww.GGGBBBBGGGG....",
"wwGGgBBBBBBgGGGPP.",
"wwGG.BBBBBB..GGPP.",
".wGG.BBGGBB.......",
".w...BBBBBB.......",
"..w..GGGGGG.......",
".....SGGSGG.......",
"....GG....GG......",
"...BB......BB.....",
"..BB........BB....",
"..GS........GS....",
".GG..........GG...",
"PPP...........PPP.",])
# the wings flare out when he powers up
_CE_FLARE=S(["w"+r if 8<=i<=14 else "."+r for i,r in enumerate(_CE_GUARD)])
CE={'idle':_CE_IDLE,'guard':_CE_GUARD,'punch':_CE_PUNCH,'hurt':_CE_HURT,'charge':_CE_CHARGE,'flare':_CE_FLARE}
CE_BURNT={'G':(86,140,64),'g':(40,86,34),'P':(196,184,164),'w':(58,110,50)}   # after the golden beam

# ---- background: the Cell Games ring in the wasteland -------------------------------------------
RING_Y=50                                                           # back edge of the ring's top
def _arena(d):
    for y in range(RING_Y):                                         # the sky, deep blue to haze
        k=y/(RING_Y-1); d.line([0,y,W,y],fill=(int(62+100*k),int(118+86*k),int(210+34*k)))
    haze=(150,152,186)                                              # far range, lost in the haze
    d.polygon([(0,40),(14,32),(30,34),(44,28),(70,33),(98,30),(118,34),(140,27),(160,31),(185,29),(185,44),(0,44)],fill=haze)
    rock,shade,strata=(178,124,82),(140,92,60),(198,150,104)
    for poly in ([(0,46),(0,24),(9,21),(27,21),(31,27),(40,29),(46,46)],   # the mesas and a spire
                 [(56,46),(59,18),(62,15),(65,17),(67,46)],
                 [(118,46),(124,27),(132,21),(158,21),(164,28),(185,30),(185,46)],
                 [(84,46),(88,36),(96,35),(100,46)]):
        d.polygon(poly,fill=rock)
    for y in (26,32,38):                                            # strata lines
        d.line([2,y,34,y],fill=strata); d.line([126,y-1,176,y-1],fill=strata)
    d.polygon([(27,21),(31,27),(40,29),(46,46),(36,46)],fill=shade)    # shaded flanks
    d.polygon([(158,21),(164,28),(185,30),(185,46),(166,46)],fill=shade)
    d.line([64,17,66,46],fill=shade); d.line([96,35,99,46],fill=shade)
    d.rectangle([0,44,W,H],fill=(200,170,118))               # the wasteland floor
    rr=random.Random(4242)
    for _ in range(40): d.point((rr.randint(0,W-1),rr.randint(44,RING_Y)),fill=rr.choice([(170,140,96),(222,196,146)]))
    x0b,x1b,x0f,x1f=12,172,4,180                                    # the ring: tiled top in perspective
    d.polygon([(x0b,RING_Y),(x1b,RING_Y),(x1f,GROUND+1),(x0f,GROUND+1)],fill=(232,230,220))
    for y in (52,55): d.line([lerp(x0b,x0f,(y-RING_Y)/9),y,lerp(x1b,x1f,(y-RING_Y)/9),y],fill=(196,194,184))
    for i in range(-7,8):
        d.line([92+i*11,RING_Y,92+i*12.5,GROUND],fill=(196,194,184))
    d.line([x0b,RING_Y,x1b,RING_Y],fill=(250,250,244))
    d.rectangle([x0f,GROUND+1,x1f,H],fill=(176,174,166))           # the front face, stone blocks
    d.line([x0f,GROUND+1,x1f,GROUND+1],fill=(246,246,238))
    for x in range(x0f+8,x1f,14): d.line([x,GROUND+2,x,H],fill=(140,138,132))
    d.line([x0f,GROUND+4,x1f,GROUND+4],fill=(150,148,140))
    for x in (x0b,x1b-2):                                           # corner posts
        d.rectangle([x,RING_Y-5,x+2,RING_Y],fill=(244,244,236)); d.point((x+2,RING_Y-4),fill=(190,188,180))
register_bg(THEME, lambda v: (v+120,v+120,v+112), decor=_arena)

# ---- effects -----------------------------------------------------------------------------------
CLOUDS=[(0,5,1.0),(70,11,0.7),(128,3,0.85),(190,9,0.6)]             # (x, y, size) — a 225px loop
@fx('dbzc_clouds')
def _fx_clouds(d,im,e,f):
    """Clouds drifting right; exactly one lap per clip, so the loop is seamless."""
    o=f*225//N_
    for x0,y,k in CLOUDS:
        x=(x0+o)%225-20; w=int(22*k)
        for dx,dy,r in ((0,3,4),(6,1,5),(13,2,4),(18,4,3)):
            rr_=max(2,int(r*k)); cx=x+dx*k
            d.ellipse([cx-rr_,y+dy-rr_,cx+rr_,y+dy+rr_//2+1],fill=(246,248,255))
        d.line([x-3,y+5,x+w,y+5],fill=(206,220,242))

@fx('dbzc_speed')
def _fx_speed(d,im,e,f):
    """Horizontal speed streaks across the frame."""
    rr=random.Random(f*7)
    for _ in range(8):
        y=rr.randint(10,GROUND-2); x=rr.randint(0,W-20); d.line([x,y,x+rr.randint(10,24),y],fill=(255,255,255))

@fx('dbzc_zip')
def _fx_zip(d,im,e,f):
    """Instant Transmission: the flicker lines left behind."""
    _,x,y=e; rr=random.Random(f*3+int(x))
    for _ in range(4):
        yy=y+rr.randint(-10,2); xx=x+rr.randint(-6,6); d.line([xx-5,yy,xx+5,yy],fill=(255,255,255))
        d.line([xx-3,yy+1,xx+3,yy+1],fill=(150,180,255))

@fx('dbzc_ball')
def _fx_ball(d,im,e,f):
    """A ki ball in the hands: x,y,r,(outer,mid), with a spiky corona."""
    _,x,y,r,(oc,mc)=e; ball(d,int(x),int(y),int(r),oc,mc,f); asterisk(d,int(x),int(y),int(r)+3,oc,f)

@fx('dbzc_clash')
def _fx_clash(d,im,e,f):
    """Where the two beams meet: a white-hot knot throwing sparks."""
    _,x,y,big=e; r=6+(f%3)+big; rr=random.Random(f)
    d.ellipse([x-r-2,y-r-2,x+r+2,y+r+2],fill=(255,236,170)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255))
    asterisk(d,x,y,r+5,(255,200,120),f)
    for _ in range(6):
        a=rr.random()*6.28; L=rr.randint(r+2,r+12); d.point((int(x+math.cos(a)*L),int(y+math.sin(a)*L*0.7)),fill=(255,255,200))

@fx('dbzc_bolt')
def _fx_bolt(d,im,e,f):
    """A little lightning crackle in the aura."""
    _,x,y=e; rr=random.Random(f*11+int(x)); pts=[(x,y)]
    for _ in range(4): x+=rr.randint(-3,3); y+=rr.randint(2,4); pts.append((x,y))
    d.line(pts,fill=(210,245,255)); d.point(pts[0],fill=(255,255,255))

@fx('dbzc_genki')
def _fx_genki(d,im,e,f):
    """The Spirit Bomb: a blue-white sun with a flickering corona."""
    _,x,y,r=e; x,y,r=int(x),int(y),int(r)
    glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([x-r-6,y-r-6,x+r+6,y+r+6],fill=120)
    im.paste((170,220,255),(0,0),glow.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=(120,190,255)); d.ellipse([x-r,y-r,x+r,y+r],fill=(190,232,255))
    d.ellipse([x-r+2,y-r+2,x+r//3,y+r//3],fill=(236,248,255)); d.ellipse([x-r//2,y-r//2,x,y],fill=(255,255,255))
    asterisk(d,x,y,r+5,(200,236,255),f)

@fx('dbzc_shard')
def _fx_shard(d,im,e,f):
    """A chip of the white ring tiles flying off."""
    _,x,y=e; d.rectangle([x,y,x+1,y],fill=(246,246,238)); d.point((x,y+1),fill=(150,148,140))

@fx('dbzc_regen')
def _fx_regen(d,im,e,f):
    """Cell regenerating: a writhing green mass that swells up out of one scrap (t 0..1)."""
    _,x,t=e; rr=random.Random(f%6)
    h=int(2+18*ease(t)); w=int(2+7*ease(t))
    for _ in range(int(6+22*t)):
        yy=GROUND-rr.randint(0,h); xx=x+rr.randint(-w,w)*(1-(GROUND-yy)/(h+8)); r=rr.randint(1,3)
        d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=(112,192,84) if rr.random()<0.6 else (52,118,44))
    for _ in range(3): d.point((x+rr.randint(-w,w),GROUND-rr.randint(0,h)),fill=(24,34,24))

# ---- close-up: Super Saiyan ---------------------------------------------------------------------
_HAIR_BASE=[(40,58,26,8),(50,70,54,0),(62,84,82,2),(76,98,106,8),(90,102,114,20),(40,50,24,22)]
_HAIR_GOLD=[(40,58,30,-6),(50,70,56,-10),(62,84,80,-10),(76,98,104,-4),(90,102,118,6),(40,50,22,8)]
_BANGS=[(50,62,56,40),(60,72,64,36),(78,90,86,38)]
def _hair(d,gold,sway):
    col,edge=((255,226,80),(200,140,20)) if gold else ((30,28,40),(120,130,190))
    for x0,x1,tx,ty in (_HAIR_GOLD if gold else _HAIR_BASE):
        d.polygon([(x0,30),(x1,30),(tx+sway,ty)],fill=col,outline=edge)
    d.rectangle([40,22,104,30],fill=col)
    for x0,x1,tx,ty in _BANGS: d.polygon([(x0,28),(x1,28),(tx,ty)],fill=col)
    if gold:
        for x0,x1,tx,ty in _HAIR_GOLD[1:4]: d.line([(x0+x1)//2,28,tx+sway,ty+6],fill=(255,248,190))

def closeup_ssj(t,f):
    """Primer plano: Claude strains, lightning, the hair flashes gold — SUPER SAIYAN!"""
    gold=t>=0.4 or (0.3<=t<0.4 and f%2==0)
    im=Image.new('RGB',(W,H),(110,70,10) if gold else (44,50,96)); d=ImageDraw.Draw(im)
    if gold:                                                        # a hot glow behind the head
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([10,-20,136,80],fill=150)
        im.paste((255,200,60),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    rr=random.Random(f)
    for _ in range(64 if gold else 24):                             # aura flames behind him
        x=rr.randint(12,134); h=rr.randint(8,36); y=rr.randint(20,66)
        c=((255,214,70) if rr.random()<0.6 else (255,246,190)) if gold else ((190,196,230) if rr.random()<0.5 else (90,96,140))
        d.line([x,y,x+rr.randint(-2,2),y-h],fill=c)
    jx=((f%3)-1)*(2 if t<0.4 else 0)
    ox=jx
    _hair(d,gold,(f%2)*(1 if gold else 0))
    d.rectangle([44+ox,30,100+ox,64],fill=(217,119,87)); d.rectangle([44+ox,30,50+ox,64],fill=(176,92,66))
    for x0,x1,tx,ty in _BANGS:
        d.polygon([(x0+ox,29),(x1+ox,29),(tx+ox,ty)],fill=(255,226,80) if gold else (30,28,40))
    if not gold:                                                    # eyes squeezed shut, straining
        for ex in (60,82):
            d.line([ex-3+ox,44,ex+3+ox,47],fill=(24,14,12)); d.line([ex-3+ox,50,ex+3+ox,47],fill=(24,14,12))
        d.rectangle([62+ox,55,84+ox,61],fill=(24,14,12)); d.rectangle([63+ox,56,83+ox,60],fill=(246,240,230))   # gritted teeth
        d.line([63+ox,58,83+ox,58],fill=(150,140,130))
    else:                                                           # teal Super Saiyan eyes
        for ex in (60,82):
            d.rectangle([ex-2,40,ex+3,52],fill=(24,14,12)); d.rectangle([ex-1,42,ex+2,50],fill=(60,200,176))
            d.rectangle([ex,43,ex+1,45],fill=(230,255,250))
        d.line([56,38,66,40],fill=(24,14,12)); d.line([78,40,88,38],fill=(24,14,12))   # the scowl
        d.line([66,58,78,57],fill=(120,50,36))                     # a hard set mouth
    for k in range(3 if not gold else 5):                           # lightning in the aura
        x=rr.randint(20,130); y=rr.randint(4,30); pts=[(x,y)]
        for _ in range(5): x+=rr.randint(-4,4); y+=rr.randint(3,6); pts.append((x,y))
        d.line(pts,fill=(220,240,255))
    if t<0.3: say(im,"HAAAAA",26,(236,240,255),scale=2,cx=144+jx,outline=(40,40,90))
    if 0.4<=t<0.46:
        im=fade_to(im,(255,250,220),1-(t-0.4)/0.06); d=ImageDraw.Draw(im); zoom_lines(d,(255,236,120))
    if t>=0.48:
        jj=(f%3)-1 if t<0.58 else 0
        say(im,"SUPER",10,(255,244,160),scale=3,cx=146+jj,outline=(120,70,0))
        say(im,"SAIYAN!",34,(255,255,255),scale=2,cx=146+jj,outline=(120,70,0))
    if t<0.06: zoom_lines(d,(236,240,255))
    if t>0.9: im=fade_to(im,(255,240,170),(t-0.9)/0.1*0.7)
    return im

# ---- the clip ----------------------------------------------------------------------------------
def ghost(spr,x,y=GROUND,flip=False,tint=(255,236,200),a=0.35):
    return actor(spr,x,y,flip=flip,alpha=a,tint=tint)

def clip_cellgames(f):
    s=scene(f,THEME)
    s['under'].append(('dbzc_clouds',))
    ssj=292<=f<404 or (404<=f<424 and (f//2)%2==0)                  # powers down with a flicker
    FORM=SSJ if ssj else BASE
    cl=actor(FORM[guard_pose(f)],CX,pal=SSJPAL if ssj else None)
    ce=actor(CE['idle'],EX,flip=True)
    extra=[]; aura_c=AURA_G if ssj else AURA_W
    def pose(p): cl['spr']=FORM[p]
    # 1) the stare-down: CELL GAMES, the wind, both power up
    if 8<=f<40:
        say_y=6 if f>=12 else 6-(12-f)
        s['fx'].append(('dbzc_say',"CELL GAMES",say_y,(255,255,255),2,W//2,(60,120,40)))
    if 10<=f<44:
        for i in range(8): s['fx'].append(('dust',(i*29+(f-10)*4)%W,GROUND-(i*5)%6))
    if 24<=f<44: ce['spr']=CE['guard']
    if 30<=f<44: cl['aura']=(AURA_W,1+(f%2)); ce['aura']=(CELL_AURA,1+(f%2))
    if 34<=f<44 and f%3==0: s['fx'].append(('rock',random.randint(10,175),GROUND-random.randint(0,12)))
    # 2) the clash in the middle of the ring
    if 44<=f<54:
        t=(f-44)/10; cl.update(x=ez(CX,84,t),aura=(AURA_W,2)); pose('dash')
        ce.update(spr=CE['punch'],x=ez(EX,104,t),aura=(CELL_AURA,2))
        extra+=[ghost(FORM['dash'],cl['x']-7),ghost(FORM['dash'],cl['x']-14,a=0.2),
                ghost(CE['punch'],ce['x']+8,flip=True,tint=(210,255,200)),ghost(CE['punch'],ce['x']+16,flip=True,tint=(210,255,200),a=0.2)]
        s['fx'].append(('dbzc_speed',))
    if 54<=f<62:
        cl['x']=84; ce.update(x=104,spr=CE['punch']); pose('punch')
        if f==54: s['flash']=0.9; s['fc']=(94,GROUND-8)
        for j in range(2): s['fx'].append(('ring',94,GROUND-8,(f-54)*6+j*5,(255,255,255)))
        s['fx'].append(('spark',94,GROUND-8,8-(f-54))); s['shake']=rshake(2)
        if f<58:
            for j in range(4): s['fx'].append(('dbzc_shard',random.randint(60,130),GROUND-random.randint(0,14)))
    # 3) the rush barrage, blinking up into the sky and back
    if 62<=f<96:
        k=f-62; ph=(k//3)%4
        cp,ep=[('punch','hurt'),('guard','punch'),('hurt','punch'),('punch','guard')][ph]
        air=0; cx,ex=84,104
        if 72<=f<76 or 86<=f<88:                                    # both vanish...
            cl['vis']=ce['vis']=False
            s['fx']+=[('dbzc_zip',84 if f<80 else 64,GROUND-6 if f<80 else GROUND-28),('dbzc_zip',104 if f<80 else 86,GROUND-6 if f<80 else GROUND-28)]
        elif 76<=f<86:                                              # ...and trade blows in the sky
            air=24; cx,ex=64,86
        cl.update(x=cx+random.choice([-1,0,1]),y=GROUND-air,aura=(AURA_W,1+(f%2))); pose(cp)
        ce.update(x=ex+random.choice([-1,0,1])-(2 if ep=='hurt' else 0),y=GROUND-air,spr=CE[ep],aura=(CELL_AURA,1+(f%2)))
        if k%3==0 and cl['vis']:
            s['fx'].append(('spark',(cx+ex)//2+random.randint(-2,2),GROUND-air-8+random.randint(-3,3),4+random.randint(0,2)))
            s['shake']=rshake()
        if k%12==0: s['fx'].append(('ring',(cx+ex)//2,GROUND-air-8,8,(255,255,255)))
        s['fx'].append(('dbzc_speed',))
    # 4) Cell's knee sends Claude skidding back
    if 96<=f<112:
        ce.update(spr=CE['punch'] if f<100 else CE['guard'],x=104 if f<100 else ez(104,EX,(f-100)/12),aura=(CELL_AURA,1))
        t=(f-96)/10; cl.update(x=ez(84,24,t),y=GROUND-int(8*math.sin(math.pi*min(1,t)))); pose('hurt')
        if f==96: s['fx'].append(('spark',93,GROUND-8,10)); s['flash']=0.5; s['fc']=(93,GROUND-8); s['shake']=rshake(2)
        if f>=104:
            for _ in range(2): s['fx'].append(('dust',cl['x']+random.randint(2,9),GROUND-random.randint(0,3)))
    # 5) Instant Transmission: gone, and down on him from above
    if 112<=f<124:
        cl['x']=24; pose('guard'); s['fx'].append(('twinkle',32,GROUND-8,1+(f%2)))
        shout(s,"INSTANT TRANSMISSION",(255,236,150))
    if 112<=f<144: ce.update(spr=CE['guard'],x=EX)
    if 122<=f<124: s['fx'].append(('dbzc_zip',24,GROUND-4)); cl['vis']=(f%2==0)
    if 124<=f<136:
        cl['vis']=False
        ce['flip']=not (128<=f<133)                                 # he looks around
        if f>=126: s['fx'].append(('dmg',"?",EX-1,GROUND-30,(255,255,255)))
    if 136<=f<144:
        drop=0 if f<140 else (f-140)/3
        cl.update(x=EX-2,y=int(lerp(GROUND-30,GROUND-22,drop)),vis=True); pose('armsup')
        if f<138: s['fx'].append(('dbzc_zip',EX,GROUND-36))
        s['fx'].append(('dmg',"!",EX+12,GROUND-30,(255,90,60)))
    if 143<=f<150:                                                  # the slam
        ce.update(spr=CE['hurt'],x=EX,y=GROUND+(2 if f<147 else 1))
        cl.update(x=EX-2,y=GROUND-21,vis=True); pose('armsup')
        if f==143: s['flash']=0.6; s['fc']=(EX,GROUND-14)
        s['fx'].append(('ring',EX,GROUND,(f-143)*6+4,(255,255,255))); s['shake']=rshake(2)
        s['fx'].append(('spark',EX,GROUND-22,9-(f-143)))
        for j in range(4): s['fx'].append(('dbzc_shard',EX+random.randint(-22,22),GROUND-random.randint(0,12)))
        for j in range(3): s['fx'].append(('dust',EX+random.randint(-16,16),GROUND-random.randint(0,4)))
    if 150<=f<164:                                                  # Claude backflips home
        t=(f-150)/14; cl.update(x=ez(EX-2,CX,t),y=int(ez(GROUND-21,GROUND,t)-18*math.sin(math.pi*t)),vis=True)
        cl['spr']=spin(FORM['guard'],f) if t<0.85 else FORM['guard']
        ce.update(spr=CE['hurt'],x=EX)
    if 158<=f<172:
        ce.update(spr=CE['flare'],x=EX,aura=(CELL_AURA,2+(f%2))); s['shake']=rshake() if f%2 else (0,0)
        shout(s,"ENOUGH!",(190,255,150),cx=EX-10)
    # 6) KAMEHAMEHA vs KAMEHAMEHA
    if 172<=f<250:
        ce.update(spr=CE['charge'],x=EX,aura=(CELL_AURA,2+(f%3==0)))
        cl.update(x=CX,aura=(aura_c,2+(f%3==0))); pose('charge')
    if 172<=f<200:
        t=(f-172)/28
        s['fx'].append(('dbzc_ball',142,GROUND-11,1+4*t,CELL_KI))
        if f>=180: s['fx'].append(('dbzc_ball',38,GROUND-6,1+4*(f-180)/20,KI))
        if f%3==0: s['fx'].append(('rock',random.randint(10,175),GROUND-random.randint(0,int(24*t))))
        if f>=188: s['shake']=rshake()
        shout(s,"KAMEHAMEHA!",(150,210,255),cx=138)
        if f>=180: shout(s,"KAMEHAMEHA!",(255,200,150),y=10,cx=46)
    if 200<=f<250:
        t=f-200
        mid=int(94+8*math.sin(t*0.35)-(ez(0,34,(f-220)/28) if f>=220 else 0))
        s['fx']+=[('beam',38,mid,GROUND-6,KI),('beam',mid,141,GROUND-11,CELL_KI),('dbzc_clash',mid,GROUND-8,0)]
        s['shake']=rshake(2 if f>=230 else 1)
        if f%2==0: s['fx'].append(('rock',random.randint(mid-30,mid+30),GROUND-random.randint(0,25)))
        if f>=232: cl['x']=CX+random.choice([-1,0]); shout(s,"GIVE UP!",(190,255,150),cx=EX-8)
        if f<206: s['flash']=0.5*(1-(f-200)/6); s['fc']=(94,GROUND-8)
    # 7) close-up: SUPER SAIYAN
    if 250<=f<292: s['image']=closeup_ssj((f-250)/42,f); return s
    # 8) the golden Kamehameha blows through
    if 292<=f<316:
        ce.update(spr=CE['charge'] if f<304 else CE['hurt'],x=EX,aura=(CELL_AURA,2) if f<304 else None)
        cl.update(x=CX,aura=(AURA_G,3)); pose('charge')
        if f%2==0: s['fx'].append(('dbzc_bolt',CX+random.randint(-8,8),GROUND-18))
        if f<304:
            mid=int(ez(60,141,(f-292)/12))
            s['fx']+=[('beam',38,mid,GROUND-6,KI_SSJ),('beam',mid,141,GROUND-11,CELL_KI),('dbzc_clash',mid,GROUND-8,2)]
        elif f<312: s['fx'].append(('beam',38,200,GROUND-7,KI_SSJ))
        if f==292: s['flash']=0.9; s['fc']=(CX,GROUND-8); s['flashc']=(255,240,170)
        if f==304: s['flash']=1.0; s['fc']=(EX,GROUND-10)
        if f>=304: s['fx'].append(('boom',EX,GROUND-10,(f-304)*5+4)); ce['vis']=f<306
        s['shake']=rshake(2); shout(s,"HAAAAA!",(255,236,120),cx=46)
    if 312<=f<332:                                                  # the smoke clears: Cell, burnt
        dens=1 if f<320 else max(0,(332-f)/12)
        rr=random.Random(f//2)
        for i in range(int(20*dens)):
            s['fx'].append(('smoke',EX+rr.randint(-16,16),GROUND-2-rr.randint(0,20),rr.randint(2,5),(90,86,90) if i%2 else (130,126,128)))
        ce.update(spr=CE['hurt'],x=EX,pal=CE_BURNT,vis=f>=318)
    if 316<=f<340: cl.update(x=CX,aura=(AURA_G,1+(f%2)))
    if 332<=f<346:
        ce.update(spr=CE['flare'],x=EX,pal=CE_BURNT,aura=(CELL_AURA,2+(f%2)))
        shout(s,"I AM PERFECT!",(190,255,150),cx=EX-18); s['shake']=rshake() if f%2 else (0,0)
    # 9) GENKI DAMA
    GC=lambda r: (CX,GROUND-12-r)
    if 340<=f<372:
        t=(f-340)/32; r=2+12*ease(t)
        s['under'].append(('dim',0.35*min(1,(f-340)/8)))
        cl.update(x=CX,aura=(AURA_G,1)); pose('armsup')
        x,y=GC(r); s['under'].append(('dbzc_genki',x,y,r))
        for i in range(16):                                         # the energy pours in from the sky
            a=i*2.39996; ph=((f*0.04+i*0.137)%1); L=(1-ph)*150
            s['fx'].append(('mote',x+math.cos(a)*L,y-abs(math.sin(a))*L*0.4,(200,236,255) if i%2 else (255,255,255)))
        if f>=356 and f%3==0: s['shake']=rshake()
        shout(s,"GENKI DAMA!",(200,236,255))
    if 346<=f<388: ce.update(spr=CE['charge'],x=EX,pal=CE_BURNT,aura=(CELL_AURA,2))
    if 356<=f<372: s['fx'].append(('dbzc_ball',142,GROUND-11,1+(f-356)//4,CELL_KI))
    if 372<=f<388:
        s['under'].append(('dim',0.35))
        pose('punch'); cl.update(x=CX,aura=(AURA_G,1))
        x0,y0=GC(14)
        if f<380: t=(f-372)/8; bx=lerp(x0,122,ease(t)); by=lerp(y0,GROUND-16,t)-8*math.sin(math.pi*t)
        else: bx=lerp(122,EX-8,(f-380)/8); by=GROUND-16
        s['under'].append(('dbzc_genki',bx,by,14))
        if f>=378 and int(bx)+12<141: s['under'].append(('beam',int(bx)+12,141,GROUND-11,CELL_KI)); s['fx'].append(('spark',int(bx)+13,GROUND-11+random.randint(-4,4),4))
        if f>=380: s['shake']=rshake(2); ce['spr']=CE['hurt']; shout(s,"NO!",(190,255,150),cx=EX)
    if 388<=f<404:
        ce['vis']=False; t=(f-388)/16
        s['fx'].append(('boom',EX,GROUND-12,int(6+64*t)))
        for j in range(2): s['fx'].append(('ring',EX,GROUND-8,int(10+80*t)+j*8,(200,236,255)))
        s['flash']=1.0 if f<394 else max(0,1-(f-394)/10); s['fc']=(EX,GROUND-12); s['flashc']=(236,248,255); s['shake']=rshake(2)
        cl.update(x=CX,aura=(AURA_G,1)); pose('guard')
    # 10) the aftermath: Claude powers down, Cell grows back from one scrap
    if 404<=f<432:
        ce['vis']=False
        if f<420:
            rr=random.Random(f//2)
            for i in range(int(12*(420-f)/16)): s['fx'].append(('smoke',EX+rr.randint(-14,14),GROUND-rr.randint(2,20),rr.randint(2,4),(96,92,96)))
        if f>=412: s['under'].append(('dbzc_regen',EX,(f-412)/20))
    if 404<=f<424: cl['aura']=(aura_c,1) if f%4<2 else None
    if 432<=f<446:
        ce.update(spr=CE['hurt'] if f<440 else CE['guard'],tint=(112,192,84) if f<436 else None)
    s['actors']=extra+[cl,ce]
    return s

CLIPS = [clip('cellgames', N_, clip_cellgames)]
