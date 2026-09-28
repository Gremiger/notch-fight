# Anime themes for the notch fight. Claude is always the protagonist.
# Each THEME has its own neutral "loop keyframe": every clip of a theme starts
# and ends on it, so clips of the same theme chain seamlessly. Between themes
# the app plays a pre-rendered asterisk-iris transition.
import math, random, os, shutil
from PIL import Image, ImageDraw, ImageFilter
import clips as C
from clips import (W, H, GROUND, CL, CE, PAL, S, draw, spark, lerp, ease, ez, rshake,
                   fxdraw, CL_OR, CE_BL, AUR_C, AUR_E, GOLD, GOLD_AURA, frame, CLIPS as DBZ_CLIPS)

PAL.update({
 'Y':(250,210,60),'M':(200,40,140),'D':(182,182,194),'d':(110,110,126),
 'H':(242,242,250),'h':(186,186,206),'b':(26,26,34),
 'R':(132,30,30),'X':(40,150,95),'Z':(22,22,26),
 'q':(112,72,42),'s':(240,200,160),'W':(236,236,242),'v':(168,170,198),'k':(30,28,40),
 'V':(106,58,178),'p':(64,32,120),'j':(120,200,120),'E':(70,160,255),
 'n':(240,120,170),'L':(60,90,220),'y':(250,220,60),'N':(44,44,96),'r':(220,40,40),
})

# ---------------------------------------------------------------- sprite tools
def grid(spr): return [list(r) for r in spr]
def ungrid(g): return S([''.join(r) for r in g])

def body_box(spr):
    """Top row + column span of Claude's body (first row with >=6 'O')."""
    for y,r in enumerate(spr):
        if r.count('O')>=6:
            xs=[x for x,c in enumerate(r) if c=='O']; return y,min(xs),max(xs)
    return 0,3,10

def overlay(spr, pat, dx, dy_bottom, bangs=None):
    """Paint `pat` so its last row sits just above the body top (padding upward)."""
    top,l,r=body_box(spr); g=grid(spr); w=len(g[0])
    y0=top-len(pat)
    pad=max(0,-y0)
    if pad: g=[['.']*w for _ in range(pad)]+g; top+=pad; y0+=pad
    for j,row in enumerate(pat):
        for i,ch in enumerate(row):
            x=l+dx+i
            if ch!='.' and 0<=x<w: g[y0+j][x]=ch
    if bangs:
        for i,ch in enumerate(bangs):
            x=l+dx+i
            if ch!='.' and 0<=x<w and g[top][x]!='.': g[top][x]=ch
    return ungrid(g)

def recolor_rows(spr, rows_fn):
    g=grid(spr); top,l,r=body_box(spr)
    for y in range(len(g)):
        for x in range(len(g[0])):
            n=rows_fn(x,y,top,l,r,g[y][x])
            if n: g[y][x]=n
    return ungrid(g)

def variant(fn): return {k:fn(v) for k,v in CL.items()}

YUGI=variant(lambda s: recolor_rows(overlay(s,["K..K..K..K..","MK.MK.MK.MK.","KMKMKMKMKMKK",".KKKKKKKKKK."],-2,0,bangs=".Y.Y..Y."),
    lambda x,y,t,l,r,c: ('D' if (x==l-2 or x==l-1) else 'd' if x==l-3 else None) if (t+4<=y<=t+6 and l-3<=x<=l-1) else None))
GOJO=variant(lambda s: recolor_rows(overlay(s,[".H.H.H.H.H..",".HHHHHHHHHH.","..HhHHHhHH.."],-2,0),
    lambda x,y,t,l,r,c: 'b' if (y in (t+2,t+3) and l<=x<=r and c in 'OK') else None))
TANJ=variant(lambda s: recolor_rows(overlay(s,["..RR.RR.R.",".RRRRRRRRR"],-1,0),
    lambda x,y,t,l,r,c: ('X' if (x+y)%2 else 'Z') if (t+5<=y<=t+8 and c in 'Oo' and l<=x<=r) else None))

