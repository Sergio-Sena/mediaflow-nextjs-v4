import { NextRequest, NextResponse } from 'next/server'
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'

const s3Client = new S3Client({ region: 'us-east-1' })

export async function POST(request: NextRequest) {
  try {
    const { key } = await request.json()
    
    if (!key) {
      return NextResponse.json(
        { success: false, message: 'Key is required' },
        { status: 400 }
      )
    }
    
    const command = new GetObjectCommand({
      Bucket: 'mediaflow-uploads-969430605054',
      Key: key,
    })
    
    const viewUrl = await getSignedUrl(s3Client, command, { expiresIn: 3600 })
    
    return NextResponse.json({
      success: true,
      viewUrl,
    })
  } catch (error: any) {
    console.error('[PROXY-VIEW] Error:', error)
    return NextResponse.json(
      { success: false, message: error.message },
      { status: 500 }
    )
  }
}
