import { NextRequest, NextResponse } from 'next/server'
import { getApiUrl } from '@/lib/aws-config'

export async function DELETE(request: NextRequest) {
  try {
    const { key } = await request.json()
    
    if (!key) {
      return NextResponse.json(
        { error: 'Chave do arquivo não fornecida' },
        { status: 400 }
      )
    }

    // Proxy to AWS Lambda
    const response = await fetch(`${getApiUrl('FILES').replace('/files', `/files/${encodeURIComponent(key)}`)}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    const data = await response.json()
    
    return NextResponse.json(data, { status: response.status })
  } catch (error: any) {
    console.error('Delete proxy error:', error)
    return NextResponse.json(
      { error: 'Erro ao excluir arquivo' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const { keys } = await request.json()
    
    if (!keys || !Array.isArray(keys)) {
      return NextResponse.json(
        { error: 'Lista de chaves não fornecida' },
        { status: 400 }
      )
    }

    // Proxy to AWS Lambda bulk delete
    const response = await fetch(`${getApiUrl('FILES')}/bulk-delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ keys })
    })
    
    const data = await response.json()
    
    return NextResponse.json(data, { status: response.status })
  } catch (error: any) {
    console.error('Bulk delete proxy error:', error)
    return NextResponse.json(
      { error: 'Erro ao excluir arquivos' },
      { status: 500 }
    )
  }
}