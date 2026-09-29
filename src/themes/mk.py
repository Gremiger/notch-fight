"""Mortal Kombat: Claude (Scorpion) vs Sub-Zero, with the arcade HUD. Ice ball and slide, "GET
OVER HERE!" spear and uppercut, a combo — FINISH HIM! — then the Toasty fatality: close-up of the
mask coming off (skull underneath), fire breath, a skeleton, a pile of bones; the stage resets."""
from engine import *

THEME = 'mk'
N_ = 300

def _scorpion(x,y,t,l,r,c):
    if c=='.': return None
    inside=l<=x<=r
    if inside and y in (t,t+1): return 'Y'                  # hood
    if c=='K': return 'W'                                    # glowing white eyes
    if inside and y==t+4: return 'k'                         # mask
    if inside and y==t+7: return 'k'                         # belt
    if inside and t+5<=y<=t+8 and (x<=l+1 or x>=r-1): return 'Y'
    return None
SCORP=variant(lambda s: recolor_rows(s,_scorpion))
def _skull(x,y,t,l,r,c):
    if c=='.' or not (l<=x<=r): return None
    if y in (t,t+1): return 'Y'
    if c=='K': return 'r'                                    # burning sockets
    if t+2<=y<=t+3: return 'W'
    if y==t+4: return 'W' if (x-l)%2 else 'k'                # teeth
    return None
SKULL=variant(lambda s: recolor_rows(s,_skull))

SUBZERO=poses(S([
"....LLLLLL......","...LLLLLLLL.....","...LssssssL.....","...LsWssWsL.....","...LvvvvvvL.....",
"....vvvvvv......","..LLLLLLLLLL....",".LLLkLLLLkLLL...",".ss.LLLLLL.ss...",".ss.LLkkLL.ss...",
".kk.kkkkkk.kk...","....LLLLLL......","....LLLLLL......","....LL..LL......","....LL..LL......",
"....kk..kk......","....kk..kk......","...kkk..kkk.....",]),8,'ss',4)
SKELETON=S(["....WWWW....","...WKWWKW...","...WWWWWW...","....WkWk....","...WWWWWW...","..W.WWWW.W..",
            "..W.W..W.W..","....WWWW....","....W..W....","....W..W....","....W..W....","...WW..WW..."])
BONES=S(["..W.WW.W..",".WWWKWWWW.","WWWWWWWWWW"])
ICE=((200,240,255),(90,170,255))

def _stage(d):
    d.ellipse([86,10,98,22],fill=(46,40,34))
    for x in (14,58,122,166):
        d.rectangle([x,16,x+4,GROUND],fill=(22,16,22)); d.rectangle([x-1,14,x+5,15],fill=(30,22,30))
