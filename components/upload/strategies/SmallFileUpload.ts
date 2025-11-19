import { UploadStrategy, UploadResult, UploadProgress, UploadConfig } from './UploadStrategy'
import { mediaflowClient } from '@/lib/aws-client'

export class SmallFileUpload implements UploadStrategy {
  private config: UploadConfig = {
    timeout: 5 * 60 * 1000,   // 5 minutos (reduzido)
    retries: 5,               // Aumentado para 5
    progressInterval: 500     // 500ms (mais responsivo)
  }

  async upload(
    file: File, 
    filename: string, 
    onProgress?: (progress: UploadProgress) => void
  ): Promise<UploadResult> {
    
    console.log(`🚀 SmallFileUpload SIMPLE: ${filename} (${Math.round(file.size / 1024 / 1024)}MB)`)
    
    try {
      // Usar Next.js API com CORS habilitado
      const urlResponse = await fetch('/api/upload/presigned-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: filename,
          contentType: file.type,
          fileSize: file.size
        })
      })

      const urlData = await urlResponse.json()
      
      if (!urlData.success) {
        throw new Error(urlData.error || 'Falha ao obter URL')
      }

      console.log(`✅ Got presigned URL: ${filename}`)

      // Upload direto - método que funciona
      await this.simpleUpload(file, urlData.uploadUrl, onProgress)
      
      console.log(`✅ SmallFileUpload SUCCESS: ${filename}`)
      return {
        success: true,
        url: `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${urlData.key}`
      }
      
    } catch (error) {
      console.error(`❌ SmallFileUpload failed:`, error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed'
      }
    }
  }



  private simpleUpload(
    file: File, 
    uploadUrl: string, 
    onProgress?: (progress: UploadProgress) => void
  ): Promise<void> {
    
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      
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
          console.error(`❌ Upload failed: ${xhr.status} ${xhr.statusText}`)
          reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`))
        }
      })
      
      xhr.addEventListener('error', () => {
        reject(new Error('Network error'))
      })
      
      xhr.open('PUT', uploadUrl)
      xhr.setRequestHeader('Content-Type', file.type)
      xhr.send(file)
    })
  }
}
