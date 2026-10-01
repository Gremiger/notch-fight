"""Argentina sub-theme "arg-alejo": Alejo y Valentina (LocoArts), no fight. Claude as Carlitox (the messy
green hair, the pale face, navy tank top, dark trousers) on the brown couch next to Alejo (black hair,
purple t-shirt), Valentina (long black hair, pink) standing by, the old TV on its stand, the framed
CUADRITO on the pink wall. Two clips on that neutral pose:
  patas  - MIRA COMO REVOLEO LAS PATAS, and he does: his legs spin like a fan, faster and faster. Close-up:
           the grin and the blur — HOLA, VENGO A REVOLEAR LAS PATAS! Alejo and Valentina just look.
  flotar - a cut to the series' other set (orange wall, the brown curtain, green floor): Carlitox floats
           out from behind the curtain, arms out — HOLA, VENGO A FLOTAR — drifts across and back.
The series' look: thick black outlines, flat colours, nothing shaded."""
from engine import *
from themes.arg import PLAYER                                       # the generic people, dressed as the cast

THEME = 'arg-alejo'
N_ = 288                                                            # a multiple of 12
PINK, FLOOR = (246,196,200), (90,58,20)
COUCH, COUCH_D = (150,100,58), (110,72,40)
INK = (20,20,20)
CX, AX, VX, TVX = 112, 88, 58, 160                                  # Carlitox, Alejo, Valentina, the TV
SEAT = GROUND-6                                                     # where they sit on the couch
# Carlitox: green hair everywhere, a pale face, the navy tank top, bare arms, dark grey trousers
CPAL = {'1':(70,200,70),'2':(40,150,50),'3':(236,232,226),'4':(34,44,90),'5':(70,70,76)}
HAIR = ["1.1..1.1.1.1.","21111112111..","1111111111111"]
APAL = {'h':(20,20,24),'s':(236,226,214),'j':(130,60,180),'J':(130,60,180),'p':(40,40,46),'k':(30,30,34)}
VALENTINA = S([
"...hhhhhh...","..hhhhhhhh..","..hssssssh..","..hsKssKsh..","..hssssssh..","..hhssssh...","..hh.ss.hh..",
"..nnnnnnnn..",".snnnnnnnns.",".snnnnnnnns.","..nnnnnnnn..","...nnnnnn...","...nnnnnn...","...ss..ss...",
"...ss..ss...","...kk..kk...",])
VPAL = {'h':(20,20,24),'s':(240,220,206),'n':(240,120,170),'k':(60,40,40)}

def _carlitox(spr):
    g=[list(r) for r in overlay(spr,HAIR,-2,0,bangs="1.1.1.1.1.1")]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g)
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y<top+5: g[y][x]='3'                           # the pale face
            elif c=='O': g[y][x]='4'                                     # the tank top
            elif c=='o' and y<top+8: g[y][x]='3'                         # bare arms
            elif c=='o': g[y][x]='5'
    return S([''.join(x) for x in g])
CARLITOX=variant(_carlitox)
def seated(spr, cut=3): return S(spr[:len(spr)-cut])                    # the legs are drawn apart, sitting

# ---- the living room (the pixel-art reference) -----------------------------------------------------------
def _living(d):
    d.rectangle([0,0,W,H],fill=PINK)
    d.rectangle([0,GROUND+1,W,H],fill=FLOOR); d.line([0,GROUND+1,W,GROUND+1],fill=INK)
    d.rectangle([24,14,58,24],fill=(170,210,240),outline=INK)            # the CUADRITO
    d.line([41,10,30,14],fill=INK); d.line([41,10,52,14],fill=INK)
    text(d,"CUADRITO",26,17,INK,shadow=None)
    x=TVX                                                               # the TV on its stand
    d.rectangle([x-14,GROUND-12,x+14,GROUND],fill=(130,80,40),outline=INK); d.rectangle([x-12,GROUND-8,x+2,GROUND-3],fill=(80,50,24))
    d.rectangle([x-12,GROUND-30,x+12,GROUND-12],fill=(90,90,96),outline=INK); d.rectangle([x-9,GROUND-27,x+5,GROUND-15],fill=(60,64,70),outline=INK)
    text(d,"T.V",x-6,GROUND-24,(20,20,20),shadow=None)
    d.line([x,GROUND-30,x-5,GROUND-37],fill=INK); d.line([x,GROUND-30,x+6,GROUND-36],fill=INK)
