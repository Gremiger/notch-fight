"""scripts/mod_cells.py packs frames into the block cells the Claude Code mod draws."""
import os, struct, subprocess, sys, tempfile, unittest
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
SCRIPT = os.path.join(ROOT, 'scripts', 'mod_cells.py')

def pack(frames, columns, rows, glyphs='quad'):
    tmp = tempfile.mkdtemp()
    for i, im in enumerate(frames): im.save(os.path.join(tmp, f'{i:03d}.png'))
    out = os.path.join(tmp, 'out', 'clip')
    subprocess.run([sys.executable, SCRIPT, tmp, str(columns), str(rows), out, glyphs], check=True, capture_output=True)
    return b''.join(open(os.path.join(out, n), 'rb').read() for n in sorted(os.listdir(out)))

def cells(data):
    return [(int.from_bytes(data[i:i+3], 'little'), tuple(data[i+3:i+6]), tuple(data[i+6:i+9])) for i in range(0, len(data), 9)]

class ModCells(unittest.TestCase):
    def test_nine_bytes_a_cell_frames_back_to_back(self):
        data = pack([Image.new('RGB', (40, 16), (10, 20, 30))]*3, 5, 2)
        self.assertEqual(len(data), 3*5*2*9)

    def test_a_flat_cell_is_a_space_in_its_colour(self):
        self.assertEqual(cells(pack([Image.new('RGB', (4, 4), (200, 0, 0))], 2, 2))[0], (0x20, (200, 0, 0), (200, 0, 0)))

    def test_a_split_cell_picks_the_quadrant_and_both_colours(self):
        im = Image.new('RGB', (2, 2), (0, 0, 0)); im.putpixel((0, 0), (255, 255, 255))   # only the top left lit
        cp, fg, bg = cells(pack([im], 1, 1))[0]
        self.assertEqual(cp, 0x2598)                                                    # ▘
        self.assertEqual((fg, bg), ((255, 255, 255), (0, 0, 0)))

    def test_a_sextant_cell_takes_2x3_pixels(self):
        im = Image.new('RGB', (2, 3), (0, 0, 0)); im.putpixel((0, 0), (255, 255, 255))   # only the top left lit
        cp, fg, bg = cells(pack([im], 1, 1, 'sextant'))[0]
        self.assertEqual(cp, 0x1FB00)                                                   # BLOCK SEXTANT-1
        self.assertEqual((fg, bg), ((255, 255, 255), (0, 0, 0)))

    def test_sextants_reuse_the_half_blocks_unicode_skips(self):
        im = Image.new('RGB', (2, 3), (0, 0, 0))
        for y in range(3): im.putpixel((0, y), (255, 255, 255))                         # the left column
        cp, fg, bg = cells(pack([im], 1, 1, 'sextant'))[0]
        self.assertEqual((cp, fg, bg), (0x258C, (255, 255, 255), (0, 0, 0)))            # ▌

    def test_every_sextant_matches_its_unicode_name(self):
        import unicodedata
        sys.path.insert(0, os.path.join(ROOT, 'scripts'))
        from mod_cells import sextant
        for mask in range(64):
            if sextant(mask) >= 0x1FB00:                                                # BLOCK SEXTANT-<lit pixels, 1-based>
                self.assertEqual(unicodedata.name(chr(sextant(mask))), 'BLOCK SEXTANT-'+''.join(str(i+1) for i in range(6) if mask >> i & 1))

    def test_an_octant_cell_takes_2x4_pixels(self):
        im = Image.new('RGB', (2, 4), (0, 0, 0))
        for p in ((1, 0), (0, 2)): im.putpixel(p, (255, 255, 255))                         # pixels 2 and 5 lit
        cp, fg, bg = cells(pack([im], 1, 1, 'octant'))[0]
        self.assertEqual((cp, fg, bg), (0x1CD0B, (255, 255, 255), (0, 0, 0)))           # BLOCK OCTANT-25

    def test_octants_reuse_the_older_blocks(self):
        im = Image.new('RGB', (2, 4), (0, 0, 0))
        for p in ((0, 0), (1, 0), (0, 1), (1, 1)): im.putpixel(p, (255, 255, 255))         # the top half
        self.assertEqual(cells(pack([im], 1, 1, 'octant'))[0][0], 0x2580)                # ▀

    def test_frames_split_into_chunks_under_the_read_limit(self):
        sys.path.insert(0, os.path.join(ROOT, 'scripts'))
        from mod_cells import chunk_frames
        tmp = tempfile.mkdtemp()
        for i in range(5): Image.new('RGB', (4, 4), (i, 0, 0)).save(os.path.join(tmp, f'{i:03d}.png'))
        out = os.path.join(tmp, 'clip')
        subprocess.run([sys.executable, SCRIPT, tmp, '400', '400', out], check=True, capture_output=True)
        self.assertEqual(chunk_frames(400, 400), 2)                                       # 1.44 MB a frame
        self.assertEqual(sorted(os.listdir(out)), ['000.cells', '001.cells', '002.cells'])
        self.assertTrue(all(os.path.getsize(os.path.join(out, n)) <= 4194304 for n in os.listdir(out)))

if __name__ == '__main__':
    unittest.main()
