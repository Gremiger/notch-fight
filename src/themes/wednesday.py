"""What a week, huh? (the Tintin meme): no fight, as in the panel. Claude as Captain Haddock, a bit worse
for wear: hair all over the place, the black beard, red nose and cheeks, the blue sweater, slumped over
the bar with a pint. Herge's clear line: flat ochre wall, fine black outlines, a thick panel border.
He drinks: WHAT A WEEK, HUH? Tintin, in his brown coat, a sideways look: CAPTAIN, IT'S WEDNESDAY.
Close-up: the Captain's bleary face taking it in — the eyes pop: BLISTERING BARNACLES! Snowy, up on the
counter, sniffs the beer, sweat flying off his ears; the Captain pulls the pint back."""
from engine import *

THEME = 'wednesday'
N_ = 288                                                            # a multiple of 12
TOP = 55                                                            # the top of the counter
TX, HX, BEER, SNX = 36, 98, 138, 166                                 # Tintin, Haddock, the pint, Snowy
SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(20,20,24)
BAR, BAR_D = (120,74,40), (84,50,26)
# Haddock: hair everywhere, the beard, a red nose and cheeks, half-shut eyes, the blue sweater
HPAL = {'1':(20,20,24),'2':(28,26,30),'4':(70,110,190),'5':(64,100,176),'6':(220,70,60)}
HAIR = ["1..1.1..1.1.",".1111111111.","111111111111"]
# Tintin: ginger quiff, rosy cheek, the brown coat over a white collar
TPAL = {'h':(230,130,50),'s':(244,200,170),'j':(150,120,70),'J':(150,120,70),'W':(250,250,250),'r':(240,130,120),'p':(130,104,60),'k':(80,56,30)}
TINTIN = S([
"....hh......","...hhh......","...hhhhh....","...ssssss...","...sKssKs...","...ssrsss...","....ssss....",
"...WWWWWW...","..jjjjjjjj..",".jjjjjjjjjj.",".jjjjjjjjjj.","..jjjjjjjj..","..jjjjjjjj..",])          # cut by the bar

def _haddock(spr):
    g=[list(r) for r in overlay(spr,HAIR,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g])); w=len(g[0])
    for y in range(len(g)):
        for x in range(w):
            c=g[y][x]
            if c=='K' and y==top+2: g[y][x]='O'                         # half-shut, bleary eyes
            elif c=='O' and y<=top+1 and x<=l+1: g[y][x]='1'            # the mop over the back of the head
            elif c=='O' and top+3<=y<=top+5 and x>=l+3: g[y][x]='2'     # the beard
            elif c=='O' and y>=top+6: g[y][x]='4' if (x+y)%5 else '5'   # the sweater
            elif c=='o' and top+5<=y<top+8: g[y][x]='4'
    if r+1<w: g[top+3][r+1]='6'                                         # the red nose, poking out
    if g[top+3][r-3]=='2': g[top+3][r-3]='6'                            # a flushed cheek above the beard
    return S([''.join(x) for x in g])
HADDOCK=variant(_haddock)
def scale2(spr): return S([''.join(c*2 for c in r) for r in spr for _ in (0,1)])
BIG={k:scale2(v) for k,v in HADDOCK.items()}                         # the panel is a close shot: double size
TINTIN2=scale2(TINTIN)
SNOWY=scale2(S(["..W.W...","..WWW...",".WWWWWWW","KWWWWWWW",".WWWWWWW","..W...W."]))

# ---- background: the bar, ochre and flat --------------------------------------------------------------
def _bar(d):
    d.rectangle([0,0,W,H],fill=(196,168,116))                       # the ochre wall
    rr=random.Random(41)
    for _ in range(40): d.point((rr.randint(0,W-1),rr.randint(0,TOP)),fill=(186,158,108))
    d.rectangle([0,TOP,W,H],fill=BAR)                               # the counter (drawn again over them)
register_bg(THEME, lambda v: (v+120,v+90,v+50), decor=_bar)

@fx('wd_border')
def _fx_border(d,im,e,f):
    """The panel: a cream margin and a thick, slightly wobbly black border."""
    d.rectangle([0,0,W-1,H-1],outline=(244,240,230),width=2)
    d.rectangle([2,2,W-3,H-3],outline=INK,width=1); d.line([3,3,W-4,3],fill=INK)

@fx('wd_pint')
def _fx_pint(d,im,e,f):
    """A pint of beer, foam on top (level 0..1); x,y = its foot."""
    _,x,y,level=e; x,y=int(x),int(y)
    d.polygon([(x-3,y-11),(x+3,y-11),(x+2,y),(x-2,y)],fill=(236,236,230),outline=INK)
    top=int(y-1-9*level)
    if level>0: d.polygon([(x-2,top),(x+2,top),(x+2,y-1),(x-2,y-1)],fill=(230,170,60)); d.line([x-2,top,x+2,top],fill=(255,250,240))
    d.line([x-1,y-9,x-1,y-2],fill=(255,255,255))

@fx('wd_sweat')
def _fx_sweat(d,im,e,f):
    """Drops flying off Snowy's ears."""
    _,x,y=e
    for k in range(3): a=-2.6+k*0.6; d.point((int(x+math.cos(a)*(6+f%4)),int(y+math.sin(a)*(4+f%4))),fill=(120,190,240))

