"""JoJo's Bizarre Adventure: Claude (Jotaro-style cap) and his Stand vs DIO and The World.
Menacing standoff, Stand rush ORA vs MUDA, ZA WARUDO stops time (negative sphere, grey world,
close-up of DIO and the stopped clock). DIO walks up to frozen Claude, but Claude moves inside
the stopped time: his colour returns and his Stand's ORA ORA barrage sends DIO flying as time
resumes. DIO walks back for the loop."""
from engine import *
from PIL import ImageOps

THEME = 'jojo'
N_ = 264

# Claude with a Jotaro cap: brim to the front, gold badge
JOTARO=variant(lambda s: overlay(s,["..kkkkkk....",".kkkkYYkkk..","kkkkkkkkkkkk"],-1,0,bangs=".kkkkkkkk"))
# only his eyes (glowing white) — the first thing that moves inside the stopped time
EYES={k:S([''.join('W' if c=='K' else '.' for c in r) for r in v]) for k,v in JOTARO.items()}

DIO=poses(S([
"....YYYYYY......","...YYYYYYYY.....","..YYQYYYYQYY....","..YXXXXXXXY.....","..YQsrssrsQ.....",
"...YsssssY......","....ssVss.......",".....sss........","...yykkkkyy.....","..yyykkkkyyy....",
"..yyQkkkkQyy....","..ss.kkkk.ss....",".....kkkk.......","....yyyyyy......","....yyyyyy......",
"....yy..yy......","....XX..XX......","....yy..yy......","....yy..yy......","...kkk..kkk.....",]),10,'yy',3)

_STAND=[
"....hhhhhh......","...hhhhhhhh.....","...hhhhEhhE.....","...hhhhhhhh.....","....hhhhhh......",
"..bbbbbbbbbb....",".bbbbcbbcbbbb...",".bb.bbbbbb.bb...",".bb.bbccbb.bb...",".ff.bbbbbb.ff...",
"....bbbbbb......","....aaaaaa......","....bbbbbb......","....bb..bb......","....bb..bb......",
"....cc..cc......","....bb..bb......","....bb..bb......","...bbb..bbb.....",]
def _stand(m,fist):
    tr=str.maketrans(m); return poses(S([r.translate(tr) for r in _STAND]),8,fist,1)
STAR=_stand({'h':'O','E':'H','b':'U','c':'p','f':'O','a':'Y'},'UUUUOO')    # Claude's Stand
WORLD=_stand({'h':'Y','E':'H','b':'Q','c':'X','f':'Y','a':'X'},'QQQQYY')   # The World (heart knees)
ST_A=0.7   # Stands are translucent

ORA_C=((217,119,87),(106,58,178))    # Claude's Stand fists: orange, purple streaks
MUDA_C=((250,210,60),(160,110,20))

register_bg(THEME, lambda v: (v//2+8,v//3,v+8))

def _grey(im): return ImageOps.colorize(ImageOps.grayscale(im),(0,0,0),(196,202,232))
def _neg(im): return ImageOps.colorize(ImageOps.invert(ImageOps.grayscale(im)),(30,0,50),(206,176,255))
def _disc(cx,cy,r):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255); return m

@fx('jojo_zawarudo')
def _fx_zawarudo(d,im,e,f):
    """Time stop. 'stop': a negative sphere of radius r grows from (cx,cy), blending to the grey
    stopped world by k (r>=300, k=1 = the whole world grey). 'resume': colour returns inside r."""
    _,mode,cx,cy,r,k=e
    grey=_grey(im)
    if mode=='stop':
        neg=Image.blend(_neg(im),Image.new('RGB',(W,H),(0,0,0)),0.6)   # dimmed: a white panel under the notch is too loud
        inside=Image.blend(neg,grey,k) if k<1 else grey
        im.paste(inside,(0,0),_disc(cx,cy,r))
    else:
        out=grey; out.paste(im,(0,0),_disc(cx,cy,r)); im.paste(out)
    if 0<r<240: d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(255,255,255))

@fx('jojo_live')
def _fx_live(d,im,e,f):
    """Redraw a sprite in colour on top of the stopped (grey) world."""
    _,spr,x,y,flip,alpha=e; draw(im,spr,x,y,flip,alpha=alpha,f=f)

