"""Among Us: Claude (an orange crewmate with a little asterisk on his head) and Codex (a white
crewmate, ">_" on the visor) in the cafeteria of The Skeld, next to the emergency button. Claude
fixes the wiring (close-up: four wires connected, TASK COMPLETE!) and turns round just as Codex
hops into a vent — ?! The lights go out; in the circle of his vision Claude finds a body. DEAD
BODY REPORTED. Meeting: CODEX VENTED! / I WAS IN ELECTRICAL. Close-up: Codex sweating behind his
visor. The votes pile up on Codex; he tumbles out into space — CODEX WAS THE IMPOSTOR. VICTORY.
A new round: the lights come back, Codex climbs out of the vent and everybody walks back."""
from engine import *

THEME = 'amongus'
N_ = 390
CX, KX = 30, 150           # Claude, Codex in the neutral pose
PANEL_X = 22               # where Claude stands to fix the wiring
TABLE = 92                 # the table with the emergency button
VENT = 126
BODY_X, FIND_X = 112, 98   # the body, where Claude stops when he finds it
TASKS0, TASKS1 = 0.3, 0.45 # the task bar before / after the wiring

# ---- crewmates -----------------------------------------------------------------------------------
# '1' body, '2' backpack, '3'/'4' visor + shine, '5'/'6' Codex's dark visor + ">_", '7' bone / hat,
# '8' the cut. Facing right.
_BODY = [
"....111111...",
"...11111111..",
"...111111111.",
".22111333333.",
".221133444433",
".221133333333",
".22111333333.",
".22111111111.",
".22111111111.",
".22111111111.",
"...111111111.",
"...111111111."]
_KVISOR = {3:".22111655555.", 4:".221155655555", 5:".221156555555", 6:".22111555666."}
_KBODY = [_KVISOR.get(i, r) for i, r in enumerate(_BODY)]
_HAT = ["....7.7.7....", ".....777.....", "....7.7.7...."]
_LEGS = {'idle':["...1111.1111.", "...111...111."],
         'walk1':["...1111..111.", "..111.....111"],
         'walk2':["...111111111.", "....111.111.."]}
_DEAD = [".....7.7.....", "......7......", "......7......", "...88888888.."]+_BODY[7:]+_LEGS['idle']

def _crew(body, hat=()): return {k: S(list(hat)+body+legs) for k, legs in _LEGS.items()}
CLAUDE = _crew(_BODY, _HAT)
CODEX = _crew(_KBODY)
PLAIN = _crew(_BODY)
DEAD = S(_DEAD)

def cpal(body, shade):
    return {'1':body, '2':shade, '3':(150,200,222), '4':(232,246,252), '5':(20,22,28),
            '6':(240,240,245), '7':(245,235,220), '8':(200,50,60)}
CLPAL = cpal((217,119,87), (168,80,54))
KPAL = cpal((222,226,236), (150,158,178))
GPAL = cpal((40,160,60), (20,100,40))
YPAL = cpal((240,220,60), (190,150,30))
PPAL = cpal((240,110,190), (180,60,140))
CPAL = cpal((60,226,220), (30,158,170))

def sprite_img(spr, pal, scale=1):
    """The sprite (with the same 1px dark outline core.draw gives it) as an RGBA image, for the
    cards that scale or rotate it."""
    m, w, h = mask_of(spr, False)
    im = Image.new('RGBA', (w+2, h+2), (0,0,0,0)); px = im.load()
    for x, y in dilate(set(m), 1): px[x+1, y+1] = OUT+(255,)
    for (x, y), ch in m.items(): px[x+1, y+1] = pal[ch]+(255,)
    return im.resize((im.width*scale, im.height*scale), Image.NEAREST) if scale > 1 else im

def paste_feet(im, spr_im, cx, feet):
    im.paste(spr_im, (int(cx-spr_im.width/2), int(feet-spr_im.height)), spr_im)

