"""Papers, Please: Claude as the border inspector of Grestin checkpoint (Arstotzka, 1982): a grey fur ushanka with
a red-yellow badge, a grey-brown greatcoat and a Claude-orange scarf, seen from behind at the booth desk. The layout
follows the game: the outside seen from above on top (grey concrete, the queue as black silhouettes, navy guards,
the black gate booth), the entrant face-on in the booth window (left, dark striped back, olive counter), the dark
desk on the right (the rule book, the stamp bar with the red DENIED and the green APPROVED stamp, the papers).
Clips: `denied` (an expired passport, the red stamp), `jorji` (Jorji Costava's crayon passport, a bribe, a green
stamp), `permission` (shell commands asking for permission: rm -rf / is denied, git status approved).
Everything is drawn here as full frames; the neutral pose breathes, the lamp flickers, snow falls."""
from engine import *
from PIL import ImageChops
import math, random

THEME = 'papersplease'
# the game's muted palette: greys, olive, brown-green; the only strong colours are the stamps and Claude's scarf
CONC, CONC2 = (126,126,128), (100,100,102)
DESK, OLIVE, OLIVE2 = (24,24,26), (104,116,78), (136,148,100)
SK, SKS = (170,150,118), (128,110,88)
ORANGE, ORD = (217,119,87), (168,80,54)
COAT, COATD, FUR, FURD = (92,84,76), (70,62,56), (146,148,150), (112,114,118)
RED, GREEN, YEL = (190,40,36), (70,140,50), (240,200,60)
PAPER, PAPD, INKC = (214,214,160), (130,124,84), (40,36,30)
WHITE, BLK = (226,222,208), (18,16,16)
CREAM = (255,240,170)
CLOSEBG = (30,30,32)
HOME, GATE = (110,58), 64                                           # Claude's resting hand; the gate's x outside
NEXT, GLORY, NOPROB, SEEYA = "NEXT!", "GLORY TO ARSTOTZKA.", "IS NO PROBLEM!", "SEE YOU, INSPECTOR!"
FOREIGN = (150,170,150)                                             # a foreign passport's cover

def R(d, x0, y0, x1, y1, c, ox=0, oy=0, s=1):
    d.rectangle([ox + x0 * s, oy + y0 * s, ox + x1 * s - 1, oy + y1 * s - 1], fill=c)

def kf(f, pts):
    """Piecewise-linear value through (frame, value) keyframes; a value is a number or a tuple."""
    if f <= pts[0][0]: return pts[0][1]
    for (a, va), (b, vb) in zip(pts, pts[1:]):
        if f <= b:
            t = (f - a) / max(1, b - a)
            return tuple(lerp(x, y, t) for x, y in zip(va, vb)) if isinstance(va, tuple) else lerp(va, vb, t)
    return pts[-1][1]

# ---- faces -----------------------------------------------------------------------------------------------
def _eyes(r, y, xs, look=0, blink=False, wink=False, h=2):
    for i, x in enumerate(xs):
        if blink or (wink and i == 1): r(x, y + h - 1, x + 2, y + h, BLK); continue
        r(x, y, x + 2, y + h, WHITE); p = 1 if look > 0 else 0; r(x + p, y, x + p + 1, y + h, BLK)

