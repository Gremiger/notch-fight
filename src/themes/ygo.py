"""Yu-Gi-Oh: Claude (Yugi-style duelist) vs Kaiba — Dark Magician, Blue-Eyes, Mirror Force."""
from engine import *

THEME = 'ygo'

YUGI=variant(lambda s: recolor_rows(overlay(s,["K..K..K..K..","MK.MK.MK.MK.","KMKMKMKMKMKK",".KKKKKKKKKK."],-2,0,bangs=".Y.Y..Y."),
    lambda x,y,t,l,r,c: ('D' if (x==l-2 or x==l-1) else 'd' if x==l-3 else None) if (t+4<=y<=t+6 and l-3<=x<=l-1) else None))

KAIBA=poses(S([
".....qqqq.......","....qqqqqq......","....qqssss......","....qssks.......","....qsssss......",".....ssss.......",
"...WWkkkkWW.....","..WWWkkkkWWW....","..WWWkkkkWWW....","..WW.kkkk.WW....","..WW.kkkk.WW....","..Ws.kkkk.sW....",
".WW..kkkk..WW...",".WW..kkkk..WW...","WWv..kkkk..vWW..","Wv...kk.kk...vW.","W....kk.kk.....W",".....kk.kk......",
".....kk.kk......","....kkk.kkk.....",]),7,'Ws',3)
DARKMAG=S([
"..........pp....","........ppV.....",".......pVVp.....","......pVVVp.....",".....pVVVVVp....","....pVVVVVVVp...",
".....sssss......",".....sKsKs......",".....sssss..j...","....VVVVVVV.jj..","...VVVVVVVVVjj..","..VVpVVVVVpVsj..",
"..Vs.VVVVV..j...","....VVVVVVV.j...","....VVVVVVV.j...","...VVVVVVVVVj...","...VVpVVVpVVj...","..VVVVVVVVVVV...",
"..pp..ppp..pp...",])
BLUEEYES=S([
"....v.......v...............","...vWv.....vWv..............","..vWWWv...vWWWv.............",".vWWWWWv.vWWWWWv............",
"vWWWWWWWvWWWWWWWv.....WWW...","..vWWWWWWWWWWWWv.....WWWWWE.","....vWWWWWWWWWv.....WWWWWWWW","......vWWWWWWWWWWWWWWWv.vvv.",
".......WWWWWWWWWWWWv..v.v...","......WWWWWWWWWWWv..........",".....WWWWWWWWWWWW...........","....WWWvWWWWWWWWW...........",
"...WWW..WWWWWWWWW...........","..WW....WWW..WWW............",".WW.....WW....WW............","WW.....WWW...WWW............",])

def _decor(d):
    for x in range(8,W,12): d.point((x,GROUND+3),fill=(40,18,60))
