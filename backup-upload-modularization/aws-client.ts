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
}

export const mediaflowClient = new MediaflowClient()