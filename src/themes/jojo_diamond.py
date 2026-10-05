"""JoJo's Bizarre Adventure: Diamond is Unbreakable (sub-theme of `jojo`). Claude is Josuke (the
huge black pompadour, the dark school uniform with the heart and peace pins) with Crazy Diamond,
in a quiet Morioh street; Yoshikage Kira (lilac suit, skull tie) and Killer Queen. "MY NAME IS
YOSHIKAGE KIRA...": Killer Queen flicks a coin, CLICK, it blows up at Claude's feet. Sheer Heart
Attack rolls out (LOOK HERE!); Crazy Diamond punches it into the wall, which blows a hole in it.
Kira mocks the hair: the rage close-up (WHAT DID YOU SAY ABOUT MY HAIR?!), DORARARARA, Kira bleeds
on the street. Crazy Diamond repairs the wall, and the blood drops fly back into Kira as bullets:
he flies off. Everything is fixed; Kira walks back to his spot."""
import zlib
from engine import *
from themes.jojo import _stand, ST_A, MENACE, _go

THEME = 'jojo-diamond'
N_ = 288
CX, VX = 30, 150                                                   # the neutral pose: Claude, Kira

# ---- Claude as Josuke: the pompadour out front, the dark uniform, the pins ---------------------
def _josuke(spr):
    spr=paint(spr,[],left=3,right=3)                                # room for the pompadour
    t,l,r=body_box(spr); g=grid(spr); h=len(g)
    bot=max(y for y in range(h) if 'O' in spr[y])
    coat=max(bot-3,max(y for y in range(h) if 'K' in spr[y])+2)
    for y in range(h):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y>=coat and l<=x<=r: g[y][x]='u'           # the gakuran
            elif c=='o' and y>=coat-1: g[y][x]='u'
    if coat<h:                                                      # the pins on the collar: heart, peace
        g[coat][r-1]='n'; g[coat][l+1]='y'
    return overlay(ungrid(g),["....kkkkkkk...","..kkkkkkkkkkkk",".kkkkkkkkkkkkkk",".kkkkkkkkkkkkk.","kkkkkkkk......."],-2,0,bangs="kkkkk")
JOSUKE=variant(_josuke)
JOPAL={'k':(26,22,34),'u':(44,40,78),'n':(240,110,160),'y':(250,220,70)}

# ---- the Stands --------------------------------------------------------------------------------
CD=_stand({'h':'n','E':'c','b':'n','c':'L','f':'L','a':'Y'},'nnnnLL')             # Crazy Diamond
CDPAL={'n':(232,150,196),'L':(70,120,220),'c':(80,230,230),'Y':(250,210,90)}
def _ears(spr): return paint(spr,[(4,-2,'n....n'),(4,-1,'nn..nn')],top=2)
KQ={k:_ears(v) for k,v in _stand({'h':'n','E':'k','b':'n','c':'k','f':'n','a':'H'},'nnnnnn').items()}
KQPAL={'n':(240,180,206),'k':(40,24,40),'H':(240,240,240)}           # Killer Queen: cat ears, skull belt
CD_C=((232,150,196),(70,120,220))                                   # Crazy Diamond's fists

# ---- Yoshikage Kira ----------------------------------------------------------------------------
_KIRA=S([
"....yyyyyy......",
"...yyyyyyyy.....",
"..yyysyyyyyy....",
"..yyssssssy.....",
"..yysskssks.....",
"...ysssssss.....",
"....sssmss......",
".....ssss.......",
"...VVVHWHVV.....",
"..VVVVHkHVVV....",
"..VVVVVkVVVV....",
"..VV.VHkHV.VV...",
"..VV.VVkVV.VV...",
"..ss.VVVVV.ss...",
".....VVVVV......",
".....VV.VV......",
".....VV.VV......",
".....VV.VV......",
".....VV.VV......",
"....kkk.kkk.....",])
KIRA=poses(_KIRA,9,'s',3)
KIRA['idle2']=S(_KIRA[:13]+[".....VVVVV......"]+_KIRA[14:])
KIRA['down']=rotate90(KIRA['hurt'],3,trim=True)
KIRAPAL={'y':(244,222,130),'s':(246,214,184),'k':(30,24,34),'m':(170,90,90),'V':(170,140,200),
         'H':(244,244,250),'W':(240,240,240)}
