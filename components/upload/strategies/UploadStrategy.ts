// Interface comum para estratégias de upload
export interface UploadResult {
  success: boolean
  url?: string
  error?: string
}

export interface UploadProgress {
  loaded: number
  total: number
  percentage: number
}

export interface UploadStrategy {
  upload(file: File, filename: string, onProgress?: (progress: UploadProgress) => void): Promise<UploadResult>
}

export interface UploadConfig {
  timeout: number
  retries: number
  progressInterval: number
}