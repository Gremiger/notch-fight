"""The Witcher 3: Claude as Geralt of Rivia (white hair in a ponytail, scarred face, yellow cat eyes, dark leather and
chainmail, two sword hilts over his shoulders, the wolf medallion; Claude's orange on the grip wraps and a chest strap), on a
hill above White Orchard at golden hour (rolling hills, a windmill turning, trees, an orange-pink sky). Clip `grifo`:
the griffin. "WIND'S HOWLING." and the grass bends; close-up: he drinks a potion, his eyes go black and dark veins spread;
the griffin screeches and dives, Aard knocks it out of the air into the ground, he draws the silver sword (a gleam) and
Igni burns it as it gets up, then a spinning slash ends it in a burst of feathers. He sheathes the sword, back on the hill."""
from engine import *

THEME = 'witcher'
N_ = 264                                                            # a multiple of 12 (the idle) and of 66 (the windmill)
CX = 50                                                             # Claude-Geralt
INK = (16,14,22)
LINE = "WIND'S HOWLING."
CLOSE = "SWALLOW"
LINE_AT = 8
CLOSE_AT, CLOSE_LEN = LINE_AT + hold(LINE) + 4, 40                  # 32..72
GXL = 128                                                           # where the griffin crashes
ORANGE = (217,119,87)

# ---- people ------------------------------------------------------------------------------------------------
GW, GH, C = 24, 24, 11
POSES = dict(POSES)
POSES.update({
 'idle1': ((-1,4),(0,7),(2,4),(3,7),0,'stand'),
 'idle2': ((-1,4),(0,7),(2,4),(3,6),0,'stand'),
 'aard':  ((1,4),(3,6),(5,2),(11,-1),1,'stance'),                   # the palm out
 'draw1': ((-1,4),(0,7),(-1,-2),(-6,-4),-1,'stance'),               # the hand at the hilt
 'draw2': ((1,4),(3,6),(4,-3),(6,-6),1,'stance'),                   # the sword out and up
 'sword': ((1,4),(3,5),(5,3),(8,1),0,'stance'),
 'igni':  ((5,3),(10,-1),(3,4),(6,2),1,'stance'),                   # far hand casts, near hand holds the blade
 'spin1': ((2,2),(6,0),(-1,2),(-6,0),0,'stance'),
 'spin2': ((-1,2),(-6,1),(2,2),(7,-1),0,'stance'),
 'slash': ((-2,3),(-5,2),(4,1),(10,-2),1,'lunge'),
})
BLADE = {'draw1': 60, 'draw2': 80, 'sword': 38, 'igni': 62}

def _chest(g, at):
    c, ty, sh = at['c'], at['ty'], at['sh']
    for i in range(5): put(g, c - 2 + i + sh(ty + i), ty + i, 'o')            # the orange strap across the chest
    put(g, c + 1 + sh(ty + 3), ty + 3, 'm')                                  # the wolf medallion
    for x in range(-3, 3): put(g, c + x + sh(at['hip']), at['hip'], 'c')    # the mail skirt

def _hilts(g, at):
    c, ty = at['c'], at['ty']
    hilts = [((-3, 1), (-7, -4))] + ([] if at['flags'].get('drawn') else [((-4, 2), (-8, -2))])
    for (x0, y0), (x1, y1) in hilts:
        seg(g, c + x0, ty + y0, c + x1, ty + y1, 'g')
        seg(g, c + x0 - 1, ty + y0 - 1, c + x1 + 1, ty + y1 + 1, 'o')       # the orange grip wrap
        put(g, c + x1, ty + y1 - 1, 'b'); put(g, c + x1 - 1, ty + y1, 'b')  # the pommel
        put(g, c + x0 + 1, ty + y0 + 1, 'b'); put(g, c + x0 - 2, ty + y0 - 2, 'b')

