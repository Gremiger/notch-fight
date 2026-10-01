"""The Bear: Claude as Carmy (white tee, the blue apron, a towel on the shoulder) at the pass, in the kitchen
with EVERY SECOND COUNTS taped to the wall over the line. The printer starts spitting tickets (ORDERS IN!);
the brigade (Sydney, Marcus, Tina, Richie) answers YES CHEF!; a pan goes up in flames, BEHIND!, a plate
smashes, the clock on the wall racing. Close-up: the sign, its letters jumping with every second. Carmy
plates the last one with his tweezers (HANDS!), the printer stops, the kitchen goes quiet — YES CHEF."""
from engine import *
from themes.arg import PLAYER                                       # the generic people, in kitchen whites

THEME = 'thebear'
N_ = 384                                                            # a multiple of 12: the guard pose loops
CX = 30                                                             # Carmy at the pass
STEEL, STEEL_D = (186,190,196), (130,134,142)
# Carmy: dark curls, the white tee, the blue apron
CPAL = {'1':(40,30,26),'2':(242,242,242),'3':(44,74,130),'4':(200,200,206)}
CURLS = ["..1.1.1.1...",".11111111...","1111111111.."]
BRIGADE = [('Sydney',72,{'j':(244,244,244),'J':(244,244,244),'s':(150,100,70),'h':(36,26,22),'p':(40,40,46),'k':(30,30,34)}),
           ('Marcus',106,{'j':(244,244,244),'J':(244,244,244),'s':(120,80,56),'h':(24,24,28),'p':(60,60,70),'k':(30,30,34)}),
           ('Tina',140,{'j':(244,244,244),'J':(244,244,244),'s':(200,150,110),'h':(30,24,22),'p':(40,40,46),'k':(30,30,34)}),
           ('Richie',168,{'j':(30,40,70),'J':(30,40,70),'s':(230,190,160),'h':(60,44,34),'p':(30,30,36),'k':(20,20,24)})]

