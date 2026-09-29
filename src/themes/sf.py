"""Street Fighter II: Claude (Ryu) vs M. Bison, with the arcade HUD. ROUND 1 - FIGHT!, a jump
kick, Bison's Psycho Crusher, HADOUKEN vs a Psycho Ball clash, SHORYUKEN with flames, then the
Super Art: close-up of Claude's face on the lightning panel, SHINKU HADOUKEN, K.O., YOU WIN;
the round resets."""
from engine import *

THEME = 'sf'
N_ = 288

def _ryu(tail):
    """White gi, black belt, red headband whose tails flutter behind (two tail shapes)."""
    def fn(x,y,t,l,r,c):
        if c=='.':
            if y==t+1 and x in (l-1,l-2): return 'r'
            if y==t+2-tail and x==l-3: return 'r'
            if tail and y==t+1 and x==l-4: return 'r'
            return None
        inside=l<=x<=r
        if inside and y==t+1: return 'r'                              # headband
        if inside and y==t+4: return 'O' if x in (l+4,l+5) else 'W'    # gi collar, open chest
        if inside and y==t+7: return 'k'                               # black belt
        if inside and t+5<=y<=t+8: return 'W' if x!=r else 'h'
        if y>=t+7 and c=='o' and not inside: return 'W'                # gi trousers
        if y==t+9 and c=='o': return 'W'
        return None
    return fn