def _face(g, at):
    c, hy, o, fl = at['c'], at['hy'], at['sh'](at['hy']), at['flags']
    for x in range(0, 3): put(g, c + x + o, hy + 4, 'q')                     # stubble
    put(g, c + o, hy + 1, 'r'); put(g, c - 1 + o, hy + 3, 'r')               # the scar
    t = fl.get('tail', 0)                                                    # the ponytail
    for y in (1, 2): put(g, c - 3 + o, hy + y, 'h')
    for y in (3, 4, 5): put(g, c - 4 + t + o, hy + y, 'h')
    if fl.get('dark'):                                                       # dark veins, black eyes
        for dx, dy in ((-1, 2), (1, 3), (2, 3), (1, 1), (2, 1), (3, 3)): put(g, c + dx + o, hy + dy, 'v')
        for ex in (0, 2): put(g, c + ex + o, hy + 2, 'K')

_BODY = dict(w=GW, h=GH, c=C, legs=9, torso=7)
CLAUDE = dict(_BODY, name='witcher-claude', eye='y', hair=['.hhhhh', 'hhhh..'], hair_x=-3, hair_y=1,
              leg=dict(color='p', boot='k', boot_rows=2),
              body=dict(color='j', top='c', collar='c', belt='g'),
              arm=dict(sleeve='j', fore='g', hand='g'),
              paint=dict(body=[_hilts, _chest], face=[_face]))
CPAL = {'s':(206,160,132),'K':INK,'k':(30,24,26),'h':(228,228,236),'j':(38,40,52),'p':(40,36,40),'c':(122,126,138),
        'g':(92,62,40),'o':ORANGE,'m':(238,242,250),'b':(200,206,216),'y':(255,226,50),'q':(150,130,120),
        'r':(176,92,92),'v':(66,50,92)}

def build(pose, **flags):
    return figure(CLAUDE, POSES[pose], **flags)

def hand(pose, x, flip=False, part='hand'):
    return figure_point(CLAUDE, POSES[pose], part, x, GROUND, flip)

# ---- the place: White Orchard at golden hour -----------------------------------------------------------------
def _far(x): return 36 + 4 * math.sin(x / 23) + 3 * math.sin(x / 9.7)
def _mid(x): return 45 + 5 * math.sin(x / 31 + 1) + 2 * math.sin(x / 12)
def _near(x): return 52 + 3 * math.sin(x / 17 + 2)
MILL = (152, int(_mid(152)))                                        # the windmill's foot

def _set(d):
    for y in range(H):
        k = y / GROUND
        top, mid, low = (214,110,120), (246,160,120), (255,210,140)
        c = tuple(int(lerp(a, b, k * 2)) for a, b in zip(top, mid)) if k < 0.5 else tuple(int(lerp(a, b, (k - 0.5) * 2)) for a, b in zip(mid, low))
        d.line([0, y, W, y], fill=c)
    for r, c in ((14, (250,190,140)), (10, (255,215,150)), (7, (255,240,190))): d.ellipse([100 - r, 34 - r, 100 + r, 34 + r], fill=c)
    for mx, mw, mh in ((14, 26, 22), (172, 22, 16)):                  # far mountains with snow
        d.polygon([(mx - mw, 44), (mx, 44 - mh), (mx + mw, 44)], fill=(150,110,140))
        d.polygon([(mx - mw * .3, 44 - mh * .7), (mx, 44 - mh), (mx + mw * .3, 44 - mh * .7), (mx, 44 - mh * .62)], fill=(250,225,225))
    for x in range(W + 1): d.line([x, _far(x), x, H], fill=(176,112,124))
    for x in range(W + 1): d.line([x, _mid(x), x, H], fill=(128,120,68))
    for tx, r in ((18, 3), (36, 4), (66, 3), (112, 4), (128, 3), (172, 4), (182, 3)):  # trees on the middle hills
        ty = int(_mid(tx)); d.line([tx, ty, tx, ty + 2], fill=(70,50,40))
        d.ellipse([tx - r, ty - r * 2 + 1, tx + r, ty + 1], fill=(62,84,50)); d.ellipse([tx - r + 1, ty - r * 2 + 1, tx + 1, ty - r], fill=(98,112,58))
    for x in range(W + 1): d.line([x, _near(x), x, H], fill=(112,118,56))
    d.rectangle([0, GROUND + 2, W, H], fill=(98,106,48))
    for x in range(0, W, 4): d.point((x + (x * 7) % 3, GROUND + 3 + (x * 5) % 5), fill=(214,176,72))
    mx, my = MILL                                                    # the windmill: body, cap, door
    d.polygon([(mx - 5, my), (mx - 3, my - 17), (mx + 3, my - 17), (mx + 5, my)], fill=(184,150,118), outline=(70,50,48))
    d.polygon([(mx - 4, my - 17), (mx, my - 23), (mx + 4, my - 17)], fill=(150,70,60), outline=(70,40,40))
    d.rectangle([mx - 1, my - 4, mx + 1, my], fill=(80,56,44))
