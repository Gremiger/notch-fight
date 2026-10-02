"""scripts/mod_cells.py packs frames into the quadrant cells the Claude Code mod draws."""
import os, struct, subprocess, sys, tempfile, unittest
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
SCRIPT = os.path.join(ROOT, 'scripts', 'mod_cells.py')

def pack(frames, columns, rows):
    tmp = tempfile.mkdtemp()
    for i, im in enumerate(frames): im.save(os.path.join(tmp, f'{i:03d}.png'))
    out = os.path.join(tmp, 'out', 'clip.cells')
    subprocess.run([sys.executable, SCRIPT, tmp, str(columns), str(rows), out], check=True, capture_output=True)
    return open(out, 'rb').read()

def cells(data):
    return [(struct.unpack('<H', data[i:i+2])[0], tuple(data[i+2:i+5]), tuple(data[i+5:i+8])) for i in range(0, len(data), 8)]

class ModCells(unittest.TestCase):
    def test_eight_bytes_a_cell_frames_back_to_back(self):
        data = pack([Image.new('RGB', (40, 16), (10, 20, 30))]*3, 5, 2)
        self.assertEqual(len(data), 3*5*2*8)

    def test_a_flat_cell_is_a_space_in_its_colour(self):
        self.assertEqual(cells(pack([Image.new('RGB', (4, 4), (200, 0, 0))], 2, 2))[0], (0x20, (200, 0, 0), (200, 0, 0)))

    def test_a_split_cell_picks_the_quadrant_and_both_colours(self):
        im = Image.new('RGB', (2, 2), (0, 0, 0)); im.putpixel((0, 0), (255, 255, 255))   # only the top left lit
        cp, fg, bg = cells(pack([im], 1, 1))[0]
        self.assertEqual(cp, 0x2598)                                                    # ▘
        self.assertEqual((fg, bg), ((255, 255, 255), (0, 0, 0)))

if __name__ == '__main__':
    unittest.main()
