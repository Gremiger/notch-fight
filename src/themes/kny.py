"""Kimetsu no Yaiba: Claude (Tanjiro-style) vs Akaza — Water Breathing, Hinokami Kagura."""
from engine import *

THEME = 'kny'

TANJ=variant(lambda s: recolor_rows(overlay(s,["..RR.RR.R.",".RRRRRRRRR"],-1,0),
    lambda x,y,t,l,r,c: ('X' if (x+y)%2 else 'Z') if (t+5<=y<=t+8 and c in 'Oo' and l<=x<=r) else None))

AKAZA=poses(S([
".....nnnn.......","....nnnnnn......","...nnPPPPn......","....PLyPyL......","....PPPPPP......",".....PLLP.......",
"...NNPLLPNN.....","..NNNPPPPNNN....","..PLNPLLPNLP....","..PL.PPPP.LP....","..PP.PLLP.PP....","..LP.PPPP.PL....",
".....WWWW.......",".....WWWW.......","....WW..WW......","....WW..WW......","....WW..WW......","....LP..PL......",
"....PP..PP......","...PPP..PPP.....",]),8,'PL',4)

def _decor(d):
    d.ellipse([164,3,176,15],fill=(236,228,180)); d.ellipse([167,1,179,13],fill=(0,0,0))
