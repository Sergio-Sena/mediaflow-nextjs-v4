import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching users:', error)
    return NextResponse.json({ success: false, error: 'Failed to fetch users' }, { status: 500 })
  }
}