register_bg(THEME, lambda v: (v + 50, v + 54, 30), decor=_set)

@fx('wi_mill')
def _fx_mill(d, im, e, f):
    """The windmill's four sails turning (a quarter turn per cycle, so they loop)."""
    mx, my = MILL; cy = my - 17
    base = loop.phase(f, 66) * math.pi / 2
    for i in range(4):
        a = base + i * math.pi / 2; ca, sa = math.cos(a), math.sin(a)
        p = lambda r, w: (mx + ca * r - sa * w, cy + sa * r + ca * w)
        d.polygon([p(3, 0), p(15, 0), p(15, 4), p(3, 4)], fill=(236,214,170), outline=(90,60,48))
    d.ellipse([mx - 1, cy - 1, mx + 1, cy + 1], fill=(90,60,48))

@fx('wi_grass')
def _fx_grass(d, im, e, f):
    """Foreground grass swaying; amp > 1 bends it (the wind)."""
    amp = e[1] if len(e) > 1 else 1.0
    rr = random.Random(5)
    for i in range(0, W + 4, 3):
        h = rr.randint(5, 8); x = i + rr.randint(-1, 1); col = rr.choice([(214,176,72), (150,150,60), (196,160,64), (120,138,56)])
        sw = loop.wave(f, 40, i * 0.31) * amp * 1.3 + amp * 0.8
        d.line([x, H - 1, x + sw * 0.4, H - 1 - h * 0.5], fill=col); d.line([x + sw * 0.4, H - 1 - h * 0.5, x + sw, H - 1 - h], fill=col)

@fx('wi_wind')
def _fx_wind(d, im, e, f):
    """Streaks of wind blowing left (k: frames since it began)."""
    k = e[1]
    for i in range(6):
        y = 6 + i * 8 + (i * 5) % 4; x = (W + 20 - (k * 7 + i * 41)) % (W + 30) - 12
        d.line([x, y, x + 10 + i % 3 * 3, y], fill=(255,236,214))

@fx('wi_aard')
def _fx_aard(d, im, e, f):
    """The Aard blast: arcs of force expanding from the palm (k: frames since it began)."""
    _, x, y, k = e
    for j in range(4):
        r = 4 + k * 5 - j * 6
        if r > 3:
            col = (230,248,255) if j % 2 == 0 else (110,180,255)
            d.arc([x - r, y - r, x + r, y + r], -40, 40, fill=col, width=2 if j < 2 else 1)
    for j in range(7):
        a = (j - 3) * 0.2; r = 6 + k * 5
        d.point((x + math.cos(a) * r, y + math.sin(a) * r), fill=(255,255,255))

@fx('wi_igni')
def _fx_igni(d, im, e, f):
    """The Igni cone of fire from the palm (k: frames since it began)."""
    _, x, y, k = e
    ln = min(k * 7, 62) * (1 if k < 18 else max(0.2, 1 - (k - 18) * 0.15)); rr = loop.rng(f, 17)
    for _ in range(80):
        t = rr.random() ** 0.8; dist = t * ln; sp = dist * 0.34 + 1
        px, py = x + dist, y + rr.uniform(-1, 1) * sp - dist * 0.04; r = max(1, int((1 - t) * 3 + rr.random() * 2))
        col = (255,246,190) if t < 0.2 else ((255,170,50) if t < 0.6 else ((230,70,24) if t < 0.85 else (150,40,24)))
        d.ellipse([px - r, py - r, px + r, py + r], fill=col)

