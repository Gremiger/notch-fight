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
N_ = 288                                                            # idle cycles of 8, 16 and 24 frames divide it
CX = 90                                                            # Claude (Kronk), next to the levers
YX = 38                                                             # Yzma, on the trapdoor
INK = (16,14,22)
LINE1 = "PULL THE LEVER, KRONK!"
CLOSE = "WHY DO WE EVEN HAVE THAT LEVER?"
CLUNK = "CLUNK!"
LINE1_AT = 8
WRONG_AT = 106
CLOSE_AT, CLOSE_LEN = 138, 46
PINK, GOLD = (255,160,230), (255,226,110)

WRONG = "WRONG LEVEEEER!"

def mix(a, b, k): return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
def sm(f, a, b): return max(0.0, min(1.0, (f - a) / (b - a)))

# ---- Kronk, built from a pose (engine/people.py: figure(), POSES) ----------------------------------------
GW, GH, C = 56, 46, 28
L_, T_ = 10, 22                                                     # short legs, a huge torso
TY = GROUND - L_ - T_                                               # screen row of his shoulders (29); his hand is at CX + its column
def _kface(g, at):
    """A small head, a square jaw, thick brows, beady eyes that dart, a wide grin with teeth."""
    c, hy, sh, fl = at['c'], at['hy'], at['sh'], at['flags']
    for y in range(hy, hy + 6):
        for x in range(c - 4, c + 5): put(g, x + sh(y), y, 's')
    for y, x in ((hy + 2, c + 4), (hy + 3, c + 4), (hy + 3, c + 5)): put(g, x + sh(y), y, 'n')
    for x in (c - 3, c - 2, c + 1, c + 2): put(g, x + sh(hy + 2), hy + 2, 'W'); put(g, x + sh(hy + 1), hy + 1, 'h')
    for x in {'r': (c - 2, c + 2), 'l': (c - 3, c + 1)}[fl.get('look', 'r')]: put(g, x + sh(hy + 2), hy + 2, 'K')
    if fl.get('mood', 'smile') == 'smile':
        for x in range(c - 3, c + 4): put(g, x + sh(hy + 4), hy + 4, 'W')
        put(g, c - 4 + sh(hy + 4), hy + 4, 'm'); put(g, c + 4 + sh(hy + 4), hy + 4, 'm')
    else:
        for y in (hy + 4, hy + 5):
            for x in (c, c + 1): put(g, x + sh(y), y, 'm')
def _klegs(g, at):
    c, hip, h = at['c'], at['hip'], at['h']
    for y in range(hip + 1, h):
        for x in list(range(c - 6, c - 1)) + list(range(c + 2, c + 7)): put(g, x, y, 'b' if y == h - 1 else 's')
    for y in range(hip + 1, hip + 4):
        for x in range(c - 9, c + 10): put(g, x, y, 'G' if y == hip + 3 else 'j')
    for x in range(c - 9, c + 10, 3): put(g, x, hip + 2, 'o')
def _kbody(g, at):
    """The inverted triangle: huge shoulders, a narrow waist, a gold diamond on the chest."""
    c, ty, T, sh = at['c'], at['ty'], at['T'], at['sh']
    for i in range(T - 3):
        y = ty + i; half = round(12 - 6 * i / (T - 1)); o = sh(y)
        for x in range(c - half + o, c + half + o + 1): put(g, x, y, 'j')
        if i < 3:
            for x in (c - half + o, c - half + 1 + o, c + half + o, c + half - 1 + o): put(g, x, y, 's')
    for x in range(c - 8, c + 9): put(g, x + sh(ty + 3), ty + 3, 'G')
    for dy, w in ((5, 1), (6, 2), (7, 3), (8, 4), (9, 3), (10, 2), (11, 1)):
        for x in range(c - w, c + w + 1): put(g, x + sh(ty + dy), ty + dy, 'G')
