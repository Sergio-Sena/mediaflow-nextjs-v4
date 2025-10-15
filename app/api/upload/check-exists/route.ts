import { NextRequest, NextResponse } from 'next/server'
import { getApiUrl } from '@/lib/aws-config'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(getApiUrl('UPLOAD') + '/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filenames: body.filenames })
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error: any) {
    return NextResponse.json(
      { error: error?.message || 'Erro ao verificar arquivos' },
      { status: 500 }
    )
  }
}
