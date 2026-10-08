"""Red Dead Redemption 2: Arthur Morgan's last sunrise on the mountain. Claude is Arthur (a hat, a worn coat, an
orange bandana, a satchel). Micah Bell (a white hat, a moustache, a revolver) comes up the ridge; they fight,
Arthur lands a few punches and coughs, and Micah runs. Arthur sinks down on the ridge and the sun comes up over
the peaks, the sky going from blue to gold. Close-up: his face lit orange, eyes half shut: THAT'S THE WAY IT IS.
Then the sun goes back down, Arthur gets up, his horse nudges him, and the clip is back on the neutral pose:
Arthur on the ridge with his horse under the pre-dawn stars."""
import math, random
from engine import *

THEME = 'rdr2'
register_bg(THEME, lambda v: (v+30,v+24,v+44))                       # the dotted ridge line
N_ = 360                                                            # a multiple of 12: the guard bounce loops
CLOSE = "THAT'S THE WAY IT IS."
CLOSE_AT, CLOSE_LEN = 252, 44                                       # the close-up (ends before the sun goes down)
CX, HX, MX, RX_IN = 50, 22, 68, W + 14                              # Arthur, his horse, where Micah stops, where he enters
INK = (16,14,22)
PALE, PALE_SHADE, HORSE_LINE = (232,226,214), (170,160,150), (36,30,40)

# ---- people, built from a pose (engine/people.py: figure(), POSES) ----------------------------------------
GW, GH, C = 24, 24, 11                                              # the grid and its centre column (they face right)
POSES = dict(POSES)
POSES['cough'] = ((1, 4), (4, -2), (5, 1), (2, -3), 0, 'stance')    # a hand up to the mouth
_BODY = dict(w=GW, h=GH, c=C, legs=9, torso=7)

def _satchel(g, at):                                                # a satchel on his back (the left side)
    for y in (at['ty'] + 2, at['ty'] + 3, at['ty'] + 4): put(g, at['c'] - 4 + at['sh'](y), y, 'b')

def _moustache(g, at):                                              # a thick moustache under the eyes
    y, o = at['hy'] + 3, at['sh'](at['hy'])
    for x in (at['c'] - 1, at['c'], at['c'] + 1): put(g, x + o, y, 'm')

CLAUDE = dict(_BODY, name='rdr2-arthur', hair=['.hhhhh.', 'hhhhhhh'], hair_y=2, shut='K',
              body=dict(color='j', collar='o', hip='b'), leg=dict(color='p', boot='k'),
              paint=dict(body=[_satchel]))
RIVAL = dict(_BODY, name='rdr2-micah', hair=['.hhhhh.', 'hhhhhhh'], hair_y=2, shut='K',
             body=dict(color='j', hip='p'), leg=dict(color='p', boot='k'), paint=dict(face=[_moustache]))
CPAL = {'s':(226,176,136), 'K':INK, 'h':(92,58,34), 'j':(120,84,56), 'p':(62,50,44), 'k':INK, 'o':(217,119,87),
        'b':(72,44,26)}
RPAL = {'s':(206,164,130), 'K':INK, 'h':(236,232,222), 'j':(52,48,66), 'p':(44,40,60), 'k':INK, 'm':(64,44,34)}

def build(who, pose):
    """Arthur or Micah in a pose (POSES): engine/people.py's figure()."""
    return figure(CLAUDE if who == 'claude' else RIVAL, POSES[pose])

def put_on(spr, wx, flip=False, pal=None):
    """An actor standing at world x."""
    return actor(spr, int(wx), flip=flip, pal=pal)

def ready(f):                                                       # the neutral pose: it moves every 12 frames, which divides N_
    return pose_cycle(f, 'guard', 'guard2')

# ---- the sky, the peaks and the sun: one picture per frame, so the sunrise can be drawn ------------------
NIGHT_TOP, NIGHT_BOT = (10,12,34), (46,42,88)                      # pre-dawn
DAY_TOP, DAY_MID, DAY_BOT = (62,88,150), (214,122,92), (255,184,98)  # the sunrise: blue to orange gold
_rr = random.Random(9)
STARS = [(_rr.randint(0, W - 1), _rr.randint(0, 26), _rr.random()) for _ in range(22)]
PINES = (5, 13, 25, 98, 108, 150, 160, 176)

def _mix(a, b, t): return tuple(int(lerp(x, y, t)) for x, y in zip(a, b))

