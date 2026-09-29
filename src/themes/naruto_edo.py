"""Naruto sub-theme "naruto-edo": Claude (Naruto) vs Kabuto on the Fourth Great Ninja War
battlefield, a cracked rocky plain strewn with broken blades. Kabuto raises three coffins with Edo
Tensei (coffin close-up: the Codex, OpenCode and Grok logos, reanimated); Claude's shadow clones
Rasengan them apart, but the paper-dust bodies re-form (USELESS!). Claude enters Sage Mode
(close-up of the toad eyes) and a Rasenshuriken swallows all three in a wind dome and seals them
for good; Kabuto is blown back and limps in for the loop."""
import zlib
from engine import *
from themes.nrt import NARU, poof, callout, shout, naru_face   # same franchise: reuse Claude-as-Naruto

THEME = 'naruto-edo'
N_ = 336
CX, EX = 30, 164                                                    # the loop keyframe positions

PAL.update({'c':(78,66,66),'x':(96,62,34),'l':(146,100,58)})

KABUTO=poses(S([
".....hhhhh......","....hhhhhhh.....","...hhhsssss.....","..hh.sDHsDH.....","..h..sssss......",".....ssss.......",
"....VVVVVV......","...VVVpVVVV.....","...VV.VVVV.VV...","...VV.VVVV.VV...","...ss.pppp.ss...","......VVVV......",
"......VVVV......",".....NN..NN.....",".....NN..NN.....",".....NN..NN.....",".....NN..NN.....",".....NN..NN.....",
"....kkk..kkk....",]),8,'Vs',4)
EDO=(170,110,230)                                                   # Edo Tensei chakra
SAGE=(255,150,50)                                                   # Sage Mode aura

def revived(name):
    """Logo on a little body, cracked like an Edo Tensei vessel."""
    g=[list(r) for r in ICONS[name]+LOGO_BODY]; rr=random.Random(zlib.crc32(name.encode()))
    for _ in range(9):   # crack lines
        x,y=rr.randint(0,10),rr.randint(0,17)
        for _ in range(3):
            if 0<=x<11 and 0<=y<18 and g[y][x] in 'Hd': g[y][x]='c'
            x+=rr.choice([-1,0,1]); y+=1
    return S([''.join(r) for r in g])
LOGOS={n:revived(n) for n in ICONS}
ORDER=['CODEX','OPENCODE','GROK']

def scale2(spr): return S([''.join(c*2 for c in r) for r in spr for _ in (0,1)])
BIG={n:scale2(s) for n,s in LOGOS.items()}

# ---- background: the Fourth Great Ninja War battlefield ------------------------------------------
def _battlefield(d):
    for y in range(46):                                             # dust-choked sky
        k=y/45; d.line([0,y,W,y],fill=(int(150+88*k),int(118+84*k),int(104+40*k)))
    d.ellipse([128,6,142,20],fill=(250,232,190)); d.ellipse([130,8,140,18],fill=(255,246,220))   # a pale sun
    haze=(196,164,128)
    d.polygon([(0,40),(18,33),(40,35),(62,30),(88,34),(112,29),(140,33),(166,28),(185,31),(185,46),(0,46)],fill=haze)
    rock,shade=(128,96,72),(96,70,54)
    for poly in ([(4,46),(8,24),(12,20),(16,26),(20,46)],       # jagged spires and a broken arch
                 [(150,46),(154,18),(160,14),(166,20),(170,46)],
                 [(170,46),(176,30),(185,28),(185,46)],
                 [(60,46),(64,34),(70,32),(74,46)],
                 [(96,46),(98,38),(104,37),(106,46)]):
        d.polygon(poly,fill=rock)
    for x0,x1 in ((12,20),(160,170),(70,74),(104,106)):
        d.polygon([(x0,46),(x0+2,30),(x1,46)],fill=shade)
    d.rectangle([0,46,W,H],fill=(196,160,112))                      # the plain
    d.line([0,46,W,46],fill=(170,134,92))
    rr=random.Random(1984)
    for _ in range(9):                                              # cracks in the dry earth
        x=rr.randint(0,W); y=rr.randint(48,H-1); pts=[(x,y)]
        for _ in range(4): x+=rr.randint(3,7); y+=rr.randint(-1,1); pts.append((x,y))
        d.line(pts,fill=(150,116,80))
    for x,y,tilt in ((14,52,2),(52,49,-1),(84,55,1),(122,50,-2),(176,54,1),(108,62,2)):   # blades in the ground
        d.line([x,y,x+tilt,y-5],fill=(190,194,204)); d.line([x-1,y-4,x+1,y-4],fill=(90,70,52))
    for x in (40,140):                                              # a torn allied-forces banner
        d.line([x,48,x+1,34],fill=(92,70,52))
        d.polygon([(x+1,35),(x+9,36),(x+7,39),(x+9,42),(x+1,41)],fill=(200,196,184)); d.point((x+4,38),fill=(70,70,90))
    for _ in range(60): d.point((rr.randint(0,W-1),rr.randint(47,H-1)),fill=rr.choice([(176,140,96),(214,182,136)]))