@fx('jojo_fists')
def _fx_fists(d,im,e,f):
    """Stand rush: a cloud of afterimage fists with speed lines, thrown in direction dirn."""
    _,x0,x1,y0,y1,(c,dark),dirn,n,seed=e; rr=random.Random(seed)
    for _ in range(n):
        x=rr.randint(x0,x1); y=rr.randint(y0,y1); L=rr.randint(3,8)
        d.line([x-dirn*(L+2),y,x-dirn*2,y],fill=dark)
        d.rectangle([x-2,y-2,x+2,y+1],fill=(18,12,16)); d.rectangle([x-1,y-1,x+1,y],fill=c)
        d.point((x+dirn,y-1),fill=(255,255,255))

def _go(d,x,y,c):
    """One menacing 'go' (katakana ko + dakuten), 6 px, slanted."""
    for (ox,oy),col in (((1,1),(18,6,24)),((0,0),c)):
        X,Y=x+ox,y+oy
        d.line([X+1,Y,X+6,Y],fill=col); d.line([X+6,Y,X+5,Y+6],fill=col); d.line([X,Y+6,X+5,Y+6],fill=col)
        d.line([X+1,Y+1,X+5,Y+1],fill=col); d.line([X,Y+5,X+5,Y+5],fill=col)
        d.point((X+8,Y-2),fill=col); d.point((X+8,Y-1),fill=col); d.point((X+10,Y-2),fill=col); d.point((X+10,Y-1),fill=col)

MENACE=[(4,20),(12,31),(3,42),(166,18),(174,29),(165,40)]
@fx('jojo_menace')
def _fx_menace(d,im,e,f):
    """ゴゴゴ: menacing glyphs beside both fighters, pulsing on a 12-frame cycle (loop-safe)."""
    for i,(x,y) in enumerate(MENACE):
        ph=(f+i*4)%12
        c=(220,130,255) if ph<6 else (150,70,210)
        _go(d,x+(1 if ph in (2,3) else 0),y-(1 if ph<6 else 0),c)