def far_y(x): return 30 + 7 * math.sin(x * 0.05 + 0.6) + 4 * math.sin(x * 0.14 + 2.2)
def mid_y(x): return 44 + 3 * math.sin(x * 0.08 + 1.4) + 1.5 * math.sin(x * 0.21)
def ridge_y(x): return 57 + 1.2 * math.sin(x * 0.04)

def _ridge_poly(fn):
    return [(x, fn(x)) for x in range(0, W + 3, 3)] + [(W + 3, H), (0, H)]

def k_of(f):
    """How far the sun has come up: 0 before dawn, 1 at full sunrise (the close-up), back to 0 by the end."""
    if f < 186: return 0.0
    if f < 250: return ease((f - 186) / 64)
    if f < 300: return 1.0
    if f < 350: return 1 - ease((f - 300) / 50)
    return 0.0

def _paint_dawn(d, k, f):
    for y in range(H):
        t = min(1.0, y / 50)
        day = _mix(DAY_TOP, DAY_MID, t * 2) if t < 0.5 else _mix(DAY_MID, DAY_BOT, (t - 0.5) * 2)
        d.line([0, y, W, y], fill=_mix(_mix(NIGHT_TOP, NIGHT_BOT, t), day, k))
    for x, y, off in STARS:                                         # they twinkle, and go as the sky warms
        b = (0.55 + 0.45 * math.sin(2 * math.pi * ((loop.phase(f, 36) + off) % 1))) * (1 - k)
        if b > 0.1: d.point((x, y), fill=tuple(int(v * b) for v in (220, 226, 255)))
    if k > 0.02:                                                    # the sun, behind the far peaks until it clears them
        sx, sy = 124, lerp(74, 20, ease(k))
        d.ellipse([sx - 13, sy - 13, sx + 13, sy + 13], fill=_mix((200,110,90), (250,170,90), k))
        d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(255,214,120))
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255,242,196))
    d.polygon(_ridge_poly(far_y), fill=_mix((26,24,54), (120,84,112), k))
    d.polygon(_ridge_poly(mid_y), fill=_mix((18,16,36), (70,46,74), k))
    for px in PINES:
        by = mid_y(px) + 1
        d.polygon([(px, by - 9), (px - 2, by), (px + 2, by)], fill=_mix((10,10,22), (40,28,44), k))
    d.polygon(_ridge_poly(ridge_y), fill=_mix((12,10,22), (44,30,40), k))

@fx('rd_dawn')
def _fx_dawn(d, im, e, f):
    """The whole sky, hills and sun for this frame: ('rd_dawn', {'k': 0..1})."""
    _paint_dawn(d, e[1]['k'], f)

@fx('rd_horse')
def _fx_horse(d, im, e, f):
    """Arthur's pale horse, feet on the ridge, body at x: ('rd_horse', {'x': x})."""
    x, fy = int(e[1]['x']), GROUND
    d.rectangle([x - 9, fy - 7, x - 8, fy - 1], fill=PALE_SHADE); d.rectangle([x - 6, fy - 7, x - 5, fy - 1], fill=PALE_SHADE)
    d.rectangle([x + 5, fy - 7, x + 6, fy - 1], fill=PALE); d.rectangle([x + 8, fy - 7, x + 9, fy - 1], fill=PALE)
    d.polygon([(x - 11, fy - 12), (x - 16, fy - 8), (x - 14, fy - 3), (x - 10, fy - 7)], fill=PALE_SHADE)   # tail
    d.ellipse([x - 11, fy - 14, x + 8, fy - 5], fill=PALE, outline=HORSE_LINE)
    d.polygon([(x + 3, fy - 12), (x + 9, fy - 14), (x + 15, fy - 24), (x + 11, fy - 27), (x + 6, fy - 20)],
              fill=PALE, outline=HORSE_LINE)                                                          # neck
    d.polygon([(x + 10, fy - 28), (x + 14, fy - 30), (x + 21, fy - 24), (x + 21, fy - 21), (x + 15, fy - 22),
               (x + 11, fy - 20)], fill=PALE, outline=HORSE_LINE)                                     # head
    d.line([x + 6, fy - 25, x + 11, fy - 19], fill=HORSE_LINE)                                         # mane
    d.point((x + 16, fy - 25), fill=HORSE_LINE)                                                        # eye

