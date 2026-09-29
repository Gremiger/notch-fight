"""Counter-Strike: Claude (Counter-Terrorist) vs a Terrorist on a de_dust2-ish bomb site, with the
1.6 HUD. GO GO GO, the Terrorist plants the bomb, a firefight, a flashbang whites the screen,
Claude draws the AWP — close-up through the scope — HEADSHOT, the defuse, COUNTER-TERRORISTS WIN,
and a new round puts everyone back where they started."""
from engine import *

THEME = 'cs'
N_ = 288

# Theme colours live in each actor's `pal` (no PAL.update: other themes are added in parallel).
CT_PAL={'1':(66,76,92),'2':(74,100,132),'3':(120,200,230)}
T_PAL={'a':(78,74,84),'c':(108,104,116),'i':(118,84,52),'u':(96,92,84)}
AMBER=(236,168,48)
CT_BLUE=(140,190,255)
T_RED=(255,120,90)

def _ct(x,y,t,l,r,c):
    if c=='.': return None
    inside=l<=x<=r
    if inside and y==t: return '1'                             # helmet brim
    if inside and y==t+1: return '3' if x in (l+4,l+5,l+7,l+8) else '1'   # goggles pushed up
    if inside and t+4<=y<=t+7: return '2'                      # blue-grey vest
    return None
CT=variant(lambda s: recolor_rows(overlay(s,["..1111111..",".111111111."],-1,0),_ct))

T_IDLE=S([
"....cccc.......","...aaaaaa......","...aaaaaaa.....","...aaassss.....","...aaasKsK.....","...aaaaaaa.....",
"....aaaaa......","..iiiiiiiii....",".iiiiiiiiiii...",".ii.iiiiii.ii..",".ii.iikiii.ii..",".ss.iiiiii.ss..",
"....kkkkkk.....","....uuuuuu.....","....uuuuuu.....","....uu..uu.....","....uu..uu.....","...kkk..kkk....",])
TERR=poses(T_IDLE,9,'ii',3)
TERR['crouch']=S([r for i,r in enumerate(T_IDLE) if i not in (13,14)])
TERR['dead']=S([''.join(T_IDLE[len(T_IDLE)-1-r][c] for r in range(len(T_IDLE))) for c in range(1,14)])

def crouch(spr): return S([r for i,r in enumerate(spr) if i not in (7,8)])

