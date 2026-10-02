// Notch Fight inside Claude Code: while a turn runs, the band above the prompt plays the clips the
// notch app plays (same build/clips, same config.json selection, theme-to-theme transitions).
// display "image" shows the real PNG frames (kitty graphics protocol: kitty, Ghostty) and falls back
// to "raster" where the terminal draws the Image's alt; "raster" packs each frame into coloured
// quadrant-block cells, 2x2 pixels each (scripts/mod_cells.py), which every terminal shows.
// The clip sits at the right end of the band.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Mode } from '../types'

const isPlaying = atom({ plugin: 'notch-fight', key: 'isPlaying' } as const, false)
const mode = atom({ plugin: 'notch-fight', key: 'mode' } as const, 'image' as Mode)

const FPS = 20
const MAX_PER_VISIT = 2                   // clips in one theme before moving on, like the app
const KEY = 'clip'

type Item = { name: string; dir: string; count: number }
type Config = { newClips?: string; enabled?: string[]; disabled?: string[]; first?: string | string[] }

const themeOf = (name: string) => name.split('_')[0]
const pad = (n: number) => String(n).padStart(3, '0')

// ---- playback state (module variables: a reload starts over) ----
let rows = 10
let columns = 58
let repo = ''
let root = ''
let site: string | undefined                            // the band's requestId, once it drew us
let allowed: string[] = []
let remaining: string[] = []
let forced: string[] = []
let theme = ''
let last = ''
let visits = 0
let queue: Item[] = []
let item: Item | null = null
let frame = 0
let png = ''                                            // the frame on screen, image mode
let cells = ''                                          // the frame on screen, raster mode
let packed: Uint8Array | null = null                    // the current item's raster frames
let stop: (() => void) | null = null
let isBusy = false
let hasWarned = false

async function load($: EngineInterface) {
  const home = (await $.env.get('HOME')) ?? ''
  root = repo
  for (const up of ['/..', '/../..']) {                   // this plugin is mod/ in the checkout
    if (!root && (await $.fs.exists(`${$.plugin.root}${up}/src/build.py`))) root = `${$.plugin.root}${up}`
  }
  if (!root) throw new Error('cannot find the notch-fight checkout: set the "repo" option')
  const all = (await $.fs.list(`${root}/build/clips`)).filter(d => d.kind === 'dir' && !d.name.startsWith('.')).map(d => d.name)
  let cfg: Config = {}
  try { cfg = JSON.parse(await $.fs.read(`${home}/.config/notch-fight/config.json`)) } catch { /* no config: defaults */ }
  const enabled = new Set(cfg.enabled ?? []), disabled = new Set(cfg.disabled ?? [])
  const off = new Set<string>()
  for (const c of all) if (await $.fs.exists(`${root}/build/clips/${c}/.default-off`)) off.add(c)
  allowed = cfg.newClips === 'disabled' ? all.filter(c => enabled.has(c))
    : all.filter(c => (off.has(c) ? enabled.has(c) : !disabled.has(c)))
  remaining = [...allowed]
  const first = typeof cfg.first === 'string' ? cfg.first.split(',') : cfg.first ?? []
  forced = first.map(n => n.trim()).filter(Boolean).map(n => (all.includes(n) ? n : pickOf(all.filter(c => themeOf(c) === n))))
    .filter((n): n is string => !!n)
}

const pickOf = (list: string[]) => (list.length ? list[Math.floor(Math.random() * list.length)] : undefined)

function pickNext(): string | undefined {
  if (remaining.length === 0) remaining = [...allowed]
  if (remaining.length === 0) return undefined
  let pool = remaining.filter(c => c !== last)
  if (pool.length === 0) pool = remaining
  const same = pool.filter(c => themeOf(c) === theme), other = pool.filter(c => themeOf(c) !== theme)
  if (same.length && (visits < MAX_PER_VISIT || other.length === 0)) return pickOf(same)
  return pickOf(other.length ? other : same)
}

async function itemOf($: EngineInterface, dir: string, name: string): Promise<Item | null> {
  try {
    const count = (await $.fs.list(dir)).filter(f => f.name.endsWith('.png')).length
    return count ? { name, dir, count } : null
  } catch { return null }
}

async function enqueue($: EngineInterface, name: string) {
  const t = themeOf(name)
  if (theme && t !== theme) {
    const tr = await itemOf($, `${root}/build/transitions/${theme}__${t}`, `t_${theme}__${t}`)
    if (tr) queue.push(tr)
  }
  const clip = await itemOf($, `${root}/build/clips/${name}`, name)
  if (clip) queue.push(clip)
  visits = t === theme ? visits + 1 : 1
  theme = t; last = name
  remaining = remaining.filter(c => c !== name)
}