def walk(f): return 'walk1' if (f//3) % 2 else 'walk2'

# ---- background: the cafeteria of The Skeld ------------------------------------------------------
def _skeld(d):
    d.rectangle([0, 0, W, 40], fill=(46,54,74))
    d.rectangle([0, 0, W, 3], fill=(30,34,48))
    d.rectangle([0, 13, W, 15], fill=(70,80,104)); d.line([0, 13, W, 13], fill=(92,102,128))
    for x0 in range(0, W, 23): d.line([x0, 4, x0, 38], fill=(36,42,60)); d.line([x0+1, 4, x0+1, 38], fill=(58,66,88))
    d.rectangle([0, 38, W, 40], fill=(30,34,46))
    for y0 in range(41, GROUND+1, 6):                                   # floor tiles
        for x0 in range(0, W, 8):
            d.rectangle([x0, y0, x0+7, min(GROUND, y0+5)], fill=(86,96,116) if (x0//8+y0//6) % 2 else (78,88,108))
    # the wiring panel on the left wall
    d.rectangle([4, 18, 17, 34], fill=(210,180,40), outline=(120,100,20))
    d.rectangle([6, 20, 15, 32], fill=(40,40,44))
    for i, c in enumerate(((200,40,40), (50,90,220), (240,220,40), (240,100,200))):
        d.line([7, 22+i*3, 14, 22+((i*3+2) % 4)*3], fill=c)
    # the table with the emergency button
    d.rectangle([TABLE-3, 46, TABLE+3, GROUND], fill=(90,96,110)); d.line([TABLE-3, 46, TABLE-3, GROUND], fill=(120,128,144))
    d.ellipse([TABLE-24, 42, TABLE+24, 49], fill=(150,158,176), outline=(100,108,124))
    d.rectangle([TABLE-6, 41, TABLE+6, 44], fill=(60,60,70))
    d.ellipse([TABLE-5, 34, TABLE+5, 44], fill=(170,204,226), outline=(110,140,160))
    d.ellipse([TABLE-3, 38, TABLE+3, 43], fill=(220,30,30)); d.point((TABLE-1, 39), fill=(255,150,150))
    # benches
    for bx in (TABLE-34, TABLE+26): d.rectangle([bx, 51, bx+8, 53], fill=(110,118,134)); d.line([bx+4, 53, bx+4, GROUND], fill=(70,76,90))
register_bg(THEME, lambda v: (v, v+4, v+12), decor=_skeld, clip_ground=True)

@fx('au_vent')
def _fx_vent(d, im, e, f):
    """The floor vent at x, its lid opened to k (0..1)."""
    _, x, k = e
    d.rectangle([x-9, GROUND-2, x+9, GROUND], fill=(24,26,32))
    if k <= 0:
        d.rectangle([x-8, GROUND-2, x+8, GROUND], fill=(56,60,72))
        for i in range(x-7, x+8, 2): d.line([i, GROUND-2, i, GROUND], fill=(100,106,120))
    else:
        d.rectangle([x-8, GROUND-2, x+8, GROUND], fill=(8,8,12))
        h = int(9*k); d.rectangle([x-10, GROUND-2-h, x-8, GROUND-1], fill=(100,106,120), outline=(24,26,32))

@fx('au_dark')
def _fx_dark(d, im, e, f):
    """Lights sabotaged: everything outside Claude's circle of vision goes dark (k 0..1)."""
    _, cx, cy, k = e
    if k <= 0: return
    m = Image.new('L', (W, H), int(235*k)); r = 30
    ImageDraw.Draw(m).ellipse([cx-r, cy-r*0.8, cx+r, cy+r*0.8], fill=0)
    im.paste(Image.composite(Image.new('RGB', (W, H), (0,0,0)), im, m.filter(ImageFilter.GaussianBlur(4))))

@fx('au_tasks')
def _fx_tasks(d, im, e, f):
    """The TOTAL TASKS COMPLETED bar in the top left corner."""
    _, v = e
    d.rectangle([2, 2, 62, 6], fill=(40,46,40), outline=(0,0,0))
    if v > 0: d.rectangle([3, 3, 3+int(58*v), 5], fill=(68,210,68))

# ---- close-up: fix wiring ------------------------------------------------------------------------
WIRES = [(200,40,40), (50,90,220), (240,220,40), (240,100,200)]
_WTO = [2, 3, 0, 1]        # wire i (left) plugs into right socket _WTO[i]

def closeup_wires(fr, f):
    im = Image.new('RGB', (W, H), (30,30,34)); d = ImageDraw.Draw(im)
    d.rectangle([18, 1, 166, 62], fill=(58,56,52), outline=(200,170,40), width=2)
    ys = [10, 23, 36, 49]
    for i, c in enumerate(WIRES):
        d.rectangle([22, ys[i]-2, 34, ys[i]+2], fill=c, outline=(0,0,0))
        d.rectangle([150, ys[_WTO.index(i)]-2, 162, ys[_WTO.index(i)]+2], fill=c, outline=(0,0,0))
    for i, c in enumerate(WIRES):
        p = ease((fr-4-i*7)/5)
        if p <= 0: continue
        y0, y1 = ys[i], ys[_WTO[i]]
        x, y = lerp(34, 150, p), lerp(y0, y1, p)
        d.line([34, y0+1, x, y+1], fill=tuple(v//2 for v in c), width=3); d.line([34, y0, x, y], fill=c, width=3)
        if p < 1: d.ellipse([x-2, y-2, x+2, y+2], fill=c, outline=(0,0,0))
        d.rectangle([163, y1-1, 165, y1+1], fill=(60,230,60) if p >= 1 else (40,60,40))
    if fr < 3: zoom_lines(d, (240,220,120))
    if fr >= 31: big_text(im, "TASK COMPLETE!", 26, (255,255,255), outline=(20,120,20))
    return im

# ---- card: dead body reported --------------------------------------------------------------------
def card_report(fr, f):
    im = Image.new('RGB', (W, H), (70,6,8)); d = ImageDraw.Draw(im)
    for i in range(24):
        a = i*0.2618+fr*0.03; c = (130,20,20) if i % 2 else (90,8,10)
        d.polygon([(44,34), (44+math.cos(a)*240, 34+math.sin(a)*240), (44+math.cos(a+0.13)*240, 34+math.sin(a+0.13)*240)], fill=c)
    k = ease(fr/5); sc = 3
    body = sprite_img(DEAD, GPAL, sc)
    j = ((f % 3)-1) if fr < 10 else 0
    body = body.resize((max(1, int(body.width*k)), max(1, int(body.height*k))), Image.NEAREST)
    paste_feet(im, body, 44+j, 34+body.height//2)
    if fr >= 4:
        big_text(im, "DEAD BODY", 14, (255,255,255), cx=128+j, outline=(0,0,0))
        big_text(im, "REPORTED", 32, (255,255,255), cx=128+j, outline=(0,0,0))
    if fr < 3: im = fade_to(im, (255,255,255), 1-fr/3)
    return im

# ---- the meeting ---------------------------------------------------------------------------------
PLAYERS = [('CLAUDE', _BODY, CLPAL), ('CODEX', _KBODY, KPAL), ('GREEN', _BODY, GPAL),
           ('YELLOW', _BODY, YPAL), ('PINK', _BODY, PPAL), ('CYAN', _BODY, CPAL)]
ICONS_ = {n: sprite_img(S(b[:8]), p) for n, b, p in PLAYERS}
VOTERS = ['CLAUDE', 'YELLOW', 'PINK', 'CYAN']          # all on Codex; Codex votes Claude

def _card(i):
    return 5+(i % 3)*59, 11+(i//3)*18

def meeting(fr, f, bubble=None, voted=0, dots=0, results=False):
    """The voting tablet: six player cards, an optional chat bubble (speaker, text, age), the I VOTED
    stickers of the first `voted` voters and the first `dots` vote chips on the cards."""
    im = Image.new('RGB', (W, H), (26,30,40)); d = ImageDraw.Draw(im)
    d.rectangle([1, 0, 183, 63], fill=(170,186,204), outline=(60,70,84), width=2)
    title = "VOTING RESULTS" if results else "WHO IS THE IMPOSTOR?"
    text(d, title, W//2-len(title)*2, 3, (30,36,50), shadow=(230,236,244))
    for i, (name, _, pal) in enumerate(PLAYERS):
        x0, y0 = _card(i); dead = name == 'GREEN'
        hot = results and name == 'CODEX' and (fr//2) % 2
        d.rectangle([x0, y0, x0+55, y0+15], fill=(120,126,138) if dead else (236,240,246),
                    outline=(220,40,40) if hot else (70,78,92))
        ic = ICONS_[name]; im.paste(ic, (x0+2, y0+3), ic)
        if dead:
            d.line([x0+3, y0+4, x0+14, y0+13], fill=(220,30,30), width=2); d.line([x0+14, y0+4, x0+3, y0+13], fill=(220,30,30), width=2)
        text(d, name, x0+18, y0+3, (60,64,74) if dead else (24,26,34), shadow=None)
        voters = VOTERS[:voted]+(['CODEX'] if voted >= len(VOTERS) else [])
        if name in voters:
            d.rectangle([x0+46, y0+2, x0+53, y0+7], fill=(220,60,60), outline=(120,20,20)); d.point((x0+49, y0+4), fill=(255,255,255))
    chips = [('CODEX', v) for v in VOTERS]+[('CLAUDE', 'CODEX')]
    for k, (target, voter) in enumerate(chips[:dots]):
        x0, y0 = _card([p[0] for p in PLAYERS].index(target))
        n = sum(1 for t, _ in chips[:k] if t == target)
        pal = dict((p[0], p[2]) for p in PLAYERS)[voter]
        cx = x0+18+n*7
        d.rectangle([cx, y0+10, cx+4, y0+13], fill=pal['1'], outline=(0,0,0)); d.point((cx+3, y0+11), fill=pal['3'])
    if bubble:
        who, msg, age = bubble; dy = max(0, 4-age)
        d.rectangle([12, 47+dy, 172, 61+dy], fill=(248,248,252), outline=(40,44,56))
        ic = ICONS_[who]; im.paste(ic, (15, 49+dy), ic)
        pal = dict((p[0], p[2]) for p in PLAYERS)[who]
        text(d, who+":", 31, 52+dy, tuple(v//2 for v in pal['1']), shadow=None)
        text(d, msg, 31+len(who)*4+6, 52+dy, (24,26,34), shadow=None)
    return im

# ---- close-up: Codex sweating --------------------------------------------------------------------
def closeup_sweat(fr, f):
    im = Image.new('RGB', (W, H), (40,50,84)); d = ImageDraw.Draw(im)
    for i in range(16):
        a = i*0.3927; d.line([150, 32, 150+math.cos(a)*200, 32+math.sin(a)*200], fill=(48,60,98))
    j = (f % 2)*2-1 if fr >= 6 else 0
    ox = 10+j
    d.ellipse([ox, 6, ox+120, 130], fill=(0,0,0)); d.ellipse([ox+3, 9, ox+117, 127], fill=KPAL['1'])
    d.ellipse([ox+3, 30, ox+40, 127], fill=KPAL['2'])
    d.rounded_rectangle([ox+54, 16, ox+132, 48], 14, fill=(0,0,0)); d.rounded_rectangle([ox+57, 19, ox+129, 45], 12, fill=KPAL['5'])
    d.line([ox+74, 24, ox+84, 32, ox+74, 40], fill=KPAL['6'], width=3)
    if (fr//3) % 2: d.line([ox+90, 40, ox+106, 40], fill=KPAL['6'], width=3)
    for k, (sx, t0) in enumerate(((ox+50, 2), (ox+46, 9), (ox+134, 5))):
        if fr < t0: continue
        y = 14+(fr-t0)*2.5
        d.polygon([(sx, y-4), (sx-2, y), (sx+2, y)], fill=(150,210,255)); d.ellipse([sx-2, y-2, sx+2, y+2], fill=(150,210,255))
        d.point((sx-1, y-1), fill=(255,255,255))
    if fr >= 8: big_text(im, "GULP", 26, (255,255,255), cx=160, outline=(20,30,70))
    if fr < 3: zoom_lines(d, (180,200,255))
    return im

# ---- the ejection --------------------------------------------------------------------------------
_STARS = [(random.Random(5+i).randint(0, W), random.Random(50+i).randint(0, H-1), 0.5+(i % 3)*0.8) for i in range(46)]

def card_eject(fr, f):
    im = Image.new('RGB', (W, H), (0,0,4)); d = ImageDraw.Draw(im)
    for x, y, v in _STARS:
        c = (255,255,255) if v > 2 else ((170,170,200) if v > 1 else (90,90,120))
        d.point(((x-fr*v) % W, y), fill=c)
    t = fr/44
    if t <= 1:
        sp = sprite_img(CODEX['idle'], KPAL).rotate(-fr*19, resample=Image.NEAREST, expand=True)
        x, y = lerp(-16, W+16, t), 34+6*math.sin(t*3)
        im.paste(sp, (int(x-sp.width/2), int(y-sp.height/2)), sp)
    l1, l2 = "CODEX WAS", "THE IMPOSTOR."
    n = max(0, fr-10)
    if n: big_text(im, l1[:n], 17, (255,255,255))
    if n > len(l1): big_text(im, l2[:n-len(l1)], 31, (255,255,255))
    if fr >= 36:
        s = "0 IMPOSTORS REMAIN"; text(d, s, W//2-len(s)*2, 50, (200,200,210))
    if fr >= 46: im = fade_to(im, (0,0,0), (fr-45)/5)
    return im

# ---- the victory screen --------------------------------------------------------------------------
def card_victory(fr, f):
    im = Image.new('RGB', (W, H), (0,0,0)); d = ImageDraw.Draw(im)
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse([40, 30, 145, 90], fill=120)
    im.paste((40,90,200), (0, 0), g.filter(ImageFilter.GaussianBlur(10)))
    big_text(im, "VICTORY", 3, (70,150,255), scale=3, outline=(10,30,90))
    k = ease(fr/6)
    for x, pal in ((44, YPAL), (64, CPAL), (122, PPAL), (142, GPAL)):
        sp = sprite_img(PLAIN['idle'], pal)
        if pal is GPAL:                                                # the ghost: see-through
            sp.putalpha(sp.getchannel('A').point(lambda a: a*100//255))
        paste_feet(im, sp, x, 62+int((1-k)*10))
    paste_feet(im, sprite_img(CLAUDE['idle'], CLPAL, 2), 93, 63+int((1-k)*20))
    if fr < 3: im = fade_to(im, (0,0,0), 1-fr/3)
    if fr >= 26: im = fade_to(im, (0,0,0), (fr-25)/5)
    return im

# ---- the clip ------------------------------------------------------------------------------------
def clip_impostor(f):
    s = scene(f, THEME)
    if 20 <= f < 56: s['image'] = closeup_wires(f-20, f); return s
    if 138 <= f < 168: s['image'] = card_report(f-138, f); return s
    if 168 <= f < 218:
        fr = f-168
        b = ('CLAUDE', "CODEX VENTED!", fr-4) if 4 <= fr < 26 else (('CODEX', "I WAS IN ELECTRICAL", fr-28) if fr >= 28 else None)
        s['image'] = meeting(fr, f, bubble=b); return s
    if 218 <= f < 238: s['image'] = closeup_sweat(f-218, f); return s
    if 238 <= f < 266:
        fr = f-238
        s['image'] = meeting(fr, f, voted=min(5, fr//2), dots=max(0, min(5, (fr-12)//2)), results=fr >= 18); return s
    if 266 <= f < 316: s['image'] = card_eject(f-266, f); return s
    if 316 <= f < 346: s['image'] = card_victory(f-316, f); return s
    # --- the cafeteria: state defaults = the neutral pose ---
    cx, cpose, cflip, cy = CX, 'idle', False, GROUND
    kx, kpose, kflip, ky = KX, 'idle', True, GROUND
    vent, dark, tasks, body = 0.0, 0.0, TASKS0, False
    # 1) to the wiring panel; the task bar after it
    if 8 <= f < 20: cx = ez(CX, PANEL_X, (f-8)/12); cpose = walk(f); cflip = True
    if 56 <= f < 346:
        tasks = lerp(TASKS0, TASKS1, (f-56)/6)
        cx, cflip = PANEL_X, f < 80
    # 2) Codex walks to the vent and hops in; Claude turns round — ?!
    if 58 <= f < 346: kx = VENT if f >= 74 else ez(KX, VENT, (f-58)/16); kpose = walk(f) if f < 74 else 'idle'
    if 72 <= f < 92: vent = ease((f-72)/3) if f < 88 else 1-ease((f-88)/3)
    if 74 <= f < 78: ky = GROUND-[2, 4, 4, 2][f-74]
    if 78 <= f < 346: ky = min(GROUND+18, GROUND+(f-78)*2.2)
    if 80 <= f < 100: s['fx'].append(('big', "?!", 28, (255,230,90), cx))
    # 3) the lights go out; Claude runs to the body
    if 100 <= f < 346:
        dark = ease((f-100)/6); body = True
        if (f//6) % 2: s['fx'].append(('dmg', "FIX LIGHTS", 3, 9, (240,60,60)))
    if 104 <= f < 346:
        cx = ez(PANEL_X, FIND_X, (f-104)/28); cflip = False; cpose = walk(f) if f < 132 else 'idle'
    if 132 <= f < 138: s['fx'].append(('big', "!", 28, (255,80,60), cx))
    if 132 <= f < 135: s['flash'] = 0.35; s['fc'] = (BODY_X, GROUND-6); s['flashc'] = (255,120,110)
    # 4) a new round: Codex climbs out of the vent, everybody walks back
    if f >= 346:
        cx = ez(FIND_X, CX, (f-350)/30); cflip = f < 380; cpose = walk(f) if 350 <= f < 380 else 'idle'
        kx, kflip = VENT, False
        if 352 <= f < 366: vent = ease((f-352)/3) if f < 362 else 1-ease((f-362)/3)
        if f < 356: ky = GROUND+18
        elif f < 362: ky = GROUND-[6, 7, 6, 4, 2, 1][f-356]
        if f >= 364: kx = ez(VENT, KX, (f-364)/14); kpose = walk(f) if f < 378 else 'idle'; kflip = f >= 378
    if cpose != 'idle' and (f//3) % 2: cy = GROUND-1
    s['under'].append(('au_vent', VENT, vent))
    if body: s['actors'].append(actor(DEAD, BODY_X, GROUND, pal=GPAL))
    s['actors'].append(actor(CODEX[kpose], kx, int(ky), flip=kflip, pal=KPAL))
    s['actors'].append(actor(CLAUDE[cpose], cx, cy, flip=cflip, pal=CLPAL))
    if dark > 0: s['fx'].insert(0, ('au_dark', int(cx), GROUND-8, dark))
    s['fx'].append(('au_tasks', tasks))
    if 346 <= f < 350: s['fx'].append(('dim', 1-(f-346)/4))
    return s

CLIPS = [clip('impostor', N_, clip_impostor)]