register_bg(THEME, lambda v: (v+40,v+30,v+10), decor=_living)

@fx('av_couch_back')
def _fx_couch_back(d,im,e,f):
    d.rectangle([66,GROUND-20,130,GROUND-8],fill=COUCH,outline=INK)
    for x in (88,110): d.line([x,GROUND-19,x,GROUND-9],fill=COUCH_D)

@fx('av_couch_front')
def _fx_couch_front(d,im,e,f):
    """The seat and arms of the couch, over their laps."""
    d.rectangle([66,GROUND-9,130,GROUND-2],fill=COUCH,outline=INK)
    for ax in (62,128): d.rectangle([ax,GROUND-14,ax+6,GROUND-2],fill=COUCH_D,outline=INK)
    for lx in (68,128): d.line([lx,GROUND-2,lx,GROUND],fill=INK)

@fx('av_legs')
def _fx_legs(d,im,e,f):
    """Carlitox's legs from the edge of the seat: hanging (a=None), or spinning like a fan (angle a)."""
    _,x,y,a,blur=e; x,y=int(x),int(y)
    grey=CPAL['5']
    if a is None:
        for dx in (-3,2): d.line([x+dx,y,x+dx+2,y+7],fill=grey,width=3); d.line([x+dx+1,y+7,x+dx+4,y+7],fill=INK,width=2)
        return
    for k in range(int(blur)):                                       # motion arcs behind the spin
        d.arc([x-11,y-11,x+11,y+11],math.degrees(a)-60-k*25,math.degrees(a)-40-k*25,fill=(120,120,130))
    for s in (0,math.pi):
        ex,ey=x+math.cos(a+s)*10,y+math.sin(a+s)*10
        d.line([x,y,ex,ey],fill=grey,width=3); d.ellipse([ex-2,ey-2,ex+2,ey+2],fill=INK)
    d.ellipse([x-2,y-2,x+2,y+2],fill=grey)

@fx('av_bubble')
def _fx_bubble(d,im,e,f):
    _,lines,cx,y,tail=e; lines=[lines] if isinstance(lines,str) else lines
    w=max(len(l) for l in lines)*4+7; h=len(lines)*7+4; x=max(1,min(W-w-2,int(cx-w/2)))
    d.rectangle([x,y,x+w,y+h],fill=(255,255,255),outline=INK,width=1)
    tx=max(x+4,min(x+w-4,int(tail))); d.polygon([(tx-2,y+h),(tx+2,y+h),(int(tail),y+h+5)],fill=(255,255,255),outline=INK)
    d.line([tx-1,y+h,tx+1,y+h],fill=(255,255,255))
    for i,l in enumerate(lines): text(d,l,x+4,y+3+i*7,INK,shadow=None)

@fx('av_stage')
def _fx_stage(d,im,e,f):
    """The series' other set: an orange wall with the black band, the brown curtain, the green floor."""
    d.rectangle([0,0,W,H],fill=(244,160,30))
    d.rectangle([0,4,W,12],fill=(20,20,20)); d.line([0,14,W,14],fill=(200,200,200),width=2)
    d.rectangle([70,14,128,GROUND],fill=(140,62,20),outline=INK)
    for x in (80,92,99,112,120): d.line([x,18,x+(1 if x%2 else -1),GROUND-2],fill=INK)
    d.rectangle([0,GROUND,W,H],fill=(40,110,30)); d.line([0,GROUND,W,GROUND],fill=INK)

@fx('av_wipe')
def _fx_wipe(d,im,e,f):
    _,k=e; d.rectangle([0,0,int(W*k),H],fill=(0,0,0))

