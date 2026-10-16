"""The Emperor's New Groove: Claude as Kronk (huge, barrel-chested, a tiny head with a square jaw and a
big grin, black flat-top, gold-and-red Inca tunic, Claude-orange headband and belt) in Yzma's secret lab
(purple and green stone, Inca carvings, two levers on the wall, a trapdoor, a bubbling cauldron).
Clip `lever`: Yzma, stick-thin on the trapdoor, points: "PULL THE LEVER, KRONK!" Kronk reaches, dithers
between the skull lever and the plain one, pulls the plain one: CLUNK. The trapdoor opens under Yzma, she
hangs in the air with a deadpan look, then drops: "WRONG LEVEEEER!" Close-up of Kronk scratching his head:
"WHY DO WE EVEN HAVE THAT LEVER?" Yzma rises out of the pit on a little rollercoaster cart, soaking wet, an
alligator clamped on her headdress, and glares; she shakes it off, hops off the cart, the cart sinks, the
trapdoor closes and she walks back to her spot. Back on the neutral pose."""
import math
from engine import *
from engine.people import put, seg, blank, to_sprite, _row

THEME = 'groove'
N_ = 336                                                            # idle cycles of 8 and 16 frames divide it
CX = 98                                                            # Claude (Kronk), next to the levers
YX = 38                                                             # Yzma, on the trapdoor
INK = (16,14,22)
LINE1 = "PULL THE LEVER, KRONK!"
CLOSE = "WHY DO WE EVEN HAVE THAT LEVER?"
CLUNK = "CLUNK!"
LINE1_AT = 10
WRONG_AT = 126
CLOSE_AT, CLOSE_LEN = 158, 52
PINK, GOLD = (255,160,230), (255,226,110)

WRONG = "WRONG LEVEEEER!"

def mix(a, b, k): return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
def sm(f, a, b): return max(0.0, min(1.0, (f - a) / (b - a)))

# ---- Kronk, built from a pose (engine/people.py: figure(), POSES) ----------------------------------------
GW, GH, C = 42, 36, 14
TY = GROUND - 12 - 12                                                # screen row of his shoulders (34)
XO = C - GW // 2                                                    # screen x of his hand = CX + XO + its column
def _kface(g, at):
    """A tiny head with a square jaw, beady eyes that dart, a big grin."""
    c, hy, sh, fl = at['c'], at['hy'], at['sh'], at['flags']
    for y in range(hy, hy + 6):
        w = 3 if y < hy + 4 else 4
        for x in range(c - w, c + w + 1): put(g, x + sh(y), y, 's')
    for x in (c - 2, c - 1, c + 1, c + 2): put(g, x + sh(hy + 1), hy + 1, 'W')
    for x in {'r': (c - 1, c + 2), 'l': (c - 2, c + 1)}[fl.get('look', 'r')]: put(g, x + sh(hy + 1), hy + 1, 'K')
    if fl.get('mood', 'smile') == 'smile':
        for x in range(c - 2, c + 3): put(g, x + sh(hy + 3), hy + 3, 'W')
        put(g, c - 3 + sh(hy + 3), hy + 3, 'm'); put(g, c + 3 + sh(hy + 3), hy + 3, 'm')
    else:
        for y in (hy + 3, hy + 4):
            for x in (c, c + 1): put(g, x + sh(y), y, 'm')
def _kskirt(g, at):
    c, hip = at['c'], at['hip']
    for y in range(hip + 1, hip + 4):
        for x in range(c - 7, c + 8): put(g, x, y, 'G' if y == hip + 3 else 'j')
    for x in range(c - 7, c + 8, 2): put(g, x, hip + 2, 'o')
def _kchest(g, at):
    c, ty, hip = at['c'], at['ty'], at['hip']
    o = at['sh']
    for dy, w in ((2, 1), (3, 2), (4, 3), (5, 2), (6, 1)):
        for x in range(c - w, c + w + 1): put(g, x + o(ty + dy), ty + dy, 'G')
def _karms(g, at):
    """Thicker arms: a second line beside each (he is huge)."""
    c, ty, T, sh = at['c'], at['ty'], at['T'], at['sh']
    be, bh, fe, fh = at['pose'][:4]
    for e, h, front in ((be, bh, False), (fe, fh, True)):
        pts = [(c + (7 if front else -7) + sh(ty + 1), ty + 1), (c + e[0] + sh(ty), ty + _row(e[1], T)),
               (c + h[0] + sh(ty), ty + _row(h[1], T))]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            dx, dy = (0, 1) if abs(x1 - x0) >= abs(y1 - y0) else (1, 0)
            seg(g, x0 + dx, y0 + dy, x1 + dx, y1 + dy, 's')
