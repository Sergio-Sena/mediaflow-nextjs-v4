import { UploadStrategy, UploadResult, UploadProgress, UploadConfig } from './UploadStrategy'
import { mediaflowClient } from '@/lib/aws-client'

export class LargeFileUpload implements UploadStrategy {
  private config: UploadConfig = {
    timeout: 2 * 60 * 60 * 1000,  // 2 horas
    retries: 5,
    progressInterval: 500          // 0.5 segundos (mais responsivo)
  }

  async upload(
    file: File, 
    filename: string, 
    onProgress?: (progress: UploadProgress) => void
  ): Promise<UploadResult> {
    
    console.log(`LargeFileUpload: ${filename} (${Math.round(file.size / 1024 / 1024)}MB)`)
    
    // Upload único para arquivos grandes (>100MB)
    console.log('LargeFileUpload: Presigned URL com timeout estendido')
    
    try {
      // Upload único para arquivos 50-200MB
      const urlData = await mediaflowClient.getUploadUrl(filename, file.type, file.size)
      if (!urlData.success) throw new Error(urlData.message)
      
      const result = await this.uploadWithExtendedTimeout(file, urlData.uploadUrl, onProgress)
      
      return {
        success: true,
        url: `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${urlData.key}`
      }
      
    } catch (error) {
      console.error('LargeFileUpload error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed'
      }
    }
  }

  private uploadWithExtendedTimeout(
    file: File, 
    uploadUrl: string, 
    onProgress?: (progress: UploadProgress) => void
  ): Promise<void> {
    
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      
      // Timeout estendido para arquivos grandes
      xhr.timeout = this.config.timeout
      
      // Progress mais frequente para arquivos grandes
      let lastProgressTime = 0
      xhr.upload.addEventListener('progress', (e) => {
        const now = Date.now()
        if (e.lengthComputable && onProgress && (now - lastProgressTime) >= this.config.progressInterval) {
          lastProgressTime = now
          onProgress({
            loaded: e.loaded,
            total: e.total,
            percentage: Math.round((e.loaded / e.total) * 100)
          })
        }
      })
      
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve()
        } else {
          reject(new Error(`Upload failed: ${xhr.status}`))
        }
      })
      
      xhr.addEventListener('error', () => reject(new Error('Network error')))
      xhr.addEventListener('timeout', () => reject(new Error('Upload timeout (2h limit)')))
      
      xhr.open('PUT', uploadUrl)
      xhr.setRequestHeader('Content-Type', file.type)
      xhr.send(file)
    })
  }
}