def bust(d, kind, ox, oy, s=1, f=0, look=0, sweat=False, wink=False, blink=False, wave=0):
    """An entrant, face-on: head box 14x14 units from (ox, oy), shoulders under it. kind: mous, jorji, hood, neat."""
    r = lambda *a: R(d, *a, ox=ox, oy=oy, s=s)
    wv = f // 3 % 2
    if kind == 'mous':
        r(-5,13,19,24,(100,70,46)); r(3,13,10,17,(184,178,160)); r(6,15,7,24,(76,54,36))
        r(4,11,9,13,SKS); r(1,1,12,13,SK); r(0,6,1,9,SK); r(12,6,13,9,SK)
        r(0,0,13,3,(72,58,42)); r(-1,2,14,3,(72,58,42)); r(1,3,12,4,(46,36,28))
        _eyes(r, 6, (3,8), look, blink); r(3,5,5,6,BLK); r(8,5,10,6,BLK); r(5,4,6,5,BLK); r(7,4,8,5,BLK)
        r(6,7,7,10,SKS); r(2,10,11,12,BLK); r(1,11,2,13,BLK); r(11,11,12,13,BLK); r(5,12,8,13,(110,56,48))
        if sweat:
            for k in range(2):
                y = 3 + (f // 2 + k * 5) % 9; x = -1 if k == 0 else 13; r(x,y,x+1,y+2,(160,210,240))
    elif kind == 'jorji':
        if wave: r(-9,4+wv,-6,14,(150,40,40)); r(-9,1+wv,-6,4+wv,SK)
        r(-6,13,20,24,(150,40,40)); r(3,13,10,15,(60,20,20))
        r(0,1,13,13,SK); r(-1,0,14,4,(124,86,52))
        for x in range(-1,14,2): r(x,0,x+1,4,(100,68,40))
        B = (38,28,24); r(0,8,13,14,B); r(1,13,12,15,B); r(0,5,1,8,B); r(12,5,13,8,B)
        r(1,7,3,9,(190,120,100)); r(10,7,12,9,(190,120,100))
        _eyes(r, 5, (3,8), look, blink, wink); r(3,4,5,5,B); r(8,4,10,5,B)
        r(5,7,8,9,(190,120,100)); r(3,9,10,12,(30,20,20)); r(4,9,9,11,WHITE); r(6,9,7,11,(190,186,176))
    elif kind == 'hood':
        r(-5,13,19,24,(34,34,42)); r(-2,13,15,15,(46,46,56))
        r(-2,0,15,14,(34,34,44)); r(-1,-1,14,0,(34,34,44)); r(0,0,13,1,(52,52,64))
        r(2,3,11,13,(8,8,12))
        if not blink: r(3,6,5,8,(236,236,246)); r(8,6,10,8,(236,236,246))
    elif kind == 'neat':
        if wave: r(-9,4+wv,-6,14,(86,90,98)); r(-9,1+wv,-6,4+wv,SK)
        r(-5,13,19,24,(86,90,98)); r(4,13,9,17,WHITE); r(6,14,7,22,(150,52,52))
        r(4,11,9,13,SKS); r(1,1,12,13,SK); H = (62,50,40)
        r(1,0,12,3,H); r(0,2,1,6,H); r(12,2,13,6,H)
        _eyes(r, 6, (3,8), look, blink, wink); G = (30,30,36)
        for x0 in (2,7): r(x0,5,x0+4,6,G); r(x0,8,x0+4,9,G); r(x0,5,x0+1,9,G); r(x0+3,5,x0+4,9,G)
        r(6,6,8,7,G); r(6,8,7,10,SKS); r(4,11,9,12,(150,80,70)); r(3,10,4,11,(150,80,70)); r(9,10,10,11,(150,80,70))

def claude_face(d, ox, oy, s, f, mode='stare'):
    """Claude's face for the close-ups: the ushanka with its badge, the orange scarf, a stern face."""
    r = lambda *a: R(d, *a, ox=ox, oy=oy, s=s)
    r(-6,17,20,24,COAT); r(-3,12,17,18,ORANGE); r(-3,15,17,16,ORD)
    r(1,1,12,13,(206,176,148)); r(0,5,1,8,(206,176,148)); r(12,5,13,8,(206,176,148))
    r(-2,-3,16,5,FUR); r(-3,0,17,3,FUR); r(-3,3,0,12,FURD); r(14,3,17,12,FURD)
    for y in range(-3,5):
        for x in range(-2,16):
            if (x * 7 + y * 3) % 5 == 0: r(x,y,x+1,y+1,FURD)
    r(6,-1,9,3,RED); r(7,0,8,2,YEL)
    _eyes(r, 7, (3,8), 0, mode == 'stare' and 10 <= f % 30 < 12)
    r(2,5,6,6,BLK); r(5,6,6,7,BLK)
    if mode == 'brow': r(8,3,12,4,BLK); r(7,4,8,5,BLK)
    else: r(7,5,11,6,BLK); r(7,6,8,7,BLK)
    r(4,11,10,12,(120,70,60))

# ---- the room ---------------------------------------------------------------------------------------------
_STATIC = []
def _counter(d):
    d.rectangle([0,46,60,H], fill=OLIVE); d.line([0,46,60,46], fill=OLIVE2); d.line([0,47,60,47], fill=(70,80,52))
    d.rectangle([6,58,54,59], fill=(30,32,22)); d.rectangle([0,60,60,H], fill=(80,70,50))

def _static():
    """What never moves: the window with its counter, the dark desk, the stamp bar, the rule book."""
    if _STATIC: return _STATIC[0]
    im = Image.new('RGB', (W, H), DESK); d = ImageDraw.Draw(im); rr = random.Random(3)
    for _ in range(260): d.point((rr.randrange(64, W), rr.randrange(21, H)), fill=(32,32,34))
    d.rectangle([0,21,60,46], fill=(30,24,20))                                    # the window: a dark striped back
    for y in range(22, 46, 4): d.line([0,y,60,y], fill=(44,36,28))
    _counter(d); d.rectangle([60,21,64,H], fill=(10,10,12))
    d.rectangle([114,22,W,38], fill=(54,56,54)); d.rectangle([114,38,W,40], fill=(36,38,36))      # the stamp bar
    for x0, c, c2 in ((122, RED, (120,22,22)), (152, GREEN, (46,96,30))):
        d.rectangle([x0,28,x0+18,38], fill=c); d.rectangle([x0,36,x0+18,38], fill=c2)
        d.rectangle([x0+5,21,x0+13,29], fill=(44,44,44)); d.rectangle([x0+6,22,x0+9,25], fill=(70,70,70))
    d.rectangle([112,42,150,63], fill=(40,44,28)); d.rectangle([113,43,149,62], fill=(200,210,152))   # the rule book
    for y in range(46, 62, 3): d.line([115,y,116,y], fill=(30,30,30))
    for x0 in (126, 140): d.ellipse([x0-4,47,x0+4,55], fill=(214,70,56)); d.rectangle([x0-1,49,x0+1,53], fill=(236,200,190))
    d.rectangle([121,58,144,61], outline=(120,124,90))
    _STATIC.append(im); return im

def _walker(d, x, kind, f, y=20, wave=False, down=False):
    coat = {'mous':(76,54,36),'jorji':(110,30,30),'hood':(30,30,38),'neat':(70,74,82)}[kind]
    hat = {'mous':(40,32,24),'jorji':(100,68,40),'hood':(30,30,38),'neat':(50,40,32)}[kind]
    st = (f // 3) % 2; hd = 1 if down else 0; x = int(x)
    d.rectangle([x-2,y-3,x-1,y-(1 if st else 0)], fill=(20,20,22)); d.rectangle([x+1,y-3,x+2,y-(0 if st else 1)], fill=(20,20,22))
    d.rectangle([x-2,y-8+hd,x+2,y-3], fill=coat)
    d.rectangle([x-1,y-10+hd,x+1,y-8+hd], fill=(30,30,34) if kind == 'hood' else SK)
    d.rectangle([x-2,y-11+hd,x+2,y-10+hd], fill=hat)
    if kind == 'jorji': d.rectangle([x-1,y-9+hd,x+1,y-8+hd], fill=(30,22,20))
    if wave: d.line([x+3,y-7,x+4+(f//3%2),y-12], fill=coat)

def _outside(im, d, f, walker, loud, gate):
    d.rectangle([0,0,W,21], fill=CONC); d.rectangle([0,0,W,3], fill=CONC2)
    for x in range(0, W, 41): d.line([x,4,x,21], fill=(112,112,114))
    for x in range(116, 132, 4): d.line([x,20,x+6,6], fill=(60,60,62), width=2)
    for x in range(80, W, 6): d.point((x,19), fill=(160,160,162))
    for row in range(3):
        for i in range(12):
            x = 3 + i * 4 + (row * 2) % 4; y = 8 + row * 5 - (1 if (loop.frame(f) // 6 + i) % 3 == 0 else 0)
            d.rectangle([x,y-1,x+2,y+4], fill=(14,14,18))
    d.rectangle([54,10,74,21], fill=(18,18,20)); d.rectangle([58,12,70,14], fill=(70,74,66))
    d.rectangle([58,6,66,10], fill=(150,150,154)); d.rectangle([60,7,64,9], fill=(60,60,62))   # the loudspeaker
    if gate: d.line([74,14,97,4], fill=(210,210,210), width=2)
    else:
        d.line([74,14,110,14], fill=(210,210,210), width=2)
        for x in range(78, 110, 6): d.point((x,14), fill=(80,30,30))
    for x in (134, 152, 172):
        d.rectangle([x,9,x+2,17], fill=(38,44,84)); d.rectangle([x,7,x+2,9], fill=(60,66,100)); d.line([x+3,6,x+3,18], fill=(20,20,24))
    if loud and loop.frame(f) % 4 < 3:
        for rad in (4, 8, 12): d.arc([66-rad,8-rad,66+rad,8+rad], -50, 50, fill=CREAM)
    if walker: _walker(d, walker[0], walker[1], f, wave=walker[2], down=walker[3])
    draw_fx(d, im, ('snow', {'top': 0, 'bottom': 21, 'n': 26}), f)

def room(f, wk=None, wkind=None, by=None, bk=None, items=(), doc=False, hand=HOME, look=0, loud=False,
         gate=False, dis=0.0, hl=None, wwave=False, hdown=False):
    """One frame of the booth. wk: the walker's x outside (a wkind); by: the head top of the bust in the window."""
    im = _static().copy(); d = ImageDraw.Draw(im)
    _outside(im, d, f, (wk, wkind, wwave, hdown) if wk is not None else None, loud, gate)
    bk = bk or {}
    if by is not None:                                                            # the entrant in the window
        lay = Image.new('RGBA', (W, H), (0,0,0,0)); bust(ImageDraw.Draw(lay), wkind, 31, int(by), 1, f, **bk)
        px = lay.load(); out = []
        for y in range(22, 46):
            for x in range(2, 59):
                p = px[x, y]
                if p[3] == 0: continue
                rg = random.Random(x * 131 + y * 7); th = rg.random() * 0.8
                if dis <= th: im.putpixel((x, y), p[:3])
                else:                                                             # a pixel breaking loose and floating off
                    q = (dis - th) / (1 - th)
                    if q < 0.8: out.append((x + int((rg.random() - 0.3) * 26 * q), y - int(rg.random() * 16 * q), tuple(int(lerp(a, b, q)) for a, b in zip(p[:3], (190,190,215)))))
        for x, y, c in out:
            if 1 <= x < 60 and 21 <= y < 46: im.putpixel((x, y), c)
        d = ImageDraw.Draw(im); _counter(d)
    for it in items:                                                              # on the counter
        x = int(it[1])
        if it[0] == 'pass':
            d.rectangle([x,49,x+10,55], fill=it[2], outline=(24,22,18)); d.rectangle([x+4,51,x+6,53], fill=YEL)
            if len(it) > 3: d.rectangle([x+1,50,x+4,52], fill=RED)
        else: d.rectangle([x,50,x+9,55], fill=(176,176,180), outline=(24,22,18)); d.rectangle([x+2,52,x+7,53], fill=RED)
    if doc:                                                                       # the open papers on the desk
        d.rectangle([152,42,184,63], fill=PAPER, outline=(120,60,50)); d.rectangle([154,52,163,61], fill=(120,126,120))
        for y in range(46, 62, 3): d.line([166,y,181,y], fill=PAPD)
    for name, box in (('doc', (151,41,185,64)), ('book', (111,41,151,64))):
        if hl == name: d.rectangle(box, outline=(240,230,120))
    bob = 1 if (loop.frame(f) // 6) % 2 else 0; lk = int(look)                    # Claude, from behind
    d.rectangle([78,52,106,H], fill=COAT); d.rectangle([76,56,108,H], fill=COAT); d.line([92,58,92,H], fill=COATD)
    d.line([78,52,106,52], fill=(116,108,98)); d.rectangle([98,50,102,58], fill=ORD)
    d.rectangle([83+lk,46+bob,101+lk,52], fill=ORANGE); d.line([83+lk,50,101+lk,50], fill=ORD)
    d.rectangle([84+lk,34+bob,100+lk,47+bob], fill=FUR); d.rectangle([82+lk,37+bob,102+lk,45+bob], fill=FUR)
    d.rectangle([81+lk,42+bob,84+lk,49+bob], fill=FURD); d.rectangle([100+lk,42+bob,103+lk,49+bob], fill=FURD)
    for y in range(34, 47):
        for x in range(82, 103):
            if (x * 7 + y * 3) % 5 == 0: d.point((x + lk, y + bob), fill=FURD)
    d.rectangle([101+lk,38+bob,103+lk,41+bob], fill=RED); d.point((102+lk,39+bob), fill=YEL)
    hx, hy = int(hand[0]), int(hand[1])
    d.line([106,56,hx,hy], fill=COAT, width=5); d.line([106,56,hx,hy], fill=COATD, width=1)
    d.rectangle([hx-1,hy-2,hx+2,hy+1], fill=SK)
    d.rectangle([50,22,56,25], fill=(210,150,60))                                  # the desk lamp flickers
    if random.Random(loop.frame(f) // 4 * 7919 + 5).random() < 0.14:
        im.paste(Image.blend(im.crop((0,21,W,H)), Image.new('RGB', (W, H - 21), (0,0,0)), 0.2), (0,21)); d.rectangle([50,22,56,25], fill=(110,80,40))
    return im

def cap(im, txt, col=CREAM, box=(2,2,W-2,19), max_scale=2):
    text_block(im, txt, box, col, max_scale, shadow=None, outline=(0,0,0))

# ---- papers, close-up -------------------------------------------------------------------------------------
def page(im, d, x0, y0, x1, y1, head, hcol, rows=(), photo=None, paper=PAPER, bars=()):
    d.rectangle([x0,y0,x1,y1], fill=paper, outline=(110,100,64))
    d.rectangle([x0+1,y0+1,x1-1,y0+8], fill=hcol); text(d, head, x0 + 4, y0 + 3, (236,232,210), shadow=None)
    if photo:
        ph = Image.new('RGB', (28,42), (118,126,118)); bust(ImageDraw.Draw(ph), photo, 0, 0, 2, 0); im.paste(ph, (x0 + 4, y0 + 12))
    xl = x0 + 36
    for dy, lbl, val, sc in rows:
        text(d, lbl, xl, y0 + dy, PAPD, shadow=None)
        if sc == 1: text(d, val, xl + (len(lbl) + 1) * 4, y0 + dy, INKC, shadow=None)
        else: big_text(im, val, y0 + dy + 7, INKC, scale=sc, cx=xl + len(val) * 2 * sc, shadow=None)
    for y in bars: d.rectangle([x0+8,y,x1-8,y+1], fill=PAPD)

def shift(im, dx, dy):
    out = Image.new('RGB', im.size, CLOSEBG); out.paste(im, (dx, dy)); return out

def _redtint(im):
    t = ImageChops.multiply(im, Image.new('RGB', (W, H), (255,150,140)))
    return Image.blend(Image.blend(im, t, 0.85), Image.new('RGB', (W, H), (60,0,0)), 0.25)

def _bg(d): d.rectangle([0,0,W,H], fill=CLOSEBG)
RLINE = (235,30,30)

def _passport_rows(rows):
    return rows

def _inspect(t, f):
    """Inspection mode: the screen tints red, a red line joins the expiry to today's date."""
    def draw(im, d, t, f):
        _bg(d)
        page(im, d, 4, 3, 120, 61, 'KOLECHIA', (74,90,108), [(11,'NAME','PAVEL KOLOV',1),(19,'BORN','1941.06.12',1),
             (27,'ISS','GRESTIN',1),(36,'EXPIRES','82.03.14',2)], photo='mous')
        d.rectangle([126,3,181,21], fill=(16,16,18)); text(d, 'DATE', 130, 6, (150,150,140), shadow=None)
        text(d, '82.11.26', 130, 14, CREAM, shadow=None)
        im = _redtint(im); d = ImageDraw.Draw(im)
        p = ease((t - 0.1) / 0.4); a, b = (103, 52), (126, 14)
        if p > 0:
            e = (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p); d.line([a, e], fill=RLINE, width=2)
            d.rectangle([a[0]-2,a[1]-2,a[0]+2,a[1]+2], fill=RLINE)
            if p >= 1: d.rectangle([b[0]-2,b[1]-2,b[0]+2,b[1]+2], fill=RLINE)
        if t >= 0.45: d.rectangle([124,27,182,61], outline=RLINE); big_text(im, 'EXPIRED', 30, (235,40,40), scale=2, cx=153, shadow=None)
        if t >= 0.65: text(d, 'DISCREPANCY', 132, 52, (255,250,220) if (f // 3) % 2 else (235,40,40), shadow=None)
        return im
    return closeup(t, f, draw=draw, zoom=(235,60,60))

def _sweat(t, f):
    def draw(im, d, t, f):
        d.rectangle([0,0,W,H], fill=(30,24,20))
        for y in range(2, H, 8): d.line([0,y,W,y], fill=(44,36,28))
        bust(d, 'mous', 16, 3, 3, f, look=1 if (f // 5) % 2 else -1, sweat=True, blink=(f % 17 == 0))
    return closeup(t, f, draw=draw, txt="...IT IS FINE, YES?", box=(80,4,W-3,60), color=CREAM)

L_STAMP = 34
def _stamp_draw(im, d, k, kind, pagefn):
    _bg(d); pagefn(im, d)
    c, c2 = ((200,40,36), (110,20,20)) if kind == 'red' else ((80,150,54), (40,92,30))
    word = 'DENIED' if kind == 'red' else 'APPROVED'; hx = 90
    if k < 8: yb = lerp(42, 18, ease(k / 8))                                      # up
    elif k < 12: yb = 18 + (k % 2)                                                # a held breath
    elif k == 12: yb = 28                                                         # then down fast
    elif k == 13: yb = 37
    elif k < 20: yb = 42                                                          # pressed
    elif k < 28: yb = lerp(42, 24, ease((k - 20) / 8))
    else: yb = 24
    yb = int(yb)
    if k >= 14:                                                                   # the mark, big
        sc = 3 if kind == 'red' else 2                                            # APPROVED is longer: crisper at 2
        w = len(word) * 4 * sc - sc + 10; ty = 44 if sc == 3 else 47
        d.rectangle([hx - w // 2, ty - 4, hx + w // 2, ty + 5 * sc + 3], fill=PAPER, outline=c, width=2)
        big_text(im, word, ty, c, scale=sc, cx=hx, shadow=None)
        if k < 19:
            for i in range(8):
                a = i * 0.8 + 0.3; r = 14 + (k - 13) * 4
                d.point((hx + int(math.cos(a) * r * 1.6), yb + int(math.sin(a) * r * 0.2) - 1), fill=(236,232,210))
    p2 = (hx, yb - 28); p1 = (hx - 52, -18)
    d.line([p1, p2], fill=COAT, width=13); d.line([(p1[0] + 4, p1[1]), (p2[0] + 4, p2[1])], fill=COATD, width=2)
    d.line([(p2[0] - 9, p2[1] - 9), p2], fill=ORANGE, width=13)                    # the orange cuff
    d.rectangle([hx-6,yb-26,hx+6,yb-14], fill=(206,176,148)); d.rectangle([hx-6,yb-16,hx+6,yb-14], fill=(170,140,116))
    d.rectangle([hx-4,yb-14,hx+4,yb-6], fill=(60,60,62)); d.rectangle([hx-12,yb-6,hx+12,yb], fill=c); d.rectangle([hx-12,yb-2,hx+12,yb], fill=c2)

def stamp_frame(k, kind, pagefn):
    """The stamp slamming down: it winds up, drops, the whole frame jolts and flashes, the mark is there."""
    im = closeup(k / L_STAMP, k, draw=lambda im, d, t, f: _stamp_draw(im, d, k, kind, pagefn), zoom=None)
    sh = {14:(0,4),15:(-3,-2),16:(3,2),17:(-2,-1),18:(2,1),19:(-1,0),20:(1,0)}.get(k)
    if sh: im = shift(im, *sh)
    if k in (14, 15): im = Image.blend(im, Image.new('RGB', (W, H), (255,255,255)), 0.6 if k == 14 else 0.2)
    return im

def pg_koll(im, d): page(im, d, 28, 28, 152, 62, 'KOLECHIA', (74,90,108), bars=(42,48,54))
def pg_cobra(im, d):
    d.rectangle([28,28,152,62], fill=(238,236,224), outline=(150,140,120))
    for i, ch in enumerate('COBRASTAN'): text(d, ch, 40 + i * 6, 32 + (i * 3) % 3, ((200,50,50),(50,70,200),(40,150,60))[i % 3], shadow=None)
    for y in (46, 52): d.line([36,y,120,y], fill=(190,184,170))
def pg_arst(im, d): page(im, d, 28, 28, 152, 62, 'ARSTOTZKA', (86,110,70), bars=(42,48,54))

def _crayon(t, f):
    """Jorji's passport: a crayon sheet, wobbly letters, a stick-figure photo."""
    def draw(im, d, t, f):
        _bg(d); d.rectangle([14,3,170,61], fill=(240,236,222), outline=(150,140,120))
        d.rectangle([22,12,56,46], outline=(60,60,200))
        d.ellipse([34,15,44,25], outline=(30,30,30)); d.point((37,19), fill=(30,30,30)); d.point((41,19), fill=(30,30,30))
        d.line([37,23,41,23], fill=(200,40,40)); d.line([39,25,39,36], fill=(30,30,30))
        d.line([39,28,32,33], fill=(30,30,30)); d.line([39,28,46,33], fill=(30,30,30))
        d.line([39,36,34,44], fill=(30,30,30)); d.line([39,36,44,44], fill=(30,30,30)); d.line([34,15,44,15], fill=(120,80,40), width=2)
        for i, ch in enumerate('PASPORT'): text(d, ch, 66 + i * 5, 7 + round(math.sin(f * 0.6 + i)), (150,60,200), shadow=None)
        cols = ((210,50,40),(50,80,210),(40,160,60),(230,150,30))
        for i, ch in enumerate('COBRASTAN'):
            big_text(im, ch, 22 + round(math.sin(f * 0.5 + i * 1.3) * 2), cols[i % 4], scale=2, cx=72 + i * 9, shadow=None)
        text(d, 'NAME JORJI', 66, 44, (60,60,60), shadow=None); text(d, 'FOTO', 30, 50, (60,60,200), shadow=None)
        d.ellipse([124,40,150,58], outline=(210,50,40)); text(d, 'OK', 131, 47, (210,50,40), shadow=None)
    return closeup(t, f, draw=draw)

def _cmd(t, f, name, purpose, dur, photo, flagged=False):
    """A command's passport: NAME, PURPOSE and DURATION coming up one by one (flagged: inspection mode, in red)."""
    def draw(im, d, t, f):
        _bg(d); page(im, d, 14, 3, 170, 61, 'ARSTOTZKA', (86,110,70), [(11,'NAME',name,2)], photo=photo)
        if t > 0.2 or flagged: text(d, 'PURPOSE', 50, 38, PAPD, shadow=None); text(d, purpose, 82, 38, INKC, shadow=None)
        if t > 0.4 or flagged: text(d, 'DURATION', 50, 47, PAPD, shadow=None); text(d, dur, 86, 47, INKC, shadow=None)
        if not flagged: return
        im = _redtint(im); d = ImageDraw.Draw(im)
        if (f // 3) % 3: d.rectangle([48,16,128,34], outline=RLINE, width=2)
        if t > 0.35: d.rectangle([48,45,134,54], outline=RLINE)
        d.rectangle([128,50,183,62], fill=(170,24,24)); text(d, 'DANGEROUS', 134, 54, (255,250,220), shadow=None)
        return im
    return closeup(t, f, draw=draw, zoom=(235,60,60) if flagged else (255,255,255))

def _claude(t, f, mode, txt):
    def draw(im, d, t, f):
        d.rectangle([0,0,W,H], fill=(30,24,20))
        for y in range(2, H, 8): d.line([0,y,W,y], fill=(44,36,28))
        claude_face(d, 22, 10, 3, f, mode)
    return closeup(t, f, draw=draw, txt=txt, box=(90,4,W-3,60), max_scale=3)

# ---- the clips: each starts and ends on the neutral booth (frame N is frame 0) ----------------------------------
def seg(f, a, n, fn):
    """fn(local frame) while a <= f < a + n, else None."""
    return fn(f - a) if a <= f < a + n else None

def walk_in(f, t0):
    """(walker x, head top): up the queue to the gate in 24 frames, then the head rises in the window in 12."""
    if f < t0: return None, None
    if f < t0 + 24: return lerp(48, GATE, (f - t0) / 24), None
    return None, lerp(48, 24, ease((f - t0 - 24) / 12))

def walk_out(f, t0, dur=30):
    """The head sinks in 8 frames, then the walker goes off to the right (x, head top)."""
    if f < t0 + 8: return None, lerp(24, 50, ease((f - t0) / 8))
    x = GATE + (190 - GATE) * (f - t0 - 8) / dur
    return (x if x < 188 else None), None

def clip_denied(f):
    s = scene(f, THEME)
    im = seg(f, 96, 44, lambda k: _inspect(k / 44, f)) or seg(f, 140, 36, lambda k: _sweat(k / 36, f)) \
        or seg(f, 176, L_STAMP, lambda k: stamp_frame(k, 'red', pg_koll))
    if im: s['image'] = im; return s
    wk, by = (None, 24) if 46 <= f < 218 else walk_in(f, 10)                     # in the window from 46 to 218
    if f >= 218: wk, by = walk_out(f, 218)
    items = []
    if 46 <= f < 62: items = [('pass', lerp(30, 54, ease((f - 46) / 14)), FOREIGN)]
    if 210 <= f < 224: items = [('pass', lerp(54, 30, ease((f - 210) / 12)), FOREIGN, 'x')]    # handed back, stamped
    doc = 70 <= f < 96
    hl = ('doc' if (f // 6) % 2 == 0 else 'book') if doc else None
    hand = kf(f, [(0,HOME),(48,HOME),(58,(58,52)),(63,(58,52)),(72,(150,54)),(94,(150,54)),(100,HOME),(264,HOME)])
    im = room(f, wk, 'mous', by, dict(look=-1 if 46 <= f < 62 else 0, blink=(f % 40 == 0)), items, doc, hand,
              look=(2 if hl == 'doc' else 0), loud=(6 <= f < 26), hl=hl, hdown=(f >= 228))
    if cue(f, 6, NEXT): cap(im, NEXT, max_scale=3)
    if cue(f, 224, GLORY): cap(im, GLORY, col=(255,230,150))
    s['image'] = im; return s

def clip_jorji(f):
    s = scene(f, THEME)
    im = seg(f, 54, 40, lambda k: _crayon(k / 40, f)) or seg(f, 94, 18, lambda k: _claude(k / 18, f, 'stare', '...')) \
        or seg(f, 134, L_STAMP, lambda k: stamp_frame(k, 'red', pg_cobra)) \
        or seg(f, 244, L_STAMP, lambda k: stamp_frame(k, 'green', pg_arst))
    if im: s['image'] = im; return s
    wk, by = (None, 24) if 46 <= f < 168 else walk_in(f, 10)
    if 168 <= f < 204: wk, by = walk_out(f, 168, 14)                              # leaves ...
    if 176 <= f < 190: wk = lerp(GATE, 100, (f - 176) / 14)
    elif 190 <= f < 204: wk = lerp(100, GATE, (f - 190) / 14)                     # ... and comes right back
    if 204 <= f < 216: by = lerp(48, 24, ease((f - 204) / 12))
    elif 216 <= f < 300: by = 24
    if 278 <= f < 300 and f >= 292: by = 24 - (f // 3) % 2                        # cheering
    if f >= 300: wk, by = walk_out(f, 300, 24)
    if 168 <= f < 204 and by is None and wk is None: by = None
    items = []
    if 44 <= f < 54: items = [('pass', lerp(30, 54, ease((f - 44) / 10)), (240,236,222))]
    if 214 <= f < 232: items = [('pass', 54, FOREIGN), ('tin', lerp(30, 42, ease((f - 214) / 12)))]
    hand = kf(f, [(0,HOME),(230,HOME),(234,(131,31)),(238,(131,31)),(240,(161,31)),(244,(161,31)),(280,HOME)])
    bk = dict(wink=(222 <= f < 230), wave=(292 <= f < 308))
    im = room(f, wk, 'jorji', by, bk, items, 232 <= f < 244, hand, loud=(6 <= f < 26), wwave=(f >= 300))
    if 222 <= f < 230: spark(ImageDraw.Draw(im), 40, 29, 2 + f % 2, CREAM)
    if cue(f, 6, NEXT): cap(im, NEXT, max_scale=3)
    if 112 <= f < 134: cap(im, NOPROB, max_scale=2)
    if cue(f, 280, SEEYA): cap(im, SEEYA, col=(255,230,150))
    s['image'] = im; return s

def clip_permission(f):
    s = scene(f, THEME)
    im = seg(f, 56, 38, lambda k: _cmd(k / 38, f, 'rm -rf /', 'CLEANUP', 'FOREVER', 'hood')) \
        or seg(f, 94, 16, lambda k: _claude(k / 16, f, 'brow', '?')) \
        or seg(f, 110, 26, lambda k: _cmd(k / 26, f, 'rm -rf /', 'CLEANUP', 'FOREVER', 'hood', True)) \
        or seg(f, 136, L_STAMP, lambda k: stamp_frame(k, 'red', pg_arst)) \
        or seg(f, 248, 32, lambda k: _cmd(k / 32, f, 'git status', 'LOOK', 'INSTANT', 'neat')) \
        or seg(f, 280, L_STAMP, lambda k: stamp_frame(k, 'green', pg_arst))
    if im: s['image'] = im; return s
    items, dis, gate, kind = [], 0.0, False, 'hood'
    if f < 198:                                                                   # the hooded command
        wk, by = (None, 24) if 46 <= f < 198 else walk_in(f, 10)
        if 46 <= f < 56: items = [('pass', lerp(30, 54, ease((f - 46) / 10)), FOREIGN)]
        if f >= 170:                                                              # denied: he breaks up into pixels
            dis = min(1.0, (f - 170) / 24)
            if dis < 0.5: items = [('pass', 54, FOREIGN, 'x')]
            if dis >= 1.0: by = None
    else:                                                                         # the tidy command
        kind = 'neat'; wk, by = (None, 24) if 226 <= f < 314 else walk_in(f, 202)
        if 238 <= f < 248: items = [('pass', lerp(30, 54, ease((f - 238) / 8)), FOREIGN)]
        if f >= 314: wk, by = walk_out(f, 314, 36)
        gate = 322 <= f < 358
    bk = dict(blink=(f % 40 == 0), wave=(kind == 'neat' and 306 <= f < 322))
    im = room(f, wk, kind, by, bk, items, False, HOME, loud=(6 <= f < 26 or 200 <= f < 218), gate=gate, dis=dis, wwave=(322 <= f < 358))
    if cue(f, 6, NEXT) or cue(f, 200, NEXT): cap(im, NEXT, max_scale=3)
    s['image'] = im; return s

register_bg(THEME, lambda v: (v+30,v+30,v+32))
CLIPS = [clip('denied', 264, clip_denied), clip('jorji', 336, clip_jorji), clip('permission', 360, clip_permission)]
