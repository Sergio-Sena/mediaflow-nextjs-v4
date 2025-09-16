import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    // Aceitar FormData da versão antiga
    const formData = await request.formData()
    const file = formData.get('file') as File
    const filename = formData.get('filename') as string || file?.name
    
    if (!file) {
      return NextResponse.json(
        { success: false, error: 'File required' },
        { status: 400 }
      )
    }
    
    console.log('🔄 Direct route FormData:', filename, file.size)
    
    // 1. Obter URL presigned
    const urlResponse = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/presigned', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        filename: filename,
        contentType: file.type,
        fileSize: file.size
      })
    })

    const urlData = await urlResponse.json()
    
    if (!urlData.success) {
      throw new Error(urlData.message || 'Failed to get upload URL')
    }
    
    // 2. Upload file to S3
    const uploadResponse = await fetch(urlData.uploadUrl, {
      method: 'PUT',
      body: file,
      headers: {
        'Content-Type': file.type
      }
    })
    
    if (!uploadResponse.ok) {
      throw new Error(`Upload failed: ${uploadResponse.status}`)
    }
    
    return NextResponse.json({
      success: true,
      url: `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${urlData.key}`,
      key: urlData.key
    })
    
  } catch (error: any) {
    console.error('❌ Direct route error:', error)
    return NextResponse.json(
      { success: false, error: error?.message || 'Direct route failed' },
      { status: 500 }
    )
  }
}