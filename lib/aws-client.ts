// Direct AWS API Client for Static Frontend
import { AWS_CONFIG, getApiUrl } from './aws-config'

export class MediaflowClient {
  private baseUrl = AWS_CONFIG.API_BASE_URL
  
  async login(email: string, password: string) {
    const response = await fetch(getApiUrl('AUTH'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    })
    
    return response.json()
  }
  
  async getFiles() {
    const response = await fetch(getApiUrl('FILES'), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    return response.json()
  }
  
  async getViewUrl(key: string) {
    const response = await fetch(`${this.baseUrl}/view/${encodeURIComponent(key)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    return response.json()
  }
  
  async getUploadUrl(filename: string, contentType: string, fileSize?: number) {
    const response = await fetch(getApiUrl('UPLOAD'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ filename, contentType, fileSize })
    })
    
    return response.json()
  }
  
  async deleteFile(key: string) {
    const response = await fetch(`${getApiUrl('FILES')}/${encodeURIComponent(key)}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    return response.json()
  }
  
  async bulkDelete(keys: string[]) {
    const response = await fetch(`${getApiUrl('FILES')}/bulk-delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ keys })
    })
    
    return response.json()
  }
  
  async uploadThumbnail(key: string, thumbnailBuffer: ArrayBuffer) {
    try {
      // Get presigned URL for thumbnail upload
      const uploadResponse = await this.getUploadUrl(key, 'image/jpeg', thumbnailBuffer.byteLength)
      
      if (!uploadResponse.success) {
        return { success: false, error: uploadResponse.message }
      }
      
      // Upload thumbnail directly to S3
      const uploadResult = await fetch(uploadResponse.uploadUrl, {
        method: 'PUT',
        body: thumbnailBuffer,
        headers: {
          'Content-Type': 'image/jpeg'
        }
      })
      
      if (uploadResult.ok) {
        return { success: true, url: `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${key}` }
      } else {
        return { success: false, error: `Upload failed: ${uploadResult.status}` }
      }
      
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      }
    }
  }
}

export const mediaflowClient = new MediaflowClient()