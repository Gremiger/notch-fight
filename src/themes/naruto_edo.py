"""Naruto sub-theme "naruto-edo": Claude (Naruto) vs Kabuto. Kabuto reanimates the Codex,
OpenCode and Grok logos with Edo Tensei (coffin close-up); Claude answers with shadow clones,
Rasengan and a Rasenshuriken that erases them for good."""
import zlib
from engine import *
from themes.nrt import NARU, poof, callout   # same franchise: reuse Claude-as-Naruto

THEME = 'naruto-edo'

PAL.update({'c':(78,66,66),'x':(96,62,34),'l':(146,100,58)})

KABUTO=poses(S([
".....hhhhh......","....hhhhhhh.....","...hhhsssss.....","..hh.sDHsDH.....","..h..sssss......",".....ssss.......",
"....VVVVVV......","...VVVpVVVV.....","...VV.VVVV.VV...","...VV.VVVV.VV...","...ss.pppp.ss...","......VVVV......",
"......VVVV......",".....NN..NN.....",".....NN..NN.....",".....NN..NN.....",".....NN..NN.....",".....NN..NN.....",
"....kkk..kkk....",]),8,'Vs',4)

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

register_bg(THEME, lambda v: (v//2+6,v//3,v//2+10), clip_ground=True)   # coffins rise OUT of the ground

@fx('coffin')
def _fx_coffin(d,im,e,f):
    _,x,rise,opened=e; x=int(x); top=int(GROUND-18*rise)
    d.rectangle([x-5,top,x+5,top+18],fill=(96,62,34),outline=(146,100,58))
    if opened: d.rectangle([x-4,top+1,x+4,top+17],fill=(24,10,30))
    else: d.line([x,top+4,x,top+12],fill=(60,36,20)); d.line([x-3,top+7,x+3,top+7],fill=(60,36,20))

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

def closeup_coffins(t,f):
    """Primer plano: three coffins, lids fall one by one, the revived logos stare out."""
    im=Image.new('RGB',(W,H),(6,2,10)); d=ImageDraw.Draw(im)
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
    if t<0.08:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    if t>0.9: im=Image.blend(im,Image.new('RGB',(W,H),(60,0,90)),0.5*(t-0.9)/0.1)
    return im

CX=[96,118,140]   # coffin / creature spots
def clip_edotensei(f):
    s=scene(f,THEME)
    cl=actor(NARU[guard_pose(f)],30); kb=actor(KABUTO['idle'],164,flip=True)
    mobs=[]; clones=[]
    if 12<=f<30: kb['spr']=KABUTO['attack']; callout(s,"KUCHIYOSE: EDO TENSEI!",c=(200,150,255))
    if 18<=f<36:
        for i,x in enumerate(CX):
            s['under'].append(('coffin',x,min(1,(f-18-i*3)/10) if f>=18+i*3 else 0,False))
            if f%2==0: s['fx'].append(('dust',x+random.randint(-6,6),GROUND-random.randint(0,2)))
        if f%3==0: s['shake']=rshake()
    if 36<=f<84: s['image']=closeup_coffins((f-36)/48,f); return s
    if 84<=f<100:
        for i,x in enumerate(CX):
            s['under'].append(('lid',x-8)); s['under'].append(('coffin',x,1-max(0,(f-92)/8),True))
    # the three revived logos
    X0={0:96,1:118,2:140}
    for i,name in enumerate(ORDER):
        x=X0[i]; vis=84<=f<200
        if 100<=f<124: x=lerp(X0[i],58+i*20,(f-100)/24)
        elif f>=124: x=58+i*20
        m=actor(LOGOS[name],x,y=GROUND-(1 if (f//4+i)%2 and 100<=f<124 else 0),flip=False,aura=((150,90,210),1) if 84<=f<200 else None)
        hit=126+i*4
        if hit<=f<hit+14: m['vis']=False; flakes(s,LOGOS[name],x,GROUND,f-hit,i)              # blown apart...
        elif hit+14<=f<hit+26: m['vis']=False; flakes(s,LOGOS[name],x,GROUND,f-hit-14,i,regen=True)   # ...and back
        if 190+i*4<=f<216: m['vis']=False; flakes(s,LOGOS[name],x,GROUND,f-190-i*4,50+i)          # sealed: gone
        if vis and m['vis']: mobs.append(m)
    if 104<=f<124:   # Codex fires prompts, Claude guards
        for j in range(3):
            t0=104+j*6
            if t0<=f<t0+12: s['fx'].append(('prompt',lerp(90,34,(f-t0)/12),GROUND-9-j*2))
        if f in (115,121): s['fx'].append(('spark',36,GROUND-8,3))
    if 100<=f<116: callout(s,"KAGE BUNSHIN NO JUTSU!")
    if 106<=f<146:   # three clones, one Rasengan each
        for i in range(3):
            hit=126+i*4; x0=40+i*8
            poof(s,x0,f-106)
            if f<hit-6: clones.append(actor(NARU['charge'],x0))
            elif f<hit: t=(f-(hit-6))/6; clones.append(actor(NARU['dash'],lerp(x0,50+i*20,t)))
            if hit-10<=f<hit: s['fx'].append(('orbc',(x0+8) if f<hit-6 else lerp(x0,50+i*20,(f-(hit-6))/6)+8,GROUND-7,2,((170,220,255),(70,150,255))))
            if f==hit: s['fx'].append(('spark',58+i*20,GROUND-8,6)); s['shake']=rshake()
            poof(s,50+i*20,f-hit-2)
    if 140<=f<156: callout(s,"USELESS!",c=(200,150,255)); kb['spr']=KABUTO['attack']
    if 150<=f<190:   # Rasenshuriken
        cl['spr']=NARU['armsup']; cl['aura']=((160,210,255),1+(f%2))
        r=int(3+9*min(1,(f-150)/24)); s['fx'].append(('rasenshuriken',30,GROUND-26,r))
        if f>=160: callout(s,"RASENSHURIKEN!",c=(160,220,255))
        if f>=170 and f%3==0: s['shake']=rshake()
    if 190<=f<206:
        cl['spr']=NARU['punch']; x=lerp(36,200,(f-190)/16)
        s['fx'].append(('rasenshuriken',x,GROUND-10,12))
        for j in range(2): s['fx'].append(('circle',x,GROUND-10,8+j*5+(f%3),(200,230,255)))
        if f in (192,196,200): s['flash']=0.7; s['fc']=(x,GROUND-10); s['flashc']=(210,235,255); s['shake']=rshake(2)
    if 204<=f<220: kb.update(spr=KABUTO['hurt'],x=ez(164,176,(f-204)/8))
    if 220<=f<244: kb.update(x=ez(176,164,(f-220)/24),spr=KABUTO['hurt'] if f<230 else KABUTO['idle'])
    s['actors']=mobs+clones+[cl,kb]
    return s

CLIPS = [clip('edotensei', 264, clip_edotensei)]
