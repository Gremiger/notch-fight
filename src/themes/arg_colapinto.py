"""Argentina sub-theme "arg-colapinto": Claude as Franco Colapinto, number 43, in the dark-blue Williams.
On the grid; he climbs in, the five red lights come on one by one and go out (AND AWAY WE GO!). The
camera rides with him down the straight, the stands a sea of celeste and white; he passes four cars, the
TV tower ticking COL up from P12 to P8. Team radio: GOOD JOB FRANCO. P8. POINTS. The chequered flag.
Close-up: his helmet, the visor full of the stands' flags — VAMOS FRANCO. A lap of honour under the
flags, and back to the grid. Everything that scrolls repeats every 192 px, so the lap closes the loop."""
from engine import *
from themes.arg import CELESTE, WHITE                               # same country

THEME = 'arg-colapinto'
N_ = 384                                                            # a multiple of 12: the guard pose loops too
CX, CAR_X = 30, 74                                                  # Claude on the grid; his car
PERIOD = 192                                                        # every scrolling pattern repeats here
LAP = PERIOD*6                                                      # how far the camera travels in the clip
NAVY, CYAN = (18,30,74), (40,170,230)                               # the Williams
RIVALS = [((200,30,40),(240,240,240)),((240,130,30),(40,40,50)),((180,184,196),(30,190,170)),((30,110,70),(230,200,60))]
OVERTAKES = (78,98,118,138)                                         # P12 -> P11 -> P10 -> P9 -> P8
HUD_BG, HUD_INK, GOLD = (16,16,22), (236,236,236), (246,190,50)
# Claude in the team kit: the helmet over his head, the race suit navy and cyan
FPAL = {'1':(60,150,220),'2':(240,240,240),'3':NAVY,'4':CYAN}
HELMET = ["..11111111..",".1112222111.","11111111111."]

