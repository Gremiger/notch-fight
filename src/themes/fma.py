"""Fullmetal Alchemist: Claude (Colonel Mustang) vs Envy. Envy disguises himself as Claude;
close-up of the glove's transmutation circle and the snap — then snap after snap until Envy
is burned down to his tiny true form. The Philosopher's Stone rebuilds him for the loop."""
from engine import *

THEME = 'fma'

MUSTANG=variant(lambda s: recolor_rows(overlay(s,["..NdNNNdN...",".NNNNNNNNNN.","NNdNNNNdNNNN"],-2,0),
    lambda x,y,t,l,r,c: ('L' if (t+5<=y<=t+8 and l<=x<=r and c in 'Oo') else
                         ('H' if (c=='o' and (x>r+3 or x<l-1) and t+4<=y<=t+7) else None))))

ENVY=poses(S([
"..g.g.g.g.......",".gSgSgSgSg......","gSSSSSSSSSg.....","gSSDDDDDSSg.....","gSsssssssSg.....",
"gSsVssVsSg......","gS.sssss.Sg.....","g..ssnss..g.....","...ssss.........","..kkkkkkk.......",
"..kkkkkkk.......",".ss.sssss.ss....",".ss.sssss.ss....",".ss.sssss.ss....","....kkkkk.......",
"....kkkkkk......","....ss..ss......","....ss..ss......","....ss..ss......","....kk..kk......",
"...kkk..kkk.....",]),11,'ss',4)
FAKE=variant(lambda s: S([r.replace('K','V') for r in s]))   # Envy as Claude: purple eyes
TINY=S([".gg.....","gVgg..g.","gggggggg",".g.g.gg."])
CHAR=[None,{'s':(170,110,84),'g':(40,70,34),'S':(20,26,20)},{'s':(110,66,50),'g':(34,44,28),'S':(16,16,14),'k':(20,14,12)}]