register_bg(THEME, lambda v: (v+8,v//2,v+18), _decor)

@fx('card')
def _fx_card(d,im,e,f):
    # card flying/lying: x,y,face(bool),glow
    _,x,y,face,glow=e; x,y=int(x),int(y)
    if glow: d.rectangle([x-4,y-5,x+4,y+5],outline=glow)
    d.rectangle([x-3,y-4,x+3,y+4],fill=(170,70,150) if face else (120,76,40)); d.rectangle([x-2,y-3,x+2,y+3],outline=(236,210,120))

@fx('flatcard')
def _fx_flatcard(d,im,e,f):
    _,x,c=e; x=int(x); d.rectangle([x-4,GROUND-1,x+4,GROUND],fill=c)

@fx('pillar')
def _fx_pillar(d,im,e,f):
    _,x,a,c=e; x=int(x)
    for dx in range(-3,4):
        aa=a*(1-abs(dx)/4)
        for y in range(0,GROUND):
            if (y+f)%2==0: blend(im.load(),x+dx,y,c,aa*(y/GROUND))

@fx('barrier')
def _fx_barrier(d,im,e,f):
    _,x,a=e
    for y in range(GROUND-28,GROUND+1):
        for dx in (-1,0,1):
            blend(im.load(),int(x+dx+math.sin(y*0.5+f)*0.8),y,[(255,120,120),(255,240,120),(120,255,160),(120,180,255),(220,130,255)][(y//3+f)%5],a*(0.9-abs(dx)*0.35))

@fx('lpbar')
def _fx_lpbar(d,im,e,f):
    _,x0,frac,c=e
    d.rectangle([x0,1,x0+34,3],fill=(40,30,50)); d.rectangle([x0,1,x0+int(34*frac),3],fill=c)


def clip_duel(f):
    s=scene(f,'ygo'); N=216
    cl=actor(YUGI[guard_pose(f)],24); kb=actor(KAIBA['idle'],160,flip=True)
    dm=actor(DARKMAG,62,vis=False,holo=1.0); be=actor(BLUEEYES,130,flip=True,vis=False,holo=1.0)
    lp_k=1.0
    if 12<=f<24:
        cl['spr']=YUGI['punch']; s['fx'].append(('card',cl['x']+6,GROUND-14-(f-12),False,(255,240,160)))
        if f>=18: s['fx'].append(('twinkle',cl['x']+9,GROUND-19-(f-12),2))
    if 24<=f<36:
        t=(f-24)/12; s['fx'].append(('card',lerp(30,62,t),lerp(GROUND-26,GROUND-3,t),True,None))
    if 34<=f<156: s['under'].append(('flatcard',62,(150,70,200)))
    if 34<=f<48: s['under'].append(('pillar',62,0.9-(f-34)/20,(190,120,255)))
    if 36<=f<150: dm.update(vis=True,holo=min(1,(f-36)/12))
    if 48<=f<60:
        kb['spr']=KAIBA['attack']
        t=(f-48)/10; s['fx'].append(('card',lerp(150,124,min(1,t)),lerp(GROUND-20,GROUND-3,min(1,t)),True,(160,220,255)))
    if 58<=f<108: s['under'].append(('flatcard',124,(90,150,230)))
    if 58<=f<72: s['under'].append(('pillar',124,0.9-(f-58)/20,(170,220,255)))
    if 60<=f<96: be.update(vis=True,holo=min(1,(f-60)/12))
    if 70<=f<76: s['shake']=rshake()
    if 76<=f<96:   # White Lightning
        hx=116; tgt=80 if f>=84 else lerp(hx,74,(f-76)/8)
        s['fx'].append(('beam',tgt,hx,GROUND-13,((200,230,255),(90,160,255))))
    if 82<=f<108:  # Mirror Force: trap flips up, barrier reflects
        s['fx'].append(('card',80,GROUND-5,True,(255,120,160))) if f<88 else None
        s['fx'].append(('barrier',80,min(0.9,(f-82)/4)*(1 if f<100 else (108-f)/8)))
    if 86<=f<98:
        s['fx'].append(('beam',80,lerp(80,118,(f-86)/6),GROUND-15,((255,230,255),(230,140,255))))
        s['shake']=rshake()
    if 96<=f<120:  # Blue-Eyes shatters
        be['vis']=False; rr=random.Random(7); t=f-96
        for j,row in enumerate(BLUEEYES):
            for i,ch in enumerate(row):
                if ch=='.' or rr.random()<0.55: continue
                vx=rr.uniform(-2.2,2.2); vy=rr.uniform(-2.5,0.8)
                x=130+ (len(row)/2-i) + vx*t; y=GROUND-len(BLUEEYES)+j+vy*t+0.12*t*t
                if y<GROUND and rr.random()>t/26: s['fx'].append(('shard',x,y,PAL.get(ch,(255,255,255))))
        if f<100: s['flash']=0.5; s['fc']=(124,GROUND-12); s['flashc']=(210,230,255)
    if 96<=f<176: lp_k=max(0.25,1-(f-96)/24*0.75) if f<130 else max(0,0.25-(f-124)/10*0.25)
    if 96<=f<120: kb['spr']=KAIBA['hurt']
    if 108<=f<132:  # Dark Magic Attack
        if f<118: s['fx'].append(('circle',68,GROUND-18,2+(f-108),(200,120,255)))
        if 116<=f<126: s['fx'].append(('orbc',lerp(70,154,(f-116)/10),GROUND-12,3,((120,60,200),(40,10,70))))
        if f==126: s['fx'].append(('spark',156,GROUND-12,8)); s['flash']=0.6; s['fc']=(156,GROUND-12); s['flashc']=(220,170,255)
        if f>=126: kb.update(spr=KAIBA['hurt'],x=ez(160,168,(f-126)/6)); s['shake']=rshake() if f<130 else (0,0)
    if 132<=f<160: kb['x']=ez(168,160,(f-132)/28); kb['spr']=KAIBA['hurt'] if f<146 else KAIBA['idle']
    if 136<=f<150: dm['holo']=max(0,1-(f-136)/14)
    if 176<=f<200: lp_k=(f-176)/24
    if 176<=f<N: s['fx'].append(('twinkle',162,2,1)) if f<200 and f%4==0 else None
    if f>=200: lp_k=1.0
    s['fx']+=[('lpbar',3,1.0,(232,120,80)),('lpbar',148,lp_k,(90,160,255))]
    s['actors']=[dm,be,cl,kb]
    return s

CLIPS = [clip('duel', 216, clip_duel)]
