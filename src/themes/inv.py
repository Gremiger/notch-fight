"""Invincible: Claude (Mark) vs Omni-Man. Omni-Man grabs him, flies him over the city and holds him
in front of an incoming train; then the close-up — "PIENSA CLAUDE!" — and the beatdown. Omni-Man
leaves, Claude heals (Viltrumite) and floats back up for the loop."""
from engine import *

THEME = 'inv'
N_ = 300
FLOAT = GROUND-6   # both hover over the city in the neutral pose

def _mark(beaten):
    def fn(x,y,t,l,r,c):
        if c=='.': return None
        inside=l<=x<=r
        if inside and y in (t,t+1): return 'L'                         # blue cowl
        if c=='K': return 'W'                                          # white mask lenses
        if c=='o': return 'L'                                          # blue gloves / boots
        if inside and t+4<=y<=t+8: return 'L' if x in (l,r) else ('r' if beaten and (x*3+y)%5==0 else 'Y')
        if beaten and c=='O' and (x+y*2)%4==0: return 'r'              # bruises
        return None
    return fn
MARK=variant(lambda s: recolor_rows(s,_mark(False)))
BEAT=variant(lambda s: recolor_rows(s,_mark(True)))

OMNI=poses(S([
"....kkkkkk......","...kkkkkkkk.....","...kssssssk.....","...sKsssKss.....","...ssssssss.....",
"...skkkkkks.....","....ssssss......","..WWWWWWWWWW....",".WWWWrrWWWWWW...",".WW.WrrWWW.WW...",
".WW.WWWWWW.WW...",".rr.rrrrrr.rr...","....WWWWWW......","....WWWWWW......","....WW..WW......",
"....WW..WW......","....rr..rr......","...rrr..rrr.....",]),9,'rr',3)

def _city(d):
    rr=random.Random(17); x=0
    while x<W:
        w=rr.randint(10,20); h=rr.randint(14,34)
        d.rectangle([x,GROUND-h,x+w-2,GROUND],fill=(16,18,34))
        for wy in range(GROUND-h+3,GROUND-2,4):
            for wx in range(x+2,x+w-3,3):
                if rr.random()<0.3: d.point((wx,wy),fill=(90,80,40))
        x+=w
