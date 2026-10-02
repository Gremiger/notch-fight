export type Mode = 'image' | 'raster'

declare module 'claude-code' {
  interface PluginState {
    'notch-fight': { isPlaying: boolean; mode: Mode }
  }
}
