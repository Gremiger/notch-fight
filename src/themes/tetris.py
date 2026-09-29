"""Tetris: Claude (in an ushanka) vs the falling tetrominoes, on an NES/Game Boy playfield with the
SCORE / LINES / NEXT HUD and the Kremlin and St. Basil's onion domes behind him. The pieces fall
faster and faster and the stack climbs toward the top; Claude jumps and punches / kicks each one to
rotate it and slot it into place, always keeping the leftmost column open. The long I piece finally
comes up NEXT — close-up: FINALLY! — Claude kicks it straight down the well: TETRIS! Four lines
blink and vanish, the stack collapses, and the Game Boy ending plays: the rocket lifts off from
behind the Kremlin wall. The HUD resets and the playfield is back to its frame-0 state."""
from engine import *

THEME = 'tetris'
N_ = 312
CX = 34                                                             # Claude's spot in the neutral pose

# ---- the playfield ---------------------------------------------------------------------------
BS = 6                                                              # block size (art px)
COLS, ROWS = 10, 9
WX = 66                                                             # interior left edge of the well
def cell_xy(c,r): return WX+c*BS, GROUND-(r+1)*BS

TC = {'I':(0,214,230),'O':(240,208,0),'T':(168,64,210),'S':(64,200,72),'Z':(230,52,52),
      'J':(44,92,232),'L':(244,140,24)}                              # the 7 classic colours

