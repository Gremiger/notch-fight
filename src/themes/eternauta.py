"""El Eternauta (Oesterheld & Solano Lopez, 1957; the 2025 series): Claude as Juan Salvo in the home-made
insulated suit (grey rubber, the round glass visor, gloves, an old rifle) on a street in Vicente Lopez
under the deadly snowfall: chalets and a Falcon buried in white, a street lamp, flakes that glow. A
cascarudo, a giant beetle, scuttles in; the bullets spark off its shell. Close-up: a Mano at the
console, its many fingers driving the beetles. The cascarudo rears up — and Favalli, Lucas and Polsky
come out of the snow in their suits; they fire together and it goes over on its back. Close-up: four
visors side by side, NADIE SE SALVA SOLO. They go back into the snow; it buries the beetle."""
from engine import *

THEME = 'eternauta'
N_ = 340
CX, KX = 30, 140                                                    # Juan; where the cascarudo stops

# the insulated suit: grey rubber, darker joints, the glass visor and its rim, black boots
JPAL = {'1':(124,130,128),'2':(88,94,94),'3':(150,196,206),'4':(52,54,58),'5':(36,36,40)}
HOOD = ["...111111...","..11111111..",".1111111111."]
ALLIES = [('Favalli',{'1':(112,118,124),'2':(80,86,92)}),('Lucas',{'1':(130,124,112),'2':(94,88,78)}),
          ('Polsky',{'1':(118,128,116),'2':(84,94,82)})]

