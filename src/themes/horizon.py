"""Horizon Zero Dawn / Forbidden West: Claude as Aloy (a Nora hunter: thick braided hair in Claude's orange, a leather
tunic with fur at the shoulders, a bow and a quiver on her back, a spear, the Focus glowing on her temple), on a grassy
hill at sunset above the rusted, overgrown skyscrapers, a Tallneck walking on the horizon with its ring turning.
Clips: `thunderjaw` (the ground shakes, a Thunderjaw stomps in and roars, Focus view outlines its parts and lights the
disc launcher orange, she rolls under a disc, shoots the launcher off, hefts it in a close-up and fires the discs back
until it collapses in blue sparks), `tallneck` (she leaps from a ruin onto its leg, climbs the yellow handholds, drives
her spear into the core: OVERRIDE, the lights go red to blue and a blue wave unrolls a map, she slides down a rope) and
`acecho` (crouched in tall red grass, a Watcher's blue eye turns yellow, she whistles, springs out: SILENT STRIKE).
Every clip starts and ends on Aloy looking out over the valley."""
import math, random
from PIL import ImageOps
from engine import *

THEME = 'horizon'
CX = 48                                                             # Aloy on the mound
INK = (16,14,22)
SKYTOP, SKYMID, SKYLOW = (104,52,88), (226,104,62), (255,190,92)
MOUND_Y = GROUND - 4                                                # the top of her hill
TALL_X, TALL_Y, TALL_SC = 150, 45, 0.30                             # the Tallneck on the horizon

# ---- colours -------------------------------------------------------------------------------------------------
WHITE, WSH, GREY = (238,236,230), (178,180,192), (112,114,130)
DARK, CABLE = (30,28,38), (52,48,62)
PURP, PURPD = (160,78,210), (98,48,140)
CYAN, ORANGE, YEL = (96,226,255), (255,142,30), (255,222,60)
LIGHT = {'calm': (74,190,255), 'warn': (255,214,58), 'hot': (255,54,40), 'off': (44,44,58)}
RUST, RUSTD, MOSS, MOSSL = (118,84,72), (84,62,60), (66,118,52), (110,160,70)

def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * max(0, min(1, t))) for i in range(3))

# ---- Aloy, built from a pose (engine/people.py) ------------------------------------------------------------
GW, GH, C = 24, 24, 11
POSES = dict(POSES)
POSES.update({
 'idle2':  ((-1,4),(-1,7),(3,4),(3,7),0,'stand'),
 'focus':  ((-1,4),(-1,7),(4,0),(1,-3),0,'stance'),                 # a hand to her temple
 'aim':    ((-4,0),(0,-1),None,(9,-1),0,'stance'),                  # the bow drawn
 'spear':  ((2,3),(6,1),(4,2),(10,0),1,'lunge'),                    # the thrust
 'hold':   ((-2,-1),(-3,-5),(3,2),(1,-3),0,'stance'),               # the launcher up on the shoulder
 'climb1': ((1,-4),(3,-9),(4,3),(6,-2),0,'bent'),
 'climb2': ((1,2),(5,-2),(3,-5),(5,-9),0,'bent'),
 'leap':   ((-3,-1),(-4,-5),(4,-2),(8,-5),1,'jump'),
 'stab1':  ((0,-4),(2,-9),(4,-4),(6,-8),0,'stance'),                # the spear raised
 'stab2':  ((2,2),(6,0),(5,3),(9,4),2,'lunge'),                     # driven down
})
_BODY = dict(w=GW, h=GH, c=C, legs=9, torso=7)

