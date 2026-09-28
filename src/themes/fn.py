"""Fortnite: Claude (default + pickaxe) vs Geno — builds, damage numbers, Victory Royale, Battle Bus."""
from engine import *

THEME = 'fn'

PAL.update({'A':(26,24,32),'Q':(212,170,60),'F':(150,96,52)})
JONES=variant(lambda s: recolor_rows(s,
    lambda x,y,t,l,r,c: ('F' if x==l-1 else 'k') if (t+1<=y<=t+6 and l-2<=x<=l-1 and c in '.o') else None))
GENO=poses(S([
".....kkkk.......","....kkHkkk......","....kkHkss......","....kssEsE......","....ksssss......",".....ssss.......",
"...AAAQAAAA.....","..AAAArQAAAA....","..AQAArrAAQA....","..AA.AQQAA.AA...","..AA.ArrA..AA...","..AA.AAAA..sA...",
"..ss.AQQA.......",".....AAAA.......","....AA..AA......","....AQ..QA......","....AA..AA......","....Ar..rA......",
"....AA..AA......","...AAA..AAA.....",]),9,'As',4)

register_bg(THEME, lambda v: (v//2,v,v//3+4))

@fx('pickaxe')
def _fx_pickaxe(d,im,e,f):
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(150,96,52))
    dx,dy=x1-x0,y1-y0; L=max(1,math.hypot(dx,dy)); nx,ny=-dy/L,dx/L
    d.line([x1-nx*3,y1-ny*3,x1+nx*3,y1+ny*3],fill=(190,200,215),width=2)

@fx('wall')
def _fx_wall(d,im,e,f):
    _,x,prog=e; top=GROUND-16; x=int(x)
    if prog<1:
        d.rectangle([x,top,x+3,GROUND],outline=(90,170,255))
        d.rectangle([x,int(GROUND-16*prog),x+3,GROUND],fill=(80,140,230))
    else:
        d.rectangle([x,top,x+3,GROUND],fill=(176,118,60))
        for yy in range(top+3,GROUND,4): d.line([x,yy,x+3,yy],fill=(120,76,36))

@fx('ramp')
def _fx_ramp(d,im,e,f):
    _,x0,prog=e; L=int(24*prog)
    for i in range(L):
        yy=GROUND-int(i*0.66); c=(80,140,230) if prog<1 else ((176,118,60) if i%5 else (120,76,36))
        d.line([x0+i,yy,x0+i,yy+2],fill=c)

@fx('bars')
def _fx_bars(d,im,e,f):
    _,x0,hp,sh,flip=e
    d.rectangle([x0,1,x0+30,2],fill=(30,30,30)); d.rectangle([x0,4,x0+30,5],fill=(30,30,30))
    if flip:
        if sh>0: d.rectangle([x0+30-int(30*sh),1,x0+30,2],fill=(60,150,255))
        if hp>0: d.rectangle([x0+30-int(30*hp),4,x0+30,5],fill=(40,210,90))
    else:
        if sh>0: d.rectangle([x0,1,x0+int(30*sh),2],fill=(60,150,255))
        if hp>0: d.rectangle([x0,4,x0+int(30*hp),5],fill=(40,210,90))

@fx('banner')
def _fx_banner(d,im,e,f):
    _,a=e
    if a<=0: return
    w=64; x0=W//2-w//2
    for x in range(x0,x0+w):
        for y in range(8,19): blend(im.load(),x,y,(40,70,190) if 9<y<17 else (250,210,60),a)
    if a>0.6: text(d,"VICTORY ROYALE",x0+4,11,(255,226,90),(20,30,90))

@fx('chest')
def _fx_chest(d,im,e,f):
    _,x,open_=e; x=int(x)
    d.rectangle([x-5,GROUND-5,x+5,GROUND],fill=(200,150,40)); d.rectangle([x-5,GROUND-5,x+5,GROUND-4],fill=(250,210,70))
    d.rectangle([x-1,GROUND-4,x+1,GROUND-2],fill=(90,60,20))
    if open_:
        for i in range(5): d.line([x-4+i*2,GROUND-6,x-8+i*4,GROUND-6-12],fill=(255,236,150))

@fx('rifle')
def _fx_rifle(d,im,e,f):
    _,x,y,flip=e; s_=-1 if flip else 1
    d.line([x,y,x+9*s_,y],fill=(240,200,60),width=2); d.point((x+2*s_,y+2),fill=(200,160,40))

@fx('potion')
def _fx_potion(d,im,e,f):
    _,x,y=e; d.rectangle([x-1,y-3,x+1,y+1],fill=(80,170,255)); d.point((x,y-4),fill=(230,230,240))

@fx('bus')
def _fx_bus(d,im,e,f):
    _,x,y=e; x,y=int(x),int(y)
    d.ellipse([x-6,y-9,x+6,y-1],fill=(60,120,230)); d.line([x-3,y-1,x-4,y+2],fill=(200,200,210)); d.line([x+3,y-1,x+4,y+2],fill=(200,200,210))
    d.rectangle([x-8,y+2,x+8,y+7],fill=(40,110,220)); d.rectangle([x-7,y+3,x+6,y+4],fill=(190,230,255)); d.rectangle([x-8,y+6,x+8,y+7],fill=(250,210,60))

@fx('glider')
def _fx_glider(d,im,e,f):
    _,x,y=e; d.arc([x-8,y-6,x+8,y+4],180,360,fill=(250,210,60),width=2); d.line([x-6,y-1,x,y+6],fill=(200,200,210)); d.line([x+6,y-1,x,y+6],fill=(200,200,210))

@fx('storm')
def _fx_storm(d,im,e,f):
    for x in list(range(0,5))+list(range(W-5,W)):
        a=0.5*(1-min(x,W-1-x)/5)
        for y in range(0,H,2): blend(im.load(),x,(y+f)%H,(150,60,220),a)


def dmg(s,f,t0,txt,x,y,c):
    if t0<=f<t0+14: s['fx'].append(('dmg',txt,x,y-(f-t0)*0.7,c))

def clip_royale(f):
    s=scene(f,'fn'); N=228
    cl=actor(JONES[guard_pose(f)],28); gn=actor(GENO['idle'],152,flip=True)
    gn['pal']={'r':(255,60,60) if (f//4)%2 else (170,20,30)}
    ch,cs,gh,gs=1.0,1.0,1.0,1.0; tool='pick'; pose=None
    s['under'].append(('storm',))
    if 12<=f<28:
        gn['spr']=GENO['attack']
        for j in range(3):
            t0=12+j*4
            if t0<=f: x=140-8*(f-t0)
            if t0<=f and x>50: s['fx'].append(('orbc',x,GROUND-10-j*2,1,((255,120,120),(220,30,40))))
            if t0<=f and x<=50 and f-t0<(140-50)//8+2: s['fx'].append(('spark',48,GROUND-10-j*2,3))
    if 14<=f<48: s['under'].append(('wall',46,min(1,(f-14)/4)))
    if 24<=f<48: s['under'].append(('ramp',50,min(1,(f-24)/5)))
    if 28<=f<36:
        t=(f-28)/8; cl['x']=lerp(28,48,t); pose='dash'
    if 36<=f<44:
        t=(f-36)/8; cl['x']=lerp(50,72,t); cl['y']=GROUND-int(t*15); pose='dash'
    if 44<=f<52:
        t=(f-44)/8; cl['x']=lerp(72,138,t); cl['y']=GROUND-15+int(15*t*t)-int(10*math.sin(math.pi*t)); pose='punch'
    if f==52: s['fx'].append(('spark',146,GROUND-14,7)); s['shake']=rshake(2)
    dmg(s,f,52,"74",140,GROUND-26,(90,170,255))
    if f>=52: gs=0.26
    if 52<=f<60: gn['spr']=GENO['hurt']; cl.update(x=138,y=GROUND); pose='punch'
    if 60<=f<72:   # Geno slam shockwave
        gn['spr']=GENO['attack']; t=(f-60)/12; cl['x']=ez(138,36,t); cl['y']=GROUND-int(8*math.sin(math.pi*t)); pose='hurt'
        s['fx'].append(('ring',150-(f-60)*5,GROUND,6,(255,80,80)))
        if f==60: s['flash']=0.5; s['fc']=(150,GROUND-8); s['flashc']=(255,120,120); s['shake']=rshake(2)
    dmg(s,f,62,"50",40,GROUND-22,(90,170,255))
    if f>=62: cs=0.5
    if 72<=f<88:
        cl['x']=36; tool=None; pose='punch' if (f//3)%2 else 'guard'
        s['fx'].append(('potion',cl['x']+8,GROUND-6)); cs=0.5+0.5*(f-72)/16
        if f%3==0: s['fx'].append(('mote',cl['x']+random.randint(-4,4),GROUND-12-random.randint(0,6),(120,200,255)))
    if f>=88: cs=1.0
    if 72<=f<140: gn['spr']=GENO['idle'] if f<96 else GENO['hurt'] if f<112 else gn['spr']
    if 88<=f<100:
        cl['x']=ez(36,40,(f-88)/12); tool=None
        s['under'].append(('chest',56,f>=92))
        if f>=92: s['fx'].append(('twinkle',56,GROUND-14-(f-92),2))
    if 100<=f<116:
        tool='rifle'; pose='punch'
        if f%3==0:
            s['fx'].append(('tracer',52,144,GROUND-6)); s['fx'].append(('spark',146,GROUND-10+random.randint(-3,3),3))
    for j,t0 in enumerate(range(100,116,3)): dmg(s,f,t0,"32",140+(j%2)*6,GROUND-28+(j%3)*2,(255,255,255) if j>0 else (90,170,255))
    if f>=100: gs=0.0; gh=max(0,1-(f-100)/15)
    if 116<=f<136:   # eliminated: dissolves into rising cubes
        gn['vis']=False; rr=random.Random(3); t=f-116
        for j,row in enumerate(GENO['hurt']):
            for i,c in enumerate(row):
                if c=='.' or rr.random()<0.6: continue
                x=152+(len(row)/2-i)+rr.uniform(-1,1)*t*0.5; y=GROUND-len(GENO['hurt'])+j-t*rr.uniform(0.8,2.2)
                if rr.random()>t/22: s['fx'].append(('shard',x,y,(120,200,255) if (i+j+f)%3 else (255,255,255)))
    if 116<=f<200 and not (184<=f): gn['vis']=False
    if 124<=f<164:   # Victory Royale + default dance
        a=min(1,(f-124)/6) if f<152 else max(0,1-(f-152)/12)
        s['fx'].append(('banner',a)); tool=None
        dance=['guard','armsup','guard2','punch']; pose=dance[(f//3)%4]; cl['flip']=(f//6)%2==1
    if 136<=f<200:   # battle bus drops Geno back in
        s['fx'].append(('bus',lerp(-20,W+20,(f-136)/64),9))
    if 160<=f<200:
        t=(f-160)/40; x=lerp(100,152,t); y=lerp(30,GROUND,t)
        if f>=162: gn.update(vis=True,x=x,y=y,spr=GENO['idle']); s["fx"].append(("glider",x,y-22)) if f<198 else None
        gs=gh=min(1,t*1.3)
    elif f>=200: gs=gh=1.0
    if pose: cl['spr']=JONES[pose]
    p=pose or 'guard'
    if tool=='pick':
        sx=-1 if cl['flip'] else 1
        if p in ('guard','guard2'): s['fx'].append(('pickaxe',cl['x']+5*sx,cl['y']-5,cl['x']+9*sx,cl['y']-15))
        elif p=='hurt': s['fx'].append(('pickaxe',cl['x']+4*sx,cl['y']-8,cl['x']-3*sx,cl['y']-15))
        else: s['fx'].append(('pickaxe',cl['x']+8*sx,cl['y']-5,cl['x']+17*sx,cl['y']-9))
    elif tool=='rifle': s['fx'].append(('rifle',cl['x']+8,GROUND-6,False))
    s['fx']+=[('bars',3,ch,cs,False),('bars',151,gh,gs,True)]
    s['actors']=[cl,gn]
    return s

CLIPS = [clip('royale', 228, clip_royale)]
