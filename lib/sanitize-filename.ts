/**
 * Sanitiza nome de arquivo para S3
 * Remove sites, resoluções, caracteres especiais
 * Trunca em 45 chars no limite de palavra
 */
export function sanitizeFilename(filename: string): string {
  const lastDot = filename.lastIndexOf('.')
  const name = lastDot > 0 ? filename.substring(0, lastDot) : filename
  const ext = lastDot > 0 ? filename.substring(lastDot).toLowerCase() : ''

  let base = name

  // Remove sites
  base = base.replace(/EPORNER[\s._]*COM[\s_]*-?[\s_]*/gi, '')
  base = base.replace(/[\s_]*-?[\s_]*(Pornhub[\s_]*com|Pornhub\.com|Pornhub)/gi, '')
  base = base.replace(/[\s_]*-?[\s_]*Por$/i, '')

  // Remove hash codes (ex: [N9FKXd0AyEN])
  base = base.replace(/^\[?[a-zA-Z0-9]{8,15}\]?[\s_-]*/g, '')

  // Remove resolutions/codecs
  base = base.replace(/[\s_(-]*(1920x1080|1080p?|720p?|480p?|HEVC|x265|x264|XXX)[\s_)]*/gi, '')

  // Remove brackets but keep content
  base = base.replace(/\[NO WM\.?\]/gi, '')
  base = base.replace(/\[([^\]]+)\]/g, '$1')
  base = base.replace(/\(([^)]+)\)/g, '$1')

  // Remove production prefixes
  base = base.replace(/^(OnlyFans[\s_]*\d{4}|REALITY[\s_]*KINGS|MOFOS|BLACKED|WOWGIRLS|Lifeselector|GIRLSWAY)[\s_]*-?[\s_]*/i, '')

  // Normalize: remove accents, replace special chars
  base = base
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-zA-Z0-9]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '')

  // Truncate to 45 chars at word boundary
  if (base.length > 45) {
    base = base.substring(0, 45).replace(/_$/, '')
  }

  // Fallback
  const finalName = base || `file_${Date.now()}`

  return finalName + ext
}
