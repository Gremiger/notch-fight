"""League of Legends sub-theme "lol-yasuo": Yasuo, the Unforgiven. Clip `flute`, no fight: sunset in Ionia,
Yasuo (the high ponytail, the steel pauldron, blue tunic and red sash) sitting on a rock under a cherry
tree, his katana leaning beside him, playing the bamboo flute; the notes come out as petals and the wind
carries them off. Close-up: eyes closed, hair in the wind — DEATH IS LIKE THE WIND. ALWAYS BY MY SIDE.
A small bird lands on the katana's hilt; he stops, smiles, takes a sip from his sake gourd, plays on, and
the bird flies off."""
from engine import *

THEME = 'lol-yasuo'
N_ = 360                                                            # a multiple of 12
YX, ROCK = 64, 64                                                   # Yasuo on his rock
TREE = 146
PINK, PINK_D, PINK_L = (240,150,180), (214,110,150), (255,200,220)
SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(40,20,16)
# Yasuo: dark brown hair tied high with a long tail, the steel pauldron, blue-grey tunic, red sash, dark pants
YPAL = {'1':(56,40,34),'2':(84,62,50),'3':(170,176,186),'4':(80,104,140),'5':(170,50,50),'6':(46,44,54)}
HAIR = ["11..........",".11..1......","..1111111...",".111111111..","11111111111."]

def _yasuo(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0,bangs="1111......")]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y==top+5 and x in (l,l+1,l+2): g[y][x]='3'        # the pauldron
            elif c=='O' and y==top+7: g[y][x]='5'                          # the sash
            elif c=='O' and y>=top+5: g[y][x]='4'
            elif c=='o' and y<top+8: g[y][x]='4'
            elif c=='o': g[y][x]='6'
    return S([''.join(x) for x in g])
YASUO=variant(_yasuo)
def scale2(spr): return S([''.join(c*2 for c in r) for r in spr for _ in (0,1)])
BIG={k:scale2(v) for k,v in YASUO.items()}                          # he sits close to us: double size

# ---- background: Ionia at sunset ----------------------------------------------------------------------
def _ionia(d):
    for y in range(44):                                             # the sunset
        k=y/43; d.line([0,y,W,y],fill=(int(250-60*k),int(150+20*k),int(120+40*k)) if k<0.5 else (int(220-60*(k-0.5)),int(160-40*(k-0.5)),int(150+20*(k-0.5))))
    d.ellipse([22,26,46,50],fill=(255,220,150))                        # the sun going down
    for pts,c in (([(0,40),(30,26),(60,34),(96,22),(130,32),(170,24),(185,30),(185,44),(0,44)],(150,110,150)),
                  ([(0,44),(40,34),(80,40),(120,32),(160,40),(185,36),(185,46),(0,46)],(120,90,130))):
        d.polygon(pts,fill=c)                                          # far mountains, in layers
    d.rectangle([0,44,W,H],fill=(96,140,90))                            # the grass
    for x in range(0,W,5): d.line([x,45,x+1,43],fill=(120,170,100))
    rr=random.Random(21)
    for _ in range(30): d.point((rr.randint(0,W-1),rr.randint(46,H-1)),fill=PINK_L)   # fallen petals
    x=TREE                                                             # the cherry tree
    d.polygon([(x-4,GROUND),(x-2,24),(x+3,24),(x+5,GROUND)],fill=(70,46,40))
    d.line([x,30,x-16,18],fill=(70,46,40),width=2); d.line([x+2,28,x+16,16],fill=(70,46,40),width=2)
    for _ in range(46):
        cx=x+rr.randint(-30,30); cy=rr.randint(2,26); r=rr.randint(4,8)
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=rr.choice([PINK,PINK_D,PINK_L]))
    d.rectangle([20,40,26,46],fill=(150,150,140)); d.polygon([(18,40),(23,36),(28,40)],fill=(130,130,120))   # a stone lantern
    d.point((23,43),fill=(255,220,140))
register_bg(THEME, lambda v: (v+60,v+90,v+60), decor=_ionia)

