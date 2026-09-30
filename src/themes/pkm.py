"""Pokemon: Claude (in Ash's cap) vs Mewtwo, on a Game Boy Advance battle screen — the grass field
with the two oval platforms, the HP boxes (name, level, green-yellow-red HP bar, EXP bar) and the
text box with the FIGHT / BAG / PKMN / RUN menu. QUICK ATTACK; Mewtwo's PSYCHIC warps the whole
screen and drains Claude into the yellow; Claude answers with SHADOW BALL — close-up: IT'S SUPER
EFFECTIVE! Mewtwo faints, the EXP bar overflows, Claude grows to LV. 51, YOU WIN! Then a new
battle: A WILD MEWTWO APPEARED!, Claude is called back and sent out again — close-up of the Poke
Ball splitting open, GO! CLAUDE! — and the menu is back."""
from engine import *

THEME = 'pkm'
N_ = 336
CX, CY = 44, 46                                                     # Claude on the near platform (feet)
EX, EY = 138, 27                                                    # Mewtwo on the far platform (feet)
TB = 48                                                             # top of the text box

PAL.update({'m':(206,196,222),'u':(150,92,176),'I':(120,40,160)})
def _x2(spr): return S([''.join(c*2 for c in row) for row in spr for _ in range(2)])
ASH=variant(lambda s: _x2(overlay(s,["..rrrrrr....",".rrrHHrrr...",".rrrrrrrrrrr"],-1,0)))
MEWTWO=poses(S([
".....mm.mm........",".....mmmmm........","....mmmmmmm.......","....mmmImmI.......","....mmmmmmm.......",".....mmmmm........",
"......mmm.........","....mmmmmmm.......","...mmmmmmmmm......","..mm.mmmmm.mm.....","..mm.muuum.mm.....","..m..muuum..m.....",
"uu...muuum........","uu...uuuuu........",".uu.uuu.uuu.......","..uuu...uu........","...mm.....mm......","...mm.....mm......",
"..mmm.....mmm.....",]),9,'mm',4)

# ---- local glyphs: a wider M and W (the 3x5 font's read as H), an apostrophe and a slash --------
_GLYPH={'M':(5,"10001"+"11011"+"10101"+"10001"+"10001"),'W':(5,"10001"+"10001"+"10101"+"11011"+"10001"),
        "'":(1,"11000"),'/':(3,"001001010100100")}

