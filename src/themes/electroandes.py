"""Electro Andes: Claude as Cal, the Argentine ethno-cyberpunk anime's lead (a bleached orange fringe, a black
topknot, an oversized mustard tee with a white X, a teal neon choker, black gloves with teal fingertips, sneakers
that shoot a teal jet), on the lookout of Arcadia Iruyana at dusk: a wooden clock tower, lavender peaks and, on the
horizon, the Black Mountain with its red triangle. Three clips from that pose: `salamanca` (the Supay asks "¿TENÉS
MIEDO?" in the red void; Claude answers "NO." and punches through the beast with a teal fist), `potrero` (a bicycle
kick on the dirt pitch, "¡GOLAZO!", no fight) and `apu` (with Pietro, the giant stone Apu rises; they make the mountain
sign: "PERMISO, APU."). Ships off by default: a niche series."""
import math
from engine import *

THEME = 'electroandes'
DEFAULT_OFF = True                                                  # niche series
INK = (16, 14, 22)
TEAL, TEAL_D, TEAL_L = (63, 230, 200), (20, 110, 108), (200, 255, 244)
RED, RED_D = (226, 46, 58), (110, 16, 32)
ORANGE = (217, 119, 87)                                             # Claude's orange
BM = (44, 36, 58)                                                   # Black Mountain
BLUE, BLUE_L = (96, 176, 255), (214, 240, 255)
STONE = (104, 94, 100)
CX = 50
CLOSE_LEN = 36

def mix(a, b, k): return tuple(int(lerp(x, y, k)) for x, y in zip(a, b))
def teal(f): return mix(TEAL_D, TEAL, 0.5 + 0.5 * loop.wave(f, 20))   # the choker and the gloves pulse (loops on 20)
def vgrad(d, y0, y1, c0, c1):
    for y in range(y0, y1): d.line([0, y, W, y], fill=mix(c0, c1, (y - y0) / max(1, y1 - y0 - 1)))
