"""Shingeki no Kyojin: Claude (Survey Corps, ODM gear) vs 5 titans and the Armored Titan."""
from engine import *

THEME = 'snk'

PAL.update({'t':(232,186,160),'T':(194,146,122),'z':(208,174,112),'a':(132,100,62)})
SCOUT=variant(lambda s: recolor_rows(s,
    lambda x,y,t,l,r,c: ('X' if c in '.o' and x<l else None) if (t+1<=y<=t+8 and l-2<=x<l) else
                        ('F' if (y==t+6 and l<=x<=r and c=='O') else ('D' if (y==t+7 and x in (l,r)) else None))))

_TCACHE={}
def titan(h,hair,walk=0,armored=False):
    key=(h,hair,walk,armored)
    if key in _TCACHE: return _TCACHE[key]
    w=max(11,int(h*0.5))|1; cx=w//2; g=[['.']*w for _ in range(h)]
    sk,sh=('z','a') if armored else ('t','T')
    hh=max(7,int(h*0.3)); hw=max(5,int(w*0.6))
    for y in range(hh):
        for x in range(w):
            if ((x-cx)/(hw/2))**2+((y-hh/2+0.5)/(hh/2))**2<=1:
                g[y][x]=hair if (y<hh*0.35 or (y<hh*0.65 and abs(x-cx)>=hw/2-1)) else sk
    ey=int(hh*0.5); g[ey][cx-2]='K'; g[ey][cx+1]='K'
    my=int(hh*0.78)
    for x in range(cx-hw//3,cx+hw//3+1): g[my][x]='H'
    g[my][cx-hw//3-1]='K'; g[my][cx+hw//3+1]='K'
    g[hh][cx-1]=g[hh][cx]=g[hh][cx+1]=sk
    th=int(h*0.33); tw=max(5,int(w*0.62)); t0=hh+1; l=cx-tw//2; r=cx+tw//2
    for y in range(t0,min(h,t0+th)):
        for x in range(l,r+1): g[y][x]=sh if x==l else (('a' if (y-t0)%3==0 else sk) if armored else sk)
    for y in range(t0,min(h,t0+th+3)):
        sw=walk if y>t0+th//2 else 0
        for x in (l-2-sw,l-1-sw,r+1+sw,r+2+sw):
            if 0<=x<w: g[y][x]=sk
    for y in range(t0+th,h):
        o=walk if y>t0+th+(h-t0-th)//2 else 0
        for x in range(l+1,cx):
            xx=x+o
            if 0<=xx<w: g[y][xx]=sh if x==l+1 else sk
        for x in range(cx+1,r):
            xx=x-o
            if 0<=xx<w: g[y][xx]=sk
    out=S([''.join(r) for r in g]); _TCACHE[key]=out; return out

register_bg(THEME, lambda v: (v,v-4,v-10), clip_ground=True)   # titans sink INTO the ground

@fx('wire')
def _fx_wire(d,im,e,f):
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(170,170,180))

@fx('blades')
def _fx_blades(d,im,e,f):
    _,x,y,fl=e; s_=-1 if fl else 1
    d.line([x+6*s_,y-5,x+14*s_,y-8],fill=(220,224,238)); d.line([x+5*s_,y-3,x+13*s_,y-3],fill=(200,206,222))

@fx('spear')
def _fx_spear(d,im,e,f):
    _,x0,y0,x1,y1=e; d.line([x0,y0,x1,y1],fill=(120,120,130)); d.point((int(x1),int(y1)),fill=(230,50,40))

@fx('wallbg')
def _fx_wallbg(d,im,e,f):
    for y in range(12,GROUND+1):
        for x in range(0,8):
            c=(70,68,64) if (y%4==0 or (x+(y//4)*3)%6==0) else (104,100,94)
            d.point((x,y),fill=c)
    for x in range(0,8,3): d.rectangle([x,9,x+1,11],fill=(104,100,94))


TITANS=[dict(h=26,hair='q',tx=118,kill=34),dict(h=34,hair='k',tx=146,kill=66),dict(h=30,hair='Y',tx=102,kill=98),
        dict(h=38,hair='R',tx=156,kill=130),dict(h=24,hair='k',tx=128,kill=160)]

def nape(T,armored=False):
    h=T['h']; w=max(11,int(h*0.5))|1; hh=max(7,int(h*0.3))
    return T['x']+w//2-1, GROUND-h+hh+1

def clip_survey(f):
    s=scene(f,'snk'); N=264
    s['under'].append(('wallbg',))
    cl=actor(SCOUT[guard_pose(f)],30); pos=(30.0,float(GROUND)); flip=False; blades=True; pose=None
    titans=[]
    for i,T in enumerate(TITANS):
        enter=T['kill']-34
        if not (enter<=f<T['kill']+24): continue
        t=min(1,(f-enter)/26); x=lerp(205,T['tx'],t); walking=t<1
        y=GROUND-(1 if walking and (f//4)%2 else 0)
        a=actor(titan(T['h'],T['hair'],walk=((f//4)%2*2-1) if walking else 0),x,y=y)
        T=dict(T,x=x)
        if f>=T['kill']+2:
            k=(f-T['kill']-2)/20; a['y']=GROUND+int(T['h']*0.45*k); a['alpha']=max(0,1-k)
            rr=random.Random(f//2+i)
            for j in range(int(8*(1-k)+3)): s['fx'].append(('smoke',x+rr.randint(-8,8),GROUND-rr.randint(4,T['h']),rr.randint(2,4),(236,236,240) if j%2 else (190,190,200)))
        titans.append(a); TITANS[i]['x']=x
    # Claude's flight path: launch -> zip to nape -> spin slash -> drop
    prev=(30,GROUND)
    for i,T in enumerate(TITANS):
        tk=T['kill']; nx,ny=nape(dict(T,x=T['tx'])); land=(T['tx']-26,GROUND)
        if tk-10<=f<tk-2:
            t=(f-(tk-10))/8; pos=(lerp(prev[0],nx+4,ease(t)),lerp(prev[1],ny,ease(t))-10*math.sin(math.pi*t)); pose='dash'
            s['fx'].append(('wire',pos[0],pos[1]-5,nx,ny))
            s['fx'].append(('mote',pos[0]-4,pos[1]-4,(240,240,250)))
        elif tk-2<=f<tk+4:
            pos=(nx+4,ny); flip=(f%2==0); pose='punch'
            s['fx'].append(('circle',pos[0],pos[1]-6,8,(240,240,255)))
            if f==tk: s['fx'].append(('spark',nx,ny-2,7)); s['shake']=rshake()
        elif tk+4<=f<tk+14:
            t=(f-(tk+4))/10; pos=(lerp(nx+4,land[0],t),lerp(ny,GROUND,t*t)); pose='guard'
        elif i+1<len(TITANS) and tk+14<=f<TITANS[i+1]['kill']-10: pos=land
        prev=land
    last=TITANS[-1]; lx=last['tx']-26
    if 174<=f<200: pos=(lx,GROUND)
    # --- the Armored Titan
    AH=46; arm=None
    if 170<=f<262:
        if f<196: x=lerp(215,140,(f-170)/26); walking=True
        elif f<200: x=140; walking=False
        elif f<210: x=lerp(140,86,ease((f-200)/10)); walking=False
        else: x=86; walking=False
        arm=actor(titan(AH,'Y',walk=((f//5)%2*2-1) if walking else 0,armored=True),x)
        if walking and f%5==0: s['shake']=rshake()
        if 232<=f<250: arm['y']=GROUND+int(12*ease((f-232)/18))
        if f>=250: arm['y']=GROUND+12; arm['alpha']=max(0,1-(f-250)/12)
        if f>=232:
            rr=random.Random(f//2)
            for j in range(10): s['fx'].append(('smoke',x+rr.randint(-12,12),GROUND-rr.randint(6,40),rr.randint(2,5),(236,236,240) if j%2 else (190,190,200)))
        titans.append(arm)
    AT=dict(h=AH,x=86); anx,any_=nape(AT)
    if 200<=f<210:
        t=(f-200)/10; pos=(lerp(lx,48,ease(t)),lerp(GROUND,GROUND-26,ease(t))); pose='dash'; flip=False
        s['fx'].append(('wire',pos[0],pos[1]-5,6,12))
    if 210<=f<216:
        t=(f-210)/6; pos=(lerp(48,anx+4,t),lerp(GROUND-26,any_,t)); pose='dash'
        s['fx'].append(('wire',pos[0],pos[1]-5,anx,any_))
    if 216<=f<222:
        pos=(anx+4,any_); pose='punch'; flip=True; blades=f<217
        if f==216: s['fx'].append(('spark',anx,any_-2,6)); s['shake']=rshake(2)
        for j in range(4): s['fx'].append(('shard',anx+random.randint(-6,6)+(f-216)*2,any_-4+random.randint(-4,4)+(f-216),(220,224,238)))
    if 222<=f<230:
        t=(f-222)/8; pos=(lerp(anx+4,58,t),lerp(any_,GROUND,t*t)); pose='hurt'; flip=False; blades=False
    if 228<=f<236:
        pos=(58,GROUND); pose='charge'; blades=False
        if f<232:
            t=(f-228)/4
            for dy in (0,3): s['fx'].append(('spear',58+8,GROUND-6+dy,lerp(66,anx,t),lerp(GROUND-6+dy,any_+dy,t)))
        else:
            for dy in (0,3): s['fx'].append(('spear',anx-6,any_+dy+2,anx,any_+dy))
    if f==232: s['flash']=0.9; s['fc']=(anx,any_); s['flashc']=(255,190,120); s['shake']=rshake(2)
    if 232<=f<242: s['fx'].append(('boom',anx,any_,int(4+(f-232)*3)))
    if 236<=f<256: pos=(ez(58,30,(f-236)/20),GROUND); blades=False
    if 252<=f<258: s['fx'].append(('twinkle',36,GROUND-7,1+(f%2)))
    if f>=256: blades=True
    cl.update(x=pos[0],y=pos[1],flip=flip)
    if pose: cl['spr']=SCOUT[pose]
    if blades: s['fx'].append(('blades',cl['x'],cl['y'],flip))
    s['actors']=titans+[cl]
    return s

CLIPS = [clip('survey', 264, clip_survey)]
