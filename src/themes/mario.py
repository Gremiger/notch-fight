"""Super Mario Bros.: Claude (Mario) vs Bowser on the castle bridge of WORLD 8-4. Bowser breathes
fire and throws hammers; Claude jumps, bumps a coin out of a "?" block, then a Super Star (close-up
of the block being hit from below). Rainbow-invincible, Claude shrugs off the flame, vaults Bowser
and grabs the axe: the bridge collapses tile by tile and Bowser drops into the lava. THANK YOU
CLAUDE! - BUT OUR PRINCESS IS IN ANOTHER CASTLE! - then the black WORLD 8-4 intro and a reset."""
from engine import *

THEME = 'mario'
N_ = 300

# --- Claude as Mario: red cap with the white mark, moustache, red shirt, blue overalls ----------
def _mario_dress(spr):
    ks=[(x,y) for y,row in enumerate(spr) for x,ch in enumerate(row) if ch=='K']
    ky=max(y for _,y in ks); kx0=min(x for x,_ in ks); kx1=max(x for x,_ in ks); h=len(spr)
    def fn(x,y,t,l,r,c):
        if c=='.': return None
        if y==ky+1 and kx0-1<=x<=kx1+1 and c=='O': return 'k'           # moustache
        if y>=h-2: return 'q' if y==h-1 else 'L'                          # legs, brown shoes
        if y>=t+5:
            if l<=x<=r:
                if y==t+5: return 'L' if x in (l+2,r-2) else 'r'          # shirt + straps
                if y==t+6 and x in (l+2,r-2): return 'Y'                  # buttons
                return 'L'
            return 'W' if c=='O' else 'r'                                 # white gloves, sleeves
        if c=='o': return 'r'
        return None
    return overlay(recolor_rows(spr,fn),["..rrrr....",".rrrWrr...","rrrrrrrrrr"],0,0)
MARIO=variant(_mario_dress)
STAR_PALS=[None,{'r':(40,150,40),'L':(240,190,60),'O':(250,190,130)},
           {'r':(250,250,250),'L':(220,40,40)},{'r':(30,30,30),'L':(250,140,40),'O':(250,160,80)}]

BOWSER_ROWS=[
".......rr.W..........",
"......rrrWW..W.......",
".....rrrrGGGWW.......",
"....rrrrGGGGGGG......",
"...WrrrGGGGGWKGG.....",
"..WgWrGGGGGGWKGGGG...",
".WgggWGGGGGGGGGGGGG..",
"WgggggWGGGGGGGGGGGKG.",
"gWgggWgGGGGGGGGGGGGG.",
"ggWgWggGGGGGWWWWWWWW.",
"gggWgggyGGGGGGGGGGG..",
"gWgggWgyyGGGGGGGGG...",
"WgggggWyyyyGGGG......",
"gWgggWgyyyyyGGGWW....",
"ggWgWggyyyyyyG.......",
"ggggggyyyyyyyy.......",
"WWWWWWWyyyyyyy.......",
".gGGGGGGyyyyyG.......",
".GGGGGG..GGGGG.......",
".GGGGG....GGGG.......",
"WGGGGW....WGGGGW.....",
"WWWWW......WWWWW.....",]
BOWSER={'idle':S(BOWSER_ROWS)}
_roar=list(BOWSER_ROWS)
_roar[9] ="ggWgWggGGGGGWWWWWWWWW"
_roar[10]="gggWgggyGGGGrrrrrrrr."
_roar[11]="gWgggWgyyGGGrrrrrr..."
_roar[12]="WgggggWyyyyGGWWWWW..."
BOWSER['roar']=S(_roar)
BOWSER_PAL={'y':(232,196,110)}
BX=150                                            # Bowser's home spot (feet centre)

# --- stage geometry ------------------------------------------------------------------------------
BR0,BR1=36,164                                    # bridge span (16 tiles of 8 px)
TILES=[(x,x+7) for x in range(BR1-8,BR0-1,-8)]    # index 0 = right-most (collapses first)
AXE_X=179
BLOCKS={1:(52,25),2:(72,25)}                      # "?" blocks: top-left (9x9)
COLLAPSE=192

