"""Meme boss rush: Claude fights his way through three internet memes on a vaporwave stage.
BOSS 1, Forever Alone (the rage-comic face: squashed forehead, huge dimpled chin, tears) cries and
flails — Claude gives him a hug and he vanishes happy (NEW FRIEND!). BOSS 2, Tung Tung Tung Sahur
(the wooden log with a baseball bat) hops in chanting TUNG TUNG TUNG... SAHUR!, bonks Claude three
times and gets uppercut into orbit. WARNING — FINAL BOSS: the "6 7" (six seven), a giant pair of
numerals doing the palms-up weighing gesture. Close-up (6-7!), it throws 6s and 7s, Claude jumps
them, charges, combos and blasts it apart. MEME DEFEATED, deal-with-it shades, back to guard."""
from engine import *

THEME = 'memes'
N_ = 432
CX = 30                                                            # Claude's spot in the neutral pose

# ---- background: a dim vaporwave stage ---------------------------------------------------------
HORIZON = 45
def _stage(d):
    for y in range(HORIZON):                                        # night sky, warmer at the horizon
        k=y/HORIZON; d.line([0,y,W,y],fill=(int(8+22*k),int(4+4*k),int(20+22*k)))
    rr=random.Random(67)
    for _ in range(26): d.point((rr.randint(0,W-1),rr.randint(0,30)),fill=(70,60,110))
    cx,r=92,17                                                      # the striped sun
    for y in range(HORIZON-r,HORIZON):
        if y>HORIZON-9 and (HORIZON-y)%3==0: continue
        k=(y-(HORIZON-r))/r; w=int(math.sqrt(max(0,r*r-(HORIZON-y)**2)))
        d.line([cx-w,y,cx+w,y],fill=(int(120-40*k),int(70-50*k),int(50+30*k)))
    d.rectangle([0,HORIZON,W,GROUND],fill=(14,6,26))                # the grid floor
    for x0 in range(-260,W+280,26): d.line([cx+(x0-cx)*0.18,HORIZON,x0,GROUND],fill=(52,18,70))
    for y in (HORIZON+2,HORIZON+5,HORIZON+9,HORIZON+13): d.line([0,y,W,y],fill=(52,18,70))
    d.line([0,HORIZON,W,HORIZON],fill=(120,40,120))