register_bg(THEME, lambda v: (v+140,v+110,v+70), decor=_battlefield)

# ---- effects -----------------------------------------------------------------------------------
@fx('coffin')
def _fx_coffin(d,im,e,f):
    """A coffin rising out of the ground (rise 0..1), clipped at the ground line."""
    _,x,rise,opened=e; x=int(x); top=int(GROUND-18*rise); bot=min(GROUND,top+18)
    if rise<=0: return
    d.rectangle([x-5,top,x+5,bot],fill=(96,62,34),outline=(146,100,58))
    if opened: d.rectangle([x-4,top+1,x+4,bot-1],fill=(24,10,30))
    else:
        if top+12<=GROUND: d.line([x,top+4,x,top+12],fill=(60,36,20))
        if top+7<=GROUND: d.line([x-3,top+7,x+3,top+7],fill=(60,36,20))

@fx('lid')
def _fx_lid(d,im,e,f):
    _,x=e; x=int(x); d.rectangle([x-9,GROUND-1,x+9,GROUND],fill=(96,62,34))

@fx('flake')
def _fx_flake(d,im,e,f):
    _,x,y,c=e; d.rectangle([int(x),int(y),int(x)+1,int(y)],fill=c)

@fx('prompt')   # Codex's ">_" projectile
def _fx_prompt(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y)
    d.line([x+2,y-2,x,y],fill=(240,240,240)); d.line([x,y,x+2,y+2],fill=(240,240,240)); d.line([x+3,y+2,x+6,y+2],fill=(240,240,240))

