import { NextRequest, NextResponse } from 'next/server'
import { getApiUrl } from '@/lib/aws-config'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    console.log('Upload request:', body)
    
    // Proxy to AWS Lambda
    const response = await fetch(getApiUrl('UPLOAD'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        filename: body.filename,
        contentType: body.contentType
      })
    })
    
    const data = await response.json()
    console.log('AWS Lambda response:', data)
    
    if (data.success) {
      // Transform response to match frontend expectations
      return NextResponse.json({
        success: true,
        uploadUrl: data.uploadUrl,
        key: data.key,
        bucket: data.bucket,
        fileUrl: `https://${data.bucket}.s3.amazonaws.com/${data.key}`
      })
    }
    
    return NextResponse.json(data, { status: response.status })
  } catch (error: any) {
    console.error('Upload proxy error:', error)
    return NextResponse.json(
      { error: error?.message || 'Erro ao gerar URL de upload' },
      { status: 500 }
    )
  }
}