def _karms(g, at):
    """Big arms: three cells thick, a fist at the end."""
    c, ty, T, sh = at['c'], at['ty'], at['T'], at['sh']
    be, bh, fe, fh = at['pose'][:4]
    for e, h, front in ((be, bh, False), (fe, fh, True)):
        pts = [(c + (12 if front else -12) + sh(ty + 1), ty + 1), (c + e[0] + sh(ty), ty + _row(e[1], T)),
               (c + h[0] + sh(ty), ty + _row(h[1], T))]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            for k in (1, 2):
                dx, dy = (0, k) if abs(x1 - x0) >= abs(y1 - y0) else (k, 0)
                seg(g, x0 + dx, y0 + dy, x1 + dx, y1 + dy, 's')
        hx, hy_ = pts[-1]
        for dx in range(3):
            for dy in range(3): put(g, hx + dx, hy_ + dy, 's')
CLAUDE = dict(name='groove-kronk', w=GW, h=GH, c=C, legs=L_, torso=T_, head=6, torso_cols=(-6, 6), eyes=(),
              body=dict(color='j', top='G', belt='o', hip='G'),
              arm=dict(sleeve='s', hand='s', hand_w=3, shoulders=((-12, 1), (12, 1))),
              leg=dict(color='s', boot='b', boot_rows=1, gap=-3, stand=(-2, 2)),
              hair=['....hhhhhhhh..', '..hhhhhhhhhhhh', '.hhhhhhhhhhhhh', '.hhhhhhhhhhh..', '.ooooooooo....'], hair_x=-5, hair_y=4,
              paint=dict(legs=[_klegs], body=[_kbody], head=[_kface], end=[_karms]))
CPAL = {'s':(190,128,86),'K':INK,'h':(22,18,28),'j':(196,46,46),'G':(240,192,64),'o':(217,119,87),'b':(116,74,46),
        'W':(246,246,246),'m':(60,24,24),'n':(150,98,66),'k':INK,'p':(60,52,70)}

def kp(hx, hy, lean=0, legs='stand'):
    """A Kronk pose with his front hand at (hx, hy) from (c, shoulders row): the elbow falls in between."""
    return ((-14, 6), (-15, 13), (round(12 + (hx - 12) * 0.5), round(1 + (hy - 1) * 0.5) + 4), (hx, hy), lean, legs)
POSES = dict(POSES)
POSES.update(kstand=kp(15, 14), kstand2=kp(15, 13))

def build(pose, **flags):
    return figure(CLAUDE, POSES[pose] if isinstance(pose, str) else pose, **flags)

