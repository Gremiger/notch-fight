"""The resident app (the default): up and hidden between prompts, it shows itself while a Claude session
works and hides again, following the markers in sessions/, the gate, "delay" and a running preview.

A copy of the app runs straight from its binary against a temporary config folder (NOTCH_FIGHT_CONFIG,
so its sessions/ and .preview are there too) and reports each change to NOTCH_FIGHT_TRACE. The panel
really shows, so these only run with NOTCH_FIGHT_TEST_PANEL=1 (like test_app_filter.AppPanel)."""
import json, os, platform, signal, subprocess, tempfile, time, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BIN = os.path.join(ROOT, 'build', 'NotchFight.app', 'Contents', 'MacOS', 'NotchFight')
CLIPS = os.path.join(ROOT, 'build', 'clips')
RUN = platform.system() == 'Darwin' and os.path.exists(BIN) and os.environ.get('NOTCH_FIGHT_TEST_PANEL') == '1'

@unittest.skipUnless(RUN, 'shows the panel: opt in with NOTCH_FIGHT_TEST_PANEL=1 (needs macOS and ./build.sh)')
class Resident(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.cfg = os.path.join(self.dir, 'config.json')
        self.sessions = os.path.join(self.dir, 'sessions'); os.makedirs(self.sessions)
        self.trace = os.path.join(self.dir, 'trace')
        clip = sorted(c for c in os.listdir(CLIPS) if not os.path.exists(os.path.join(CLIPS, c, '.default-off')))[0]
        self.config(newClips='disabled', enabled=[clip], pauseOnShare=False)
        self.worker = subprocess.Popen(['sleep', '120'])                 # stands in for a working `claude`
        env = dict(os.environ, NOTCH_FIGHT_CONFIG=self.cfg, NOTCH_FIGHT_TRACE=self.trace)
        self.app = subprocess.Popen([BIN], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.0)

    def tearDown(self):
        self.app.terminate(); self.app.wait(timeout=5)
        self.worker.kill(); self.worker.wait()

    def config(self, **cfg): json.dump(cfg, open(self.cfg, 'w'))
    def poke(self): self.app.send_signal(signal.SIGUSR1)
    def marker(self, pid=None, name='s1'):
        tmp = os.path.join(self.sessions, f'.{name}.tmp')
        open(tmp, 'w').write(str(pid or self.worker.pid)); os.replace(tmp, os.path.join(self.sessions, name))
    def unmark(self, name='s1'): os.remove(os.path.join(self.sessions, name))
    def lines(self): return open(self.trace).read().split() if os.path.exists(self.trace) else []
    def state(self, wait=2.0, want=None):
        """The last change reported ('hidden' before any), waiting up to `wait` s for `want`."""
        end = time.time() + wait
        while True:
            last = (self.lines() or ['hidden'])[-1]
            if last == want or time.time() > end: return last
            time.sleep(0.05)

    def test_hidden_until_a_session_works_then_hidden_again(self):
        self.assertEqual(self.lines(), [])
        self.marker(); self.assertEqual(self.state(want='shown'), 'shown')
        self.unmark(); self.assertEqual(self.state(want='hidden'), 'hidden')
        self.marker(); self.assertEqual(self.state(want='shown'), 'shown')   # and again on the next prompt
        self.assertEqual(self.app.poll(), None)                              # never quit

    def test_a_dead_session_does_not_count(self):
        dead = subprocess.Popen(['true']); dead.wait()
        self.marker(dead.pid); time.sleep(1.0)
        self.assertEqual(self.lines(), [])
        self.assertFalse(os.path.exists(os.path.join(self.sessions, 's1')))  # pruned

    def test_a_pause_hides_it_and_resume_brings_it_back(self):
        self.marker(); self.state(want='shown')
        json.dump({'until': None}, open(os.path.join(self.dir, 'paused'), 'w')); self.poke()
        self.assertEqual(self.state(want='hidden'), 'hidden')
        os.remove(os.path.join(self.dir, 'paused')); self.poke()
        self.assertEqual(self.state(want='shown'), 'shown')

    def test_delay(self):
        self.config(**dict(json.load(open(self.cfg)), delay=2))
        self.marker(); time.sleep(1.0)
        self.assertEqual(self.lines(), [])                                   # not yet
        self.assertEqual(self.state(wait=3.0, want='shown'), 'shown')

    def test_it_steps_aside_for_a_preview(self):
        self.marker(); self.state(want='shown')
        preview = os.path.join(self.dir, '.preview')
        open(preview, 'w').write(str(self.worker.pid)); self.poke()          # a live "preview" copy
        self.assertEqual(self.state(want='hidden'), 'hidden')
        os.remove(preview); self.poke()
        self.assertEqual(self.state(want='shown'), 'shown')

    def test_sigterm_quits(self):
        self.marker(); self.state(want='shown')
        self.app.terminate()
        self.assertEqual(self.app.wait(timeout=3), 0)

if __name__ == '__main__':
    unittest.main()
