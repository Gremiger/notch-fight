"""Haikyuu!!: Claude as Hinata (the orange hair sticking up, Karasuno's black number 10) in the tournament gym:
the wooden court, the net, the stands with the black FLY banner, the scoreboard at 20-19. Shiratorizawa
serves; Kageyama gets under it; Hinata runs and jumps with his eyes shut, the freak quick. Close-up: up there,
over the block, THE VIEW FROM THE TOP (the whole other court below). The spike goes over Ushijima's hands
and slams into the floor; black crow feathers come down, the score turns to 21-19, OI, I'M HERE!"""
from engine import *
from themes.arg import PLAYER                                       # the generic players, in the two kits

THEME = 'haikyuu'
N_ = 264                                                            # a multiple of 12: the guard pose loops
CX, KX, NX, UX = 30, 70, 100, 116                                   # Hinata, Kageyama, the net, Ushijima
NET_TOP = GROUND-26
ORANGE, BLACK, WHITE = (250,140,30), (24,24,28), (244,244,244)
FLOOR, FLOOR_D = (214,160,96), (196,142,80)
PURPLE = (120,70,170)

# Hinata: the orange hair sticking up, the black jersey with the white 10, black shorts
CPAL = {'1':ORANGE,'2':BLACK,'3':WHITE}
HAIR = ["1..1.1..1.1.",".1.111.111..","111111111111"]
def _hinata(spr):
    g=[list(r) for r in overlay(spr,HAIR,-2,0)]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(top+4,min(top+9,h)):
        for x in range(l,r+1):
            if g[y][x]=='O': g[y][x]='2'
    for y in range(top+4,min(top+8,h)):                                      # the 10
        if g[y][l+2]=='2': g[y][l+2]='3'
        for x in (l+4,l+6):
            if g[y][x]=='2': g[y][x]='3'
        if y in (top+4,top+7) and g[y][l+5]=='2': g[y][l+5]='3'
    return S([''.join(x) for x in g])
HINATA=variant(_hinata)
_eye=next(i for i,r in enumerate(HINATA['dash']) if 'K' in r)
SHUT=S([r.replace('K','O') if i==_eye else r for i,r in enumerate(HINATA['dash'])])   # the jump: eyes shut

KIT_KARASUNO = {'j':BLACK,'J':BLACK,'s':(236,196,160),'h':(20,20,24),'p':BLACK,'k':(240,240,240)}
KIT_SHIRA = {'j':(236,236,240),'J':PURPLE,'s':(214,170,130),'h':(60,44,30),'p':PURPLE,'k':(240,240,240)}
KIT_TENDOU = dict(KIT_SHIRA, h=(210,40,40))
BLOCK=S([                                                           # up at the net, both hands high
".s........s.",".s..hhhh..s.",".s.hhhhhh.s.",".s.ssssss.s.",".s.sKssKs.s.",".s.ssssss.s.",
".sj.ssss.js.","..jJjJjJjJ..","..jJjJjJjJ..","..jJjJjJjJ..","..jJjJjJjJ..","...pppppp...",
"...pppppp...","...ss..ss...","...ss..ss...","...kk..kk...",])
SETTER=S([                                                          # Kageyama under the ball, fingers up
"....s..s....","...s....s...","...hhhhhh...","..hhhhhhhh..","..hssssssh..","...sKssKs...",
"...ssssss...","..sjjjjjjs..","..jjjjjjjj..","..jjjjjjjj..","..jjjjjjjj..","...pppppp...",
"...pppppp...","...ss..ss...","..ss....ss..","..kk....kk..",])

# ---- the gym ------------------------------------------------------------------------------------------
def _gym(d):
    d.rectangle([0,0,W,H],fill=(206,200,184))                       # the wall
    d.rectangle([0,0,W,14],fill=(70,62,58))                          # the stands, full
    rr=random.Random(10)
    for x in range(2,W,4):
        for y in (3,8):
            d.point((x+rr.randint(-1,1),y),fill=rr.choice([(230,200,170),(60,40,30),(200,60,60),(240,240,240),(30,30,30),(140,90,190)]))
            d.point((x,y+2),fill=rr.choice([(20,20,24),(240,240,240),(140,90,190),(200,200,200)]))
    d.rectangle([0,14,W,15],fill=(150,150,156))                       # the railing
    d.rectangle([10,15,40,24],fill=BLACK); text(d,"FLY",19,17,WHITE,shadow=None)   # Karasuno's banner
    d.rectangle([150,15,180,24],fill=PURPLE); text(d,"SRZ",158,17,WHITE,shadow=None)
    d.rectangle([0,GROUND-12,W,H],fill=FLOOR)                        # the court
    for y in (GROUND-9,GROUND-5): d.line([0,y,W,y],fill=FLOOR_D)
    d.line([0,GROUND+1,W,GROUND+1],fill=WHITE); d.line([NX,GROUND-12,NX,GROUND+1],fill=WHITE)
    d.line([NX-34,GROUND-12,NX-38,GROUND+1],fill=WHITE); d.line([NX+34,GROUND-12,NX+38,GROUND+1],fill=WHITE)   # attack lines
    d.rectangle([NX-1,NET_TOP-2,NX+1,GROUND],fill=(60,60,70))         # the post