async function loadPacked($: EngineInterface, it: Item) {
  const out = `${root}/build/mod/${it.name}.${columns}x${rows}.q.cells`
  const src = await $.fs.stat(`${it.dir}/000.png`)
  const have = (await $.fs.exists(out)) && (await $.fs.stat(out)).mtimeMs >= src.mtimeMs
  if (!have) {
    const r = await $.process.run(['python3', `${root}/scripts/mod_cells.py`, it.dir, String(columns), String(rows), out], { timeoutMs: 120000 })
    if (r.exitCode !== 0) throw new Error(`mod_cells.py: ${r.stderr.slice(0, 200)}`)
  }
  packed = Uint8Array.fromBase64((await $.fs.read(out, { as: 'bytes' })).base64)
}

function cellsOf(i: number) {
  const n = columns * rows, p = packed!, words = new Uint32Array(n * 3)
  for (let k = 0, b = i * n * 8; k < n; k++, b += 8) {     // a quadrant character, its fg, its bg
    words[k * 3] = p[b] | (p[b + 1] << 8)
    words[k * 3 + 1] = (p[b + 2] << 16) | (p[b + 3] << 8) | p[b + 4]
    words[k * 3 + 2] = (p[b + 5] << 16) | (p[b + 6] << 8) | p[b + 7]
  }
  return new Uint8Array(words.buffer).toBase64()
}

// One frame: move to the next item when this one is done, read the frame, swap it into the band.
async function tick($: EngineInterface) {
  if (isBusy) return                                     // a slow read or a raster pack: skip, never pile up
  isBusy = true
  try {
    const m = await read($, mode)
    if (!item || frame >= item.count) {
      if (!queue.length) {
        const name = forced.shift() ?? pickNext()
        if (!name) return
        await enqueue($, name)
      }
      item = queue.shift() ?? null; frame = 0
      if (!item) return
      if (m === 'raster') await loadPacked($, item)
    }
    if (m === 'raster') {
      if (!packed) await loadPacked($, item)
      cells = cellsOf(frame)
      if (site) await $.ui.blit({ requestId: site, key: KEY, cells })
    } else {
      png = (await $.fs.read(`${item.dir}/${pad(frame)}.png`, { as: 'bytes' })).base64
      if (site) {
        const r = await $.ui.blit({ requestId: site, key: KEY, source: { png } })
        if (r.deny && /alt|placeholder|cannot/i.test(r.deny)) {     // this terminal shows no pictures
          if (!hasWarned) { hasWarned = true; $.ui.toast('Notch Fight: no inline images in this terminal, drawing cells instead') }
          packed = null
          await loadPacked($, item); cells = cellsOf(frame)
          await update($, mode, () => 'raster')
        }
      }
    }
    frame += 1
  } finally { isBusy = false }
}


export const register: Register = (on, options) => {
  rows = Math.max(4, Math.min(14, Math.round(Number(options.rows) || 10)))
  columns = Math.round((rows * 2 * 185) / 64)             // the clip is 185x64; a cell is twice as tall as wide
  repo = String(options.repo || '')

  on('session.start', async ($, e, next) => {
    await update($, mode, () => (options.display === 'raster' ? 'raster' : 'image'))
    await update($, isPlaying, () => false)
    return next(e)
  })

  on('turn.start', async ($, e, next) => {
    try {
      if (!root) await load($)
      if (allowed.length || forced.length) {
        await tick($)                                      // the first frame, before the band draws
        await update($, isPlaying, () => true)
        stop?.()
        stop = $.clock.every(1000 / FPS, () => { void tick($).catch(err => $.ui.log(`notch-fight: ${err}`)) })
      }
    } catch (err) { $.ui.log(`notch-fight: ${err}`) }
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    stop?.(); stop = null
    await update($, isPlaying, () => false)
    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.surface !== 'terminal' || !(await read($, isPlaying)) || e.props.hasSurvey || e.props.bodyColumns < columns) return next(e)
    const m = await read($, mode)
    if (m === 'image' ? !png : !cells) return next(e)
    site = e.requestId
    const { Box, Image, Raster } = $.ui.resolve(e)
    return (
      <Box width={e.props.bodyColumns} justifyContent="flex-end">
        {m === 'image'
          ? <Image key={KEY} source={{ png }} columns={columns} rows={rows} alt="Notch Fight (this terminal shows no images)" />
          : <Raster key={KEY} columns={columns} rows={rows} cells={cells} />}
      </Box>
    )
  })
}
