"""Dragon Ball sub-theme "dbz-buu": Claude vs Kid Buu. Codex flies in, they do the fusion dance
(FU-SION-HA!) and Clodex takes Buu apart. Buu regenerates, the fusion wears off, back to the standoff."""
from engine import *

THEME = 'dbz-buu'

BUU=poses(S([
"........nn......","......nnn.......","....nnnnnn......","...nnnnnnnn.....","...nnKnnnKn.....",
"...nnKKnKKn.....","...nnnnnnnn.....","....nnKKKn......",".....nnnn.......","...nnnnnnnn.....",
"..nnnnnnnnnn....","..nn.nnnnn.nn...","..nn.nnnnn.nn...","..nn.kkykk.nn...",".....WWWWWW.....",
"....WWWWWWWW....","....WWW..WWW....","....WWW..WWW....",".....WW..WW.....","....kkk..kkk....",]),10,'nn',4)

# Codex, alive this time: blue eyes instead of the Edo Tensei glow. Body variants for the dance.
CODEX_BODY={
 'idle':LOGO_BODY,
 'up':["d...ddd...d","dd.ddddd.dd",".ddddddddd.","....ddd....","...dd.dd...","...dd.dd...","..ddd.ddd.."],
 'point':["....ddd....","dddddddd...","....ddd.dd.","....ddd....","...dd.dd...","...dd.dd...","..ddd.ddd.."],
}
CODEX={k:S([r.replace('y','E') for r in ICONS['CODEX']]+b) for k,b in CODEX_BODY.items()}

# Clodex: Codex's white spiky hair + a Metamoran vest over Claude.
CLODEX=variant(lambda s: recolor_rows(overlay(s,["..H..H..H...",".HHH.HHHHH..","HHHHHHHHHHH.",".HHHHHHHHHH."],-2,0),
    lambda x,y,t,l,r,c: 'k' if (t+5<=y<=t+7 and c=='O' and (x<=l+1 or x>=r-1)) else
                        ('Y' if (y==t+4 and c=='O' and x in (l,r)) else None)))

GOLD={'O':(255,214,90),'o':(210,156,40)}
BUU_KI=((255,170,220),(230,60,160))
CL_KI=((255,236,200),(255,160,90))
CODEX_AURA=((120,170,255),1)

