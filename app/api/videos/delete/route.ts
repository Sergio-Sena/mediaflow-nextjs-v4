import { NextRequest, NextResponse } from 'next/server'

export async function DELETE(request: NextRequest) {
  try {
    const body = await request.json()
    const { key } = body
    
    if (!key) {
      return NextResponse.json({ success: false, message: 'Key is required' }, { status: 400 })
    }

    const token = request.headers.get('authorization')?.replace('Bearer ', '')
    if (!token) {
      return NextResponse.json({ success: false, message: 'Unauthorized' }, { status: 401 })
    }
    
    // Tentar endpoint de user primeiro
    const deleteResponse = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files/delete', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ key })
    })

    if (deleteResponse.ok) {
      const data = await deleteResponse.json()
      return NextResponse.json(data)
    }
    
    // Se falhar, tentar bulk-delete (admin)
    const bulkResponse = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files/bulk-delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ keys: [key] })
    })

    if (bulkResponse.ok) {
      const data = await bulkResponse.json()
      return NextResponse.json(data)
    }
    
    return NextResponse.json({ success: false, message: 'Delete failed' }, { status: 403 })
  } catch (error) {
    console.error('Delete proxy error:', error)
    return NextResponse.json({ success: false, message: 'Internal server error' }, { status: 500 })
  }
}
