import AppKit
import QuartzCore

// The light a clip spills below the panel (config "glow": "soft" / "strong"; off by default): a window of
// its own under the panel that takes no clicks, holding a radial gradient in the colour of the frame on
// screen (build.py writes one colour per frame, clips/<clip>/glow), eased from frame to frame. It fades in
// once the panel is down and out before it goes up.
final class Glow {
    let win: NSPanel
    let grad = CAGradientLayer()
    var color = SIMD3<Double>(0, 0, 0)
    var strength: Double = 0.35

    init() {
        win = NSPanel(contentRect: .zero, styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: true)
        win.level = .screenSaver
        win.backgroundColor = .clear
        win.isOpaque = false
        win.hasShadow = false
        win.ignoresMouseEvents = true
        win.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary, .ignoresCycle]
        let v = NSView(); v.wantsLayer = true; v.layer!.addSublayer(grad); win.contentView = v
        grad.type = .radial
        grad.startPoint = CGPoint(x: 0.5, y: 1)                         // the centre: top middle, under the panel
        grad.endPoint = CGPoint(x: 1, y: 0)                             // reaching the sides and the bottom
        grad.locations = [0, 0.45, 1]
        grad.opacity = 0
        grad.actions = ["colors": NSNull(), "bounds": NSNull(), "position": NSNull()]
    }

    /// Strength for a config value: "soft" (or true), "strong"; nil when off.
    static func strength(_ cfg: Any?) -> Double? {
        switch cfg {
        case let s as String where s == "strong": return 0.6
        case let s as String where s == "soft": return 0.35
        case let b as Bool where b: return 0.35
        default: return nil
        }
    }

    /// Lays it under `panel`: centred on x, hanging from `top`, w×h.
    func place(below panel: NSWindow, centerX x: CGFloat, top: CGFloat, width w: CGFloat, height h: CGFloat) {
        win.setFrame(NSRect(x: x - w / 2, y: top - h, width: w, height: h), display: false)
        grad.frame = CGRect(x: 0, y: 0, width: w, height: h)
        win.order(.below, relativeTo: panel.windowNumber)
    }

    func fade(to opacity: Float, duration: Double, done: (() -> Void)? = nil) {
        CATransaction.begin()
        CATransaction.setCompletionBlock(done)
        let a = CABasicAnimation(keyPath: "opacity")
        a.fromValue = grad.presentation()?.opacity ?? grad.opacity; a.toValue = opacity; a.duration = duration
        grad.add(a, forKey: "fade"); grad.opacity = opacity
        CATransaction.commit()
    }

    /// One step towards this frame's colour ("rrggbb"); called every frame while the panel is out.
    func step(toward hex: SIMD3<Double>?) {
        if let hex { color += (hex - color) * 0.15 }
        let c = NSColor(srgbRed: color.x, green: color.y, blue: color.z, alpha: 1)
        CATransaction.begin(); CATransaction.setDisableActions(true)
        grad.colors = [c.withAlphaComponent(strength).cgColor, c.withAlphaComponent(strength * 0.35).cgColor,
                       c.withAlphaComponent(0).cgColor]
        CATransaction.commit()
    }

    static func load(_ dir: URL) -> [SIMD3<Double>] {
        let raw = (try? String(contentsOf: dir.appendingPathComponent("glow"), encoding: .utf8)) ?? ""
        return raw.split(separator: "\n").compactMap { line in
            guard line.count == 6, let v = UInt32(line, radix: 16) else { return nil }
            return SIMD3(Double(v >> 16 & 255), Double(v >> 8 & 255), Double(v & 255)) / 255
        }
    }
}
