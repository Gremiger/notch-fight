"""Packs one clip (or transition) for the Claude Code mod's Raster mode in quadrant blocks: every
frame shrunk to `columns*2` x `rows*2` pixels, and each cell's 2x2 pixels drawn as one of the 16
quadrant characters (▘▝▀▖▌▞▛▗▚▐▜▄▙▟█ and space) in the two colours that fit them best (a cell holds
only a foreground and a background). 8 bytes a cell: the character's code point (u16, little
endian), the foreground's RGB, the background's RGB; row-major, frames back to back.

    python3 scripts/mod_cells.py <frames dir> <columns> <rows> <out file>"""
import os, struct, sys
from PIL import Image

# the quadrant character for each mask of foreground pixels: bit 1 top left, 2 top right,
# 4 bottom left, 8 bottom right
QUAD = [0x20, 0x2598, 0x259D, 0x2580, 0x2596, 0x258C, 0x259E, 0x259B,
        0x2597, 0x259A, 0x2590, 0x259C, 0x2584, 0x2599, 0x259F, 0x2588]

def mean(px): return tuple(sum(c[i] for c in px)//len(px) for i in range(3))
def dist(a, b): return sum((a[i]-b[i])**2 for i in range(3))

def cell(px):
    """The (code point, fg, bg) whose two colours best match the 4 pixels (TL, TR, BL, BR)."""
    if len(set(px)) == 1: return QUAD[0], px[0], px[0]
    best = None
    for mask in range(1, 8):                     # every split into two groups (mask and ~mask)
        fg = [p for i, p in enumerate(px) if mask >> i & 1]; bg = [p for i, p in enumerate(px) if not mask >> i & 1]
        f, b = mean(fg), mean(bg)
        err = sum(dist(p, f) for p in fg)+sum(dist(p, b) for p in bg)
        if best is None or err < best[0]: best = (err, mask, f, b)
    _, mask, f, b = best
    return QUAD[mask], f, b

def main(src, columns, rows, out):
    names = sorted(n for n in os.listdir(src) if n.endswith('.png'))
    data = bytearray(); memo = {}
    for n in names:
        im = Image.open(os.path.join(src, n)).convert('RGB').resize((columns*2, rows*2), Image.BOX)
        px = im.load()
        for y in range(0, rows*2, 2):
            for x in range(0, columns*2, 2):
                key = (px[x, y], px[x+1, y], px[x, y+1], px[x+1, y+1])
                if key not in memo:
                    cp, f, b = cell(key); memo[key] = struct.pack('<H', cp)+bytes(f)+bytes(b)
                data += memo[key]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out+'.tmp'; open(tmp, 'wb').write(data); os.replace(tmp, out)   # the mod never reads half a file
    print(len(names))

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