CLAUDE = dict(name='groove-kronk', w=GW, h=GH, c=C, legs=12, torso=12, head=6, torso_cols=(-7, 7), eyes=(),
              body=dict(color='j', top='G', belt='o', hip='G'),
              arm=dict(sleeve='s', hand='s', hand_w=2, shoulders=((-7, 1), (7, 1))),
              leg=dict(color='s', boot='b', boot_rows=1, gap=-3, stand=(-2, 2)),
              hair=['hhhhhhh', 'hhhhhhh', 'ooooooo'], hair_x=-3, hair_y=2,
              paint=dict(legs=[_kskirt], body=[_kchest], head=[_kface], end=[_karms]))
CPAL = {'s':(190,128,86),'K':INK,'h':(22,18,28),'j':(196,46,46),'G':(240,192,64),'o':(217,119,87),'b':(116,74,46),
        'W':(246,246,246),'m':(60,24,24),'k':INK,'p':(60,52,70)}

def kp(hx, hy, lean=0, legs='stand'):
    """A Kronk pose with his front hand at (hx, hy) from (c, shoulders row): the elbow falls in between."""
    return ((-8, 5), (-8, 10), (round(7 + (hx - 7) * 0.45), round(1 + (hy - 1) * 0.45) + 3), (hx, hy), lean, legs)
POSES = dict(POSES)
POSES.update(kstand=kp(9, 10), kstand2=kp(9, 9))

def build(pose, **flags):
    return figure(CLAUDE, POSES[pose] if isinstance(pose, str) else pose, **flags)

# ---- Yzma: tall, thin, a feathered headdress, long bony arms (a sprite grid, outlined by the engine) -----
YW, YH, YC = 38, 40, 19
YPAL = {'P':(110,54,160),'p':(70,34,108),'V':(238,116,186),'U':(172,104,228),'g':(244,198,70),'y':(196,150,190),
        'Y':(150,106,150),'e':(70,90,235),'w':(246,246,246),'k':(20,14,26),'r':(204,40,80),'b':(150,210,255),'D':(60,50,90)}
