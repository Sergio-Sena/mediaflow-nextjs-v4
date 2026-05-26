/**
 * Sanitiza nome de arquivo para S3
 * Remove sites, resoluções, stopwords, caracteres especiais
 * Trunca em 40 chars no limite de palavra
 */

const STOPWORDS = new Set([
  'Uma','Para','que','Sua','Seu','Enquanto','Depois','Dela','Meu',
  'Minha','com','Com','the','The','and','And','with','With','from',
  'From','her','Her','his','His','she','She','Ela','Ele','Num','nos',
  'Das','Dos','Nas','Nos','Est','Voc','Sabe','Esse','Essa','Este',
  'Em','De','Do','Da','No','Na','Os','As','Se','Ao','Eu','Me','Te',
  'Um','Uns','Umas','Pelo','Pela','Pra','Pro','Que','Isso','Aqui'
])

const MAX_CHARS = 40

export function sanitizeFilename(filename: string, folderName?: string): string {
  const lastDot = filename.lastIndexOf('.')
  const name = lastDot > 0 ? filename.substring(0, lastDot) : filename
  const ext = lastDot > 0 ? filename.substring(lastDot).toLowerCase() : ''

  let base = name

  // Remove sites
  base = base.replace(/EPORNER[\s._]*COM[\s_]*-?[\s_]*/gi, '')
  base = base.replace(/[\s_]*-?[\s_]*(Pornhub[\s_]*com|Pornhub\.com|Pornhub)/gi, '')
  base = base.replace(/[\s_]*-?[\s_]*Por$/i, '')

  // Remove hash codes
  base = base.replace(/^\[?[a-zA-Z0-9]{8,15}\]?[\s_-]*/g, '')

  // Remove resolutions/codecs
  base = base.replace(/[\s_(-]*(1920x1080|1080p?|720p?|480p?|4K|HEVC|x265|x264|XXX|PRT[\s_]*\d*)[\s_)]*/gi, '')

  // Remove brackets but keep content
  base = base.replace(/\[NO WM\.?\]/gi, '')
  base = base.replace(/\[([^\]]+)\]/g, '$1')
  base = base.replace(/\(([^)]+)\)/g, '$1')

  // Remove production prefixes
  base = base.replace(/^(OnlyFans[\s_]*\d{4}|REALITY[\s_]*KINGS|MOFOS|BLACKED|WOWGIRLS|Lifeselector|GIRLSWAY)[\s_]*-?[\s_]*/i, '')

  // Remove folder name words (redundant)
  if (folderName) {
    const folderWords = folderName.toLowerCase().split(/[_\s]+/)
    for (const fw of folderWords) {
      if (fw.length > 3) {
        base = base.replace(new RegExp(`\\b${fw}\\b`, 'gi'), '')
      }
    }
  }

  // Normalize: remove accents, replace special chars
  base = base
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-zA-Z0-9]/g, '_')

  // Split into words, remove stopwords and single chars
  const parts = base.split('_').filter(p => p && p.length > 1 && !STOPWORDS.has(p))

  // Build result at word boundary
  let result = ''
  for (const p of parts) {
    const candidate = result ? result + '_' + p : p
    if (candidate.length <= MAX_CHARS) {
      result = candidate
    } else {
      break
    }
  }

  // Fallback
  if (!result || result.length < 5) {
    result = parts.join('_').substring(0, MAX_CHARS)
  }
  if (!result) {
    result = `file_${Date.now()}`
  }

  return result + ext
}
