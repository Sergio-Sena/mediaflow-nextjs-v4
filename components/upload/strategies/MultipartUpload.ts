import { UploadStrategy, UploadResult, UploadProgress } from './UploadStrategy'
import { mediaflowClient } from '@/lib/aws-client'

export class MultipartUpload implements UploadStrategy {
  private readonly CHUNK_SIZE = 5 * 1024 * 1024 // 5MB chunks
  private readonly MAX_CONCURRENT = 3 // 3 uploads paralelos

  async upload(
    file: File, 
    filename: string, 
    onProgress?: (progress: UploadProgress) => void
  ): Promise<UploadResult> {
    
    console.log(`MultipartUpload: ${filename} (${Math.round(file.size / 1024 / 1024)}MB)`)
    
    try {
      // Dividir arquivo em chunks
      const chunks = this.createChunks(file)
      console.log(`Dividido em ${chunks.length} chunks de ${this.CHUNK_SIZE / 1024 / 1024}MB`)
      
      // Upload chunks em paralelo
      let uploadedBytes = 0
      const totalBytes = file.size
      
      for (let i = 0; i < chunks.length; i += this.MAX_CONCURRENT) {
        const batch = chunks.slice(i, i + this.MAX_CONCURRENT)
        
        await Promise.all(batch.map(async (chunk, index) => {
          const chunkFilename = `${filename}.part${i + index + 1}`
          await this.uploadChunk(chunk, chunkFilename)
          
          uploadedBytes += chunk.size
          if (onProgress) {
            onProgress({
              loaded: uploadedBytes,
              total: totalBytes,
              percentage: Math.round((uploadedBytes / totalBytes) * 100)
            })
          }
        }))
      }
      
      // Combinar chunks no servidor (futuro)
      console.log('Multipart upload completo')
      
      return {
        success: true,
        url: `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${filename}`
      }
      
    } catch (error) {
      console.error('MultipartUpload error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Multipart upload failed'
      }
    }
  }

  private createChunks(file: File): Blob[] {
    const chunks: Blob[] = []
    let start = 0
    
    while (start < file.size) {
      const end = Math.min(start + this.CHUNK_SIZE, file.size)
      chunks.push(file.slice(start, end))
      start = end
    }
    
    return chunks
  }

  private async uploadChunk(chunk: Blob, filename: string): Promise<void> {
    const urlData = await mediaflowClient.getUploadUrl(filename, 'application/octet-stream', chunk.size)
    if (!urlData.success) throw new Error(urlData.message)
    
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve()
        } else {
          reject(new Error(`Chunk upload failed: ${xhr.status}`))
        }
      })
      
      xhr.addEventListener('error', () => reject(new Error('Chunk network error')))
      
      xhr.open('PUT', urlData.uploadUrl)
      xhr.setRequestHeader('Content-Type', 'application/octet-stream')
      xhr.send(chunk)
    })
  }
}