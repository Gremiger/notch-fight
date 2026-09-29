"""Jujutsu Kaisen sub-theme "jjk-sukuna": the Domain Expansion battle. Sukuna opens Malevolent
Shrine; Claude (Gojo) answers with Unlimited Void (eye close-up), freezes him with infinite
information and lands four Black Flashes before both domains shatter."""
from engine import *
from themes.jjk import GOJO, SUKUNA   # same franchise: reuse Claude-as-Gojo and Sukuna (+ 'slash' fx)

THEME = 'jjk-sukuna'

register_bg(THEME, lambda v: (v+6,v//4,v//3+4))

def _shrine():
    """Malevolent Shrine: two-tier roof, fanged mouth between the pillars, a pile of skulls."""
    w,h=44,36; im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.polygon([(3,1),(8,3),(36,3),(41,1),(38,9),(6,9)],fill=(120,16,24)); d.line([(6,9),(38,9)],fill=(190,40,40))
    d.polygon([(0,10),(5,12),(39,12),(44,10),(41,17),(3,17)],fill=(140,20,30)); d.line([(3,17),(41,17)],fill=(200,50,44))
    for x in (7,15,28,36): d.rectangle([x,17,x+1,30],fill=(64,18,20))
    d.rectangle([17,18,27,29],fill=(40,0,4))
    for x in range(17,28,2): d.polygon([(x,18),(x+2,18),(x+1,21)],fill=(236,226,206)); d.polygon([(x,29),(x+2,29),(x+1,26)],fill=(236,226,206))
    for i,x in enumerate(range(2,43,5)):
        y=31+(i%2); d.ellipse([x,y,x+4,y+4],fill=(222,212,190)); d.point((x+1,y+2),fill=(30,20,20)); d.point((x+3,y+2),fill=(30,20,20))
    for x in (8,22,36): d.line([(x,1),(x,-1)],fill=(190,40,40)); d.point((x,0),fill=(220,60,50))
    return im
SHRINE=_shrine()

@fx('shrine')
def _fx_shrine(d,im,e,f):
    """Rises out of the ground: only the part above GROUND is shown."""
    _,x,rise=e; w,h=SHRINE.size; top=int(GROUND+1-h*rise); vis=GROUND+1-top
    if vis>0: im.paste(SHRINE.crop((0,0,w,vis)),(int(x)-w//2,top),SHRINE.crop((0,0,w,vis)))

@fx('redsky')
def _fx_redsky(d,im,e,f):
    _,a=e; im.paste(fade_to(im,(70,0,10),a))

_STARS=[(random.Random(i).randint(0,W-1),random.Random(i*7+1).randint(0,H-1),random.Random(i*3+2).random()) for i in range(90)]
@fx('void')
def _fx_void(d,im,e,f):
    """Unlimited Void: a starfield with a slow galaxy swirl, inside an ellipse of radius r."""
    _,cx,cy,r=e
    v=Image.new('RGB',(W,H),(2,2,10)); vd=ImageDraw.Draw(v)
    for k in range(3):
        rr=16+k*14; a0=(f*6+k*120)%360
        vd.arc([W//2-rr*2,H//2-rr,W//2+rr*2,H//2+rr],a0,a0+140,fill=(60,40,140) if k%2 else (40,80,170))
    for i,(x,y,p) in enumerate(_STARS):
        c=(255,255,255) if (i+f//3)%5 else (150,190,255)
        vd.point((x,y),fill=c)
        if p>0.9 and (f+i)%8<4: vd.point((x+1,y),fill=(180,200,255)); vd.point((x-1,y),fill=(180,200,255))
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r*0.7,cx+r,cy+r*0.7],fill=255)
    im.paste(v,(0,0),m)
    if r<200: ImageDraw.Draw(im).ellipse([cx-r,cy-r*0.7,cx+r,cy+r*0.7],outline=(170,210,255))

@fx('blackflash')
def _fx_blackflash(d,im,e,f):
    """Black Flash: black lightning with a red rim, radiating from the point of impact."""
    _,x,y,sz=e; rr=random.Random(f)
    for k in range(6):
        a=k*1.05+rr.random()*0.5; pts=[(x,y)]; px,py=x,y
        for j in range(3): px+=math.cos(a)*sz/3+rr.randint(-2,2); py+=math.sin(a)*sz/5+rr.randint(-2,2); pts.append((px,py))
        d.line(pts,fill=(230,30,40),width=3); d.line(pts,fill=(0,0,0),width=1)
    d.ellipse([x-3,y-3,x+3,y+3],fill=(0,0,0),outline=(255,60,60))

def closeup_eyes(t,f):
    """Primer plano: the blindfold slides up over Claude's face and the Six Eyes light up."""
    im=Image.new('RGB',(W,H),(217,119,87)); d=ImageDraw.Draw(im)
    for x in range(0,W,6): d.line([x,56,x+3,64],fill=(168,80,54))
    hair=[(0,0)]+[(x,8+(5 if (x//12)%2 else 0)) for x in range(0,W+12,6)]+[(W,0)]
    d.polygon(hair,fill=(242,242,250)); d.line(hair[1:-1],fill=(186,186,206))
    open_=ease((t-0.15)/0.3)
    for ex in (74,118):
        d.rounded_rectangle([ex-8,18,ex+8,48],radius=6,fill=(24,14,12))
        if open_>0:
            d.rounded_rectangle([ex-6,21,ex+6,45],radius=5,fill=(40,110,240))
            d.rounded_rectangle([ex-4,24,ex+4,42],radius=4,fill=(120,200,255))
            d.ellipse([ex-2,30,ex+2,36],fill=(230,248,255))
            d.point((ex-3,25),fill=(255,255,255)); d.point((ex+2,26),fill=(255,255,255))
            if (f//2)%2: d.point((ex+3,40),fill=(255,255,255))
    by=int(16-40*open_)   # the blindfold
    if by>-18: d.rectangle([0,by,W,by+34],fill=(26,26,34)); d.line([0,by+33,W,by+33],fill=(60,60,76))
    if t>0.5: text(d,"MURYOKUSHO",W//2-20,52,(200,230,255))
    if t>0.72:   # the void swallows the frame from between the eyes
        r=int((t-0.72)/0.28*220); _fx_void(d,im,('void',96,33,r),f)
    if t<0.06: zoom_lines(d)
    return im

def clip_domain(f):
    s=scene(f,THEME)
    cl=actor(GOJO[guard_pose(f)],30); sk=actor(SUKUNA['idle'],150,flip=True)
    domain=20<=f<200
    # 1) Malevolent Shrine
    if 12<=f<44: sk['spr']=SUKUNA['attack']
    if 12<=f<30: callout(s,"RYOIKI TENKAI!",c=(255,90,90))
    elif 30<=f<50: callout(s,"FUKUMA MIZUSHI",c=(255,90,90))
    if 36<=f<200: s['under'].append(('redsky',min(0.55,(f-36)/12*0.55)))
    if domain and f<160: s['under'].append(('shrine',166,min(1,(f-20)/20)))
    if 20<=f<40 and f%3==0: s['shake']=rshake()
    if 44<=f<86:   # Dismantle everywhere; Infinity keeps it off Claude
        rr=random.Random(f)
        for j in range(5):
            x=rr.randint(20,W-10); y=rr.randint(12,GROUND-2)
            if abs(x-38)<14 and y>GROUND-26: s['fx'].append(('spark',46,y,2))
            else: s['fx'].append(('slash',x,y,6,(255,200,200)))
        for r in range(3): s['fx'].append(('circle',38,GROUND-10,5+r*4+(f%3),(90,150,255) if r%2 else (170,210,255)))
    # 2) Unlimited Void (close-up)
    if 86<=f<98: cl['spr']=GOJO['armsup']; callout(s,"RYOIKI TENKAI!",c=(150,200,255)); cl['aura']=((150,200,255),1)
    if 98<=f<146: s['image']=closeup_eyes((f-98)/48,f); return s
    if 146<=f<198: s['under'].append(('void',30,GROUND-10,min(260,90+(f-146)*14)))
    # 3) infinite information: Sukuna freezes
    if 146<=f<200:
        sk.update(spr=SUKUNA['hurt'],x=150+(1 if f%4<2 else 0))
        rr=random.Random(f*3)
        for j in range(4):
            ang=rr.random()*6.28; L=(1-((f+j*5)%10)/10)*28
            s['fx'].append(('dmg',str(rr.randint(0,9)),150+math.cos(ang)*L,GROUND-18+math.sin(ang)*L*0.6,(170,210,255)))
    # 4) four Black Flashes
    if 160<=f<168: cl.update(spr=GOJO['dash'],x=lerp(30,132,(f-160)/8))
    if 168<=f<198:
        k=(f-168)//7; ph=(f-168)%7; px=150+k*6
        cl.update(spr=GOJO['punch' if ph<4 else 'guard'],x=px-18)
        sk.update(x=px+(2 if ph<3 else 0))
        if ph<3: s['fx'].append(('blackflash',px-6,GROUND-8,16+ph*4))
        if ph==0: s['flash']=0.8; s['fc']=(px-6,GROUND-8); s['flashc']=(255,40,50); s['shake']=rshake(2)
        callout(s,"KOKUSEN!",c=(255,70,70))
    if 196<=f<216:   # both domains shatter
        t=(f-196)/20; rr=random.Random(5)
        for j in range(40):
            a=rr.random()*6.28; sp=rr.uniform(20,110)
            x=30+math.cos(a)*sp*(0.3+t); y=GROUND-10+math.sin(a)*sp*0.5*(0.3+t)+20*t*t
            s['fx'].append(('shard',x,y,(200,220,255) if j%3 else (255,120,120)))
        if f==198: s['flash']=0.7; s['fc']=(90,GROUND-10); s['flashc']=(220,235,255)
    if 198<=f<222: cl.update(spr=GOJO['guard'],x=ez(156,30,(f-198)/24))
    if 198<=f<240: sk.update(spr=SUKUNA['hurt'] if f<222 else SUKUNA['idle'],x=ez(174,150,(f-212)/28) if f>=212 else 174)
    s['actors']=[cl,sk]
    return s

CLIPS = [clip('domain', 264, clip_domain)]
