"""League of Legends: Claude as Quinn, Demacia's Wings (blue hood, gold-and-blue armour, the crossbow on her
arm) with Valor, her eagle, on her shoulder, in a lane of Summoner's Rift before the enemy turret. A wave of
red minions marches in: bolts, damage numbers, gold; Harrier marks one (the bird over its head) and the
marked shot hits harder. Q, Blinding Assault: Valor dives into the caster. Close-up: Valor's eye and a
feather — DEMACIA! E, Vault: she leaps off the last minion. R, Behind Enemy Lines: she rides Valor over the
turret and Skystrike brings it down (TURRET DESTROYED). VICTORY; a new game, the turret standing again."""
from engine import *

THEME = 'lol'
N_ = 372                                                            # a multiple of 12
CX, TX = 30, 168                                                    # Quinn; the enemy turret
BLUE, BLUE_D, GOLDL, WHITE_ = (60,100,200), (36,60,130), (236,190,70), (236,240,248)
# Quinn: the blue hood with its gold trim and a peak, brown fringe, blue armour with gold pauldrons and
# belt, a dark cape off the back shoulder, brown leather leggings and boots
QPAL = {'1':(110,70,40),'2':BLUE,'3':GOLDL,'4':BLUE_D,'5':(28,40,96),'6':(110,76,50),'7':(56,40,30)}
HOOD = ["..2.........","..222222....",".22222222...",".2222223111."]
MPAL = {'r':(200,50,60),'R':(140,30,40),'m':(170,170,180),'s':(230,200,170),'k':(40,30,30),'y':(250,220,90)}
MELEE = S(["..mmm...","..mrm..m",".rrrr.m.","rrRrrm..",".rrrr...",".R..R...",".k..k..."])
CASTER = S(["...rrr...y","..rrrrr..m","...sss...m","..RrrrR..m","..rrrrr..m","..R...R..m","..k...k..."])

def _quinn(spr):
    g=[list(r) for r in overlay(spr,HOOD,-1,0)]
    top,l,r=body_box(S([''.join(x) for x in g])); h=len(g); w=len(g[0])
    for y in range(h):
        for x in range(w):
            c=g[y][x]
            if c=='O' and y<=top+4 and x<=l+1: g[y][x]='2'               # the hood down the back...
            elif c=='O' and y<=top+4 and x==l+2: g[y][x]='3'             # ...its gold trim round the face
            elif c=='O' and y==top+5: g[y][x]='3' if x in (l,l+1,r) else '4'   # pauldrons
            elif c=='O' and y==top+7: g[y][x]='3'                        # the belt
            elif c=='O' and y>top+4: g[y][x]='4' if (x+y)%4 else '2'
            elif c=='o' and y<top+8: g[y][x]='2'
            elif c=='o': g[y][x]='7' if y==h-1 else '6'
    for y in range(top+5,min(top+10,h)):                                 # the cape, off the back shoulder
        for x in (l-2,l-1):
            if 0<=x<w and g[y][x]=='.' and (y-top-5)>=(l-1-x): g[y][x]='5'
    return S([''.join(x) for x in g])
QUINN=variant(_quinn)
GRIP={'guard':(13,4),'guard2':(13,4),'punch':(16,5),'charge':(15,5),'dash':(16,5),'armsup':(12,0)}

# ---- background: a lane of the Rift --------------------------------------------------------------------
def _rift(d):
    for y in range(0,34):
        k=y/33; d.line([0,y,W,y],fill=(int(30+30*k),int(70+50*k),int(50+20*k)))   # the jungle behind the wall
    rr=random.Random(2009)
    for _ in range(40):
        x=rr.randint(0,W); y=rr.randint(0,30); r=rr.randint(4,9); d.ellipse([x-r,y-r,x+r,y+r],fill=rr.choice([(40,90,56),(50,110,64),(34,76,48)]))
    d.polygon([(0,34),(W,30),(W,38),(0,40)],fill=(110,104,96))      # the stone wall of the lane
    for x in range(0,W,14): d.line([x,33,x+2,39],fill=(84,80,74))
    d.rectangle([0,38,W,H],fill=(84,130,64))                         # grass, and the dirt of the lane
    d.polygon([(0,34),(W,30),(W,38),(0,40)],fill=(110,104,96))
    d.polygon([(0,46),(W,44),(W,H),(0,H)],fill=(150,124,86))
    for _ in range(60): d.point((rr.randint(0,W-1),rr.randint(45,H-1)),fill=rr.choice([(130,108,74),(168,140,98)]))
    for x in range(0,W,9): d.line([x,41,x+1,39],fill=(110,160,80))
