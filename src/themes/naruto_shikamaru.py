"""Naruto sub-theme "naruto-shikamaru": Claude as Shikamaru vs Hidan in the Nara clan forest, deer
between the trees. Hidan throws his three-bladed scythe on its cable (FOR JASHIN!) and Claude hops it.
Close-up: the thinking pose, fingertips in a ring, shogi pieces sliding behind his closed eyes (WHAT A
DRAG...). Hidan charges; Claude's shadow stretches along the ground and catches him mid-run (KAGEMANE NO
JUTSU!): Hidan copies every move, raises his arms and drops the scythe (I CANT MOVE!). Explosive tags
glint on the wires round him. Close-up: Asuma's lighter lights the cigarette (FOR ASUMA.). The lighter
is tossed onto the fuse, the tags go up and Hidan drops into the pit (CHECKMATE.). He is immortal, so a
hand pokes out of the dirt, he climbs out with the scythe and walks back for the loop."""
from engine import *
from themes.nrt import shout                                       # same franchise: outlined big text

THEME = 'naruto-shikamaru'
N_ = 400
CX, EX = 30, 150                                                    # the loop keyframe positions
HX = 124                                                            # where Hidan is caught (the trap)

SKIN,SKIN_D,INK=(217,119,87),(168,80,54),(40,20,16)
# Shikamaru: black pineapple ponytail, the olive Chunin flak vest
SPAL={'l':(34,32,40),'f':(74,72,90),'a':(96,112,62),'i':(64,78,40)}
HAIR=[".l.l.l....",".lflfl....","..lll.....","lllllllll."]

def _shika(spr):
    spr=overlay(spr,HAIR,-1,0,bangs="llllllllll")
    def vest(x,y,t,l,r,c):
        if c=='O' and t+5<=y<=t+7: return 'i' if x==l+5 or y==t+5 and x in (l,r) else 'a'
    return recolor_rows(spr,vest)
SHIKA=variant(_shika)

# Hidan: slicked-back silver hair, the open Akatsuki cloak (red clouds), the Jashin pendant
HIDAN=S([
"....hhhhh.......","...hHHhhhh......","...hhssssss.....","...h.sUssU......",".....sssss......","......sss.......",
"....bbsssbbb....","...bbbsDsbbbb...","..bbrbssssbrbb..","..bWrbbssbbrWb..","..bb.bbbbbb.bb..","..ss.bbbbbb.ss..",
".....bbrrbb.....",".....bWrrWb.....","....bbbbbbbb....","....bbbbbbbb....",".....NN..NN.....",".....NN..NN.....",
"....kkk..kkk....",])
def _arms(spr,back,front):
    """Raise the back and/or front arm straight up (the sleeve along the side, the hand above the head)."""
    g=[list(r) for r in spr]
    for raise_,cols,sleeve in ((back,(2,3),(1,2)),(front,(12,13),(13,14))):
        if not raise_: continue
        for y in (10,11):
            for x in cols: g[y][x]='.'
        for y in range(2,8):
            for x in sleeve: g[y][x]='b'
        for y in (0,1):
            for x in sleeve: g[y][x]='s'
    return S([''.join(r) for r in g])
HID={'idle':HIDAN,'raise':_arms(HIDAN,False,True),'up':_arms(HIDAN,True,True),'hurt':hurt(HIDAN)}
HAND_IDLE,HAND_UP=(12,11),(13,0)                                    # his front hand (the scythe hand)
JASHIN=(220,40,50)

