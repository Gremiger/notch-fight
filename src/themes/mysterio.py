"""Rey Mysterio: Claude as the masked luchador (orange mask with a silver cross, orange-and-silver baggy pants, white
boots) in a wrestling ring seen from the side: blue apron, red / white / blue ropes, a dark crowd with camera flashes.
Clip `619`: a huge bald heel charges, Claude dropkicks him onto the ropes, the crowd chants 6...1...9, Claude grabs
the top rope and swings his whole body through the gap, feet first, into the heel's face (hand-drawn swing poses and
a motion arc). Close-up: the mask, the eyes narrowing ("BOOYAKA!"). Then the West Coast Pop off the top rope onto the
heel's shoulders, a roll into the pin, the ref's count and the bell, Claude with an arm raised, back on the neutral pose."""
import math
from engine import *

THEME = 'mysterio'
N_ = 360                                                            # a multiple of 12: the ready bounce loops
CX = 58                                                             # Claude's corner of the ring
INK = (16,14,22)
ORANGE, SILVER, WHITE, SKIN = (217,119,87), (200,206,220), (245,245,250), (226,172,130)
ROPES = ((30,(210,50,60)), (40,(240,240,245)), (50,(60,100,220)))   # y of the top, middle, bottom rope and its colour
HX = 96                                                             # the x where Claude grabs the top rope
CHANT = "6... 1... 9!"
COUNT = "1! 2! 3!"
BELL = "DING DING!"
CLOSE = "BOOYAKA!"
CHANT_AT, COUNT_AT, BELL_AT = 54, 236, 262
CLOSE_AT, CLOSE_LEN = 126, 40                                       # the close-up follows the kick

# ---- people, built from a pose (engine/people.py: figure(), POSES) ----------------------------------------
POSES = dict(POSES)
POSES.update({
 'dazed':  ((-4,-1), (-5,-5), (-2,-2), (-3,-6), -3, 'reel'),       # the heel hooked on the ropes, leaning back
 'bent':   ((1,6), (3,'T+3'), (3,6), (5,'T+3'), 3, 'bent'),        # bent over, arms hanging
 'victory':((-3,3), (-4,5), (4,-3), (5,-9), 0, 'stand'),           # one arm to the sky
 'slap_up':((-1,4), (-1,7), (4,1), (7,-4), 0, 'kneel'),            # the ref's hand up...
 'slap_dn':((-1,4), (-1,7), (5,5), (9,8), 1, 'kneel'),             # ...and down on the mat
})

def _mask(g, at):
    """The luchador mask: orange, a silver band and cross on the forehead, white eye trims."""
    c, hy, o = at['c'], at['hy'], at['sh'](at['hy'])
    for y, row in enumerate(('oovoo', 'ovvvo', 'owKwK', 'oooKo', 'ooooo')):
        for i, ch in enumerate(row): put(g, c - 2 + i + o, hy + y, ch)

def _stripes(g, at):                                                # the ref's black and white shirt
    c, ty, hip = at['c'], at['ty'], at['hip']
    for y in range(ty, hip + 1):
        for x in range(c - 3, c + 3): put(g, x + at['sh'](y), y, 'K' if (y - ty) % 2 else 'w')

def _brow(g, at):                                                   # the heel: a wide bald head, a scowl, a goatee
    c, hy, o = at['c'], at['hy'], at['sh'](at['hy'])
    for y in range(hy, hy + 6):
        for x in range(c - 3, c + 4): put(g, x + o, y, 's')
    put(g, c - 3 + o, hy, '.'); put(g, c + 3 + o, hy, '.')
    for x in (c, c + 1, c + 2, c + 3): put(g, x + o, hy + 1, 'K')
    for x in (c + 1, c + 3): put(g, x + o, hy + 2, 'K')
    for x in (c + 1, c + 2, c + 3): put(g, x + o, hy + 4, 'K')
    put(g, c + 3 + o, hy + 5, 'K'); put(g, c + 2 + o, hy + 5, 'K')

def _trunks(g, at):                                                 # long black trunks
    c, hip = at['c'], at['hip']
    for y in range(hip - 2, hip + 4):
        for x in range(c - 5 + at['sh'](y), c + 5 + at['sh'](y)): put(g, x, y, 'p')

