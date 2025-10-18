'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function TwoFactorPage() {
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [userId, setUserId] = useState('')
  const [showQR, setShowQR] = useState(false)
  const [qrCodeUrl, setQrCodeUrl] = useState('')
  const router = useRouter()
  
  useEffect(() => {
    const selectedUser = localStorage.getItem('selected_user')
    if (!selectedUser) {
      router.push('/users')
      return
    }
    setUserId(selectedUser)
  }, [router])
  
  const handleVerify = async () => {
    if (code.length !== 6) {
      setError('Código deve ter 6 dígitos')
      return
    }
    
    setLoading(true)
    setError('')
    
    try {
      const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/verify-2fa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, code })
      })
      
      const data = await res.json()
      
      if (data.success) {
        localStorage.setItem('token', data.token)
        localStorage.setItem('current_user', JSON.stringify(data.user))
        localStorage.setItem('2fa_session', Date.now().toString())
        localStorage.removeItem('selected_user')
        router.push('/dashboard')
      } else {
        setError(data.message || 'Código inválido')
      }
    } catch (error) {
      setError('Erro ao verificar código')
    } finally {
      setLoading(false)
    }
  }
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && code.length === 6) {
      handleVerify()
    }
  }
  
  const getSecretForUser = (userId: string) => {
    const secrets: {[key: string]: string} = {
      'user_admin': 'JBSWY3DPEHPK3PXP',
      'sergio_sena': 'KBSWY3DPEHPK3PXQ',
      'lid': 'LBSWY3DPEHPK3PXR'
    }
    return secrets[userId] || 'JBSWY3DPEHPK3PXP'
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-dark-900 to-dark-800">
      <div className="glass-card p-8 max-w-md w-full">
        <div className="text-center mb-6">
          <div className="text-5xl mb-4">🔒</div>
          <h1 className="text-3xl font-bold neon-text mb-2">
            Autenticação 2FA
          </h1>
          <p className="text-gray-400">
            Insira o código do Google Authenticator
          </p>
        </div>
        
        <div className="mb-6">
          <input
            type="text"
            maxLength={6}
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
            onKeyPress={handleKeyPress}
            placeholder="000000"
            className="w-full px-4 py-4 bg-dark-800 border border-gray-700 rounded-lg text-center text-3xl tracking-widest text-white focus:border-neon-cyan focus:outline-none transition-colors"
            autoFocus
          />
          
          {error && (
            <p className="text-red-400 text-sm mt-3 text-center">{error}</p>
          )}
        </div>
        
        <button 
          onClick={handleVerify} 
          className="btn-neon w-full mb-3"
          disabled={loading || code.length !== 6}
        >
          {loading ? 'Verificando...' : 'Verificar Código'}
        </button>
        
        <button 
          onClick={() => router.push('/users')}
          className="btn-secondary w-full"
          disabled={loading}
        >
          ← Voltar aos Perfis
        </button>
        
        <div className="mt-6 space-y-3">
          <button
            onClick={() => setShowQR(!showQR)}
            className="w-full px-4 py-2 bg-purple-500/20 border border-purple-500/30 rounded-lg text-purple-300 hover:bg-purple-500/30 transition-colors text-sm"
          >
            {showQR ? '❌ Esconder QR Code' : '📱 Configurar Google Authenticator'}
          </button>
          
          {showQR && (
            <div className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-lg">
              <h3 className="text-sm font-semibold text-purple-300 mb-3 text-center">
                Escaneie com Google Authenticator
              </h3>
              
              <div className="bg-white p-4 rounded-lg mb-3">
                <img 
                  src={`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=otpauth://totp/Mediaflow:${userId}?secret=${getSecretForUser(userId)}&issuer=Mediaflow`}
                  alt="QR Code"
                  className="w-full h-auto"
                />
              </div>
              
              <div className="text-xs text-gray-400 space-y-2">
                <p><strong>Secret Manual:</strong></p>
                <code className="block bg-dark-800 p-2 rounded text-purple-300 break-all">
                  {getSecretForUser(userId)}
                </code>
                <p className="text-center mt-3">
                  📱 Abra o app Google Authenticator → + → Escanear QR Code
                </p>
              </div>
            </div>
          )}
          
          <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
            <p className="text-xs text-blue-300 text-center">
              💡 Após configurar, insira o código de 6 dígitos acima
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
