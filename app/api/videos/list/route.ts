import { NextRequest, NextResponse } from 'next/server'
import { getApiUrl } from '@/lib/aws-config'

export async function GET(request: NextRequest) {
  try {
    // Proxy to AWS Lambda
    const response = await fetch(getApiUrl('FILES'), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    const data = await response.json()
    
    if (data.success) {
      // Transform AWS response to match frontend expectations
      const files = data.files.map((file: any) => ({
        key: file.key,
        name: file.key.split('/').pop() || '',
        size: file.size,
        lastModified: file.lastModified,
        url: file.url || `https://${file.bucket === 'uploads' ? 'mediaflow-uploads-969430605054' : 'mediaflow-processed-969430605054'}.s3.amazonaws.com/${file.key}`,
        type: getFileType(file.key),
        folder: getFolder(file.key),
        bucket: file.bucket
      }))
      
      const folderSet = new Set(files.map((f: any) => f.folder).filter(Boolean))
      const folders = Array.from(folderSet)
      
      return NextResponse.json({
        success: true,
        files,
        folders,
        total: files.length,
      })
    }
    
    return NextResponse.json(data, { status: response.status })
  } catch (error: any) {
    console.error('List videos proxy error:', error)
    return NextResponse.json({
      success: false,
      error: error?.message || 'Erro ao listar vídeos',
      files: [],
      folders: [],
      total: 0,
    }, { status: 200 })
  }
}

function getFileType(filename: string): string {
  const ext = filename.split('.').pop()?.toLowerCase()
  
  if (['mp4', 'avi', 'mov', 'mkv', 'webm', 'ts'].includes(ext || '')) {
    return 'video'
  }
  if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext || '')) {
    return 'image'
  }
  if (['pdf', 'doc', 'docx', 'txt'].includes(ext || '')) {
    return 'document'
  }
  return 'other'
}

function getFolder(key: string): string {
  const parts = key.split('/')
  return parts.length > 1 ? parts[0] : 'root'
}