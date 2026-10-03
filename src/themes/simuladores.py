"""Los Simuladores: no fight, an operation. Claude is the fifth simulador (dark suit, white shirt and
tie, dark glasses) on a Buenos Aires street at night, the team's grey van parked by the lamp post.
The client wrings his hands: ME ESTAFARON. ME QUEDE SIN NADA. Card: UN NUEVO CASO. The plan on the
whiteboard, written name by name (SANTOS, MEDINA, RAVENNA, LAMPONNE, CLAUDE), every arrow into the
red circle round CODEX. Codex, the crook, struts in with his briefcase of money; Ravenna appears in a
puff of smoke and is an inspector in the next one, Lamponne walks up with his toolcase. A three-panel
montage: CONFIE EN MI, FIRME ACA, ERA TODO SIMULADO. The handshake in close-up (GRACIAS, MUCHACHOS),
the five walk in slow motion, and the client fills in the satisfaction questionnaire: every box
ticked."""
import zlib
from engine import *

THEME = 'simuladores'
N_ = 288
CX, VX = 30, 150                                                   # the neutral pose: Claude, the client

# ---- Claude, the fifth simulador: dark suit, white shirt and tie, dark glasses ------------------
def _suit(spr):
    t,l,r=body_box(spr); g=grid(spr); h=len(g); w=len(g[0])
    bot=max(y for y in range(h) if 'O' in spr[y]); m=(l+r)//2
    kbot=max(y for y in range(h) if 'K' in spr[y])
    for y in range(h):
        for x in range(w):
            c=g[y][x]; inside=l<=x<=r
            if c=='O' and inside and y>=kbot+2:
                g[y][x]='W' if x==m and y<bot else ('t' if x==m+1 and y<bot else 'N')   # shirt, tie, jacket
            elif c=='O' and not inside: g[y][x]='O'                                     # a fist stays a hand
            elif c=='o' and y>bot: g[y][x]='k'                                          # shoes
            elif c=='o': g[y][x]='N'                                                    # sleeves
    eyes=[(x,y) for y in range(1,h-1) for x in range(w) if g[y][x]=='K' and g[y-1][x]!='K']
    if len(eyes)>=2:                                                                    # the dark glasses
        (x0,y0),(x1,_)=eyes[0],eyes[-1]
        for x in range(x0-1,x1+1):
            if g[y0][x] in 'OK': g[y0][x]='k'
        for x,y in eyes:
            g[y][x-1]='k'
            if y+1<h and g[y+1][x]=='K': g[y+1][x]='k'
        g[y0][x1]='g'                                                                   # a glint
    return ungrid(g)
CLAUDE=variant(_suit)
CLPAL={'N':(36,38,52),'W':(236,236,240),'t':(150,30,40),'k':(14,14,18),'g':(170,190,220)}

# ---- the people: one template, hair and clothes per character ---------------------------------
_BODY=[
"....ss....",
"..JJWtWJJ.",
".JJJWtWJJJ",
".JJJJtJJJJ",
".JJ.JJJ.JJ",
".JJ.JJJ.JJ",
".ss.JJJ.ss",
"....JJJJ..",]
_LEGS={'idle':["....PP.PP.","....PP.PP.","....PP.PP.","....PP.PP.","...kkk.kkk"],
       'walk':["....PP.PP.","...PP...PP","...PP...PP","..PP....PP","..kk....kkk"]}
_FACE=[".hsssKssK.","..ssssssss","..ssMMMss.","...ssssss."]
def person(hair,face=_FACE,body=_BODY):
    """Poses of a person facing right: hair rows on top of the face, the body and the legs."""
    out={k:S(hair+face+body+legs) for k,legs in _LEGS.items()}
    out['arm']=attack(out['idle'],len(hair)+len(face)+2,3,'J')      # an arm out, talking
    out['arm']=paint(out['arm'],[(13,len(hair)+len(face)+2,'s'),(13,len(hair)+len(face)+3,'s')],right=1)
    out['hurt']=hurt(out['idle'])
    return out
