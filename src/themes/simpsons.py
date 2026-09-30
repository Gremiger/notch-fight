"""The Simpsons: Claude (a Sector 7G safety inspector: white work shirt, blue pants, two Homer hairs)
vs Mr. Burns in the Springfield Nuclear Power Plant control room. Burns presses a button — ALERTA,
a glowing green uranium rod pops out of the core — D'OH! — MELTDOWN! Close-up: Burns steepling his
fingers, "EXCELENTE...". He releases the hounds; Claude punches them away, stomps the rod back into
the core (the shockwave blows Burns across the room), and eats a donut: MMM... ROSQUILLAS."""
from engine import *

THEME = 'simpsons'
N_ = 288
CORE_X = 95                         # the rod hatch in the middle of the floor
CL_X, BU_X = 30, 158                # neutral positions

# ---- text: the engine font lacks ' and the inverted !, so this theme carries both ------------
_GLYPHS = dict(FONT); _GLYPHS.update({"'": "010010000000000", '¡': "010000010010010"})

def _txt(d,txt,x,y,c,shadow=(0,0,0)):
    for i,ch in enumerate(txt):
        for j,b in enumerate(_GLYPHS.get(ch,_GLYPHS[' '])):
            if b=='1':
                px,py=x+i*4+j%3,y+j//3
                if shadow: d.point((px+1,py+1),fill=shadow)
                d.point((px,py),fill=c)

def _panel(im,box):
    """A dark translucent strip behind a line of text, so it reads over the busy room."""
    x0,y0,x1,y1=[int(v) for v in box]; x0,y0=max(0,x0),max(0,y0); x1,y1=min(W,x1),min(H,y1)
    im.paste(Image.blend(im.crop((x0,y0,x1,y1)),Image.new('RGB',(x1-x0,y1-y0),(8,10,8)),0.7),(x0,y0))

