/**
 * Sanitiza nome de arquivo para S3
 * Substitui caracteres especiais por underscore (não remove)
 * Mantém: a-z, A-Z, 0-9, -, _, .
 */
export function sanitizeFilename(filename: string): string {
  // Separar nome e extensão
  const lastDot = filename.lastIndexOf('.')
  const name = lastDot > 0 ? filename.substring(0, lastDot) : filename
  const ext = lastDot > 0 ? filename.substring(lastDot) : ''
  
  const sanitized = name
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')      // Remove acentos
    .replace(/[^a-zA-Z0-9\s\-_]/g, '_')  // Substitui especiais por _
    .replace(/\s+/g, '_')                  // Espaços → underscore
    .replace(/_+/g, '_')                   // Remove underscores duplicados
    .replace(/^_|_$/g, '')                 // Remove _ no início/fim
    .substring(0, 100)                     // Limita tamanho
  
  // Se ficou vazio, usar timestamp
  const finalName = sanitized || `file_${Date.now()}`
  
  return finalName + ext.toLowerCase()
}
