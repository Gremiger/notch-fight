"""Fight Club: Claude as the Narrator (white shirt, the tie loosened, a black eye) in the basement of Lou's
Tavern: one bare bulb swinging on its cord, the crowd standing in a ring in the dark (a back row against
the bricks, a front row in silhouette). Clip `rules`, raw: THE FIRST RULE OF FIGHT CLUB IS... (and the rest
is crossed out); Tyler (the red leather jacket, the shades) steps into the ring and they trade bare-knuckle
punches, the blood landing on the concrete, his face getting worse. Close-up: the bloody grin, the pink bar
of Paper Street soap, I AM JACK'S SMIRKING REVENGE. Then Tyler flickers, and is gone: Claude alone in the
ring, hitting himself. The end: the window, the towers coming down one by one, holding Marla's hand —
WHERE IS MY MIND?"""
from engine import *

THEME = 'fightclub'
N_ = 384                                                            # a multiple of 12 and of 48 (the bulb)
CX, TX = 80, 98                                                     # Claude; Tyler, when he's there (in reach)
INK = (16,12,12)
BLOOD, BLOOD_D = (176,20,24), (110,10,14)
SOAP = (236,150,170)

# ---- the two of them: built from a pose, so they move alike --------------------------------------------
GW, GH, C = 28, 24, 12                                              # grid, centre column (they face right)
ARMS = {    # pose -> (back elbow, back fist, front elbow, front fist), from (C, shoulder row); lean; legs
 'guard': ((1,4),(4,-2),(3,4),(6,-3),0,'stance'),
 'guard2':((1,4),(4,-1),(3,4),(6,-2),0,'stance'),
 'jab':   ((1,4),(4,-2),(6,0),(11,-2),1,'lunge'),
 'hook':  ((4,-1),(10,-3),(3,4),(5,-1),2,'lunge'),
 'hurt':  ((-3,3),(-6,1),(1,5),(4,6),-2,'reel'),
 'self':  ((1,4),(4,-2),(7,2),(3,-4),-1,'stance'),
 'down':  ((0,6),(1,8),(2,6),(4,8),0,'stand'),
}
def _put(g,x,y,c):
    if 0<=x<GW and 0<=y<GH: g[y][x]=c
def _seg(g,x0,y0,x1,y1,c):
    n=max(abs(x1-x0),abs(y1-y0),1)
    for i in range(n+1): _put(g,round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n),c)
LEGS = {                                                            # (back foot dx, front foot dx, knee bend)
 'stance':(-3,3,0),'lunge':(-5,5,1),'reel':(-4,2,0),'stand':(-1,1,0)}

_built={}
def build(who,pose,blood=0):
    """A fighter: legs, torso (leaning), head, two arms of two segments each with a fist; blood 0..3."""
    key=(who['name'],pose,blood)
    if key in _built: return _built[key]
    g=[['.']*GW for _ in range(GH)]
    be,bf,fe,ff,lean,legs=ARMS[pose]
    hip=GH-9; ty=hip-7; hy=ty-5                                      # legs 9 rows, torso 7, head 5
    bx,fx_,bend=LEGS[legs]
    for k,(dx,c) in enumerate(((bx,'P'),(fx_,'p'))):                 # the legs, the shoes
        for t in range(9):
            fr=t/8; x=C+round(dx*fr)+(bend if 3<t<7 and k==1 else 0)+(k*2-1)
            _put(g,x,hip+t,c); _put(g,x+1,hip+t,c)
        _put(g,C+dx+(k*2-1)+2,GH-1,'k'); _put(g,C+dx+(k*2-1),GH-1,'k'); _put(g,C+dx+(k*2-1)+1,GH-1,'k')
    sh=lambda y: round(lean*(hip-y)/(hip-hy))                       # the lean, more at the top
    def arm(e,f_,front):
        sx=C+(2 if front else -2)+sh(ty+1); sy=ty+1
        ex,ey=C+e[0]+sh(ty),ty+e[1]; fx2,fy2=C+f_[0]+sh(ty),ty+f_[1]
        _seg(g,sx,sy,ex,ey,'a' if front else 'A'); _seg(g,ex,ey,fx2,fy2,'s' if who['bare'] else ('a' if front else 'A'))
        for dx,dy in ((0,0),(1,0),(0,1),(1,1)): _put(g,fx2+dx,fy2+dy,'f')
    arm(be,bf,False)
    for y in range(ty,hip+1):                                        # the torso, the belt
        o=sh(y)
        for x in range(C-3+o,C+3+o): _put(g,x,y,'b' if y==hip-1 else ('w' if y==ty else 'j'))
        if who['name']=='narr' and y<hip-1: _put(g,C+1+o,y,'t')      # the tie, loosened
        if who['name']=='tyler' and y<hip-1: _put(g,C+o,y,'u'); _put(g,C+1+o,y,'u')   # the shirt under the open jacket
    o=sh(hy)
    for y in range(hy,hy+5):                                         # the head
        for x in range(C-2+o,C+3+o): _put(g,x,y,'s')
    _put(g,C+1+o,hy+2,'K'); _put(g,C-1+o,hy+2,'K')
    if who['name']=='tyler':
        for x in range(C-2+o,C+3+o): _put(g,x,hy+2,'G')              # the shades
    else:
        _put(g,C+1+o,hy+1,'v'); _put(g,C+2+o,hy+2,'v'); _put(g,C+2+o,hy+3,'v')   # the black eye
    for i,row in enumerate(who['hair']):
        for j,ch in enumerate(row):
            if ch!='.': _put(g,C-3+o+j,hy-len(who['hair'])+1+i,ch)
    for x,y in ((C+2,hy+1),(C+2,hy+4),(C+1,hy+4),(C+2,hy+3),(C,hy+4),(C+1,ty+1))[:blood*2]:   # the brow, the nose, the mouth, the shirt
        _put(g,x+o,y,'r')
    arm(fe,ff,True)
    _built[key]=S([''.join(r) for r in g]); return _built[key]