_yz_cache = {}
def yz_rows(arm, eyes, mouth, wet, tap, sway, sweat):
    key = (arm, eyes, mouth, wet, tap, sway, sweat)
    if key in _yz_cache: return _yz_cache[key]
    g = blank(YW, YH); c = YC
    def R(x0, y0, x1, y1, ch):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1): put(g, xx, yy, ch)
    def A(pts, ch='y'):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]): seg(g, x0, y0, x1, y1, ch)
    R(c - 4, 38, c - 2, 39, 'k'); R(c + 1, 38 - tap, c + 3, 39 - tap, 'k')       # shoes (one taps)
    for y in range(19, 38):                                                        # the dress
        half = round(3 + 4.5 * (y - 19) / 18)
        R(c - half, y, c + half, y, 'P'); put(g, c - half, y, 'p'); put(g, c - half + 1, y, 'p')
        if y % 4 == 1: put(g, c + 1, y, 'p')
    R(c - 7, 37, c + 7, 37, 'V'); R(c - 6, 36, c + 6, 36, 'g')
    R(c - 3, 18, c + 3, 19, 'p'); put(g, c - 4, 17, 'V'); put(g, c + 4, 17, 'V'); R(c - 1, 16, c, 17, 'y')   # collar, neck
    for y in range(9, 16):                                                         # the long face
        half = 3 if y <= 12 else (2 if y <= 14 else 1)
        R(c - half, y, c + half, y, 'y')
    R(c - 3, 9, c - 3, 12, 'Y'); put(g, c + 4, 12, 'y'); put(g, c + 4, 13, 'y'); put(g, c + 5, 13, 'y')   # the nose
    R(c - 3, 10, c + 3, 10, 'e')                                                   # the eye shadow
    if eyes == 'shut': R(c - 3, 11, c - 1, 11, 'k'); R(c + 1, 11, c + 3, 11, 'k'); pl = []
    elif eyes == 'wide': R(c - 3, 10, c - 1, 12, 'w'); R(c + 1, 10, c + 3, 12, 'w'); pl = [(c - 2, 11), (c + 2, 11)]
    else:
        R(c - 3, 11, c - 1, 12, 'w'); R(c + 1, 11, c + 3, 12, 'w')
        pl = {'fwd': [(c - 1, 11), (c + 3, 11)], 'down': [(c - 1, 12), (c + 3, 12)], 'cam': [(c - 2, 12), (c + 2, 12)],
              'glare': [(c - 1, 12), (c + 3, 12)]}[eyes]
    for x, y in pl: put(g, x, y, 'k')
    if eyes == 'glare':                                                            # heavy lids and angry brows
        R(c - 3, 11, c - 1, 11, 'k'); R(c + 1, 11, c + 3, 11, 'k'); put(g, c - 2, 10, 'k'); put(g, c - 1, 10, 'k')
        put(g, c + 1, 10, 'k'); put(g, c + 2, 10, 'k'); put(g, c - 3, 9, 'k'); put(g, c + 3, 9, 'k')
    put(g, c - 4, 11, 'k'); put(g, c + 4, 11, 'k'); put(g, c - 4, 10, 'k')       # the lashes
    if mouth == 'shut': R(c - 1, 14, c + 1, 14, 'r')
    elif mouth == 'frown': R(c - 1, 14, c + 1, 14, 'r'); put(g, c - 2, 14, 'k'); put(g, c + 2, 14, 'k')
    elif mouth == 'open': R(c - 1, 14, c + 1, 15, 'k'); R(c - 1, 14, c + 1, 14, 'r'); put(g, c, 15, 'V')
    elif mouth == 'wide': R(c - 2, 13, c + 2, 15, 'k'); R(c - 1, 13, c + 1, 13, 'w'); put(g, c, 15, 'r')
    elif mouth == 'teeth': R(c - 2, 14, c + 2, 14, 'w'); R(c - 1, 15, c + 1, 15, 'w'); put(g, c, 14, 'k'); put(g, c, 15, 'k')
    wetl = wet > 0
    s = sway
    R(c - 5 + s, 8, c + 5 + s, 8, 'g'); R(c - 5 + s, 7, c + 5 + s, 7, 'V'); put(g, c + s, 7, 'w')      # headdress band
    for x in range(c - 5, c + 6):
        hgt = 6 - abs(x - c) // 2 - (1 if (x - c) % 2 else 0)
        if wetl: hgt = max(1, hgt // 2)
        R(x + s, 7 - hgt, x + s, 6, ('U', 'V', 'P')[(x - c) % 3])
    if wetl:
        for yy in range(9, 17): put(g, c - 4, yy, 'D'); put(g, c + 4, yy, 'D') if yy < 12 else None
        for yy in range(7, 13): put(g, c - 6 + s, yy, 'U'); put(g, c + 6 + s, yy, 'P')
    if sweat: put(g, c + 5, 8 + sweat, 'b'); put(g, c + 5, 9 + sweat, 'b')
    put(g, c - 3, 20, 'p'); put(g, c + 3, 20, 'p')
    L, F = (c - 3, 20), (c + 3, 20)
    if arm == 'point': A([L, (c - 7, 25), (c - 4, 29)]); A([F, (c + 15, 17)]); A([(c + 15, 17), (c + 17, 16)]); put(g, c + 18, 16, 'r')
    elif arm == 'cross': A([L, (c - 4, 25), (c + 3, 26)]); A([F, (c + 4, 25), (c - 3, 27)])
    elif arm == 'clasp': A([L, (c - 4, 25), (c, 28)]); A([F, (c + 4, 25), (c + 1, 28)])
    elif arm == 'up': A([L, (c - 9, 13), (c - 11, 6)]); A([F, (c + 9, 13), (c + 11, 6)]); R(c - 12, 4, c - 10, 6, 'y'); R(c + 10, 4, c + 12, 6, 'y')
    elif arm == 'fist': A([L, (c - 7, 25), (c - 4, 29)]); A([F, (c + 9, 16), (c + 8, 11)]); R(c + 7, 9, c + 9, 11, 'y')
    else: A([L, (c - 7, 25), (c - 4, 29)]); A([F, (c + 7, 25), (c + 4, 29)])      # hands on hips
    _yz_cache[key] = [''.join(r) for r in g]; return _yz_cache[key]

def stretched(rows, k):
    n = max(1, round(len(rows) * k)); return S([rows[min(len(rows) - 1, int(i / k))] for i in range(n)])

_GA = S(["." * 26] * 9)
def gator(tail):
    g = blank(26, 9)
    def R(x0, y0, x1, y1, ch):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1): put(g, xx, yy, ch)
    R(6, 2, 19, 6, 'G'); R(6, 6, 19, 6, 'g'); R(17, 2, 25, 4, 'G'); R(18, 5, 25, 6, 'G'); R(19, 4, 25, 4, 'k')
    for x in range(20, 26, 2): put(g, x, 4, 'w')
    put(g, 18, 1, 'y'); put(g, 19, 1, 'k'); put(g, 17, 1, 'G')
    for x in (8, 10, 12, 14): put(g, x, 1, 'H')
    if tail: R(0, 2, 5, 3, 'G'); R(0, 1, 1, 1, 'G')
    else: R(0, 4, 5, 5, 'G'); R(0, 6, 1, 7, 'G')
    for x in (9, 16): R(x, 7, x + 1, 8, 'H')
    return to_sprite(g)
