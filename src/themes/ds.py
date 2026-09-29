"""Dark Souls / Elden Ring: Claude (a Solaire-style Knight of Astora: bucket helm, sun tabard,
sword and shield) vs Malenia, Blade of Miquella. Waterfowl Dance: Claude rolls through the
flurry on i-frames until his stamina runs dry and a slash lands; Estus, PRAISE THE SUN! Malenia's
lunge kills him — close-up: YOU DIED... the letters crack, the sun burns through, he gets back up.
Plunging attack, the boss dissolves into golden motes: ENEMY FELLED. The fog gate re-forms her."""
from engine import *

THEME = 'ds'
N_ = 288

# ---- sprites ---------------------------------------------------------------------------------
def _col(x,y0,y1,ch): return [(x,y,ch) for y in range(y0,y1+1)]
def _shield(y): return [(0,y,'qqq'),(0,y+1,'qYq'),(0,y+2,'YYY'),(0,y+3,'qYq'),(0,y+4,'qqq')]

_ARMED={
 'guard':  lambda s: paint(s,_col(13,-6,1,'H')+[(12,2,'YYY')]+_shield(4),top=6),
 'guard2': lambda s: paint(s,_col(13,-5,2,'H')+[(12,3,'YYY')]+_shield(5),top=5),
 'punch':  lambda s: paint(s,[(17,5,'HHHHHHH'),(17,6,'hhhhhhh'),(17,4,'Y'),(17,7,'Y')]+_shield(3),right=8),
 'dash':   lambda s: paint(s,[(17,5,'HHHHHHH'),(17,6,'hhhhhhh'),(17,4,'Y'),(17,7,'Y')]+_shield(3),right=8),
}
def _knight_colors(x,y,t,l,r,c):
    if c=='.' or not (l<=x<=r) or c!='O': return None
    if t+4<=y<=t+7 and l+2<=x<=r-2:                        # white tabard with the sun of Astora
        return 'Y' if (t+5<=y<=t+6 and l+3<=x<=r-3) else 'W'
    return None
_HELM=[".DDDDDD.","DDDDDDDD","dkdddkdd"]                  # bucket helm with its slit rim
def _knight(name, s):
    s=_ARMED.get(name,lambda z: z)(s)
    return overlay(recolor_rows(s,_knight_colors),_HELM,0,0)
KN={k:_knight(k,v) for k,v in CL.items()}
KN['plunge']=overlay(recolor_rows(paint(CL['armsup'],_col(6,11,17,'H')+[(5,10,'YYY')],bottom=7),
                                  _knight_colors),_HELM,0,0)   # sword pointing down: feet = the tip

ROLL=[rotate90(KN['guard2'],k) for k in range(4)]
LYING=rotate90(KN['hurt'],1)

_MAL=S([
"....y......y......",
"....yy....yy......",
"...yyyYYYYyyy.....",
".....YYYYYY.......",
"....rYkkkkYr......",
"...rrYssssYrr.....",
"..rrr.ssss.rrr....",
"..rr.DDDDDD.rr....",
"..r.DDdDDdDD.r....",
"..r.DD.DD.D.YY....",
"..rsDDdDDdD..YY...",
"...sDDDDDDD...YH..",
"....RRRRRR.....H..",
"....RRRRRR......H.",
"...RRRRRRRR......H",
"...RRRRRRRR.......",
"..RRRRRRRRRR......",
"..RRRRRRRRRR......",
"...dd....dd.......",
"...dd....dd.......",
"..ddd....ddd......",])
_MAL2=S([r[:2]+r[2:4].replace('r','.')+r[4:] if 5<=i<=10 else r for i,r in enumerate(_MAL)])  # hair sway
_MAL_ATK=S([r[:11]+'.'*7 if 9<=i<=14 else r for i,r in enumerate(_MAL)][:9]+
           ["..r.DD.DD.D.YYYYY.........","..rsDDdDDdD..YYHHHHHHHHHH."]+
           [r[:11] for r in _MAL[11:]])
