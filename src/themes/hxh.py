"""Hunter x Hunter: Claude (Gon) vs Neferpitou. Fishing-rod whip, Terpsichora, then the close-up:
Claude's eyes go dark, the hair grows to the ceiling — adult form, "JAN KEN... GU!"."""
from engine import *

THEME = 'hxh'

GON=variant(lambda s: recolor_rows(overlay(s,["..g...g...g.",".gg..ggg.gg.",".ggggggggggg","gggggggggggg"],-2,0),
    lambda x,y,t,l,r,c: 'X' if (y==t+8 and l<=x<=r and c in 'oO') else None))

def _adult(pose,sway=0):
    """Adult Gon (Claude grown up): stern orange face, bare torso, green shorts, and a jet-black mane
    — big jagged spikes on top, falling behind him past the knees in flowing strands (to the left)."""
    T=6; w,h=30,42+T; g=[['.']*w for _ in range(h)]   # T rows of headroom for the spikes
    def put(x,y,c):
        if 0<=x<w and 0<=y+T<h: g[y+T][x]=c
    lean=2 if pose=='dash' else 0
    for tx,ty,bw in ((10,-6,3),(15,-2,2),(5,-3,3),(19,3,2),(1,3,3),(13,-5,2),(8,-1,2)):   # the spikes, tips up/back
        for y in range(ty,11):
            half=(y-ty)*bw//6
            for x in range(tx-half,tx+half+1): put(x+lean,y,'S')
    for y in range(8,37):                                                  # the mane behind him
        k=(y-8)/28; l=int(7-8*k)-(sway if y>20 else 0); r=int(19-5*k)
        for x in range(l,r+1):
            if y>30 and (x*5+sway)%4==0 and y>31+(x%3): continue            # ragged strand ends
            put(x+(lean if y<16 else 0),y,'g' if (x+y//4+sway)%5==0 and y>12 else 'S')
    for x0 in (1,4):                                                       # loose strands at the side
        for y in range(18,36): put(x0-(y-18)//6-sway,y,'S')
    L=11+lean                                                              # face block, eyes, brow
    for y in range(8,15):
        for x in range(L,L+9): put(x,y,'O')
    for x in range(L+1,L+9): put(x,7,'S')                                  # fringe
    put(L+2,8,'S'); put(L+5,8,'S'); put(L+8,8,'S')
    for x,y in ((L+4,10),(L+5,10),(L+7,10),(L+8,10)): put(x,y,'K')         # stern slanted brows
    for x in (L+5,L+8): put(x,11,'K'); put(x,12,'K')
    for x in range(L+5,L+8): put(x,13,'o')                                 # set jaw
    body=L+(1 if pose=='dash' else 0)
    for y in range(15,26):                                                 # neck + muscular torso
        for x in range(body,body+9): put(x,y,'O')
    for x in (body,body+8): put(x,15,'.')
    for x in range(body+1,body+8): put(x,19,'o') if x!=body+4 else None    # pecs
    for y in (21,23): put(body+3,y,'o'); put(body+5,y,'o')                 # abs
    put(body+4,20,'o'); put(body+4,22,'o'); put(body+4,24,'o')
    for y in range(26,30):                                                 # green shorts
        for x in range(body-1,body+10): put(x,y,'X')
    for y in range(30,40):                                                 # long legs
        st=(y-30)//4 if pose=='dash' else (y-30)//5
        for x in range(body+1-st,body+4-st): put(x,y,'O')
        for x in range(body+5+st,body+8+st): put(x,y,'O')
    for x in range(body-2,body+4): put(x-(2 if pose=='dash' else 1),40,'o'); put(x-(2 if pose=='dash' else 1),41,'o')
    for x in range(body+5,body+11): put(x+(2 if pose=='dash' else 1),40,'o'); put(x+(2 if pose=='dash' else 1),41,'o')
    ax0,ax1=body-2,body+9                                                  # arms
    if pose in ('guard','guard2'):
        for y in range(16,26): put(ax0,y,'O'); put(ax0+1,y,'o'); put(ax1,y,'O'); put(ax1+1,y,'O')
        for y in (26,27): put(ax0,y,'o'); put(ax1+1,y,'o'); put(ax1,y,'o')
    elif pose=='charge':                                                   # fist drawn back at the hip
        for y in range(16,23): put(ax0,y,'O'); put(ax1,y,'O')
        for x in range(ax1,ax1+5): put(x,22,'O'); put(x,23,'O')
        for x in range(ax1+3,ax1+7): put(x,20,'o'); put(x,21,'O'); put(x,24,'o')
    else:                                                                  # punch / dash: arm fully out
        for y in range(16,24): put(ax0,y,'O'); put(ax0+1,y,'o')
        for x in range(ax1,w-2): put(x,17,'O'); put(x,18,'O')
        for y in (16,17,18,19):
            for x in (w-3,w-2,w-1): put(x,y,'O' if y in (17,18) else 'o')
    return S([''.join(r) for r in g])
ADULT={k:_adult(k,sway=1 if k=='guard2' else 0) for k in ('guard','guard2','charge','punch','dash')}
ADULT_PAL={'S':(8,8,12),'g':(44,50,72)}          # jet-black hair, cold blue sheen (never green)

PITOU=poses(S([
"....H.....H.....","....HH...HH.....","....HHHHHHH.....","...HHHHHHHHH....","...HHssssHHH....",
"...HsrssrsHH....","...HssssssH.....","....ssnss.......",".....ssss.......","....WWWWWW......",
"...WWWWWWWW.....","...ss.WWWW.ss...","...ss.WWWW.ss...","H....NNNNNN.....","HH...NNNNNN.....",
".HH..NN..NN.....","..HH.ss..ss.....","...H.ss..ss.....",".....ss..ss.....","....kkk..kkk....",]),11,'ss',3)

# ---- background: East Gorteau — the palace beyond the jungle, and the torn-up clearing ----------
def _gorteau(d):
    for y in range(GROUND+1):                                        # pre-dawn sky, green-teal haze low
        k=y/GROUND; d.line([0,y,W,y],fill=(int(8+14*k),int(12+26*k),int(24+18*k)))
    rr=random.Random(2011)
    for _ in range(18): d.point((rr.randint(0,W-1),rr.randint(0,16)),fill=rr.choice([(70,90,110),(130,150,160)]))
    d.ellipse([22,5,32,15],fill=(196,210,200)); d.point((25,8),fill=(170,186,178)); d.point((28,12),fill=(170,186,178))
    far=(22,36,40)                                                    # the palace on its hill, far away
    d.polygon([(70,40),(96,30),(140,29),(168,40)],fill=far)
    pal=(30,44,50)
    d.rectangle([96,22,142,31],fill=pal); d.rectangle([108,16,130,23],fill=pal)
    d.ellipse([112,8,126,20],fill=pal); d.line([119,3,119,9],fill=pal)               # the great dome and spire
    for tx in (98,138):
        d.rectangle([tx-2,12,tx+2,24],fill=pal); d.polygon([(tx-3,12),(tx,7),(tx+3,12)],fill=pal)
    for x in range(100,140,4): d.point((x,27),fill=(90,100,70) if rr.random()<0.3 else (40,56,60))
    for x in range(-4,W+6,5):                                         # jungle treeline, two depths
        h=rr.randint(6,12); d.ellipse([x-5,40-h,x+5,48],fill=(14,32,22))
    for x in range(-4,W+6,7):
        h=rr.randint(3,8); d.ellipse([x-6,46-h,x+6,52],fill=(10,24,16))
    d.rectangle([0,50,W,GROUND],fill=(30,26,20))                      # the clearing: churned earth
    for _ in range(60): d.point((rr.randint(0,W-1),rr.randint(50,GROUND)),fill=rr.choice([(44,38,28),(20,18,14)]))
    for x0,top in ((6,30),(68,40),(178,34)):                          # shattered trunks, splintered tops
        d.rectangle([x0-2,top,x0+2,GROUND],fill=(40,30,24)); d.line([x0+2,top,x0+2,GROUND],fill=(58,44,32))
        d.polygon([(x0-2,top),(x0-1,top-4),(x0,top+1),(x0+1,top-6),(x0+2,top)],fill=(80,64,46))
    d.line([56,GROUND-1,70,GROUND-4],fill=(46,34,26)); d.line([57,GROUND,71,GROUND-3],fill=(34,26,20))   # a felled log
    for x,w,h in ((96,8,5),(112,5,3),(170,6,4),(14,4,2)):                # boulders
        d.ellipse([x-w,GROUND-h*2,x+w,GROUND+1],fill=(54,54,52)); d.line([x-w+2,GROUND-h*2+1,x,GROUND-h*2+1],fill=(84,84,78))
    for x0,pts in ((80,[(0,0),(4,2),(7,1),(11,3)]),(132,[(0,0),(3,-1),(6,1),(10,0)])):   # ground cracks
        d.line([(x0+a,GROUND-1+b) for a,b in pts],fill=(14,12,10))
register_bg(THEME, lambda v: (v//2+30,v//2+24,v//3+16), decor=_gorteau)

@fx('hxh_crack')
def _fx_crack(d,im,e,f):
    """The ground splitting under adult Gon's nen: jagged cracks of length L out from (x)."""
    _,x,L=e; rr=random.Random(4)
    for sgn in (-1,1):
        for k in range(2):
            px,py=x,GROUND
            for j in range(int(L)):
                nx=px+sgn*rr.randint(2,4); ny=GROUND-rr.randint(0,2) if k==0 else GROUND-1-rr.randint(0,3)
                d.line([px,py,nx,ny],fill=(255,150,60) if j==int(L)-1 else (12,8,6)); px,py=nx,ny

def _puppet():
    """Terpsichora: the marionette that moves Pitou's body."""
    w,h=34,46; im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    body,dark,face=(170,120,220,255),(96,54,150,255),(236,226,240,255)
    d.polygon([(7,8),(3,0),(13,5),(17,0),(21,5),(31,0),(27,8)],fill=dark)
    d.ellipse([9,5,25,19],fill=face); d.point((13,11),fill=dark); d.point((20,11),fill=dark)
    d.arc([11,9,23,17],20,160,fill=(200,40,60,255))
    for x in range(12,23,2): d.point((x,15),fill=dark)
    d.polygon([(10,20),(24,20),(27,36),(7,36)],fill=body); d.line([(17,20),(17,36)],fill=dark)
    for sx in (1,-1):
        x0=17+sx*8; d.line([(x0,22),(x0+sx*8,30),(x0+sx*6,40)],fill=body,width=2)
        d.line([(17+sx*4,36),(17+sx*6,45)],fill=body,width=2)
    return im
PUPPET=_puppet()

@fx('hxh_nen')
def _fx_nen(d,im,e,f):
    """Adult Gon's nen: a soft orange glow hugging the silhouette, flickering, with flame licks
    rising off the top edges (drawn under the actor, so the glow sits AROUND him)."""
    _,spr,cx,feet,flip=e; w,h=len(spr[0]),len(spr); ox=int(round(cx-w/2)); oy=int(round(feet-h))
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    tops={}
    for y,row in enumerate(spr):
        for x,c in enumerate(row):
            if c!='.':
                X=ox+((w-1-x) if flip else x); md.point((X,oy+y),fill=255); tops.setdefault(X,oy+y)
    fl=0.75+0.25*math.sin(f*1.7)+(0.1 if f%3==0 else 0)
    glow=m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2.5)).point(lambda v: int(min(255,v*1.6*fl)))
    im.paste(Image.composite(Image.new('RGB',(W,H),(255,140,50)),im,glow))
    rr=random.Random(f)
    for X,Y in tops.items():
        if rr.random()<0.3:
            L=rr.randint(2,6); d.line([X,Y-2,X+rr.choice((-1,0,0,1)),Y-2-L],fill=(255,200,110) if L>4 else (255,140,50))

@fx('puppet')
def _fx_puppet(d,im,e,f):
    _,x,a=e; w,h=PUPPET.size; y=GROUND-h-6+int(2*math.sin(f*0.3))
    m=PUPPET.getchannel('A').point(lambda v: int(v*a*0.75))
    im.paste(PUPPET.convert('RGB'),(int(x)-w//2,y),m)
    for dx in (-10,0,10): d.line([x+dx,y+22,x+dx//3,GROUND-12],fill=(120,80,170))

@fx('claw')
def _fx_claw(d,im,e,f):
    _,x,y=e
    for k in range(3): d.line([x-4+k*3,y-6,x+k*3,y+4],fill=(255,220,235) if k!=1 else (255,255,255))

@fx('rod')
def _fx_rod(d,im,e,f):
    _,x0,y0,x1,y1=e
    d.line([x0,y0,x0+6,y0-8],fill=(150,100,60))
    d.line([x0+6,y0-8,x1,y1],fill=(220,220,230))
    d.rectangle([x1-1,y1-1,x1+1,y1],fill=(230,50,50)); d.point((x1,y1+1),fill=(255,255,255))

def closeup_gon(t,f):
    """Primer plano: Claude's face goes dark, the eyes empty, and the hair grows out of the frame."""
    im=Image.new('RGB',(W,H),(217,119,87)); d=ImageDraw.Draw(im)
    for x in range(0,W,6): d.line([x,56,x+3,64],fill=(168,80,54))
    hollow=ease((t-0.25)/0.25)
    for ex in (74,118):
        ew=int(5+3*hollow); d.rounded_rectangle([ex-ew,20,ex+ew,46],radius=3,fill=(10,4,4))
        if hollow<0.9: d.rectangle([ex-1,24,ex,26],fill=(255,255,255))
        elif (f//3)%3==0: d.point((ex,32),fill=(120,30,20))
    dark=0.65*ease((t-0.2)/0.4)
    if dark>0: im=fade_to(im,(20,6,4),dark); d=ImageDraw.Draw(im)
    g=ease((t-0.3)/0.5)   # the hair grows: bangs lengthen, side locks run down the frame
    mix=lambda a,b: tuple(int(lerp(a[i],b[i],g)) for i in range(3))   # green kid hair -> jet-black mane
    hc,hl=mix((52,118,44),(8,8,12)),mix((78,150,66),(44,50,72)); base=int(8+6*g)
    pts=[(0,0)]
    for x in range(0,W+14,14): pts+=[(x,base),(x+7,base+4+int(12*g))]
    d.polygon(pts+[(W,0)],fill=hc)
    for x in range(3,W,9): d.line([x,0,x+2,base],fill=hl)
    side=int(70*g)
    if side:
        for sx,sg in ((0,1),(W,-1)):
            p=[(sx,0)]+[(sx+sg*(14+(7 if (y//6)%2 else 0)),y) for y in range(0,side,6)]+[(sx,side)]
            d.polygon(p,fill=hc); d.line([(sx+sg*6,0),(sx+sg*8,side)],fill=hl)
    if t>0.4:   # heavy nen rising
        rr=random.Random(f)
        for _ in range(14):
            x=rr.randint(0,W); y=rr.randint(0,H); d.line([x,y,x,y-rr.randint(3,8)],fill=(255,150,60))
    if t>0.55: text(d,"JAN KEN...",W//2-20,50,(255,190,120))
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,(255,170,90),0.7*(t-0.9)/0.1)
    return im

def clip_jajanken(f):
    s=scene(f,THEME)
    cl=actor(GON[guard_pose(f)],30); pt=actor(PITOU['idle'],150,flip=True)
    # 1) Pitou pounces, Claude dodges and whips it back with the fishing rod
    if 12<=f<18: pt.update(spr=PITOU['hurt'],y=GROUND)   # crouch
    if 18<=f<30:
        t=(f-18)/12; pt.update(spr=PITOU['attack'],x=lerp(150,40,t),y=GROUND-18*math.sin(math.pi*t))
        if f>=26: s['fx'].append(('claw',42,GROUND-8))
    if 24<=f<32: cl.update(spr=GON['dash'],x=ez(30,14,(f-24)/6),flip=True)
    if 30<=f<36: pt.update(spr=PITOU['idle'],x=40)
    if 32<=f<46:
        cl.update(spr=GON['punch'],x=14); tx=lerp(22,40,min(1,(f-32)/4))
        s['fx'].append(('rod',20,GROUND-6,tx,GROUND-10))
        if f==36: s['fx'].append(('spark',40,GROUND-10,6)); s['shake']=rshake()
    if 36<=f<52: pt.update(spr=PITOU['hurt'],x=ez(40,150,(f-36)/16),y=GROUND-int(10*math.sin(math.pi*(f-36)/16)))
    if 46<=f<60: cl['x']=ez(14,30,(f-46)/12)
    # 2) Terpsichora: the puppet takes over and Pitou gets much faster
    if 60<=f<104:
        a=min(1,(f-60)/10); s['under'].append(('puppet',160,a))
        pt['spr']=PITOU['attack'] if f<72 else pt['spr']
    if 62<=f<80: callout(s,"TERPSICHORA",c=(200,160,255))
    if 76<=f<98:
        k=(f-76)//5; ph=(f-76)%5; hx=[48,20,52,18,50][k]
        pt.update(spr=PITOU['attack'],x=hx,flip=hx>30,vis=ph>0)
        if ph==0: s['fx'].append(('mote',hx+random.randint(-6,6),GROUND-random.randint(4,14),(220,190,255)))
        if ph==2: s['fx'].append(('claw',34,GROUND-7)); s['fx'].append(('spark',32,GROUND-8,4)); s['shake']=rshake()
        cl.update(spr=GON['hurt'],x=30-(2 if ph<3 else 0))
    if 98<=f<104: pt.update(spr=PITOU['idle'],x=ez(50,150,(f-98)/6)); cl.update(spr=GON['hurt'],x=26)
    # 3) close-up: the transformation
    if 104<=f<150: s['image']=closeup_gon((f-104)/46,f); return s
    # 4) adult form
    ad=None
    if 150<=f<232:
        cl['vis']=False; ad=actor(ADULT[guard_pose(f)],40,pal=ADULT_PAL)
        pt.update(spr=PITOU['hurt'] if f<200 else pt['spr'],x=150)
        s['under'].append(('hxh_crack',40,min(6,(f-150)/3)))
        if f<176:
            s['shake']=rshake(2) if f%3==0 else rshake()
            rr=random.Random(f//2)
            for j in range(6): s['fx'].append(('rock',rr.randint(10,120),GROUND-((f-150)*2+rr.randint(0,20))%40))
    if 176<=f<200:
        ad['spr']=ADULT['charge']; r=1+(f-176)//4
        s['fx'].append(('orbc',53,GROUND-20,r,((255,220,140),(255,140,40))))
        if f>=186: callout(s,"...GU!",c=(255,190,90)); s['shake']=rshake()
    if 200<=f<206: ad.update(spr=ADULT['dash'],x=lerp(40,128,(f-200)/6))
    if 206<=f<218:
        ad.update(spr=ADULT['punch'],x=128)
        if f==206: s['flash']=1.0; s['fc']=(144,GROUND-24); s['flashc']=(255,200,120)
        s['fx'].append(('boom',146,GROUND-24,int(4+(f-206)*4))); s['shake']=rshake(2)
    if 206<=f<226: pt.update(spr=PITOU['hurt'],x=lerp(150,230,(f-206)/10),y=GROUND-int(14*math.sin(math.pi*min(1,(f-206)/10))))
    if 218<=f<232: ad.update(spr=ADULT['guard'],x=128)
    # 5) the power is spent: back to normal, and the cat lands on its feet
    if 226<=f<236: pt['vis']=False
    if 230<=f<238:
        rr=random.Random(f)
        for j in range(8): s['fx'].append(('smoke',128+rr.randint(-8,8),GROUND-rr.randint(0,30),rr.randint(2,4),(236,236,240) if j%2 else (200,200,210)))
    if 232<=f<256: cl.update(vis=True,x=ez(128,30,(f-236)/20) if f>=236 else 128,spr=GON['hurt'] if f<236 else cl['spr'])
    if 236<=f<256:
        t=(f-236)/20; pt.update(spr=PITOU['idle'] if t>0.8 else PITOU['hurt'],x=lerp(210,150,ease(t)),y=GROUND-int(16*math.sin(math.pi*t)))
    if ad and ad['vis']: s['under'].append(('hxh_nen',ad['spr'],ad['x'],ad['y'],ad['flip']))
    s['actors']=[a for a in (cl,ad,pt) if a]
    return s

CLIPS = [clip('jajanken', 264, clip_jajanken)]