def kira_idle(f): return KIRA['idle'] if (f//8)%2==0 else KIRA['idle2']

# Sheer Heart Attack: the little tank with the skull face
SHA=S([
"..kkkkk..",
".kDDDDDk.",
"kDHkDkHDk",
"kDDDDDDDk",
"kDkHkHkDk",
"kkkkkkkkk",
"kdkdkdkdk",])
SHAPAL={'D':(150,150,160),'d':(80,80,90),'H':(240,240,240),'k':(30,30,36)}

# ---- background: a Morioh street at dusk -------------------------------------------------------
WALL=(70,112,GROUND-15)                                             # the stone wall Crazy Diamond fixes
def _morioh(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(54+40*k),int(30+24*k),int(56+10*k)))
    d.ellipse([20,30,36,46],fill=(240,170,110))                     # the low sun
    for x0,x1,top,roof in ((0,40,30,(46,30,44)),(118,160,28,(50,32,48)),(158,185,34,(46,30,44)),(40,72,36,(52,34,50))):
        d.rectangle([x0,top,x1,GROUND],fill=(70,50,64))
        d.polygon([(x0-3,top+1),(x0+4,top-6),(x1-4,top-6),(x1+3,top+1)],fill=roof)
        for wx in range(x0+4,x1-4,9): d.rectangle([wx,top+5,wx+4,top+9],fill=(250,210,140))
    for x in (60,140):                                              # telephone poles and wires
        d.line([x,8,x,GROUND],fill=(40,28,40)); d.line([x-4,11,x+4,11],fill=(40,28,40))
    d.line([0,13,60,11],fill=(40,28,40)); d.line([60,11,140,11],fill=(40,28,40)); d.line([140,11,W,13],fill=(40,28,40))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(40,30,40))
