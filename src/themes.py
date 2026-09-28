# Anime themes for the notch fight. Claude is always the protagonist.
# Each THEME has its own neutral "loop keyframe": every clip of a theme starts
# and ends on it, so clips of the same theme chain seamlessly. Between themes
# the app plays a pre-rendered asterisk-iris transition.
import math, random, os, shutil, zlib
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
        c={'nrt':(v,v//2+6,v//4),'pkm':(v//3,v,v//3),'snk':(v,v-4,v-10),'fn':(v//2,v,v//3+4),'dbz':(v,v,v+4),'ygo':(v+8,v//2,v+18),'kny':(v//2,v,v//2+6),'jjk':(v//2+4,v//2,v+14)}[kind]
        d.point((x,GROUND+1),fill=c)
    if kind=='ygo':
        for x in range(8,W,12): d.point((x,GROUND+3),fill=(40,18,60))
    if kind=='kny':
        d.ellipse([164,3,176,15],fill=(236,228,180)); d.ellipse([167,1,179,13],fill=(0,0,0))
    return im
BGS={k:make_bg(k) for k in ('dbz','ygo','kny','jjk','fn','pkm','snk','nrt')}

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
    if 'closeup' in s: return closeup_frame(s['closeup'],f)
    im=make_bg(s['kind']) if s['kind'] not in BGS else BGS[s['kind']].copy(); d=ImageDraw.Draw(im)
    for e in s['under']: fx_snk(d,im,e,f)
    for a in s['actors']:
        if not a['vis']: continue
        if a['holo'] is not None: draw_holo(im,a['spr'],a['x'],a['y'],a['flip'],a['holo'],f)
        else: draw(im,a['spr'],a['x'],a['y'],a['flip'],aura=a['aura'],f=f,pal=a['pal'],alpha=a.get('alpha',1.0),tint=a.get('tint'))
    if s['kind']=='snk': d.rectangle([0,GROUND+2,W,H],fill=(0,0,0))   # titans sink INTO the ground
    for e in s['fx']: fx_snk(d,im,e,f)
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


# ---------------------------------------------------------------- FORTNITE
PAL.update({'A':(26,24,32),'Q':(212,170,60),'F':(150,96,52)})
JONES=variant(lambda s: recolor_rows(s,
    lambda x,y,t,l,r,c: ('F' if x==l-1 else 'k') if (t+1<=y<=t+6 and l-2<=x<=l-1 and c in '.o') else None))
GENO=poses(S([
".....kkkk.......","....kkHkkk......","....kkHkss......","....kssEsE......","....ksssss......",".....ssss.......",
"...AAAQAAAA.....","..AAAArQAAAA....","..AQAArrAAQA....","..AA.AQQAA.AA...","..AA.ArrA..AA...","..AA.AAAA..sA...",
"..ss.AQQA.......",".....AAAA.......","....AA..AA......","....AQ..QA......","....AA..AA......","....Ar..rA......",
"....AA..AA......","...AAA..AAA.....",]),9,'As',4)
FONT={'V':"101101101101010",'I':"111010010010111",'C':"111100100100111",'T':"111010010010010",'O':"111101101101111",
'R':"110101110101101",'Y':"101101010010010",'A':"010101111101101",'L':"100100100100111",'E':"111100110100111",' ':"000000000000000",
'0':"111101101101111",'1':"010110010010111",'2':"111001111100111",'3':"111001111001111",'4':"101101111001001",
'5':"111100111001111",'6':"111100111101111",'7':"111001001001001",'8':"111101111101111",'9':"111101111001111"}
def text(d,txt,x,y,c,shadow=(0,0,0)):
    for i,ch in enumerate(txt):
        bits=FONT.get(ch,FONT[' '])
        for j,b in enumerate(bits):
            if b=='1':
                px,py=x+i*4+j%3,y+j//3
                if shadow: d.point((px+1,py+1),fill=shadow)
                d.point((px,py),fill=c)

def fx_fn(d,im,e,f):
    k=e[0]
    if k=='pickaxe':
        _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(150,96,52))
        dx,dy=x1-x0,y1-y0; L=max(1,math.hypot(dx,dy)); nx,ny=-dy/L,dx/L
        d.line([x1-nx*3,y1-ny*3,x1+nx*3,y1+ny*3],fill=(190,200,215),width=2)
    elif k=='wall':
        _,x,prog=e; top=GROUND-16; x=int(x)
        if prog<1:
            d.rectangle([x,top,x+3,GROUND],outline=(90,170,255))
            d.rectangle([x,int(GROUND-16*prog),x+3,GROUND],fill=(80,140,230))
        else:
            d.rectangle([x,top,x+3,GROUND],fill=(176,118,60))
            for yy in range(top+3,GROUND,4): d.line([x,yy,x+3,yy],fill=(120,76,36))
    elif k=='ramp':
        _,x0,prog=e; L=int(24*prog)
        for i in range(L):
            yy=GROUND-int(i*0.66); c=(80,140,230) if prog<1 else ((176,118,60) if i%5 else (120,76,36))
            d.line([x0+i,yy,x0+i,yy+2],fill=c)
    elif k=='bars':
        _,x0,hp,sh,flip=e
        d.rectangle([x0,1,x0+30,2],fill=(30,30,30)); d.rectangle([x0,4,x0+30,5],fill=(30,30,30))
        if flip:
            if sh>0: d.rectangle([x0+30-int(30*sh),1,x0+30,2],fill=(60,150,255))
            if hp>0: d.rectangle([x0+30-int(30*hp),4,x0+30,5],fill=(40,210,90))
        else:
            if sh>0: d.rectangle([x0,1,x0+int(30*sh),2],fill=(60,150,255))
            if hp>0: d.rectangle([x0,4,x0+int(30*hp),5],fill=(40,210,90))
    elif k=='dmg':
        _,txt,x,y,c=e; text(d,txt,int(x),int(y),c)
    elif k=='banner':
        _,a=e
        if a<=0: return
        w=64; x0=W//2-w//2
        for x in range(x0,x0+w):
            for y in range(8,19): C.blend(im.load(),x,y,(40,70,190) if 9<y<17 else (250,210,60),a)
        if a>0.6: text(d,"VICTORY ROYALE",x0+4,11,(255,226,90),(20,30,90))
    elif k=='chest':
        _,x,open_=e; x=int(x)
        d.rectangle([x-5,GROUND-5,x+5,GROUND],fill=(200,150,40)); d.rectangle([x-5,GROUND-5,x+5,GROUND-4],fill=(250,210,70))
        d.rectangle([x-1,GROUND-4,x+1,GROUND-2],fill=(90,60,20))
        if open_:
            for i in range(5): d.line([x-4+i*2,GROUND-6,x-8+i*4,GROUND-6-12],fill=(255,236,150))
    elif k=='rifle':
        _,x,y,flip=e; s_=-1 if flip else 1
        d.line([x,y,x+9*s_,y],fill=(240,200,60),width=2); d.point((x+2*s_,y+2),fill=(200,160,40))
    elif k=='tracer':
        _,x0,x1,y=e; d.line([x0,y,x1,y],fill=(255,240,140))
    elif k=='potion':
        _,x,y=e; d.rectangle([x-1,y-3,x+1,y+1],fill=(80,170,255)); d.point((x,y-4),fill=(230,230,240))
    elif k=='bus':
        _,x,y=e; x,y=int(x),int(y)
        d.ellipse([x-6,y-9,x+6,y-1],fill=(60,120,230)); d.line([x-3,y-1,x-4,y+2],fill=(200,200,210)); d.line([x+3,y-1,x+4,y+2],fill=(200,200,210))
        d.rectangle([x-8,y+2,x+8,y+7],fill=(40,110,220)); d.rectangle([x-7,y+3,x+6,y+4],fill=(190,230,255)); d.rectangle([x-8,y+6,x+8,y+7],fill=(250,210,60))
    elif k=='glider':
        _,x,y=e; d.arc([x-8,y-6,x+8,y+4],180,360,fill=(250,210,60),width=2); d.line([x-6,y-1,x,y+6],fill=(200,200,210)); d.line([x+6,y-1,x,y+6],fill=(200,200,210))
    elif k=='storm':
        for x in list(range(0,5))+list(range(W-5,W)):
            a=0.5*(1-min(x,W-1-x)/5)
            for y in range(0,H,2): C.blend(im.load(),x,(y+f)%H,(150,60,220),a)
    else: fx2(d,im,e,f)

def dmg(s,f,t0,txt,x,y,c):
    if t0<=f<t0+14: s['fx'].append(('dmg',txt,x,y-(f-t0)*0.7,c))

def clip_royale(f):
    s=scene(f,'fn'); N=228
    cl=actor(JONES[guard_pose(f)],28); gn=actor(GENO['idle'],152,flip=True)
    gn['pal']={'r':(255,60,60) if (f//4)%2 else (170,20,30)}
    ch,cs,gh,gs=1.0,1.0,1.0,1.0; tool='pick'; pose=None
    s['under'].append(('storm',))
    if 12<=f<28:
        gn['spr']=GENO['attack']
        for j in range(3):
            t0=12+j*4
            if t0<=f: x=140-8*(f-t0)
            if t0<=f and x>50: s['fx'].append(('orbc',x,GROUND-10-j*2,1,((255,120,120),(220,30,40))))
            if t0<=f and x<=50 and f-t0<(140-50)//8+2: s['fx'].append(('spark',48,GROUND-10-j*2,3))
    if 14<=f<48: s['under'].append(('wall',46,min(1,(f-14)/4)))
    if 24<=f<48: s['under'].append(('ramp',50,min(1,(f-24)/5)))
    if 28<=f<36:
        t=(f-28)/8; cl['x']=lerp(28,48,t); pose='dash'
    if 36<=f<44:
        t=(f-36)/8; cl['x']=lerp(50,72,t); cl['y']=GROUND-int(t*15); pose='dash'
    if 44<=f<52:
        t=(f-44)/8; cl['x']=lerp(72,138,t); cl['y']=GROUND-15+int(15*t*t)-int(10*math.sin(math.pi*t)); pose='punch'
    if f==52: s['fx'].append(('spark',146,GROUND-14,7)); s['shake']=rshake(2)
    dmg(s,f,52,"74",140,GROUND-26,(90,170,255))
    if f>=52: gs=0.26
    if 52<=f<60: gn['spr']=GENO['hurt']; cl.update(x=138,y=GROUND); pose='punch'
    if 60<=f<72:   # Geno slam shockwave
        gn['spr']=GENO['attack']; t=(f-60)/12; cl['x']=ez(138,36,t); cl['y']=GROUND-int(8*math.sin(math.pi*t)); pose='hurt'
        s['fx'].append(('ring',150-(f-60)*5,GROUND,6,(255,80,80)))
        if f==60: s['flash']=0.5; s['fc']=(150,GROUND-8); s['flashc']=(255,120,120); s['shake']=rshake(2)
    dmg(s,f,62,"50",40,GROUND-22,(90,170,255))
    if f>=62: cs=0.5
    if 72<=f<88:
        cl['x']=36; tool=None; pose='punch' if (f//3)%2 else 'guard'
        s['fx'].append(('potion',cl['x']+8,GROUND-6)); cs=0.5+0.5*(f-72)/16
        if f%3==0: s['fx'].append(('mote',cl['x']+random.randint(-4,4),GROUND-12-random.randint(0,6),(120,200,255)))
    if f>=88: cs=1.0
    if 72<=f<140: gn['spr']=GENO['idle'] if f<96 else GENO['hurt'] if f<112 else gn['spr']
    if 88<=f<100:
        cl['x']=ez(36,40,(f-88)/12); tool=None
        s['under'].append(('chest',56,f>=92))
        if f>=92: s['fx'].append(('twinkle',56,GROUND-14-(f-92),2))
    if 100<=f<116:
        tool='rifle'; pose='punch'
        if f%3==0:
            s['fx'].append(('tracer',52,144,GROUND-6)); s['fx'].append(('spark',146,GROUND-10+random.randint(-3,3),3))
    for j,t0 in enumerate(range(100,116,3)): dmg(s,f,t0,"32",140+(j%2)*6,GROUND-28+(j%3)*2,(255,255,255) if j>0 else (90,170,255))
    if f>=100: gs=0.0; gh=max(0,1-(f-100)/15)
    if 116<=f<136:   # eliminated: dissolves into rising cubes
        gn['vis']=False; rr=random.Random(3); t=f-116
        for j,row in enumerate(GENO['hurt']):
            for i,c in enumerate(row):
                if c=='.' or rr.random()<0.6: continue
                x=152+(len(row)/2-i)+rr.uniform(-1,1)*t*0.5; y=GROUND-len(GENO['hurt'])+j-t*rr.uniform(0.8,2.2)
                if rr.random()>t/22: s['fx'].append(('shard',x,y,(120,200,255) if (i+j+f)%3 else (255,255,255)))
    if 116<=f<200 and not (184<=f): gn['vis']=False
    if 124<=f<164:   # Victory Royale + default dance
        a=min(1,(f-124)/6) if f<152 else max(0,1-(f-152)/12)
        s['fx'].append(('banner',a)); tool=None
        dance=['guard','armsup','guard2','punch']; pose=dance[(f//3)%4]; cl['flip']=(f//6)%2==1
    if 136<=f<200:   # battle bus drops Geno back in
        s['fx'].append(('bus',lerp(-20,W+20,(f-136)/64),9))
    if 160<=f<200:
        t=(f-160)/40; x=lerp(100,152,t); y=lerp(30,GROUND,t)
        if f>=162: gn.update(vis=True,x=x,y=y,spr=GENO['idle']); s["fx"].append(("glider",x,y-22)) if f<198 else None
        gs=gh=min(1,t*1.3)
    elif f>=200: gs=gh=1.0
    if pose: cl['spr']=JONES[pose]
    p=pose or 'guard'
    if tool=='pick':
        sx=-1 if cl['flip'] else 1
        if p in ('guard','guard2'): s['fx'].append(('pickaxe',cl['x']+5*sx,cl['y']-5,cl['x']+9*sx,cl['y']-15))
        elif p=='hurt': s['fx'].append(('pickaxe',cl['x']+4*sx,cl['y']-8,cl['x']-3*sx,cl['y']-15))
        else: s['fx'].append(('pickaxe',cl['x']+8*sx,cl['y']-5,cl['x']+17*sx,cl['y']-9))
    elif tool=='rifle': s['fx'].append(('rifle',cl['x']+8,GROUND-6,False))
    s['fx']+=[('bars',3,ch,cs,False),('bars',151,gh,gs,True)]
    s['actors']=[cl,gn]
    return s


# ---------------------------------------------------------------- shared: full 3x5 font
FONT.update({
'A':"010101111101101",'B':"110101110101110",'C':"111100100100111",'D':"110101101101110",'E':"111100110100111",
'F':"111100110100100",'G':"111100101101111",'H':"101101111101101",'I':"111010010010111",'J':"001001001101111",
'K':"101101110101101",'L':"100100100100111",'M':"101111111101101",'N':"110101101101101",'O':"111101101101111",
'P':"111101111100100",'Q':"111101101111001",'R':"110101110101101",'S':"111100111001111",'T':"111010010010010",
'U':"101101101101111",'V':"101101101101010",'W':"101101111111101",'X':"101101010101101",'Y':"101101010010010",
'Z':"111001010100111",'!':"010010010000010",':':"000010000010000",'.':"000000000000010"})

# ---------------------------------------------------------------- POKEMON
PAL.update({'m':(206,196,222),'u':(150,92,176),'U':(120,40,160)})
ASH=variant(lambda s: overlay(s,["..rrrrrr....",".rrrHHrrr...",".rrrrrrrrrrr"],-1,0))
MEWTWO=poses(S([
".....mm.mm........",".....mmmmm........","....mmmmmmm.......","....mmmUmmU.......","....mmmmmmm.......",".....mmmmm........",
"......mmm.........","....mmmmmmm.......","...mmmmmmmmm......","..mm.mmmmm.mm.....","..mm.muuum.mm.....","..m..muuum..m.....",
"uu...muuum........","uu...uuuuu........",".uu.uuu.uuu.......","..uuu...uu........","...mm.....mm......","...mm.....mm......",
"..mmm.....mmm.....",]),9,'mm',4)

def hp_color(v): return (40,210,90) if v>0.5 else (240,200,40) if v>0.2 else (230,50,40)

def fx_pkm(d,im,e,f):
    k=e[0]
    if k=='hp':
        _,x0,name,v=e; text(d,name,x0,1,(240,240,240)); d.rectangle([x0,8,x0+34,9],fill=(40,40,40))
        if v>0: d.rectangle([x0,8,x0+int(34*v),9],fill=hp_color(v))
    elif k=='textbox':
        _,l1,l2=e; d.rectangle([46,10,139,24],fill=(0,0,0),outline=(236,236,236))
        text(d,l1,49,12,(240,240,240)); text(d,l2,49,18,(240,240,240))
    elif k=='pball':
        _,x,y,op=e; x,y=int(x),int(y); o=int(op)
        d.ellipse([x-3,y-3-o,x+3,y+3-o],fill=(230,40,40)) if o else None
        d.pieslice([x-3,y-3-o,x+3,y+3-o],180,360,fill=(230,40,40)); d.pieslice([x-3,y-3+o,x+3,y+3+o],0,180,fill=(240,240,240))
        d.line([x-3,y,x+3,y],fill=(20,20,20)); d.point((x,y),fill=(240,240,240))
    elif k=='psywave':
        _,x0,x1,y0,y1=e
        for j in range(3):
            pts=[(x,lerp(y0,y1,(x-x0)/max(1,x1-x0))+3*math.sin(x*0.4+f*0.8+j*2)) for x in range(int(min(x0,x1)),int(max(x0,x1)),2)]
            if len(pts)>1: d.line(pts,fill=(200,120,255) if j%2 else (150,80,230))
    elif k=='platform':
        _,x=e; d.ellipse([x-16,GROUND-2,x+16,GROUND+3],outline=(60,90,60))
    else: fx_fn(d,im,e,f)

def clip_psychic(f):
    s=scene(f,'pkm'); N=240
    hov=GROUND-3+round(2*math.sin(2*math.pi*f/24))
    cl=actor(ASH[guard_pose(f)],30); mw=actor(MEWTWO['idle'],150,y=hov,flip=True)
    hc=hm=1.0; msg=None
    s['under']+=[('platform',30),('platform',150)]
    if 12<=f<48: msg=("CLAUDE USED","QUICK ATTACK!")
    if 18<=f<30:
        t=(f-18)/12; cl['x']=lerp(30,134,t); cl['y']=GROUND-int(6*abs(math.sin(t*math.pi*3))); cl['spr']=ASH['dash']
        cl['aura']=((255,255,255),1)
        for i in range(3): y=random.randint(30,58); x=random.randint(0,120); s['fx'].append(('tracer',x,x+10,y))
    if f==30: s['fx'].append(('spark',142,hov-10,7)); s['shake']=rshake(2)
    if 30<=f<34: cl.update(x=134,spr=ASH['punch']); mw['spr']=MEWTWO['hurt']
    if f>=30: hm=0.8
    if 34<=f<46: t=(f-34)/12; cl.update(x=ez(134,30,t),y=GROUND-int(8*math.sin(math.pi*t)))
    if 48<=f<96:
        msg=("MEWTWO USED","PSYCHIC!"); mw['spr']=MEWTWO['attack']; mw['aura']=((200,120,255),1+(f%2))
        if 54<=f<90:
            lift=ez(0,18,(f-54)/10) if f<86 else ez(18,0,(f-86)/4)
            cl.update(y=GROUND-int(lift)+random.choice([-1,0,1]),x=30+random.choice([-1,0,1]),spr=ASH['hurt'],aura=((200,120,255),2))
            s['under'].append(('psywave',40,140,cl['y']-6,hov-10))
            s['fx'].append(('circle',cl['x'],cl['y']-6,2+(f*2)%10,(200,120,255)))
            hc=lerp(1,0.55,(f-60)/30) if f>=60 else 1
        if f==90: s['shake']=rshake(2); s['fx'].append(('spark',30,GROUND-4,6))
        if 90<=f<96:
            for i in range(2): s['fx'].append(('dust',30+random.randint(-8,8),GROUND-random.randint(0,3)))
    if f>=90: hc=0.55
    if 96<=f<136:
        msg=("CLAUDE USED","FLAMETHROWER!"); cl['spr']=ASH['charge']; cl['aura']=((255,150,60),1+(f%2))
        if 102<=f<130:
            for i in range(16):
                t=((f*0.09+i/16)%1); x=lerp(42,140,t); y=GROUND-6+lerp(0,hov-10-(GROUND-6),t)+math.sin(i*1.7+f*0.9)*t*4
                c=[(255,240,160),(255,190,70),(240,110,40),(200,60,30)][min(3,int(t*4))]
                s['fx'].append(('smoke',x,y,1+int(t*2.5),c))
        if f>=110: mw['spr']=MEWTWO['hurt']; hm=lerp(0.8,0.25,(f-110)/20)
    if f>=130: hm=0.25
    if 136<=f<152:
        msg=("MEWTWO USED","SHADOW BALL!"); mw['spr']=MEWTWO['attack']
        if f>=138:
            x=140-10*(f-138)
            if x>-10: s['fx'].append(('orbc',x,GROUND-8,3,((90,40,130),(30,10,50))))
        if 142<=f<154: t=(f-142)/12; cl['y']=GROUND-int(16*math.sin(math.pi*t))
    if 152<=f<172: msg=("CLAUDE THREW A","POKE BALL!")
    if 154<=f<160: cl['spr']=ASH['punch']
    if 156<=f<166:
        t=(f-156)/10; s['fx'].append(('pball',lerp(38,150,t),lerp(GROUND-10,hov-12,t)-14*math.sin(math.pi*t),0))
    if 166<=f<172:
        mw.update(tint=(255,70,70),alpha=1-(f-166)/6); s['fx'].append(('pball',150,hov-12,2))
        s['fx'].append(('tracer',146,154,hov-12))
    if 172<=f<200:
        mw['vis']=False; wob=(1 if f in range(176,180) or f in range(192,196) else -1 if f in range(184,188) else 0)
        s['fx'].append(('pball',150+wob,GROUND-3,0)); msg=(".  .  .","") if f<188 else (".  .  .  .","")
    if 200<=f<224:
        msg=("OH NO!","IT BROKE FREE!")
        if f<204: s['flash']=0.8; s['fc']=(150,GROUND-8); s['flashc']=(255,255,255)
        if f<206: s['fx'].append(('pball',150,GROUND-3,3))
        mw.update(tint=(255,70,70) if f<208 else None,alpha=min(1,(f-200)/6))
    if 216<=f<232: hc=lerp(0.55,1,(f-216)/16); hm=lerp(0.25,1,(f-216)/16)
    if f>=232: hc=hm=1.0
    s['fx']+=[('hp',3,'CLAUDE',hc),('hp',148,'MEWTWO',hm)]
    if msg: s['fx'].append(('textbox',)+msg)
    s['actors']=[cl,mw]
    return s

# ---------------------------------------------------------------- SHINGEKI NO KYOJIN
PAL.update({'t':(232,186,160),'T':(194,146,122),'z':(208,174,112),'a':(132,100,62)})
SCOUT=variant(lambda s: recolor_rows(s,
    lambda x,y,t,l,r,c: ('X' if c in '.o' and x<l else None) if (t+1<=y<=t+8 and l-2<=x<l) else
                        ('F' if (y==t+6 and l<=x<=r and c=='O') else ('D' if (y==t+7 and x in (l,r)) else None))))

_TCACHE={}
def titan(h,hair,walk=0,armored=False):
    key=(h,hair,walk,armored)
    if key in _TCACHE: return _TCACHE[key]
    w=max(11,int(h*0.5))|1; cx=w//2; g=[['.']*w for _ in range(h)]
    sk,sh=('z','a') if armored else ('t','T')
    hh=max(7,int(h*0.3)); hw=max(5,int(w*0.6))
    for y in range(hh):
        for x in range(w):
            if ((x-cx)/(hw/2))**2+((y-hh/2+0.5)/(hh/2))**2<=1:
                g[y][x]=hair if (y<hh*0.35 or (y<hh*0.65 and abs(x-cx)>=hw/2-1)) else sk
    ey=int(hh*0.5); g[ey][cx-2]='K'; g[ey][cx+1]='K'
    my=int(hh*0.78)
    for x in range(cx-hw//3,cx+hw//3+1): g[my][x]='H'
    g[my][cx-hw//3-1]='K'; g[my][cx+hw//3+1]='K'
    g[hh][cx-1]=g[hh][cx]=g[hh][cx+1]=sk
    th=int(h*0.33); tw=max(5,int(w*0.62)); t0=hh+1; l=cx-tw//2; r=cx+tw//2
    for y in range(t0,min(h,t0+th)):
        for x in range(l,r+1): g[y][x]=sh if x==l else (('a' if (y-t0)%3==0 else sk) if armored else sk)
    for y in range(t0,min(h,t0+th+3)):
        sw=walk if y>t0+th//2 else 0
        for x in (l-2-sw,l-1-sw,r+1+sw,r+2+sw):
            if 0<=x<w: g[y][x]=sk
    for y in range(t0+th,h):
        o=walk if y>t0+th+(h-t0-th)//2 else 0
        for x in range(l+1,cx):
            xx=x+o
            if 0<=xx<w: g[y][xx]=sh if x==l+1 else sk
        for x in range(cx+1,r):
            xx=x-o
            if 0<=xx<w: g[y][xx]=sk
    out=S([''.join(r) for r in g]); _TCACHE[key]=out; return out

def fx_snk(d,im,e,f):
    k=e[0]
    if k=='wire': _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(170,170,180))
    elif k=='blades':
        _,x,y,fl=e; s_=-1 if fl else 1
        d.line([x+6*s_,y-5,x+14*s_,y-8],fill=(220,224,238)); d.line([x+5*s_,y-3,x+13*s_,y-3],fill=(200,206,222))
    elif k=='spear':
        _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(120,120,130)); d.point((int(x1),int(y1)),fill=(230,50,40))
    elif k=='gunbai':
        _,x,y=e; d.line([x,y+4,x+6,y-4],fill=(120,80,50)); d.ellipse([x-6,y-10,x+4,y],fill=(230,220,200),outline=(140,30,30))
        d.line([x-5,y-5,x+3,y-5],fill=(140,30,30))
    elif k=='wallbg':
        for y in range(12,GROUND+1):
            for x in range(0,8):
                c=(70,68,64) if (y%4==0 or (x+(y//4)*3)%6==0) else (104,100,94)
                d.point((x,y),fill=c)
        for x in range(0,8,3): d.rectangle([x,9,x+1,11],fill=(104,100,94))
    else: fx_pkm(d,im,e,f)

TITANS=[dict(h=26,hair='q',tx=118,kill=34),dict(h=34,hair='k',tx=146,kill=66),dict(h=30,hair='Y',tx=102,kill=98),
        dict(h=38,hair='R',tx=156,kill=130),dict(h=24,hair='k',tx=128,kill=160)]

def nape(T,armored=False):
    h=T['h']; w=max(11,int(h*0.5))|1; hh=max(7,int(h*0.3))
    return T['x']+w//2-1, GROUND-h+hh+1

def clip_survey(f):
    s=scene(f,'snk'); N=264
    s['under'].append(('wallbg',))
    cl=actor(SCOUT[guard_pose(f)],30); pos=(30.0,float(GROUND)); flip=False; blades=True; pose=None
    titans=[]
    for i,T in enumerate(TITANS):
        enter=T['kill']-34
        if not (enter<=f<T['kill']+24): continue
        t=min(1,(f-enter)/26); x=lerp(205,T['tx'],t); walking=t<1
        y=GROUND-(1 if walking and (f//4)%2 else 0)
        a=actor(titan(T['h'],T['hair'],walk=((f//4)%2*2-1) if walking else 0),x,y=y)
        T=dict(T,x=x)
        if f>=T['kill']+2:
            k=(f-T['kill']-2)/20; a['y']=GROUND+int(T['h']*0.45*k); a['alpha']=max(0,1-k)
            rr=random.Random(f//2+i)
            for j in range(int(8*(1-k)+3)): s['fx'].append(('smoke',x+rr.randint(-8,8),GROUND-rr.randint(4,T['h']),rr.randint(2,4),(236,236,240) if j%2 else (190,190,200)))
        titans.append(a); TITANS[i]['x']=x
    # Claude's flight path: launch -> zip to nape -> spin slash -> drop
    prev=(30,GROUND)
    for i,T in enumerate(TITANS):
        tk=T['kill']; nx,ny=nape(dict(T,x=T['tx'])); land=(T['tx']-26,GROUND)
        if tk-10<=f<tk-2:
            t=(f-(tk-10))/8; pos=(lerp(prev[0],nx+4,ease(t)),lerp(prev[1],ny,ease(t))-10*math.sin(math.pi*t)); pose='dash'
            s['fx'].append(('wire',pos[0],pos[1]-5,nx,ny))
            s['fx'].append(('mote',pos[0]-4,pos[1]-4,(240,240,250)))
        elif tk-2<=f<tk+4:
            pos=(nx+4,ny); flip=(f%2==0); pose='punch'
            s['fx'].append(('circle',pos[0],pos[1]-6,8,(240,240,255)))
            if f==tk: s['fx'].append(('spark',nx,ny-2,7)); s['shake']=rshake()
        elif tk+4<=f<tk+14:
            t=(f-(tk+4))/10; pos=(lerp(nx+4,land[0],t),lerp(ny,GROUND,t*t)); pose='guard'
        elif i+1<len(TITANS) and tk+14<=f<TITANS[i+1]['kill']-10: pos=land
        prev=land
    last=TITANS[-1]; lx=last['tx']-26
    if 174<=f<200: pos=(lx,GROUND)
    # --- the Armored Titan
    AH=46; arm=None
    if 170<=f<262:
        if f<196: x=lerp(215,140,(f-170)/26); walking=True
        elif f<200: x=140; walking=False
        elif f<210: x=lerp(140,86,ease((f-200)/10)); walking=False
        else: x=86; walking=False
        arm=actor(titan(AH,'Y',walk=((f//5)%2*2-1) if walking else 0,armored=True),x)
        if walking and f%5==0: s['shake']=rshake()
        if 232<=f<250: arm['y']=GROUND+int(12*ease((f-232)/18))
        if f>=250: arm['y']=GROUND+12; arm['alpha']=max(0,1-(f-250)/12)
        if f>=232:
            rr=random.Random(f//2)
            for j in range(10): s['fx'].append(('smoke',x+rr.randint(-12,12),GROUND-rr.randint(6,40),rr.randint(2,5),(236,236,240) if j%2 else (190,190,200)))
        titans.append(arm)
    AT=dict(h=AH,x=86); anx,any_=nape(AT)
    if 200<=f<210:
        t=(f-200)/10; pos=(lerp(lx,48,ease(t)),lerp(GROUND,GROUND-26,ease(t))); pose='dash'; flip=False
        s['fx'].append(('wire',pos[0],pos[1]-5,6,12))
    if 210<=f<216:
        t=(f-210)/6; pos=(lerp(48,anx+4,t),lerp(GROUND-26,any_,t)); pose='dash'
        s['fx'].append(('wire',pos[0],pos[1]-5,anx,any_))
    if 216<=f<222:
        pos=(anx+4,any_); pose='punch'; flip=True; blades=f<217
        if f==216: s['fx'].append(('spark',anx,any_-2,6)); s['shake']=rshake(2)
        for j in range(4): s['fx'].append(('shard',anx+random.randint(-6,6)+(f-216)*2,any_-4+random.randint(-4,4)+(f-216),(220,224,238)))
    if 222<=f<230:
        t=(f-222)/8; pos=(lerp(anx+4,58,t),lerp(any_,GROUND,t*t)); pose='hurt'; flip=False; blades=False
    if 228<=f<236:
        pos=(58,GROUND); pose='charge'; blades=False
        if f<232:
            t=(f-228)/4
            for dy in (0,3): s['fx'].append(('spear',58+8,GROUND-6+dy,lerp(66,anx,t),lerp(GROUND-6+dy,any_+dy,t)))
        else:
            for dy in (0,3): s['fx'].append(('spear',anx-6,any_+dy+2,anx,any_+dy))
    if f==232: s['flash']=0.9; s['fc']=(anx,any_); s['flashc']=(255,190,120); s['shake']=rshake(2)
    if 232<=f<242: s['fx'].append(('boom',anx,any_,int(4+(f-232)*3)))
    if 236<=f<256: pos=(ez(58,30,(f-236)/20),GROUND); blades=False
    if 252<=f<258: s['fx'].append(('twinkle',36,GROUND-7,1+(f%2)))
    if f>=256: blades=True
    cl.update(x=pos[0],y=pos[1],flip=flip)
    if pose: cl['spr']=SCOUT[pose]
    if blades: s['fx'].append(('blades',cl['x'],cl['y'],flip))
    s['actors']=titans+[cl]
    return s


# ---------------------------------------------------------------- NARUTO
NARU=variant(lambda s: recolor_rows(overlay(s,["Y.Y.Y.Y.Y.Y.","YYYYYYYYYYYY",".YYYYYYYYYY."],-2,0),
    lambda x,y,t,l,r,c: ('D' if l+2<=x<=l+5 else 'N') if (y==t and l<=x<=r and c!='.') else None))
MADARA=poses(S([
"....kkkkkk........","..kkkkkkkkkk......",".kkkkkkkkkkkk.....","kkkkkkksssssk.....","kkkkkksrssrsk.....",
"kkkkkksssssk......",".kkkkkksssk.......","kkkkkRRRRRRR......","kkkkRRRRRRRRR.....","kkkRRZRRRRZRRR....",
"kkkRR.NNNN.RR.....",".kkRR.NNNN.RR.....",".kk.s.RRRR.s......","..k...RRRR........","......RZZR........",
".....RRRRRR.......",".....RR..RR.......",".....RR..RR.......",".....NN..NN.......",".....NN..NN.......",
".....NN..NN.......","....kkk..kkk......",]),10,'Rs',4)

def callout(s,txt,y=2,c=(255,226,90)):
    s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))

def poof(s,x,t):
    """Shadow-clone smoke puff, t = frames since the poof started (0..6)."""
    if 0<=t<7:
        rr=random.Random(int(x)*7+t)
        for j in range(6): s['fx'].append(('smoke',x+rr.randint(-6,6),GROUND-5-rr.randint(0,9),2+t//2+rr.randint(0,1),(236,236,240) if j%2 else (200,200,210)))

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
    if t<0.1:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    if t>0.9: im=Image.blend(im,Image.new('RGB',(W,H),(200,0,20)),0.5*(t-0.9)/0.1)
    return im

def clip_shadowclone(f):
    s=scene(f,'nrt'); N=252
    cl=actor(NARU[guard_pose(f)],30); md=actor(MADARA['idle'],152,flip=True)
    clones=[]
    OFF=[18,42,54,66]
    if 64<=f<100: s['closeup']=(f-64)/36; return s
    if 12<=f<36:
        callout(s,"KAGE BUNSHIN NO JUTSU!")
        cl['spr']=NARU['armsup'] if f<22 else NARU[guard_pose(f)]
        for i,x in enumerate(OFF):
            t0=20+i*2
            poof(s,x,f-t0)
            if f>=t0+2: clones.append(actor(NARU[guard_pose(f+i*3)],x))
    if 36<=f<64:
        for i,x0 in enumerate(OFF):
            t0=36+i*5
            if f<t0: clones.append(actor(NARU[guard_pose(f+i*3)],x0)); continue
            k=f-t0
            if k<6: clones.append(actor(NARU['dash'],lerp(x0,138,k/6)))
            elif k==6:
                md['spr']=MADARA['attack']; s['fx'].append(('spark',142,GROUND-8,6)); s['shake']=rshake()
            poof(s,138,k-6)
            if 6<=k<9: md['spr']=MADARA['attack']; s['fx'].append(('gunbai',140,GROUND-12))
    if 100<=f<132:
        callout(s,"KATON!",c=(255,140,60)); md['spr']=MADARA['attack']
        front=lerp(140,-20,(f-102)/26) if f>=102 else 140
        rr=random.Random(f)
        for j in range(40):
            x=rr.uniform(front,140); hgt=rr.uniform(4,22)*(0.6+0.4*math.sin(x*0.2+f))
            c=[(255,240,160),(255,190,70),(240,110,40),(200,50,30)][rr.randint(0,3)]
            s['fx'].append(('smoke',x,GROUND-hgt*rr.random(),rr.randint(1,3),c))
        if 102<=f<130: t=(f-102)/28; cl['y']=GROUND-int(32*math.sin(math.pi*t)); cl['spr']=NARU['guard2']
        if f>=102: s['shake']=rshake() if f%2 else (0,0)
    if 136<=f<168:
        poof(s,44,f-136)
        if f>=138 and f<162: clones.append(actor(NARU['charge'],46,flip=True))
        poof(s,46,f-162)
        cl['spr']=NARU['charge']
        r=min(5,1+(f-140)//4) if f>=140 else 0
        bx=38 if f<160 else lerp(38,140,(f-160)/8)
        if f>=160: cl.update(x=lerp(30,132,(f-160)/8),spr=NARU['dash']); callout(s,"RASENGAN!",c=(140,210,255))
        if r: s['fx']+= [('orbc',bx,GROUND-7,r,((170,220,255),(70,150,255))),('arc',bx,GROUND-7,r+2,int(f*40)%360,int(f*40)%360+120,(235,245,255),1)]
    if 168<=f<182:
        k=f-168; cl.update(x=132,spr=NARU['punch']); md.update(spr=MADARA['hurt'],x=ez(152,176,k/12))
        for j in range(3): s['fx'].append(('circle',140,GROUND-8,2+k*2+j*3,(150,210,255) if j%2 else (90,160,255)))
        if k==0: s['flash']=0.8; s['fc']=(140,GROUND-8); s['flashc']=(170,220,255); s['shake']=rshake(2)
        if k>=8: s['fx'].append(('dust',md['x']-6,GROUND-random.randint(0,3)))
    if 172<=f<192: t=(f-172)/20; cl.update(x=ez(132,30,t),y=GROUND-int(10*math.sin(math.pi*t)),spr=NARU['guard'])
    if 182<=f<212: md.update(x=ez(176,152,(f-182)/30))
    if 196<=f<206: s['fx'].append(('twinkle',md['x']+1,GROUND-18,1+(f%2)))
    s['actors']=clones+[cl,md]
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
 'fn':[('royale',clip_royale,228)],
 'pkm':[('psychic',clip_psychic,240)],
 'snk':[('survey',clip_survey,264)],
 'nrt':[('shadowclone',clip_shadowclone,252)],
}

if __name__=='__main__':
    shutil.rmtree('clips',ignore_errors=True); shutil.rmtree('transitions',ignore_errors=True)
    first={}
    for theme,items in THEMES.items():
        for name,fn,n in items:
            random.seed(zlib.crc32(name.encode()))
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
