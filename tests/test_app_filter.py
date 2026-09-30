"""The app honours the clip selection in config.json. Runs the built binary (the panel shows for a
moment) against temporary configs via NOTCH_FIGHT_CONFIG; skipped when there is no build or no Mac."""
import json, os, platform, select, subprocess, tempfile, time, unittest

ROOT = os.path.join(os.path.dirname(__file__), '..')
BIN = os.path.join(ROOT, 'build', 'NotchFight.app', 'Contents', 'MacOS', 'NotchFight')
CLIPS = sorted(os.listdir(os.path.join(ROOT, 'build', 'clips'))) if os.path.isdir(os.path.join(ROOT, 'build', 'clips')) else []

@unittest.skipUnless(platform.system() == 'Darwin' and os.path.exists(BIN), 'needs macOS and ./build.sh')
class AppFilter(unittest.TestCase):
    def launch(self, cfg, wait=1.0):
        """Run the app with this config; return (stderr log, whether it quit on its own `wait` s after
        logging its selection)."""
        path = os.path.join(tempfile.mkdtemp(), 'config.json'); json.dump(cfg, open(path, 'w'))
        env = dict(os.environ, NOTCH_FIGHT_CONFIG=path); env.pop('NOTCH_FIGHT_FIRST', None)
        p = subprocess.Popen([BIN], env=env, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
        log, t0, seen = b'', time.time(), None
        while time.time() - t0 < 10:                   # wait for the selection line, not a fixed time
            r, _, _ = select.select([p.stderr], [], [], 0.1)
            if r:
                chunk = os.read(p.stderr.fileno(), 65536)
                if not chunk: break                    # the app quit
                log += chunk
            if seen is None and b'clips active' in log: seen = time.time()
            if seen is not None and time.time() - seen >= wait: break
        try: p.wait(timeout=1); quit_alone = True        # it quit on its own (e.g. nothing to show)
        except subprocess.TimeoutExpired: quit_alone = False; p.kill()
        rest = p.communicate()[1]
        return (log + (rest or b'')).decode(errors='replace'), quit_alone

    def test_no_selection_keys_plays_everything(self):
        log, _ = self.launch({})
        self.assertIn(f'{len(CLIPS)}/{len(CLIPS)} clips active', log)

    def test_new_disabled_plays_only_the_enabled_list(self):
        log, _ = self.launch({'newClips': 'disabled', 'enabled': [CLIPS[0]]})
        self.assertIn(f'1/{len(CLIPS)} clips active', log)

    def test_new_enabled_skips_the_disabled_list(self):
        log, _ = self.launch({'newClips': 'enabled', 'disabled': CLIPS[:2]})
        self.assertIn(f'{len(CLIPS) - 2}/{len(CLIPS)} clips active', log)

    def test_nothing_active_quits_without_a_panel(self):
        log, quit_alone = self.launch({'newClips': 'disabled', 'enabled': []})
        self.assertIn('no clips active', log)
        self.assertTrue(quit_alone)

    def test_a_forced_clip_plays_even_when_disabled(self):
        log, quit_alone = self.launch({'newClips': 'disabled', 'enabled': [], 'first': [CLIPS[0]]})
        self.assertIn(f'0/{len(CLIPS)} clips active', log)
        self.assertFalse(quit_alone)

    def test_unknown_names_in_the_lists_are_logged(self):
        log, _ = self.launch({'newClips': 'enabled', 'disabled': ['nope__clip']})
        self.assertIn("unknown clip 'nope__clip'", log)

if __name__ == '__main__':
    unittest.main()
