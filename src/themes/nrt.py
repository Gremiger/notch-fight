"""Naruto: Claude (Naruto) vs Madara in the Hidden Leaf, under the Hokage rock faces. The cross
hand-seal close-up (KAGE BUNSHIN NO JUTSU!), a street full of clones that Madara swats away with
his gunbai, the Sharingan close-up, a Great Fireball that Claude leaps over, the Rasengan charging
in his palm (close-up) — Claude and a clone drive it into Madara, who is blasted down the street
and walks back for the loop."""
from engine import *

THEME = 'nrt'
N_ = 336
CX, EX = 30, 152                                                    # the loop keyframe positions

NARU=variant(lambda s: recolor_rows(overlay(s,["Y.Y.Y.Y.Y.Y.","YYYYYYYYYYYY",".YYYYYYYYYY."],-2,0),
    lambda x,y,t,l,r,c: ('D' if l+2<=x<=l+5 else 'N') if (y==t and l<=x<=r and c!='.') else None))
MADARA=poses(S([
"....kkkkkk........","..kkkkkkkkkk......",".kkkkkkkkkkkk.....","kkkkkkksssssk.....","kkkkkksrssrsk.....",
"kkkkkksssssk......",".kkkkkksssk.......","kkkkkRRRRRRR......","kkkkRRRRRRRRR.....","kkkRRZRRRRZRRR....",
"kkkRR.NNNN.RR.....",".kkRR.NNNN.RR.....",".kk.s.RRRR.s......","..k...RRRR........","......RZZR........",
".....RRRRRR.......",".....RR..RR.......",".....RR..RR.......",".....NN..NN.......",".....NN..NN.......",
".....NN..NN.......","....kkk..kkk......",]),10,'Rs',4)
MADARA_AURA=(170,110,255)
CHAKRA=((170,220,255),(70,150,255))
SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(40,20,16)                 # Claude's hands in the close-ups

# ---- background: the Hidden Leaf village under the Hokage rock -----------------------------------
def _face(d,x,hair):
    """One carved Hokage head on the cliff, hair style 0..3."""
    rock,lit,dark=(214,196,164),(232,218,190),(120,102,80)
    d.rectangle([x-7,17,x+7,33],fill=dark)
    d.rectangle([x-6,18,x+6,32],fill=rock); d.rectangle([x+3,18,x+6,32],fill=(170,150,120))
    d.polygon([(x-6,32),(x+6,32),(x+3,35),(x-3,35)],fill=rock)     # the chin
    if hair==0: d.polygon([(x-8,34),(x-7,15),(x+7,15),(x+8,34),(x+6,34),(x+6,19),(x-6,19),(x-6,34)],fill=dark)
    if hair==1: d.polygon([(x-7,19),(x-6,14),(x-3,16),(x,12),(x+3,16),(x+6,13),(x+7,19)],fill=lit)
    if hair==2: d.polygon([(x-8,20),(x-6,13),(x+6,13),(x+8,20)],fill=dark); d.line([x-8,20,x+8,20],fill=lit)
    if hair==3:
        for k in range(5): d.polygon([(x-7+k*3,19),(x-5+k*3,19),(x-8+k*3,12+(k%2)*2)],fill=lit)
        d.polygon([(x-7,19),(x-9,27),(x-6,24)],fill=lit)
    for ex in (x-3,x+2): d.line([ex-1,24,ex+1,24],fill=(70,56,44))
    d.line([x,25,x,28],fill=dark); d.line([x-2,30,x+2,30],fill=(96,80,64))