# ---- effects --------------------------------------------------------------------------------------------
@fx('ys_rock')
def _fx_rock(d,im,e,f):
    """His rock, over his legs (he is sitting), the katana leaning on it, the sake gourd at its foot."""
    x=ROCK
    d.polygon([(x-24,GROUND+2),(x-20,GROUND-12),(x-6,GROUND-17),(x+12,GROUND-15),(x+22,GROUND-6),(x+24,GROUND+2)],fill=(120,116,110),outline=(70,66,62))
    d.line([x-14,GROUND-14,x+10,GROUND-12],fill=(150,146,140)); d.line([x+4,GROUND-6,x+16,GROUND-4],fill=(96,92,88))

@fx('ys_katana')
def _fx_katana(d,im,e,f):
    """The katana in its scabbard, leaning against the rock, the hilt up."""
    x=ROCK+28
    d.line([x,GROUND,x-5,GROUND-28],fill=(40,30,40),width=3)
    d.line([x-5,GROUND-28,x-6,GROUND-37],fill=(150,40,40),width=3); d.line([x-9,GROUND-28,x-1,GROUND-28],fill=(200,170,80),width=2)

@fx('ys_gourd')
def _fx_gourd(d,im,e,f):
    """The sake gourd: x,y = its foot."""
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-3,y-5,x+3,y],fill=(170,70,40),outline=INK); d.ellipse([x-2,y-9,x+2,y-5],fill=(170,70,40),outline=INK)
    d.line([x-3,y-6,x+3,y-6],fill=(230,210,150))

@fx('ys_flute')
def _fx_flute(d,im,e,f):
    """The bamboo flute, held across from his mouth."""
    _,x,y=e; x,y=int(x),int(y)
    d.line([x,y,x+20,y+2],fill=(200,180,110),width=3)
    for k in (6,10,14,18): d.point((x+k,y+1),fill=(110,90,50))

@fx('ys_notes')
def _fx_notes(d,im,e,f):
    """Notes and petals drifting off the end of the flute and away on the wind (a loop of 60 frames)."""
    _,x,y,a=e
    if a<=0: return
    for i in range(6):
        ph=((f+i*10)%60)/60
        px=x+ph*90; py=y-ph*26+math.sin(ph*9+i)*4
        if i%2:
            d.ellipse([px-1,py-1,px+1,py+1],fill=PINK if i%3 else PINK_L)    # a petal
        else:
            d.ellipse([px-1,py,px+1,py+2],fill=(250,250,250)); d.line([px+1,py+1,px+1,py-3],fill=(250,250,250))   # a note
            if i%4==0: d.line([px+1,py-3,px+3,py-2],fill=(250,250,250))

@fx('ys_petals')
def _fx_petals(d,im,e,f):
    """Petals off the tree, blowing across the panel (the wind), one lap per 120 frames."""
    rr=random.Random(7)
    for i in range(18):
        x0=rr.uniform(0,W); y0=rr.uniform(0,40); sp=rr.choice((1,2,3))
        x=(x0-f*W*sp/120)%W; y=(y0+f*50*sp/N_+math.sin(2*math.pi*f/120+i)*3)%50
        d.point((int(x),int(y)),fill=PINK if i%2 else PINK_L)

