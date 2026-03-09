// Cache helper for files
const CACHE_KEY = 'midiaflow_files_cache'
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutos

export const filesCache = {
  get: () => {
    try {
      const cached = localStorage.getItem(CACHE_KEY)
      if (!cached) return null
      
      const { data, timestamp } = JSON.parse(cached)
      const now = Date.now()
      
      if (now - timestamp > CACHE_DURATION) {
        localStorage.removeItem(CACHE_KEY)
        return null
      }
      
      return data
    } catch {
      return null
    }
  },
  
  set: (data: any) => {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({
        data,
        timestamp: Date.now()
      }))
    } catch {
      // Ignore cache errors
    }
  },
  
  clear: () => {
    localStorage.removeItem(CACHE_KEY)
  }
}