CLAUDE = dict(w=24, h=24, c=11, legs=8, torso=6, name='mysterio-claude', shorts='o', eyes=(0,2),
              leg=dict(color='o', stripe='v', boot='w', boot_rows=2, stand=(-2,2)),
              body=dict(color='s'), arm=dict(sleeve='s', hand='w', hand_w=2, shoulders=((-2,1),(2,1))), paint=dict(head=[_mask]))
RIVAL = dict(w=34, h=34, c=15, legs=12, torso=11, head=6, name='mysterio-heel', shorts='p', eyes=(0,2), torso_cols=(-5,5),
             leg=dict(color='s', boot='k', boot_rows=2, stand=(-2,2), stance=(-3,3)),
             body=dict(color='s'), arm=dict(sleeve='s', fist=2, shoulders=((-4,1),(4,1))), paint=dict(head=[_brow], body=[_trunks]))
REF = dict(w=24, h=24, c=11, legs=8, torso=6, name='mysterio-ref', eyes=(0,2), leg=dict(color='p', boot='K'),
           body=dict(color='w'), arm=dict(sleeve='w', hand='s'), hair=['.KKKK.'], hair_x=-2, hair_y=0, paint=dict(body=[_stripes]))
CPAL = {'s':SKIN,'K':INK,'o':ORANGE,'v':SILVER,'w':WHITE,'p':(60,52,70),'k':INK,'f':SKIN,'j':SKIN}
RPAL = {'s':(205,150,118),'f':(205,150,118),'K':INK,'p':(24,22,30),'k':(24,22,30),'j':(205,150,118),'h':(205,150,118)}
FPAL = {'s':(226,184,150),'K':INK,'w':WHITE,'p':(30,30,36),'j':WHITE,'h':INK}

def build(who, pose):
    return figure({'claude': CLAUDE, 'rival': RIVAL, 'ref': REF}[who], POSES[pose])

_lying = {}
def lying(who):
    """The standing figure turned on its back (head to the left), cropped, to lie on the mat."""
    if who not in _lying:
        spr = build(who, 'stand')
        rows = [''.join(r[j] for r in spr) for j in reversed(range(len(spr[0])))]
        rows = [r for r in rows if r.strip('.')]
        cols = [i for i in range(len(rows[0])) if any(r[i] != '.' for r in rows)]
        _lying[who] = S([r[cols[0]:cols[-1] + 1] for r in rows])
    return _lying[who]

# ---- the place ------------------------------------------------------------------------------------------
def _ring(d):
    for y in range(H):
        k = y / GROUND; d.line([0, y, W, y], fill=tuple(int(lerp(a, b, k)) for a, b in zip((12,10,24), (30,24,50))))
    rr = random.Random(619)
    for row, y in enumerate(range(15, 30, 5)):                      # the crowd: rows of dark heads
        col = (10 + row * 3, 8 + row * 2, 18 + row * 3)
        for x in range(-3 + row * 2, W, 6):
            hx, hy = x + rr.randint(-1, 1), y + rr.randint(-1, 1)
            d.ellipse([hx, hy, hx + 4, hy + 4], fill=col); d.rectangle([hx - 1, hy + 4, hx + 5, hy + 8], fill=col)
    for lx in (30, 92, 154):                                        # the arena lights: a bar and a cone of light
        d.rectangle([lx - 8, 0, lx + 8, 2], fill=(230,230,200))
        for y in range(3, 20):
            half = 3 + (y - 3) // 2
            for x in range(lx - half, lx + half):
                if (x + y) % 2 == 0: d.point((x, y), fill=(52,48,70))
    d.rectangle([0, GROUND + 2, W, H], fill=(36,66,160))            # the apron
    d.line([0, GROUND + 3, W, GROUND + 3], fill=(120,160,240)); d.line([0, GROUND + 9, W, GROUND + 9], fill=(20,40,110))
    d.rectangle([0, GROUND - 1, W, GROUND], fill=(150,130,110))     # the mat's edge
    for y, c in ROPES: d.line([8, y, 177, y], fill=c); d.line([8, y + 1, 177, y + 1], fill=tuple(int(v * .6) for v in c))
    for px in (3, 177):                                             # the posts and their turnbuckle pads
        d.rectangle([px, 24, px + 4, GROUND], fill=(150,150,165), outline=INK)
        for y, c in ROPES: d.rectangle([px - 1, y - 2, px + 5, y + 3], fill=(200,40,50), outline=INK)