GATOR = [gator(0), gator(1)]
GPAL = {'G':(74,152,62),'H':(40,104,48),'g':(176,204,112),'w':(250,250,240),'y':(250,230,70),'k':INK}

def _cart():
    g = blank(28, 12)
    def R(x0, y0, x1, y1, ch):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1): put(g, xx, yy, ch)
    R(0, 2, 27, 9, 'T'); R(0, 2, 27, 2, 'g'); R(0, 5, 27, 5, 'g'); R(0, 8, 27, 9, 't')
    put(g, 27, 3, '.'); put(g, 27, 2, '.'); put(g, 27, 9, '.')
    for x in (4, 20): R(x, 9, x + 3, 11, 'k'); put(g, x + 1, 10, 'W'); put(g, x + 2, 10, 'W')
    return to_sprite(g)
CART = _cart()
CPAL2 = {'T':(196,52,52),'t':(130,28,40),'g':(244,198,70),'k':INK,'W':(190,194,210)}

# ---- the place: Yzma's lab -----------------------------------------------------------------------------
P1, P2, PULL = 113, 122, 0.8                                        # the lever pivots; how far lever 2 goes (radians)
PIVY, LEVL = 46, 13
DX0, DX1 = 21, 55                                                   # the trapdoor (a trapezoid on the floor, rows 53..62)
FLOOR_Y, CLIP_Y = 51, 62
def _lab(d):
    for y in range(GROUND + 1):
        k = y / GROUND; d.line([0, y, W, y], fill=tuple(int(lerp(a, b, k)) for a, b in zip((38,26,58), (22,42,44))))
    for r, y in enumerate(range(12, GROUND, 12)):                   # stone blocks
        d.line([0, y, W, y], fill=(24,18,36))
        for x in range(6 * (r % 2), W, 18): d.line([x, y, x, y + 12], fill=(24,18,36))
    for x in range(0, W, 10):                                       # an Inca stepped frieze
        d.line([x, 10, x, 5, x + 5, 5, x + 5, 7, x + 8, 7, x + 8, 10], fill=(70,126,110))
    d.rectangle([0, 3, W, 4], fill=(40,30,60)); d.line([0, 11, W, 11], fill=(24,18,36))
    d.ellipse([60, 17, 88, 45], outline=(70,126,110)); d.ellipse([65, 22, 83, 40], outline=(150,120,60))   # the sun carving
    for a in range(8):
        ax, ay = 74 + 13 * math.cos(a * math.pi / 4), 31 + 13 * math.sin(a * math.pi / 4)
        d.line([74 + 15 * math.cos(a * math.pi / 4), 31 + 15 * math.sin(a * math.pi / 4), ax, ay], fill=(150,120,60))
    d.rectangle([70, 27, 72, 29], fill=(150,120,60)); d.rectangle([76, 27, 78, 29], fill=(150,120,60)); d.line([70, 36, 78, 36], fill=(150,120,60))
    d.rectangle([107, 12, 133, 50], fill=(48,42,64), outline=(14,10,22)); d.rectangle([109, 14, 131, 48], outline=(70,62,92))
    for px in (P1, P2):
        d.rectangle([px - 1, 32, px + 1, 46], fill=(14,10,20)); d.ellipse([px - 3, 43, px + 3, 49], fill=(112,112,132), outline=(14,10,20))
    d.ellipse([110, 16, 116, 22], fill=(232,228,200)); d.rectangle([111, 22, 115, 24], fill=(232,228,200))   # the skull
    d.rectangle([111, 18, 112, 19], fill=INK); d.rectangle([114, 18, 115, 19], fill=INK); d.point((113, 21), fill=INK)
    d.line([112, 24, 112, 24], fill=INK); d.line([114, 24, 114, 24], fill=INK)
    for x in range(111, 132, 3): d.point((x, 13), fill=(80,200,120))
    d.rectangle([0, 14, 6, GROUND], fill=(34,26,50), outline=(20,14,30)); d.rectangle([2, 22, 4, 26], fill=(70,126,110))   # a carved pillar
    d.rectangle([146, 28, 183, 30], fill=(100,66,52)); d.rectangle([146, 41, 183, 43], fill=(100,66,52))        # shelves
    for i, (bx, col, hh) in enumerate(((149,(120,230,110),7),(155,(240,110,190),9),(162,(120,160,250),6),(168,(180,110,240),8),(176,(120,230,110),10))):
        for sy in (28, 41):
            d.rectangle([bx, sy - hh, bx + 3, sy - 1], fill=col if (i + sy) % 3 else (230,200,90), outline=(20,14,30)); d.point((bx + 1, sy - hh - 1), fill=(140,100,60))
    d.ellipse([150, 44, 176, 60], fill=(26,22,32)); d.rectangle([152, 56, 154, 59], fill=(26,22,32)); d.rectangle([172, 56, 174, 59], fill=(26,22,32))   # the cauldron
    d.ellipse([151, 43, 175, 50], fill=(88,224,100), outline=(130,130,150))
    d.rectangle([0, FLOOR_Y, W, H], fill=(46,36,58)); d.line([0, FLOOR_Y, W, FLOOR_Y], fill=(76,60,92))
    d.line([0, FLOOR_Y + 1, W, FLOOR_Y + 1], fill=(30,22,40)); d.line([0, 57, W, 57], fill=(40,31,52)); d.line([0, 62, W, 62], fill=(36,28,46))
    for x in range(8, W, 24): d.line([x, FLOOR_Y + 2, x - 3, 57], fill=(36,28,46)); d.line([x + 12, 58, x + 14, 62], fill=(36,28,46))