register_bg(THEME, lambda v: (v+8,v//3,v//2+4))

def blobs(s,cx,feet,t,seed,back=False):
    """Buu's bits: pink blobs fly apart; with back=True they pull back into one body (t=16 → whole)."""
    rr=random.Random(seed); k=max(0,16-t) if back else t
    for j in range(16):
        vx=rr.uniform(-2.4,2.4); vy=rr.uniform(-2.2,0.3); r=rr.randint(1,3)
        s['fx'].append(('smoke',cx+vx*k,min(feet-9+vy*k+0.09*k*k,GROUND-1),r,(240,120,170) if j%3 else (196,64,136)))

def burst(s,x,y,t,c=(255,255,255)):
    for j in range(3): s['fx'].append(('circle',x,y,4+t*3+j*4,c))

def clip_fusion(f):
    s=scene(f,THEME)
    cl=actor(CL[guard_pose(f)],30); bu=actor(BUU['idle'],152,y=GROUND-((f//6)%2),flip=True)
    cx=None; cd=None
    # 1) Buu rushes in and smacks Claude away
    if 12<=f<18: bu['spr']=BUU['attack']; callout(s,"HEE HEE!",c=(255,150,210))
    if 18<=f<28:
        bu.update(spr=BUU['attack'],x=lerp(152,48,(f-18)/10),y=GROUND)
        s['fx'].append(('mote',bu['x']+10,GROUND-10+random.randint(-3,3),(255,170,220)))
    if f==28: s['fx'].append(('spark',40,GROUND-7,7)); s['shake']=rshake(2)
    if 28<=f<40: cl.update(spr=CL['hurt'],x=ez(30,12,(f-28)/8)); bu.update(spr=BUU['idle'],x=48)
    if 40<=f<56: bu.update(x=ez(48,152,(f-40)/16),y=GROUND-(3 if (f//3)%2 else 0))   # bounces back, cackling
    if 40<=f<60: cl['x']=ez(12,30,(f-40)/12)
    # 2) Codex flies in
    if 42<=f<60:
        t=(f-42)/12; cx=actor(CODEX['idle'],lerp(-12,74,ease(t)),y=lerp(GROUND-24,GROUND,ease(t)),aura=CODEX_AURA)
        if f<54:
            for j in range(3): s['fx'].append(('mote',cx['x']-8-j*4,cx['y']-8+j,(170,200,255)))
    if 48<=f<62: callout(s,"CODEX!",c=(150,190,255))
    # 3) the fusion dance: FU (step in, arms up) - SION (arms out) - HA! (fingers touch)
    beats=[(60,'armsup','up',36,66,"FU"),(72,'charge','idle',42,58,"FU SION"),(84,'punch','point',44,56,"FU SION HA!")]
    for i,(t0,cp,xp,clx,cxx,txt) in enumerate(beats):
        if t0<=f<t0+12:
            px,pcx=(30,74) if i==0 else beats[i-1][3:5]
            t=min(1,(f-t0)/5)
            cl.update(spr=CL[cp],x=lerp(px,clx,t)); cx=actor(CODEX[xp],lerp(pcx,cxx,t),aura=CODEX_AURA)
            callout(s,txt,c=(255,226,90))
    # 4) flash: Clodex is born
    if 94<=f<108:
        s['flash']=max(0,1-(f-96)/12) if f>=96 else 0.6; s['fc']=(50,GROUND-8)
        burst(s,50,GROUND-8,f-94,(255,240,190))
        if f>=96: cl['vis']=False; cx=None
        else: cl.update(spr=CL['punch'],x=44); cx=actor(CODEX['point'],56,aura=CODEX_AURA)
        if f%2==0: s['shake']=rshake()
    if 96<=f<208: cl['vis']=False; cd=actor(CLODEX[guard_pose(f)],50,aura=((255,240,190),1+(f%2)))
    if 104<=f<120: callout(s,"CLODEX!",c=(255,190,120))
    # 5) barrage: teleport strikes, Buu can't keep up
    if 120<=f<150:
        k=(f-120)//7; ph=(f-120)%7; sx=[136,168,134,166,136][k]
        cd.update(spr=CLODEX['punch' if ph<4 else 'dash'],x=sx,flip=sx>152,vis=ph>0)
        if ph==0:
            s['fx'].append(('mote',sx+random.randint(-6,6),GROUND-random.randint(4,12),(255,240,200)))
        if ph==2: s['fx'].append(('spark',152+(-6 if sx<152 else 6),GROUND-9,6)); s['shake']=rshake()
        bu.update(spr=BUU['hurt'],y=GROUND,x=152+(2 if ph<3 else 0)*(1 if sx<152 else -1))
        s['fx'].append(('dmg',str(9000+k*111),144,GROUND-26-min(ph,4),(255,240,160)))
    if 150<=f<158: cd.update(spr=CLODEX['dash'],x=lerp(146,50,(f-150)/8),flip=False); bu.update(spr=BUU['hurt'],x=ez(152,170,(f-150)/8),y=GROUND)
    if 158<=f<180: bu.update(spr=BUU['hurt'] if f<166 else BUU['idle'],x=170,y=GROUND)
    # 6) 10x Kamehameha, gold
    if 158<=f<200:
        cd.update(spr=CLODEX['charge'],pal=GOLD,aura=((255,244,150),1+(f%2)),x=50)
        if f<176:
            s['fx'].append(('orbc',64,GROUND-6,1+(f-158)//4,CL_KI))
            for i in range(6):
                a=i*1.05+f*0.3; L=(1-((f*0.08+i*0.17)%1))*22
                s['fx'].append(('mote',64+math.cos(a)*L,GROUND-6+math.sin(a)*L*0.6,(255,230,170)))
            if f>=166: s['shake']=rshake()
        callout(s,"10X KAMEHAMEHA!",c=(255,214,90))
    if 176<=f<200:
        x1=lerp(64,200,min(1,(f-176)/5)); s['fx'].append(('beam',64,x1,GROUND-6,CL_KI))
        if f<180: s['fx'].append(('orbc',x1,GROUND-6,4,CL_KI))
        s['shake']=rshake(2 if f<190 else 1)
    if f==180: s['flash']=1.0; s['fc']=(170,GROUND-8)
    if 180<=f<200: bu['vis']=False; blobs(s,170,GROUND,f-180,3)
    # 7) Buu pulls himself back together; the fusion wears off
    if 200<=f<216: bu['vis']=False; blobs(s,170,GROUND,f-200,3,back=True)
    if 216<=f<228: bu.update(spr=BUU['hurt'],x=170,y=GROUND)
    if 228<=f<248: bu.update(x=ez(170,152,(f-228)/20),y=GROUND-((f//6)%2))
    if 204<=f<214: burst(s,50,GROUND-8,f-204,(200,220,255))
    if f==208: s['flash']=0.6; s['fc']=(50,GROUND-8)
    if 208<=f<224: callout(s,"FUSION OVER!",c=(200,220,255))
    if 208<=f<240:
        cl.update(vis=True,spr=CL['hurt'] if f<216 else CL[guard_pose(f)],x=ez(44,30,(f-216)/20) if f>=216 else 44)
        t=max(0,(f-220)/16)
        cx=actor(CODEX['up' if 216<=f<224 else 'idle'],lerp(58,-14,ease(t)),y=lerp(GROUND,GROUND-26,ease(t)),aura=CODEX_AURA)
    s['actors']=[a for a in (cx,cl,cd,bu) if a]
    return s

CLIPS = [clip('fusion', 264, clip_fusion)]