def attack(spr,row,ext,col):
    g=[r for r in spr]
    for rr in (row,row+1):
        L=max(i for i,c in enumerate(g[rr]) if c!='.')
        g[rr]=g[rr][:L+1]+col*ext
    return S(g)
def hurt(spr):
    h=len(spr); out=[]
    for i,r in enumerate(spr):
        s=round((h-1-i)/(h-1)*2); out.append(r[s:]+'.'*s)
    return S(out)
def poses(idle,row,col,ext=4):
    return {'idle':idle,'attack':attack(idle,row,ext,col),'hurt':hurt(idle)}

KAIBA=poses(S([
".....qqqq.......","....qqqqqq......","....qqssss......","....qssks.......","....qsssss......",".....ssss.......",
"...WWkkkkWW.....","..WWWkkkkWWW....","..WWWkkkkWWW....","..WW.kkkk.WW....","..WW.kkkk.WW....","..Ws.kkkk.sW....",
".WW..kkkk..WW...",".WW..kkkk..WW...","WWv..kkkk..vWW..","Wv...kk.kk...vW.","W....kk.kk.....W",".....kk.kk......",
".....kk.kk......","....kkk.kkk.....",]),7,'Ws',3)
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
AKAZA=poses(S([
".....nnnn.......","....nnnnnn......","...nnPPPPn......","....PLyPyL......","....PPPPPP......",".....PLLP.......",
"...NNPLLPNN.....","..NNNPPPPNNN....","..PLNPLLPNLP....","..PL.PPPP.LP....","..PP.PLLP.PP....","..LP.PPPP.PL....",
".....WWWW.......",".....WWWW.......","....WW..WW......","....WW..WW......","....WW..WW......","....LP..PL......",
"....PP..PP......","...PPP..PPP.....",]),8,'PL',4)
SUKUNA=poses(S([
".....n.n.n......","....nnnnnnn.....","....nPPPPPn.....","....PkrPkr......","....PPrPPr......","....PkPPPk......",
".....PPPP.......","...WWWWWWWW.....","..WWWkWWkWWW....","..WWW.WW.WWW....","..PPW.kk.WPP....","..kP.WWWW.Pk....",
".....WWWW.......",".....kkkk.......","....WWWWWW......","....WWWWWW......","....WW..WW......","....WW..WW......",
"....vv..vv......","...kkk..kkk.....",]),10,'Pk',4)