def _konoha(d):
    for y in range(46):                                             # late-afternoon sky
        k=y/45; d.line([0,y,W,y],fill=(int(96+150*k),int(150+62*k),int(222-60*k)))
    cliff,cshade=(170,150,120),(138,118,94)
    d.polygon([(40,46),(46,16),(56,11),(80,9),(120,8),(150,10),(166,14),(176,24),(185,26),(185,46)],fill=cliff)
    d.polygon([(166,14),(176,24),(185,26),(185,46),(170,46)],fill=cshade)
    for y in (36,40): d.line([48,y,180,y],fill=cshade)
    for i,x in enumerate((72,98,124,150)): _face(d,x,i)
    rr=random.Random(77)
    for _ in range(26):                                             # the forest on the left ridge
        x=rr.randint(-4,52); y=rr.randint(22,40); r=rr.randint(4,8)
        d.ellipse([x-r,y-r,x+r,y+r],fill=rr.choice([(58,120,62),(72,140,70),(46,100,54)]))
    walls,roofs=[(232,214,180),(214,198,168),(238,226,196)],[(178,72,52),(150,60,46),(96,120,90),(190,96,60)]
    x=0; i=0
    while x<W:                                                      # the rooftops
        w=rr.randint(12,22); top=rr.randint(34,40); c=walls[i%3]; rf=roofs[rr.randint(0,3)]
        d.rectangle([x,top,x+w,50],fill=c); d.line([x+w,top,x+w,50],fill=(170,150,124))
        d.polygon([(x-2,top+1),(x+w//2,top-4),(x+w+2,top+1)],fill=rf)
        for wx in range(x+3,x+w-2,5): d.rectangle([wx,top+4,wx+1,top+6],fill=(70,56,50))
        x+=w+rr.randint(0,3); i+=1
    d.rectangle([0,50,W,H],fill=(206,176,128))                      # the dirt street
    d.line([0,50,W,50],fill=(170,140,100)); d.line([0,GROUND+1,W,GROUND+1],fill=(186,154,110))
    for _ in range(50): d.point((rr.randint(0,W-1),rr.randint(51,H-1)),fill=rr.choice([(180,150,106),(226,198,150)]))
register_bg(THEME, lambda v: (v+150,v+120,v+80), decor=_konoha)

# ---- effects -----------------------------------------------------------------------------------
@fx('gunbai')
def _fx_gunbai(d,im,e,f):
    _,x,y=e; d.line([x,y+4,x+6,y-4],fill=(120,80,50)); d.ellipse([x-6,y-10,x+4,y],fill=(230,220,200),outline=(140,30,30))
    d.line([x-5,y-5,x+3,y-5],fill=(140,30,30))

@fx('nrt_gunbai_back')
def _fx_gunbai_back(d,im,e,f):
    """Madara's war fan slung on his back."""
    _,x,y=e; x=int(x)
    d.line([x+2,y-4,x+7,y-20],fill=(110,74,46)); d.ellipse([x+2,y-28,x+12,y-18],fill=(226,216,196),outline=(140,30,30))
    d.line([x+3,y-23,x+11,y-23],fill=(140,30,30))

CLOUDS=[(0,4,1.0),(80,10,0.7),(150,2,0.85)]
@fx('nrt_clouds')
def _fx_clouds(d,im,e,f):
    """Clouds drifting left behind the Hokage rock: one 225px lap per clip, a seamless loop."""
    o=f*225//N_
    for x0,y,k in CLOUDS:
        x=(x0-o)%225-20
        for dx,dy,r in ((0,3,3),(5,1,4),(11,2,3),(15,4,2)):
            rr_=max(2,int(r*k)); cx=x+dx*k
            d.ellipse([cx-rr_,y+dy-rr_,cx+rr_,y+dy+rr_//2+1],fill=(255,244,226))

@fx('nrt_leaf')
def _fx_leaf(d,im,e,f):
    _,x,y,c=e; x,y=int(x),int(y); d.point((x,y),fill=c); d.point((x+1,y+(f//3)%2),fill=(40,96,44))

@fx('nrt_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,cx,outline=e; big_text(im,txt,int(y),c,scale=scale,cx=int(cx),outline=outline)

def shout(s,txt,c,y=2,scale=2,cx=W//2,outline=(0,0,0)):
    """Outlined big text (shared with the naruto sub-themes)."""
    s['fx'].append(('nrt_say',txt,y,c,scale,cx,outline))

def rasengan(d,x,y,r,f,c=CHAKRA):
    """A spinning chakra sphere: glowing ball + rotating spiral streaks."""
    oc,mc=c; x,y,r=int(x),int(y),max(1,int(r))
    d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=oc); d.ellipse([x-r,y-r,x+r,y+r],fill=mc)
    for k in range(3):
        a=f*50+k*120; rk=max(1,int(r*(0.5+0.25*k)))
        d.arc([x-rk,y-rk,x+rk,y+rk],a,a+110,fill=(235,248,255))
    rc=max(1,r//3); d.ellipse([x-rc,y-rc,x+rc,y+rc],fill=(255,255,255))

@fx('nrt_rasengan')
def _fx_rasengan(d,im,e,f):
    _,x,y,r=e; rasengan(d,x,y,r,f)

@fx('nrt_fireball')
def _fx_fireball(d,im,e,f):
    """Katon: Gokakyu — a rolling ball of fire, flame tongues streaming behind it (to the right)."""
    _,x,y,r=e; x,y=int(x),int(y); rr=random.Random(f*5)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([x-r-8,y-r-8,x+r+8,y+r+8],fill=150)
    im.paste((255,150,50),(0,0),g.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    for _ in range(9):
        a=rr.uniform(-1.2,1.2); L=rr.randint(r+4,r+16)
        d.polygon([(x+math.sin(a)*r*0.2,y-math.cos(a)*r*0.8),(x+L,y+math.sin(a)*r),(x+math.sin(a)*r*0.2,y+math.cos(a)*r*0.8)],fill=rr.choice([(240,110,30),(200,50,20)]))
    for rk,c in ((r+2,(200,50,20)),(r,(240,110,30)),(int(r*0.72),(255,190,70)),(int(r*0.4),(255,245,190))):
        jx=rr.randint(-1,1); d.ellipse([x-rk+jx,y-rk,x+rk+jx,y+rk],fill=c)

def poof(s,x,t,y=GROUND):
    """Shadow-clone smoke puff, t = frames since the poof started (0..7)."""
    if 0<=t<8:
        rr=random.Random(int(x)*7+t)
        for j in range(9):
            r=2+t//2+rr.randint(0,2)
            s['fx'].append(('smoke',x+rr.randint(-7,7),y-5-rr.randint(0,10),r,(244,244,248) if j%3 else (196,196,208)))
        if t<2: s['fx'].append(('ring',x,y-8,4+t*4,(255,255,255)))

# ---- close-ups ---------------------------------------------------------------------------------
def closeup_seal(t,f):
    """Primer plano: the cross hand seal, chakra rising — KAGE BUNSHIN NO JUTSU!"""
    im=Image.new('RGB',(W,H),(232,110,36)); d=ImageDraw.Draw(im)
    cx,cy=48,34
    for i in range(20):                                             # a turning burst behind the hands
        a=i*math.tau/20+f*0.03
        d.polygon([(cx,cy),(cx+math.cos(a)*240,cy+math.sin(a)*240),(cx+math.cos(a+0.16)*240,cy+math.sin(a+0.16)*240)],fill=(250,168,58))
    rr=random.Random(f)
    for _ in range(18):                                             # chakra wisps
        x=rr.randint(10,90); y=rr.randint(0,64); d.line([x,y,x+rr.randint(-2,2),y-rr.randint(4,10)],fill=(170,220,255))
    jx=((f%3)-1) if 0.3<=t<0.5 else 0
    # left arm from below, index+middle fingers straight up
    d.polygon([(22,H),(34,40),(58,40),(52,H)],fill=(30,28,40))    # black sleeve
    d.rectangle([34+jx,34,56+jx,52],fill=SKIN,outline=INK); d.line([34+jx,43,56+jx,43],fill=SKIN_D)
    d.rectangle([41+jx,6,50+jx,34],fill=SKIN,outline=INK); d.line([45+jx,8,45+jx,33],fill=SKIN_D)
    # right arm from the right, fingers pointing left across them
    d.polygon([(W//2+10,4),(64,18),(64,40),(W//2+14,40)],fill=(236,130,40))
    d.rectangle([58+jx,16,76+jx,38],fill=SKIN,outline=INK); d.line([62+jx,27,76+jx,27],fill=SKIN_D)
    d.rectangle([28+jx,18,58+jx,27],fill=SKIN,outline=INK); d.line([30+jx,22,57+jx,22],fill=SKIN_D)
    d.rectangle([41+jx,18,50+jx,27],fill=SKIN)                      # the crossing point, left fingers under
    d.line([41+jx,18,41+jx,27],fill=SKIN_D); d.line([50+jx,18,50+jx,27],fill=SKIN_D)
    for nx in (42,46): d.rectangle([nx+jx,7,nx+2+jx,10],fill=(246,196,170))      # fingernails
    for ny in (19,23): d.rectangle([29+jx,ny,32+jx,ny+2],fill=(246,196,170))
    for k in range(3): d.line([36+jx+k*7,36,36+jx+k*7,41],fill=SKIN_D); d.line([60+jx,19+k*6,64+jx,19+k*6],fill=SKIN_D)   # knuckles
    if t>=0.2:
        sj=((f%3)-1) if t<0.3 else 0
        big_text(im,"KAGE",5,(255,236,120),scale=3,cx=140+sj,outline=(90,30,0))
        if t>=0.3: big_text(im,"BUNSHIN",27,(255,255,255),scale=2,cx=140+sj,outline=(90,30,0))
        if t>=0.42: big_text(im,"NO JUTSU!",44,(255,255,255),scale=1,cx=140,outline=(90,30,0))
    if t>0.78:                                                       # the smoke of a hundred clones
        k=(t-0.78)/0.22; rr=random.Random(3)
        for j in range(int(60*k)):
            x=rr.randint(-10,W+10); y=rr.randint(-6,H+6); r=rr.randint(6,16)
            d.ellipse([x-r,y-r,x+r,y+r],fill=(244,244,248) if j%3 else (206,206,216))
    if t<0.07: zoom_lines(d)
    return im

def closeup_frame(t,f):
    """Extreme close-up of Madara's eyes: tomoe spin up and lock into the Eternal Mangekyo."""
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    d.rectangle([0,10,W,54],fill=(232,208,182))
    for y in range(44,55): d.line([0,y,W,y],fill=(214,188,160) if y%2 else (224,198,172))
    rr=random.Random(5)
    for i in range(40):   # hair strands over the forehead and the sides
        x=rr.randint(-10,W+10); L=rr.randint(6,20); d.polygon([(x,8),(x+rr.randint(3,8),8),(x+rr.randint(-4,4),8+L)],fill=(16,14,18))
    for x in list(range(0,22))+list(range(W-22,W)):
        d.line([x,8,x+int(4*math.sin(x*0.7)),58],fill=(16,14,18))
    spin=f*(0.18+0.9*t)
    for cx in (62,123):
        cy=33
        d.ellipse([cx-19,cy-8,cx+19,cy+8],fill=(236,232,226))
        d.arc([cx-20,cy-9,cx+20,cy+9],195,345,fill=(20,16,18),width=3); d.arc([cx-20,cy-9,cx+20,cy+9],20,160,fill=(120,90,80),width=1)
        d.line([cx-18,cy-13,cx+16,cy-10+(4 if cx<W//2 else -4)],fill=(24,18,20),width=2)   # angry brows
        r=8; d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(200,18,32),outline=(90,0,8))
        if t<0.62:
            for k in range(3):
                a=spin+k*2.094; tx,ty=cx+math.cos(a)*5,cy+math.sin(a)*5
                d.ellipse([tx-1.6,ty-1.6,tx+1.6,ty+1.6],fill=(10,6,8))
                d.arc([tx-3,ty-3,tx+3,ty+3],math.degrees(a)+90,math.degrees(a)+170,fill=(10,6,8),width=1)
            d.ellipse([cx-2,cy-2,cx+2,cy+2],fill=(10,6,8))
        else:
            for k in range(3):   # Eternal Mangekyo pinwheel
                a=spin*0.3+k*2.094
                d.polygon([(cx,cy),(cx+math.cos(a)*7.5,cy+math.sin(a)*7.5),(cx+math.cos(a+0.9)*5,cy+math.sin(a+0.9)*5)],fill=(10,6,8))
            d.ellipse([cx-3,cy-3,cx+3,cy+3],outline=(10,6,8)); d.ellipse([cx-1,cy-1,cx+1,cy+1],fill=(10,6,8))
        d.rectangle([cx-4,cy-5,cx-3,cy-4],fill=(255,255,255))
    sc=1.0+0.18*ease(t)   # slow push-in
    cw,ch=int(W/sc),int(H/sc); x0,y0=(W-cw)//2,(H-ch)//2
    im=im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.NEAREST); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,5],fill=(0,0,0)); d.rectangle([0,58,W,H],fill=(0,0,0))   # letterbox
    if t>=0.62: text(d,"SHARINGAN",W//2-18,59,(255,60,70))
    if t<0.1: zoom_lines(d)
    if t>0.9: im=fade_to(im,(200,0,20),0.5*(t-0.9)/0.1)
    return im

def naru_face(d,ox=0,sage=0.0,eye=(90,170,255)):
    """Claude-as-Naruto's face for close-ups (x ox..ox+56): blond spikes, headband, whisker marks.
    sage 0..1 paints the orange Sage Mode pigment in; at 1 the eyes turn into toad eyes."""
    for k in range(7): d.polygon([(ox+k*9-4,14),(ox+k*9+6,14),(ox+k*9+2-(k%2)*3,-2)],fill=(250,210,60))
    d.rectangle([ox,20,ox+54,H],fill=SKIN); d.rectangle([ox+48,20,ox+54,H],fill=SKIN_D)
    d.rectangle([ox,13,ox+56,21],fill=(44,44,96)); d.rectangle([ox+12,14,ox+38,20],fill=(186,186,206),outline=(110,110,126))
    d.arc([ox+21,15,ox+29,20],20,340,fill=(110,110,126))
    for ex in (ox+16,ox+38):
        if sage>0:
            p=int(2+3*sage); d.ellipse([ex-4-p,25-p,ex+4+p,39+p//2],fill=(214,90,30)); d.ellipse([ex-3-p//2,26-p//2,ex+3+p//2,39],fill=(236,120,44))
        if sage>=1:
            d.rectangle([ex-4,28,ex+4,38],fill=(24,14,12)); d.rectangle([ex-3,29,ex+3,37],fill=(250,206,60))
            d.rectangle([ex-3,32,ex+3,33],fill=(24,14,12)); d.point((ex-2,29),fill=(255,255,255))
        else:
            d.rectangle([ex-3,28,ex+3,38],fill=(24,14,12)); d.rectangle([ex-1,30,ex+2,35],fill=eye)
            d.point((ex,30),fill=(255,255,255))
    d.line([ox+10,26,ox+21,28],fill=(24,14,12)); d.line([ox+33,28,ox+44,26],fill=(24,14,12))
    for k in range(3): d.line([ox+2,42+k*3,ox+10,43+k*3],fill=(120,50,36)); d.line([ox+44,43+k*3,ox+52,42+k*3],fill=(120,50,36))
    d.line([ox+22,54,ox+34,53],fill=(90,30,20))

def closeup_rasengan(t,f):
    """Primer plano: Claude's face lit blue, the Rasengan swelling in his palm — RASENGAN!"""
    im=Image.new('RGB',(W,H),(16,26,56)); d=ImageDraw.Draw(im)
    bx=104; r=int(3+17*ease(t/0.6)); by=50-r
    for i in range(14):                                             # wind lines spiralling in
        a=i*0.45+f*0.35; L=r+14+(i%4)*8
        d.arc([bx-L,by-L*0.6,bx+L,by+L*0.6],math.degrees(a),math.degrees(a)+40,fill=(60,96,160))
    naru_face(d)
    # the palm, fingers curled round the sphere
    d.polygon([(bx-10,H),(bx-8,52),(bx+12,52),(bx+18,H)],fill=(236,130,40))
    d.ellipse([bx-12,46,bx+12,58],fill=SKIN,outline=INK)
    for k in range(4): d.rectangle([bx-11+k*6,42,bx-8+k*6,50],fill=SKIN,outline=INK)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([bx-r-8,by-r-8,bx+r+8,by+r+8],fill=160)
    im.paste((120,190,255),(0,0),g.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    rasengan(d,bx,by,r,f)
    for k in range(2): d.ellipse([bx-r-3-k*3,by-r//3-1-k,bx+r+3+k*3,by+r//3+1+k],outline=(200,232,255))
    if t>=0.55:
        jj=(f%3)-1 if t<0.65 else 0
        big_text(im,"RASEN",12,(210,238,255),scale=2,cx=158+jj,outline=(20,40,110))
        big_text(im,"GAN!",30,(255,255,255),scale=2,cx=158+jj,outline=(20,40,110))
    if t<0.06: zoom_lines(d,(170,220,255))
    if t>0.88: im=fade_to(im,(190,228,255),(t-0.88)/0.12*0.8)
    return im

# ---- the clip ----------------------------------------------------------------------------------
CLONE_X=[12,20,44,52,62,72,82,92]
def clip_shadowclone(f):
    s=scene(f,THEME); s['under'].append(('nrt_clouds',))
    cl=actor(NARU[guard_pose(f)],CX); md=actor(MADARA['idle'],EX,flip=True)
    clones=[]
    # 1) the stand-off: leaves blow down the street
    if 8<=f<40:
        for i in range(10):
            x=(i*37+(f-8)*5)%W; y=12+(i*13)%40+int(3*math.sin(f*0.3+i))
            s['fx'].append(('nrt_leaf',x,y,(96,170,70) if i%2 else (150,200,80)))
    if 14<=f<32: callout(s,"DATTEBAYO!"); cl['spr']=NARU['armsup'] if f<22 else cl['spr']
    if 22<=f<36: md['aura']=(MADARA_AURA,1+(f%2))
    if 30<=f<36: cl['spr']=NARU['charge']
    # 2) close-up: the hand seal
    if 36<=f<64: s['image']=closeup_seal((f-36)/28,f); return s
    # 3) eight clones pop into the street...
    if 64<=f<120:
        for i,x0 in enumerate(CLONE_X):
            t0=64+(i%4)*2
            if f<t0+8: poof(s,x0,f-t0)
            if f<t0+2: continue
            h0=80+i*4                                               # 4) ...and rush Madara in turn
            if f<h0: clones.append(actor(NARU[guard_pose(f+i*3)],x0,flip=False)); continue
            k=f-h0
            if k<6:
                y=GROUND-(int(14*math.sin(math.pi*k/6)) if i%2 else 0)
                clones.append(actor(NARU['dash'] if i%2==0 else NARU['armsup'],lerp(x0,136,k/6),y=y))
            elif k==6: md['spr']=MADARA['attack']; s['fx'].append(('spark',140,GROUND-9,6)); s['shake']=rshake()
            poof(s,136,k-6)
            if 6<=k<9: md['spr']=MADARA['attack']; s['fx'].append(('gunbai',140,GROUND-12))
        if f<80: callout(s,"KAGE BUNSHIN NO JUTSU!")
    if 110<=f<120: callout(s,"IS THAT ALL?",c=(220,150,255))
    # 5) close-up: the Sharingan
    if 120<=f<156: s['image']=closeup_frame((f-120)/36,f); return s
    # 6) Katon: Gokakyu — Claude leaps the fireball
    if 156<=f<196:
        md['spr']=MADARA['attack'] if f<180 else MADARA['idle']
        if f<184: shout(s,"KATON!",(255,170,70),outline=(110,20,0))
        if 158<=f<184:
            x=lerp(136,-30,(f-158)/24); s['fx'].append(('nrt_fireball',x,GROUND-13,12))
            for j in range(3):
                fx_=x+18+j*14
                if fx_<136: s['under'].append(('fire',fx_,GROUND,max(1,4-j-(f-158)//10)))
            s['shake']=rshake() if f%2 else (0,0)
        if 162<=f<184:
            t=(f-162)/22; cl.update(y=GROUND-int(34*math.sin(math.pi*t)),spr=NARU['guard2'] if t<0.5 else NARU['dash'])
        if 182<=f<196:
            rr=random.Random(f//2)
            for j in range(int(8*(196-f)/14)): s['fx'].append(('smoke',rr.randint(0,130),GROUND-rr.randint(0,10),rr.randint(1,3),(120,110,104)))
    if 190<=f<196: cl['spr']=NARU['charge']
    # 7) close-up: the Rasengan
    if 196<=f<236: s['image']=closeup_rasengan((f-196)/40,f); return s
    # 8) Claude and a clone drive it in
    if 236<=f<250:
        t=(f-236)/14; cl.update(x=ez(CX,134,t),spr=NARU['dash'])
        s['fx'].append(('nrt_rasengan',cl['x']+9,GROUND-7,5))
        if f<246: clones.append(actor(NARU['dash'],cl['x']-10,y=GROUND-2))
        poof(s,cl['x']-10,f-246)
        poof(s,44,f-236)
        md['spr']=MADARA['attack'] if f>=244 else MADARA['idle']
    # 9) impact: Madara blasted down the street
    if 250<=f<272:
        k=f-250; cl.update(x=134,spr=NARU['punch'])
        md.update(spr=MADARA['hurt'],x=ez(EX,215,k/12),y=GROUND-int(6*math.sin(math.pi*min(1,k/12))))
        for j in range(3): s['fx'].append(('circle',142,GROUND-8,2+k*3+j*4,(150,210,255) if j%2 else (90,160,255)))
        if k<8: s['fx'].append(('nrt_rasengan',143,GROUND-8,8-k//2))
        if k==0: s['flash']=1.0; s['fc']=(142,GROUND-8); s['flashc']=(170,220,255)
        if k<10: s['shake']=rshake(2)
        if 4<=k<14: s['fx']+= [('dust',md['x']-8-random.randint(0,20),GROUND-random.randint(0,4)) for _ in range(3)]
        shout(s,"RASENGAN!",(210,238,255),outline=(20,40,110),y=4)
    # 10) Claude hops home; the dust settles
    if 272<=f<292:
        t=(f-272)/20; cl.update(x=ez(134,CX,t),y=GROUND-int(14*math.sin(math.pi*t)),spr=NARU['guard'])
    if 262<=f<300: md['vis']=False
    if 272<=f<296:
        rr=random.Random(f//3)
        for j in range(int(8*(296-f)/24)): s['fx'].append(('smoke',170+rr.randint(-10,14),GROUND-rr.randint(0,14),rr.randint(2,4),(214,190,150)))
    # 11) Madara walks back up the street
    if 300<=f<326:
        t=(f-300)/26; md.update(vis=True,x=ez(200,EX,t),spr=MADARA['hurt'] if t<0.6 else MADARA['idle'],y=GROUND-((f//3)%2 if t<1 else 0))
    if md['vis']: s['under'].append(('nrt_gunbai_back',md['x'],md['y']))
    s['actors']=clones+[cl,md]
    return s

CLIPS = [clip('shadowclone', N_, clip_shadowclone)]