register_bg(THEME, lambda v: (v+20,v//3+6,v+36), decor=_stage, clip_ground=True)

# ---- boss 1: Forever Alone ---------------------------------------------------------------------
_FA_HEAD=[
"......kkkkkkkkk......",
"....kkWWWWWWWWWkk....",
"...kWWkkkWWWkkkWWk...",
"...kWWWWWWWWWWWWWk...",
"..kWWkkkWWWWWkkkWWk..",
"..kWkWWkkWWWkkWWkWk..",
"..kWWkkWWWWWWWkkWWk..",
".kWWWTWWWWWWWWWTWWWk.",
".kWWWTWWWWkWWWWTWWWk.",
"kWWWWTWWWWkkWWWTWWWWk",
"kWWWWTWWWWWWWWWTWWWWk",
"kWkkkTkkkkkkkkkTkkkWk",
"kWkWWTWWWWWWWWWTWWkWk",
"kWWkkkkkkkkkkkkkkkWWk",
"kWWWkWWWWWWWWWWWkWWWk",
"kWWWWkkkkkkkkkkkWWWWk",
"kWWWWWWWWWWWWWWWWWWWk",
"kWWWWWWWWWkWWWWWWWWWk",
".kWWWWWWWWkWWWWWWWWk.",
"..kkWWWWWWWWWWWWWkk..",
"....kkkkkkkkkkkkk....",]
_FA_ARMS={                                                          # rows 1-3 of the stick torso
 'down':["......lll......", ".....l.l.l.....", "....l..l..l...."],
 'up':  ["....l..l..l....", ".....l.l.l.....", "......lll......"],
 'slapA':["..lll.lll......", ".......l.l.....", ".......l..l...."],
 'slapB':["......lll.lll..", ".....l.l.......", "....l..l......."],
 'hug': ["..llllllllll...", ".......l.......", ".......l......."],
}
_FA_LEGS=[[".......l.l.......","......l...l......",".....l.....l....."],
          [".......ll........","......l.l........","......l..l......."]]
def _fa(arms='down',legs=0,happy=False):
    head=[r.replace('T','W') for r in _FA_HEAD] if happy else list(_FA_HEAD)
    if happy:                                                       # tears gone, a real smile + blush
        head[10]="kWnnWWWWWWWWWWWWnnWk"; head[11]="kWWWWWWWWWWWWWWWWWWWk"; head[12]="kWkWWWWWWWWWWWWWWWkWk"
        head[13]="kWWkkWWWWWWWWWWWkkWWk"; head[14]="kWWWWkkkkkkkkkkkWWWWk"; head[15]="kWWWWWWWWWWWWWWWWWWWk"
    body=["..........l.........."]+["...."+a+".." for a in _FA_ARMS[arms]]+["..........l..........","..........l.........."]+[".."+l+".." for l in _FA_LEGS[legs]]
    return S(head+body)
FAPAL={'W':(236,236,232),'k':(34,34,40),'T':(110,190,255),'l':(214,214,220),'n':(250,150,170)}
FA_R=21                                                            # rows of the head

# ---- boss 2: Tung Tung Tung Sahur ------------------------------------------------------------
_LOG=[
"....cccccccc....",
"...cCCCCCCCCc...",
"..AAccccccccAA..",
"..AAAAAAAAAAAA..",
"..AAkkkAAkkkAA..",
"..AAAAAAAAAAAA..",
"..AeeeAAAeeeAA..",
"..AeekAAAeekAA..",
"..AeeeAAAeeeAA..",
"..AAAAAaaAAAAA..",
"..AAAAAaaAAAAA..",
"..AAAAAAAAAAAA..",
"..AkAAAAAAAAkA..",
"..AAkmmmmmmkAA..",
"..AAAkkkkkkAAA..",
"..AAAAAAAAAAAA..",
"..AaAAAAAAAaAA..",
"..AAAAaAAAAAAA..",
"..AAAAAAAAaAAA..",
"..AaAAAAAAAAAA..",
"..AAAAAaAAAAaA..",
"..AAAAAAAAAAAA..",
"..AAaAAAAAAAAA..",
"...AAAAAAAAAA...",
"....s.....s.....",
"....s.....s.....",
"....s.....s.....",
"...ss....ss.....",]
_BACK_ARM=[(1,13,'s'),(1,14,'s'),(0,15,'s'),(0,16,'s'),(0,17,'s')]
def _cells(x0,y0,x1,y1,ch):
    n=max(abs(x1-x0),abs(y1-y0))
    return [(round(lerp(x0,x1,i/n)),round(lerp(y0,y1,i/n)),ch) for i in range(n+1)]
def _bat(x0,y0,x1,y1):
    """A baseball bat from the grip (x0,y0) to the tip: the far half is thicker (the barrel)."""
    cs=_cells(x0,y0,x1,y1,'b'); n=len(cs); horiz=abs(x1-x0)>=abs(y1-y0)
    thick=[(x,y+dy,'b') if horiz else (x+1,y,'b') for i,(x,y,_) in enumerate(cs) if i>n*0.45 for dy in ((-1,1) if horiz else (0,))]
    return cs+thick
TUNG={
 'idle':  paint(S(_LOG),_BACK_ARM+[(14,13,'s'),(15,14,'s')]+_bat(16,15,16,0),grow=True),
 'raise': paint(S(_LOG),_BACK_ARM+[(14,12,'s'),(14,11,'s')]+_bat(14,10,5,-6),grow=True),
 'swing': paint(S(_LOG),_BACK_ARM+[(14,14,'ss')]+_bat(16,14,31,14),grow=True),
}
TUNG['hurt']=hurt(TUNG['idle'])
TUNG['hop']=S(TUNG['idle'][:-4]+TUNG['idle'][-2:])                 # legs tucked
TUNGPAL={'A':(150,98,56),'C':(226,184,128),'a':(100,62,34),'c':(204,158,106),'e':(245,245,240),'k':(20,14,10),'m':(120,20,24),
         's':(196,146,96),'b':(214,158,92)}

# ---- the final boss: "6 7" -----------------------------------------------------------------------
_D6=[".###.","#....","#....","####.","#...#","#...#",".###."]
_D7=["#####","....#","...#.","...#.","..#..","..#..","..#.."]
SC=5; NW,NH=25,35; BW,BH=74,44; X6,X7=8,41
def _numeral(bits,c):
    """Scale a 5x7 digit by SC, shading: light on top edges, dark on bottom edges."""
    on=lambda x,y: 0<=y<NH and 0<=x<NW and bits[y//SC][x//SC]=='#'
    g=[['.']*NW for _ in range(NH)]
    for y in range(NH):
        for x in range(NW):
            if on(x,y): g[y][x]=c[1] if not on(x,y-1) or not on(x-1,y) else (c[2] if not on(x,y+1) or not on(x+1,y) else c[0])
    return g
def _boss(ph,shout=False,hurt_=False):
    """The 6-7 pair; ph in -1..1: the 6's hand goes up while the 7's goes down (the weighing gesture)."""
    g=[['.']*BW for _ in range(BH)]
    for key,bits,x0,dy in (('6',_D6,X6,-ph),('7',_D7,X7,ph)):
        top=4+round(1.5*dy); num=_numeral(bits,'FfG' if key=='6' else 'JjI')
        for y in range(NH):
            for x in range(NW):
                if num[y][x]!='.': g[top+y][x0+x]=num[y][x]
        put=lambda x,y,ch: 0<=x<BW and 0<=y<BH and g[y].__setitem__(x,ch)
        # face: eyes looking left (at Claude), angry brows, mouth
        ex=(7,13) if key=='6' else (5,11); my,mx=(16,6) if key=='6' else (11,15)
        for i,e0 in enumerate(ex):
            for yy in range(1,4):
                for xx in range(3): put(x0+e0+xx,top+yy,'W')
            put(x0+e0,top+2,'k'); put(x0+e0,top+3,'k') if hurt_ else None
            if hurt_: put(x0+e0+2,top+1,'k'); put(x0+e0+1,top+2,'k')
            put(x0+e0+(1 if i==0 else 0),top,'k'); put(x0+e0+(2 if i==0 else -1),top,'k')
        mw=8 if key=='6' else 4
        if shout or hurt_:
            for yy in range(3):
                for xx in range(mw): put(x0+mx+xx,top+my+yy,'k' if yy!=1 or xx in (0,mw-1) else 'r')
            for xx in range(1,mw-1,2): put(x0+mx+xx,top+my,'W')
        else:
            for xx in range(mw): put(x0+mx+xx,top+my+1,'k')
            put(x0+mx,top+my,'k'); put(x0+mx+mw-1,top+my,'k')
        # legs down to the feet (they stretch as the body bobs)
        legs=(7,16) if key=='6' else (9,14)
        for lx in legs:
            for y in range(top+NH,BH): put(x0+lx,y,'a'); put(x0+lx+1,y,'a')
            put(x0+lx-1,BH-1,'a'); put(x0+lx+2,BH-1,'a')
        # the arm and the palm-up hand, on the outer side
        if key=='6': sx,sy,hx,hy=x0,top+22,1,top+22+round(3*dy)
        else:        sx,sy,hx,hy=x0+NW-1,top+5,BW-6,top+11+round(3*dy)
        for x,y,_ in _cells(sx,sy,hx+2,hy,'a'): put(x,y,'a')
        for xx in range(5): put(hx+xx,hy,'H')
        put(hx,hy-1,'H'); put(hx+4,hy-1,'H'); put(hx+1,hy+1,'H'); put(hx+2,hy+1,'H'); put(hx+3,hy+1,'H')
    return S([''.join(r) for r in g])
BOSSPAL={'F':(222,52,78),'f':(255,128,140),'G':(140,22,48),'J':(40,150,245),'j':(130,210,255),'I':(20,70,160),
         'W':(250,250,250),'k':(16,10,20),'r':(200,30,40),'a':(40,30,54),'H':(250,250,250)}
BOSS_X=140
def gesture(f): return math.sin(2*math.pi*f/8)                     # 8-frame cycle: 4 up, 4 down

# ---- effects ---------------------------------------------------------------------------------
@fx('meme_bar')
def _fx_bar(d,im,e,f):
    """Boss-rush health bar at the top: name + bar (hp 0..1), grown in by prog 0..1."""
    _,name,hp,prog,c=e
    if prog<=0: return
    x0,x1,y=38,146,9; xe=int(lerp(x0,x1,ease(prog)))
    d.rectangle([x0-1,y-1,xe+1,y+3],fill=(10,6,16),outline=(200,190,220))
    w=int((xe-x0)*max(0,min(1,hp)))
    if w>0: d.rectangle([x0,y,x0+w,y+2],fill=c); d.line([x0,y,x0+w,y],fill=tuple(min(255,v+70) for v in c))
    if prog>=1: text(d,name,W//2-len(name)*2,2,(240,230,250),shadow=(20,10,30))

@fx('meme_pop')
def _fx_pop(d,im,e,f):
    """Scaled, outlined text (captions, chants, banners), centred at cx."""
    _,txt,y,c,scale,cx,ol=e; big_text(im,txt,int(y),c,scale=scale,cx=int(cx),outline=ol)

@fx('meme_tears')
def _fx_tears(d,im,e,f):
    """Forever Alone's tears: drops rolling off the chin line from both eyes."""
    _,x,top=e
    x=int(round(x))
    for k,dx in enumerate((-5,5)):
        for j in range(2):
            ph=(f*1.5+j*9+k*5)%18; yy=top+13+ph; xx=x+dx+(1 if k else -1)*(1+int(ph//5))
            if yy<GROUND-1: d.point((xx,int(yy)),fill=(150,210,255)); d.point((xx,int(yy)+1),fill=(90,160,240))

@fx('meme_heart')
def _fx_heart(d,im,e,f):
    _,x,y,c=e; x,y=int(x),int(y)
    for dy,row in enumerate([".r.r.","rrrrr",".rrr.","..r.."]):
        for dx,ch in enumerate(row):
            if ch=='r': d.point((x-2+dx,y+dy),fill=c)

@fx('meme_shades')
def _fx_shades(d,im,e,f):
    """Pixel "deal with it" shades over the eyes ('K' cells) of sprite spr at (cx,feet), dy above them."""
    _,spr,cx,feet,flip,dy=e
    ox,oy=origin(spr,cx,feet); w=len(spr[0])
    ks=[(ox+((w-1-x) if flip else x),oy+y) for y,r in enumerate(spr) for x,c in enumerate(r) if c=='K']
    if not ks: return
    exs=sorted({x for x,_ in ks}); y0=min(y for _,y in ks)+int(dy); ink=(8,8,10)
    d.line([exs[0]-3,y0,exs[-1]+2,y0],fill=ink)
    for ex in (exs[0],exs[-1]):                                     # the stepped 8-bit lenses
        d.line([ex-1,y0+1,ex+1,y0+1],fill=ink); d.line([ex-1,y0+2,ex,y0+2],fill=ink)
        d.point((ex-1,y0+1),fill=(240,240,255))

@fx('meme_warn')
def _fx_warn(d,im,e,f):
    """Flashing red WARNING band across the middle, hazard stripes, red edges."""
    _,a=e
    if a<=0 or (f//4)%2: return
    box=(0,22,W,38); im.paste(Image.blend(im.crop(box),Image.new('RGB',(W,16),(200,20,30)),0.6*a),box[:2])
    for x in range(-16,W+16,12):
        for y0 in (22,36): d.line([x+(f%12),y0,x+(f%12)+2,y0+1],fill=(255,200,60))
    for y in (0,1,62,63): d.line([0,y,W,y],fill=(200,20,30))
    big_text(im,"WARNING",25,(255,230,230),outline=(90,0,10))

@fx('meme_digit')
def _fx_digit(d,im,e,f):
    """A thrown numeral (the 6-7 boss' projectile) with speed lines behind it."""
    _,ch,x,y,c=e
    for k in (3,6,9): d.line([int(x)+4+k*2,int(y)+3+k%2*4,int(x)+8+k*3,int(y)+3+k%2*4],fill=tuple(v//2 for v in c))
    big_text(im,ch,int(y),c,scale=2,cx=int(x),outline=(20,10,30))

# ---- close-up --------------------------------------------------------------------------------
def closeup_67(t,f):
    """Primer plano: the 6-7 boss fills the screen, eyes glaring, hands weighing — SIX! SEVEN! 6-7!"""
    im=Image.new('RGB',(W,H),(14,4,20)); d=ImageDraw.Draw(im)
    for i in range(14):                                             # a red burst behind it
        a=i*2*math.pi/14+f*0.03; d.polygon([(W//2,H//2),(W//2+math.cos(a)*140,H//2+math.sin(a)*80),
                                            (W//2+math.cos(a+0.2)*140,H//2+math.sin(a+0.2)*80)],fill=(40,8,30))
    shout=t>0.3 and (f//3)%3!=0
    tmp=Image.new('RGB',(W,H),(1,2,3)); spr=_boss(gesture(f),shout=shout)
    draw(tmp,spr,W//2,BH,False,pal=BOSSPAL,aura=((255,60,90),1),f=f)
    ox=W//2-BW//2; crop=tmp.crop((ox-4,0,ox+BW+4,32)).resize(((BW+8)*2,64),Image.NEAREST)
    m=crop.point(lambda v: 255 if v>3 else 0).convert('L')
    jx=(f%3-1)*2 if shout else 0; zoom=ease(t/0.15)
    if zoom<1: crop=crop.resize((max(1,int(crop.width*(0.5+zoom/2))),max(1,int(64*(0.5+zoom/2)))),Image.NEAREST); m=m.resize(crop.size)
    im.paste(crop,(W//2-crop.width//2+jx,64-crop.height),m)
    if 0.3<t<0.55: big_text(im,"SIX!",2,(255,140,150),scale=2,cx=36,outline=(90,10,30))
    if 0.45<t<0.7: big_text(im,"SEVEN!",2,(140,210,255),scale=2,cx=W-40,outline=(10,30,90))
    if t>0.65: big_text(im,"6-7!",36+(f%2),(255,240,120),scale=4,cx=W//2+jx,outline=(120,20,40))
    if t<0.06: zoom_lines(d,(255,120,140))
    if t>0.92: im=fade_to(im,(0,0,0),(t-0.92)/0.08*0.6)
    return im

# ---- the clip --------------------------------------------------------------------------------
def pop(s,txt,y,c,scale=2,cx=W//2,ol=(20,10,30)): s['fx'].append(('meme_pop',txt,y,c,scale,cx,ol))

FA_HP=[(76,0.55),(90,0.0)]
TT_HP=[(190,0.66),(194,0.4),(198,0.2),(204,0.0)]
SS_HP=[(362,0.72),(368,0.48),(374,0.28),(390,0.0)]

def clip_bossrush(f):
    s=scene(f,THEME)
    cl=actor(CL[guard_pose(f)],CX); acts=[]
    # ======== BOSS 1: FOREVER ALONE =========================================================
    if 8<=f<24: pop(s,"BOSS 1",20,(250,220,110))
    if 14<=f<112:
        fa=actor(_fa(legs=(f//4)%2 if f<34 else 0),ez(205,136,(f-14)/20),pal=FAPAL); acts.append(fa)
        s['fx'].append(('meme_bar',"FOREVER ALONE",track(f,FA_HP,refill=None),(f-24)/8,(120,190,255)))
        if 34<=f<56: pop(s,"FOREVER ALONE",16,(240,240,240))
        if 56<=f<64: fa.update(spr=_fa(legs=(f//2)%2),x=ez(136,58,(f-56)/8))
        if 64<=f<76:                                                  # the flailing slaps
            fa.update(spr=_fa('slapA' if (f//3)%2 else 'slapB'),x=58)
            if f%6==3: s['fx'].append(('spark',42,GROUND-10,2))
            if 68<=f<76: s['fx'].append(('dmg',"MISS",24,GROUND-22,(200,200,210)))
        if 74<=f<78: cl.update(spr=CL['punch'])
        if f==76: s['fx'].append(('spark',48,GROUND-6,5)); s['shake']=rshake()
        if 76<=f<82: fa.update(spr=hurt(_fa()),x=ez(58,74,(f-76)/5))
        if 82<=f<100:                                                 # the hug
            fa.update(spr=_fa('hug',happy=f>=88),x=74); cl.update(spr=CL['armsup'],x=ez(CX,64,(f-82)/6))
            if 86<=f<96: s['fx'].append(('meme_heart',66,GROUND-33-(f-86)//2,(250,80,120)))
            if f>=94: pop(s,"NEW FRIEND!",16,(120,240,140),ol=(10,50,20))
        if 100<=f<112:
            fa.update(spr=_fa('up',happy=True),x=74,y=GROUND-(f-100),alpha=max(0,1-(f-100)/10))
            for j in range(3): s['fx'].append(('twinkle',74+random.randint(-10,10),GROUND-random.randint(4,30),1))
            cl.update(spr=CL[guard_pose(f)],x=ez(64,CX,(f-100)/12))
        if f<76: s['fx'].append(('meme_tears',fa['x'],fa['y']-len(fa['spr'])))
    # ======== BOSS 2: TUNG TUNG TUNG SAHUR =================================================
    if 112<=f<128: pop(s,"BOSS 2",20,(250,220,110))
    if 120<=f<226:
        tt=actor(TUNG['idle'],136,flip=True,pal=TUNGPAL); acts.append(tt)
        s['fx'].append(('meme_bar',"TUNG TUNG SAHUR",track(f,TT_HP,refill=None),(f-122)/8,(210,150,80)))
        if f<152:                                                     # hopping in to the drum beat
            k=min(3,(f-120)//8); ph=(f-120)%8
            x=lerp(205,136,min(1,(k+ph/8)/4)) if f<152 else 136
            hop=int(8*math.sin(math.pi*ph/8)) if f<152 else 0
            tt.update(x=x,y=GROUND-hop,spr=TUNG['hop'] if hop>2 else TUNG['idle'])
            if 128<=f<146: pop(s," ".join(["TUNG"]*min(3,(f-128)//8+1)),18,(230,180,110))
        if 146<=f<160: pop(s,"SAHUR!",16,(255,230,120),scale=3,ol=(90,40,10)); s['shake']=rshake() if f<150 else (0,0)
        if 160<=f<166: tt.update(spr=TUNG['hop'],x=ez(136,52,(f-160)/6),y=GROUND-int(6*math.sin(math.pi*(f-160)/6)))
        if 166<=f<190:                                                # three bonks
            ph=(f-166)%8; tt['x']=52
            tt['spr']=TUNG['raise'] if ph<4 else TUNG['swing']
            if ph==4: s['fx'].append(('spark',36,GROUND-8,5)); s['shake']=rshake(2)
            if ph>=4: cl.update(spr=CL['hurt'],x=CX-2)
            if ph>=4: pop(s,"TUNG!",22,(255,200,120),cx=34,ol=(80,30,10))
        if 186<=f<192: s['fx'].append(('dizzy',CX,GROUND-14))
        if 190<=f<202:                                                # Claude counters: a 3-hit combo
            k=(f-190)//4; ph=(f-190)%4; tt.update(spr=TUNG['hurt'],x=52+k*3)
            cl.update(spr=CL['dash' if ph<2 else 'punch'],x=CX+8+k*3)
            if ph==0: s['fx'].append(('spark',46+k*3,GROUND-10+k*2,4)); s['shake']=rshake()
        if 202<=f<205: cl.update(spr=CL['armsup'],x=48); tt.update(spr=TUNG['hurt'],x=58)
        if f==204: s['fx'].append(('spark',56,GROUND-14,7)); s['shake']=rshake(2); s['flash']=0.3; s['fc']=(56,GROUND-14)
        if 204<=f<226:                                                # uppercut into orbit, spinning
            t=(f-204)/12; tt.update(spr=rotate90(TUNG['hurt'],(f-204)//2%4),x=58+t*40,y=GROUND-int(90*t))
            for j in range(2): s['fx'].append(('shard',58+random.randint(-4,8),GROUND-random.randint(6,24)-(f-204)*2,(204,158,106)))
            cl.update(spr=CL['armsup'] if f<210 else CL[guard_pose(f)],x=48 if f<212 else ez(48,CX,(f-212)/12))
            if f>=208: pop(s,"K.O.",18,(255,90,80))
            if tt['y']<-10: tt['vis']=False
        if 186<=f<190: cl.update(spr=CL['hurt'],x=CX-2)
    # ======== FINAL BOSS: 6 7 ===============================================================
    if 228<=f<420: s['under'].append(('dim',0.4*min(1,(f-228)/10) if f<404 else 0.4*(1-(f-404)/16)))
    if 228<=f<248: s['fx'].append(('meme_warn',1)); s['shake']=rshake() if f%4<2 else (0,0)
    if 250<=f<404:
        b=actor(_boss(gesture(f)),BOSS_X,pal=BOSSPAL); acts.append(b)
        if f<272: b['y']=GROUND+int(BH*(1-ease((f-250)/20))); s['shake']=rshake()
        if 250<=f<272: pop(s,"FINAL BOSS",18,(255,70,70),ol=(60,0,10))
        if 272<=f<304: s['image']=closeup_67((f-272)/32,f); return s
        s['fx'].append(('meme_bar',"SIX SEVEN",track(f,SS_HP,refill=None),(f-304)/10,(230,70,140)))
        # the attack pattern follows the gesture: each hand that drops throws its numeral
        shots=[(316,'6'),(324,'7'),(332,'6'),(340,'7')]
        for t0,ch in shots:
            if t0<=f<t0+14:
                t=(f-t0)/12; x=lerp(BOSS_X-40 if ch=='6' else BOSS_X+34,-12,t)   # 6s roll low, 7s are lobbed
                y=GROUND-14 if ch=='6' else lerp(4,GROUND-14,min(1,t*1.4))
                s['fx'].append(('meme_digit',ch,x,y,(255,120,140) if ch=='6' else (120,190,255)))
            if t0-4<=f<t0+2: b['spr']=_boss(gesture(f),shout=True); pop(s,"SIX!" if ch=='6' else "SEVEN!",15,(255,240,150),scale=1,cx=BOSS_X-16 if ch=='6' else BOSS_X+16)
        for t0 in (320,329,336):                                      # Claude hops the 6s and 7s
            if t0<=f<t0+7: cl.update(spr=CL['guard2'],y=GROUND-int(15*math.sin(math.pi*(f-t0+0.5)/7)))
        if 348<=f<356:                                                # ...the last 7 lands
            cl.update(spr=CL['hurt'],x=CX-3)
            if f==348: s['fx'].append(('spark',32,GROUND-8,6)); s['shake']=rshake(2)
        if 356<=f<362: cl.update(spr=CL['charge'],aura=((250,200,80),1+(f%2)))
        if 362<=f<380:                                                # the combo
            k=(f-362)//6; ph=(f-362)%6
            cl.update(spr=CL['dash' if ph<2 else 'punch'],x=ez(CX,96,(f-362)/3) if k==0 else 96,aura=((250,200,80),1))
            if ph==0: s['fx'].append(('spark',106,GROUND-10-k*6,6)); s['shake']=rshake(2); b['tint']=(255,255,255)
            if ph<3: b['spr']=_boss(0,hurt_=True)
        if 380<=f<384: cl.update(spr=CL['dash'],x=ez(96,56,(f-380)/4))
        if 384<=f<396:                                                # the final blast
            cl.update(spr=CL['charge'],x=56,aura=((250,200,80),2))
            x1=lerp(66,BOSS_X,min(1,(f-384)/4)); s['fx'].append(('beam',66,x1,GROUND-7,((250,160,60),(255,230,140))))
            b['spr']=_boss(0,hurt_=True); b['tint']=(255,255,255) if f%2 else None; s['shake']=rshake(2)
            if f==390: s['flash']=0.8; s['fc']=(BOSS_X,GROUND-20); s['flashc']=(255,240,210)
        if f>=396: b['vis']=False
    if 390<=f<412:                                                    # the explosion
        rr=random.Random(f)
        for k in range(3):
            t=((f-390)+k*4)/12
            if 0<t<1: s['fx'].append(('boom',BOSS_X+(k-1)*18,GROUND-22+(k%2)*8,int(4+10*t)))
        if f<404:
            for j in range(6): s['fx'].append(('shard',BOSS_X+rr.randint(-40,40),GROUND-rr.randint(0,44),(255,rr.randint(80,220),90)))
            s['fx'].append(('meme_digit',"6",BOSS_X-20-(f-390)*3,GROUND-24-(f-390)*2,(255,120,140)))
            s['fx'].append(('meme_digit',"7",BOSS_X+20+(f-390)*3,GROUND-24-(f-390)*2,(120,190,255)))
    if 396<=f<420:                                                    # victory: back home in shades
        cl.update(spr=CL[guard_pose(f)],x=ez(56,CX,(f-396)/12),aura=None)
        if f<414: pop(s,"MEME DEFEATED",14,(255,230,120),ol=(90,40,10))
        if 404<=f<414: s['fx'].append(('dmg',"GG",W//2-3,30,(140,255,160)))
        if 398<=f<418:
            dy=-30*(1-ease((f-398)/6)) if f<414 else -30*ease((f-414)/4)
            s['fx'].append(('meme_shades',cl['spr'],cl['x'],cl['y'],False,dy))
            if 404<=f<414: s['fx'].append(('dmg',"DEAL WITH IT",CX-2,GROUND-22,(240,240,240)))
    s['actors']=acts+[cl]
    return s

CLIPS = [clip('bossrush', N_, clip_bossrush)]