@fx('wi_feather')
def _fx_feather(d, im, e, f):
    """Feathers bursting out and drifting down: (name, x, y, k, n)."""
    _, x, y, k, n = e
    for i in range(n):
        rr = random.Random(i * 977 + int(x)); a = rr.uniform(-math.pi * 0.95, -0.1); sp = rr.uniform(1.4, 4.6)
        px = x + math.cos(a) * sp * min(k, 14) * 1.2 + loop.wave(f, 22, i) * 2 * (k > 10)
        py = min(GROUND + 2, y + math.sin(a) * sp * min(k, 14) * 1.0 + 0.045 * max(0, k - 8) ** 2)
        col = rr.choice([(150,100,50), (200,150,80), (240,224,184), (110,70,40)])
        d.line([px, py, px + 3, py - 2 if i % 2 else py + 2], fill=col); d.point((px + 1, py), fill=(255,248,226))

@fx('wi_blade')
def _fx_blade(d, im, e, f):
    """The silver sword: (name, x, y, angle, length, flip, gleam)."""
    _, x, y, ang, ln, flip, gl = e
    if ln <= 0: return
    a = math.radians(ang); dx = math.cos(a) * (-1 if flip else 1); dy = -math.sin(a)
    tip = (x + dx * ln, y + dy * ln)
    for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)): d.line([x + ox, y + oy, tip[0] + ox, tip[1] + oy], fill=INK)
    d.line([x, y, tip[0], tip[1]], fill=(226,236,250)); d.line([x - dy * 2, y + dx * 2, x + dy * 2, y - dx * 2], fill=ORANGE)
    if gl > 0:
        m = (x + dx * ln * 0.7, y + dy * ln * 0.7); s = int(2 + gl * 3)
        d.line([m[0] - s, m[1], m[0] + s, m[1]], fill=(255,255,255)); d.line([m[0], m[1] - s, m[0], m[1] + s], fill=(255,255,255))

# ---- the griffin ---------------------------------------------------------------------------------------------
BRN, TAN, LT, CRM, BEAK, DK, RED = (116,74,40), (190,140,70), (228,186,108), (244,230,194), (250,198,40), (62,40,28), (200,40,40)
def _tc(c, t): return c if t is None else tuple(int(a * .4 + b * .6) for a, b in zip(c, t))

def _wing(d, rx, ry, tx, ty, w, t=None):
    """A feathered wing from its root to its tip; the feathers hang w px to the lower side."""
    vx, vy = tx - rx, ty - ry; ln = math.hypot(vx, vy) or 1; nx, ny = -vy / ln, vx / ln
    if ny < 0: nx, ny = -nx, -ny
    P = lambda s, o: (rx + vx * s + nx * o, ry + vy * s + ny * o)
    outer = [P(0, -2), P(.5, -w * .25), (tx, ty), P(.97, w * .45), P(.86, w * .8), P(.72, w * 1.0), P(.56, w * 1.0), P(.4, w * .95), P(.2, w * .8), P(0, w * .6)]
    d.polygon(outer, fill=_tc(BRN, t), outline=INK)
    inner = [P(0, 0), P(.5, -w * .1), P(.8, w * .05), P(.7, w * .45), P(.5, w * .5), P(.25, w * .45), P(0, w * .35)]
    d.polygon(inner, fill=_tc(TAN, t))
    for s in (.86, .72, .56, .4):                                   # the long feathers
        d.line([P(s, w * (.9 if s > .5 else .85)), P(s - .12, w * .35)], fill=_tc(DK, t))
    d.line([(tx, ty), P(.9, w * .35)], fill=_tc(DK, t))