def _gear(g, at):
    """Quiver and bow on her back, behind the torso."""
    c, ty, hip, sh = at['c'], at['ty'], at['hip'], at['sh']
    for i in range(0, 6):
        put(g, c - 4 - i // 3 + sh(ty + i), ty + 4 - i, 'u'); put(g, c - 3 - i // 3 + sh(ty + i), ty + 4 - i, 'u')
    put(g, c - 6 + sh(ty - 2), ty - 3, 'W'); put(g, c - 5 + sh(ty - 2), ty - 3, 'W')                      # the feathers
    for y in range(ty - 4, hip + 4):
        t = (y - (ty - 4)) / (hip + 3 - (ty - 4)); put(g, c - 7 + round(1.4 * (1 - abs(2 * t - 1) ** 2)) + sh(y), y, 'q')

def _fur(g, at):
    c, ty, sh = at['c'], at['ty'], at['sh']
    for x in range(c - 3, c + 3): put(g, x + sh(ty), ty, 'P')
    put(g, c - 3 + sh(ty + 1), ty + 1, 'P'); put(g, c + 2 + sh(ty + 1), ty + 1, 'P')

def _belt(g, at):
    c, hip, sh = at['c'], at['hip'], at['sh']
    for x in range(c - 3, c + 3): put(g, x + sh(hip - 1), hip - 1, 't')
    put(g, c + 1 + sh(hip - 1), hip - 1, 'Y')

HAIR = ['..OOOO..', '.OOOOOO.', 'OOOOOO..', 'OOO.....', 'OOo.....', 'Oo......', 'oO......', 'Oo......', 'oO......', 'Oo......', 'oO......']
CLAUDE = dict(_BODY, name='horizon-aloy', hair=HAIR, hair_x=-4, hair_y=2, eyes=(0, 2),
              body=dict(color='j', belt='t'), arm=dict(sleeve='j', fore='u'),
              leg=dict(color='p', boot='k', boot_rows=2, toe=True),
              paint={'legs': [_gear], 'body': [_fur, _belt]})
CPAL = {'K':INK,'j':(128,84,52),'p':(92,66,46),'k':(52,34,26),'t':(222,196,140),'u':(90,56,34),'Y':(240,226,170)}

def build(pose, **flags): return figure(CLAUDE, POSES[pose], **flags)

def aloy_y(x):
    """The mound under her: flat up to x=64, a slope down to the ground by x=78."""
    return MOUND_Y if x <= 64 else int(round(lerp(MOUND_Y, GROUND, (x - 64) / 14)))

def aloy(s, pose, x, y=None, flip=False, spr=None, focus=True):
    """Aloy at x (feet on the mound or the ground) in a pose, her Focus flickering at the temple."""
    y = aloy_y(x) if y is None else y
    s['actors'].append(actor(spr or build(pose), x, y, flip=flip, pal=CPAL))
    if focus and spr is None:
        pt = POSES[pose]
        def glow(d, im, f):
            hx, hy = figure_point(CLAUDE, pt, 'head', x, y, flip)
            hx += -1 if flip else 1; hy += 1
            on = loop.wave(f, 20) > -0.3
            d.point((hx, hy), fill=(255,255,255) if on else CYAN); d.point((hx, hy + 1), fill=CYAN if on else (40,130,170))
            if on: d.point((hx + (-1 if flip else 1), hy), fill=(60,170,230))
        s['fx'].append(('ho_do', glow))

def ready(f): return pose_cycle(f, 'stand', 'idle2', 12)

@fx('ho_do')
def _fx_do(d, im, e, f):
    """A closure of the clip drawn as an effect: ('ho_do', fn(d, im, f))."""
    e[1](d, im, f)

@fx('ho_spark')
def _fx_spark(d, im, e, f):
    _, x, y, k = e; spark(d, int(x), int(y), 3 + int(k))

# ---- the place -----------------------------------------------------------------------------------------
def _tower(d, x, base, w, h, col, dark, seed):
    """A rusted skyscraper with a broken top, windows and green overgrowth."""
    r = random.Random(seed); top = base - h
    pts = [(x, base), (x, top + r.randint(0, 5))] + [(x + min(w, i * 3 + r.randint(0, 2)), top + r.randint(0, 6) - (3 if i % 2 else 0)) for i in range(w // 3 + 1)] + [(x + w, base)]
    d.polygon(pts, fill=col); d.line([x + w - 1, top + 6, x + w - 1, base], fill=dark)
    for yy in range(top + 8, base - 3, 5):
        for xx in range(x + 2, x + w - 2, 4):
            if r.random() < 0.7: d.point((xx, yy), fill=dark)
    for i in range(w):
        if r.random() < 0.7: d.line([x + i, top + 4 + r.randint(-3, 3), x + i, top + 4 + r.randint(2, 9)], fill=MOSS if r.random() < 0.6 else MOSSL)

def _sky(d, hy=46):
    for y in range(64):
        k = y / hy
        d.line([0, y, W, y], fill=mix(SKYTOP, SKYMID, k * 1.4) if k < 0.72 else mix(SKYMID, SKYLOW, (k - 0.72) / 0.28))

def _far(d):
    _sky(d)
    for (cx, cy, w, col) in ((30, 10, 34, (240,140,100)), (96, 6, 44, (214,102,92)), (170, 14, 40, (250,160,96)), (70, 22, 30, (255,176,110)), (150, 25, 36, (255,196,120))):
        d.rectangle([cx - w // 2, cy, cx + w // 2, cy + 1], fill=col); d.rectangle([cx - w // 3, cy - 1, cx + w // 3, cy - 1], fill=col)
    for r, col in ((15, (255,200,110)), (11, (255,214,130)), (7, (255,238,176))): d.ellipse([122 - r, 40 - r, 122 + r, 40 + r], fill=col)
    d.polygon([(0,47),(0,39),(10,37),(16,41),(30,41),(34,45),(34,47)], fill=(150,86,96))
    d.polygon([(120,47),(130,41),(150,40),(162,37),(176,37),(185,41),(185,47)], fill=(160,90,92))
    for y in range(47, GROUND + 1): d.line([0, y, W, y], fill=mix((186,134,60), (150,128,52), (y - 47) / 11))
    for i, (x, w, h) in enumerate(((78, 10, 20), (92, 8, 28), (104, 12, 16), (170, 10, 22), (180, 8, 16), (138, 8, 12))):
        _tower(d, x, 47, w, h, (140,98,96), (112,78,84), 100 + i)                                           # far, hazy
    d.rectangle([0, 47, W, 49], fill=(176,128,58))

def _near(d):
    for i, (x, w, h) in enumerate(((84, 13, 31), (100, 10, 22), (112, 14, 34), (128, 9, 18), (154, 12, 28), (170, 13, 24))):
        _tower(d, x, GROUND - 3, w, h, RUST, RUSTD, 7 + i)                                                  # near, in the valley
    for y in range(GROUND - 3, GROUND + 1): d.line([0, y, W, y], fill=mix((150,128,52), (96,120,50), (y - GROUND + 3) / 3))
    d.polygon([(0,GROUND),(0,MOUND_Y + 5),(10,MOUND_Y + 1),(22,MOUND_Y),(64,MOUND_Y),(70,MOUND_Y + 2),(80,GROUND)], fill=(86,126,50))
    d.line([10, MOUND_Y + 1, 22, MOUND_Y, 64, MOUND_Y, 70, MOUND_Y + 2, 78, GROUND - 1], fill=(130,168,66))
    d.rectangle([0, GROUND + 1, W, H], fill=(70,92,40)); d.line([0, GROUND + 1, W, GROUND + 1], fill=(112,140,56))
def _set(d): _far(d); _near(d)
register_bg(THEME, lambda v: (v + 70, v + 80, v + 20), decor=_set)

# ---- machine toolkit: drawn on a PIL draw in local (u right, v up) coordinates, facing left -----------------------
def _col(m, flash=0.0):
    """c(part, colour): the colour, flashed toward white; or, in a Focus mask (m: part -> grey), the part's grey."""
    if m is not None: return lambda part, col: m.get(part, 200)
    return lambda part, col: tuple(int(v + (255 - v) * flash) for v in col) if flash else col

def _knee(hx, hy, fx_, fy, l1, l2):
    """Two-bone IK: the knee, bent toward the left (the way these machines face)."""
    dx, dy = fx_ - hx, fy - hy; dist = max(0.01, min(math.hypot(dx, dy), l1 + l2 - 0.05))
    a = (l1 * l1 - l2 * l2 + dist * dist) / (2 * dist); h = math.sqrt(max(0, l1 * l1 - a * a))
    return hx + a * dx / dist - h * dy / dist, hy + a * dy / dist + h * dx / dist

def _gait(ph, stride, lift):
    p = ph % 1.0
    if p < 0.6: return stride * (0.5 - p / 0.6), 0.0
    q = (p - 0.6) / 0.4; return stride * (-0.5 + q), lift * math.sin(math.pi * q)

def _leg(d, P, sc, hu, hv, ph, stride, lift, l1, l2, wd, c, far=False, thigh=None, raise_=0.0, big=False):
    """One leg by two-bone IK: thicker at the top (thigh), a dark joint at the knee and the ankle, a foot."""
    fu, fv = _gait(ph, stride, lift)
    Hp, Fp = P(hu, hv), P(hu + fu, fv + raise_); Kp = _knee(*Hp, *Fp, l1 * sc, l2 * sc)
    th = thigh or wd
    d.line([Hp, Kp, Fp], fill=c('cable', CABLE), width=th + 1, joint='curve')
    d.line([Hp, Kp], fill=c('leg', WSH if far else WHITE), width=th)
    d.line([Kp, Fp], fill=c('leg', GREY if far else WSH), width=max(1, wd - (0 if big else 1)))
    r = max(1, th // 2); d.ellipse([Kp[0] - r, Kp[1] - r, Kp[0] + r, Kp[1] + r], fill=c('cable', DARK))
    d.ellipse([Fp[0] - r + 0.5, Fp[1] - r, Fp[0] + r - 0.5, Fp[1] + r - 1], fill=c('cable', DARK))
    if big:
        d.polygon([(Fp[0] + 3, Fp[1] + 1), (Fp[0] - 9, Fp[1] + 1), (Fp[0] - 9, Fp[1] - 1), (Fp[0] - 3, Fp[1] - 4), (Fp[0] + 3, Fp[1] - 4)], fill=c('leg', WSH if far else WHITE), outline=c('cable', DARK))
        for k in range(3): d.line([Fp[0] - 8 - (k == 1), Fp[1] + 1 - k, Fp[0] - 11, Fp[1] + 1 - k + (1 if k else 0)], fill=c('cable', DARK))
    else: d.line([Fp[0] + 1, Fp[1], Fp[0] - 3 * sc, Fp[1]], fill=c('cable', DARK), width=2 if sc > 0.6 else 1)

def _poly(d, P, pts, fill): d.polygon([P(u, v) for u, v in pts], fill=fill)
def _rot(u, v, a): return u * math.cos(a) + v * math.sin(a), -u * math.sin(a) + v * math.cos(a)

def launcher(d, cx, cy, ang, sc=1.0, m=None, flash=0.0):
    """A disc launcher (grey housing, purple rings, a stack of discs) centred at (cx, cy), its barrel at ang (screen radians)."""
    c = _col(m, flash); ca, sa = math.cos(ang), math.sin(ang)
    p = lambda u, v: (cx + (u * ca - v * sa) * sc, cy + (u * sa + v * ca) * sc)
    d.polygon([p(-6, -3), p(6, -3), p(7, 2), p(-6, 3)], fill=c('lau', GREY))
    d.polygon([p(-3, -3), p(3, -3), p(3, 3), p(-3, 3)], fill=c('lau', PURPD))
    d.polygon([p(2, -4), p(7, -3), p(7, 3), p(2, 4)], fill=c('lau', PURP))
    d.line([p(-6, -3), p(6, -3)], fill=c('lau', WSH))
    for k in range(3):
        q = p(-4 + k * 3, -6); d.ellipse([q[0] - 1.5 * sc, q[1] - 1.5 * sc, q[0] + 1.5 * sc, q[1] + 1.5 * sc], fill=c('lau', mix(PURP, WHITE, 0.3 * k)))

LAU_NEAR, LAU_FAR = (-0.3, 1.5), (-0.35, 1.25)

def tj_launcher(x, gy, hh=22, near=True):
    """Screen position of a Thunderjaw's launcher (for the shots, the hit and the highlight)."""
    return (x + 2, gy - hh - 25) if near else (x - 9, gy - hh - 26)

def draw_tj(d, x, gy, ph=0.0, m=None, jaw=0.0, hup=0.0, eye='hot', hh=22, lau=3, flash=0.0, stride=15, lift=6, recoil=0.0, dead=0.0, tilt=0.0):
    """A heavy T-rex machine facing left, ~50 px tall: a boxy head with a lower jaw, a thick neck, a deep chest, two massive
    clawed legs, small arms, a long tail, white plates over black cables, two drums on its back. dead: the legs kicked up."""
    c = _col(m, flash); ca, sa = math.cos(tilt), math.sin(tilt)
    P = lambda u, v: (x + u * ca - v * sa, gy - (u * sa + v * ca)); hv = hh; eyec = LIGHT[eye]
    for far, hu, off in ((True, -3, 0.5), (False, 7, 0.0)):
        _leg(d, P, 1, hu, hv - 3, ph + off, stride, lift, 15, 15, 5, c, far, thigh=7, raise_=dead * (hh * 0.9), big=True)
    # tail: cable core with plates, tapering
    _poly(d, P, [(12, hv + 12), (28, hv + 8), (46, hv + 1), (49, hv - 1), (45, hv - 2), (28, hv - 3), (12, hv - 5)], c('cable', CABLE))
    for k in range(5):
        a, b = 14 + k * 6.5, 19.5 + k * 6.5; hgt = 11 - k * 2
        _poly(d, P, [(a, hv + 11 - k * 1.8), (b, hv + 10 - k * 1.8), (b - .5, hv + 11 - k * 1.8 - hgt * .6), (a, hv + 11 - k * 1.8 - hgt * .6)], c('plate', WHITE if k % 2 == 0 else WSH))
    # body: black cable core, then plates with gaps
    _poly(d, P, [(-21, hv + 17), (-8, hv + 24), (8, hv + 22), (19, hv + 14), (18, hv - 3), (2, hv - 8), (-12, hv - 7), (-23, hv + 2)], c('cable', CABLE))
    for k, (a, b) in enumerate(((-18, -11), (-9.5, -2), (0, 7), (8.5, 15))):                    # back plates
        _poly(d, P, [(a, hv + 18 - abs(k - 1.2)), (b, hv + 21 - abs(k - 1.2)), (b, hv + 12), (a, hv + 11)], c('plate', WHITE))
    _poly(d, P, [(-20, hv + 9), (-8, hv + 9), (-6, hv - 3), (-18, hv - 1)], c('plate', WSH))      # chest
    _poly(d, P, [(-4, hv + 8), (7, hv + 9), (9, hv - 3), (-4, hv - 5)], c('plate', WSH))          # flank
    _poly(d, P, [(10, hv + 8), (17, hv + 11), (16, hv - 1), (10, hv - 3)], c('plate', WHITE))     # hip
    # drums on the back
    if lau & 2: launcher(d, *P(-9, hv + 26), -0.35, LAU_FAR[1], m, flash)
    # thick neck and the boxy head
    _poly(d, P, [(-17, hv + 22), (-27, hv + 26), (-30, hv + 14), (-19, hv + 8)], c('cable', CABLE))
    _poly(d, P, [(-18, hv + 21), (-26, hv + 24), (-28, hv + 17), (-19, hv + 15)], c('plate', WHITE))
    hp = (-27, hv + 22)
    def Hd(pts):
        out = []
        for u, v in pts: ru, rv = _rot(u - hp[0], v - hp[1], hup); out.append((hp[0] + ru, hp[1] + rv))
        return out
    jv = jaw * 11
    _poly(d, P, Hd([(-27, hv + 16 - jv * .2), (-46, hv + 15 - jv), (-47, hv + 11 - jv), (-28, hv + 10 - jv * .3)]), c('head', WHITE))               # lower jaw
    _poly(d, P, Hd([(-28, hv + 15), (-45, hv + 14), (-45, hv + 17), (-28, hv + 19)]), c('cable', DARK))                                            # mouth
    _poly(d, P, Hd([(-26, hv + 30), (-40, hv + 29), (-48, hv + 23), (-47, hv + 17), (-30, hv + 17), (-25, hv + 20)]), c('head', WHITE))         # head block
    _poly(d, P, Hd([(-26, hv + 30), (-34, hv + 30), (-33, hv + 25), (-26, hv + 25)]), c('plate', WSH))
    d.line([P(*Hd([(-31, hv + 23)])[0]), P(*Hd([(-47, hv + 20)])[0])], fill=c('cable', DARK))                                                         # the gap along the snout
    for k in range(4):
        tp = Hd([(-44 + k * 4, hv + 17)])[0]; tq = P(*tp); d.point((tq[0], tq[1] + 1), fill=c('head', WHITE))
    for ex, ey in ((-35, hv + 26), (-30, hv + 25)):
        ee = P(*Hd([(ex, ey)])[0]); d.rectangle([ee[0], ee[1], ee[0] + 1, ee[1] + 2], fill=c('eye', eyec)); d.point((ee[0], ee[1] - 1), fill=c('eye', mix(eyec, WHITE, 0.5)))
    # small arms
    d.line([P(-18, hv + 5), P(-23, hv - 1), P(-26, hv + 1)], fill=c('cable', DARK), width=2); d.point(P(-27, hv + 1), fill=c('head', WHITE))
    if lau & 1: launcher(d, *P(2 - recoil * 2, hv + 25 + recoil), -0.3, LAU_NEAR[1], m, flash)

HL, TOP = 34, 90                                                    # a Tallneck's leg height and where its neck ends

def neck_u(v):
    """The neck's centre line (local u) at height v: rising slightly forward (to the left)."""
    return -12 - 7 * (max(0.0, v - HL) / (TOP - HL)) ** 1.4

def neck_hw(v): return 3.4 - 1.4 * (max(0.0, v - HL) / (TOP - HL))

def draw_tn(d, x, gy, sc=1.0, ph=0.0, ring=0.0, light='calm', m=None, lights=1.0, holds=(), flash=0.0):
    """A Tallneck facing left: a short deep plated torso, four long legs with knees and ankles (thick at the top), a very long
    neck of stacked plate segments, a flat round saucer head with a ring of lights and a dark centre."""
    c = _col(m, flash); P = lambda u, v: (x + u * sc, gy - v * sc); wd = max(1, round(1.5 * sc)); th = max(1, round(2.6 * sc)); hl = HL; top = TOP
    lc = LIGHT[light]
    for far, hu, off in ((True, -6, 0.5), (True, 9, 0.0), (False, -10, 0.0), (False, 6, 0.5)):
        _leg(d, P, sc, hu, hl, ph + off, 11, 6, 18, 18, wd, c, far, thigh=th)
    _poly(d, P, [(-15, hl + 3), (-12, hl + 12), (-2, hl + 15), (9, hl + 13), (14, hl + 6), (11, hl - 4), (-3, hl - 6), (-12, hl - 3)], c('cable', CABLE))
    _poly(d, P, [(-12, hl + 4), (-10, hl + 11), (-2, hl + 13.5), (8, hl + 12), (12, hl + 6), (-1, hl + 4)], c('plate', WHITE))
    _poly(d, P, [(-11, hl + 1), (-1, hl + 3), (10, hl + 3), (9, hl - 3), (-3, hl - 4)], c('plate', WSH))
    for u in (-6, 0, 6): d.line([P(u, hl + 12), P(u + 0.5, hl + 4)], fill=c('cable', DARK))
    v = hl + 8                                                                         # the neck: stacked segments with dark gaps
    d.polygon([P(neck_u(v) - neck_hw(v), v), P(neck_u(v) + neck_hw(v), v), P(neck_u(top) + neck_hw(top), top), P(neck_u(top) - neck_hw(top), top)], fill=c('cable', CABLE))
    while v < top - 1:
        v2 = min(top, v + 5); a, b = neck_hw(v), neck_hw(v2)
        _poly(d, P, [(neck_u(v) - a, v + .6), (neck_u(v) + a, v + .6), (neck_u(v2) + b, v2 - .6), (neck_u(v2) - b, v2 - .6)], c('plate', WHITE if int(v) % 10 < 5 else WSH))
        v = v2
    for (u, vv) in holds:
        q = P(u, vv); d.rectangle([q[0] - 1, q[1] - 1, q[0] + 1, q[1] + 1], fill=c('hold', YEL))
    u0, v0 = neck_u(top), top + 3; R, r = 11, 2.6
    d.polygon([P(u0 - R, v0), P(u0 - 5, v0 - 3.5), P(u0 + 5, v0 - 3.5), P(u0 + R, v0)], fill=c('head', WSH))
    a, b = P(u0 - R, v0 + r), P(u0 + R, v0 - r); d.ellipse([a[0], a[1], b[0], b[1]], fill=c('head', WHITE), outline=c('cable', DARK))
    a, b = P(u0 - R * 0.45, v0 + r * 0.45), P(u0 + R * 0.45, v0 - r * 0.45); d.ellipse([a[0], a[1], b[0], b[1]], fill=c('cable', DARK))
    e = 1 if sc > 0.6 else 0
    for k in range(8):
        ang = 2 * math.pi * (k / 8 + ring); front = math.sin(ang) > 0
        px, py = P(u0 + (R - 0.5) * math.cos(ang), v0 - (r - 0.3) * math.sin(ang))
        d.rectangle([px - e, py, px + e, py + e], fill=c('ring', mix(DARK, lc, lights if front else lights * 0.55)))
    cp = P(u0, v0 + 3.5); rr = max(1, round(1.6 * sc))
    d.ellipse([cp[0] - rr, cp[1] - rr, cp[0] + rr, cp[1] + rr], fill=c('core', mix(lc, WHITE, 0.5 * lights)))

def draw_watcher(d, x, gy, ph=0.0, eye='calm', m=None, tilt=0.0, hh=10, flash=0.0, still=False, lights=1.0):
    """A Watcher facing left: two thin legs, a plated body, a long neck with one big round lens, a short tail.
    Returns where the lens is (for its light)."""
    c = _col(m, flash); ca, sa = math.cos(tilt), math.sin(tilt)
    P = lambda u, v: (x + u * ca - v * sa, gy - (u * sa + v * ca))
    for far, hu, off in ((True, 1, 0.5), (False, 3, 0.0)):
        _leg(d, P, 1, hu, hh, ph + off, 0 if still else 6, 3, 5.5, 5.5, 1, c, far)
    _poly(d, P, [(-5, hh + 3), (0, hh + 6), (7, hh + 5), (9, hh + 2), (3, hh - 1), (-4, hh)], c('cable', CABLE))
    _poly(d, P, [(-4, hh + 3), (0, hh + 6), (6, hh + 5), (7, hh + 3), (0, hh + 2)], c('plate', WHITE))
    d.line([P(8, hh + 3), P(14, hh + 1)], fill=c('cable', CABLE), width=2); d.line([P(8, hh + 4), P(12, hh + 2)], fill=c('plate', WSH))
    d.line([P(-3, hh + 4), P(-5, hh + 8), P(-8, hh + 10)], fill=c('cable', CABLE), width=2)
    d.line([P(-3, hh + 4), P(-4.5, hh + 7)], fill=c('plate', WSH))
    ec = P(-9, hh + 13)
    d.ellipse([ec[0] - 3, ec[1] - 3, ec[0] + 3, ec[1] + 3], fill=c('head', WHITE), outline=c('cable', DARK))
    lc = mix(DARK, LIGHT[eye], lights) if eye != 'off' else LIGHT['off']
    d.ellipse([ec[0] - 2, ec[1] - 2, ec[0] + 2, ec[1] + 2], fill=c('eye', lc))
    d.point((ec[0] - 1, ec[1] - 1), fill=c('eye', mix(lc, WHITE, 0.6)))
    return ec

def cone(im, ex, ey, ang, spread, length, color, alpha=0.4):
    """A flashlight cone from the eye (ang: screen radians), blended onto im."""
    mk = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mk).polygon([(ex, ey), (ex + length * math.cos(ang - spread), ey + length * math.sin(ang - spread)),
                               (ex + length * math.cos(ang + spread), ey + length * math.sin(ang + spread))], fill=int(255 * alpha))
    im.paste(color, (0, 0), mk.filter(ImageFilter.GaussianBlur(0.8)))

def layer_paste(im, fn, alpha=1.0):
    """fn(draw) paints on a transparent layer that goes onto im at alpha (a machine fading out)."""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if alpha < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * alpha)))
    im.paste(lay, (0, 0), lay)

def blast(d, x, y, k, big=1.0):
    """An orange blast with blue sparks, k frames old."""
    r = (2 + k * 1.5) * big
    if k < 6:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255,140,30)); d.ellipse([x - r * 0.65, y - r * 0.65, x + r * 0.65, y + r * 0.65], fill=(255,236,150))
        d.ellipse([x - r * 0.3, y - r * 0.3, x + r * 0.3, y + r * 0.3], fill=(255,255,255))
    for i in range(10):
        a = i * 0.628 + 0.2 * (i % 3); rr = (3 + k * 2.8) * big * (0.7 + 0.4 * (i % 2))
        d.point((x + math.cos(a) * rr, y + math.sin(a) * rr), fill=(120,210,255) if i % 2 else (255,190,80))

