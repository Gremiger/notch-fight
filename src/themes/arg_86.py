"""Argentina sub-theme "arg-86": Mexico 1986, Argentina 2-1 England, at the Azteca under the sun.
Claude as Diego - the '86 albiceleste, curly dark hair, the captain's armband. Two clips on the same
neutral pose (the ball in the centre circle):
  mano  - a high looping ball into the box; Diego and Shilton go up together; close-up: his fist gets there
          before the keeper's gloves. The goal stands: LA MANO DE DIOS. Told with a wink, not as a fight.
  siglo - from his own half he turns and runs, past four Englishmen one by one, sits Shilton down and
          walks it in; close-up: the commentary as captions, BARRILETE COSMICO, then GOLAZO.
England: generic figures in white, the keeper in grey - kit colours, never likenesses."""
from engine import *
from themes.arg import PLAYER, DIVE, KIT_ARG, CELESTE, WHITE, albiceleste, draw_goal   # same country

THEME = 'arg-86'
N_MANO, N_SIGLO = 250, 330

INK = (20,20,24)
DPAL = {'c':CELESTE, 'W':WHITE, 'b':(24,24,28), 'y':(236,200,60), 'h':(30,24,22), 'H':(56,44,40)}
KIT_ENG  = {'j':(240,240,240), 'J':(240,240,240), 's':(226,184,150), 'h':(120,80,50), 'p':(30,40,90)}
KIT_KEEP = {'j':(120,120,128), 'J':(120,120,128), 's':(226,184,150), 'h':(90,70,50), 'p':(40,40,48)}
KIT_REF  = {'j':(30,30,34), 'J':(30,30,34), 's':(210,160,120), 'h':(40,30,26), 'p':(30,30,34)}

CURLS = ["h.H.hh.H.h..", ".hhHhhhhHhh.", "hHhhhhhhhhHh"]
DIEGO=variant(lambda s: albiceleste(overlay(s,CURLS,-1,0)))

