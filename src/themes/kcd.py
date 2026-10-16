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
N_ = 336                                                            # a multiple of 12: the idle bounce loops
CX, RX = 48, 92                                                     # Henry; where the Cuman fights
INK = (16,14,22)
SKY, SKY2, MUD = (96,150,205), (176,208,226), (112,88,62)
STEEL = (214,220,230)
RAID = "WAAAAAH!"
MASTER = "MASTER STRIKE"
VILLAGER = "JESUS CHRIST BE PRAISED!"
RAID_AT, VIL_AT = 26, 238
CLOSE_AT, CLOSE_LEN = 148, 18                                       # the master strike close-up (it pauses the action)

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

def _lamellar(g, at):                                               # rows of small scale plates, grey over brown
    for y in range(at['ty'], at['hip'] - 1):
        for x in range(C - 3, C + 3):
            if g[y][x + at['sh'](y)] == 'j': put(g, x + at['sh'](y), y, ('jq' if y % 2 == 0 else 'mn')[(x + y // 2) % 2])

def _baggy(g, at):                                                  # baggy trousers over the boots
    for y in range(at['hip'], at['hip'] + 5):
        for x in range(C - 3, C + 3): put(g, x, y, 'P' if (x + y) % 3 == 0 else 'p')

def _moustache(g, at):                                              # a drooping moustache
    o = at['sh'](at['hy'])
    for x in (C + 1, C + 2, C + 3): put(g, x + o, at['hy'] + 3, 'k')
    put(g, C + 1 + o, at['hy'] + 4, 'k'); put(g, C + 3 + o, at['hy'] + 4, 'k')

CLAUDE = dict(_BODY, name='kcd-claude', hair=['.hhhhh.', 'hhhhhhh'], hair_y=2,
              paint=dict(body=[_quilt('q'), _tabard]), arm=dict(sleeve='j', fore='j'))
CUMAN = dict(_BODY, name='kcd-cuman', hair=['...H...', '...H...', '..HHH..', '..HHH..', 'FFFFFFF', 'F.....F'], hair_y=5,
             body=dict(color='j', belt='r'), leg=dict(boot_rows=3), paint=dict(body=[_lamellar], head=[_moustache], legs=[_baggy]),
             arm=dict(sleeve='r', fore='r'))
VIL = dict(_BODY, name='kcd-villager', hair=['.vvvvv.', 'vvvvvvv'], hair_y=2, paint=dict(body=[_quilt('q')]),
           arm=dict(sleeve='j', fore='j'))
CPAL = {'s':(232,190,160),'K':INK,'h':(44,30,24),'j':(122,90,62),'q':(104,76,52),'o':(217,119,87),'b':(90,60,40),
        'p':(70,60,52),'k':INK}
UPAL = {'s':(206,160,120),'K':INK,'H':(176,52,40),'F':(62,44,34),'j':(138,138,142),'q':(104,104,112),'m':(122,84,50),
        'n':(92,62,38),'r':(130,50,40),'p':(112,92,70),'P':(88,70,52),'k':INK,'h':(60,40,30)}
VPAL = {'s':(226,184,150),'K':INK,'v':(168,150,110),'j':(92,110,70),'q':(78,94,58),'p':(110,90,66),'k':INK}

_big = {}
def build(spec, pose):
    """figure() grown by 4/3 (a fighter about 32 px tall)."""
    k = (spec['name'], pose)
    if k not in _big:
        g = figure(spec, POSES[pose]); h, w = len(g), len(g[0])
        _big[k] = S([''.join(g[j * 3 // 4][i * 3 // 4] for i in range(w * 4 // 3)) for j in range(h * 4 // 3)])
    return _big[k]

def hand(spec, pose, x, flip):
    """Where the near hand of build(spec, pose) is on screen, standing at x."""
    X, Y = figure_point(spec, POSES[pose], 'hand', x, GROUND, False)
    cx = (X - int(round(x - GW / 2)) + 0.5) * 4 / 3; cy = (Y - (GROUND - GH) + 0.5) * 4 / 3
    w2, h2 = GW * 4 // 3, GH * 4 // 3; ox = int(round(x - w2 / 2))
    return int(ox + (w2 - 1 - cx if flip else cx)), int(GROUND - h2 + cy)

def lying():
    """The Cuman on his back, head to the right, legs apart, arms out, his hat beside his head."""
    g = blank(34, 11)
    for y in (5, 8):                                                  # the legs and boots
        for x in range(2, 12): put(g, x, y, 'p'); put(g, x, y + 1, 'P')
        for x in range(0, 3): put(g, x, y, 'k'); put(g, x, y + 1, 'k')
    for y in range(4, 10):                                            # the lamellar coat
        for x in range(11, 22): put(g, x, y, ('jq' if y % 2 == 0 else 'mn')[(x + y // 2) % 2])
    for x in range(11, 22): put(g, x, 8, 'r')
    for x in range(20, 29): put(g, x, 2, 'r'); put(g, x, 3, 'r')      # one arm flung up over his head
    put(g, 29, 2, 's'); put(g, 30, 2, 's')
    for x in range(14, 25): put(g, x, 10, 'r')                        # the other arm out below
    put(g, 25, 10, 's'); put(g, 26, 10, 's')
    for y in range(4, 9):                                             # the head
        for x in range(22, 28): put(g, x, y, 's')
    put(g, 24, 5, 'K'); put(g, 26, 5, 'K'); put(g, 24, 7, 'k'); put(g, 25, 7, 'k'); put(g, 26, 7, 'k'); put(g, 24, 8, 'k')
    for x in range(25, 33): put(g, x, 9 if x < 29 else 8, 'F')        # the fur hat rolled off beside him
    for x in range(28, 33): put(g, x, 7, 'H')
    return to_sprite(g)

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
    """A hazy grey castle on its wooded hill, far off: a wall, a square keep, towers."""
    c, dk, rf = (146,156,170), (112,122,138), (92,96,112)
    d.rectangle([x, base - 8, x + 50, base], fill=c)                   # the wall
    for bx in range(x, x + 51, 4): d.rectangle([bx, base - 10, bx + 1, base - 9], fill=c)
    d.rectangle([x + 20, base - 18, x + 31, base], fill=c, outline=dk) # the square keep
    for bx in range(x + 20, x + 32, 4): d.rectangle([bx, base - 20, bx + 1, base - 19], fill=c)
    d.polygon([(x + 19, base - 18), (x + 26, base - 24), (x + 32, base - 18)], fill=rf)
    d.rectangle([x + 4, base - 15, x + 9, base], fill=c, outline=dk)   # a corner tower
    d.polygon([(x + 3, base - 15), (x + 6, base - 21), (x + 10, base - 15)], fill=rf)
    d.rectangle([x + 40, base - 13, x + 45, base], fill=c, outline=dk)
    d.polygon([(x + 39, base - 13), (x + 42, base - 18), (x + 46, base - 13)], fill=rf)
    for wx in (x + 24, x + 27): d.rectangle([wx, base - 14, wx, base - 12], fill=dk)

def _set(d):
    for y in range(H):
        k = min(1, y / 40); d.line([0, y, W, y], fill=tuple(int(lerp(a, b, k)) for a, b in zip(SKY, SKY2)))
    for cx_, cy, rr in ((130, 12, 14), (60, 8, 10), (172, 18, 9)):    # soft clouds
        d.ellipse([cx_ - rr * 2, cy - rr // 2, cx_ + rr * 2, cy + rr // 2], fill=(220,234,240))
    d.polygon([(0,40),(40,32),(100,36),(150,34),(185,38),(185,56),(0,56)], fill=(122,160,104))
    d.polygon([(0,48),(60,42),(120,46),(185,43),(185,56),(0,56)], fill=(96,138,74))
    d.ellipse([-30, 30, 90, 90], fill=(92,128,96))                    # the wooded hill the castle sits on
    _castle(d, 6)
    for tx, ty, rr in ((2,36,6),(14,37,5),(36,38,6),(52,37,7),(60,40,5),(72,41,5)):      # trees in front of it
        d.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], fill=(58,96,62)); d.point((tx - 2, ty - 2), fill=(88,126,76))
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
    """Billowing puffs that grow and drift as they rise, and loop: power fades the column in and out."""
    for i in range(n):
        a = (loop.phase(f, 60) + i / n) % 1
        px = x + a * 14 + loop.wave(f, 52, i) * 2; py = y - a * rise
        r = (1.5 + a * size) * power
        if r < 1.5: continue
        c = tuple(int(lerp(p, q, a)) for p, q in zip(col0, col1))
        for ox, oy, k in ((0, 0, 1), (-r * 0.6, r * 0.3, 0.7), (r * 0.6, -r * 0.2, 0.75)):
            d.ellipse([px + ox - r * k, py + oy - r * k * 0.85, px + ox + r * k, py + oy + r * k * 0.85], fill=c)

def _ambient(d, im, f, g):
    smoke(d, f, 151, 25, 5, 22, 4, (236,236,236), (196,214,226))      # the chimney
    burn = lerp(0, 1, (g - 8) / 30) * lerp(1, 0, (g - 230) / 60)     # the raid's fire behind the middle house
    if burn > 0.05:
        gl = (2.5 + 0.6 * loop.wave(f, 12)) * burn
        d.ellipse([80 - gl * 3, 33 - gl, 80 + gl * 3, 33 + gl // 2], fill=(214,92,34))
        d.ellipse([80 - gl * 1.6, 33 - gl * 0.6, 80 + gl * 1.6, 33 + gl // 3], fill=(255,170,60))
    smoke(d, f, 80, 33, 9, 34, 7, (40,38,42), (112,110,116), burn)
    for i, gx in enumerate(range(2, W, 6)):                           # the grass sways
        sway = 1 if loop.wave(f, 52, i * 0.9) > 0.2 else 0
        d.line([gx, GROUND, gx + sway, GROUND - 2], fill=(86,134,62)); d.point((gx + 2, GROUND - 1), fill=(120,162,80))

# ---- weapons and HUD, drawn over the people --------------------------------------------------------------
def blade(d, x, y, ang, L, curve=0, flip=False, col=(190,198,212), edge=(248,250,255)):
    """A 2 px blade from (x, y) at angle ang (degrees, 0 = forward, -90 = up), mirrored when flip; curve bends
    it along its length; a light edge and a gold crossguard."""
    if L < 1: return
    px, py = float(x), float(y)
    for i in range(int(L)):
        a = math.radians((180 - ang - curve * i / L) if flip else (ang + curve * i / L))
        qx, qy = px + math.cos(a), py + math.sin(a)
        dx, dy = (0, 1) if abs(math.cos(a)) > abs(math.sin(a)) else (1, 0)
        d.line([round(px), round(py), round(qx), round(qy)], fill=edge)
        d.line([round(px) + dx, round(py) + dy, round(qx) + dx, round(qy) + dy], fill=col); px, py = qx, qy
    a = math.radians((180 - ang) if flip else ang)
    d.line([round(x - math.sin(a) * 3), round(y + math.cos(a) * 3), round(x + math.sin(a) * 3), round(y - math.cos(a) * 3)], fill=(214,170,64))

def _overlay(im, draw_fn, a):
    """draw_fn(d, a) onto a transparent layer, composited at opacity a (0..1)."""
    if a <= 0: return
    lay = Image.new('RGBA', (W, H), (0,0,0,0)); draw_fn(ImageDraw.Draw(lay), int(255 * min(1, a)))
    im.paste(Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB'))

STAR = (72, 30)
def star(d, a, lit, color):
    """The combat star: six spokes in a ring, semi-transparent white; spoke `lit` in color."""
    cx, cy = STAR
    for off, shade in (((1, 1), True), ((0, 0), False)):
        for k in range(6):
            ang = math.radians(-90 + 60 * k); on = (k == lit)
            c = (0, 0, 0, a // 4) if shade else (color + (a,) if on else (255, 255, 255, a))
            r0, r1 = 7, 19
            x0, y0 = cx + off[0] + math.cos(ang) * r0, cy + off[1] + math.sin(ang) * r0
            x1, y1 = cx + off[0] + math.cos(ang) * r1, cy + off[1] + math.sin(ang) * r1
            d.line([x0, y0, x1, y1], fill=c, width=3 if on else 2)
            n = 2 if on else 1; d.rectangle([x1 - n, y1 - n, x1 + n, y1 + n], fill=c)
        d.ellipse([cx - 7 + off[0], cy - 7 + off[1], cx + 7 + off[0], cy + 7 + off[1]], outline=(0, 0, 0, a // 4) if shade else (255, 255, 255, a * 8 // 10))

def stamina(d, a, v):
    d.rectangle([6, 60, 56, 62], fill=(20,20,20, a)); d.rectangle([7, 61, 7 + int(48 * v), 61], fill=(240,150,90, a) if v < 0.4 else (220,240,200, a))

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

def hud(g):
    """(opacity, lit spoke, its colour, stamina)."""
    a = min(seg_t(g, 60, 74), 1 - seg_t(g, 168, 182))
    lit = 3 if g < 104 else (5 if g < 134 else 0)
    green = g >= 146
    attacking = 80 <= g < 96 or 108 <= g < 124 or 138 <= g
    col = (110,255,140) if green else ((255,70,60) if attacking else (255,255,255))
    v = 1 - 0.38 * seg_t(g, 90, 98) - 0.37 * seg_t(g, 119, 126) + 0.75 * seg_t(g, 172, 182)
    return a, (lit if attacking else -1), col, max(0.0, v)

def _shield(d, cx, cy, w, h, a=255):
    d.polygon([(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy)], fill=(40,160,76), outline=(210,255,220))
    d.polygon([(cx - w + 3, cy - h + 3), (cx + w - 3, cy - h + 3), (cx + w - 3, cy - 1), (cx, cy + h - 5), (cx - w + 3, cy - 1)], fill=(70,200,100))
    d.line([cx, cy - h + 3, cx, cy + h - 6], fill=(210,255,220)); d.line([cx - w + 3, cy - h // 2, cx + w - 3, cy - h // 2], fill=(210,255,220))

def _swords(im, d, t, f):
    """The close-up: a big green shield, Henry's straight blade and the Cuman's curved sabre crossing on it."""
    for r in range(3):                                                # rings spreading from the shield
        rr = 22 + r * 9 + int(t * 14); d.ellipse([46 - rr, 32 - rr, 46 + rr, 32 + rr], outline=(40 + r * 15, 120 + r * 20, 70))
    _shield(d, 46, 30, 26, 28)
    j = int(2 * math.sin(f * 2.1))
    push = int(lerp(10, 0, ease(min(1, t * 3))))                      # the blades slam together
    blade(d, 8 - push, 56 + j, -38, 62, col=(200,208,222))            # Henry, straight
    px, py = 86 + push, 56 - j                                        # the sabre comes from the right, curved
    blade(d, px, py, -38, 64, curve=-30, flip=True, col=(200,208,222))
    if t > 0.1:
        spark(d, 47, 30 + j, 5 + int(3 * math.sin(f * 1.7)), (255,255,200))

def clip_cuman(f):
    s = scene(f, THEME)
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:                           # the master strike close-up: the action waits
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=(14,40,30), draw=_swords, txt=MASTER, box=(92, 8, W - 3, H - 8),
                             color=(120,255,140), outline=(0,50,10), zoom=None)
        return s
    g = f if f < CLOSE_AT else f - 14                                  # the game time; the close-up paused it
    s['under'].append(('kc_do', lambda d, im, f: _ambient(d, im, f, g)))
    hp, hx, hang, hL = henry(g)
    actors = [put_on(build(CLAUDE, hp), hx, pal=CPAL)]
    cu = cuman(g)
    if cu:
        cpose, cx, csab, calpha = cu
        spr = lying() if cpose == 'lying' else build(CUMAN, cpose)
        actors.append(put_on(spr, cx + 2 if cpose == 'lying' else cx, flip=cpose != 'lying', pal=UPAL, alpha=calpha))
    vi = villager(g)
    if vi: actors.append(put_on(build(VIL, vi[0]), vi[1], flip=vi[2], pal=VPAL))
    s['actors'] = actors

    if cu and csab is not None: ux, uy = hand(CUMAN, cpose, cx, True)
    sx, sy = hand(CLAUDE, hp, hx, False)
    def arms(d, im, f):
        d.line([sx - 1, sy, sx - 9, sy + 7], fill=(78,56,38), width=2); d.point((sx - 9, sy + 7), fill=(214,170,64))   # the sheath
        if hang is not None: blade(d, sx, sy, hang, hL * 20 / 14)
        if cu and csab is not None: blade(d, ux, uy, csab, 18, curve=-55, flip=True, col=(206,206,214))
        elif cu and cpose == 'lying' and calpha > 0.5: blade(d, cx - 20, GROUND - 1, -4, 16, curve=24, col=(206,206,214))   # dropped beside him
    s['fx'].append(('kc_do', arms))

    a, lit, col, v = hud(g)
    s['fx'].append(('kc_do', lambda d, im, f: _overlay(im, lambda dd, al: (star(dd, al * 8 // 10, lit, col), stamina(dd, al, v)), a)))

    if cue(g, RAID_AT, RAID): s['fx'].append(('caption', RAID, {'color': (255,200,90), 'outline': (60,20,10)}))
    if cue(g, VIL_AT, VILLAGER): s['fx'].append(('caption', VILLAGER, {'outline': (30,20,10)}))
    for t0 in (90, 119):                                               # the clumsy blocks: steel on steel
        if t0 <= g < t0 + 4 and cu and csab is not None:
            s['fx'].append(('kc_spark', (sx + ux) // 2, min(sy, uy) - 2, g - t0)); s['shake'] = rshake(1)
    if 154 <= g < 162:                                                 # the master strike's riposte lands
        s['fx'].append(('kc_spark', RX - 12, GROUND - 22, g - 154)); s['shake'] = rshake(2)
        s['flash'] = 0.35 * (1 - seg_t(g, 154, 159)); s['fc'] = (RX - 12, GROUND - 22)
    return s

CLIPS = [clip('cuman', N_, clip_cuman)]