def _carmy(spr):
    g=[list(r) for r in overlay(spr,CURLS,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y>=top+5: g[y][x]='3' if y>=top+6 and l+2<=x<=r-1 else '2'   # tee, apron over it
            elif c=='o' and top+5<=y<top+8 and x<l: g[y][x]='4'                       # the towel on the arm
    return S([''.join(x) for x in g])
CARMY=variant(_carmy)

# ---- background: the kitchen -------------------------------------------------------------------------
def _kitchen(d):
    d.rectangle([0,0,W,H],fill=(230,230,224))                       # subway tiles
    for y in range(0,44,4):
        d.line([0,y,W,y],fill=(206,206,200))
        for x in range((y//4)%2*4,W,8): d.line([x,y,x,y+3],fill=(206,206,200))
    d.polygon([(118,0),(178,0),(172,16),(124,16)],fill=STEEL_D); d.rectangle([124,16,172,18],fill=STEEL)   # the hood
    d.rectangle([4,22,56,24],fill=STEEL_D)                            # the ticket rail over the pass
    for x0 in (8,30): d.rectangle([x0,26,x0+16,28],fill=(80,80,86)); d.rectangle([x0+2,28,x0+14,29],fill=(255,170,80))   # heat lamps
    d.rectangle([0,38,58,42],fill=STEEL); d.line([0,38,58,38],fill=(230,232,236))       # the pass
    d.rectangle([60,40,W,46],fill=STEEL_D); d.line([60,40,W,40],fill=STEEL)            # the line
    for bx in (128,146,164): d.ellipse([bx-5,38,bx+5,42],fill=(40,40,44)); d.ellipse([bx-3,39,bx+3,41],fill=(70,70,80))   # burners
    for x,y in ((70,30),(84,28),(98,30)): d.ellipse([x-5,y-3,x+5,y+3],fill=(110,110,118))   # pans on the shelf
    d.line([64,34,104,34],fill=STEEL_D)
    d.rectangle([0,46,W,H],fill=(150,140,130))                        # the floor
    for x in range(0,W,10): d.line([x,46,x,H],fill=(136,126,118))
register_bg(THEME, lambda v: (v+100,v+96,v+90), decor=_kitchen)

@fx('tb_sign')
def _fx_sign(d,im,e,f):
    """EVERY SECOND COUNTS, printed out and taped up on the wall (jolt: it shakes with the second)."""
    _,jolt=e; x0,y0=64,3; jx=jolt
    d.rectangle([x0+jx,y0,x0+56+jx,y0+16],fill=(250,250,248),outline=(200,200,196))
    for tx,ty in ((x0+1,y0-1),(x0+52,y0-1)): d.rectangle([tx+jx,ty,tx+3+jx,ty+1],fill=(220,210,170))   # tape
    text(d,"EVERY",x0+8+jx,y0+2,(20,20,20),shadow=None); text(d,"SECOND",x0+30+jx,y0+2,(20,20,20),shadow=None)
    text(d,"COUNTS",x0+16+jx,y0+9,(200,30,30),shadow=None)

@fx('tb_tickets')
def _fx_tickets(d,im,e,f):
    """Tickets hanging off the rail (n of them), and the printer spitting one out (printing)."""
    _,n,printing=e
    for i in range(n):
        x=6+i*5; d.rectangle([x,24,x+4,31],fill=(250,250,244),outline=(200,200,190))
        for k in range(3): d.line([x+1,26+k*2,x+3,26+k*2],fill=(120,120,120))
    d.rectangle([44,31,54,37],fill=(50,50,56))                         # the printer
    if printing:
        L=2+(f%6); d.rectangle([47,31-L,51,31],fill=(250,250,244)); d.point((52,33),fill=(90,220,110))

@fx('tb_clock')
def _fx_clock(d,im,e,f):
    """The clock on the wall, racing through the service (secs)."""
    _,secs=e; m,s_=divmod(int(secs),60)
    d.rectangle([150,22,180,30],fill=(20,20,24),outline=(90,90,100))
    text(d,f"{m:02d}:{s_:02d}".replace(':',':'),152,24,(255,70,60),shadow=None)

@fx('tb_bubble')
def _fx_bubble(d,im,e,f):
    _,txt,cx,y=e; w=len(txt)*4+5; x=max(1,min(W-w-2,int(cx-w/2))); tx=max(x+3,min(x+w-3,cx))
    d.rectangle([x,y,x+w,y+9],fill=(250,250,250),outline=(30,30,30)); d.polygon([(tx-2,y+9),(tx+2,y+9),(tx+1,y+13)],fill=(250,250,250))
    text(d,txt,x+3,y+2,(30,30,30),shadow=None)

@fx('tb_plate')
def _fx_plate(d,im,e,f):
    """A plate: whole (on the pass, with its food) or smashed (pieces on the floor)."""
    _,x,y,state=e; x,y=int(x),int(y)
    if state=='whole':
        d.ellipse([x-6,y-2,x+6,y+1],fill=(250,250,250),outline=(190,190,190))
        d.ellipse([x-2,y-3,x+2,y-1],fill=(150,80,50)); d.point((x+1,y-4),fill=(80,170,70)); d.point((x-2,y-2),fill=(240,200,80))
    else:
        rr=random.Random(4)
        for _ in range(7): px=x+rr.randint(-9,9); d.line([px,y,px+rr.randint(1,3),y-rr.randint(0,1)],fill=(240,240,240))

@fx('tb_tweezers')
def _fx_tweezers(d,im,e,f):
    _,x,y=e; d.line([x,y,x+5,y-6],fill=(200,200,210)); d.line([x+1,y,x+6,y-5],fill=(160,160,170))

# ---- close-up -----------------------------------------------------------------------------------------
def closeup_sign(t,f):
    """Primer plano: EVERY SECOND COUNTS, pushed in on; every second the letters jump and the room flashes."""
    tick=(f%20)<3
    im=Image.new('RGB',(W,H),(230,230,224)); d=ImageDraw.Draw(im)
    for y in range(0,H,8):
        d.line([0,y,W,y],fill=(206,206,200))
        for x in range((y//8)%2*8,W,16): d.line([x,y,x,y+7],fill=(206,206,200))
    k=1+0.15*ease(t)
    pw,ph=int(150*k),int(54*k); px,py=(W-pw)//2,(H-ph)//2
    jx=random.Random(f).randint(-2,2) if tick else 0
    d.rectangle([px+jx,py,px+pw+jx,py+ph],fill=(250,250,248),outline=(190,190,186))
    d.rectangle([px+2+jx,py-2,px+12+jx,py+3],fill=(220,210,170)); d.rectangle([px+pw-12+jx,py-2,px+pw-2+jx,py+3],fill=(220,210,170))
    big_text(im,"EVERY SECOND",py+6,(20,20,20),scale=2,cx=W//2+jx,shadow=None)
    big_text(im,"COUNTS",py+24,(200,30,30),scale=3,cx=W//2+jx,shadow=None)
    if tick: im=fade_to(im,(255,60,40),0.18); d=ImageDraw.Draw(im)
    if t<0.05: zoom_lines(d,(200,30,30))
    return im

# ---- the clip -----------------------------------------------------------------------------------------
def clip_service(f):
    s=scene(f,THEME)
    pose=guard_pose(f); jolt=0
    rush=16<=f<236
    n=0 if not rush else min(9,(f-16)//8+1)
    if 200<=f<236: n=max(0,9-(f-200)//4)                               # the last ones coming down
    secs=0 if f<16 else (min(f,236)-16)*0.6                            # the clock races through the night
    if rush and (f%20)<2: jolt=1
    s['under'].append(('tb_sign',jolt))
    s['under'].append(('tb_tickets',n,16<=f<120))
    if 16<=f<272: s['under'].append(('tb_clock',secs))                  # on for the service only
    bposes=['idle']*4
    if 18<=f<50: s['fx'].append(('tb_bubble',"ORDERS IN!",CX+4,12))
    if 50<=f<88:
        for i,(name,x,_) in enumerate(BRIGADE[:3]):
            if (f//10+i)%2==0: s['fx'].append(('tb_bubble',"YES CHEF!",x,18+(i%2)*2))
    if rush: bposes=['attack' if (f//6+i)%2 else 'idle' for i in range(4)]
    # the pan goes up; BEHIND!; a plate on the floor
    if 86<=f<124: s['fx'].append(('fire',146,38,3+(f%3))); s['fx'].append(('smoke',146,24-(f-86)//6,3,(160,160,166)))
    if 90<=f<124: s['fx'].append(('tb_bubble',"BEHIND!",BRIGADE[3][1],14))
    rx=BRIGADE[3][1] if not 90<=f<124 else lerp(168,96,(f-90)/34)
    if 116<=f<128: s['fx'].append(('tb_plate',rx-8,GROUND-1,'smashed')); s['shake']=rshake(1) if f<120 else (0,0)
    if 116<=f<124: s['fx'].append(('dmg',"CRASH",rx-16,GROUND-12,(200,40,40)))
    # close-up: the sign
    if 128<=f<188: s['image']=closeup_sign((f-128)/60,f); return s
    # the last plate: tweezers, HANDS!
    if 188<=f<236:
        pose='punch' if (f//4)%2 and f<212 else pose
        s['fx'].append(('tb_plate',CX+14,38,'whole'))
        if f<212: s['fx'].append(('tb_tweezers',CX+16,34))
        if 202<=f<236: s['fx'].append(('tb_bubble',"HANDS!",CX+10,18))
    # silence; YES CHEF.
    if 240<=f<272: s['fx'].append(('tb_bubble',"...",CX+4,20))
    if 276<=f<310: s['fx'].append(('tb_bubble',"YES CHEF.",BRIGADE[0][1],18))
    acts=[]
    for i,(name,x,pal) in enumerate(BRIGADE):
        bx=rx if name=='Richie' else x
        acts.append(actor(PLAYER[bposes[i]],bx,flip=name=='Richie' and 90<=f<124,pal=pal))
    acts.append(actor(CARMY[pose],CX,pal=CPAL))
    s['actors']=acts
    return s

CLIPS = [clip('service', N_, clip_service)]