register_bg(THEME, lambda v: (v+120,v+90,v+50), decor=_gym)

@fx('hq_net')
def _fx_net(d,im,e,f):
    """The net, in front of the players at the net."""
    d.rectangle([NX-2,NET_TOP,NX+2,NET_TOP+1],fill=WHITE)
    for y in range(NET_TOP+3,NET_TOP+15,3): d.line([NX-1,y,NX+1,y],fill=(40,40,46))
    d.line([NX,NET_TOP,NX,NET_TOP+15],fill=(40,40,46)); d.line([NX-2,NET_TOP+15,NX+2,NET_TOP+15],fill=WHITE)

@fx('hq_score')
def _fx_score(d,im,e,f):
    _,us,them,glow=e
    d.rectangle([76,1,108,11],fill=(16,16,20),outline=(90,90,96))
    if us is None: return                                            # dark between rallies
    c=tuple(int(lerp(v,255,glow)) for v in (255,170,60))
    text(d,f"{us:02d}",79,4,c,shadow=None); text(d,"-",91,4,(200,200,200),shadow=None); text(d,f"{them:02d}",97,4,(255,170,60),shadow=None)

def draw_ball(d,x,y,r=2):
    x,y=int(x),int(y)
    d.ellipse([x-r,y-r,x+r,y+r],fill=(250,214,40),outline=(30,60,150)); d.line([x-r+1,y,x+r-1,y],fill=(30,60,150))

@fx('hq_ball')
def _fx_ball(d,im,e,f):
    _,x,y,trail=e
    for k in range(1,int(trail)+1): d.line([x-k*5,y-k*2,x-k*5+3,y-k*2+1],fill=(255,240,180))
    draw_ball(d,x,y)

@fx('hq_feather')
def _fx_feather(d,im,e,f):
    """A black crow feather, rocking as it falls."""
    _,x,y,a=e; dx,dy=math.cos(a)*4,math.sin(a)*2
    d.polygon([(x-dx,y-dy),(x+dy*0.6,y-dx*0.3-1),(x+dx,y+dy),(x-dy*0.6,y+dx*0.3+1)],fill=(18,18,26))
    d.line([x-dx,y-dy,x+dx,y+dy],fill=(60,64,90))

@fx('hq_bubble')
def _fx_bubble(d,im,e,f):
    _,txt,cx,y=e; w=len(txt)*4+5; x=max(1,min(W-w-2,int(cx-w/2))); tx=max(x+3,min(x+w-3,int(cx)))
    d.rectangle([x,y,x+w,y+9],fill=(250,250,250),outline=(30,30,30)); d.polygon([(tx-2,y+9),(tx+2,y+9),(tx+1,y+13)],fill=(250,250,250))
    text(d,txt,x+3,y+2,(30,30,30),shadow=None)

# ---- close-up -----------------------------------------------------------------------------------------
def closeup_top(t,f):
    """Primer plano: from up there, over the block — the whole other court below. THE VIEW FROM THE TOP."""
    im=Image.new('RGB',(W,H),(70,62,58)); d=ImageDraw.Draw(im)
    rr=random.Random(3)
    for x in range(0,W,3):
        for y in range(2,18,4): d.point((x+rr.randint(0,1),y),fill=rr.choice([(230,200,170),(140,90,190),(240,240,240),(40,30,30)]))
    d.rectangle([0,18,W,20],fill=(150,150,156))
    d.polygon([(30,22),(155,22),(W+30,H),(-30,H)],fill=FLOOR)       # their court, from above
    for k in range(1,5): y=22+k*9; d.line([0,y,W,y],fill=FLOOR_D)
    d.line([30,22,155,22],fill=WHITE); d.line([30,22,-30,H],fill=WHITE); d.line([155,22,W+30,H],fill=WHITE)
    d.line([12,40,173,40],fill=WHITE)                                # the attack line
    for i,x in enumerate((40,80,120,150)):                            # the players down there, small
        y=30+(i%2)*6; d.rectangle([x,y,x+3,y+5],fill=(236,236,240)); d.rectangle([x,y-2,x+3,y-1],fill=(60,44,30))
    d.rectangle([0,H-8,W,H-6],fill=WHITE)                            # the top of the net, under him
    for x in range(0,W,4): d.line([x,H-5,x,H],fill=(40,40,46))
    lift=int(6*(1-t))
    for hx in (60,76,110,126):                                       # the block's hands, reaching but short
        d.rectangle([hx,H-12+lift,hx+7,H],fill=(214,170,130),outline=(120,80,60))
        d.rectangle([hx,min(H,H-4+lift),hx+7,H],fill=PURPLE)
    draw_ball(d,172,30,4)
    if t>=0.1: big_text(im,"THE VIEW FROM THE TOP",4,(255,255,255),scale=2,shadow=BLACK)
    if t<0.05: zoom_lines(d,(255,255,255))
    return im