def glow(im, x, y, r, c, a=0.5):
    """A soft round glow of colour c, centre (x, y), radius r."""
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([x - r, y - r, x + r, y + r], fill=int(255 * a))
    im.paste(c, (0, 0), m.filter(ImageFilter.GaussianBlur(max(1, r // 2))))

# ---- people (engine/people.py) -----------------------------------------------------------------------------
GW, GH, C = 24, 24, 11
POSES = dict(POSES)
POSES.update({
 'idle1': ((-1, 4), (-1, 7), (3, 4), (4, 6), 0, 'stand'),            # the neutral pose: a calm stand, a hand shifting
 'idle2': ((-1, 4), (-1, 7), (3, 4), (5, 6), 0, 'stand'),
 'sign': ((2, 4), (6, 1), (4, 4), (6, 0), 0, 'stand'),               # both hands together at the chest: the mountain sign
 'hands_head': ((-4, 0), (-2, -5), (4, 0), (0, -5), 0, 'stand'),     # Cal's pose: hands behind the head
 'dash': ((-3, 2), (-6, 4), (3, 3), (6, 2), 3, 'run1'),
 'wall': ((-3, 2), (-6, 4), (3, 3), (6, 2), 0, 'run2'),
})

def _ring(g, at):                                                   # the teal ring round the sneakers' ankles
    for x in range(len(g[0])):
        if g[at['h'] - 2][x] == 'p': g[at['h'] - 2][x] = 'T'
def _bib(g, at):                                                    # the navy collar and the white X on the tee
    c, ty, sh = at['c'], at['ty'], at['sh']
    for dx, dy in ((0, 1), (1, 1), (2, 1), (1, 2)): put(g, c + dx + sh(ty + dy), ty + dy, 'N')
    for dx, dy in ((0, 3), (2, 3), (1, 4), (0, 5), (2, 5)): put(g, c + dx + sh(ty + dy), ty + dy, 'W')
def _choker(g, at):                                                 # the teal neon choker
    for dx in (-1, 0, 1, 2): put(g, at['c'] + dx + at['sh'](at['ty'] - 1), at['ty'] - 1, 'T')
def _gold(g, at):                                                   # Pietro's jacket: two gold stripes on the sleeve
    c, ty, sh = at['c'], at['ty'], at['sh']
    for dx in (3, 4): put(g, c + dx + sh(ty + 2), ty + 2, 'y')

_BODY = dict(w=GW, h=GH, c=C, legs=9, torso=7)
CAL = dict(_BODY, torso_cols=(-4, 3), name='ea-cal', hair=['.h.OOO.', 'hhOOOOO', 'hhhOOOO', '.hh..OO'], hair_y=2,
           leg=dict(color='p', boot='u'), body=dict(color='j', top='N'), arm=dict(sleeve='k', fore='k', hand='t'),
           paint=dict(legs=[_ring], body=[_bib], head=[_choker]))
PIETRO = dict(_BODY, name='ea-pietro', hair=['.nn....', '.nnnnn.', 'nnnnnn.', '.nn..n.'], hair_y=2,
              leg=dict(color='p', boot='u'), body=dict(color='m', top='k', collar='k'),
              arm=dict(sleeve='m', fore='k', hand='t', mark='y'), paint=dict(legs=[_ring], body=[_gold], head=[_choker]))
BIG = dict(name='ea-big', w=32, h=30, c=15, legs=11, torso=9, torso_cols=(-5, 5), hair=[], leg=dict(color='q', boot='b'),
           body=dict(color='k'), arm=dict(sleeve='s', fore='s', hand='s', shoulders=((-4, 1), (4, 1))),
           paint=dict(head=[lambda g, at: [put(g, at['c'] + dx + at['sh'](at['hy'] + 4), at['hy'] + 4, 'K') for dx in (1, 2)]]))

def _jersey(g, at):                                                 # the Argentina shirt: light-blue and white stripes
    c, ty, sh = at['c'], at['ty'], at['sh']
    for y in range(ty, at['hip'] + 1):
        for x in range(c - 2 + sh(y), c + 3 + sh(y)):
            if (x - c) % 2 == 0: put(g, x, y, 'B')
def kid(name, hair, shirt, jersey=False):
    return dict(name=name, w=16, h=17, c=7, legs=6, torso=5, head=4, torso_cols=(-2, 3), hair=hair, hair_y=1,
                leg=dict(color='p', boot='u'), body=dict(color=shirt), arm=dict(sleeve=shirt, fore='s', hand='s', shoulders=((-2, 1), (2, 1))),
                paint=dict(body=[_jersey] if jersey else []))
KIDS = [kid('ea-k1', ['.hhhhh.', 'hhhhhhh'], 'W', True), kid('ea-k2', ['.hhhhh.', 'hhhhhhh'], 'g'), kid('ea-k3', ['.rrrrr.', 'rrrrrrr'], 'n')]

SKIN, RSKIN = (122, 78, 54), (178, 34, 38)
def cpal(f=0, skin=SKIN):
    t = teal(f)
    return {'s': skin, 'K': INK, 'h': (22, 20, 30), 'O': ORANGE, 'j': (214, 164, 52), 'N': (30, 48, 104), 'W': (246, 246, 250),
            'k': (28, 26, 38), 'p': (42, 42, 58), 'u': (56, 58, 78), 'T': t, 't': t}
def ppal(f=0):
    t = teal(f)
    return {'s': (150, 100, 70), 'K': INK, 'n': (44, 70, 160), 'm': (178, 40, 58), 'y': (232, 190, 70), 'k': (28, 26, 38),
            'p': (42, 42, 58), 'u': (56, 58, 78), 'T': t, 't': t}
BPAL = {'s': (150, 98, 66), 'K': INK, 'k': (22, 22, 28), 'q': (118, 100, 80), 'b': (70, 48, 34)}
KPAL = {'s': (170, 116, 82), 'K': INK, 'h': (30, 24, 28), 'r': (30, 24, 28), 'W': (240, 240, 246), 'B': (130, 186, 232), 'g': (70, 150, 90),
        'n': (70, 90, 160), 'p': (70, 66, 90), 'u': (80, 70, 60)}

def cal(pose): return figure(CAL, POSES[pose])
def ready(f): return pose_cycle(f, 'idle1', 'idle2', every=10)       # every 10: a 20-frame cycle, divides the clips' length

# ---- the places (static backgrounds; the moving things are effects) ---------------------------------------------
def _lookout(d):
    vgrad(d, 0, GROUND + 2, (96, 82, 152), (248, 170, 124))
    d.ellipse([88, 34, 106, 52], fill=(255, 214, 150))
    d.polygon([(0, 42), (14, 28), (26, 38), (46, 22), (64, 40), (82, 30), (100, 42), (118, 30), (140, 40), (162, 28), (185, 38), (185, 54), (0, 54)], fill=(160, 138, 198))
    d.polygon([(0, 50), (20, 40), (38, 48), (60, 36), (84, 50), (108, 44), (126, 52), (185, 52), (185, 58), (0, 58)], fill=(128, 108, 168))
    d.polygon([(104, 54), (112, 40), (126, 38), (132, 30), (140, 30), (162, 30), (166, 36), (176, 36), (185, 42), (185, 54)], fill=BM)   # the mine
    d.polygon([(140, 54), (143, 8), (159, 8), (163, 54)], fill=BM)                                                              # the tower
    d.line([151, 0, 151, 8], fill=BM)
    for x, y in ((146, 40), (156, 36), (120, 46), (170, 44)): d.point((x, y), fill=(255, 190, 90))
    d.rectangle([112, 22, 114, 40], fill=BM); d.rectangle([168, 24, 170, 38], fill=BM)                                           # stacks
    d.polygon([(6, 30), (15, 16), (24, 30)], fill=(150, 70, 60)); d.rectangle([8, 30, 22, 58], fill=(112, 80, 58))               # clock tower
    for y in range(34, 58, 5): d.line([8, y, 22, y], fill=(92, 64, 46))
    d.ellipse([10, 33, 20, 43], fill=(244, 234, 204), outline=(70, 46, 36)); d.line([15, 38, 15, 35], fill=INK); d.line([15, 38, 18, 38], fill=INK)
    d.rectangle([0, GROUND + 1, W, H], fill=(120, 84, 58))                                                                        # planks
    for x in range(10, W, 22): d.line([x, GROUND + 1, x, H], fill=(92, 64, 46))
    for x in range(0, W, 20): d.rectangle([x + 2, 48, x + 4, GROUND], fill=(86, 58, 42))                                          # the rail
    d.rectangle([0, 48, W, 49], fill=(98, 68, 48)); d.line([0, 54, W, 54], fill=(86, 58, 42))
register_bg(THEME, lambda v: (v + 60, v + 40, v + 50), decor=_lookout)

def slope_y(x): return 58 - 0.205 * x
def _ridge(d):
    vgrad(d, 0, H, (10, 20, 34), (40, 70, 86))
    d.ellipse([111, -1, 145, 33], fill=(232, 150, 96)); d.ellipse([113, 1, 143, 31], fill=(246, 240, 210))
    for x, y, r in ((20, 38, 12), (46, 34, 9), (150, 34, 12), (90, 36, 8), (176, 30, 9)): d.ellipse([x - r * 1.6, y - r * 0.6, x + r * 1.6, y + r * 0.6], fill=(58, 92, 104))
    d.polygon([(0, 58), (185, 20), (185, H), (0, H)], fill=(52, 72, 90))
    d.polygon([(8, 50), (12, 26), (22, 26), (26, 48)], fill=(60, 74, 84)); d.rectangle([13, 20, 21, 26], fill=(64, 60, 70))   # the village rock
    d.polygon([(12, 20), (17, 14), (22, 20)], fill=(90, 80, 84)); d.point((17, 22), fill=(255, 190, 90))
    d.rectangle([0, GROUND + 1, W, H], fill=(34, 48, 62))
register_bg('ea-ridge', lambda v: (v, v + 30, v + 30), decor=_ridge)

def _flat(d): d.rectangle([0, 0, W, H], fill=(14, 8, 18))
register_bg('ea-mine', lambda v: (v, 20, 30), decor=_flat)

def _cave(d):
    vgrad(d, 0, H, (22, 8, 22), (92, 20, 36))
    d.polygon([(0, 0), (30, 0), (20, 20), (0, 30)], fill=(40, 22, 36)); d.polygon([(185, 0), (150, 0), (166, 24), (185, 30)], fill=(40, 22, 36))
    for x, h in ((8, 14), (14, 9), (172, 12), (178, 16), (166, 8), (96, 6)):
        d.polygon([(x - 3, 60), (x, 60 - h), (x + 3, 60)], fill=(214, 50, 62)); d.line([x, 60 - h, x, 58], fill=(255, 150, 150))
    d.rectangle([0, GROUND + 1, W, H], fill=(56, 30, 42)); d.line([0, GROUND + 1, W, GROUND + 1], fill=(120, 40, 56))
register_bg('ea-cave', lambda v: (v + 50, 30, 40), decor=_cave)

def _void(d):
    d.rectangle([0, 0, W, 38], fill=(136, 16, 26)); d.rectangle([0, 38, W, H], fill=(84, 8, 18)); d.line([0, 38, W, 38], fill=(214, 70, 60))
    for i, y in enumerate((42, 46, 51, 57, 62)):
        for x in range(i * 7 % 17, W, 17): d.line([x, y, x + 5 + i, y], fill=(150, 30, 40))
register_bg('ea-void', lambda v: (v + 60, 30, 40), decor=_void)

def _pitch(d):
    vgrad(d, 0, 40, (112, 160, 214), (206, 222, 238))
    for x, y, r in ((30, 12, 9), (46, 9, 6), (120, 8, 8), (150, 14, 10), (176, 8, 6)): d.ellipse([x - r * 1.7, y - r * 0.6, x + r * 1.7, y + r * 0.6], fill=(250, 250, 255))
    d.polygon([(0, 40), (20, 28), (46, 36), (70, 24), (98, 38), (130, 30), (160, 38), (185, 30), (185, 42), (0, 42)], fill=(170, 150, 190))
    d.polygon([(60, 44), (64, 10), (82, 10), (86, 44)], fill=BM); d.line([73, 2, 73, 10], fill=BM)                                 # the tower
    for y in (16, 24, 32): d.line([66, y, 80, y], fill=(70, 60, 84))
    d.polygon([(72, 15), (76, 22), (68, 22)], outline=(236, 236, 240))                                                             # its logo
    d.rectangle([0, 40, W, H], fill=(214, 160, 100))
    for i in range(18): x = i * 53 % 185; y = 42 + i * 7 % 22; d.line([x, y, x + 9, y], fill=(196, 142, 88))
    d.polygon([(2, 18), (46, 18), (50, 24), (0, 24)], fill=(146, 100, 70)); d.rectangle([4, 24, 6, 40], fill=(110, 76, 54)); d.rectangle([42, 24, 44, 40], fill=(110, 76, 54))   # a stall
    for x in range(150, 178, 3): d.line([x, 30, x, 49], fill=(212, 206, 196))                                                      # the net
    for y in range(30, 50, 3): d.line([150, y, 177, y], fill=(212, 206, 196))
    d.rectangle([148, 28, 150, 50], fill=(150, 104, 70)); d.rectangle([176, 28, 178, 50], fill=(150, 104, 70)); d.rectangle([148, 28, 178, 30], fill=(150, 104, 70))
    d.line([0, 41, W, 41], fill=(70, 50, 40))                                                                                      # the rope
    for x in range(0, W, 12): d.line([x, 41, x, 43], fill=(70, 50, 40))
register_bg('ea-pitch', lambda v: (v + 90, v + 50, v + 20), decor=_pitch)

def _slope(d):
    d.rectangle([0, 48, W, H], fill=(190, 112, 60))
    vgrad(d, 0, 50, (240, 130, 84), (255, 218, 150))
    d.ellipse([20, 14, 60, 54], fill=(255, 232, 170))
    for x, y, r in ((30, 12, 10), (84, 8, 8), (120, 20, 7), (172, 10, 8)): d.ellipse([x - r * 1.8, y - r * 0.5, x + r * 1.8, y + r * 0.5], fill=(255, 150, 80))
    d.polygon([(0, 46), (18, 28), (40, 40), (60, 26), (84, 40), (100, 34), (110, 50), (0, 50)], fill=(150, 110, 140))
register_bg('ea-slope', lambda v: (v + 100, v + 60, v + 20), decor=_slope)

# ---- effects -----------------------------------------------------------------------------------------------
@fx('ea_logo')
def _fx_logo(d, im, e, f):
    """The Black Mountain triangle: ('ea_logo', x, y, size)."""
    _, x, y, s = e; k = 0.5 + 0.5 * loop.wave(f, 40)
    d.polygon([(x, y - s), (x + s, y + s * 0.8), (x - s, y + s * 0.8)], fill=mix((150, 24, 40), RED, k))
    d.polygon([(x, y - s // 3), (x + s // 2, y + s * 0.5), (x - s // 2, y + s * 0.5)], fill=mix((60, 10, 24), (255, 200, 190), k * 0.6))

@fx('ea_mech')
def _fx_mech(d, im, e, f):
    """A thin grey machine with a red core, climbing: ('ea_mech', x, feet_y, phase)."""
    _, x, y, ph = e; s = math.sin(ph); c = math.cos(ph)
    for col, o in (((30, 34, 48), 1), ((100, 108, 130), 0)):
        pel = (x - 1 + o, y - 11); sho = (x + 3 + o, y - 21)
        d.line([pel, sho], fill=col)                                                       # spine
        k1 = (x + 4 + o + 2 * s, y - 6); f1 = (x + 2 + o + 5 * s, y - 1 - 2 * max(0, c))
        k2 = (x + 4 + o - 2 * s, y - 6); f2 = (x + 2 + o - 5 * s, y - 1 - 2 * max(0, -c))
        d.line([pel, k1, f1], fill=col); d.line([pel, k2, f2], fill=col)                   # legs
        d.line([sho, (x + 8 + o, y - 21 - 2 * s), (x + 11 + o, y - 17 + 3 * c)], fill=col)  # a long arm reaching ahead
        d.line([sho, (x + 1 + o, y - 14), (x + 4 + o, y - 8 - 2 * c)], fill=col)
        d.ellipse([x + 3 + o, y - 26, x + 6 + o, y - 23], fill=col)
    d.rectangle([x + 2, y - 20, x + 4, y - 17], fill=RED); d.point((x + 3, y - 19), fill=(255, 190, 170)); d.point((x + 5, y - 25), fill=RED)

@fx('ea_rot')
def _fx_rot(d, im, e, f):
    """A sprite turned by an angle: ('ea_rot', spr, pal, cx, cy, degrees counter-clockwise)."""
    _, spr, pal, cx, cy, ang = e
    sp = sprite_img(spr, pal).rotate(ang, resample=Image.NEAREST, expand=True)
    im.paste(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)), sp)

@fx('ea_trail')
def _fx_trail(d, im, e, f):
    """A teal streak from (x0, y0) back to (x1, y1), fading away from the head: ('ea_trail', x0, y0, x1, y1)."""
    _, x0, y0, x1, y1 = e
    for i in range(9):
        a, b = i / 9, (i + 1) / 9
        d.line([lerp(x0, x1, a), lerp(y0, y1, a), lerp(x0, x1, b), lerp(y0, y1, b)], fill=mix(TEAL_L, TEAL_D, a), width=3 if i < 5 else 1)

SL, SR = 44, 140                                                     # the shaft's walls
def crystal(d, x, y, h, w=3, up=True, c=(222, 48, 60)):
    s = -1 if up else 1
    d.polygon([(x - w, y), (x - w // 2, y + s * h * 0.8), (x, y + s * h), (x + w, y + s * h * 0.6), (x + w, y)], fill=c)
    d.line([x - w // 2, y + s * h * 0.7, x, y + s * h], fill=(255, 150, 150)); d.line([x, y, x, y + s * h * 0.6], fill=(150, 20, 40))

@fx('ea_shaft')
def _fx_shaft(d, im, e, f):
    """The mine shaft: rock walls and red crystals scrolling up as Claude runs down: ('ea_shaft', offset)."""
    off = int(e[1]); L, R = SL, SR
    for y in range(H): d.line([L, y, R, y], fill=mix((26, 8, 22), (90, 22, 40), y / H))
    for x0, x1 in ((0, L), (R, W)):                                       # the walls: stones in rows
        d.rectangle([x0, 0, x1, H], fill=(56, 36, 48))
        for row in range(-1, 8):
            rid = row + off // 10; y = row * 10 - off % 10; xx = x0 - (rid * 7) % 11
            while xx <= x1:
                w = 8 + (xx * 7 + rid * 13) % 9; a, b = max(xx, x0), min(xx + w - 2, x1)
                if a < b:
                    d.rectangle([a, y, b, y + 8], fill=((70, 46, 58), (50, 32, 44), (82, 56, 66), (62, 40, 54))[(xx + rid) % 4]); d.line([a, y, b, y], fill=(100, 68, 78))
                xx += w
    d.line([L, 0, L, H], fill=(30, 14, 26)); d.line([R, 0, R, H], fill=(30, 14, 26))
    for k in range(2):                                                    # timber beams across
        y = int((k * 36 - off) % 72) - 8; d.rectangle([L, y, R, y + 2], fill=(86, 58, 44)); d.line([L, y, R, y], fill=(120, 84, 60))
    rr = random.Random(11)
    for i in range(28):                                                   # dense crystals growing out of both walls
        side = i % 2; y = int((i * 4.5 + rr.randint(0, 3) - off) % 126) - 12; h = rr.randint(6, 13); x = L if side == 0 else R; dn = 1 if side == 0 else -1
        if y < -8 or y > H + 8: continue
        glow(im, x + dn * 4, y, 7, RED, 0.2); d = ImageDraw.Draw(im)
        for dy, hh in ((0, h), (-3, h - 4), (3, h - 3)):
            d.polygon([(x, y + dy - 3), (x + dn * hh, y + dy), (x, y + dy + 3)], fill=(214, 48, 62)); d.line([x, y + dy - 2, x + dn * hh, y + dy], fill=(255, 160, 160))

@fx('ea_ghoul')
def _fx_ghoul(d, im, e, f):
    """A hunched grey ghoul clinging to the right wall: ('ea_ghoul', x, y(feet), look 0..1). It faces left, its
    eyes light up as it turns towards Claude."""
    _, x, y, look = e; G, RIM = (74, 76, 94), (150, 154, 176)
    d.line([x + 3, y - 4, x + 7, y], fill=G, width=2)
    d.ellipse([x - 5, y - 15, x + 7, y - 2], fill=G, outline=RIM)                       # the hump
    d.ellipse([x - 10, y - 12, x - 3, y - 5], fill=G, outline=RIM)                      # the head, low
    d.line([x - 4, y - 8, x - 9, y - 1], fill=G, width=2); d.line([x - 2, y - 7, x - 5, y], fill=G, width=2)    # arms hanging
    if look > 0.4:
        d.point((x - 9, y - 9), fill=RED); d.point((x - 7, y - 9), fill=RED)
        if look > 0.8: glow(im, x - 8, y - 9, 4, RED, 0.5)

@fx('ea_beast')
def _fx_beast(d, im, e, f):
    """The hulking grey beast of the lost miners, facing left: ('ea_beast', x, feet, hole 0..1, crumble 0..1[, hole_y[, light]])."""
    _, x, y, hole, cr, *r = e; hy = r[0] if r else y - 22; light = r[1] if len(r) > 1 else 0
    G, Gd, Gl, Gk = (98, 102, 120), (62, 66, 82), (140, 146, 164), (38, 40, 52)
    if cr >= 1: return
    j = int(cr * 8)
    d.rectangle([x - 12, y - 10, x - 4, y], fill=Gd); d.rectangle([x + 6, y - 10, x + 14, y], fill=Gk)                 # stubby legs
    d.line([x - 4, y - 30 + j, x - 14, y - 14, x - 18, y - 3], fill=Gd, width=5)                                       # the far arm
    d.ellipse([x - 24, y - 46 + j, x + 26, y - 10], fill=Gd)                                                           # the hump
    for lx, ly, rr_ in ((20, -40, 6), (26, -28, 5), (8, -47, 6), (-6, -48, 5), (24, -16, 5), (-24, -22, 5)):          # merged bodies: a lumpy outline
        d.ellipse([x + lx - rr_, y + ly - rr_ + j, x + lx + rr_, y + ly + rr_ + j], fill=Gd)
    d.ellipse([x - 22, y - 36 + j, x + 12, y - 8], fill=G)                                                             # the chest
    d.ellipse([x - 24, y - 42 + j, x - 4, y - 28 + j], fill=Gl)                                                        # a shoulder catching the light
    d.ellipse([x + 4, y - 44 + j, x + 22, y - 30 + j], fill=G)
    d.ellipse([x - 27, y - 37 + j, x - 14, y - 26 + j], fill=Gk)                                                       # the small head, sunk between the shoulders
    for ex, ey in ((-25, -33), (-22, -35), (-24, -30), (-20, -32)): d.point((x + ex, y + ey + j), fill=RED)
    glow(im, x - 22, y - 32 + j, 7, RED, 0.4); d = ImageDraw.Draw(im)
    d.line([x - 20, y - 34 + j, x - 33, y - 16, x - 31, y - 4], fill=G, width=5)                                       # the near arm, knuckles on the ground
    d.ellipse([x - 36, y - 7, x - 26, y + 1], fill=Gl); d.rectangle([x - 35, y - 3, x - 27, y - 2], fill=Gd)
    for cx_, cy_, h in ((-2, -46, 10), (8, -48, 13), (18, -44, 9), (26, -33, 8), (-12, -44, 7), (14, -17, 6)): crystal(d, x + cx_, y + cy_ + j, h, 3)
    if hole > 0:
        r_ = int(2 + 7 * hole); hx = x - 10
        d.ellipse([hx - r_ - 1, hy - r_ - 1, hx + r_ + 1, hy + r_ + 1], fill=TEAL)
        d.ellipse([hx - r_ + 1, hy - r_ + 1, hx + r_ - 1, hy + r_ - 1], fill=TEAL_L if light else (14, 8, 18))
        if light: glow(im, hx, hy, r_ + 6, TEAL_L, 0.55)

@fx('ea_ledge')
def _fx_ledge(d, im, e, f):
    """A crystal ledge Claude stands on, a few px above the floor: ('ea_ledge',)."""
    d.rectangle([0, GROUND - 5, 112, GROUND + 1], fill=(74, 42, 56)); d.line([0, GROUND - 5, 112, GROUND - 5], fill=(150, 70, 84)); d.line([112, GROUND - 5, 112, GROUND + 1], fill=(40, 20, 34))
    for x, h in ((4, 8), (10, 5), (104, 7), (109, 4)): crystal(d, x, GROUND - 5, h, 2)

@fx('ea_supay')
def _fx_supay(d, im, e, f):
    """The Supay crawling out of the water: ('ea_supay', x, k 0..1)."""
    _, x, k = e; wl = 38
    top = int(wl + 4 - 38 * ease(k))                                                       # the head's top
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    skin = (150, 30, 40); horn = (232, 224, 196)
    ld.polygon([(x - 18, top + 36), (x - 14, top + 14), (x - 6, top + 8), (x + 6, top + 8), (x + 14, top + 14), (x + 18, top + 36)], fill=(120, 20, 34))   # shoulders
    ld.ellipse([x - 11, top, x + 11, top + 20], fill=skin, outline=(60, 8, 18))                                                                # the head
    for sgn in (-1, 1):
        ld.line([x + sgn * 8, top + 3, x + sgn * 14, top - 8, x + sgn * 11, top - 16], fill=horn, width=2)                   # curved horns
        ld.line([x + sgn * 11, top - 16, x + sgn * 7, top - 20], fill=horn)
        ld.line([x + sgn * 16, top + 28, x + sgn * 24, top + 20, x + sgn * 30 * (1 if k > 0.5 else 0.7), top + 22], fill=(120, 20, 34), width=3)   # arms
        for t in (-2, 0, 2): ld.line([x + sgn * 30 * (1 if k > 0.5 else 0.7), top + 22, x + sgn * (33 + t), top + 22 + t], fill=horn)           # claws
    for sgn in (-1, 1): ld.rectangle([x + sgn * 5 - 1, top + 7, x + sgn * 5 + 1, top + 9], fill=(214, 255, 70))
    for i in range(-4, 5, 2): ld.polygon([(x + i - 1, top + 14), (x + i + 1, top + 14), (x + i, top + 17)], fill=(250, 250, 240))   # the grin
    ld.line([x - 5, top + 13, x + 5, top + 13], fill=(60, 8, 18))
    ld.rectangle([0, wl + 3 + (0 if k > 0.8 else int((1 - k) * 4)), W, H], fill=(0, 0, 0, 0))                          # hidden below the water
    im.paste(lay, (0, 0), lay); d = ImageDraw.Draw(im)
    glow(im, x - 5, top + 8, 5, (214, 255, 70), 0.4); glow(im, x + 5, top + 8, 5, (214, 255, 70), 0.4); d = ImageDraw.Draw(im)
    for r in (14, 22): d.ellipse([x - r - 8, wl + 2, x + r + 8, wl + 4 + r // 6], outline=(190, 60, 56))                  # ripples

@fx('ea_net')
def _fx_net(d, im, e, f):
    """The net bulging as the ball hits it: ('ea_net', frames since)."""
    k = e[1]
    for i in range(3):
        r = 3 + k + i * 3
        if k < 12: d.arc([164 - r, 40 - r, 164 + r, 40 + r], 100, 260, fill=(250, 250, 244))

@fx('ea_ball')
def _fx_ball(d, im, e, f):
    """The ball: ('ea_ball', x, y, charged): charged crackles teal."""
    _, x, y, ch = e
    if ch:
        rr = random.Random(int(x) * 7 + int(y) + f)
        for _ in range(6):
            a = rr.uniform(0, 6.28); L = rr.randint(3, 7); d.line([x, y, x + math.cos(a) * L, y + math.sin(a) * L], fill=rr.choice([TEAL, TEAL_L]))
        glow(im, x, y, 7, TEAL, 0.45); d = ImageDraw.Draw(im)
    d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(250, 250, 250), outline=INK); d.point((x, y), fill=INK)

@fx('ea_fist')
def _fx_fist(d, im, e, f):
    """A fist on fire with teal light: ('ea_fist', x, y, r)."""
    _, x, y, r = e
    glow(im, x, y, r + 5, TEAL, 0.6); d = ImageDraw.Draw(im)
    d.ellipse([x - r, y - r, x + r, y + r], fill=TEAL); d.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], fill=TEAL_L)
    rr = random.Random(f * 31 + int(x))
    for _ in range(5): a = rr.uniform(0, 6.28); d.line([x + math.cos(a) * r, y + math.sin(a) * r, x + math.cos(a) * (r + 5), y + math.sin(a) * (r + 5)], fill=TEAL_L)

@fx('ea_shards')
def _fx_shards(d, im, e, f):
    """Red crystal shards flying out of (x, y): ('ea_shards', x, y, frames since)."""
    _, x, y, k = e; rr = random.Random(5)
    for i in range(16):
        a = rr.uniform(0, 6.28); v = rr.uniform(2, 5); px, py = x + math.cos(a) * v * k, y + math.sin(a) * v * k + 0.25 * k * k
        d.rectangle([px, py, px + 1, py + 1], fill=rr.choice([RED, (255, 140, 140), TEAL_L]))

def slope_y2(x): return 62 - 0.13 * x

@fx('ea_ground')
def _fx_ground(d, im, e, f):
    """The dusty slope, its dust streaming back, and glowing cracks: ('ea_ground', scroll, crack 0..1)."""
    _, sc, cr = e
    d.polygon([(0, 64), (0, slope_y2(0)), (W, slope_y2(W)), (W, 64)], fill=(214, 138, 72))
    d.polygon([(0, 64), (0, slope_y2(0) + 8), (W, slope_y2(W) + 8), (W, 64)], fill=(176, 100, 56))
    for i in range(9):
        x = (i * 41 - sc * 3) % (W + 30) - 15; y = slope_y2(x) + 3 + i * 5 % 12; d.line([x, y, x + 12, y - 2.5], fill=(238, 170, 100))
    if cr > 0:
        rr = random.Random(9)
        for i in range(6):
            x = 96 + rr.randint(-30, 50); y = slope_y2(x) + 4; n = int(14 * cr)
            pts = [(x + j * 3 + rr.randint(-1, 1), y + j * 0.4 + rr.randint(-2, 2)) for j in range(max(2, n // 3))]
            d.line(pts, fill=BLUE_L if f % 4 < 2 else BLUE)

@fx('ea_apu')
def _fx_apu(d, im, e, f):
    """The Apu: a huge stone llama, head and long neck in profile facing right, two banana ears, a slit eye, blue glyph
    bands round the neck: ('ea_apu', dx, dy, flare 0..1 (the eye), glyph 0..1[, bow 0..1: the head tips forward and down])."""
    _, dx, dy, fl, gl, *b = e; bow = b[0] if b else 0
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    sq = lambda y: y if y >= 40 else 40 - (40 - y) * 0.8                                                       # a shorter head over the long neck
    P = lambda pts: [(x + dx, sq(y) + dy) for x, y in pts]; OUTL = (40, 32, 46)
    SD, SM, SL, SLL = (78, 68, 82), (112, 98, 102), (164, 136, 124), (214, 172, 134)
    L = lambda y: 90 - (y - 30) * 0.25; R = lambda y: 110 + (y - 30) * 0.3
    ear = lambda pts, c: ld.polygon(P(pts), fill=c, outline=OUTL)
    ear([(94, 18), (88, 8), (84, 0), (87, -1), (95, 5), (103, 15)], SD)                                            # far ear, banana, up and back
    ear([(102, 16), (97, 6), (95, 0), (98, -1), (105, 5), (111, 14)], SM)                                         # near ear
    ld.line(P([(97, 4), (101, 12)]), fill=SL)
    ld.polygon(P([(86, 26), (L(70), 70), (R(70), 70), (114, 36)]), fill=SM, outline=OUTL)                         # the long neck
    ld.polygon(P([(86, 26), (L(70), 70), (L(70) + 10, 70), (100, 30)]), fill=SD)                                  # shadowed left
    ld.polygon(P([(110, 34), (R(70) - 8, 70), (R(70), 70), (114, 36)]), fill=SL)                                  # sunset-lit right edge
    head = [(86, 26), (88, 17), (95, 13), (110, 12), (124, 17), (138, 23), (147, 28), (150, 33), (146, 38), (134, 39), (120, 37), (112, 35)]
    ld.polygon(P(head), fill=SM, outline=OUTL)
    ld.polygon(P([(88, 17), (95, 13), (110, 12), (124, 17), (138, 23), (147, 28), (140, 27), (124, 22), (110, 17), (96, 18)]), fill=SL)   # lit forehead and bridge
    ld.polygon(P([(110, 12), (124, 17), (131, 20), (118, 17)]), fill=SLL)
    ld.polygon(P([(86, 26), (88, 17), (96, 18), (100, 28), (112, 35), (100, 34)]), fill=SD)                      # dark back of the head
    ld.polygon(P([(112, 35), (120, 37), (134, 39), (146, 38), (140, 36), (122, 34)]), fill=SD)                    # under the jaw
    ld.line(P([(114, 31), (124, 33), (134, 30)]), fill=SD)                                                         # carved chevron cheek
    ld.polygon(P([(143, 26), (147, 28), (150, 33), (147, 35), (144, 31)]), fill=SLL)                             # blunt muzzle, lit
    ld.line(P([(139, 34), (148, 33)]), fill=(34, 28, 38)); ld.point(P([(145, 29)])[0], fill=(34, 28, 38))        # mouth, nostril
    gc = mix((90, 90, 104), mix((60, 120, 190), BLUE, 0.5 + 0.5 * math.sin(f * 0.5)), gl)
    for k, y in enumerate((34, 41, 48, 55)):                                                                       # glyph bands round the neck
        xl, xr = int(L(y)) + 1, int(R(y)) - 1
        ld.polygon(P([(xl, y), (xr, y), (xr, y + 5), (xl, y + 5)]), fill=mix((56, 52, 70), (34, 48, 100), gl))
        for i, x in enumerate(range(xl + 2, xr - 4, 6)):
            xx, yy = x + dx, y + dy; t = (i + k) % 4
            if t == 0: ld.line([(xx, yy + 4), (xx, yy + 2), (xx + 2, yy + 2), (xx + 2, yy), (xx + 4, yy)], fill=gc)      # step-fret
            elif t == 1: ld.polygon([(xx + 2, yy), (xx + 4, yy + 2), (xx + 2, yy + 4), (xx, yy + 2)], outline=gc)         # diamond
            elif t == 2: ld.line([(xx, yy + 4), (xx + 1, yy + 1), (xx + 2, yy + 4), (xx + 3, yy + 1), (xx + 4, yy + 4)], fill=gc)   # zigzag
            else: ld.point([(xx + 2, yy), (xx + 2, yy + 1), (xx, yy + 2), (xx + 1, yy + 2), (xx + 2, yy + 2), (xx + 3, yy + 2), (xx + 4, yy + 2), (xx + 2, yy + 3), (xx + 2, yy + 4)], fill=gc)   # chakana cross
    ec = BLUE_L if fl > 0.5 else (130, 180, 240); w = 1 + int(2 * fl)
    ld.polygon(P([(120, 20), (134, 24), (133, 26 + w // 2), (121, 22 + w // 2)]), fill=ec)                         # the narrow slanted blue eye
    piv = (98 + dx, 52 + dy); ang = -30 * bow
    if bow: lay = lay.rotate(ang, resample=Image.NEAREST, center=piv)
    im.paste(lay, (0, 0), lay)
    a = math.radians(ang); vx, vy = 128 + dx - piv[0], sq(23) + dy - piv[1]
    ex, ey = piv[0] + vx * math.cos(a) + vy * math.sin(a), piv[1] - vx * math.sin(a) + vy * math.cos(a)
    glow(im, ex, ey, int(4 + 9 * fl), BLUE, 0.3 + 0.5 * fl)

@fx('ea_rock')
def _fx_rock2(d, im, e, f):
    """A falling rock: ('ea_rock', x, y, size)."""
    _, x, y, s = e
    d.rectangle([x, y, x + s, y + s], fill=(96, 84, 90)); d.rectangle([x, y, x + s - 2, y + 1], fill=(150, 130, 126)); d.line([x + 1, y - s * 2, x + 1, y - 1], fill=(246, 190, 120))

@fx('ea_ride')
def _fx_ride(d, im, e, f):
    """A rider seated on a long, low dirt bike (teal-ringed wheels), tilted up the slope; Cal (orange fringe, mustard tee)
    or Pietro (navy hair, maroon jacket), told apart by the palette: ('ea_ride', unused, pal, x, y, ring 0..1)."""
    _, _, pal, x, y, ring = e
    lay = Image.new('RGBA', (64, 40), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rc = mix((70, 70, 80), TEAL, ring); FR, FRL = (52, 40, 44), (150, 116, 96)
    for wx in (11, 46):
        ld.ellipse([wx - 6, 26, wx + 5, 37], fill=(26, 22, 30)); ld.ellipse([wx - 4, 28, wx + 3, 35], outline=rc)
        a = f * 0.9 + wx
        for k in range(2): ld.point((wx - 0.5 + math.cos(a + k * math.pi) * 2.5, 31.5 + math.sin(a + k * math.pi) * 2.5), fill=TEAL_L if ring > 0.5 else (150, 150, 160))
        ld.point((wx - 1, 31), fill=(190, 180, 170))
    ld.arc([4, 22, 18, 36], 200, 330, fill=FR, width=2); ld.arc([39, 22, 53, 36], 200, 340, fill=FR, width=2)          # mudguards
    ld.line([11, 31, 22, 28], fill=FR, width=2)                                                                         # swingarm
    ld.polygon([(16, 25), (22, 23), (40, 23), (42, 27), (36, 29), (20, 29)], fill=FR); ld.line([20, 23, 40, 23], fill=FRL)   # long low body
    ld.polygon([(12, 25), (28, 22), (28, 24), (14, 27)], fill=(24, 20, 26)); ld.line([13, 24, 27, 22], fill=(90, 80, 84))   # the long seat
    ld.line([38, 24, 45, 31], fill=(120, 112, 118), width=2); ld.line([38, 25, 44, 31], fill=(40, 36, 44))              # the chunky fork
    ld.line([37, 19, 40, 17], fill=(30, 26, 30), width=2); ld.line([38, 23, 37, 19], fill=(90, 82, 88))                 # the bars
    cal_ = 'O' in pal; skin = pal['s']
    pants, shirt = ((42, 42, 58), pal['j']) if cal_ else ((40, 36, 48), (178, 40, 58))
    ld.line([19, 21, 28, 24], fill=pants, width=3); ld.line([28, 24, 23, 29], fill=pants, width=2); ld.rectangle([21, 29, 25, 30], fill=(20, 18, 24))   # thigh, shin, boot on the peg
    ld.line([21, 21, 29, 13], fill=shirt, width=5)                                                                      # torso leaning forward
    ld.line([28, 15, 38, 18], fill=shirt, width=2); ld.point((39, 18), fill=skin)                                         # arm to the bars
    if not cal_: ld.line([22, 19, 27, 14], fill=(240, 196, 70))                                                         # gold stripe
    else: ld.line([29, 12, 31, 11], fill=TEAL, width=1)                                                                 # choker
    ld.ellipse([28, 6, 34, 12], fill=skin)
    if cal_:
        ld.polygon([(27, 8), (28, 4), (31, 3), (34, 5), (35, 8), (33, 7), (30, 7)], fill=ORANGE)                         # orange fringe
    else:
        ld.polygon([(26, 10), (27, 5), (31, 4), (35, 6), (34, 8), (30, 7), (28, 10)], fill=pal['n'])                     # navy hair
    lay = lay.rotate(8, resample=Image.NEAREST, expand=True)
    im.paste(lay, (int(x - lay.width / 2), int(y - lay.height + 7)), lay)
    if ring > 0.5:
        for k in range(4): d.point((x - 32 - k * 3, y - 1 - k % 2 - k // 2), fill=TEAL_L if k == 0 else (240, 190, 130))   # dust behind the rear wheel

# ---- the close-ups -----------------------------------------------------------------------------------------
def _supay_face(im, d, t, f):
    d.rectangle([0, 0, W, H], fill=(150, 18, 28)); dx = int(lerp(2, -2, ease(t)))
    horn = (236, 228, 200); skin = (124, 22, 34)
    for sgn, x0 in ((-1, 14), (1, 62)):
        d.line([x0 + dx, 22, x0 + sgn * 6 + dx, 8, x0 + sgn * 2 + dx, -2], fill=horn, width=4); d.line([x0 + dx, 22, x0 + sgn * 6 + dx, 8], fill=(190, 180, 150), width=1)
    d.ellipse([10 + dx, 14, 70 + dx, 72], fill=skin, outline=(70, 8, 22))
    ex, ey = 46 + dx, 30
    glow(im, ex, ey, 14, (214, 255, 70), 0.5 + 0.2 * math.sin(f)); d = ImageDraw.Draw(im)
    d.ellipse([ex - 9, ey - 5, ex + 9, ey + 5], fill=(226, 255, 90), outline=(120, 150, 20)); d.rectangle([ex - 1, ey - 5, ex + 1, ey + 5], fill=(30, 8, 12))
    d.line([ex - 12, ey - 8, ex + 10, ey - 11], fill=(60, 8, 18), width=2)
    d.rectangle([14 + dx, 50, 66 + dx, 52], fill=(40, 4, 12))
    for i in range(16, 66, 5): d.polygon([(i + dx, 51), (i + 4 + dx, 51), (i + 2 + dx, 58)], fill=(250, 248, 236)); d.polygon([(i + dx, 51), (i + 4 + dx, 51), (i + 2 + dx, 45)], fill=(250, 248, 236))
    pal = (92, 12, 24)
    d.polygon([(-2, 66), (0, 40), (16, 34), (26, 44), (22, 66)], fill=pal, outline=(60, 6, 16))                       # the palm
    for fx_, fy_ in ((34, 20), (44, 18), (52, 22), (58, 30)):                                                         # claws across the eye
        d.line([12, 48, fx_, fy_], fill=pal, width=3); d.line([12, 48, fx_, fy_], fill=(60, 6, 16), width=1)
        d.polygon([(fx_ - 2, fy_ + 1), (fx_ + 2, fy_ + 4), (fx_ + 5, fy_ - 4)], fill=horn)

def _cal_face(im, d, t, f):
    d.rectangle([0, 0, W, H], fill=(40, 14, 30)); k = ease((t - 0.15) / 0.3)
    skin = mix(SKIN, RSKIN, k); x = 38
    d.ellipse([12, 4, 32, 36], fill=(22, 20, 30)); d.ellipse([6, 0, 16, 10], fill=(22, 20, 30))                          # the black hair and its topknot
    d.polygon([(x - 18, 11), (x - 16, 28), (x - 10, 42), (x, 47), (x + 10, 42), (x + 17, 28), (x + 18, 11)], fill=skin)    # the face
    d.polygon([(x - 19, 14), (x - 15, 3), (x - 10, 11), (x - 5, -2), (x, 9), (x + 6, 0), (x + 10, 11), (x + 16, 3), (x + 19, 14),
               (x + 17, 22), (x + 12, 17), (x + 4, 22), (x - 4, 16), (x - 12, 22)], fill=ORANGE)                       # the orange fringe
    for ex in (x - 8, x + 7):
        d.ellipse([ex - 4, 24, ex + 4, 30], fill=mix((240, 240, 240), (4, 2, 8), k))                                   # the sclera goes black
        d.rectangle([ex - 1, 25, ex + 1, 29], fill=mix(INK, (232, 232, 240), k * 0.9))
    d.line([x - 14, 21, x - 3, 24], fill=(22, 20, 30), width=2); d.line([x + 3, 24, x + 14, 21], fill=(22, 20, 30), width=2)
    d.line([x - 5, 38, x + 5, 38], fill=mix((60, 30, 24), (30, 4, 10), k))
    d.rectangle([x - 8, 47, x + 8, 49], fill=teal(f))                                                                   # the choker
    d.polygon([(x - 30, 64), (x - 26, 52), (x - 8, 49), (x + 8, 49), (x + 26, 52), (x + 30, 64)], fill=(214, 164, 52))
    d.polygon([(x - 9, 49), (x + 9, 49), (x + 3, 57), (x - 3, 57)], fill=(30, 48, 104))
    gx, gy = x, 59
    if t > 0.45:
        g = ease((t - 0.45) / 0.3); glow(im, gx, gy, int(4 + 8 * g), TEAL, 0.7 * g); d = ImageDraw.Draw(im)
    xc = mix((246, 246, 250), TEAL_L, ease((t - 0.45) / 0.3))
    d.line([gx - 3, gy - 3, gx + 3, gy + 3], fill=xc, width=2); d.line([gx - 3, gy + 3, gx + 3, gy - 3], fill=xc, width=2)

def _hands(im, d, t, f):
    """Pietro's hands, seen from the front, making the mountain sign: thumbs touching at the bottom, index fingers at
    the top, a triangle between them with the sky showing through (it glows teal-white), sleeves going out of frame."""
    for y in range(H): d.line([0, y, W, y], fill=mix((244, 150, 100), (255, 224, 160), y / H))
    G, GL, TIP, cx = (24, 22, 32), (70, 66, 88), teal(f), 38
    g = ease((t - 0.3) / 0.4)
    tri = [(cx, 12), (cx + 14, 40), (cx - 14, 40)]
    d.polygon(tri, fill=mix((255, 226, 170), TEAL_L, g))                                                              # the sky through the triangle
    if g > 0: glow(im, cx, 32, int(10 + 12 * g), TEAL, 0.65 * g); d = ImageDraw.Draw(im)
    for s in (-1, 1):
        px = cx + s * 22
        d.polygon([(px - 8, 64), (px + 8, 64), (px + 6, 50), (px - 6, 50)], fill=(170, 40, 56))                       # the maroon sleeve, gold stripes
        d.line([px - 3, 50, px - 4, 64], fill=(240, 196, 70)); d.line([px + 3, 50, px + 4, 64], fill=(240, 196, 70))
        d.rectangle([px - 7, 47, px + 7, 51], fill=G); d.line([px - 7, 49, px + 7, 49], fill=TIP)                      # the glove's teal cuff
        d.ellipse([px - 9, 33, px + 9, 49], fill=G, outline=GL)                                                        # the palm
        for k in range(3): d.ellipse([px + s * 9 - 2 + s * 0, 36 + k * 4 - 1, px + s * 9 + 3, 36 + k * 4 + 3], fill=G, outline=GL)   # curled fingers
        d.line([px - s * 5, 36, cx + s * 1, 12], fill=G, width=4)                                                      # the index finger up to the apex
        d.line([px - s * 5, 36, cx + s * 1, 12], fill=GL, width=1)
        d.line([px - s * 3, 42, cx + s * 1, 43], fill=G, width=4)                                                      # the thumb along the base
        d.ellipse([cx + s * 2 - 2, 10, cx + s * 2 + 2, 14], fill=TIP); d.ellipse([cx + s * 2 - 2, 41, cx + s * 2 + 2, 45], fill=TIP)   # teal fingertips
    d.polygon([(cx, 17), (cx + 10, 38), (cx - 10, 38)], fill=mix((255, 226, 170), TEAL_L, g))

# ---- the clips -----------------------------------------------------------------------------------------------
def lookout(f, pose=None, x=CX):
    """The neutral pose: Claude on the lookout, the Black Mountain's red triangle pulsing, his teal pulsing."""
    s = scene(f, THEME); s['under'].append(('ea_logo', 151, 24, 6))
    s['actors'] = [actor(cal(pose or ready(f)), x, pal=cpal(f))]; return s

def shot(im): return {'image': im}

MECHS = ((54, 0.3), (88, 0.25), (126, 0.35))

def clip_salamanca(f):
    if f < 22 or f >= 286: return lookout(f)                                        # the lookout: the neutral pose
    if f < 56:                                                                      # under the full moon, three thin mechs climb the ridge
        s = scene(f, 'ea-ridge'); s['under'].append(('stars', {'n': 26, 'area': (0, 0, 108, 26)}))
        for i, (x0, sp) in enumerate(MECHS):
            x = x0 + (f - 22) * sp; s['under'].append(('ea_mech', x, slope_y(x) + 2, f * 0.35 + i * 2))
        return s
    if f < 86:                                                                      # Claude dashes along the ridge, a teal trail behind
        s = scene(f, 'ea-ridge'); x = -10 + (f - 56) * 7; s['under'].append(('stars', {'n': 26, 'area': (0, 0, 108, 26)}))
        for i, (x0, sp) in enumerate(MECHS):
            xm = x0 + (f - 22) * sp; s['under'].append(('ea_mech', xm, slope_y(xm) + 2, f * 0.35 + i * 2))
        s['actors'] = [actor(cal('dash' if f % 4 < 2 else 'run2'), x, pal=cpal(f))]
        s['fx'] += [('ea_trail', x - 6, GROUND - 8, x - 64, GROUND - 8), ('ea_trail', x - 6, GROUND - 3, x - 44, GROUND - 3)]
        return s
    if f < 150:                                                                     # down the shaft, feet on the wall, red crystals, ghouls turn, the beast rises
        s = scene(f, 'ea-mine'); k = f - 86
        s['under'].append(('ea_shaft', k * 4))
        for i, y in enumerate((20, 40, 60)): s['under'].append(('ea_ghoul', SR - 5, y, ease((f - 100 - i * 5) / 12)))
        if f >= 118: s['under'].append(('ea_beast', 94, 64 + 70 * (1 - ease((f - 118) / 28)), 0, 0))
        y = 30 + math.sin(k * 0.4) * 1.5
        s['fx'].append(('ea_rot', figure(CAL, POSES['wall' if f % 4 < 2 else 'dash']), cpal(f), SL + 11, y, -60))
        s['fx'] += [('ea_trail', SL + 2, y + 6, SL + 2, y - 34), ('ea_trail', SL + 6, y + 2, SL + 6, y - 24)]      # the teal jet, going UP behind him
        return s
    if f < 172:                                                                     # the red void: the Supay crawls out of the water
        s = scene(f, 'ea-void'); s['under'].append(('ea_supay', 96, ease((f - 150) / 20)))
        if f >= 164: s['shake'] = rshake(1)
        return s
    if f < 208:
        return shot(closeup((f - 172) / CLOSE_LEN, f, bg=(150, 18, 28), draw=_supay_face, txt='¿TENÉS MIEDO?', color=(255, 240, 150), outline=(70, 6, 16)))
    if f < 244:
        return shot(closeup((f - 208) / CLOSE_LEN, f, bg=(40, 14, 30), draw=_cal_face, txt='NO.', text_from=0.5, color=TEAL_L, outline=(10, 30, 36)))
    s = scene(f, 'ea-cave'); k = f - 244                                            # on a crystal ledge, the teal fist goes through the beast
    bx, hole, cr, pose, x, fy = 128, 0, 0, 'guard', 22, GROUND - 6
    if k >= 12: pose, x = 'jab', min(bx - 23, 22 + (k - 12) * 10)
    if k >= 20: hole = ease((k - 20) / 8); s['shake'] = rshake(2) if k < 30 else (0, 0)
    if k >= 32: cr = min(1, (k - 32) / 10)
    light = 1 if 24 <= k < 32 else 0                                                # light shows through the hole before he falls apart
    s['under'].append(('ea_ledge',))
    hx, hy = figure_point(CAL, POSES[pose], 'hand', x, fy)
    s['under'].append(('ea_beast', bx, GROUND, hole, cr, hy, light))
    s['actors'] = [actor(cal(pose), x, fy, pal=cpal(f))]
    if 12 <= k < 20: s['fx'].append(('ea_trail', x - 6, hy + 2, x - 40, hy + 2))
    if k >= 4: s['fx'].append(('ea_fist', hx + 1, hy + 1, max(1, 2 + min(4, (k - 4) // 2) - max(0, k - 34))))
    if k >= 20: s['fx'] += [('ea_fist', bx + 22, hy + 1, max(1, 5 - (k - 20) // 3)), ('ea_shards', bx + 22, hy, k - 20)]       # out through his back
    if k >= 32: s['fx'].append(('ea_shards', bx, GROUND - 46, k - 32))                                          # the crystals shatter
    if 20 <= k < 23: s['flash'] = 0.4; s['flashc'] = TEAL_L; s['fc'] = (bx, hy)
    return s

ST = Stage(far_y=38, near_y=62, vp_x=92, far_scale=0.7, far_below=0.3, far_k=0.8)   # the pitch seen at an angle
ZC, ZR, ZK = 0.82, 0.6, 0.04                                                           # depth: Claude near, the big guy behind, the kids by the rope
GOLAZO = '¡GOLAZO!'

# Hand-drawn poses (26x26 grids): the bicycle kick in three stills, Cal's celebration seen from the front, the big guy sat dazed.
def _thick(g, x0, y0, x1, y1, c, n=2, side=False):
    for i in range(n): seg(g, x0 + (i if side else 0), y0 + (0 if side else i), x1 + (i if side else 0), y1 + (0 if side else i), c)
def _fill(g, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): put(g, x, y, c)
def _x(g, pts):
    for x, y in pts: put(g, x, y, 'W')

_KICK = {}
def kick(k):
    """The bicycle kick: 'A' takes off leaning back, 'B' flat in the air, feet over head, 'C' the kick."""
    if k in _KICK: return _KICK[k]
    g = blank(26, 26)
    if k == 'A':
        _fill(g, 7, 4, 11, 8, 's'); _fill(g, 9, 2, 12, 3, 'O'); _fill(g, 8, 4, 12, 4, 'O'); put(g, 7, 3, 'h'); _fill(g, 6, 4, 6, 6, 'h'); put(g, 12, 3, 'O'); put(g, 11, 1, 'O')
        put(g, 9, 6, 'K'); put(g, 11, 6, 'K'); _fill(g, 8, 9, 10, 9, 'T')
        for i in range(4): seg(g, 8 + i, 10, 12 + i, 18, 'j')
        _fill(g, 8, 10, 11, 10, 'N'); _x(g, [(11, 13), (13, 13), (12, 14), (11, 15), (13, 15)])
        seg(g, 8, 11, 3, 8, 'k'); seg(g, 3, 8, 1, 4, 'k'); _fill(g, 1, 3, 2, 3, 't')
        seg(g, 13, 11, 18, 12, 'k'); seg(g, 18, 12, 21, 9, 'k'); _fill(g, 22, 8, 22, 9, 't')
        _thick(g, 12, 18, 13, 24, 'p', 2, True); _fill(g, 13, 25, 16, 25, 'u'); _fill(g, 12, 23, 14, 23, 'T')
        _thick(g, 14, 18, 20, 17, 'p', 2); _thick(g, 20, 17, 22, 21, 'p', 2, True); _fill(g, 22, 22, 25, 22, 'u')
    else:
        c = k == 'C'; hy = 17 if c else 15
        _fill(g, 3, hy, 7, hy + 4, 's'); _fill(g, 1, hy - 1, 2, hy + 5, 'O'); put(g, 0, hy + 1, 'O'); put(g, 0, hy + 3, 'O')
        _fill(g, 2, hy - 2, 3, hy - 2, 'h'); _fill(g, 2, hy + 6, 3, hy + 6, 'h')
        put(g, 6, hy + 1, 'K'); put(g, 6, hy + 3, 'K'); _fill(g, 8, hy, 8, hy + 3, 'T')
        for i in range(4): seg(g, 9, hy + i, 17, hy - 3 + i, 'j')
        _fill(g, 9, hy, 9, hy + 3, 'N'); _x(g, [(12, hy - 1), (14, hy - 1), (13, hy), (12, hy + 1), (14, hy + 1)])
        seg(g, 11, hy, 11, hy - 6, 'k'); seg(g, 11, hy - 6, 13, hy - 9, 'k'); _fill(g, 13, hy - 10, 14, hy - 10, 't')
        seg(g, 10, hy + 3, 6, hy + 7, 'k'); seg(g, 6, hy + 7, 3, min(25, hy + 9), 'k'); _fill(g, 2, min(25, hy + 10), 3, min(25, hy + 10), 't')
        if not c:
            _thick(g, 17, 12, 18, 2, 'p', 2, True); _fill(g, 18, 0, 21, 1, 'u'); _fill(g, 18, 4, 19, 4, 'T')
        else:
            _thick(g, 17, 14, 21, 4, 'p', 2, True); _fill(g, 21, 2, 24, 3, 'u'); _fill(g, 20, 6, 21, 6, 'T')
        _thick(g, 17, hy - 1, 22, hy + 1, 'p', 2); _thick(g, 22, hy + 1, 24, hy - 3, 'p', 2, True); _fill(g, 24, hy - 5, 25, hy - 4, 'u')
    _KICK[k] = to_sprite(g); return _KICK[k]
KICK_FOOT = (22, 3)                                                                   # where the ball meets the boot in 'C'

_FRONT = {}
def front(f):
    """Cal facing us, elbows wide, hands behind the head: a 'W' of arms over the hair; it sways on a 20-frame loop."""
    w = loop.wave(f, 20); key = (round(w), f % 2 if False else 0)
    sway = 1 if w > 0.5 else (-1 if w < -0.5 else 0); up = 1 if w > 0 else 0
    if (sway, up) in _FRONT: return _FRONT[(sway, up)]
    g = blank(26, 26); c = 13
    _fill(g, c - 2, 4, c + 2, 8, 's'); _fill(g, c - 3, 3, c + 3, 4, 'O'); put(g, c - 2, 2, 'O'); put(g, c, 1, 'O'); put(g, c + 2, 2, 'O'); put(g, c - 3, 5, 'h'); put(g, c + 3, 5, 'h'); put(g, c, 0, 'h'); put(g, c + 1, 0, 'h')
    put(g, c - 1, 6, 'K'); put(g, c + 1, 6, 'K'); _fill(g, c - 1, 9, c + 1, 9, 'T')
    _fill(g, c - 4, 10, c + 4, 17, 'j'); _fill(g, c - 4, 10, c + 4, 10, 'N'); _x(g, [(c - 1, 13), (c + 1, 13), (c, 14), (c - 1, 15), (c + 1, 15)])
    for s in (-1, 1):
        seg(g, c + s * 4, 11, c + s * 9, 10 + up, 'k'); seg(g, c + s * 9, 10 + up, c + s * 5, 4 + up, 'k')                   # upper arm out, forearm up behind the head
        put(g, c + s * 4, 4 + up, 't'); put(g, c + s * 5, 3 + up, 't')
        _fill(g, c + s * 3 - (1 if s < 0 else 0), 18, c + s * 3 + (0 if s < 0 else 1), 25, 'p'); _fill(g, c + s * 3 - 1 - (1 if s < 0 else 0), 25, c + s * 3 + 1 + (0 if s < 0 else 1), 25, 'u')
        _fill(g, c + s * 3 - (1 if s < 0 else 0), 23, c + s * 3 + (0 if s < 0 else 1), 23, 'T')
    g = [([ '.'] * sway + r)[:26] if sway > 0 else (r[-sway:] + ['.'] * -sway if sway < 0 else r) for r in g]
    _FRONT[(sway, up)] = to_sprite(g); return _FRONT[(sway, up)]

_SIT = []
def sit():
    """The big guy sat on the ground, dazed (facing right: drawn flipped)."""
    if _SIT: return _SIT[0]
    g = blank(28, 20); c = 12
    _fill(g, c - 2, 1, c + 2, 5, 's'); put(g, c, 3, 'K'); put(g, c + 2, 3, 'K'); put(g, c + 1, 5, 'K'); put(g, c + 2, 5, 'K')
    _fill(g, c - 4, 6, c + 4, 13, 'k'); seg(g, c - 4, 7, c - 8, 13, 's'); seg(g, c - 3, 7, c - 7, 13, 's'); seg(g, c + 4, 8, c + 7, 13, 's')
    _fill(g, c - 4, 14, c + 14, 16, 'q'); _fill(g, c + 13, 12, c + 15, 16, 'b'); _fill(g, c - 1, 17, c + 14, 17, 'q')
    _SIT.append(to_sprite(g)); return _SIT[0]

def clip_potrero(f):
    if f < 16 or f >= 160: return lookout(f)
    s = scene(f, 'ea-pitch')
    wx = lerp(-15, 72, (f - 16) / 48) if f < 64 else (lerp(72, 134, (f - 64) / 12) if f < 76 else 134)
    cxs, Fy = ST.proj(wx, ZC); items = []
    # the big bald guy blocks the way, lunges, is fooled, and sits dazed
    if f < 80:
        rp = pose_cycle(f, 'guard', 'guard2') if f < 64 else ('jab' if f < 72 else 'hurt')
        items.append((ZR, ST.place(figure(BIG, POSES[rp]), 96, ZR, flip=True, pal=BPAL)))
    else:
        items.append((ZR, ST.place(sit(), 96, ZR, flip=True, pal=BPAL)))
        if f < 150: s['fx'].append(('dizzy', 96 + 3, ST.proj(96, ZR)[1] - 17))
    for i, (spec, wk) in enumerate(zip(KIDS, (-22, -8, 6))):                       # the kids at the rope jump after the goal
        up = 108 <= f < 156; hop = int(abs(math.sin((f - 108 + i * 2) * 0.5)) * 4) if up else 0
        items.append((ZK, ST.place(figure(spec, POSES['cheer' if up else 'stand']), wk, ZK, h=hop, pal=KPAL)))
    rot = None                                                                      # Claude: running, then the three kick stills, then the front-facing celebration
    if f < 74: items.append((ZC, actor(cal('run1' if f % 6 < 3 else 'run2'), cxs, Fy, pal=cpal(f))))
    elif f < 86: items.append((ZC, actor(cal('guard' if f < 82 else 'crouch'), cxs, Fy, pal=cpal(f))))
    elif f < 116:
        kc = {86: 'A', 90: 'B', 94: 'C'}
        st = 'A' if f < 90 else ('B' if f < 94 else ('C' if f < 98 else 'B'))
        if f < 98: cx, cy = (cxs - 4 + (f - 86), Fy - 18 - (f - 86) * 2) if f < 90 else (131, 36 - (f - 90) // 2) if f < 94 else (130, 32)
        else: u = min(1, (f - 98) / 10); cx, cy = 130 - 3 * u, lerp(32, Fy - 14, u * u)
        items.append((ZC, actor(kick(st), cx, cy + 13, pal=cpal(f))))
    elif f < 122: items.append((ZC, actor(cal('crouch' if f >= 118 else 'hurt'), cxs - 3, Fy, pal=cpal(f))))
    else: items.append((ZC, actor(front(f), 131, Fy, pal=cpal(f))))
    s['actors'] = ST.back_to_front(items)
    if 68 <= f < 74: s['fx'].append(('ring', cxs + 4, Fy - 1, 2 + (f - 68) * 2, TEAL))                       # a sneaker flashes teal
    ch = False                                                                      # the ball
    if f < 76: bx, by = cxs + 9, Fy - 2 - abs(math.sin(f * 0.8)) * 3
    elif f < 90: u = (f - 76) / 14; bx, by = lerp(cxs + 9, 138, u), lerp(Fy - 2, 20, 1 - (1 - u) ** 2)
    elif f < 96: bx, by = 138, 20 + (f - 90) * 0.2
    elif f < 106: u = (f - 96) / 10; bx, by = lerp(138, 166, u), lerp(21, 41, u); ch = True
    else: bx, by = 166, min(47, 41 + (f - 106) * 0.8)
    if 90 <= f < 106: ch = True
    if f < 150: s['fx'].append(('ea_ball', bx, by, ch))
    if 94 <= f < 98: s['fx'].append(('spark', 138, 21, 5 - (f - 94)))
    if 106 <= f < 118: s['fx'].append(('ea_net', f - 106))
    if 106 <= f < 112: s['shake'] = rshake(1)
    if cue(f, 106, GOLAZO): s['fx'].append(('caption', GOLAZO, dict(box=(2, 1, W - 2, 25), color=(255, 232, 90), outline=(70, 30, 20), shadow=None, max_scale=3)))
    return s

@fx('ea_tri')
def _fx_tri(d, im, e, f):
    """The mountain sign glowing: ('ea_tri', x, y, size, strength 0..1)."""
    _, x, y, r, a = e
    glow(im, x, y, int(r * 2), TEAL, 0.6 * a); d = ImageDraw.Draw(im)
    d.polygon([(x, y - r), (x + r, y + r * 0.8), (x - r, y + r * 0.8)], outline=mix(TEAL, TEAL_L, a))

ROCKS = ((70, 100, 6), (92, 106, 7), (122, 112, 6), (82, 118, 5), (106, 124, 7), (60, 130, 6))
APU_TXT, SIGN_TXT = 'APU...', 'PERMISO, APU.'

def clip_apu(f):
    if f < 20 or f >= 260: return lookout(f)
    if 140 <= f < 176:
        return shot(closeup((f - 140) / 36, f, bg=(244, 150, 100), draw=_hands, txt=APU_TXT, color=BLUE_L, outline=(20, 30, 70)))
    s = scene(f, 'ea-slope')
    cr = ease((f - 60) / 20) if f < 176 else 0
    if f < 176: dy = -4 if f < 70 else -4 + 74 * (1 - ease((f - 70) / 30))
    else: dy = -4 + 80 * ease((f - 212) / 16)
    fl = 1.0 if f < 176 else 1 - 0.85 * ease((f - 182) / 20)
    bow = ease((f - 198) / 14) if f >= 198 else 0
    if 70 <= f < 230: s['under'].append(('ea_apu', -14, dy, fl, 1.0, bow))
    s['under'].append(('ea_ground', f if f < 140 or f >= 220 else 140, cr))
    if 62 <= f < 104: s['shake'] = rshake(1)
    if f < 140:                                                                      # riding up the slope; Claude swerves, Pietro stalls
        sw = 7 * math.sin(math.pi * (f - 104) / 30) if 104 <= f < 134 else 0
        cx_ = 112 - (max(0, f - 126) * 1.6 if f > 126 else 0)
        px = max(64 - ((f - 118) * 1.4 if f > 118 else 0), 44)
        s['fx'].append(('ea_ride', figure(PIETRO, POSES['crouch']), ppal(f), px, slope_y2(px) + 8, 1 - ease((f - 118) / 10)))
        s['fx'].append(('ea_ride', cal('crouch'), cpal(f), cx_, slope_y2(cx_) + 4 + sw, 1.0 if f < 128 else 0.3))
        for x, t0, sz in ROCKS:
            y = (f - t0) * 4 - 8; g = slope_y2(x) + 2
            if 0 <= f - t0: s['fx'].append(('ea_rock', x, min(y, g), sz))
    elif f < 228:                                                                    # the sign: both make it, the Apu calms and bows
        t = min(1, (f - 176) / 14)
        s['actors'] = [actor(figure(PIETRO, POSES['sign']), 36, slope_y2(36) + 8, pal=ppal(f)), actor(cal('sign'), 62, slope_y2(62) + 8, pal=cpal(f))]
        for x, sp in ((36, PIETRO), (62, CAL)):
            hx, hy = figure_point(sp, POSES['sign'], 'hand', x, slope_y2(x) + 8); s['fx'].append(('ea_tri', hx, hy, 3, ease(t)))
        if cue(f, 184, SIGN_TXT): s['fx'].append(('caption', SIGN_TXT, dict(box=(2, 1, W - 2, 25), color=BLUE_L, outline=(40, 24, 70), shadow=None, max_scale=2)))
        if 212 <= f < 228: s['fx'] += [('dust', 100 + (i * 17 + f * 3) % 70, slope_y2(140) + 4 - (f + i) % 6) for i in range(6)]
    else:                                                                            # they ride off, the way open
        u = f - 228
        for spr, pl, x0 in ((figure(PIETRO, POSES['crouch']), ppal(f), 36), (cal('crouch'), cpal(f), 62)):
            x = x0 + u * 4.2 + 0.02 * u * u; s['fx'].append(('ea_ride', spr, pl, x, slope_y2(x) + 8, 1.0))
    return s

CLIPS = [clip('salamanca', 300, clip_salamanca), clip('potrero', 180, clip_potrero), clip('apu', 280, clip_apu)]