@fx('rd_spark')
def _fx_spark(d, im, e, f):
    """A spark: (name, x, y, k), k the frames since it started."""
    _, x, y, k = e; spark(d, int(x), int(y), 3 + int(k) // 2)

@fx('rd_cough')
def _fx_cough(d, im, e, f):
    """Red specks from the mouth: (name, x, y, k), k the frames since the cough."""
    _, x, y, k = e
    for i in range(3):
        px, py = x - 2 * i - int(k * 0.5), y + i + int(k * 0.4)
        d.point((px, py), fill=(190, 24, 34)); d.point((px - 1, py), fill=(140, 16, 26))

# ---- the close-up ---------------------------------------------------------------------------------------
def _face(im, d, t, f):                                             # his face, lit by the sun, eyes half shut
    _paint_dawn(d, 1.0, f)
    ox = int(lerp(0, -4, ease(t)))                                  # a slow push in
    d.rectangle([14 + ox, 46, 60 + ox, 64], fill=(217,119,87))      # the bandana
    d.rectangle([20 + ox, 26, 56 + ox, 48], fill=(236,150,100), outline=INK)   # the face, lit orange
    d.rectangle([14 + ox, 18, 62 + ox, 22], fill=(92,58,34), outline=INK)     # the brim
    d.rectangle([24 + ox, 8, 52 + ox, 19], fill=(92,58,34), outline=INK)      # the crown
    d.rectangle([25 + ox, 31, 31 + ox, 32], fill=INK); d.rectangle([41 + ox, 31, 47 + ox, 32], fill=INK)   # eyes, half shut
    d.rectangle([28 + ox, 40, 44 + ox, 42], fill=(120,72,46))       # moustache
    d.rectangle([28 + ox, 43, 44 + ox, 47], fill=(132,84,56))       # stubble

# ---- the clip: starts and ends on the neutral pose, so frame N_ is frame 0 --------------------------------
def nudge(f):                                                       # the horse steps in to nudge him, then back
    return 3 * math.sin(math.pi * (f - 330) / 18) if 330 <= f < 348 else 0.0

def clip_main(f):
    s = scene(f, THEME)
    k = k_of(f)
    me, rival, rx = ready(f), None, MX
    if 16 <= f < 52: rival, rx = pose_cycle(f, 'walk1', 'walk2'), lerp(RX_IN, MX, ease((f - 16) / 36))   # Micah walks in
    if 52 <= f < 118: rival = ready(f)                              # the standoff
    if 64 <= f < 70: me = 'jab'                                     # Arthur lands a punch
    if 68 <= f < 80: rival, rx = 'hurt', MX + 4
    if 78 <= f < 86: rival = 'hook'                                 # Micah hits back
    if 84 <= f < 94: me = 'hurt'
    if 94 <= f < 108: me = 'cough'                                  # the tuberculosis
    if 108 <= f < 114: me = 'jab'                                   # he still lands one
    if 112 <= f < 118: rival, rx = 'hurt', MX + 4
    if 118 <= f < 152: rival, rx = pose_cycle(f, 'run1', 'run2', 3), lerp(MX, W + 30, (f - 118) / 34)   # Micah runs
    if 124 <= f < 146: me = 'crouch'                                # Arthur sinks down
    if 146 <= f < 304: me = 'kneel'                                 # ...and sits on the ridge
    if 304 <= f < 314: me = 'crouch'                                # gets up
    if 68 <= f < 76: s['fx'].append(('rd_spark', 60, 40, f - 68))
    if 84 <= f < 92: s['fx'].append(('rd_spark', 58, 36, f - 84))
    if 112 <= f < 118: s['fx'].append(('rd_spark', 60, 40, f - 112))
    if 94 <= f < 106: s['fx'].append(('rd_cough', 51, 39, f - 94))
    if CLOSE_AT <= f < CLOSE_AT + CLOSE_LEN:
        s['image'] = closeup((f - CLOSE_AT) / CLOSE_LEN, f, bg=(236,150,100), draw=_face, txt=CLOSE); return s
    s['under'].append(('rd_dawn', {'k': k}))
    s['under'].append(('rd_horse', {'x': HX + nudge(f)}))
    s['actors'] = [put_on(build('claude', me), CX, pal=CPAL)]
    if rival: s['actors'].append(put_on(build('rival', rival), rx, flip=f < 118, pal=RPAL))
    return s

CLIPS = [clip('sunrise', N_, clip_main)]