# ---- background: the Nara clan forest at dusk -------------------------------------------------------
TRUNKS=((6,7),(28,4),(58,6),(84,3),(104,6),(150,7),(172,5))         # (x, half-width); 104 and 150 hold the wires
def _nara(d):
    for y in range(50):                                             # dusk through the canopy
        k=y/49; d.line([0,y,W,y],fill=(int(40+80*k),int(58+70*k),int(46+30*k)))
    rr=random.Random(1012)
    for x0 in (20,70,118,160):                                      # shafts of evening light
        d.polygon([(x0,0),(x0+10,0),(x0-6,50),(x0-18,50)],fill=(108,124,78))
    for _ in range(12):                                             # far trunks, faded
        x=rr.randint(0,W); d.rectangle([x,6,x+1,50],fill=(58,70,52))
    for x,y in ((44,46),(132,45)):                                  # Nara deer, far off between the trees
        c=(52,60,44); d.rectangle([x,y-4,x+6,y-2],fill=c); d.line([x+1,y-2,x+1,y],fill=c); d.line([x+5,y-2,x+5,y],fill=c)
        d.rectangle([x+6,y-7,x+7,y-4],fill=c); d.point((x+8,y-6),fill=c)
        d.line([x+6,y-8,x+5,y-10],fill=c); d.line([x+7,y-8,x+8,y-10],fill=c); d.point((x+4,y-10),fill=c); d.point((x+9,y-10),fill=c)
    for x,w in TRUNKS:                                              # the near trunks
        d.rectangle([x-w,0,x+w,52],fill=(56,40,30)); d.rectangle([x-w,0,x-w+1,52],fill=(84,62,44))
        d.rectangle([x+w-1,0,x+w,52],fill=(40,28,22))
        for y in range(4,50,7): d.line([x-w+2,y,x-w+3,y+2],fill=(40,28,22))
        d.polygon([(x-w-3,52),(x-w,46),(x+w,46),(x+w+3,52)],fill=(56,40,30))   # roots
    for _ in range(40):                                             # the canopy
        x=rr.randint(-6,W+6); y=rr.randint(-6,8); r=rr.randint(5,10)
        d.ellipse([x-r,y-r,x+r,y+r],fill=rr.choice([(30,58,34),(40,72,40),(24,46,28)]))
    d.rectangle([0,52,W,H],fill=(62,72,40))                         # the forest floor
    d.line([0,52,W,52],fill=(84,98,52))
    for _ in range(70): d.point((rr.randint(0,W-1),rr.randint(53,H-1)),fill=rr.choice([(80,92,48),(48,56,32),(96,84,52)]))
    for _ in range(14):                                             # grass tufts
        x=rr.randint(0,W-3); y=rr.randint(53,62); d.line([x,y,x+1,y-2],fill=(96,120,56)); d.line([x+2,y,x+2,y-2],fill=(96,120,56))
register_bg(THEME, lambda v: (v+40,v+50,v+20), decor=_nara)

# ---- effects ----------------------------------------------------------------------------------------
def scythe(d,x,y,a,side=1):
    """Hidan's triple-bladed scythe: the pole from (x,y) along angle a, three red blades at its end."""
    L=20; ex,ey=x+math.cos(a)*L,y+math.sin(a)*L
    d.line([x-math.cos(a)*3,y-math.sin(a)*3,ex,ey],fill=(70,50,40))
    nx,ny=math.cos(a+side*math.pi/2),math.sin(a+side*math.pi/2); ux,uy=math.cos(a),math.sin(a)
    for k in range(3):
        bx,by=ex-ux*k*3,ey-uy*k*3; s=8-k*1.5
        tip=(bx+nx*s-ux*3,by+ny*s-uy*3)
        d.polygon([(bx,by),tip,(bx-ux*2.5,by-uy*2.5)],fill=(196,28,40))
        d.line([(bx,by),tip],fill=(250,120,120))

@fx('sk_scythe')
def _fx_scythe(d,im,e,f):
    _,x,y,a,side=e; scythe(d,x,y,a,side)

@fx('sk_cable')
def _fx_cable(d,im,e,f):
    _,x0,y0,x1,y1,slack=e; n=10
    pts=[(lerp(x0,x1,i/n),lerp(y0,y1,i/n)+slack*math.sin(math.pi*i/n)) for i in range(n+1)]
    d.line(pts,fill=(150,150,160))

@fx('sk_shadow')
def _fx_shadow(d,im,e,f):
    """Kagemane: Claude's shadow stretched along the ground from x0 to its tip x1."""
    _,x0,x1=e; x0,x1=int(x0),int(x1)
    if x1<=x0: return
    m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m)
    for x in range(x0,x1+1):
        w=1.6+0.6*math.sin(x*0.45-f*0.5)
        if x1-x<4: w*= (x1-x+1)/5                                 # the pointed tip, feeling its way
        md.line([x,GROUND+1-w,x,GROUND+1+w],fill=225)
    md.ellipse([x0-8,GROUND-1,x0+8,GROUND+3],fill=225)
    im.paste((8,6,12),(0,0),m)