@fx('wd_balloon')
def _fx_balloon(d,im,e,f):
    """A Herge balloon: a white box with a fine black line and a zigzag tail down to the speaker."""
    _,lines,x,y,tail=e; lines=[lines] if isinstance(lines,str) else lines
    w=max(len(l) for l in lines)*4+9; h=len(lines)*7+5
    d.rectangle([x,y,x+w,y+h],fill=(255,255,255),outline=INK)
    tx,ty=int(tail[0]),int(tail[1])
    bx=max(x+6,min(x+w-6,tx+4))
    d.line([bx,y+h,bx-3,y+h+3,bx+1,y+h+5,tx,ty],fill=INK)
    for i,l in enumerate(lines): text(d,l,x+5,y+3+i*7,INK,shadow=None)

# ---- close-up -----------------------------------------------------------------------------------------
def closeup_haddock(t,f):
    """Primer plano: the Captain's bleary face, hair everywhere, red nose — it sinks in, the eyes pop:
    BLISTERING BARNACLES!"""
    im=Image.new('RGB',(W,H),(196,168,116)); d=ImageDraw.Draw(im)
    ox=22; pop=t>=0.35
    d.rectangle([ox,12,ox+60,H],fill=SKIN,outline=INK)
    d.polygon([(ox,38),(ox+60,38),(ox+60,H),(ox,H)],fill=(24,24,28))    # the beard
    rr=random.Random(3)
    for k in range(18):                                               # the hair, all over the place
        x=ox-4+rr.randint(0,68); d.line([x,16,x+rr.randint(-6,6),rr.randint(0,8)],fill=INK,width=2)
    d.rectangle([ox,8,ox+60,16],fill=INK)
    for ex in (ox+18,ox+42):
        if pop: d.ellipse([ex-5,22,ex+5,34],fill=(255,255,255),outline=INK); d.ellipse([ex-1,27,ex+1,30],fill=INK)
        else:                                                         # half-shut, bleary
            d.chord([ex-5,24,ex+5,34],0,180,fill=(255,255,255),outline=INK); d.point((ex,30),fill=INK)
            d.line([ex-6,24,ex+6,24],fill=INK,width=2)
        d.ellipse([ex-7,32,ex+1,36],fill=(230,110,100))                   # flushed cheeks
    d.ellipse([ox+26,28,ox+38,42],fill=(220,70,60),outline=INK)          # the red nose
    d.ellipse([ox+28,46,ox+34,50],fill=(250,250,250))                    # the open mouth in the beard
    if t>=0.45:
        for k in range(3):
            a=-2.2+k*0.5; x0,y0=ox+30+math.cos(a)*42,26+math.sin(a)*28
            d.line([x0,y0,x0+math.cos(a)*6,y0+math.sin(a)*6],fill=INK,width=2)
    if t>=0.55:
        jj=(f%3)-1
        big_text(im,"BLISTERING",14,(220,40,40),scale=2,cx=138+jj,outline=INK)
        big_text(im,"BARNACLES!",32,(220,40,40),scale=2,cx=138+jj,outline=INK)
    FX['wd_border'](d,im,('wd_border',),f)
    if t<0.05: zoom_lines(d,INK)
    return im

# ---- the clip -----------------------------------------------------------------------------------------
def clip_wednesday(f):
    s=scene(f,THEME)
    sway=int(round(math.sin(2*math.pi*f/48)))                          # he isn't quite steady
    hpose='guard'; level=0.8; pint=(BEER,TOP); sniff=False
    # 1) a long pull at the pint
    if 14<=f<44:
        p=min(1,(f-14)/8) if f<36 else max(0,1-(f-36)/8)
        pint=(lerp(BEER,HX+16,p),lerp(TOP,44,p)); hpose='charge' if p>0.2 else 'guard'
        level=0.8-0.3*min(1,max(0,(f-22)/14))
    if 44<=f<240: level=0.5
    if 30<=f<62: s['fx'].append(('dmg',"HIC",HX+14,22,(60,40,30)))
    if 62<=f<108: s['fx'].append(('wd_balloon',"WHAT A WEEK, HUH?",70,3,(HX+6,26)))
    if 108<=f<154: s['fx'].append(('wd_balloon',"CAPTAIN, IT'S WEDNESDAY",6,14,(TX+4,28)))
    # 2) close-up
    if 154<=f<214: s['image']=closeup_haddock((f-154)/60,f); return s
    # 3) Snowy at the beer; the Captain takes it back
    if 214<=f<246: sniff=True; level=0.5-0.2*(f-214)/32
    if 246<=f<258: p=(f-246)/12; pint=(lerp(BEER,BEER-6,p),TOP); hpose='charge'; level=0.3
    if 258<=f<288: level=0.3+0.5*(f-258)/30                             # topped up for the loop
    s['actors']=[actor(TINTIN2,TX,y=GROUND+2,flip=True,pal=TPAL),actor(BIG[hpose],HX+sway,y=GROUND+1,pal=HPAL),
                 actor(SNOWY,SNX,y=TOP+(2 if sniff else 0),flip=True,pal={'W':(250,250,250),'K':INK})]
    if sniff: s['fx'].append(('wd_sweat',SNX-2,TOP-14))
    s['fx'].append(('wd_counter',))
    s['fx'].append(('wd_pint',pint[0],pint[1],level))
    s['fx'].append(('wd_border',))
    return s

@fx('wd_counter')
def _fx_counter(d,im,e,f):
    """The front of the bar, over the two of them: they are leaning on it."""
    d.rectangle([0,TOP,W,H],fill=BAR); d.line([0,TOP,W,TOP],fill=INK); d.rectangle([0,TOP+1,W,TOP+2],fill=(150,96,54))
    for x in range(12,W,30): d.line([x,TOP+3,x+4,H],fill=BAR_D)

CLIPS = [clip('wednesday', N_, clip_wednesday)]
