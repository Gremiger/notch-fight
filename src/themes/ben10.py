"""Ben 10: Claude (Ben Tennyson, brown fringe, white shirt with the black stripe, the Omnitrix on
his wrist) vs Vilgax, the green squid-faced warlord in black-and-red armour, in the desert at night.
Vilgax wants the watch. Close-up: the dial pops up, the alien silhouettes spin, SLAM — IT'S HERO
TIME! Heatblast hurls fireballs; Vilgax swats him, the dial switches him into Four Arms, who
ground-pounds and pummels; XLR8 blurs back and forth landing hits. Then BEEP BEEP: the Omnitrix
times out, Claude is Claude again right under Vilgax's fist and gets sent flying. The watch
recharges, one last slam — Diamondhead — and a line of crystal spikes launches Vilgax across the
desert. The watch clicks back, Vilgax limps back to his spot."""
from engine import *

THEME = 'ben10'
N_ = 336
CX, VX = 30, 150                                                   # the neutral pose: Claude, Vilgax

OMNI = (110,240,60)                                                # the Omnitrix green
OMNI_HI = (200,255,170)
BEEP_RED = (255,50,40)

# ---- local glyphs: an apostrophe and a wider M (the 3x5 font's M reads as H) ------------------
_GLYPH = {"'":(1,"11000"), 'M':(5,"10001"+"11011"+"10101"+"10001"+"10001")}

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