register_bg(THEME, lambda v: (v,v//2+8,v//3))

@fx('snapspark')
def _fx_snapspark(d,im,e,f):
    """The spark racing through the air from the glove to the target (drawn up to progress p)."""
    _,x0,y0,x1,y1,p=e; rr=random.Random(f)
    for k in range(int(12*p)):
        t=k/12; x=lerp(x0,x1,t)+rr.randint(-1,1); y=lerp(y0,y1,t)+rr.randint(-2,2)
        d.point((x,y),fill=(255,230,120) if k%2 else (255,140,40))

@fx('redbolt')
def _fx_redbolt(d,im,e,f):
    """Red alchemical lightning (Philosopher's Stone) around a point."""
    _,x,y,r=e; rr=random.Random(f*7)
    for _ in range(3):
        a=rr.random()*6.28; pts=[(x+math.cos(a)*r*0.3,y+math.sin(a)*r*0.3)]
        for j in range(3): a+=rr.uniform(-0.8,0.8); pts.append((pts[-1][0]+math.cos(a)*r/3,pts[-1][1]+math.sin(a)*r/4))
        d.line(pts,fill=(255,60,60)); d.point(pts[-1],fill=(255,200,200))

@fx('bluespark')
def _fx_bluespark(d,im,e,f):
    _,x,y=e
    for k in range(3): a=f*1.3+k*2.1; d.line([x,y,x+math.cos(a)*4,y+math.sin(a)*3],fill=(150,200,255))

def closeup_snap(t,f):
    """Primer plano: the glove with its transmutation circle; the snap sparks and the fire takes the frame."""
    im=Image.new('RGB',(W,H),(10,8,16)); d=ImageDraw.Draw(im)
    d.polygon([(118,64),(150,34),(185,40),(185,64)],fill=(44,60,150)); d.line([(118,64),(150,34)],fill=(80,100,200))
    glove,shade=(240,240,244),(190,190,204)
    snapped=t>=0.5
    d.rounded_rectangle([62,24,126,70],radius=10,fill=glove,outline=shade)                 # back of the hand
    for fx_ in (64,112): d.rounded_rectangle([fx_,16,fx_+11,30],radius=5,fill=glove,outline=shade)   # ring + pinky, curled
    d.rounded_rectangle([96,4,106,28],radius=5,fill=glove,outline=shade)                  # index, relaxed
    if not snapped:
        d.rounded_rectangle([80,-2,92,28],radius=5,fill=glove,outline=shade)             # middle finger, pressed on the thumb
        d.rounded_rectangle([88,-4,118,6],radius=5,fill=glove,outline=shade)             # thumb
    else:
        d.rounded_rectangle([80,14,92,30],radius=5,fill=glove,outline=shade)             # middle finger snapped down
        d.rounded_rectangle([96,-4,126,6],radius=5,fill=glove,outline=shade)
    cx,cy=94,47   # transmutation circle
    d.ellipse([cx-15,cy-15,cx+15,cy+15],outline=(210,40,40)); d.ellipse([cx-12,cy-12,cx+12,cy+12],outline=(210,40,40))
    d.polygon([(cx,cy-11),(cx+10,cy+6),(cx-10,cy+6)],outline=(210,40,40))
    d.polygon([(cx,cy-5),(cx+3,cy+2),(cx,cy+1),(cx-3,cy+2)],fill=(210,40,40))           # the salamander flame
    for k in range(6): a=k*1.047; d.point((cx+math.cos(a)*17,cy+math.sin(a)*17),fill=(210,40,40))
    if t<0.5 and (f//2)%2: d.point((cx+rand_off(f),cy-15),fill=(150,200,255))
    if 0.5<=t<0.7:
        s=int(3+(t-0.5)*40); spark(d,88,2,s,(255,230,120))
        text(d,"SNAP!",130,8,(255,230,120))
    if t>=0.66:   # the air ignites
        r=int((t-0.66)/0.34*240); m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([88-r,2-r//2,88+r,2+r],fill=255)
        fire=Image.new('RGB',(W,H),(255,150,40)); fd=ImageDraw.Draw(fire); rr=random.Random(f)
        for _ in range(40): x,y=rr.randint(0,W),rr.randint(0,H); fd.ellipse([x-4,y-3,x+4,y+3],fill=(255,230,140) if rr.random()<0.4 else (230,70,20))
        im.paste(fire,(0,0),m)
    if t<0.06:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    return im
def rand_off(f): return (f*5)%11-5

HAND=(46,GROUND-6)   # where the snapping glove is when Claude points
def snap(s,f,t0,tx,big=6):
    """Claude snaps at frame t0: spark to (tx) in 3 frames, then a burst of flame there."""
    if t0<=f<t0+3: s['fx'].append(('snapspark',*HAND,tx,GROUND-8,(f-t0+1)/3)); s['fx'].append(('bluespark',*HAND))
    if t0+3<=f<t0+14:
        k=f-t0-3; s['fx'].append(('fire',tx,GROUND,big*(1-k/14)+2))
        if k==0: s['flash']=0.9; s['fc']=(tx,GROUND-10); s['flashc']=(255,180,90); s['shake']=rshake(2)
    if t0<=f<t0+10: callout(s,"SNAP!",c=(255,200,110))

def clip_flame(f):
    s=scene(f,THEME)
    cl=actor(MUSTANG[guard_pose(f)],30); en=actor(ENVY['idle'],150,flip=True)
    # 1) Envy shapeshifts into Claude and walks up with a grin
    if 12<=f<24: s['fx'].append(('redbolt',150,GROUND-10,16))
    if 18<=f<22: s['fx'].append(('smoke',150,GROUND-8,6,(200,200,210)))
    if 20<=f<60:
        en.update(spr=FAKE[guard_pose(f)],flip=True)
        if f<44: en['x']=lerp(150,70,(f-20)/24)
    if 30<=f<46: callout(s,"WHICH ONE IS REAL?",c=(200,150,255))
    if 44<=f<52: en.update(spr=FAKE['punch'],x=62); cl.update(spr=MUSTANG['hurt'],x=ez(30,22,(f-44)/6))
    if f==46: s['fx'].append(('spark',44,GROUND-7,5)); s['shake']=rshake()
    if 52<=f<60: en.update(spr=FAKE['dash'],x=ez(62,110,(f-52)/8)); cl['x']=ez(22,30,(f-52)/8)
    if 56<=f<64: cl['spr']=MUSTANG['punch']; s['fx'].append(('bluespark',*HAND))
    # 2) close-up: the snap
    if 64<=f<104: s['image']=closeup_snap((f-64)/40,f); return s
    # 3) the flame burns the disguise off, then snap after snap
    if 104<=f<196: cl['spr']=MUSTANG['punch']
    snap(s,f,104,110,8)
    if 104<=f<116: en.update(spr=FAKE['hurt'],x=110)
    if 116<=f<126: en.update(spr=ENVY['hurt'],x=110,pal=CHAR[0]); s['fx'].append(('redbolt',110,GROUND-10,12))
    if 126<=f<136: en.update(spr=ENVY['attack'],x=lerp(110,74,(f-126)/10))
    snap(s,f,133,78,7)
    if 136<=f<150: en.update(spr=ENVY['hurt'],x=ez(76,118,(f-136)/8),pal=CHAR[1])
    snap(s,f,148,118,7)
    if 150<=f<162: en.update(spr=ENVY['hurt'],x=ez(118,128,(f-150)/8),pal=CHAR[2])
    snap(s,f,160,128,8)
    snap(s,f,170,130,9)
    if 162<=f<180: en.update(spr=ENVY['hurt'],x=128+(1 if f%2 else 0),pal=CHAR[2])
    if 170<=f<192: cl['aura']=((255,110,40),1+(f%2))
    if 176<=f<192: callout(s,"NOT DONE YET.",c=(255,140,80))
    # 4) what's left of Envy: the tiny true form, and it scurries away
    if 180<=f<212:
        x=128 if f<194 else lerp(128,200,(f-194)/18)
        en.update(spr=TINY,x=x,y=GROUND-(1 if (f//2)%2 else 0),pal=None)
        if f<186: s['fx'].append(('smoke',128,GROUND-6-(f-180),3+(f-180)//2,(90,90,96)))
    if 196<=f<212: s['fx'].append(('dmg',"EEK!",min(180,en['x']-6),GROUND-12,(120,220,120)))
    if 212<=f<222: en['vis']=False
    # 5) the Philosopher's Stone rebuilds him
    if 218<=f<244:
        t=(f-218)/26
        if 222<=f<244: en.update(vis=True,spr=ENVY['idle'] if t>0.35 else TINY,alpha=min(1,0.3+t) if t>0.35 else 1,x=150 if t>0.35 else lerp(186,150,t/0.35))
        s['fx'].append(('redbolt',150,GROUND-10,10+10*(1-t)))
    s['actors']=[cl,en]
    return s

CLIPS = [clip('flame', 264, clip_flame)]
