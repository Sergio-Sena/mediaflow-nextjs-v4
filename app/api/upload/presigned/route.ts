import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const authHeader = request.headers.get('authorization')
    
    if (!authHeader) {
      return NextResponse.json({ success: false, error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()

    const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/presigned', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authHeader,
      },
      body: JSON.stringify(body)
    })

    const data = await response.json()
    
    if (!response.ok) {
      console.error('API Gateway error:', response.status, data)
    }
    
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Upload presigned proxy error:', error)
    return NextResponse.json({ success: false, error: 'Failed to generate presigned URL' }, { status: 500 })
  }
}
