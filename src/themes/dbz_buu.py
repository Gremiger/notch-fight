"""Dragon Ball sub-theme "dbz-buu": Claude vs Kid Buu on the Supreme Kai's world — grassy plains,
huge boulders and a pink-purple sky. Buu cackles, steams and headbutts Claude across the field;
Codex flies in and the two do the fusion dance — FU-SION-HA! Close-up of the fingers touching, the
flash, and CLODEX (spiky hair, Potara earrings, a blue gi) is born. Clodex takes Buu apart and kicks
him into the sky; close-up of Kid Buu's grin as he raises a planet-destroying ball. Clodex goes blue,
FINAL KAMEHAMEHA pushes the ball back into him. The fusion wears off, Codex flies home, Buu pulls
his blobs back together — back to the standoff."""
from engine import *

THEME = 'dbz-buu'
N_ = 360
CX, EX = 30, 152                                                    # the loop keyframe positions

# ---- local glyphs: a wider M and W (the 3x5 font's read as H) ------------------------------------
_GLYPH = {'+':(3,"000010111010000"),'M':(5,"10001"+"11011"+"10101"+"10001"+"10001"), 'W':(5,"10001"+"10001"+"10101"+"11011"+"10001")}

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

@fx('buu_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,cx=W//2,outline=None):
    s['fx'].append(('buu_say',txt,y,c,scale,cx,outline))

# ---- Kid Buu: pink, antenna, white pants, black boots; arms up for the planet ball ---------------
BUU=poses(S([
"........nn......","......nnn.......","....nnnnnn......","...nnnnnnnn.....","...nnKnnnKn.....",
"...nnKKnKKn.....","...nnnnnnnn.....","....nnKKKn......",".....nnnn.......","...nnnnnnnn.....",
"..nnnnnnnnnn....","..nn.nnnnn.nn...","..nn.nnnnn.nn...","..nn.kkykk.nn...",".....WWWWWW.....",
"....WWWWWWWW....","....WWW..WWW....","....WWW..WWW....",".....WW..WW.....","....kkk..kkk....",]),10,'nn',4)
BUU['up']=S([
"........nn......","......nnn.......","nn..nnnnnn..nn..","nn.nnnnnnnn.nn..","nn.nnKnnnKn.nn..",
"nn.nnKKnKKn.nn..","nn.nnnnnnnn.nn..",".nn.nnKKKn.nn...","..nn.nnnn.nn....","...nnnnnnnn.....",
"...nnnnnnnn.....",".....nnnnn......",".....nnnnn......",".....kkykk......",".....WWWWWW.....",
"....WWWWWWWW....","....WWW..WWW....","....WWW..WWW....",".....WW..WW.....","....kkk..kkk....",])
BUU_KI=((255,170,220),(230,60,160))
BUU_AURA=(255,140,200)

# ---- Codex, alive: blue eyes instead of the Edo Tensei glow. Body variants for the dance ----------
CODEX_BODY={
 'idle':LOGO_BODY,
 'up':["d...ddd...d","dd.ddddd.dd",".ddddddddd.","....ddd....","...dd.dd...","...dd.dd...","..ddd.ddd.."],
 'point':["....ddd....","dddddddd...","....ddd.dd.","....ddd....","...dd.dd...","...dd.dd...","..ddd.ddd.."],
}
CODEX={k:S([r.replace('y','E') for r in ICONS['CODEX']]+b) for k,b in CODEX_BODY.items()}
CODEX_AURA=((120,170,255),1)

# ---- Claude: Goku's spiky hair. Clodex: spiky dark hair with Codex-white tips, Potara earrings and
# a blue gi over the orange; for the finish the hair goes blue -----------------------------------
BASE=variant(lambda s: overlay(s,["..k..k.k.....",".kkk.kkkkk...","kkkkkkkkkkk.."],-2,0,bangs="..kk.k.kk"))
def _clodex(x,y,t,l,r,c):
    if c=='.' and y==t+3 and x==l-1: return 'Y'                     # the Potara earring
    if c=='O' and t+5<=y<=t+7 and (x<=l+2 or x>=r-1): return 'L'    # blue gi over the orange
    if c=='O' and y==t+7: return 'L'
    return None
CLODEX=variant(lambda s: overlay(recolor_rows(s,_clodex),["..H..H.H.H...",".kkH.kkkkH...","kkkkkkkkkkkH."],-2,0,
                                 bangs="..kk.k.kk"))
CLODEX_BLUE={'k':(70,170,255),'H':(200,236,255)}
AURA_F=(255,240,200)                                                # the fused aura
AURA_B=(120,200,255)                                                # blue form
KI=((255,236,200),(255,160,90))
KI_B=((200,240,255),(70,170,255))

# ---- background: the Supreme Kai's world --------------------------------------------------------
HOR=44
def _world(d):
    for y in range(HOR):                                            # purple sky melting into pink
        k=y/(HOR-1); d.line([0,y,W,y],fill=(int(84+156*k),int(52+104*k),int(128+70*k)))
    d.ellipse([140,6,154,20],fill=(255,226,236)); d.ellipse([142,8,152,18],fill=(255,244,248))   # a pale sun
    d.polygon([(0,40),(20,34),(44,37),(66,31),(92,36),(116,32),(142,37),(166,33),(185,36),(185,44),(0,44)],fill=(186,138,186))
    for cx,w,top in ((10,26,36),(70,34,38),(128,30,37),(176,24,38)): # rolling green hills
        d.ellipse([cx-w,top,cx+w,top+18],fill=(94,150,96))
    rock,shade,lite=(164,138,126),(118,96,98),(200,176,158)
    def boulder(x0,y0,x1,y1):
        d.ellipse([x0,y0,x1,y1],fill=rock); d.chord([x0,y0,x1,y1],300,120,fill=shade)
        d.arc([x0+2,y0+1,x1-2,y1-2],200,260,fill=lite)
    def pillar(x,top,w,cap):                                        # the Kai world's capped rock spires
        d.rectangle([x-w,top+cap//2,x+w,HOR+2],fill=rock); d.rectangle([x+w//2,top+cap//2,x+w,HOR+2],fill=shade)
        d.ellipse([x-w-cap//2,top,x+w+cap//2,top+cap],fill=rock); d.chord([x-w-cap//2,top,x+w+cap//2,top+cap],0,180,fill=shade)
        d.line([x-w-cap//2+2,top+2,x-1,top+1],fill=lite)
    pillar(58,14,3,8); pillar(104,22,2,6); pillar(164,10,4,10)
    boulder(-8,20,30,50); boulder(18,34,40,50); boulder(120,28,150,50); boulder(144,36,160,50); boulder(176,30,200,52)
    for y in range(HOR,H):                                          # the grass plain
        k=(y-HOR)/(H-HOR); d.line([0,y,W,y],fill=(int(128-30*k),int(190-40*k),int(96-26*k)))
    rr=random.Random(5151)
    for _ in range(70):                                             # tufts, a few pink flowers
        x=rr.randint(0,W-1); y=rr.randint(HOR+1,H-1)
        if rr.random()<0.1: d.point((x,y),fill=(255,190,220))
        else: d.line([x,y,x+rr.choice([-1,0,1]),y-1-(y>52)],fill=rr.choice([(80,140,64),(160,214,110)]))
    d.line([0,HOR,W,HOR],fill=(150,200,110))
register_bg(THEME, lambda v: (v+60,v+120,v+40), decor=_world)

# ---- effects ------------------------------------------------------------------------------------
CLOUDS=[(0,6,1.0),(64,13,0.7),(124,3,0.85),(186,10,0.6)]            # (x, y, size) — a 225px loop
@fx('buu_clouds')
def _fx_clouds(d,im,e,f):
    """Pink-lit clouds drifting left; one lap per clip, so the loop is seamless."""
    o=f*225//N_
    for x0,y,k in CLOUDS:
        x=(x0-o)%225-20; w=int(22*k)
        for dx,dy,r in ((0,3,4),(6,1,5),(13,2,4),(18,4,3)):
            rr_=max(2,int(r*k)); cx=x+dx*k
            d.ellipse([cx-rr_,y+dy-rr_,cx+rr_,y+dy+rr_//2+1],fill=(255,222,240))
        d.line([x-3,y+5,x+w,y+5],fill=(222,160,206))

@fx('buu_steam')
def _fx_steam(d,im,e,f):
    """Kid Buu venting steam from the holes in his head: x,y (head top)."""
    _,x,y=e
    for j in range(3):
        ph=(f+j*3)%9; r=1+ph//4
        for sx in (-5,5):
            d.ellipse([x+sx-r+(sx//5)*ph//2,y-ph-r,x+sx+r+(sx//5)*ph//2,y-ph+r],fill=(255,255,255) if ph<5 else (236,226,240))

@fx('buu_speed')
def _fx_speed(d,im,e,f):
    """Horizontal speed streaks across the frame."""
    rr=random.Random(f*7)
    for _ in range(8):
        y=rr.randint(10,GROUND-2); x=rr.randint(0,W-20); d.line([x,y,x+rr.randint(10,24),y],fill=(255,255,255))

@fx('buu_zip')
def _fx_zip(d,im,e,f):
    """Instant movement: the flicker lines left behind."""
    _,x,y=e; rr=random.Random(f*3+int(x))
    for _ in range(4):
        yy=y+rr.randint(-10,2); xx=x+rr.randint(-6,6); d.line([xx-5,yy,xx+5,yy],fill=(255,255,255))
        d.line([xx-3,yy+1,xx+3,yy+1],fill=(255,210,160))

@fx('buu_ball')
def _fx_ball(d,im,e,f):
    """Kid Buu's planet-destroying ball: a magenta sun, glowing, with a dark churning core ring."""
    _,x,y,r=e; x,y,r=int(x),int(y),int(r)
    glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([x-r-7,y-r-7,x+r+7,y+r+7],fill=130)
    im.paste((255,110,190),(0,0),glow.filter(ImageFilter.GaussianBlur(3))); d=ImageDraw.Draw(im)
    d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=(170,30,120)); d.ellipse([x-r,y-r,x+r,y+r],fill=(236,80,170))
    if r>4:
        d.arc([x-r+2,y-r+2,x+r-2,y+r-2],(f*40)%360,(f*40)%360+200,fill=(150,20,100))
        d.ellipse([x-r+3,y-r+3,x+r//3,y+r//3],fill=(255,150,214))
    d.ellipse([x-r//3,y-r//2,x,y-r//6],fill=(255,236,248))
    asterisk(d,x,y,r+4,(255,160,220),f)

@fx('buu_kiball')
def _fx_kiball(d,im,e,f):
    """A ki ball in the hands: x,y,r,(outer,mid), with a spiky corona."""
    _,x,y,r,(oc,mc)=e; ball(d,int(x),int(y),int(r),oc,mc,f); asterisk(d,int(x),int(y),int(r)+3,oc,f)

@fx('buu_clash')
def _fx_clash(d,im,e,f):
    """Where the beam meets the ball: a white-hot knot throwing sparks."""
    _,x,y=e; x,y=int(x),int(y); r=5+(f%3); rr=random.Random(f)
    d.ellipse([x-r-2,y-r-2,x+r+2,y+r+2],fill=(220,240,255)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255))
    for _ in range(7):
        a=rr.random()*6.28; L=rr.randint(r+2,r+12); d.point((int(x+math.cos(a)*L),int(y+math.sin(a)*L*0.7)),fill=(255,220,240))

@fx('buu_splat')
def _fx_splat(d,im,e,f):
    """A pink gob knocked off Buu."""
    _,x,y,r=e; d.ellipse([x-r,y-r,x+r,y+r],fill=(240,120,170)); d.point((x-r//2,y-r//2),fill=(255,200,226))

def blobs(s,cx,feet,t,seed,back=False):
    """Buu's bits: pink blobs fly apart; with back=True they pull back into one body (t=16 → whole)."""
    rr=random.Random(seed); k=max(0,16-t) if back else t
    for j in range(18):
        vx=rr.uniform(-2.4,2.4); vy=rr.uniform(-2.2,0.3); r=rr.randint(1,3)
        s['fx'].append(('smoke',cx+vx*k,min(feet-9+vy*k+0.09*k*k,GROUND-1),r,(240,120,170) if j%3 else (196,64,136)))

# ---- close-up: the fusion dance -----------------------------------------------------------------
def _arm(d,x0,x1,y,sleeve,skin,edge,right):
    """A straight arm from the screen edge to a pointing index finger (right=True: points right)."""
    s=1 if right else -1; hx=x1-s*14                                # hand starts 14 px before the tip
    d.rectangle([min(x0,hx),y-7,max(x0,hx),y+7],fill=sleeve); d.line([min(x0,hx),y+7,max(x0,hx),y+7],fill=edge)
    d.line([min(x0,hx),y-7,max(x0,hx),y-7],fill=edge)
    d.rectangle([min(hx,hx+s*10),y-6,max(hx,hx+s*10),y+6],fill=skin,outline=edge)     # the fist
    for k in (-2,2): d.line([hx+s*8,y+k,hx+s*10,y+k],fill=edge)
    d.rectangle([min(hx+s*10,x1),y-6,max(hx+s*10,x1),y-3],fill=skin,outline=edge)   # the index finger

def closeup_fusion(t,f):
    """Primer plano: the two index fingers meet — FU-SION-HA! — a flash, and CLODEX grins."""
    rr=random.Random(f)
    if t<0.5:
        im=Image.new('RGB',(W,H),(60,30,90)); d=ImageDraw.Draw(im)
        for i in range(24):                                         # radial rays from the contact
            a=i*0.2618+f*0.02; c=(110,60,150) if i%2 else (84,44,120)
            d.polygon([(92,40),(92+math.cos(a)*200,40+math.sin(a)*120),(92+math.cos(a+0.13)*200,40+math.sin(a+0.13)*120)],fill=c)
        gap=int(lerp(30,0,t/0.3))
        _arm(d,-4,92-gap,40,(217,119,87),(236,150,112),(90,40,26),True)             # Claude: orange, bare
        _arm(d,W+4,92+gap,40,(70,70,86),(110,110,126),(20,20,28),False)             # Codex: grey sleeve
        if gap==0:
            k=int((f%3)+4+t*12); spark(d,92,35,k,(255,240,200))
            d.ellipse([88,31,96,39],fill=(255,255,255))
        word="FU" if t<0.14 else ("FU-SION" if t<0.28 else "FU-SION-HA!")
        jx=(f%3)-1 if t>=0.28 else 0
        say(im,word,6,(255,236,120),scale=2,cx=92+jx,outline=(120,40,110))
        if t<0.05: zoom_lines(d,(255,220,240))
        if t>=0.4: im=fade_to(im,(255,255,255),(t-0.4)/0.1)
        return im
    im=Image.new('RGB',(W,H),(250,236,190)); d=ImageDraw.Draw(im)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([6,-24,122,84],fill=160)
    im.paste((255,250,236),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    for _ in range(50):                                             # the fused aura, white-gold flames
        x=rr.randint(8,124); h=rr.randint(8,34); y=rr.randint(20,66)
        d.line([x,y,x+rr.randint(-2,2),y-h],fill=(255,220,120) if rr.random()<0.6 else (255,255,255))
    sw=f%2
    for x0,x1,tx,ty,tip in ((36,52,20,4,1),(46,62,40,-6,1),(56,76,64,-8,0),(70,90,92,-6,1),(84,100,112,6,0),(92,102,120,22,1)):
        d.polygon([(x0,30),(x1,30),(tx+sw,ty)],fill=(30,28,40),outline=(90,90,120))
        if tip: d.polygon([(tx+sw,ty),(tx+sw+(x0-tx)//4,ty+(30-ty)//4),(tx+sw+(x1-tx)//4,ty+(30-ty)//4)],fill=(242,242,250))
    d.rectangle([36,22,102,30],fill=(30,28,40))
    d.rectangle([42,30,98,64],fill=(217,119,87)); d.rectangle([42,30,48,64],fill=(176,92,66))
    d.polygon([(54,29),(66,29),(62,44)],fill=(30,28,40))            # the single Vegito bang
    for ex in (38,102):                                             # the Potara earrings
        d.line([ex,40,ex,44],fill=(200,150,30)); d.ellipse([ex-3,44,ex+3,50],fill=(255,214,60),outline=(170,110,20))
        d.point((ex,47),fill=(100,200,120))
    for ex in (62,82):                                              # confident eyes, a raised brow
        d.rectangle([ex-2,40,ex+3,51],fill=(24,14,12)); d.rectangle([ex,42,ex+1,44],fill=(255,255,255))
    d.line([56,37,66,39],fill=(24,14,12)); d.line([78,37,88,35],fill=(24,14,12))
    d.line([66,58,78,58],fill=(90,40,26)); d.line([78,58,82,55],fill=(90,40,26))       # the smirk
    d.rectangle([42,60,98,64],fill=(60,90,220)); d.polygon([(62,60),(70,64),(78,60)],fill=(217,119,87))   # blue gi collar
    jj=(f%3)-1 if t<0.62 else 0
    say(im,"CLODEX!",14,(255,255,255),scale=3,cx=148+jj,outline=(200,120,40))
    say(im,"CLAUDE + CODEX",40,(120,70,30),cx=148)
    if t<0.56: im=fade_to(im,(255,255,255),1-(t-0.5)/0.06); d=ImageDraw.Draw(im); zoom_lines(d,(255,220,140))
    if t>0.92: im=fade_to(im,(255,255,255),(t-0.92)/0.08*0.6)
    return im

# ---- close-up: Kid Buu's grin -------------------------------------------------------------------
def closeup_buu(t,f):
    """Primer plano: Kid Buu's face, steam jetting out, eyes narrowed, the huge jagged grin."""
    im=Image.new('RGB',(W,H),(50,14,46)); d=ImageDraw.Draw(im)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([60,-60,200,20],fill=int(200*ease(t/0.6)))
    im.paste((255,90,180),(0,0),g.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)   # the ball's glow above
    rr=random.Random(f)
    for _ in range(26):
        x=rr.randint(10,130); y=rr.randint(20,64); d.line([x,y,x+rr.randint(-2,2),y-rr.randint(6,26)],fill=(200,70,150) if rr.random()<0.7 else (255,150,210))
    jx=((f%2)*2-1) if t>0.3 else 0
    d.ellipse([28+jx,8,112+jx,110],fill=(240,120,170)); d.ellipse([28+jx,8,54+jx,110],fill=(214,96,150))   # head
    d.polygon([(66+jx,10),(78+jx,-8),(86+jx,-4),(76+jx,12)],fill=(240,120,170))                            # the antenna
    for hx in (44,96):                                              # head holes, steam jetting
        d.ellipse([hx-3+jx,16,hx+3+jx,21],fill=(150,40,100))
        for k in range(4):
            ph=(f*2+k*5)%18; r=2+ph//5
            d.ellipse([hx+jx-r+(hx-70)*ph//40,14-ph-r,hx+jx+r+(hx-70)*ph//40,14-ph+r],fill=(255,255,255) if ph<9 else (230,210,230))
    for ex,s in ((58,1),(84,-1)):                                   # slanted black eyes, red pupils
        d.polygon([(ex-8+jx,30-2*s),(ex+8+jx,30+2*s),(ex+6+jx,36+s),(ex-6+jx,36-s)],fill=(20,8,16))
        d.rectangle([ex-1+jx,31,ex+1+jx,33],fill=(230,40,50))
    d.chord([46+jx,34,98+jx,62],0,180,fill=(20,8,16))               # the grin
    for i in range(9):                                              # jagged teeth, top and bottom
        x=50+i*5+jx; d.polygon([(x,48),(x+4,48),(x+2,52)],fill=(250,246,236))
    for i in range(7):
        x=55+i*5+jx; d.polygon([(x,60),(x+4,60),(x+2,56)],fill=(250,246,236))
    d.line([46+jx,48,98+jx,48],fill=(250,246,236))
    if t>0.25:
        jj=(f%3)-1
        say(im,"HEE HEE",14,(255,190,230),scale=2,cx=152+jj,outline=(110,20,80))
        say(im,"HEE!",30,(255,255,255),scale=2,cx=152-jj,outline=(110,20,80))
    if t<0.06: zoom_lines(d,(255,180,220))
    if t>0.9: im=fade_to(im,(255,140,210),(t-0.9)/0.1*0.6)
    return im

# ---- the clip -----------------------------------------------------------------------------------
def ghost(spr,x,y=GROUND,flip=False,tint=(255,236,200),a=0.35):
    return actor(spr,x,y,flip=flip,alpha=a,tint=tint)

def spin(spr,f): return rotate90(spr,(f//2)%4)

def clip_fusion(f):
    s=scene(f,THEME)
    s['under'].append(('buu_clouds',))
    cl=actor(BASE[guard_pose(f)],CX)
    bu=actor(BUU['idle'],EX,y=GROUND-((f//6)%2),flip=True)
    cx=cd=None; extra=[]
    # 1) KID BUU: he cackles, hops and steams
    if 10<=f<40:
        y=6 if f>=14 else 6-(14-f)*2
        s['fx'].append(('buu_say',"KID BUU",y,(255,200,230),2,W//2,(150,30,100)))
    if 16<=f<40:
        bu['y']=GROUND-int(abs(math.sin((f-16)*0.4))*5); s['fx'].append(('buu_steam',EX,GROUND-21))
        if f>=28: shout(s,"HEE HEE!",(255,160,210),y=22,cx=EX-6)
    # 2) the headbutt: Buu rockets across, Claude goes flying
    if 40<=f<50:
        t=(f-40)/10; bu.update(spr=BUU['attack'],x=ez(EX,48,t),y=GROUND-3)
        extra+=[ghost(BUU['attack'],bu['x']+9,y=GROUND-3,flip=True,tint=(255,170,220)),ghost(BUU['attack'],bu['x']+18,y=GROUND-3,flip=True,tint=(255,170,220),a=0.2)]
        s['fx'].append(('buu_speed',))
    if 50<=f<58:
        bu.update(spr=BUU['attack'],x=48,y=GROUND-3)
        if f==50: s['flash']=0.8; s['fc']=(40,GROUND-8)
        s['fx'].append(('spark',40,GROUND-8,9-(f-50))); s['fx'].append(('ring',40,GROUND-8,(f-50)*5+3,(255,220,240)))
        s['shake']=rshake(2)
    if 50<=f<66:
        t=(f-50)/12; cl.update(x=ez(CX,8,t),y=GROUND-int(10*math.sin(math.pi*min(1,t))))
        cl['spr']=spin(BASE['hurt'],f) if f<60 else BASE['hurt']
        if f>=60:
            for _ in range(2): s['fx'].append(('dust',cl['x']+random.randint(0,8),GROUND-random.randint(0,3)))
    if 66<=f<84: cl.update(spr=BASE['hurt'] if f<72 else BASE[guard_pose(f)],x=ez(8,CX,(f-70)/14))
    if 58<=f<78:
        t=(f-58)/20; bu.update(spr=BUU['idle'],x=ez(48,EX,t),y=GROUND-int(abs(math.sin(t*math.pi*3))*6))
        shout(s,"HEE HEE HEE!",(255,160,210),cx=100)
    # 3) Codex flies in
    if 76<=f<96:
        t=(f-76)/14; cx=actor(CODEX['idle'],ez(-12,72,t),y=int(ez(GROUND-30,GROUND,t)),aura=CODEX_AURA)
        if f<90:
            for j in range(5): s['fx'].append(('mote',cx['x']-8-j*5,cx['y']-9+j,(170,200,255)))
            s['fx'].append(('tracer',cx['x']-30,cx['x']-8,cx['y']-8))
        if f==90:
            for j in range(4): s['fx'].append(('dust',72+random.randint(-8,8),GROUND-random.randint(0,3)))
        shout(s,"CODEX!",(160,200,255),y=4,scale=2,outline=(30,40,100))
    # 4) the dance: FU (apart, arms up) - SION (step in, arms swept) - HA! (the fingers touch)
    steps=[(96,'armsup','up',18,82,"FU"),(108,'charge','point',36,64,"FU SION"),(120,'punch','point',44,56,"FU SION HA!")]
    for i,(t0,cp,xp,clx,cxx,txt) in enumerate(steps):
        if t0<=f<t0+12:
            px,pcx=(CX,72) if i==0 else steps[i-1][3:5]
            t=min(1,(f-t0)/5)
            cl.update(spr=BASE[cp],x=ez(px,clx,t),y=GROUND-(2 if (f-t0)<3 and i==0 else 0))
            cx=actor(CODEX[xp],ez(pcx,cxx,t),aura=CODEX_AURA,flip=(i==0))
            shout(s,txt,(255,236,120),y=4,scale=2,outline=(120,40,110))
            if i==2 and f>=124: s['fx'].append(('spark',50,GROUND-6,1+(f%3)))
    if 96<=f<132: bu.update(spr=BUU['idle']); s['fx'].append(('dmg',"?",EX-1,GROUND-28,(255,255,255)))
    # 5) close-up: FU-SION-HA! and CLODEX
    if 132<=f<172: s['image']=closeup_fusion((f-132)/40,f); return s
    blue=276<=f<338
    CD=CLODEX
    if 172<=f<338:
        cl['vis']=False; cd=actor(CD[guard_pose(f)],50,aura=((AURA_B if blue else AURA_F),1+(f%2)),pal=CLODEX_BLUE if blue else None)
    if 172<=f<186:
        for j in range(2): s['fx'].append(('ring',50,GROUND-8,(f-172)*6+j*6,(255,240,200)))
        if f<176: s['flash']=0.7; s['fc']=(50,GROUND-8)
        bu['spr']=BUU['hurt']; s['fx'].append(('dmg',"!?",EX-3,GROUND-28,(255,255,255)))
    if 180<=f<192:
        s['fx'].append(('buu_steam',EX,GROUND-21)); shout(s,"GRRR!",(255,160,210),cx=EX-10)
    # 6) the beating: blink strikes from both sides, gobs of Buu flying
    if 192<=f<226:
        k=(f-192)//6; ph=(f-192)%6; sx=[134,170,136,168,134,170][k]
        cd.update(spr=CD['punch' if ph<4 else 'dash'],x=sx,flip=sx>EX,vis=ph>0)
        if ph==0: s['fx'].append(('buu_zip',sx,GROUND-4))
        if ph==1:
            hx=EX+(-6 if sx<EX else 6); s['fx'].append(('spark',hx,GROUND-10,7)); s['shake']=rshake(2)
            s['fx'].append(('ring',hx,GROUND-10,6,(255,255,255)))
        if ph<4:
            rr=random.Random(k*17)
            for j in range(3):
                d_=1 if sx<EX else -1
                s['fx'].append(('buu_splat',int(EX+d_*(4+ph*5+j*3)),int(GROUND-14+rr.randint(-6,4)+ph*ph*0.6),1+(j%2)))
        bu.update(spr=BUU['hurt'],y=GROUND,x=EX+(2 if ph<3 else 0)*(1 if sx<EX else -1),flip=True)
        s['fx'].append(('buu_speed',))
    if 192<=f<200: cd['vis']=cd['vis'] and f>=193
    if 226<=f<236:                                                  # the kick into the sky
        cd.update(spr=CD['armsup'],x=146,flip=False)
        t=(f-226)/10; bu.update(spr=BUU['hurt'],x=EX,y=int(GROUND-30*ease(t)))
        if f==226: s['flash']=0.6; s['fc']=(EX,GROUND-12); s['fx'].append(('boom',EX,GROUND-12,4))
        s['shake']=rshake(2) if f<230 else (0,0)
    # 7) close-up: Kid Buu grins, the planet ball rising
    if 236<=f<260: s['image']=closeup_buu((f-236)/24,f); return s
    # 8) the planet ball
    BY=GROUND-14                                                    # Buu hovers, feet here
    if 260<=f<300:
        bu.update(spr=BUU['up'] if f<290 else BUU['attack'],x=EX,y=BY+int(math.sin(f*0.3)),aura=(BUU_AURA,1+(f%2)))
        s['under'].append(('dim',0.4*min(1,(f-260)/10)))
    r_=lambda f: 2+11*ease((f-260)/26)
    if 260<=f<290:
        r=r_(f); s['under'].append(('buu_ball',EX,BY-21-r,r))
        for i in range(12):
            a=i*2.39996; ph=((f*0.05+i*0.13)%1); L=(1-ph)*60
            s['fx'].append(('mote',EX+math.cos(a)*L,BY-21-r+math.sin(a)*L*0.5,(255,170,220)))
        if f>=276 and f%2==0: s['shake']=rshake()
        if f>=270: shout(s,"BYE BYE!",(255,170,220),cx=EX-30,y=46)
        if cd: cd.update(spr=CD['guard'],x=50)
    if 276<=f<282:                                                  # Clodex goes blue
        if f==276: s['flash']=0.9; s['fc']=(50,GROUND-8); s['flashc']=(200,236,255)
        s['fx'].append(('ring',50,GROUND-8,(f-276)*6+4,(200,236,255)))
    if 276<=f<292: shout(s,"SUPER CLODEX BLUE",(200,236,255),y=4)
    # the throw, and the beam that answers it
    ball_x=ball_y=None
    if 290<=f<306:
        t=(f-290)/16; ball_x=lerp(EX,104,ease(t)); ball_y=lerp(BY-34,GROUND-12,t)
    if 306<=f<316: ball_x=104-2*math.sin((f-306)*0.9); ball_y=GROUND-12
    if 316<=f<326: t=(f-316)/10; ball_x=lerp(104,EX,ease(t)); ball_y=lerp(GROUND-12,BY-10,t)
    if 290<=f<326:
        s['under'].append(('dim',0.4)); s['under'].append(('buu_ball',ball_x,ball_y,13))
        if f%2==0: s['fx'].append(('rock',random.randint(10,175),GROUND-random.randint(0,20)))
        s['shake']=rshake(1 if f<306 else 2)
    if 292<=f<326:
        cd.update(spr=CD['charge'],x=50,aura=(AURA_B,2+(f%3==0)))
        shout(s,"FINAL KAMEHAMEHA!",(200,236,255),y=4,outline=(20,60,140))
    if 292<=f<306: s['fx'].append(('buu_kiball',64,GROUND-6,1+(f-292)//3,KI_B))
    if 306<=f<326:
        bx=int(ball_x)-13; s['fx'].append(('beam',62,bx,GROUND-6 if f<316 else int(lerp(GROUND-6,ball_y,(f-316)/10)),KI_B))
        s['fx'].append(('buu_clash',bx,GROUND-6 if f<316 else lerp(GROUND-6,ball_y,(f-316)/10)))
        if f<310: s['flash']=0.5; s['fc']=(90,GROUND-10); s['flashc']=(220,240,255)
    if 316<=f<326: bu.update(spr=BUU['hurt']); shout(s,"NOOO!",(255,170,220),cx=EX,y=16)
    # 9) the ball and the beam swallow Buu
    if 326<=f<338:
        bu['vis']=False; t=(f-326)/12
        s['fx'].append(('boom',EX,BY-10,int(6+50*t)))
        for j in range(2): s['fx'].append(('ring',EX,BY-10,int(10+70*t)+j*8,(255,180,230)))
        s['flash']=1.0 if f<330 else max(0,1-(f-330)/10); s['fc']=(EX,BY-10); s['flashc']=(255,236,248); s['shake']=rshake(2)
        blobs(s,EX,GROUND,int((f-326)*1.1),3)
        if cd: cd.update(spr=CD['guard'],x=50)
    # 10) the fusion wears off, Codex heads home, Buu pulls himself together
    if 338<=f<346:
        for j in range(2): s['fx'].append(('ring',50,GROUND-8,(f-338)*5+j*5,(200,220,255)))
        if f==338: s['flash']=0.6; s['fc']=(50,GROUND-8); s['flashc']=(220,236,255)
        if f<342: bu['vis']=False
    if 338<=f<N_:
        cd=None
        cl.update(spr=BASE['hurt'] if f<342 else BASE[guard_pose(f)],x=ez(46,CX,(f-342)/14))
        if f<356:
            t=(f-342)/14; cx=actor(CODEX['up' if f<346 else 'idle'],ez(58,-14,t),y=int(ez(GROUND,GROUND-30,t)),aura=CODEX_AURA)
        if 340<=f<352: shout(s,"SEE YOU!",(160,200,255),cx=70,y=14)
    if 342<=f<354: bu['vis']=False; blobs(s,EX,GROUND,16-(f-342)*16//12,3)
    if 354<=f<357: bu.update(spr=BUU['hurt'],tint=(255,170,220) if f<355 else None)
    s['actors']=[a for a in extra+[cx,cl,cd,bu] if a]
    return s

CLIPS = [clip('fusion', N_, clip_fusion)]