@fx('ben10_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

def shout(s,txt,c,y=2,scale=1,outline=None):
    s['fx'].append(('ben10_say',txt,y,c,scale,W//2,outline))

# ---- Claude as Ben: brown fringe, white shirt with the black stripe, green cargo pants --------
def _ben(x,y,t,l,r,c):
    if c=='.': return None
    inside=l<=x<=r
    if inside and y>=t+6 and c=='O': return 'k' if x==(l+r)//2+1 else 'W'
    if c=='o' and y>=t+8: return 'j'
    return None

# the Omnitrix on the front wrist ('Z' band, 'X' green face), per pose
_WATCH={
 'guard':  [(11,3,'ZX'),(11,4,'ZX')],
 'guard2': [(11,4,'ZX'),(11,5,'ZX')],
 'punch':  [(13,5,'ZX'),(13,6,'ZX')],
 'dash':   [(13,5,'ZX'),(13,6,'ZX')],
 'charge': [(12,5,'ZX'),(12,6,'ZX')],
 'armsup': [(11,1,'XX'),(11,2,'ZZ')],
 'hurt':   [(13,1,'X')],
}
def _mk_ben(name,s):
    s=paint(s,_WATCH[name])
    s=recolor_rows(s,_ben)
    return overlay(s,[".qqqqqqqq..","qqqqqqqqqq."],-1,0,bangs="qqq..qq.")
BEN={k:_mk_ben(k,v) for k,v in CL.items()}
BENPAL={'W':(232,232,236),'k':(30,30,36),'j':(84,122,62),'q':(112,70,40),'X':OMNI,'Z':(26,26,30)}

def _chest(spr,c='X'):
    """The Omnitrix hourglass on an alien's chest (2 px, centre of the body's 7th row)."""
    t,l,r=body_box(spr); g=grid(spr); m=(l+r)//2
    for x in (m,m+1):
        if t+6<len(g) and g[t+6][x]!='.': g[t+6][x]=c
    return ungrid(g)

# ---- the aliens --------------------------------------------------------------------------------
def _heat(x,y,t,l,r,c):
    if c=='.': return None
    if c=='K': return 'F'
    if (x*2+y*3)%7==0 or (x+y*2)%9==0: return 'f'                   # lava cracks in the rock
    return 'R' if c=='O' else 'c'
def _mk_heat(s): return _chest(overlay(recolor_rows(s,_heat),["..F..f...F..",".fFf.FF.fFf.","cfFFfFFfFFfc"],-1,0))
HEAT=variant(_mk_heat)
HEATPAL={'R':(96,34,22),'c':(66,22,16),'f':(255,140,30),'F':(255,236,120),'X':OMNI}

# Four Arms: hand-drawn, bigger than Claude; front arms 'r', back arms 'a' (darker), black-and-white outfit
_FA=S([
".......rrrrrr.........",
"......rrrrrrrr........",
"......rrrrYrrY........",
"......rrrrrrrr........",
"......rrrrYrrY........",
".......rrrrrr.........",
"...aaaakkkkkkrrrr.....",
"..aaaakkkkkkkkrrrr.rr.",
"..aa..kkkkkkkk..rrrrr.",
"..aa..kkkXXkkk...rrrr.",
"..aa..kkkkkkkk........",
"..aaaakkkkkkkkrrrr.rr.",
"..aa..kkkkkkkk..rrrrr.",
"..aa..WWWWWWWW...rrrr.",
"..aa..kkkkkkkk........",
"......kkkk.kkkk.......",
"......kkk...kkk.......",
"......kkk...kkk.......",
".....kkkk...kkkk......",])
_FA_PUNCH=S([
".......rrrrrr..........",
"......rrrrrrrr.........",
"......rrrrYrrY.........",
"......rrrrrrrr.........",
"......rrrrYrrY.........",
".......rrrrrr..........",
"...aaaakkkkkkrrr.......",
"..aaaakkkkkkkkrrrrrrrrr",
"..aa..kkkkkkkk.rrrrrrrr",
"..aa..kkkXXkkk.........",
"..aa..kkkkkkkk.........",
"..aaaakkkkkkkkrrrrrrr..",
"..aa..kkkkkkkk.rrrrrr..",
"..aa..WWWWWWWW.........",
"..aa..kkkkkkkk.........",
"......kkkk.kkkk........",
"......kkk...kkk........",
".....kkk.....kkk.......",
"....kkkk.....kkkk......",])
_FA_UP=S([
"..rr..............rr..",
"..rr..aa.......aa.rr..",
"..rr..aa.rrrrr.aa.rr..",
"..rr..aarrrrrrraa.rr..",
"..rr..aarrrYrrYaa.rr..",
"..rrr.aarrrrrrraa.rrr.",
"...rrraarrrYrrYaarrr..",
"......aarrrrrrraa.....",
"......aakkkkkkkaa.....",
"......kkkkkkkkkk......",
"......kkkkXXkkkk......",
"......kkkkkkkkkk......",
"......kkkkkkkkkk......",
"......WWWWWWWWWW......",
"......kkkkkkkkkk......",
"......kkkk..kkkk......",
"......kkk....kkk......",
".....kkkk....kkkk.....",])
FOUR={'guard':_FA,'guard2':S(['.'*len(_FA[0])]+_FA[:5]+_FA[6:]),'punch':_FA_PUNCH,'dash':_FA_PUNCH,
      'charge':_FA_PUNCH,'armsup':_FA_UP,'hurt':hurt(_FA)}
FOURPAL={'r':(214,58,48),'a':(150,34,30),'W':(230,230,230),'Y':(255,220,60),'k':(28,26,32),'X':OMNI}

def _xlr(x,y,t,l,r,c):
    if c=='.': return None
    inside=l<=x<=r
    if c=='K': return 'E'
    if inside and y in (t+2,t+3): return 'k'                        # the black visor
    if c=='o': return 'k'
    if inside and (x+y)%4==0 and y>=t+5: return 'N'                  # dark stripes
    return 'L'
_TAIL=[(-5,7,'kLL'),(-3,8,'LL')]
def _mk_xlr(s):
    s=recolor_rows(s,_xlr)
    t,l,r=body_box(s)
    s=paint(s,[(l-5,t+6,'kLLL'),(l-3,t+7,'LL')],left=5,right=5)      # the tail, out the back
    return _chest(overlay(s,["......LLL.","..LLLLLLLL"],0,0))          # the crest, swept forward
XLR=variant(_mk_xlr)
XLRPAL={'L':(52,108,226),'N':(24,48,120),'k':(22,22,30),'E':(150,220,255),'X':OMNI}

def _dia(x,y,t,l,r,c):
    if c=='.': return None
    if c=='K': return 'k'
    if (x-y)%5==0: return 'H'                                        # facet highlights
    if (x+y)%6==0: return 'g'
    return 'j' if c=='O' else 'g'
def _mk_dia(s):
    s=recolor_rows(s,_dia)
    return _chest(overlay(s,["....H.....","...HHj....","..HjjjgH..",".jjjjjjjg."],0,0))
DIA=variant(_mk_dia)
DIAPAL={'j':(70,200,150),'g':(30,110,84),'H':(200,255,230),'k':(14,40,34),'X':OMNI}

FORMS={'ben':(BEN,BENPAL),'heat':(HEAT,HEATPAL),'four':(FOUR,FOURPAL),'xlr':(XLR,XLRPAL),'dia':(DIA,DIAPAL)}

# ---- Vilgax ------------------------------------------------------------------------------------
_VG=S([
"........gggg........",
"......gGGGGGg.......",
".....gGGGGGGGg......",
".....GGGGGGGGGg.....",
".....GGGGGGrrGG.....",
".....gGGGGGGGGG.....",
"......gGGGGGGGg.....",
"..RRk.gGgGgGgG.kRR..",
".RRRkkgGgGgGgGkkRRR.",
".RRkkkkg.g.g.gkkkRR.",
".kk.kkkg.g.g.gkk.kk.",
".kk.kkkkrkkrkkkk.kk.",
".GG.kkkkkkkkkkkk.GG.",
".GG.kkRkkkkkkRkk.GG.",
".GG.kkkkkkkkkkkk.GG.",
"..G.DDDDDDDDDDDD.G..",
".....kkkkkkkkkk.....",
".....kkkk..kkkk.....",
".....kkk....kkk.....",
".....kkk....kkk.....",
".....GGk....kGG.....",
".....kkk....kkk.....",
".....RRk....kRR.....",
"....kkkk....kkkk....",])
_VG2=S(_VG[:7]+[r.replace('g.g.g.g','.g.g.g.') if 9<=i<=10 else r for i,r in enumerate(_VG) if i>=7])   # beard sway
def _raise(spr):
    """The front fist raised overhead."""
    g=[list(r) for r in spr]
    for y in range(12,16): g[y][17]=g[y][18]='.'
    top=[list('.'*20) for _ in range(6)]
    for y in range(0,6): top[y][17]=top[y][18]='G'
    for y in (0,1): top[y][16]=top[y][19]='G'
    for y in range(0,11): g[y][17]='k' if y>=7 else 'G'; g[y][18]='k' if y>=7 else 'G'
    return S([''.join(r) for r in top+g])
VG=poses(_VG,12,'G',5)
VG.update(idle2=_VG2,raise_=_raise(_VG))
VG['attack']=paint(VG['attack'],[(24,12,'G'),(24,13,'G')],right=1)
VG['down']=rotate90(VG['hurt'],3,trim=True)
def vg_idle(f): return VG['idle'] if (f//6)%2==0 else VG['idle2']
VGPAL={'G':(92,160,74),'g':(46,100,50),'r':(255,48,40),'R':(176,32,34),'k':(30,28,36),'D':(150,152,168)}

# ---- background: the desert at night -----------------------------------------------------------
def _desert(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(6+10*k),int(8+10*k),int(22+10*k)))
    rr=random.Random(1010)
    for _ in range(34): d.point((rr.randint(0,W-1),rr.randint(0,34)),fill=rr.choice([(80,90,120),(130,140,170),(60,70,100)]))
    d.ellipse([160,5,168,13],fill=(200,210,190)); d.ellipse([163,4,170,12],fill=(14,16,30))   # a crescent moon
    d.polygon([(0,GROUND),(0,40),(10,40),(14,36),(34,36),(38,42),(52,GROUND)],fill=(26,20,34))  # mesas
    d.polygon([(120,GROUND),(132,44),(136,38),(162,38),(166,44),(185,46),(185,GROUND)],fill=(26,20,34))
    d.polygon([(60,GROUND),(72,48),(96,48),(110,GROUND)],fill=(20,16,28))
    for x,h in ((88,10),(104,7)):                                    # saguaros
        d.rectangle([x,GROUND-h,x+1,GROUND],fill=(22,40,28)); d.rectangle([x-2,GROUND-h+3,x-2,GROUND-h+5],fill=(22,40,28))
        d.point((x-1,GROUND-h+5),fill=(22,40,28))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(24,20,24))
register_bg(THEME, lambda v: (v+12,v//2+10,v//3+6), decor=_desert)

# ---- effects -----------------------------------------------------------------------------------
@fx('ben10_burst')
def _fx_burst(d,im,e,f):
    """The transformation: green rings and rays out of the Omnitrix, t frames old."""
    _,x,y,t=e
    if t>=8: return
    for j in range(2):
        r=4+t*3+j*4
        d.ellipse([x-r,y-r//2-2,x+r,y+r//2+2],outline=OMNI if j else OMNI_HI)
    rr=random.Random(77)
    for k in range(8):
        a=k*math.pi/4+rr.random()*0.3; L=6+t*3
        d.line([x+math.cos(a)*L*0.4,y+math.sin(a)*L*0.2,x+math.cos(a)*L,y+math.sin(a)*L*0.5],fill=OMNI)

@fx('ben10_embers')
def _fx_embers(d,im,e,f):
    """Sparks and a flicker rising off Heatblast's head (a 12-frame cycle)."""
    _,x,y=e; rr=random.Random(f%12)
    for i in range(5):
        k=((f*0.09+i*0.21)%1); xx=x+rr.randint(-4,4)+math.sin(k*5+i)*1.5; yy=y-k*12
        d.point((int(xx),int(yy)),fill=(255,236,120) if k<0.4 else (255,120,30))

@fx('ben10_after')
def _fx_after(d,im,e,f):
    """A blue speed afterimage of XLR8."""
    _,spr,x,y,flip,a=e; draw(im,spr,x,y,flip,alpha=a,tint=(70,130,255),f=f)

@fx('ben10_streak')
def _fx_streak(d,im,e,f):
    _,x0,x1,y=e
    for k,c in ((0,(170,220,255)),(-3,(60,110,230)),(3,(60,110,230)),(-6,(40,70,160))):
        d.line([x0,y+k,x1,y+k],fill=c)

@fx('ben10_spike')
def _fx_spike(d,im,e,f):
    """A crystal spike from the ground: x, height, lean."""
    _,x,h,lean=e; x=int(x); h=int(h)
    if h<=0: return
    d.polygon([(x-3,GROUND),(x+3,GROUND),(x+lean,GROUND-h)],fill=(70,200,150),outline=(20,70,56))
    d.line([x,GROUND-1,x+lean,GROUND-h+1],fill=(200,255,230))

@fx('ben10_rock')
def _fx_rock(d,im,e,f):
    _,x,y=e; d.rectangle([x,y,x+1,y+1],fill=(150,110,80))

# ---- close-up: the Omnitrix ---------------------------------------------------------------------
_SIL=[(HEAT['guard'],HEATPAL),(FOUR['guard'],FOURPAL),(XLR['guard'],XLRPAL),(DIA['guard'],DIAPAL)]
def closeup_omnitrix(t,f):
    """The wrist, the dial pops up, the silhouettes spin, the palm slams down: HERO TIME!"""
    im=Image.new('RGB',(W,H),(6,14,8)); d=ImageDraw.Draw(im)
    d.rectangle([0,30,150,58],fill=(217,119,87)); d.rectangle([0,52,150,58],fill=(176,92,66))  # the arm
    d.ellipse([136,24,172,62],fill=(217,119,87)); d.arc([136,24,172,62],200,330,fill=(176,92,66))  # the fist
    for k in range(3): d.line([150+k*6,30,150+k*6,40],fill=(176,92,66))
    d.rectangle([50,26,106,62],fill=(30,30,34))                    # the band
    for x in range(52,106,6): d.line([x,27,x,61],fill=(44,44,50))
    pop=int(4*ease((t-0.12)/0.1))
    cx,cy=78,40-pop
    d.ellipse([cx-21,cy-17,cx+21,cy+19],fill=(150,152,164)); d.ellipse([cx-18,cy-15,cx+18,cy+16],fill=(200,202,212))
    lit=t>=0.12
    d.ellipse([cx-14,cy-13,cx+14,cy+13],fill=(16,20,16))
    spin=0.25<=t<0.6
    if spin:                                                        # the alien silhouettes cycle
        k=int((t-0.25)/0.35*8)%4 if t<0.5 else 0
        spr,pal=_SIL[k]; sil=Image.new('RGB',(W,H)); draw(sil,spr,cx,cy+len(spr)//2,False,tint=OMNI,pal=pal)
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-12,cy-12,cx+12,cy+12],fill=255)
        mask=Image.eval(sil.convert('L'),lambda v:255 if v>0 else 0)
        mm=Image.new('L',(W,H),0); mm.paste(mask,(0,0),m)
        im.paste(sil,(0,0),mm); d=ImageDraw.Draw(im)
    else:                                                           # the hourglass
        c=OMNI if lit else (40,90,30)
        d.polygon([(cx-9,cy-11),(cx+9,cy-11),(cx+1,cy),(cx-1,cy)],fill=c)
        d.polygon([(cx-9,cy+11),(cx+9,cy+11),(cx+1,cy),(cx-1,cy)],fill=c)
    if lit and not spin and t<0.6 and f%4<2:                        # the glow pulse
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([cx-20,cy-18,cx+20,cy+18],fill=70)
        im.paste(OMNI,(0,0),g.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    if 0.12<=t<0.24: say(im,"BEEP",4,OMNI,cx=130)
    if 0.5<=t<0.64:                                                 # the palm comes down
        y=int(lerp(-40,cy-10,ease((t-0.5)/0.12)))
        d.rounded_rectangle([56,y,104,y+30],radius=8,fill=(217,119,87)); d.rectangle([56,y+24,104,y+30],fill=(176,92,66))
    if t>=0.62:
        a=1-ease((t-0.62)/0.3)*0.55
        im=fade_to(im,(170,255,130),a); d=ImageDraw.Draw(im)
        if t<0.7: zoom_lines(d,(255,255,255))
        if t>=0.66:
            jx=(f%3)-1 if t<0.76 else 0
            say(im,"IT'S",8,(255,255,255),scale=2,cx=W//2+jx,outline=(20,90,20))
            say(im,"HERO TIME!",30,(255,255,255),scale=3,cx=W//2+jx,outline=(20,90,20))
    if t<0.06: zoom_lines(d,OMNI)
    return im

# ---- the clip ----------------------------------------------------------------------------------
def morph(s,a,t,frm,to):
    """12-frame Omnitrix switch on actor a: frm blinks green, a green flash, `to` resolves.
    frm/to are (form, pose). Between two aliens Claude flickers through for 2 frames."""
    x,y=a['x'],a['y']
    if t<4: fm,p=frm; tint=OMNI if t%2 else None
    elif t<6: fm,p=('ben','armsup') if frm[0]!='ben' else to; tint=OMNI_HI
    elif t<8: fm,p=to; tint=OMNI
    else: fm,p=to; tint=None
    sp,pal=FORMS[fm]; a.update(spr=sp[p],pal=pal,tint=tint)
    if t>=4: s['fx'].append(('ben10_burst',x,y-9,t-4))
    if 4<=t<8: s['flash']=0.4-(t-4)*0.09; s['fc']=(int(x),y-10); s['flashc']=(170,255,130)
    if 4<=t<6: s['shake']=rshake()

def form(a,fm,p,**kw):
    sp,pal=FORMS[fm]; a.update(spr=sp[p],pal=pal,**kw)

def clip_hero(f):
    s=scene(f,THEME)
    cl=actor(BEN[guard_pose(f)],CX,pal=BENPAL); vg=actor(vg_idle(f),VX,flip=True,pal=VGPAL)
    fronts=[]
    # 1) Vilgax wants the watch; Claude looks at his wrist
    if 12<=f<32:
        shout(s,"THE OMNITRIX IS MINE!",(255,90,70))
        if f<20: vg['spr']=VG['raise_']
    if 24<=f<32: form(cl,'ben','charge')
    # 2) close-up: HERO TIME!
    if 32<=f<64: s['image']=closeup_omnitrix((f-32)/32,f); return s
    # 3) Heatblast: three fireballs
    if 64<=f<76: morph(s,cl,f-60,('ben','charge'),('heat','guard'))   # joins the close-up's flash
    if 72<=f<88: shout(s,"HEATBLAST!",(255,170,60))
    if 76<=f<112:
        k=(f-76)//12; ph=(f-76)%12
        form(cl,'heat','punch' if ph<5 else guard_pose(f))
        if ph<9:
            bx=lerp(48,VX-8,ph/8); r=2+(k==2)
            s['fx'].append(('orbc',bx,GROUND-6-(k==2),r,((200,50,20),(255,170,40))))
            for j in range(3): s['fx'].append(('mote',bx-4-j*3,GROUND-6+random.randint(-1,1),(255,120,30)))
        if ph==8:
            s['fx'].append(('boom',VX-8,GROUND-9,3+k)); s['shake']=rshake(1+(k==2))
        if 8<=ph<12:
            vg.update(spr=VG['hurt'],x=VX+2*k+2)
            s['fx'].append(('dmg',str(10*(k+1)),VX-6,GROUND-30-(ph-8),(255,200,90)))
    if 64<=f<124 and f>=76: s['fx'].append(('ben10_embers',cl['x'],GROUND-14))
    # 4) Vilgax charges and swats Heatblast away
    if 112<=f<120: vg.update(spr=VG['attack'],x=ez(VX+6,52,(f-112)/8)); s['fx'].append(('dust',vg['x']+10,GROUND-1)); form(cl,'heat',guard_pose(f))
    if f==120: s['fx'].append(('spark',36,GROUND-8,7)); s['shake']=rshake(2)
    if 120<=f<126: vg.update(spr=VG['attack'],x=52); form(cl,'heat','hurt',x=ez(CX,16,(f-120)/6))
    if 126<=f<142: vg.update(x=ez(52,VX,(f-126)/16))
    if 124<=f<136: shout(s,"PATHETIC!",(255,90,70))
    # 5) Four Arms: the leap and the ground pound, then the four-fisted barrage
    if 126<=f<138: cl['x']=16; morph(s,cl,f-126,('heat','hurt'),('four','guard'))
    if 136<=f<152: shout(s,"FOUR ARMS!",(255,110,90))
    if 138<=f<148:
        t=(f-138)/10; form(cl,'four','armsup',x=lerp(16,122,t),y=GROUND-int(24*math.sin(math.pi*t)))
    if f==148:
        s['shake']=rshake(3); s['flash']=0.35; s['fc']=(122,GROUND-2); s['flashc']=(255,230,190)
    if 148<=f<160:
        t=f-148
        for j in range(2): s['fx'].append(('ring',122,GROUND,4+t*4+j*5,(210,170,120)))
        for j in range(4): s['fx'].append(('ben10_rock',122+(j-1.5)*t*3,GROUND-2-int(8*math.sin(math.pi*t/12))*(1+j%2)))
        vg.update(spr=VG['hurt'],y=GROUND-int(8*math.sin(math.pi*min(1,t/8))))
    if 148<=f<172: form(cl,'four','guard' if f<152 else ('punch' if (f//3)%2 else 'guard'),x=122 if f<152 else 128)
    if 152<=f<172:
        ph=(f-152)%6; vg.update(spr=VG['hurt'],x=VX+(f-152)//4)
        if ph==2: s['fx'].append(('spark',VX-8,GROUND-8-(f//6)%2*6,5)); s['shake']=rshake()
        s['fx'].append(('dmg',str(4*(1+(f-152)//6)),VX-4,GROUND-32,(255,200,120)))
    if 172<=f<180:
        t=(f-172)/8; form(cl,'four','punch',x=128); vg.update(spr=VG['hurt'],x=ez(VX+5,158,t),y=GROUND-int(10*math.sin(math.pi*t)))
        if f==172: s['fx'].append(('spark',VX-6,GROUND-12,7)); s['shake']=rshake(2)
    # 6) XLR8: hits from both sides at blurring speed
    VG8=158
    if 180<=f<192: vg.update(spr=VG['hurt'] if f<184 else vg_idle(f),x=VG8); cl['x']=128; morph(s,cl,f-180,('four','guard'),('xlr','guard'))
    if 190<=f<206: shout(s,"XLR8!",(120,190,255))
    if 192<=f<224:
        k=(f-192)//8; ph=(f-192)%8; side=[1,-1,1,-1][k]
        sx=VG8-side*14; px=VG8+side*14 if k else 128
        vg.update(spr=VG['hurt'],x=VG8+(side if ph<3 else 0))
        if ph<2:
            form(cl,'xlr','dash',x=lerp(px,sx,ph/2),flip=side<0)
            s['fx'].append(('ben10_streak',min(px,sx),max(px,sx),GROUND-6))
            s['fx'].append(('ben10_after',XLR['dash'],px,GROUND,side<0,0.35))
        else: form(cl,'xlr','punch' if ph<5 else 'guard',x=sx,flip=side<0)
        if ph==2: s['fx'].append(('spark',VG8-side*6,GROUND-9,5)); s['shake']=rshake()
        if 2<=ph<6: s['fx'].append(('dmg',str(8+k*3),VG8-4,GROUND-30-ph,(170,220,255)))
    # 7) BEEP BEEP: the Omnitrix times out right under Vilgax
    X7=VG8-14
    if 224<=f<238:
        vg.update(spr=vg_idle(f),x=VG8)
        red=(f//2)%2==0; pal=dict(XLRPAL,X=BEEP_RED if red else OMNI)
        cl.update(spr=XLR['guard'],pal=pal,x=X7,flip=False,tint=(255,120,110) if f>=234 and red else None)
        shout(s,"BEEP BEEP",BEEP_RED)
    if 238<=f<246:
        form(cl,'ben','hurt' if f<240 else 'guard',x=X7)
        if f<242: s['flash']=0.4-(f-238)*0.09; s['fc']=(X7,GROUND-10); s['flashc']=(255,120,100)
        shout(s,"UH OH",(255,255,255))
        vg.update(spr=vg_idle(f),x=VG8)
    if 246<=f<254: form(cl,'ben','hurt',x=X7); vg.update(spr=VG['raise_'],x=VG8)
    if f==254: s['fx'].append(('spark',X7+2,GROUND-10,8)); s['shake']=rshake(3); s['flash']=0.4; s['fc']=(X7,GROUND-10); s['flashc']=(255,255,255)
    if 254<=f<270:
        t=(f-254)/14; form(cl,'ben','hurt',x=ez(X7,20,t),y=GROUND-int(16*math.sin(math.pi*min(1,t))))
        vg.update(spr=VG['attack'] if f<260 else vg_idle(f),x=VG8)
    # 8) Vilgax closes in; the watch recharges; Diamondhead
    if 262<=f<296: vg.update(spr=vg_idle(f),x=ez(VG8,74,(f-262)/24))
    if 270<=f<280:
        form(cl,'ben','armsup',x=20)
        if f<276: shout(s,"BEEP",OMNI)
        if f%2==0: cl['pal']=dict(BENPAL,X=OMNI_HI)
    if 280<=f<292: cl['x']=20; morph(s,cl,f-280,('ben','armsup'),('dia','guard'))
    if 288<=f<304: shout(s,"DIAMONDHEAD!",(140,255,200))
    if 292<=f<300: form(cl,'dia','armsup' if f<296 else 'charge',x=20)
    if 296<=f<312:
        t=f-296
        form(cl,'dia','charge' if t<12 else guard_pose(f),x=20)
        for i,sx in enumerate(range(34,86,7)):
            h=max(0,min(1,(t-i*0.8)/2))*(6+i*1.6)*(1 if t<12 else max(0,1-(t-12)/4))
            s['under'].append(('ben10_spike',sx,h,1+i%2))
        if t>=6:
            u=(t-6)/10; vg.update(spr=VG['hurt'],x=ez(74,160,u),y=GROUND-int(22*math.sin(math.pi*min(1,u))))
            if t<9:
                for j in range(4): s['fx'].append(('shard',74+random.randint(-6,6),GROUND-random.randint(6,20),(200,255,230)))
        if t==6: s['shake']=rshake(2); s['flash']=0.4; s['fc']=(74,GROUND-6); s['flashc']=(200,255,230)
    if 312<=f<320: vg.update(spr=VG['down'],x=160)
    if f==312: s['fx'].append(('dust',152,GROUND-1)); s['fx'].append(('dust',168,GROUND-1)); s['shake']=rshake()
    if 320<=f<324: vg.update(spr=VG['hurt'],x=160)
    if 324<=f<332: vg.update(spr=vg_idle(f),x=ez(160,VX,(f-324)/8))
    # 9) the watch clicks back: Claude
    if 312<=f<318: form(cl,'dia',guard_pose(f),x=20)
    if 318<=f<324:
        t=f-318; form(cl,'ben' if t>=2 else 'dia',guard_pose(f),x=20,tint=OMNI_HI if t<2 else (OMNI if t<4 else None))
        s['fx'].append(('ben10_burst',20,GROUND-9,t))
    if 324<=f<336: form(cl,'ben',guard_pose(f),x=ez(20,CX,(f-324)/8))
    s['actors']=[vg,cl]+fronts
    return s

CLIPS = [clip('hero', N_, clip_hero)]
