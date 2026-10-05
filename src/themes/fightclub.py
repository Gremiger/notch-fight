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
CX, TX = 70, 116                                                    # Claude; Tyler, when he's there
INK = (16,12,12)
BLOOD, BLOOD_D = (176,20,24), (110,10,14)
SOAP = (236,150,170)

# the Narrator: the white shirt, the dark tie loosened, grey trousers, a bruise round one eye (and blood)
CPAL = {'1':(236,232,220),'2':(110,24,28),'3':(64,64,70),'4':(110,60,120),'5':BLOOD}
def _narrator(spr):
    g=[list(r) for r in spr]; top,l,r=body_box(spr); h=len(g)
    for y in range(h):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and y>=top+5:
                g[y][x]='2' if x==(l+r)//2+1 and y<top+8 else ('3' if y>=top+8 else '1')
            elif c=='O' and top+2<=y<=top+3 and g[y][x+1:x+2]==['K']: g[y][x]='4'     # the black eye
            elif c=='o' and y>=top+8: g[y][x]='3'
    return S([''.join(x) for x in g])
NARR=variant(_narrator)
def bloody(spr,level):
    """The same pose with blood on the face: a split brow, then the nose, then the mouth."""
    g=[list(r) for r in spr]; top,l,r=body_box(spr)
    spots=[(r-1,top+1),(r-1,top+4),(r-2,top+4),(l+3,top+1),(r-3,top+4),(l+2,top+4)][:level]
    for x,y in spots:
        if g[y][x]=='O': g[y][x]='5'
    return S([''.join(x) for x in g])

TPAL = {'h':(196,166,110),'s':(232,196,166),'G':(16,16,20),'r':(168,40,30),'R':(120,24,18),'W':(214,190,120),'p':(70,80,110),'k':(30,26,24),'5':BLOOD}
TYLER=poses(S([
"...h.hh.h...","..hhhhhhhh..","...ssssss...","...GGsGGs...","...ssssss...","....ssss....",
"..rrrrrrrr..",".srrrWWrrrs.",".sRrrWWrrRs.","..rrrWWrrr..","..rrrrrrrr..","...pppppp...",
"...pppppp...","...pp..pp...","...pp..pp...","...kk..kk...",]),7,'s',3)

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

@fx('fc_selfhit')
def _fx_selfhit(d,im,e,f):
    """His own fist, back into his own face."""
    _,x,y=e; d.line([x-6,y+6,x,y],fill=(168,80,54),width=2); d.rectangle([x-1,y-2,x+2,y+1],fill=(217,119,87),outline=INK)

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
    d.rectangle([4,6,66,H+4],fill=(217,119,87),outline=INK)          # Claude's face, big
    d.rectangle([60,6,66,H],fill=(168,80,54))
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
        d.rectangle([sx-6,40,sx+4,56],fill=(217,119,87),outline=INK)  # the thumb
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
HITS = ((100,'tyler'),(116,'claude'),(130,'tyler'),(144,'claude'),(156,'tyler'),(166,'claude'))

def clip_rules(f):
    s=scene(f,THEME)
    if 14<=f<80: s['image']=card_rules((f-14)/66,f); return s
    if 170<=f<250: s['image']=closeup_soap((f-170)/80,f); return s
    if 296<=f<352: s['image']=window((f-296)/56,f); return s
    if 352<=f<366: s['image']=fade_to(window(1.0,f),(0,0,0),(f-352)/14); return s
    s['under']+=[('fc_crowd','back'),('fc_light',)]
    pose=guard_pose(f); tpose='idle'; tx=None; blood=0; spatters=0
    fight=80<=f<296
    if 80<=f<170:
        tx=lerp(W+10,TX,ease((f-80)/16))
        for hf,who in HITS:
            if hf<=f<hf+8:
                if who=='tyler': tpose='attack'; pose='hurt'; tx-=4
                else: pose='punch'; tpose='hurt'
            if f>=hf: blood+=1 if who=='tyler' else 0; spatters+=2
            if hf<=f<hf+14:
                k=f-hf
                if who=='tyler': s['fx'].append(('fc_spray',CX+4,GROUND-9,k,-1))
                else: s['fx'].append(('fc_spray',tx-4,GROUND-13,k,1))
                if k<3: s['shake']=rshake(1)
    if 250<=f<296:
        blood,spatters=3,12
        if f<262 and (f//2)%3==0: tx=TX                              # Tyler flickers... and is gone
        k=(f-262)%10
        if f>=262: pose='hurt' if k<4 else 'guard';
        if f>=262 and k<3: s['fx'].append(('fc_selfhit',CX+4,GROUND-9)); s['shake']=rshake(1) if k==0 else (0,0)
    if fight: s['under'].append(('fc_floorblood',spatters))
    acts=[]
    if tx is not None: acts.append(actor(TYLER[tpose],tx,flip=True,pal=TPAL))
    acts.append(actor(bloody(NARR[pose],min(6,blood*2)) if blood else NARR[pose],CX,pal=CPAL))
    s['actors']=acts
    s['fx'].append(('fc_crowd','front'))
    return s

CLIPS = [clip('rules', N_, clip_rules)]
