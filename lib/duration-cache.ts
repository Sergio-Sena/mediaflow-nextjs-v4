const CACHE_KEY = 'midiaflow_duration_cache'

type DurationMap = Record<string, number>

export const durationCache = {
  getAll: (): DurationMap => {
    try {
      return JSON.parse(localStorage.getItem(CACHE_KEY) || '{}')
    } catch {
      return {}
    }
  },

  get: (fileKey: string): number | null => {
    try {
      const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}')
      return fileKey in cache ? cache[fileKey] : null
    } catch {
      return null
    }
  },

  set: (fileKey: string, duration: number) => {
    try {
      const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}')
      cache[fileKey] = duration
      localStorage.setItem(CACHE_KEY, JSON.stringify(cache))
    } catch {}
  },

  setMany: (entries: DurationMap) => {
    try {
      const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}')
      Object.assign(cache, entries)
      localStorage.setItem(CACHE_KEY, JSON.stringify(cache))
    } catch {}
  },

  delete: (fileKey: string) => {
    try {
      const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}')
      delete cache[fileKey]
      localStorage.setItem(CACHE_KEY, JSON.stringify(cache))
    } catch {}
  }
}
