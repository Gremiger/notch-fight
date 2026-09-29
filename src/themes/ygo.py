"""Yu-Gi-Oh!: Claude (Yugi: star-spiked hair, duel disk) vs Kaiba in the Kaiba Corp stadium, on the
holographic duel field. Close-up: IT'S TIME TO D-D-D-DUEL! Claude sets a card face-down; Kaiba
summons BLUE-EYES WHITE DRAGON (hologram fade-in) and White Lightning drops Claude's life points to
5000. Close-up: the Heart of the Cards glows on the deck — close-up: I SUMMON... DARK MAGICIAN! The
dragon attacks again: TRAP CARD, MIRROR FORCE reflects the blast, Blue-Eyes shatters and Kaiba falls
to 2500. DARK MAGIC ATTACK takes him to 0: CLAUDE WINS. The holograms fade, the counters refill."""
from engine import *

THEME = 'ygo'
N_ = 336
CX, KX = 20, 165                                                    # the loop keyframe positions
DMX, BEX, TRAPX = 62, 122, 40                                       # monster zones, Claude's trap zone

# ---- local glyphs: a wider M and W (the 3x5 font's read as H) and an apostrophe --------------------
_GLYPH = {'M':(5,"10001"+"11011"+"10101"+"10001"+"10001"), 'W':(5,"10001"+"10001"+"10101"+"11011"+"10001"),
          "'":(1,"11000")}