_HAIR={
 'santos':  ["..hhhhhh..",".hhhhhhhh.",".hhssssss."],
 'medina':  [".hhhhhhh..","hhhhhhhhh.","hhhssssss."],
 'ravenna': ["...ssss...","..ssssss..",".hsssssss."],
 'lamponne':[".h.hh.hh..","hhhhhhhhhh","hhhhhhhhh.","hhhssssss."],
 'client':  ["..hhhhh...",".hhhhhhhh.",".hhssssss."],
}
SKIN=(234,190,150)
_JACKET=["....ss....","..JJJJJJJ.",".JJJJWJJJJ",".JJJJJJJJJ",".JJ.JJJ.JJ",".JJ.JJJ.JJ",".ss.JJJ.ss","....JJJJ.."]   # no tie
_CLIENTB=["....ss....","..JJWWWJJ.",".JJJWWWJJJ",".JJJJJJJJJ",".JJ.JJJ.JJ",".JJ.JJJ.JJ",".ss.JJJ.ss","....JJJJ.."]
SANTOS=person(_HAIR['santos'])
MEDINA=person(_HAIR['medina'])
RAVENNA=person(_HAIR['ravenna'])
LAMPONNE=person(_HAIR['lamponne'],body=_JACKET)
CLIENT=person(_HAIR['client'],body=_CLIENTB)
_WRING=S(_HAIR['client']+_FACE+["....ss....","..JJWWWJJ.",".JJJWWWJJJ",".JJssssJJJ",".JJ.ss.JJ.",".JJ.JJJ.JJ","....JJJ...","....JJJJ.."]+_LEGS['idle'])
CLIENT['wring']=_WRING                                              # hands clasped at the chest
def _pal(**kw):
    p={'s':SKIN,'K':(24,18,16),'W':(236,236,240),'k':(20,18,22),'M':SKIN}; p.update(kw); return p
SANTOSPAL=_pal(h=(196,196,204),J=(70,72,84),t=(130,30,36),P=(56,58,70))
MEDINAPAL=_pal(h=(30,26,28),J=(34,34,42),t=(40,70,150),P=(30,30,38))
RAVENNAPAL=_pal(h=(176,172,168),M=(150,146,142),J=(110,84,60),t=(60,90,60),P=(84,64,48))
LAMPONNEPAL=_pal(h=(70,46,30),J=(58,40,30),W=(40,60,90),P=(50,70,120))
CLIENTPAL=_pal(h=(110,76,46),J=(200,180,130),W=(236,236,240),P=(84,84,96))

# Ravenna's disguise: a fedora and a beige trench coat, the inspector's badge
_INSP=paint(RAVENNA['idle'],[(1,-2,'.FFFFFF.'),(0,-1,'FFFFFFFFFF'),(7,7,'Y')],grow=True)
INSPECTOR={'idle':_INSP,'arm':paint(RAVENNA['arm'],[(1,-2,'.FFFFFF.'),(0,-1,'FFFFFFFFFF'),(7,7,'Y')],grow=True)}
INSPPAL=dict(RAVENNAPAL,J=(196,170,120),F=(80,60,44),Y=(250,210,60))
# Lamponne's toolcase, at his front hand
LAMP_CASE={k:paint(v,[(8,len(v)-6,'BBBB'),(8,len(v)-5,'BBBB'),(9,len(v)-7,'b.b')],right=2) for k,v in LAMPONNE.items() if k in ('idle','walk')}
LAMPCPAL=dict(LAMPONNEPAL,B=(170,40,30),b=(60,60,60))

# Codex, the crook: the Codex logo for a head, a flashy suit, a gold chain, the briefcase of money
_KHEAD=ICONS['CODEX']
_KBODY=["....kk.....","..JJJWJJJ..",".JJJJYJJJJ.",".JJJYJYJJJ.",".JJ.JJJ.JJ.",".JJ.JJJ.JJ.",".ss.JJJ.ss.","....JJJJ..."]
_KLEGS={'idle':["....PP.PP..","....PP.PP..","....PP.PP..","...kkk.kkk."],
        'walk':["....PP.PP..","...PP...PP.","..PP....PP.","..kk....kkk"]}