# ---------------------------------------------------------------- rendering
def make_bg(kind):
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    for x in range(0,W,2):
        a=1-abs(x-W/2)/(W/2); v=int(10+26*a)
        c={'dbz':(v,v,v+4),'ygo':(v+8,v//2,v+18),'kny':(v//2,v,v//2+6),'jjk':(v//2+4,v//2,v+14)}[kind]
        d.point((x,GROUND+1),fill=c)
    if kind=='ygo':
        for x in range(8,W,12): d.point((x,GROUND+3),fill=(40,18,60))
    if kind=='kny':
        d.ellipse([164,3,176,15],fill=(236,228,180)); d.ellipse([167,1,179,13],fill=(0,0,0))
    return im
BGS={k:make_bg(k) for k in ('dbz','ygo','kny','jjk')}

def actor(spr,x,y=GROUND,flip=False,**kw):
    a=dict(spr=spr,x=x,y=y,flip=flip,aura=None,pal=None,vis=True,holo=None); a.update(kw); return a

def scene(f,kind):
    return dict(kind=kind,actors=[],under=[],fx=[],shake=(0,0),flash=0.0,fc=(93,GROUND-10),flashc=(255,250,235))

def draw_holo(im,spr,x,feet,flip,prog,f,alpha=0.85):
    """Hologram: reveal from the feet up, scanline flicker."""
    h=len(spr); cut=int(h*(1-prog))
    full=prog>=1
    rows=[(r if (i>=cut and (full or (i+f)%3)) else '.'*len(r)) for i,r in enumerate(spr)]
    if full and f%9==0: rows=[r if i%2 else '.'*len(r) for i,r in enumerate(rows)]
    draw(im,S(rows),x,feet,flip,alpha=alpha,f=f)
    if 0<prog<1:
        y=int(feet-h+cut); w=len(spr[0])
        ImageDraw.Draw(im).line([x-w//2-1,y,x+w//2+1,y],fill=(200,160,255))

def render(s,f):
    im=make_bg(s['kind']) if s['kind'] not in BGS else BGS[s['kind']].copy(); d=ImageDraw.Draw(im)
    for e in s['under']: fx2(d,im,e,f)
    for a in s['actors']:
        if not a['vis']: continue
        if a['holo'] is not None: draw_holo(im,a['spr'],a['x'],a['y'],a['flip'],a['holo'],f)
        else: draw(im,a['spr'],a['x'],a['y'],a['flip'],aura=a['aura'],f=f,pal=a['pal'],alpha=a.get('alpha',1.0),tint=a.get('tint'))
    for e in s['fx']: fx2(d,im,e,f)
    if s['shake']!=(0,0):
        im2=BGS[s['kind']].copy(); im2.paste(im,s['shake']); im=im2
    if s['flash']>0:
        m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); r=int(20+90*s['flash']); cx,cy=s['fc']
        md.ellipse([cx-r,cy-r//2,cx+r,cy+r//2],fill=int(255*min(1,s['flash'])))
        m=m.filter(ImageFilter.GaussianBlur(8))
        im=Image.composite(Image.new('RGB',(W,H),s['flashc']),im,m)
    return im

def fx2(d,im,e,f):
    k=e[0]
    if k=='katana':
        _,x0,y0,x1,y1,glow=e
        if glow: d.line([x0,y0,x1,y1],fill=glow,width=3)
        d.line([x0,y0,x1,y1],fill=(222,224,238))
        d.line([x0,y0,x0+(x1-x0)*0.18,y0+(y1-y0)*0.18],fill=(40,30,30),width=2)
    elif k=='card':    # card flying/lying: x,y,face(bool),glow
        _,x,y,face,glow=e; x,y=int(x),int(y)
        if glow: d.rectangle([x-4,y-5,x+4,y+5],outline=glow)
        d.rectangle([x-3,y-4,x+3,y+4],fill=(170,70,150) if face else (120,76,40)); d.rectangle([x-2,y-3,x+2,y+3],outline=(236,210,120))
    elif k=='flatcard':
        _,x,c=e; x=int(x); d.rectangle([x-4,GROUND-1,x+4,GROUND],fill=c)
    elif k=='pillar':
        _,x,a,c=e; x=int(x)
        for dx in range(-3,4):
            aa=a*(1-abs(dx)/4)
            for y in range(0,GROUND):
                if (y+f)%2==0: C.blend(im.load(),x+dx,y,c,aa*(y/GROUND))
    elif k=='barrier':
        _,x,a=e
        for y in range(GROUND-28,GROUND+1):
            for dx in (-1,0,1):
                C.blend(im.load(),int(x+dx+math.sin(y*0.5+f)*0.8),y,[(255,120,120),(255,240,120),(120,255,160),(120,180,255),(220,130,255)][(y//3+f)%5],a*(0.9-abs(dx)*0.35))
    elif k=='shard':
        _,x,y,c=e; d.point((int(x),int(y)),fill=c)
    elif k=='lpbar':
        _,x0,frac,c=e
        d.rectangle([x0,1,x0+34,3],fill=(40,30,50)); d.rectangle([x0,1,x0+int(34*frac),3],fill=c)
    elif k=='wave':      # water trail between x0 and x1
        _,x0,x1,yb=e
        for x in range(int(min(x0,x1)),int(max(x0,x1))):
            y=yb+3*math.sin(x*0.35+f*0.7)
            d.point((x,int(y)),fill=(90,170,255)); d.point((x,int(y)-1),fill=(220,240,255)); d.point((x,int(y)+2),fill=(40,100,220))
    elif k=='arc':
        _,x,y,r,a0,a1,c,wd=e; d.arc([x-r,y-r,x+r,y+r],a0,a1,fill=c,width=wd)
    elif k=='firering':
        _,x,y,r=e
        for i in range(14):
            a=i/14*6.283+f*0.6; px=x+math.cos(a)*r; py=y+math.sin(a)*r*0.8
            d.rectangle([px,py,px+1,py+1],fill=(255,120,40) if i%2 else (255,210,70))
    elif k=='ember':
        _,x,y=e; d.point((int(x),int(y)),fill=random.choice([(255,140,40),(255,210,80),(230,70,30)]))
    elif k=='compass':
        _,x,r=e
        for i in range(8):
            a=i/8*6.283; d.line([x,GROUND,x+math.cos(a)*r,GROUND+math.sin(a)*r*0.3],fill=(120,220,255))
        d.ellipse([x-r,GROUND-r*0.3,x+r,GROUND+r*0.3],outline=(80,160,230))
    elif k=='circle':
        _,x,y,r,c=e; d.ellipse([x-r,y-r,x+r,y+r],outline=c)
    elif k=='slash':
        _,x,y,L,c=e; d.line([x,y,x+L,y-L*0.8],fill=c); d.line([x+1,y,x+L+1,y-L*0.8],fill=(255,255,255))
    elif k=='orbc':      # colored orb: x,y,r,(outer,mid)
        _,x,y,r,(oc,mc)=e; r=r+(f%2)
        d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=oc); d.ellipse([x-r,y-r,x+r,y+r],fill=mc); rc=max(1,r//2); d.ellipse([x-rc,y-rc,x+rc,y+rc],fill=(255,255,255))
    elif k=='trail':
        _,x0,x1,y,hh,a=e
        for x in range(int(max(0,x0)),int(min(W,x1))):
            for yy in range(int(y-hh),int(y+hh)+1): C.blend(im.load(),x,yy,(120,50,200),a*(0.4 if abs(yy-y)<hh-1 else 0.9))
    elif k=='petal':
        _,x,y=e; d.point((int(x)%W,int(y)),fill=(200,160,240)); d.point((int(x+1)%W,int(y)),fill=(160,120,210))
    else: fxdraw(d,e,f)

def katana_for(pose,x,y,flip,glow=None):
    s=-1 if flip else 1
    if pose in ('guard','guard2'): return ('katana',x+5*s,y-6,x+11*s,y-16,glow)
    if pose=='hurt': return ('katana',x+4*s,y-8,x-3*s,y-14,glow)
    return ('katana',x+8*s,y-5,x+20*s,y-7,glow)

def guard_pose(f): return 'guard' if (f//6)%2==0 else 'guard2'

# ---------------------------------------------------------------- YU-GI-OH
def clip_duel(f):
    s=scene(f,'ygo'); N=216
    cl=actor(YUGI[guard_pose(f)],24); kb=actor(KAIBA['idle'],160,flip=True)
    dm=actor(DARKMAG,62,vis=False,holo=1.0); be=actor(BLUEEYES,130,flip=True,vis=False,holo=1.0)
    lp_k=1.0
    if 12<=f<24:
        cl['spr']=YUGI['punch']; s['fx'].append(('card',cl['x']+6,GROUND-14-(f-12),False,(255,240,160)))
        if f>=18: s['fx'].append(('twinkle',cl['x']+9,GROUND-19-(f-12),2))
    if 24<=f<36:
        t=(f-24)/12; s['fx'].append(('card',lerp(30,62,t),lerp(GROUND-26,GROUND-3,t),True,None))
    if 34<=f<156: s['under'].append(('flatcard',62,(150,70,200)))
    if 34<=f<48: s['under'].append(('pillar',62,0.9-(f-34)/20,(190,120,255)))
    if 36<=f<150: dm.update(vis=True,holo=min(1,(f-36)/12))
    if 48<=f<60:
        kb['spr']=KAIBA['attack']
        t=(f-48)/10; s['fx'].append(('card',lerp(150,124,min(1,t)),lerp(GROUND-20,GROUND-3,min(1,t)),True,(160,220,255)))
    if 58<=f<108: s['under'].append(('flatcard',124,(90,150,230)))
    if 58<=f<72: s['under'].append(('pillar',124,0.9-(f-58)/20,(170,220,255)))
    if 60<=f<96: be.update(vis=True,holo=min(1,(f-60)/12))
    if 70<=f<76: s['shake']=rshake()
    if 76<=f<96:   # White Lightning
        hx=116; tgt=80 if f>=84 else lerp(hx,74,(f-76)/8)
        s['fx'].append(('beam',tgt,hx,GROUND-13,((200,230,255),(90,160,255))))
    if 82<=f<108:  # Mirror Force: trap flips up, barrier reflects
        s['fx'].append(('card',80,GROUND-5,True,(255,120,160))) if f<88 else None
        s['fx'].append(('barrier',80,min(0.9,(f-82)/4)*(1 if f<100 else (108-f)/8)))
    if 86<=f<98:
        s['fx'].append(('beam',80,lerp(80,118,(f-86)/6),GROUND-15,((255,230,255),(230,140,255))))
        s['shake']=rshake()
    if 96<=f<120:  # Blue-Eyes shatters
        be['vis']=False; rr=random.Random(7); t=f-96
        for j,row in enumerate(BLUEEYES):
            for i,ch in enumerate(row):
                if ch=='.' or rr.random()<0.55: continue
                vx=rr.uniform(-2.2,2.2); vy=rr.uniform(-2.5,0.8)
                x=130+ (len(row)/2-i) + vx*t; y=GROUND-len(BLUEEYES)+j+vy*t+0.12*t*t
                if y<GROUND and rr.random()>t/26: s['fx'].append(('shard',x,y,PAL.get(ch,(255,255,255))))
        if f<100: s['flash']=0.5; s['fc']=(124,GROUND-12); s['flashc']=(210,230,255)
    if 96<=f<176: lp_k=max(0.25,1-(f-96)/24*0.75) if f<130 else max(0,0.25-(f-124)/10*0.25)
    if 96<=f<120: kb['spr']=KAIBA['hurt']
    if 108<=f<132:  # Dark Magic Attack
        if f<118: s['fx'].append(('circle',68,GROUND-18,2+(f-108),(200,120,255)))
        if 116<=f<126: s['fx'].append(('orbc',lerp(70,154,(f-116)/10),GROUND-12,3,((120,60,200),(40,10,70))))
        if f==126: s['fx'].append(('spark',156,GROUND-12,8)); s['flash']=0.6; s['fc']=(156,GROUND-12); s['flashc']=(220,170,255)
        if f>=126: kb.update(spr=KAIBA['hurt'],x=ez(160,168,(f-126)/6)); s['shake']=rshake() if f<130 else (0,0)
    if 132<=f<160: kb['x']=ez(168,160,(f-132)/28); kb['spr']=KAIBA['hurt'] if f<146 else KAIBA['idle']
    if 136<=f<150: dm['holo']=max(0,1-(f-136)/14)
    if 176<=f<200: lp_k=(f-176)/24
    if 176<=f<N: s['fx'].append(('twinkle',162,2,1)) if f<200 and f%4==0 else None
    if f>=200: lp_k=1.0
    s['fx']+=[('lpbar',3,1.0,(232,120,80)),('lpbar',148,lp_k,(90,160,255))]
    s['actors']=[dm,be,cl,kb]
    return s

# ---------------------------------------------------------------- KIMETSU NO YAIBA
def clip_breath(f):
    s=scene(f,'kny'); N=204
    cl=actor(TANJ[guard_pose(f)],28); ak=actor(AKAZA['idle'],150,flip=True)
    glow=None; pose='guard'
    for i in range(8):   # periodic wisteria petals: y advances 128px per clip -> seamless loop
        s['under'].append(('petal',i*23+10*math.sin(f*0.05+i),(i*13+f*128/N)%GROUND))
    if 12<=f<28:
        glow=(70,150,255)
        for i in range(6):
            a=f*0.5+i; s['fx'].append(('mote',cl['x']+math.cos(a)*9,GROUND-6+math.sin(a)*5,(120,190,255)))
        if f%4==0: s['fx'].append(('mote',cl['x']+3,GROUND-9,(230,230,240)))
    if 28<=f<40:
        t=(f-28)/8; cl['x']=ez(28,122,t); pose='dash'; glow=(70,150,255)
        s['under'].append(('wave',28,cl['x'],GROUND-5))
        if f>=36:
            s['fx'].append(('arc',140,GROUND-9,11,200,520,(120,200,255),2)); ak['spr']=AKAZA['hurt']
            s['fx'].append(('spark',138,GROUND-10,5)); s['shake']=rshake()
    if 36<=f<42: ak['x']=ez(150,160,(f-36)/6)
    if 40<=f<48:
        cl['x']=122; ak.update(x=160,spr=AKAZA['idle']); s['under'].append(('compass',160,6+(f-40)*2))
    if 48<=f<60:
        ak['spr']=AKAZA['attack']; t=(f-48)/12; cl.update(x=ez(122,34,t)); pose='hurt'
        for j in range(3): s['fx'].append(('circle',lerp(146,40,t)+j*8,GROUND-9,3+j,(120,220,255)))
        s['fx'].append(('dust',cl['x']+5,GROUND-random.randint(0,3)))
        if f==48: s['shake']=rshake(2); s['flash']=0.4; s['fc']=(146,GROUND-9); s['flashc']=(200,240,255)
    if 60<=f<72: ak['spr']=AKAZA['idle']; ak['x']=ez(160,150,(f-60)/12)
    if 60<=f<76:
        cl['x']=34; pose='charge'; glow=(255,120,40)
        for i in range(3): s['fx'].append(('ember',cl['x']+10+random.randint(0,10),GROUND-6-random.randint(0,10)))
        cl['aura']=((255,150,60),1+(f%2))
    if 76<=f<92:
        t=(f-76)/16; cl['x']=ez(34,128,t); cl['y']=GROUND-int(14*math.sin(math.pi*t))
        cl['flip']=(f//2)%2==1; pose='dash'; glow=(255,120,40)
        s['fx'].append(('firering',cl['x'],cl['y']-6,10))
        for i in range(3): s['fx'].append(('ember',cl['x']-random.randint(4,18),cl['y']-random.randint(0,12)))
    if 88<=f<96:
        s['fx'].append(('arc',146,GROUND-10,13,150,400,(255,140,50),3)); s['fx'].append(('arc',146,GROUND-10,10,160,390,(255,230,120),1))
        ak['spr']=AKAZA['hurt']
        if f==88: s['flash']=0.7; s['fc']=(146,GROUND-10); s['flashc']=(255,190,110); s['shake']=rshake(2)
    if 92<=f<108:
        cl.update(x=128,y=GROUND,flip=False); pose='punch'; glow=(255,120,40) if f<100 else None
        ak.update(spr=AKAZA['hurt'],x=ez(150,170,(f-92)/10))
        for i in range(2): s['fx'].append(('ember',ak['x']+random.randint(-6,6),GROUND-random.randint(0,20)))
    if 108<=f<150:
        ak['x']=ez(170,150,(f-108)/42); ak['spr']=AKAZA['hurt'] if f<124 else AKAZA['idle']
        if f<130:
            for i in range(3): s['fx'].append(('mote',ak['x']+random.randint(-6,6),GROUND-random.randint(0,22),(255,150,200)))
    if 108<=f<124:
        t=(f-108)/16; cl['x']=ez(128,28,t); cl['y']=GROUND-int(8*math.sin(math.pi*t)); pose='guard'
    if pose!='guard': cl['spr']=TANJ[pose]
    s['fx'].append(katana_for(pose,cl['x'],cl['y'],cl['flip'],glow))
    s['actors']=[cl,ak]
    return s

# ---------------------------------------------------------------- JUJUTSU KAISEN
def clip_infinity(f):
    s=scene(f,'jjk')
    cl=actor(GOJO[guard_pose(f)],30); sk=actor(SUKUNA['idle'],150,flip=True)
    if 12<=f<24: sk['spr']=SUKUNA['attack']
    if 16<=f<40:   # Dismantle vs Infinity
        for j in range(3):
            t0=16+j*3
            if f<t0: continue
            x=max(46+j*3,140-9*(f-t0)); y=GROUND-4-j*6
            if f<34: s['fx'].append(('slash',x,y,7,(230,230,255)))
        if f>=24:
            for r in range(3): s['fx'].append(('circle',44,GROUND-10,4+r*4+(f%3),(90,150,255) if r%2 else (170,210,255)))
        if f>=32:
            for i in range(4): s['fx'].append(('mote',46+random.randint(0,8),GROUND-random.randint(2,20),(220,220,255)))
    if 36<=f<60:   # Blue: attraction
        cl['spr']=GOJO['charge']
        s['fx'].append(('orbc',92,GROUND-14,3+(f-36)//8,((120,180,255),(40,90,240))))
        for i in range(10):
            a=i*2.4; ph=((f*0.06+i*0.13)%1); L=(1-ph)*40
            s['fx'].append(('mote',92+math.cos(a)*L,GROUND-14+math.sin(a)*L*0.6,(150,200,255)))
        if f>=44: sk.update(spr=SUKUNA['hurt'],x=ez(150,116,(f-44)/16))
        if f%3==0: s['shake']=rshake()
    if 60<=f<84:   # Red: repulsion
        cl['spr']=GOJO['punch']
        if f<68: s['fx'].append(('orbc',40,GROUND-6,1+(f-60)//3,((255,140,140),(220,30,40))))
        if 68<=f<74: s['fx'].append(('orbc',lerp(40,110,(f-68)/6),GROUND-8,3,((255,140,140),(220,30,40))))
        if f==74: s['flash']=0.8; s['fc']=(112,GROUND-10); s['flashc']=(255,120,120); s['fx'].append(('spark',112,GROUND-10,9))
        if f>=74:
            sk.update(spr=SUKUNA['hurt'],x=ez(116,172,(f-74)/10)); s['fx'].append(('ring',112,GROUND,(f-74)*3,(255,100,100)))
            if f<80: s['shake']=rshake(2)
        else: sk.update(x=116,spr=SUKUNA['hurt'])
    if 84<=f<96: sk.update(x=ez(172,150,(f-84)/12),spr=SUKUNA['idle'])
    if 96<=f<124:  # Hollow Purple forms
        cl['spr']=GOJO['armsup']; t=min(1,(f-96)/16)
        if t<1:
            s['fx'].append(('orbc',lerp(22,34,t),GROUND-24,3,((120,180,255),(40,90,240))))
            s['fx'].append(('orbc',lerp(46,34,t),GROUND-24,3,((255,140,140),(220,30,40))))
        else: s['fx'].append(('orbc',34,GROUND-24,3+(f-112)//3,((200,150,255),(130,50,210))))
        if f>=110: s['shake']=rshake()
    if 124<=f<146:
        cl['spr']=GOJO['charge']; t=(f-124)/18; x=lerp(40,210,t)
        s['under'].append(('trail',40,x,GROUND-10,9,0.8))
        s['fx'].append(('orbc',x,GROUND-10,9,((210,160,255),(120,40,200))))
        if x>=140: sk['vis']=False
        if 132<=f<136: s['flash']=0.9; s['fc']=(150,GROUND-10); s['flashc']=(220,170,255)
        s['shake']=rshake(2)
    if 146<=f<168:
        a=max(0,0.8-(f-146)/22*0.8); s['under'].append(('trail',40,W,GROUND-10,9,a)); sk['vis']=False
    if 164<=f<192:
        t=(f-164)/28; sk.update(vis=True,spr=SUKUNA['hurt'] if f<182 else SUKUNA['idle'],alpha=min(1,t*1.5))
        if f<180:
            for i in range(10):
                a=i*2.4+f*0.2; L=(1-t)*30; s['fx'].append(('mote',150+math.cos(a)*L,GROUND-10+math.sin(a)*L*0.6,(170,20,40)))
    s['actors']=[cl,sk]
    return s

# ---------------------------------------------------------------- transitions
def asterisk_thick(d,x,y,r,f,c=(217,119,87)):
    for k in range(8):
        a=k*math.pi/4+f*0.25; L=r*(1 if k%2==0 else 0.75)
        d.line([x,y,x+math.cos(a)*L,y+math.sin(a)*L],fill=c,width=max(1,int(r/5)))
    d.ellipse([x-r*0.18,y-r*0.18,x+r*0.18,y+r*0.18],fill=c)

def transition(a_img,b_img,T=22):
    out=[]
    for i in range(T):
        half=T//2; src=a_img if i<half else b_img
        t=i/(half-1) if i<half else (T-1-i)/(half-1)   # 0 -> 1 (closed) -> 0
        r=int(lerp(115,0,t)); cx,cy=W//2,GROUND-12
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
        im=Image.composite(src,Image.new('RGB',(W,H)),m)
        d=ImageDraw.Draw(im); asterisk_thick(d,cx,cy,int(4+14*t),i)
        out.append(im)
    return out

THEMES={
 'dbz':[('beam',None,200)]+[(n,fn,nn) for n,(fn,nn) in DBZ_CLIPS.items()],
 'ygo':[('duel',clip_duel,216)],
 'kny':[('breath',clip_breath,204)],
 'jjk':[('infinity',clip_infinity,216)],
}

if __name__=='__main__':
    shutil.rmtree('clips',ignore_errors=True); shutil.rmtree('transitions',ignore_errors=True)
    first={}
    for theme,items in THEMES.items():
        for name,fn,n in items:
            random.seed(hash(name)%1000)
            if theme=='dbz':
                frames=[frame(f) for f in range(n)] if name=='beam' else [C.render(fn(f),f) for f in range(n)]
            else: frames=[render(fn(f),f) for f in range(n)]
            dd=f'clips/{theme}__{name}'; os.makedirs(dd)
            for i,fr in enumerate(frames): fr.save(f'{dd}/{i:03d}.png')
            first.setdefault(theme,frames[0])
            big=[fr.resize((W*2,H*2),Image.NEAREST) for fr in frames]
            sh=Image.new('RGB',(W*4,H*12)); pick=[int(i*(n-1)/11) for i in range(12)]
            for j,i in enumerate(pick): sh.paste(big[i],((j%2)*W*2,(j//2)*H*2))
            sh.save(f'sheet_{theme}_{name}.png'); print(theme,name,n)
    for a in first:
        for b in first:
            if a==b: continue
            dd=f'transitions/{a}__{b}'; os.makedirs(dd)
            for i,fr in enumerate(transition(first[a],first[b])): fr.save(f'{dd}/{i:03d}.png')
    print('transitions ok')
