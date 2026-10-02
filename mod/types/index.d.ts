export type Mode = 'image' | 'raster' | 'sextant' | 'octant'

declare module 'claude-code' {
  interface PluginState {
    'notch-fight': { isPlaying: boolean; mode: Mode; tick: number }
  }
}