# ---- the clip -----------------------------------------------------------------------------------------
def arc(p0,p1,peak,t):
    t=max(0,min(1,t)); x=lerp(p0[0],p1[0],t); y=lerp(p0[1],p1[1],t)-4*peak*t*(1-t); return x,y

def clip_quick(f):
    s=scene(f,THEME)
    pose=guard_pose(f); spr=None; hx,hy=CX,GROUND
    k_spr=PLAYER['idle']; u_spr,uy=PLAYER['idle'],GROUND
    score=(20,19,0.0) if 14<=f<236 else (None,None,0.0)
    ball=None
    # the serve comes over, Kageyama gets under it
    if 14<=f<44: ball=(*arc((W+4,22),(KX,GROUND-19),24,(f-14)/30),0)
    if 34<=f<56: k_spr=SETTER
    if 44<=f<52: ball=(*arc((KX,GROUND-19),(NX-6,NET_TOP-12),2,(f-44)/8),0)
    # Hinata: the run, the jump, eyes shut
    if 24<=f<40: hx=lerp(CX,64,(f-24)/16); spr=HINATA['dash']
    if 40<=f<52: t=(f-40)/12; hx=lerp(64,NX-12,t); hy=GROUND-26*math.sin(t*math.pi/2); spr=SHUT
    if 52<=f<126: hx,hy=NX-12,GROUND-26; spr=SHUT if f<118 else HINATA['punch']
    if 52<=f<118: ball=(NX-6,NET_TOP-12,0)
    # Ushijima goes up for the block
    if 42<=f<52: u_spr=BLOCK; uy=GROUND-14*math.sin((f-42)/10*math.pi/2)
    if 52<=f<126: u_spr,uy=BLOCK,GROUND-14
    if 126<=f<140: u_spr=BLOCK; uy=GROUND-14*(1-(f-126)/14)
    if 56<=f<118: s['image']=closeup_top((f-56)/62,f); return s
    # the spike: over the hands, into the floor
    if 118<=f<121: t=(f-118)/3; ball=(lerp(NX-6,126,t),lerp(NET_TOP-12,NET_TOP-10,t),3)       # just over the hands...
    if 121<=f<126: t=(f-121)/5; ball=(lerp(126,148,t),lerp(NET_TOP-10,GROUND-2,t),3)          # ...and down
    if 126<=f<150:
        t=(f-126)/24; ball=(*arc((148,GROUND-2),(W+8,8),10,t),0)
        if f<134: s['shake']=rshake(1)
    if 126<=f<146: s['fx'].append(('dmg',"DON!",134,GROUND-20,(255,240,120)))
    if 126<=f<132:
        for k in range(6): s['fx'].append(('dust',148+k*3-8,GROUND-1-k%3))
    # down again, and the gym goes up: feathers, 21-19
    if 126<=f<148: t=(f-126)/22; hx=NX-12; hy=GROUND-26*(1-t)**2; spr=HINATA['dash' if f<140 else 'guard']
    if 148<=f<200: hx=NX-12
    if 200<=f<244: hx=lerp(NX-12,CX,ease((f-200)/44))
    if 130<=f<236: score=(21,19,max(0.0,1-(f-130)/20) if f<150 else 0.0)
    if 130<=f<230:
        rr=random.Random(7)
        for i in range(22):
            x0=rr.uniform(0,W); start=130+rr.uniform(0,40); v=rr.uniform(0.35,0.7)
            y=-6+(f-start)*v
            if f>=start and y<GROUND+2: s['fx'].append(('hq_feather',x0+4*math.sin((f+i*7)/9),y,math.sin((f+i*5)/7)*0.8))
    if 150<=f<194: s['fx'].append(('hq_bubble',"OI, I'M HERE!",hx+4,26))
    s['under'].append(('hq_score',*score))
    if ball: s['fx'].append(('hq_ball',*ball))
    s['actors']=[actor(k_spr,KX,pal=KIT_KARASUNO),
                 actor(PLAYER['idle'],160,flip=True,pal=KIT_TENDOU),
                 actor(u_spr,UX,y=uy,flip=True,pal=KIT_SHIRA),
                 actor(spr or HINATA[pose],hx,y=hy,pal=CPAL)]
    s['fx'].insert(0,('hq_net',))
    return s

CLIPS = [clip('quick', N_, clip_quick)]
