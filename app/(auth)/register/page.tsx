'use client'

import { useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Upload, X } from 'lucide-react'

export default function RegisterPage() {
  const [newUser, setNewUser] = useState({ 
    user_id: '', 
    email: '', 
    password: '', 
    confirmPassword: '', 
    name: '', 
    s3_prefix: '', 
    role: 'user' 
  })
  const [createLoading, setCreateLoading] = useState(false)
  const [createError, setCreateError] = useState('')
  const [avatarFile, setAvatarFile] = useState<File | null>(null)
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null)
  const [qrCodeUri, setQrCodeUri] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const router = useRouter()

  const generateUserId = (name: string) => {
    return name
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s]/g, '')
      .trim()
      .replace(/\s+/g, '_')
  }

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setAvatarFile(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setAvatarPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleCreateUser = async () => {
    setCreateError('')

    if (!newUser.name || !newUser.email || !newUser.password) {
      setCreateError('Preencha nome, email e senha')
      return
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(newUser.email)) {
      setCreateError('Email inválido')
      return
    }

    if (newUser.password.length < 6) {
      setCreateError('Senha deve ter no mínimo 6 caracteres')
      return
    }

    if (newUser.password !== newUser.confirmPassword) {
      setCreateError('As senhas não coincidem')
      return
    }

    const userId = newUser.user_id || generateUserId(newUser.name)

    setCreateLoading(true)
    try{
      const body: any = {
        user_id: userId,
        email: newUser.email,
        password: newUser.password,
        name: newUser.name,
        role: 'user', // Sempre user para registro público
        s3_prefix: `users/${userId}/`
      }

      if (avatarPreview) {
        body.avatar_image = avatarPreview
      }

      const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })

      const data = await res.json()
      
      if (data.success) {
        setQrCodeUri(data.user.totp_uri)
      } else {
        setCreateError(data.message || 'Erro ao criar usuário')
      }
    } catch (error) {
      setCreateError('Erro ao criar usuário')
    } finally {
      setCreateLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="glass-card p-8 md:p-12 w-full max-w-md animate-fade-in">
        <div className="text-center mb-8">
          <div className="text-5xl mb-4 animate-float">👤</div>
          <h1 className="text-3xl font-bold mb-2">
            <span className="neon-text-large">Criar Conta</span>
          </h1>
          <p className="text-gray-400">Junte-se ao Mídiaflow</p>
        </div>

        {qrCodeUri ? (
          <div className="text-center">
            <div className="mb-4 p-4 bg-yellow-500/20 border border-yellow-500/50 rounded-lg">
              <p className="text-yellow-400 font-semibold">⏳ Conta criada! Aguardando aprovação do administrador</p>
            </div>
            <p className="text-white mb-4">Configure o 2FA no Google Authenticator (opcional):</p>
            <img 
              src={`https://api.qrserver.net/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrCodeUri)}`}
              alt="QR Code 2FA"
              className="mx-auto mb-4"
            />
            <div className="space-y-3">
              <button 
                onClick={() => router.push('/login')} 
                className="btn-neon w-full"
              >
                Configurar 2FA e Fazer Login
              </button>
              <button 
                onClick={() => router.push('/login')} 
                className="btn-secondary w-full"
              >
                Pular 2FA e Fazer Login
              </button>
            </div>
            <p className="text-xs text-gray-400 mt-3">
              📝 Você pode configurar o 2FA depois no seu perfil
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {createError && (
              <div className="text-red-400 text-sm text-center bg-red-400/10 border border-red-400/20 rounded-lg p-3">
                {createError}
              </div>
            )}

            <div className="text-center">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleAvatarChange}
                className="hidden"
              />
              <div 
                onClick={() => fileInputRef.current?.click()}
                className="w-20 h-20 mx-auto rounded-full bg-gray-700 flex items-center justify-center cursor-pointer hover:bg-gray-600 transition-colors border-2 border-dashed border-gray-500 overflow-hidden"
              >
                {avatarPreview ? (
                  <img src={avatarPreview} alt="Preview" className="w-full h-full object-cover" />
                ) : (
                  <Upload className="w-8 h-8 text-gray-400" />
                )}
              </div>
              <p className="text-xs text-gray-400 mt-2">Clique para enviar avatar (opcional)</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Nome Completo</label>
              <input
                type="text"
                value={newUser.name}
                onChange={(e) => {
                  const name = e.target.value
                  const userId = generateUserId(name)
                  setNewUser({...newUser, name, user_id: userId, s3_prefix: `users/${userId}/`})
                }}
                className="input-neon"
                placeholder="João Silva"
                required
                disabled={createLoading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <input
                type="email"
                value={newUser.email}
                onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                className="input-neon"
                placeholder="joao@email.com"
                required
                disabled={createLoading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Senha (mínimo 6 caracteres)</label>
              <input
                type="password"
                value={newUser.password}
                onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                className="input-neon"
                placeholder="••••••••"
                required
                disabled={createLoading}
                minLength={6}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Confirmar Senha</label>
              <input
                type="password"
                value={newUser.confirmPassword}
                onChange={(e) => setNewUser({...newUser, confirmPassword: e.target.value})}
                className="input-neon"
                placeholder="••••••••"
                required
                disabled={createLoading}
              />
            </div>

            <button 
              onClick={handleCreateUser} 
              className="btn-neon w-full text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={createLoading || !newUser.name || !newUser.email || !newUser.password || !newUser.confirmPassword}
            >
              {createLoading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-dark-900 border-t-transparent rounded-full animate-spin"></div>
                  Criando conta...
                </div>
              ) : (
                <>🚀 Criar Conta</>
              )}
            </button>
          </div>
        )}

        <div className="mt-8 text-center space-y-4">
          <div className="border-t border-gray-700 pt-6">
            <p className="text-sm text-gray-400 mb-3">Já tem uma conta?</p>
            <Link 
              href="/login" 
              className="btn-secondary px-6 py-3 inline-flex items-center gap-2"
            >
              <span>🔑</span>
              Fazer Login
            </Link>
          </div>
          
          <div className="text-xs text-gray-500 space-y-1">
            <p>📝 <strong>Usuários existentes:</strong> Continuam funcionando normalmente</p>
            <p>🆕 <strong>Novos usuários:</strong> 2FA opcional (recomendado para segurança)</p>
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