def block(d,x,y,c,s=BS):
    """A bevelled block: light top-left edge, dark bottom-right edge, a shine pixel."""
    hi=tuple(min(255,v+(255-v)//2) for v in c); lo=tuple(int(v*0.5) for v in c)
    d.rectangle([x,y,x+s-1,y+s-1],fill=c)
    d.line([x,y,x+s-1,y],fill=hi); d.line([x,y,x,y+s-1],fill=hi)
    d.line([x+s-1,y+1,x+s-1,y+s-1],fill=lo); d.line([x+1,y+s-1,x+s-1,y+s-1],fill=lo)
    if s>=5: d.point((x+1,y+1),fill=(255,255,255))

# The 9 pieces that build rows 0-3 (full except column 0) plus rows 4-5, which are an exact copy of
# the frame-0 rows 0-1: after the TETRIS clears rows 0-3, rows 4-5 fall into their place and the
# field is back to its frame-0 state. (kind, target cells (col,row)), in drop order (each one lands
# supported and falls through empty cells).
PIECES=[
 ('L',[(1,1),(1,2),(2,2),(3,2)]), ('T',[(4,1),(4,2),(4,3),(5,2)]), ('T',[(6,2),(7,2),(7,3),(8,2)]),
 ('S',[(8,3),(8,4),(9,2),(9,3)]), ('O',[(1,3),(1,4),(2,3),(2,4)]), ('L',[(2,5),(3,3),(3,4),(3,5)]),
 ('Z',[(4,4),(5,3),(5,4),(6,3)]), ('Z',[(5,5),(6,4),(6,5),(7,4)]), ('J',[(7,5),(8,5),(9,4),(9,5)]),
]
I_CELLS=[(0,0),(0,1),(0,2),(0,3)]

def _base():
    """Frame-0 rows 0-1: the colours of rows 4-5 once every piece has landed."""
    top={}
    for k,cs in PIECES:
        for c,r in cs:
            if r>=4: top[(c,r-4)]=TC[k]
    return top
BASE=_base()

def _check():
    filled=set(BASE)
    for k,cs in PIECES:
        assert not filled&set(cs), k
        assert any(r==0 or (c,r-1) in filled for c,r in cs), k
        assert all((c,rr) not in filled for c,r in cs for rr in range(r+1,ROWS)), k
        filled|=set(cs)
    assert all((c,r) in filled for c in range(1,COLS) for r in range(4)) and not any((0,r) in filled for r in range(ROWS))
    assert {(c,r-4) for c,r in filled if r>=4}==set(BASE)
_check()

def _norm(cs):
    mx=min(c for c,_ in cs); my=min(r for _,r in cs); return [(c-mx,r-my) for c,r in cs]
def _rot(cs): return _norm([(r,-c) for c,r in cs])                  # 90 degrees clockwise

# timing: (spawn, land) — every piece falls faster than the last
FALLS=[28,24,20,17,14,12,10,8,7]
TIMES=[]; _t=14
for n in FALLS: TIMES.append((_t,_t+n)); _t+=n+2
I_SPAWN, I_HIT, I_LAND = 208, 214, 219
BLINK0, VANISH0, COLLAPSE0 = 222, 238, 246
SPAWN_COL, SPAWN_ROW = 4, 8

def spawn_shape(i):
    k,cs=PIECES[i]; return _rot(_norm(cs)) if k!='O' else _norm(cs)

def piece_state(i,f):
    """(kind, cells) of falling piece i at frame f, or None when not falling. It spawns rotated at the
    top centre; Claude's hit at 40% of the fall snaps it to its final rotation and slides it over."""
    k,cs=PIECES[i]; t0,t1=TIMES[i]
    if not t0<=f<t1: return None
    tgt=_norm(cs); sp=spawn_shape(i)
    th=t0+int((t1-t0)*0.4)
    tc=min(c for c,_ in cs); tr=min(r for _,r in cs)
    shape=sp if f<th else tgt
    col=SPAWN_COL if f<th else int(round(lerp(SPAWN_COL,tc,(f-th+1)/3)))
    top=SPAWN_ROW-max(r for _,r in shape)
    row=int(lerp(top,tr,(f-t0)/(t1-t0-1)))                         # whole-row steps, like the game
    return k,[(col+c,row+r) for c,r in shape]

def field(f):
    """{(col,row): colour} of the settled stack at frame f."""
    g=dict(BASE)
    for (k,cs),(t0,t1) in zip(PIECES,TIMES):
        if f>=t1:
            for c in cs: g[c]=TC[k]
    if f>=I_LAND:
        for c in I_CELLS: g[c]=TC['I']
    if f>=VANISH0+6:
        g={(c,r):v for (c,r),v in g.items() if r>=4}
        drop=min(4,max(0,(f-COLLAPSE0)//2+1)) if f>=COLLAPSE0 else 0
        g={(c,r-drop):v for (c,r),v in g.items()}
    return g

def danger(f):
    """The stack is high: from the 6th piece until the TETRIS."""
    return TIMES[5][1]<=f<VANISH0

# ---- text: the engine's 3x5 font, with a 4-wide N (the shared one reads as a lowercase n) ----------
_WIDE={'N':["1001","1101","1011","1001","1001"]}
def _glyph(ch):
    if ch in _WIDE: return _WIDE[ch]
    b=FONT.get(ch,FONT[' ']); return [b[i*3:i*3+3] for i in range(5)]
def text_w(txt): return sum(len(_glyph(ch)[0])+1 for ch in txt)-1
def ttext(d,txt,x,y,c,shadow=None):
    for ch in txt:
        g=_glyph(ch)
        for j,row in enumerate(g):
            for i,b in enumerate(row):
                if b=='1':
                    if shadow: d.point((x+i+1,y+j+1),fill=shadow)
                    d.point((x+i,y+j),fill=c)
        x+=len(g[0])+1
def big_ttext(im,txt,y,c,scale=2,cx=W//2,outline=None,shadow=(0,0,0)):
    m=Image.new('L',(text_w(txt),5),0); ttext(ImageDraw.Draw(m),txt,0,0,255)
    m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        if shadow is not None: im.paste(shadow,(x+2,y+2),m)
    elif shadow is not None: im.paste(shadow,(x+1,y+1),m)
    im.paste(c,(x,y),m)

# ---- sprites ---------------------------------------------------------------------------------
USHANKA=["..qqqqqq..",".qqqqqqqq.","FFFFYFFFFF"]
KICK=S([
"...OOOOOOOO......",
"...OOOOOOOO......",
"...OOOOKOOK......",
"...OOOOKOOK......",
"...OOOOOOOO......",
".ooOOOOOOOO......",
"ooOOOOOOOOO......",
"...OOOOOOOO......",
"...oOOOOOOoooooOO",
"..oo.......oooOO.",
".oo..............",])
def _dress(spr):
    s=overlay(spr,USHANKA,-1,0)
    top,l,r=body_box(s)                                              # ear flaps down the sides
    return paint(s,[(l-1,top,'F'),(l-1,top+1,'F'),(l-1,top+2,'F'),(r+1,top,'F'),(r+1,top+1,'F')],grow=True)
CLT={k:_dress(v) for k,v in list(CL.items())+[('kick',KICK)]}
CLPAL={'q':(96,64,40),'F':(170,130,90),'Y':(236,40,40)}

# ---- background: the Kremlin at night + the well + the HUD panel ---------------------------------
WALL_Y = 47
def _onion(d,x,y,r,c,stripe):
    """An onion dome: a bulb of radius r with a pointed tip, striped."""
    d.ellipse([x-r,y-r,x+r,y+r],fill=c)
    d.polygon([(x-r+1,y-1),(x+r-1,y-1),(x,y-r-4)],fill=c)
    for k in range(-r,r+1,2): d.line([x+k,y+r-1,x+k//2,y-r-1],fill=stripe)
    d.line([x,y-r-7,x,y-r-4],fill=(120,110,70)); d.point((x-1,y-r-6),fill=(120,110,70)); d.point((x+1,y-r-6),fill=(120,110,70))

def _kremlin(d):
    for y in range(GROUND):                                          # night sky
        k=y/GROUND; d.line([0,y,W,y],fill=(int(6+10*k),int(8+10*k),int(26+16*k)))
    rr=random.Random(1984)
    for _ in range(30): d.point((rr.randint(0,60),rr.randint(0,30)),fill=(80,80,120))
    # St. Basil's: the tent spire and the domes
    d.polygon([(19,22),(25,22),(22,6)],fill=(70,40,40)); d.rectangle([19,22,25,WALL_Y],fill=(66,36,34))
    for x,y,r,c,s in ((10,30,4,(40,90,70),(80,150,110)),(22,24,3,(110,90,40),(170,140,60)),
                      (32,30,4,(90,40,60),(150,70,90)),(16,34,3,(40,60,110),(90,110,170)),(28,35,3,(100,50,40),(160,90,60))):
        d.rectangle([x-r+1,y+r-1,x+r-1,WALL_Y],fill=(60,32,32)); _onion(d,x,y,r,c,s)
    # the Spasskaya tower with its red star
    d.rectangle([44,26,52,WALL_Y],fill=(84,30,28)); d.rectangle([45,20,51,26],fill=(90,34,30))
    d.rectangle([46,23,50,25],fill=(210,190,120)); d.point((48,24),fill=(40,30,30))   # the clock
    d.polygon([(45,20),(51,20),(48,9)],fill=(46,60,52))
    for p in ((48,5),(47,6),(48,6),(49,6),(46,7),(47,7),(48,7),(49,7),(50,7),(47,8),(49,8)): d.point(p,fill=(230,40,40))
    # the wall with its swallowtail merlons
    d.rectangle([0,WALL_Y,61,GROUND],fill=(72,26,24))
    for x in range(0,61,5): d.rectangle([x,WALL_Y-3,x+2,WALL_Y-1],fill=(72,26,24)); d.point((x+1,WALL_Y-3),fill=(12,12,30))
    for y in range(WALL_Y+2,GROUND,3): d.line([0,y,61,y],fill=(58,20,20))
    # the well: grey brick walls, dark interior
    for x0 in (62,126):
        for y in range(0,GROUND+1,3):
            d.rectangle([x0,y,x0+3,y+2],fill=(120,120,132)); d.line([x0,y+2,x0+3,y+2],fill=(70,70,82))
            d.point((x0+(0 if (y//3)%2 else 2),y),fill=(160,160,172))
    d.rectangle([WX,0,WX+COLS*BS-1,GROUND-1],fill=(10,10,20))
    for c in range(1,COLS):
        for r in range(ROWS):
            x,y=cell_xy(c,r); d.point((x,y),fill=(24,24,40))
    d.rectangle([62,GROUND,129,GROUND],fill=(120,120,132))
    # the HUD panel
    d.rectangle([131,0,W-1,GROUND],fill=(16,16,30)); d.rectangle([132,1,W-2,GROUND-1],outline=(70,70,100))
    for y,label in ((3,"SCORE"),(19,"LINES"),(35,"NEXT")): ttext(d,label,HX-text_w(label)//2,y,(170,170,200))
    d.rectangle([142,41,174,56],fill=(6,6,14),outline=(110,110,140))
HX = 158                                                            # HUD centre
register_bg(THEME, lambda v: (v//2+10,v//2+10,v+20), decor=_kremlin)

# ---- effects ---------------------------------------------------------------------------------
@fx('tetris_field')
def _fx_field(d,im,e,f):
    """The stack + the falling piece; the 4 cleared rows blink white, then vanish from the middle out."""
    _,g,fall=e
    for (c,r),col in g.items():
        if r>=ROWS: continue
        x,y=cell_xy(c,r)
        if r<4 and BLINK0<=f<VANISH0 and (f-BLINK0)//4%2==0: block(d,x,y,(236,236,244)); continue
        if r<4 and VANISH0<=f<VANISH0+6 and abs(c-4.5)<(f-VANISH0+1)*1: continue
        block(d,x,y,col)
    if fall:
        k,cs=fall
        for c,r in cs:
            if r<ROWS: x,y=cell_xy(c,r); block(d,x,y,TC[k])

@fx('tetris_danger')
def _fx_danger(d,im,e,f):
    """A red pulse over the well walls while the stack is high."""
    a=0.35+0.25*math.sin(f*0.8)
    px=im.load()
    for x0 in (62,126):
        for y in range(0,GROUND):
            for x in range(x0,x0+4): blend(px,x,y,(230,40,40),a)

@fx('tetris_hud')
def _fx_hud(d,im,e,f):
    _,score,lines,nxt,blink=e
    if not blink:
        text(d,f"{score:06d}",HX-12,10,(255,255,255),shadow=None); text(d,f"{lines:03d}",HX-6,26,(255,255,255),shadow=None)
    k=PIECES[nxt][0] if nxt>=0 else 'I'
    cs=spawn_shape(nxt) if nxt>=0 else [(0,0),(1,0),(2,0),(3,0)]
    w=max(c for c,_ in cs)+1; h=max(r for _,r in cs)+1; s=4
    x0=HX-w*s//2; y0=49-h*s//2
    for c,r in cs: block(d,x0+c*s,y0+(h-1-r)*s,TC[k],s=s)
    if nxt<0 and (f//3)%2==0: d.rectangle([142,41,174,56],outline=(120,255,255))

@fx('tetris_wave')
def _fx_wave(d,im,e,f):
    """Claude's punch/kick shockwave flying from (x0,y0) to the piece at (x1,y1), p 0..1."""
    _,x0,y0,x1,y1,p=e
    x=lerp(x0,x1,p); y=lerp(y0,y1,p); xt=lerp(x0,x1,max(0,p-0.35)); yt=lerp(y0,y1,max(0,p-0.35))
    d.line([xt,yt,x,y],fill=(255,230,150)); d.line([xt,yt+1,x,y+1],fill=(200,120,60))
    d.arc([x-3,y-4,x+3,y+4],-70,70,fill=(255,255,255))

@fx('tetris_trail')
def _fx_trail(d,im,e,f):
    """Speed streaks above the hard-dropped I piece."""
    _,c,r0,r1=e
    x,_=cell_xy(c,0)
    for k in range(r0,r1):
        _,y=cell_xy(c,k); a=0.5*(1-(k-r0)/max(1,r1-r0))
        for yy in range(y,y+BS):
            for xx in (x+1,x+3): blend(im.load(),xx,yy,(160,250,255),a)

@fx('tetris_pop')
def _fx_pop(d,im,e,f):
    _,txt,y,c,scale,cx,ol=e; big_ttext(im,txt,int(y),c,scale=scale,cx=int(cx),outline=ol)

ROCKET=S([
"...w...",
"..www..",
"..wWw..",
".wwkww.",
".wwwww.",
".wWwww.",
".wwwww.",
".wrrrw.",
".wwwww.",
".wWwww.",
".wwwww.",
"rwwwwwr",
"rrwwwrr",
"r.ddd.r",])
RKPAL={'w':(230,230,236),'W':(255,255,255),'k':(40,70,140),'r':(210,40,40),'d':(90,90,100)}
RK_X = 14

@fx('tetris_rocket')
def _fx_rocket(d,im,e,f):
    """The Game Boy ending: the rocket rises from behind the Kremlin wall (hidden below WALL_Y-3)
    on a flickering flame, smoke billowing at the launch line."""
    _,feet,smoke=e
    feet=int(feet); rr=random.Random(f)
    for i in range(int(14*smoke)):                                   # smoke at the wall
        x=RK_X+rr.randint(-14,14); y=WALL_Y-3-rr.randint(0,4); r=rr.randint(2,4)
        d.ellipse([x-r,y-r,x+r,y+r],fill=(150,150,160) if i%2 else (110,110,122))
    top=im.copy(); td=ImageDraw.Draw(top)                          # drawn apart, pasted above the wall only
    fl=5+rr.randint(0,4)
    td.polygon([(RK_X-2,feet),(RK_X+3,feet),(RK_X+0.5,feet+fl)],fill=(255,160,40)); td.line([RK_X,feet,RK_X,feet+fl-3],fill=(255,245,180))
    draw(top,ROCKET,RK_X+0.5,feet,False,pal=RKPAL)
    im.paste(top.crop((0,0,W,WALL_Y-3)),(0,0))

# ---- close-up --------------------------------------------------------------------------------
def closeup_ipiece(t,f):
    """Primer plano: the NEXT box, huge — the long I piece slides in, glowing; Claude's eyes light up
    cyan. FINALLY!"""
    im=Image.new('RGB',(W,H),(8,8,20)); d=ImageDraw.Draw(im)
    for y in range(0,H,4): d.line([0,y,W,y],fill=(12,12,28))
    # Claude's face (under the ushanka) on the left
    d.rectangle([6,18,62,H],fill=(217,119,87)); d.rectangle([6,18,11,H],fill=(176,92,66))
    d.rectangle([4,0,64,8],fill=(96,64,40)); d.rectangle([2,8,66,18],fill=(170,130,90))    # the ushanka
    d.rectangle([0,14,8,40],fill=(170,130,90)); d.rectangle([60,14,68,40],fill=(170,130,90))
    for p in ((34,9),(33,10),(34,10),(35,10),(32,11),(33,11),(34,11),(35,11),(36,11),(33,12),(35,12)): d.point(p,fill=(230,40,40))
    g=ease((t-0.3)/0.2)
    for ex in (28,46):
        d.rectangle([ex,26,ex+5,40],fill=(24,14,12))
        if g>0:
            c=tuple(int(lerp(24,v,g)) for v in (0,214,230)); d.rectangle([ex+1,28,ex+4,38],fill=c)
            d.rectangle([ex+1,28,ex+2,31],fill=tuple(int(lerp(24,255,g)) for _ in range(3)))
    # the NEXT box
    d.rectangle([82,4,180,44],fill=(4,4,12),outline=(110,110,140)); d.rectangle([83,5,179,43],outline=(50,50,80))
    big_ttext(im,"NEXT",8,(170,170,200),cx=131,shadow=None)
    y=int(ez(-20,24,t/0.3))
    glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).rectangle([100,y-3,162,y+15],fill=int(170*ease((t-0.2)/0.2)))
    im.paste((0,160,200),(0,0),glow.filter(ImageFilter.GaussianBlur(4))); d=ImageDraw.Draw(im)
    for i in range(4): block(d,103+i*14,y,TC['I'],s=14)
    if t>0.35:
        rr=random.Random(f//2)
        for _ in range(4): spark(d,rr.randint(96,168),rr.randint(12,40),2,(160,250,255))
    if t>0.5:
        jx=(f%3)-1 if t<0.62 else 0
        big_ttext(im,"FINALLY!",49,(255,236,120),cx=128+jx,outline=(150,60,20))
    if t<0.08: zoom_lines(d,(120,220,255))
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

# ---- the clip --------------------------------------------------------------------------------
def _fist(cl):
    """World point in front of Claude's fist / foot (the wave's origin)."""
    return cl['x']+9, cl['y']-(3 if cl['spr'] is CLT['kick'] else 6)

def clip_tetris(f):
    s=scene(f,THEME)
    cl=actor(CLT[guard_pose(f)],CX,pal=CLPAL)
    fall=None; nxt=0; score=0; lines=0; hud_blink=False
    # 1) the pieces fall, faster and faster; Claude jumps and hits each one into place
    for i,(t0,t1) in enumerate(TIMES):
        st=piece_state(i,f)
        if st: fall=st
        if t0<=f<t1: nxt=i+1 if i+1<len(PIECES) else -1
        th=t0+int((t1-t0)*0.4); j=f-(th-5)
        if 0<=j<9:                                                   # the jump + the hit
            kick=i%2==1; ph=math.sin(math.pi*j/9)
            cl.update(x=CX+6*ph,y=GROUND-int(16*ph),spr=CLT['kick' if kick else 'punch'] if 3<=j<7 else CLT['armsup' if j<3 else 'guard2'])
            if 3<=j<6:
                k,cs=piece_state(i,th) if piece_state(i,th) else PIECES[i]
                cx_=sum(cell_xy(c,r)[0] for c,r in cs)/4+3; cy_=sum(cell_xy(c,r)[1] for c,r in cs)/4+3
                x0,y0=_fist(cl); s['fx'].append(('tetris_wave',x0,y0,cx_,cy_,(j-3)/2))
                if j==5: s['fx'].append(('spark',int(cx_),int(cy_),3)); s['shake']=rshake()
    if f>=TIMES[-1][0]: nxt=-1
    # the stack is high: Claude flinches as the fast pieces slam down
    if danger(f): s['under'].append(('tetris_danger',))
    for t1 in (TIMES[6][1],TIMES[7][1],TIMES[8][1]):
        if t1<=f<t1+3: s['shake']=rshake()
    if TIMES[7][1]<=f<TIMES[7][1]+6: cl.update(spr=CLT['hurt'],x=CX-2)
    # 2) close-up: the I piece is NEXT — FINALLY!
    if 172<=f<208: s['image']=closeup_ipiece((f-172)/36,f); return s
    # 3) the I piece spawns flat; Claude's jump kick stands it up and sends it down the well
    if f>=TIMES[-1][1]: nxt=0 if f>=I_SPAWN else -1
    if I_SPAWN<=f<I_LAND:
        if f<I_HIT: fall=('I',[(3+c,8) for c in range(4)])
        else:
            r0=int(lerp(5,0,(f-I_HIT)/(I_LAND-I_HIT-1))); fall=('I',[(0,r0+k) for k in range(4)])
            s['under'].append(('tetris_trail',0,r0+4,ROWS))
        j=f-(I_HIT-6)
        if 0<=j<10:
            ph=math.sin(math.pi*j/10)
            cl.update(x=CX+14*ph,y=GROUND-int(30*ph),spr=CLT['kick'] if 4<=j<8 else CLT['armsup'])
            if 4<=j<6:
                x0,y0=_fist(cl); s['fx'].append(('tetris_wave',x0,y0,cell_xy(3,8)[0]+2,cell_xy(3,8)[1]+3,(j-4)/1.5))
            if j==6: s['fx'].append(('spark',cell_xy(3,8)[0]+2,cell_xy(3,8)[1]+3,4)); s['shake']=rshake(2)
    if I_LAND<=f<I_LAND+4:
        s['shake']=rshake(2); s['flash']=0.4 if f==I_LAND else 0; s['fc']=(69,GROUND-12); s['flashc']=(170,250,255)
    # 4) TETRIS! the lines blink and vanish, the stack collapses
    if f>=I_LAND+8: lines=min(4,max(0,(f-VANISH0)//2+1)); score=lines*300 if f<VANISH0+12 else 1200
    if I_LAND<=f<262:
        jx=(f%3)-1 if f<I_LAND+8 else 0
        y=int(ez(-18,14,(f-I_LAND)/6))
        s['fx'].append(('tetris_pop',"TETRIS!",y,(255,236,120) if (f//3)%2 else (120,250,255),3,96+jx,(40,40,120)))
    if I_LAND<=f<252: cl.update(spr=CLT['armsup'] if (f//6)%2==0 else CLT['guard'],x=CX,y=GROUND-(2 if (f//6)%2==0 else 0))
    if 246<=f<262 and f%2==0: s['fx'].append(('dust',WX+random.randint(4,56),GROUND-random.randint(1,14)))
    # 5) the Game Boy ending: the rocket launches from behind the Kremlin
    if 252<=f<300:
        t=(f-252)/48
        feet=WALL_Y-3+18-ease(min(1,t/0.35))*16-max(0,t-0.35)**2*220
        s['under'].append(('tetris_rocket',feet,max(0,1-t*1.4)))
        if f<272: s['shake']=rshake() if f%2 else (0,0)
        cl.update(spr=CLT['armsup'] if (f//4)%2==0 else CLT['guard'],x=CX,y=GROUND-(3 if (f//4)%2==0 else 0))
        if 276<=f<300 and f%4==0:
            rr=random.Random(f); s['fx'].append(('spark',rr.randint(4,56),rr.randint(4,26),2,(255,230,120)))
    # 6) the HUD resets for the next game
    if f>=292: score=lines=0; hud_blink=f<300 and (f//2)%2==0
    if f>=300: cl.update(spr=CLT[guard_pose(f)],x=CX,y=GROUND)
    s['under'].insert(0,('tetris_field',field(f),fall))
    s['fx'].append(('tetris_hud',score,lines,nxt,hud_blink))
    s['actors']=[cl]
    return s

CLIPS = [clip('tetris', N_, clip_tetris)]
