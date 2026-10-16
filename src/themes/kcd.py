"""Kingdom Come: Deliverance: Claude as Henry, the blacksmith's son (short dark hair, a brown gambeson with a
Claude-orange tabard, a longsword at his hip), on the muddy road of a Bohemian village in 1403 (thatched houses,
a fence, green hills, a castle on a hill, soft daylight). Clip `cuman`: smoke rises behind a house and a Cuman
raider (fur hat, lamellar coat, curved sabre, moustache) runs in shouting; Henry draws, the combat star HUD fades
in, two clumsy blocks drain his stamina, then the green shield flashes MASTER STRIKE: parry and riposte in one
move, the Cuman falls. A villager walks by: "JESUS CHRIST BE PRAISED!". Henry nods, sheathes, back to neutral."""
import math
from PIL import Image, ImageDraw
from engine import *
from engine import loop

THEME = 'kcd'
N_ = 312                                                            # a multiple of 12: the idle bounce loops
CX, RX = 50, 88                                                     # Henry; where the Cuman fights
INK = (16,14,22)
SKY, SKY2, MUD = (96,150,205), (176,208,226), (112,88,62)
STEEL = (214,220,230)
RAID = "WAAAAAH!"
MASTER = "MASTER STRIKE"
VILLAGER = "JESUS CHRIST BE PRAISED!"
RAID_AT, MASTER_AT, VIL_AT = 26, 146, 238

# ---- people, built from a pose (engine/people.py: figure(), POSES) ----------------------------------------
GW, GH, C = 24, 24, 11
POSES = dict(POSES)
POSES.update({
 'idle2': ((-1, 4), (-1, 7), (3, 4), (4, 7), 0, 'stand'),            # Henry's breathing
 'nod':   ((-1, 4), (-1, 7), (3, 4), (4, 6), 2, 'stand'),
 'wind':  ((1, 4), (4, -1), (4, 2), (7, -6), -1, 'stance'),          # the sabre back and up
 'swing': ((1, 4), (4, -2), (6, 1), (10, 3), 2, 'lunge'),            # the sabre coming down
 'low':   ((-1, 4), (-1, 7), (3, 4), (5, 6), 1, 'stand'),            # a sword hanging at the side
})
_BODY = dict(w=GW, h=GH, c=C, legs=9, torso=7)

def _tabard(g, at):                                                 # the orange tabard over the gambeson
    for y in range(at['ty'] + 1, at['hip'] + 1):
        for x in (C - 1, C, C + 1): put(g, x + at['sh'](y), y, 'o')
    for x in range(C - 3, C + 3): put(g, x + at['sh'](at['hip'] - 1), at['hip'] - 1, 'b')

def _quilt(col):
    def p(g, at):                                                   # gambeson / lamellar rows
        for y in range(at['ty'] + 1, at['hip'] - 1, 2):
            for x in range(C - 3, C + 3):
                if g[y][x + at['sh'](y)] == 'j': put(g, x + at['sh'](y), y, col)
    return p

def _moustache(g, at):
    for x in (C + 1, C + 2, C + 3): put(g, x + at['sh'](at['hy']), at['hy'] + 3, 'k')

CLAUDE = dict(_BODY, name='kcd-claude', hair=['.hhhhh.', 'hhhhhhh'], hair_y=2,
              paint=dict(body=[_quilt('q'), _tabard]), arm=dict(sleeve='j', fore='j'))
CUMAN = dict(_BODY, name='kcd-cuman', hair=['...H...', '..HHH..', 'FFFFFFF', 'F.....F'], hair_y=3,
             paint=dict(body=[_quilt('q')], head=[_moustache]), arm=dict(sleeve='r', fore='r'))
VIL = dict(_BODY, name='kcd-villager', hair=['.vvvvv.', 'vvvvvvv'], hair_y=2, paint=dict(body=[_quilt('q')]),
           arm=dict(sleeve='j', fore='j'))
CPAL = {'s':(232,190,160),'K':INK,'h':(44,30,24),'j':(122,90,62),'q':(104,76,52),'o':(217,119,87),'b':(90,60,40),
        'p':(70,60,52),'k':INK}
