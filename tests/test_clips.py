"""Tests for scripts/clips.py (choose which clips play). Run: python3 -m unittest discover tests"""
import json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import clips

CLIPS = ['dbz__beam', 'dbz__teleport', 'meshi__dragonstew', 'terraria__melee', 'terraria__summoner']


class Active(unittest.TestCase):
    def test_no_keys_means_everything_plays(self):
        self.assertEqual(clips.active({}, CLIPS), set(CLIPS))

    def test_new_enabled_plays_all_but_disabled(self):
        cfg = {'newClips': 'enabled', 'disabled': ['dbz__teleport']}
        self.assertEqual(clips.active(cfg, CLIPS), set(CLIPS) - {'dbz__teleport'})

    def test_new_disabled_plays_only_enabled(self):
        cfg = {'newClips': 'disabled', 'enabled': ['meshi__dragonstew']}
        self.assertEqual(clips.active(cfg, CLIPS), {'meshi__dragonstew'})

    def test_a_new_clip_follows_the_mode(self):
        new = CLIPS + ['sw__father']
        self.assertIn('sw__father', clips.active({'newClips': 'enabled', 'disabled': []}, new))
        self.assertNotIn('sw__father', clips.active({'newClips': 'disabled', 'enabled': CLIPS}, new))


class Updates(unittest.TestCase):
    def test_enabled_mode_writes_only_the_disabled_list(self):
        up, drop = clips.updates({}, CLIPS, set(CLIPS) - {'dbz__beam'}, 'enabled')
        self.assertEqual(up, {'newClips': 'enabled', 'disabled': ['dbz__beam']})
        self.assertEqual(drop, {'enabled'})

    def test_disabled_mode_writes_only_the_enabled_list(self):
        up, drop = clips.updates({}, CLIPS, {'meshi__dragonstew'}, 'disabled')
        self.assertEqual(up, {'newClips': 'disabled', 'enabled': ['meshi__dragonstew']})
        self.assertEqual(drop, {'disabled'})

    def test_switching_mode_keeps_what_plays(self):
        cfg = {'newClips': 'enabled', 'disabled': ['dbz__teleport']}
        up, _ = clips.updates(cfg, CLIPS, clips.active(cfg, CLIPS), 'disabled')
        self.assertEqual(clips.active(up, CLIPS), clips.active(cfg, CLIPS))

    def test_unknown_names_survive_a_save_in_the_same_mode(self):
        cfg = {'newClips': 'enabled', 'disabled': ['gone__clip']}
        up, _ = clips.updates(cfg, CLIPS, set(CLIPS) - {'dbz__beam'}, 'enabled')
        self.assertEqual(up['disabled'], ['dbz__beam', 'gone__clip'])


class Expand(unittest.TestCase):
    def test_a_theme_expands_to_its_clips(self):
        self.assertEqual(clips.expand(['terraria'], CLIPS), ['terraria__melee', 'terraria__summoner'])

    def test_a_clip_stays_itself(self):
        self.assertEqual(clips.expand(['dbz__beam'], CLIPS), ['dbz__beam'])

    def test_an_unknown_name_fails_with_a_suggestion(self):
        with self.assertRaises(clips.ClipsError) as e: clips.expand(['meshi__dragonstw'], CLIPS)
        self.assertIn('meshi__dragonstew', str(e.exception))


class Files(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(); self.path = os.path.join(self.dir, 'config.json')

    def test_save_rereads_and_keeps_other_keys(self):
        json.dump({'scale': 1.5, 'first': ['a__b'], 'enabled': ['x']}, open(self.path, 'w'))
        clips.save(self.path, {'newClips': 'enabled', 'disabled': ['dbz__beam']}, {'enabled'})
        self.assertEqual(json.load(open(self.path)),
                         {'scale': 1.5, 'first': ['a__b'], 'newClips': 'enabled', 'disabled': ['dbz__beam']})

    def test_a_missing_config_is_created(self):
        clips.save(self.path, {'newClips': 'disabled', 'enabled': []}, set())
        self.assertEqual(json.load(open(self.path)), {'newClips': 'disabled', 'enabled': []})

    def test_broken_json_is_never_overwritten(self):
        open(self.path, 'w').write('{"scale": 1.5,\n "first": [}\n')
        with self.assertRaises(clips.ClipsError) as e: clips.save(self.path, {'newClips': 'enabled'}, set())
        self.assertIn('line 2', str(e.exception))
        self.assertEqual(open(self.path).read(), '{"scale": 1.5,\n "first": [}\n')

    def test_clip_names_come_from_the_build(self):
        for n in ('dbz__beam', 'meshi__dragonstew'): os.makedirs(os.path.join(self.dir, 'clips', n))
        self.assertEqual(clips.clip_names(os.path.join(self.dir, 'clips')), ['dbz__beam', 'meshi__dragonstew'])

    def test_no_build_is_an_error(self):
        with self.assertRaises(clips.ClipsError) as e: clips.clip_names(os.path.join(self.dir, 'nope'))
        self.assertIn('./build.sh', str(e.exception))


class Checklist(unittest.TestCase):
    """The checklist's state, without curses."""
    def model(self, cfg=None):
        return clips.Checklist(CLIPS, cfg if cfg is not None else {})

    def test_rows_are_themes_then_their_clips(self):
        self.assertEqual([r[1] for r in self.model().rows()[:3]], ['dbz', 'dbz__beam', 'dbz__teleport'])

    def test_toggling_a_theme_toggles_all_its_clips(self):
        m = self.model(); m.toggle('terraria')
        self.assertFalse({'terraria__melee', 'terraria__summoner'} & m.on)
        m.toggle('terraria')
        self.assertTrue({'terraria__melee', 'terraria__summoner'} <= m.on)

    def test_a_partly_selected_theme_shows_tilde(self):
        m = self.model(); m.toggle('terraria__summoner')
        self.assertEqual(m.mark('terraria'), '~')

    def test_toggling_a_partly_selected_theme_selects_all(self):
        m = self.model(); m.toggle('terraria__summoner'); m.toggle('terraria')
        self.assertEqual(m.mark('terraria'), 'x')

    def test_mode_switch_keeps_the_selection(self):
        m = self.model(); m.toggle('dbz__beam'); before = set(m.on); m.switch_mode()
        self.assertEqual((m.mode, m.on), ('disabled', before))

    def test_clear_first_empties_the_forced_list(self):
        m = self.model({'first': ['meshi__dragonstew']}); m.clear_first()
        self.assertEqual(m.first, [])
        up, drop = m.result({})
        self.assertEqual(up['first'], [])


if __name__ == '__main__':
    unittest.main()
