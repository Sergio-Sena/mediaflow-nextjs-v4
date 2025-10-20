'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

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
        localStorage.setItem('current_user', JSON.stringify({
          user_id: data.user_id,
          name: data.user.name,
          email: data.user.email,
          role: data.user.role
        }))
        
        // 2FA apenas para admin
        if (data.user.role === 'admin' || data.user_id === 'user_admin') {
          router.push('/2fa')
        } else {
          // Usuários comuns vão direto ao dashboard
          localStorage.setItem('2fa_session', Date.now().toString())
          router.push('/dashboard')
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
      <div className="glass-card p-8 md:p-12 w-full max-w-md animate-fade-in">
        <div className="text-center mb-8">
          <div className="text-5xl mb-4 animate-float">🎬</div>
          <h1 className="text-3xl font-bold mb-2">
            <span className="neon-text-large">Mídiaflow</span>
          </h1>
          <p className="text-gray-400">Sistema de Streaming Modular</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="animate-fade-in">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-neon"
              placeholder="seu@email.com"
              autoComplete="email"
              required
              disabled={isLoading}
            />
          </div>

          <div className="animate-fade-in">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Senha
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-neon"
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
            <button
              type="submit"
              disabled={isLoading}
              className="btn-neon w-full text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-dark-900 border-t-transparent rounded-full animate-spin"></div>
                  Entrando...
                </div>
              ) : (
                <>🚀 Entrar</>
              )}
            </button>
          </div>
        </form>

        <div className="mt-8 text-center space-y-4">
          <div className="border-t border-gray-700 pt-6">
            <p className="text-sm text-gray-400 mb-3">Não tem uma conta?</p>
            <Link 
              href="/register" 
              className="btn-secondary px-6 py-3 inline-flex items-center gap-2"
            >
              <span>👤</span>
              Criar Conta
            </Link>
          </div>
          
          <Link 
            href="/" 
            className="text-sm text-gray-400 hover:text-neon-cyan transition-colors"
          >
            ← Voltar ao início
          </Link>
        </div>
      </div>
    </div>
  )
}