def closeup_dio(t,f):
    """Primer plano: DIO's grin next to a clock whose hands race, then stop — TOKI WO TOMARE."""
    im=Image.new('RGB',(W,H),(12,6,18)); d=ImageDraw.Draw(im)
    skin,shade,hair,hair2=(240,204,168),(206,160,126),(250,214,70),(200,150,36)
    d.polygon([(22,0),(126,0),(136,34),(122,62),(112,24),(40,24),(30,62),(14,34)],fill=hair2)
    d.polygon([(30,0),(120,0),(128,22),(116,38),(36,38),(24,22)],fill=hair)
    d.polygon([(44,14),(108,14),(106,44),(92,60),(60,60),(46,44)],fill=skin)
    d.polygon([(44,14),(52,14),(56,46),(62,60),(46,44)],fill=shade)
    d.rectangle([38,11,114,16],fill=(40,150,95))                                  # headband
    hx=76; d.polygon([(hx-6,10),(hx-3,8),(hx,11),(hx+3,8),(hx+6,10),(hx,18)],fill=(90,210,140))   # its heart
    for x in (46,56,92,102): d.polygon([(x,15),(x+8,15),(x+3,25)],fill=hair)     # fringe over the band
    d.polygon([(54,27),(71,31),(71,33),(54,30)],fill=(150,100,20))                # angry brows
    d.polygon([(81,31),(98,27),(98,30),(81,33)],fill=(150,100,20))
    for ex,ey in ((63,35),(90,35)):
        d.polygon([(ex-8,ey-1),(ex+7,ey),(ex+5,ey+3),(ex-6,ey+2)],fill=(250,246,236))
    d.line([(76,36),(73,46),(78,47)],fill=shade)
    d.polygon([(62,50),(90,50),(85,55),(67,55)],fill=(80,20,50)); d.line([(64,51),(88,51)],fill=(250,246,236))
    d.line([(62,50),(90,50)],fill=(120,50,140))
    cx,cy,r=154,28,24   # the clock
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(232,222,190),outline=(160,116,40),width=2)
    for k in range(12):
        a=k*math.pi/6; d.line([cx+math.cos(a)*(r-5),cy+math.sin(a)*(r-5),cx+math.cos(a)*(r-2),cy+math.sin(a)*(r-2)],fill=(60,40,30))
    stop=t>=0.45; ft=f if not stop else 0
    am=(ft*0.55 if not stop else -1.2); ah=am/12-0.6
    d.line([cx,cy,cx+math.cos(am)*(r-6),cy+math.sin(am)*(r-6)],fill=(30,20,20),width=1)
    d.line([cx,cy,cx+math.cos(ah)*(r-12),cy+math.sin(ah)*(r-12)],fill=(30,20,20),width=2)
    d.ellipse([cx-2,cy-2,cx+2,cy+2],fill=(160,116,40))
    if stop:   # time stops: negative flash, then grey — only DIO's eyes stay red
        k=min(1,(t-0.45)/0.1); im.paste(Image.blend(_neg(im),_grey(im),k)); d=ImageDraw.Draw(im)
    for ex,ey in ((63,35),(90,35)): d.rectangle([ex-2,ey,ex+1,ey+2],fill=(220,30,40))
    if t>=0.5:
        d.rectangle([0,55,W,H],fill=(0,0,0)); text(d,"TOKI WO TOMARE!",W//2-30,57,(255,226,90))
    if t<0.06:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    if t>0.9: im=Image.blend(im,Image.new('RGB',(W,H),(0,0,0)),(t-0.9)/0.1*0.6)
    return im

# debris from the Stand clash: flies from the middle, freezes when time stops, resumes after
_DEBRIS=[(random.Random(i).uniform(-2.2,2.2),random.Random(i*5+3).uniform(-1.6,0.6)) for i in range(10)]
T_STOP,T_GO=100,222
def debris(s,f):
    if not (84<=f<250): return
    tau=(f-84) if f<T_STOP else (T_STOP-84 if f<T_GO else T_STOP-84+(f-T_GO))
    for i,(vx,vy) in enumerate(_DEBRIS):
        x=93+vx*tau; y=GROUND-18+vy*tau+0.04*tau*tau
        if 0<=x<W and 0<=y<GROUND:
            s['under'].append(('spark',x,y,1) if i%3==0 else ('shard',x,y,(255,236,150) if i%2 else (220,150,255)))

def clip_theworld(f):
    s=scene(f,THEME)
    cl=actor(JOTARO[guard_pose(f)],30); dio=actor(DIO['idle'],150,flip=True)
    sp=actor(STAR['idle'],24,GROUND-3,alpha=ST_A,vis=False)
    tw=actor(WORLD['idle'],162,GROUND-3,flip=True,alpha=ST_A,vis=False)
    stop=None   # time-stop fx tuple, inserted before every colour (live) fx
    # 1) menacing standoff (also the loop keyframe)
    if f<30 or f>=244: s['under'].append(('jojo_menace',f))
    # 2) the Stands appear
    if 24<=f<44:
        t=(f-24)/20; sp.update(vis=True,alpha=ST_A*t,y=GROUND-3*t); tw.update(vis=True,alpha=ST_A*t,y=GROUND-3*t)
        if f<32: cl['spr']=JOTARO['punch']; dio['spr']=DIO['attack']
        if f<30: callout(s,"STAND!",y=2,c=(220,130,255))
    # rush: ORA ORA vs MUDA MUDA, fists clashing in the middle
    if 44<=f<84:
        t=(f-44)/8; hit=(f//2)%2
        sp.update(vis=True,x=ez(24,76,t),spr=STAR['attack' if hit else 'idle'])
        tw.update(vis=True,x=ez(162,110,t),spr=WORLD['idle' if hit else 'attack'])
        if f>=50:
            s['fx'].append(('jojo_fists',80,94,GROUND-24,GROUND-8,ORA_C,1,9,f*7))
            s['fx'].append(('jojo_fists',92,106,GROUND-24,GROUND-8,MUDA_C,-1,9,f*7+3))
            rr=random.Random(f); s['fx'].append(('spark',93+rr.randint(-2,2),GROUND-rr.randint(9,23),rr.choice((2,3,4))))
            if f%3==0: s['shake']=rshake()
            s['fx'].append(('dmg',"ORA ORA ORA!",4,2,(220,130,255))); s['fx'].append(('dmg',"MUDA MUDA MUDA!",W-62,2,(255,220,80)))
    # 3) ZA WARUDO
    if 84<=f<94:
        t=(f-84)/6; sp.update(vis=True,x=ez(76,40,t)); tw.update(vis=True,x=ez(110,162,t),spr=WORLD['idle'])
        if f==84: s['flash']=0.8; s['fc']=(93,GROUND-16); s['shake']=rshake(2)
    if 88<=f<112:
        dio['spr']=DIO['attack']; dio['aura']=((250,210,60),1+(f%2))
        s['fx'].append(('big',"ZA WARUDO!",20,(255,220,80)))
    if 94<=f<T_STOP:   # Claude sends his Stand again... and it freezes mid-dash
        sp.update(vis=True,x=lerp(40,58,(f-94)/6),spr=STAR['attack']); tw.update(vis=True,spr=WORLD['attack'])
    if T_STOP<=f<T_GO:   # the stopped world: Claude and his Stand frozen as they were at T_STOP
        cl['spr']=JOTARO['guard']; sp.update(vis=True,x=58,spr=STAR['attack']); tw.update(vis=True,spr=WORLD['attack'])
        s['under'].append(('jojo_fists',60,72,GROUND-20,GROUND-10,ORA_C,1,5,T_STOP))
        if f<110: stop=('jojo_zawarudo','stop',150,GROUND-14,(f-T_STOP)*24,0)
        elif f<116: stop=('jojo_zawarudo','stop',150,GROUND-14,999,(f-110)/6)
        else: stop=('jojo_zawarudo','stop',150,GROUND-14,999,1)
    debris(s,f)
    # close-up: DIO, the clock stops
    if 116<=f<148: s['image']=closeup_dio((f-116)/32,f); return s
    # DIO walks up to the frozen Claude (The World behind him)
    if 148<=f<176:
        x=ez(150,92,(f-148)/26); dio.update(x=x,y=GROUND-((f//3)%2)); tw.update(x=x+12)
        if f<170: s['fx'].append(('dmg',"KONO DIO DA!",W//2+14,10,(255,220,80)))
    if 176<=f<T_GO: dio['x']=92; tw['x']=104
    # 4) ...but Claude moves in stopped time
    live=[]
    if 176<=f<184: live.append(('jojo_live',EYES['guard'],30,GROUND,False,1.0 if (f//2)%2 else 0.6))
    if 184<=f<T_GO:
        cl['vis']=sp['vis']=False
        live.append(('jojo_live',JOTARO['punch' if f>=188 else 'guard'],30,GROUND,False,1.0))
    if 184<=f<200:
        dio.update(x=92+(1 if f>=186 else 0)); s['fx'].append(('dmg',"!?",dio['x']-3,GROUND-28,(255,90,90)))
        if f<188: live.append(('jojo_live',STAR['idle'],58,GROUND-3,False,ST_A))
    if 188<=f<T_GO:   # the barrage
        hit=(f//2)%2; sx=ez(58,74,(f-188)/4)
        live.append(('jojo_live',STAR['attack' if hit else 'idle'],sx,GROUND-3,False,0.8))
        if f>=192:
            live.append(('jojo_fists',78,92,GROUND-22,GROUND-6,ORA_C,1,10,f*11))
            rr=random.Random(f*3); live.append(('spark',88+rr.randint(0,8),GROUND-rr.randint(6,20),rr.choice((2,3))))
            dio.update(spr=DIO['hurt'],x=94+(1 if hit else -1)); s['shake']=rshake(1) if f%2 else (0,0)
            if f<218: live.append(('big',"ORA ORA ORA!",22,(220,130,255)))
    # final ORA! — time resumes, DIO flies off to the right
    if T_GO-4<=f<T_GO:
        live.append(('big',"ORA!",22,(255,160,90)))
        s['flash']=0.4; s['fc']=(96,GROUND-14); s['flashc']=(255,240,255)
    if T_GO<=f<T_GO+10: stop=('jojo_zawarudo','resume',96,GROUND-14,(f-T_GO)*24,0)
    if T_GO<=f<240:
        t=(f-T_GO)/16; dio.update(spr=DIO['hurt'],x=ez(94,215,t),y=GROUND-int(16*math.sin(math.pi*min(1,t))))
        if f<T_GO+10: callout(s,"ORA!",y=22,c=(255,160,90)); s['fx'].append(('spark',dio['x']-6,dio['y']-10,4)); s['shake']=rshake(2)
        cl['spr']=JOTARO['punch'] if f<T_GO+10 else JOTARO[guard_pose(f)]
        sp.update(vis=True,spr=STAR['attack'] if f<T_GO+8 else STAR['idle'],x=ez(74,24,(f-T_GO-8)/12),alpha=ST_A*max(0,1-max(0,f-T_GO-10)/8))
        tw.update(vis=f<T_GO+6,x=108,alpha=ST_A*(1-(f-T_GO)/6))
    if T_GO<=f<T_GO+10:   # during the colour wave the live overlays are no longer needed
        cl['vis']=True
    # 5) DIO walks back for the loop
    if 240<=f<254: dio.update(spr=DIO['idle'],x=ez(200,150,(f-240)/14),y=GROUND-((f//3)%2) if f<252 else GROUND)
    s['actors']=[sp,tw,cl,dio]
    if stop: s['fx']=[stop]+live+s['fx']
    else: s['fx']=live+s['fx']
    return s

CLIPS = [clip('theworld', N_, clip_theworld)]
