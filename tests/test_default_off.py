"""Clips can ship off by default: DEFAULT_OFF = True in a theme, or clip(..., off=True/False) per clip."""
import os, sys, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from engine import clip
from themes import normalize

def fn(f): return None

class ClipDeclaration(unittest.TestCase):
    def test_clip_carries_its_options(self):
        self.assertEqual(clip('a', 1, fn, off=True)[3], {'off': True})

    def test_clip_without_options_has_none(self):
        self.assertEqual(clip('a', 1, fn)[3], {})

class Normalize(unittest.TestCase):
    """load_themes() hands build.py (name, frames, frame_fn, off) for every clip."""
    def off(self, item, default_off): return normalize([item], default_off)[0][3]

    def test_plain_tuples_still_work(self):                  # themes that build the tuple by hand (dbz)
        self.assertFalse(self.off(('a', 1, fn), False))

    def test_theme_default_off_applies_to_its_clips(self):
        self.assertTrue(self.off(('a', 1, fn), True))
        self.assertTrue(self.off(clip('a', 1, fn), True))

    def test_a_clip_can_opt_out_of_the_theme_default(self):
        self.assertFalse(self.off(clip('a', 1, fn, off=False), True))

    def test_a_clip_can_ship_off_in_a_theme_that_is_on(self):
        self.assertTrue(self.off(clip('a', 1, fn, off=True), False))

    def test_name_frames_and_fn_pass_through(self):
        self.assertEqual(normalize([('a', 7, fn)], False)[0][:3], ('a', 7, fn))

if __name__ == '__main__':
    unittest.main()
