import { NextRequest, NextResponse } from 'next/server'
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'

const s3Client = new S3Client({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
})

export async function POST(request: NextRequest) {
  try {
    const { filename, contentType, fileSize } = await request.json()
    
    // Validar token JWT
    const authHeader = request.headers.get('authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Token não fornecido' },
        { status: 401 }
      )
    }

    // Sanitizar nome do arquivo
    const sanitizedFilename = filename.replace(/[^a-zA-Z0-9.-]/g, '_')
    const key = `uploads/${Date.now()}-${sanitizedFilename}`

    // Criar comando S3
    const command = new PutObjectCommand({
      Bucket: 'video-streaming-sstech-v3',
      Key: key,
      ContentType: contentType,
      Metadata: {
        'original-filename': filename,
        'upload-timestamp': new Date().toISOString(),
      },
    })

    // Gerar URL assinada (válida por 1 hora)
    const uploadUrl = await getSignedUrl(s3Client, command, { 
      expiresIn: 3600 
    })

    return NextResponse.json({
      success: true,
      uploadUrl,
      key,
      bucket: 'video-streaming-sstech-v3',
    })

  } catch (error) {
    console.error('Upload URL error:', error)
    return NextResponse.json(
      { error: 'Erro ao gerar URL de upload' },
      { status: 500 }
    )
  }
}