def blue_burst(d, x, y, k, n=26, spread=20):
    """Blue sparks flying out and falling, k frames after it started."""
    t = k / 14
    if t > 1: return
    for i in range(n):
        rr = random.Random(i * 31 + 5); a = rr.uniform(0, 6.283); sp = rr.uniform(0.4, 1.0) * spread
        d.point((int(x + math.cos(a) * sp * t), int(y + math.sin(a) * sp * t * 0.8 + 6 * t * t)), fill=(255,255,255) if i % 5 == 0 else ((110,200,255) if i % 2 else (60,140,255)))

def dust(d, x, y, k):
    for i in range(6):
        rr = random.Random(i * 13 + int(x)); dx = rr.uniform(-6, 6) * (k + 2) / 5
        d.point((int(x + dx), int(y - k * 0.7 - rr.randint(0, 3))), fill=(190,160,110))

# ---- Focus view: purple, the machine's parts outlined in yellow, what is weak in orange -------------------------------
MONO = dict(plate=255, cable=90, leg=170, head=215, lau=60, eye=130, ring=240, core=250, hold=255)

def focus_view(im, k, mach, weak=None, f=0):
    """k 0..1 in. mach(draw, parts) draws the machine into a mask; weak(draw) the weak point."""
    if k <= 0: return
    vi = ImageOps.colorize(ImageOps.autocontrast(im.convert('L'), cutoff=1), (18,6,44), (214,168,255))
    im.paste(Image.blend(im, vi, min(1, k)))
    if mach:
        mk = Image.new('L', (W, H), 0); mach(ImageDraw.Draw(mk), MONO)
        body = mk.point(lambda v: 255 if v else 0)
        im.paste((70,24,140), (0, 0), body.point(lambda v: int(v * 0.35 * k)))
        im.paste(YEL, (0, 0), mk.filter(ImageFilter.FIND_EDGES).point(lambda v: int(255 * k) if v > 40 else 0))
    if weak:
        mk = Image.new('L', (W, H), 0); weak(ImageDraw.Draw(mk))
        body = mk.point(lambda v: 255 if v else 0); ring = body.filter(ImageFilter.MaxFilter(3))
        pulse = 0.65 + 0.35 * loop.wave(f, 12)
        im.paste(ORANGE, (0, 0), body.point(lambda v: int(v * 0.65 * pulse * k)))
        im.paste((255,190,60), (0, 0), Image.composite(ring, Image.new('L', (W, H), 0), body.point(lambda v: 255 - v)).point(lambda v: int(v * pulse * k)))

