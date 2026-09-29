"""Star Wars: Claude (a hooded Jedi, green saber) vs Darth Vader on a dark Death Star gantry.
Sabers humming, a clash exchange, the Force choke, Claude's Force push, Vader's thrown saber
deflected — then the close-up of the helmet: "CLAUDE... I AM YOUR FATHER." and a cut to Claude's
"NOOOO!". An enraged flurry sends Vader's saber flying (sparks at the wrist, bloodless); Vader
pulls it back with the Force, re-ignites it and both return to guard for the loop."""
from engine import *

THEME = 'sw'
N_ = 288

# --- sprites -------------------------------------------------------------------------------
JEDI_PAL = {'5': (86, 54, 32), '6': (150, 104, 64)}   # hood, robe highlight

def _jedi(x, y, t, l, r, c):
    inside = l <= x <= r
    if c == '.':
        if x == l - 1 and t <= y <= t + 4: return '5'   # hood drapes down the side of the head
        return None
    if inside and y == t: return '5'                       # hood over the forehead
    if inside and y in (t + 5, t + 6): return 'q'          # robe
    if inside and y == t + 7: return 'k'                   # belt
    if inside and y == t + 8: return '6'                   # tunic
    return None
JEDI = variant(lambda s: recolor_rows(overlay(s, ["..555555..", ".55555555."], -1, 0), _jedi))

# Vader faces right here (flip=True puts him on the right facing left). Hand/hilt at (16,12).
_VADER = [
"....111111........",
"...12222211.......",
"..1222221111......",
"..2111111112......",
"..1ZZ1111ZZ1......",
"..1Z31111Z31......",
"..1111dd1111......",
".111.1dd1.111.....",
".11.1dddd1.11.....",
"11..11dd11..11....",
".cc4111111114cc...",
"cc441111111144cc..",
"cc41178911111111DD",
"cc41111111111111DD",
"cc4111111111114c..",
"cc41dddddddd14cc..",
"cc4111111111114c..",
"ccc411111111114cc.",
"cccc111....111ccc.",
"cccc111....111cccc",
"ccc1111....1111ccc",
"cc11111....11111cc",
]
VADER = poses(S(_VADER), 12, '11', 0)
VADER_CUT = S([r[:14] + '..' + r[16:] if i in (12, 13) else r for i, r in enumerate(_VADER)])
VADER_CUT = S([r[:16] + '..' if i in (12, 13) else r for i, r in enumerate(VADER_CUT)])
V_HAND = (16, 12)
C_HAND = {'guard': (13, 4), 'guard2': (13, 5), 'punch': (16, 5), 'dash': (16, 5),
          'charge': (15, 5), 'armsup': (12, 0), 'hurt': (15, 1)}

