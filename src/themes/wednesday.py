"""What a week, huh? (the Tintin meme): no fight. Claude as Captain Haddock (the cap with the anchor, the
black beard, the blue sweater, the pipe) in the salon at Marlinspike, in Herge's clear line: thin black
outlines, flat colours, no shading. He drops into the armchair, the pipe smoking: WHAT A WEEK, HUH?
Tintin (the quiff, the plus-fours, Snowy at his feet) looks at him: CAPTAIN, IT'S WEDNESDAY. Close-up:
Haddock taking it in, the pipe falls out of his mouth, a drop of sweat, the cartoon anger lines —
BLISTERING BARNACLES! Snowy barks; the Captain gets up and it starts again."""
from engine import *

THEME = 'wednesday'
N_ = 288                                                            # a multiple of 12
CX, CHAIR, TX = 34, 70, 136                                         # Haddock standing; the armchair; Tintin
SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(20,20,24)
NAVY, NAVY_D = (40,60,130), (26,40,96)
# Haddock: the peaked cap with the gold anchor, the black beard, the navy sweater with its anchor
HPAL = {'1':NAVY_D,'2':(20,20,24),'3':(240,200,80),'4':NAVY,'5':(230,230,230)}
CAP = ["...111111...","..11131111..","1111111111.."]
# Tintin: ginger quiff, blue sweater over a white collar, plus-fours, brown shoes
TPAL = {'h':(220,130,50),'s':(240,200,170),'j':(90,140,200),'J':(90,140,200),'W':(250,250,250),'p':(200,170,120),'k':(110,70,40)}
TINTIN = S([
"....hh......","...hhh......","...hhhhh....","...ssssss...","...sKssKs...","...ssssss...","....ssss....",
"...WWWWWW...","..jjjjjjjj..",".sjjjjjjjjs.",".sjjjjjjjjs.","..jjjjjjjj..","...pppppp...","...pppppp...",
"...pp..pp...","...ss..ss...","...kk..kk...",])