# ---------------------------------------------------------------- the Azteca at noon
def _azteca(d):
    """Midday sky, the Azteca's tiers packed with fans, a sun-bleached pitch, the goal on the right."""
    for y in range(0,12):
        t=y/12; d.line([0,y,W,y],fill=(int(lerp(120,170,t)),int(lerp(180,210,t)),int(lerp(236,240,t))))
    d.rectangle([0,12,W,28],fill=(96,90,86))
    rr=random.Random(1986)
    for y in range(13,28,2):
        for x in range((y//2)%2,W,3):
            if rr.random()<0.75: d.point((x,y),fill=rr.choice(((116,172,223),(240,240,240),(220,60,60),(240,200,60),(60,60,70))))
    for x in range(0,W,16): d.rectangle([x,28,x+7,GROUND],fill=(110,140,70))
    for x in range(8,W,16): d.rectangle([x,28,x+7,GROUND],fill=(122,152,78))
    d.line([0,28,W,28],fill=(240,240,230))
    d.line([20,28,20,GROUND],fill=(240,240,230)); d.arc([4,32,36,GROUND+10],-60,60,fill=(240,240,230))   # halfway line, circle
    d.line([150,34,150,GROUND],fill=(240,240,230))
    draw_goal(d,176,1)
register_bg(THEME, lambda v: (v//2+40,v+30,v//3+10), decor=_azteca)

@fx('a86_trail')
def _fx_trail(d,im,e,f):
    """Speed streaks behind Diego's run."""
    _,x,y=e
    for k in range(4): d.line([x-10-k*5,y-4-k*2,x-4-k*5,y-4-k*2],fill=(250,250,240))

@fx('a86_big')
def _fx_big(d,im,e,f):
    _,txt,y,c=e; big_text(im,txt,y,c,shadow=(0,0,0),outline=(0,0,0))

def closeup_hand(t,f):
    """Primer plano: in the air, Diego's fist beats Shilton's gloves to the ball."""
    im=Image.new('RGB',(W,H),(150,196,238)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([0,y,W,y],fill=(int(lerp(130,176,y/H)),int(lerp(186,214,y/H)),int(lerp(236,242,y/H))))
    d.ellipse([150,4,176,30],fill=(255,244,200))                                           # the sun
    rise=ease(min(1,t/0.35))
    # Shilton, from the right: grey sleeve, big gloves reaching up
    sx=int(lerp(W+10,112,rise)); sy=int(lerp(H+10,26,rise))
    d.line([W+4,H+4,sx+8,sy+8],fill=KIT_KEEP['j'],width=10)
    d.rounded_rectangle([sx-4,sy-4,sx+14,sy+10],radius=4,fill=(250,250,250),outline=(80,80,80))
    # Diego, from the left: albiceleste sleeve, the fist up
    fx_=int(lerp(-10,92,rise)); fy=int(lerp(H+10,16,rise))
    for k in range(6): d.line([-4+k*2,H+4,fx_-6+k*2,fy+10],fill=CELESTE if k%2 else WHITE,width=2)
    d.rounded_rectangle([fx_-8,fy-6,fx_+6,fy+8],radius=4,fill=(217,119,87),outline=(120,60,40))
    for k in range(3): d.line([fx_+6,fy-3+k*4,fx_+2,fy-3+k*4],fill=(168,80,54))
    # the ball: dropping in, off the fist, away towards the goal (right, down)
    if t<0.35: bx,by=lerp(100,98,t/0.35),lerp(-10,10,t/0.35)
    else: q=min(1,(t-0.35)/0.35); bx,by=lerp(98,W+10,q),lerp(10,40,q)
    d.ellipse([bx-5,by-5,bx+5,by+5],fill=(250,250,250),outline=(40,40,40)); d.point((int(bx),int(by)),fill=(40,40,40))
    if 0.33<t<0.42: spark(d,96,12,5,(255,255,255))
    if t<0.06: zoom_lines(d)
    return im

def closeup_joy(t,f):
    """Primer plano: Diego celebrating, arms up, the crowd behind; the commentary as captions."""
    im=Image.new('RGB',(W,H),(96,90,86)); d=ImageDraw.Draw(im)
    rr=random.Random(10+f//4)
    for _ in range(160): d.point((rr.randint(0,W),rr.randint(0,H)),fill=rr.choice(((116,172,223),(240,240,240),(220,60,60),(240,200,60))))
    cx=46
    for sx in (-1,1):                                                                     # arms up, fists
        d.line([cx+sx*16,44,cx+sx*26,12],fill=CELESTE,width=6)
        d.ellipse([cx+sx*26-5,4,cx+sx*26+5,14],fill=(217,119,87),outline=(120,60,40))
    d.rectangle([cx-20,38,cx+20,H],fill=WHITE)
    for x in range(cx-20,cx+20,8): d.rectangle([x,38,x+3,H],fill=CELESTE)
    d.rectangle([cx-16,10,cx+16,40],fill=(217,119,87)); d.rectangle([cx+12,10,cx+16,40],fill=(168,80,54))
    d.ellipse([cx-20,2,cx+20,18],fill=DPAL['h'])                                           # the curls
    for k in range(7): d.ellipse([cx-20+k*6,0,cx-14+k*6,8],fill=DPAL['H'])
    d.rectangle([cx-10,22,cx-6,27],fill=(24,14,12)); d.rectangle([cx+4,22,cx+8,27],fill=(24,14,12))
    d.chord([cx-8,28,cx+8,38],0,180,fill=(70,20,20))                                         # shouting
    if 0.1<=t<0.58: big_text(im,"BARRILETE",10,(250,250,250),cx=132,shadow=(0,0,0),outline=(0,0,0)); big_text(im,"COSMICO",28,CELESTE,cx=132,shadow=(0,0,0),outline=(0,0,0))
    if t>=0.6: big_text(im,"GOLAZO",20,(250,210,60),cx=132,shadow=(0,0,0),outline=(0,0,0))
    if t<0.06: zoom_lines(d)
    return im

# ---------------------------------------------------------------- clip 1: la mano de Dios
def clip_mano(f):
    s=scene(f,THEME)
    dx,dy,dpose,dflip=40,GROUND,guard_pose(f),False
    ball=(49,GROUND-2) if f<14 or f>=236 else None
    others=[]; kx,ky,kpose=172,GROUND,'idle'
    if 14<=f<44: dx,dpose=ez(40,118,(f-14)/30),'dash'; ball=(dx+9,GROUND-2)
    if 44<=f<50: dx=118; ball=(lerp(127,146,(f-44)/6),GROUND-2)
    if 44<=f<126: others.append(actor(PLAYER['attack' if 48<=f<54 else 'idle'],150,flip=True,pal=KIT_ENG))
    if 50<=f<78:                                                         # the miscued clearance loops up
        p=(f-50)/28; ball=(lerp(146,164,p),lerp(GROUND-4,24,p)-30*math.sin(p*math.pi))
    if 50<=f<80: dx,dpose=ez(118,158,(f-50)/18),'dash'
    if 70<=f<80:
        p=(f-70)/10; dy=GROUND-18*math.sin(min(1,p)*math.pi/2); dpose='armsup'
        ky=GROUND-14*math.sin(min(1,p)*math.pi/2); kpose='attack'
    if 80<=f<126: s['image']=closeup_hand((f-80)/46,f); return s
    if 126<=f<140: ball=(180,40); s['fx'].append(('arg_net',182,40,f-126))
    if 126<=f<150: dx,dflip,dpose=ez(158,110,(f-126)/24),True,'armsup'
    if 128<=f<200: others.append(actor(PLAYER['attack'],96,pal=KIT_REF))                  # the referee: goal, centre spot
    if 150<=f<200:
        dx,dpose=110,'armsup' if (f//8)%2 else guard_pose(f)
        s['fx'].append(('a86_big',"LA MANO",8,(250,250,250))); s['fx'].append(('a86_big',"DE DIOS",24,CELESTE))   # 2.5 s
        if (f//6)%3==0: s['fx'].append(('twinkle',dx+8,dy-16,1))
    if 200<=f<236: dx,dflip,dpose=ez(110,40,(f-200)/36),True,guard_pose(f)
    if f>=236: dx,dflip=40,False
    if 14<=f<200: others.append(actor(PLAYER[kpose],kx,ky,flip=True,pal=KIT_KEEP))
    if ball: s['fx'].append(('arg_ball',)+ball)
    s['actors']=others+[actor(DIEGO[dpose],dx,dy,flip=dflip,pal=DPAL)]
    return s

# ---------------------------------------------------------------- clip 2: el gol del siglo
DEFENDERS=(70,92,114,134)
def beaten_at(i): return 40+int((DEFENDERS[i]-8-40)/110*144)+26    # when Diego reaches each one

def clip_siglo(f):
    s=scene(f,THEME)
    dx,dy,dpose,dflip=40,GROUND,guard_pose(f),False
    ball=(49,GROUND-2) if f<14 or f>=318 else None
    others=[]
    if 14<=f<26:                                                        # he receives it and spins away
        ball=(lerp(4,40,(f-14)/8),GROUND-2) if f<22 else (dx+9,GROUND-2); dflip=(f//3)%2==1
    if 26<=f<170:
        dx,dpose=lerp(40,150,(f-26)/144),'dash'; ball=(dx+9+math.sin(f*0.8),GROUND-2)
        s['under'].append(('a86_trail',dx,GROUND))
    for i,x in enumerate(DEFENDERS):                                    # four Englishmen, one by one
        t0=beaten_at(i)
        if f<t0-6: others.append(actor(PLAYER['idle'],x,flip=True,pal=KIT_ENG))
        elif f<t0: others.append(actor(PLAYER['attack'],x,flip=True,pal=KIT_ENG))            # the lunge
        elif f<280: others.append(actor(DIVE,x+4,flip=True,pal=KIT_ENG))                      # left on the grass
        else: others.append(actor(DIVE,x+4,flip=True,pal=KIT_ENG,alpha=max(0,1-(f-280)/20)))
    kpose=DIVE if 178<=f<280 else PLAYER['idle']                        # Shilton, sat down by the feint
    if f<300: others.append(actor(kpose,166 if f<178 else 160,flip=True,pal=KIT_KEEP,alpha=1 if f<280 else max(0,1-(f-280)/20)))
    if 170<=f<186: dx,dpose,dflip=150+(3 if (f//4)%2 else -3),'guard',(f//4)%2==1; ball=(dx+9,GROUND-2)   # the feint
    if 186<=f<196:
        dx,dpose=ez(150,160,(f-186)/10),'dash'; ball=(lerp(168,180,(f-186)/10),GROUND-2)
    if 194<=f<206: ball=(180,GROUND-3); s['fx'].append(('arg_net',182,GROUND-4,f-194))
    if 196<=f<280: s['image']=closeup_joy((f-196)/84,f); return s
    if 280<=f<318:
        s['fx'].append(('arg_confetti',f-280,1-(f-280)/38))
        dx,dflip,dpose=ez(160,40,(f-280)/38),True,guard_pose(f)
    if f>=318: dx,dflip=40,False
    if ball: s['fx'].append(('arg_ball',)+ball)
    s['actors']=others+[actor(DIEGO[dpose],dx,dy,flip=dflip,pal=DPAL)]
    return s

CLIPS = [clip('mano', N_MANO, clip_mano), clip('siglo', N_SIGLO, clip_siglo)]