register_bg(THEME, lambda v: (v,v//3+4,v//3), decor=_stage)

@fx('hud')
def _fx_hud(d,im,e,f):
    _,hl,hr=e
    for x0,hp,name,right in ((4,hl,"CLAUDEPION",False),(101,hr,"SUBZERO",True)):
        d.rectangle([x0,2,x0+79,6],fill=(150,20,20),outline=(230,200,90))
        w=int(78*max(0,hp))
        if w>0:
            if right: d.rectangle([x0+79-w,3,x0+78,5],fill=(40,200,60))
            else: d.rectangle([x0+1,3,x0+w,5],fill=(40,200,60))
        text(d,name,x0+79-len(name)*4 if right else x0,9,(230,200,90))

@fx('kunai')
def _fx_kunai(d,im,e,f):
    _,x0,y0,x1,y1=e
    for k in range(0,int(abs(x1-x0)),3): d.line([x0+k,y0,x0+k+2,y0+(k//3)%2],fill=(170,130,80))
    d.polygon([(x1,y1-2),(x1+5,y1),(x1,y1+2)],fill=(220,224,238))

@fx('iceblock')
def _fx_iceblock(d,im,e,f):
    _,x=e; im.paste(Image.blend(im.crop((x-9,GROUND-15,x+9,GROUND+1)),Image.new('RGB',(18,16),(150,210,255)),0.35),(x-9,GROUND-15))
    d.rectangle([x-9,GROUND-15,x+9,GROUND],outline=(200,240,255)); d.line([x-6,GROUND-12,x-2,GROUND-8],fill=(240,250,255))

def hp(f,marks,full=1.0): return track(f,marks,full)
HP_L=[(54,0.85),(72,0.7)]
HP_R=[(92,0.85),(110,0.65),(136,0.45),(144,0.25),(152,0.05)]

def closeup_mask(t,f):
    """Primer plano: Scorpion pulls the mask off — a skull with burning sockets — and inhales fire."""
    im=Image.new('RGB',(W,H),(10,4,4)); d=ImageDraw.Draw(im)
    bone=ease((t-0.4)/0.2)
    face=tuple(int(lerp(a,b,bone)) for a,b in zip((217,119,87),(236,232,214)))
    d.rectangle([34,0,150,64],fill=face)
    d.polygon([(20,0),(164,0),(164,64),(150,64),(150,12),(34,12),(34,64),(20,64)],fill=(250,210,60))
    d.line([(34,12),(150,12)],fill=(200,160,30))
    for ex in (74,110):
        if bone<1: d.rectangle([ex-7,22,ex+7,32],fill=(255,255,255) if bone<0.5 else (20,0,0))
        else:
            d.ellipse([ex-9,18,ex+9,36],fill=(14,4,4)); rr=random.Random(f+ex)
            for _ in range(5): x=ex+rr.randint(-5,5); d.line([x,34,x,34-rr.randint(4,12)],fill=(255,140,40) if rr.random()<0.6 else (255,230,120))
    if bone>=1:
        d.polygon([(92,40),(88,48),(96,48)],fill=(20,6,6))
        d.rectangle([62,52,122,62],fill=(236,232,214))
        for x in range(62,123,6): d.line([x,52,x,62],fill=(60,40,30))
    my=int(38+40*ease((t-0.12)/0.3))   # the mask slides off
    if my<64: d.rectangle([34,my,150,my+30],fill=(24,20,22)); d.line([34,my,150,my],fill=(60,56,60))
    if t>0.8:   # fire from the jaws
        r=int((t-0.8)/0.2*140); m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([92-r,57-r//2,92+r,57+r//2],fill=255)
        fire=Image.new('RGB',(W,H),(255,150,40)); fd=ImageDraw.Draw(fire); rr=random.Random(f)
        for _ in range(30): x,y=rr.randint(0,W),rr.randint(0,H); fd.ellipse([x-4,y-3,x+4,y+3],fill=(255,230,140) if rr.random()<0.4 else (220,60,20))
        im.paste(fire,(0,0),m)
    if t<0.06:
        zoom_lines(d)
    return im

def clip_fatality(f):
    s=scene(f,THEME)
    cl=actor(SCORP[guard_pose(f)],30); sz=actor(SUBZERO['idle'],150,flip=True)
    s['fx'].append(('hud',hp(f,HP_L),hp(f,HP_R)))
    if 12<=f<24: s['fx'].append(('big',"ROUND 1",22,(230,200,90)))
    if 24<=f<36: s['fx'].append(('big',"FIGHT!",22,(255,80,60)))
    # 1) ice ball, frozen, slide
    if 36<=f<46: sz['spr']=SUBZERO['attack']
    if 44<=f<54: s['fx'].append(('orbc',lerp(138,36,(f-44)/10),GROUND-9,3,ICE))
    if 54<=f<74:
        cl.update(spr=SCORP['hurt'],tint=(170,220,255)); s['fx'].append(('iceblock',30))
        if f==54: s['fx'].append(('spark',34,GROUND-8,5))
    if 60<=f<72: sz.update(spr=SUBZERO['hurt'],x=lerp(150,44,(f-60)/12),y=GROUND+3)   # the slide
    if f==72: s['fx'].append(('spark',36,GROUND-6,7)); s['shake']=rshake(2)
    if 72<=f<80:
        cl.update(spr=SCORP['hurt'],x=ez(30,18,(f-72)/6))
        for j in range(6): s['fx'].append(('shard',30+random.randint(-10,10),GROUND-random.randint(0,15),(200,240,255)))
    if 72<=f<88: sz.update(x=ez(44,140,(f-72)/16) if f>=76 else 44)
    if 80<=f<90: cl['x']=ez(18,30,(f-80)/10)
    # 2) GET OVER HERE!
    if 84<=f<104: callout(s,"GET OVER HERE!",y=13,c=(250,210,60))
    if 86<=f<108: cl['spr']=SCORP['punch']
    if 86<=f<92: s['fx'].append(('kunai',44,GROUND-6,lerp(44,132,(f-86)/6),GROUND-6))
    if f==92: s['fx'].append(('spark',134,GROUND-8,5))
    if 92<=f<104:
        x=lerp(140,56,(f-92)/12); sz.update(spr=SUBZERO['hurt'],x=x); s['fx'].append(('kunai',44,GROUND-6,x-8,GROUND-6))
    if 104<=f<108: sz.update(spr=SUBZERO['hurt'],x=56)
    if 108<=f<112: cl['spr']=SCORP['armsup']
    if f==110: s['fx'].append(('spark',50,GROUND-14,7)); s['shake']=rshake(2)
    if 110<=f<130:
        t=(f-110)/20; sz.update(spr=SUBZERO['hurt'],x=lerp(56,120,t),y=GROUND-int(26*math.sin(math.pi*t)))
    if 130<=f<134: sz.update(spr=SUBZERO['hurt'],x=120)
    # 3) combo
    if 130<=f<156:
        k=(f-130)//8; ph=(f-130)%8
        cl.update(spr=SCORP['dash' if ph<3 else 'punch'],x=lerp(30,104,min(1,ph/3)) if k==0 else 104+k*4)
        sz.update(spr=SUBZERO['hurt'],x=120+k*4+(2 if ph in (4,5) else 0))
        if ph==4: s['fx'].append(('spark',116+k*4,GROUND-8-k*3,5)); s['shake']=rshake()
    # 4) FINISH HIM!
    if 156<=f<262: s['under'].append(('dim',0.55))   # the stage goes dark for the finisher
    if 156<=f<176:
        cl.update(spr=SCORP[guard_pose(f)],x=ez(116,40,(f-156)/12)); sz.update(spr=SUBZERO['hurt'] if (f//6)%2 else SUBZERO['idle'],x=132)
        s['fx'].append(('dizzy',132,GROUND-20)); s['fx'].append(('big',"FINISH HIM!",20,(255,60,50)))
    if 176<=f<216: s['image']=closeup_mask((f-176)/40,f); return s
    # 5) Toasty: fire breath, skeleton, bones
    if 216<=f<262: cl.update(spr=SKULL['charge'] if f<238 else SKULL[guard_pose(f)],x=40)
    if 216<=f<236:
        x1=lerp(50,134,min(1,(f-216)/6)); s['fx'].append(('beam',50,x1,GROUND-7,((255,140,40),(255,220,120))))
        for j in range(4): s['fx'].append(('fire',lerp(56,x1,j/3),GROUND-3,3))
        if f>=220: s['fx'].append(('fire',132,GROUND,8)); s['shake']=rshake()
    if 216<=f<232: sz.update(spr=SUBZERO['hurt'],x=132,tint=(40,20,14) if f>=224 else None)
    if 232<=f<246:
        sz.update(spr=SKELETON,x=132,tint=None)
        if f<238: s['fx'].append(('fire',132,GROUND,4))
    if 246<=f<262: sz.update(spr=BONES,x=132,tint=None)
    if 240<=f<262:
        s['fx'].append(('big',"FATALITY",18,(220,20,20)))
        for k in range(6): x=W//2-30+k*11; s['fx'].append(('tracer',x,x,30+min(8,(f-240)//2)))
        if f>=250: callout(s,"CLAUDEPION WINS",y=36,c=(250,210,60))
    # 6) the stage lights come back and Sub-Zero is back for the loop
    if 262<=f<280:
        s['under'].append(('dim',0.55*(1-(f-262)/18)))
        sz.update(spr=SUBZERO['idle'],x=150,alpha=max(0.1,(f-268)/12) if f>=268 else 0.0,vis=f>=268)
        cl.update(spr=SCORP[guard_pose(f)],x=ez(40,30,(f-262)/12))
    s['actors']=[cl,sz]
    return s

CLIPS = [clip('fatality', N_, clip_fatality)]