def griffin_front(d, cx, cy, s=1.0, flap=0.0, fold=0.0, beak=False, t=None):
    """Seen from the front, wings spread (flap -1 up .. 1 down; fold 0..1 pulls them in), a lion's body under an eagle's head."""
    P = lambda x, y: (cx + x * s, cy + y * s)
    for sg in (-1, 1):
        L = 38 * (1 - .55 * fold); tipy = 3 + 14 * flap - 14 * fold
        _wing(d, *P(sg * 4, -1), *P(sg * L, tipy), 11 * s, t)
    d.line([P(0, 19), P(9, 27)], fill=INK, width=3); d.line([P(0, 19), P(9, 27)], fill=_tc(BRN, t), width=1)   # the lion's tail
    d.ellipse([*P(8, 24), *P(13, 29)], fill=_tc(DK, t), outline=INK)
    d.ellipse([*P(-7, 0), *P(7, 21)], fill=_tc(TAN, t), outline=INK)                                       # the body
    d.ellipse([*P(-4, 3), *P(4, 12)], fill=_tc(LT, t))
    for sg in (-1, 1):                                                                                     # forepaws, claws out
        a, b = P(sg * 4, 15), P(sg * 6, 24 + 2 * (1 - fold))
        d.line([a, b], fill=INK, width=3); d.line([a, b], fill=_tc(TAN, t), width=1)
        d.point((b[0] - 1, b[1] + 2), fill=BEAK); d.point((b[0] + 1, b[1] + 2), fill=BEAK)
    d.ellipse([*P(-5.5, -13), *P(5.5, -2)], fill=_tc(CRM, t), outline=INK)                                 # the head
    d.polygon([P(-5, -11), P(-7, -17), P(-2, -13)], fill=_tc(BRN, t)); d.polygon([P(5, -11), P(7, -17), P(2, -13)], fill=_tc(BRN, t))
    if beak:
        d.polygon([P(-2.5, -8), P(2.5, -8), P(0, -2)], fill=BEAK, outline=INK)
        d.polygon([P(-1.8, -3.5), P(1.8, -3.5), P(0, 3)], fill=BEAK, outline=INK); d.polygon([P(-1.2, -4.5), P(1.2, -4.5), P(0, -2)], fill=RED)
    else:
        d.polygon([P(-2.5, -8), P(2.5, -8), P(1, -1), P(0, 0)], fill=BEAK, outline=INK)
    for ex in (-3, 3):
        d.point(P(ex, -9), fill=(30, 20, 10)); d.point(P(ex - (1 if ex < 0 else -1), -10), fill=INK)

def griffin_side(d, x, y, lift=0.0, t=None):
    """On the ground, facing left, at x (its middle) with its feet at y: lift 0 lying stunned .. 1 up on its legs, wings flared."""
    L = lift; by = y - 8 - 4 * L
    _wing(d, x - 6, by - 4, x - 32, by - 12 - 18 * L, 10, t)                      # the far wing, behind
    d.line([x + 14, by, x + 24, y - 13 - 5 * L], fill=INK, width=3)
    d.line([x + 14, by, x + 24, y - 13 - 5 * L], fill=_tc(BRN, t), width=1)        # the tail
    d.ellipse([x + 22, y - 17 - 5 * L, x + 28, y - 11 - 5 * L], fill=_tc(DK, t), outline=INK)
    for hx in (x + 6, x - 8):                                                      # legs
        if L > .5: d.line([hx, by + 3, hx + 1, y], fill=INK, width=3); d.line([hx, by + 3, hx + 1, y], fill=_tc(TAN, t), width=1)
    d.ellipse([x - 14, by - 7, x + 18, by + 7], fill=_tc(TAN, t), outline=INK)     # the body
    d.ellipse([x - 12, by + 1, x + 2, by + 7], fill=_tc(LT, t))
    if L <= .5: d.line([x - 12, y - 3, x - 21, y - 2], fill=INK, width=3); d.line([x - 12, y - 3, x - 21, y - 2], fill=_tc(TAN, t), width=1)
    hx, hy = x - 20 - 2 * L, y - 15 - 11 * L                                       # head and neck, low when stunned
    d.polygon([(x - 12, by - 4), (hx + 3, hy + 3), (hx + 3, hy + 8), (x - 8, by + 4)], fill=_tc(LT, t), outline=INK)
    d.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=_tc(CRM, t), outline=INK)
    d.polygon([(hx - 4, hy - 2), (hx - 4, hy + 3), (hx - 11, hy + 3)], fill=BEAK, outline=INK); d.point((hx - 11, hy + 4), fill=INK)
    d.polygon([(hx + 2, hy - 4), (hx + 5, hy - 9), (hx + 6, hy - 3)], fill=_tc(BRN, t))
    d.point((hx - 1, hy - 1), fill=(30, 20, 10)); d.line([hx - 3, hy - 3, hx + 1, hy - 2], fill=INK)
    if L <= .5: d.line([hx - 2, hy - 1, hx, hy + 1], fill=INK); d.line([hx - 2, hy + 1, hx, hy - 1], fill=INK)   # dazed
    _wing(d, x - 3, by - 6, x + 34, by - 8 - 24 * L, 11, t)                       # the near wing