@fx('ys_bird')
def _fx_bird(d,im,e,f):
    """A little bird; flying (wings beating) or perched."""
    _,x,y,flying=e; x,y=int(x),int(y)
    d.ellipse([x-2,y-2,x+2,y+1],fill=(120,90,60),outline=INK); d.point((x+3,y-1),fill=(240,180,60))
    d.point((x+1,y-1),fill=INK); d.line([x-2,y,x-4,y+1],fill=(90,66,44))
    if flying:
        up=(f//2)%2; d.line([x-1,y-1,x-3,y-4+up*3],fill=(90,66,44)); d.line([x,y-1,x+2,y-4+up*3],fill=(90,66,44))

# ---- close-up -------------------------------------------------------------------------------------------
def closeup_wind(t,f):
    """Primer plano: eyes closed, the flute at his lips, his hair streaming in the wind and petals going
    past — DEATH IS LIKE THE WIND. ALWAYS BY MY SIDE."""
    im=Image.new('RGB',(W,H),(230,150,140)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([0,y,W,y],fill=(int(240-40*y/H),int(160-30*y/H),int(140+20*y/H)))
    ox=24
    for k in range(9):                                              # the hair, blowing out behind
        y0=6+k*5; L=30+int(8*math.sin(f*0.2+k))
        d.polygon([(ox,y0),(ox-L,y0+3+int(3*math.sin(f*0.25+k))),(ox,y0+6)],fill=YPAL['1'])
    d.rectangle([ox,12,ox+54,H],fill=SKIN,outline=INK); d.rectangle([ox+48,12,ox+54,H],fill=SKIN_D)
    d.rectangle([ox-2,4,ox+56,14],fill=YPAL['1']); d.polygon([(ox+20,4),(ox+30,-6),(ox+34,4)],fill=YPAL['1'])
    for ex in (ox+16,ox+38): d.arc([ex-6,26,ex+6,34],20,160,fill=INK,width=2)   # eyes closed
    d.line([ox+10,22,ox+22,23],fill=INK); d.line([ox+32,23,ox+44,22],fill=INK)
    d.line([ox+20,48,ox+130,52],fill=(200,180,110),width=5)          # the flute, across
    for k in range(5): d.ellipse([ox+50+k*14,48,ox+53+k*14,51],fill=(110,90,50))
    d.ellipse([ox+46,44,ox+60,56],fill=SKIN,outline=INK); d.ellipse([ox+86,44,ox+100,56],fill=SKIN,outline=INK)   # fingers
    rr=random.Random(4)
    for i in range(16):                                              # petals going by on the wind
        x=(rr.uniform(0,W)+f*3)%W; y=(rr.uniform(0,H)+math.sin(f*0.1+i)*6)%H
        d.ellipse([x-2,y-1,x+2,y+1],fill=PINK if i%2 else PINK_L)
    if t>=0.15:
        big_text(im,"DEATH IS LIKE",4,(255,255,255),scale=1,cx=146,outline=(80,40,60))
        big_text(im,"THE WIND.",12,(255,255,255),scale=1,cx=146,outline=(80,40,60))
    if t>=0.4:
        big_text(im,"ALWAYS",24,PINK_L,scale=2,cx=146,outline=(80,40,60))
        big_text(im,"BY MY SIDE.",40,PINK_L,scale=1,cx=146,outline=(80,40,60))
    if t<0.05: zoom_lines(d)
    if t>0.92: im=fade_to(im,(255,220,200),0.5*(t-0.92)/0.08)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
SEAT=GROUND-12                                                       # his feet, up on the rock
def clip_flute(f):
    s=scene(f,THEME)
    pose=guard_pose(f); playing=True
    spr=BIG[pose]; ox,oy=origin(spr,YX,SEAT); top,l,r=body_box(spr)
    mouth=(ox+r+1,oy+top+9)
    gourd=(ROCK-30,GROUND)
    if 120<=f<210: s['image']=closeup_wind((f-120)/90,f); return s
    # the bird lands on the hilt; he stops, a sip of sake, plays on; the bird goes
    hilt=(ROCK+22,GROUND-39)
    bird=None
    if 214<=f<232: p=(f-214)/18; bird=(lerp(W+6,hilt[0],p),lerp(10,hilt[1],p)-8*math.sin(p*math.pi),True)
    if 232<=f<326: bird=(hilt[0],hilt[1],False)
    if 326<=f<344: p=(f-326)/18; bird=(lerp(hilt[0],-10,p),lerp(hilt[1],4,p),True)
    if 236<=f<300: playing=False
    if 262<=f<290: gourd=(mouth[0]+3,mouth[1]+12); pose='charge'
    s['under'].append(('ys_petals',))
    s['under'].append(('ys_katana',))
    s['actors']=[actor(BIG[pose],YX,SEAT,pal=YPAL)]
    s['fx'].append(('ys_rock',))
    s['fx'].append(('ys_gourd',)+gourd)
    if playing:
        s['fx'].append(('ys_flute',)+mouth)
        s['fx'].append(('ys_notes',mouth[0]+20,mouth[1]+2,1.0))
    if bird: s['fx'].append(('ys_bird',)+bird)
    return s

CLIPS = [clip('flute', N_, clip_flute)]
