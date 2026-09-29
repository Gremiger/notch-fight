"""Naruto: Claude (Naruto) vs Madara — shadow clones, Sharingan close-up, Katon, Rasengan."""
from engine import *

THEME = 'nrt'

NARU=variant(lambda s: recolor_rows(overlay(s,["Y.Y.Y.Y.Y.Y.","YYYYYYYYYYYY",".YYYYYYYYYY."],-2,0),
    lambda x,y,t,l,r,c: ('D' if l+2<=x<=l+5 else 'N') if (y==t and l<=x<=r and c!='.') else None))
MADARA=poses(S([
"....kkkkkk........","..kkkkkkkkkk......",".kkkkkkkkkkkk.....","kkkkkkksssssk.....","kkkkkksrssrsk.....",
"kkkkkksssssk......",".kkkkkksssk.......","kkkkkRRRRRRR......","kkkkRRRRRRRRR.....","kkkRRZRRRRZRRR....",
"kkkRR.NNNN.RR.....",".kkRR.NNNN.RR.....",".kk.s.RRRR.s......","..k...RRRR........","......RZZR........",
".....RRRRRR.......",".....RR..RR.......",".....RR..RR.......",".....NN..NN.......",".....NN..NN.......",
".....NN..NN.......","....kkk..kkk......",]),10,'Rs',4)