register_bg(THEME, lambda v: (v//2,v,v//2+6), _decor)

@fx('katana')
def _fx_katana(d,im,e,f):
    _,x0,y0,x1,y1,glow=e
    if glow: d.line([x0,y0,x1,y1],fill=glow,width=3)
    d.line([x0,y0,x1,y1],fill=(222,224,238))
    d.line([x0,y0,x0+(x1-x0)*0.18,y0+(y1-y0)*0.18],fill=(40,30,30),width=2)

@fx('wave')
def _fx_wave(d,im,e,f):
    # water trail between x0 and x1
    _,x0,x1,yb=e
    for x in range(int(min(x0,x1)),int(max(x0,x1))):
        y=yb+3*math.sin(x*0.35+f*0.7)
        d.point((x,int(y)),fill=(90,170,255)); d.point((x,int(y)-1),fill=(220,240,255)); d.point((x,int(y)+2),fill=(40,100,220))

@fx('firering')
def _fx_firering(d,im,e,f):
    _,x,y,r=e
    for i in range(14):
        a=i/14*6.283+f*0.6; px=x+math.cos(a)*r; py=y+math.sin(a)*r*0.8
        d.rectangle([px,py,px+1,py+1],fill=(255,120,40) if i%2 else (255,210,70))

@fx('ember')
def _fx_ember(d,im,e,f):
    _,x,y=e; d.point((int(x),int(y)),fill=random.choice([(255,140,40),(255,210,80),(230,70,30)]))

@fx('compass')
def _fx_compass(d,im,e,f):
    _,x,r=e
    for i in range(8):
        a=i/8*6.283; d.line([x,GROUND,x+math.cos(a)*r,GROUND+math.sin(a)*r*0.3],fill=(120,220,255))
    d.ellipse([x-r,GROUND-r*0.3,x+r,GROUND+r*0.3],outline=(80,160,230))

@fx('petal')
def _fx_petal(d,im,e,f):
    _,x,y=e; d.point((int(x)%W,int(y)),fill=(200,160,240)); d.point((int(x+1)%W,int(y)),fill=(160,120,210))


def katana_for(pose,x,y,flip,glow=None):
    s=-1 if flip else 1
    if pose in ('guard','guard2'): return ('katana',x+5*s,y-6,x+11*s,y-16,glow)
    if pose=='hurt': return ('katana',x+4*s,y-8,x-3*s,y-14,glow)
    return ('katana',x+8*s,y-5,x+20*s,y-7,glow)

def clip_breath(f):
    s=scene(f,'kny'); N=204
    cl=actor(TANJ[guard_pose(f)],28); ak=actor(AKAZA['idle'],150,flip=True)
    glow=None; pose='guard'
    for i in range(8):   # periodic wisteria petals: y advances 128px per clip -> seamless loop
        s['under'].append(('petal',i*23+10*math.sin(f*0.05+i),(i*13+f*128/N)%GROUND))
    if 12<=f<28:
        glow=(70,150,255)
        for i in range(6):
            a=f*0.5+i; s['fx'].append(('mote',cl['x']+math.cos(a)*9,GROUND-6+math.sin(a)*5,(120,190,255)))
        if f%4==0: s['fx'].append(('mote',cl['x']+3,GROUND-9,(230,230,240)))
    if 28<=f<40:
        t=(f-28)/8; cl['x']=ez(28,122,t); pose='dash'; glow=(70,150,255)
        s['under'].append(('wave',28,cl['x'],GROUND-5))
        if f>=36:
            s['fx'].append(('arc',140,GROUND-9,11,200,520,(120,200,255),2)); ak['spr']=AKAZA['hurt']
            s['fx'].append(('spark',138,GROUND-10,5)); s['shake']=rshake()
    if 36<=f<42: ak['x']=ez(150,160,(f-36)/6)
    if 40<=f<48:
        cl['x']=122; ak.update(x=160,spr=AKAZA['idle']); s['under'].append(('compass',160,6+(f-40)*2))
    if 48<=f<60:
        ak['spr']=AKAZA['attack']; t=(f-48)/12; cl.update(x=ez(122,34,t)); pose='hurt'
        for j in range(3): s['fx'].append(('circle',lerp(146,40,t)+j*8,GROUND-9,3+j,(120,220,255)))
        s['fx'].append(('dust',cl['x']+5,GROUND-random.randint(0,3)))
        if f==48: s['shake']=rshake(2); s['flash']=0.4; s['fc']=(146,GROUND-9); s['flashc']=(200,240,255)
    if 60<=f<72: ak['spr']=AKAZA['idle']; ak['x']=ez(160,150,(f-60)/12)
    if 60<=f<76:
        cl['x']=34; pose='charge'; glow=(255,120,40)
        for i in range(3): s['fx'].append(('ember',cl['x']+10+random.randint(0,10),GROUND-6-random.randint(0,10)))
        cl['aura']=((255,150,60),1+(f%2))
    if 76<=f<92:
        t=(f-76)/16; cl['x']=ez(34,128,t); cl['y']=GROUND-int(14*math.sin(math.pi*t))
        cl['flip']=(f//2)%2==1; pose='dash'; glow=(255,120,40)
        s['fx'].append(('firering',cl['x'],cl['y']-6,10))
        for i in range(3): s['fx'].append(('ember',cl['x']-random.randint(4,18),cl['y']-random.randint(0,12)))
    if 88<=f<96:
        s['fx'].append(('arc',146,GROUND-10,13,150,400,(255,140,50),3)); s['fx'].append(('arc',146,GROUND-10,10,160,390,(255,230,120),1))
        ak['spr']=AKAZA['hurt']
        if f==88: s['flash']=0.7; s['fc']=(146,GROUND-10); s['flashc']=(255,190,110); s['shake']=rshake(2)
    if 92<=f<108:
        cl.update(x=128,y=GROUND,flip=False); pose='punch'; glow=(255,120,40) if f<100 else None
        ak.update(spr=AKAZA['hurt'],x=ez(150,170,(f-92)/10))
        for i in range(2): s['fx'].append(('ember',ak['x']+random.randint(-6,6),GROUND-random.randint(0,20)))
    if 108<=f<150:
        ak['x']=ez(170,150,(f-108)/42); ak['spr']=AKAZA['hurt'] if f<124 else AKAZA['idle']
        if f<130:
            for i in range(3): s['fx'].append(('mote',ak['x']+random.randint(-6,6),GROUND-random.randint(0,22),(255,150,200)))
    if 108<=f<124:
        t=(f-108)/16; cl['x']=ez(128,28,t); cl['y']=GROUND-int(8*math.sin(math.pi*t)); pose='guard'
    if pose!='guard': cl['spr']=TANJ[pose]
    s['fx'].append(katana_for(pose,cl['x'],cl['y'],cl['flip'],glow))
    s['actors']=[cl,ak]
    return s

CLIPS = [clip('breath', 204, clip_breath)]