CODEX={k:paint(S(_KHEAD+_KBODY+legs),[(8,len(_KHEAD)+5,'.CCCC'),(8,len(_KHEAD)+6,'.CYCC'),(8,len(_KHEAD)+7,'.CCCC')],right=2)
       for k,legs in _KLEGS.items()}
CODEX['scared']=S([r.replace('y','W') for r in _KHEAD]+_KBODY+_KLEGS['idle'])
CODEXPAL={'k':(22,22,26),'H':(236,236,244),'y':(250,220,70),'J':(120,40,140),'W':(236,236,240),
          'Y':(250,210,60),'s':SKIN,'P':(40,30,50),'C':(110,74,40)}

# ---- background: a Buenos Aires street at night --------------------------------------------------
def _street(d):
    for y in range(GROUND):
        k=y/GROUND; d.line([0,y,W,y],fill=(int(10+8*k),int(12+8*k),int(26+10*k)))
    rr=random.Random(zlib.crc32(b'buenos-aires'))
    for x0,x1,top in ((0,40,10),(42,92,4),(94,130,14),(132,185,6)):          # old facades, balconies
        d.rectangle([x0,top,x1,GROUND],fill=(34,32,44))
        d.line([x0,top,x1,top],fill=(60,56,70))
        for y in range(top+5,GROUND-12,11):
            for x in range(x0+4,x1-5,9):
                lit=rr.random()<0.3
                d.rectangle([x,y,x+4,y+6],fill=(150,116,70) if lit else (20,22,34))
                d.line([x-1,y+7,x+5,y+7],fill=(70,66,80))                       # the balcony rail
    d.rectangle([60,GROUND-16,74,GROUND-1],fill=(52,40,30))                       # a door
    d.line([118,GROUND,118,GROUND-34],fill=(60,64,70))                            # the lamp post
    d.line([118,GROUND-34,123,GROUND-34],fill=(60,64,70)); d.ellipse([121,GROUND-35,125,GROUND-32],fill=(255,230,160))
    d.polygon([(116,GROUND),(130,GROUND),(124,GROUND-31),(122,GROUND-31)],fill=(40,40,52))
    d.rectangle([82,GROUND-14,112,GROUND-3],fill=(150,154,160))                   # the van
    d.rectangle([104,GROUND-12,110,GROUND-8],fill=(60,80,100))
    d.line([82,GROUND-9,112,GROUND-9],fill=(120,124,130))
    for x in (88,106): d.ellipse([x-3,GROUND-5,x+3,GROUND+1],fill=(20,20,24))
    d.rectangle([0,GROUND-1,W,GROUND],fill=(44,44,54))