def _haddock(spr):
    g=[list(r) for r in overlay(spr,CAP,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g]))
    for y in range(len(g)):
        for x in range(len(g[0])):
            c=g[y][x]
            if c=='O' and top+3<=y<=top+5 and x>=l+3: g[y][x]='2'          # the beard
            elif c=='O' and y>=top+6: g[y][x]='3' if (y==top+6 and x==(l+r)//2+1) else '4'   # sweater, anchor
            elif c=='o' and y>=top+5 and y<top+8: g[y][x]='4'
    return S([''.join(x) for x in g])
HADDOCK=variant(_haddock)

# ---- background: the salon at Marlinspike, in clear line -----------------------------------------------
def _salon(d):
    d.rectangle([0,0,W,H],fill=(214,226,196))                       # pale green wallpaper
    for x in range(8,W,16):
        for y in range(6,44,12): d.point((x,y),fill=(190,206,170)); d.point((x+8,y+6),fill=(190,206,170))
    d.rectangle([0,42,W,44],fill=(150,96,60)); d.line([0,42,W,42],fill=INK)   # the dado rail
    d.rectangle([96,6,128,26],fill=(160,120,60)); d.rectangle([98,8,126,24],fill=(170,210,230),outline=INK)   # a painting: a ship
    d.rectangle([98,18,126,24],fill=(70,110,170)); d.polygon([(104,18),(120,18),(118,21),(106,21)],fill=(120,70,40))
    d.line([112,10,112,18],fill=INK); d.polygon([(112,10),(112,17),(118,17)],fill=(250,250,250),outline=INK)
    d.rectangle([150,4,180,36],fill=(180,210,230),outline=INK)        # the window and its red curtains
    d.line([165,4,165,36],fill=INK); d.line([150,20,180,20],fill=INK)
    d.polygon([(146,2),(154,2),(152,38),(146,38)],fill=(190,50,50),outline=INK); d.polygon([(176,2),(184,2),(184,38),(178,38)],fill=(190,50,50),outline=INK)
    d.rectangle([0,44,W,H],fill=(170,120,80))                         # the floor and a rug
    d.ellipse([40,50,110,64],fill=(160,50,50),outline=INK); d.ellipse([48,53,102,62],outline=(220,190,120))
register_bg(THEME, lambda v: (v+120,v+80,v+50), decor=_salon)

@fx('wd_chair_back')
def _fx_chair_back(d,im,e,f):
    x=CHAIR; d.rounded_rectangle([x-10,GROUND-22,x+10,GROUND-6],radius=4,fill=(60,120,80),outline=INK)

@fx('wd_chair_front')
def _fx_chair_front(d,im,e,f):
    """The armchair's seat and arms, over the Captain's legs."""
    x=CHAIR
    d.rectangle([x-11,GROUND-8,x+11,GROUND-2],fill=(70,140,90),outline=INK)
    for ax in (x-13,x+9): d.rounded_rectangle([ax,GROUND-12,ax+4,GROUND-2],radius=2,fill=(60,120,80),outline=INK)
    for lx in (x-10,x+9): d.line([lx,GROUND-2,lx,GROUND],fill=INK)

@fx('wd_pipe')
def _fx_pipe(d,im,e,f):
    """The pipe in his mouth, smoke curling up from the bowl."""
    _,x,y,smoke=e; x,y=int(x),int(y)
    d.line([x,y,x+3,y+1],fill=(90,56,30)); d.rectangle([x+3,y-1,x+5,y+2],fill=(110,70,40),outline=INK)
    if smoke:
        for k in range(3): ph=(f+k*4)%12; d.point((x+4+int(math.sin(ph*0.6)),y-3-ph//2),fill=(200,200,206))

@fx('wd_snowy')
def _fx_snowy(d,im,e,f):
    """Snowy: small, white, black nose; bark: his mouth open and the lines."""
    _,x,bark=e; x=int(x); y=GROUND
    d.rectangle([x-4,y-5,x+2,y-1],fill=(250,250,250),outline=INK)
    d.ellipse([x+1,y-9,x+6,y-4],fill=(250,250,250),outline=INK); d.point((x+6,y-6),fill=INK); d.point((x+3,y-7),fill=INK)
    d.line([x-5,y-6,x-7,y-8],fill=INK)                               # the tail, up
    for lx in (x-3,x+1): d.line([lx,y-1,lx,y],fill=INK)
    if bark:
        d.line([x+5,y-5,x+7,y-5],fill=INK)
        for k in range(3): d.line([x+8,y-8+k*2,x+10,y-9+k*2],fill=INK)

@fx('wd_balloon')
def _fx_balloon(d,im,e,f):
    """A Herge balloon: white, a fine black line, the tail to the speaker."""
    _,lines,cx,y,tail=e; lines=[lines] if isinstance(lines,str) else lines
    w=max(len(l) for l in lines)*4+7; h=len(lines)*7+4; x=max(1,min(W-w-2,int(cx-w/2)))
    d.rounded_rectangle([x,y,x+w,y+h],radius=4,fill=(255,255,255),outline=INK)
    tx=max(x+4,min(x+w-4,int(tail))); d.polygon([(tx-2,y+h),(tx+2,y+h),(int(tail),y+h+5)],fill=(255,255,255),outline=INK)
    d.line([tx-1,y+h,tx+1,y+h],fill=(255,255,255))
    for i,l in enumerate(lines): text(d,l,x+4,y+3+i*7,INK,shadow=None)

# ---- close-up -----------------------------------------------------------------------------------------
def closeup_haddock(t,f):
    """Primer plano: the Captain taking it in. The eyes go round, the pipe drops, a bead of sweat, the
    anger lines — BLISTERING BARNACLES!"""
    im=Image.new('RGB',(W,H),(214,226,196)); d=ImageDraw.Draw(im)
    ox=22; shock=t>=0.3
    d.rectangle([ox,16,ox+60,H],fill=SKIN,outline=INK)
    d.polygon([(ox,40),(ox+60,40),(ox+60,H),(ox,H)],fill=(24,24,28))  # the beard
    for k in range(6): d.line([ox+4+k*10,40,ox+8+k*10,48],fill=(60,60,66))
    d.rectangle([ox-4,4,ox+64,18],fill=NAVY_D,outline=INK); d.rectangle([ox-8,16,ox+40,20],fill=(20,20,30),outline=INK)   # the cap
    d.ellipse([ox+26,6,ox+34,14],fill=(240,200,80),outline=INK); d.line([ox+30,8,ox+30,13],fill=INK)   # the anchor badge
    for ex in (ox+18,ox+42):
        if shock: d.ellipse([ex-5,24,ex+5,36],fill=(255,255,255),outline=INK); d.ellipse([ex-1,28,ex+1,31],fill=INK)
        else: d.line([ex-4,30,ex+4,30],fill=INK,width=2)             # tired, half shut
        d.line([ex-6,22 if shock else 25,ex+6,21 if shock else 26],fill=INK,width=2)
    py=36 if t<0.4 else int(lerp(36,H+10,(t-0.4)/0.15))              # the pipe falls out
    d.line([ox+34,py+6,ox+46,py+10],fill=(90,56,30),width=2); d.rectangle([ox+46,py+4,ox+52,py+12],fill=(110,70,40),outline=INK)
    if t>=0.45:                                                      # sweat, anger lines
        d.polygon([(ox+64,22),(ox+61,28),(ox+67,28)],fill=(120,190,240),outline=INK)
        for k in range(3):
            a=-2.2+k*0.5; x0,y0=ox+30+math.cos(a)*44,24+math.sin(a)*30
            d.line([x0,y0,x0+math.cos(a)*6,y0+math.sin(a)*6],fill=INK,width=2)
    if t>=0.55:
        jj=(f%3)-1
        big_text(im,"BLISTERING",14,(220,40,40),scale=2,cx=138+jj,outline=INK)
        big_text(im,"BARNACLES!",32,(220,40,40),scale=2,cx=138+jj,outline=INK)
    if t<0.05: zoom_lines(d,INK)
    return im

# ---- the clip -----------------------------------------------------------------------------------------
def clip_wednesday(f):
    s=scene(f,THEME)
    hx,hy,hpose,hflip,sitting=CX,GROUND,guard_pose(f),False,False
    # 1) he drops into the armchair
    if 14<=f<28: hx,hpose=ez(CX,CHAIR,(f-14)/14),'dash'
    if 28<=f<200: hx,hy,hpose,sitting=CHAIR,GROUND-4,'guard',True
    if 40<=f<86: s['fx'].append(('wd_balloon',"WHAT A WEEK, HUH?",CHAIR-6,8,CHAIR+2))
    if 88<=f<134: s['fx'].append(('wd_balloon',"CAPTAIN, IT'S WEDNESDAY.",TX-26,8,TX))
    # 2) close-up
    if 134<=f<194: s['image']=closeup_haddock((f-134)/60,f); return s
    # 3) Snowy barks; the Captain gets up and goes back
    bark=196<=f<228 and (f//4)%2==0
    if 196<=f<228: s['fx'].append(('wd_balloon',"WOOF!",TX+14,26,TX+16))
    if 200<=f<222: hx,hy,hpose,sitting=CHAIR,GROUND,'armsup',False
    if 222<=f<240: hx,hpose,hflip=ez(CHAIR,CX,(f-222)/18),'dash',True
    s['under'].append(('wd_chair_back',))
    acts=[actor(TINTIN,TX,flip=True,pal=TPAL),actor(HADDOCK[hpose],hx,hy,flip=hflip,pal=HPAL)]
    s['actors']=acts
    if sitting: s['fx'].append(('wd_chair_front',))
    else: s['under'].append(('wd_chair_front',))
    ox,oy=origin(HADDOCK[hpose],hx,hy); top,l,r=body_box(HADDOCK[hpose])
    px=ox+(r+1 if not hflip else len(HADDOCK[hpose][0])-r-5); s['fx'].append(('wd_pipe',px,oy+top+4,sitting))
    s['fx'].append(('wd_snowy',TX+14,bark))
    return s

CLIPS = [clip('wednesday', N_, clip_wednesday)]