def _mask(txt):
    gl=[_GLYPH.get(ch) or (3,FONT.get(ch,FONT[' '])) for ch in txt]
    m=Image.new('L',(max(1,sum(w+1 for w,_ in gl)-1),5),0); md=ImageDraw.Draw(m); x=0
    for w,bits in gl:
        for j,b in enumerate(bits):
            if b=='1': md.point((x+j%w,j//w),fill=255)
        x+=w+1
    return m

def say(im,txt,y,c,scale=1,cx=W//2,outline=None,shadow=(0,0,0),left=None):
    """big_text with the local glyphs; scale=1 is a normal line; left= aligns left instead of centring."""
    m=_mask(txt); m=m.resize((m.width*scale,m.height*scale),Image.NEAREST)
    x=int(cx-m.width//2) if left is None else int(left)
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
        if shadow is not None: im.paste(shadow,(x+2,y+2),m)
    elif shadow is not None: im.paste(shadow,(x+1,y+1),m)
    im.paste(c,(x,y),m)

@fx('pkm_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,*rest=e; say(im,txt,y,c,*rest)

# ---- the battle field (GBA grass battle background) ----------------------------------------------
def _field(d):
    for y in range(12):
        k=y/11; d.line([0,y,W,y],fill=(int(lerp(150,200,k)),int(lerp(206,236,k)),int(lerp(248,250,k))))
    for x in range(W):                                              # the tree line on the horizon
        y=int(9+2*math.sin(x*0.3)+1.5*math.sin(x*0.11+1)); d.line([x,y,x,16],fill=(56,128,72))
        if (x*7)%5==0: d.point((x,y),fill=(96,168,96))
    for y in range(16,TB):                                          # grass field in soft bands
        c=(168,216,120) if ((y-16)//4)%2 else (152,204,108)
        d.line([0,y,W,y],fill=c)
    rr=random.Random(1996)
    for _ in range(70):
        x,y=rr.randint(0,W-1),rr.randint(18,TB-2); d.line([x,y,x+1,y-1],fill=(112,176,84)); d.point((x+2,y),fill=(112,176,84))
    for (cx,cy,rx,ry) in ((EX,EY,22,5),(CX,CY,28,6)):               # the two oval platforms
        d.ellipse([cx-rx-1,cy-ry-1,cx+rx+1,cy+ry+1],fill=(96,152,72))
        d.ellipse([cx-rx,cy-ry,cx+rx,cy+ry],fill=(128,188,92))
        d.ellipse([cx-rx+3,cy-ry+1,cx+rx-3,cy+ry-2],fill=(144,200,100))
        d.arc([cx-rx,cy-ry,cx+rx,cy+ry],0,180,fill=(88,140,64))
register_bg(THEME, lambda v: (152,204,108), decor=_field)

def hp_color(v): return (72,200,96) if v>0.5 else (240,200,40) if v>0.2 else (230,56,40)

# ---- the HUD -----------------------------------------------------------------------------------
INK,INK2=(64,64,72),(222,222,212)

@fx('pkm_hpbox')
def _fx_hpbox(d,im,e,f):
    """x,y: name, level, HP bar (0..1); mine=True adds the HP numbers and the EXP bar."""
    _,x,y,name,lv,v,mine,xp=e; x,y=int(x),int(y); w=64; h=16 if mine else 13
    d.rectangle([x+1,y+1,x+w+1,y+h+1],fill=(72,88,72))
    d.rectangle([x,y,x+w,y+h],fill=(248,248,224),outline=(80,80,80))
    d.line([x+1,y+1,x+w-1,y+1],fill=(255,255,244))
    say(im,name,y+2,INK,left=x+3,shadow=INK2); say(im,lv,y+2,INK,left=x+w-len(lv)*4-1,shadow=INK2)
    d.rectangle([x+8,y+7,x+w-3,y+11],fill=(72,72,72))
    say(im,"HP",y+7,(248,176,56),left=x+9,shadow=None)
    bx=x+18; d.rectangle([bx,y+8,bx+42,y+10],fill=(40,48,40))
    if v>0:
        c=hp_color(v); L=max(1,int(42*v)); d.rectangle([bx,y+8,bx+L,y+10],fill=c)
        d.line([bx,y+8,bx+L,y+8],fill=tuple(min(255,k+60) for k in c))
        if v<=0.2 and (f//4)%2: d.rectangle([bx,y+8,bx+L,y+10],fill=(255,140,120))
    if mine:
        d.rectangle([x+8,y+13,x+w-3,y+14],fill=(64,64,64))
        if xp>0: d.rectangle([x+8,y+13,x+8+int((w-11)*min(1,xp)),y+14],fill=(64,176,248))

@fx('pkm_textbox')
def _fx_textbox(d,im,e,f):
    """The text box: two lines typed out `n` chars at a time, plus the FIGHT menu when menu>=0."""
    _,l1,l2,n,menu=e
    d.rectangle([0,TB,W-1,H-1],fill=(40,80,120)); d.rectangle([2,TB+1,W-3,H-2],fill=(248,248,248))
    d.rectangle([2,TB+1,W-3,H-2],outline=(104,176,208))
    s1=l1[:n]; s2=l2[:max(0,n-len(l1))]
    if s1: say(im,s1,TB+3,INK,left=6,shadow=INK2)
    if s2: say(im,s2,TB+9,INK,left=6,shadow=INK2)
    if n>=len(l1)+len(l2) and menu<0 and (f//5)%2:                  # the blinking "more" arrow
        d.polygon([(W-10,H-5),(W-6,H-5),(W-8,H-3)],fill=(232,72,56))
    if menu>=0:
        mx=112; d.rectangle([mx,TB,W-1,H-1],fill=(88,96,120)); d.rectangle([mx+2,TB+1,W-3,H-2],fill=(248,248,248),outline=(120,112,144))
        for i,lab in enumerate(("FIGHT","BAG","PKMN","RUN")):
            px,py=mx+10+(i%2)*34,TB+3+(i//2)*6
            sel=i==0
            say(im,lab,py,(232,72,56) if (sel and menu==1) else INK,left=px,shadow=INK2)
            if sel and (menu==1 or (f//4)%2): d.polygon([(px-5,py),(px-5,py+4),(px-2,py+2)],fill=INK)

@fx('pkm_warp')
def _fx_warp(d,im,e,f):
    """Psychic: every row of the field sways sideways and the screen goes pink (a 0..1)."""
    _,a=e; src=im.copy(); amp=3*a
    for y in range(TB):
        dx=int(round(amp*math.sin(y*0.35+f*0.8)))
        if dx: im.paste(src.crop((0,y,W,y+1)),(dx,y))
    im.paste(Image.blend(im,Image.new('RGB',(W,H),(236,120,220)),0.28*a).crop((0,0,W,TB)),(0,0))

@fx('pkm_rings')
def _fx_rings(d,im,e,f):
    """Psychic rings squeezing in on a target."""
    _,x,y,k=e
    for j in range(3):
        r=int(14-((f*1.2+j*5)%14)); d.ellipse([x-r,y-r//2,x+r,y+r//2],outline=(250,150,240) if j%2 else (200,90,230))

@fx('pkm_sball')
def _fx_sball(d,im,e,f):
    """Shadow Ball: a dark purple orb with a crackling rim."""
    _,x,y,r=e; x,y,r=int(x),int(y),int(r)
    d.ellipse([x-r-1,y-r-1,x+r+1,y+r+1],fill=(40,16,60)); d.ellipse([x-r,y-r,x+r,y+r],fill=(96,48,140))
    d.ellipse([x-r//2,y-r//2,x+r//3,y+r//3],fill=(150,90,200)); rr=random.Random(f)
    for _ in range(r+2):
        a=rr.random()*6.28; d.point((int(x+math.cos(a)*(r+2)),int(y+math.sin(a)*(r+2))),fill=(200,140,255))

@fx('pkm_star')
def _fx_star(d,im,e,f):
    """The GBA hit star."""
    _,x,y,r=e; x,y=int(x),int(y); pts=[]
    for k in range(10):
        a=k*math.pi/5-math.pi/2; L=r if k%2==0 else r*0.45; pts.append((x+math.cos(a)*L,y+math.sin(a)*L))
    d.polygon(pts,fill=(255,250,200),outline=(250,170,40))

@fx('pkm_beam')
def _fx_beam(d,im,e,f):
    """The red recall beam from the trainer (off-screen left)."""
    _,x,y=e; d.line([0,y-1,x,y-1],fill=(255,120,120)); d.line([0,y,x,y],fill=(236,40,40)); d.line([0,y+1,x,y+1],fill=(170,20,20))

@fx('pkm_speed')
def _fx_speed(d,im,e,f):
    rr=random.Random(f)
    for _ in range(7):
        y=rr.randint(14,TB-2); x=rr.randint(0,W-30); d.line([x,y,x+rr.randint(10,26),y],fill=(255,255,255))

@fx('pkm_sparkle')
def _fx_sparkle(d,im,e,f):
    _,x,y,c=e; x,y=int(x),int(y); d.line([x-2,y,x+2,y],fill=c); d.line([x,y-2,x,y+2],fill=c); d.point((x,y),fill=(255,255,255))

# ---- close-up 1: IT'S SUPER EFFECTIVE! -----------------------------------------------------------
def closeup_effective(t,f):
    im=Image.new('RGB',(W,H),(60,20,80)); d=ImageDraw.Draw(im)
    for k in range(18):                                             # impact rays
        a=k*math.pi/9+f*0.03
        d.polygon([(70,32),(70+math.cos(a)*240,32+math.sin(a)*240),(70+math.cos(a+0.17)*240,32+math.sin(a+0.17)*240)],
                  fill=(110,40,140) if k%2 else (80,28,110))
    hit=t>=0.22; jx=((f%3)-1)*3 if 0.22<=t<0.5 else 0
    hx=70+jx+(6 if hit else 0); hy=36
    lil,dk,pur=(214,204,230),(160,146,186),(150,92,176)
    d.polygon([(hx+14,hy-4),(hx+44,hy+6),(hx+50,hy+30),(hx+30,hy+30)],fill=pur)            # the neck tube
    d.ellipse([hx-24,hy-22,hx+24,hy+22],fill=lil,outline=(40,30,50))
    d.ellipse([hx-24,hy-22,hx+24,hy+22],outline=(40,30,50))
    d.chord([hx-24,hy-22,hx+24,hy+22],300,60,fill=dk)
    for sx in (-1,1):                                               # the stubby horns
        d.polygon([(hx+sx*10,hy-18),(hx+sx*18,hy-30),(hx+sx*20,hy-14)],fill=lil,outline=(40,30,50))
    if not hit:                                                     # the cold stare
        for ex in (hx-10,hx+8):
            d.polygon([(ex-5,hy-4),(ex+5,hy-2),(ex+4,hy+3),(ex-4,hy+2)],fill=(255,255,255),outline=(40,30,50))
            d.rectangle([ex-1,hy-2,ex+2,hy+2],fill=(120,40,160))
        d.line([hx-16,hy-8,hx-4,hy-5],fill=(40,30,50)); d.line([hx+2,hy-5,hx+14,hy-7],fill=(40,30,50))
        d.line([hx-4,hy+12,hx+6,hy+12],fill=(40,30,50))
    else:                                                           # reeling: eyes screwed shut, mouth open
        for ex in (hx-10,hx+8):
            d.line([ex-5,hy-4,ex+4,hy],fill=(40,30,50),width=2); d.line([ex-5,hy+4,ex+4,hy],fill=(40,30,50),width=2)
        d.ellipse([hx-6,hy+8,hx+6,hy+17],fill=(80,30,60))
    if t<0.24:                                                      # the Shadow Ball flies in
        bx=int(lerp(-20,hx-20,t/0.22)); FX['pkm_sball'](d,im,('pkm_sball',bx,hy,10),f)
    elif t<0.45:
        k=(t-0.22)/0.23
        for j in range(3): d.ellipse([hx-20-(k*60+j*8),hy-(k*30+j*4),hx-20+(k*60+j*8),hy+(k*30+j*4)],outline=(200,140,255))
        FX['pkm_star'](d,im,('pkm_star',hx-18,hy-2,int(14-8*k)),f)
    if t>=0.3:
        jj=(f%2) if t<0.4 else 0
        say(im,"IT'S SUPER",int(ez(-12,6,(t-0.3)/0.06)),(255,255,255),scale=2,cx=144+jj,outline=(90,30,110))
    if t>=0.4:
        jj=(f%2) if t<0.5 else 0
        say(im,"EFFECTIVE!",int(ez(80,26,(t-0.4)/0.06)),(255,226,90),scale=2,cx=144+jj,outline=(110,50,0))
    if 0.22<=t<0.26: im=fade_to(im,(255,255,255),0.7); d=ImageDraw.Draw(im)
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,(255,255,255),(t-0.9)/0.1*0.7)
    return im

# ---- close-up 2: the Poke Ball splits open — GO! CLAUDE! -----------------------------------------
def closeup_pokeball(t,f):
    im=Image.new('RGB',(W,H),(30,40,70)); d=ImageDraw.Draw(im)
    bx,by,r=62,34,22
    op=0 if t<0.36 else ez(0,1,(t-0.36)/0.16)                         # how far the top half has lifted
    wob=int(round(3*math.sin(t*40)*max(0,1-t/0.3))) if t<0.3 else 0
    if op>0:                                                        # the light pouring out of the gap
        for k in range(14):
            a=math.pi+k*math.pi/13
            L=40+60*op; d.polygon([(bx,by),(bx+math.cos(a)*L,by+math.sin(a)*L),(bx+math.cos(a+0.12)*L,by+math.sin(a+0.12)*L)],
                                  fill=(255,255,220) if k%2 else (255,236,160))
    x=bx+wob
    d.chord([x-r-1,by-r-1,x+r+1,by+r+1],0,180,fill=(20,20,24)); d.chord([x-r,by-r,x+r,by+r],0,180,fill=(244,244,244))
    d.chord([x-r+4,by-r+4,x+r-8,by+r-8],30,150,fill=(210,210,214))
    lift=int(op*18); tilt=op*10
    top=Image.new('RGBA',(2*r+3,r+3),(0,0,0,0)); td=ImageDraw.Draw(top)
    td.chord([0,0,2*r+2,2*r+2],180,360,fill=(20,20,24)); td.chord([1,1,2*r+1,2*r+1],180,360,fill=(226,48,44))
    td.chord([6,5,2*r-6,2*r-6],200,260,fill=(255,140,120)); td.rectangle([0,r,2*r+2,r+2],fill=(20,20,24))
    top=top.rotate(tilt,resample=Image.NEAREST,expand=False,center=(0,r+1))
    im.paste(top,(x-r-1,by-r-1-lift),top); d=ImageDraw.Draw(im)
    d.rectangle([x-r,by-1,x+r,by+1],fill=(20,20,24))                # the band and the button
    glow=0.26<=t<0.36 and (f//2)%2
    d.ellipse([x-7,by-6,x+7,by+6],fill=(20,20,24)); d.ellipse([x-5,by-4,x+5,by+4],fill=(255,255,180) if glow else (244,244,244))
    d.ellipse([x-2,by-2,x+2,by+2],outline=(150,150,150))
    if glow: asterisk(d,x,by,10,(255,255,200),f)
    if t>=0.1:
        say(im,"GO!",int(ez(-14,8,(t-0.1)/0.06)),(255,226,90),scale=3,cx=142,outline=(40,40,90))
    if t>=0.2:
        say(im,"CLAUDE!",int(ez(80,34,(t-0.2)/0.06)),(255,255,255),scale=2,cx=142,outline=(200,60,40))
    if t>=0.56: im=fade_to(im,(255,255,255),min(1,(t-0.56)/0.2)); d=ImageDraw.Draw(im)
    if t<0.06: zoom_lines(d)
    return im

# ---- the clip ----------------------------------------------------------------------------------
QA,PSY,SB,EFF,BACK,FAINT,EXP,WIN,WILD,GO,OUT=22,48,104,140,176,188,212,244,272,296,320
LINES=[(0,"WHAT WILL","CLAUDE DO?",1),(QA,"CLAUDE USED","QUICK ATTACK!",0),(PSY,"MEWTWO USED","PSYCHIC!",0),
       (SB,"CLAUDE USED","SHADOW BALL!",0),(BACK,"IT'S SUPER","EFFECTIVE!",0),(FAINT,"THE FOE MEWTWO","FAINTED!",0),
       (EXP,"CLAUDE GAINED","1200 EXP. POINTS!",0),(232,"CLAUDE GREW TO","LV. 51!",0),(WIN,"YOU WIN!","",0),
       (WILD,"A WILD MEWTWO","APPEARED!",0),(OUT,"WHAT WILL","CLAUDE DO?",1)]

def clip_psychic(f):
    s=scene(f,THEME)
    if EFF<=f<BACK: s['image']=closeup_effective((f-EFF)/(BACK-EFF),f); return s
    if GO<=f<OUT: s['image']=closeup_pokeball((f-GO)/(OUT-GO),f); return s
    hov=EY-2+round(1.5*math.sin(2*math.pi*f/24))
    cl=actor(ASH[guard_pose(f)],CX,CY); mw=actor(MEWTWO['idle'],EX,hov,flip=True)
    hc,hm,xp=1.0,1.0,0.2; lv='L50'; ebox,pbox=0,0                   # box slide offsets
    after=[]
    # 1) QUICK ATTACK
    if QA+2<=f<QA+10:
        t=(f-QA-2)/8; cl.update(x=lerp(CX,110,t),y=int(lerp(CY,36,t)),spr=ASH['dash'],aura=((255,255,255),1))
        s['fx'].append(('pkm_speed',))
        for k in (1,2): s['under'].append(('pkm_sparkle',cl['x']-k*14,cl['y']-10,(255,255,255)))
    if QA+10<=f<QA+14:
        cl.update(x=110,y=36,spr=ASH['punch']); s['shake']=rshake(2)
        after.append(('pkm_star',EX-4,hov-10,9-(f-QA-10)*2))
    if QA+14<=f<QA+26:
        t=(f-QA-14)/12; cl.update(x=ez(110,CX,t),y=int(ez(36,CY,t)-8*math.sin(math.pi*t)))
    if QA+10<=f<QA+20: mw['vis']=(f%4)<2
    if QA+12<=f<WILD: hm=lerp(1,0.8,(f-QA-12)/10)
    # 2) PSYCHIC: the screen warps, Claude is lifted and wrung out
    if PSY<=f<SB:
        mw.update(spr=MEWTWO['attack'] if f<PSY+10 else MEWTWO['idle'],aura=((200,120,255),1+(f%2)))
        if PSY<=f<PSY+8: mw['tint']=(250,170,255) if f%2 else None
    if PSY+8<=f<PSY+48:
        a=min(1,(f-PSY-8)/6,(PSY+48-f)/6)
        lift=ez(0,10,(f-PSY-8)/10)
        cl.update(y=int(CY-lift)+random.choice([-1,0,1]),x=CX+random.choice([-1,0,1]),spr=ASH['hurt'],aura=((236,120,236),2))
        after.insert(0,('pkm_warp',a)); s['fx'].append(('pkm_rings',cl['x'],cl['y']-12,0))
        hc=lerp(1,0.42,(f-PSY-16)/28)
    if PSY+48<=f<PSY+56:
        t=(f-PSY-48)/8; cl.update(y=int(lerp(CY-10,CY,t*t)),spr=ASH['hurt'])
        if f==PSY+52: s['shake']=rshake(2)
        if f>=PSY+52:
            for _ in range(2): s['fx'].append(('dust',CX+random.randint(-14,14),CY-random.randint(0,3)))
    if PSY+44<=f<WILD: hc=0.42
    # 3) SHADOW BALL
    if SB+4<=f<SB+22:
        k=(f-SB-4)/18; cl.update(spr=ASH['charge'],aura=((150,80,220),1+(f%2)))
        s['fx'].append(('pkm_sball',CX+26,CY-10,1+int(6*k)))
        for i in range(6):
            a=i*1.047+f*0.4; L=(1-((f*0.08+i/6)%1))*16
            s['fx'].append(('mote',CX+26+math.cos(a)*L,CY-10+math.sin(a)*L,(200,140,255)))
    if SB+22<=f<EFF:
        cl['spr']=ASH['punch']; t=(f-SB-22)/(EFF-SB-22)
        s['fx'].append(('pkm_sball',lerp(CX+26,EX-2,t),lerp(CY-10,hov-10,t)-8*math.sin(math.pi*t),7))
        mw['spr']=MEWTWO['idle']
    # 4) back from the close-up: HP crashes, Mewtwo faints
    if BACK<=f<FAINT+4:
        mw.update(spr=MEWTWO['hurt'],vis=(f%4)<2 if f<BACK+10 else True)
        if f<BACK+6: after.append(('pkm_star',EX-2,hov-10,8)); s['shake']=rshake(2)
    if EFF<=f<WILD: hm=lerp(0.8,0,(f-BACK-2)/14)
    if FAINT+4<=f<WILD:
        k=int(ez(0,19,(f-FAINT-4)/10)); hm=0
        if k<19: mw.update(spr=MEWTWO['hurt'][:19-k],y=EY)
        else: mw['vis']=False
        if f<FAINT+8: s['fx'].append(('pkm_say',"MEW!",3,(255,255,255),1,EX,(90,30,110)))
    if FAINT+14<=f<WILD: ebox=int(ez(0,-70,(f-FAINT-14)/8))
    # 5) EXP, level up, YOU WIN!
    if EXP<=f<WILD:
        xp=ez(0.2,1,(f-EXP-4)/16) if f<232 else ez(0,0.15,(f-232)/10)
        if f>=232: lv='L51'
        if 232<=f<240:
            cl['tint']=(255,255,255) if f%2 else None; hc=ez(0.42,1,(f-232)/8)
            s['fx'].append(('ring',CX,CY-10,(f-232)*4+4,(255,236,120)))
        if f>=240: hc=1
        if 232<=f<252:
            for i in range(4):
                ph=((f-232)*0.05+i/4)%1; s['fx'].append(('pkm_sparkle',CX-16+i*10,CY-6-ph*30,(255,226,90) if i%2 else (120,200,255)))
    if WIN<=f<WILD:
        k=f-WIN; cl.update(spr=ASH['armsup'],y=CY-int(abs(6*math.sin(k*math.pi/8))))
        jj=(f%2) if k<6 else 0
        s['fx'].append(('pkm_say',"YOU WIN!",int(ez(-16,10,k/6)),(255,226,90),3,W//2+jj,(40,40,110)))
        for i in range(5):
            ph=(k*0.04+i/5)%1; s['fx'].append(('pkm_sparkle',20+i*36,4+ph*44,(255,255,255)))
    if WIN<=f<WILD: hc=1
    # 6) a new battle: A WILD MEWTWO APPEARED!, Claude is called back
    if WILD<=f<GO:
        k=f-WILD; hc=1; lv='L51'
        mw.update(vis=True,spr=MEWTWO['idle'],tint=(24,24,40) if k<10 else None,x=int(ez(W+20,EX,k/10)))
        ebox=int(ez(-70,0,(k-4)/8))
        if 12<=k<24:                                                # recalled: red, shrinking into the beam
            cl['tint']=(236,60,60); sh=max(0,1-(k-12)/10)
            spr=cl['spr']; hh,ww=int(len(spr)*sh),int(len(spr[0])*sh)
            if hh>1 and ww>1: cl['spr']=S([''.join(spr[int(j/sh)][int(i/sh)] for i in range(ww)) for j in range(hh)])
            else: cl['vis']=False
            s['fx'].append(('pkm_beam',CX,CY-8))
        if k>=24: cl['vis']=False
        if k>=12: pbox=int(ez(0,80,(k-12)/8))
    if OUT<=f<OUT+8:                                                # Claude materializes out of the light
        cl['tint']=(255,255,255) if f<OUT+4 else ((255,255,200) if f%2 else None)
        s['flash']=1-(f-OUT)/8; s['fc']=(CX,CY-12); s['flashc']=(255,255,255)
        s['fx'].append(('ring',CX,CY-2,(f-OUT)*4+6,(255,255,255)))
    # the HUD
    msg=None
    for t0,l1,l2,menu in LINES:
        if f>=t0: msg=(t0,l1,l2,menu)
    t0,l1,l2,menu=msg
    n=int((f-t0)*2.5)+1 if t0>0 else 99
    if t0==OUT: n=99
    mstate=menu
    if menu and QA-6<=f<QA: mstate=1                                 # FIGHT pressed
    elif menu: mstate=0
    else: mstate=-1
    s['fx']+=after
    s['fx'].append(('pkm_hpbox',3+ebox,2,"MEWTWO","L70",hm,False,0))
    s['fx'].append(('pkm_hpbox',116+pbox,30,"CLAUDE",lv if f<GO else 'L50',hc,True,xp if f<WILD else (0.2 if f>=OUT else xp)))
    s['fx'].append(('pkm_textbox',l1,l2,n,mstate))
    s['actors']=[mw,cl]
    return s

CLIPS = [clip('psychic', N_, clip_psychic)]
