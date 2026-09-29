"""Half-Life: Claude (Gordon Freeman, HEV suit, glasses, goatee, lambda on the chest) vs a
Combine soldier in City 17. Headcrabs leap and meet the crowbar, the soldier's pulse rifle drains
the HEV, the Gravity Gun catches a falling saw blade and throws it back. Close-up of the G-Man
("RISE AND SHINE, MR. FREEMAN"), then an explosive barrel ends the fight, the lambda lights up,
a headcrab drops from a vent, the soldier walks back and the HEV recharges for the loop."""
from engine import *

THEME = 'hl'
N_ = 288

# --- Claude as Gordon Freeman -------------------------------------------------------------------
_LAMBDA = ["k..", ".k.", "k.k"]
def _gordon(spr):
    g=[list(r) for r in spr]; t,l,r=body_box(spr)
    ks=[i for i,c in enumerate(g[t+2]) if c=='K']
    if ks:
        for i in range(min(ks)-1,max(ks)+1):                   # glasses: frame + bridge between the eyes
            if 0<=i<len(g[t+2]) and g[t+2][i]=='O': g[t+2][i]='k'
        cx=(min(ks)+max(ks))//2
        for i in (cx,cx+1):                                    # goatee
            if g[t+4][i]=='O': g[t+4][i]='q'
    for j,row in enumerate(_LAMBDA):                           # lambda on the HEV chest plate
        for i,ch in enumerate(row):
            if ch!='.' and g[t+5+j][l+1+i]=='O': g[t+5+j][l+1+i]=ch
    return overlay(S([''.join(r) for r in g]),["qqqqqqqq"],0,0)
GORDON=variant(_gordon)

# hand position (col,row) of each base pose, measured from the base CL grids (feet-anchored)
_HAND={'guard':(13,4),'guard2':(13,5),'punch':(16,5),'dash':(16,5),'charge':(15,5),'armsup':(11,0),'hurt':(14,2)}
def hand(pose,x): return hand_at(CL[pose],x,GROUND,False,*_HAND[pose])

# --- Opponents ----------------------------------------------------------------------------------
SOLDIER_PAL={'c':(62,72,84),'i':(150,225,255)}
SOLDIER=poses(S([
"....kkkkk......","...kvvvvvk.....","...kvivvik.....","...kvvvvvk.....","....kdkdk......",
"...ccccccc.....","..cNNNNNNNc....","..cNNvNNNNc....","..cNNNNNNNkdddd","..kNNNNNNNkdddk",
"...NNNkNNN.....","...cccccccc....","...NNN..NNN....","...NNN..NNN....","...ccc..ccc....",
"...NNN..NNN....","...kkk..kkk....","..kkkk..kkkk...",]),8,'k',3)
CRAB_PAL={'a':(206,180,140),'b':(140,104,76)}
CRAB=S(["...aaaa...",".aabbbbaa.","aa.a..a.aa"])
CRAB_LEAP=S(["a..aaaa..a",".aabbbbaa.","...a..a..."])
CRAB_FLAT=S([".aabbbbaa.","aaaaaaaaaa"])

HUD_C=(255,160,30)
PULSE=((80,170,255),(200,240,255))

