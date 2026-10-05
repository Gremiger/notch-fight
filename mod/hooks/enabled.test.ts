import { expect, test } from 'claude-code/testing'

// A plugin beneath notch-fight reports the display mode it left in the session's state.
const probe = {
  name: 'probe',
  tier: 'append',
  register(on) {
    on('session.start', async ($, e) => ({ cwd: String((await $.state.get({ plugin: 'notch-fight', key: 'mode' })).value ?? 'unset') }))
  },
} as const
const START = { cwd: '/tmp', surface: 'terminal', isInteractive: true } as const

test('on: session.start picks the display', { plugins: [probe], options: { display: 'raster' } }, async $ => {
  expect((await $.session.start(START)).cwd).toBe('raster')
})

test('off in /config: no hooks run', { plugins: [probe], options: { enabled: false, display: 'raster' } }, async $ => {
  expect((await $.session.start(START)).cwd).toBe('unset')
})