register_bg(THEME, lambda v: (v,v//2+6,v//4))

@fx('gunbai')
def _fx_gunbai(d,im,e,f):
    _,x,y=e; d.line([x,y+4,x+6,y-4],fill=(120,80,50)); d.ellipse([x-6,y-10,x+4,y],fill=(230,220,200),outline=(140,30,30))
    d.line([x-5,y-5,x+3,y-5],fill=(140,30,30))


def poof(s,x,t):
    """Shadow-clone smoke puff, t = frames since the poof started (0..6)."""
    if 0<=t<7:
        rr=random.Random(int(x)*7+t)
        for j in range(6): s['fx'].append(('smoke',x+rr.randint(-6,6),GROUND-5-rr.randint(0,9),2+t//2+rr.randint(0,1),(236,236,240) if j%2 else (200,200,210)))

def closeup_frame(t,f):
    """Extreme close-up of Madara's eyes: tomoe spin up and lock into the Eternal Mangekyo."""
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    d.rectangle([0,10,W,54],fill=(232,208,182))
    for y in range(44,55): d.line([0,y,W,y],fill=(214,188,160) if y%2 else (224,198,172))
    rr=random.Random(5)
    for i in range(40):   # hair strands over the forehead and the sides
        x=rr.randint(-10,W+10); L=rr.randint(6,20); d.polygon([(x,8),(x+rr.randint(3,8),8),(x+rr.randint(-4,4),8+L)],fill=(16,14,18))
    for x in list(range(0,22))+list(range(W-22,W)):
        d.line([x,8,x+int(4*math.sin(x*0.7)),58],fill=(16,14,18))
    spin=f*(0.18+0.9*t)
    for cx in (62,123):
        cy=33
        d.ellipse([cx-19,cy-8,cx+19,cy+8],fill=(236,232,226))
        d.arc([cx-20,cy-9,cx+20,cy+9],195,345,fill=(20,16,18),width=3); d.arc([cx-20,cy-9,cx+20,cy+9],20,160,fill=(120,90,80),width=1)
        d.line([cx-18,cy-13,cx+16,cy-10+(4 if cx<W//2 else -4)],fill=(24,18,20),width=2)   # angry brows
        r=8; d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(200,18,32),outline=(90,0,8))
        if t<0.62:
            for k in range(3):
                a=spin+k*2.094; tx,ty=cx+math.cos(a)*5,cy+math.sin(a)*5
                d.ellipse([tx-1.6,ty-1.6,tx+1.6,ty+1.6],fill=(10,6,8))
                d.arc([tx-3,ty-3,tx+3,ty+3],math.degrees(a)+90,math.degrees(a)+170,fill=(10,6,8),width=1)
            d.ellipse([cx-2,cy-2,cx+2,cy+2],fill=(10,6,8))
        else:
            for k in range(3):   # Eternal Mangekyo pinwheel
                a=spin*0.3+k*2.094
                d.polygon([(cx,cy),(cx+math.cos(a)*7.5,cy+math.sin(a)*7.5),(cx+math.cos(a+0.9)*5,cy+math.sin(a+0.9)*5)],fill=(10,6,8))
            d.ellipse([cx-3,cy-3,cx+3,cy+3],outline=(10,6,8)); d.ellipse([cx-1,cy-1,cx+1,cy+1],fill=(10,6,8))
        d.rectangle([cx-4,cy-5,cx-3,cy-4],fill=(255,255,255))
    sc=1.0+0.18*ease(t)   # slow push-in
    cw,ch=int(W/sc),int(H/sc); x0,y0=(W-cw)//2,(H-ch)//2
    im=im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.NEAREST); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,5],fill=(0,0,0)); d.rectangle([0,58,W,H],fill=(0,0,0))   # letterbox
    if t<0.1: zoom_lines(d)
    if t>0.9: im=fade_to(im,(200,0,20),0.5*(t-0.9)/0.1)
    return im

def clip_shadowclone(f):
    s=scene(f,'nrt'); N=252
    cl=actor(NARU[guard_pose(f)],30); md=actor(MADARA['idle'],152,flip=True)
    clones=[]
    OFF=[18,42,54,66]
    if 64<=f<100: s['image']=closeup_frame((f-64)/36,f); return s
    if 12<=f<36:
        callout(s,"KAGE BUNSHIN NO JUTSU!")
        cl['spr']=NARU['armsup'] if f<22 else NARU[guard_pose(f)]
        for i,x in enumerate(OFF):
            t0=20+i*2
            poof(s,x,f-t0)
            if f>=t0+2: clones.append(actor(NARU[guard_pose(f+i*3)],x))
    if 36<=f<64:
        for i,x0 in enumerate(OFF):
            t0=36+i*5
            if f<t0: clones.append(actor(NARU[guard_pose(f+i*3)],x0)); continue
            k=f-t0
            if k<6: clones.append(actor(NARU['dash'],lerp(x0,138,k/6)))
            elif k==6:
                md['spr']=MADARA['attack']; s['fx'].append(('spark',142,GROUND-8,6)); s['shake']=rshake()
            poof(s,138,k-6)
            if 6<=k<9: md['spr']=MADARA['attack']; s['fx'].append(('gunbai',140,GROUND-12))
    if 100<=f<132:
        callout(s,"KATON!",c=(255,140,60)); md['spr']=MADARA['attack']
        front=lerp(140,-20,(f-102)/26) if f>=102 else 140
        rr=random.Random(f)
        for j in range(40):
            x=rr.uniform(front,140); hgt=rr.uniform(4,22)*(0.6+0.4*math.sin(x*0.2+f))
            c=[(255,240,160),(255,190,70),(240,110,40),(200,50,30)][rr.randint(0,3)]
            s['fx'].append(('smoke',x,GROUND-hgt*rr.random(),rr.randint(1,3),c))
        if 102<=f<130: t=(f-102)/28; cl['y']=GROUND-int(32*math.sin(math.pi*t)); cl['spr']=NARU['guard2']
        if f>=102: s['shake']=rshake() if f%2 else (0,0)
    if 136<=f<168:
        poof(s,44,f-136)
        if f>=138 and f<162: clones.append(actor(NARU['charge'],46,flip=True))
        poof(s,46,f-162)
        cl['spr']=NARU['charge']
        r=min(5,1+(f-140)//4) if f>=140 else 0
        bx=38 if f<160 else lerp(38,140,(f-160)/8)
        if f>=160: cl.update(x=lerp(30,132,(f-160)/8),spr=NARU['dash']); callout(s,"RASENGAN!",c=(140,210,255))
        if r: s['fx']+= [('orbc',bx,GROUND-7,r,((170,220,255),(70,150,255))),('arc',bx,GROUND-7,r+2,int(f*40)%360,int(f*40)%360+120,(235,245,255),1)]
    if 168<=f<182:
        k=f-168; cl.update(x=132,spr=NARU['punch']); md.update(spr=MADARA['hurt'],x=ez(152,176,k/12))
        for j in range(3): s['fx'].append(('circle',140,GROUND-8,2+k*2+j*3,(150,210,255) if j%2 else (90,160,255)))
        if k==0: s['flash']=0.8; s['fc']=(140,GROUND-8); s['flashc']=(170,220,255); s['shake']=rshake(2)
        if k>=8: s['fx'].append(('dust',md['x']-6,GROUND-random.randint(0,3)))
    if 172<=f<192: t=(f-172)/20; cl.update(x=ez(132,30,t),y=GROUND-int(10*math.sin(math.pi*t)),spr=NARU['guard'])
    if 182<=f<212: md.update(x=ez(176,152,(f-182)/30))
    if 196<=f<206: s['fx'].append(('twinkle',md['x']+1,GROUND-18,1+(f%2)))
    s['actors']=clones+[cl,md]
    return s

CLIPS = [clip('shadowclone', 252, clip_shadowclone)]
