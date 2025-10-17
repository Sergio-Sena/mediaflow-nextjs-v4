import { NextRequest, NextResponse } from 'next/server'
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'

const s3Client = new S3Client({
  region: 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
})

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File
    const userId = formData.get('userId') as string

    if (!file || !userId) {
      return NextResponse.json({ success: false, error: 'Missing file or userId' })
    }

    // Convert file to buffer
    const bytes = await file.arrayBuffer()
    const buffer = Buffer.from(bytes)

    // Upload to S3
    const key = `avatars/avatar_${userId}.${file.name.split('.').pop()}`
    
    await s3Client.send(new PutObjectCommand({
      Bucket: 'mediaflow-uploads',
      Key: key,
      Body: buffer,
      ContentType: file.type,
    }))

    const avatarUrl = `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${key}`

    return NextResponse.json({ 
      success: true, 
      avatarUrl 
    })

  } catch (error) {
    console.error('Avatar upload error:', error)
    return NextResponse.json({ 
      success: false, 
      error: 'Upload failed' 
    })
  }
}