def _dust2(d):
    d.rectangle([0,20,W,GROUND],fill=(26,20,14))                               # sandstone wall
    for y in range(24,GROUND,7):
        for x in range((y//7)%2*9,W,18): d.line([x,y,x,y+6],fill=(20,15,10))
        d.line([0,y,W,y],fill=(21,16,11))
    d.rectangle([60,24,104,GROUND],fill=(8,7,6))                              # the archway
    d.ellipse([60,12,104,36],fill=(8,7,6)); d.arc([58,10,106,38],180,360,fill=(40,31,20),width=2)
    d.line([58,24,58,GROUND],fill=(40,31,20),width=2); d.line([105,24,105,GROUND],fill=(40,31,20),width=2)
    for x0,y0,s in ((2,42,16),(4,28,13),(160,40,18),(170,28,12)):            # crates
        d.rectangle([x0,y0,x0+s,y0+s],fill=(44,32,18),outline=(62,46,26))
        d.line([x0,y0,x0+s,y0+s],fill=(58,43,24)); d.line([x0,y0+s,x0+s,y0],fill=(58,43,24))
    text(d,"B",126,30,(86,34,28),shadow=None)                                 # bomb site marker
    d.rectangle([122,27,133,37],outline=(64,28,22))
register_bg(THEME, lambda v: (v,int(v*0.8),int(v*0.55)), decor=_dust2)

# --- tiny text with the HUD glyphs the engine font lacks ($ + -) ------------------------------
_GLYPH={'$':"011110010011110",'+':"000010111010000",'-':"000000111000000"}
def _txt(d,s,x,y,c,shadow=(0,0,0)):
    for i,ch in enumerate(s):
        if ch in _GLYPH:
            if ch=='$': d.point((x+i*4+1,y-1),fill=c)
            for j,b in enumerate(_GLYPH[ch]):
                if b=='1':
                    px,py=x+i*4+j%3,y+j//3
                    if shadow: d.point((px+1,py+1),fill=shadow)
                    d.point((px,py),fill=c)
        else: text(d,ch,x+i*4,y,c,shadow)

# --- guns ------------------------------------------------------------------------------------
GUNS={   # (i0,i1,j,colour) runs along the barrel direction; i grows forward
 'usp':[(0,4,0,(170,170,182)),(0,1,1,(120,120,130))],
 'ak': [(-4,-1,0,(140,90,50)),(-4,-3,1,(140,90,50)),(0,6,0,(84,84,90)),(4,6,0,(150,98,54)),(7,10,0,(120,120,130)),
        (2,3,1,(70,70,76)),(3,4,2,(70,70,76))],
 'awp':[(-5,-1,0,(86,112,62)),(-5,-2,1,(86,112,62)),(0,9,0,(96,124,68)),(10,17,0,(120,126,120)),
        (2,7,-1,(34,34,40)),(3,3,1,(60,60,64))],
}
GUN_LEN={'usp':4,'ak':10,'awp':17}

@fx('cs_gun')
def _fx_gun(d,im,e,f):
    _,x,y,flip,kind,fire=e; s_=-1 if flip else 1; x,y=int(x),int(y)
    for i0,i1,j,c in GUNS[kind]:
        d.line([x+i0*s_,y+j,x+i1*s_,y+j],fill=c)
    if kind=='awp': d.point((x+7*s_,y-1),fill=(120,200,230))
    if fire:
        tip=x+(GUN_LEN[kind]+2)*s_; d.line([tip-s_,y,tip+2*s_,y],fill=(255,255,255))
        d.point((tip,y-1),fill=(255,220,120)); d.point((tip,y+1),fill=(255,220,120))

def _gun_icon(d,x,y,kind,c):
    """Killfeed silhouette (facing right), returns its width."""
    if kind=='ak':
        d.line([x,y+1,x+9,y+1],fill=c); d.line([x,y+2,x+1,y+2],fill=c); d.line([x+4,y+2,x+5,y+3],fill=c); return 10
    d.line([x,y+1,x+13,y+1],fill=c); d.line([x,y+2,x+2,y+2],fill=c); d.line([x+4,y,x+7,y],fill=c); return 14

def _hs_icon(d,x,y,c):
    d.ellipse([x,y-1,x+4,y+3],outline=c); d.point((x+2,y+1),fill=(255,60,60)); return 6

@fx('cs_kill')
def _fx_kill(d,im,e,f):
    """Killfeed line, right-aligned: killer [gun] [hs] victim."""
    _,y,killer,kc,gun,hs,victim,vc,mine=e
    w=len(killer)*4+2+(10 if gun=='ak' else 14)+2+(6 if hs else 0)+len(victim)*4
    x=W-3-w; px=im.load()
    for yy in range(y-2,y+7):
        for xx in range(x-3,W-1): blend(px,xx,yy,(0,0,0),0.6)
    if mine: d.rectangle([x-3,y-2,W-2,y+6],outline=(190,40,40))
    text(d,killer,x,y,kc); x+=len(killer)*4+1
    x+=_gun_icon(d,x,y,gun,(230,230,230))+1
    if hs: x+=_hs_icon(d,x,y,(230,230,230))
    text(d,victim,x,y,vc)

@fx('cs_hud')
def _fx_hud(d,im,e,f):
    """1.6 HUD on the bottom row: health, armor, round timer (or the blinking C4), money."""
    _,hp,ar,timer,c4,money=e
    y=59; d.rectangle([0,y,W,H],fill=(0,0,0))
    _txt(d,'+',2,y,AMBER); _txt(d,str(hp),7,y,AMBER if hp>25 else (230,50,40))
    d.polygon([(26,y),(30,y),(30,y+2),(28,y+4),(26,y+2)],outline=AMBER); _txt(d,str(ar),33,y,AMBER)
    if c4:
        if (f//(3 if c4>1 else 5))%2==0: d.rectangle([86,y,96,y+4],fill=(200,30,30)); d.line([88,y+2,94,y+2],fill=(255,150,140))
        else: d.rectangle([86,y,96,y+4],outline=(120,30,30))
    else: _txt(d,timer,84,y,AMBER)
    ms='$'+str(money); _txt(d,ms,W-3-len(ms)*4,y,(120,220,90))

@fx('cs_c4')
def _fx_c4(d,im,e,f):
    """The planted bomb: a brick with a keypad, a red LED and a beep ring. period = beep interval."""
    _,x,period,armed=e; x=int(x)
    d.rectangle([x-4,GROUND-4,x+4,GROUND-1],fill=(80,70,46),outline=(40,34,22)); d.rectangle([x-2,GROUND-3,x+1,GROUND-2],fill=(40,40,40))
    if armed:
        ph=f%period
        d.point((x+3,GROUND-4),fill=(255,40,40) if ph<2 else (90,20,20))
        if ph<4: d.ellipse([x+3-2*ph-2,GROUND-4-ph-1,x+3+2*ph+2,GROUND-4+ph+1],outline=(200,40,40))

@fx('cs_bar')
def _fx_bar(d,im,e,f):
    """Defuse progress bar."""
    _,p=e; x0,y0,w=W//2-30,26,60
    text(d,"DEFUSING...",W//2-22,y0-7,AMBER)
    d.rectangle([x0,y0,x0+w,y0+4],outline=AMBER)
    if p>0: d.rectangle([x0+2,y0+2,x0+2+int((w-4)*min(1,p)),y0+2],fill=AMBER)

@fx('cs_slot')
def _fx_slot(d,im,e,f):
    """Weapon-select slot (top-left): the AWP highlighted."""
    _,a=e
    if a<=0: return
    px=im.load()
    for yy in range(2,13):
        for xx in range(2,40): blend(px,xx,yy,(0,0,0),0.6*a)
    d.rectangle([2,2,39,12],outline=AMBER if (f//2)%2 or a<1 else (255,220,120))
    text(d,"1",4,4,AMBER); _gun_icon(d,10,4,'awp',AMBER); text(d,"AWP",25,7,(255,220,120))

@fx('cs_nade')
def _fx_nade(d,im,e,f):
    _,x,y=e; d.rectangle([x-1,y-1,x+1,y+1],fill=(190,190,200)); d.point((x,y-2),fill=(120,120,130))

@fx('cs_white')
def _fx_white(d,im,e,f):
    _,a=e
    if a>0: im.paste(Image.blend(im,Image.new('RGB',(W,H),(255,255,255)),min(1,a)))

@fx('cs_fade')
def _fx_fade(d,im,e,f):
    _,a=e
    if a>0: im.paste(Image.blend(im,Image.new('RGB',(W,H),(0,0,0)),min(1,a)))

@fx('cs_line')
def _fx_line(d,im,e,f):
    _,x0,y0,x1,y1,c=e; d.line([x0,y0,x1,y1],fill=c)

def closeup_scope(t,f):
    """Primer plano: through the AWP scope — the balaclava drifts into the crosshair; the shot."""
    im=Image.new('RGB',(W,H),(0,0,0)); world=Image.new('RGB',(W,H),(62,48,30)); wd=ImageDraw.Draw(world)
    for y in range(0,H,12):                                                   # zoomed sandstone blocks
        for x in range((y//12)%2*20-10,W,40): wd.rectangle([x,y,x+39,y+11],outline=(46,35,22))
    fired=t>=0.72
    sway=math.sin(f*0.5)*3*(1-ease(t/0.6))
    hx=int(ez(150,92,t/0.62)+sway); hy=int(33+math.cos(f*0.4)*2*(1-ease(t/0.6)))
    if fired: hx+=int(ez(0,14,(t-0.72)/0.12)); hy+=int(ez(0,-3,(t-0.72)/0.12))
    head=Image.new('RGB',(15,8),(0,0,0)); m=Image.new('L',(15,8),0); hp_,mp=head.load(),m.load()
    for y,row in enumerate(T_IDLE[:8]):
        for x,ch in enumerate(row):
            if ch!='.': hp_[x,y]=T_PAL.get(ch) or PAL[ch]; mp[x,y]=255
    k=5; head=head.resize((15*k,8*k),Image.NEAREST); m=m.resize((15*k,8*k),Image.NEAREST)
    world.paste(head,(hx-6*k,hy-4*k-k//2),m)                                  # eye slit on the crosshair
    if fired:
        rr=random.Random(5)
        for _ in range(26):
            a=rr.uniform(-1.2,1.2); r=rr.uniform(2,14)*ease((t-0.72)/0.2)
            wd.rectangle([hx+math.cos(a)*r,hy-10+math.sin(a)*r*0.7,hx+math.cos(a)*r+1,hy-10+math.sin(a)*r*0.7+1],fill=(170,20,20))
    mk=Image.new('L',(W,H),0); ImageDraw.Draw(mk).ellipse([92-40,32-40,92+40,32+40],fill=255)
    im.paste(world,(0,0),mk); d=ImageDraw.Draw(im)
    d.ellipse([92-40,32-40,92+40,32+40],outline=(20,20,20),width=2)
    d.line([52,32,132,32],fill=(0,0,0)); d.line([92,-8,92,72],fill=(0,0,0))
    if 0.72<=t<0.78:
        d.rectangle([0,0,W,H],fill=(255,255,255))

    if t<0.06:
        for i in range(10): a=i*0.63; d.line([W//2,H//2,W//2+math.cos(a)*120,H//2+math.sin(a)*60],fill=(255,255,255))
    return im

def _hp(f,marks,base=100):
    v=base
    for t0,val in marks:
        if f>=t0: v=val
    return v if f<270 else base

def clip_defuse(f):
    s=scene(f,THEME)
    reset=f>=270
    cl=actor(CT[guard_pose(f)],30,pal=CT_PAL); tr=actor(TERR['idle'],150,flip=True,pal=T_PAL)
    cgun=['usp',False]; tgun=['ak',False]; cgp=None
    # --- timer / bomb state -------------------------------------------------------------------
    secs=115 if (f<24 or reset) else 115-(min(f,236)-24)//3
    planted=56<=f<236 and not reset
    period=max(3,int(lerp(14,4,(f-56)/180)))
    if 24<=f<38: callout(s,"GO GO GO!",y=20,c=(120,220,90))
    # --- 1) the Terrorist runs to B and plants ------------------------------------------------
    if 24<=f<40: tr.update(x=ez(150,112,(f-24)/16),spr=TERR['idle'] if (f//3)%2 else TERR['attack'])
    if 40<=f<56:
        tr.update(x=112,spr=TERR['crouch']); tgun[0]=None
        if f%4==0: s['fx'].append(('mote',106+(f//4)%3,GROUND-5,(120,255,120)))
    if f>=48 and not reset and f<236: s['under'].append(('cs_c4',104,period,f>=56))
    if 236<=f<270 and not reset: s['under'].append(('cs_c4',104,period,False))
    if 56<=f<80: callout(s,"THE BOMB HAS BEEN PLANTED",y=20,c=(255,90,70))
    if 56<=f<66: tr.update(x=ez(112,140,(f-56)/10))
    # --- 2) firefight -------------------------------------------------------------------------
    if 66<=f<104:
        tr['x']=140; cl['spr']=CT['charge']; cgp=(cl['x']+7,GROUND-6)
        if f%6==0: cgun[1]=True; s['fx'].append(('tracer',cl['x']+14,tr['x']-2,GROUND-7-(f//6)%3))
        if f%6==1: s['fx'].append(('spark',tr['x']+random.choice([-10,10]),GROUND-10-random.randint(0,8),2))
        if f%4==2:
            tgun[1]=True; y=GROUND-9+(f//4)%3
            s['fx'].append(('tracer',cl['x']+6,tr['x']-16,y))
        if f in (78,94): cl['spr']=CT['hurt']; s['shake']=rshake(1); s['fx'].append(('spark',cl['x']+2,GROUND-8,3))
    if 80<=f<262 and not reset: s['fx'].append(('cs_kill',2,"PHOENIX",T_RED,'ak',False,"BOT",CT_BLUE,False))
    # --- 3) flashbang -------------------------------------------------------------------------
    if 100<=f<110:
        t=(f-100)/10; s['fx'].append(('cs_nade',lerp(136,70,t),GROUND-12-int(26*math.sin(math.pi*t)*0.8)))
        tr['spr']=TERR['attack']; tgun[0]=None
    if 110<=f<130: cl.update(spr=CT['hurt'],x=30+((f//2)%2)); cgun[0]=None
    white=0.8 if 110<=f<118 else (lerp(0.8,0,(f-118)/12) if 118<=f<130 else 0)   # not a full white panel under the notch
    # --- 4) draw the AWP ----------------------------------------------------------------------
    if 124<=f<150: s['fx'].append(('cs_slot',min(1,(f-124)/3) if f<146 else (150-f)/4))
    if 130<=f<136: cl['spr']=CT['armsup']; cgun[0]=None
    if f>=136: cgun[0]='awp'
    if 136<=f<150: cl['spr']=CT['charge']; cgp=(cl['x']+7,GROUND-6)
    if 150<=f<190: s['image']=closeup_scope((f-150)/40,f); return s
    # --- 5) HEADSHOT ----------------------------------------------------------------------------
    dead=190<=f<270
    if 190<=f<206: cl['spr']=CT['charge']; cgp=(cl['x']+7,GROUND-6)
    if 190<=f<193: s['fx'].append(('cs_line',cl['x']+26,GROUND-6,150,GROUND-15,(255,255,255))); cgun[1]=True
    if 190<=f<196: tr.update(spr=TERR['hurt'],x=ez(150,158,(f-190)/6)); tgun[0]=None
    if 196<=f<270: tr.update(spr=TERR['dead'],x=160,flip=False); tgun[0]=None
    if 190<=f<196:
        for j in range(5): s['fx'].append(('shard',152+random.randint(0,8),GROUND-18+random.randint(-3,3),(180,20,20)))
    if 190<=f<212: s['fx'].append(('big',"HEADSHOT",26,(230,40,40)))
    if 190<=f<262 and not reset: s['fx'].append(('cs_kill',11,"CLAUDE",CT_BLUE,'awp',True,"PHOENIX",T_RED,True))
    # --- 6) the defuse ------------------------------------------------------------------------
    if 206<=f<218: cl.update(spr=CT['guard' if (f//2)%2 else 'guard2'],x=ez(30,94,(f-206)/12)); cgun[0]=None
    if 218<=f<236:
        cl.update(spr=crouch(CT['charge']),x=94); cgun[0]=None; s['fx'].append(('cs_bar',(f-218)/16))
        if f%3==0: s['fx'].append(('mote',100+(f//3)%3,GROUND-6,(120,200,255)))
    if 236<=f<270:
        cl.update(spr=CT['armsup'] if (f//4)%2 else CT['guard'],x=94); cgun[0]=None
        if f<256: callout(s,"BOMB HAS BEEN DEFUSED",y=20,c=CT_BLUE)
        if f>=244: s['fx'].append(('big',"COUNTER-TERRORISTS WIN",29,CT_BLUE))
    # --- 7) new round: fade out, respawn at the neutral pose, fade in ---------------------------
    fade=ez(0,1,(f-258)/10) if 258<=f<270 else (ez(1,0,(f-270)/12) if 270<=f<282 else 0)
    if reset: cl.update(spr=CT[guard_pose(f)],x=30); tr.update(spr=TERR['idle'],x=150); cgun=['usp',False]; tgun=['ak',False]
    # --- guns + HUD ---------------------------------------------------------------------------
    if cgun[0]:
        if cgp is None: cgp=(cl['x']+5,GROUND-7)
        s['fx'].append(('cs_gun',cgp[0],cgp[1],False,cgun[0],cgun[1]))
    if tgun[0] and tr['spr'] in (TERR['idle'],TERR['attack']):
        s['fx'].append(('cs_gun',tr['x']-3 if tr['spr'] is TERR['idle'] else tr['x']-6,GROUND-8,True,'ak',tgun[1]))
    hp=_hp(f,[(78,76),(94,53)]); ar=_hp(f,[(78,64),(94,31)])
    s['fx'].append(('cs_hud',hp,ar,f"{secs//60}:{secs%60:02d}",(2 if f>=176 else 1) if planted else 0,800))
    s['fx'].append(('cs_white',white)); s['fx'].append(('cs_fade',fade))
    s['actors']=[tr,cl]
    return s

CLIPS = [clip('defuse', N_, clip_defuse)]