register_bg(THEME, lambda v: (v//2+4,v//2+4,v+10), decor=_city)

@fx('inv_cape')
def _fx_cape(d,im,e,f):
    """Omni-Man's red cape, flowing behind his shoulders (dirn = the way he faces)."""
    _,x,feet,dirn,flying=e; x,feet=int(x),int(feet); sx=x-dirn*3; top=feet-11
    wave=(f//3)%2
    tail=[(sx-dirn*(8 if flying else 3),top+(3 if flying else 11)+wave),(sx-dirn*(10 if flying else 4),top+(6 if flying else 12))]
    d.polygon([(sx,top),(sx+dirn*2,top)]+tail,fill=(170,24,30))

@fx('inv_wind')
def _fx_wind(d,im,e,f):
    _,x,y,dirn=e; rr=random.Random(f)
    for _ in range(6):
        yy=y+rr.randint(-10,6); L=rr.randint(6,16); x0=x-dirn*rr.randint(8,20)
        d.line([x0,yy,x0-dirn*L,yy],fill=(210,220,240))

@fx('inv_train')
def _fx_train(d,im,e,f):
    """An elevated commuter train (3 cars) whose front is at x, running left to right."""
    _,x=e; x=int(x); y0,y1=GROUND-15,GROUND-2
    d.line([0,GROUND-1,W,GROUND-1],fill=(70,70,84))
    for k in range(3):
        cx1=x-k*44; cx0=cx1-42
        d.rectangle([cx0,y0,cx1,y1],fill=(150,156,170),outline=(90,94,108))
        d.line([cx0,y0+9,cx1,y0+9],fill=(200,60,60))
        for wx in range(cx0+3,cx1-3,6): d.rectangle([wx,y0+3,wx+3,y0+6],fill=(250,220,120))
    d.rectangle([x-3,y0+3,x,y0+7],fill=(40,60,90)); d.rectangle([x,y0+10,x+1,y0+11],fill=(255,255,200))

def closeup_think(t,f):
    """Primer plano: Omni-Man, bloodied and furious — PIENSA CLAUDE!"""
    im=Image.new('RGB',(W,H),(6,6,14)); d=ImageDraw.Draw(im)
    d.rectangle([44,0,140,64],fill=(232,190,160))                               # face
    d.polygon([(40,0),(144,0),(144,12),(128,8),(110,14),(92,8),(74,14),(56,8),(40,14)],fill=(24,20,24))   # hair
    d.rectangle([40,0,48,40],fill=(24,20,24)); d.rectangle([136,0,144,40],fill=(24,20,24))
    shout=t>0.3 and (f//3)%3!=0
    for ex in (74,110):
        d.polygon([(ex-12,20),(ex+12,24),(ex+12,27),(ex-12,24)],fill=(20,14,14))   # angry brows
        d.ellipse([ex-8,26,ex+8,33],fill=(245,245,245)); d.ellipse([ex-3,27,ex+3,32],fill=(40,30,24))
    d.polygon([(92,30),(88,42),(96,42)],fill=(200,150,120))
    d.polygon([(66,44),(92,41),(118,44),(116,48),(92,45),(68,48)],fill=(24,20,24))   # the moustache
    if shout: d.rectangle([76,49,108,60],fill=(60,10,14)); d.rectangle([78,49,106,51],fill=(245,245,240))
    else: d.line([78,52,106,52],fill=(90,40,40),width=2)
    for x0,y0,L in ((58,14,20),(124,20,26),(100,34,10)):                         # blood
        d.line([x0,y0,x0+1,y0+L],fill=(170,20,24),width=2)
    d.rectangle([0,58,W,H],fill=(6,6,14))
    if t>0.25:
        jx=(f%3)-1 if shout else 0
        big_text(im,"PIENSA CLAUDE!",50,(255,230,90),cx=W//2+jx)
    if t<0.06: zoom_lines(d)
    return im

def clip_train(f):
    s=scene(f,THEME)
    bob=(f//6)%2
    cl=actor(MARK[guard_pose(f)],30,y=FLOAT-bob); om=actor(OMNI['idle'],150,y=FLOAT-bob,flip=True)
    cape=True; oflying=False
    # 1) Omni-Man grabs Claude and flies him over the city
    if 12<=f<22:
        om.update(spr=OMNI['attack'],x=lerp(150,44,(f-12)/10),y=FLOAT); oflying=True
        s['fx'].append(('inv_wind',om['x'],FLOAT-8,-1))
    if f==22: s['fx'].append(('spark',38,FLOAT-8,6)); s['shake']=rshake(2)
    if 22<=f<48:
        t=(f-22)/26; x=lerp(44,112,ease(t)); y=FLOAT-int(18*math.sin(math.pi*t))
        om.update(spr=OMNI['attack'],x=x+12,y=y,flip=True); cl.update(spr=MARK['hurt'],x=x,y=y+2,flip=True)
        s['fx'].append(('inv_wind',x+12,y-8,1)); oflying=True
    # 2) the train: he holds Claude in its path
    if 48<=f<66:
        om.update(spr=OMNI['attack'],x=124,y=GROUND-3,flip=True); cl.update(spr=MARK['hurt'],x=112,y=GROUND-3,flip=True)
    if 44<=f<96:
        tx=lerp(-10,300,(f-44)/52); s['fx'].append(('inv_train',tx))
        if f>=66:   # pinned to the front of the train
            cl.update(spr=BEAT['hurt'],x=min(tx+4,210),y=GROUND-3,flip=True)
            for j in range(3): s['fx'].append(('shard',tx+random.randint(-2,6),GROUND-random.randint(4,14),(230,236,255) if j else (200,30,30)))
            s['shake']=rshake(2 if f<74 else 1)
        if f==66: s['flash']=1.0; s['fc']=(112,GROUND-8); s['flashc']=(255,220,200)
        if f>=66: om.update(spr=OMNI['idle'],x=124,y=FLOAT-6,flip=False)
    if 58<=f<66: callout(s,"...",y=14,c=(230,230,240))
    if 96<=f<110:   # he brings him back and drops him on the street
        t=(f-96)/14; om.update(spr=OMNI['idle'],x=lerp(200,76,ease(t)),y=FLOAT-8,flip=True); oflying=True
        cl.update(spr=BEAT['hurt'],x=lerp(200,64,ease(t)),y=lerp(FLOAT,GROUND,t),flip=False)
        if f==109: s['fx'].append(('dust',60,GROUND-1)); s['shake']=rshake(2)
    # 3) close-up
    if 110<=f<150: s['image']=closeup_think((f-110)/40,f); return s
    # 4) the beatdown
    if 150<=f<214:
        k=(f-150)//4; ph=(f-150)%4
        cl.update(spr=BEAT['hurt'],x=60+(1 if ph<2 else 0),y=GROUND)
        om.update(spr=OMNI['attack' if ph<2 else 'idle'],x=78,y=GROUND,flip=True)
        if ph==0:
            s['fx'].append(('spark',64,GROUND-6,4)); s['shake']=rshake(2 if k%3==0 else 1)
            for j in range(3): s['fx'].append(('shard',62+random.randint(-4,4),GROUND-random.randint(2,10),(200,24,28)))
        if f<196 and (f//12)%2==0: callout(s,"PIENSA CLAUDE!",y=14,c=(255,230,90))
        s['under'].append(('ring',60,GROUND+1,6+min(10,k),(90,70,60)))
    # 5) he leaves; Claude heals and floats back up
    if 214<=f<226:
        t=(f-214)/12; om.update(spr=OMNI['idle'],x=78,y=lerp(GROUND,-30,ease(t)),flip=True); oflying=True
        if f==214: s['fx'].append(('ring',78,GROUND-10,4,(240,240,255)))
        if f<220: s['fx'].append(('ring',78,GROUND-10,4+(f-214)*6,(240,240,255)))
    if 214<=f<250: cl.update(spr=BEAT['hurt'] if f<232 else BEAT[guard_pose(f)],x=60,y=GROUND)
    if 226<=f<262: om['vis']=False
    if 244<=f<252:
        for j in range(4): s['fx'].append(('twinkle',60+random.randint(-6,6),GROUND-random.randint(2,12),1))
    if 250<=f<276: cl.update(spr=MARK[guard_pose(f)],x=ez(60,30,(f-250)/24),y=int(lerp(GROUND,FLOAT-bob,ease((f-250)/20))))
    if 262<=f<282:   # Omni-Man descends back into place
        t=(f-262)/20; om.update(vis=True,spr=OMNI['idle'],x=150,y=int(lerp(-24,FLOAT-bob,ease(t))),flip=True); oflying=t<1
    if om['vis'] and cape: s['under'].append(('inv_cape',om['x'],om['y'],-1 if om['flip'] else 1,oflying))
    s['actors']=[cl,om]
    return s

CLIPS = [clip('train', N_, clip_train)]
