"""JoJo's Bizarre Adventure: Golden Wind (sub-theme of jojo). Claude is Giorno Giovanna (the three
golden curls on the forehead, the braid, the pink suit with the ladybug brooch) with Gold Experience
vs Diavolo (pink hair with green spots, the open net shirt) and King Crimson (red, the Epitaph face
on its forehead) at the Colosseum at night. KING CRIMSON!: time is erased (a red glitch, the frames
jump) and Claude is hit without ever seeing it. Close-up: the Arrow pierces Gold Experience — it
becomes REQUIEM. King Crimson tries again and the erased time is returned to zero; MUDA MUDA MUDA,
the last MUDA! sends Diavolo flying and he never reaches death: he falls, and falls again, the loop
restarting each time. ARRIVEDERCI. Requiem fades, Diavolo gets back to his spot."""
import zlib
from engine import *
from themes.jojo import _stand, MUDA_C, ST_A

THEME = 'jojo-golden'
N_ = 280
CX, VX = 30, 150                                                   # the neutral pose: Claude, Diavolo

# ---- Claude as Giorno: golden hair, three curls, the braid, the pink suit, the ladybug -----------
def _gio(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    kb=max(y for y in range(h) if 'K' in spr[y])                   # the eyes' last row
    bot=max(y for y in range(h) if 'O' in spr[y])
    m=(l+r)//2
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='O' and inside and y>kb:
                g[y][x]='O' if (y==kb+1 and x in (m,m+1)) else 'q'   # the suit, the heart-cut collar
            elif c=='o' and y>bot: g[y][x]='Q'                         # trousers
            elif c=='o': g[y][x]='q'                                   # sleeves
    if kb+2<h and g[kb+2][l+1]=='q': g[kb+2][l+1]='r'                 # the ladybug brooch
    for y in range(t+1,min(h,t+6)):                                   # the braid down his back
        if l-1>=0 and g[y][l-1]=='.': g[y][l-1]='Y'
    return overlay(ungrid(g),["..YYYYYY..",".YYYYYYYYY","YYYYYYYYYY"],-1,0,bangs="Y.Y.Y.YY")
GIO=variant(_gio)
GIOPAL={'Y':(250,214,70),'q':(236,120,170),'Q':(184,70,120),'r':(220,30,40)}

# ---- the Stands (the jojo theme's Stand body, recoloured) -----------------------------------------
GE=_stand({'h':'y','E':'X','b':'y','c':'X','f':'y','a':'X'},'yyyyyy')         # Gold Experience
GEPAL={'y':(236,196,60),'X':(60,170,90)}
GER=_stand({'h':'y','E':'H','b':'y','c':'W','f':'y','a':'W'},'yyyyyy')        # Requiem
GERPAL={'y':(255,226,120),'W':(255,255,236),'H':(120,240,160)}
KC=_stand({'h':'r','E':'H','b':'r','c':'W','f':'r','a':'k'},'rrrrrr')         # King Crimson
KC={k:paint(v,[(6,0,'gg')]) for k,v in KC.items()}                            # Epitaph on its forehead
KCPAL={'r':(196,36,56),'W':(240,236,236),'H':(255,255,255),'k':(40,20,30),'g':(90,220,120)}

# ---- Diavolo -------------------------------------------------------------------------------------
_DV=S([
"....pppppp......",
"...pppGpppp.....",
"..ppGpppppGp....",
"..ppppsssspp....",
"..pGpsKssKsp....",
"..ppssssssspG...",
"..pppssssspp....",
"..pGpssGGspp....",
"...pp.sss.pp....",
"....NsNsNsN.....",
"...sNsNsNsNs....",
"..ssNsNsNsNss...",
"..ss.NsNsNs.ss..",
"..ss.sNsNsN.ss..",
"..s..NNNNNN..s..",
".....LLLLLL.....",
".....LLLLLL.....",
".....LLL.LLL....",
".....LL...LL....",
".....LL...LL....",
".....LL...LL....",
"....kkk...kkk...",])
DV=poses(_DV,10,'s',4)
DV['idle2']=S([r.replace('pG','Gp',1) if i in (2,5) else r for i,r in enumerate(_DV)])    # the hair stirs
DV['down']=rotate90(DV['hurt'],3,trim=True)
DVPAL={'p':(240,140,180),'G':(60,130,70),'s':(236,196,160),'K':(30,20,24),'N':(110,50,140),
       'L':(40,70,80),'k':(24,20,28)}
def dv_idle(f): return DV['idle'] if (f//6)%2==0 else DV['idle2']

# ---- background: the Colosseum at night ----------------------------------------------------------
def _colosseum(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(8+18*k),int(10+14*k),int(30+26*k)))
    rr=random.Random(zlib.crc32(b'colosseo'))
    for _ in range(28): d.point((rr.randint(0,W-1),rr.randint(0,30)),fill=rr.choice([(120,120,170),(200,200,230),(80,80,120)]))
    d.ellipse([18,4,30,16],fill=(236,232,200)); d.ellipse([21,7,24,10],fill=(214,210,180))       # the full moon
    wall,lit,dark=(70,58,66),(96,82,86),(18,14,28)
    tiers=[(48,18,184,28),(44,28,185,38),(40,38,185,50)]               # three tiers, the top one broken
    d.polygon([(70,18),(84,14),(185,10),(185,50),(40,50),(40,38),(44,28),(56,24)],fill=wall)
    for i,(x0,y0,x1,y1) in enumerate(tiers):
        d.line([x0,y0,x1,y0],fill=lit)
        for x in range(x0+3+i*2,x1-5,10):
            if i==0 and x<74: continue
            d.rectangle([x,y0+3,x+5,y1-1],fill=dark); d.pieslice([x,y0+1,x+5,y0+6],180,360,fill=dark)
            if rr.random()<0.15: d.rectangle([x+1,y0+5,x+4,y1-1],fill=(110,70,40))   # a warm light inside
    d.rectangle([0,50,W,GROUND],fill=(40,34,42)); d.line([0,50,W,50],fill=(70,60,66))   # the stone
    for x in range(2,W,9): d.line([x,52,x+4,52],fill=(54,46,56)); d.line([x+4,55,x+8,55],fill=(54,46,56))
register_bg(THEME, lambda v: (v//2+30,v//2+24,v+30), decor=_colosseum)

# ---- effects -------------------------------------------------------------------------------------
@fx('jojog_erase')
def _fx_erase(d,im,e,f):
    """King Crimson's erased time: the world goes red, bands of it slip sideways."""
    _,k,seed=e
    im.paste(fade_to(im,(150,0,30),0.32*k))
    rr=random.Random(seed)
    for _ in range(int(1+3*k)):
        y=rr.randint(0,H-6); h=rr.randint(2,6); dx=rr.randint(-12,12)
        band=im.crop((0,y,W,y+h)); im.paste(band,(dx,y))
    d=ImageDraw.Draw(im)
    for _ in range(int(3*k)):
        y=rr.randint(0,H-1); d.line([0,y,W,y],fill=(255,60,90))

@fx('jojog_ghost')
def _fx_ghost(d,im,e,f):
    """A translucent afterimage (Diavolo moving through the erased time)."""
    _,spr,x,flip,a,pal=e; draw(im,spr,x,GROUND,flip,alpha=a,pal=pal,f=f)

@fx('jojog_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)

@fx('jojog_gleam')
def _fx_gleam(d,im,e,f):
    """Golden sparkles around Requiem (an 8-frame cycle)."""
    _,x,y=e; rr=random.Random(f%8)
    for _ in range(5):
        a=rr.random()*math.tau; r=6+rr.random()*10
        d.point((int(x+math.cos(a)*r),int(y+math.sin(a)*r*0.8)),fill=(255,236,150))

def banner(s,txt,y,c,scale=2,outline=None): s['fx'].append(('jojog_say',txt,y,c,scale,outline))
def shout(s,txt,c,y=2,x=None): s['fx'].append(('dmg',txt,W//2-len(txt)*2 if x is None else x,y,c))
GOLD,RED=(255,214,80),(255,80,90)

# ---- close-up: the Arrow -------------------------------------------------------------------------
def closeup_requiem(t,f):
    """The Arrow flies in and pierces Gold Experience; white light; Requiem stands up golden."""
    im=Image.new('RGB',(W,H),(20,10,30)); d=ImageDraw.Draw(im)
    for i in range(16):                                            # golden rays
        a=i*math.pi/8+t*0.6
        d.line([92,32,92+math.cos(a)*140,32+math.sin(a)*90],fill=(60,40,40) if i%2 else (44,28,44),width=3)
    req=t>=0.42
    spr,pal=(GER['idle'],GERPAL) if req else (GE['idle'],GEPAL)
    if req:                                                        # the glow behind Requiem
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([60,0,124,64],fill=150)
        im.paste((255,214,90),(0,0),g.filter(ImageFilter.GaussianBlur(8))); d=ImageDraw.Draw(im)
    paste_feet(im,sprite_img(spr,pal,scale=3),92,H+2); d=ImageDraw.Draw(im)
    tip=lerp(-20,88,ease(t/0.3)) if t<0.3 else 88                  # the Arrow
    y=36
    d.line([tip-40,y,tip-6,y],fill=(200,160,90),width=3)
    d.polygon([(tip-8,y-6),(tip+6,y),(tip-8,y+6)],fill=(250,214,90),outline=(120,80,20))
    d.ellipse([tip-5,y-2,tip-1,y+2],fill=(60,170,90))                     # the beetle on the head
    for k in (0,4): d.line([tip-40+k,y-5,tip-34+k,y],fill=(230,230,230)); d.line([tip-40+k,y+5,tip-34+k,y],fill=(230,230,230))
    if 0.3<=t<0.5:
        im=fade_to(im,(255,255,240),1-(t-0.3)/0.2); d=ImageDraw.Draw(im)
    if req:
        rr=random.Random(f)
        for _ in range(10): d.point((rr.randint(50,134),rr.randint(0,63)),fill=(255,240,170))
    if t>=0.55:
        big_text(im,"GOLD EXPERIENCE",2,(255,255,255),scale=1)
        big_text(im,"REQUIEM",44,GOLD,scale=3,outline=(120,60,20))
    if t<0.06: zoom_lines(d,GOLD)
    if t>0.92: im=fade_to(im,(0,0,0),(t-0.92)/0.08*0.6)
    return im

# ---- the clip ------------------------------------------------------------------------------------
T_CU=100                                                           # the close-up
def clip_requiem(f):
    s=scene(f,THEME)
    cl=actor(GIO[guard_pose(f)],CX,pal=GIOPAL)
    dv=actor(dv_idle(f),VX,flip=True,pal=DVPAL)
    st=actor(GE['idle'],CX-6,GROUND-3,pal=GEPAL,alpha=ST_A,vis=False)        # Claude's Stand
    kc=actor(KC['idle'],VX+12,GROUND-3,flip=True,pal=KCPAL,alpha=ST_A,vis=False)
    if 8<=f<44 or 254<=f<272: s['under'].append(('jojo_menace',f))
    # 1) the Stands
    if 14<=f<60:
        a=min(1,(f-14)/10); st.update(vis=True,alpha=ST_A*a,y=GROUND-int(3*a))
        if f<30: shout(s,"GOLD EXPERIENCE!",GOLD); cl['spr']=GIO['charge']
    if 28<=f<60:
        a=min(1,(f-28)/10); kc.update(vis=True,alpha=ST_A*a,y=GROUND-int(3*a))
        if 30<=f<46: shout(s,"KING CRIMSON!",RED); dv['spr']=DV['attack']
    if 46<=f<60:                                                    # Gold Experience lunges
        st.update(spr=GE['attack'],x=ez(CX-6,70,(f-46)/8))
    # 2) time is erased: Diavolo walks through it, King Crimson strikes; Claude never sees it
    if 60<=f<64: banner(s,"KING CRIMSON!",20,RED,2,(60,0,10)); s['flash']=0.5; s['fc']=(VX,GROUND-14); s['flashc']=(255,60,80)
    if 60<=f<82:
        st.update(vis=True,spr=GE['attack'],x=70)                   # frozen mid-lunge
        t=(f-64)/14; x=ez(VX,56,t) if f>=64 else VX
        dv.update(spr=DV['idle'],x=x,alpha=0.85); kc.update(vis=True,x=x+10,alpha=0.5)
        if f>=64:
            for k in (1,2,3): s['under'].append(('jojog_ghost',DV['idle'],x+k*8,True,0.25/k,DVPAL))
        if 74<=f<80: kc.update(spr=KC['attack'],x=x-6)
        s['fx'].append(('jojog_erase',0.6 if f<64 else 1.0,f))
        if 66<=f<80: shout(s,"TIME HAS BEEN ERASED!",RED,y=4)
    if f==82: s['shake']=rshake(3); s['fx'].append(('spark',CX+4,GROUND-10,8)); s['flash']=0.4; s['fc']=(CX,GROUND-10); s['flashc']=(255,60,80)
    if 82<=f<T_CU:                                                  # it already happened
        t=(f-82)/6; cl.update(spr=GIO['hurt'],x=ez(CX,16,t))
        st.update(vis=True,spr=GE['hurt'],x=ez(70,10,t))
        dv.update(spr=DV['idle'],x=56); kc.update(vis=True,spr=KC['attack'] if f<88 else KC['idle'],x=50)
        s['fx'].append(('dmg','50',34,GROUND-26-(f-82)//3,RED))
        if f>=88: shout(s,"!?",(255,255,255),y=GROUND-30,x=12)
    # 3) the Arrow: REQUIEM
    if T_CU<=f<T_CU+40: s['image']=closeup_requiem((f-T_CU)/40,f); return s
    if T_CU+40<=f<214:                                              # Requiem stays behind Claude
        st.update(vis=True,spr=GER['idle'],pal=GERPAL,x=CX-6,alpha=0.8)
        s['fx'].append(('jojog_gleam',CX-6,GROUND-12))
    if T_CU+40<=f<160: dv.update(x=ez(56,VX-20,(f-140)/10)); kc.update(vis=True,x=dv['x']+10)
    # 4) King Crimson again — the erased time is returned to zero
    if 160<=f<176:
        dv.update(x=VX-20,spr=DV['attack']); kc.update(vis=True,x=VX-10,spr=KC['attack'])
        if f<166: shout(s,"KING CRIMSON!",RED)
        if 162<=f<170: s['fx'].append(('jojog_erase',1-(f-162)/8,f))     # it starts... and unwinds
        if f>=166: shout(s,"RETURN TO ZERO.",GOLD,y=10)
    if 170<=f<180: shout(s,"!?",(255,255,255),y=GROUND-30,x=VX-26)
    # 5) MUDA MUDA MUDA
    if 176<=f<210:
        hit=(f//2)%2; sx=ez(CX-6,VX-40,(f-176)/6)
        st.update(spr=GER['attack' if hit else 'idle'],x=sx)
        dv.update(spr=DV['hurt'],x=VX-20+(1 if hit else -1)); kc.update(vis=f<186,spr=KC['hurt'],x=VX-6,alpha=ST_A*max(0,1-(f-176)/10))
        if f>=182:
            s['fx'].append(('jojo_fists',VX-34,VX-16,GROUND-22,GROUND-6,MUDA_C,1,10,f*13))
            rr=random.Random(f*5); s['fx'].append(('spark',VX-20+rr.randint(-4,4),GROUND-rr.randint(6,20),rr.choice((2,3))))
            if f%3==0: s['shake']=rshake()
            banner(s,"MUDA MUDA MUDA!",4,GOLD,2,(120,60,20))
            s['fx'].append(('dmg',str(10+(f-182)*7),VX-12+(f%3)*4,GROUND-34-(f%4),(255,236,150)))
    if f==210: s['flash']=0.6; s['fc']=(VX-20,GROUND-12); s['flashc']=(255,240,190); s['shake']=rshake(3)
    if 210<=f<222:                                                  # the last MUDA!
        t=(f-210)/12; dv.update(spr=rotate90(DV['hurt'],(f//2)%4),x=lerp(VX-20,210,t),y=int(lerp(GROUND,-10,t)))
        st.update(spr=GER['attack'],x=VX-40)
        if f<216: banner(s,"MUDA!",18,GOLD,3,(120,60,20))
    # 6) he never reaches death: the fall restarts, again and again
    if 222<=f<246:
        k=(f-222)%8; dv.update(spr=DV['hurt'],x=VX,y=int(lerp(-6,GROUND-8,k/7)))
        if k==7: s['flash']=0.3; s['fc']=(VX,GROUND-8); s['flashc']=(255,255,255)
    if 246<=f<254: dv.update(spr=DV['hurt'],x=VX,y=int(ez(-6,GROUND,(f-246)/6)))
    if f==252: s['fx'].append(('dust',VX-6,GROUND-1)); s['fx'].append(('dust',VX+6,GROUND-1)); s['shake']=rshake()
    if 254<=f<262: dv.update(spr=DV['down'],x=VX)
    if 262<=f<268: dv['spr']=DV['hurt']
    if 214<=f<258:                                                  # ARRIVEDERCI.
        cl.update(spr=GIO['charge'] if f<250 else GIO[guard_pose(f)],x=CX)
        banner(s,"ARRIVEDERCI.",22,GOLD,2,(120,60,20))
        a=max(0,1-(f-238)/16) if f>=238 else 0.8
        st.update(vis=a>0,spr=GER['idle'],pal=GERPAL,x=CX-6,alpha=a)
        if f<238: s['fx'].append(('jojog_gleam',CX-6,GROUND-12))
    s['actors']=[st,kc,cl,dv]
    return s

CLIPS = [clip('requiem', N_, clip_requiem)]