def _franco(spr):
    g=[list(r) for r in overlay(spr,HELMET,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y>=top+5: g[y][x]='4' if y==top+6 else '3'
            elif c=='o' and y>=top+5: g[y][x]='3'
    return S([''.join(x) for x in g])
FRANCO=variant(_franco)

def cam_at(f):
    """How far the camera has rolled: still on the grid, a whole number of PERIODs by the end."""
    if f<58: return 0.0
    if f>=346: return float(LAP)
    return LAP*ease((f-58)/288)

# ---- background: the sky; the rest scrolls ------------------------------------------------------------
def _sky(d):
    for y in range(14):
        k=y/13; d.line([0,y,W,y],fill=(int(120+60*k),int(170+40*k),int(220+20*k)))
register_bg(THEME, lambda v: (v+60,v+60,v+64), decor=_sky)

@fx('fc_track')
def _fx_track(d,im,e,f):
    """The stands (half speed), the advertising boards, the asphalt, the kerbs and the grid boxes."""
    _,cam=e
    s=cam*0.5
    d.rectangle([0,14,W,34],fill=(40,40,52))                          # the stands: rows of fans...
    for row,y in enumerate(range(16,34,4)):
        for x in range(-2,W+2,3):
            wx=int(x+s+row*2)%PERIOD; rr=random.Random(wx*7+row)
            d.point((x,y),fill=rr.choice(((226,184,150),(196,140,104),(150,104,78))))
            d.point((x,y+1),fill=rr.choice((CELESTE,WHITE,CELESTE,(60,60,80),(230,190,60))))
    for k in range(-1,W//24+2):                                     # ...and their flags, big and waving
        wx=k*24-int(s)%24; ph=f*math.tau/48+k*1.7
        for j in range(9):
            dy=int(round(math.sin(ph-j*0.6)*1.2))
            for yy in range(7): d.point((wx+j,16+(k%2)*8+yy+dy),fill=WHITE if 2<=yy<=4 else CELESTE)
        d.point((wx+4,19+(k%2)*8+int(round(math.sin(ph-2.4)*1.2))),fill=GOLD)
    d.rectangle([0,34,W,38],fill=(30,30,40))                         # the boards
    for k in range(-1,W//48+2):
        bx=k*48-int(cam)%48
        d.rectangle([bx+2,35,bx+44,37],fill=(200,40,40) if k%2 else (40,90,200)); d.line([bx+8,36,bx+30,36],fill=(240,240,240))
    d.rectangle([0,38,W,40],fill=(70,140,60))                        # grass, asphalt
    d.rectangle([0,40,W,GROUND],fill=(76,76,84))
    for k in range(-1,W//16+2):                                     # dashes down the middle
        x=k*16-int(cam)%16; d.line([x,49,x+7,49],fill=(200,200,200))
    for k in range(-1,W//8+2):                                      # the kerb
        x=k*8-int(cam)%8; d.rectangle([x,GROUND,x+3,GROUND+2],fill=(220,40,40)); d.rectangle([x+4,GROUND,x+7,GROUND+2],fill=(240,240,240))
    d.rectangle([0,GROUND+3,W,H],fill=(70,140,60))
    gx=CAR_X-14-int(cam)%PERIOD                                       # the grid box (and the start line beyond)
    for gxx in (gx,gx+PERIOD):
        d.line([gxx,51,gxx,GROUND-1],fill=(240,240,240)); d.line([gxx,51,gxx+6,51],fill=(240,240,240))
        for j in range(0,18,2): d.point((gxx+34+(j//2)%2,40+j),fill=(240,240,240)); d.point((gxx+35-(j//2)%2,41+j),fill=(240,240,240))   # the line, chequered

def car(d,x,y,main,accent,helmet=None,f=0,speed=0.0):
    """A Formula 1 car side-on, facing right, its rear tyre at x-8; helmet: the driver's colour (or None)."""
    x,y=int(x),int(y)
    d.rectangle([x-14,y-11,x-12,y-5],fill=main); d.line([x-15,y-11,x-11,y-11],fill=accent)        # rear wing
    d.polygon([(x-13,y-3),(x-12,y-7),(x-4,y-8),(x-1,y-10),(x+2,y-8),(x+8,y-5),(x+15,y-3),(x+15,y-1),(x-13,y-1)],fill=main)
    d.line([x-11,y-4,x+13,y-3],fill=accent)                          # the stripe
    if helmet: d.ellipse([x-2,y-11,x+2,y-7],fill=helmet); d.line([x,y-9,x+2,y-9],fill=(30,30,40))
    d.arc([x-4,y-12,x+5,y-6],180,330,fill=(40,40,46))                # the halo
    d.line([x+11,y,x+16,y],fill=accent)                               # front wing
    for wx in (x-8,x+8):                                             # tyres, spokes turning
        d.ellipse([wx-3,y-4,wx+3,y+2],fill=(24,24,28)); a=f*speed
        d.point((wx+int(math.cos(a)*2),y-1+int(math.sin(a)*2)),fill=(150,150,160))
    if speed>0.5:
        for j in range(3): d.line([x-22-j*6,y-6+j*3,x-16-j*6,y-6+j*3],fill=(220,220,230))

@fx('fc_car')
def _fx_car(d,im,e,f):
    _,x,y,main,accent,helmet,speed=e; car(d,x,y,main,accent,helmet,f,speed)

@fx('fc_lights')
def _fx_lights(d,im,e,f):
    """The start gantry: five pairs of lights; n of them red."""
    _,n=e; x0=58
    d.rectangle([x0-2,2,x0+66,12],fill=(20,20,24))
    for i in range(5):
        cx=x0+6+i*13
        for cy in (5,9): d.ellipse([cx-2,cy-2,cx+2,cy+2],fill=(230,30,30) if i<n else (60,20,20))

@fx('fc_tower')
def _fx_tower(d,im,e,f):
    """The TV timing tower: COL's position, a green arrow when he has just gained one."""
    _,pos,gain=e
    d.rectangle([3,3,48,11],fill=HUD_BG,outline=(90,90,110))
    d.rectangle([4,4,17,10],fill=(230,230,236)); text(d,"P"+str(pos),5 if pos>9 else 7,5,(20,20,24),shadow=None)
    d.rectangle([19,4,20,10],fill=CYAN); text(d,"COL",23,5,HUD_INK,shadow=None)
    if gain: d.polygon([(41,9),(43,5),(45,9)],fill=(60,220,90))

@fx('fc_radio')
def _fx_radio(d,im,e,f):
    """Team radio, as on the broadcast: a dark box with the team colour and the message."""
    _,lines=e; w=max(len(l) for l in lines)*4+20; x=W-w-3; y=16
    d.rectangle([x,y,x+w,y+len(lines)*7+10],fill=(14,16,26),outline=CYAN)
    text(d,"RADIO",x+3,y+2,CYAN,shadow=None)
    for k in range(4): d.line([x+w-12+k*2,y+5-((f//2+k)%4),x+w-12+k*2,y+5],fill=CYAN)   # the voice bars
    for i,l in enumerate(lines): text(d,l,x+3,y+9+i*7,(240,240,240),shadow=None)

@fx('fc_flag')
def _fx_flag(d,im,e,f):
    """The chequered flag, waved at the line."""
    _,x=e; x=int(x); sw=int(3*math.sin(f*0.8))
    d.line([x,40,x+sw,24],fill=(200,200,200))
    for i in range(4):
        for j in range(3): d.rectangle([x+sw+1+i*2,24+j*2,x+sw+2+i*2,25+j*2],fill=(240,240,240) if (i+j)%2 else (20,20,20))

@fx('fc_confetti')
def _fx_confetti(d,im,e,f):
    _,k,dens=e; rr=random.Random(43)
    for i in range(int(60*dens)):
        x=(rr.uniform(0,W)+math.sin(k*0.1+i)*4)%W; y=(rr.uniform(-H,0)+k*rr.uniform(0.8,1.6))%(H+10)-5
        d.rectangle([x,y,x+1,y],fill=CELESTE if i%2 else WHITE)

# ---- close-up -----------------------------------------------------------------------------------------
def closeup_helmet(t,f):
    """Primer plano: Franco's helmet, the visor full of celeste-and-white flags going by — VAMOS FRANCO."""
    im=Image.new('RGB',(W,H),(10,14,30)); d=ImageDraw.Draw(im)
    for i in range(14):                                              # speed lines behind
        y=(i*9+f*3)%H; d.line([0,y,60,y],fill=(30,40,70))
    hx,hy=58,34
    d.ellipse([hx-38,hy-34,hx+38,hy+40],fill=(60,150,220),outline=(20,40,80),width=2)    # the helmet shell
    d.chord([hx-38,hy-34,hx+38,hy+40],200,340,fill=(240,240,240))
    d.rectangle([hx-38,hy+18,hx+38,hy+24],fill=NAVY)
    text(d,"43",hx-4,hy+26,(240,240,240))
    vx0,vx1,vy0,vy1=hx-28,hx+30,hy-10,hy+10                          # the visor and what it reflects
    d.rounded_rectangle([vx0,vy0,vx1,vy1],radius=6,fill=(20,24,36),outline=(10,10,16),width=2)
    for x in range(vx0+3,vx1-2):
        wx=(x*3+f*4)//6
        for y in range(vy0+3,vy1-2):
            band=((y-vy0)//4+wx)%5
            if band in (0,1): d.point((x,y),fill=(70,110,150) if band==0 else (110,140,170))
            elif band==3: d.point((x,y),fill=(150,160,176))
    d.line([vx0+4,vy0+3,vx1-10,vy0+3],fill=(220,230,240))            # the shine
    fx0,fy0=hx+16,hy+12                                              # the flag on its side
    d.rectangle([fx0,fy0,fx0+12,fy0+2],fill=CELESTE); d.rectangle([fx0,fy0+3,fx0+12,fy0+4],fill=WHITE); d.rectangle([fx0,fy0+5,fx0+12,fy0+7],fill=CELESTE)
    d.point((fx0+6,fy0+3),fill=GOLD)
    if t>=0.3:
        big_text(im,"VAMOS",12,(255,255,255),scale=2,cx=146,outline=NAVY)
        big_text(im,"FRANCO",30,CELESTE,scale=2,cx=146,outline=NAVY)
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,(255,255,255),0.6*(t-0.9)/0.1)
    return im

# ---- the clip -----------------------------------------------------------------------------------------
def clip_debut(f):
    s=scene(f,THEME)
    cam=cam_at(f); speed=(cam_at(f+1)-cam)
    s['under'].append(('fc_track',cam))
    cx,cpose,cflip,show=CX,guard_pose(f),False,True
    in_car=18<=f<348
    # 1) he climbs in; the lights
    if 14<=f<18: cx,cpose=ez(CX,CAR_X-2,(f-14)/4),'dash'
    if 348<=f<358: cx,cpose,cflip=ez(CAR_X-2,CX,(f-348)/10),guard_pose(f),True
    if in_car: show=False
    if 24<=f<62:
        n=min(5,(f-24)//6+1) if f<56 else 0
        s['fx'].append(('fc_lights',n))
    if 58<=f<102: s['fx'].append(('big',"AND AWAY WE GO!",18,(255,255,255)))
    # 2) four cars passed; the tower climbs
    pos=12-sum(1 for t0 in OVERTAKES if f>=t0+12)
    if 30<=f<210: s['fx'].append(('fc_tower',pos,any(t0+12<=f<t0+24 for t0 in OVERTAKES)))
    for i,t0 in enumerate(OVERTAKES):
        if t0-10<=f<t0+30:
            rx=lerp(W+20,-30,(f-t0+10)/40); main,acc=RIVALS[i]
            s['under'].append(('fc_car',rx,GROUND-9,main,acc,(200,200,60),speed))   # the far lane
    # 3) GOOD JOB FRANCO. P8. POINTS.; the flag
    if 160<=f<212: s['fx'].append(('fc_radio',["GOOD JOB FRANCO.","P8. POINTS."]))
    if 188<=f<212: s['under'].append(('fc_flag',lerp(W+4,CAR_X-30,(f-188)/24)))
    # 4) close-up: the helmet
    if 212<=f<272: s['image']=closeup_helmet((f-212)/60,f); return s
    # 5) the lap of honour under the flags
    if 272<=f<346: s['fx'].append(('fc_confetti',f-272,1.0 if f<330 else 1-(f-330)/16))
    s['fx'].append(('fc_car',CAR_X,GROUND,NAVY,CYAN,(60,150,220) if in_car else None,speed))
    if 286<=f<330 and (f//6)%2: s['fx'].append(('twinkle',CAR_X+1,GROUND-14,2))       # his hand out, waving
    if show: s['actors']=[actor(FRANCO[cpose],cx,flip=cflip,pal=FPAL)]
    return s

CLIPS = [clip('debut', N_, clip_debut)]
