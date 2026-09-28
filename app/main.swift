import AppKit
import QuartzCore

// Drops a black pixel-art fight from under the MacBook notch. Click it to retract and quit.
final class NotchPanel: NSPanel {
    override var canBecomeKey: Bool { true }
    override func constrainFrameRect(_ r: NSRect, to s: NSScreen?) -> NSRect { r }
}

final class App: NSObject, NSApplicationDelegate {
    var win: NotchPanel!
    let art = CALayer()
    // Clips are grouped by theme (dir name "<theme>__<clip>"). Clips of one theme share a
    // loop keyframe and chain seamlessly; switching theme plays transitions/<from>__<to>.
    var themes: [String: [[CGImage]]] = [:]
    var transitions: [String: [CGImage]] = [:]
    var bags: [String: [Int]] = [:]
    var queue: [[CGImage]] = []
    var theme = "", lastClip: [String: Int] = [:]
    var clipIndex: [String: (String, Int)] = [:]   // "<theme>__<clip>" -> (theme, index)
    var current: [CGImage] = []
    var idx = 0
    var playTimer: Timer?
    var animTimer: Timer?
    let clipH: CGFloat = 64, corner: CGFloat = 12
    // overlap: rises into the notch to cover its rounded bottom corners.
    // fillet: concave flare where the panel meets the notch's bottom edge.
    let overlap: CGFloat = 10, fillet: CGFloat = 8
    let shape = CAShapeLayer()
    var root: CALayer!
    var notchW: CGFloat = 185, notchH: CGFloat = 32, screen: NSScreen!

    func applicationDidFinishLaunching(_ n: Notification) {
        screen = NSScreen.screens.first { $0.auxiliaryTopLeftArea != nil } ?? NSScreen.main!
        let f = screen.frame
        if let l = screen.auxiliaryTopLeftArea, let r = screen.auxiliaryTopRightArea {
            notchW = f.width - l.width - r.width
            notchH = screen.safeAreaInsets.top
        }
        let res = Bundle.main.resourceURL!
        for (name, imgs) in loadDirs(res.appendingPathComponent("clips")) {
            let t = String(name.split(separator: "_", maxSplits: 1).first ?? "")
            themes[t, default: []].append(imgs)
            clipIndex[name] = (t, themes[t]!.count - 1)
        }
        transitions = Dictionary(uniqueKeysWithValues: loadDirs(res.appendingPathComponent("transitions")))
        theme = themes.keys.randomElement() ?? ""
        // Forced clips play first, in order; then normal playback resumes from the last one's theme.
        for first in forcedFirst() {
            if let (t, i) = clipIndex[first] {        // a specific clip, e.g. "fn__royale"
                theme = t; lastClip[t] = i; queue.append(themes[t]![i])
            } else if themes[first] != nil {          // a whole theme, e.g. "ygo"
                theme = first; queue.append(nextClip(in: first))
            } else {
                NSLog("NotchFight: unknown first clip/theme '\(first)'. Known: \(clipIndex.keys.sorted())")
            }
        }
        if !queue.isEmpty, let prev = queue.last, let t = themes.first(where: { $0.value.contains { $0 == prev } })?.key {
            theme = t
        }
        enqueueVisit()
        win = NotchPanel(contentRect: rect(height: 0), styleMask: [.borderless, .nonactivatingPanel],
                         backing: .buffered, defer: false)
        win.level = .screenSaver
        win.backgroundColor = .clear
        win.isOpaque = false
        win.hasShadow = false
        win.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary, .ignoresCycle]

        let v = ClickView(frame: NSRect(origin: .zero, size: win.frame.size))
        v.onClick = { [weak self] in self?.close() }
        v.wantsLayer = true
        root = v.layer!
        root.backgroundColor = NSColor.black.cgColor
        root.mask = shape
        art.frame = CGRect(x: fillet, y: 0, width: notchW, height: clipH)
        art.contentsGravity = .resizeAspect
        art.magnificationFilter = .nearest
        art.contentsScale = screen.backingScaleFactor
        art.actions = ["contents": NSNull()]
        root.addSublayer(art)
        v.autoresizingMask = [.width, .height]
        win.contentView = v
        tick()
        updateMask()
        win.orderFrontRegardless()