register_bg(THEME, lambda v: (v+30,v+24,v+44), decor=_lab)

@fx('gr_lab')
def _fx_lab(d, im, e, f):
    """The living lab: green torch flames, the cauldron's bubbles and steam (all loop-safe), the levers."""
    ph = loop.phase(f, 24)
    for i in range(5):                                              # bubbles rising from the pot
        t = (ph + i * 0.2) % 1; bx = 156 + i * 4 + (1 if i % 2 else 0); by = 46 - t * 14
        r = 1 + (i % 2); d.ellipse([bx - r, by - r, bx + r, by + r], outline=(150,255,160))
        if t > 0.9: d.point((bx, by - 2), fill=(200,255,200))
    for i in range(3):                                              # steam
        t = (ph + i * 0.33) % 1; d.point((160 + i * 6 + int(2 * math.sin(6.28 * (t + i))), 40 - int(t * 8)), fill=(70,130,90))
    rr = loop.rng(loop.frame(f) // 2, salt=3)
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse([-8, 4, 22, 30], fill=40)
    im.paste((90, 240, 130), (0, 0), g.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(im)
    d.rectangle([2, 30, 4, 32], fill=(60,50,70))
    for _ in range(3):
        h = rr.randint(4, 7); dx = rr.randint(-1, 1)
        d.polygon([(2 + dx, 30), (3 + dx, 30 - h), (5 + dx, 30)], fill=rr.choice([(150,255,110), (60,220,110)]))
    a1, a2 = e[1], e[2]
    for px, a, ball in ((P1, a1, (236,232,200)), (P2, a2, (230,70,70))):
        tx, ty = px - LEVL * math.sin(a), PIVY - LEVL * math.cos(a)
        d.line([px, PIVY, tx, ty], fill=(20,16,26), width=4); d.line([px, PIVY, tx, ty], fill=(168,168,190), width=2)
        d.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill=(20,16,26)); d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=ball)

def _trap(p):
    """The two halves of the trapdoor as polygons, p 0 shut .. 1 open (each swings down on its outer hinge)."""
    k = 1 - 0.86 * p
    L = [(26, 53), (26 + 12 * k, 53), (21 + 17 * k, 62), (21, 62)]; Rr = [(50, 53), (50 - 12 * k, 53), (55 - 17 * k, 62), (55, 62)]
    return L, Rr

@fx('gr_door')
def _fx_door(d, im, e, f):
    """('gr_door', p): the trapdoor, p 0 shut .. 1 open; a green glow comes up out of the pit."""
    p = e[1]
    d.polygon([(26, 53), (50, 53), (55, 62), (21, 62)], fill=(10,8,16))
    if p > 0.2:
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(24, 55), (52, 55), (46, 24), (30, 24)], fill=int(70 * p))
        im.paste((90, 240, 130), (0, 0), m.filter(ImageFilter.GaussianBlur(5))); d = ImageDraw.Draw(im)
        d.rectangle([32, 59, 44, 61], fill=(40,120,70))
    for poly, ring in zip(_trap(p), ((0, 1), (1, 0))):
        d.polygon(poly, fill=(116,78,52), outline=(30,20,20))
        d.line([poly[0], poly[1]], fill=(170,124,80))
        for t in (0.35, 0.7): d.line([(poly[0][0] + (poly[3][0] - poly[0][0]) * t, 53 + 9 * t), (poly[1][0] + (poly[2][0] - poly[1][0]) * t, 53 + 9 * t)], fill=(84,56,40))
    if p < 0.5:
        for x in (35, 40): d.rectangle([x, 56, x + 1, 57], fill=(244,198,70))

