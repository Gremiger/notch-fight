"""Naruto sub-theme "naruto-lee": Claude as Rock Lee vs Gaara in the Chunin Exam preliminaries hall,
under the giant ram-seal statue. Leaf Whirlwind (KONOHA SENPU!) is stopped by the sand shield that rises
by itself, and Lee hops Gaara's sand stream. Gai shouts from the balcony (LEE! TAKE THEM OFF!); close-up:
the leg warmer rolled down, the weight dropped (DOSUN!). Back in the hall the weights crater the floor and
Lee is too fast for the sand: afterimages, three hits, Gaara's sand armour flakes off. Close-up: the
Eight Gates open (HACHIMON TONKO: KAIMON! KYUMON! SEIMON!), skin red, eyes white. Kage Buyo kicks Gaara
into the air, Lee follows, and they come down spinning in the bandage drill (OMOTE RENGE!). The dust
settles on a heap of sand: the sand gathers back into Gaara for the loop. THE POWER OF YOUTH!"""
from engine import *
from themes.nrt import shout                                       # same franchise: outlined big text

THEME = 'naruto-lee'
N_ = 360
CX, EX = 30, 150                                                    # the loop keyframe positions

SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(40,20,16)
SAND,SAND_D,SAND_L=(214,180,112),(166,130,76),(240,214,156)
AURA=(110,240,130)

# ---- Lee: black bowl cut, thick brows, green jumpsuit, the headband as a belt, orange leg warmers ----
LPAL={'l':(18,18,24),'J':(52,148,62),'j':(32,104,44),'A':(240,130,40),'I':(250,246,236)}
GATES={**LPAL,'O':(236,92,70),'o':(184,52,44)}                     # the Gates turn the skin red
BOWL=["..llllllll..",".llllllllll.","llllllllllll"]

def _lee(spr):
    spr=overlay(spr,BOWL,-2,0,bangs="llllllllllll")
    eyes=next((y,[x for x,c in enumerate(r) if c=='K']) for y,r in enumerate(spr) if 'K' in r)
    hip=len(spr)-3
    def fn(x,y,t,l,r,c):
        if c=='.': return None
        if y==eyes[0]-1 and any(x in (k-1,k) for k in eyes[1]) and l<=x<=r: return 'l'   # the brows
        if y<t and c=='o': return 'I'                                # bandaged hands raised
        if y==hip and c in 'Oo': return 'D' if x==(l+r)//2 else 'r'  # the forehead protector, worn as a belt
        if y==len(spr)-1 and c=='o': return 'A'                      # leg warmers
        if y>=eyes[0]+3 and c=='O': return 'J'
        if y>=eyes[0]+2 and c=='o': return 'j'
        return None
    return recolor_rows(spr,fn)
LEE=variant(_lee)

# ---- Gaara: red hair, black-ringed eyes, the gourd on his back, the white sash -----------------------
GPAL={'I':(240,236,226),'a':(196,44,34),'c':(120,56,48),'C':(86,38,34),'T':(206,170,112),'t':(160,124,80)}
GAARA=poses(S([
".......aaaaa......","...TT.aaaaaaaa.....","..TTTTaaaaaaaaa....","..TTTTaasssaaa.....","...TT.sKKsKKs......",
"...tt.ssssss.......","..TTT..ssss........",".TTTTTcccccccc.....","TTTTTccIcccccc.....","TTTTtcccIcccc......",
"TTTTtcc.cIcc.cc....",".TTTtcc.ccIc.ss....","..TT....cccc.......","........CCCC.......",".......cccccc......",
".......cc..cc......",".......cc..cc......",".......CC..CC......","......CCC..CCC.....",]),10,'cccs',1)
GAARA['sand']=recolor_rows(GAARA['idle'],lambda x,y,t,l,r,c: None if c=='.' else ('T' if (x+y)%3 else 't'))

