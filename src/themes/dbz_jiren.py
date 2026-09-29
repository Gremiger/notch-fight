"""Dragon Ball sub-theme "dbz-jiren": Claude awakens Ultra Instinct (silver hair and aura), dodges
Jiren's barrage without effort, vanishes, reappears BEHIND him — a beat of silence — and Jiren
takes a flood of instant hits from everywhere at once."""
from engine import *

THEME = 'dbz-jiren'

JIREN=poses(S([
"....DDDDDDD.......","...DDDDDDDDD......","..DDDDDDDDDDD.....","..DDKKKDKKKDD.....","..DDKKKDKKKDD.....",
"..DDDDDDDDDDD.....","...DDDdddDDD......","....DDDDDDD.......",".RRRRRRRRRRRRR....","RRRRRkkkkRRRRRR...",
"RRR.RRkkRR.RRRR...","RRR.RRkkRR.RRR....","DDD.RRkkRR.DDD....","HHH.kkkkkk.HHH....","....kkkkkk........",
"....kkk.kkk.......","....kkk.kkk.......","....kkk.kkk.......","....RR...RR.......","...RRR...RRR......",]),10,'RR',3)

UI=variant(lambda s: overlay(s,["..H..v..H...",".HvH.HvHHv..","HHHHHHHHHHH."],-2,0))   # silver hair
UI_AURA=(210,222,255)
GHOST=(190,205,255)
JI_KI=((255,160,160),(230,50,50))

register_bg(THEME, lambda v: (v//2+6,v//2+8,v+12))

@fx('speed')
def _fx_speed(d,im,e,f):
    """Speed lines converging on a point."""
    _,x,y=e; rr=random.Random(f)
    for _ in range(10):
        a=rr.random()*6.28; r0=rr.randint(14,22); r1=r0+rr.randint(8,20)
        d.line([x+math.cos(a)*r0,y+math.sin(a)*r0*0.6,x+math.cos(a)*r1,y+math.sin(a)*r1*0.6],fill=(220,228,255))

def ghost(x,spr,flip=False,a=0.35,tint=GHOST):
    return actor(spr,x,flip=flip,alpha=a,tint=tint)

def clip_ultra(f):
    s=scene(f,THEME)
    cl=actor(CL[guard_pose(f)],30); ji=actor(JIREN['idle'],150,flip=True); extra=[]
    ui=36<=f<236
    # 1) awakening: silver motes gather, the aura bursts
    if 12<=f<40:
        t=(f-12)/28
        for i in range(10):
            a=i*0.63+f*0.1; L=(1-t)*34+4
            s['fx'].append(('mote',30+math.cos(a)*L,GROUND-6+math.sin(a)*L*0.5,UI_AURA if i%2 else (150,180,255)))
    if f==36: s['flash']=1.0; s['fc']=(30,GROUND-8); s['flashc']=(225,232,255)
    if 36<=f<44: s['fx'].append(('ring',30,GROUND-4,(f-36)*5,UI_AURA)); s['shake']=rshake()
    if ui:
        cl['spr']=UI[guard_pose(f)]; cl['aura']=(UI_AURA,1+((f//2)%2))
        if f%3==0: s['fx'].append(('mote',30+random.randint(-8,8),GROUND-random.randint(10,18),(170,200,255)))
    if 38<=f<56: callout(s,"MIGATTE NO GOKUI",c=(210,222,255))
    # 2) Jiren's barrage: every punch lands on an afterimage
    if 56<=f<96:
        k=(f-56)//8; ph=(f-56)%8
        ji.update(spr=JIREN['attack'] if ph<4 else JIREN['idle'],x=58 if f>=60 else lerp(150,58,(f-56)/4))
        dodge=[16,34,20,36,18][k]
        cl.update(x=dodge if ph>=2 else [30,16,34,20,36][k])
        if ph<3: extra.append(ghost([30,16,34,20,36][k],UI['guard']))
        if ph==2: s['fx'].append(('mote',46,GROUND-7,(255,255,255)))
        if f%8==1: s['fx'].append(('dmg',"MISS",44+k*2,GROUND-22,(200,210,240)))
    if 96<=f<104: ji.update(spr=JIREN['attack'],x=58); s['fx'].append(('orbc',lerp(46,20,(f-96)/8),GROUND-8,3,JI_KI))
    if 99<=f<104: cl['vis']=(f%2==0); extra.append(ghost(30,UI['guard'],a=0.5))
    # 3) gone — and behind him
    if 104<=f<124:
        cl.update(vis=True,x=78,flip=True); ji.update(spr=JIREN['idle'],x=58)
        if f<106: cl['vis']=False
        if f>=108: s['fx'].append(('dmg',"!",ji['x']-2,GROUND-28,(255,255,255)))
    if 104<=f<112: s['fx'].append(('twinkle',78,GROUND-8,1+(f%2)))
    # 4) instant hits from everywhere
    if 124<=f<170:
        rr=random.Random(f*5); ji.update(spr=JIREN['hurt'],x=58+rr.randint(-1,1),y=GROUND-rr.randint(0,1))
        cl['vis']=False
        for j in range(4):
            gx=58+rr.choice([-18,-14,14,18]); extra.append(ghost(gx,UI[rr.choice(['punch','dash'])],flip=gx>58,a=0.5,tint=None))
        for j in range(3): s['fx'].append(('spark',58+rr.randint(-8,8),GROUND-rr.randint(4,18),rr.randint(2,4)))
        s['fx'].append(('speed',58,GROUND-10))
        if f%4==0: s['fx'].append(('ring',58,GROUND-10,6+(f%8),UI_AURA)); s['shake']=rshake(2)
        s['fx'].append(('dmg',str((f-124)*37+12),120,GROUND-30,(230,236,255)))
    if 170<=f<178:   # the last palm strike
        cl.update(vis=True,spr=UI['punch'],x=42,flip=False); ji.update(spr=JIREN['hurt'],x=lerp(58,120,(f-170)/8))
        if f==170: s['flash']=1.0; s['fc']=(56,GROUND-10); s['flashc']=(225,232,255); s['fx'].append(('boom',56,GROUND-10,10))
        s['shake']=rshake(2)
    if 178<=f<200: ji.update(spr=JIREN['hurt'],x=ez(120,172,(f-178)/12)); cl.update(spr=UI['guard'],x=42)
    if 200<=f<236: ji.update(spr=JIREN['hurt'] if f<214 else JIREN['idle'],x=ez(172,150,(f-200)/28)); cl['x']=ez(42,30,(f-200)/20)
    if 226<=f<236: cl['aura']=(UI_AURA,1) if f%2 else None
    s['actors']=extra+[cl,ji]
    return s

CLIPS = [clip('ultra', 264, clip_ultra)]
