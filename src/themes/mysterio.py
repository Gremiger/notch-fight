"""Rey Mysterio: Claude as the masked luchador (orange mask with a silver cross, orange-and-silver baggy pants, white
boots) in a wrestling ring seen from the side: blue apron, red / white / blue ropes, a dark crowd with camera flashes,
raised arms and a "619" sign.
Clip `619`: a huge bald heel charges, Claude dropkicks him and he ends draped over the middle rope, the crowd chants
6...1...9, Claude grabs the rope and swings his whole body through the gap, feet first, into the heel's hanging head
(hand-drawn swing poses and a motion arc). Close-up: the mask, the eyes narrowing ("BOOYAKA!"). Then the West Coast Pop
off the top rope onto the heel's shoulders, a roll into the pin, the ref's count and the bell, Claude with an arm
raised, back on the neutral pose."""
import math
from engine import *

THEME = 'mysterio'
N_ = 360                                                            # a multiple of 12: the ready bounce loops
CX = 58                                                             # Claude's corner of the ring
INK = (16,14,22)
ORANGE, SILVER, WHITE, SKIN = (217,119,87), (200,206,220), (245,245,250), (226,172,130)
ROPES = ((31,(210,50,60)), (43,(240,240,245)), (55,(60,100,220)))   # y of the top, middle, bottom rope and its colour
HX = 84                                                             # the x where Claude grabs the middle rope
CHANT = "6... 1... 9!"
COUNT = "1! 2! 3!"
BELL = "DING DING!"
CLOSE = "BOOYAKA!"
CHANT_AT, COUNT_AT, BELL_AT = 54, 236, 262
CLOSE_AT, CLOSE_LEN = 126, 40                                       # the close-up follows the kick