@fx('wi_grif')
def _fx_grif(d, im, e, f):
    """('wi_grif', 'front', x, y, scale, flap, fold, beak_open, tint) or ('wi_grif', 'side', x, y, lift, tint)."""
    if e[1] == 'front': griffin_front(d, *e[2:])
    else: griffin_side(d, *e[2:])

# ---- the close-up ---------------------------------------------------------------------------------------------
def _poly_part(d, pts, frac, col):
    n = len(pts) - 1; k = frac * n
    for i in range(n):
        if k <= i: break
        u = min(1, k - i); a, b = pts[i], pts[i + 1]
        d.line([a[0], a[1], a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u], fill=col)

def _face_big(im, d, t, f):
    cx, cy = 40, 33
    d.polygon([(cx - 23, cy - 6), (cx - 20, cy - 25), (cx, cy - 31), (cx + 20, cy - 25), (cx + 23, cy - 6), (cx + 21, cy + 22), (cx - 21, cy + 26)], fill=(212,212,222), outline=INK)
    for k in range(-18, 20, 5): d.line([cx + k, cy - 28 + abs(k) // 5, cx + k * 1.15, cy + 14], fill=(170,170,188))
    d.polygon([(cx - 34, H), (cx - 26, cy + 26), (cx - 8, cy + 20), (cx + 8, cy + 20), (cx + 26, cy + 26), (cx + 34, H)], fill=(40,38,50), outline=INK)
    for x in range(cx - 28, cx + 29, 2):                                                      # chainmail
        for y in range(cy + 26, H, 2):
            if (x + y) % 4 == 0 and abs(x - cx) < 22 + (y - cy - 26) // 2: d.point((x, y), fill=(138,142,154))
    d.line([cx - 22, cy + 24, cx + 14, H], fill=ORANGE, width=2)                              # the orange strap
    d.ellipse([cx + 1, cy + 33, cx + 7, cy + 39], outline=(236,240,250)); d.point((cx + 4, cy + 36), fill=(236,240,250))   # the wolf
    d.rectangle([cx - 7, cy + 12, cx + 7, cy + 24], fill=(172,128,104))
    d.ellipse([cx - 14, cy - 17, cx + 14, cy + 17], fill=(214,168,138), outline=(96,66,54))
    for y in range(cy + 4, cy + 17):                                                          # stubble
        for x in range(cx - 13, cx + 14):
            if random.Random(x * 91 + y).random() < 0.35 and ((x - cx) / 14) ** 2 + ((y - cy) / 17) ** 2 < 0.9: d.point((x, y), fill=(140,118,112))
    d.line([cx - 4, cy + 9, cx + 4, cy + 9], fill=(106,58,58))
    d.line([cx, cy - 4, cx - 1, cy + 4], fill=(176,126,100)); d.line([cx - 2, cy + 5, cx + 1, cy + 5], fill=(150,100,84))
    d.polygon([(cx - 15, cy - 14), (cx - 14, cy - 18), (cx, cy - 20), (cx + 14, cy - 18), (cx + 15, cy - 14), (cx + 5, cy - 11), (cx - 8, cy - 12)], fill=(212,212,222))
    d.line([cx - 12, cy - 10, cx - 3, cy - 6], fill=(190,190,204), width=2); d.line([cx + 3, cy - 6, cx + 12, cy - 10], fill=(190,190,204), width=2)
    bl = max(0.0, min(1.0, (t - 0.5) / 0.15)); vp = max(0.0, min(1.0, (t - 0.55) / 0.4))
    for ex in (cx - 8, cx + 8):
        ey = cy - 2
        if bl > 0: d.rectangle([ex - 4, ey - 2, ex + 4, ey + 2], fill=(8, 8, 12))
        else:
            d.rectangle([ex - 4, ey - 2, ex + 4, ey + 2], fill=(236,200,150)); d.rectangle([ex - 3, ey - 1, ex + 3, ey + 1], fill=(255,226,40))
            d.line([ex, ey - 2, ex, ey + 2], fill=(20,16,12))
    d.line([cx - 11, cy - 13, cx - 6, cy + 4], fill=(180,84,84)); d.point((cx - 10, cy - 8), fill=(220,170,160)); d.point((cx - 8, cy - 2), fill=(220,170,160))   # the scar
    veins = [[(0, 2), (-3, 7), (-4, 13), (-8, 18)], [(0, -3), (-3, -8), (-2, -14)], [(-3, 0), (-8, 3), (-12, 7)], [(2, 2), (4, 8), (3, 12)]]
    if vp > 0:
        for ex, sg in ((cx - 8, 1), (cx + 8, -1)):
            for v in veins: _poly_part(d, [(ex + sg * px, cy - 2 + py) for px, py in v], vp, (58,40,84))
    vt = ease(max(0, min(1, t / 0.15))) - ease(max(0, min(1, (t - 0.4) / 0.15)))              # the vial: up to the mouth, tilts, away
    if vt > 0:
        vx, vy = lerp(cx + 26, cx + 4, vt), lerp(cy + 24, cy + 9, vt); tilt = max(0, min(1, (t - 0.15) / 0.2)) * 7
        d.polygon([(vx - 3, vy + 8 - tilt), (vx + 3, vy + 8 + tilt * 0.3), (vx + 3, vy - 2 + tilt * 0.3), (vx - 3, vy - 2 - tilt)], fill=(100,210,130), outline=INK)
        d.rectangle([vx - 1, vy - 5 - tilt * 0.4, vx + 1, vy - 2 - tilt * 0.4], fill=(180,120,70), outline=INK)
        d.rectangle([vx + 3, vy + 2, vx + 8, vy + 9], fill=(92,62,40), outline=INK)

# ---- the clip: starts and ends on the neutral pose, so frame N_ is frame 0 --------------------------------------
def ready(f):
    return pose_cycle(f, 'idle1', 'idle2')

def _lerp(a, b, f, f0, f1): return a + (b - a) * ez(0, 1, (f - f0) / (f1 - f0))
FLAP = [-1, -.2, 1, .2]

def clip_grifo(f):
    s = scene(f, THEME); s['fc'] = (100, 40)
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=(70,42,58), draw=_face_big, txt=CLOSE, color=(255,226,160)); return s
    me, x, flip = ready(f), CX, False
    flags = dict(tail=(f // 6) % 2)
    if 72 <= f < 224: flags['dark'] = 1                                       # the potion: black eyes, dark veins
    if 140 <= f < 240: flags['drawn'] = 1                                     # one hilt is empty
    bl = None                                                                 # (angle, length, gleam) of the silver sword
    amp = 1.0 + 2.6 * ease(1 - abs(f - 26) / 20) if 6 <= f < 46 else 1.0      # the grass bends in the wind
    if 8 <= f < 46: s['fx'].append(('wi_wind', f - 8))
    if cue(f, LINE_AT, LINE): s['fx'].append(('caption', LINE))
    # Geralt
    if 72 <= f < 98: me = 'guard' if f % 12 < 6 else 'guard2'
    if 98 <= f < 118: me = 'aard'
    if 118 <= f < 140: me = 'guard'
    if 140 <= f < 144: me = 'draw1'; bl = (BLADE['draw1'], (f - 140) * 3, 0)
    if 144 <= f < 150: me = 'draw2'; bl = (BLADE['draw2'], 24, ez(1, 0, (f - 144) / 6))
    if 150 <= f < 156: me = 'sword'; bl = (BLADE['sword'], 24, 0)
    if 156 <= f < 178: me = 'igni'; bl = (BLADE['igni'], 24, 0)
    if 178 <= f < 186:
        me = 'run1' if (f // 2) % 2 else 'run2'; x = _lerp(CX, 94, f, 178, 186); bl = (28, 24, 0)
    if 186 <= f < 198:
        me = 'spin1' if (f // 2) % 2 else 'spin2'; x = 94; flip = (f // 2) % 2 == 0; bl = (0, 24, 0)
    if 198 <= f < 202: me = 'sword'; x = 94; bl = (-20, 24, 0)
    if 202 <= f < 224:
        me = 'walk1' if (f // 4) % 2 else 'walk2'; x = _lerp(94, CX, f, 202, 224); flip = True; bl = (-35, 24, 0)
    if 224 <= f < 232: me = 'sword'; bl = (BLADE['sword'], 24, 0)
    if 232 <= f < 236: me = 'draw2'; bl = (BLADE['draw2'], 24 - (f - 232) * 3, 0)
    if 236 <= f < 240: me = 'draw1'; bl = (BLADE['draw1'], max(0, 12 - (f - 236) * 4), 0)
    xi = int(round(x))
    s['actors'].append(put_on(build(me, **flags), xi, flip, CPAL))
    if bl:
        hx, hy = hand(me, xi, flip)
        s['fx'].append(('wi_blade', hx, hy, bl[0], bl[1], flip, bl[2]))
    # the griffin
    t = (255, 255, 255) if (104 <= f < 108 or (160 <= f < 178 and f % 2)) else None
    if 74 <= f < 80: s['fx'].append(('wi_grif', 'front', 156, 8, .8, FLAP[f % 4], 0, True, t))
    if 80 <= f < 104:
        k = min(1, (f - 80) / 20)
        s['fx'].append(('wi_grif', 'front', _lerp(156, 96, f, 80, 100), _lerp(8, 32, f, 80, 100), lerp(.8, 1.15, k), FLAP[f % 4] * (1 - .6 * k), .3 * k, f < 92, t))
    if 74 <= f < 92 and f % 4 < 2: s['fx'].append(('caption', 'SKREEE!', {'box': (2, 2, 100, 20), 'color': (255,214,120), 'max_scale': 2}))
    if 104 <= f < 120:
        k = (f - 104) / 16
        s['fx'].append(('wi_grif', 'front', _lerp(96, 150, f, 104, 120), _lerp(32, 10, f, 104, 120) - 6 * math.sin(math.pi * k), lerp(1.15, .8, k), 0, 1, False, t))
    if 120 <= f < 134:
        k = (f - 120) / 14; s['fx'].append(('wi_grif', 'front', lerp(150, GXL, k), lerp(10, GROUND - 14, k * k), .8, 0, 1, False, t))
    if 134 <= f < 148: s['fx'].append(('wi_grif', 'side', GXL, GROUND, 0, None))
    if 148 <= f < 192: s['fx'].append(('wi_grif', 'side', GXL, GROUND, ease((f - 148) / 18), t))
    # Aard, Igni, the crash, the kill
    if 100 <= f < 116: s['fx'].append(('wi_aard', *hand('aard', CX), f - 100))
    if 156 <= f < 178: s['fx'].append(('wi_igni', *hand('igni', CX, part='back_hand'), f - 156))
    if 134 <= f < 142: s['shake'] = rshake(1)
    if 134 <= f < 146:
        s['fx'].append(('wi_feather', GXL - 10, GROUND - 4, f - 134, 8))
        if f < 140: s['fx'] += [('dust', GXL - 20 + i * 10, GROUND - 1 - (f - 134) // 2 - i % 2) for i in range(5)]
    if 186 <= f < 194: s['fx'].append(('arc', x, GROUND - 14, 17, (f - 186) * 90 + 180, (f - 186) * 90 + 330, (255,255,255), 2))
    if 192 <= f < 196: s['flash'] = 0.8 - (f - 192) * 0.2; s['fc'] = (GXL - 14, GROUND - 18)
    if 192 <= f < 198: s['shake'] = rshake(2)
    if 192 <= f < 226: s['fx'].append(('wi_feather', GXL - 6, GROUND - 14, f - 192, 34))
    if 192 <= f < 196: s['fx'].append(('wi_spark', GXL - 12, GROUND - 16, f - 192))
    s['under'].append(('wi_mill',))
    s['fx'].append(('wi_grass', amp))
    return s

@fx('wi_spark')
def _fx_spark(d, im, e, f):
    _, x, y, k = e; spark(d, int(x), int(y), 4 + 2 * int(k))

def put_on(spr, wx, flip=False, pal=None):
    return actor(spr, wx, flip=flip, pal=pal)

CLIPS = [clip('grifo', N_, clip_grifo)]