def sunset_img(top=SKYTOP, mid=SKYMID, low=SKYLOW):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([0, y, W, y], fill=mix(top, mid, y / 30) if y < 30 else mix(mid, low, (y - 30) / 34))
    return im

# ---- the wide scene: the neutral pose and what is around it ---------------------------------------------------------
RED_X0, RED_X1 = 70, 124                                            # the patch of tall red grass

def tufts(s, red=True):
    """Grass swaying in the foreground, and the red patch (drawn after Aloy, so it hides her legs)."""
    def fg(d, im, f):
        rr = random.Random(3)
        for i in range(34):
            bx = rr.randint(0, W - 1); h = rr.randint(3, 6); ph = rr.random()
            if red and RED_X0 - 4 < bx < RED_X1 + 4: continue
            sw = loop.wave(f, 48, ph * 6.28) * 1.4
            d.line([bx, H - 1, bx + sw, H - 1 - h], fill=(130,170,60)); d.line([bx + 1, H - 1, bx + 1 + sw * 0.7, H - 1 - h + 1], fill=(88,128,46))
        if red:
            rr = random.Random(11)
            for i in range((RED_X1 - RED_X0) * 3):
                bx = RED_X0 + rr.random() * (RED_X1 - RED_X0); h = rr.randint(6, 14) - (3 if bx < RED_X0 + 5 or bx > RED_X1 - 5 else 0)
                ph = rr.random(); sw = loop.wave(f, 40, ph * 6.28) * (h / 7)
                d.line([bx, GROUND + 5, bx + sw, GROUND + 5 - h], fill=[(214,52,40), (170,34,36), (240,96,50), (130,26,34)][rr.randint(0, 3)])
    s['fx'].append(('ho_do', fg))