@fx('gr_yz')
def _fx_yz(d, im, e, f):
    """('gr_yz', {yz: {...} | None, cart: (x, bottom) | None, gator: {...} | None}): Yzma, her cart and the gator."""
    o = e[1]; yz = o.get('yz'); cart = o.get('cart')
    if cart:
        cx, cb = cart
        for rx in (cx - 8, cx + 8): d.line([rx, 55, rx, 61], fill=(120,120,146))
    keep = im.crop((0, CLIP_Y, W, H))                              # what is below the pit's lip stays: she falls INTO it
    if yz:
        wet = round(yz['wet'] * 4) / 4
        rows = yz_rows(yz['arm'], yz['eyes'], yz['mouth'], wet, yz['tap'], yz['sway'], yz['sweat'])
        pal = dict(YPAL)
        if wet: pal.update({k: tuple(int(YPAL[k][i] * (1 - 0.35 * wet) + (30, 40, 120)[i] * 0.35 * wet) for i in range(3)) for k in 'PUVp'})
        draw(im, stretched(rows, yz.get('stretch', 1.0)), yz['x'], yz['feet'], False, pal=pal)
        d = ImageDraw.Draw(im)
        if wet:
            for i in range(4):
                dy = (loop.frame(f) * 2 + i * 5) % 11
                d.point((yz['x'] - 6 + i * 4, yz['feet'] - 2 + dy), fill=(150,210,255)); d.point((yz['x'] - 6 + i * 4, yz['feet'] - 3 + dy), fill=(96,160,230))
    if cart: draw(im, CART, cart[0], cart[1], False, pal=CPAL2)
    im.paste(keep, (0, CLIP_Y)); d = ImageDraw.Draw(im)
    g = o.get('gator')
    if g: draw(im, GATOR[g['tail']], g['x'], g['y'], g.get('flip', False), pal=GPAL)

@fx('gr_spray')
def _fx_spray(d, im, e, f):
    """('gr_spray', x, y, k): water flung off in all directions."""
    _, x, y, k = e
    for i in range(14):
        a = i * 0.9 + 0.3; r = 3 + k * (1.6 + (i % 3) * 0.6)
        d.point((int(x + r * math.cos(a)), int(y + r * math.sin(a) * 0.7 + 0.04 * k * k)), fill=(170,225,255) if i % 2 else (110,170,240))

@fx('gr_splash')
def _fx_splash(d, im, e, f):
    """('gr_splash', k): a splash climbing out of the pit, far below."""
    k = e[1]
    for i in range(7):
        a = -1.2 + i * 0.4; r = k * 1.2
        d.point((int(38 + r * math.cos(a) * 2), int(58 + r * math.sin(a) * 2.5 + 0.35 * k * k)), fill=(170,230,255) if i % 2 else (110,230,150))

@fx('gr_spark')
def _fx_spark(d, im, e, f):
    _, x, y, k = e; spark(d, int(x), int(y), 3 + int(k))

