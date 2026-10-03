"""American Dragon: Jake Long ("El Dragon Occidental"): Claude is Jake (black hair with green tips,
the red jacket) on the Chinatown rooftops of New York at night. The Huntsman (armour, the bone mask,
the staff) takes aim; Claude ollies the first blast on his skateboard. Close-up: DRAGON UP! — the
fire runs up his body and he is the red dragon with the black-and-green crest and the wings. He
flies through the staff blasts and breathes fire; Fu Dog, on a roof: YO, JAKE! LOOK OUT! — the
Huntsclan net drops on him; he burns his way out, a tail-whip sends the Huntsman flying, and he
lands back as Jake: HAHA, DRAGON! The Huntsman drops back onto his spot."""
import zlib
from engine import *

THEME = 'jakelong'
N_ = 280
CX, VX = 30, 150                                                   # the neutral pose: Claude, the Huntsman
AIR = GROUND-14                                                    # the dragon's flying height (feet)

FIRE = ((255,240,170),(255,170,50),(230,70,30))
BOLT = (120,255,140)

def _say(im,txt,y,c,scale=2,outline=None,cx=W//2): big_text(im,txt,y,c,scale=scale,cx=cx,outline=outline)

@fx('jl_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; _say(im,txt,y,c,scale,outline)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))
def banner(s,txt,y,c,scale=2,outline=None): s['fx'].append(('jl_say',txt,y,c,scale,outline))

# ---- Claude as Jake: black hair with green tips, the red jacket over a white tee -----------------
def _jake(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y])
    coat=max(bot-3,max(y for y in range(h) if 'K' in spr[y])+2)
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='O' and not inside: g[y][x]='O'                      # a fist stays skin
            elif c=='O' and y>=coat: g[y][x]='W' if x==(l+r)//2+1 else 'R'
            elif c=='o' and y>bot: g[y][x]='n'                         # jeans
            elif c=='o' and y==bot and inside: g[y][x]='R'
            elif c=='o': g[y][x]='R'                                   # sleeves
    return overlay(ungrid(g),[".J..J..J..",".kJkkJkkJ.","kkkkkkkkkk"],-1,0,bangs="kkk.kkkk")
JAKE=variant(_jake)
JAKEPAL={'k':(22,20,26),'J':(80,230,110),'R':(210,40,44),'W':(240,240,240),'n':(52,62,110)}

# ---- the dragon: red scales, cream belly, the black crest with green tips, dark wings ----------
_DR_UP=S([
"..w.................kJ.kJ..",
"..ww...............kkkkkk..",
".wwww.............rrrrrrrr.",
".wwwww...........rrrrYKrrrr",
"..wwwww..........rrrrrrrrrr",
"...wwwww..........rrrrrrrr.",
"....wwwww........rrrcccc...",
".....wwwwrr.....rrrr.......",
"......wwrrrrrrrrrrrr.......",
"........rrrrcccccrrr.......",
"..r....rrrrcccccrrr........",
".rr...rrrrrcccccrr.........",
"rr...rrrrrrrcccrrrr........",
"rr..rrrrrrrrrrrr.rr........",
".rrrrrr..rr...rr..kk.......",
"..rrr....rr...rr...........",
".........kkk..kkk..........",])
_DR_DN=S([
"....................kJ.kJ..",
"...................kkkkkk..",
"..................rrrrrrrr.",
".................rrrrYKrrrr",
".................rrrrrrrrrr",
"..................rrrrrrrr.",
".................rrrcccc...",
"...........rr...rrrr.......",
"........rrrrrrrrrrrr.......",
"......wwwwrrcccccrrr.......",
"..r..wwwwwrcccccrrr........",
".rr.wwwwwwrcccccrr.........",
"rr.wwwwwwrrrcccrrrr........",
"rr.wwwwwrrrrrrrr.rr........",
".rrwwwwr..rr...rr..kk......",
"..rww....rr...rr...........",
"..w......kkk..kkk..........",])
def _breath(spr):
    g=grid(spr)
    for x in range(22,27): g[4][x]='.'                                 # the jaw drops open
    g[5][23:27]=list('cccc'); g[3][26]='r'
    return ungrid(g)
DRAGON={'up':_DR_UP,'dn':_DR_DN,'breath':_breath(_DR_UP),'hurt':hurt(_DR_DN),
        'whip':S([r[::-1] for r in _DR_DN])}                           # spun round: the tail leads
DRPAL={'r':(200,36,40),'c':(246,220,160),'w':(110,24,40),'k':(22,20,26),'J':(80,230,110),
       'Y':(255,220,60),'K':(20,10,10)}
def dr_fly(f): return DRAGON['up'] if (f//4)%2 else DRAGON['dn']

# ---- the Huntsman: armour, the bone mask, the staff --------------------------------------------
_HU=S([
"......kkkk.......",
".....kHHHHk......",
".....HkHHkH....E.",
".....HHHHHH....b.",
"......HkkH.....b.",
"....gggggggg...b.",
"...ggDDDDDDgg..b.",
"...gDDDDDDDDg..b.",
"..gg.DDDDDD.ggHb.",
"..gg.DDrrDD.ggHb.",
"..HH.DDDDDD....b.",
".....DDDDDD....b.",
".....kkkkkk....b.",
".....DDDDDD....b.",
".....DDD.DDD...b.",
".....DD...DD...b.",
".....DD...DD...b.",
".....gg...gg...b.",
".....DD...DD.....",
".....DD...DD.....",
"....kkk...kkk....",])
_HU_AIM=S([
"......kkkk..............",
".....kHHHHk.............",
".....HkHHkH.............",
".....HHHHHH.............",
"......HkkH..............",
"....gggggggg............",
"...ggDDDDDDgg...........",
"...gDDDDDDDDgHH.........",
"..gg.DDDDDD.gbbbbbbbbbbE",
"..gg.DDrrDD.HH..........",
"..HH.DDDDDD.............",
".....DDDDDD.............",
".....kkkkkk.............",
".....DDDDDD.............",
".....DDD.DDD............",
".....DD...DD............",
".....DD....DD...........",
".....gg....gg...........",
"....DD......DD..........",
"....DD......DD..........",
"...kkk......kkk.........",])
HUNT={'idle':_HU,'idle2':S([_HU[0]]+[r for r in _HU[1:]]),'aim':_HU_AIM,'hurt':hurt(_HU)}
HUNT['idle2']=S([r.replace('E','e') for r in _HU])                     # the staff's tip pulses
HUNT['down']=rotate90(HUNT['hurt'],3,trim=True)
HUPAL={'H':(226,220,200),'k':(26,24,30),'g':(84,96,84),'D':(52,60,58),'r':(200,30,30),'b':(120,84,50),
       'E':BOLT,'e':(60,170,80)}
def hu_idle(f): return HUNT['idle'] if (f//6)%2==0 else HUNT['idle2']
TIP=hand_at(_HU_AIM,VX,GROUND,True,23,8)                              # the staff's tip, aiming left

# ---- Fu Dog, the wrinkly shar-pei ---------------------------------------------------------------
FUDOG=S([
".s.....s.",
"sss...sss",
".sssssss.",
".sKssKss.",
".sssssss.",
".ssWWWss.",
"..sssss..",
".sssssss.",
".ss.s.ss.",])
FUPAL={'s':(160,146,160),'K':(20,16,20),'W':(240,236,230)}
FU_X,FU_Y=96,GROUND-21                                                 # on the pagoda roof

# ---- background: Chinatown rooftops at night ----------------------------------------------------
def _chinatown(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(14+16*k),int(10+10*k),int(34+16*k)))
    rr=random.Random(zlib.crc32(b'chinatown'))
    for _ in range(24): d.point((rr.randint(0,W-1),rr.randint(0,24)),fill=(150,140,190))
    d.ellipse([20,4,32,16],fill=(240,232,200)); d.ellipse([24,5,30,11],fill=(226,216,186))
    for x,w,h in ((0,18,26),(40,14,20),(122,16,30),(140,22,22),(166,19,28)):  # far towers
        d.rectangle([x,GROUND-h,x+w,GROUND],fill=(28,20,44))
        for wy in range(GROUND-h+3,GROUND-2,4):
            for wx in range(x+2,x+w-1,4):
                if rr.random()<0.4: d.point((wx,wy),fill=(250,210,120))
    # the pagoda roof Fu Dog sits on
    d.rectangle([80,GROUND-12,112,GROUND],fill=(54,24,30))
    d.polygon([(74,GROUND-11),(80,GROUND-13),(112,GROUND-13),(118,GROUND-11),(114,GROUND-14),(78,GROUND-14)],fill=(30,70,50))
    d.rectangle([84,GROUND-20,108,GROUND-14],fill=(54,24,30))
    d.polygon([(78,GROUND-19),(84,GROUND-21),(108,GROUND-21),(114,GROUND-19),(110,GROUND-22),(82,GROUND-22)],fill=(30,70,50))
    for x in range(86,108,5): d.rectangle([x,GROUND-10,x+2,GROUND-6],fill=(250,190,90))
    # a neon sign
    d.rectangle([58,GROUND-30,64,GROUND-6],fill=(40,16,30),outline=(255,60,120))
    for y in range(GROUND-27,GROUND-8,5): d.line([60,y,62,y],fill=(255,120,170)); d.point((61,y+2),fill=(255,120,170))
    # strings of red lanterns
    for x0,x1,yy in ((0,56,GROUND-24),(118,185,GROUND-26)):
        for x in range(x0,x1):
            y=yy+int(4*math.sin(math.pi*(x-x0)/(x1-x0)))
            d.point((x,y),fill=(70,50,50))
            if (x-x0)%9==4: d.rectangle([x-1,y+1,x+1,y+3],fill=(230,50,40)); d.point((x,y+4),fill=(255,200,80))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(60,40,40))                  # the rooftop ledge
    for x in range(0,W,6): d.point((x,GROUND-1),fill=(90,60,56))
register_bg(THEME, lambda v: (v+10,v//2+6,v//2+10), decor=_chinatown)

# ---- effects ------------------------------------------------------------------------------------
@fx('jl_board')
def _fx_board(d,im,e,f):
    """The skateboard under the feet, tilted by `tilt` pixels at the nose."""
    _,x,y,tilt=e; x=int(x); y=int(y)
    d.line([x-6,y-tilt,x+6,y+tilt],fill=(60,180,90),width=2)
    for wx in (x-4,x+4): d.point((wx,y+2+(tilt if wx>x else -tilt)//2),fill=(230,230,230))

@fx('jl_bolt')
def _fx_bolt(d,im,e,f):
    """A green staff blast: a short glowing dart between two points (t: 0..1 along the line)."""
    _,x0,y0,x1,y1,t=e
    if not 0<=t<=1: return
    hx,hy=lerp(x0,x1,t),lerp(y0,y1,t); bx,by=lerp(x0,x1,max(0,t-0.12)),lerp(y0,y1,max(0,t-0.12))
    d.line([bx,by,hx,hy],fill=(40,160,70),width=4); d.line([bx,by,hx,hy],fill=BOLT,width=2)
    d.ellipse([hx-2,hy-2,hx+2,hy+2],fill=(230,255,230))

@fx('jl_flame')
def _fx_flame(d,im,e,f):
    """Dragon fire: a widening cone of flickering puffs from (x0,y) to x1."""
    _,x0,y,x1=e; rr=random.Random(f*31+int(x0))
    n=int(abs(x1-x0)//2)
    for i in range(n):
        k=i/max(1,n-1); x=lerp(x0,x1,k)+rr.uniform(-1,1); yy=y+rr.uniform(-1,1)*(1+k*5); r=1+int(k*3)+rr.randint(0,1)
        c=FIRE[0] if k<0.25 else (FIRE[1] if k<0.65 else FIRE[2])
        d.ellipse([x-r,yy-r,x+r,yy+r],fill=c)

@fx('jl_net')
def _fx_net(d,im,e,f):
    """The Huntsclan net over a box; `burn` 0..1 eats it from the middle out."""
    _,x,y,w,h,burn=e; x,y=int(x),int(y)
    c=(170,180,170); rr=random.Random(zlib.crc32(b'net'))
    for i in range(0,w+1,3):
        for j in range(0,h+1,3):
            cut=abs(i-w/2)/(w/2)<burn or abs(j-h/2)/(h/2)<burn*0.8
            if cut: continue
            if i+3<=w: d.line([x+i,y+j,x+i+3,y+j],fill=c)
            if j+3<=h: d.line([x+i,y+j,x+i,y+j+3],fill=c)
            if 0<burn<1 and rr.random()<0.25: d.point((x+i,y+j),fill=FIRE[1])
    for k in (0,w): d.point((x+k,y),fill=(90,90,96))

@fx('jl_lanternglow')
def _fx_lanternglow(d,im,e,f):
    """The pagoda's windows flicker."""
    if f<8 or f>=N_-8: return                                          # still at the loop seam
    for i,x in enumerate(range(86,108,5)):
        if (f//7+i*3)%5==0: d.rectangle([x,GROUND-10,x+2,GROUND-6],fill=(255,230,150))

# ---- close-up: DRAGON UP! ------------------------------------------------------------------------
_BIG_JAKE=sprite_img(JAKE['armsup'],JAKEPAL,scale=4)
_BIG_DR=sprite_img(DRAGON['up'],DRPAL,scale=3)
def closeup_dragonup(t,f):
    """Jake, arms up; the fire runs up his body leaving red scales; the dragon roars: DRAGON UP!"""
    im=Image.new('RGB',(W,H),(20,8,16)); d=ImageDraw.Draw(im)
    for i in range(12):                                                # the fire-ring backdrop
        a=i*math.pi/6+t*2; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(60,18,20))
    if t<0.62:
        spr=_BIG_JAKE.copy(); line=int(spr.height*(1-ease((t-0.12)/0.45)))  # the fire line, rising
        if t>=0.12:
            px=spr.load()
            for y in range(max(0,line),spr.height):
                for x in range(spr.width):
                    if px[x,y][3]:
                        sc=(200,36,40) if (x//4+y//4)%2 else (170,26,34)
                        px[x,y]=(sc if px[x,y][:3]!=OUT else OUT)+(255,)
        paste_feet(im,spr,W//2,H+2); d=ImageDraw.Draw(im)
        if t>=0.12:
            fy=H+2-spr.height+line
            rr=random.Random(f)
            for i in range(26):
                x=W//2-spr.width//2-4+rr.randint(0,spr.width+8); h=rr.randint(3,10)
                c=FIRE[rr.randint(0,2)]; d.ellipse([x-2,fy-h,x+2,fy+2],fill=c)
    else:
        a=ease((t-0.62)/0.12)
        sp=_BIG_DR; paste_feet(im,sp,W//2-12+int(4*(1-a)),H+6)
        d=ImageDraw.Draw(im)
        if t<0.72: im=fade_to(im,(255,200,120),0.6*(1-(t-0.62)/0.1)); d=ImageDraw.Draw(im)
        if t>=0.66:
            jx=(f%3)-1 if t<0.78 else 0
            _say(im,"DRAGON UP!",6,(255,230,120),scale=3,outline=(150,20,20),cx=W//2+jx)
    if t<0.06: zoom_lines(d,(255,140,60))
    return im

# ---- the clip ------------------------------------------------------------------------------------
def dr_pos(f):
    """The dragon's (x, feet) while airborne."""
    if f<84: return CX,AIR
    if f<96: return ez(CX,70,(f-84)/12),AIR-ez(0,10,(f-84)/12)
    if f<132:                                                          # dodges: up, down, up
        k=(f-96)/36; return 70+4*math.sin(k*math.pi*2),AIR-10+12*math.sin(k*math.pi*3)
    if f<160: return 70,AIR-10+math.sin(f/3)
    return 70,AIR-10

def clip_dragon(f):
    s=scene(f,THEME); s['under'].append(('jl_lanternglow',))
    cl=actor(JAKE[guard_pose(f)],CX,pal=JAKEPAL)
    hu=actor(hu_idle(f),VX,flip=True,pal=HUPAL)
    extra=[]
    # 1) the Huntsman takes aim; Claude hops on the board and ollies the blast
    if 10<=f<40: shout(s,"THE DRAGON WILL BE MINE!",(160,255,170))
    if 14<=f<44: cl['spr']=JAKE['punch' if f<18 else 'guard']; s['under'].append(('jl_board',cl['x'],GROUND,0))
    if 24<=f<44: hu['spr']=HUNT['aim']
    if 30<=f<40: s['fx'].append(('jl_bolt',TIP[0],TIP[1],0,GROUND-4,(f-30)/8))
    if 32<=f<40:
        t=(f-32)/8; y=GROUND-int(12*math.sin(math.pi*t)); cl.update(spr=JAKE['armsup'],y=y)
        s['fx'].append(('jl_board',cl['x'],y,1 if t<0.5 else -1))
        s['under']=[u for u in s['under'] if u[0]!='jl_board']
    if f==38: s['fx'].append(('spark',2,GROUND-4,5)); s['shake']=rshake()
    if 40<=f<44: cl['spr']=JAKE['armsup']
    # 2) close-up: DRAGON UP!
    if 44<=f<76: s['image']=closeup_dragonup((f-44)/32,f); return s
    # 3) the dragon takes off, flies through three blasts
    if 76<=f<232:
        x,y=dr_pos(f); spr=dr_fly(f)
        cl.update(spr=spr,x=x,y=int(y),pal=DRPAL)
    if 76<=f<82: s['flash']=0.5-(f-76)*0.08; s['fc']=(CX,AIR-8); s['flashc']=(255,190,110); s['fx'].append(('ring',CX,AIR-6,4+(f-76)*4,FIRE[1]))
    for k,f0 in enumerate((96,108,120)):
        if f0-4<=f<f0+10: hu['spr']=HUNT['aim']
        if f0<=f<f0+8:
            x,y=dr_pos(f0+4); miss=8 if k%2==0 else -8
            s['fx'].append(('jl_bolt',TIP[0],TIP[1],x-6,y-8+miss,(f-f0)/6))
    if 96<=f<130 and f%12<6: shout(s,"HOLD STILL, DRAGON!",(160,255,170))
    # 4) the fire breath
    if 132<=f<150:
        x,y=dr_pos(f); cl['spr']=DRAGON['breath']
        mx=x+14
        if f>=134: s['fx'].append(('jl_flame',mx,int(y)-13,min(VX-4,mx+(f-134)*12)))
    if 140<=f<154:
        hu.update(spr=HUNT['hurt'],x=VX+(f-140)//3); s['fx'].append(('smoke',VX+random.randint(-4,4),GROUND-24-(f-140),2,(70,60,64)))
        if f<146: s['fx'].append(('dmg','HOT!',VX-6,GROUND-34,(255,200,90)))
    if 154<=f<200: hu['x']=VX+4
    # 5) Fu Dog: YO, JAKE! LOOK OUT! — the net
    if 140<=f<204:
        k=min(1,(f-140)/6,(204-f)/6); extra.append(actor(FUDOG,FU_X,FU_Y+int(6*(1-k)),pal=FUPAL))
    if 154<=f<170: shout(s,"YO, JAKE! LOOK OUT!",(200,190,220))
    NETX=70
    if 162<=f<170:                                                     # the net drops from above
        t=(f-162)/8; s['fx'].append(('jl_net',NETX-16,int(lerp(-24,AIR-30,t)),32,22,0))
    if 170<=f<200:
        t=min(1,(f-170)/8); y=int(lerp(AIR-10,GROUND,t*t))
        cl.update(spr=DRAGON['hurt'],x=NETX+((f//2)%2 if f>=178 else 0),y=y)
        burn=0 if f<188 else (f-188)/10
        s['fx'].append(('jl_net',NETX-16,y-20,32,22,burn))
        if f>=184: s['fx'].append(('jl_flame',NETX-2,y-9,NETX+2+(f%3)))
        if f==170+8: s['shake']=rshake(2); s['fx'].append(('dust',NETX-8,GROUND-1)); s['fx'].append(('dust',NETX+8,GROUND-1))
        if 170<=f<184: shout(s,"GOT YOU!",(160,255,170))
    if 188<=f<200:
        for j in range(6): s['fx'].append(('shard',NETX+random.randint(-16,16),GROUND-random.randint(4,22),FIRE[random.randint(0,2)]))
        if f==190: s['flash']=0.4; s['fc']=(NETX,GROUND-10); s['flashc']=(255,200,120)
    # 6) the tail-whip
    if 200<=f<212:
        t=(f-200)/12; cl.update(spr=dr_fly(f),x=ez(NETX,VX-18,t),y=int(GROUND-2-6*math.sin(math.pi*t)))
    if 212<=f<218: cl.update(spr=DRAGON['whip'],x=VX-14,y=GROUND-2)
    if f==213: s['fx'].append(('spark',VX-6,GROUND-12,8)); s['shake']=rshake(3); s['flash']=0.45; s['fc']=(VX-6,GROUND-12); s['flashc']=(255,240,200)
    if 213<=f<218: banner(s,"WHAM!",8,(255,230,120),2,(150,20,20))
    if 213<=f<230:
        t=(f-213)/17; hu.update(spr=rotate90(HUNT['hurt'],(f//2)%4),x=lerp(VX,210,t),y=int(lerp(GROUND,-24,t)))
    if 230<=f<242: hu['vis']=False
    # 7) back to Jake: HAHA, DRAGON!
    if 218<=f<232:
        t=(f-218)/14; cl.update(spr=dr_fly(f),x=ez(VX-14,CX,t),y=int(GROUND-2-12*math.sin(math.pi*t)))
    if 232<=f<240:
        t=f-232; cl.update(spr=DRAGON['dn'] if t<3 else JAKE['armsup'],x=CX,y=GROUND,pal=DRPAL if t<3 else JAKEPAL)
        s['fx'].append(('ring',CX,GROUND-6,3+t*3,FIRE[1]))
        if t<4: s['flash']=0.35-t*0.08; s['fc']=(CX,GROUND-8); s['flashc']=(255,190,110)
    if 240<=f<262:
        cl.update(spr=JAKE['armsup' if (f//4)%2 else 'guard'],pal=JAKEPAL)
        banner(s,"HAHA, DRAGON!",10,(255,230,120),2,(150,20,20))
    # the Huntsman drops back onto his spot
    if 242<=f<250: hu.update(vis=True,spr=HUNT['hurt'],x=VX,y=int(ez(-24,GROUND,(f-242)/8)))
    if f==250: s['fx'].append(('dust',VX-6,GROUND-1)); s['fx'].append(('dust',VX+6,GROUND-1)); s['shake']=rshake()
    if 250<=f<262: hu.update(spr=HUNT['down']); s['fx'].append(('dizzy',VX,GROUND-8))
    if 262<=f<268: hu['spr']=HUNT['hurt']
    s['actors']=extra+[hu,cl]
    return s

CLIPS = [clip('dragon', N_, clip_dragon)]
