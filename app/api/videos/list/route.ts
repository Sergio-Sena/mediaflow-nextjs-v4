import { NextRequest, NextResponse } from 'next/server'
import { S3Client, ListObjectsV2Command } from '@aws-sdk/client-s3'

const s3Client = new S3Client({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
})

export async function GET(request: NextRequest) {
  try {
    // Validar token JWT
    const authHeader = request.headers.get('authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Token não fornecido' },
        { status: 401 }
      )
    }

    const command = new ListObjectsV2Command({
      Bucket: 'video-streaming-sstech-v3',
      MaxKeys: 1000,
    })

    const response = await s3Client.send(command)
    
    // Processar arquivos
    const files = response.Contents?.map(file => ({
      key: file.Key,
      name: file.Key?.split('/').pop() || '',
      size: file.Size || 0,
      lastModified: file.LastModified,
      url: `https://d2we88koy23cl4.cloudfront.net/${file.Key}`,
      type: getFileType(file.Key || ''),
      folder: getFolder(file.Key || ''),
    })) || []

    // Organizar por pastas
    const folders = [...new Set(files.map(f => f.folder).filter(Boolean))]
    
    return NextResponse.json({
      success: true,
      files,
      folders,
      total: files.length,
    })

  } catch (error) {
    console.error('List videos error:', error)
    return NextResponse.json(
      { error: 'Erro ao listar vídeos' },
      { status: 500 }
    )
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