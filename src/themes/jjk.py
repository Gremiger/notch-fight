"""Jujutsu Kaisen: Claude (Gojo-style) vs Sukuna — Infinity, Blue, Red, Hollow Purple."""
from engine import *

THEME = 'jjk'

GOJO=variant(lambda s: recolor_rows(overlay(s,[".H.H.H.H.H..",".HHHHHHHHHH.","..HhHHHhHH.."],-2,0),
    lambda x,y,t,l,r,c: 'b' if (y in (t+2,t+3) and l<=x<=r and c in 'OK') else None))

SUKUNA=poses(S([
".....n.n.n......","....nnnnnnn.....","....nPPPPPn.....","....PkrPkr......","....PPrPPr......","....PkPPPk......",
".....PPPP.......","...WWWWWWWW.....","..WWWkWWkWWW....","..WWW.WW.WWW....","..PPW.kk.WPP....","..kP.WWWW.Pk....",
".....WWWW.......",".....kkkk.......","....WWWWWW......","....WWWWWW......","....WW..WW......","....WW..WW......",
"....vv..vv......","...kkk..kkk.....",]),10,'Pk',4)

register_bg(THEME, lambda v: (v//2+4,v//2,v+14))

@fx('slash')
def _fx_slash(d,im,e,f):
    _,x,y,L,c=e; d.line([x,y,x+L,y-L*0.8],fill=c); d.line([x+1,y,x+L+1,y-L*0.8],fill=(255,255,255))

@fx('trail')
def _fx_trail(d,im,e,f):
    _,x0,x1,y,hh,a=e
    for x in range(int(max(0,x0)),int(min(W,x1))):
        for yy in range(int(y-hh),int(y+hh)+1): blend(im.load(),x,yy,(120,50,200),a*(0.4 if abs(yy-y)<hh-1 else 0.9))


def clip_infinity(f):
    s=scene(f,'jjk')
    cl=actor(GOJO[guard_pose(f)],30); sk=actor(SUKUNA['idle'],150,flip=True)
    if 12<=f<24: sk['spr']=SUKUNA['attack']
    if 16<=f<40:   # Dismantle vs Infinity
        for j in range(3):
            t0=16+j*3
            if f<t0: continue
            x=max(46+j*3,140-9*(f-t0)); y=GROUND-4-j*6
            if f<34: s['fx'].append(('slash',x,y,7,(230,230,255)))
        if f>=24:
            for r in range(3): s['fx'].append(('circle',44,GROUND-10,4+r*4+(f%3),(90,150,255) if r%2 else (170,210,255)))
        if f>=32:
            for i in range(4): s['fx'].append(('mote',46+random.randint(0,8),GROUND-random.randint(2,20),(220,220,255)))
    if 36<=f<60:   # Blue: attraction
        cl['spr']=GOJO['charge']
        s['fx'].append(('orbc',92,GROUND-14,3+(f-36)//8,((120,180,255),(40,90,240))))
        for i in range(10):
            a=i*2.4; ph=((f*0.06+i*0.13)%1); L=(1-ph)*40
            s['fx'].append(('mote',92+math.cos(a)*L,GROUND-14+math.sin(a)*L*0.6,(150,200,255)))
        if f>=44: sk.update(spr=SUKUNA['hurt'],x=ez(150,116,(f-44)/16))
        if f%3==0: s['shake']=rshake()
    if 60<=f<84:   # Red: repulsion
        cl['spr']=GOJO['punch']
        if f<68: s['fx'].append(('orbc',40,GROUND-6,1+(f-60)//3,((255,140,140),(220,30,40))))
        if 68<=f<74: s['fx'].append(('orbc',lerp(40,110,(f-68)/6),GROUND-8,3,((255,140,140),(220,30,40))))
        if f==74: s['flash']=0.8; s['fc']=(112,GROUND-10); s['flashc']=(255,120,120); s['fx'].append(('spark',112,GROUND-10,9))
        if f>=74:
            sk.update(spr=SUKUNA['hurt'],x=ez(116,172,(f-74)/10)); s['fx'].append(('ring',112,GROUND,(f-74)*3,(255,100,100)))
            if f<80: s['shake']=rshake(2)
        else: sk.update(x=116,spr=SUKUNA['hurt'])
    if 84<=f<96: sk.update(x=ez(172,150,(f-84)/12),spr=SUKUNA['idle'])
    if 96<=f<124:  # Hollow Purple forms
        cl['spr']=GOJO['armsup']; t=min(1,(f-96)/16)
        if t<1:
            s['fx'].append(('orbc',lerp(22,34,t),GROUND-24,3,((120,180,255),(40,90,240))))
            s['fx'].append(('orbc',lerp(46,34,t),GROUND-24,3,((255,140,140),(220,30,40))))
        else: s['fx'].append(('orbc',34,GROUND-24,3+(f-112)//3,((200,150,255),(130,50,210))))
        if f>=110: s['shake']=rshake()
    if 124<=f<146:
        cl['spr']=GOJO['charge']; t=(f-124)/18; x=lerp(40,210,t)
        s['under'].append(('trail',40,x,GROUND-10,9,0.8))
        s['fx'].append(('orbc',x,GROUND-10,9,((210,160,255),(120,40,200))))
        if x>=140: sk['vis']=False
        if 132<=f<136: s['flash']=0.9; s['fc']=(150,GROUND-10); s['flashc']=(220,170,255)
        s['shake']=rshake(2)
    if 146<=f<168:
        a=max(0,0.8-(f-146)/22*0.8); s['under'].append(('trail',40,W,GROUND-10,9,a)); sk['vis']=False
    if 164<=f<192:
        t=(f-164)/28; sk.update(vis=True,spr=SUKUNA['hurt'] if f<182 else SUKUNA['idle'],alpha=min(1,t*1.5))
        if f<180:
            for i in range(10):
                a=i*2.4+f*0.2; L=(1-t)*30; s['fx'].append(('mote',150+math.cos(a)*L,GROUND-10+math.sin(a)*L*0.6,(170,20,40)))
    s['actors']=[cl,sk]
    return s

CLIPS = [clip('infinity', 216, clip_infinity)]