@fx('gr_wrong')
def _fx_wrong(d, im, e, f):
    """('gr_wrong', k): WRONG LEVEEEER! drawn once and stretched sideways as she falls (k: 0..1)."""
    key = (255, 0, 255); t = Image.new('RGB', (120, 16), key)
    text_block(t, WRONG, (0, 0, 120, 16), PINK, 2, shadow=None, outline=INK)
    w = int(120 + 62 * e[1]); t = t.resize((w, 16), Image.NEAREST)
    m = t.convert('RGB').point(lambda v: v).split(); mask = Image.eval(m[1], lambda v: 0 if v == 0 else 255)
    im.paste(t, ((W - w) // 2, 2), mask)

# ---- the close-up: Kronk, puzzled, scratching his head ----------------------------------------------------
def _face(im, d, t, f):
    SK, DK = (190,128,86), (150,98,66)
    k = f - CLOSE_AT; cx = 40 + (1 if (k // 6) % 2 else 0)
    for y in range(H): d.line([0, y, 78, y], fill=(int(36 - y * 0.2), int(26 + y * 0.3), int(54 - y * 0.2)))
    d.rectangle([cx - 25, 3, cx + 25, 18], fill=(22,18,28), outline=INK); d.rectangle([cx - 14, 0, cx + 14, 4], fill=(22,18,28))       # the flat-top
    d.rectangle([cx - 27, 16, cx + 27, 23], fill=(217,119,87), outline=INK); d.rectangle([cx - 2, 17, cx + 2, 22], fill=(240,192,64))   # the headband
    d.rectangle([cx - 28, 30, cx - 22, 40], fill=SK, outline=INK); d.rectangle([cx + 22, 30, cx + 28, 40], fill=SK, outline=INK)       # ears
    d.rectangle([cx - 24, 23, cx + 24, 59], fill=SK, outline=INK)                                                                    # the square jaw
    look = (k // 8) % 2 * 2 - 1
    for ex in (cx - 13, cx + 7):
        d.rectangle([ex, 31, ex + 7, 36], fill=(246,246,246), outline=INK); d.rectangle([ex + 3 + look, 31, ex + 5 + look, 33], fill=INK)
    d.line([cx - 15, 27, cx - 6, 24], fill=INK, width=2)                                                                              # one brow up
    d.line([cx + 6, 28, cx + 15, 30], fill=INK, width=2)                                                                              # one frowning
    d.rectangle([cx - 4, 36, cx + 3, 46], fill=DK, outline=INK)                                                                       # the big nose
    mh = 3 + (k // 5) % 2
    d.ellipse([cx - 5, 50, cx + 4, 50 + mh + 3], fill=(60,24,24), outline=INK)                                                        # a puzzled "o"
    off = int(3 * math.sin(k * 0.9))
    d.line([cx + 40, 62, cx + 26 + off, 14], fill=INK, width=9); d.line([cx + 40, 62, cx + 26 + off, 14], fill=SK, width=7)           # the arm
    d.rectangle([cx + 20 + off, 6, cx + 31 + off, 16], fill=SK, outline=INK)
    for fx_ in (cx + 21, cx + 24, cx + 27, cx + 30): d.line([fx_ + off, 8, fx_ + off - 1, 13], fill=INK)                              # fingers scratching
    big_text(im, '?', 6, (255,226,110), scale=3, cx=9, outline=INK)

# ---- the clip -----------------------------------------------------------------------------------------------
def lever_angles(f):
    a1 = 0.35 * math.sin(math.pi * (f - 52) / 8) if 52 <= f < 60 else 0.0
    a2 = 0.0
    if 84 <= f < 92: a2 = PULL * ease((f - 84) / 8)
    elif 92 <= f < 298: a2 = PULL
    elif 298 <= f < 306: a2 = PULL * (1 - ease((f - 298) / 8))
    return a1, a2

def _tip(px, a): return px - LEVL * math.sin(a), PIVY - LEVL * math.cos(a)

def hand_xy(f):
    """Where Kronk's hand is while he deals with the levers (None: at his side)."""
    a1, a2 = lever_angles(f); idle = (CX + XO + 9, TY + 10); t1, t2 = _tip(P1, a1), _tip(P2, a2)
    if f < 36 or f >= 108: return None
    if f < 44: return mix(idle, t1, ease((f - 36) / 8))
    if f < 62: return t1
    if f < 70: return mix(_tip(P1, 0), t2, ease((f - 62) / 8))
    if f < 100: return t2
    return mix(t2, idle, ease((f - 100) / 8))

def kronk(f):
    look = 'r'; mood = 'smile'
    if 44 <= f < 90: look = 'l' if (f // 4) % 2 else 'r'
    if 96 <= f < 214 or 262 <= f < 290: look = 'l'
    if 100 <= f < 158 or 214 <= f < 246 or 262 <= f < 290: mood = 'oh'
    h = hand_xy(f)
    if h:
        pose = kp(round(h[0]) - (CX + XO), round(h[1]) - TY, lean=1)
    elif 210 <= f < 232: pose = ((-8, 5), (-8, 10), (10, -3), (1 + 2 * ((f // 3) % 2), -9), 0, 'stand')
    elif 246 <= f < 262: pose = ((-8, 5), (-8, 10), (11, -2), (12 + 2 * ((f // 3) % 2), -10), 0, 'stand')
    else: pose = 'kstand' if (loop.frame(f) // 8) % 2 == 0 else 'kstand2'
    return build(pose, look=look, mood=mood)

def yzma(f):
    """(Yzma's state, the cart, the gator) at frame f."""
    y = dict(x=YX, feet=GROUND, arm='akimbo', eyes='fwd', mouth='frown', tap=1 if loop.frame(f) % 8 < 4 else 0,
             sway=0, sweat=0, wet=0.0, stretch=1.0)
    cart = gator_ = None
    if 10 <= f < 46:
        y.update(arm='point', mouth=('wide' if (f // 3) % 2 else 'open') if f < 34 else 'shut', tap=0)
    elif 46 <= f < 98: y.update(arm='cross' if 56 <= f < 84 else 'akimbo', tap=1 if f % 4 < 2 else 0)
    elif 98 <= f < 122:
        y.update(arm='clasp', eyes='down' if f < 108 else ('shut' if 114 <= f < 117 else 'cam'), mouth='shut' if f < 118 else ('open' if f < 120 else 'frown'), tap=0,
                 sweat=max(0, min(5, (f - 114) // 2)) if f >= 114 else 0)
    elif 122 <= f < WRONG_AT: y.update(arm='up', eyes='wide', mouth='open', feet=GROUND - (f - 121), tap=0)
    elif 126 <= f < 140:
        t = f - 126; y.update(arm='up', eyes='wide', mouth='wide', feet=GROUND - 4 + 0.5 * 1.7 * t * t, stretch=1 + min(0.5, t * 0.07), tap=0)
        if y['feet'] - YH * y['stretch'] > H: y = None
    elif 140 <= f < 214: y = None
    elif 214 <= f < 336:
        wet = 1.0 if f < 290 else max(0.0, 1 - (f - 290) / 32)
        y.update(wet=wet, tap=0)
        cb = GROUND + 52 * (1 - ease(sm(f, 214, 240))) if f < 286 else GROUND + 52 * ease(sm(f, 286, 298))
        jit = (1 if (f // 2) % 2 else 0) if 214 <= f < 240 else 0
        if f < 240: y.update(arm='cross', mouth='frown', feet=cb - 7 + jit, x=YX + jit)
        elif f < 262: y.update(arm='fist' if (f // 2) % 2 else 'akimbo', eyes='glare', mouth='teeth' if (f // 4) % 2 else 'frown', feet=GROUND - 7)
        elif f < 278: y.update(sway=2 if f % 4 < 2 else -2, eyes='glare', mouth='wide', feet=GROUND - 7)
        elif f < 280: y.update(eyes='glare', mouth='frown', feet=GROUND - 7)
        elif f < 290:
            k = sm(f, 280, 290); y.update(eyes='glare', mouth='frown', x=YX + 28 * ease(k), feet=GROUND - 7 + 7 * k - 7 * math.sin(math.pi * k))
        elif f < 304: y.update(eyes='glare', mouth='frown', x=YX + 28, feet=GROUND, tap=1 if f % 4 < 2 else 0)
        elif f < 328: y.update(eyes='fwd', x=YX + 28 - 28 * sm(f, 304, 328), feet=GROUND - (1 if (f // 3) % 2 else 0))
        else: y.update(wet=0.0)
        if f >= 286 and f < 304: cart = None
        if f < 298: cart = (YX, cb)
        if f < 286: pass
        if 214 <= f < 270: gator_ = dict(x=YX - 10 + (y['sway'] // 2 if y else 0), y=(cb if f < 240 else GROUND) - 35, tail=(f // 2) % 2)
        if 270 <= f < 282:
            t = sm(f, 270, 282); gator_ = dict(x=YX - 10 - 54 * t, y=(GROUND - 35) - 10 * t + 60 * t * t, tail=(f // 2) % 2, flip=False)
        if f < 214 or f >= 328: cart = None
    return y, cart, gator_

def clip_lever(f):
    s = scene(f, THEME)
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=(30,22,44), draw=_face, txt=CLOSE, max_scale=2); return s
    a1, a2 = lever_angles(f)
    p = ease(sm(f, 92, 98)) if f < 200 else 1 - ease(sm(f, 298, 306))
    if f < 92 or f >= 306: p = 0.0
    s['under'] += [('gr_lab', a1, a2), ('gr_door', p)]
    y, cart, gat = yzma(f)
    s['fx'].append(('gr_yz', dict(yz=y, cart=cart, gator=gat)))
    s['actors'] = [actor(kronk(f), CX, pal=CPAL)]
    if cue(f, LINE1_AT, LINE1): s['fx'].append(('caption', LINE1, dict(box=(2, 2, W - 2, 17), max_scale=2, color=PINK, shadow=None, outline=INK)))
    if cue(f, 92, CLUNK): s['fx'].append(('caption', CLUNK, dict(box=(60, 2, W - 2, 17), max_scale=2, color=GOLD, shadow=None, outline=INK)))
    if cue(f, WRONG_AT, WRONG, extra=12): s['fx'].append(('gr_wrong', ease(sm(f, WRONG_AT, WRONG_AT + 26))))
    if 92 <= f < 96: s['shake'] = ((1, 0), (-1, 1), (1, 0), (0, 0))[f - 92]; s['fx'].append(('gr_spark', P2 - 4, PIVY, f - 92))
    if 298 <= f < 300: s['shake'] = (0, 1)
    if 141 <= f < 150: s['fx'].append(('gr_splash', f - 141))
    if 262 <= f < 280: s['fx'].append(('gr_spray', YX, 24, f - 262))
    return s

CLIPS = [clip('lever', N_, clip_lever)]
