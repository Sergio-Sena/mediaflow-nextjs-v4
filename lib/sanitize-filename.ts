/**
 * Sanitiza nome de arquivo removendo caracteres não-ASCII e especiais
 * Mantém apenas: a-z, A-Z, 0-9, -, _, ., espaços
 */
export function sanitizeFilename(filename: string): string {
  // Separar nome e extensão
  const lastDot = filename.lastIndexOf('.')
  const name = lastDot > 0 ? filename.substring(0, lastDot) : filename
  const ext = lastDot > 0 ? filename.substring(lastDot) : ''
  
  // Remover acentos e caracteres especiais
  const sanitized = name
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove acentos
    .replace(/[^a-zA-Z0-9\s\-_]/g, '') // Remove caracteres especiais
    .replace(/\s+/g, '_') // Substitui espaços por underscore
    .replace(/_+/g, '_') // Remove underscores duplicados
    .replace(/^_|_$/g, '') // Remove underscores no início/fim
  
  return sanitized + ext.toLowerCase()
}
