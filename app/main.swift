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
    var clips: [String: [CGImage]] = [:]            // "<theme>__<clip>" -> frames
    var transitions: [String: [CGImage]] = [:]
    var queue: [[CGImage]] = []
    var theme = ""
    // Per-launch shuffle bag: forced clips first, then every other clip in random order;
    // no clip repeats until all have played, then a new round starts.
    var remaining: [String] = []
    var lastPlayed = ""
    var visitCount = 0                                 // clips played in the current theme visit
    let maxPerVisit = 2
    var current: [CGImage] = []
    var idx = 0
    var playTimer: Timer?
    var animTimer: Timer?
    let clipH: CGFloat = 64, corner: CGFloat = 12
    // overlap: rises into the notch to cover its rounded bottom corners.
    // fillet: concave flare where the panel meets the notch's bottom edge. 0 = panel is exactly
    // notch-wide (the flare showed up as a protruding ledge on some Macs). Config: "fillet".
    let overlap: CGFloat = 10, fillet: CGFloat = CGFloat(App.cfgNumber("fillet") ?? 0)
    // stretch: fill the real notch width with the art (true) or keep square pixels, centred (false). Config: "stretch".
    let stretch: Bool = (App.config["stretch"] as? Bool) ?? true

    // ~/.config/notch-fight/config.json, read once. Keys: "first", "fillet", "stretch", "widthTweak".
    static let config: [String: Any] = {
        let url = FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent(".config/notch-fight/config.json")
        guard let data = try? Data(contentsOf: url),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return [:] }
        return json
    }()
    static func cfgNumber(_ key: String) -> Double? { (config[key] as? NSNumber)?.doubleValue }
    let shape = CAShapeLayer()
    var root: CALayer!
    var notchW: CGFloat = 185, notchH: CGFloat = 32, notchMidX: CGFloat = 0, screen: NSScreen!

    // Per-model width correction (pt): the auxiliary areas can report a notch slightly wider than the
    // real one. Keyed by `hw.model`; add an entry when a Mac's panel visibly overhangs the notch.
    static let notchWidthTweak: [String: CGFloat] = ["Mac14,2": -1]
    static let hwModel: String = {
        var n = 0; sysctlbyname("hw.model", nil, &n, nil, 0)
        var b = [CChar](repeating: 0, count: n); sysctlbyname("hw.model", &b, &n, nil, 0)
        return String(cString: b)
    }()

    func applicationDidFinishLaunching(_ n: Notification) {
        screen = NSScreen.screens.first { $0.auxiliaryTopLeftArea != nil } ?? NSScreen.main!
        let f = screen.frame
        notchMidX = f.midX
        if let l = screen.auxiliaryTopLeftArea, let r = screen.auxiliaryTopRightArea {
            // The notch is not always centred on the screen: anchor to its real edges.
            notchW = r.minX - l.maxX
            notchMidX = (l.maxX + r.minX) / 2
            notchH = screen.safeAreaInsets.top
            notchW += CGFloat(Self.cfgNumber("widthTweak") ?? Double(Self.notchWidthTweak[Self.hwModel] ?? 0))
        }
        let res = Bundle.main.resourceURL!
        clips = Dictionary(uniqueKeysWithValues: loadDirs(res.appendingPathComponent("clips")))
        transitions = Dictionary(uniqueKeysWithValues: loadDirs(res.appendingPathComponent("transitions")))
        remaining = Array(clips.keys)
        // Forced clips play first, in order (and count as played for this round).
        for first in forcedFirst() {
            let name = clips[first] != nil ? first
                : (remaining.filter { themeOf($0) == first }.randomElement() ?? clips.keys.filter { themeOf($0) == first }.randomElement())
            guard let name else {
                NSLog("NotchFight: unknown first clip/theme '\(first)'. Known: \(clips.keys.sorted())"); continue
            }
            enqueue(name)
        }
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
        // Art is authored at a fixed W×H canvas (185×64, MacBookPro18,3's notch width) with effects
        // drawn edge-to-edge. `notchW` varies per Mac (e.g. 209pt on a MacBook Air M2), so `.resizeAspect`
        // would center the unscaled art and leave dead black margins instead of reaching the real notch
        // edges. `.resize` stretches horizontally only — clipH always equals the art's native height, so
        // the vertical scale factor is always 1 and no content is ever cropped.
        // Config "stretch": false keeps the art at its native width, centred (the black margins blend in).
        art.contentsGravity = stretch ? .resize : .resizeAspect
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
        return NSRect(x: notchMidX - notchW / 2 - fillet, y: f.maxY - notchH - h,
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
        let json = Self.config
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

    func themeOf(_ name: String) -> String { String(name.split(separator: "_", maxSplits: 1).first ?? "") }

    // Stay in the current theme for up to maxPerVisit clips, then move to another theme;
    // always drawing from the clips not yet played this round.
    func pickNext() -> String? {
        if remaining.isEmpty { remaining = Array(clips.keys) }       // new round
        var pool = remaining.filter { $0 != lastPlayed }
        if pool.isEmpty { pool = remaining }
        let same = pool.filter { themeOf($0) == theme }
        let other = pool.filter { themeOf($0) != theme }
        if !same.isEmpty && (visitCount < maxPerVisit || other.isEmpty) { return same.randomElement() }
        return (other.isEmpty ? same : other).randomElement()
    }

    func enqueue(_ name: String) {
        guard let frames = clips[name] else { return }
        let t = themeOf(name)
        if !theme.isEmpty && t != theme, let tr = transitions["\(theme)__\(t)"] { queue.append(tr) }
        visitCount = (t == theme) ? visitCount + 1 : 1
        theme = t; lastPlayed = name
        remaining.removeAll { $0 == name }
        queue.append(frames)
    }

    func tick() {
        if idx >= current.count {
            if queue.isEmpty, let next = pickNext() { enqueue(next) }
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