@fx('sk_tags')
def _fx_tags(d,im,e,f):
    """The trap: two wires between the trunks, explosive tags hanging off them (gone = list of burnt ones)."""
    _,gone=e
    for i,(x0,y0,x1,y1) in enumerate(((110,22,143,30),(110,44,143,38))):
        d.line([x0,y0,x1,y1],fill=(170,170,180))
        for j in range(4):
            if i*4+j in gone: continue
            t=(j+0.6)/4.2; x=int(lerp(x0,x1,t)); y=int(lerp(y0,y1,t))
            d.rectangle([x-1,y+1,x+1,y+6],fill=(236,226,196)); d.line([x,y+2,x,y+5],fill=(200,40,40))

@fx('sk_fuse')
def _fx_fuse(d,im,e,f):
    """The fuse along the ground to the trap, burnt up to x (None: unlit)."""
    _,x0,x1,burn=e
    d.line([x0,GROUND+2,x1,GROUND+2],fill=(150,140,120))
    if burn is not None:
        d.line([x0,GROUND+2,int(burn),GROUND+2],fill=(40,34,30))
        rr=random.Random(f)
        for _ in range(4): d.point((int(burn)+rr.randint(-2,2),GROUND+2-rr.randint(0,3)),fill=rr.choice([(255,220,90),(255,140,40),(255,255,255)]))

@fx('sk_lighter')
def _fx_lighter(d,im,e,f):
    """Asuma's lighter tumbling through the air, lit."""
    _,x,y=e; x,y=int(x),int(y)
    d.rectangle([x-1,y-1,x+1,y+2],fill=(196,200,210)); d.point((x,y-1),fill=(255,255,255))
    d.point((x,y-2),fill=(255,200,80)); d.point((x,y-3),fill=(255,240,170) if f%2 else (255,150,40))

@fx('sk_cig')
def _fx_cig(d,im,e,f):
    """The cigarette in Claude's mouth, smoke curling up from its tip."""
    _,x,y=e; x,y=int(x),int(y)
    d.line([x,y,x+2,y],fill=(240,236,226)); d.point((x+3,y),fill=(255,110,40) if f%6<4 else (255,190,90))
    for k in range(4):
        ph=(f*0.6+k*5)%20; d.point((x+3+int(1.5*math.sin(ph*0.4+k)),y-1-int(ph*0.6)),fill=(200,200,206) if ph<12 else (150,150,156))

@fx('sk_pit')
def _fx_pit(d,im,e,f):
    _,x,w=e; d.ellipse([x-w,GROUND-1,x+w,GROUND+3],fill=(14,10,8))

@fx('sk_lip')
def _fx_lip(d,im,e,f):
    """The front lip of the pit, drawn over the sinking body so it reads as going in."""
    _,x,w=e; d.rectangle([x-w,GROUND+1,x+w,GROUND+4],fill=(62,72,40)); d.line([x-w,GROUND+1,x+w,GROUND+1],fill=(84,98,52))

@fx('sk_mound')
def _fx_mound(d,im,e,f):
    """The dirt the blast threw back over the pit (k 0..1: its height)."""
    _,x,k=e
    if k<=0: return
    h=int(5*k); d.ellipse([x-13,GROUND+1-h,x+13,GROUND+1+h],fill=(98,74,48)); d.ellipse([x-9,GROUND+2-h,x+7,max(GROUND,GROUND+2-h)],fill=(122,94,60))
    rr=random.Random(5)
    for _ in range(int(10*k)): d.point((x+rr.randint(-10,10),GROUND+1-rr.randint(0,max(1,h-1))),fill=(70,54,36))

@fx('sk_hand')
def _fx_hand(d,im,e,f):
    """A hand clawing up out of the mound (k 0..1: how far out)."""
    _,x,k=e; h=int(6*k)
    if h<=0: return
    d.rectangle([x-1,GROUND-h,x+1,GROUND-1],fill=(26,26,34)); d.rectangle([x-1,GROUND-h-2,x+1,GROUND-h],fill=(240,200,160))
    for dx in (-1,1): d.point((x+dx,GROUND-h-3),fill=(240,200,160))