def _suit(spr):
    g=[list(r) for r in overlay(spr,HOOD,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(h):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='K': continue                                        # his eyes, behind the glass
            if c=='O' and top+1<=y<=top+4 and l+3<=x<=r: g[y][x]='4' if x==l+3 or y in (top+1,top+4) else '3'
            elif c=='O': g[y][x]='1'
            elif c=='o': g[y][x]='5' if y==h-1 else '2'
    return S([''.join(x) for x in g])
JUAN=variant(_suit)
SNOW=(226,236,246)

# ---- background: Vicente Lopez under the snow --------------------------------------------------------
def _street(d):
    for y in range(46):
        k=y/45; d.line([0,y,W,y],fill=(int(22+30*k),int(28+34*k),int(44+40*k)))
    rr=random.Random(1957)
    for x0,w,top in ((2,34,24),(54,40,20),(120,36,26),(160,30,22)):  # chalets with snowy tiled roofs
        d.rectangle([x0,top+8,x0+w,46],fill=(70,64,72))
        d.polygon([(x0-3,top+9),(x0+w//2,top),(x0+w+3,top+9)],fill=(110,60,52))
        d.polygon([(x0-3,top+9),(x0+w//2,top),(x0+w+3,top+9),(x0+w//2,top+3)],fill=SNOW)
        for wx in range(x0+5,x0+w-5,10): d.rectangle([wx,top+14,wx+5,top+20],fill=(30,30,40) if rr.random()<0.7 else (200,170,90))
    d.line([100,46,100,16],fill=(40,40,46)); d.line([100,16,108,16],fill=(40,40,46))     # the street lamp
    d.ellipse([105,15,111,19],fill=(255,236,170))
    for x in (34,176):                                              # bare trees
        d.line([x,46,x,24],fill=(40,34,32))
        for k in range(4): d.line([x,30+k*3,x+(-6 if k%2 else 6),24+k*3],fill=(40,34,32))
    d.rectangle([0,46,W,H],fill=(196,208,222))                      # the snow on the street
    d.line([0,46,W,46],fill=SNOW)
    for _ in range(40): d.point((rr.randint(0,W-1),rr.randint(47,H-1)),fill=rr.choice([(176,190,206),(236,242,250)]))
    # a Ford Falcon buried in snow
    d.rounded_rectangle([58,38,92,48],radius=3,fill=(70,90,110)); d.rectangle([64,33,86,39],fill=(60,78,96))
    d.rectangle([66,34,74,38],fill=(30,36,46)); d.rectangle([76,34,84,38],fill=(30,36,46))
    d.ellipse([62,44,70,52],fill=(30,30,34)); d.ellipse([80,44,88,52],fill=(30,30,34))
    d.rounded_rectangle([63,31,87,34],radius=1,fill=SNOW); d.rectangle([57,37,63,39],fill=SNOW); d.rectangle([87,37,93,39],fill=SNOW)   # snow on the roof and hoods
    d.point((58,42),fill=(250,230,150)); d.point((92,42),fill=(200,60,50))
register_bg(THEME, lambda v: (v+150,v+160,v+176), decor=_street)

@fx('et_lamp')
def _fx_lamp(d,im,e,f):
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).polygon([(108,18),(86,H),(132,H)],fill=46)
    im.paste((255,230,170),(0,0),g.filter(ImageFilter.GaussianBlur(5)))

FLAKES=[(random.Random(i).uniform(0,W),random.Random(i+500).uniform(0,H),3+i%3) for i in range(46)]
@fx('et_snow')
def _fx_snow(d,im,e,f):
    """The deadly snowfall: every flake laps the panel a whole number of times per clip (a clean loop)."""
    for i,(x0,y0,k) in enumerate(FLAKES):
        y=(y0+f*H*k/N_)%H; x=(x0+3*math.sin(2*math.pi*f*2/N_+i))%W
        c=(236,246,255) if i%4 else (190,230,255)
        d.point((int(x),int(y)),fill=c)
        if i%5==0: d.point((int(x)+1,int(y)),fill=(170,210,240))

@fx('et_rifle')
def _fx_rifle(d,im,e,f):
    """The old rifle, held level; fire: the muzzle flash."""
    _,x,y,flip,fire=e; s=-1 if flip else 1; x,y=int(x),int(y)
    d.line([x-s*3,y+1,x+s*9,y],fill=(60,44,30)); d.line([x+s*3,y,x+s*11,y],fill=(40,40,44))
    if fire:
        fx_=x+s*12; d.polygon([(fx_,y-2),(fx_+s*5,y),(fx_,y+2)],fill=(255,230,120)); d.point((fx_+s*2,y),fill=(255,255,255))

# ---- the cascarudo ----------------------------------------------------------------------------------
SHELL,SHELL_D,SHELL_HI=(70,48,34),(40,28,22),(140,104,70)
def cascarudo(d,x,f,state='walk',rear=0.0,walking=False):
    """The giant beetle, facing left. state: walk | dead (on its back); rear 0..1 lifts its front."""
    x=int(x); g=GROUND
    if state=='dead':
        d.ellipse([x-20,g-14,x+20,g+1],fill=SHELL,outline=OUT); d.arc([x-16,g-12,x+16,g-2],200,340,fill=SHELL_HI)
        for k in range(6):                                          # legs in the air, twitching
            lx=x-14+k*6; tw=int(2*math.sin(f*0.8+k)) if f%40<20 else 0
            d.line([lx,g-13,lx-2+tw,g-20,lx+tw,g-24],fill=SHELL_D,width=2)
        return
    lift=int(10*rear)
    for k in range(6):                                              # six jointed legs
        lx=x-14+k*6; ph=math.sin(f*0.9+k*1.7)*3 if walking else 0
        ky=g-8-(lift if k<2 else 0)
        d.line([lx,ky,lx-3+ph,ky-4,lx-6+ph,g],fill=SHELL_D,width=2)
    pts=[(x-18,g-8-lift),(x-10,g-20-lift),(x+10,g-22),(x+22,g-12),(x+20,g-4),(x-14,g-4)]
    d.polygon(pts,fill=SHELL,outline=OUT)                            # the shell
    d.line([x-6,g-20-lift//2,x+16,g-8],fill=SHELL_D); d.line([x-10,g-14-lift//2,x+12,g-18],fill=SHELL_HI)
    hx,hy=x-22,g-11-lift
    d.ellipse([hx-6,hy-5,hx+6,hy+5],fill=SHELL_D,outline=OUT)        # the head
    d.point((hx-3,hy-2),fill=(255,90,40)); d.point((hx-1,hy-3),fill=(255,90,40))
    op=2+int(3*rear)+(1 if f%6<3 else 0)                             # the mandibles
    d.line([hx-5,hy+1,hx-11,hy-op],fill=SHELL_HI,width=2); d.line([hx-5,hy+3,hx-11,hy+3+op],fill=SHELL_HI,width=2)
    for k in (-1,1): d.line([hx-2,hy-4,hx-8,hy-12+k*2+int(math.sin(f*0.3+k))],fill=SHELL_D)   # antennae

@fx('et_cascarudo')
def _fx_cascarudo(d,im,e,f):
    _,x,state,rear,walking,a=e
    if a>=1: cascarudo(d,x,f,state,rear,walking); return
    L=im.copy(); cascarudo(ImageDraw.Draw(L),x,f,state,rear,walking); im.paste(Image.blend(im,L,a))

@fx('et_mound')
def _fx_mound(d,im,e,f):
    """The snow burying the beetle (k 0..1)."""
    _,x,k=e; h=int(18*k)
    if h>0: d.ellipse([x-24,GROUND-h,x+24,GROUND+4],fill=SNOW); d.arc([x-20,GROUND-h+2,x+20,max(GROUND,GROUND-h+2)],200,340,fill=(250,252,255))

# ---- close-ups --------------------------------------------------------------------------------------
def closeup_mano(t,f):
    """Primer plano: a Mano at its console in the dark, the dozens of fingers flickering over the keys;
    the screens show the beetles in the snow."""
    im=Image.new('RGB',(W,H),(10,12,18)); d=ImageDraw.Draw(im)
    for i,sx in enumerate((14,66,118)):                              # the screens
        d.rectangle([sx,4,sx+50,26],fill=(16,40,36),outline=(60,90,80))
        rr=random.Random(i)
        for _ in range(16): d.point((sx+rr.randint(2,48),4+(rr.randint(0,22)+f//2)%22),fill=(200,230,220))
        bx=sx+18+int(8*math.sin(f*0.1+i)); d.ellipse([bx,16,bx+14,24],fill=(40,30,22)); d.point((bx+1,19),fill=(255,90,40))
    d.polygon([(0,H),(20,36),(166,36),(185,H)],fill=(40,44,52))      # the console
    rr=random.Random(7)
    for _ in range(30): d.rectangle([(x:=rr.randint(22,160)),(y:=rr.randint(40,60)),x+2,y+1],fill=rr.choice([(220,80,60),(80,200,120),(230,200,80),(90,90,110)]) if rr.random()<0.7 else (60,60,70))
    px,py=92,62                                                     # the palm, below; the fingers fan out
    skin,line=(196,184,160),(120,106,90)
    d.ellipse([px-22,py-10,px+22,py+16],fill=skin,outline=line)
    n=18
    for i in range(n):
        a=math.pi*(1.08+0.84*i/(n-1)); L=24+(i%3)*4
        tap=3*max(0,math.sin(f*1.3+i*2.1))                           # each finger taps on its own beat
        x1,y1=px+math.cos(a)*L,py+math.sin(a)*(L-tap)
        d.line([px+math.cos(a)*14,py+math.sin(a)*8,x1,y1],fill=line,width=3); d.line([px+math.cos(a)*14,py+math.sin(a)*8,x1,y1],fill=skin,width=1)
        d.point((int(x1),int(y1)),fill=(236,226,206))
    if t<0.06: zoom_lines(d,(120,200,180))
    if t>0.9: im=fade_to(im,(0,0,0),0.6*(t-0.9)/0.1)
    return im

def visor(d,cx,cy,shade,f,i):
    """One suited head, face-on: the rubber hood, the round visor, Claude's eyes behind the glass."""
    d.ellipse([cx-17,cy-20,cx+17,cy+26],fill=shade,outline=(30,32,34))
    d.ellipse([cx-12,cy-12,cx+12,cy+12],fill=(40,42,46))
    d.ellipse([cx-10,cy-10,cx+10,cy+10],fill=(150,196,206))
    d.ellipse([cx-8,cy-8,cx+8,cy+8],fill=(217,119,87))               # the face behind the glass
    d.rectangle([cx-5,cy-3,cx-3,cy+1],fill=(24,14,12)); d.rectangle([cx+3,cy-3,cx+5,cy+1],fill=(24,14,12))
    d.arc([cx-9,cy-9,cx+3,cy+3],200,260,fill=(236,246,255),width=2)   # the shine on the glass
    if (f//10+i)%3==0: d.ellipse([cx-6,cy+3,cx+6,cy+8],fill=(196,214,222))   # breath fogging it

def closeup_juntos(t,f):
    """Primer plano: four visors side by side in the snow — NADIE SE SALVA SOLO."""
    im=Image.new('RGB',(W,H),(30,36,52)); d=ImageDraw.Draw(im)
    shades=[JPAL['1']]+[p['1'] for _,p in ALLIES]
    for i,cx in enumerate((24,62,100,138)):
        k=min(1,max(0,(t-i*0.08)/0.12))
        if k>0: visor(d,cx,int(lerp(H+30,30,ease(k))),shades[i],f,i)
    for j,(x0,y0,k) in enumerate(FLAKES):
        y=(y0+f*H*k/N_)%H; d.point((int((x0*1.3)%W),int(y)),fill=(236,246,255))
    if t>=0.35: FX['et_say'](d,im,('et_say',),f)
    if t<0.05: zoom_lines(d)
    if t>0.9: im=fade_to(im,SNOW,0.6*(t-0.9)/0.1)
    return im

@fx('et_say')
def _fx_say(d,im,e,f):
    """NADIE SE / SALVA SOLO, over the bottom of the visors."""
    for j,(w,y) in enumerate((("NADIE SE",34),("SALVA SOLO",48))):
        big_text(im,w,y,(255,255,255) if j==0 else (255,226,120),scale=2,cx=W//2,outline=(20,30,50))

# ---- the clip ---------------------------------------------------------------------------------------
GRIP={'guard':(13,4),'guard2':(13,4),'punch':(16,5),'charge':(15,5)}
ALLY_X=[6,44,62]
RX=110                                                              # where the beetle rears up
def clip_nevada(f):
    s=scene(f,THEME)
    s['under'].append(('et_lamp',))
    jx,jpose,fire=CX,guard_pose(f),False
    kx,kstate,rear,walking,ka=None,'walk',0.0,False,1.0
    # 1) the cascarudo scuttles in; the bullets spark off it
    if 14<=f<306: kx=ez(220,KX,(f-14)/26); walking=f<40
    if 44<=f<82:
        k=(f-44)%8; jpose='punch'; fire=k<2
        if k==2: s['fx'].append(('spark',KX-14,GROUND-14+((f//8)%3)*3,3))
        callout(s,"PAC! PAC! PAC!",c=(255,226,150))
    # 2) close-up: the Mano
    if 82<=f<138: s['image']=closeup_mano((f-82)/56,f); return s
    # 3) it rears up and comes on
    if 138<=f<180:
        kx=ez(KX,RX,(f-138)/30); walking=f<168; rear=min(1,(f-150)/10) if f>=150 else 0
        if f>=160: s['shake']=rshake(1)
    # 4) Favalli, Lucas and Polsky, out of the snow: they fire together
    allies=[]
    for i,(name,pal) in enumerate(ALLIES):
        t0=170+i*5
        if t0<=f<306:
            ax=ALLY_X[i] if f>=t0+10 else lerp(-10,ALLY_X[i],(f-t0)/10)
            if f>=278: ax=lerp(ALLY_X[i],-20-i*4,(f-278)/26)
            apose='punch' if 190<=f<214 else guard_pose(f+i*3)
            allies.append((ax,apose,dict(JPAL,**pal),190<=f<214 and (f+i*3)%6<2,f>=278))
    if 180<=f<214:
        kx=RX; rear=1.0
        if 190<=f<214: jpose,fire='punch',(f%6)<2; s['fx'].append(('spark',RX-12+random.randint(-6,6),GROUND-16+random.randint(-6,6),3))
        if 204<=f<214: s['shake']=rshake(2)
    if 214<=f<306:
        kx,kstate=RX,'dead'
        if f<218: s['shake']=rshake(2)
    if 190<=f<214: callout(s,"FUEGO!",c=(255,226,150))
    # 5) close-up: four visors — NADIE SE SALVA SOLO
    if 222<=f<272: s['image']=closeup_juntos((f-222)/50,f); return s
    # 6) back into the snow; the snow buries the beetle
    if 280<=f<332: s['under'].append(('et_mound',RX,min(1,(f-280)/22) if f<308 else max(0,1-(f-308)/24)))
    if f>=304: kx=None
    if kx is not None: s['under'].insert(1,('et_cascarudo',kx,kstate,rear,walking,ka))
    acts=[]
    for ax,apose,pal,afire,leaving in allies:
        acts.append(actor(JUAN[apose],ax,pal=pal,flip=leaving))
        hx,hy=hand_at(JUAN[apose],ax,GROUND,leaving,*GRIP.get(apose,(13,4)),h=11)
        s['fx'].append(('et_rifle',hx,hy,leaving,afire))
    acts.append(actor(JUAN[jpose],jx,pal=JPAL))
    hx,hy=hand_at(JUAN[jpose],jx,GROUND,False,*GRIP.get(jpose,(13,4)),h=11)
    s['fx'].append(('et_rifle',hx,hy,False,fire))
    s['actors']=acts
    s['under'].insert(1,('et_snow',))
    return s

CLIPS = [clip('nevada', N_, clip_nevada)]