register_bg(THEME, lambda v: (0,0,0), clip_ground=True)

def _lava_col(x,f):
    k=(x+f//3)%10
    return (250,150,40) if k==0 else ((200,60,16) if k in (1,9) else (150,30,10))

@fx('mario_stage')
def _fx_stage(d,im,e,f):
    """Stone floor, bridge (tiles gone after `gone` of them collapsed), lava strip, axe + chain."""
    _,gone,axe=e
    for x in range(W):
        c=_lava_col(x,f); d.point((x,63),fill=c); d.point((x,62),fill=tuple(v*2//3 for v in c))
    for x0,x1 in ((0,BR0-1),(BR1,W-1)):           # castle stone at both ends
        d.rectangle([x0,59,x1,63],fill=(70,66,78))
        for x in range(x0,x1,6): d.line([x,59,x,63],fill=(40,36,46))
        d.line([x0,61,x1,61],fill=(40,36,46)); d.line([x0,59,x1,59],fill=(110,106,120))
    for i,(x0,x1) in enumerate(TILES):
        if i<gone: continue
        d.rectangle([x0,59,x1,61],fill=(200,76,12)); d.line([x0,59,x1,59],fill=(252,152,56))
        d.point((x1,60),fill=(90,30,0)); d.point((x1,61),fill=(90,30,0)); d.point((x0+3,60),fill=(120,44,4))
    if axe:
        for k in range(6): d.point((BR1-1+k*2,58-k*2),fill=(150,150,160))                   # chain
        d.line([AXE_X,44,AXE_X,58],fill=(150,90,40)); d.line([AXE_X+1,44,AXE_X+1,58],fill=(110,60,24))
        d.polygon([(AXE_X-1,43),(AXE_X-6,40),(AXE_X-7,46),(AXE_X-6,52),(AXE_X-1,49)],fill=(200,200,214),outline=(90,90,104))
        d.line([AXE_X-5,42,AXE_X-5,50],fill=(250,250,255))

@fx('mario_block')
def _fx_block(d,im,e,f):
    _,x,y,used=e
    if used:
        d.rectangle([x,y,x+8,y+8],fill=(150,80,30),outline=(70,30,6))
    else:
        c=[(252,152,56),(252,152,56),(220,120,40),(180,90,30)][(f//5)%4]
        d.rectangle([x,y,x+8,y+8],fill=c,outline=(110,40,0))
        text(d,"?",x+3,y+2,(110,40,0),shadow=None)
    for cx,cy in ((x+1,y+1),(x+7,y+1),(x+1,y+7),(x+7,y+7)): d.point((cx,cy),fill=(70,30,6))

@fx('mario_flame')
def _fx_flame(d,im,e,f):
    """Bowser's fire breath, travelling left: red tail, orange body, yellow-white tip."""
    _,x,y=e; x,y=int(x),int(y); w=(f%2)
    d.ellipse([x,y-2-w,x+20,y+2+w],fill=(210,50,16))
    d.ellipse([x,y-2,x+13,y+2],fill=(252,152,56))
    d.ellipse([x,y-1,x+6,y+1],fill=(255,240,170))
    for k in range(3): d.point((x+14+k*3,y+((f+k)%3)-1),fill=(252,120,40))

@fx('mario_hammer')
def _fx_hammer(d,im,e,f):
    _,x,y=e; a=f*0.9+x*0.1; ca,sa=math.cos(a),math.sin(a)
    d.line([x-ca*3,y-sa*3,x+ca*2,y+sa*2],fill=(170,110,50))
    hx,hy=x+ca*3,y+sa*3; d.rectangle([hx-1,hy-1,hx+1,hy+1],fill=(190,190,204))

@fx('mario_coin')
def _fx_coin(d,im,e,f):
    _,x,y=e; w=int(abs(math.cos(f*0.9))*2.5)
    d.ellipse([x-w,y-3,x+w,y+3],fill=(250,200,40),outline=(170,110,10))

def _star_poly(cx,cy,R,r,rot=0.0):
    return [(cx+math.cos(rot-math.pi/2+k*math.pi/5)*(R if k%2==0 else r),
             cy+math.sin(rot-math.pi/2+k*math.pi/5)*(R if k%2==0 else r)) for k in range(10)]
STAR_COLS=[(252,216,60),(255,250,200),(252,152,56),(252,216,60)]

@fx('mario_star')
def _fx_star(d,im,e,f):
    _,x,y,R=e
    d.polygon(_star_poly(x,y,R,R*0.45),fill=STAR_COLS[(f//2)%4],outline=(150,90,10))
    ey=int(y-R*0.1); d.line([x-2,ey,x-2,ey+2],fill=(20,14,12)); d.line([x+1,ey,x+1,ey+2],fill=(20,14,12))

@fx('mario_splash')
def _fx_splash(d,im,e,f):
    _,x,t=e; rr=random.Random(int(x))
    for k in range(10):
        vx=rr.uniform(-1.6,1.6); vy=rr.uniform(2.5,4.5); tt=t*10
        px,py=x+vx*tt,62-vy*tt+0.35*tt*tt
        if py<63: d.rectangle([px,py,px+1,py+1],fill=(250,150,40) if k%2 else (220,60,16))

# --- HUD ----------------------------------------------------------------------------------------
def _hud_values(f):
    if f>=270: return 12300,7,400                 # reset behind the black intro screen
    score=12300+200*(f>=80)+1000*(f>=150)+5000*(f>=208)
    t=400-min(f,COLLAPSE)//8                     # the clock stops at the axe
    return score,7+(f>=80),t

@fx('mario_hud')
def _fx_hud(d,im,e,f):
    score,coins,t=_hud_values(f); c=(228,228,236)
    text(d,"CLAUDE",3,1,c); text(d,f"{score:06d}",3,7,c)
    d.ellipse([54,7,56,11],fill=(250,200,40)); text(d,f"X{coins:02d}",59,7,c)
    text(d,"WORLD",96,1,c); text(d,"8-4",100,7,c)
    text(d,"TIME",164,1,c); text(d,f"{t:3d}",166,7,c)

def closeup_block(t,f):
    """Primer plano: the "?" block smacked from below by Mario's cap; the Super Star rises out."""
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    for y in range(28,64,6):                      # dim castle bricks framing the block
        for x in range((y//6)%2*6-6,W,12):
            if 74<=x+10 and x<=110: continue
            d.rectangle([x,y,x+10,y+4],fill=(40,36,46))
    hit=0.16
    bump=-int(6*math.sin(math.pi*min(1,max(0,(t-hit)/0.12)))) if t>=hit else 0
    x0,y0=80,24+bump
    if t>=0.3:                                    # the star climbs out (drawn under the block)
        up=ease((t-0.3)/0.3); sy=int(lerp(y0+12,11,up)); bob=int(math.sin(f*0.5)*1.5) if t>0.6 else 0
        d.polygon(_star_poly(92,sy+bob,11,5),fill=STAR_COLS[(f//2)%4],outline=(150,90,10))
        d.rectangle([88,sy+bob-3,89,sy+bob+1],fill=(20,14,12)); d.rectangle([95,sy+bob-3,96,sy+bob+1],fill=(20,14,12))
    used=t>=hit+0.1
    body=(150,80,30) if used else [(252,152,56),(252,152,56),(220,120,40)][(f//4)%3]
    d.rectangle([x0,y0,x0+24,y0+24],fill=body,outline=(70,30,6))
    d.rectangle([x0+1,y0+1,x0+23,y0+1],fill=(252,200,120) if not used else (180,110,50))
    for cx,cy in ((x0+2,y0+2),(x0+21,y0+2),(x0+2,y0+21),(x0+21,y0+21)): d.rectangle([cx,cy,cx+1,cy+1],fill=(70,30,6))
    if not used:
        m=Image.new('L',(3,5),0); text(ImageDraw.Draw(m),"?",0,0,255,shadow=None)
        m=m.resize((9,15),Image.NEAREST); im.paste((110,40,0),(x0+8,y0+5),m)
    # Mario's cap punching up from below, then dropping away
    cy=int(lerp(70,y0+25,t/hit)) if t<hit else int(lerp(y0+25,76,(t-hit)/0.2))
    if cy<64:
        d.ellipse([74,cy,110,cy+30],fill=(220,40,40),outline=(120,16,16))
        d.ellipse([86,cy+4,98,cy+14],fill=(250,250,250)); text(d,"M",91,cy+7,(220,40,40),shadow=None)
    if hit<=t<hit+0.1:
        for sx in (78,106): spark(d,sx,y0+24,4)
    if t>0.6:
        rr=random.Random(f//3)
        for _ in range(4):
            a=rr.random()*6.28; r=rr.randint(16,24); FX['twinkle'](d,im,('twinkle',92+math.cos(a)*r*1.4,20+math.sin(a)*r*0.6,2),f)
        text(d,"SUPER",130,16,(252,216,60)); text(d,"STAR!",134,23,(252,216,60))
    if t<0.06:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    return im

def intro_screen(f):
    """The black level-intro card: WORLD 8-4, Claude x 3."""
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    FX['big'](d,im,('big',"WORLD 8-4",20,(236,236,242)),f)
    draw(im,MARIO['guard'],80,50,False)
    text(d,"X  3",94,42,(236,236,242))
    _fx_hud(d,im,('mario_hud',),f)
    return im

def jump(f,f0,dur,h): return GROUND-h*math.sin(math.pi*max(0,min(1,(f-f0)/dur)))
def walk(f): return 'dash' if (f//3)%2 else 'guard'

HAMMERS=[(64,98),(76,108),(88,92)]                 # (throw frame, landing x)
def hammer_pos(f,t0,xl):
    t=(f-t0)/20; x=lerp(BX-12,xl,t); y=GROUND-22-30*t+46*t*t
    return x,y

def clip_castle(f):
    s=scene(f,THEME)
    reset=f>=270
    bx=BX+3*math.sin(2*math.pi*f/60)             # Bowser paces on the bridge (period divides N)
    cl=actor(MARIO[guard_pose(f)],30); bw=actor(BOWSER['idle'],bx,flip=True,pal=BOWSER_PAL)
    gone=0 if (reset or f<COLLAPSE) else min(len(TILES),int((f-COLLAPSE)/1.5)+1)
    axe=reset or f<COLLAPSE
    used1=(not reset) and f>=80; used2=(not reset) and f>=106
    bump=lambda hf: -[1,2,2,1][f-hf] if 0<=f-hf<4 else 0
    s['fx'].append(('mario_stage',gone,axe))
    s['fx'].append(('mario_block',BLOCKS[1][0],BLOCKS[1][1]+bump(80),used1))
    s['fx'].append(('mario_block',BLOCKS[2][0],BLOCKS[2][1],used2))
    if 270<=f<284: s['image']=intro_screen(f); return s

    # 1) fire breath: Claude hops over it
    if 24<=f<34: bw['spr']=BOWSER['roar']
    if 30<=f<62:
        fx_=bx-14-(f-30)*4.5; fy=lerp(46,52,(f-30)/10)
        if fx_>-24: s['fx'].append(('mario_flame',fx_,fy))
    if 44<=f<58: cl.update(spr=MARIO['armsup'],y=jump(f,44,14,18))
    # 2) hammers while Claude goes for the first block
    for t0,xl in HAMMERS:
        if t0<=f<t0+22:
            x,y=hammer_pos(f,t0,xl)
            if y<GROUND+1: s['fx'].append(('mario_hammer',x,y))
    if 62<=f<74: cl.update(spr=MARIO[walk(f)],x=lerp(30,56,(f-62)/12))
    if 74<=f<92: cl['x']=56
    if 74<=f<86: cl.update(spr=MARIO['armsup'],y=jump(f,74,12,12))
    if 80<=f<92: s['fx'].append(('mario_coin',56,BLOCKS[1][1]-4-int(16*math.sin(math.pi*(f-80)/12))))
    if 90<=f<104: s['fx'].append(('dmg',"200",51,int(lerp(20,14,(f-90)/14)),(236,236,242)))
    if 92<=f<100: cl.update(spr=MARIO[walk(f)],x=lerp(56,76,(f-92)/8))
    if 100<=f<106: cl.update(spr=MARIO['armsup'],x=76,y=jump(f,100,12,12))
    # 3) close-up: the "?" block and the Super Star
    if 106<=f<142: s['image']=closeup_block((f-106)/36,f); return s
    star=None
    if 142<=f<150:
        t=(f-142)/8; cl.update(x=lerp(76,84,t),spr=MARIO[walk(f)])
        star=(lerp(76,86,t),lerp(18,GROUND-8,t*t)-6*math.sin(math.pi*t))
    if 142<=f<146: s['fx'].append(('twinkle',80,20,2))
    if star: s['fx'].append(('mario_star',star[0],star[1],5))
    if 150<=f<156:
        cl['x']=84
        for k in range(5): a=k*1.26+f*0.3; s['fx'].append(('twinkle',84+math.cos(a)*10,GROUND-8+math.sin(a)*7,2))
    if 150<=f<164: s['fx'].append(('dmg',"1000",78,int(lerp(38,30,(f-150)/14)),(252,216,60)))
    starred=150<=f<COLLAPSE
    # 4) invincible dash through the fire, vault over Bowser, grab the axe
    if 150<=f<160: bw['spr']=BOWSER['roar']
    if 156<=f<168:
        fx_=bx-14-(f-156)*5
        if fx_>cl['x']+2: s['fx'].append(('mario_flame',fx_,lerp(46,52,(f-156)/8)))
    if 156<=f<168: cl.update(spr=MARIO['dash'],x=lerp(84,116,(f-156)/12))
    if 163<=f<167: s['fx'].append(('spark',cl['x']+7,GROUND-8,4))
    if 168<=f<186: cl.update(spr=MARIO['armsup'],x=lerp(116,170,(f-168)/18),y=jump(f,168,18,34))
    if 186<=f<270: cl['x']=170
    if 190<=f<194: cl['spr']=MARIO['punch']
    if f==COLLAPSE: s['fx'].append(('spark',AXE_X-3,48,5))
    if starred:
        cl['pal']=STAR_PALS[(f//2)%4]
        if f%3==0: s['fx'].append(('twinkle',cl['x']+((f*7)%13)-6,cl['y']-4-((f*5)%11),1))
    # 5) the bridge falls, and so does Bowser
    if COLLAPSE<=f<270:
        bw['x']=bx=BX+3*math.sin(2*math.pi*COLLAPSE/60)
        bw['spr']=BOWSER['roar']
        if f<200: bw['x']=bx+((f%2)*2-1)
        else:
            bw['y']=GROUND+0.35*(f-200)**2
            bw['vis']=bw['y']<GROUND+26
    if 208<=f<224: s['fx'].append(('mario_splash',BX,(f-208)/16)); s['shake']=rshake(1) if f<212 else (0,0)
    if 208<=f<222: s['fx'].append(('dmg',"5000",BX-8,int(lerp(46,38,(f-208)/14)),(236,236,242)))
    if 214<=f<222: cl['spr']=MARIO['armsup']
    if 220<=f<262:
        W1="THANK YOU CLAUDE!"
        s['fx'].append(('dmg',W1,W//2-len(W1)*2-6,36,(236,236,242)))
        if f>=236:
            for i,ln in enumerate(("BUT OUR PRINCESS IS","IN ANOTHER CASTLE!")):
                s['fx'].append(('dmg',ln,W//2-len(ln)*2-6,45+i*7,(236,236,242)))
    # 6) fade to the black intro card, then back to the bridge for the loop
    if 262<=f<270: s['fx'].append(('dim',(f-262)/8))
    if 284<=f<292: s['fx'].append(('dim',1-(f-284)/8))
    s['fx'].append(('mario_hud',))
    s['actors']=[bw,cl]
    return s

CLIPS = [clip('castle', N_, clip_castle)]
