// Estratégia de upload baseada no tamanho do arquivo

export interface UploadStrategy {
  method: 'proxy' | 'presigned' | 'multipart'
  maxSize: number
  description: string
}

export function getUploadStrategy(fileSize: number): UploadStrategy {
  const MB = 1024 * 1024
  
  // v4.0: Upload único otimizado (sem multipart)
  if (fileSize <= 100 * MB) {
    return {
      method: 'proxy',
      maxSize: 100 * MB,
      description: 'Upload via proxy (rápido para pequenos)'
    }
  } else {
    return {
      method: 'presigned',
      maxSize: 5 * 1024 * 1024 * 1024, // 5GB
      description: 'Upload direto S3 (sem limite para grandes)'
    }
  }
}

export const UPLOAD_LIMITS = {
  PRESIGNED_URL: 100 * 1024 * 1024,    // 100MB
  PROXY_MAX: 5 * 1024 * 1024 * 1024,   // 5GB
  TIMEOUT: 2 * 60 * 60 * 1000          // 2 horas
}