# ---- Yzma: tall, thin, a feathered headdress, long bony arms (a sprite grid, outlined by the engine) -----
YW, YH, YC = 44, 44, 22
YPAL = {'P':(110,54,160),'p':(70,34,108),'V':(238,116,186),'U':(172,104,228),'g':(244,198,70),'y':(196,150,190),
        'Y':(150,106,150),'e':(140,64,226),'w':(246,246,246),'k':(20,14,26),'r':(204,40,80),'b':(150,210,255),'D':(60,50,90)}
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
    R(c - 3, 42, c - 2, 43, 'k'); R(c + 1, 42 - tap, c + 2, 43 - tap, 'k')       # shoes (one taps)
    for y in range(21, 42):                                                        # a stick-thin dress
        half = round(2 + 3.2 * ((y - 21) / 20) ** 1.5)
        R(c - half, y, c + half, y, 'P'); put(g, c - half, y, 'p')
        if y % 4 == 1: put(g, c + 1, y, 'p')
    R(c - 5, 41, c + 5, 41, 'V'); R(c - 5, 40, c + 5, 40, 'g')
    R(c - 2, 20, c + 2, 21, 'p'); put(g, c - 4, 19, 'V'); put(g, c + 4, 19, 'V'); put(g, c - 3, 20, 'V'); put(g, c + 3, 20, 'V')
    R(c - 1, 17, c, 19, 'y'); put(g, c - 1, 18, 'Y')                                # a bony neck
    for y in range(8, 17):                                                         # a long narrow head, a pointed chin
        half = 2 if y <= 13 else (1 if y <= 15 else 0)
        R(c - half, y, c + half, y, 'y')
    R(c - 2, 11, c - 2, 13, 'Y'); put(g, c + 3, 13, 'y'); put(g, c + 3, 14, 'y'); put(g, c + 4, 14, 'y')   # cheek, long nose
    R(c - 2, 9, c + 2, 10, 'e')                                                    # heavy purple eyeshadow
    if eyes == 'shut': R(c - 2, 11, c - 1, 11, 'k'); R(c + 1, 11, c + 2, 11, 'k'); pl = []
    elif eyes == 'wide': R(c - 2, 10, c - 1, 12, 'w'); R(c + 1, 10, c + 2, 12, 'w'); pl = [(c - 1, 11), (c + 2, 11)]
    else:
        R(c - 2, 11, c - 1, 12, 'w'); R(c + 1, 11, c + 2, 12, 'w')
        pl = {'fwd': [(c - 1, 11), (c + 2, 11)], 'down': [(c - 1, 12), (c + 2, 12)], 'cam': [(c - 2, 12), (c + 1, 12)],
              'glare': [(c - 1, 12), (c + 2, 12)]}[eyes]
    for x, y in pl: put(g, x, y, 'k')
    if eyes == 'glare':
        R(c - 2, 11, c - 1, 11, 'k'); R(c + 1, 11, c + 2, 11, 'k'); put(g, c - 2, 9, 'k'); put(g, c - 1, 9, 'k'); put(g, c + 1, 9, 'k'); put(g, c + 2, 9, 'k')
    put(g, c - 3, 10, 'k'); put(g, c - 3, 11, 'k'); put(g, c + 3, 10, 'k')       # the lashes
    if mouth == 'shut': R(c - 1, 14, c + 1, 14, 'r')
    elif mouth == 'frown': R(c - 1, 14, c + 1, 14, 'r'); put(g, c - 2, 14, 'k'); put(g, c + 2, 14, 'k')
    elif mouth == 'open': R(c - 1, 14, c + 1, 15, 'k'); R(c - 1, 14, c + 1, 14, 'r')
    elif mouth == 'wide': R(c - 2, 13, c + 2, 15, 'k'); R(c - 1, 13, c + 1, 13, 'w'); put(g, c, 15, 'r')
    elif mouth == 'teeth': R(c - 2, 14, c + 2, 14, 'w'); R(c - 1, 15, c + 1, 15, 'w'); put(g, c, 14, 'k'); put(g, c, 15, 'k')
    wetl = wet > 0; s = sway
    R(c - 7 + s, 7, c + 7 + s, 7, 'g'); R(c - 7 + s, 6, c + 7 + s, 6, 'V'); put(g, c + s, 6, 'w')   # the headband
    for x in range(c - 10, c + 11):                                                # a big feather fan
        hgt = 7 - round(abs(x - c) * 0.45) - (1 if (x - c) % 2 else 0)
        if wetl: hgt = max(1, hgt // 2)
        R(x + s, 6 - hgt, x + s, 5, ('U', 'V', 'P')[(x - c) % 3])
    for yy in range(6, 9 if not wetl else 17):
        put(g, c - 8 + s, yy, 'U'); put(g, c + 8 + s, yy, 'P')
    if wetl:
        for yy in range(8, 18): put(g, c - 3, yy, 'D'); put(g, c + 3, yy, 'D') if yy < 13 else None
    if sweat: put(g, c + 4, 8 + sweat, 'b'); put(g, c + 4, 9 + sweat, 'b')
    put(g, c - 2, 22, 'p'); put(g, c + 2, 22, 'p')
    L, F = (c - 2, 22), (c + 2, 22)
    if arm == 'point': A([L, (c - 6, 27), (c - 3, 31)]); A([F, (c + 16, 19)]); A([(c + 16, 19), (c + 19, 18)]); put(g, c + 20, 18, 'r')
    elif arm == 'cross': A([L, (c - 3, 27), (c + 2, 28)]); A([F, (c + 3, 27), (c - 2, 29)])
    elif arm == 'clasp': A([L, (c - 3, 27), (c, 30)]); A([F, (c + 3, 27), (c + 1, 30)])
    elif arm == 'up': A([L, (c - 8, 15), (c - 11, 7)]); A([F, (c + 8, 15), (c + 11, 7)]); R(c - 12, 5, c - 10, 7, 'y'); R(c + 10, 5, c + 12, 7, 'y')
    elif arm == 'fist': A([L, (c - 6, 27), (c - 3, 31)]); A([F, (c + 8, 18), (c + 7, 13)]); R(c + 6, 11, c + 8, 13, 'y')
    else: A([L, (c - 6, 27), (c - 3, 31)]); A([F, (c + 6, 27), (c + 3, 31)])
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
    SK, DK, HAIR = (190,128,86), (150,98,66), (22,18,28)
    k = f - CLOSE_AT; cx = 38 + (1 if (k // 6) % 2 else 0)
    for y in range(H): d.line([0, y, 78, y], fill=(int(36 - y * 0.2), int(26 + y * 0.3), int(54 - y * 0.2)))
    d.polygon([(cx - 24, 24), (cx - 25, 12), (cx - 15, 4), (cx - 2, 0), (cx + 16, 1), (cx + 29, 6), (cx + 33, 12), (cx + 26, 14), (cx + 25, 24)], fill=HAIR, outline=INK)
    d.line([cx - 12, 6, cx + 18, 4], fill=(70,60,96)); d.line([cx - 4, 10, cx + 22, 9], fill=(70,60,96))                          # the quiff's shine
    d.rectangle([cx - 26, 29, cx - 22, 39], fill=SK, outline=INK); d.rectangle([cx + 22, 29, cx + 26, 39], fill=SK, outline=INK)   # ears
    d.polygon([(cx - 24, 20), (cx + 24, 20), (cx + 24, 52), (cx + 20, 60), (cx - 20, 60), (cx - 24, 52)], fill=SK, outline=INK)     # the square jaw
    d.rectangle([cx - 24, 20, cx + 24, 25], fill=(217,119,87), outline=INK); d.rectangle([cx - 2, 21, cx + 2, 24], fill=(240,192,64))   # the headband
    look = (k // 8) % 2 * 2 - 1
    for ex in (cx - 15, cx + 7):
        d.rectangle([ex, 33, ex + 8, 38], fill=(246,246,246), outline=INK); d.rectangle([ex + 3 + look, 33, ex + 5 + look, 35], fill=INK)
    d.line([cx - 17, 30, cx - 5, 26], fill=INK, width=4)                                                                          # thick brows: one up
    d.line([cx + 5, 29, cx + 17, 32], fill=INK, width=4)                                                                          # one frowning
    d.rectangle([cx - 4, 38, cx + 4, 48], fill=DK, outline=INK)
    mh = 3 + (k // 5) % 2
    d.ellipse([cx - 6, 51, cx + 5, 51 + mh + 4], fill=(60,24,24), outline=INK)
    off = int(3 * math.sin(k * 0.9))
    for wd, col in ((13, INK), (11, SK)): d.line([cx + 14 + off, 0, cx + 42, 12, cx + 42, 64], fill=col, width=wd)               # the arm
    px = cx + 4 + off
    d.rectangle([px, -2, px + 17, 8], fill=SK, outline=INK)                                                                       # the palm
    for i in range(4):
        fx_ = px + i * 4 + (1 if (k + i) % 2 else 0); d.rectangle([fx_, 8, fx_ + 3, 15 - (i % 2)], fill=SK, outline=INK)            # fingers on the hair
    d.rectangle([px + 17, 2, px + 21, 6], fill=SK, outline=INK)                                                                   # the thumb
    big_text(im, '?', 6, (255,226,110), scale=3, cx=9, outline=INK)

# ---- the clip -----------------------------------------------------------------------------------------------
def lever_angles(f):
    a1 = 0.35 * math.sin(math.pi * (f - 42) / 6) if 42 <= f < 48 else 0.0
    a2 = 0.0
    if 66 <= f < 74: a2 = PULL * ease((f - 66) / 8)
    elif 74 <= f < 262: a2 = PULL
    elif 262 <= f < 270: a2 = PULL * (1 - ease((f - 262) / 8))
    return a1, a2

def _tip(px, a): return px - LEVL * math.sin(a), PIVY - LEVL * math.cos(a)

def hand_xy(f):
    """Where Kronk's hand is while he deals with the levers (None: at his side)."""
    a1, a2 = lever_angles(f); idle = (CX + 15, TY + 14); t1, t2 = _tip(P1, a1), _tip(P2, a2)
    if f < 32 or f >= 88: return None
    if f < 38: return mix(idle, t1, ease((f - 32) / 6))
    if f < 50: return t1
    if f < 56: return mix(_tip(P1, 0), t2, ease((f - 50) / 6))
    if f < 80: return t2
    return mix(t2, idle, ease((f - 80) / 8))

def kronk(f):
    look = 'r'; mood = 'smile'
    if 38 <= f < 66: look = 'l' if (f // 3) % 2 else 'r'
    if 78 <= f < 190 or 230 <= f < 262: look = 'l'
    if 84 <= f < 138 or 190 <= f < 214 or 230 <= f < 262: mood = 'oh'
    h = hand_xy(f)
    if h: pose = kp(round(h[0]) - CX, round(h[1]) - TY, lean=1)
    elif 184 <= f < 200: pose = ((-14, 6), (-15, 13), (17, -4), (3 + 3 * ((f // 3) % 2), -10), 0, 'stand')
    elif 214 <= f < 230: pose = ((-14, 6), (-15, 13), (18, 1), (19 + 2 * ((f // 3) % 2), -8), 0, 'stand')
    else: pose = 'kstand' if (loop.frame(f) // 8) % 2 == 0 else 'kstand2'
    return build(pose, look=look, mood=mood)

def yzma(f):
    """(Yzma's state, the cart, the gator) at frame f."""
    y = dict(x=YX, feet=GROUND, arm='akimbo', eyes='fwd', mouth='frown', tap=1 if loop.frame(f) % 8 < 4 else 0,
             sway=0, sweat=0, wet=0.0, stretch=1.0)
    cart = gator_ = None
    if 8 <= f < 40: y.update(arm='point', mouth=('wide' if (f // 3) % 2 else 'open') if f < 30 else 'shut', tap=0)
    elif 40 <= f < 80: y.update(arm='cross' if 48 <= f < 66 else 'akimbo', tap=1 if f % 4 < 2 else 0)
    elif 80 <= f < 102:
        y.update(arm='clasp', eyes='down' if f < 88 else ('shut' if 94 <= f < 97 else 'cam'), mouth='shut' if f < 98 else ('open' if f < 100 else 'frown'),
                 tap=0, sweat=max(0, min(5, (f - 92) // 2)) if f >= 92 else 0)
    elif 102 <= f < WRONG_AT: y.update(arm='up', eyes='wide', mouth='open', feet=GROUND - (f - 101), tap=0)
    elif 106 <= f < 120:
        t = f - 106; y.update(arm='up', eyes='wide', mouth='wide', feet=GROUND - 4 + 0.5 * 1.7 * t * t, stretch=1 + min(0.5, t * 0.07), tap=0)
        if y['feet'] - YH * y['stretch'] > H: y = None
    elif 120 <= f < 190: y = None
    elif 190 <= f < 282:
        y.update(wet=1.0 if f < 256 else max(0.0, 1 - (f - 256) / 24), tap=0)
        cb = GROUND + 52 * (1 - ease(sm(f, 190, 212))) if f < 252 else GROUND + 52 * ease(sm(f, 252, 262))
        jit = (1 if (f // 2) % 2 else 0) if f < 212 else 0
        if f < 212: y.update(arm='cross', mouth='frown', feet=cb - 7 + jit, x=YX + jit)
        elif f < 230: y.update(arm='fist' if (f // 2) % 2 else 'akimbo', eyes='glare', mouth='teeth' if (f // 4) % 2 else 'frown', feet=GROUND - 7)
        elif f < 244: y.update(sway=2 if f % 4 < 2 else -2, eyes='glare', mouth='wide', feet=GROUND - 7)
        elif f < 246: y.update(eyes='glare', mouth='frown', feet=GROUND - 7)
        elif f < 254:
            k = sm(f, 246, 254); y.update(eyes='glare', mouth='frown', x=YX + 28 * ease(k), feet=GROUND - 7 + 7 * k - 7 * math.sin(math.pi * k))
        elif f < 268: y.update(eyes='glare', mouth='frown', x=YX + 28, feet=GROUND, tap=1 if f % 4 < 2 else 0)
        else: y.update(eyes='fwd', x=YX + 28 - 28 * sm(f, 268, 282), feet=GROUND - (1 if (f // 2) % 2 else 0))
        if f < 262: cart = (YX, cb)
        if f < 236: gator_ = dict(x=YX - 10 + (y['sway'] // 2), y=(cb if f < 212 else GROUND) - 44, tail=(f // 2) % 2)
        elif f < 248:
            t = sm(f, 236, 248); gator_ = dict(x=YX - 10 - 54 * t, y=(GROUND - 44) - 10 * t + 60 * t * t, tail=(f // 2) % 2)
    return y, cart, gator_

def clip_lever(f):
    s = scene(f, THEME)
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=(30,22,44), draw=_face, txt=CLOSE, max_scale=2); return s
    a1, a2 = lever_angles(f)
    p = ease(sm(f, 72, 78)) if f < 200 else 1 - ease(sm(f, 262, 270))
    if f < 72 or f >= 270: p = 0.0
    s['under'] += [('gr_lab', a1, a2), ('gr_door', p)]
    y, cart, gat = yzma(f)
    s['fx'].append(('gr_yz', dict(yz=y, cart=cart, gator=gat)))
    s['actors'] = [actor(kronk(f), CX, pal=CPAL)]
    box = (2, 1, W - 2, 15)
    if cue(f, LINE1_AT, LINE1): s['fx'].append(('caption', LINE1, dict(box=box, max_scale=2, color=PINK, shadow=None, outline=INK)))
    if cue(f, 72, CLUNK): s['fx'].append(('caption', CLUNK, dict(box=(60, 1, W - 2, 15), max_scale=2, color=GOLD, shadow=None, outline=INK)))
    if cue(f, WRONG_AT, WRONG, extra=12): s['fx'].append(('gr_wrong', ease(sm(f, WRONG_AT, WRONG_AT + 26))))
    if 72 <= f < 76: s['shake'] = ((1, 0), (-1, 1), (1, 0), (0, 0))[f - 72]; s['fx'].append(('gr_spark', P2 - 4, PIVY, f - 72))
    if 262 <= f < 264: s['shake'] = (0, 1)
    if 121 <= f < 130: s['fx'].append(('gr_splash', f - 121))
    if 230 <= f < 248: s['fx'].append(('gr_spray', YX, 22, f - 230))
    return s

CLIPS = [clip('lever', N_, clip_lever)]