def _city(d):
    """City 17 at night: the Citadel on the horizon, dark blocks, a few lit windows, a wall vent."""
    d.polygon([(88,GROUND),(94,8),(97,0),(100,0),(102,8),(108,GROUND)],fill=(22,26,36))
    d.line([(97,2),(97,GROUND)],fill=(34,40,54)); d.point((98,3),fill=(90,120,160))
    rr=random.Random(17)
    for x0,x1,top in ((0,20,30),(22,40,40),(44,70,24),(74,86,36),(112,128,20),(130,150,34),(152,170,28),(172,185,38)):
        d.rectangle([x0,top,x1,GROUND],fill=(12,13,18))
        for _ in range((x1-x0)//4):
            wx,wy=rr.randint(x0+2,x1-2),rr.randint(top+3,GROUND-6)
            d.point((wx,wy),fill=(70,60,26) if rr.random()<0.7 else (40,60,70))
    d.rectangle([118,22,126,25],fill=(28,30,36),outline=(46,48,56))      # the vent
    for x in range(120,126,2): d.line([x,23,x,24],fill=(8,8,10))
register_bg(THEME, lambda v: (v//2+2,v//2+4,v), decor=_city)

# --- Effects ------------------------------------------------------------------------------------
_TINY={'L':"100010010101101",'+':"000010111010000"}
def _glyph(d,ch,x,y,c):
    for j,b in enumerate(_TINY[ch]):
        if b=='1': d.point((x+1+j%3,y+1+j//3),fill=(0,0,0)); d.point((x+j%3,y+j//3),fill=c)

@fx('hl_hud')
def _fx_hud(d,im,e,f):
    """HEV HUD: health cross + value, suit value, lambda badge on the right."""
    _,hp,suit=e
    c=HUD_C if hp>25 else (255,40,30)
    _glyph(d,'+',2,59,c); text(d,f"{int(round(hp))}",7,59,c)
    text(d,"SUIT",24,59,HUD_C); text(d,f"{int(round(suit))}",42,59,HUD_C)
    _glyph(d,'L',W-6,59,HUD_C)

@fx('hl_crowbar')
def _fx_crowbar(d,im,e,f):
    """The crowbar held at (hx,hy), pointing at `ang` degrees, hooked end outwards."""
    _,hx,hy,ang=e; a=math.radians(ang); L=11
    x1,y1=hx+math.cos(a)*L,hy+math.sin(a)*L; x0,y0=hx-math.cos(a)*2,hy-math.sin(a)*2
    px,py=-math.sin(a),math.cos(a)
    hook=[(x1,y1),(x1+px*2-math.cos(a),y1+py*2-math.sin(a))]
    d.line([(x0,y0),(x1,y1)],fill=(18,12,16),width=3); d.line(hook,fill=(18,12,16),width=3)
    d.line([(x0,y0),(x1,y1)],fill=(200,34,30)); d.line(hook,fill=(200,34,30))

@fx('hl_swoosh')
def _fx_swoosh(d,im,e,f):
    _,x,y,r,a0,a1=e; d.arc([x-r,y-r,x+r,y+r],a0,a1,fill=(255,230,200))

@fx('hl_gravgun')
def _fx_gravgun(d,im,e,f):
    """Zero-point energy field manipulator held at the hand, prongs glowing orange by `glow`."""
    _,hx,hy,glow=e; hx,hy=int(hx),int(hy)
    d.rectangle([hx-4,hy-2,hx+5,hy+2],fill=(64,64,72),outline=(18,12,16))
    d.line([hx-3,hy-1,hx+3,hy-1],fill=(230,130,40)); d.point((hx,hy+1),fill=(150,150,160))
    pc=(255,170,60) if glow>0 else (190,110,40)
    for (a,b),(c,g) in (((hx+6,hy-2),(hx+10,hy-4)),((hx+6,hy+2),(hx+10,hy+4))):
        d.line([a,b,c,g],fill=pc); d.point((c,g),fill=(255,240,180))
    d.line([hx+6,hy,hx+8,hy],fill=pc)
    if glow>0:
        r=2+int(2*glow)+(f%2)
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([hx+10-r,hy-r,hx+10+r,hy+r],fill=int(160*glow))
        im.paste((255,190,90),(0,0),m)

@fx('hl_gbeam')
def _fx_gbeam(d,im,e,f):
    """Gravity Gun tractor beam: a wavy orange ribbon from the prongs to the object."""
    _,x0,y0,x1,y1=e; n=max(2,int(abs(x1-x0)+abs(y1-y0))//2)
    for side,c in ((1,(255,150,40)),(-1,(255,210,120))):
        pts=[]
        for k in range(n+1):
            t=k/n; w=math.sin(t*9+f*1.3)*1.6*side*math.sin(math.pi*t)
            pts.append((lerp(x0,x1,t),lerp(y0,y1,t)+w))
        d.line(pts,fill=c)

@fx('hl_saw')
def _fx_saw(d,im,e,f):
    """A spinning saw blade; `fast` adds motion streaks behind it."""
    _,x,y,fast=e; x,y=int(x),int(y)
    if fast:
        for k in range(1,4): d.line([x-4-k*4,y-2+k,x-k*4,y-2+k],fill=(120,120,130))
    rot=f*0.7
    for k in range(8):
        a=rot+k*math.pi/4; d.point((x+math.cos(a)*5,y+math.sin(a)*5),fill=(220,220,230))
    d.ellipse([x-4,y-4,x+4,y+4],fill=(150,152,164),outline=(18,12,16))
    d.ellipse([x-1,y-1,x+1,y+1],fill=(30,30,36))
    d.line([x+math.cos(rot)*3,y+math.sin(rot)*3,x-math.cos(rot)*3,y-math.sin(rot)*3],fill=(200,200,210))

@fx('hl_barrel')
def _fx_barrel(d,im,e,f):
    """The red explosive barrel (hazard stripe), centred at (x,y)."""
    _,x,y=e; x,y=int(x),int(y)
    d.rectangle([x-4,y-5,x+4,y+5],fill=(170,30,24),outline=(18,12,16))
    d.line([x-3,y-4,x+3,y-4],fill=(220,70,50)); d.line([x-3,y+3,x+3,y+3],fill=(110,18,14))
    d.rectangle([x-3,y-1,x+3,y+1],fill=(230,210,60))
    for k in range(-3,4,2): d.point((x+k,y),fill=(20,16,10))

@fx('hl_pulse')
def _fx_pulse(d,im,e,f):
    """An AR2 pulse round: a short blue-white bolt at x heading left along y."""
    _,x,y=e; x,y=int(x),int(y)
    d.line([x,y,x+6,y],fill=PULSE[0]); d.line([x,y,x+2,y],fill=PULSE[1])

@fx('hl_muzzle')
def _fx_muzzle(d,im,e,f):
    _,x,y=e
    for k in range(4): a=k*math.pi/2+f; d.line([x,y,x+math.cos(a)*3,y+math.sin(a)*2],fill=PULSE[1])
    d.point((x,y),fill=(255,255,255))

@fx('hl_lambda')
def _fx_lambda(d,im,e,f):
    """The big lambda in its ring, scaled by s and faded by a (0..1)."""
    _,x,y,s,a=e
    if a<=0: return
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    md.ellipse([x-s-3,y-s-3,x+s+3,y+s+3],outline=255,width=2)
    md.line([(x-s*0.55,y-s*0.9),(x+s*0.6,y+s*0.85)],fill=255,width=3)
    md.line([(x+s*0.02,y-s*0.05),(x-s*0.6,y+s*0.85)],fill=255,width=3)
    glow=m.filter(ImageFilter.GaussianBlur(2))
    im.paste((255,120,20),(0,0),glow.point(lambda v: int(v*a*0.9)))
    im.paste((255,190,90),(0,0),m.point(lambda v: int(v*a)))

# --- HEV health / suit --------------------------------------------------------------------------
def _meter(f,marks,base=100.0):
    v=base
    for t0,t1,val in marks:
        if f>=t0: v=lerp(v,val,(f-t0)/max(1,t1-t0))
    if f>=254: v=lerp(v,base,(f-254)/22)                 # HEV charger: back to full for the loop
    return v
HP=[(50,54,85),(84,104,71)]
SUIT=[(84,104,38)]

# --- Close-up: the G-Man -------------------------------------------------------------------------
_GMAN_LINES=[(0.06,0.48,["RISE AND SHINE","MR. FREEMAN."]),(0.52,0.96,["WAKE UP AND","SMELL THE ASHES."])]
def closeup_gman(t,f):
    """Primer plano: the G-Man in his blue suit, speaking to the camera; his lines type out."""
    im=Image.new('RGB',(W,H),(4,8,6)); d=ImageDraw.Draw(im)
    d.ellipse([10,-20,114,70],fill=(12,22,16)); d.ellipse([26,-8,98,60],fill=(18,30,22))
    suit,lapel=(30,38,64),(20,24,42)
    d.polygon([(8,64),(22,48),(46,42),(78,42),(102,48),(116,64)],fill=suit)
    d.polygon([(48,42),(62,62),(76,42)],fill=(214,214,204))                       # shirt
    d.polygon([(46,42),(58,58),(48,64),(38,64)],fill=lapel); d.polygon([(78,42),(66,58),(76,64),(86,64)],fill=lapel)
    d.rectangle([59,43,65,47],fill=(76,88,146)); d.polygon([(59,47),(65,47),(67,62),(62,65),(57,62)],fill=(60,70,124))  # tie
    d.rectangle([54,34,70,44],fill=(176,142,116))                                 # neck
    d.ellipse([40,19,47,30],fill=(196,160,132)); d.ellipse([77,19,84,30],fill=(196,160,132))   # ears
    d.ellipse([44,3,80,43],fill=(212,178,148))                                    # head
    d.pieslice([43,1,81,34],195,345,fill=(54,40,30)); d.ellipse([50,8,74,24],fill=(212,178,148))  # receding slick hair
    d.line([50,31,54,37],fill=(180,144,118)); d.line([74,31,70,37],fill=(180,144,118))          # gaunt cheeks
    blink=(f%36) in (0,1)
    for ex in (54,70):
        d.line([ex-5,18,ex+3,17] if ex<62 else [ex-3,17,ex+5,18],fill=(60,44,34))  # brows
        if blink: d.line([ex-3,22,ex+3,22],fill=(120,90,70)); continue
        d.rectangle([ex-3,21,ex+3,23],fill=(226,224,206)); d.rectangle([ex-1,21,ex+1,23],fill=(60,130,80))
        d.point((ex,22),fill=(10,20,10)); d.line([ex-3,20,ex+3,20],fill=(140,100,80))
    d.line([62,23,61,30],fill=(178,142,116)); d.line([59,31,65,31],fill=(160,120,96))          # nose
    typing=False; lines=[]
    for t0,t1,ls in _GMAN_LINES:
        if t0<=t<t1:
            n=int((t-t0)/(t1-t0-0.12)*sum(len(x) for x in ls)); typing=n<sum(len(x) for x in ls)
            for x in ls: lines.append(x[:max(0,n)]); n-=len(x)
    if typing and f%3: d.ellipse([58,34,66,38],fill=(70,24,22))                                 # mouth
    else: d.line([57,36,67,36],fill=(128,76,64))
    d.line([60,40,64,40],fill=(186,150,124))
    for j,s in enumerate(lines): text(d,s.replace(',',''),118,20+j*10,(196,214,188))
    if t<0.06:
        zoom_lines(d)
    return im

# --- The clip -----------------------------------------------------------------------------------
def _arc(p0,p1,t,hgt):
    t=max(0,min(1,t)); return lerp(p0[0],p1[0],t), lerp(p0[1],p1[1],t)-hgt*math.sin(math.pi*t)

def clip_lambda(f):
    s=scene(f,THEME)
    pose=guard_pose(f); cx=30; weapon=('bar',-110); cy=GROUND
    sol=actor(SOLDIER['idle'],150,flip=True,pal=SOLDIER_PAL)
    crabs=[]
    s['fx'].append(('hl_hud',_meter(f,HP),_meter(f,SUIT)))

    # 1) headcrab A leaps, crowbar whack
    if 20<=f<32: crabs.append((*_arc((132,GROUND),(46,GROUND-10),(f-20)/12,18),CRAB_LEAP,True))
    if 26<=f<30: weapon=('bar',-160)
    if 30<=f<36:
        pose='punch'; weapon=('bar',lerp(-60,25,(f-30)/4))
        if f<33: s['fx'].append(('hl_swoosh',38,52,12,-60,30))
    if f==32: s['fx'].append(('spark',46,GROUND-12,5)); s['shake']=rshake()
    if 32<=f<46: crabs.append((*_arc((46,GROUND-12),(118,-6),(f-32)/14,10),CRAB if f%4<2 else CRAB_LEAP,f%4<2))
    # 2) headcrab B latches onto the head, gets thrown down and whacked
    if 36<=f<48: crabs.append((*_arc((140,GROUND),(31,GROUND-12),(f-36)/12,20),CRAB_LEAP,True))
    if 48<=f<60:
        pose='hurt' if (f//3)%2 else 'guard'; weapon=None
        crabs.append((31+(1 if f%2 else -1),GROUND-12,CRAB,True))
    if 60<=f<64: pose='armsup'; weapon=None; crabs.append((31,GROUND-15,CRAB,True))
    if 64<=f<68: pose='guard'; weapon=('bar',-160); crabs.append((*_arc((34,GROUND-15),(52,GROUND),(f-64)/4,6),CRAB_LEAP,False))
    if 68<=f<74:
        pose='punch'; weapon=('bar',lerp(-40,40,(f-68)/3))
        if f<70: crabs.append((52,GROUND,CRAB,False))
        else: crabs.append((52,GROUND,CRAB_FLAT,False))
        if f==70: s['fx'].append(('spark',50,GROUND-3,5)); s['shake']=rshake()
    if 74<=f<82: s['actors'].append(actor(CRAB_FLAT,52,GROUND,pal=CRAB_PAL,alpha=1-(f-74)/8))
    # 3) the soldier opens fire: pulse rounds drain the suit
    if 76<=f<106: sol['spr']=SOLDIER['attack']
    if 80<=f<104:
        if f%2==0: s['fx'].append(('hl_muzzle',139,49))
        for k in range(3):
            x=138-((f-80)*9+k*31)%100
            if x>38: s['fx'].append(('hl_pulse',x,49+(k%2)))
        if f>=84:
            pose='hurt'; weapon=None; cx=30+(1 if f%2 else 0)
            if f%3==0: s['fx'].append(('spark',36+random.randint(-2,2),50+random.randint(-3,2),2))
    # 4) Gravity Gun: catch the falling saw blade and throw it back
    grav=None
    if 104<=f<140 or 208<=f<238: pose='charge'; weapon=None
    if 104<=f<126: callout(s,"GRAVITY GUN",c=(255,170,60))
    if 104<=f<140:
        hx,hy=hand('charge',30); tip=(hx+10,hy)
        glow=1.0 if 114<=f<134 else 0.0; grav=(hx,hy,glow)
        if 108<=f<114: s['fx'].append(('hl_saw',84,lerp(-6,32,(f-108)/6),False))
        if 114<=f<128:
            p=ease((f-116)/8); bx,by=lerp(84,tip[0]+6,p),lerp(32,tip[1],p)
            s['fx'].append(('hl_gbeam',tip[0],tip[1],bx-4,by))
            if f>=114: s['fx'].append(('hl_saw',bx,by,False))
        if 128<=f<134:
            if f==128: s['flash']=0.35; s['fc']=tip; s['flashc']=(255,190,90)
            s['fx'].append(('hl_saw',lerp(tip[0]+6,140,(f-128)/6),tip[1],True))
    if f==134: s['fx'].append(('spark',140,48,7)); s['shake']=rshake(2)
    if 134<=f<142: s['fx'].append(('hl_saw',*_arc((142,48),(176,-8),(f-134)/8,6),False))
    if 134<=f<146: sol.update(spr=SOLDIER['hurt'],x=ez(150,164,(f-134)/6))
    if 146<=f<160: sol.update(x=ez(164,150,(f-146)/12))
    # 5) close-up: the G-Man
    if 160<=f<208: s['image']=closeup_gman((f-160)/48,f); return s
    # 6) big finish: the explosive barrel
    if 208<=f<238:
        hx,hy=hand('charge',30); tip=(hx+10,hy); glow=1.0 if 214<=f<232 else 0.0; grav=(hx,hy,glow)
        if 208<=f<214: s['fx'].append(('hl_barrel',96,lerp(-8,30,(f-208)/6)))
        if 214<=f<226:
            p=ease((f-216)/8); bx,by=lerp(96,tip[0]+6,p),lerp(30,tip[1]-2,p)
            s['fx'].append(('hl_gbeam',tip[0],tip[1],bx-4,by))
            if f>=214: s['fx'].append(('hl_barrel',bx,by))
        if 226<=f<232:
            if f==226: s['flash']=0.35; s['fc']=tip; s['flashc']=(255,190,90)
            s['fx'].append(('hl_barrel',lerp(tip[0]+6,142,(f-226)/6),tip[1]-2))
    if 232<=f<250:
        t=(f-232)/18
        if f<238: s['flash']=0.6*(1-(f-232)/6); s['fc']=(144,46); s['flashc']=(255,170,70); s['shake']=rshake(2)
        s['fx'].append(('boom',144,46,int(4+14*t)))
        s['fx'].append(('fire',144,GROUND,int(8*(1-t))+1))
        for k in range(3): s['fx'].append(('smoke',144+k*6-6,40-int(16*t)-k*3,int(3+5*t),(40,36,34)))
    if 232<=f<246: sol.update(spr=SOLDIER['hurt'],x=lerp(150,200,(f-232)/12),y=GROUND-int(24*math.sin(math.pi*min(1,(f-232)/14))),tint=(40,30,26))
    elif 246<=f<262: sol['vis']=False
    # 7) the lambda moment
    if 240<=f<262:
        pose='armsup'; weapon=('bar',-80)
        a=min(1,(f-240)/6,(262-f)/6); s['fx'].append(('hl_lambda',93,24,11,a))
        if f>=246: callout(s,"HALF LIFE 3 CONFIRMED",y=44,c=(255,170,60))
    # 8) back to the loop: a headcrab drops from the vent, the soldier walks back in
    if 256<=f<262: crabs.append((122,lerp(26,GROUND,(f-256)/6),CRAB,True))
    if 262<=f<266: crabs.append((122,GROUND,CRAB,True))
    if 266<=f<274: crabs.append((*_arc((122,GROUND),(46,GROUND-10),(f-266)/8,16),CRAB_LEAP,True))
    if 268<=f<272: weapon=('bar',-160)
    if 272<=f<276:
        pose='punch'; weapon=('bar',lerp(-60,25,(f-272)/3))
        if f<275: s['fx'].append(('hl_swoosh',38,52,12,-60,30))
    if f==274: s['fx'].append(('spark',46,GROUND-12,5))
    if 274<=f<286: crabs.append((*_arc((46,GROUND-12),(120,-8),(f-274)/12,10),CRAB if f%4<2 else CRAB_LEAP,f%4<2))
    if 262<=f<282: sol.update(vis=True,tint=None,spr=SOLDIER['idle'],x=ez(196,150,(f-262)/20),y=GROUND-((f//3)%2))

    cl=actor(GORDON[pose],cx,cy)
    s['actors']=[cl,sol]+[actor(sp,x,y,flip=fl,pal=CRAB_PAL) for x,y,sp,fl in crabs]+[a for a in s['actors']]
    if weapon:
        hx,hy=hand(pose,cx); s['fx'].append(('hl_crowbar',hx,hy,weapon[1]))
    if grav: s['fx'].append(('hl_gravgun',*grav))
    return s

CLIPS = [clip('lambda', N_, clip_lambda)]