def _mask(txt):
    gl=[_GLYPH.get(ch) or (3,''.join(FONT.get(ch,FONT[' '])[j*3:j*3+3] for j in range(5))) for ch in txt]
    m=Image.new('L',(sum(w+1 for w,_ in gl)-1,5),0); md=ImageDraw.Draw(m); x=0
    for w,bits in gl:
        for j,b in enumerate(bits):
            if b=='1': md.point((x+j%w,j//w),fill=255)
        x+=w+1
    return m

def say(im,txt,y,c,scale=1,cx=W//2,outline=None,shadow=(0,0,0),upto=None):
    """Like big_text, with the local glyphs. upto: show only that many characters of txt, laid out
    where the whole line goes (a line typed out / stuttered in place)."""
    m=_mask(txt); x=int(cx-m.width*scale//2)
    if upto is not None: m=m.crop((0,0,_mask(txt[:upto]).width if upto else 0,5))
    if m.width==0: return
    m=m.resize((m.width*scale,m.height*scale),Image.NEAREST)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        if shadow is not None: im.paste(shadow,(x+2,y+2),m)
    elif shadow is not None: im.paste(shadow,(x+1,y+1),m)
    im.paste(c,(x,y),m)

@fx('ygo_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=16,scale=1,cx=W//2,outline=(0,0,0)):
    s['fx'].append(('ygo_say',txt,y,c,scale,cx,outline))

# ---- sprites -----------------------------------------------------------------------------------
YUGI=variant(lambda s: recolor_rows(overlay(s,["K..K..K..K..","MK.MK.MK.MK.","KMKMKMKMKMKK",".KKKKKKKKKK."],-2,0,bangs=".Y.Y..Y."),
    lambda x,y,t,l,r,c: ('D' if (x==l-2 or x==l-1) else 'd' if x==l-3 else None) if (t+4<=y<=t+6 and l-3<=x<=l-1) else None))

KAIBA=poses(S([
".....qqqq.......","....qqqqqq......","....qqssss......","....qssks.......","....qsssss......",".....ssss.......",
"...WWkkkkWW.....","..WWWkkkkWWW....","..WWWkkkkWWW....","..WW.kkkk.WW....","..WW.kkkk.WW....","..Ws.kkkk.sW....",
".WW..kkkk..WW...",".WW..kkkk..WW...","WWv..kkkk..vWW..","Wv...kk.kk...vW.","W....kk.kk.....W",".....kk.kk......",
".....kk.kk......","....kkk.kkk.....",]),7,'Ws',3)
KAIBA['kneel']=S(['.'*16]*5+[r for i,r in enumerate(KAIBA['hurt']) if i not in (13,14,15,16,17)])
DARKMAG=S([
"..........pp....","........ppV.....",".......pVVp.....","......pVVVp.....",".....pVVVVVp....","....pVVVVVVVp...",
".....sssss......",".....sKsKs......",".....sssss..j...","....VVVVVVV.jj..","...VVVVVVVVVjj..","..VVpVVVVVpVsj..",
"..Vs.VVVVV..j...","....VVVVVVV.j...","....VVVVVVV.j...","...VVVVVVVVVj...","...VVpVVVpVVj...","..VVVVVVVVVVV...",
"..pp..ppp..pp...",])
BLUEEYES=S([
"....v.......v...............","...vWv.....vWv..............","..vWWWv...vWWWv.............",".vWWWWWv.vWWWWWv............",
"vWWWWWWWvWWWWWWWv.....WWW...","..vWWWWWWWWWWWWv.....WWWWWE.","....vWWWWWWWWWv.....WWWWWWWW","......vWWWWWWWWWWWWWWWv.vvv.",
".......WWWWWWWWWWWWv..v.v...","......WWWWWWWWWWWv..........",".....WWWWWWWWWWWW...........","....WWWvWWWWWWWWW...........",
"...WWW..WWWWWWWWW...........","..WW....WWW..WWW............",".WW.....WW....WW............","WW.....WWW...WWW............",])
BLUEEYES2=S([''.join(ch*2 for ch in r) for r in BLUEEYES for _ in (0,1)])
BE_PAL={'W':(226,236,255),'v':(120,150,210)}

# ---- background: the Kaiba Corp stadium and the holographic duel field ----------------------------
FIELD_Y=46                                                          # back edge of the duel field
def _stadium(d):
    for y in range(FIELD_Y):                                        # night sky over the dome
        k=y/(FIELD_Y-1); d.line([0,y,W,y],fill=(int(20+30*k),int(10+18*k),int(46+40*k)))
    rr=random.Random(909)
    for tier,(y0,y1,c) in enumerate(((14,24,(40,30,70)),(24,34,(52,40,86)),(34,FIELD_Y,(64,50,100)))):
        d.rectangle([0,y0,W,y1],fill=c); d.line([0,y0,W,y0],fill=(96,84,140))
        for _ in range(90):                                        # the crowd
            x=rr.randint(0,W-1); y=rr.randint(y0+2,y1-1)
            d.point((x,y),fill=rr.choice([(150,120,120),(120,96,90),(170,150,96),(90,120,170),(160,90,120),(30,24,40)]))
    for x in range(0,W,23): d.rectangle([x,14,x+1,FIELD_Y],fill=(30,22,50))   # aisles
    d.rectangle([66,1,118,13],fill=(14,14,24)); d.rectangle([67,2,117,12],fill=(24,40,90))   # the big screen
    d.rectangle([66,13,68,16],fill=(40,40,60)); d.rectangle([116,13,118,16],fill=(40,40,60))
    text(d,"KC",72,5,(236,236,250)); text(d,"DUEL",87,5,(120,200,255)); d.line([70,11,114,11],fill=(60,90,170))
    for x0,x1 in ((0,0),(W,W)):                                     # spotlight rigs
        d.rectangle([x0-3 if x0 else x0,0,x0+2 if not x0 else x0,4],fill=(200,200,210))
    # the holographic field in perspective
    d.polygon([(10,FIELD_Y),(175,FIELD_Y),(185,GROUND+1),(0,GROUND+1)],fill=(14,24,52))
    for i in range(-8,9):
        d.line([92+i*10,FIELD_Y,92+i*13,GROUND],fill=(30,70,130))
    for y in (49,53): d.line([0,y,W,y],fill=(30,70,130))
    d.line([10,FIELD_Y,175,FIELD_Y],fill=(90,200,255))
    for zx in (DMX,BEX,TRAPX,144):                                  # the card zones
        d.polygon([(zx-7,49),(zx+7,49),(zx+8,55),(zx-8,55)],outline=(80,170,255))
    d.line([92,FIELD_Y,92,GROUND],fill=(90,200,255))                # the centre line
    d.rectangle([0,GROUND+1,W,H],fill=(26,26,40)); d.line([0,GROUND+1,W,GROUND+1],fill=(90,200,255))
    for x in range(4,W,10): d.point((x,GROUND+3),fill=(60,120,200))
register_bg(THEME, lambda v: (v+20,v+60,v+120), decor=_stadium)

# ---- effects -----------------------------------------------------------------------------------
CARD_C={'back':(122,76,40),'normal':(214,168,72),'trap':(186,70,140),'blue':(120,160,230)}
@fx('ygo_card')
def _fx_card(d,im,e,f):
    """A standing card: x,y centre, kind (back/normal/trap/blue), glow colour or None, wk (flip 0..1)."""
    _,x,y,kind,glow,*wk=e; x,y=int(x),int(y); hw=max(0,int(3.5*(wk[0] if wk else 1)+0.5))
    if glow: d.rectangle([x-hw-2,y-7,x+hw+2,y+7],outline=glow)
    d.rectangle([x-hw-1,y-6,x+hw+1,y+6],fill=(20,14,10))
    if hw==0: return
    d.rectangle([x-hw,y-5,x+hw,y+5],fill=CARD_C[kind])
    if kind=='back': d.ellipse([x-hw+1,y-3,x+hw-1,y+3],fill=(40,24,14)); d.point((x,y),fill=(200,160,80))
    else:
        d.rectangle([x-hw+1,y-3,x+hw-1,y+1],fill=(60,40,110) if kind!='trap' else (120,30,90))
        d.line([x-hw+1,y-4,x+hw-1,y-4],fill=(250,246,230))

@fx('ygo_flat')
def _fx_flat(d,im,e,f):
    """A card lying in its zone (perspective), with the zone lit."""
    _,x,kind=e; x=int(x)
    d.polygon([(x-7,49),(x+7,49),(x+8,55),(x-8,55)],outline=(160,230,255))
    d.polygon([(x-4,50),(x+4,50),(x+5,54),(x-5,54)],fill=CARD_C[kind],outline=(20,14,10))
    if kind=='back': d.line([x-1,52,x+1,52],fill=(40,24,14))

@fx('ygo_pillar')
def _fx_pillar(d,im,e,f):
    """The column of light a summoned monster rises from."""
    _,x,a,c=e; x=int(x); px=im.load()
    for dx in range(-6,7):
        aa=a*(1-abs(dx)/7)
        for y in range(0,GROUND):
            if (y+f)%2==0 or abs(dx)<2: blend(px,x+dx,y,c,aa*(0.3+0.7*y/GROUND))

@fx('ygo_mirror')
def _fx_mirror(d,im,e,f):
    """Mirror Force: a wall of hexagon panes with a moving rainbow sheen."""
    _,x,a=e; px=im.load()
    cols=[(255,120,140),(255,230,120),(120,255,170),(120,190,255),(210,140,255)]
    for y in range(GROUND-32,GROUND+1):
        for dx in range(-3,4):
            c=cols[((y+dx)//3+f)%5]; edge=abs(dx)==3 or (y+dx*2)%6==0
            blend(px,x+dx,y,(255,255,255) if edge else c,a*(0.95 if edge else 0.45))

@fx('ygo_zap')
def _fx_zap(d,im,e,f):
    """White Lightning: a crackling blue-white bolt from x0 to x1."""
    _,x0,x1,y=e; rr=random.Random(f*7)
    d.rectangle([min(x0,x1),y-3,max(x0,x1),y+3],fill=(70,140,255))
    d.rectangle([min(x0,x1),y-2,max(x0,x1),y+2],fill=(170,210,255))
    d.line([min(x0,x1),y,max(x0,x1),y],fill=(255,255,255))
    pts=[(x0,y)]; n=max(1,int(abs(x1-x0)//6))
    for i in range(1,n+1): pts.append((x0+(x1-x0)*i/n,y+rr.randint(-6,6)))
    d.line(pts,fill=(230,240,255))

@fx('ygo_darkmagic')
def _fx_darkmagic(d,im,e,f):
    """Dark Magic Attack: a violet orb with a trail of rings."""
    _,x,y,r=e
    for k in range(4): d.ellipse([x-k*7-r+k,y-r+k,x-k*7+r-k,y+r-k],outline=(170,90,255))
    d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=(60,20,110)); d.ellipse([x-r+1,y-r+1,x+r-1,y+r-1],fill=(150,70,240))
    d.ellipse([x-2,y-2,x+2,y+2],fill=(255,230,255)); asterisk(d,int(x),int(y),r+4,(220,170,255),f)

@fx('ygo_rune')
def _fx_rune(d,im,e,f):
    """A magic circle spinning at the staff."""
    _,x,y,r=e
    d.ellipse([x-r,y-r,x+r,y+r],outline=(200,120,255))
    for k in range(5):
        a=k*1.2566+f*0.2; d.point((int(x+math.cos(a)*r),int(y+math.sin(a)*r)),fill=(255,230,255))
        b=a+2.513; d.line([x+math.cos(a)*r,y+math.sin(a)*r,x+math.cos(b)*r,y+math.sin(b)*r],fill=(150,80,230))

@fx('ygo_lp')
def _fx_lp(d,im,e,f):
    """A life-points counter: label, 4 digits (rolling while ticking), and a bar."""
    _,x,v,c,right,ticking=e; n=int(v/10)*10 if v>0 else 0
    txt="LP %d"%n; w=len(txt)*4
    x0=x-w if right else x
    d.rectangle([x0-2,0,x0+w,9],fill=(10,10,24))
    col=(255,255,255) if ticking and f%2 else c
    text(d,txt,x0,1,col)
    bx0=x0-1; bw=w
    d.rectangle([bx0,7,bx0+bw,8],fill=(40,34,60))
    fr=max(0,v/8000); d.rectangle([bx0+(bw-int(bw*fr) if right else 0),7,bx0+(bw if right else int(bw*fr)),8],fill=c)

@fx('ygo_confetti')
def _fx_confetti(d,im,e,f):
    _,t=e; rr=random.Random(51)
    for _ in range(40):
        x=rr.randint(0,W); v=rr.uniform(0.6,1.4); y=-4+t*80*v-rr.randint(0,30)
        if 0<=y<GROUND: d.rectangle([x+int(3*math.sin(y*0.3)),y,x+int(3*math.sin(y*0.3))+1,y],fill=rr.choice([(255,90,120),(255,220,80),(120,200,255),(160,255,140)]))

# ---- close-ups ---------------------------------------------------------------------------------
def _yugi_face(im,d,f,ox=0,eyes='open',glow=False):
    """Claude's face, zoomed: black star spikes tipped magenta, blond lightning bangs, violet eyes."""
    for x0,x1,tx,ty in ((4,20,-4,6),(12,30,10,-6),(24,42,30,-8),(36,54,50,-8),(48,66,70,-6),(58,74,86,6),(66,78,90,20)):
        d.polygon([(x0+ox,26),(x1+ox,26),(tx+ox,ty)],fill=(24,20,34))
        d.polygon([(tx+ox,ty),((x0+tx)/2+ox+3,(26+ty)/2),((x1+tx)/2+ox-3,(26+ty)/2)],fill=(200,40,140))
    d.rectangle([8+ox,18,74+ox,26],fill=(24,20,34))
    d.rectangle([12+ox,24,70+ox,64],fill=(217,119,87)); d.rectangle([12+ox,24,17+ox,64],fill=(176,92,66))
    for pts in (((18,22),(28,22),(22,36),(26,34),(20,44)),((50,22),(62,22),(58,34),(62,32),(56,42)),((32,22),(40,22),(36,30))):
        d.polygon([(x+ox,y) for x,y in pts],fill=(250,210,60),outline=(200,150,20))
    for ex in (30,48):
        if eyes=='closed': d.line([ex-3+ox,42,ex+3+ox,43],fill=(24,14,12))
        else:
            d.rectangle([ex-3+ox,36,ex+3+ox,48],fill=(24,14,12)); d.rectangle([ex-2+ox,38,ex+2+ox,47],fill=(170,90,230) if not glow else (255,220,90))
            d.rectangle([ex-1+ox,39,ex+ox,41],fill=(255,250,240))
    d.line([23+ox,33,34+ox,35],fill=(40,20,20)); d.line([44+ox,35,55+ox,33],fill=(40,20,20))
    d.line([34+ox,55,46+ox,54],fill=(110,44,32))
    d.rectangle([0,58,86+ox,64],fill=(30,30,60))                    # the jacket collar and the puzzle
    d.polygon([(34+ox,57),(50+ox,57),(42+ox,64)],fill=(240,200,60),outline=(160,110,20))
    d.point((42+ox,59),fill=(120,70,10))

def closeup_duel(t,f):
    """Primer plano: Claude snaps on the duel disk — IT'S TIME TO D-D-D-DUEL!"""
    im=Image.new('RGB',(W,H),(40,16,70)); d=ImageDraw.Draw(im)
    for i in range(14):                                             # a purple sunburst
        a0=i*0.4488+f*0.03; d.polygon([(40,34),(40+math.cos(a0)*240,34+math.sin(a0)*240),(40+math.cos(a0+0.2)*240,34+math.sin(a0+0.2)*240)],fill=(70,30,110))
    jx=((f%3)-1) if 0.3<t<0.8 else 0
    _yugi_face(im,d,f,ox=jx)
    if t>=0.08: say(im,"IT'S TIME TO",8,(255,236,160),scale=1,cx=128,outline=(60,20,90))
    k=t-0.22                                                        # the stutter: D- ... D-D- ... D-D-D-DUEL!
    if k>=0:
        upto=2 if k<0.12 else 4 if k<0.24 else 6 if k<0.34 else 11
        say(im,"D-D-D-DUEL!",22,(255,255,255),scale=2,cx=130+jx,outline=(160,30,60),upto=upto)
        if upto==11: say(im,"DUEL!",40,(255,200,60),scale=2,cx=130,outline=(90,40,0),upto=5 if f%4<2 else 0)
    if t<0.06 or 0.56<t<0.6: zoom_lines(d,(255,220,255))
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

def closeup_heart(t,f):
    """Primer plano: the hand on the deck — the Heart of the Cards glows, the card slides out."""
    lit=t>=0.35
    im=Image.new('RGB',(W,H),(60,40,10) if lit else (12,10,24)); d=ImageDraw.Draw(im)
    cx,cy=92,30
    if lit:
        for i in range(16):                                         # golden rays
            a=i*0.3927+f*0.05; d.polygon([(cx,cy),(cx+math.cos(a)*200,cy+math.sin(a)*120),(cx+math.cos(a+0.12)*200,cy+math.sin(a+0.12)*120)],fill=(120,86,20))
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([cx-40,cy-30,cx+40,cy+30],fill=170)
        im.paste((255,220,110),(0,0),g.filter(ImageFilter.GaussianBlur(8))); d=ImageDraw.Draw(im)
    d.polygon([(20,64),(40,40),(150,40),(170,64)],fill=(150,150,166),outline=(70,70,90))   # the duel disk
    d.line([30,56,160,56],fill=(110,110,126))
    for k in range(6): d.rectangle([70-k,42-k*2,114-k,56-k*2],fill=(122,76,40),outline=(40,24,14))   # the deck
    top=int(ease((t-0.4)/0.4)*22) if lit else 0
    d.rectangle([64,30-top,108,46-top],fill=(122,76,40),outline=(255,236,140) if lit else (40,24,14))
    d.ellipse([74,33-top,98,43-top],fill=(40,24,14)); d.point((86,38-top),fill=(220,180,90))
    hx=44+int(math.sin(f*0.3)*1) if not lit else 44
    d.polygon([(0,40),(hx,24-top),(hx+26,22-top),(hx+30,30-top),(hx+8,38-top),(0,52)],fill=(217,119,87),outline=(168,80,54))  # the hand
    d.line([hx+10,28-top,hx+28,26-top],fill=(168,80,54))
    rr=random.Random(f)
    if lit:
        for _ in range(14): d.point((rr.randint(40,150),rr.randint(0,50)),fill=(255,250,200))
    else: say(im,"...",8,(160,150,200),cx=150)
    if 0.35<=t<0.4: im=fade_to(im,(255,240,190),1-(t-0.35)/0.05); d=ImageDraw.Draw(im); zoom_lines(d,(255,220,120))
    if t>=0.45:
        d.rectangle([0,50,W,H],fill=(20,12,4))
        say(im,"HEART OF THE CARDS",53,(255,226,110),scale=2,cx=W//2,outline=(100,60,0))
    if t>0.9: im=fade_to(im,(255,240,200),(t-0.9)/0.1*0.6)
    return im

def _sprite_img(spr,scale,bg,pal=None):
    tmp=Image.new('RGB',(W,H),bg); w,h=len(spr[0]),len(spr)
    draw(tmp,spr,W//2,h+2,False,pal=pal)
    ox=int(round(W//2-w/2))
    return tmp.crop((ox-1,1,ox+w+1,h+3)).resize(((w+2)*scale,(h+2)*scale),Image.NEAREST)

def closeup_summon(t,f):
    """Primer plano: the drawn card flips round — I SUMMON... DARK MAGICIAN!"""
    im=Image.new('RGB',(W,H),(24,10,44)); d=ImageDraw.Draw(im)
    for i in range(0,W+64,8): d.line([i,0,i-64,H],fill=(34,16,60))
    ph=min(1,t/0.34); wk=abs(math.cos(ph*math.pi))                  # back, edge-on, front
    front=ph>=0.5; cx=92; hw=int(20*wk)
    if front and t>=0.34:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).rectangle([cx-30,-4,cx+30,68],fill=150)
        im.paste((190,120,255),(0,0),g.filter(ImageFilter.GaussianBlur(6))); d=ImageDraw.Draw(im)
    d.rectangle([cx-hw-1,0,cx+hw+1,63],fill=(20,14,10))
    if hw>1:
        if not front:
            d.rectangle([cx-hw,1,cx+hw,62],fill=(122,76,40)); d.ellipse([cx-hw+3,14,cx+hw-3,48],fill=(40,24,14))
            d.ellipse([cx-hw//2,24,cx+hw//2,38],fill=(160,100,40))
        else:
            d.rectangle([cx-hw,1,cx+hw,62],fill=(214,168,72))
            d.rectangle([cx-hw+2,3,cx+hw-2,8],fill=(250,246,230))
            if hw>=18:
                text(d,"DARK",cx-17,3,(20,14,10),shadow=None)
                for k in range(7): d.point((cx+hw-4-k*3,11),fill=(220,60,40)); d.point((cx+hw-4-k*3,10),fill=(250,120,60))
            d.rectangle([cx-hw+2,13,cx+hw-2,52],fill=(60,40,110))
            if hw>=18:
                art=_sprite_img(DARKMAG,2,(60,40,110))
                aw=min(art.width,2*hw-4); im.paste(art.crop(((art.width-aw)//2,0,(art.width-aw)//2+aw,min(art.height,40))),(cx-aw//2,13))
                d=ImageDraw.Draw(im)
            d.rectangle([cx-hw+2,54,cx+hw-2,61],fill=(236,220,180))
            if hw>=18: text(d,"2500",cx-8,55,(20,14,10),shadow=None)
    if t>=0.1: say(im,"I SUMMON",20,(255,236,160),scale=2,cx=35,outline=(60,20,90),upto=None if t>=0.3 else max(0,int((t-0.1)/0.2*8)))
    if t>=0.42:
        jj=(f%3)-1 if t<0.52 else 0
        say(im,"DARK",14,(255,255,255),scale=2,cx=149+jj,outline=(90,30,160))
        say(im,"MAGICIAN",30,(220,180,255),scale=2,cx=149+jj,outline=(90,30,160))
    if 0.34<=t<0.4: zoom_lines(d,(230,200,255))
    if t>0.9: im=fade_to(im,(230,200,255),(t-0.9)/0.1*0.6)
    return im

# ---- the clip ----------------------------------------------------------------------------------
def lp_claude(f):
    v=8000
    if f>=100: v=lerp(8000,5000,(f-100)/18)
    if f>=304: v=lerp(5000,8000,(f-304)/20)
    return v,(100<=f<118 or 304<=f<324)
def lp_kaiba(f):
    v=8000
    if f>=228: v=lerp(8000,2500,(f-228)/16)
    if f>=262: v=lerp(2500,0,(f-262)/14)
    if f>=304: v=lerp(0,8000,(f-304)/20)
    return v,(228<=f<244 or 262<=f<276 or 304<=f<324)

def shatter(s,spr,cx,t,pal,seed):
    """A hologram breaking into pixels that fly apart and fall (t in frames)."""
    rr=random.Random(seed); ox,oy=origin(spr,cx)
    for j,row in enumerate(spr):
        for i,ch in enumerate(row):
            if ch=='.' or rr.random()<0.4: continue
            vx=rr.uniform(-2.2,2.2); vy=rr.uniform(-2.5,0.8)
            x=ox+(len(row)-1-i)+vx*t; y=oy+j+vy*t+0.12*t*t
            if y<GROUND and rr.random()>t/26: s['fx'].append(('shard',x,y,pal.get(ch) or PAL[ch]))

def clip_duel(f):
    s=scene(f,THEME)
    cl=actor(YUGI[guard_pose(f)],CX); kb=actor(KAIBA['idle'],KX,flip=True)
    dm=actor(DARKMAG,DMX,vis=False,holo=1.0); be=actor(BLUEEYES2,BEX,flip=True,vis=False,holo=1.0,pal=BE_PAL)
    # 1) close-up: IT'S TIME TO D-D-D-DUEL!
    if 12<=f<48: s['image']=closeup_duel((f-12)/36,f); return s
    # 2) both draw; Claude sets a card face-down
    if 48<=f<60:
        cl['spr']=YUGI['punch']; kb['spr']=KAIBA['attack']
        up=min(1,(f-48)/5)
        s['fx']+=[('ygo_card',CX+8,GROUND-8-8*up,'back',(255,240,160) if f>=52 else None),('ygo_card',KX-10,GROUND-12-8*up,'back',None)]
    if 56<=f<64:
        t=(f-56)/8; s['fx'].append(('ygo_card',lerp(CX+8,TRAPX,t),lerp(GROUND-16,52,t),'back',None,1-0.7*t))
    if 62<=f<304: s['under'].append(('ygo_flat',TRAPX,'back')) if f<212 else None
    # 3) Kaiba: I SUMMON BLUE-EYES WHITE DRAGON!
    if 60<=f<84: shout(s,"BLUE-EYES WHITE DRAGON!",(170,210,255),outline=(20,40,100))
    if 62<=f<72:
        kb['spr']=KAIBA['attack']; t=(f-62)/8
        s['fx'].append(('ygo_card',lerp(KX-12,BEX,t),lerp(GROUND-24,GROUND-30,t)+(t*t)*20,'normal',(170,220,255)))
    if 70<=f<226: s['under'].append(('ygo_flat',BEX,'normal'))
    if 70<=f<88: s['under'].append(('ygo_pillar',BEX,0.9-(f-70)/20,(170,220,255)))
    if 72<=f<226: be.update(vis=True,holo=min(1,(f-72)/12))
    if 84<=f<92:
        s['shake']=rshake(); s['fx'].append(('ring',BEX-22,GROUND-20,(f-84)*6+4,(200,230,255)))
        shout(s,"GROAAAR!",(220,236,255),y=24,cx=BEX-14)
    # 4) WHITE LIGHTNING straight at Claude
    if 92<=f<104:
        shout(s,"WHITE LIGHTNING!",(170,210,255),outline=(20,40,100))
        hx=BEX-26; tgt=lerp(hx,CX+6,(f-92)/4)
        s['fx'].append(('ygo_zap',tgt,hx,GROUND-19))
        if f>=96:
            cl['spr']=YUGI['hurt']; cl['x']=CX-2; s['shake']=rshake(2); s['fx'].append(('spark',CX+4,GROUND-8,6+(f%2)))
        if f==96: s['flash']=0.6; s['fc']=(CX,GROUND-10); s['flashc']=(200,230,255)
    if 104<=f<118:
        cl['spr']=YUGI['hurt'] if f<110 else cl['spr']
        s['fx'].append(('dmg',"-3000",CX-8,GROUND-26-(f-104)//2,(255,120,90)))
        kb['spr']=KAIBA['attack'] if f%4<2 else KAIBA['idle']; shout(s,"HAHAHA!",(170,210,255),y=24,cx=KX-14)
    # 5) close-ups: the Heart of the Cards, then I SUMMON... DARK MAGICIAN!
    if 118<=f<150: s['image']=closeup_heart((f-118)/32,f); return s
    if 150<=f<180: s['image']=closeup_summon((f-150)/30,f); return s
    # 6) Dark Magician rises
    if 180<=f<188:
        cl['spr']=YUGI['punch']; t=(f-180)/8
        s['fx'].append(('ygo_card',lerp(CX+10,DMX,t),lerp(GROUND-20,GROUND-28,t)+(t*t)*18,'normal',(220,170,255)))
    if 186<=f<304: s['under'].append(('ygo_flat',DMX,'normal'))
    if 186<=f<204: s['under'].append(('ygo_pillar',DMX,0.9-(f-186)/20,(200,140,255)))
    if 188<=f<290: dm.update(vis=True,holo=min(1,(f-188)/12))
    if 290<=f<300: dm.update(vis=f%2==0,holo=1.0)                  # the hologram flickers out
    # 7) Blue-Eyes attacks — TRAP CARD: MIRROR FORCE
    if 204<=f<214: shout(s,"BLUE-EYES, ATTACK!",(170,210,255),outline=(20,40,100)); kb['spr']=KAIBA['attack']
    if 206<=f<216:
        hx=BEX-26; s['fx'].append(('ygo_zap',lerp(hx,86,(f-206)/4),hx,GROUND-19))
    if 212<=f<226:
        up=min(1,(f-212)/4)
        s['fx'].append(('ygo_card',TRAPX,GROUND-6-10*up,'trap',(255,140,200),max(0.05,up)))
        if f<220: shout(s,"TRAP CARD!",(255,150,210),y=26,cx=TRAPX+10,outline=(90,20,60))
    if 214<=f<228:
        s['fx'].append(('ygo_mirror',86,min(0.9,(f-214)/3)*(1 if f<224 else (228-f)/4)))
        if f>=218: shout(s,"MIRROR FORCE!",(255,230,255),outline=(90,20,90))
    if 216<=f<226:                                                  # the blast bounces back
        s['fx'].append(('ygo_zap',86,lerp(86,BEX-10,(f-216)/5),GROUND-16)); s['shake']=rshake()
        if f<218: s['fx'].append(('spark',86,GROUND-12,8))
    if 226<=f<252:                                                  # Blue-Eyes shatters, Kaiba takes it
        be['vis']=False; shatter(s,BLUEEYES2,BEX,f-226,BE_PAL,7)
        if f<230: s['flash']=0.5; s['fc']=(BEX,GROUND-12); s['flashc']=(210,230,255)
        if f<236: s['fx'].append(('spark',KX-2,GROUND-12,6)); kb['spr']=KAIBA['hurt']
    if 228<=f<244: s['fx'].append(('dmg',"-5500",KX-24,GROUND-30-(f-228)//3,(255,120,90)))
    # 8) DARK MAGIC ATTACK
    if 244<=f<262:
        shout(s,"DARK MAGIC ATTACK!",(220,170,255),outline=(60,20,100))
        s['fx'].append(('ygo_rune',DMX+6,GROUND-20,3+min(6,(f-244)//2)))
    if 252<=f<262: s['fx'].append(('ygo_darkmagic',lerp(DMX+8,KX,(f-252)/10),GROUND-14,4))
    if 262<=f<274:
        t=(f-262)/12; s['fx'].append(('boom',KX,GROUND-12,int(4+26*t)))
        kb.update(spr=KAIBA['hurt'],x=ez(KX,172,t)); s['shake']=rshake(2) if f<268 else (0,0)
        if f==262: s['flash']=0.8; s['fc']=(KX,GROUND-12); s['flashc']=(220,170,255)
    if 274<=f<312: kb.update(spr=KAIBA['kneel'],x=172 if f<300 else ez(172,KX,(f-300)/12))
    if 312<=f<320: kb['spr']=KAIBA['hurt']
    # 9) the winner
    if 276<=f<304:
        cl['spr']=YUGI['armsup']
        s['fx'].append(('ygo_confetti',(f-276)/28))
        jj=(f%3)-1 if f<282 else 0
        s['fx'].append(('ygo_say',"CLAUDE WINS!",16,(255,236,120),2,W//2+jj,(120,60,0)))
        if f%4==0: s['fx'].append(('twinkle',CX+random.randint(-8,8),GROUND-14-random.randint(0,8),2))
    vc,tc=lp_claude(f); vk,tk=lp_kaiba(f)
    s['fx']+=[('ygo_lp',2,vc,(255,150,100),False,tc),('ygo_lp',W-2,vk,(120,190,255),True,tk)]
    s['actors']=[dm,be,cl,kb]
    return s

CLIPS = [clip('duel', N_, clip_duel)]