def wide(f, tall=True, light='calm', red=True):
    """The scene: sunset, ruins, the Tallneck far off walking in place, motes and grass."""
    s = scene(f, THEME)
    if tall:
        gx = TALL_X + 3 * loop.wave(f, loop.N or 240)
        s['under'].append(('ho_do', lambda d, im, f: draw_tn(d, gx, TALL_Y, TALL_SC, ph=loop.phase(f, 30), ring=loop.phase(f, 60), light=light)))
    s['under'].append(('fireflies', {'n': 7, 'area': (0, 14, W, GROUND - 6), 'color': (255,226,140)}))
    tufts(s, red)
    return s

def neutral(f):
    s = wide(f); aloy(s, ready(f), CX); return s


# ---- thunderjaw ----------------------------------------------------------------------------------------
HEFT = 'DISC LAUNCHER'
FIRE = (192, 197, 202, 207)                                         # her shots with the launcher; they land 4 frames on
C0, C1 = 152, 192                                                   # the close-up
REST = (108, GROUND - 2)                                            # where the launcher lands

def _heft(im, d, t, f):
    """Aloy picks the launcher up off the ground and hefts it onto her shoulder."""
    d.rectangle([0, GROUND - 4, W, H], fill=(96,112,50))
    pose = 'crouch' if t < 0.3 else ('reach' if t < 0.6 else 'hold')
    spr = sprite_img(build(pose), CPAL, 3)
    im.paste(spr, (4, H - spr.height + 12), spr)
    k = ease((t - 0.1) / 0.55)
    launcher(d, lerp(80, 58, k), lerp(50, 22, k), lerp(0.1, -0.8, k), 2.4)
    if t > 0.65 and f % 4 < 2: spark(d, 84, 16, 2, (255,230,140))
    if 0.3 < t < 0.6:
        for i in range(5): d.point((58 + i * 5, 56 - (f + i * 3) % 5), fill=(190,160,110))

def tuck(k):
    """Three hand-drawn poses of Aloy tucked into a roll (hair, tunic, knees and boots, a hand): the ball turns by a third each time."""
    g = blank(14, 14); a0 = (-2.1, 0.0, 2.1)[k]
    for y in range(14):
        for x in range(14):
            if math.hypot(x - 6.5, y - 7) < 5.2: g[y][x] = 'j'
    def blob(a, r, ch, n=1):
        bx, by = round(6.5 + math.cos(a) * r), round(7 + math.sin(a) * r)
        for dx in range(-n, n + 1):
            for dy in range(-n, n + 1): put(g, bx + dx, by + dy, ch)
        return bx, by
    blob(a0 + 3.14, 4.6, 'p', 1); blob(a0 + 3.14, 6, 'k', 1)               # knees and boots on one side
    blob(a0, 4.2, 'O', 1); blob(a0 + .4, 5.4, 'o', 0); blob(a0 - .5, 5.6, 'O', 0)   # her hair on the other
    blob(a0 + 1.7, 4.6, 's', 0); blob(a0 - 1.5, 3.5, 'u', 0)
    return to_sprite(g)