        playTimer = Timer.scheduledTimer(withTimeInterval: 1.0 / 20.0, repeats: true) { [weak self] _ in self?.tick() }
        animate(to: clipH, duration: 0.55, spring: true)
    }

    func rect(height h: CGFloat) -> NSRect {
        let f = screen.frame
        // Hangs from the notch's bottom edge; never overlaps the notch itself.
        return NSRect(x: f.midX - notchW / 2 - fillet, y: f.maxY - notchH - h,
                      width: notchW + 2 * fillet, height: h + overlap)
    }

    // Body = notch width with rounded bottom; top flares concavely into the notch edge.
    func updateMask() {
        let size = win.frame.size, h = size.height - overlap
        let cb = min(corner, h / 2), fr = min(fillet, h / 2)
        let l = fillet, r = fillet + notchW, w = size.width
        let p = CGMutablePath()
        p.move(to: CGPoint(x: l + cb, y: 0))
        p.addLine(to: CGPoint(x: r - cb, y: 0))
        p.addQuadCurve(to: CGPoint(x: r, y: cb), control: CGPoint(x: r, y: 0))
        p.addLine(to: CGPoint(x: r, y: h - fr))
        p.addQuadCurve(to: CGPoint(x: r + fr, y: h), control: CGPoint(x: r, y: h))
        p.addLine(to: CGPoint(x: min(w, r + fr), y: h))
        p.addLine(to: CGPoint(x: r, y: h))
        p.addLine(to: CGPoint(x: r, y: size.height))
        p.addLine(to: CGPoint(x: l, y: size.height))
        p.addLine(to: CGPoint(x: l, y: h))
        p.addLine(to: CGPoint(x: l - fr, y: h))
        p.addQuadCurve(to: CGPoint(x: l, y: h - fr), control: CGPoint(x: l, y: h))
        p.addLine(to: CGPoint(x: l, y: cb))
        p.addQuadCurve(to: CGPoint(x: l + cb, y: 0), control: CGPoint(x: l, y: 0))
        p.closeSubpath()
        CATransaction.begin(); CATransaction.setDisableActions(true)
        shape.frame = CGRect(origin: .zero, size: size); shape.path = p
        CATransaction.commit()
    }

    // First clip override, in priority order:
    //   1. open -g NotchFight.app --args --first <theme__clip|theme>[,<...>]
    //   2. NOTCH_FIGHT_FIRST env var (same comma-separated format)
    //   3. ~/.config/notch-fight/config.json  {"first": "<name>"} or {"first": ["<name>", ...]}
    func forcedFirst() -> [String] {
        func split(_ s: String) -> [String] { s.split(separator: ",").map { $0.trimmingCharacters(in: .whitespaces) }.filter { !$0.isEmpty } }
        let args = CommandLine.arguments
        if let i = args.firstIndex(of: "--first"), i + 1 < args.count { return split(args[i + 1]) }
        if let env = ProcessInfo.processInfo.environment["NOTCH_FIGHT_FIRST"], !env.isEmpty { return split(env) }
        let cfg = FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent(".config/notch-fight/config.json")
        guard let data = try? Data(contentsOf: cfg),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return [] }
        if let one = json["first"] as? String { return split(one) }
        return (json["first"] as? [String]) ?? []
    }

    func loadDirs(_ root: URL) -> [(String, [CGImage])] {
        let fm = FileManager.default
        return ((try? fm.contentsOfDirectory(atPath: root.path)) ?? []).sorted().compactMap { name in
            let dir = root.appendingPathComponent(name)
            let files = ((try? fm.contentsOfDirectory(atPath: dir.path)) ?? []).filter { $0.hasSuffix(".png") }.sorted()
            let imgs = files.compactMap { f -> CGImage? in
                guard let src = CGImageSourceCreateWithURL(dir.appendingPathComponent(f) as CFURL, nil) else { return nil }
                return CGImageSourceCreateImageAtIndex(src, 0, nil)
            }
            return imgs.isEmpty ? nil : (name, imgs)
        }
    }

    // Shuffle bag per theme: every clip plays once per round, never twice in a row.
    func nextClip(in t: String) -> [CGImage] {
        let clips = themes[t] ?? []
        if bags[t, default: []].isEmpty {
            var bag = Array(clips.indices).shuffled()
            if bag.count > 1, bag.last == lastClip[t] { bag.swapAt(0, bag.count - 1) }
            bags[t] = bag
        }
        let i = bags[t]!.removeLast(); lastClip[t] = i
        return clips[i]
    }

    // One visit = up to 2 clips of the current theme, then a transition to another theme.
    func enqueueVisit() {
        guard let clips = themes[theme], !clips.isEmpty else { return }
        for _ in 0..<min(2, clips.count) { queue.append(nextClip(in: theme)) }
        let others = themes.keys.filter { $0 != theme }
        if let next = others.randomElement() {
            if let tr = transitions["\(theme)__\(next)"] { queue.append(tr) }
            theme = next
        }
    }

    func tick() {
        if idx >= current.count {
            if queue.isEmpty { enqueueVisit() }
            guard !queue.isEmpty else { return }
            current = queue.removeFirst(); idx = 0
        }
        art.contents = current[idx]
        idx += 1
    }

    // Manual 60 fps frame animation: window frames don't take spring timing reliably.
    func animate(to target: CGFloat, duration: Double, spring: Bool, done: (() -> Void)? = nil) {
        animTimer?.invalidate()
        let start = win.frame.height - overlap, t0 = CACurrentMediaTime()
        animTimer = Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { [weak self] t in
            guard let self else { return }
            let p = min(1, (CACurrentMediaTime() - t0) / duration)
            let e = spring ? 1 - exp(-6 * p) * cos(9 * p) : p * p * (3 - 2 * p)
            self.win.setFrame(self.rect(height: max(0, start + (target - start) * CGFloat(p >= 1 ? 1 : e))), display: true)
            self.updateMask()
            if p >= 1 { t.invalidate(); done?() }
        }
    }

    var closing = false
    func close() {
        if closing { return }; closing = true
        animate(to: 0, duration: 0.3, spring: false) { NSApp.terminate(nil) }
    }
}

final class ClickView: NSView {
    var onClick: (() -> Void)?
    override func mouseDown(with e: NSEvent) { onClick?() }
    override func acceptsFirstMouse(for e: NSEvent?) -> Bool { true }
}

let app = NSApplication.shared
let d = App()
app.delegate = d
app.setActivationPolicy(.accessory)
// SIGTERM (pkill, e.g. from a Claude Code Stop hook) retracts into the notch before quitting.
signal(SIGTERM, SIG_IGN)
let term = DispatchSource.makeSignalSource(signal: SIGTERM, queue: .main)
term.setEventHandler { d.close() }
term.resume()
app.run()
