import { NextRequest, NextResponse } from 'next/server'

export async function DELETE(request: NextRequest) {
  try {
    const body = await request.json()
    const { key } = body
    
    if (!key) {
      return NextResponse.json({ success: false, message: 'Key is required' }, { status: 400 })
    }

    const token = request.headers.get('authorization')?.replace('Bearer ', '')
    
    // Tentar endpoint de user primeiro, depois bulk-delete
    const endpoints = [
      'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files/delete',
      'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files/bulk-delete'
    ]
    
    for (const endpoint of endpoints) {
      const body = endpoint.includes('bulk-delete') 
        ? JSON.stringify({ keys: [key] })
        : JSON.stringify({ key })
        
      const response = await fetch(endpoint, {
        method: endpoint.includes('bulk-delete') ? 'POST' : 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body
      })

      if (response.ok) {
        const data = await response.json()
        return NextResponse.json(data, { status: response.status })
      }
    }
    
    return NextResponse.json({ success: false, message: 'Delete failed' }, { status: 403 })
  } catch (error) {
    console.error('Delete proxy error:', error)
    return NextResponse.json({ success: false, message: 'Internal server error' }, { status: 500 })
  }
}
