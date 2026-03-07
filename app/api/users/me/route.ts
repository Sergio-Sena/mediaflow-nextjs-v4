import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  try {
    const authHeader = request.headers.get('authorization')
    
    if (!authHeader) {
      return NextResponse.json({ success: false, error: 'Unauthorized' }, { status: 401 })
    }

    const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/me', {
      method: 'GET',
      headers: {
        'Authorization': authHeader
      }
    })

    const data = await response.json()
    
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Get user profile error:', error)
    return NextResponse.json({ success: false, error: 'Failed to get user profile' }, { status: 500 })
  }
}
