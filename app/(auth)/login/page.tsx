'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button, Input } from '@/components/ui'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    try {
      const { mediaflowClient } = await import('@/lib/aws-client')
      const data = await mediaflowClient.login(email, password)
      if (data.success) {
        localStorage.setItem('token', data.token)
        localStorage.setItem('user', JSON.stringify(data.user))
        localStorage.setItem('current_user', JSON.stringify(data.user))
        if (data.user.role === 'admin' || data.user_id === 'user_admin') {
          setTimeout(() => window.location.href = '/2fa', 100)
        } else {
          localStorage.setItem('2fa_session', Date.now().toString())
          setTimeout(() => window.location.href = '/public-feed', 100)
        }
      } else {
        setError(data.error || 'Credenciais inválidas')
      }
    } catch {
      setError('Erro de conexão')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex" style={{ background: 'linear-gradient(315deg, #000000 0%, #0d0d1a 50%, #0a0a1f 100%)' }}>

      {/* Left — Visual */}
      <div className="hidden lg:flex flex-1 relative items-center justify-center p-16 overflow-hidden">
        <div className="absolute inset-0 opacity-30" style={{ background: 'radial-gradient(ellipse at 60% 50%, #667eea 0%, transparent 70%)' }}></div>
        <div className="relative z-10 max-w-md">
          <div className="text-4xl font-bold mb-6 tracking-tight">
            <span className="text-white">Mídia</span><span style={{ color: '#667eea' }}>flow</span>
          </div>
          <h2 className="text-3xl font-bold text-white mb-4 leading-tight">
            Sua biblioteca de mídia, sempre disponível.
          </h2>
          <p className="text-gray-400 leading-relaxed mb-10">
            Player premium, CDN global e organização inteligente para toda sua coleção.
          </p>
          {/* Mini player mockup */}
          <div className="rounded-2xl overflow-hidden border border-white/10" style={{ background: 'rgba(255,255,255,0.03)' }}>
            <div className="aspect-video relative flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #0d0d1a, #1a1a2e)' }}>
              <div className="absolute inset-0 opacity-20" style={{ background: 'radial-gradient(ellipse at center, #667eea, transparent 70%)' }}></div>
              <div className="w-12 h-12 rounded-full flex items-center justify-center border border-white/20 relative z-10" style={{ background: 'rgba(102,126,234,0.2)' }}>
                <svg className="w-5 h-5 text-white ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              </div>
              <div className="absolute bottom-0 left-0 right-0 p-3">
                <div className="h-0.5 rounded-full bg-white/10 mb-2">
                  <div className="h-full w-1/3 rounded-full" style={{ background: 'linear-gradient(90deg, #667eea, #764ba2)' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right — Form */}
      <div className="flex-1 lg:max-w-md flex items-center justify-center p-8">
        <div className="w-full max-w-sm animate-fade-in">
          {/* Mobile logo */}
          <div className="lg:hidden text-2xl font-bold mb-10 text-center">
            <span className="text-white">Mídia</span><span style={{ color: '#667eea' }}>flow</span>
          </div>

          <h1 className="text-2xl font-bold text-white mb-2">Bem-vindo de volta</h1>
          <p className="text-gray-500 mb-8 text-sm">Entre com suas credenciais para acessar</p>

          <form onSubmit={handleSubmit} className="space-y-5">
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

            {error && (
              <div className="text-red-400 text-sm text-center bg-red-400/10 border border-red-400/20 rounded-lg p-3 animate-slide-down">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3.5 rounded-xl font-semibold text-white transition-all duration-300 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', boxShadow: '0 8px 30px rgba(102,126,234,0.3)' }}
            >
              {isLoading ? 'Entrando...' : 'Entrar'}
            </button>
          </form>

          <div className="mt-8 pt-6 border-t border-white/5 text-center">
            <Link href="/" className="text-sm text-gray-600 hover:text-gray-400 transition-colors">
              ← Voltar ao início
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
