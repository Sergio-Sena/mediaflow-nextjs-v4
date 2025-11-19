import { NextRequest, NextResponse } from 'next/server'
import { getApiUrl } from '@/lib/aws-config'

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Max-Age': '86400',
}

export async function OPTIONS() {
  return new NextResponse(null, { headers: CORS_HEADERS })
}

export async function GET(request: NextRequest, { params }: { params: { key: string } }) {
  try {
    const key = params.key || request.nextUrl.searchParams.get('key') || ''
    
    if (!key) {
      return NextResponse.json(
        { error: 'Key is required' },
        { status: 400, headers: CORS_HEADERS }
      )
    }
    
    const response = await fetch(`${getApiUrl('VIEW')}/${encodeURIComponent(key)}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    
    const data = await response.json()
    return NextResponse.json(data, { headers: CORS_HEADERS })
  } catch (error: any) {
    return NextResponse.json(
      { error: error?.message || 'Error getting view URL' },
      { status: 500, headers: CORS_HEADERS }
    )
  }
}
