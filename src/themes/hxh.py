"""Hunter x Hunter: Claude (Gon) vs Neferpitou. Fishing-rod whip, Terpsichora, then the close-up:
Claude's eyes go dark, the hair grows to the ceiling — adult form, "JAN KEN... GU!"."""
from engine import *

THEME = 'hxh'

GON=variant(lambda s: recolor_rows(overlay(s,["..g...g...g.",".gg..ggg.gg.",".ggggggggggg","gggggggggggg"],-2,0),
    lambda x,y,t,l,r,c: 'X' if (y==t+8 and l<=x<=r and c in 'oO') else None))

def long_hair(h=26,w=16):
    """Adult-form hair: three flame spikes (tips at different heights) merging into one mane."""
    spikes=[(w//2-4,6,0.34),(w//2,0,0.3),(w//2+4,3,0.34)]   # centre, tip row, widening per row
    rows=[]
    for j in range(h):
        row=''
        for x in range(w):
            on=any(j>=t and abs(x-c)<=(j-t)*k+(1 if (j+x)%5==0 else 0) for c,t,k in spikes)
            row+=('g' if (x*3+j)%5==0 else 'S') if on else '.'
        rows.append(row)
    return rows
def tall(spr): return S([r for r in spr for _ in (0,1)])
ADULT={k:overlay(tall(GON[k]),long_hair(),-4,0) for k in ('guard','guard2','charge','punch','dash')}

PITOU=poses(S([
"....H.....H.....","....HH...HH.....","....HHHHHHH.....","...HHHHHHHHH....","...HHssssHHH....",
"...HsrssrsHH....","...HssssssH.....","....ssnss.......",".....ssss.......","....WWWWWW......",
"...WWWWWWWW.....","...ss.WWWW.ss...","...ss.WWWW.ss...","H....NNNNNN.....","HH...NNNNNN.....",
".HH..NN..NN.....","..HH.ss..ss.....","...H.ss..ss.....",".....ss..ss.....","....kkk..kkk....",]),11,'ss',3)

register_bg(THEME, lambda v: (v//2+4,v,v//2+8))

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
    hc,hl=(52,118,44),(78,150,66); base=int(8+6*g)
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
        cl['vis']=False; ad=actor(ADULT[guard_pose(f)],40,aura=((255,140,50),2))
        pt.update(spr=PITOU['hurt'] if f<200 else pt['spr'],x=150)
        if f<176:
            if f%3==0: s['shake']=rshake()
            rr=random.Random(f//2)
            for j in range(6): s['fx'].append(('rock',rr.randint(10,120),GROUND-((f-150)*2+rr.randint(0,20))%40))
    if 176<=f<200:
        ad['spr']=ADULT['charge']; r=1+(f-176)//4
        s['fx'].append(('orbc',52,GROUND-14,r,((255,220,140),(255,140,40))))
        if f>=186: callout(s,"...GU!",c=(255,190,90)); s['shake']=rshake()
    if 200<=f<206: ad.update(spr=ADULT['dash'],x=lerp(40,128,(f-200)/6))
    if 206<=f<218:
        ad.update(spr=ADULT['punch'],x=128)
        if f==206: s['flash']=1.0; s['fc']=(144,GROUND-14); s['flashc']=(255,200,120)
        s['fx'].append(('boom',146,GROUND-14,int(4+(f-206)*4))); s['shake']=rshake(2)
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
    s['actors']=[a for a in (cl,ad,pt) if a]
    return s

CLIPS = [clip('jajanken', 264, clip_jajanken)]
