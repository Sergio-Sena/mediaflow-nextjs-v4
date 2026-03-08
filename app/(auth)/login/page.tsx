'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button, Input, Card } from '@/components/ui'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const { mediaflowClient } = await import('@/lib/aws-client')
      const data = await mediaflowClient.login(email, password)

      if (data.success) {
        // Salvar token e dados do usuário
        localStorage.setItem('token', data.token)
        localStorage.setItem('user', JSON.stringify(data.user))
        
        // Buscar dados completos do usuário (incluindo avatar) via proxy
        try {
          const usersRes = await fetch('/api/users/list', {
            headers: {
              'Authorization': `Bearer ${data.token}`
            }
          })
          const usersData = await usersRes.json()
          if (usersData.success) {
            const fullUser = usersData.users.find((u: any) => u.user_id === data.user_id || u.email === email)
            if (fullUser) {
              console.log('✅ Current user saved:', fullUser)
              localStorage.setItem('current_user', JSON.stringify(fullUser))
            } else {
              console.warn('⚠️ User not found in list, using fallback')
              // Fallback se não encontrar
              const fallbackUser = {
                user_id: data.user_id,
                name: data.user?.name || email.split('@')[0],
                email: email,
                role: data.user?.role || 'user',
                s3_prefix: `users/${data.user_id}/`
              }
              console.log('Fallback user:', fallbackUser)
              localStorage.setItem('current_user', JSON.stringify(fallbackUser))
            }
          }
        } catch (err) {
          console.error('❌ Erro ao buscar dados do usuário:', err)
          // Fallback - buscar avatar diretamente do DynamoDB
          try {
            const avatarRes = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/${data.user_id}`)
            const avatarData = await avatarRes.json()
            const fallbackUser = {
              user_id: data.user_id,
              name: data.user?.name || email.split('@')[0],
              email: email,
              role: data.user?.role || 'user',
              s3_prefix: `users/${data.user_id}/`,
              avatar_url: avatarData.avatar_url || undefined
            }
            localStorage.setItem('current_user', JSON.stringify(fallbackUser))
          } catch (e2) {
            // Fallback final sem avatar
            const fallbackUser = {
              user_id: data.user_id,
              name: data.user?.name || email.split('@')[0],
              email: email,
              role: data.user?.role || 'user',
              s3_prefix: `users/${data.user_id}/`
            }
            localStorage.setItem('current_user', JSON.stringify(fallbackUser))
          }
        }
        
        // 2FA apenas para admin
        if (data.user.role === 'admin' || data.user_id === 'user_admin') {
          window.location.href = '/2fa'
        } else {
          // Usuários comuns vão direto ao dashboard
          localStorage.setItem('2fa_session', Date.now().toString())
          window.location.href = '/dashboard'
        }
      } else {
        setError(data.error || 'Erro ao fazer login')
      }
    } catch (err) {
      setError('Erro de conexão')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card variant="glass" padding="lg" className="w-full max-w-md animate-fade-in">
        <div className="text-center mb-8">
          <div className="text-5xl mb-4 animate-float">🎬</div>
          <h1 className="text-3xl font-bold mb-2">
            <span className="neon-text-large">Mídiaflow</span>
          </h1>
          <p className="text-gray-400">Sistema de Streaming Modular</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="animate-fade-in">
            <Input
              type="email"
              label="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              autoComplete="email"
              required
              disabled={isLoading}
            />
          </div>

          <div className="animate-fade-in">
            <Input
              type="password"
              label="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              autoComplete="current-password"
              required
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="text-red-400 text-sm text-center bg-red-400/10 border border-red-400/20 rounded-lg p-3 animate-slide-down">
              {error}
            </div>
          )}

          <div className="animate-fade-in">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              loading={isLoading}
              disabled={isLoading}
              className="w-full"
            >
              🚀 Entrar
            </Button>
          </div>
        </form>

        <div className="mt-6 sm:mt-8 text-center space-y-3 sm:space-y-4">
          <div className="border-t border-gray-700 pt-4 sm:pt-6">
            <p className="text-xs sm:text-sm text-gray-400 mb-2 sm:mb-3">Não tem uma conta?</p>
            <Link href="/register" className="block">
              <Button variant="secondary" size="md" className="w-full sm:w-auto">
                <span>👤</span>
                Criar Conta
              </Button>
            </Link>
          </div>
          
          <Link 
            href="/" 
            className="block text-xs sm:text-sm text-gray-400 hover:text-neon-cyan transition-colors py-2"
          >
            ← Voltar ao início
          </Link>
        </div>
      </Card>
    </div>
  )
}