# ---- close-ups --------------------------------------------------------------------------------------
def shika_face(d,ox,eyes):
    """Claude-as-Shikamaru's face for close-ups (x ox..ox+56): the ponytail, eyes 'closed'|'open'|'lidded'."""
    hair,hl=SPAL['l'],SPAL['f']
    for k in range(5):                                              # the pineapple, outlined against the dark
        p=[(ox+12+k*6,11),(ox+21+k*6,11),(ox+15+k*6+(k%2)*5,-3+(k%2)*3)]
        d.polygon(p,fill=hair,outline=hl)
    d.rectangle([ox+16,8,ox+40,11],fill=(60,50,40))                # the hair tie
    d.rectangle([ox,14,ox+54,H],fill=SKIN); d.rectangle([ox+48,14,ox+54,H],fill=SKIN_D)
    d.polygon([(ox-2,22),(ox-2,9),(ox+56,9),(ox+56,22),(ox+50,15),(ox+4,15)],fill=hair)   # pulled-back hairline
    d.line([ox+6,13,ox+46,13],fill=hl)
    for ex in (ox+16,ox+38):
        if eyes=='closed':
            d.arc([ex-5,28,ex+5,36],20,160,fill=INK,width=2)
        else:
            top=31 if eyes=='lidded' else 29
            d.rectangle([ex-4,top,ex+4,37],fill=(24,14,12)); d.rectangle([ex-2,top+1,ex+1,36],fill=(70,56,50))
            d.point((ex-1,top+1),fill=(255,255,255)); d.line([ex-5,top,ex+5,top],fill=INK)
        d.line([ex-6,24,ex+6,25 if ex<ox+27 else 23],fill=(24,14,12))  # flat, bored brows
    d.rectangle([ox-3,34,ox,40],fill=SKIN_D); d.point((ox-2,40),fill=(200,200,214))   # ear + stud earring
    d.rectangle([ox+54,34,ox+57,40],fill=SKIN_D); d.point((ox+56,40),fill=(200,200,214))

PIECES=[(94,8),(94,54),(124,58),(156,58),(178,8),(178,52)]   # round the text, never under it
def _shogi(d,x,y,c,edge):
    d.polygon([(x,y-5),(x+4,y-2),(x+4,y+4),(x-4,y+4),(x-4,y-2)],fill=c,outline=edge); d.line([x-1,y,x+1,y],fill=edge)

def closeup_think(t,f):
    """Primer plano: the thinking pose, fingertips in a ring under his chin; behind his closed eyes the
    shogi pieces slide square by square through the moves — WHAT A DRAG... — then the eyes open."""
    open_=t>=0.8
    im=Image.new('RGB',(W,H),(14,24,20)); d=ImageDraw.Draw(im)
    for x in range(86,W,12): d.line([x,0,x,H],fill=(26,42,34))  # the board, faint
    for y in range(2,H,12): d.line([86,y,W,y],fill=(26,42,34))
    step=int(t*12)
    for i,(x,y) in enumerate(PIECES):
        dx=4*((step+i)%3-1) if not open_ else 0; dy=3*((step*2+i)%3-1) if not open_ else 0
        c,edge=((150,126,80),(70,56,36)) if not open_ else ((250,214,110),(140,90,20))
        _shogi(d,x+dx,y+dy,c,edge)
    shika_face(d,10,'open' if open_ else 'closed')
    cx,cy=38,52                                                     # the hands: fingertips meeting in a ring
    for sx in (-1,1): d.polygon([(cx+sx*30,H),(cx+sx*18,56),(cx+sx*8,H)],fill=(44,44,96))   # sleeves
    d.ellipse([cx-18,cy-12,cx+18,cy+12],outline=INK,width=8)
    d.ellipse([cx-17,cy-11,cx+17,cy+11],outline=SKIN,width=6)
    for a in range(20,360,40):                                      # the gaps between the fingers
        r=math.radians(a); d.line([cx+math.cos(r)*11,cy+math.sin(r)*6,cx+math.cos(r)*17,cy+math.sin(r)*11],fill=SKIN_D)
    for yy in (cy-12,cy+6):  d.line([cx,yy,cx,yy+6],fill=INK)        # where the fingertips touch
    for sx in (-1,1): d.rectangle([cx+sx*4-2,cy+7,cx+sx*4+2,cy+12],fill=SKIN,outline=INK)   # the thumbs
    if 0.12<=t:
        big_text(im,"WHAT A",14,(230,236,220),scale=2,cx=140,outline=(20,34,26))
        big_text(im,"DRAG...",32,(230,236,220),scale=2,cx=140,outline=(20,34,26))
    if open_ and t<0.86: im=fade_to(im,(255,240,180),0.5*(1-(t-0.8)/0.06)); d=ImageDraw.Draw(im); zoom_lines(d,(250,214,110))
    if t<0.06: zoom_lines(d,(120,150,120))
    if t>0.92: im=fade_to(im,(0,0,0),0.6*(t-0.92)/0.08)
    return im