register_bg(THEME, lambda v: (v+20,v//2+12,v//2+20), decor=_morioh)

def _brick(i):
    x0,x1,top=WALL; rr=random.Random(zlib.crc32(b'brick')+i)
    return rr.randint(84,98),rr.randint(top+2,top+10),rr.uniform(-2.5,2.5),rr.uniform(-2.4,-0.6)

@fx('jojod_wall')
def _fx_wall(d,im,e,f):
    """The stone wall; hole 0..1 is the blown-out gap (pieces flying out or back are separate)."""
    _,hole=e; x0,x1,top=WALL
    d.rectangle([x0,top,x1,GROUND-1],fill=(118,112,108),outline=(70,64,64))
    for y in range(top+3,GROUND,4):
        for x in range(x0+(y//4%2)*3,x1,6): d.line([x,y,x,y+3],fill=(84,78,78))
        d.line([x0,y,x1,y],fill=(84,78,78))
    if hole>0:
        r=10*hole; cx,cy=91,top+7
        pts=[(cx+math.cos(a/8*math.tau)*r*(0.8+0.25*(a%2)),cy+math.sin(a/8*math.tau)*r*0.7*(0.8+0.25*(a%2))) for a in range(8)]
        if r>=1: d.polygon(pts,fill=(80,56,74),outline=(60,52,52))

@fx('jojod_blast')
def _fx_blast(d,im,e,f):
    """A Killer Queen explosion, t frames old: pink-white core, orange puffs, then smoke."""
    _,x,y,t,size=e; rr=random.Random(zlib.crc32(b'kq-blast')+int(x))
    for j in range(10):
        a=rr.random()*math.tau; dist=rr.random()*(2+t*size*0.5); r=int((2+rr.randint(0,3)+min(t,6)*0.5)*size/3)
        px,py=x+math.cos(a)*dist,y+math.sin(a)*dist*0.7-t*0.5
        c=[(255,240,250),(255,170,200),(250,130,60)][min(2,(j+t)//4)] if t<6 else (int(110-t*4),int(90-t*4),int(100-t*4))
        if r>0: d.ellipse([px-r,py-r,px+r,py+r],fill=c)

@fx('jojod_piece')
def _fx_piece(d,im,e,f):
    _,x,y=e; d.rectangle([x,y,x+1,y+1],fill=(118,112,108))

@fx('jojod_drop')
def _fx_drop(d,im,e,f):
    """A blood drop: on the ground, or flying (a short streak)."""
    _,x,y,dx=e; x,y=int(x),int(y)
    if dx: d.line([x-dx*4,y,x,y],fill=(120,10,20))
    d.rectangle([x,y,x+1,y],fill=(200,20,30))

@fx('jojod_coin')
def _fx_coin(d,im,e,f):
    _,x,y,hot=e; x,y=int(x),int(y)
    d.ellipse([x-1,y-1,x+1,y+1],fill=(255,120,160) if hot else (240,210,90))
    if hot: d.point((x,y-3),fill=(255,180,210))

@fx('jojod_menace')
def _fx_menace(d,im,e,f):
    """ゴゴゴ in Crazy Diamond pink."""
    for i,(x,y) in enumerate(MENACE):
        ph=(f+i*4)%12; _go(d,x+(1 if ph in (2,3) else 0),y-(1 if ph<6 else 0),(250,150,200) if ph<6 else (180,80,140))

@fx('jojod_heal')
def _fx_heal(d,im,e,f):
    """Crazy Diamond's restoration glow: little sparkles over a box."""
    _,x0,y0,x1,y1=e; rr=random.Random(f)
    for _ in range(6): d.point((rr.randint(x0,x1),rr.randint(y0,y1)),fill=rr.choice([(255,200,230),(140,240,255)]))

# ---- close-up: the rage -------------------------------------------------------------------------
def closeup_hair(t,f):
    """Josuke's face, the pompadour filling the top, the eyes go blank with rage."""
    im=Image.new('RGB',(W,H),(40,14,40)); d=ImageDraw.Draw(im)
    for i in range(14):                                             # speed lines
        a=i*0.45+f*0.05; d.line([92,30,92+math.cos(a)*140,30+math.sin(a)*80],fill=(70,24,70))
    skin,shade=(217,119,87),(176,92,66)
    d.polygon([(52,20),(132,20),(130,56),(112,70),(72,70),(54,56)],fill=skin)
    d.polygon([(52,20),(60,20),(62,58),(72,70),(54,56)],fill=shade)
    hair=(26,22,34); hl=(76,70,110)
    d.ellipse([44,-12,182,26],fill=hair)                            # the pompadour, out over the brow
    d.polygon([(48,22),(50,2),(70,-2),(60,26)],fill=hair)
    for k in range(3): d.arc([62+k*12,-4+k*5,176-k*8,24-k],200,330,fill=hl)
    d.rectangle([54,20,130,24],fill=hair)
    rage=t>=0.3
    for ex in (74,108):
        d.polygon([(ex-12,36),(ex+10,34),(ex+9,42),(ex-11,43)],fill=(250,250,250))
        if not rage: d.rectangle([ex-2,37,ex+2,41],fill=(40,30,60))
        else: d.point((ex,38),fill=(0,0,0))
    if rage:
        d.line([(62,30),(84,34)],fill=(40,20,20),width=2); d.line([(98,34),(120,30)],fill=(40,20,20),width=2)
        jx=(f%3)-1
        for vx,vy in ((140,26),(46,30)):                             # the anger marks
            d.line([vx-4+jx,vy,vx+4+jx,vy],fill=(230,30,40),width=2); d.line([vx+jx,vy-4,vx+jx,vy+4],fill=(230,30,40),width=2)
        d.polygon([(80,56),(104,56),(100,62),(84,62)],fill=(60,10,20)); d.line([(82,57),(102,57)],fill=(250,250,250))
    else: d.line([(84,58),(100,58)],fill=shade)
    if t>=0.3:
        d.rectangle([0,H-9,W,H],fill=(0,0,0)); text(d,"WHAT DID YOU SAY ABOUT MY HAIR?!",W//2-64,H-7,(255,140,190))
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

# ---- the clip ----------------------------------------------------------------------------------
COIN0=(132,GROUND-20); COIN1=(48,GROUND-1)
SHA_HIT=104                                                         # Crazy Diamond punches it into the wall
DROPS=[(108+i*5+(i%2)*2,GROUND-1) for i in range(6)]                 # where Kira's blood lands

def clip_kira(f):
    s=scene(f,THEME)
    cl=actor(JOSUKE[guard_pose(f)],CX,pal=JOPAL)
    ki=actor(kira_idle(f),VX,flip=True,pal=KIRAPAL)
    cd=actor(CD['idle'],CX-6,GROUND-3,alpha=ST_A,vis=False,pal=CDPAL)
    kq=actor(KQ['idle'],VX+12,GROUND-3,flip=True,alpha=ST_A,vis=False,pal=KQPAL)
    extra=[]
    # the wall: whole, blown out at SHA_HIT+12, repaired from 224
    hole=0 if f<SHA_HIT+12 else (1 if f<224 else max(0,1-(f-224)/12))
    s['under'].append(('jojod_wall',hole))
    if 4<=f<28 or 268<=f<284: s['under'].append(('jojod_menace',))
    # 1) MY NAME IS YOSHIKAGE KIRA, Killer Queen, the coin
    if 8<=f<40: callout(s,"MY NAME IS YOSHIKAGE KIRA...",y=2,c=(200,170,240))
    if 24<=f<84:
        kq.update(vis=True,alpha=ST_A*min(1,(f-24)/8))
    if 40<=f<56:
        kq['spr']=KQ['attack'] if f<44 else KQ['idle']
        t=(f-40)/16; x=lerp(COIN0[0],COIN1[0],t); y=lerp(COIN0[1],COIN1[1],t)-14*math.sin(math.pi*t)
        s['fx'].append(('jojod_coin',x,y,f>=50))
    if 56<=f<64: s['fx'].append(('jojod_coin',*COIN1,True)); callout(s,"CLICK",y=2,c=(255,150,200))
    if 58<=f<64: kq['spr']=KQ['attack']
    if f==64: s['flash']=0.7; s['fc']=COIN1; s['flashc']=(255,220,200); s['shake']=rshake(3)
    if 64<=f<74:
        s['fx'].append(('jojod_blast',COIN1[0],COIN1[1]-4,f-64,3))
        s['fx'].append(('big',"BOOM!",14,(255,200,120)))
        cl.update(spr=JOSUKE['hurt'],x=ez(CX,18,(f-64)/6))
    if 74<=f<84: cl.update(spr=JOSUKE['guard'],x=ez(18,CX,(f-74)/10))
    if 84<=f<92: kq.update(vis=True,alpha=ST_A*(1-(f-84)/8))
    # 2) Sheer Heart Attack rolls in; Crazy Diamond punches it into the wall
    if 76<=f<96: cd.update(vis=True,alpha=ST_A*min(1,(f-76)/8))
    if 80<=f<SHA_HIT:
        x=lerp(VX-14,CX+30,(f-80)/(SHA_HIT-80)); extra.append(actor(SHA,x,GROUND-(f//2)%2,flip=True,pal=SHAPAL))
        if f<98: callout(s,"LOOK HERE!",y=2,c=(230,230,240))
        s['fx'].append(('dust',x+5,GROUND-1))
    if 96<=f<SHA_HIT+4: cd.update(vis=True,x=ez(CX-6,CX+16,(f-96)/4),spr=CD['attack'] if f>=SHA_HIT-2 else CD['idle'])
    if SHA_HIT<=f<SHA_HIT+12:
        t=(f-SHA_HIT)/12; extra.append(actor(rotate90(SHA,(f//2)%4),lerp(CX+30,91,t),int(lerp(GROUND,WALL[2]+10,t)-14*math.sin(math.pi*t)),pal=SHAPAL))
        if f<SHA_HIT+3: s['fx'].append(('spark',CX+30,GROUND-6,5)); callout(s,"DORA!",y=2,c=(250,150,200))
    if f==SHA_HIT+12: s['flash']=0.7; s['fc']=(91,WALL[2]+7); s['shake']=rshake(3)
    if SHA_HIT+12<=f<SHA_HIT+24:
        t=f-SHA_HIT-12; s['fx'].append(('jojod_blast',91,WALL[2]+7,t,4))
        for i in range(10):
            x,y,vx,vy=_brick(i); s['fx'].append(('jojod_piece',x+vx*t,y+vy*t+0.25*t*t))
    if SHA_HIT+4<=f<130: cd.update(vis=True,x=ez(CX+16,CX-6,(f-SHA_HIT-4)/8),alpha=ST_A*max(0,1-max(0,f-122)/8))
    # 3) Kira mocks the hair: the close-up
    if 128<=f<148:
        callout(s,"WHAT A RIDICULOUS HAIRDO.",y=2,c=(200,170,240)); ki['spr']=KIRA['attack']
    if 148<=f<180: s['image']=closeup_hair((f-148)/32,f); return s
    # 4) DORARARARA
    if 180<=f<190:
        cl['aura']=((250,150,200),1+(f%2)); cd.update(vis=True,x=ez(CX-6,108,(f-180)/8),spr=CD['idle'],alpha=0.8)
        cl.update(x=ez(CX,92,(f-180)/10),spr=JOSUKE['dash'])
    if 190<=f<212:
        hit=(f//2)%2; cl.update(x=92,spr=JOSUKE['punch'])
        cd.update(vis=True,x=118,spr=CD['attack' if hit else 'idle'],alpha=0.8)
        s['fx'].append(('jojo_fists',124,140,GROUND-24,GROUND-8,CD_C,1,10,f*13))
        rr=random.Random(f*7); s['fx'].append(('spark',138+rr.randint(0,6),GROUND-rr.randint(8,22),rr.choice((2,3))))
        ki.update(spr=KIRA['hurt'],x=VX-4+hit*2); s['shake']=rshake() if f%2 else (0,0)
        s['fx'].append(('big',"DORARARARA!",22,(250,150,200)))
        for i,(dx,dy) in enumerate(DROPS):                          # the blood flies out and lands
            t=min(1,(f-196-i)/6)
            if t>0: s['under'].append(('jojod_drop',lerp(VX-6,dx,t),lerp(GROUND-14,dy,t)-6*math.sin(math.pi*t),0))
    if 212<=f<224:
        ki.update(spr=KIRA['hurt'],x=ez(VX-4,VX+4,(f-212)/6)); cl.update(x=ez(92,CX+20,(f-212)/10),spr=JOSUKE[guard_pose(f)])
        cd.update(vis=True,x=ez(118,CX+8,(f-212)/10),alpha=0.8)
        for dx,dy in DROPS: s['under'].append(('jojod_drop',dx,dy,0))
    # 5) Crazy Diamond fixes the wall... and the blood flies back into Kira
    if 224<=f<246:
        cl.update(x=CX+20,spr=JOSUKE['armsup'] if f<236 else JOSUKE[guard_pose(f)]); cd.update(vis=True,x=CX+8,spr=CD['attack'] if f<236 else CD['idle'],alpha=0.8)
    if 224<=f<236:
        t=(f-224)/12; s['fx'].append(('jojod_heal',WALL[0],WALL[2],WALL[1],GROUND-2))
        for i in range(10):
            x,y,vx,vy=_brick(i); tt=(1-t)*12; s['fx'].append(('jojod_piece',x+vx*tt,y+vy*tt+0.25*tt*tt))
        if f<232: callout(s,"CRAZY DIAMOND!",y=2,c=(250,150,200))
    if 224<=f<230:
        for dx,dy in DROPS: s['under'].append(('jojod_drop',dx,dy-(f-224),0))
    if 230<=f<236:
        t=(f-230)/6; ki['spr']=KIRA['hurt']
        for i,(dx,dy) in enumerate(DROPS): s['fx'].append(('jojod_drop',lerp(dx,VX+2,t),lerp(dy-6,GROUND-12+i%3*3,t),1))
    if f==236: s['flash']=0.4; s['fc']=(VX,GROUND-12); s['flashc']=(255,120,140); s['shake']=rshake(2)
    if 236<=f<252:
        t=(f-236)/14; ki.update(spr=KIRA['hurt'],x=ez(VX+4,215,t),y=GROUND-int(14*math.sin(math.pi*min(1,t))))
        if f<246: s['fx'].append(('spark',ki['x']-6,ki['y']-12,4)); callout(s,"NANI?!",y=2,c=(200,170,240))
    if 246<=f<262: cd.update(vis=True,x=CX+8,alpha=0.8*max(0,1-(f-246)/12))
    if 246<=f<262: cl.update(x=ez(CX+20,CX,(f-246)/12))
    if 252<=f<268: ki['vis']=False
    # 6) Kira walks back to his spot
    if 268<=f<284: ki.update(vis=True,spr=kira_idle(f),x=ez(200,VX,(f-268)/14),y=GROUND-((f//3)%2) if f<282 else GROUND)
    s['actors']=[kq,cd,ki,cl]+extra
    return s

CLIPS = [clip('kira', N_, clip_kira)]