def _big(im,txt,y,c,scale=2,cx=W//2,outline=None,panel=False):
    m=Image.new('L',(len(txt)*4,6),0); _txt(ImageDraw.Draw(m),txt,0,0,255,shadow=None)
    m=m.resize((m.width*scale,m.height*scale),Image.NEAREST); x=int(cx-m.width//2)
    if panel: _panel(im,(x-4,y-3,x+m.width+3,y+m.height+3))
    if outline is not None:
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): im.paste(outline,(x+dx,y+dy),m)
    im.paste((0,0,0),(x+2,y+2),m); im.paste(c,(x,y),m)

@fx('simp_txt')
def _fx_txt(d,im,e,f):
    _,txt,x,y,c=e
    _panel(im,(x-2,y-2,x+len(txt)*4+1,y+7)); _txt(d,txt,int(x),int(y),c)

@fx('simp_big')
def _fx_big(d,im,e,f):
    _,txt,y,c,cx,outline=e; _big(im,txt,y,c,cx=cx,outline=outline,panel=True)

# ---- sprites ---------------------------------------------------------------------------------
def _worker(x,y,t,l,r,c):
    if c=='.': return None
    inside=l<=x<=r
    if inside and y==t+8: return 'L'                                # belt line of the blue pants
    if inside and t+5<=y<=t+7: return 'e' if (x,y)==(l+2,t+6) else 'W'   # white shirt, pocket protector
    if c=='o' and y>=t+9: return 'L'                                # blue trousers
    return None
def _homer(s): return overlay(recolor_rows(s,_worker),[".k..k..","k.kk.k."],2,0)   # the two hairs
CLS=variant(_homer)
CLPAL={'W':(246,246,240),'L':(70,110,210),'e':(250,120,160),'k':(40,30,26)}

_BU=S([
".....yYYYy.....",
"....YYYYYYY....",
"...hYYYYYYYY...",
"...hYWWYWWYY...",
"...hYWKYWKYYY..",
"....YYYYYYYYYY.",
"....YYYYYYYYYYY",
"....YYYYYYYYYy.",
".....YYkkkYY...",
".....YYYYYY....",
"......YYYY.....",
".....gHTHgg....",
"....gggTTggg...",
"...ggggTggggg..",
"...gggggggYYY..",
"...ggggggg.YY..",
"...gg.gggg.....",
"...YY.gggg.....",
"......gggg.....",
"......gg.g.....",
"......g..g.....",
"......g..g.....",
"......g..g.....",
"......g..g.....",
".....kk.kk.....",])
_BU2=S([(r if i!=14 else "...ggggggggYY..") if i!=15 else "...gggggggYYY.." for i,r in enumerate(_BU)])   # finger tapping
_BU_ATK=S([r for r in _BU[:13]]+["...gggggggggggYY","...ggggTgg......","...gggggggg....."]+[r for r in _BU[16:]])
_BU_FIST=S([r for r in _BU[:12]]+["...gggggggggggYY","...ggggTgg......","...gggggggg.....","...gggggggg....."]+[r for r in _BU[16:]])   # shaking a fist
BU={'idle':_BU,'idle2':_BU2,'attack':_BU_ATK,'fist':_BU_FIST,'hurt':hurt(_BU)}
BU['down']=rotate90(BU['hurt'],3,trim=True)
def bu_idle(f): return BU['idle'] if (f//6)%2==0 else BU['idle2']
BUPAL={'Y':(255,217,15),'y':(214,170,10),'g':(78,128,74),'H':(240,240,236),'T':(140,30,48),
       'K':(20,20,20),'W':(255,255,255),'h':(176,176,184),'k':(34,30,30)}

_DOG=S([
".........kk..",
"k.......kkWk.",
".k......kkkkr",
".kkkkkkkkkk..",
"..kkRkRkkk...",
"..k.k...k.k..",
"..k.k...k.k..",])
_DOG2=S(_DOG[:5]+["..kk....kk...",".k...k.k...k."])
DOG=[_DOG,_DOG2]
DOGPAL={'k':(150,98,60),'W':(255,255,255),'r':(20,10,10),'R':(210,40,40)}

# ---- background ------------------------------------------------------------------------------
def _plant(d):
    d.rectangle([0,0,W,GROUND],fill=(38,70,58))                     # plant-green wall
    for x in range(0,W,16): d.line([x,0,x,GROUND],fill=(32,60,50))
    d.rectangle([0,GROUND-8,W,GROUND],fill=(32,58,48))              # skirting
    d.rectangle([58,6,132,40],fill=(28,42,40))                      # the big window...
    d.rectangle([60,8,130,38],fill=(96,166,226))                    # ...over a Springfield sky
    for i in range(6):
        d.line([60,8+i*5,130,8+i*5],fill=(104,174,232) if i%2 else (92,160,222))
    d.rectangle([60,33,130,38],fill=(80,120,70))
    for tx,tw,top in ((80,8,17),(111,9,14)):
        for yy in range(top,39):                                    # the cooling towers (hyperboloids)
            hw=tw*(0.62+0.38*abs((yy-top)/(38-top)-0.35)/0.65); d.line([tx-hw,yy,tx+hw,yy],fill=(176,176,172))
            d.point((int(tx+hw),yy),fill=(130,130,128))
        d.line([tx-tw*0.62+1,top,tx+tw*0.62-1,top],fill=(210,210,206))
        for k,(sx,sy,r) in enumerate(((0,-3,3),(-3,-6,3),(3,-8,4),(0,-11,3))):   # steam
            d.ellipse([tx+sx-r,top+sy-r,tx+sx+r,top+sy+r],fill=(236,240,244) if k%2 else (220,226,232))
    d.line([95,8,95,38],fill=(28,42,40))                            # window mullion
    # the radiation sign and the SECTOR 7G plate
    d.ellipse([36,10,46,20],fill=(250,210,40)); d.ellipse([39,13,43,17],fill=(30,26,20))
    for a in (90,210,330):
        d.pieslice([37,11,45,19],a-30,a+30,fill=(30,26,20))
    d.ellipse([40,14,42,16],fill=(250,210,40))
    d.rectangle([138,10,168,18],fill=(220,220,210)); text(d,"7G",146,12,(40,60,50),shadow=None)
    # left console (Claude's station) with a pink-box of donuts on top
    d.polygon([(2,GROUND-18),(20,GROUND-18),(22,GROUND-12),(22,GROUND),(2,GROUND)],fill=(150,150,140))
    d.polygon([(3,GROUND-17),(19,GROUND-17),(21,GROUND-12),(3,GROUND-12)],fill=(90,96,94))
    d.rectangle([4,GROUND-10,20,GROUND-1],fill=(120,122,114))
    d.rectangle([5,GROUND-23,17,GROUND-19],fill=(250,150,190)); d.line([5,GROUND-23,17,GROUND-23],fill=(255,200,220))
    for dx in (8,13): d.ellipse([dx-2,GROUND-25,dx+2,GROUND-22],fill=(240,110,170)); d.point((dx,GROUND-24),fill=(120,70,40))
    # right console behind Burns
    d.polygon([(168,GROUND-18),(184,GROUND-18),(184,GROUND),(166,GROUND),(166,GROUND-12)],fill=(150,150,140))
    d.polygon([(169,GROUND-17),(183,GROUND-17),(183,GROUND-12),(167,GROUND-12)],fill=(90,96,94))
    # the core hatch and the alarm beacon
    d.rectangle([CORE_X-10,GROUND-2,CORE_X+10,GROUND],fill=(110,112,106))
    d.rectangle([CORE_X-4,GROUND-2,CORE_X+4,GROUND-1],fill=(30,34,30))
    for hx in (CORE_X-8,CORE_X+7): d.point((hx,GROUND-1),fill=(250,210,40))
    d.rectangle([CORE_X-3,0,CORE_X+3,2],fill=(70,70,70)); d.ellipse([CORE_X-3,1,CORE_X+3,5],fill=(110,30,30))
register_bg(THEME, lambda v: (v+30,v+30,v+26), decor=_plant)

# ---- effects ---------------------------------------------------------------------------------
LIGHTS=[(5,GROUND-15),(8,GROUND-15),(11,GROUND-15),(14,GROUND-15),(17,GROUND-15),(6,GROUND-7),(10,GROUND-7),(14,GROUND-7),(18,GROUND-7),
        (171,GROUND-15),(174,GROUND-15),(177,GROUND-15),(180,GROUND-15),(170,GROUND-7),(174,GROUND-7),(178,GROUND-7),(182,GROUND-7)]

@fx('simp_lights')
def _fx_lights(d,im,e,f):
    """Console lights: calm (slow green/yellow blinking) or alarm (fast red). 12/24-frame cycles."""
    _,alarm=e; rr=random.Random(5)
    for i,(x,y) in enumerate(LIGHTS):
        ph=rr.randint(0,23)
        if alarm: c=(255,50,40) if ((f+ph)//3)%2 else (90,20,20)
        else:
            on=((f+ph)//12)%2==0
            base=(80,230,90) if i%3 else (250,210,60)
            c=base if on else tuple(v//3 for v in base)
        d.rectangle([x,y,x+1,y+1],fill=c)

_GLOW={}
def _glow_mask(r):
    if r not in _GLOW:
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([CORE_X-r,GROUND-10-r//2,CORE_X+r,GROUND-10+r//2],fill=255)
        _GLOW[r]=m.filter(ImageFilter.GaussianBlur(6))
    return _GLOW[r]

@fx('simp_glow')
def _fx_glow(d,im,e,f):
    """Radioactive green light around the core, strength a 0..1."""
    _,a=e
    if a<=0: return
    m=_glow_mask(int(22+10*a)).point(lambda v: int(v*min(1,a)*(0.62+0.08*(f%2))))
    im.paste((120,255,70),(0,0),m)

@fx('simp_rod')
def _fx_rod(d,im,e,f):
    """The uranium rod sticking `out` px out of the hatch, rattling while `hot`."""
    _,out,hot=e
    if out<=0: return
    jx=((f//2)%2)*2-1 if hot else 0; x=CORE_X+jx; top=int(GROUND-2-out)
    d.rectangle([x-3,top,x+3,GROUND-2],fill=(60,160,40))
    d.rectangle([x-2,top,x+2,GROUND-2],fill=(140,255,90)); d.line([x,top+1,x,GROUND-3],fill=(230,255,210))
    d.rectangle([x-3,top-1,x+3,top],fill=(160,170,160))
    if hot:
        rr=random.Random(f)
        for _ in range(3): d.point((x+rr.randint(-7,7),top+rr.randint(-4,int(out))),fill=(200,255,150))

@fx('simp_alarm')
def _fx_alarm(d,im,e,f):
    """The red alarm: beacon lit + a red wash over the room on every other 4-frame beat."""
    on=(f//4)%2==0
    if on:
        im.paste(Image.blend(im,Image.new('RGB',(W,H),(255,20,20)),0.26))
        d.ellipse([CORE_X-3,1,CORE_X+3,5],fill=(255,70,50))
        for k in (-1,1): d.polygon([(CORE_X,3),(CORE_X+k*30,10),(CORE_X+k*26,14)],fill=(150,40,40))
        d.ellipse([CORE_X-3,1,CORE_X+3,5],fill=(255,90,70))

_DONUT=S(["..nnn..",".nynbn.","nnc.cnn",".ccccc.","..ccc.."])
DONUTPAL={'n':(245,110,170),'y':(250,240,90),'b':(120,200,255),'c':(206,146,74)}

@fx('simp_donut')
def _fx_donut(d,im,e,f):
    """A pink-frosted donut with sprinkles; each bite takes two columns off the right."""
    _,x,y,bites=e
    spr=S([r[:7-2*bites] for r in _DONUT]); draw(im,spr,x-bites,y,False,pal=DONUTPAL)

# ---- close-up --------------------------------------------------------------------------------
def closeup_excellent(t,f):
    """Primer plano: Mr. Burns in three-quarter view, lit green from below, the hooked nose
    jutting out, a sinister grin, fingers steepled and tapping — EXCELENTE..."""
    im=Image.new('RGB',(W,H),(10,22,16)); d=ImageDraw.Draw(im)
    skin,shade,line,hair=(255,217,15),(214,166,8),(120,86,6),(176,176,184)
    glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([-10,40,120,110],fill=110)
    im.paste((80,210,60),(0,0),glow.filter(ImageFilter.GaussianBlur(10))); d=ImageDraw.Draw(im)
    d.polygon([(0,64),(14,54),(90,54),(104,64)],fill=(78,128,74))                    # green suit
    d.polygon([(42,54),(52,64),(62,54)],fill=(240,240,236)); d.polygon([(50,56),(54,56),(53,64),(51,64)],fill=(140,30,48))
    d.ellipse([16,-26,88,40],fill=skin,outline=line)                              # the bald dome
    d.polygon([(22,20),(84,20),(78,44),(62,56),(44,56),(28,44)],fill=skin)        # the narrow jaw
    d.line([(28,44),(44,56),(62,56),(78,44)],fill=line); d.line([(22,20),(28,44)],fill=line); d.line([(84,20),(78,44)],fill=line)
    d.arc([22,-20,80,34],200,250,fill=(255,240,150),width=2)                       # shine on the dome
    d.rectangle([14,12,22,30],fill=hair); d.ellipse([10,14,22,30],fill=skin,outline=line)   # grey fringe, ear
    d.line([15,20,17,24],fill=line)
    for ex,w in ((42,7),(66,6)):                                                   # heavy-lidded eyes
        d.ellipse([ex-w,10,ex+w,24],fill=(255,255,255),outline=line)
        d.ellipse([ex+w-6,15,ex+w-2,21],fill=(20,20,20))                            # a sideways, scheming look
        d.chord([ex-w,10,ex+w,24],180,360,fill=shade); d.line([ex-w,17,ex+w,17],fill=line)
    d.polygon([(56,14),(62,14),(98,34),(96,38),(78,40)],fill=shade)                # the huge hooked nose...
    d.polygon([(56,14),(61,14),(96,33),(94,35),(76,37)],fill=skin)
    d.line([(61,14),(97,34),(95,38),(78,40)],fill=line)                            # ...its silhouette
    grin=ease((t-0.2)/0.15)
    if grin>0:                                                                     # the sinister grin
        d.chord([36,38-int(3*grin),76,48],0,180,fill=(70,20,20))
        d.line([40,43-int(3*grin)+3,72,43-int(3*grin)+3],fill=(250,250,240))
        d.line([34,40,38,43],fill=line); d.line([78,38,74,42],fill=line)          # the upturned corners
    else: d.line([42,46,70,46],fill=line)
    tap=(f//3)%2 and t>0.3                                                         # steepled fingers, tapping
    for sgn,px in ((-1,78),(1,106)):                                  # held up in front, under the nose
        d.ellipse([px-9,58,px+9,80],fill=skin,outline=line)
        for i in range(4):
            tipx=92+sgn*(1+(3 if (tap and sgn>0 and i%2) else 0)); tipy=42+i*4
            d.line([px+sgn*(-6+i*4),60,tipx,tipy],fill=line,width=4)
            d.line([px+sgn*(-6+i*4),60,tipx,tipy],fill=skin,width=2)
    for sgn,px in ((-1,78),(1,106)): d.polygon([(px-10,64),(px+10,64),(px+12,H),(px-12,H)],fill=(78,128,74))   # sleeves
    if t>0.3:
        dots=min(3,int((t-0.45)/0.1)+1) if t>0.45 else 0
        _big(im,"EXCELENTE",14,(255,226,90),cx=148,outline=(40,90,40))
        _big(im,"."*dots+" "*(3-dots),30,(255,226,90),cx=160,outline=(40,90,40))
    if t<0.06: zoom_lines(d,(180,255,140))
    if t>0.9: im=fade_to(im,(0,0,0),(t-0.9)/0.1*0.6)
    return im

# ---- the clip --------------------------------------------------------------------------------
def rod_out(f):
    if f<28 or f>=206: return 0
    if f<36: return ease((f-28)/8)*16
    if f<202: return 16
    return lerp(16,0,(f-202)/4)

def glow(f):
    if 28<=f<206: return min(1,(f-28)/10)
    if 206<=f<234: return 1-(f-206)/28
    return 0

def clip_meltdown(f):
    s=scene(f,THEME)
    cl=actor(CLS[guard_pose(f)],CL_X,pal=CLPAL); bu=actor(bu_idle(f),BU_X,flip=True,pal=BUPAL)
    alarm=28<=f<206; out=rod_out(f)
    s['under'].append(('simp_lights',alarm)); s['under'].append(('simp_glow',glow(f)))
    s['under'].append(('simp_rod',out,alarm))
    extra=[]
    # 1) Burns presses the button
    if 16<=f<28:
        bu['spr']=BU['attack']
        if 20<=f<24: s['fx'].append(('twinkle',BU_X-9,GROUND-11,1))
    # 2) the alarm, the rod pops out
    if 28<=f<40: s['shake']=rshake(1 if f>=34 else 2)
    if 30<=f<46 and (f//4)%2==0: s['fx'].append(('simp_big',"ALERTA",10,(255,240,240),W//2,(160,20,20)))
    if 30<=f<42:
        t=(f-30)/12; cl.update(spr=CLS['armsup'],y=GROUND-int(8*math.sin(math.pi*t)))
    if 42<=f<60:
        cl['spr']=CLS['armsup'] if (f//4)%2 else CLS['hurt']
        s['fx'].append(('simp_big',"¡D'OH!",14,(255,217,15),42,(60,40,20)))
    if 60<=f<84:
        if (f//4)%2==0: s['fx'].append(('simp_big',"MELTDOWN!",10,(140,255,90),W//2,(30,80,20)))
        if f%8==0: s['shake']=rshake(1)
    # 3) close-up
    if 84<=f<124:
        s['image']=closeup_excellent((f-84)/40,f); return s
    # 4) the hounds
    if 124<=f<150:
        bu['spr']=BU['attack']
        s['fx'].append(('simp_txt',"SUELTEN A LOS PERROS!",W//2-42,16,(255,226,90)))
    hounds=[]
    for i,(t0,hit) in enumerate(((132,150),(142,164))):
        if t0<=f<hit:
            x=lerp(200,48,(f-t0)/(hit-t0)); hounds.append(actor(DOG[(f//2)%2],x,flip=True,pal=DOGPAL))
            if f%3==0: s['fx'].append(('dust',x+6,GROUND-1))
        if hit<=f<hit+22:
            t=(f-hit)/22; spr=rotate90(DOG[0],(f//3)%4)
            hounds.append(actor(spr,lerp(50,50+140*(1 if i==0 else 0.8),t),GROUND-int((40 if i==0 else 24)*math.sin(math.pi*min(1,t*0.9))),flip=True,pal=DOGPAL))
            if f<hit+3:
                s['fx'].append(('spark',48,GROUND-6,5)); s['shake']=rshake(2)
                s['fx'].append(('simp_txt',"KAPOW!" if i==0 else "ZAS!",36,GROUND-26,(255,255,255)))
    if 146<=f<150 or 158<=f<162: cl['spr']=CLS['charge']
    if 150<=f<156: cl['spr']=CLS['punch']
    if 162<=f<168: cl.update(spr=CLS['dash'],x=CL_X+4)
    # 5) Claude runs to the core, stomps the rod back in; Burns blown away
    if 176<=f<194: cl.update(spr=CLS['dash'],x=ez(CL_X,82,(f-176)/14))
    if 186<=f<206:
        bu.update(spr=BU['fist'] if (f//3)%2 else BU['attack'],x=ez(BU_X,116,(f-186)/12))
        if f<200: s['fx'].append(('simp_txt',"NO! MI PLANTA!",108,10,(255,226,90)))
    if 194<=f<202:                                                   # the jump onto the rod...
        t=(f-194)/8; cl.update(spr=CLS['armsup'],x=lerp(82,CORE_X,t),y=int(lerp(GROUND,GROUND-3-out,t)-10*math.sin(math.pi*t)))
    if 202<=f<206:                                                   # ...stomping it back into the core
        cl.update(spr=CLS['charge'],x=CORE_X,y=int(GROUND-3-out)); s['shake']=rshake(1)
        s['fx'].append(('simp_txt',"PUM!",CORE_X+10,GROUND-30,(255,255,255)))
    if 206<=f<226:
        cl.update(spr=CLS['guard'] if f>=210 else CLS['charge'],x=CORE_X)
        if f==206: s['flash']=0.9; s['fc']=(CORE_X,GROUND-6); s['flashc']=(200,255,170); s['shake']=rshake(2)
        if f<214: s['fx'].append(('ring',CORE_X,GROUND-2,4+(f-206)*6,(170,255,120)))
    if 206<=f<220:
        t=(f-206)/14; bu.update(spr=BU['hurt'],x=ez(116,166,t),y=GROUND-int(16*math.sin(math.pi*t)))
    if 220<=f<248:
        bu.update(spr=BU['down'],x=166); s['fx'].append(('dizzy',160,GROUND-8))
        if f==220: s['fx'].append(('dust',156,GROUND-1)); s['fx'].append(('dust',176,GROUND-1))
    # 6) the core stabilises; back to the console for a donut
    if 226<=f<244: cl.update(spr=CLS[guard_pose(f)],x=ez(CORE_X,CL_X,(f-226)/16))
    if 244<=f<268:
        cl['x']=CL_X
        bites=0 if f<252 else (1 if f<258 else 2)
        s['fx'].append(('simp_donut',CL_X+8,GROUND-6-(2 if f<252 else 4),bites))
        s['fx'].append(('simp_txt',"MMM... ROSQUILLAS",2,20,(250,150,190)))
    if 248<=f<256: bu.update(spr=BU['hurt'],x=166)
    if 256<=f<272: bu.update(spr=bu_idle(f),x=ez(166,BU_X,(f-256)/14))
    if 262<=f<282: s['fx'].append(('simp_txt',"...EXCELENTE.",126,20,(200,210,200)))
    if alarm: s['fx'].insert(0,('simp_alarm',))                     # under the shouts, over the room
    s['actors']=[cl,bu]+hounds+extra
    return s

CLIPS = [clip('meltdown', N_, clip_meltdown)]
