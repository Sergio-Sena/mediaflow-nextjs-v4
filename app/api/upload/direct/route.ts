import { NextRequest, NextResponse } from 'next/server'
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'

const s3Client = new S3Client({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
})

export async function POST(request: NextRequest) {
  try {
    console.log('API Upload Direct - Iniciando...')
    
    // Validar configuração AWS
    if (!process.env.AWS_ACCESS_KEY_ID || !process.env.AWS_SECRET_ACCESS_KEY) {
      console.error('AWS credentials not configured')
      return NextResponse.json(
        { error: 'AWS credentials not configured' },
        { status: 500 }
      )
    }

    const formData = await request.formData()
    const file = formData.get('file') as File
    const folder = formData.get('folder') as string
    const relativePath = formData.get('relativePath') as string

    if (!file) {
      return NextResponse.json(
        { error: 'Nenhum arquivo fornecido' },
        { status: 400 }
      )
    }

    // Sanitizar nome do arquivo
    const sanitizedFilename = file.name.replace(/[^a-zA-Z0-9.-]/g, '_')
    let key: string
    
    if (folder && relativePath) {
      const sanitizedPath = relativePath.replace(/[^a-zA-Z0-9.\/\-_]/g, '_')
      key = `uploads/${folder}/${sanitizedPath}`
    } else {
      key = `uploads/files/${Date.now()}-${sanitizedFilename}`
    }

    console.log('Uploading to S3:', key)

    // Converter File para Buffer
    const arrayBuffer = await file.arrayBuffer()
    const buffer = Buffer.from(arrayBuffer)

    // Upload direto para S3
    const command = new PutObjectCommand({
      Bucket: 'drive-online-frontend',
      Key: key,
      Body: buffer,
      ContentType: file.type,
      Metadata: {
        'original-filename': file.name,
        'upload-timestamp': new Date().toISOString(),
        'folder': folder || 'files',
        'relative-path': relativePath || file.name,
      },
    })

    await s3Client.send(command)
    
    const fileUrl = `https://d1k8z7g2w8j4qr.cloudfront.net/${key}`

    console.log('Upload successful:', fileUrl)

    return NextResponse.json({
      success: true,
      key,
      fileUrl,
      bucket: 'drive-online-frontend',
      size: file.size,
      contentType: file.type,
    })

  } catch (error: any) {
    console.error('Direct upload error:', error)
    return NextResponse.json(
      { error: error?.message || 'Erro no upload direto' },
      { status: 500 }
    )
  }
}