register_bg(THEME, lambda v: (v + 20, v + 14, v + 24), decor=_ring)

@fx('my_rope')
def _fx_rope(d, im, e, f):
    """The middle rope drawn over a body, to hook him on it."""
    y = ROPES[1][0]; d.line([int(e[1]), y, int(e[2]), y], fill=ROPES[1][1]); d.line([int(e[1]), y + 1, int(e[2]), y + 1], fill=(150,150,155))

@fx('my_spark')
def _fx_spark(d, im, e, f):
    _, x, y, k = e; spark(d, int(x), int(y), 3 + int(k) * 2)
    for a in range(6): d.point((x + math.cos(a + k) * (4 + k * 3), y + math.sin(a + k) * (4 + k * 3)), fill=(255,255,255))

@fx('my_burst')
def _fx_burst(d, im, e, f):
    """The impact flash: a white core with rays, bigger each frame."""
    _, x, y, k = e; r = 3 + 2 * int(k)
    for a in range(8):
        t = a * math.pi / 4 + .3
        d.line([x + math.cos(t) * r * .5, y + math.sin(t) * r * .5, x + math.cos(t) * (r + 5), y + math.sin(t) * (r + 5)], fill=(255,230,120) if a % 2 else (255,255,255))
    d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], fill=(255,255,255), outline=(255,200,80))

@fx('my_stars')
def _fx_stars(d, im, e, f):
    _, x, y = e
    for k in range(3):
        a = loop.phase(f, 24) * 2 * math.pi + k * 2.1
        px, py = x + math.cos(a) * 7, y + math.sin(a) * 2
        d.line([px - 1, py, px + 1, py], fill=(255,230,90)); d.line([px, py - 1, px, py + 1], fill=(255,230,90))

@fx('my_bell')
def _fx_bell(d, im, e, f):
    _, x, y, k = e; sw = (-2, 2)[k % 2]
    d.polygon([(x - 4 + sw, y + 6), (x - 2 + sw, y), (x + 2 + sw, y), (x + 4 + sw, y + 6)], fill=(240,200,60), outline=INK)
    d.point((x + sw, y + 8), fill=(240,200,60))

# ---- the hand-drawn Mysterio, for what a figure can't do (hanging from the rope, turning in the air) ---------
KICK = (((.5,4.5),(1.5,9.5)), ((-1,4),(-3,7.5)))                    # (knee, foot) of the near leg and of the far one
HANG = (((.5,4),(0,8.5)), ((-.5,4.5),(-2,8.5)))
TUCK = (((3,3),(1,6.5)), ((2,3.5),(-1,6.5)))
STRADDLE = (((3,3),(5,7)), ((-3,3),(-5,7)))
ARMS_BACK = ((-2,-7), (-5,-9))                                      # elbow, hand (local, from the shoulder at (0,-5.5))
ARMS_FWD = ((2,-4), (5,-2))
ARMS_UP = ((1,-9), (2,-13))
RS = 1.25                                                           # the hand-drawn Mysterio is drawn a bit bigger than a figure