NARRATOR = dict(name='narr', bare=False, hair=["..hhhh.","hhhhhhh","hh....."])
TYLER    = dict(name='tyler',bare=False, hair=["h.h.h..","hhhhhh.","hhhhhhh","hh....."])
CPAL = {'s':(232,192,160),'K':INK,'h':(70,46,32),'j':(232,228,216),'w':(250,248,240),'A':(200,196,186),'a':(232,228,216),
        't':(110,24,28),'b':(40,30,26),'p':(64,64,70),'P':(50,50,56),'k':(24,20,20),'f':(232,192,160),'v':(110,60,120),'r':BLOOD}
TPAL = {'s':(232,196,166),'K':INK,'G':(12,12,14),'h':(204,170,110),'j':(168,40,30),'w':(120,24,18),'A':(130,28,20),'a':(168,40,30),
        'u':(214,180,90),'b':(40,30,26),'p':(70,84,120),'P':(56,68,100),'k':(30,26,24),'f':(232,196,166),'r':BLOOD}

# ---- the basement -------------------------------------------------------------------------------------
def _basement(d):
    d.rectangle([0,0,W,H],fill=(26,20,18))
    for y in range(0,42,4):                                          # the bricks, barely there
        for x in range((y//4)%2*6,W,12): d.rectangle([x,y,x+10,y+2],fill=(36,28,24))
    d.line([0,5,W,5],fill=(46,40,36)); d.line([0,7,W,7],fill=(40,34,30))   # a pipe along the ceiling
    d.rectangle([0,42,W,H],fill=(44,42,40))                          # the concrete
    for x in range(-40,W+40,22): d.line([92+(x-92)*0.4,42,x,H],fill=(38,36,34))
register_bg(THEME, lambda v: (v+20,v+18,v+16), decor=_basement)

def bulb_x(f): return 92+6*math.sin(2*math.pi*(f%48)/48)

@fx('fc_light')
def _fx_light(d,im,e,f):
    """The bulb on its cord, the cone and the pool of light on the floor (it swings)."""
    bx=bulb_x(f); m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    md.polygon([(bx-3,12),(bx+3,12),(bx+60,H),(bx-60,H)],fill=46)
    md.ellipse([bx-58,46,bx+58,H+8],fill=70)
    im.paste((255,214,150),(0,0),m.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    d.line([92,0,bx,9],fill=(20,20,20)); d.rectangle([bx-1,8,bx+1,9],fill=(60,60,60))
    d.ellipse([bx-2,10,bx+2,14],fill=(255,240,200))

@fx('fc_crowd')
def _fx_crowd(d,im,e,f):
    """The ring: a back row against the wall, lit along the tops of their heads; or the front row, in silhouette."""
    _,row=e; rr=random.Random(5 if row=='back' else 6)
    if row=='back':
        for i in range(17):
            x=4+i*11+rr.randint(-2,2); y=30+rr.randint(-2,2)+((f//24+i)%4==0)
            d.rectangle([x-4,y+5,x+4,46],fill=(14,12,12)); d.ellipse([x-3,y,x+3,y+6],fill=(18,14,14))
            d.line([x-2,y,x+2,y],fill=(110,86,60))
    else:
        for x,y in ((6,46),(20,49),(170,48),(182,46)):
            d.ellipse([x-8,y,x+8,y+14],fill=(8,6,6)); d.rectangle([x-12,y+10,x+12,H],fill=(8,6,6))

@fx('fc_floorblood')
def _fx_floorblood(d,im,e,f):
    """Blood on the concrete: n spatters so far."""
    _,n=e; rr=random.Random(32)
    for i in range(n):
        x=rr.randint(60,128); y=rr.randint(54,62); r=rr.randint(1,3)
        d.ellipse([x-r,y-r*0.5,x+r,y+r*0.5],fill=BLOOD_D); d.point((x+r+1,y),fill=BLOOD_D)

@fx('fc_spray')
def _fx_spray(d,im,e,f):
    """Drops flying off a punch (k frames old), going dir."""
    _,x,y,k,dr=e; rr=random.Random(int(x)*3+int(y))
    for _ in range(6):
        vx=rr.uniform(0.6,1.8)*dr; vy=rr.uniform(-1.6,-0.3)
        px=x+vx*k; py=y+vy*k+0.18*k*k
        if py<GROUND: d.point((int(px),int(py)),fill=BLOOD); d.point((int(px)+1,int(py)),fill=BLOOD_D)

# ---- the card, the close-up, the window -----------------------------------------------------------------
def card_rules(t,f):
    """THE FIRST RULE OF FIGHT CLUB IS... and the rest, crossed out before it's said."""
    im=Image.new('RGB',(W,H),(8,6,6)); d=ImageDraw.Draw(im)
    big_text(im,"THE FIRST RULE",4,(236,232,220),scale=2,shadow=None)
    if t>=0.15: big_text(im,"OF FIGHT CLUB IS...",20,(236,232,220),scale=2,shadow=None)
    if t>=0.5:
        text(d,"YOU DO NOT TALK ABOUT FIGHT CLUB",W//2-64,44,(200,190,176),shadow=None)
        k=min(1,(t-0.6)/0.15)
        if k>0: d.line([W//2-67,46,W//2-67+int(134*k),46],fill=BLOOD); d.line([W//2-67,47,W//2-67+int(134*k),47],fill=BLOOD_D)
    if (f//2)%7==0: d.point((random.Random(f).randint(0,W-1),random.Random(f+1).randint(0,H-1)),fill=(80,80,80))   # film grain
    return im

def closeup_soap(t,f):
    """Primer plano: the grin with blood in the teeth, the bruised eye; the pink bar of soap, PAPER STREET
    SOAP CO.; then I AM JACK'S SMIRKING REVENGE."""
    im=Image.new('RGB',(W,H),(30,24,20)); d=ImageDraw.Draw(im)
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([-30,-30,110,90],fill=90); im.paste((255,210,150),(0,0),g.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    d.rectangle([4,6,66,H+4],fill=CPAL['s'],outline=INK)            # his face, big
    d.rectangle([60,6,66,H],fill=(200,156,124)); d.rectangle([4,0,66,9],fill=CPAL['h'],outline=INK)
    d.rectangle([18,18,22,28],fill=INK); d.rectangle([42,18,46,28],fill=INK)   # the eyes
    d.ellipse([36,13,54,32],outline=(110,60,120),width=3)            # the black eye
    d.line([16,13,26,15],fill=BLOOD,width=2); d.line([24,15,22,24],fill=BLOOD)  # the split brow, running
    d.rectangle([14,40,54,48],fill=(250,246,236),outline=INK)        # the grin
    for x in range(20,54,6): d.line([x,40,x,48],fill=INK)
    for x in (26,38): d.rectangle([x-2,41,x+2,47],fill=BLOOD)        # blood in the teeth
    d.line([34,30,35,40],fill=BLOOD,width=2); d.line([48,48,50,60],fill=BLOOD,width=2)   # the nose, the chin
    if t<0.45:                                                       # the soap, held up
        sx=lerp(W+10,92,ease(min(1,t/0.15)))
        d.rounded_rectangle([sx,18,sx+76,50],radius=8,fill=SOAP,outline=(170,90,110))
        d.rounded_rectangle([sx+4,22,sx+72,46],radius=6,outline=(214,124,148))
        text(d,"PAPER STREET",int(sx)+14,28,(176,86,108),shadow=None); text(d,"SOAP CO.",int(sx)+22,36,(176,86,108),shadow=None)
        d.rectangle([sx-6,40,sx+4,56],fill=CPAL['s'],outline=INK)  # the thumb
    else:
        big_text(im,"I AM JACK'S",6,(236,232,220),scale=2,cx=126,shadow=INK)
        big_text(im,"SMIRKING",24,(236,232,220),scale=2,cx=126,shadow=INK)
        big_text(im,"REVENGE.",42,BLOOD,scale=2,cx=126,shadow=INK)
    if t<0.04: zoom_lines(d,(255,214,150))
    return im

def window(t,f):
    """The end: the dark office, the big window, the towers coming down one by one; the two of them from
    behind, holding hands. WHERE IS MY MIND?"""
    im=Image.new('RGB',(W,H),(14,16,30)); d=ImageDraw.Draw(im)
    for y in range(44): d.line([0,y,W,y],fill=(int(18+20*y/44),int(20+14*y/44),int(44+20*y/44)))
    towers=((10,16,22),(30,8,16),(50,20,18),(74,4,20),(100,14,16),(122,10,22),(150,6,18),(170,18,14))
    for i,(x,top,w) in enumerate(towers):
        start=0.12+0.08*i; k=max(0,min(1,(t-start)/0.18))
        y0=top+int(k*(48-top))                                     # it sinks into its own dust
        if y0<46:
            d.rectangle([x,y0,x+w,46],fill=(30,32,44))
            rr=random.Random(i)
            for wy in range(y0+3,46,4):
                for wx in range(x+2,x+w-1,3):
                    if rr.random()<0.5: d.point((wx,wy),fill=(240,210,120))
        raw=(t-start)/0.18
        if 0<raw<1.6:                                                # its dust, rising and thinning
            a=1-abs(raw-0.6)/1.0
            for j in range(5):
                r=3+raw*3; cx=x+j*w/4; cy=44-raw*6-j%2*3
                d.ellipse([cx-r,cy-r*0.7,cx+r,cy+r*0.7],fill=tuple(int(lerp(c0,c1,max(0,a))) for c0,c1 in zip((24,26,42),(96,92,96))))
        if start<=t<start+0.03: d.rectangle([x-2,0,x+w+2,46],outline=(255,200,120))   # the flash
    d.rectangle([0,44,W,H],fill=(10,10,14))
    for x in (0,62,124,184): d.rectangle([x-1,0,x+1,46],fill=(8,8,10))   # the mullions
    d.rectangle([0,44,W,47],fill=(8,8,10))
    for x,hair in ((84,False),(100,True)):                           # the two of them, from behind
        d.ellipse([x-4,30,x+4,40],fill=(6,6,8)); d.rectangle([x-6,38,x+6,H],fill=(6,6,8))
        if hair: d.ellipse([x-6,28,x+6,38],fill=(6,6,8))
    d.line([90,48,94,48],fill=(6,6,8),width=2)                       # their hands
    if t>=0.15: big_text(im,"WHERE IS MY MIND?",6,(236,232,220),scale=2,shadow=INK)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
HITS = ((100,'tyler','jab'),(114,'claude','jab'),(126,'tyler','hook'),(140,'claude','hook'),(152,'tyler','jab'),(162,'claude','hook'))

def clip_rules(f):
    s=scene(f,THEME)
    if 14<=f<80: s['image']=card_rules((f-14)/66,f); return s
    if 170<=f<250: s['image']=closeup_soap((f-170)/80,f); return s
    if 296<=f<352: s['image']=window((f-296)/56,f); return s
    if 352<=f<366: s['image']=fade_to(window(1.0,f),(0,0,0),(f-352)/14); return s
    s['under']+=[('fc_crowd','back'),('fc_light',)]
    g=guard_pose(f); pose,tpose='guard' if g=='guard' else 'guard2','guard' if g=='guard2' else 'guard2'
    cx,tx=CX,None; blood=0; spatters=0
    fight=80<=f<296
    if 80<=f<170:
        tx=lerp(W+14,TX,ease((f-80)/18))
        for hf,who,kind in HITS:
            if f>=hf+2 and who=='tyler': blood=min(3,blood+1)
            if f>=hf+2: spatters+=2
            if hf<=f<hf+7:                                           # the punch: a step in, it lands
                if who=='tyler': tpose=kind; tx-=3
                else: pose=kind; cx+=3
            if hf+2<=f<hf+10:                                        # the head snaps back
                if who=='tyler': pose='hurt'; cx-=2
                else: tpose='hurt'; tx+=2
            if hf+2<=f<hf+16:
                k=f-hf-2
                if who=='tyler': s['fx'].append(('fc_spray',cx+1,GROUND-19,k,-1))
                else: s['fx'].append(('fc_spray',tx-1,GROUND-19,k,1))
                if k<2: s['shake']=rshake(1)
    if 250<=f<296:
        blood,spatters=3,12
        if f<262 and (f//2)%3==0: tx=TX                              # Tyler flickers... and is gone
        if f>=262:
            k=(f-262)%12; pose='self' if k<5 else ('hurt' if k<9 else 'guard')
            if k==3: s['shake']=rshake(1)
            if 3<=k<10: s['fx'].append(('fc_spray',cx+2,GROUND-19,k-3,-1))
    if fight: s['under'].append(('fc_floorblood',spatters))
    acts=[]
    if tx is not None: acts.append(actor(build(TYLER,tpose),tx,flip=True,pal=TPAL))
    acts.append(actor(build(NARRATOR,pose,blood),cx,pal=CPAL))
    s['actors']=acts
    s['fx'].append(('fc_crowd','front'))
    return s

CLIPS = [clip('rules', N_, clip_rules)]
