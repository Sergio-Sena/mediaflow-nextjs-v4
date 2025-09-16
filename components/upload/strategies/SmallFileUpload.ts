import { UploadStrategy, UploadResult, UploadProgress, UploadConfig } from './UploadStrategy'
import { mediaflowClient } from '@/lib/aws-client'

export class SmallFileUpload implements UploadStrategy {
  private config: UploadConfig = {
    timeout: 30 * 60 * 1000,  // 30 minutos
    retries: 3,
    progressInterval: 1000     // 1 segundo
  }

  async upload(
    file: File, 
    filename: string, 
    onProgress?: (progress: UploadProgress) => void
  ): Promise<UploadResult> {
    
    console.log(`SmallFileUpload: ${filename} (${Math.round(file.size / 1024 / 1024)}MB)`)
    
    try {
      // Obter presigned URL
      const urlData = await mediaflowClient.getUploadUrl(filename, file.type, file.size)
      if (!urlData.success) throw new Error(urlData.message)
      
      // Upload com timeout otimizado para arquivos pequenos
      const result = await this.uploadWithProgress(file, urlData.uploadUrl, onProgress)
      
      return {
        success: true,
        url: `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${urlData.key}`
      }
      
    } catch (error) {
      console.error('SmallFileUpload error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed'
      }
    }
  }

  private uploadWithProgress(
    file: File, 
    uploadUrl: string, 
    onProgress?: (progress: UploadProgress) => void
  ): Promise<void> {
    
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      
      // Timeout otimizado para arquivos pequenos
      xhr.timeout = this.config.timeout
      
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable && onProgress) {
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
      xhr.addEventListener('timeout', () => reject(new Error('Upload timeout')))
      
      xhr.open('PUT', uploadUrl)
      xhr.setRequestHeader('Content-Type', file.type)
      xhr.send(file)
    })
  }
}