def rig(d, ox, oy, th, legs, arm, hand=None):
    """Mysterio drawn limb by limb, his hips at (ox, oy), turned th degrees clockwise (0 = upright, facing right).
    hand: a world point where the near hand grips (the rope); the arm stretches to it."""
    a = math.radians(th); ca, sa = math.cos(a), math.sin(a)
    P = lambda p: (round(ox + RS * (p[0] * ca - p[1] * sa)), round(oy + RS * (p[0] * sa + p[1] * ca)))
    def leg(k, col):
        kn, ft = legs[k]; pts = [P((0, 0)), P(kn), P(ft)]
        d.line(pts, fill=INK, width=5); d.line(pts, fill=col, width=3)
        d.line([P((kn[0] + (ft[0] - kn[0]) * .5, kn[1] + (ft[1] - kn[1]) * .5)), P(ft)], fill=WHITE, width=3)
        d.point(P((kn[0] * .4, kn[1] * .4)), fill=SILVER)
    def arm_(col, grip):
        sh = P((0, -5.5)); h = grip or P(arm[1]); e = P(arm[0])
        if grip: e = ((sh[0] + h[0]) // 2 + 1, (sh[1] + h[1]) // 2 + 1)
        d.line([sh, e, h], fill=INK, width=4); d.line([sh, e, h], fill=col, width=2); d.point(h, fill=WHITE)
    arm_((190,130,100), None)                                       # the far arm, then the far leg
    leg(1, (170,92,66))
    sh, hp = P((0, -5.5)), P((0, 0))
    d.line([sh, hp], fill=INK, width=6); d.line([sh, hp], fill=SKIN, width=4)       # the chest
    d.line([P((0, -1)), hp], fill=ORANGE, width=4)                                  # the pants' top
    leg(0, ORANGE)
    hd = P((0.5, -9.5)); r = 3
    d.ellipse([hd[0] - r - 1, hd[1] - r - 1, hd[0] + r + 1, hd[1] + r + 1], fill=INK)
    d.ellipse([hd[0] - r, hd[1] - r, hd[0] + r, hd[1] + r], fill=ORANGE)
    d.point(P((0.5, -11)), fill=SILVER); d.point(hd, fill=SILVER)  # the cross on the mask
    d.point(P((2.5, -10)), fill=WHITE); d.point(P((2.5, -9)), fill=INK)
    arm_(SKIN, hand)                                                # the near arm over everything

@fx('my_rig')
def _fx_rig(d, im, e, f):
    o = e[1]; rig(d, o['x'], o['y'], o['th'], o.get('legs', KICK), o.get('arm', ARMS_BACK), o.get('hand'))

def swing_hip(phi, sag=4):
    """Where the hips are when the body hangs from the top rope and has swung phi degrees toward the heel."""
    a = math.radians(phi); return HX + 11 * RS * math.sin(a), ROPES[0][0] + 11 * RS * math.cos(a) + sag * math.sin(a)

@fx('my_arc')
def _fx_arc(d, im, e, f):
    """The motion arc of the feet swinging from the hang to the kick, drawn up to phi = e[1] degrees."""
    for k in range(0, int(e[1]) + 1, 3):
        a = math.radians(k); x = HX + 24 * math.sin(a); y = ROPES[0][0] + 24 * math.cos(a) + 4 * math.sin(a)
        d.point((round(x), round(y)), fill=(255,236,160) if k % 6 == 0 else (200,160,90))
        if k % 12 == 0: d.point((round(x) - 1, round(y) - 1), fill=(255,255,255))

# ---- the close-up ---------------------------------------------------------------------------------------
def _face(im, d, t, f):
    x = int(lerp(26, 20, ease(t))); cy = 34
    d.polygon([(x - 2, 64), (x + 6, 50), (x + 46, 50), (x + 54, 64)], fill=SKIN, outline=INK)   # the bare shoulders
    d.ellipse([x + 2, 4, x + 50, 56], fill=ORANGE, outline=INK, width=2)                       # the mask
    d.polygon([(x + 26, 6), (x + 21, 22), (x + 31, 22)], fill=SILVER, outline=INK)               # the silver arrow up the forehead
    d.rectangle([x + 24, 22, x + 28, 38], fill=SILVER); d.rectangle([x + 17, 28, x + 35, 32], fill=SILVER)   # and the cross
    n = ease(min(1, t * 2.2))                                                                  # the eyes narrow
    for ex in (x + 8, x + 34):
        hh = int(lerp(7, 2, n))
        d.polygon([(ex - 2, cy + 6 - hh), (ex + 12, cy + 6 - hh - 3), (ex + 12, cy + 6 + hh), (ex - 2, cy + 6 + hh + 2)], fill=WHITE, outline=INK)
        d.rectangle([ex + 3, cy + 6 - hh // 2, ex + 8, cy + 6 + hh // 2], fill=INK)
    d.polygon([(x + 17, 46), (x + 33, 46), (x + 29, 51), (x + 21, 51)], fill=INK)               # the mouth hole
    d.line([x + 4, 18, x + 20, 21], fill=INK); d.line([x + 46, 18, x + 31, 21], fill=INK)        # the narrowed brow

# ---- the clip --------------------------------------------------------------------------------------------
def ready(f):                                                       # the neutral pose: it moves every 12 frames
    return pose_cycle(f, 'guard', 'guard2')

def clip_619(f):
    s = scene(f, THEME)
    s['under'].append(('flashes', {'area': (0, 12, W, 34), 'n': 4}))
    cl = ('fig', ready(f), CX, GROUND, False)        # Claude: a figure (pose, x, y, flip) or a rig (its parameters)
    rv = rf = lie = None                             # the heel (pose, x, flip), the ref, the heel lying down (x, y)
    fxs = []
    # ---- 1. the heel charges, Claude dropkicks him onto the ropes ------------------------------------------
    if 18 <= f < 36: rv = (pose_cycle(f, 'run1', 'run2', 3), lerp(215, 104, (f - 18) / 18), True)
    if 30 <= f < 31: cl = ('fig', 'crouch', 62, GROUND, False)
    if 31 <= f < 38:
        t = (f - 31) / 6
        cl = ('rig', dict(x=ez(64, 88, t), y=ez(47, 43, t), th=-82, legs=KICK, arm=ARMS_BACK))
    if 38 <= f < 43:                                                 # falls to the mat
        t = (f - 38) / 5; cl = ('rig', dict(x=ez(88, 86, t), y=ez(43, 54, t), th=ez(-82, -40, t), legs=KICK, arm=ARMS_BACK))
    if 43 <= f < 48: cl = ('fig', 'crouch', 88, GROUND, False)
    if 48 <= f < 62: cl = ('fig', pose_cycle(f, 'walk1', 'walk2', 3), ez(88, CX, (f - 48) / 14), GROUND, True)
    if 36 <= f < 48: rv = ('hurt', ez(104, 124, (f - 36) / 10), True)
    if 48 <= f < 112: rv = ('dazed', 124, True); fxs += [('my_stars', 126, 25), ('my_rope', 112, 138)]
    if 36 <= f < 40: s['shake'] = rshake(1); fxs += [('my_burst', 100, 40, f - 36)]
    # ---- 2. the chant ------------------------------------------------------------------------------------------
    if cue(f, CHANT_AT, CHANT, extra=14):
        n = min(3, 1 + (f - CHANT_AT) // 10)
        fxs += [('caption', ' '.join(CHANT.split(' ')[:n]), {'box': (10, 2, W - 10, 24), 'max_scale': 3, 'color': (255,220,70), 'outline': INK})]
    # ---- 3. the 619: run, grab the rope, swing through the gap, kick ----------------------------------------
    if 76 <= f < 94: cl = ('fig', pose_cycle(f, 'run1', 'run2', 3), ez(CX, 90, (f - 76) / 18), GROUND, False)
    if 94 <= f < 98: cl = ('fig', 'jump', ez(90, 96, (f - 94) / 4), ez(GROUND, 46, (f - 94) / 4), False)
    SW = ((98, 0, HANG), (104, 38, KICK), (110, 72, KICK), (116, 90, KICK))      # swing poses: (the frame it starts, phi, legs)
    for i, (a, phi, legs) in enumerate(SW):
        if a <= f < (SW[i + 1][0] if i + 1 < len(SW) else 122):
            hx, hy = swing_hip(phi)
            cl = ('rig', dict(x=hx, y=hy, th=-phi, legs=legs, arm=ARMS_BACK, hand=(HX, ROPES[0][0] - 1)))
    if 98 <= f < 122: fxs += [('my_arc', min(90, (f - 98) * 5))]
    if 122 <= f < 126:
        hx, hy = swing_hip(90); t = (f - 122) / 4
        cl = ('rig', dict(x=hx - ez(0, 6, t), y=hy + ez(0, 14, t), th=-ez(90, 40, t), legs=KICK, arm=ARMS_BACK))
    if 112 <= f < 120: rv = ('hurt', ez(124, 127, (f - 112) / 4), True)
    if 112 <= f < 118: s['shake'] = rshake(2); fxs += [('my_burst', 122, 35, f - 112)]
    if 120 <= f < 124: rv = ('hurt', 127, True)
    if 124 <= f < 126: rv = ('bent', 127, True)
    # ---- 4. the close-up ---------------------------------------------------------------------------------------
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=(30,22,48), draw=_face, txt=CLOSE, box=(88, 6, W - 4, 58),
                              color=(255,220,70)); return s
    # ---- 5. West Coast Pop ---------------------------------------------------------------------------------------
    if 126 <= f < 216: rv = ('bent', ez(127, 112, (f - 126) / 12), True)
    if 126 <= f < 168: cl = ('fig', 'crouch', 100, GROUND, False)
    if 168 <= f < 186: cl = ('fig', pose_cycle(f, 'run1', 'run2', 3), ez(100, 24, (f - 168) / 18), GROUND, True)
    if 186 <= f < 192: cl = ('fig', 'crouch', 24, ROPES[1][0], False)
    if 192 <= f < 208:                                               # the springboard flip off the rope
        t = (f - 192) / 15; mid = 0.15 < t < 0.85
        cl = ('rig', dict(x=ez(26, 112, t), y=ROPES[1][0] - 9 - 22 * math.sin(math.pi * t) + ez(0, 4, t), th=ez(0, 360, t),
                          legs=TUCK if mid else KICK, arm=ARMS_FWD if mid else ARMS_UP))
    if 208 <= f < 216: cl = ('rig', dict(x=111, y=29 + (f - 208) // 3, th=0, legs=STRADDLE, arm=ARMS_UP))     # sat on his shoulders
    if 216 <= f < 224:                                               # he rolls the heel over, into the pin
        t = (f - 216) / 8; lie = (112 - ez(0, 6, t), ez(GROUND - 26, GROUND, t)); rv = None
        cl = ('rig', dict(x=ez(111, 106, t), y=ez(31, 49, t), th=ez(0, -60, t), legs=TUCK, arm=ARMS_FWD))
    if 224 <= f < 296: lie = (106, GROUND)
    if 224 <= f < 228: s['shake'] = rshake(2); fxs += [('my_spark', 106, GROUND - 4, f - 224)]
    if 224 <= f < 270: cl = ('fig', 'crouch', 112, GROUND, True)
    if 226 <= f < 296:                                               # the ref slides in and counts
        rx = ez(190, 132, (f - 226) / 8)
        rf = ('slap_dn' if 234 <= f < 264 and (f - 236) % 9 < 4 else 'slap_up' if f < 264 else 'stand', rx, True)
    # ---- 6. the bell, the arm raised, back to the neutral pose -------------------------------------------------
    if 270 <= f < 300: cl = ('fig', 'victory', 112, GROUND, False)
    if cue(f, BELL_AT, BELL): fxs += [('my_bell', 168, 38, (f - BELL_AT) // 3)]
    if 296 <= f < 336: rf = ('walk1' if (f // 4) % 2 else 'walk2', lerp(132, 215, (f - 296) / 40), False)
    if 296 <= f < 332: lie = (lerp(106, 230, (f - 296) / 36), GROUND)
    if 300 <= f < 326: cl = ('fig', pose_cycle(f, 'walk1', 'walk2', 4), ez(112, CX, (f - 300) / 26), GROUND, True)
    # ---- the text that stays up -------------------------------------------------------------------------------
    if cue(f, COUNT_AT, COUNT, extra=4):
        n = min(3, 1 + (f - COUNT_AT) // 9)
        fxs += [('caption', ' '.join(COUNT.split(' ')[:n]), {'box': (60, 4, 150, 24), 'max_scale': 3, 'color': (255,255,255), 'outline': INK})]
    if cue(f, BELL_AT, BELL): fxs += [('caption', BELL, {'box': (20, 6, 140, 24), 'max_scale': 3, 'color': (255,220,70), 'outline': INK})]
    # ---- put it on the stage ----------------------------------------------------------------------------------
    acts = []
    if rv: acts.append(actor(build('rival', rv[0]), rv[1], flip=rv[2], pal=RPAL))
    if lie: acts.append(actor(lying('rival'), lie[0], lie[1], pal=RPAL))
    if rf: acts.append(actor(build('ref', rf[0]), rf[1], flip=rf[2], pal=FPAL))
    if cl[0] == 'fig': acts.append(actor(build('claude', cl[1]), cl[2], cl[3], flip=cl[4], pal=CPAL))
    s['actors'] = acts
    s['fx'] += fxs
    if cl[0] == 'rig': s['fx'].append(('my_rig', cl[1]))
    return s

CLIPS = [clip('619', N_, clip_619)]