def clip_thunderjaw(f):
    s = wide(f)
    tx, ph, jaw, hup, eye, hh, lau, flash, alpha, rec, dead, tilt = 260, 0.0, 0.0, 0.0, 'hot', 22, 3, 0.0, 1.0, 0.0, 0.0, 0.0
    show = 12 <= f < 236
    if 12 <= f < 46: tx = ez(250, 142, (f - 12) / 34); ph = (250 - tx) / 18.0
    elif f >= 46: tx = 142
    if 46 <= f < 62: jaw = math.sin(math.pi * (f - 46) / 16) ** 0.6; hup = 0.35 * jaw
    if 137 <= f < 149: jaw = 0.8 * (1 - (f - 137) / 12); hup = 0.3 * jaw; tx += 3 * math.sin((f - 137) * 0.9)
    if 98 <= f < 102: rec = 1.0 - (f - 98) / 4
    if f >= 137: lau = 2
    for i, t0 in enumerate(FIRE):                                    # the discs land and push it back
        g = f - (t0 + 4)
        if 0 <= g < 8: tx += 4 * (i + 1) * (1 - g / 8) * 0.6
        if 0 <= g < 3: flash = 0.5 * (1 - g / 2) if g < 2 else 0.0
        if f >= t0 + 4: tx += 1.5
        if 0 <= g < 3: s['shake'] = rshake(1)
    if f >= 207:                                                     # the legs buckle, the body drops, it tips over
        ph = 0.0; hh = 22 - 10 * ease((f - 207) / 9) - 5 * ease((f - 216) / 8)
        hup = -0.3 * ease((f - 207) / 9); tilt = 0.3 * ease((f - 216) / 8); dead = ease((f - 216) / 8)
        if f >= 209: eye = 'off'
    if f >= 228: alpha = max(0.0, 1 - (f - 228) / 8)
    if 14 <= f < 50 and f % 7 < 2: s['shake'] = (0, 1 if f % 7 == 0 else -1)
    if 46 <= f < 58 or 137 <= f < 142 or 207 <= f < 211: s['shake'] = rshake(1)
    if 222 <= f < 230: s['shake'] = (0, 2 if f % 2 == 0 else -1)                  # it hits the ground
    jx = tx
    def tj(d, im, f, m=None):
        if m is not None: draw_tj(d, jx, GROUND, ph, m, jaw, hup, eye, hh, lau, 0.0, dead=dead, tilt=tilt)
        elif alpha < 1: layer_paste(im, lambda dd: draw_tj(dd, jx, GROUND, ph, None, jaw, hup, eye, hh, lau, flash, recoil=rec, dead=dead, tilt=tilt), alpha)
        else: draw_tj(d, jx, GROUND, ph, None, jaw, hup, eye, hh, lau, flash, recoil=rec, dead=dead, tilt=tilt)
    if show:
        s['under'].append(('ho_do', tj))
        if 14 <= f < 54: s['fx'].append(('ho_do', lambda d, im, f: [dust(d, jx + dx, GROUND, (f * 2 + dx) % 8) for dx in (-6, 0, 8, 14)]))
    # --- Aloy: the pose, where she is ----------------------------------------------------------------------
    pose, ax, spr = ready(f), CX, None
    if 20 <= f < 62: pose = pose_cycle(f, 'guard', 'guard2')
    focus_k = 0.0
    if 62 <= f < 96:
        pose = 'focus'; focus_k = ease((f - 62) / 4) if f < 90 else 1 - ease((f - 90) / 5)
    if 96 <= f < 104: pose = 'guard'
    if 104 <= f < 116:
        ax = CX + 18 * ease((f - 104) / 12); spr = tuck(((f - 104) // 2) % 3)
    if f >= 116: ax = CX + 18
    if 116 <= f < 124: pose = 'crouch'
    if 124 <= f < 142: pose = 'aim'
    if 142 <= f < C0: pose = 'guard'
    if C0 <= f < 192: pose = 'crouch'
    if 192 <= f < 224: pose = 'hold'
    if 224 <= f < 238: pose = pose_cycle(f, 'walk1', 'walk2', 3); ax = ez(CX + 18, CX, (f - 224) / 14)
    if f >= 238: ax = CX
    ay = aloy_y(ax)
    # --- the close-up -----------------------------------------------------------------------------------------
    if C0 <= f < C1:
        s['image'] = closeup((f - C0) / (C1 - C0), f, bg=sunset_img((70,36,70), (190,84,64), (250,170,90)), draw=_heft, txt=HEFT,
                             box=(88, 8, W - 4, 40), color=(255,236,160), max_scale=2, text_from=0.35); return s
    # --- the beats around her ----------------------------------------------------------------------------------------
    if focus_k > 0:
        def fview(d, im, f):
            focus_view(im, focus_k, lambda dd, m: draw_tj(dd, jx, GROUND, ph, m, jaw, hup, eye, hh, lau, 0.0),
                       lambda dd: [launcher(dd, *tj_launcher(jx, GROUND, hh), LAU_NEAR[0], LAU_NEAR[1], {'lau': 255}), launcher(dd, *tj_launcher(jx, GROUND, hh, False), LAU_FAR[0], LAU_FAR[1], {'lau': 255})], f)
            kk = (f - 62) / 28; r = int(lerp(2, 120, kk))
            if kk < 1: d.ellipse([ax - r, ay - 14 - r // 3, ax + r, ay - 14 + r // 3], outline=(150,230,255))
        s['fx'].append(('ho_do', fview))
    aloy(s, pose, ax, ay, False, spr)
    if spr is not None:
        s['actors'][-1]['y'] = ay + 1
        s['fx'].append(('ho_do', lambda d, im, f: [dust(d, ax - 8 + dx, ay + 1, (f * 2 + dx) % 7) for dx in (-6, -1, 4)]))
    if 98 <= f < 122:                                                 # the disc, aimed at her chest
        dx_ = 145 - 8 * (f - 98); dy_ = 17 + (145 - dx_) * 0.2
        def disc(d, im, f):
            r = 4; a = f * 0.9
            d.ellipse([dx_ - r - 1, dy_ - r - 1, dx_ + r + 1, dy_ + r + 1], fill=(40,20,70)); d.ellipse([dx_ - r, dy_ - r, dx_ + r, dy_ + r], fill=(206,150,255))
            for i in range(6): d.point((dx_ + math.cos(a + i * 1.047) * (r + 1.5), dy_ + math.sin(a + i * 1.047) * (r + 1.5)), fill=(255,255,255))
            d.ellipse([dx_ - 1, dy_ - 1, dx_ + 1, dy_ + 1], fill=(255,255,255)); d.line([dx_ + 6, dy_ - 1, dx_ + 15, dy_ - 3], fill=(255,200,255))
        s['fx'].append(('ho_do', disc))
    if pose == 'aim':
        hx, hy = figure_point(CLAUDE, POSES['aim'], 'hand', ax, ay); bx, by = figure_point(CLAUDE, POSES['aim'], 'back_hand', ax, ay)
        def bow(d, im, f):
            d.line([hx + 2, hy - 8, hx + 4, hy, hx + 2, hy + 8], fill=(160,106,56), width=1)
            d.line([hx + 2, hy - 8, bx, by, hx + 2, hy + 8], fill=(236,230,210))
            if f < 132: d.line([bx, by, hx + 6, hy], fill=(255,255,255))
        s['fx'].append(('ho_do', bow))
        if 132 <= f < 137:                                            # the arrow flies to the launcher, a white trail behind it
            lx, ly = tj_launcher(jx, GROUND); k = (f - 132) / 4; ex, ey = lerp(hx + 6, lx, k), lerp(hy, ly, k)
            vx, vy = lx - hx, ly - hy; n = math.hypot(vx, vy)
            def arrow(d, im, f):
                d.line([ex - vx / n * 26, ey - vy / n * 26, ex - vx / n * 12, ey - vy / n * 12], fill=(190,196,220), width=1)
                d.line([ex - vx / n * 14, ey - vy / n * 14, ex, ey], fill=(255,255,255), width=1); d.point((ex, ey), fill=(255,230,150))
            s['fx'].append(('ho_do', arrow))
    if 137 <= f < 142: s['fx'].append(('ho_spark', *tj_launcher(jx, GROUND), 3 if f < 141 else 2))
    if 137 <= f < C0:                                                 # the launcher flies off its back and lands
        k = min(1.0, (f - 137) / 14); lx0, ly0 = tj_launcher(142, GROUND)
        lx, ly = lerp(lx0, REST[0], k), lerp(ly0, REST[1], k * k) - 16 * math.sin(math.pi * k)
        s['fx'].append(('ho_do', lambda d, im, f: launcher(d, lx, ly, -0.45 + 0.45 * k + 6.283 * k, 1.15)))
    if 192 <= f < 228:                                                # the launcher on her shoulder
        sx_, sy_ = figure_point(CLAUDE, POSES['hold'], 'shoulder', ax, ay)
        rc = max([2 - (f - t0) for t0 in FIRE if 0 <= f - t0 < 3] or [0])
        if f < 218: s['fx'].append(('ho_do', lambda d, im, f: launcher(d, sx_ + 1 - rc, sy_ - 3, -0.35, 1.3)))
        else: s['fx'].append(('ho_do', lambda d, im, f: layer_paste(im, lambda dd: launcher(dd, sx_ + 1, sy_ - 3, -0.35, 1.3), max(0.0, 1 - (f - 218) / 8))))
        for i, t0 in enumerate(FIRE):                                  # the discs: blue and orange
            ty_ = GROUND - 26 + (i % 2) * 8 - i * 2
            if 0 <= f - t0 < 4:
                k = (f - t0) / 3; px, py = lerp(sx_ + 8, jx - 8, k), lerp(sy_ - 5, ty_, k)
                s['fx'].append(('ho_do', lambda d, im, f, px=px, py=py, i=i: (d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255,150,40) if i % 2 else (90,190,255)),
                                                                           d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255,255,255)), d.line([px - 9, py + 1, px - 3, py], fill=(255,210,120)))))
            if 4 <= f - t0 < 15:
                s['fx'].append(('ho_do', lambda d, im, f, ty_=ty_, k=f - t0 - 4, i=i: blast(d, jx - 8 + (i % 2) * 4, ty_, k, 1.0 + i * 0.12)))
    if 218 <= f < 234: s['fx'].append(('ho_do', lambda d, im, f: [dust(d, jx + dx, GROUND, (f - 218 + abs(dx)) % 12) for dx in (-40, -30, -18, -6, 8, 20, 32)]))
    if 224 <= f < 238: s['fx'].append(('ho_do', lambda d, im, f: blue_burst(d, jx - 8, GROUND - 10, f - 224 if f < 231 else f - 231 + 7, 30, 24)))
    return s


