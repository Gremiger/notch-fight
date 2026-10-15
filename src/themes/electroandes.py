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
    return {'s': (150, 100, 70), 'K': INK, 'n': (34, 46, 100), 'm': (136, 36, 50), 'y': (232, 190, 70), 'k': (28, 26, 38),
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
    """The mine shaft, scrolling up as Claude runs down: ('ea_shaft', offset)."""
    off = e[1]; L, R = SL, SR
    d.rectangle([0, 0, L, H], fill=(52, 34, 46)); d.rectangle([R, 0, W, H], fill=(52, 34, 46))
    d.line([L, 0, L, H], fill=(96, 56, 66)); d.line([R, 0, R, H], fill=(96, 56, 66))
    for y in range(-12, H + 12, 12): yy = y + int(off) % 12; d.line([0, yy, L - 2, yy], fill=(44, 28, 40)); d.line([R + 2, yy, W, yy], fill=(44, 28, 40))
    for k in range(2):                                                   # timber beams across
        y = int((k * 36 - off) % 72) - 8; d.rectangle([L, y, R, y + 2], fill=(86, 58, 44)); d.line([L, y, R, y], fill=(120, 84, 60))
    for i, (side, y0, h) in enumerate(((0, 6, 9), (1, 20, 12), (0, 30, 6), (1, 44, 10), (0, 52, 8), (1, 58, 7), (0, 18, 7), (1, 2, 8))):
        y = int((y0 * 2.2 - off * 1.0) % 90) - 10
        glow(im, L - 4 if side == 0 else R + 4, y, 8, RED, 0.25)
        if side == 0:
            for dx, hh in ((0, h), (-3, h - 3)): d.polygon([(L, y - 3 + dx), (L + hh // 2 + 2, y + dx), (L, y + 3 + dx)], fill=(214, 48, 62))
        else:
            for dx, hh in ((0, h), (3, h - 3)): d.polygon([(R, y - 3 + dx), (R - hh // 2 - 2, y + dx), (R, y + 3 + dx)], fill=(214, 48, 62))

@fx('ea_ghoul')
def _fx_ghoul(d, im, e, f):
    """A small ghoul on the wall: ('ea_ghoul', x, y, look 0..1): its eyes turn towards Claude as look grows."""
    _, x, y, look = e
    d.ellipse([x - 4, y - 3, x + 4, y + 4], fill=(70, 70, 86)); d.ellipse([x - 3, y - 7, x + 1, y - 2], fill=(86, 86, 104))
    if look > 0.4:
        d.point((x - 3, y - 5), fill=RED); d.point((x - 1, y - 5), fill=RED)
        if look > 0.8: glow(im, x - 2, y - 5, 4, RED, 0.5)
    d.line([x - 4, y, x - 8, y + 4], fill=(70, 70, 86)); d.line([x + 4, y + 1, x + 7, y + 6], fill=(70, 70, 86))

@fx('ea_beast')
def _fx_beast(d, im, e, f):
    """The hulking grey beast of the lost miners: ('ea_beast', x, feet, hole 0..1, crumble 0..1)."""
    _, x, y, hole, cr, *hy = e; hy = hy[0] if hy else y - 28
    G, Gd, Gl = (92, 96, 114), (60, 64, 80), (130, 136, 156)
    if cr >= 1: return
    j = int(cr * 8)
    d.rectangle([x - 15, y - 16, x - 6, y], fill=Gd); d.rectangle([x + 6, y - 16, x + 15, y], fill=Gd)                 # legs
    d.polygon([(x - 24, y - 44 + j), (x + 24, y - 44 + j), (x + 17, y - 12), (x - 17, y - 12)], fill=G)              # the body
    d.polygon([(x - 24, y - 44 + j), (x - 10, y - 50 + j), (x + 10, y - 50 + j), (x + 24, y - 44 + j)], fill=Gl)
    d.ellipse([x - 8, y - 58 + j, x + 8, y - 44 + j], fill=Gd)                                                        # the small head
    d.rectangle([x - 5, y - 52 + j, x - 3, y - 51 + j], fill=RED); d.rectangle([x + 2, y - 52 + j, x + 4, y - 51 + j], fill=RED)
    glow(im, x, y - 52 + j, 8, RED, 0.35); d = ImageDraw.Draw(im)
    d.line([x - 24, y - 42 + j, x - 30, y - 20, x - 27, y - 4], fill=G, width=4); d.line([x + 24, y - 42 + j, x + 30, y - 20, x + 27, y - 4], fill=G, width=4)
    for cx_, cy_, h in ((-18, -44, 11), (-8, -48, 9), (18, -44, 12), (26, -40, 8), (-26, -36, 8)): crystal(d, x + cx_, y + cy_ + j, h, 3)
    if hole > 0:
        r = int(2 + 7 * hole); d.ellipse([x - r - 1, hy - r - 1, x + r + 1, hy + r + 1], fill=TEAL); d.ellipse([x - r + 1, hy - r + 1, x + r - 1, hy + r - 1], fill=(14, 8, 18))

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

def slope_y2(x): return 62 - 0.2 * x

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
    """The Apu, a giant stone head with glowing blue glyphs: ('ea_apu', dx, dy, flare 0..1 (eye), glyph 0..1)."""
    _, dx, dy, fl, gl = e
    P = lambda pts: [(x + dx, y + dy) for x, y in pts]
    head = [(60, 80), (72, 44), (90, 22), (110, 7), (132, 4), (152, 10), (162, 20), (176, 28), (185, 36), (184, 46), (170, 50), (158, 54), (148, 66), (142, 80)]
    d.polygon(P(head), fill=(50, 40, 56)); d.polygon(P([(x + 1 if x < 100 else x - 1, y) for x, y in head]), fill=STONE)
    for band in (((72, 56), (84, 32), (98, 18), (108, 24), (98, 38), (90, 58)), ((112, 64), (120, 46), (134, 34), (140, 40), (130, 52), (124, 66))):
        d.polygon(P(band), fill=mix((46, 58, 100), (60, 90, 150), gl), outline=mix((70, 70, 90), BLUE, gl))
    d.polygon(P([(110, 7), (132, 4), (152, 10), (162, 20), (150, 20), (132, 12), (112, 16), (92, 30)]), fill=(148, 124, 120))        # lit brow
    d.polygon(P([(112, 8), (104, -6), (110, -8), (124, 6)]), fill=(120, 106, 108)); d.polygon(P([(130, 4), (130, -10), (136, -10), (140, 5)]), fill=(120, 106, 108))   # horns
    d.polygon(P([(60, 80), (72, 44), (90, 22), (96, 30), (84, 52), (78, 80)]), fill=(76, 68, 78))
    d.polygon(P([(158, 54), (170, 50), (184, 46), (184, 40), (170, 42), (156, 46)]), fill=(84, 76, 84))                                 # the snout's lower plane
    d.line(P([(150, 28), (164, 32), (176, 36)]), fill=(70, 62, 70)); d.polygon(P([(176, 40), (180, 40), (180, 43), (176, 43)]), fill=(40, 34, 44))
    gc = mix(STONE, mix((60, 120, 190), BLUE, 0.5 + 0.5 * math.sin(f * 0.5)), gl)
    for row, y in enumerate((32, 42, 52)):
        for i in range(8):
            x = 78 + i * 6 + row * 4; yy = y - (i * 1.2)
            if not (x < 150 - row * 6 and yy > 10): continue
            k = (i * 3 + row * 5) % 4; xx, yy = x + dx, yy + dy
            if k == 0: d.line([(xx, yy), (xx + 2, yy - 2), (xx + 4, yy)], fill=gc)
            elif k == 1: d.rectangle([xx, yy - 2, xx + 2, yy], outline=gc)
            elif k == 2: d.line([xx, yy, xx + 4, yy], fill=gc); d.point((xx + 2, yy - 2), fill=gc)
            else: d.line([(xx, yy - 2), (xx + 3, yy - 2), (xx + 3, yy), (xx, yy)], fill=gc)
    ex, ey = 150 + dx, 22 + dy                                                            # the blue eye
    glow(im, ex, ey, int(5 + 9 * fl), BLUE, 0.35 + 0.5 * fl); d = ImageDraw.Draw(im)
    d.polygon([(ex - 8, ey + 3), (ex + 6, ey - 4), (ex + 10, ey), (ex, ey + 5)], fill=BLUE_L if fl > 0.5 else (120, 170, 235))

@fx('ea_rock')
def _fx_rock2(d, im, e, f):
    """A falling rock: ('ea_rock', x, y, size)."""
    _, x, y, s = e
    d.rectangle([x, y, x + s, y + s], fill=(96, 84, 90)); d.rectangle([x, y, x + s - 2, y + 1], fill=(150, 130, 126)); d.line([x + 1, y - s * 2, x + 1, y - 1], fill=(246, 190, 120))

@fx('ea_ride')
def _fx_ride(d, im, e, f):
    """A rider on a small dirt bike with glowing wheel rings, tilted up the slope: ('ea_ride', spr, pal, x, y, ring 0..1)."""
    _, spr, pal, x, y, ring = e
    lay = Image.new('RGBA', (52, 44), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    rc = mix((60, 60, 70), TEAL, ring); sp = (f * 0.7)
    for wx in (9, 36):
        ld.ellipse([wx - 6, 26, wx + 6, 38], fill=(40, 34, 42), outline=rc)
        ld.ellipse([wx - 5, 27, wx + 5, 37], outline=rc)
        a = sp + (0 if wx == 9 else 1); ld.line([wx, 32, wx + math.cos(a) * 4, 32 + math.sin(a) * 4], fill=(150, 130, 120))
    ld.line([9, 32, 17, 22], fill=(86, 58, 44), width=2); ld.line([17, 22, 34, 20], fill=(120, 84, 60), width=3)
    ld.line([34, 20, 36, 32], fill=(86, 58, 44), width=2); ld.line([32, 14, 38, 14], fill=(60, 50, 52), width=1); ld.line([34, 20, 35, 14], fill=(60, 50, 52))
    ld.rectangle([14, 19, 24, 21], fill=(60, 40, 40))
    if spr:
        r = sprite_img(spr, pal); lay.paste(r, (10, 19 - r.height + 11), r)
    lay = lay.rotate(12, resample=Image.NEAREST, expand=True)
    im.paste(lay, (int(x - lay.width / 2), int(y - lay.height + 10)), lay)
    if ring > 0.5:
        for k in range(3): d.point((x - 22 - k * 3, y - 1 - k % 2), fill=TEAL_L if k == 0 else TEAL)

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
    """Pietro's hands making the mountain sign (a triangle of thumbs and index fingers), the triangle glowing."""
    for y in range(H): d.line([0, y, W, y], fill=mix((120, 70, 100), (250, 160, 90), y / H))
    G, TIP = (26, 24, 34), teal(f); cx = 38
    for sgn in (-1, 1):
        px = cx + sgn * 24
        d.polygon([(px - 6, 64), (px + 6, 64), (px + sgn * 8 + 2, 46), (px + sgn * 4 - 4, 46)], fill=(136, 36, 50))                   # the maroon sleeve
        d.line([px + sgn * 2 - 1, 62, px + sgn * 4, 46], fill=(232, 190, 70)); d.line([px + sgn * 2 + 3, 62, px + sgn * 6, 46], fill=(232, 190, 70))
        d.ellipse([px - 9, 28, px + 9, 50], fill=G)                                                                                 # the palm
        d.line([px - sgn * 3, 33, cx + sgn * 1, 10], fill=G, width=5)                                                               # index finger up to the apex
        d.line([px - sgn * 3, 44, cx + sgn * 1, 44], fill=G, width=5)                                                               # thumb along the base
        d.ellipse([cx + sgn * 2 - 2, 8, cx + sgn * 2 + 2, 12], fill=TIP); d.ellipse([cx + sgn * 2 - 2, 42, cx + sgn * 2 + 2, 46], fill=TIP)
    inner = [(cx, 14), (cx + 12, 41), (cx - 12, 41)]
    g = ease((t - 0.35) / 0.4)
    d.polygon(inner, fill=mix((70, 70, 120), (150, 245, 255), g))
    if g > 0: glow(im, cx, 32, int(8 + 10 * g), TEAL, 0.55 * g)

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
    if f < 150:                                                                     # down the shaft, red crystals, ghouls turn, the beast rises
        s = scene(f, 'ea-mine'); k = f - 86
        s['under'].append(('ea_shaft', k * 4))
        for i, y in enumerate((12, 34, 54)): s['under'].append(('ea_ghoul', SR - 6, y, ease((f - 100 - i * 4) / 12)))
        if f >= 118: s['under'].append(('ea_beast', 92, 64 + 70 * (1 - ease((f - 118) / 28)), 0, 0))
        y = 34 + math.sin(k * 0.4) * 1.5
        s['actors'] = [actor(rotate90(cal('wall' if f % 4 < 2 else 'dash'), 1), SL + 12, y + 12, pal=cpal(f))]
        s['fx'].append(('ea_trail', SL + 2, y - 8, SL + 2, y - 44))
        return s
    if f < 172:                                                                     # the red void: the Supay crawls out of the water
        s = scene(f, 'ea-void'); s['under'].append(('ea_supay', 96, ease((f - 150) / 20)))
        if f >= 164: s['shake'] = rshake(1)
        return s
    if f < 208:
        return shot(closeup((f - 172) / CLOSE_LEN, f, bg=(150, 18, 28), draw=_supay_face, txt='¿TENÉS MIEDO?', color=(255, 240, 150), outline=(70, 6, 16)))
    if f < 244:
        return shot(closeup((f - 208) / CLOSE_LEN, f, bg=(40, 14, 30), draw=_cal_face, txt='NO.', text_from=0.5, color=TEAL_L, outline=(10, 30, 36)))
    s = scene(f, 'ea-cave'); k = f - 244                                            # the teal fist goes through the beast
    bx, hole, cr, pose, x = 134, 0, 0, 'guard', 36
    if k >= 12: pose, x = 'jab', 36 + min(72, (k - 12) * 10)
    if k >= 20: hole = ease((k - 20) / 8); s['shake'] = rshake(2) if k < 30 else (0, 0)
    if k >= 28: cr = min(1, (k - 28) / 10)
    s['actors'] = [actor(cal(pose), x, pal=cpal(f))]
    hx, hy = figure_point(CAL, POSES[pose], 'hand', x, GROUND)
    s['under'].append(('ea_beast', bx, GROUND, hole, cr, hy))
    if 12 <= k < 20: s['fx'].append(('ea_trail', x - 6, hy + 2, x - 40, hy + 2))
    if k >= 4: s['fx'].append(('ea_fist', hx + 1, hy + 1, max(1, 2 + min(4, (k - 4) // 2) - max(0, k - 34))))
    if k >= 20: s['fx'].append(('ea_fist', bx + 22, hy + 1, 5 - min(4, (k - 20) // 3)))                       # out through his back
    if k >= 20: s['fx'].append(('ea_shards', bx + 22, hy, k - 20))
    if k >= 28: s['fx'].append(('ea_shards', bx, GROUND - 46, k - 28))                                       # the crystals shatter
    if 20 <= k < 23: s['flash'] = 0.4; s['flashc'] = TEAL_L; s['fc'] = (bx, GROUND - 28)
    return s

ST = Stage(far_y=38, near_y=62, vp_x=92, far_scale=0.7, far_below=0.3, far_k=0.8)   # the pitch seen at an angle
ZC, ZR, ZK = 0.82, 0.6, 0.04                                                           # depth: Claude near, the big guy behind, the kids by the rope

def clip_potrero(f):
    if f < 20 or f >= 218: return lookout(f)
    s = scene(f, 'ea-pitch'); k = f - 20
    wx = lerp(-15, 78, k / 42) if f < 62 else (lerp(78, 124, (f - 62) / 12) if f < 74 else 128)
    cxs, cys = ST.proj(wx, ZC); Fy = cys
    bx_ = 0; items = []
    # the big bald guy blocks the way, lunges, then is left behind
    rp = pose_cycle(f, 'guard', 'guard2') if f < 64 else ('jab' if f < 70 else ('hurt' if f < 100 else 'kneel'))
    items.append((ZR, ST.place(figure(BIG, POSES[rp]), 112, ZR, flip=True, pal=BPAL)))
    # the kids at the rope: they jump after the goal
    for i, (spec, wk) in enumerate(zip(KIDS, (-22, -8, 6))):
        hop = int(abs(math.sin((f - 104 + i * 2) * 0.5)) * 4) if 104 <= f < 210 else 0
        items.append((ZK, ST.place(figure(spec, POSES['cheer' if 104 <= f < 210 else 'stand']), wk, ZK, h=hop, pal=KPAL)))
    # Claude
    air = 78 <= f < 126
    if not air:
        pose = ('run1' if f % 6 < 3 else 'run2') if f < 74 else ('guard' if f < 78 else 'hands_head')
        if 74 <= f < 78: pose = 'jab'
        items.append((ZC, actor(cal(pose), cxs, Fy, pal=cpal(f))))
    else:
        if f < 98: u = (f - 78) / 20; ang = 100 * min(1, (f - 78) / 12); cy = lerp(Fy - 12, Fy - 6, u * u) - 16 * math.sin(math.pi * u); cx = cxs - 2 * u
        elif f < 118: ang, cy, cx = 100, Fy - 6, cxs - 2
        else: u = (f - 118) / 8; ang = lerp(100, 0, ease(u)); cy = lerp(Fy - 6, Fy - 12, u) - 6 * math.sin(math.pi * u); cx = cxs - 2 * (1 - u)
        s['fx'].append(('ea_rot', figure(CAL, POSES['run1']), cpal(f), cx, cy, ang))
        if f < 92: s['fx'].append(('ea_trail', cx - 6, cy + 4, cx - 30, cy + 8))
    s['actors'] = ST.back_to_front(items)
    if 66 <= f < 72: s['fx'].append(('ring', cxs + 4, Fy - 1, 2 + (f - 66) * 2, TEAL))                     # a sneaker flashes teal
    # the ball
    ch = False
    if f < 72: bx, by = cxs + 9, Fy - 2 - abs(math.sin(f * 0.8)) * 3
    elif f < 84: u = (f - 72) / 12; bx, by = lerp(cxs + 9, 136, u), lerp(Fy - 2, 24, u) - 10 * math.sin(math.pi * u) * 0
    elif f < 88: bx, by = 136, 24 - (f - 84) * 0.5
    elif f < 100: u = (f - 88) / 12; bx, by = lerp(137, 166, u), lerp(24, 41, u); ch = True
    else: bx, by = 166, min(47, 41 + (f - 100) * 0.8)
    if f >= 84 and f < 100: ch = True
    if f < 210: s['fx'].append(('ea_ball', bx, by, ch))
    if 88 <= f < 92: s['fx'].append(('spark', 136, 24, 4 - (f - 88)))
    if 100 <= f < 112: s['fx'].append(('ea_net', f - 100))
    if 100 <= f < 108: s['shake'] = rshake(1)
    if cue(f, 102, GOLAZO): s['fx'].append(('caption', GOLAZO, dict(box=(2, 1, W - 2, 25), color=(255, 232, 90), outline=(70, 30, 20), shadow=None, max_scale=3)))
    return s

GOLAZO = '¡GOLAZO!'

@fx('ea_tri')
def _fx_tri(d, im, e, f):
    """The mountain sign glowing: ('ea_tri', x, y, size, strength 0..1)."""
    _, x, y, r, a = e
    glow(im, x, y, int(r * 2), TEAL, 0.6 * a); d = ImageDraw.Draw(im)
    d.polygon([(x, y - r), (x + r, y + r * 0.8), (x - r, y + r * 0.8)], outline=mix(TEAL, TEAL_L, a))

ROCKS = ((70, 100, 6), (92, 106, 7), (122, 112, 6), (82, 118, 5), (106, 124, 7), (60, 130, 6))
APU_TXT, SIGN_TXT = 'APU...', 'PERMISO, APU.'

def clip_apu(f):
    if f < 20 or f >= 278: return lookout(f)
    if 140 <= f < 182:
        return shot(closeup((f - 140) / 42, f, bg=(120, 70, 100), draw=_hands, txt=APU_TXT, color=BLUE_L, outline=(20, 30, 70)))
    s = scene(f, 'ea-slope'); k = f - 20
    cr = ease((f - 60) / 20) if f < 182 else 0
    dy = 0 if f < 70 else (70 * (1 - ease((f - 70) / 30)))
    fl = 1.0 if f < 182 else 1 - 0.85 * ease((f - 186) / 20)
    bow = ease((f - 206) / 28) if f >= 206 else 0
    if f >= 70: s['under'].append(('ea_apu', -26 - 8 * bow, dy + 64 * bow, fl, 1.0 if f < 232 else 0.3))
    s['under'].append(('ea_ground', f if f < 140 or f >= 226 else 140, cr if f < 232 else 0))
    if 62 <= f < 104: s['shake'] = rshake(1)
    if f < 140:                                                                      # riding up the slope; Claude swerves, Pietro stalls
        sw = 7 * math.sin(math.pi * (f - 104) / 30) if 104 <= f < 134 else 0
        cx_ = 112 - (max(0, f - 126) * 1.6 if f > 126 else 0)
        px = 64 - ((f - 118) * 1.4 if f > 118 else 0); px = max(px, 44)
        ring_p = 1 - ease((f - 118) / 10)
        s['fx'].append(('ea_ride', figure(PIETRO, POSES['crouch']), ppal(f), px, slope_y2(px) + 8, ring_p))
        s['fx'].append(('ea_ride', cal('crouch'), cpal(f), cx_, slope_y2(cx_) + 4 + sw, 1.0 if f < 128 else 0.3))
        for x, t0, sz in ROCKS:
            y = (f - t0) * 4 - 8; g = slope_y2(x) + 2
            if 0 <= f - t0: s['fx'].append(('ea_rock', x, min(y, g), sz))
    elif f < 226:                                                                    # the sign: both make it, the Apu calms and bows
        t = min(1, (f - 182) / 14)
        s['actors'] = [actor(figure(PIETRO, POSES['sign']), 36, slope_y2(36) + 8, pal=ppal(f)), actor(cal('sign'), 62, slope_y2(62) + 8, pal=cpal(f))]
        for sp, pl, x in ((figure(PIETRO, POSES['sign']), ppal(f), 36), (CAL, None, 62)):
            hx, hy = figure_point(PIETRO if x == 36 else CAL, POSES['sign'], 'hand', x, slope_y2(x) + 8)
            s['fx'].append(('ea_tri', hx, hy, 3, ease(t)))
        if cue(f, 190, SIGN_TXT): s['fx'].append(('caption', SIGN_TXT, dict(box=(2, 1, W - 2, 25), color=BLUE_L, outline=(40, 24, 70), shadow=None, max_scale=2)))
        if 206 <= f < 226: s['fx'] += [('dust', 120 + (i * 17 + f * 3) % 60, slope_y2(150) + 4 - (f + i) % 6) for i in range(6)]
    else:                                                                            # they ride off, the way open
        u = f - 226
        for spr, pl, x0, d_ in ((figure(PIETRO, POSES['crouch']), ppal(f), 36, 4), (cal('crouch'), cpal(f), 62, 8)):
            x = x0 + u * 3.4 + 0.02 * u * u; s['fx'].append(('ea_ride', spr, pl, x, slope_y2(x) + 8, 1.0))
    return s

CLIPS = [clip('salamanca', 300, clip_salamanca), clip('potrero', 240, clip_potrero), clip('apu', 300, clip_apu)]