def closeup_lighter(t,f):
    """Primer plano: Asuma's lighter. The lid clicks open, the wheel sparks, the flame lights the
    cigarette and the face goes warm; the smoke curls up — FOR ASUMA."""
    im=Image.new('RGB',(W,H),(18,14,14)); d=ImageDraw.Draw(im)
    lit=0.3<=t<0.62; glow=min(1,(t-0.3)/0.1) if t>=0.3 else 0
    if t>=0.62: glow=max(0.35,1-(t-0.62)/0.1)                       # the lid snaps shut, the tip still glows
    shika_face(d,4,'lidded')
    lx,top=88,38                                                    # the lighter: a big steel Zippo in the hand
    tip=(lx-2,top-9)
    d.line([50,51,tip[0],tip[1]],fill=(244,240,230),width=3)        # the cigarette, its tip in the flame
    d.line([50,51,56,48],fill=(220,170,100),width=3)
    d.polygon([(lx+14,H),(lx+30,H),(lx+22,50)],fill=(44,44,96))      # the sleeve
    d.rectangle([lx-9,top,lx+9,H],fill=(186,190,200),outline=(90,92,104)); d.line([lx-6,top+2,lx-6,H],fill=(240,242,248))
    d.line([lx-9,top+4,lx+9,top+4],fill=(90,92,104))
    if t<0.15 or t>=0.62: d.rectangle([lx-9,top-9,lx+9,top],fill=(170,174,186),outline=(90,92,104))   # the lid, shut
    else:
        d.polygon([(lx+9,top),(lx+20,top-9),(lx+23,top-6),(lx+12,top+3)],fill=(170,174,186),outline=(90,92,104))
        d.rectangle([lx-6,top-7,lx+2,top],fill=(150,154,166),outline=(90,92,104))   # the chimney
        for hx in (lx-4,lx-1): d.point((hx,top-4),fill=(60,60,70))
        d.ellipse([lx+2,top-6,lx+8,top],fill=(80,80,90),outline=(50,50,58))         # the wheel
    d.rectangle([lx-12,top+8,lx+4,H],fill=SKIN,outline=INK)         # fingers round it, the thumb on the wheel
    for k in range(4): d.line([lx-12,top+12+k*4,lx-4,top+12+k*4],fill=SKIN_D)
    d.rectangle([lx+4,top-3,lx+12,top+6],fill=SKIN,outline=INK)
    if 0.2<=t<0.3:
        rr=random.Random(f)
        for _ in range(8): d.point((lx-2+rr.randint(-4,4),top-8-rr.randint(0,6)),fill=rr.choice([(255,230,120),(255,255,255)]))
    if glow:
        g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse([lx-70,top-40,lx+20,top+40],fill=int(110*glow))
        im.paste((255,150,60),(0,0),g.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    if lit:
        fh=11+(f%3)
        d.polygon([(lx-5,top-7),(lx-2,top-7-fh),(lx+1,top-7)],fill=(255,170,50))
        d.polygon([(lx-4,top-7),(lx-2,top-4-fh),(lx,top-7)],fill=(255,240,170))
        d.point((lx-2,top-7),fill=(110,150,255))
    if t>=0.45:
        k=(f%6)/6; d.ellipse([tip[0]-2,tip[1]-2,tip[0]+2,tip[1]+2],fill=(255,110,40) if k<0.6 else (255,170,70))
    if t>=0.5:                                                      # the smoke, one curling ribbon
        n=int(min(1,(t-0.5)/0.2)*26)
        for i in range(n):
            y=tip[1]-3-i; x=tip[0]+3*math.sin(i*0.28-f*0.3)*(i/26)
            if y>=0: d.point((int(x),y),fill=(200,200,206) if i<14 else (140,140,148))
    if t>=0.4:
        big_text(im,"FOR",14,(255,226,170),scale=2,cx=150,outline=(70,30,10))
        big_text(im,"ASUMA.",32,(255,226,170),scale=2,cx=150,outline=(70,30,10))
    if t<0.06: zoom_lines(d,(255,200,120))
    if t>0.9: im=fade_to(im,(0,0,0),0.6*(t-0.9)/0.1)
    return im

# ---- the clip ---------------------------------------------------------------------------------------
TAG_SPOTS=[(lerp(110,143,(j+0.6)/4.2),lerp(y0,y1,(j+0.6)/4.2)+3) for (y0,y1) in ((22,30),(44,38)) for j in range(4)]
FUSE=(62,HX)
def sink(spr,k):
    """The sprite with its bottom k rows gone: drawn on the ground line it looks sunk k px into it."""
    k=max(0,min(len(spr)-1,int(k))); return spr[:len(spr)-k] if k else spr

def clip_kagemane(f):
    s=scene(f,THEME)
    cl=actor(SHIKA[guard_pose(f)],CX,pal=SPAL); hd=actor(HID['idle'],EX,flip=True)
    held=True                                                       # the scythe is in Hidan's hand
    # 1) FOR JASHIN!: the scythe on its cable — Claude hops it
    if 14<=f<46: shout(s,"FOR JASHIN!",(255,200,200),outline=(110,0,10))
    if 14<=f<26: hd['spr']=HID['raise']
    if 26<=f<56:
        held=False; hx,hy=hand_at(HID['idle'],EX,GROUND,True,*HAND_IDLE)
        if f<40: t=(f-26)/14; x=lerp(hx,16,t); y=lerp(hy,GROUND-2,t)-14*math.sin(math.pi*t); a=f*0.9; slack=2
        elif f<44: x,y,a,slack=16,GROUND-2,-math.pi/2-0.5,3
        else: t=(f-44)/12; x=lerp(16,hx,ease(t)); y=lerp(GROUND-2,hy,ease(t))-8*math.sin(math.pi*t); a=-math.pi/2-0.5+t*5; slack=0
        s['fx'].append(('sk_cable',hx,hy,x,y,slack)); s['fx'].append(('sk_scythe',x,y,a,1))
        if f==40: s['fx'].append(('spark',16,GROUND-2,4)); s['shake']=rshake()
        if 40<=f<44: s['fx']+= [('dust',16+random.randint(-4,4),GROUND-random.randint(0,2))]
        hd['spr']=HID['idle']
    if 30<=f<44: t=(f-30)/14; cl.update(y=GROUND-int(18*math.sin(math.pi*t)),spr=SHIKA['guard2'])
    # 2) close-up: the thinking pose
    if 56<=f<116: s['image']=closeup_think((f-56)/60,f); return s
    # 3) Hidan charges; the shadow stretches out and catches him
    caught=140<=f<300
    if 116<=f<300: cl['spr']=SHIKA['charge']
    if 116<=f<158: shout(s,"KAGEMANE",(200,220,190),y=2,outline=(10,30,20)); shout(s,"NO JUTSU!",(200,220,190),y=15,scale=1,outline=(10,30,20))
    if 120<=f<140:
        t=(f-120)/20; hd.update(spr=HID['raise'],x=lerp(EX,HX,t),y=GROUND-((f//2)%2))
    if 116<=f<300:
        tip=lerp(CX+6,HX,(f-116)/24) if f<140 else HX+4
        s['under'].append(('sk_shadow',CX+2,tip))
    if caught:
        hd.update(x=HX,spr=HID['raise'])
        if f==140: s['flash']=0.4; s['fc']=(HX,GROUND); s['flashc']=(120,140,110); s['shake']=rshake()
    # 4) he copies Claude: arms up, the scythe drops
    if 158<=f<196: callout(s,"I CANT MOVE!",c=(255,170,170))
    if 166<=f<186: cl['spr']=SHIKA['armsup']; hd['spr']=HID['up']
    dropped=166<=f<318
    if dropped:
        held=False
        hx,hy=hand_at(HID['raise'],HX,GROUND,True,*HAND_UP)
        t=min(1,(f-166)/8); s['under'].append(('sk_scythe',lerp(hx,HX-14,t),lerp(hy,GROUND-1,t*t),lerp(-math.pi/2,math.pi+0.15,t),1))
    if 186<=f<300: hd['spr']=HID['idle']
    # 5) the trap shows: tags on the wires, the fuse along the ground
    gone=[i for i in range(8) if f>=300+i*2]
    if 190<=f<316: s['under'].append(('sk_tags',gone))
    if 190<=f<300:
        burn=None if f<276 else lerp(FUSE[0],FUSE[1],(f-276)/20)
        s['under'].append(('sk_fuse',FUSE[0],FUSE[1],burn))
    if 194<=f<206:
        for i in (1,4,6): x,y=TAG_SPOTS[i]; s['fx'].append(('twinkle',x,y,1+(f+i)%2))
    # 6) close-up: Asuma's lighter
    if 206<=f<266: s['image']=closeup_lighter((f-206)/60,f); return s
    if 266<=f<336:
        ox,oy=origin(cl['spr'],cl['x']); top,_,_=body_box(cl['spr'])
        s['fx'].append(('sk_cig',ox+11,oy+top+4))
    if 266<=f<278:                                                  # the lighter tossed onto the fuse
        t=(f-266)/12; s['fx'].append(('sk_lighter',lerp(CX+8,FUSE[0],t),lerp(GROUND-10,GROUND,t)-12*math.sin(math.pi*t)))
        cl['spr']=SHIKA['punch'] if f<270 else SHIKA['charge']
    if 278<=f<300: s['under'].append(('sk_lighter',FUSE[0]-1,GROUND+1))
    # 7) the tags go up: CHECKMATE.
    if 300<=f<336: shout(s,"CHECKMATE.",(240,236,220),y=3,outline=(40,30,20))
    if 300<=f<324:
        k=f-300
        for i,(x,y) in enumerate(TAG_SPOTS):
            j=k-i*2
            if 0<=j<8: s['fx'].append(('boom',x,y,2+j*2))
            if 2<=j<14: s['fx'].append(('smoke',x+random.randint(-3,3),y-j//2,3+j//3,(120,110,100) if j%2 else (240,150,60)))
        if k==0: s['flash']=1.0; s['fc']=(HX,40); s['flashc']=(255,220,150)
        if k<18: s['shake']=rshake(2 if k<10 else 1)
        if 4<=k<16: s['fx']+= [('rock',HX+random.randint(-20,20),GROUND-random.randint(4,30)) for _ in range(3)]
    if 300<=f<322:                                                  # Hidan drops into the pit
        k=min(len(HID['hurt'])+1,(f-300)*1.4); hd.update(spr=sink(HID['hurt'],k),x=HX,vis=k<len(HID['hurt']))
        s['under'].append(('sk_pit',HX,11)); s['fx'].append(('sk_lip',HX,12))
    if 322<=f<300+60: hd['vis']=False
    mound=(1.0 if f<362 else max(0,1-(f-362)/14)) if 318<=f<376 else 0
    if 318<=f<326: mound=(f-318)/8
    if mound: s['fx'].append(('sk_mound',HX,mound))
    if 318<=f<336:
        rr=random.Random(f//3)
        for j in range(int(8*(336-f)/18)): s['fx'].append(('smoke',HX+rr.randint(-16,16),GROUND-rr.randint(0,16),rr.randint(2,4),(110,100,86)))
    # 8) ...but he is immortal: a hand claws out, he climbs out and walks back
    if 342<=f<352: s['fx'].append(('sk_hand',HX-4,min(1,(f-342)/5)))
    if 346<=f<384: callout(s,"I AM IMMORTAL!",c=(255,170,170))
    if 352<=f<362:
        k=len(HIDAN)*(1-(f-352)/10); hd.update(vis=True,spr=sink(HID['hurt'],k),x=HX)
        s['fx'].append(('sk_lip',HX,12))
        if f%2==0: s['fx'].append(('dust',HX+random.randint(-8,8),GROUND-random.randint(0,2)))
    if 362<=f<384:
        t=(f-362)/22; hd.update(vis=True,x=ez(HX,EX,t),spr=HID['hurt'] if t<0.6 else HID['idle'],y=GROUND-((f//3)%2 if t<1 else 0))
    if hd['vis'] and held and f not in range(300,362):
        sp=hd['spr']; cell=HAND_UP if sp is HID['raise'] else HAND_IDLE
        hx,hy=hand_at(sp,hd['x'],hd['y'],True,*cell)
        s['under' if sp is HID['idle'] else 'fx'].append(('sk_scythe',hx,hy,-math.pi/2+0.35,-1))
    s['actors']=[cl,hd]
    return s

CLIPS = [clip('kagemane', N_, clip_kagemane)]