# ---- tallneck: a tall scene with a camera that climbs (cam: how far up it is) ---------------------------------------
TN_X = 100                                                          # where it stops
U0, V0 = neck_u(TOP), TOP + 3                                       # the head's centre (local)
STUB = 24                                                           # the ruin Aloy stands on, its height
_far_img = []

def tn_bg(cam):
    """Sky and far country fixed (the horizon stays put when the camera cranes up), the ground plane under it, the ruin stub scrolling."""
    if not _far_img:
        im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im); _far(d)
        for y in range(GROUND + 1, H): d.line([0, y, W, y], fill=mix((150,128,52), (96,120,50), (y - 47) / 17))
        _far_img.append(im)
    im = _far_img[0].copy(); _tower(ImageDraw.Draw(im), 32, int(GROUND + cam), 30, STUB + 4, RUST, RUSTD, 41)
    return im

def u_edge(v):
    """The left edge of its leg and neck at height v."""
    e = lambda w: neck_u(w) - neck_hw(w)
    return -10 if v <= 24 else (lerp(-10, e(HL + 8), (v - 24) / 18) if v < HL + 8 else e(v))

def holo(im, f, cx, cy, r, k):
    """The blue wave: a ring spreading from (cx, cy); inside it a wireframe map, a few points."""
    if k <= 0: return
    wave_ = Image.new('L', (W, H), 0); ImageDraw.Draw(wave_).ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=255)
    gm = Image.new('L', (W, H), 0); g = ImageDraw.Draw(gm)
    for i in range(1, 6): g.line([0, 47 + 17 * (i / 5) ** 1.7, W, 47 + 17 * (i / 5) ** 1.7], fill=255)
    for j in range(-10, 11): g.line([W // 2 + 10 + j * 5, 47, W // 2 + j * 26, H], fill=255)
    for y in range(3, 47, 7): g.line([0, y, W, y], fill=110)
    inside = Image.new('RGB', (W, H), (30,110,230)); im.paste(inside, (0, 0), wave_.point(lambda v: int(v * 0.28 * k)))
    im.paste((140,230,255), (0, 0), Image.composite(gm, Image.new('L', (W, H), 0), wave_).point(lambda v: int(v * 0.75 * k)))
    d = ImageDraw.Draw(im)
    ring = Image.new('L', (W, H), 0); rd = ImageDraw.Draw(ring)
    rd.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], outline=255, width=2)
    im.paste((210,250,255), (0, 0), ring.point(lambda v: int(v * k)))
    for i, (px, py) in enumerate(((20,54),(48,58),(84,52),(122,56),(160,53),(150,36),(66,32))):
        if math.hypot((px - cx) / 1.0, (py - cy) / 0.7) < r - 3:
            pulse = (f + i * 5) % 14
            d.polygon([(px, py - 2), (px + 2, py), (px, py + 2), (px - 2, py)], fill=(255,255,255) if pulse < 7 else (120,220,255))
            if pulse < 5: d.ellipse([px - 3 - pulse, py - 1 - pulse // 2, px + 3 + pulse, py + 1 + pulse // 2], outline=(150,230,255))

def _spear(d, tail, tip):
    d.line([tail, tip], fill=(30,20,14), width=3); d.line([tail, tip], fill=(226,184,120), width=1)
    dx, dy = tip[0] - tail[0], tip[1] - tail[1]; n = max(1, math.hypot(dx, dy)); dx, dy = dx / n, dy / n
    d.polygon([(tip[0] + dx * 3, tip[1] + dy * 3), (tip[0] - dy * 1.3, tip[1] + dx * 1.3), (tip[0] + dy * 1.3, tip[1] - dx * 1.3)], fill=(236,236,244))

def _tallneck_frame(f):
    top_x = TN_X + U0 - 11; bot_x = TN_X - 34                       # the rope hangs from the saucer's left edge
    tx = ez(250, TN_X, (f - 26) / 44) if 26 <= f < 70 else (250 if f < 26 else TN_X)
    ph = (250 - tx) / 22.0 + 0.05
    ring = f / 20.0; light, lights, flash = 'hot', 1.0, 0.0
    ax, av, pose = 48, STUB, 'stand'
    if 62 <= f < 70: pose = 'crouch'
    if 70 <= f < 84:                                                 # the leap from the ruin onto its front leg
        k = (f - 70) / 14; ax = lerp(48, TN_X + u_edge(14) - 6.5, k); av = lerp(STUB, 14, k) + 12 * math.sin(math.pi * k); pose = 'leap'
    if f >= 84:                                                      # up the handholds
        v = lerp(14, 94, min(1.0, (f - 84) / 44)); ax = TN_X + u_edge(min(v, 88)) - 6.5; av = v
        if v > 86: ax = lerp(ax, TN_X + U0 - 7, (v - 86) / 8)
        pose = 'climb1' if (f // 4) % 2 == 0 else 'climb2'
        if f >= 128: pose, av, ax = 'stand', 95.6, TN_X + U0 - 7
    if 146 <= f < 150: pose = 'stab1'
    if 150 <= f < 176: pose = 'stab2' if f < 170 else 'stand'
    if 160 <= f < 164: flash = 0.8
    if f >= 160: light = 'calm'
    if 206 <= f < 226:                                               # down the rope
        k = ease((f - 206) / 20); av = lerp(95.6, 14, k); pose = 'cheer'
        ax = bot_x + (top_x - bot_x) * ((av + 9) / 94)
    if f >= 226: pose, av, ax = 'stand', 0, bot_x
    cam = max(0.0, av - 18)
    gy = GROUND + cam
    im = tn_bg(cam); d = ImageDraw.Draw(im)
    holds = [(u_edge(v) + 0.5, v) for v in range(14, 90, 8)] if 70 <= f < 164 else []
    draw_tn(d, tx, gy, 1.0, ph, ring, light, None, 1.0, holds, flash)
    if f >= 198:
        k = ease(min(1.0, (f - 198) / 8)); d.line([top_x, gy - 94, lerp(top_x, bot_x, k), gy - 94 * (1 - k)], fill=(236,200,130))
    ay = int(gy - av)
    spr = build(pose)
    draw(im, spr, ax, ay, False, f=f, pal=CPAL)
    pt = POSES[pose]; hx, hy = figure_point(CLAUDE, pt, 'head', ax, ay)
    d.point((hx + 1, hy + 1), fill=CYAN)
    core = (tx + U0, gy - V0 - 3.5)
    if pose in ('stab1', 'stab2'):
        bx, by = figure_point(CLAUDE, pt, 'back_hand', ax, ay); fx_, fy_ = figure_point(CLAUDE, pt, 'hand', ax, ay)
        if pose == 'stab1': _spear(d, (bx, by), (fx_ + (fx_ - bx) * 1.6, fy_ + (fy_ - by) * 1.6))
        else:
            n = max(1, math.hypot(core[0] - bx, core[1] - by)); _spear(d, (bx - (core[0] - bx) / n * 9, by - (core[1] - by) / n * 9), core)
    if 152 <= f < 176 and f % 4 < 2: spark(d, int(core[0]), int(core[1]), 2, (200,240,255))
    if 164 <= f < 232: holo(im, f, core[0], core[1], (f - 164) * 8.0, 1.0 if f < 214 else max(0.0, 1 - (f - 214) / 12))
    if 156 <= f < 176 + 0: draw_fx(d, im, ('caption', 'OVERRIDE', dict(box=(2, 2, W - 2, 22), color=(170,235,255), max_scale=2)), f)
    return im

def clip_tallneck(f):
    """The wide neutral dissolves into the tall scene and back out of it."""
    if f < 12 or f >= 236: return neutral(f)
    im = _tallneck_frame(f)
    white = Image.new('RGB', (W, H), (235,245,255))                  # a flash cut, so no second Aloy ghosts in
    if f < 16: im = Image.blend(render(neutral(f), f), white, (f - 11) / 5)
    elif f < 22: im = Image.blend(im, white, 1 - (f - 15) / 6)
    elif 226 <= f < 230: im = Image.blend(im, white, (f - 225) / 5)
    elif 230 <= f: im = Image.blend(render(neutral(f), f), white, 1 - (f - 229) / 7)
    return {'image': im}


# ---- acecho -----------------------------------------------------------------------------------------------
QUERY, STRIKE = '?', 'SILENT STRIKE'

def note(d, x, y, c=(255,240,170)):
    d.rectangle([x, y + 3, x + 1, y + 4], fill=c); d.line([x + 1, y, x + 1, y + 3], fill=c); d.point((x + 2, y + 1), fill=c)

def clip_acecho(f):
    s = wide(f)
    # Aloy: into the grass, crouch, whistle, spring out, back
    ax, pose, flip = CX, ready(f), False
    if 14 <= f < 34: ax = ez(CX, 88, (f - 14) / 20); pose = pose_cycle(f, 'walk1', 'walk2', 3)
    elif 34 <= f < 132: ax = 88; pose = 'crouch'
    if 132 <= f < 146: k = (f - 132) / 14; ax = lerp(88, 106, k); pose = 'spear'
    if 146 <= f < 176: ax = 106; pose = 'spear' if f < 156 else 'stand'
    if 176 <= f < 204: ax = ez(106, CX, (f - 176) / 28); pose = pose_cycle(f, 'walk1', 'walk2', 3); flip = True
    if f >= 204: ax = CX
    ay = aloy_y(ax); jump = 0
    if 132 <= f < 146: jump = int(8 * math.sin(math.pi * (f - 132) / 14)); ay -= jump
    # the Watcher
    wx, ph, eye, tilt, hh, alpha, still, show = 215, 0.0, 'calm', 0.0, 10, 1.0, False, 30 <= f < 190
    if 30 <= f < 62: wx = ez(215, 152, (f - 30) / 32)
    elif f >= 62: wx = 152
    if 104 <= f < 128: wx = ez(152, 114, (f - 104) / 24)
    if f >= 128: wx = 114
    if f >= 62: ph = (215 - wx) / 14.0
    if 80 <= f < 142: eye = 'warn'
    if f >= 142: eye = 'off'
    if f >= 142: k = ease((f - 142) / 14); tilt = 1.2 * k; hh = 10 - 5 * k; still = True; ph = 0.3
    if f >= 168: alpha = max(0.0, 1 - (f - 168) / 20)
    sweep = math.pi - 0.35 + 0.3 * math.sin(f * 0.15)
    def wat(d, im, f):
        if not show: return
        ex, ey = wx - 9, GROUND - hh - 13
        if eye != 'off' and f < 142:
            cone(im, ex, ey, sweep if eye == 'calm' else math.pi - 0.3 + 0.12 * math.sin(f * 0.5), 0.22, 60, LIGHT[eye], 0.3)
        if alpha < 1: layer_paste(im, lambda dd: draw_watcher(dd, wx, GROUND, ph, eye, None, tilt, hh, 0.0, still), alpha)
        else: draw_watcher(d, wx, GROUND, ph, eye, None, tilt, hh, 0.0, still)
    s['under'].append(('ho_do', wat))
    aloy(s, pose, ax, ay, flip)
    if pose == 'spear':
        hx, hy = figure_point(CLAUDE, POSES['spear'], 'hand', ax, ay); bx, by = figure_point(CLAUDE, POSES['spear'], 'back_hand', ax, ay)
        dx, dy = hx - bx, hy - by; n = max(1, math.hypot(dx, dy)); dx, dy = dx / n, dy / n
        s['fx'].append(('ho_do', lambda d, im, f: _spear(d, (bx - dx * 8, by - dy * 8), (hx + dx * 12, hy + dy * 12))))
    if 100 <= f < 124:                                                       # the whistle
        hx, hy = figure_point(CLAUDE, POSES['crouch'], 'head', 88, aloy_y(88))
        def whistle(d, im, f):
            for i in range(3):
                k = ((f - 100) * 0.6 + i * 3) % 9
                if (f // 4 + i) % 3 != 2 or True: note(d, int(hx + 5 + i * 5 + k * 0.5), int(hy - 3 - k * 1.2 - i))
        s['fx'].append(('ho_do', whistle))
    if 80 <= f < 80 + hold('SILENT ?') and f < 104:
        s['fx'].append(('caption', QUERY, dict(box=(int(wx) - 14, 4, int(wx) + 6, 24), color=(255,226,70), max_scale=3, outline=(40,20,0))))
    if cue(f, 138, STRIKE): s['fx'].append(('caption', STRIKE, dict(box=(2, 2, W - 2, 22), color=(255,255,255), max_scale=2)))
    if 142 <= f < 156: s['fx'].append(('ho_spark', wx - 8, GROUND - 14, f - 142))
    if 142 <= f < 156: s['fx'].append(('ho_do', lambda d, im, f: blue_burst(d, wx - 4, GROUND - 8, f - 142, 14, 12)))
    return s

CLIPS = [clip('thunderjaw', 240, clip_thunderjaw), clip('tallneck', 240, clip_tallneck), clip('acecho', 216, clip_acecho)]