register_bg(THEME, lambda v: (v+90,v+70,v+50), decor=_rift)

# ---- effects -------------------------------------------------------------------------------------------
@fx('lq_tower')
def _fx_tower(d,im,e,f):
    """The enemy turret: a stone spire with its red crystal and a health bar; hp 0 = rubble."""
    _,hp,a=e; x=TX
    if a<=0: return
    if hp<=0:
        for i,(dx,dy,w) in enumerate(((-8,0,8),(0,0,10),(6,-2,6),(-3,-4,7),(2,-6,4))):
            d.rectangle([x+dx-w//2,GROUND-4+dy,x+dx+w//2,GROUND+dy],fill=(120,112,104) if i%2 else (96,90,84))
        return
    d.polygon([(x-9,GROUND),(x-6,GROUND-26),(x+6,GROUND-26),(x+9,GROUND)],fill=(118,110,104),outline=(70,66,62))
    for y in range(GROUND-22,GROUND,6): d.line([x-7,y,x+7,y],fill=(90,86,80))
    d.polygon([(x-8,GROUND-26),(x,GROUND-34),(x+8,GROUND-26)],fill=(90,40,50))
    g=(f//3)%2; d.polygon([(x-3,GROUND-30),(x,GROUND-40-g),(x+3,GROUND-30)],fill=(230,60,70)); d.point((x,GROUND-36),fill=(255,180,180))
    d.rectangle([x-10,GROUND-47,x+10,GROUND-45],fill=(30,30,30)); d.rectangle([x-10,GROUND-47,x-10+int(20*hp),GROUND-45],fill=(220,60,60))

@fx('lq_hp')
def _fx_hp(d,im,e,f):
    _,x,y,hp=e; d.rectangle([x-5,y,x+5,y+1],fill=(30,30,30)); d.rectangle([x-5,y,x-5+int(10*hp),y+1],fill=(220,60,60))

@fx('lq_num')
def _fx_num(d,im,e,f):
    """A floating number: damage (white, orange when crit/marked) or gold (+21, yellow), rising."""
    _,txt,x,y,k,c=e; x,y=int(x),int(y-k*0.6)
    if c==(250,210,60): d.ellipse([x-5,y,x-1,y+4],fill=c,outline=(150,110,20)); x+=1     # gold: a coin first
    text(d,txt,x,y,c,shadow=(0,0,0))

@fx('lq_bolt')
def _fx_bolt(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y); d.line([x-4,y,x,y],fill=(220,226,236)); d.point((x+1,y),fill=(255,255,255)); d.point((x-5,y),fill=(120,170,255))

@fx('lq_crossbow')
def _fx_crossbow(d,im,e,f):
    """Her crossbow on the forearm: the stock, the silver limbs and string, a bolt loaded."""
    _,x,y,flip=e; s_=-1 if flip else 1; x,y=int(x),int(y)
    d.line([x-s_,y,x+s_*6,y],fill=(110,80,50))
    d.line([x+s_*5,y-3,x+s_*5,y+3],fill=(200,206,216)); d.point((x+s_*6,y-3),fill=GOLDL); d.point((x+s_*6,y+3),fill=GOLDL)
    d.line([x+s_*4,y-3,x+s_*2,y,x+s_*4,y+3],fill=(230,230,236))
    d.line([x+s_*3,y,x+s_*8,y],fill=(220,226,236))

@fx('lq_mark')
def _fx_mark(d,im,e,f):
    """Harrier: the little blue bird over a marked target."""
    _,x,y=e; x,y=int(x),int(y)
    d.polygon([(x-4,y),(x,y-2),(x+4,y),(x,y+1)],fill=BLUE,outline=(170,200,255)); d.point((x,y-1),fill=WHITE_)

VALOR_D, VALOR_L = (36,60,150), (120,160,236)
def valor(d,x,y,f,state='perch',scale=1):
    """Valor: a blue eagle with a white head and the gold beak. Perched: wings folded, the tail down.
    Flying: broad wings with fingered primaries beating up and down, the tail fanned."""
    x,y=int(x),int(y); k=scale
    if state=='perch':
        d.polygon([(x-2,y-3),(x+2,y-3),(x+3,y+2),(x-1,y+4),(x-3,y+1)],fill=BLUE,outline=(16,24,60))   # the body
        d.line([x-2,y-1,x-1,y+3],fill=VALOR_D); d.point((x-2,y+3),fill=WHITE_)                         # folded wing
        d.line([x-1,y+4,x-2,y+6],fill=VALOR_D)                                                          # the tail
        d.ellipse([x,y-6,x+3,y-3],fill=WHITE_,outline=(16,24,60))                                       # the head
        d.polygon([(x+3,y-5),(x+5,y-4),(x+3,y-3)],fill=GOLDL); d.point((x+2,y-5),fill=(20,20,20))
        d.point((x+1,y+3),fill=GOLDL)                                                                    # talons
        return
    ph=math.sin(f*0.9); up=-4*k*ph                                    # wingtips up and down
    for s_ in (-1,1):
        lead=[(x,y-1*k),(x+s_*7*k,y-3*k+up*0.5),(x+s_*14*k,y-2*k+up)]       # the leading edge
        trail=[(x+s_*13*k,y+1*k+up*0.8),(x+s_*7*k,y+2*k+up*0.3),(x,y+2*k)]
        d.polygon(lead+trail,fill=BLUE)
        d.line(lead,fill=VALOR_L)                                     # light along the front of the wing
        d.line(trail,fill=VALOR_D)
        for j in range(3):                                            # fingered primaries at the tip
            px,py=x+s_*(12+j)*k,y+(j-1)*k+up*0.9
            d.line([px,py,px+s_*2*k,py+1*k],fill=VALOR_D)
    d.polygon([(x-3*k,y),(x-8*k,y-2*k),(x-9*k,y+1*k),(x-8*k,y+3*k)],fill=VALOR_D)   # tail fan
    d.ellipse([x-3*k,y-2*k,x+3*k,y+2*k],fill=BLUE)                                   # body
    d.ellipse([x+1*k,y-4*k,x+5*k,y],fill=WHITE_)                                     # head
    d.polygon([(x+5*k,y-3*k),(x+8*k,y-2*k),(x+5*k,y-1*k)],fill=GOLDL); d.point((x+4*k,y-3*k),fill=(20,20,20))

@fx('lq_valor')
def _fx_valor(d,im,e,f):
    _,x,y,state,scale=e; valor(d,x,y,f,state,scale)

@fx('lq_feathers')
def _fx_feathers(d,im,e,f):
    """Blinding Assault: a burst of feathers (k frames since)."""
    _,x,y,k=e; rr=random.Random(9)
    for i in range(14):
        a=rr.uniform(0,6.283); L=k*rr.uniform(1,2.2); px,py=x+math.cos(a)*L,y+math.sin(a)*L+k*0.2
        d.line([px,py,px+2,py-1],fill=WHITE_ if i%2 else BLUE)

@fx('lq_banner')
def _fx_banner(d,im,e,f):
    """VICTORY, gold on a dark crest, the way the game says it."""
    _,a=e
    if a<=0: return
    L=Image.new('RGB',(W,H),(0,0,0)); ld=ImageDraw.Draw(L)
    ld.rectangle([0,0,W,H],fill=(10,14,30))
    ld.polygon([(W//2-50,14),(W//2+50,14),(W//2+60,30),(W//2+50,46),(W//2-50,46),(W//2-60,30)],fill=(30,40,80),outline=GOLDL)
    big_text(L,"VICTORY",22,GOLDL,scale=2,cx=W//2,outline=(80,50,10))
    im.paste(Image.blend(im,L,a))

# ---- close-up -------------------------------------------------------------------------------------------
def closeup_valor(t,f):
    """Primer plano: Valor's eye, the gold beak, a feather drifting down — DEMACIA!"""
    im=Image.new('RGB',(W,H),(40,70,140)); d=ImageDraw.Draw(im)
    for i in range(16):                                              # the sky rushing by
        y=(i*11+f*4)%H; d.line([0,y,W,y-6],fill=(60,96,170))
    hx,hy=60,34
    d.ellipse([hx-44,hy-40,hx+36,hy+40],fill=WHITE_,outline=(20,30,60),width=2)          # the head
    d.polygon([(hx-44,hy+10),(hx-10,hy+40),(hx-60,hy+40)],fill=BLUE)                      # blue feathers at the neck
    d.polygon([(hx+28,hy-6),(hx+62,hy+6),(hx+28,hy+16)],fill=GOLDL,outline=(150,100,20))   # the beak
    d.line([hx+30,hy+6,hx+56,hy+6],fill=(150,100,20))
    d.ellipse([hx-2,hy-14,hx+20,hy+6],fill=(250,200,60),outline=(20,20,20),width=2)        # the eye
    d.ellipse([hx+5,hy-9,hx+13,hy+1],fill=(10,10,10)); d.point((hx+7,hy-7),fill=(255,255,255))
    d.line([hx-8,hy-18,hx+24,hy-14],fill=(20,30,60),width=3)                              # the brow
    fy=int(lerp(-10,H+10,t)); fx_=110+int(8*math.sin(t*12))                              # a feather falling
    d.line([fx_,fy,fx_+6,fy+12],fill=(200,210,230)); d.polygon([(fx_,fy),(fx_+8,fy+6),(fx_+6,fy+12),(fx_-2,fy+6)],fill=BLUE)
    if t>=0.3:
        jj=(f%3)-1 if t<0.4 else 0
        big_text(im,"DEMACIA!",22,GOLDL,scale=2,cx=144+jj,outline=(20,30,80))
    if t<0.06: zoom_lines(d)
    if t>0.9: im=fade_to(im,WHITE_,0.6*(t-0.9)/0.1)
    return im

# ---- the clip -------------------------------------------------------------------------------------------
WAVE=[(100,'melee'),(118,'melee'),(136,'caster')]                    # where the minions stop
def minion_state(i,f):
    """(x, hp, alive) for minion i."""
    x0,kind=WAVE[i]
    if f<14: return None
    x=lerp(W+10+i*12,x0,(f-14)/24) if f<38 else x0
    deaths=(60,92,184)                                               # bolts; Valor's dive; the Vault
    hp=1.0
    if i==0: hp=1.0 if f<46 else (0.6 if f<56 else 0.0)
    if i==2: hp=1.0 if f<84 else 0.0
    if i==1: hp=1.0 if f<170 else (0.3 if f<184 else 0.0)
    if f>=deaths[i]+8: return None
    return x,hp,f<deaths[i]

def clip_valor(f):
    s=scene(f,THEME)
    qx,qy,qpose,qflip,show=CX,GROUND,guard_pose(f),False,True
    vstate,vx,vy=('perch',None,None)
    tower_hp,tower_a=1.0,1.0
    # 1) the wave; bolts; Harrier
    acts=[]
    for i,(x0,kind) in enumerate(WAVE):
        st=minion_state(i,f)
        if not st: continue
        x,hp,alive=st
        a=actor(MELEE if kind=='melee' else CASTER,x,flip=True,pal=MPAL)
        if not alive: a['alpha']=max(0,1-(f-(60,92,184)[i])/8)
        acts.append(a)
        if alive: s['fx'].append(('lq_hp',x,GROUND-11,hp))
    for t0,dmg,c in ((40,"45",(255,255,255)),(50,"112",(255,170,60))):
        if t0<=f<t0+6: qpose='punch'; s['fx'].append(('lq_bolt',lerp(CX+12,96,(f-t0)/6),GROUND-6))
        if t0+6<=f<t0+26: s['fx'].append(('lq_num',dmg,96,GROUND-16,f-t0-6,c))
    if 44<=f<56: s['fx'].append(('lq_mark',100,GROUND-14))
    for t0,x in ((60,100),(92,136),(184,118)):
        if t0<=f<t0+24: s['fx'].append(('lq_num',"+21",x+2,GROUND-28,f-t0,(250,210,60)))
    # 2) Q, Blinding Assault: Valor dives into the caster
    if 70<=f<92:
        p=(f-70)/14; vstate='fly'; vx=lerp(CX-2,136,min(1,p)); vy=lerp(GROUND-14,GROUND-6,min(1,p))-14*math.sin(min(1,p)*math.pi)
        if f<76: callout(s,"Q",y=2,c=(170,200,255))
    if 84<=f<100: s['fx'].append(('lq_feathers',136,GROUND-6,f-84))
    if 92<=f<100: vstate='fly'; p=(f-92)/8; vx,vy=lerp(136,CX-2,p),lerp(GROUND-6,GROUND-14,p)-10*math.sin(p*math.pi)
    # 3) close-up
    if 100<=f<160: s['image']=closeup_valor((f-100)/60,f); return s
    # 4) E, Vault: off the last minion
    if 166<=f<190:
        p=(f-166)/24
        qx=lerp(CX,108,min(1,p*2)) if p<0.5 else lerp(108,CX+4,(p-0.5)*2); qy=GROUND-int(16*math.sin(min(1,p*2)*math.pi)) if p<0.5 else GROUND-int(10*math.sin((p-0.5)*2*math.pi))
        qpose='dash' if p<0.5 else 'guard2'; qflip=p>=0.5
        if f<172: callout(s,"E",y=2,c=(170,200,255))
        if 174<=f<178: s['fx'].append(('spark',116,GROUND-8,5)); s['shake']=rshake(1)
    # 5) R, Behind Enemy Lines: on Valor over the turret; Skystrike
    if 196<=f<260:
        show=False; p=(f-196)/40
        rx=lerp(CX,TX,min(1,p)) if f<236 else lerp(TX,CX,(f-236)/24); ry=lerp(GROUND-20,10,math.sin(min(1,p)*math.pi/2)) if f<236 else lerp(10,GROUND-8,(f-236)/24)
        s['fx'].append(('lq_valor',rx,ry,'fly',2))
        acts.append(actor(QUINN['guard'],rx-2,int(ry)-2,pal=QPAL))
        if f<206: callout(s,"R",y=2,c=(170,200,255))
        if 214<=f<236 and f%4<2: s['fx'].append(('lq_bolt',rx+6,ry+6+(f%8)))
        tower_hp=1.0 if f<214 else max(0,1-(f-214)/22)
        if 236<=f<244: s['fx'].append(('lq_feathers',TX,GROUND-20,(f-236)*2)); s['flash']=0.8 if f==236 else 0; s['fc']=(TX,GROUND-20); s['flashc']=(200,220,255); s['shake']=rshake(2)
    if f>=236 and f<300: tower_hp=0.0
    if 240<=f<280: s['fx'].append(('big',"TURRET DESTROYED",4,(255,220,120)))
    # 6) VICTORY; a new game
    banner=(min(1,(f-280)/10) if f<336 else max(0,1-(f-336)/14)) if 280<=f<350 else 0
    if 300<=f<336: tower_hp=1.0
    if f>=350 or f<14: tower_hp=1.0
    s['under'].append(('lq_tower',tower_hp,tower_a))
    if show:
        acts.append(actor(QUINN[qpose],qx,qy,flip=qflip,pal=QPAL))
        hx,hy=hand_at(QUINN[qpose],qx,int(qy),qflip,*GRIP.get(qpose,(13,4)),h=11)
        s['fx'].append(('lq_crossbow',hx,hy,qflip))
        if vstate=='perch':
            ox,oy=origin(QUINN[qpose],qx,int(qy))
            top,l,r=body_box(QUINN[qpose]); bx=ox+(l-2 if not qflip else len(QUINN[qpose][0])-l+1)
            s['fx'].append(('lq_valor',bx,oy+top+5,'perch',1))                 # on the back shoulder
    if vstate=='fly' and vx is not None: s['fx'].append(('lq_valor',vx,vy,'fly',1))
    if banner: s['fx'].append(('lq_banner',banner))                     # over everything
    s['actors']=acts
    return s

CLIPS = [clip('valor', N_, clip_valor)]