register_bg(THEME, lambda v: (v//2+10,v//2+10,v//2+16), decor=_street)

# ---- effects -----------------------------------------------------------------------------------
@fx('sim_sweat')
def _fx_sweat(d,im,e,f):
    _,x,y=e; k=(f%8)/8
    d.point((x,int(y+k*5)),fill=(150,200,255)); d.point((x,int(y+k*5)+1),fill=(110,170,240))

@fx('sim_puff')
def _fx_puff(d,im,e,f):
    """The disguise flash: a puff of smoke, t frames old."""
    _,x,y,t=e; rr=random.Random(zlib.crc32(b'puff'))
    for j in range(10):
        a=rr.random()*math.tau; dist=2+t*1.4*rr.random()+t*0.6; r=max(1,4-t//3+rr.randint(0,2))
        c=(230,230,236) if t<3 else (150,150,160)
        d.ellipse([x+math.cos(a)*dist-r,y+math.sin(a)*dist*0.8-r,x+math.cos(a)*dist+r,y+math.sin(a)*dist*0.8+r],fill=c)

@fx('sim_card')
def _fx_card(d,im,e,f):
    """A title card over the dimmed scene, black bars top and bottom."""
    _,txt,a=e
    im.paste(fade_to(im,(0,0,0),0.7*a))
    dd=ImageDraw.Draw(im); bar=int(12*a)
    dd.rectangle([0,0,W,bar],fill=(0,0,0)); dd.rectangle([0,H-bar,W,H],fill=(0,0,0))
    if a>=1: big_text(im,txt,26,(255,255,255),outline=(150,30,40))

@fx('sim_say')
def _fx_say(d,im,e,f):
    _,txt,y,c,scale,outline=e; big_text(im,txt,y,c,scale=scale,outline=outline)

def shout(s,txt,c,y=2): s['fx'].append(('dmg',txt,W//2-len(txt)*2,y,c))

# ---- the whiteboard -----------------------------------------------------------------------------
PLAN=[('SANTOS','EL PLAN',(40,70,170)),('MEDINA','EL CONTACTO',(40,70,170)),('RAVENNA','INSPECTOR',(40,70,170)),
      ('LAMPONNE','TECNICO',(40,70,170)),('CLAUDE','EL CODIGO',(200,90,50))]
def whiteboard(fr,f):
    """The plan, written name by name (fr frames in), every arrow into the circle round CODEX."""
    im=Image.new('RGB',(W,H),(60,52,44)); d=ImageDraw.Draw(im)
    d.rectangle([3,2,181,61],fill=(236,238,234),outline=(150,150,156))
    d.line([3,61,181,61],fill=(120,120,126)); d.rectangle([60,60,80,62],fill=(190,40,40))  # the tray, a marker
    text(d,"EL PLAN",8,5,(30,30,36),shadow=None); d.line([8,11,35,11],fill=(30,30,36))
    for i,(name,role,c) in enumerate(PLAN):
        t0=4+i*6; y=15+i*9
        if fr<t0: break
        n=min(len(name),(fr-t0)*3)
        text(d,name[:n],8,y,c,shadow=None)
        if fr>=t0+3:
            d.line([42,y+2,52,y+2],fill=(30,30,36)); d.point((51,y+1),fill=(30,30,36)); d.point((51,y+3),fill=(30,30,36))
            text(d,role[:min(len(role),(fr-t0-3)*3)],56,y,(30,30,36),shadow=None)
        if fr>=36:
            k=min(1,(fr-36-i)/6)
            if k>0: d.line([106,y+2,lerp(106,140,k),lerp(y+2,32,k)],fill=(200,40,40))
    if fr>=32:
        text(d,"CODEX",143,30,(30,30,36),shadow=None)
        if fr>=40: d.ellipse([138,24,170,40],outline=(200,40,40),width=2)
    if fr>=44: text(d,"!",174,18,(200,40,40),shadow=None)
    if fr<3: im=fade_to(im,(0,0,0),1-fr/3)
    return im

# ---- the montage: three comic panels ------------------------------------------------------------
def _panel(im,i,bg):
    d=ImageDraw.Draw(im); x0=2+i*61
    d.rectangle([x0,2,x0+58,61],fill=bg,outline=(250,250,250),width=2)
    return x0
def _bubble(d,txt,x,y):
    w=len(txt)*4+3
    d.rectangle([x,y,x+w,y+8],fill=(250,250,250),outline=(20,20,20)); d.polygon([(x+4,y+8),(x+8,y+8),(x+5,y+11)],fill=(250,250,250))
    text(d,txt,x+2,y+2,(20,20,20),shadow=None)
def montage(fr,f):
    im=Image.new('RGB',(W,H),(10,10,14))
    ins=sprite_img(INSPECTOR['arm'],INSPPAL,2); kx=sprite_img(CODEX['idle'],CODEXPAL,2)
    kxf=kx.transpose(Image.FLIP_LEFT_RIGHT)
    if fr>=0:                                                       # 1: the inspector talks him round
        x0=_panel(im,0,(70,90,140)); d=ImageDraw.Draw(im)
        c=im.crop((x0+2,4,x0+57,60)); paste_feet(c,ins,16,56); paste_feet(c,kxf,44,56); im.paste(c,(x0+2,4))
        if fr>=4: _bubble(ImageDraw.Draw(im),"CONFIE EN MI",x0+4,6)
    if fr>=18:                                                      # 2: Codex signs, Lamponne takes the case
        x0=_panel(im,1,(140,90,60)); d=ImageDraw.Draw(im)
        c=im.crop((x0+2,4,x0+57,60)); cd=ImageDraw.Draw(c)
        cd.rectangle([10,36,46,48],fill=(240,236,220),outline=(60,50,40))       # the contract
        for y in (39,42): cd.line([14,y,40,y],fill=(150,150,150))
        sx=14+min(24,(fr-18)*2); cd.line([14,45,sx,45-(sx//3)%2],fill=(30,30,160))  # the signature
        im.paste(c,(x0+2,4)); d=ImageDraw.Draw(im)
        hd=sprite_img(S(_KHEAD),CODEXPAL,2); im.paste(hd,(x0+18,8),hd)
        if fr>=22: _bubble(d,"FIRME ACA",x0+6,50)
    if fr>=36:                                                      # 3: caught: the case is empty
        x0=_panel(im,2,(150,40,40)); d=ImageDraw.Draw(im)
        sc=sprite_img(CODEX['scared'],CODEXPAL,2)
        c=im.crop((x0+2,4,x0+57,60)); paste_feet(c,sc,22,56); im.paste(c,(x0+2,4)); d=ImageDraw.Draw(im)
        if (fr//2)%2: d.ellipse([x0+44,8,x0+50,14],fill=(60,120,255))           # the siren
        else: d.ellipse([x0+44,8,x0+50,14],fill=(255,60,60))
        text(d,"!?",x0+40,20,(255,255,255))
        if fr>=40:
            text(d,"ERA TODO",x0+14,46,(255,255,255)); text(d,"SIMULADO",x0+14,53,(255,230,120))
    return im

# ---- close-up: the handshake ---------------------------------------------------------------------
def handshake(fr,f):
    im=Image.new('RGB',(W,H),(30,26,40)); d=ImageDraw.Draw(im)
    for i in range(12): a=i*0.52; d.line([W//2,H//2+6,W//2+math.cos(a)*140,H//2+6+math.sin(a)*70],fill=(40,34,52))
    k=ease(fr/8); bob=int(2*math.sin(fr*0.9)) if fr>=8 else 0
    lx=int(lerp(-30,70,k)); rx=int(lerp(215,104,k)); y=40+bob
    d.rectangle([lx-80,y-7,lx,y+9],fill=(36,38,52))                  # Claude's dark sleeve
    d.rectangle([lx-4,y-9,lx,y+11],fill=(236,236,240))                # the shirt cuff
    d.rectangle([rx,y-7,rx+80,y+9],fill=(200,180,130))               # the client's cardigan
    d.rounded_rectangle([lx,y-6,lx+22,y+8],radius=4,fill=(217,119,87))          # Claude's hand
    d.rounded_rectangle([rx-22,y-8,rx,y+6],radius=4,fill=SKIN)                  # the client's hand, on top
    for j in range(3): d.line([rx-20+j*5,y-8,rx-20+j*5,y-2],fill=(200,150,110))
    if fr>=10: big_text(im,"GRACIAS, MUCHACHOS",6,(255,255,255),outline=(60,40,80))
    if fr<2: zoom_lines(d)
    return im

# ---- the questionnaire ---------------------------------------------------------------------------
_Q=["ATENCION","EFICACIA","DISCRECION","LOS VOLVERIA A LLAMAR"]
def questionnaire(fr,f):
    im=Image.new('RGB',(W,H),(30,30,38)); d=ImageDraw.Draw(im)
    d.rectangle([22,1,162,63],fill=(244,240,226),outline=(120,110,90))
    text(d,"CUESTIONARIO DE SATISFACCION",W//2-56,4,(30,30,36),shadow=None)
    d.line([34,10,150,10],fill=(150,140,120))
    for i,q in enumerate(_Q):
        y=15+i*11
        d.rectangle([30,y,36,y+6],outline=(40,40,48))
        text(d,q,42,y+1,(40,40,48),shadow=None)
        if fr>=3+i*4:                                               # ticked
            d.line([31,y+3,33,y+5],fill=(30,60,180),width=1); d.line([33,y+5,37,y-1],fill=(30,60,180),width=1)
            d.line([32,y+3,34,y+5],fill=(30,60,180));
    if fr<3: im=fade_to(im,(0,0,0),1-fr/3)
    return im

# ---- the clip ----------------------------------------------------------------------------------
def clip_operativo(f):
    s=scene(f,THEME)
    cl=actor(CLAUDE[guard_pose(f)],CX,pal=CLPAL)
    cli=actor(CLIENT['idle'],VX,flip=True,pal=CLIENTPAL)
    extra=[]
    # 1) the client's problem
    if 10<=f<44:
        cli['spr']=CLIENT['wring'] if (f//4)%2 else CLIENT['arm']
        s['fx'].append(('sim_sweat',VX-5,GROUND-22))
        if f<26: shout(s,"ME ESTAFARON...",(255,220,180))
        else: shout(s,"ME QUEDE SIN NADA!",(255,220,180))
    if 44<=f<60:
        a=min(1,(f-44)/4); s['fx'].append(('sim_card',"UN NUEVO CASO",a))
    # 2) the plan
    if 60<=f<108: s['image']=whiteboard(f-60,f); return s
    # 3) the operation: Codex struts in, Ravenna and Lamponne take their places
    if 108<=f<168:
        cli['vis']=False
        kx=actor(CODEX['walk'] if f<126 and (f//4)%2 else CODEX['idle'],int(ez(200,158,(f-108)/18)),flip=True,pal=CODEXPAL)
        extra.append(kx)
        if 126<=f<142: shout(s,"QUE TAL, AMIGO?",(220,160,255))
        if f>=124:
            if f<136: rv=actor(RAVENNA['idle'],118,pal=RAVENNAPAL)
            else: rv=actor(INSPECTOR['arm'] if 142<=f<160 and (f//4)%2 else INSPECTOR['idle'],118,pal=INSPPAL)
            extra.append(rv)
            if 124<=f<130: s['fx'].append(('sim_puff',118,GROUND-10,f-124))
            if 136<=f<142: s['fx'].append(('sim_puff',118,GROUND-10,f-136))
            if 144<=f<160: shout(s,"INSPECCION FEDERAL!",(250,210,60))
        if f>=140:
            lx=int(ez(-10,80,(f-140)/16))
            extra.append(actor(LAMP_CASE['walk'] if f<156 and (f//4)%2 else LAMP_CASE['idle'],lx,pal=LAMPCPAL))
        if 160<=f<168: s['fx'].append(('dmg',"SERVICE TECNICO",60,GROUND-34,(255,170,120)))
    # 4) the montage
    if 168<=f<214: s['image']=montage(f-168,f); return s
    # 5) the handshake
    if 214<=f<238: s['image']=handshake(f-214,f); return s
    # 6) the five walk in slow motion past the client
    if 238<=f<262:
        t=(f-238)/24; base=lerp(-20,64,t); cl['vis']=False
        team=[(SANTOS,SANTOSPAL),(MEDINA,MEDINAPAL),(RAVENNA,RAVENNAPAL),(LAMPONNE,LAMPONNEPAL)]
        for i,(sp,pal) in enumerate(team):
            extra.append(actor(sp['walk'] if ((f+i*3)//8)%2 else sp['idle'],int(base-i*16),pal=pal))
        extra.append(actor(CLAUDE['guard' if (f//8)%2 else 'guard2'],int(base+18),pal=CLPAL))
        s['fx'].append(('dim',0.25))
    # 7) the questionnaire
    if 262<=f<280: s['image']=questionnaire(f-262,f); return s
    s['actors']=[cli]+extra+[cl]
    return s

CLIPS = [clip('operativo', N_, clip_operativo)]