# ---- background: the preliminaries hall, the ram-seal statue between the balconies -----------------
def _hall(d):
    d.rectangle([0,0,W,50],fill=(78,76,86))
    for y in range(0,50,6):                                         # stone blocks
        d.line([0,y,W,y],fill=(66,64,74))
        for x in range((y//6)%2*9,W,18): d.line([x,y,x,y+5],fill=(66,64,74))
    st,sl,sd=(176,164,140),(204,194,170),(132,120,100)
    d.polygon([(60,50),(74,50),(88,30),(80,26)],fill=st); d.polygon([(124,50),(110,50),(96,30),(104,26)],fill=sd)   # forearms
    d.line([60,50,80,26],fill=sl)
    d.rounded_rectangle([78,18,106,38],radius=5,fill=st); d.rectangle([98,20,106,36],fill=sd)   # the clasped hands
    for k in range(4): d.ellipse([79+k*6,15,85+k*6,21],fill=st,outline=sd)                    # knuckles
    d.line([80,28,96,28],fill=sd); d.line([80,32,96,32],fill=sd)
    d.rectangle([86,0,98,16],fill=st); d.rectangle([95,0,98,16],fill=sd)                         # the ram seal
    for x in (89,92): d.line([x,0,x,16],fill=sd)
    d.line([86,0,86,16],fill=sl)
    for x0,x1 in ((0,56),(128,W)):                                  # the balconies
        rr=random.Random(x0+3)
        for x in range(x0+3,x1-2,5):                                # who is watching
            c=rr.choice([(40,40,50),(60,46,40),(90,80,60),(52,60,48),(120,60,50)])
            d.rectangle([x,9,x+2,12],fill=c); d.rectangle([x,6,x+2,8],fill=rr.choice([(220,176,140),(190,140,110)]))
        d.rectangle([x0,13,x1,18],fill=(104,92,80)); d.line([x0,13,x1,13],fill=(140,126,110))
        for x in range(x0,x1,4): d.line([x,13,x,18],fill=(86,76,66))
        d.rectangle([x0,18,x1,20],fill=(58,52,48))
    d.rectangle([0,50,W,H],fill=(116,118,128))                      # the floor
    d.line([0,50,W,50],fill=(86,88,98))
    for x in range(-40,W+40,22): d.line([x,51,x+(x-92)//4,H],fill=(100,102,112))
    for y in (54,59): d.line([0,y,W,y],fill=(104,106,116))
register_bg(THEME, lambda v: (v+70,v+72,v+82), decor=_hall)

# ---- effects ------------------------------------------------------------------------------------------
@fx('nl_grain')
def _fx_grain(d,im,e,f):
    _,x,y=e; d.point((int(x),int(y)),fill=SAND_L if (int(x)+f)%3 else SAND_D)

@fx('nl_wall')
def _fx_wall(d,im,e,f):
    """The sand shield: a curved wall that pours up between Gaara and the attack (k 0..1: its height)."""
    _,x,k=e; h=int(30*k)
    if h<=0: return
    top=GROUND-h; rr=random.Random(f)
    d.polygon([(x-5,GROUND+1),(x-6,top+6),(x-2,top),(x+3,top+2),(x+5,top+8),(x+4,GROUND+1)],fill=SAND,outline=SAND_D)
    for _ in range(14): d.point((x+rr.randint(-4,3),rr.randint(top+2,GROUND)),fill=rr.choice([SAND_D,SAND_L]))
    for _ in range(4): d.point((x+rr.randint(-6,6),top-rr.randint(0,4)),fill=SAND_L)

@fx('nl_stream')
def _fx_stream(d,im,e,f):
    """A tongue of sand from the gourd (x0) along the floor to its tip (x1); y lifts the tip."""
    _,x0,x1,lift=e
    if abs(x1-x0)<2: return
    s=1 if x1>x0 else -1; pts=[]
    for x in range(int(x0),int(x1),s*2):
        k=(x-x0)/(x1-x0); pts.append((x,GROUND-14+14*min(1,k*3)-lift*k*k+1.5*math.sin(x*0.4-f*0.7)))
    for x,y in pts: d.ellipse([x-3,y-2,x+3,y+2],fill=SAND)
    for x,y in pts[::3]: d.point((x,y-2),fill=SAND_L); d.point((x+1,y+2),fill=SAND_D)
    tx,ty=pts[-1]; d.ellipse([tx-4,ty-4,tx+4,ty+3],fill=SAND,outline=SAND_D)       # the grasping tip
    for k in (-3,0,3): d.line([tx+s*3,ty+k,tx+s*7,ty+k-s],fill=SAND)

@fx('nl_crater')
def _fx_crater(d,im,e,f):
    _,x,w=e; d.ellipse([x-w,GROUND-1,x+w,GROUND+3],fill=(70,72,82)); d.line([x-w-3,GROUND+3,x-w+2,GROUND+1],fill=(70,72,82))
    d.line([x+w-1,GROUND+1,x+w+4,GROUND+4],fill=(70,72,82))

@fx('nl_weight')
def _fx_weight(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.rectangle([x-3,y-2,x+3,y+1],fill=(50,50,60),outline=(20,20,26)); d.point((x,y-1),fill=(220,40,40))

@fx('nl_speed')
def _fx_speed(d,im,e,f):
    """Speed lines from where Lee was to where he is."""
    _,x0,y0,x1,y1=e
    for k in (-4,0,4): d.line([x0,y0+k,x1,y1+k],fill=(200,240,200) if k else (255,255,255))

@fx('nl_bandage')
def _fx_bandage(d,im,e,f):
    """The bandage drill: white wraps spiralling round the falling pair."""
    _,x,y0,y1=e
    for y in range(int(y0),int(y1),2):
        a=y*0.5+f*1.3; d.point((x+math.sin(a)*9,y),fill=(250,246,236)); d.point((x-math.sin(a)*9,y+1),fill=(200,196,186))

@fx('nl_mound')
def _fx_mound(d,im,e,f):
    _,x,k=e
    if k<=0: return
    h=int(6*k); d.ellipse([x-12,GROUND+1-h,x+12,GROUND+1+h],fill=SAND); d.ellipse([x-8,GROUND+2-h,x+5,GROUND+2],fill=SAND_L)
    rr=random.Random(9)
    for _ in range(int(12*k)): d.point((x+rr.randint(-10,10),GROUND+1-rr.randint(0,max(1,h-1))),fill=SAND_D)

def grains(s,x,y,t,n=12,seed=0,up=False):
    """Sand flaking off (falling) or being pulled in (up=True)."""
    rr=random.Random(seed)
    for _ in range(n):
        vx=rr.uniform(-1.5,1.5); vy=rr.uniform(-1.5,0.5)
        k=t if not up else max(0,12-t)
        gx=x+vx*k; gy=y+vy*k+(0.12*k*k if not up else -0.6*k)
        if gy<=GROUND+1: s['fx'].append(('nl_grain',gx,gy))

def dust(s,x,t,n=10,seed=0,c=(150,150,160)):
    rr=random.Random(seed)
    for j in range(n):
        r=2+t//3+rr.randint(0,2)
        s['fx'].append(('smoke',x+rr.randint(-12,12)+(j-n/2)*t*0.4,GROUND-2-rr.randint(0,8)-t*0.3,r,c if j%3 else (186,186,196)))

# ---- close-ups ----------------------------------------------------------------------------------------
def closeup_weights(t,f):
    """Primer plano: the leg warmer rolled down, the weight dropped — DOSUN!"""
    im=Image.new('RGB',(W,H),(40,38,48)); d=ImageDraw.Draw(im)
    for i in range(16):                                             # a burst behind the shin
        a=i*math.tau/16+f*0.02
        d.polygon([(60,32),(60+math.cos(a)*200,32+math.sin(a)*200),(60+math.cos(a+0.14)*200,32+math.sin(a+0.14)*200)],fill=(54,52,64))
    x0,x1=44,76
    d.rectangle([x0-2,0,x1+2,10],fill=LPAL['J']); d.line([x0+8,0,x0+8,10],fill=LPAL['j'])   # the jumpsuit
    d.rectangle([x0,10,x1,H],fill=SKIN); d.rectangle([x1-6,10,x1,H],fill=SKIN_D)              # the shin
    roll=ease(t/0.3)                                                # the warmer pulled down...
    wy=int(10+34*roll)
    held=0.3<=t<0.55; drop=ease((t-0.55)/0.1)
    by=12+int(70*drop)                                              # ...the weight band, then off it goes
    if t<0.55 or drop<1:
        d.rectangle([x0-3,by,x1+3,by+14],fill=(52,52,62),outline=(20,20,26))
        for k in range(3): d.line([x0+2+k*11,by+2,x0+2+k*11,by+12],fill=(70,70,82))
        text(d,"GUTS",x0+9,by+5,(230,50,50))
    d.rectangle([x0-2,wy,x1+2,H],fill=LPAL['A']); d.line([x0-2,wy,x1+2,wy],fill=(250,190,90))
    for k in range(3): d.line([x0-2,wy+3+k*5,x1+2,wy+3+k*5],fill=(210,100,30))   # the rolled-down folds
    hx,hy=(x1+6,wy-4) if t<0.3 else (x1+6,by+4)                     # the bandaged hand pulling
    if t<0.55:
        d.rounded_rectangle([hx-6,hy-5,hx+8,hy+5],radius=2,fill=LPAL['I'],outline=(150,146,136))
        for k in range(3): d.line([hx-5,hy-3+k*3,hx+7,hy-3+k*3],fill=(200,196,186))
        d.rectangle([hx+8,hy-4,hx+30,hy+4],fill=LPAL['J'])          # the sleeve, off to the right
    if t<0.5: text(d,"LEE! TAKE THEM OFF!",104,54,(140,230,140))
    if t>=0.65:
        rr=random.Random(f)
        for _ in range(26): r=rr.randint(3,9); x=rr.randint(20,110); y=H-rr.randint(0,10); d.ellipse([x-r,y-r,x+r,y+r],fill=rr.choice([(150,150,160),(186,186,196)]))
        sj=(f%3)-1 if t<0.8 else 0
        big_text(im,"DOSUN!",14,(255,236,120),scale=3,cx=146+sj,outline=(90,40,0))
        if t<0.8: im=im.transform(im.size,Image.AFFINE,(1,0,(f%2)*2-1,0,1,0))   # the floor shakes
    if t<0.06: zoom_lines(d)
    return im

def closeup_gates(t,f):
    """Primer plano: the Eight Gates open — skin goes red, the eyes white, a green blaze round his head."""
    im=Image.new('RGB',(W,H),(14,30,20)); d=ImageDraw.Draw(im)
    ox,k=26,ease((t-0.1)/0.7)
    rr=random.Random(f)
    for i in range(int(14+50*k)):                                    # the green blaze
        x=rr.randint(ox-14,ox+70); y=rr.randint(-4,H); L=rr.randint(8,26)
        d.polygon([(x-3,y),(x+3,y),(x+rr.randint(-2,2),y-L)],fill=rr.choice([AURA,(60,190,90),(190,255,200)]))
    sk=tuple(int(lerp(SKIN[i],GATES['O'][i],k)) for i in range(3)); skd=tuple(int(lerp(SKIN_D[i],GATES['o'][i],k)) for i in range(3))
    d.rectangle([ox,14,ox+56,H],fill=sk); d.rectangle([ox+50,14,ox+56,H],fill=skd)
    hair=LPAL['l']
    d.chord([ox-6,-16,ox+62,34],180,360,fill=hair); d.rectangle([ox-6,8,ox+62,20],fill=hair)   # the bowl cut
    d.rectangle([ox-6,20,ox+2,40],fill=hair); d.rectangle([ox+54,20,ox+62,40],fill=hair)
    for x in range(ox,ox+56,7): d.line([x,10,x+2,20],fill=(46,46,58))
    for ex,s in ((ox+16,1),(ox+40,-1)):
        d.polygon([(ex-9,24+s*2),(ex+9,24-s*2),(ex+9,28-s*2),(ex-9,28+s*2)],fill=hair)        # the brows
        d.ellipse([ex-7,30,ex+7,44],fill=(250,250,250),outline=INK)
        if t<0.45: d.ellipse([ex-2,34,ex+2,40],fill=INK)            # pupils, then blank white eyes
    if k>0.3:
        for vx in (ox+4,ox+50):                                     # veins at the temples
            d.line([vx,22,vx+2,26,vx,30,vx+2,34],fill=(150,30,30))
    d.line([ox+20,54,ox+36,54],fill=INK); d.line([ox+20,55,ox+36,55],fill=(150,40,30))   # gritted teeth
    if t>=0.2: big_text(im,"HACHIMON TONKO",6,(200,255,210),scale=1,cx=140,outline=(10,60,20))
    gate=[(0.35,"KAIMON!"),(0.6,"KYUMON!"),(0.82,"SEIMON!")]
    cur=[g for g in gate if t>=g[0]]
    if cur:
        sj=(f%3)-1 if t-cur[-1][0]<0.08 else 0
        big_text(im,cur[-1][1],22,(255,255,255),scale=2,cx=140+sj,outline=(10,90,30))
        text(d,f"GATE {len(cur)} OPEN",118,48,AURA)
    if t<0.06: zoom_lines(d,AURA)
    if t>0.9: im=fade_to(im,(170,255,190),(t-0.9)/0.1*0.8)
    return im

# ---- the clip -----------------------------------------------------------------------------------------
def clip_lotus(f):
    s=scene(f,THEME)
    cl=actor(LEE[guard_pose(f)],CX,pal=LPAL); ga=actor(GAARA['idle'],EX,flip=True,pal=GPAL)
    extra=[]
    # 1) Konoha Senpu: the sand shield rises by itself
    if 14<=f<24: cl.update(x=ez(CX,126,(f-14)/10),spr=LEE['dash'])
    if 14<=f<34: callout(s,"KONOHA SENPU!",c=(150,240,150))
    if 18<=f<36: s['under'].append(('nl_wall',136,min(1,(f-18)/5) if f<30 else (36-f)/6))
    if 24<=f<36:
        k=f-24; cl.update(x=lerp(126,CX,k/12),y=GROUND-int(16*math.sin(math.pi*k/12)),spr=LEE['hurt'] if k<5 else LEE['guard'])
        if k<3: s['fx'].append(('spark',132,GROUND-12,5)); s['shake']=rshake()
        grains(s,134,GROUND-20,k,n=10,seed=24)
    if 34<=f<46: s['fx'].append(('dmg',"...",ga['x']-6,GROUND-30,(255,255,255)))
    # 2) the sand stream, and Lee hops it
    if 42<=f<68:
        ga['spr']=GAARA['attack']
        tip=lerp(140,6,(f-42)/14) if f<58 else lerp(6,140,(f-58)/10)
        s['fx'].append(('nl_stream',142,tip,0))
    if 46<=f<60:
        t=(f-46)/14; cl.update(y=GROUND-int(30*math.sin(math.pi*t)),spr=LEE['dash'] if t<0.5 else LEE['guard2'])
    if 50<=f<62: grains(s,24,GROUND-6,f-50,n=8,seed=50)
    # 3) Gai from the balcony
    if 66<=f<82: callout(s,"LEE! TAKE THEM OFF!",c=(140,230,140)); cl['spr']=LEE['punch'] if f>=74 else cl['spr']
    if 76<=f<82: s['fx'].append(('dmg',"OSU!",cl['x']-6,GROUND-26,(255,255,255)))
    if 82<=f<120: s['image']=closeup_weights((f-82)/38,f); return s
    # 4) the weights crater the floor
    if 125<=f<300: s['under']+=[('nl_crater',18,5),('nl_crater',42,5)]
    if 120<=f<126:
        for x in (18,42): s['under'].append(('nl_weight',x,lerp(10,GROUND,(f-120)/5)))
    if f>=126 and f<300: s['under']+=[('nl_weight',18,GROUND+1),('nl_weight',42,GROUND+1)]
    if 125<=f<140:
        for x in (18,42): dust(s,x,f-125,n=6,seed=x)
        if f<132: s['shake']=rshake(2); shout(s,"DOSUN!",(255,236,120),outline=(90,40,0),y=4)
    if 128<=f<142: s['fx'].append(('dmg',"!?",ga['x']-4,GROUND-30,(255,255,255)))
    # 5) too fast for the sand: afterimages and three hits
    HITS=[(144,168,GROUND,True),(154,150,GROUND-24,False),(164,132,GROUND,False)]   # (frame, x, feet, flip)
    if 140<=f<176:
        cl['vis']=False; prev=(CX,GROUND-6)
        for i,(h0,hx,hy,fl) in enumerate(HITS):
            if f<h0-4: break
            if f<h0:
                extra.append(actor(LEE['dash'],lerp(prev[0],hx,(f-h0+4)/4),y=hy,flip=fl,pal=LPAL,alpha=0.45))
                s['fx'].append(('nl_speed',prev[0],prev[1],hx,hy-6))
            elif f<h0+6 or i==2:
                extra.append(actor(LEE['punch'] if f<h0+5 else LEE['guard'],hx,y=hy,flip=fl,pal=LPAL))
                if f<h0+2: s['fx'].append(('spark',EX+(6 if fl else -6),hy-10 if hy==GROUND else GROUND-18,6)); s['shake']=rshake(2)
                if f<h0+5: ga['spr']=GAARA['hurt']
                grains(s,EX-2,GROUND-16,f-h0,n=14,seed=h0)
                if f<h0+8: s['fx'].append(('nl_wall',EX+(8 if fl else -12),min(1,(f-h0)/4)*0.6))   # the sand, a beat too late
            prev=(hx,hy-6)
        if f<146: extra.append(actor(LEE['guard'],CX,pal=LPAL,alpha=max(0,1-(f-140)/6)))
        if 156<=f<176: s['fx'].append(('dmg',"TOO SLOW!",112,GROUND-36,(150,240,150)))
    if 176<=f<182: extra.append(actor(LEE['charge'],132,pal=LPAL)); cl['vis']=False
    if 176<=f<216: ga['spr']=GAARA['hurt'] if f<190 else GAARA['idle']
    if 182<=f<222: s['image']=closeup_gates((f-182)/40,f); return s
    # 6) Kage Buyo: kicked into the air, Lee follows
    if 222<=f<246:
        cl['vis']=False; k=f-222
        lx=132 if k<4 else lerp(132,EX,(k-4)/4)
        ly=GROUND if k<8 else GROUND-int((k-8)*7)
        extra.append(actor(rotate90(LEE['dash'],3) if 4<=k<12 else LEE['charge'],lx,y=ly,pal=GATES,aura=(AURA,1+(f%2))))
        if k>=6: ga.update(spr=GAARA['hurt'],y=GROUND-int((k-6)**1.6*3))
        if k==6: s['flash']=0.8; s['fc']=(EX,GROUND-10); s['flashc']=(190,255,200); s['shake']=rshake(2)
        if 6<=k<14: s['fx'].append(('ring',EX,GROUND,(k-6)*4,AURA))
        if k<18: callout(s,"KAGE BUYO!",c=(150,240,150))
    if 246<=f<258:
        cl['vis']=False; ga['vis']=False
        shout(s,"OMOTE",(200,255,210),outline=(10,70,20),y=8); shout(s,"RENGE!",(255,255,255),outline=(10,70,20),y=26)
        if f>=254: s['fx'].append(('nl_speed',EX,0,EX,GROUND-30))
    # 7) the bandage drill comes down
    if 258<=f<272:
        cl['vis']=False; ga['vis']=False; k=(f-258)/14
        y=int(lerp(-6,GROUND,k*k)); spin=(f//1)%4
        gs=rotate90(GAARA['hurt'],(spin+2)%4); ls=rotate90(LEE['dash'],(spin+3)%4)
        extra+= [actor(gs,EX,y=y,pal=GPAL),actor(ls,EX,y=y-len(gs)+2,pal=GATES,aura=(AURA,1))]
        s['fx'].append(('nl_bandage',EX,y-36,y))
    if f==272: s['flash']=1.0; s['fc']=(EX,GROUND-6); s['flashc']=(255,250,220)
    if 272<=f<300:
        k=f-272; cl['vis']=False; ga['vis']=False
        if k<10: s['shake']=rshake(2); s['fx'].append(('ring',EX,GROUND,4+k*5,(255,240,200)))
        if k<14: s['fx']+= [('rock',EX+random.randint(-20,20),GROUND-random.randint(0,14)) for _ in range(5)]
        s['under'].append(('nl_crater',EX,14))
        dust(s,EX,min(k,10),n=int(16*(1-k/28))+2,seed=272)
        if 6<=k<18: extra.append(actor(LEE['dash'],ez(EX-16,CX,(k-6)/12),y=GROUND-int(14*math.sin(math.pi*(k-6)/12)),pal=GATES,aura=(AURA,1) if k<12 else None))
        cl['vis']=k>=18
    # 8) THE POWER OF YOUTH! — a heap of sand, and the sand gathers back into Gaara
    if 290<=f<322:
        callout(s,"THE POWER OF YOUTH!",c=(150,240,150)); cl['spr']=LEE['punch']
        if f%8<5: s['fx'].append(('twinkle',CX+9,GROUND-6,2+(f%8<2)))
    if 286<=f<300: s['under'].append(('nl_mound',EX,ease((f-286)/6)))
    if 300<=f<330:
        k=(f-300)/30; s['under'].append(('nl_mound',EX,1-ease(k)))
        if k<0.8:
            sp=GAARA['sand']; cut=int(len(sp)*(1-k/0.8)); ga['spr']=S(['.'*len(r) if i<cut else r for i,r in enumerate(sp)])
        grains(s,EX,GROUND-10,(f-300)%12,n=14,seed=f//12,up=True)
    s['actors']=extra+[cl,ga]
    return s

CLIPS = [clip('lotus', N_, clip_lotus)]
