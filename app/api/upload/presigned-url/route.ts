import { NextRequest, NextResponse } from 'next/server'
import { getApiUrl } from '@/lib/aws-config'

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Max-Age': '86400',
}

export async function OPTIONS() {
  return new NextResponse(null, { headers: CORS_HEADERS })
}

export async function POST(request: NextRequest) {
  const startTime = Date.now()
  try {
    const body = await request.json()
    console.log('🔍 [PRESIGNED-URL] Request recebido:', { filename: body.filename, contentType: body.contentType, fileSize: body.fileSize })
    
    const apiUrl = getApiUrl('UPLOAD')
    console.log(`🌍 [PRESIGNED-URL] Chamando Lambda em: ${apiUrl}`)
    console.log(`🔐 [PRESIGNED-URL] Headers enviados:`, { 'Content-Type': 'application/json' })
    
    const lambdaStart = Date.now()
    let response
    try {
      const authHeader = request.headers.get('Authorization') || ''
      response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authHeader
        },
        body: JSON.stringify({
          filename: body.filename,
          contentType: body.contentType,
          fileSize: body.fileSize
        })
      })
    } catch (fetchError: any) {
      console.error(`❌ [PRESIGNED-URL] Erro ao conectar com Lambda:`, {
        message: fetchError?.message,
        code: fetchError?.code,
        apiUrl
      })
      throw fetchError
    }
    
    const lambdaTime = Date.now() - lambdaStart
    console.log(`⏱️ [PRESIGNED-URL] Lambda respondeu em ${lambdaTime}ms com status ${response.status}`)
    
    const responseText = await response.text()
    console.log(`📄 [PRESIGNED-URL] Lambda response body (${responseText.length} chars):`, responseText)
    
    if (!response.ok) {
      console.error(`❌ [PRESIGNED-URL] Lambda HTTP Error ${response.status}:`, {
        status: response.status,
        statusText: response.statusText,
        body: responseText,
        headers: Object.fromEntries(response.headers.entries())
      })
      return NextResponse.json(
        { success: false, message: `Lambda error: ${response.status} - ${responseText}` },
        { status: response.status, headers: CORS_HEADERS }
      )
    }
    
    let data
    try {
      data = JSON.parse(responseText)
    } catch (parseError) {
      console.error(`❌ [PRESIGNED-URL] Erro ao parsear JSON:`, responseText)
      return NextResponse.json(
        { success: false, message: `Invalid JSON from Lambda: ${responseText}` },
        { status: 502, headers: CORS_HEADERS }
      )
    }
    
    console.log(`✅ [PRESIGNED-URL] Lambda response parsed:`, { success: data.success, hasUrl: !!data.uploadUrl })
    
    if (data.success) {
      const result = {
        success: true,
        uploadUrl: data.uploadUrl,
        key: data.key,
        bucket: data.bucket,
        fileUrl: `https://${data.bucket}.s3.amazonaws.com/${data.key}`
      }
      console.log(`✅ [PRESIGNED-URL] Sucesso em ${Date.now() - startTime}ms`)
      return NextResponse.json(result, { headers: CORS_HEADERS })
    }
    
    console.error(`❌ [PRESIGNED-URL] Lambda retornou success=false:`, data)
    return NextResponse.json(
      { success: false, message: data.message || 'Lambda retornou erro' },
      { status: 400, headers: CORS_HEADERS }
    )
  } catch (error: any) {
    console.error(`❌ [PRESIGNED-URL] Erro em ${Date.now() - startTime}ms:`, {
      message: error?.message,
      code: error?.code,
      stack: error?.stack?.split('\n').slice(0, 3).join('\n')
    })
    return NextResponse.json(
      { success: false, message: error?.message || 'Erro ao gerar URL de upload' },
      { status: 502, headers: CORS_HEADERS }
    )
  }
}