# ---- Claude and the ref, built from a pose (engine/people.py: figure(), POSES) --------------------------------
POSES = dict(POSES)
POSES.update({
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

_BODY = dict(w=28, h=26, c=13, legs=10, torso=7)                    # a 24 px person
CLAUDE = dict(_BODY, name='mysterio-claude', shorts='o', eyes=(0,2),
              leg=dict(color='o', stripe='v', boot='w', boot_rows=2, stand=(-2,2)),
              body=dict(color='s'), arm=dict(sleeve='s', hand='w', hand_w=2, shoulders=((-2,1),(2,1))), paint=dict(head=[_mask]))
REF = dict(_BODY, name='mysterio-ref', eyes=(0,2), leg=dict(color='p', boot='K'),
           body=dict(color='w'), arm=dict(sleeve='w', hand='s'), hair=['.KKKK.'], hair_x=-2, hair_y=0, paint=dict(body=[_stripes]))
CPAL = {'s':SKIN,'K':INK,'o':ORANGE,'v':SILVER,'w':WHITE,'p':(60,52,70),'k':INK,'f':SKIN,'j':SKIN}
FPAL = {'s':(226,184,150),'K':INK,'w':WHITE,'p':(30,30,36),'j':WHITE,'h':INK}

def build(who, pose):
    return figure({'claude': CLAUDE, 'ref': REF}[who], POSES[pose])

# ---- the heel, drawn limb by limb (he bends over the rope, hangs, lies on his back) ----------------------------
HSKIN, HDARK, HBLACK = (205,150,118), (165,112,88), (24,22,30)
HIP = GROUND - 13                                                   # his hips when he stands: 34 px of man
ST = (((-1,6.5),(-2,13)), ((1,6.5),(2,13)))
R1 = (((-3,6),(-7,12.5)), ((4,6),(6,13)))
R2 = (((3,6),(5,13)), ((-3,7),(-6,11)))
REEL = (((-3,6),(-6,12.5)), ((3,6),(4,13)))
REST = (((-2,5),(-2,10)), ((2,5),(3,10)))
CHARGE = (((4,3),(8,2)), ((5,1),(10,0)))
FLAIL = (((-4,-2),(-7,-6)), ((3,-3),(5,-8)))
HANGING = (((-1,5),(-1,10)), ((2,6),(2,11)))
HEEL = {'stand': (0, ST, REST), 'run1': (12, R1, CHARGE), 'run2': (12, R2, CHARGE), 'hurt': (-18, REEL, FLAIL),
        'drape': (100, ST, HANGING), 'snap': (62, ST, FLAIL), 'bent': (85, ST, HANGING), 'lie': (0, ST, REST)}

def heel_at(pose, x, y=HIP, th=0, b=None):
    """The parameters of the 'my_heel' effect: pose (HEEL), hips at (x, y), the whole body turned th degrees, the torso b."""
    p = HEEL[pose]; return dict(ox=x, oy=y, th=th, b=p[0] if b is None else b, legs=p[1], arms=p[2])

def heel(d, ox, oy, th, b, legs, arms):
    """The heel facing left: legs from the hips, the torso bent b degrees forward, a bald head, thick arms."""
    def T(o, q, ang):
        a = math.radians(ang); return (round(o[0] - (q[0] * math.cos(a) - q[1] * math.sin(a))), round(o[1] + q[0] * math.sin(a) + q[1] * math.cos(a)))
    P = lambda q: T((ox, oy), q, th)
    br = math.radians(b); tv = (math.sin(br), -math.cos(br))
    sh, hc = P((tv[0] * 11, tv[1] * 11)), P((tv[0] * 17, tv[1] * 17))
    PS = lambda q: (sh[0] + P(q)[0] - P((0, 0))[0], sh[1] + P(q)[1] - P((0, 0))[1])
    H = lambda q: T(hc, q, th + b)
    def limb(pts, wd, col): d.line(pts, fill=INK, width=wd + 2); d.line(pts, fill=col, width=wd)
    def arm(a, col):
        pts = [sh, PS(a[0]), PS(a[1])]; limb(pts, 4, col); d.ellipse([pts[2][0] - 2, pts[2][1] - 2, pts[2][0] + 2, pts[2][1] + 2], fill=HDARK, outline=INK)
    def leg(l, col):
        kn, ft = P(l[0]), P(l[1]); limb([P((0, 0)), kn, ft], 4, col)
        d.line([T((ox, oy), ((l[0][0] + l[1][0]) / 2, (l[0][1] + l[1][1]) / 2 + 1), th), ft], fill=HBLACK, width=5)
    arm(arms[0], HDARK); leg(legs[0], HDARK)
    limb([P((0, 0)), sh], 11, HSKIN)                                # the chest
    limb([P((0, -1)), P((0, 5))], 11, HBLACK)                       # the trunks
    leg(legs[1], HSKIN)
    d.ellipse([hc[0] - 6, hc[1] - 6, hc[0] + 6, hc[1] + 6], fill=INK); d.ellipse([hc[0] - 5, hc[1] - 5, hc[0] + 5, hc[1] + 5], fill=HSKIN)
    d.point(H((-2, -3)), fill=(232,186,150))                        # the shine on the bald head
    d.line([H((0.5, -2.5)), H((4.5, -0.5))], fill=INK, width=1)     # the scowl
    d.line([H((2.5, 0.5)), H((3, 0.5))], fill=INK, width=2)
    d.line([H((1.5, 3)), H((4, 2.5))], fill=INK)                    # the frown
    for q in ((4, 4.5), (4, 5.5), (3, 5.5), (3, 6.5)): d.point(H(q), fill=INK)      # the goatee
    arm(arms[1], HSKIN)

@fx('my_heel')
def _fx_heel(d, im, e, f): heel(d, **e[1])

# ---- the place ------------------------------------------------------------------------------------------
def _ring(d):
    for y in range(H):
        k = y / GROUND; d.line([0, y, W, y], fill=tuple(int(lerp(a, b, k)) for a, b in zip((14,12,30), (34,28,58))))
    rr = random.Random(619)
    for row, y in enumerate(range(15, 31, 5)):                      # the crowd: rows of heads, some with arms up
        col = (44 + row * 8, 36 + row * 7, 74 + row * 8)
        for x in range(-3 + row * 2, W, 6):
            hx, hy = x + rr.randint(-1, 1), y + rr.randint(-1, 1)
            if rr.random() < .22:
                d.line([hx + 2, hy + 1, hx + 2 + rr.randint(-2, 2), hy - 6], fill=(col[0] + 20, col[1] + 14, col[2] + 20), width=2)
            d.ellipse([hx, hy, hx + 4, hy + 4], fill=col); d.rectangle([hx - 1, hy + 4, hx + 5, hy + 8], fill=col)
    for lx in (30, 92, 154):                                        # the arena lights: a bar and a cone of light
        d.rectangle([lx - 8, 0, lx + 8, 2], fill=(230,230,200))
        for y in range(3, 20):
            half = 3 + (y - 3) // 2
            for x in range(lx - half, lx + half):
                if (x + y) % 2 == 0: d.point((x, y), fill=(60,56,84))
    d.line([157, 10, 157, 22], fill=(120,100,70)); d.rectangle([146, 4, 168, 13], fill=(240,236,222), outline=INK)
    text(d, '619', 150, 7, (200,40,50), shadow=None)                # the sign in the crowd
    d.line([22, 12, 22, 24], fill=(120,100,70)); d.rectangle([14, 6, 30, 12], fill=(250,210,60), outline=INK)
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
RS = 1.2                                                            # drawn a bit bigger than a figure

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

def swing_hip(phi, hd=11, sag=7):
    """Where the hips are when the body hangs from the middle rope and has swung phi degrees toward the heel."""
    a = math.radians(phi); return HX + hd * RS * math.sin(a), ROPES[1][0] + hd * RS * math.cos(a) + sag * math.sin(a)

@fx('my_arc')
def _fx_arc(d, im, e, f):
    """The motion arc of the feet swinging from the hang to the kick, drawn up to phi = e[1] degrees."""
    for k in range(24, int(e[1]) + 1, 3):
        a = math.radians(k); x = HX + 24.6 * math.sin(a); y = ROPES[1][0] + 24.6 * math.cos(a) + 7 * math.sin(a)
        d.point((round(x), round(y)), fill=(255,236,160) if k % 6 == 0 else (200,160,90))
        if k % 6 == 0: d.point((round(x), round(y) + 1), fill=(255,236,160))
        if k % 12 == 0: d.point((round(x) - 1, round(y) - 1), fill=(255,255,255))

# ---- the close-up: a luchador mask --------------------------------------------------------------------------
def _face(im, d, t, f):
    cx = int(lerp(50, 44, ease(t))); cy = 29
    d.polygon([(cx - 34, 64), (cx - 22, 53), (cx + 22, 53), (cx + 34, 64)], fill=SKIN, outline=INK)      # bare shoulders
    d.rectangle([cx - 9, 46, cx + 9, 58], fill=SKIN, outline=INK)                                        # the neck
    pts = [(cx-23,22),(cx-21,10),(cx-12,3),(cx,1),(cx+12,3),(cx+21,10),(cx+23,22),(cx+19,40),(cx+10,53),(cx,57),(cx-10,53),(cx-19,40)]
    d.polygon(pts, fill=ORANGE, outline=INK)
    d.polygon([(cx + (x - cx) * .9, cy + (y - cy) * .9) for x, y in pts], outline=SILVER)                 # the trim, a second colour
    d.polygon([(cx - 9, 44), (cx + 9, 44), (cx + 6, 52), (cx, 54), (cx - 6, 52)], fill=SKIN, outline=INK)   # the mouth and jaw opening
    d.line([cx - 4, 48, cx + 4, 48], fill=INK)
    d.polygon([(cx, 3), (cx - 4, 11), (cx + 4, 11)], fill=SILVER, outline=INK)                            # the arrow and cross down the middle
    d.rectangle([cx - 1, 11, cx + 1, 41], fill=SILVER); d.rectangle([cx - 7, 15, cx + 7, 17], fill=SILVER)
    k = lerp(1, .3, ease(min(1, t * 2.2)))                                                                # the eyes narrow
    for s in (-1, 1):
        wing = [(3,27),(9,33),(20,29),(25,16),(14,22),(5,22)]                                             # flame-shaped trims, up and out
        d.polygon([(cx + s * x, y) for x, y in wing], fill=WHITE, outline=INK)
        hole = [(5,27),(9,30),(17,27),(12,24),(6,24)]
        d.polygon([(cx + s * x, 27 + (y - 27) * k) for x, y in hole], fill=INK)
    for y in (36, 40, 44):                                                                                # the laces at the sides
        d.line([cx - 22, y, cx - 18, y + 1], fill=WHITE); d.line([cx + 22, y, cx + 18, y + 1], fill=WHITE)

# ---- the clip --------------------------------------------------------------------------------------------
def ready(f):                                                       # the neutral pose: it moves every 12 frames
    return pose_cycle(f, 'guard', 'guard2')

def clip_619(f):
    s = scene(f, THEME)
    s['under'].append(('flashes', {'area': (0, 12, W, 34), 'n': 4}))
    cl = ('fig', ready(f), CX, GROUND, False)        # Claude: a figure (pose, x, y, flip) or a rig (its parameters)
    hl = rf = None                                   # the heel (heel_at), the ref (pose, x, flip)
    rope = False; fxs = []
    # ---- 1. the heel charges, Claude dropkicks him onto the ropes ------------------------------------------
    if 18 <= f < 36: hl = heel_at(pose_cycle(f, 'run1', 'run2', 3), lerp(215, 104, (f - 18) / 18))
    if 30 <= f < 31: cl = ('fig', 'crouch', 62, GROUND, False)
    if 31 <= f < 38:
        t = (f - 31) / 6
        cl = ('rig', dict(x=ez(64, 88, t), y=ez(47, 43, t), th=-82, legs=KICK, arm=ARMS_BACK))
    if 38 <= f < 43:                                                 # falls to the mat
        t = (f - 38) / 5; cl = ('rig', dict(x=ez(88, 86, t), y=ez(43, 54, t), th=ez(-82, -40, t), legs=KICK, arm=ARMS_BACK))
    if 43 <= f < 48: cl = ('fig', 'crouch', 88, GROUND, False)
    if 48 <= f < 62: cl = ('fig', pose_cycle(f, 'walk1', 'walk2', 3), ez(88, CX, (f - 48) / 14), GROUND, True)
    if 36 <= f < 48: hl = heel_at('hurt', ez(104, 126, (f - 36) / 10))
    if 48 <= f < 112: hl = heel_at('drape', 126); rope = True; fxs += [('my_stars', 110, 38)]          # hanging over the middle rope
    if 36 <= f < 40: s['shake'] = rshake(1); fxs += [('my_burst', 99, 40, f - 36)]
    # ---- 2. the chant ------------------------------------------------------------------------------------------
    if cue(f, CHANT_AT, CHANT, extra=14):
        n = min(3, 1 + (f - CHANT_AT) // 10)
        fxs += [('caption', ' '.join(CHANT.split(' ')[:n]), {'box': (10, 2, W - 10, 24), 'max_scale': 3, 'color': (255,220,70), 'outline': INK})]
    # ---- 3. the 619: run, grab the rope, swing through the gap, kick ----------------------------------------
    if 76 <= f < 90: cl = ('fig', pose_cycle(f, 'run1', 'run2', 3), ez(CX, 80, (f - 76) / 14), GROUND, False)
    if 90 <= f < 98: cl = ('fig', 'jump', ez(80, HX, (f - 90) / 8), ez(GROUND, 56, (f - 90) / 8), False)
    SW = ((98, 15, TUCK, 8), (104, 45, KICK, 10), (110, 72, KICK, 11), (116, 90, KICK, 11))   # swing poses: (the frame it starts, phi, legs, hips' distance)
    for i, (a, phi, legs, hd) in enumerate(SW):
        if a <= f < (SW[i + 1][0] if i + 1 < len(SW) else 122):
            hx, hy = swing_hip(phi, hd)
            cl = ('rig', dict(x=hx, y=hy, th=-phi, legs=legs, arm=ARMS_BACK, hand=(HX, ROPES[1][0] - 1)))
    if 98 <= f < 122: fxs += [('my_arc', min(90, (f - 98) * 5))]
    if 122 <= f < 126:
        hx, hy = swing_hip(90); t = (f - 122) / 4
        cl = ('rig', dict(x=hx - ez(0, 6, t), y=hy + ez(0, 7, t), th=-ez(90, 40, t), legs=KICK, arm=ARMS_BACK))
    if 112 <= f < 120: hl = heel_at('snap', ez(126, 129, (f - 112) / 4)); rope = True       # the kick snaps his head up
    if 112 <= f < 118: s['shake'] = rshake(2); fxs += [('my_burst', 109, 48, f - 112)]
    if 120 <= f < 126: hl = heel_at('drape', 128); rope = True
    # ---- 4. the close-up ---------------------------------------------------------------------------------------
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=(30,22,48), draw=_face, txt=CLOSE, box=(94, 6, W - 4, 58),
                              color=(255,220,70)); return s
    # ---- 5. West Coast Pop ---------------------------------------------------------------------------------------
    if 126 <= f < 216: hl = heel_at('bent', ez(128, 122, (f - 126) / 12))
    if 126 <= f < 168: cl = ('fig', 'crouch', 90, GROUND, False)
    if 168 <= f < 186: cl = ('fig', pose_cycle(f, 'run1', 'run2', 3), ez(90, 24, (f - 168) / 18), GROUND, True)
    if 186 <= f < 194: cl = ('fig', 'crouch', 24, ROPES[0][0], False)                   # 1. crouched on the top rope
    if 194 <= f < 206:                                               # 2. the flip through the air
        t = (f - 194) / 11
        cl = ('rig', dict(x=ez(26, 114, t), y=ROPES[0][0] - 10 + 6 * t - 15 * math.sin(math.pi * t), th=ez(0, 360, t),
                          legs=TUCK, arm=ARMS_FWD))
    if 206 <= f < 216: cl = ('rig', dict(x=113, y=36 + (f - 206) // 5, th=0, legs=STRADDLE, arm=ARMS_UP))     # 3. sat on his shoulders
    if 216 <= f < 220:                                               # he rolls the heel over: 1. tipping back...
        hl = heel_at('bent', 118, 44, th=-35, b=40); cl = ('rig', dict(x=112, y=36, th=-25, legs=TUCK, arm=ARMS_FWD))
    if 220 <= f < 224:                                               # ...2. nearly flat, Claude riding him down
        hl = heel_at('lie', 108, 50, th=-72, b=0); cl = ('rig', dict(x=109, y=42, th=-60, legs=TUCK, arm=ARMS_FWD))
    if 224 <= f < 296: hl = heel_at('lie', 104, 52, th=-90, b=0)                         # on his back
    if 224 <= f < 228: s['shake'] = rshake(2); fxs += [('my_burst', 104, GROUND - 3, f - 224)]
    if 224 <= f < 270: cl = ('fig', 'crouch', 112, 47, True)
    if 226 <= f < 296:                                               # the ref slides in and counts
        rx = ez(190, 138, (f - 226) / 8)
        rf = ('slap_dn' if 234 <= f < 264 and (f - 236) % 9 < 4 else 'slap_up' if f < 264 else 'stand', rx, True)
    # ---- 6. the bell, the arm raised, back to the neutral pose -------------------------------------------------
    if 270 <= f < 300: cl = ('fig', 'victory', 112, GROUND, False)
    if cue(f, BELL_AT, BELL): fxs += [('my_bell', 168, 38, (f - BELL_AT) // 3)]
    if 296 <= f < 336: rf = ('walk1' if (f // 4) % 2 else 'walk2', lerp(138, 215, (f - 296) / 40), False)
    if 296 <= f < 332: hl = heel_at('lie', lerp(104, 230, (f - 296) / 36), 52, th=-90, b=0)
    if 300 <= f < 326: cl = ('fig', pose_cycle(f, 'walk1', 'walk2', 4), ez(112, CX, (f - 300) / 26), GROUND, True)
    # ---- the text that stays up -------------------------------------------------------------------------------
    if cue(f, COUNT_AT, COUNT, extra=4):
        n = min(3, 1 + (f - COUNT_AT) // 9)
        fxs += [('caption', ' '.join(COUNT.split(' ')[:n]), {'box': (60, 4, 150, 24), 'max_scale': 3, 'color': (255,255,255), 'outline': INK})]
    if cue(f, BELL_AT, BELL): fxs += [('caption', BELL, {'box': (20, 6, 140, 24), 'max_scale': 3, 'color': (255,220,70), 'outline': INK})]
    # ---- put it on the stage ----------------------------------------------------------------------------------
    acts = []
    if rf: acts.append(actor(build('ref', rf[0]), rf[1], flip=rf[2], pal=FPAL))
    if cl[0] == 'fig': acts.append(actor(build('claude', cl[1]), cl[2], cl[3], flip=cl[4], pal=CPAL))
    s['actors'] = acts
    if hl: s['fx'].append(('my_heel', hl))
    if rope: s['fx'].append(('my_rope', 96, 134))
    if cl[0] == 'rig': s['fx'].append(('my_rig', cl[1]))
    s['fx'] += fxs
    return s

CLIPS = [clip('619', N_, clip_619)]
