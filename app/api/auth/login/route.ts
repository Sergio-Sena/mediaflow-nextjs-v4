import { NextRequest, NextResponse } from 'next/server'
import jwt from 'jsonwebtoken'

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json()
    
    // Validação simples (baseada na documentação original)
    if (email === 'sergiosenaadmin@sstech' && password === 'sergiosena') {
      const token = jwt.sign(
        { 
          email, 
          name: 'Sergio Sena',
          role: 'admin' 
        }, 
        process.env.JWT_SECRET!, 
        { expiresIn: '24h' }
      )
      
      return NextResponse.json({ 
        success: true,
        token, 
        user: { 
          email, 
          name: 'Sergio Sena',
          role: 'admin' 
        } 
      })
    }
    
    return NextResponse.json(
      { success: false, error: 'Credenciais inválidas' }, 
      { status: 401 }
    )
  } catch (error) {
    console.error('Auth error:', error)
    return NextResponse.json(
      { success: false, error: 'Erro interno do servidor' },
      { status: 500 }
    )
  }
}