"""Pokemon: Claude (Ash cap) vs Mewtwo — Game Boy battle screen with HP bars and text box."""
from engine import *

THEME = 'pkm'

PAL.update({'m':(206,196,222),'u':(150,92,176),'U':(120,40,160)})
ASH=variant(lambda s: overlay(s,["..rrrrrr....",".rrrHHrrr...",".rrrrrrrrrrr"],-1,0))
MEWTWO=poses(S([
".....mm.mm........",".....mmmmm........","....mmmmmmm.......","....mmmUmmU.......","....mmmmmmm.......",".....mmmmm........",
"......mmm.........","....mmmmmmm.......","...mmmmmmmmm......","..mm.mmmmm.mm.....","..mm.muuum.mm.....","..m..muuum..m.....",
"uu...muuum........","uu...uuuuu........",".uu.uuu.uuu.......","..uuu...uu........","...mm.....mm......","...mm.....mm......",
"..mmm.....mmm.....",]),9,'mm',4)

register_bg(THEME, lambda v: (v//3,v,v//3))

def hp_color(v): return (40,210,90) if v>0.5 else (240,200,40) if v>0.2 else (230,50,40)

@fx('hp')
def _fx_hp(d,im,e,f):
    _,x0,name,v=e; text(d,name,x0,1,(240,240,240)); d.rectangle([x0,8,x0+34,9],fill=(40,40,40))
    if v>0: d.rectangle([x0,8,x0+int(34*v),9],fill=hp_color(v))

@fx('textbox')
def _fx_textbox(d,im,e,f):
    _,l1,l2=e; d.rectangle([46,10,139,24],fill=(0,0,0),outline=(236,236,236))
    text(d,l1,49,12,(240,240,240)); text(d,l2,49,18,(240,240,240))

@fx('pball')
def _fx_pball(d,im,e,f):
    _,x,y,op=e; x,y=int(x),int(y); o=int(op)
    d.ellipse([x-3,y-3-o,x+3,y+3-o],fill=(230,40,40)) if o else None
    d.pieslice([x-3,y-3-o,x+3,y+3-o],180,360,fill=(230,40,40)); d.pieslice([x-3,y-3+o,x+3,y+3+o],0,180,fill=(240,240,240))
    d.line([x-3,y,x+3,y],fill=(20,20,20)); d.point((x,y),fill=(240,240,240))

@fx('psywave')
def _fx_psywave(d,im,e,f):
    _,x0,x1,y0,y1=e
    for j in range(3):
        pts=[(x,lerp(y0,y1,(x-x0)/max(1,x1-x0))+3*math.sin(x*0.4+f*0.8+j*2)) for x in range(int(min(x0,x1)),int(max(x0,x1)),2)]
        if len(pts)>1: d.line(pts,fill=(200,120,255) if j%2 else (150,80,230))

@fx('platform')
def _fx_platform(d,im,e,f):
    _,x=e; d.ellipse([x-16,GROUND-2,x+16,GROUND+3],outline=(60,90,60))


def clip_psychic(f):
    s=scene(f,'pkm'); N=240
    hov=GROUND-3+round(2*math.sin(2*math.pi*f/24))
    cl=actor(ASH[guard_pose(f)],30); mw=actor(MEWTWO['idle'],150,y=hov,flip=True)
    hc=hm=1.0; msg=None
    s['under']+=[('platform',30),('platform',150)]
    if 12<=f<48: msg=("CLAUDE USED","QUICK ATTACK!")
    if 18<=f<30:
        t=(f-18)/12; cl['x']=lerp(30,134,t); cl['y']=GROUND-int(6*abs(math.sin(t*math.pi*3))); cl['spr']=ASH['dash']
        cl['aura']=((255,255,255),1)
        for i in range(3): y=random.randint(30,58); x=random.randint(0,120); s['fx'].append(('tracer',x,x+10,y))
    if f==30: s['fx'].append(('spark',142,hov-10,7)); s['shake']=rshake(2)
    if 30<=f<34: cl.update(x=134,spr=ASH['punch']); mw['spr']=MEWTWO['hurt']
    if f>=30: hm=0.8
    if 34<=f<46: t=(f-34)/12; cl.update(x=ez(134,30,t),y=GROUND-int(8*math.sin(math.pi*t)))
    if 48<=f<96:
        msg=("MEWTWO USED","PSYCHIC!"); mw['spr']=MEWTWO['attack']; mw['aura']=((200,120,255),1+(f%2))
        if 54<=f<90:
            lift=ez(0,18,(f-54)/10) if f<86 else ez(18,0,(f-86)/4)
            cl.update(y=GROUND-int(lift)+random.choice([-1,0,1]),x=30+random.choice([-1,0,1]),spr=ASH['hurt'],aura=((200,120,255),2))
            s['under'].append(('psywave',40,140,cl['y']-6,hov-10))
            s['fx'].append(('circle',cl['x'],cl['y']-6,2+(f*2)%10,(200,120,255)))
            hc=lerp(1,0.55,(f-60)/30) if f>=60 else 1
        if f==90: s['shake']=rshake(2); s['fx'].append(('spark',30,GROUND-4,6))
        if 90<=f<96:
            for i in range(2): s['fx'].append(('dust',30+random.randint(-8,8),GROUND-random.randint(0,3)))
    if f>=90: hc=0.55
    if 96<=f<136:
        msg=("CLAUDE USED","FLAMETHROWER!"); cl['spr']=ASH['charge']; cl['aura']=((255,150,60),1+(f%2))
        if 102<=f<130:
            for i in range(16):
                t=((f*0.09+i/16)%1); x=lerp(42,140,t); y=GROUND-6+lerp(0,hov-10-(GROUND-6),t)+math.sin(i*1.7+f*0.9)*t*4
                c=[(255,240,160),(255,190,70),(240,110,40),(200,60,30)][min(3,int(t*4))]
                s['fx'].append(('smoke',x,y,1+int(t*2.5),c))
        if f>=110: mw['spr']=MEWTWO['hurt']; hm=lerp(0.8,0.25,(f-110)/20)
    if f>=130: hm=0.25
    if 136<=f<152:
        msg=("MEWTWO USED","SHADOW BALL!"); mw['spr']=MEWTWO['attack']
        if f>=138:
            x=140-10*(f-138)
            if x>-10: s['fx'].append(('orbc',x,GROUND-8,3,((90,40,130),(30,10,50))))
        if 142<=f<154: t=(f-142)/12; cl['y']=GROUND-int(16*math.sin(math.pi*t))
    if 152<=f<172: msg=("CLAUDE THREW A","POKE BALL!")
    if 154<=f<160: cl['spr']=ASH['punch']
    if 156<=f<166:
        t=(f-156)/10; s['fx'].append(('pball',lerp(38,150,t),lerp(GROUND-10,hov-12,t)-14*math.sin(math.pi*t),0))
    if 166<=f<172:
        mw.update(tint=(255,70,70),alpha=1-(f-166)/6); s['fx'].append(('pball',150,hov-12,2))
        s['fx'].append(('tracer',146,154,hov-12))
    if 172<=f<200:
        mw['vis']=False; wob=(1 if f in range(176,180) or f in range(192,196) else -1 if f in range(184,188) else 0)
        s['fx'].append(('pball',150+wob,GROUND-3,0)); msg=(".  .  .","") if f<188 else (".  .  .  .","")
    if 200<=f<224:
        msg=("OH NO!","IT BROKE FREE!")
        if f<204: s['flash']=0.8; s['fc']=(150,GROUND-8); s['flashc']=(255,255,255)
        if f<206: s['fx'].append(('pball',150,GROUND-3,3))
        mw.update(tint=(255,70,70) if f<208 else None,alpha=min(1,(f-200)/6))
    if 216<=f<232: hc=lerp(0.55,1,(f-216)/16); hm=lerp(0.25,1,(f-216)/16)
    if f>=232: hc=hm=1.0
    s['fx']+=[('hp',3,'CLAUDE',hc),('hp',148,'MEWTWO',hm)]
    if msg: s['fx'].append(('textbox',)+msg)
    s['actors']=[cl,mw]
    return s

CLIPS = [clip('psychic', 240, clip_psychic)]