def vader_pal(f):
    blink = (f // 5) % 3
    return {'1': (52, 52, 68), '2': (118, 118, 142), 'Z': (14, 12, 16), '3': (150, 150, 170),
            'c': (34, 30, 44), '4': (78, 74, 98),
            '7': (230, 40, 40) if blink != 1 else (90, 20, 20),
            '8': (60, 220, 90) if blink != 2 else (20, 80, 30),
            '9': (80, 150, 255) if blink != 0 else (30, 50, 100)}

GREEN = ((40, 170, 60), (190, 255, 190))
RED = ((200, 30, 24), (255, 200, 190))

def hand_at(spr, cx, feet, flip, hx, hy, h=None):
    """World position of sprite cell (hx,hy); h = the pose's original height (Claude's hood
    overlay pads rows on top, so y is measured from the feet)."""
    w = len(spr[0]); h = h or len(spr); ox = int(round(cx - w / 2))
    return (ox + (w - 1 - hx) if flip else ox + hx), feet - h + hy

def cl_hand(pose, x, y=GROUND):
    return hand_at(JEDI[pose], x, y, False, *C_HAND[pose], h=11)

def vd_hand(x, y=GROUND):
    return hand_at(VADER['idle'], x, y, True, *V_HAND)

# --- background ----------------------------------------------------------------------------
def _gantry(d):
    rr = random.Random(1977)
    for _ in range(26):
        x, y = rr.randint(0, W - 1), rr.randint(0, 40); v = rr.randint(40, 110)
        d.point((x, y), fill=(v, v, v + 12))
    d.ellipse([88, 6, 104, 22], fill=(26, 26, 32)); d.ellipse([92, 10, 97, 15], outline=(40, 40, 50))
    d.line([88, 14, 104, 14], fill=(18, 18, 22))
    for x in (8, 60, 124, 176):                          # gantry struts, barely lit
        d.line([x, 30, x, GROUND], fill=(20, 22, 32)); d.line([x - 3, 30, x + 3, 30], fill=(30, 34, 48))
    d.line([0, GROUND + 3, W, GROUND + 3], fill=(16, 18, 28))
register_bg(THEME, lambda v: (v // 2, v // 2 + 2, v + 6), decor=_gantry)

# --- effects -------------------------------------------------------------------------------
def _seg(x, y, ang, L):
    a = math.radians(ang); return x, y, x + math.cos(a) * L, y + math.sin(a) * L

@fx('sw_saber')
def _fx_saber(d, im, e, f):
    """A lightsaber from the hilt (x,y) at angle ang (degrees, 0=right, -90=up), length L."""
    _, x, y, ang, L, (glow, core) = e
    if L <= 0: return
    L = L + ((f * 7) % 3 - 1) * 0.6                        # hum
    x0, y0, x1, y1 = _seg(x, y, ang, L)
    d.line([x0, y0, x1, y1], fill=glow, width=3)
    d.line([x0, y0, x1, y1], fill=core, width=1)
    hx, hy = _seg(x, y, ang + 180, 3)[2:]
    d.line([x, y, hx, hy], fill=(170, 170, 184), width=1)

@fx('sw_spin')
def _fx_spin(d, im, e, f):
    """A thrown saber spinning around its hilt, with a faint motion ring."""
    _, x, y, ang, (glow, core) = e
    d.arc([x - 11, y - 11, x + 11, y + 11], 0, 360, fill=(70, 12, 12))
    for a0 in (ang, ang + 180):
        x0, y0, x1, y1 = _seg(x, y, a0, 11)
        d.line([x0, y0, x1, y1], fill=glow, width=3); d.line([x0, y0, x1, y1], fill=core)
    d.point((int(x), int(y)), fill=(180, 180, 190))

@fx('sw_hilt')
def _fx_hilt(d, im, e, f):
    _, x, y = e; d.line([x - 2, y, x + 2, y], fill=(170, 170, 184)); d.point((x + 2, y), fill=(60, 60, 70))

@fx('sw_push')
def _fx_push(d, im, e, f):
    """Force push: concentric pale arcs travelling right from (x,y), progress p 0..1."""
    _, x, y, p = e
    for k in range(3):
        r = int(6 + (p * 90) - k * 10)
        if r <= 2: continue
        c = int(150 - k * 40)
        d.arc([x - r, y - r, x + r, y + r], -40, 40, fill=(c, c + 20, c + 60))

@fx('sw_choke')
def _fx_choke(d, im, e, f):
    """Invisible grip: dark-red pulses closing around the throat at (x,y) + a thin link to the hand."""
    _, x, y, hx, hy = e
    r = 3 + (f % 3)
    d.arc([x - r, y - r // 2, x + r, y + r // 2], 0, 360, fill=(150, 20, 20))
    for k in range(0, 100, 12):
        t = (k + f * 4) % 100 / 100
        d.point((int(lerp(hx, x, t)), int(lerp(hy, y, t) - math.sin(t * math.pi) * 5)), fill=(120, 20, 20))

def seg_cross(a, b):
    """Intersection point of two segments (x0,y0,x1,y1), or None."""
    x1, y1, x2, y2 = a; x3, y3, x4, y4 = b
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-6: return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
    if 0 <= t <= 1 and 0 <= u <= 1: return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
    return None

# --- close-ups -----------------------------------------------------------------------------
def _zoomlines(d, t):
    if t < 0.06:
        for i in range(10): a = i * 0.63; d.line([W // 2, H // 2, W // 2 + math.cos(a) * 120, H // 2 + math.sin(a) * 60], fill=(255, 255, 255))

def closeup_vader(t, f):
    """Primer plano: the helmet fills the left of the frame, breathing; the line on the right."""
    im = Image.new('RGB', (W, H), (4, 4, 8)); d = ImageDraw.Draw(im)
    by = int(round(math.sin(t * math.pi * 4) * 1))          # the breath lifts the helmet
    hl, body, dark, lens = (112, 112, 136), (44, 44, 58), (24, 24, 32), (10, 8, 12)
    d.polygon([(12, 28 + by), (2, 64), (98, 64), (88, 28 + by)], fill=dark, outline=(70, 70, 90))   # flare
    d.ellipse([16, -22 + by, 84, 38 + by], fill=body)
    d.arc([20, -18 + by, 80, 34 + by], 200, 260, fill=hl, width=2)                                 # dome shine
    d.line([18, 24 + by, 82, 24 + by], fill=hl)                                                   # brow
    d.polygon([(22, 25 + by), (78, 25 + by), (80, 44 + by), (66, 54 + by), (34, 54 + by), (20, 44 + by)], fill=body)
    for sgn in (-1, 1):                                                                            # lenses
        pts = [(50 + sgn * 4, 29 + by), (50 + sgn * 22, 27 + by), (50 + sgn * 20, 38 + by), (50 + sgn * 6, 37 + by)]
        d.polygon(pts, fill=lens)
        gl = (150, 150, 170) if not (0.62 <= t) else (220, 60, 50)                               # the glint turns red
        d.line([50 + sgn * 18, 29 + by, 50 + sgn * 14, 29 + by], fill=gl)
    d.polygon([(50, 30 + by), (46, 42 + by), (54, 42 + by)], fill=(64, 64, 82))                   # nose
    d.polygon([(50, 43 + by), (36, 62 + by), (64, 62 + by)], fill=(18, 18, 24), outline=(90, 90, 110))   # grill
    for k in range(-3, 4): d.line([50 + k * 3, 48 + by, 50 + k * 4, 60 + by], fill=(90, 90, 110))
    for sgn in (-1, 1): d.polygon([(50 + sgn * 30, 44 + by), (50 + sgn * 46, 64), (50 + sgn * 30, 64), (50 + sgn * 16, 54 + by)], fill=dark, outline=(70, 70, 90))
    big = FX['big']
    breath = (t * 4) % 1                                   # KSSHH on the in-breath, KOOOH on the out
    if t < 0.3:
        big(d, im, ('big', "KSSHH..." if breath < 0.5 else "KOOOH...", 26, (150, 150, 170), 140), f)
        if breath >= 0.5:
            rr = random.Random(f)
            for _ in range(6): d.point((50 + rr.randint(-8, 8), 58 + rr.randint(-2, 4)), fill=(90, 90, 104))
    else:
        big(d, im, ('big', "CLAUDE...", 6, (220, 220, 232), 140), f)
        if t >= 0.5: big(d, im, ('big', "I AM YOUR", 26, (230, 60, 50), 140), f)
        if t >= 0.66: big(d, im, ('big', "FATHER.", 46, (230, 60, 50), 140), f)
    _zoomlines(d, t)
    return im

def closeup_no(t, f):
    """Cut to Claude: eyes squeezed shut, mouth wide open, hood around the face."""
    im = Image.new('RGB', (W, H), (4, 4, 8)); d = ImageDraw.Draw(im)
    sx, sy = rshake(1) if t > 0.1 else (0, 0)
    ox = 14 + sx
    d.rectangle([ox, 0 + sy, ox + 76, 64], fill=(86, 54, 32))                     # hood
    d.rectangle([ox + 8, 10 + sy, ox + 68, 64], fill=(217, 119, 87))               # face
    d.rectangle([ox + 8, 10 + sy, ox + 68, 13 + sy], fill=(86, 54, 32))
    for ex in (ox + 24, ox + 52):                                                  # > <  shut eyes
        d.line([ex - 6, 20 + sy, ex + 4, 25 + sy], fill=(24, 14, 12), width=2)
        d.line([ex - 6, 30 + sy, ex + 4, 25 + sy], fill=(24, 14, 12), width=2)
    d.ellipse([ox + 28, 36 + sy, ox + 48, 60 + sy], fill=(24, 14, 12))              # the scream
    d.ellipse([ox + 33, 50 + sy, ox + 43, 58 + sy], fill=(168, 80, 54))
    FX['big'](d, im, ('big', "NOOOO!", 26 + sy, (255, 226, 90), 140 + sx), f)
    _zoomlines(d, t)
    return im

# --- clip ----------------------------------------------------------------------------------
def clip_father(f):
    s = scene(f, THEME)
    cx, cpose, cy = 30, guard_pose(f), GROUND
    vx, vy, vspr = 150, GROUND, VADER['idle']
    c_ang, c_len = -55, 15           # Claude's blade: up and forward
    v_ang, v_len = -125, 16          # Vader's blade, mirrored
    cl_saber, vd_saber = True, True
    spin = None                      # (x,y,ang) of a thrown saber
    c_aura = None

    # 1) neutral — both sabers humming (0-24)
    # 2) they close in (24-40) and clash (40-72)
    if 24 <= f < 40:
        t = (f - 24) / 16; cx = ez(30, 76, t); vx = ez(150, 110, t)
        cpose = 'dash' if f < 34 else guard_pose(f)
    if 40 <= f < 72:
        cx, vx = 76, 110; k, ph = (f - 40) // 8, (f - 40) % 8
        hi = k % 2 == 0                                    # alternate high and low exchanges
        sw = ease(min(1, ph / 3))
        c_ang = lerp(-80 if hi else -10, -40 if hi else -25, sw)
        v_ang = lerp(-100 if hi else -170, -140 if hi else -155, sw)
        cpose = 'punch' if ph >= 2 else 'guard'
        if k == 3: cx = 76 - (ph if ph > 3 else 0)       # the last clash pushes Claude back
    if 70 <= f < 76: cx = ez(72, 60, (f - 70) / 6)

    # 3) Force choke (76-102)
    if 76 <= f < 102:
        t = (f - 76) / 26
        cx = 60; vx = 110; cl_saber = False
        vspr = VADER['attack']; v_ang, v_len = 135, 11    # blade lowered, the other hand grips
        cpose = 'hurt'; cy = GROUND - int(ez(0, 10, t / 0.4)) + (f % 2)
        callout(s, "I FIND YOUR LACK OF FAITH DISTURBING", y=2, c=(230, 60, 50))
    # 4) Force push (102-118)
    if 102 <= f < 118:
        t = (f - 102) / 16; cx = 60; cl_saber = False
        cy = GROUND - int(ez(10, 0, t / 0.3))
        cpose = 'armsup' if f < 106 else 'punch'
        if f >= 106:
            s['fx'].append(('sw_push', 72, GROUND - 8, (f - 106) / 12))
            vspr = VADER['hurt']; vx = ez(110, 150, (f - 106) / 10); v_ang = -60
            if f == 108: s['shake'] = rshake(2)
    # 5) Vader throws his saber; Claude re-ignites and deflects (118-140)
    if 118 <= f < 140:
        cx, vx = 60, 150
        c_len = ez(0, 15, (f - 118) / 4)
        vd_saber = False
        if f < 124: vspr = VADER['attack']
        t = (f - 118) / 22
        if t < 0.5: sx = lerp(138, 74, t / 0.5)
        else: sx = lerp(74, 138, (t - 0.5) / 0.5)
        sy = GROUND - 14 - math.sin(t * math.pi) * 8
        spin = (sx, sy, f * 47)
        if 128 <= f < 132:
            cpose = 'punch'; c_ang = -20
            if f in (128, 129): s['fx'].append(('spark', 76, GROUND - 14, 5)); s['shake'] = rshake()
    if 138 <= f < 140: vspr = VADER['attack']

    # 6) close-up: "I AM YOUR FATHER." (140-184) — cut to Claude "NOOOO!" (184-200)
    if 140 <= f < 184: s['image'] = closeup_vader((f - 140) / 44, f); return s
    if 184 <= f < 200: s['image'] = closeup_no((f - 184) / 16, f); return s

    # 7) enraged flurry, Vader disarmed (200-240)
    if 200 <= f < 240:
        c_aura = ((60, 200, 90), 1)
        vx = ez(150, 116, (f - 200) / 6)
    if 200 <= f < 206: cx = ez(60, 88, (f - 200) / 6); cpose = 'dash'
    if 206 <= f < 226:
        k, ph = (f - 206) // 5, (f - 206) % 5
        cx = 88 + k * 2; vx = 116 + k * 3
        c_ang = [-80, -10, -70, 0][k] + ph * ([25, -25, 25, -25][k])
        v_ang = [-110, -175, -120, -175][k]
        cpose = 'punch' if ph >= 1 else 'dash'
        if ph == 2:
            p = seg_cross(_seg(*cl_hand(cpose, cx, cy), c_ang, 15), _seg(*vd_hand(vx), v_ang, 16))
            if p: s['fx'].append(('spark', int(p[0]), int(p[1]), 4)); s['shake'] = rshake()
    if 226 <= f < 240:                                     # the saber hand is struck: sparks, saber flies
        cx = 94; cpose = 'punch'; c_ang = ez(-80, 10, (f - 226) / 3)
        vd_saber = False; vspr = VADER_CUT if f < 230 else hurt(VADER_CUT)
        vx = ez(125, 142, (f - 226) / 12)
        hx, hy = vd_hand(vx)
        if f < 234: s['fx'].append(('spark', hx - 1, hy, 5 - (f - 226) // 2))
        if f == 226: s['shake'] = rshake(2); s['flash'] = 0.5; s['fc'] = (hx, hy); s['flashc'] = (255, 190, 170)
        t = (f - 226) / 14
        spin = (lerp(hx, 176, t), GROUND - 16 - math.sin(t * math.pi) * 14 + t * 10, f * 53)

    # 8) "THE FORCE IS STRONG WITH THIS ONE", the saber comes back, re-ignition, reset (240-288)
    if 240 <= f < 288:
        vspr = VADER['idle'] if f >= 262 else VADER['hurt']
        vx = ez(142, 150, (f - 256) / 20) if f >= 256 else 142
        cx = ez(94, 30, (f - 244) / 30) if f >= 244 else 94
        cpose = guard_pose(f)
        vd_saber = f >= 262
        v_len = ez(0, 16, (f - 262) / 5)
    if 240 <= f < 262:
        s['fx'].append(('big', "THE FORCE IS STRONG", 4, (230, 60, 50)))
        s['fx'].append(('big', "WITH THIS ONE", 18, (230, 60, 50)))
    if 240 <= f < 254: s['fx'].append(('sw_hilt', 176, GROUND))
    if 254 <= f < 262:                                     # Force pull back to the hand
        hx, hy = vd_hand(vx); t = ease((f - 254) / 8)
        s['fx'].append(('sw_hilt', int(lerp(176, hx, t)), int(lerp(GROUND, hy, t))))
    if 262 <= f < 268: callout(s, "SNAP-HISS", y=2, c=(200, 60, 50))

    # --- assemble -------------------------------------------------------------------------
    cl = actor(JEDI[cpose], cx, cy, pal=JEDI_PAL, aura=c_aura)
    vd = actor(vspr, vx, vy, flip=True, pal=vader_pal(f))
    s['actors'] = [cl, vd]
    ca = cb = None
    if cl_saber and cpose in C_HAND:
        hx, hy = cl_hand(cpose, cx, cy); ca = _seg(hx, hy, c_ang, c_len)
        s['fx'].append(('sw_saber', hx, hy, c_ang, c_len, GREEN))
    if vd_saber:
        hx, hy = vd_hand(vx, vy); cb = _seg(hx, hy, v_ang, v_len)
        s['fx'].append(('sw_saber', hx, hy, v_ang, v_len, RED))
    if 40 <= f < 72 and ca and cb and (f - 40) % 8 in (3, 4):
        p = seg_cross(ca, cb)
        if p:
            s['fx'].append(('spark', int(p[0]), int(p[1]), 5 if (f - 40) % 8 == 3 else 3))
            if (f - 40) % 8 == 3: s['shake'] = rshake()
    if spin: s['fx'].append(('sw_spin', spin[0], spin[1], spin[2], RED))
    if 76 <= f < 102:
        hx, hy = hand_at(vspr, vx, vy, True, 16, 12)
        s['fx'].append(('sw_choke', cx + 1, cy - 4, hx - 3, hy - 2))
    return s

CLIPS = [clip('father', N_, clip_father)]
