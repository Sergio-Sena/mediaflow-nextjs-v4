import { NextRequest, NextResponse } from 'next/server'
import { getApiUrl } from '@/lib/aws-config'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Proxy to AWS Lambda
    const response = await fetch(getApiUrl('AUTH'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    const data = await response.json()
    
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Auth proxy error:', error)
    return NextResponse.json(
      { success: false, error: 'Erro interno do servidor' },
      { status: 500 }
    )
  }
}