MAL={'idle':_MAL,'idle2':_MAL2,'attack':_MAL_ATK,'hurt':hurt(_MAL)}
MALPAL={'r':(196,48,36),'R':(120,28,32),'D':(150,140,120),'d':(96,86,74),'y':(214,170,70),'Y':(196,160,80),'s':(232,196,170)}
def mal_idle(f): return MAL['idle'] if (f//8)%2==0 else MAL['idle2']

# ---- background ------------------------------------------------------------------------------
def _arena(d):
    for x,h in ((10,30),(46,18),(128,24),(170,34)):        # ruined pillars, very low contrast
        d.rectangle([x,GROUND-h,x+5,GROUND],fill=(20,20,24)); d.rectangle([x-1,GROUND-h-1,x+6,GROUND-h],fill=(26,26,30))
        d.line([x+1,GROUND-h-1,x+3,GROUND-h+3],fill=(12,12,14))
    d.arc([66,14,120,70],200,340,fill=(22,22,26))           # a broken arch in the back
    d.line([72,30,72,GROUND],fill=(18,18,22)); d.line([114,30,114,GROUND],fill=(18,18,22))
register_bg(THEME, lambda v: (v,v,int(v*0.9)+2), decor=_arena)

# ---- effects ---------------------------------------------------------------------------------
def _alpha_fill(im, mask_fn, c, a):
    m=Image.new('L',(W,H),0); mask_fn(ImageDraw.Draw(m)); m=m.point(lambda v: int(v*a))
    im.paste(c,(0,0),m)

@fx('ds_fog')
def _fx_fog(d,im,e,f):
    """Drifting fog banks; each bank's x period divides the clip so the loop is seamless."""
    _,a=e
    def banks(md):
        for k,(y,r,sp) in enumerate(((44,16,1),(52,12,2),(36,20,1),(56,10,3))):
            x=(k*61+f*(W+60)*sp/N_)%(W+60)-30
            md.ellipse([x-r*2,y-r//2,x+r*2,y+r//2],fill=255)
    m=Image.new('L',(W,H),0); banks(ImageDraw.Draw(m)); m=m.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v*a))
    im.paste((58,58,66),(0,0),m)

@fx('ds_hud')
def _fx_hud(d,im,e,f):
    """Souls HUD: HP (red) and stamina (green) top-left; boss name + long bar at the bottom."""
    _,hp,st,bhp,btrail=e
    for y,w,v,c in ((2,60,hp,(170,24,24)),(6,44,st,(40,150,60))):
        d.rectangle([3,y,4+w,y+2],fill=(14,12,12),outline=(70,62,50))
        if v>0.01: d.rectangle([4,y+1,4+int((w-1)*v),y+1],fill=c)
    name="MALENIA BLADE OF MIQUELLA"; x0=W//2-len(name)*2
    text(d,name,x0,53,(170,160,140))
    d.rectangle([x0-1,60,x0+len(name)*4,62],fill=(10,8,8),outline=(60,52,40))
    L=len(name)*4-1
    if btrail>bhp+0.005: d.line([x0+int(L*bhp),61,x0+int(L*btrail),61],fill=(220,190,70))
    if bhp>0.005: d.line([x0,61,x0+int(L*bhp),61],fill=(150,20,20))

@fx('ds_slash')
def _fx_slash(d,im,e,f):
    """Waterfowl Dance: a whirl of crescent slashes around (x, y)."""
    _,x,y,n=e; rr=random.Random(f*31+7)
    for _ in range(n):
        r=rr.randint(8,22); a0=rr.randint(0,359); c=(255,240,230) if rr.random()<0.4 else (230,70,60)
        d.arc([x-r,y-r//2-2,x+r,y+r//2+2],a0,a0+rr.randint(50,110),fill=c,width=1)

@fx('ds_estus')
def _fx_estus(d,im,e,f):
    """The Estus Flask at Claude's mouth, with its orange glow."""
    _,x,y,g=e
    if g>0:
        r=5+(f//3)%2; d.ellipse([x-r,y-r,x+r,y+r],outline=(200,100,30))
    d.rectangle([x-1,y-5,x+1,y-3],fill=(150,130,110))
    d.ellipse([x-3,y-3,x+3,y+3],fill=(150,120,90))
    d.ellipse([x-2,y-2,x+2,y+2],fill=(255,150,40) if (f//2)%2 else (255,190,70))
    d.point((x-1,y-1),fill=(255,240,200))

@fx('ds_sun')
def _fx_sun(d,im,e,f):
    """PRAISE THE SUN: a warm sun above the raised arms (small, not a full-screen flash)."""
    _,x,y,r=e
    if r<1: return
    for k in range(12):
        a=k*math.pi/6+f*0.05; L=r+3+(k+f//2)%3
        d.line([x+math.cos(a)*(r+1),y+math.sin(a)*(r+1),x+math.cos(a)*L,y+math.sin(a)*L],fill=(240,170,50))
    d.ellipse([x-r,y-r,x+r,y+r],fill=(250,200,70)); d.ellipse([x-r//2,y-r//2,x+r//2,y+r//2],fill=(255,236,150))

@fx('ds_lunge')
def _fx_lunge(d,im,e,f):
    _,x0,x1,y=e
    for k,c in enumerate(((120,30,30),(200,60,50),(255,220,210))): d.line([x0,y-1+k,x1,y-1+k],fill=c)

@fx('ds_motes')
def _fx_motes(d,im,e,f):
    """Golden motes rising from a dissolving body at (x, feet), progress t 0..1."""
    _,x,feet,t,n=e; rr=random.Random(4242)
    for i in range(n):
        bx=x+rr.randint(-9,9); by=feet-rr.randint(0,22); sp=rr.uniform(0.6,1.4); ph=rr.random()*6
        k=max(0,t-rr.random()*0.4)/0.6
        if k<=0 or k>1.3: continue
        yy=by-k*sp*30; xx=bx+math.sin(ph+k*5)*3
        c=(255,236,150) if (i+f)%5==0 else (220,170,60)
        d.point((int(xx),int(yy)),fill=c)
        if i%4==0 and k<0.8: d.point((int(xx),int(yy)+1),fill=(150,110,40))

@fx('ds_fogwall')
def _fx_fogwall(d,im,e,f):
    """The fog gate the boss steps back through (translucent, never a bright panel)."""
    _,x,a=e
    def wall(md):
        md.rectangle([x-10,GROUND-30,x+10,GROUND],fill=180)
        for k in range(6):
            yy=GROUND-30+((k*7+f)%32); md.ellipse([x-12,yy-2,x+12,yy+2],fill=255)
    m=Image.new('L',(W,H),0); wall(ImageDraw.Draw(m)); m=m.filter(ImageFilter.GaussianBlur(2)).point(lambda v: int(v*0.4*a))
    im.paste((140,140,160),(0,0),m)

@fx('ds_big')
def _fx_big(d,im,e,f):
    _,txt,y,c,sc=e; big_text(im,txt,y,c,sc)

@fx('ds_runes')
def _fx_runes(d,im,e,f):
    _,v,a=e; c=tuple(int(k*a) for k in (220,200,150)); t=f"{v}"
    text(d,t,W-4-len(t)*4,3,c); d.ellipse([W-10-len(t)*4,3,W-7-len(t)*4,7],outline=tuple(int(k*a) for k in (200,170,70)))

# ---- close-up --------------------------------------------------------------------------------
def closeup_died(t,f):
    """Primer plano: Claude's bucket helm in the dark, YOU DIED in red... then the letters crack,
    the sun burns through the visor slit and the text shatters."""
    im=Image.new('RGB',(W,H),(6,4,4)); d=ImageDraw.Draw(im)
    dark=0.45
    def sh(c,k=dark): return tuple(int(v*k) for v in c)
    d.rectangle([50,16,134,64],fill=sh((217,119,87)))                          # the face (Claude's body)
    d.rectangle([80,52,104,64],fill=sh((236,236,242))); d.ellipse([88,54,96,62],fill=sh((250,210,60)))
    d.rectangle([46,-4,138,18],fill=sh((182,182,194)))                         # bucket helm
    d.rectangle([46,16,138,20],fill=sh((110,110,126)))
    d.line([56,2,56,14],fill=sh((140,140,150))); d.line([128,2,128,14],fill=sh((140,140,150)))
    awake=t>=0.62
    for ex in (92,122):
        if not awake: d.line([ex-4,32,ex+4,32],fill=(14,8,6))                  # eyes closed
        else:
            g=ease((t-0.62)/0.1)
            d.rectangle([ex-3,26,ex+3,38],fill=tuple(int(lerp(20,v,g)) for v in (255,200,80)))
            d.rectangle([ex-1,28,ex+1,36],fill=tuple(int(lerp(20,v,g)) for v in (255,245,190)))
    # the souls band
    band=ease(t/0.2)
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for y in range(18,46): md.line([0,y,W,y],fill=int(210*band*(1-abs(y-32)/15)))
    im.paste((0,0,0),(0,0),m)
    # YOU DIED fading in
    k=ease((t-0.08)/0.3)
    red=(int(lerp(20,170,k)),int(lerp(4,18,k)),int(lerp(4,18,k)))
    tmask=Image.new('L',(W,H),0); x,y,w,h=big_text(tmask,"YOU DIED",23,255,3,shadow=None)
    if t<0.78: im.paste(red,(0,0),tmask)
    else:                                                                      # the letters split
        s=ease((t-0.78)/0.22)
        top=tmask.crop((0,0,W,y+h//2)); bot=tmask.crop((0,y+h//2,W,H))
        c2=tuple(int(v*(1-s)) for v in red)
        im.paste(c2,(int(-s*26),int(-s*8)),top); im.paste(c2,(int(s*26),y+h//2+int(s*8)),bot)
    if t>=0.66:                                                                # cracks of sunlight
        rr=random.Random(99); g=min(1,(t-0.66)/0.12)
        for j in range(3):
            px,py=x+int(w*(0.2+0.3*j)),y
            pts=[(px,py)]
            for _ in range(int(2+4*g)): px+=rr.randint(-5,5); py+=rr.randint(2,4); pts.append((px,py))
            d.line(pts,fill=(255,210,90) if (f+j)%3 else (255,245,200))
    if t>=0.84:                                                                # shards fly off
        rr=random.Random(123); s=(t-0.84)/0.16
        for _ in range(26):
            sx=rr.randint(x,x+w); sy=rr.randint(y,y+h); a=rr.random()*6.28; v=rr.uniform(10,40)
            d.point((sx+math.cos(a)*v*s,sy+math.sin(a)*v*s*0.6),fill=(255,200,80) if rr.random()<0.5 else (170,20,20))
    if t<0.06:
        zoom_lines(d,(120,110,110))
    return im

# ---- the clip --------------------------------------------------------------------------------
def _hp(f):
    v=1.0
    if f>=74: v=lerp(v,0.35,(f-74)/4)
    if f>=102: v=lerp(v,1.0,(f-102)/12)
    if f>=146: v=lerp(v,0.0,(f-146)/4)
    if f>=204: v=lerp(v,0.3,(f-204)/8)
    if f>=262: v=lerp(v,1.0,(f-262)/18)
    return v
def _st(f):
    v=1.0
    for t0 in (44,56):
        if f>=t0: v-=0.42*min(1,(f-t0)/3)
    if f>=78: v=lerp(v,1.0,(f-78)/30)
    for t0 in (214,):
        if f>=t0: v-=0.5*min(1,(f-t0)/3)
    if f>=236: v=lerp(v,1.0,(f-236)/24)
    return max(0,v)
def _bhp(f):
    if f<229: return 1.0
    if f<262: return lerp(1.0,0.0,(f-229)/3)
    return ez(0.0,1.0,(f-264)/16)
def _btrail(f):
    if 229<=f<262: return lerp(1.0,0.0,(f-236)/10) if f>=236 else 1.0
    return _bhp(f)

def clip_felled(f):
    s=scene(f,THEME)
    cl=actor(KN[guard_pose(f)],30); ml=actor(mal_idle(f),150,flip=True,pal=MALPAL)
    s['under'].append(('ds_fog',0.4))
    hudon=True
    # 1) Waterfowl Dance: she rises, then a whirl of slashes; Claude rolls through on i-frames
    if 20<=f<40: callout(s,"WATERFOWL DANCE",y=13,c=(230,90,70))
    if 24<=f<40:
        t=(f-24)/16; ml.update(spr=MAL['hurt'] if f<30 else MAL['attack'],x=ez(150,104,t),y=GROUND-int(18*ease(t)))
    if 40<=f<80:
        ml.update(spr=MAL['attack'],x=104+(f%3)-1,y=GROUND-18+((f//2)%2),flip=(f//3)%2==0)
        s['fx'].append(('ds_slash',104,GROUND-26,4))
    if 80<=f<92: ml.update(spr=mal_idle(f),x=ez(104,150,(f-80)/12),y=GROUND-int(18*(1-ease((f-80)/12))))
    for t0,x0,x1 in ((44,30,60),(56,60,90)):                                 # two rolls, translucent
        if t0<=f<t0+10:
            k=(f-t0)//2; cl.update(spr=ROLL[k%4],x=lerp(x0,x1,(f-t0)/10),alpha=0.45)
            if (f-t0)%3==0: s['fx'].append(('dust',int(cl['x'])-6,GROUND-1))
        if t0+10<=f<t0+12: cl.update(spr=KN['guard'],x=x1)
    if 68<=f<74: cl.update(spr=KN['guard2'],x=90)                              # out of stamina...
    if 68<=f<74 and f%2: s['fx'].append(('dmg',"!",86,GROUND-26,(220,60,40)))
    if f==74: s['fx'].append(('spark',92,GROUND-10,6)); s['shake']=rshake(2)
    if 74<=f<90:
        t=(f-74)/16; cl.update(spr=KN['hurt'],x=ez(90,34,t),y=GROUND-int(10*math.sin(math.pi*min(1,t*1.2))))
        if f<80: s['fx'].append(('dmg',"-420",88,GROUND-30,(230,70,60)))
    if 90<=f<96: cl.update(x=ez(34,30,(f-90)/6))
    # 2) Estus, then PRAISE THE SUN!
    if 96<=f<116:
        cl.update(spr=KN['charge'],x=30,aura=((255,140,40),1) if 102<=f<114 else None)
        s['fx'].append(('ds_estus',38,GROUND-14,1 if 100<=f<114 else 0))
        if 102<=f<114:
            for j in range(3): s['fx'].append(('mote',24+(j*9+f*3)%16,GROUND-4-((f*2+j*7)%18),(255,170,60)))
    if 118<=f<140:
        cl.update(spr=KN['armsup'],x=30)
        s['fx'].append(('ds_sun',30,GROUND-26,int(5*ease((f-118)/6)) if f<134 else int(5*(1-(f-134)/6))))
        callout(s,"PRAISE THE SUN!",y=13,c=(250,200,70))
    # 3) Malenia's lunge: Claude dies
    if 138<=f<146: ml.update(spr=MAL['attack'],x=ez(150,58,(f-138)/8))
    if 140<=f<146: s['fx'].append(('ds_lunge',int(ml['x'])+6,150,GROUND-11))
    if 146<=f<162: ml.update(spr=MAL['attack'] if f<152 else mal_idle(f),x=58)
    if f==146: s['fx'].append(('spark',38,GROUND-10,7)); s['shake']=rshake(2); s.update(flash=0.35,fc=(38,GROUND-10),flashc=(230,60,50))
    if 146<=f<154: cl.update(spr=KN['hurt'],x=ez(30,22,(f-146)/8),y=GROUND-int(6*math.sin(math.pi*(f-146)/8)))
    if 154<=f<162: cl.update(spr=LYING,x=22)
    if 150<=f<162: s['fx'].append(('dim',0.6*(f-150)/12))
    if 162<=f<202: s['image']=closeup_died((f-162)/40,f); return s
    # 4) back up, plunging attack, ENEMY FELLED
    if 202<=f<216:
        cl.update(spr=LYING if f<205 else (KN['hurt'] if f<209 else KN[guard_pose(f)]),x=22 if f<209 else ez(22,30,(f-209)/5),
                  aura=((250,190,60),1) if f<214 else None)
        ml.update(spr=mal_idle(f),x=ez(58,120,(f-202)/10))
        if f<208: s['fx'].append(('dim',0.6*(1-(f-202)/6)))
    if 214<=f<224:
        t=(f-214)/10; cl.update(spr=KN['dash'],x=ez(30,118,t),y=GROUND-int(34*math.sin(math.pi*min(1,t*0.62)/1.0)))
        ml.update(x=120)
    if 224<=f<229:
        t=(f-224)/5; cl.update(spr=KN['plunge'],x=120,y=int(lerp(GROUND-33,GROUND-8,t))); ml.update(x=120)
        s['fx'].append(('tracer',120,120,int(lerp(GROUND-50,GROUND-40,t))))
    if f==229: s['shake']=rshake(3); s.update(flash=0.45,fc=(120,GROUND-12),flashc=(255,220,120))
    if 229<=f<236:
        cl.update(spr=KN['plunge'],x=120,y=GROUND-8); ml.update(spr=MAL['hurt'],x=121)
        s['fx'].append(('spark',120,GROUND-12,4+(f%2)*2))
        if f<234: s['fx'].append(('dmg',"-9999",108,GROUND-36,(250,210,90)))
    if 236<=f<262:
        cl.update(spr=KN[guard_pose(f)],x=ez(120,100,(f-236)/6))
        t=(f-236)/20
        ml.update(spr=MAL['hurt'],x=121,tint=(220,170,60),alpha=max(0,1-t),vis=t<1)
        s['fx'].append(('ds_motes',121,GROUND,min(1.4,t),60))
    if 240<=f<266:
        s['fx'].append(('ds_big',"ENEMY FELLED",20,(232,196,90),2))
        a=min(1,(f-240)/4) if f<262 else 1-(f-262)/4
        s['fx'].append(('ds_runes',int(lerp(0,480000,(f-244)/14)) if f>=244 else 0,a))
    # 5) the fog gate re-forms her; Claude walks back
    if 262<=f<N_:
        cl.update(spr=KN[guard_pose(f)],x=ez(100,30,(f-262)/18))
        s['under'].append(('ds_fogwall',150,min(1,(f-256)/6)*(1-ease((f-276)/10))))
        p=(f-264)/16
        ml.update(vis=p>0,holo=p if p<1 else None)
    s['fx'].append(('ds_hud',_hp(f),_st(f),_bhp(f),_btrail(f)))
    s['actors']=[ml,cl]
    return s

CLIPS = [clip('felled', N_, clip_felled)]