# ---- close-up -------------------------------------------------------------------------------------------
def closeup_patas(t,f):
    """Primer plano: Carlitox's grin, the legs a blur below — HOLA, VENGO A REVOLEAR LAS PATAS!"""
    im=Image.new('RGB',(W,H),PINK); d=ImageDraw.Draw(im)
    ox=14
    rr=random.Random(2)
    for k in range(22):                                              # the hair, everywhere
        a=rr.uniform(math.pi,2*math.pi); L=rr.randint(16,30)
        d.line([ox+28,24,ox+28+math.cos(a)*L*1.2,24+math.sin(a)*L],fill=CPAL['1'] if k%3 else CPAL['2'],width=4)
    d.ellipse([ox+6,6,ox+50,56],fill=CPAL['3'],outline=INK,width=2)    # the face
    for ex in (ox+18,ox+38):
        d.ellipse([ex-6,20,ex+6,34],fill=(255,255,255),outline=INK,width=2); d.ellipse([ex-2,25,ex+2,30],fill=INK)
    d.chord([ox+16,38,ox+42,52],0,180,fill=(255,255,255),outline=INK,width=2)   # the grin
    for k in range(3):                                               # the spinning legs, a blur
        a=f*0.9+k*0.6; d.arc([ox+10,48,ox+46,H+20],math.degrees(a),math.degrees(a)+50,fill=(90,90,96),width=3)
    if t>=0.2:
        big_text(im,"HOLA, VENGO A",8,(30,30,30),scale=2,cx=128,shadow=None)
        big_text(im,"REVOLEAR",24,(30,30,30),scale=2,cx=128,shadow=None)
        big_text(im,"LAS PATAS!",40,(30,30,30),scale=2,cx=128,shadow=None)
    if t<0.05: zoom_lines(d,INK)
    return im

# ---- the clips ------------------------------------------------------------------------------------------
def living(s,f,cpose,legs):
    """The neutral room: Valentina standing, Alejo and Carlitox on the couch (legs: None or an angle)."""
    s['under'].append(('av_couch_back',))
    acts=[actor(VALENTINA,VX,pal=VPAL),actor(seated(PLAYER['idle'],4),AX,y=SEAT-2,pal=APAL),
          actor(seated(CARLITOX[cpose]),CX,y=SEAT,pal=CPAL)]
    s['actors']=acts
    s['fx'].append(('av_couch_front',))
    angle,blur=legs if legs else (None,0)
    s['fx'].append(('av_legs',CX,GROUND-7,angle,blur))
    return s

def clip_patas(f):
    s=scene(f,THEME)
    legs=None; cpose='guard'
    if 14<=f<64: s['fx'].append(('av_bubble',"MIRA COMO REVOLEO LAS PATAS",CX,10,CX+2))
    if 60<=f<230:                                                    # spin up... and down
        t=(f-60)/170; speed=0.15+0.85*math.sin(math.pi*min(1,t*1.1))
        ang=sum(0.15+0.85*math.sin(math.pi*min(1,((g-60)/170)*1.1)) for g in range(60,f))*0.9
        legs=(ang,min(3,speed*4)); cpose='armsup' if (f//5)%2 and speed>0.6 else 'guard'
        if speed>0.6: s['shake']=rshake(1) if f%3==0 else (0,0)
    if 120<=f<180: s['image']=closeup_patas((f-120)/60,f); return s
    if 196<=f<236: s['fx'].append(('av_bubble',"...",AX,16,AX))
    living(s,f,cpose,legs)
    return s

def clip_flotar(f):
    s=scene(f,THEME)
    if 14<=f<24: living(s,f,'guard',None); s['fx'].append(('av_wipe',(f-14)/10)); return s
    if 24<=f<240:
        s['under'].append(('av_stage',))
        x,y,vis=99,GROUND-6,False
        bob=int(round(3*math.sin(f*0.12)))
        if 30<=f<60: x,vis=lerp(99,140,(f-30)/30),True                    # out from behind the curtain
        if 60<=f<130: x,vis=lerp(140,W+16,(f-60)/70),True                  # drifting across
        if 150<=f<230: x,vis=lerp(-16,99,(f-150)/80),True                  # and back, behind the curtain again
        if vis:
            spr=CARLITOX['guard']
            s['actors']=[actor(spr,x,y=GROUND-14+bob,pal=CPAL)]          # off the floor: he floats
            s['fx'].append(('av_stage_front',))                              # he passes behind the curtain
        if 40<=f<88: s['fx'].append(('av_bubble',"HOLA, VENGO A FLOTAR",x,10,x))
        if 230<=f<240: s['fx'].append(('av_wipe',1-(f-230)/10))
        return s
    living(s,f,'guard',None)
    return s

@fx('av_stage_front')
def _fx_stage_front(d,im,e,f):
    d.rectangle([70,14,128,GROUND],fill=(140,62,20),outline=INK)
    for x in (80,92,99,112,120): d.line([x,18,x+(1 if x%2 else -1),GROUND-2],fill=INK)

CLIPS = [clip('patas', N_, clip_patas), clip('flotar', N_, clip_flotar)]
