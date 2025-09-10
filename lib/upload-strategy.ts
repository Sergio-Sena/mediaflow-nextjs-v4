// Estratégia de upload baseada no tamanho do arquivo

export interface UploadStrategy {
  method: 'proxy' | 'presigned' | 'multipart'
  maxSize: number
  description: string
}

export function getUploadStrategy(fileSize: number): UploadStrategy {
  const MB = 1024 * 1024
  
  if (fileSize <= 50 * MB) {
    return {
      method: 'proxy',
      maxSize: 50 * MB,
      description: 'Upload via Vercel API (seguro, sem CORS)'
    }
  } else if (fileSize <= 100 * MB) {
    return {
      method: 'presigned',
      maxSize: 100 * MB,
      description: 'Upload direto S3 com presigned URL'
    }
  } else {
    return {
      method: 'multipart',
      maxSize: 5 * 1024 * 1024 * 1024 * 1024, // 5TB
      description: 'Multipart upload para arquivos grandes'
    }
  }
}

export const UPLOAD_LIMITS = {
  VERCEL_PROXY: 50 * 1024 * 1024,      // 50MB
  PRESIGNED_URL: 100 * 1024 * 1024,    // 100MB
  MULTIPART_MIN: 5 * 1024 * 1024,      // 5MB (mínimo S3)
  S3_MAX: 5 * 1024 * 1024 * 1024 * 1024 // 5TB
}