KICK=S([
"...OOOOOOOO......",
"...OOOOOOOO......",
"...OOOOKOOK......",
"...OOOOKOOK......",
"...OOOOOOOO......",
".ooOOOOOOOO.oo...",
"ooOOOOOOOOO..oo..",
"...OOOOOOOO......",
"...oOOOOOOoooooOO",
"..oo.............",
".oo..............",])
RYU=[{k:recolor_rows(v,_ryu(i)) for k,v in dict(CL,kick=KICK).items()} for i in (0,1)]
def ryu(pose,f): return RYU[(f//4)%2][pose]

BISON_IDLE=S([
"......rrrrrr......",
".....rrrWWrrr.....",
"....kkkkkkkkkk....",
"......ssssss......",
"......sWssWs......",
"......ssssss......",
".......ssss.......",
"cc...DDrrrrDD.....",
"ccc.DDrrrrrrDD....",
"cccrrrrrrrrrrrr...",
"cccrr.rrrrrr.rr...",
"cccrr.rrRRrr.rr...",
"ccss..kkYYkk..ss..",
"cc....rrrrrr......",
"cc....rrrrrr......",
"cc....rr..rr......",
".c....rr..rr......",
".c....rr..rr......",
"......kk..kk......",
"......kk..kk......",
"......kk..kk......",
".....kkk..kkk.....",])
BISON=poses(BISON_IDLE,12,'ss',4)
BPAL={'c':(58,12,26)}
CRUSH=rotate90(BISON_IDLE,1,trim=True)  # horizontal, fist-first: the Psycho Crusher
DOWN=rotate90(BISON_IDLE,3,trim=True)  # flat on his back after the K.O.

HADOU=((120,200,255),(40,110,255))
PSYCHO=((210,120,255),(120,40,210))

def _stage(d):
    """Suzaku castle at night: moon, pagoda roof silhouette, lanterns — all very dim."""
    d.ellipse([140,12,152,24],fill=(40,38,54))
    for x,y in ((20,14),(46,24),(70,12),(118,20),(164,30),(10,34)): d.point((x,y),fill=(60,60,90))
    for y0,x0,x1 in ((30,62,122),(40,54,130)):
        d.polygon([(x0,y0+5),(x1,y0+5),(x1-8,y0),(x0+8,y0)],fill=(26,16,30))
        d.rectangle([x0+12,y0+5,x1-12,y0+9],fill=(18,12,22))
    d.rectangle([66,50,118,GROUND],fill=(18,12,22))
    for x in (74,90,106): d.rectangle([x,51,x+3,54],fill=(70,26,20))
register_bg(THEME, lambda v: (v//2+6,v//3+4,v//2+10), decor=_stage)

@fx('sf_hud')
def _fx_hud(d,im,e,f):
    """SF2 arcade HUD: yellow health (red where lost), names, KO emblem, the round timer."""
    _,hl,hr,tm=e
    for x0,hp,name,right in ((3,hl,"CLAUDE",False),(104,hr,"BISON",True)):
        d.rectangle([x0,2,x0+77,7],fill=(190,20,20),outline=(240,240,240))
        w=int(76*max(0,hp))
        if w>0:
            if right: d.rectangle([x0+77-w,3,x0+76,6],fill=(250,210,40))
            else: d.rectangle([x0+1,3,x0+w,6],fill=(250,210,40))
        text(d,name,x0+78-len(name)*4 if right else x0,10,(250,230,120))
    d.rectangle([84,1,100,8],fill=(200,30,20)); text(d,"KO",88,2,(255,240,120),shadow=None)
    FX['big'](d,im,('big',"%02d"%tm,11,(250,210,60),92),f)

@fx('sf_dim')
def _fx_dim(d,im,e,f):
    _,a=e; im.paste(fade_to(im,(0,0,8),a))

@fx('sf_hadou')
def _fx_hadou(d,im,e,f):
    """Energy ball with a flame tail trailing behind it: x,y,r,(outer,mid),dir."""
    _,x,y,r,(oc,mc),dr=e; x,y=int(x),int(y); rr=random.Random(f*7+x)
    for k in range(7):
        tx=x-dr*(r+k*2+rr.randint(0,2)); ty=y+rr.randint(-r+1,r-1); tr=max(1,r-1-k//2)
        d.ellipse([tx-tr,ty-tr,tx+tr,ty+tr],fill=oc if k%2 else mc)
    r2=r+(f%2); d.ellipse([x-r2-1,y-r2-1,x+r2+1,y+r2+1],fill=oc); d.ellipse([x-r2,y-r2,x+r2,y+r2],fill=mc)
    d.ellipse([x-r2//2-1+dr,y-r2//2,x+r2//2+dr,y+r2//2],fill=(255,255,255))

@fx('sf_psycho')
def _fx_psycho(d,im,e,f):
    """Psycho Crusher: a corkscrew of purple flame wrapped round the flying body."""
    _,x,y,L,dr=e; rr=random.Random(f*3)
    for k in range(18):
        u=k/17; xx=x-dr*(u*L-L*0.3); a=f*1.3+u*9
        yy=y+math.sin(a)*7*(1-u*0.4); r=max(1,int(3*(1-u))+rr.randint(0,1))
        c=(255,230,255) if k<3 else (PSYCHO[0] if math.cos(a)>0 else PSYCHO[1])
        d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=c)
    for _ in range(5): d.point((x-dr*rr.randint(0,int(L)),y+rr.randint(-9,9)),fill=(200,140,255))

@fx('sf_shinku')
def _fx_shinku(d,im,e,f):
    """The Shinku Hadouken: a thick blue beam with a big head and spiral rings travelling down it."""
    _,x0,x1,y=e; x0,x1,y=int(x0),int(x1),int(y); wob=f%2
    d.rectangle([x0,y-6-wob,x1,y+6+wob],fill=(30,70,220)); d.rectangle([x0,y-4,x1,y+4],fill=(90,170,255))
    d.rectangle([x0,y-1-wob,x1,y+1],fill=(235,250,255))
    for k in range((x1-x0)//12+1):
        cx=x0+((k*12+f*4)%max(1,x1-x0)); d.ellipse([cx-2,y-8,cx+2,y+8],outline=(170,220,255))
    d.ellipse([x1-9,y-10,x1+9,y+10],fill=(40,110,255)); d.ellipse([x1-6,y-7,x1+6,y+7],fill=(120,200,255))
    d.ellipse([x1-3,y-4,x1+3,y+4],fill=(255,255,255))

@fx('sf_bolt')
def _fx_bolt(d,im,e,f):
    """A jagged lightning streak from (x,y0) down to y1."""
    _,x,y0,y1,c,seed=e; rr=random.Random(seed); px,py=x,y0
    while py<y1:
        nx,ny=px+rr.randint(-5,5),py+rr.randint(3,7); d.line([px,py,nx,ny],fill=c); px,py=nx,ny

@fx('sf_big')
def _fx_sfbig(d,im,e,f):
    """Scaled announcer text with a thick coloured outline (K.O., YOU WIN)."""
    _,txt,y,c,oc,sc=e; big_text(im,txt,y,c,sc,outline=oc)

HP_L=[(78,0.68)]
HP_R=[(50,0.84),(142,0.6),(216,0.45),(222,0.3),(228,0.15),(234,0.0)]

def timer(f):
    if f<36 or f>=262: return 99
    return 99-(min(f,236)-36)//20

def closeup_super(t,f):
    """Primer plano: the Super Art flash. Claude's face on a dark lightning panel, headband
    streaming, eyes flaring blue — SHINKU HADOUKEN."""
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    band=int(ez(0,24,t/0.12))
    d.rectangle([0,32-band,W,32+band],fill=(8,12,40))
    for k in range(10):                                     # speed streaks across the panel
        y=32-band+2+(k*37)%(2*band-3 if band>3 else 1); x=(k*53-f*9)%(W+40)-20
        d.line([x,y,x+14+k%3*6,y],fill=(40,70,160))
    rr=random.Random(f//2)
    if t>0.12 and (f//2)%2:                                 # the lightning in the panel
        for j in range(2): FX['sf_bolt'](d,im,('sf_bolt',rr.randint(110,180),32-band,32+band,(170,210,255),f*5+j),f)
    fx0=int(ez(-80,34,(t-0.06)/0.16))                       # the face slides in from the left
    d.rectangle([fx0,10,fx0+66,54],fill=(217,119,87)); d.rectangle([fx0+60,10,fx0+66,54],fill=(186,98,70))
    d.rectangle([fx0,15,fx0+66,22],fill=(214,36,36)); d.line([fx0,22,fx0+66,22],fill=(140,20,20))
    for i in range(4):                                      # the headband tails, streaming back
        ph=f*0.6+i*0.8; y=17+i*2+int(3*math.sin(ph))
        d.line([fx0-1,17+i,fx0-10-i*6,y],fill=(214,36,36) if i%2 else (170,24,24),width=2)
    glow=ease((t-0.45)/0.2)
    for ex in (fx0+30,fx0+50):                              # the mascot's eyes, big
        d.rectangle([ex-3,27,ex+2,40],fill=(24,14,12))
        l=ex<fx0+40; d.line([ex-6,22 if l else 25,ex+4,25 if l else 22],fill=(120,50,34),width=2)   # knitted brows
        if glow>0:
            c=tuple(int(lerp(24,v,glow)) for v in (140,210,255)); d.rectangle([ex-2,29,ex+1,38],fill=c)
    d.polygon([(fx0,48),(fx0+66,48),(fx0+66,54),(fx0,54)],fill=(236,236,242))    # gi collar
    d.polygon([(fx0+26,48),(fx0+33,54),(fx0+40,48)],fill=(217,119,87))
    if t>0.3:
        k=ease((t-0.3)/0.15); x=int(lerp(W+10,112,k))
        FX['big'](d,im,('big',"SHINKU",16,(250,210,60),x+24),f)
    if t>0.4:
        k=ease((t-0.4)/0.15); x=int(lerp(W+40,114,k))
        FX['big'](d,im,('big',"HADOUKEN",34,(120,200,255),x+32),f)
    if t>0.7:                                              # the ball forming between his hands
        r=int(2+(t-0.7)*14); cx,cy=fx0+86,52
        d.ellipse([cx-r,cy-r//2-1,cx+r,cy+r//2+1],fill=(40,110,255)); d.ellipse([cx-r//2,cy-r//4,cx+r//2,cy+r//4],fill=(220,245,255))
    if t<0.06:
        zoom_lines(d)
    return im

def clip_hadouken(f):
    s=scene(f,THEME)
    cl=actor(ryu(guard_pose(f),f),30); bi=actor(BISON['idle'],150,flip=True,pal=BPAL)
    s['fx'].append(('sf_hud',track(f,HP_L,refill=(260,276)),track(f,HP_R,refill=(260,276)),timer(f)))
    if 12<=f<24: s['fx'].append(('big',"ROUND 1",26,(250,210,60)))
    if 24<=f<36: s['fx'].append(('big',"FIGHT!",26,(255,70,50)))
    # 1) jump kick
    if 36<=f<52:
        t=(f-36)/16; cl.update(spr=ryu('armsup' if t<0.4 else 'kick',f),x=lerp(30,124,t),y=GROUND-int(22*math.sin(math.pi*min(1,t*0.9))))
    if f==50: s['fx'].append(('spark',134,GROUND-14,6)); s['shake']=rshake(2)
    if 50<=f<60: bi.update(spr=BISON['hurt'],x=ez(150,158,(f-50)/6))
    if 60<=f<66: bi['x']=ez(158,150,(f-60)/6)
    if 52<=f<66:
        t=(f-52)/14; cl.update(spr=ryu('guard2',f),x=ez(124,30,t),y=GROUND-int(10*math.sin(math.pi*t)))
    # 2) Psycho Crusher
    if 64<=f<72:
        bi.update(spr=BISON['attack'],aura=(PSYCHO[1],1)); s['fx'].append(('sf_psycho',146,GROUND-12,6,-1))
    if 66<=f<86: callout(s,"PSYCHO CRUSHER!",y=24,c=PSYCHO[0])
    if 72<=f<84:
        x=lerp(150,24,(f-72)/12); bi.update(spr=CRUSH,x=x,y=GROUND-4,aura=(PSYCHO[1],1))
        s['under'].append(('sf_psycho',x-10,GROUND-13,40,-1))
    if f==78: s['fx'].append(('spark',34,GROUND-7,7)); s['shake']=rshake(2); s['flash']=0.3; s['fc']=(34,GROUND-8); s['flashc']=(200,140,255)
    if 78<=f<96: cl.update(spr=ryu('hurt',f),x=ez(30,14,(f-78)/6) if f<88 else ez(14,30,(f-88)/8))
    if 84<=f<98:   # back-flips home
        t=(f-84)/14; bi.update(spr=BISON['hurt'] if t<0.6 else BISON['idle'],x=ez(24,150,t),y=GROUND-int(20*math.sin(math.pi*t)))
    # 3) HADOUKEN vs Psycho Ball
    if 100<=f<122: cl['spr']=ryu('charge',f)
    if 100<=f<106: s['fx'].append(('orbc',46,GROUND-6,1+(f-100)//3,HADOU))
    if 100<=f<120: callout(s,"HADOUKEN!",y=24,c=HADOU[0])
    if 104<=f<112: bi.update(spr=BISON['attack'],aura=(PSYCHO[1],1))
    if 106<=f<118:
        t=(f-106)/12
        s['fx'].append(('sf_hadou',lerp(48,92,t),GROUND-6,4,HADOU,1))
        s['fx'].append(('sf_hadou',lerp(134,94,t),GROUND-6,4,PSYCHO,-1))
    if 118<=f<128:   # the clash
        k=f-118; s['fx'].append(('ring',93,GROUND-6,3+k*3,(200,220,255) if k%2 else (220,160,255)))
        if k<5: s['fx'].append(('spark',93,GROUND-6,6-k))
        for j in range(5): s['fx'].append(('shard',93+random.randint(-k*3,k*3),GROUND-6+random.randint(-k,k),HADOU[0] if j%2 else PSYCHO[0]))
        if k==0: s['shake']=rshake(2); s['flash']=0.3; s['fc']=(93,GROUND-6); s['flashc']=(180,200,255)
    # 4) SHORYUKEN
    if 126<=f<134: cl.update(spr=ryu('dash',f),x=ez(30,124,(f-126)/8))
    if 134<=f<152:
        t=(f-134)/18; cl.update(spr=ryu('armsup',f),x=lerp(124,136,t),y=GROUND-int(30*math.sin(math.pi*min(1,t*1.1))))
        if t<0.7:
            for j in range(3): s['under'].append(('fire',cl['x']-2+j*3,cl['y']+2,3))
        callout(s,"SHORYUKEN!",y=24,c=(255,160,60))
    if f==142: s['fx'].append(('spark',144,GROUND-20,7)); s['shake']=rshake(2)
    if 142<=f<160:
        t=(f-142)/18; bi.update(spr=BISON['hurt'],x=lerp(150,162,t),y=GROUND-int(16*math.sin(math.pi*t)))
    if 160<=f<166: bi.update(spr=BISON['hurt'] if f<163 else BISON['idle'],x=162)
    if 166<=f<176: bi['x']=ez(162,150,(f-166)/10)
    if 152<=f<168: cl.update(spr=ryu('guard2',f),x=ez(136,40,(f-152)/16),y=GROUND-int(6*math.sin(math.pi*(f-152)/16)))
    # 5) Super Art: the stage goes dark, the close-up, then the beam
    if 168<=f<252: s['under'].append(('sf_dim',0.6))
    if 168<=f<174: cl.update(spr=ryu('charge',f),x=40,aura=(HADOU[1],1+f%2))
    if 174<=f<210: s['image']=closeup_super((f-174)/36,f); return s
    if 210<=f<238:
        cl.update(spr=ryu('charge',f),x=40,aura=(HADOU[1],1))
        x1=lerp(54,144,min(1,(f-210)/6)); s['fx'].append(('sf_shinku',54,x1,GROUND-7))
        if f>=214:
            bi.update(spr=BISON['hurt'],x=150+(2 if f%2 else 0),tint=(180,220,255) if f%4<2 else None)
            if (f-214)%6==0: s['fx'].append(('spark',146,GROUND-10+random.randint(-6,6),6)); s['shake']=rshake(2)
    if 234<=f<240: s['flash']=0.4*(1-(f-234)/6); s['fc']=(146,GROUND-10); s['flashc']=(170,210,255)
    # 6) K.O., YOU WIN
    if 238<=f<262:
        t=(f-238)/8; bi.update(spr=BISON['hurt'] if t<1 else DOWN,x=ez(150,164,t),y=GROUND-int(10*math.sin(math.pi*min(1,t))) if t<1 else GROUND,tint=None)
    if 238<=f<252: cl.update(spr=ryu(guard_pose(f),f),x=40)
    if 236<=f<252: s['fx'].append(('sf_big',"K.O.",24,(230,20,20),(255,220,60),3))
    if 252<=f<264:
        cl.update(spr=ryu('armsup',f),x=40,y=GROUND-(2 if (f//4)%2 else 0))
        s['fx'].append(('sf_big',"YOU WIN",22,(250,210,60),(200,30,20),2))
    # 7) the round resets: lights up, Bison back on his feet, Claude to his mark
    if 252<=f<268: s['under'].append(('sf_dim',0.6*(1-(f-252)/16)))
    if 262<=f<268: bi.update(spr=DOWN,x=164,alpha=1-(f-262)/6)
    if 268<=f<N_:
        bi.update(spr=BISON['idle'],x=150,y=GROUND,alpha=min(1,(f-268)/8),tint=None)
    if 264<=f<N_: cl.update(spr=ryu(guard_pose(f),f),x=ez(40,30,(f-264)/12),y=GROUND)
    s['actors']=[cl,bi]
    return s

CLIPS = [clip('hadouken', N_, clip_hadouken)]