@fx('rasenshuriken')
def _fx_rasenshuriken(d,im,e,f):
    _,x,y,r=e; x,y=int(x),int(y)
    d.ellipse([x-r,y-r//2,x+r,y+r//2],outline=(200,230,255))
    for k in range(4):
        a=f*0.9+k*math.pi/2
        p=[(x,y),(x+math.cos(a)*r,y+math.sin(a)*r*0.5),(x+math.cos(a+0.5)*r*0.55,y+math.sin(a+0.5)*r*0.28)]
        d.polygon(p,fill=(235,245,255))
    rc=max(2,r//3); d.ellipse([x-rc,y-rc,x+rc,y+rc],fill=(120,190,255)); d.ellipse([x-rc//2,y-rc//2,x+rc//2,y+rc//2],fill=(255,255,255))

@fx('nrt_dome')
def _fx_dome(d,im,e,f):
    """The Rasenshuriken detonating: a white wind sphere laced with needles (a = 0..1 opacity)."""
    _,x,y,r,a=e; x,y,r=int(x),int(y),int(r)
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    md.ellipse([x-r,y-r,x+r,y+r],fill=int(200*a)); md.ellipse([x-r+3,y-r+3,x+r-3,y+r-3],fill=int(150*a))
    im.paste((225,240,255),(0,0),m.filter(ImageFilter.GaussianBlur(1))); d=ImageDraw.Draw(im)
    rr=random.Random(f)
    for _ in range(int(36*a)):                                      # the microscopic wind blades
        t=rr.uniform(0,6.283); L=rr.uniform(0.2,1.0)*r; k=rr.uniform(3,7)
        x0,y0=x+math.cos(t)*L,y+math.sin(t)*L
        d.line([x0,y0,x0+math.cos(t+1.4)*k,y0+math.sin(t+1.4)*k],fill=(120,180,255) if rr.random()<0.5 else (255,255,255))
    d.ellipse([x-r,y-r,x+r,y+r],outline=(160,210,255))

@fx('nrt_nature')
def _fx_nature(d,im,e,f):
    """Nature energy spiralling in on Claude (Sage Mode)."""
    _,x,y=e
    for i in range(14):
        ph=(f*0.05+i*0.071)%1; a=i*2.4+ph*4; L=(1-ph)*46
        d.point((int(x+math.cos(a)*L),int(y+math.sin(a)*L*0.6)),fill=(150,230,120) if i%2 else (255,200,90))

@fx('nrt_mist')
def _fx_mist(d,im,e,f):
    """Purple Edo Tensei mist curling up from a spot."""
    _,x=e; rr=random.Random(f//2+int(x))
    for _ in range(5): d.point((int(x)+rr.randint(-7,7),GROUND-rr.randint(0,20)),fill=rr.choice([(170,110,230),(120,70,170)]))

def flakes(s,spr,cx,feet,t,seed,regen=False,fade=26):
    """Edo Tensei bodies are paper-dust: they flake apart (and, unless sealed, fly back)."""
    rr=random.Random(seed); h=len(spr); w=len(spr[0])
    k=t if not regen else max(0,12-t)
    for j,row in enumerate(spr):
        for i,ch in enumerate(row):
            if ch=='.' or rr.random()<0.5: continue
            vx=rr.uniform(-1.6,1.6); vy=rr.uniform(-1.8,0.4)
            x=cx-w/2+i+vx*k; y=feet-h+j+vy*k+0.08*k*k
            if not regen and rr.random()<t/fade: continue
            s['fx'].append(('flake',x,min(y,GROUND),(200,196,186) if (i+j)%3 else (120,110,104)))

# ---- close-ups ---------------------------------------------------------------------------------
def closeup_coffins(t,f):
    """Primer plano: three coffins, lids fall one by one, the revived logos stare out."""
    im=Image.new('RGB',(W,H),(6,2,10)); d=ImageDraw.Draw(im)
    rr=random.Random(f//2)
    for _ in range(30): d.point((rr.randint(0,W-1),rr.randint(0,H-1)),fill=(60,30,90))
    for i,(cx,name) in enumerate(zip((40,92,144),ORDER)):
        d.rectangle([cx-16,6,cx+16,58],fill=(96,62,34),outline=(146,100,58))
        d.rectangle([cx-13,9,cx+13,55],fill=(22,8,30))
        t0=0.12+0.22*i; p=max(0,min(1,(t-t0)/0.14))
        if p>0:
            rr=random.Random(f+i)
            for _ in range(5): d.point((cx+rr.randint(-12,12),rr.randint(12,54)),fill=(120,70,160))
            spr=BIG[name]; draw(im,spr,cx,54,False,aura=((150,90,210),1) if p>=1 else None,f=f)
            if p>=1: text(d,name,cx-len(name)*2,1,(230,220,255))
        if p<1:   # the lid, sliding down and away
            ly=int(6+60*ease(p)); d.rectangle([cx-16,ly,cx+16,ly+52],fill=(118,78,42),outline=(160,112,64))
            d.line([cx,ly+10,cx,ly+34],fill=(60,36,20),width=2); d.line([cx-8,ly+18,cx+8,ly+18],fill=(60,36,20),width=2)
            d.rectangle([cx-6,ly+26,cx+6,ly+30],outline=(60,36,20))
        if p>0 and t0+0.14<=t<t0+0.2: d.rectangle([cx-16,6,cx+16,58],outline=(255,255,255))   # the thud
    if t<0.08: zoom_lines(d)
    if t>0.9: im=fade_to(im,(60,0,90),0.5*(t-0.9)/0.1)
    return im

def closeup_sage(t,f):
    """Primer plano: the pigment spreads round Claude's eyes, they snap into toad eyes — SENJUTSU!"""
    sage=0.0 if t<0.2 else min(1.0,(t-0.2)/0.3)
    big=Image.new('RGB',(W,H),(40,70,40)); bd=ImageDraw.Draw(big)
    for i in range(16):                                             # a slow green-and-gold burst behind
        a=i*math.tau/16+f*0.02
        bd.polygon([(46,26),(46+math.cos(a)*120,26+math.sin(a)*120),(46+math.cos(a+0.2)*120,26+math.sin(a+0.2)*120)],fill=(60,100,50) if sage<1 else (150,90,30))
    naru_face(bd,ox=18,sage=sage if sage<1 else 1)
    im=big.crop((0,11,92,43)).resize((184,64),Image.NEAREST)
    out=Image.new('RGB',(W,H),(40,70,40)); out.paste(im,(0,0)); im=out; d=ImageDraw.Draw(im)
    if 0.5<=t<0.55: im=fade_to(im,(255,220,140),1-(t-0.5)/0.05); d=ImageDraw.Draw(im); zoom_lines(d,(255,200,90))
    rr=random.Random(f)
    for _ in range(12 if t<0.5 else 24):                            # nature energy flickering past
        x=rr.randint(0,W-1); y=rr.randint(0,H-1); d.point((x,y),fill=(170,240,130) if rr.random()<0.6 else (255,210,100))
    if t>=0.58:
        jj=(f%3)-1 if t<0.68 else 0
        big_text(im,"SENJUTSU!",4,(255,220,120),scale=2,cx=W//2+jj,outline=(90,40,0))
    if t<0.06: zoom_lines(d,(170,240,130))
    if t>0.9: im=fade_to(im,(255,190,90),0.6*(t-0.9)/0.1)
    return im

# ---- the clip ----------------------------------------------------------------------------------
CXS=[96,118,140]                                                    # coffin / creature spots
MOB_X=lambda i: 58+i*20                                             # where they stop, marching on Claude
def clip_edotensei(f):
    s=scene(f,THEME)
    cl=actor(NARU[guard_pose(f)],CX); kb=actor(KABUTO['idle'],EX,flip=True)
    mobs=[]; clones=[]
    # 1) Kuchiyose: Edo Tensei — three coffins rise out of the plain
    if 12<=f<40:
        kb['spr']=KABUTO['attack']; kb['aura']=(EDO,1+(f%2))
        text_y=16 if f>=16 else 16-(16-f)*3
        s['fx'].append(('dmg',"KUCHIYOSE:",W//2-20,max(2,text_y-12),(220,190,255)))
        shout(s,"EDO TENSEI!",(220,180,255),y=text_y,outline=(60,0,90))
    if 18<=f<40:
        for i,x in enumerate(CXS):
            s['under'].append(('coffin',x,min(1,(f-18-i*3)/10) if f>=18+i*3 else 0,False))
            s['fx'].append(('nrt_mist',x))
            if f%2==0: s['fx'].append(('dust',x+random.randint(-7,7),GROUND-random.randint(0,2)))
        if f%3==0: s['shake']=rshake()
    # 2) close-up: the coffins open
    if 40<=f<88: s['image']=closeup_coffins((f-40)/48,f); return s
    if 88<=f<104:
        for i,x in enumerate(CXS):
            s['under'].append(('lid',x-8)); s['under'].append(('coffin',x,1-max(0,(f-96)/8),True))
    # 3) the three revived logos
    for i,name in enumerate(ORDER):
        x=CXS[i]
        if 104<=f<128: x=lerp(CXS[i],MOB_X(i),(f-104)/24)
        elif f>=128: x=MOB_X(i)
        walking=104<=f<128
        m=actor(LOGOS[name],x,y=GROUND-(1 if (f//4+i)%2 and walking else 0),aura=((150,90,210),1))
        hit=130+i*4
        if hit<=f<hit+14: m['vis']=False; flakes(s,LOGOS[name],x,GROUND,f-hit,i)              # blown apart...
        elif hit+14<=f<hit+26: m['vis']=False; flakes(s,LOGOS[name],x,GROUND,f-hit-14,i,regen=True)   # ...and back
        if 262+i*3<=f<290: m['vis']=False; flakes(s,LOGOS[name],x,GROUND,f-262-i*3,50+i)       # sealed: gone
        if 88<=f<262 and m['vis']: mobs.append(m)
    if 108<=f<128:   # Codex fires prompts, Claude guards
        for j in range(3):
            t0=108+j*6
            if t0<=f<t0+12: s['fx'].append(('prompt',lerp(88,34,(f-t0)/12),GROUND-9-j*2))
        if f in (119,125): s['fx'].append(('spark',36,GROUND-8,3))
    # 4) shadow clones, one Rasengan each
    if 104<=f<120: callout(s,"KAGE BUNSHIN NO JUTSU!")
    if 110<=f<150:
        for i in range(3):
            hit=130+i*4; x0=40+i*8; tx=MOB_X(i)-8
            poof(s,x0,f-110)
            if f<hit-6: clones.append(actor(NARU['charge'],x0))
            elif f<hit: clones.append(actor(NARU['dash'],lerp(x0,tx,(f-(hit-6))/6)))
            if hit-10<=f<hit:
                bx=(x0+8) if f<hit-6 else lerp(x0,tx,(f-(hit-6))/6)+8
                s['fx'].append(('nrt_rasengan',bx,GROUND-7,2+(f-hit+10)//4))
            if f==hit: s['fx'].append(('spark',MOB_X(i),GROUND-8,7)); s['shake']=rshake(); s['flash']=0.5; s['fc']=(MOB_X(i),GROUND-8); s['flashc']=(170,220,255)
            poof(s,tx,f-hit-2)
    if 150<=f<168:
        shout(s,"USELESS!",(220,180,255),y=4,cx=128,outline=(60,0,90)); kb.update(spr=KABUTO['attack'],aura=(EDO,1))
        for i in range(3): s['fx'].append(('nrt_mist',MOB_X(i)))
    # 5) Claude gathers nature energy
    if 164<=f<180:
        cl.update(spr=NARU['charge']); s['fx'].append(('nrt_nature',CX,GROUND-8))
        if f>=172: cl['aura']=(SAGE,1)
    # 6) close-up: Sage Mode
    if 180<=f<216: s['image']=closeup_sage((f-180)/36,f); return s
    # 7) the Rasenshuriken
    if 216<=f<246:
        cl.update(spr=NARU['armsup'],aura=(SAGE,1+(f%2)))
        r=int(3+11*min(1,(f-216)/20)); s['fx'].append(('rasenshuriken',CX,GROUND-28,r))
        for j in range(2): s['fx'].append(('circle',CX,GROUND-28,r+3+((f+j*3)%6),(200,230,255)))
        if f>=224: shout(s,"RASENSHURIKEN!",(200,236,255),y=2,outline=(20,40,110))
        if f>=228 and f%2==0: s['shake']=rshake()
        if f>=232: s['fx'].append(('dmg',"!?",EX-6,GROUND-30,(255,255,255)))
    if 246<=f<258:
        cl.update(spr=NARU['punch'],aura=(SAGE,1)); t=(f-246)/12
        x=lerp(CX+6,112,ease(t)); y=lerp(GROUND-28,GROUND-12,t)
        s['fx'].append(('rasenshuriken',x,y,14))
        s['fx'].append(('tracer',int(x)-30,int(x)-14,int(y)))
    # 8) the wind dome swallows them
    if 258<=f<290:
        k=f-258; r=ez(8,44,k/10) if k<22 else 44+2*(f%2); a=1.0 if k<22 else max(0,1-(k-22)/10)
        s['fx'].append(('nrt_dome',112,GROUND-10,r,a))
        if k==0: s['flash']=1.0; s['fc']=(112,GROUND-10); s['flashc']=(230,244,255)
        if k<22: s['shake']=rshake(2 if k<14 else 1)
        cl.update(spr=NARU['guard'],aura=(SAGE,1) if f<276 else None)
        if k<12: shout(s,"RASENSHURIKEN!",(200,236,255),y=2,outline=(20,40,110))
    if 262<=f<296:
        k=f-262; kb.update(spr=KABUTO['hurt'],x=ez(EX,180,k/10),aura=None)
        if k<14: s['fx']+= [('dust',kb['x']-random.randint(2,14),GROUND-random.randint(0,3)) for _ in range(2)]
    # 9) Kabuto limps back in
    if 296<=f<326:
        t=(f-296)/26; kb.update(x=ez(180,EX,t),spr=KABUTO['hurt'] if t<0.7 else KABUTO['idle'],y=GROUND-((f//3)%2 if t<1 else 0))
    s['actors']=mobs+clones+[cl,kb]
    return s

CLIPS = [clip('edotensei', N_, clip_edotensei)]