UPAL = {'s':(206,160,120),'K':INK,'H':(150,40,34),'F':(168,150,120),'j':(110,112,116),'q':(150,152,156),'r':(130,50,40),
        'p':(60,40,70),'k':INK,'h':(60,40,30)}
VPAL = {'s':(226,184,150),'K':INK,'v':(168,150,110),'j':(92,110,70),'q':(78,94,58),'p':(110,90,66),'k':INK}

def build(spec, pose): return figure(spec, POSES[pose])

def lying(spec):
    """The Cuman on his back: his sprite turned a quarter, head to the right, resting on the ground."""
    g = figure(spec, POSES['hurt']); h, w = len(g), len(g[0])
    rows = [''.join(g[h - 1 - y][x] for y in range(h)) for x in range(w)]    # a clockwise quarter turn
    rows = [r for r in rows if set(r) != {'.'}]
    return S(rows)

# ---- the place ------------------------------------------------------------------------------------------
def _house(d, x0, x1, base=53, wall=9, roof=11, chim=None):
    d.rectangle([x0, base - wall, x1, base], fill=(214,200,166), outline=(98,70,48))
    for bx in range(x0 + 4, x1, 7): d.line([bx, base - wall, bx, base], fill=(98,70,48))
    d.line([x0, base - wall + 4, x1, base - wall + 4], fill=(98,70,48))
    mid = (x0 + x1) // 2; d.rectangle([mid - 1, base - 6, mid + 1, base], fill=(70,48,34))
    top = base - wall
    d.polygon([(x0 - 3, top + 1), (mid, top - roof), (x1 + 3, top + 1)], fill=(176,148,82), outline=(124,98,48))
    for k in range(1, roof, 3): d.line([mid - k * (mid - x0 + 3) // roof, top - roof + k + 1, mid + k * (x1 + 3 - mid) // roof, top - roof + k + 1], fill=(146,120,62))
    if chim: d.rectangle([chim, top - roof + 3, chim + 3, top - roof + 8], fill=(120,112,104))

def _castle(d, x, base=34):
    c, dk = (150,148,150), (104,102,108)
    d.rectangle([x, base - 14, x + 30, base], fill=c, outline=dk)
    for tx in (x - 2, x + 25):
        d.rectangle([tx, base - 22, tx + 7, base], fill=c, outline=dk)
        d.polygon([(tx - 1, base - 22), (tx + 4, base - 29), (tx + 8, base - 22)], fill=(150,50,40))
    for bx in range(x + 6, x + 25, 4): d.rectangle([bx, base - 16, bx + 1, base - 15], fill=dk)
    for wx in (x + 3, x + 12, x + 21): d.rectangle([wx, base - 9, wx + 1, base - 6], fill=(40,36,50))
    d.rectangle([x + 12, base - 5, x + 16, base], fill=(60,44,34))

def _set(d):
    for y in range(H):
        k = min(1, y / 40); d.line([0, y, W, y], fill=tuple(int(lerp(a, b, k)) for a, b in zip(SKY, SKY2)))
    for cx_, cy, rr in ((130, 12, 14), (60, 8, 10), (172, 18, 9)):    # soft clouds
        d.ellipse([cx_ - rr * 2, cy - rr // 2, cx_ + rr * 2, cy + rr // 2], fill=(220,234,240))
    d.polygon([(0,40),(40,32),(100,36),(150,34),(185,38),(185,56),(0,56)], fill=(122,160,104))
    d.polygon([(0,48),(60,42),(120,46),(185,43),(185,56),(0,56)], fill=(96,138,74))
    d.ellipse([-22, 33, 62, 80], fill=(104,146,80))                   # the castle's hill
    _castle(d, 6)
    _house(d, 62, 98, chim=None)
    _house(d, 124, 162, chim=150)
    for x0, x1 in ((100, 120), (168, 184)):                           # the fence
        d.line([x0, 51, x1, 51], fill=(112,84,52)); d.line([x0, 54, x1, 54], fill=(112,84,52))
        for px in range(x0, x1 + 1, 5): d.rectangle([px, 49, px + 1, 57], fill=(98,72,44))
    d.rectangle([0, GROUND + 1, W, H], fill=MUD)
    for x in range(3, W, 11): d.point((x, GROUND + 3 + x % 3), fill=(92,70,48)); d.point((x + 4, GROUND + 5), fill=(136,108,78))
register_bg(THEME, lambda v: (v+70,v+54,v+36), decor=_set)

@fx('kc_do')
def _fx_do(d, im, e, f):
    """A closure of the clip drawn as an effect: ('kc_do', fn(d, im, f))."""
    e[1](d, im, f)

@fx('kc_spark')
def _fx_spark(d, im, e, f):
    _, x, y, k = e; spark(d, int(x), int(y), 2 + int(k))

def smoke(d, f, x, y, n, rise, size, col0, col1, power=1.0):
    """A column of puffs that loops: size and power fade it in and out."""
    for i in range(n):
        a = (loop.phase(f, 60) + i / n) % 1
        px = x + loop.wave(f, 52, i) * 2 * a + a * 7; py = y - a * rise
        r = (0.8 + a * size) * power
        if r < 1: continue
        c = tuple(int(lerp(p, q, a)) for p, q in zip(col0, col1))
        d.ellipse([px - r, py - r * 0.8, px + r, py + r * 0.8], fill=c)

def _ambient(d, im, f):
    smoke(d, f, 151, 25, 5, 20, 3, (236,236,236), (196,214,226))      # the chimney
    burn = lerp(0, 1, (f - 8) / 30) * lerp(1, 0, (f - 230) / 60)     # the raid's fire behind the left house
    smoke(d, f, 90, 27, 7, 30, 6, (46,42,46), (110,108,114), burn)
    for i, gx in enumerate(range(2, W, 6)):                           # the grass sways
        sway = 1 if loop.wave(f, 52, i * 0.9) > 0.2 else 0
        d.line([gx, GROUND, gx + sway, GROUND - 2], fill=(86,134,62)); d.point((gx + 2, GROUND - 1), fill=(120,162,80))

# ---- weapons and HUD, drawn over the people --------------------------------------------------------------
def blade(d, x, y, ang, L, col, curve=0, flip=False):
    """A blade from (x, y) at angle ang (degrees, 0 = forward, -90 = up), mirrored when flip; curve bends it."""
    if L < 1: return
    px, py = float(x), float(y)
    for i in range(int(L)):
        a = math.radians((180 - ang - curve * i / L) if flip else (ang + curve * i / L))
        qx, qy = px + math.cos(a), py + math.sin(a)
        d.line([round(px), round(py), round(qx), round(qy)], fill=col); px, py = qx, qy
    a = math.radians((180 - ang) if flip else ang)                    # the crossguard
    d.line([round(x - math.sin(a) * 2), round(y + math.cos(a) * 2), round(x + math.sin(a) * 2), round(y - math.cos(a) * 2)], fill=(200,160,60))

def hand(spec, pose, x, flip): return figure_point(spec, POSES[pose], 'hand', x, GROUND, flip)

def _overlay(im, draw_fn, a):
    """draw_fn(d, a) onto a transparent layer, composited at opacity a (0..1)."""
    if a <= 0: return
    lay = Image.new('RGBA', (W, H), (0,0,0,0)); draw_fn(ImageDraw.Draw(lay), int(255 * min(1, a)))
    im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))

STAR = (151, 26)
def star(d, a, lit, shield=0):
    cx, cy = STAR
    for off, col in (((1, 1), (14,20,30)), ((0, 0), None)):
        for k in range(6):
            ang = math.radians(-90 + 60 * k)
            on = (k == lit)
            c = col or ((120,255,140) if shield and on else ((255,236,150) if on else (246,246,246)))
            r0, r1 = 5, 12 if on else 10
            d.line([cx + off[0] + math.cos(ang) * r0, cy + off[1] + math.sin(ang) * r0, cx + off[0] + math.cos(ang) * r1, cy + off[1] + math.sin(ang) * r1], fill=c + (a,) if on else c + (a * 3 // 4,))
            tx, ty = cx + off[0] + math.cos(ang) * r1, cy + off[1] + math.sin(ang) * r1
            n = 2 if on else 1; d.rectangle([tx - n, ty - n, tx + n, ty + n], fill=c + (a,))
        d.ellipse([cx - 4 + off[0], cy - 4 + off[1], cx + 4 + off[0], cy + 4 + off[1]], outline=(col or (246,246,246)) + (a * 3 // 4,))
    if shield:
        for ring in range(3):
            r = 6 + ring * 4 + (shield % 6)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90,235,120, a * (3 - ring) // 4))
        sh = [(cx - 5, cy - 6), (cx + 5, cy - 6), (cx + 5, cy), (cx, cy + 7), (cx - 5, cy)]
        d.polygon(sh, fill=(50,190,80, a), outline=(255,255,255, a)); d.line([cx, cy - 5, cx, cy + 5], fill=(255,255,255, a))

def stamina(d, a, v):
    d.rectangle([6, 60, 56, 62], fill=(20,20,20, a)); d.rectangle([7, 61, 7 + int(48 * v), 61], fill=(220,240,200, a))
    if v < 0.4: d.rectangle([7, 61, 7 + int(48 * v), 61], fill=(240,150,90, a))

def seg_t(f, a, b): return max(0.0, min(1.0, (f - a) / (b - a)))

# ---- the clip: starts and ends on the neutral pose, so frame N_ is frame 0 --------------------------------
def ready(f): return pose_cycle(f, 'stand', 'idle2', 12)

def put_on(spr, wx, flip=False, pal=None, **kw): return actor(spr, wx, flip=flip, pal=pal, **kw)

def henry(f):
    """(pose, x, blade angle or None, blade length)."""
    ang, L, x, pose = None, 14, CX, ready(f)
    if 52 <= f < 58: pose, ang, L = 'reach', lerp(130, -60, seg_t(f, 52, 58)), 14 * seg_t(f, 52, 56)
    elif 58 <= f < 90: pose, ang = pose_cycle(f, 'guard', 'guard2', 6), -65
    elif 90 <= f < 102: pose, x, ang = 'hurt', CX - 3, -30 + 30 * math.sin(f)                 # clumsy block
    elif 102 <= f < 118: pose, ang = pose_cycle(f, 'guard', 'guard2', 6), -65
    elif 118 <= f < 132: pose, x, ang = 'crouch', CX - 5, -20 + 35 * math.sin(f * 1.3)
    elif 132 <= f < 152: pose, ang = pose_cycle(f, 'guard', 'guard2', 4), -70
    elif 152 <= f < 166: pose, x, ang = 'jab', CX + 8, 12                                        # the riposte
    elif 166 <= f < 174: pose, x, ang = 'guard', CX + 8 - 8 * seg_t(f, 166, 174), -20
    elif 174 <= f < 252: pose, ang = pose_cycle(f, 'low', 'stand', 12), 70                      # panting, sword down
    elif 252 <= f < 262: pose, ang = 'nod', 70
    elif 262 <= f < 268: pose, ang = 'low', 70
    elif 268 <= f < 280: pose, ang, L = 'low', 70, 14 * (1 - seg_t(f, 268, 278))                # sheathes it
    return pose, x, ang, L

def cuman(f):
    """(pose, x, sabre angle or None, opacity) or None."""
    if f < 20: return None
    if f < 52: return pose_cycle(f, 'run1', 'run2', 3), lerp(236, RX, seg_t(f, 20, 52)), -95, 1.0
    if f < 80: return 'wind', RX, -100, 1.0
    if 80 <= f < 87: return 'wind', RX, -110, 1.0
    if 87 <= f < 93: return 'swing', RX - 5, 25, 1.0
    if 93 <= f < 108: return 'wind', RX, -80, 1.0
    if 108 <= f < 115: return 'wind', RX, -110, 1.0
    if 115 <= f < 121: return 'swing', RX - 5, 25, 1.0
    if 121 <= f < 138: return 'wind', RX, -80, 1.0
    if 138 <= f < 151: return 'wind', RX + (f % 2), -115, 1.0
    if 151 <= f < 154: return 'swing', RX - 5, 30, 1.0
    if 154 <= f < 160: return 'hurt', RX + 3, 70, 1.0
    if 160 <= f < 166: return 'kneel', RX + 7, 90, 1.0
    if 166 <= f < 196: return 'lying', RX + 12, None, 1.0
    if 196 <= f < 212: return 'lying', RX + 12, None, 1 - seg_t(f, 196, 212)
    return None

def villager(f):
    """(pose, x, flip) or None."""
    if 196 <= f < 238: return pose_cycle(f, 'walk1', 'walk2', 5), lerp(222, 102, seg_t(f, 196, 232)), True
    if 238 <= f < 266: return 'stand', 102, True
    if 266 <= f < 310: return pose_cycle(f, 'walk1', 'walk2', 5), lerp(102, 220, seg_t(f, 266, 308)), False
    return None

def hud(f):
    """(opacity, lit direction, stamina, shield frame)."""
    a = min(seg_t(f, 60, 74), 1 - seg_t(f, 168, 182))
    lit = 3 if f < 104 else (5 if f < 134 else 0)
    v = 1 - 0.38 * seg_t(f, 90, 98) - 0.37 * seg_t(f, 119, 126) + 0.75 * seg_t(f, 172, 182)
    sh = (f - 148) if 148 <= f < 170 else 0
    return a, lit, max(0.0, v), sh

def clip_cuman(f):
    s = scene(f, THEME)
    s['under'].append(('kc_do', _ambient))
    hp, hx, hang, hL = henry(f)
    actors = [put_on(build(CLAUDE, hp), hx, pal=CPAL)]
    cu = cuman(f)
    if cu:
        cpose, cx, csab, calpha = cu
        spr = lying(CUMAN) if cpose == 'lying' else build(CUMAN, cpose)
        actors.append(put_on(spr, cx, flip=True, pal=UPAL, alpha=calpha))
    vi = villager(f)
    if vi: actors.append(put_on(build(VIL, vi[0]), vi[1], flip=vi[2], pal=VPAL))
    s['actors'] = actors

    def arms(d, im, f):
        sx, sy = hand(CLAUDE, hp, hx, False)                           # Henry's sword: a sheath at the hip, a blade out
        d.line([sx - 1, sy, sx - 7, sy + 5], fill=(78,56,38)); d.point((sx - 7, sy + 5), fill=(190,150,60))
        if hang is not None: blade(d, sx, sy, hang, hL, STEEL)
        if cu and csab is not None:
            ux, uy = hand(CUMAN, cpose, cx, True)
            blade(d, ux, uy, csab, 12, (226,226,232), curve=-35, flip=True)
        elif cu and cpose == 'lying' and calpha > 0.5:
            d.line([RX - 10, GROUND - 1, RX + 4, GROUND - 3], fill=(226,226,232))
    s['fx'].append(('kc_do', arms))

    a, lit, v, sh = hud(f)
    s['fx'].append(('kc_do', lambda d, im, f: _overlay(im, lambda dd, al: (star(dd, al, lit, sh), stamina(dd, al, v)), a)))

    if cue(f, RAID_AT, RAID): s['fx'].append(('caption', RAID, {'color': (255,200,90), 'outline': (60,20,10)}))
    if cue(f, MASTER_AT, MASTER): s['fx'].append(('caption', MASTER, {'box': (2, 2, 128, 22), 'color': (120,255,140), 'outline': (0,50,10)}))
    if cue(f, VIL_AT, VILLAGER): s['fx'].append(('caption', VILLAGER, {'outline': (30,20,10)}))
    for t0 in (90, 119):                                               # the clumsy blocks: steel on steel
        if t0 <= f < t0 + 4: s['fx'].append(('kc_spark', 68, GROUND - 26, f - t0)); s['shake'] = rshake(1)
    if 154 <= f < 162:                                                 # the master strike lands
        s['fx'].append(('kc_spark', RX - 9, GROUND - 18, f - 154)); s['shake'] = rshake(2)
        s['flash'] = 0.35 * (1 - seg_t(f, 154, 159)); s['fc'] = (RX - 9, GROUND - 18)
    return s

CLIPS = [clip('cuman', N_, clip_cuman)]
