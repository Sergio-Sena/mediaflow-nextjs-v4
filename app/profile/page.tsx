'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { getUserFromToken } from '@/lib/auth-utils'
import { getApiUrl } from '@/lib/aws-config'
import AvatarUpload from '@/components/AvatarUpload'
import { ConfirmModal } from '@/components/ui/Modal'
import { LogOut, Save, ArrowLeft } from 'lucide-react'

export default function ProfilePage() {
  const router = useRouter()
  const tokenUser = getUserFromToken()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [avatarUrl, setAvatarUrl] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [logoutModal, setLogoutModal] = useState(false)

  useEffect(() => {
    if (!tokenUser) {
      window.location.href = '/login'
      return
    }
    loadProfile()
  }, [])

  const loadProfile = () => {
    const saved = localStorage.getItem('current_user')
    if (saved) {
      const user = JSON.parse(saved)
      setName(user.name || tokenUser?.email?.split('@')[0] || '')
      setEmail(tokenUser?.email || '')
      setAvatarUrl(user.avatar_url || '')
    } else {
      setName(tokenUser?.email?.split('@')[0] || '')
      setEmail(tokenUser?.email || '')
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const token = localStorage.getItem('token')
      const body: any = { user_id: tokenUser?.user_id }
      if (name) body.name = name
      if (newPassword) body.password = newPassword

      const res = await fetch(getApiUrl('UPDATE_USER'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(body)
      })
      const data = await res.json()
      if (data.success) {
        // Update localStorage
        const current = JSON.parse(localStorage.getItem('current_user') || '{}')
        current.name = name
        localStorage.setItem('current_user', JSON.stringify(current))
        setSaved(true)
        setNewPassword('')
        setTimeout(() => setSaved(false), 3000)
      }
    } catch (e) {
      console.error('Save error:', e)
    } finally {
      setSaving(false)
    }
  }

  const handleLogout = () => {
    localStorage.clear()
    window.location.href = '/login'
  }

  if (!tokenUser) return null

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-dark-900/50 backdrop-blur-md border-b border-neon-cyan/20 sticky top-0 z-50">
        <div className="mx-auto px-3 sm:px-8 py-2.5 sm:py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2 sm:gap-3">
              <button onClick={() => router.back()} className="p-1.5 text-gray-400 hover:text-white md:hidden">
                <ArrowLeft className="w-5 h-5" />
              </button>
              <h1 className="text-base sm:text-2xl font-bold">
                👤 <span className="text-white">Meu Perfil</span>
              </h1>
            </div>
            <button
              onClick={() => setLogoutModal(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-red-600/20 hover:bg-red-600/40 text-red-300 border border-red-500/30 rounded-lg transition-colors text-sm"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Sair</span>
            </button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="mx-auto px-4 sm:px-8 py-6 max-w-lg">
        {/* Avatar */}
        <div className="flex flex-col items-center mb-8">
          <AvatarUpload
            currentAvatar={avatarUrl}
            size="lg"
            onAvatarUpdate={(url) => setAvatarUrl(url)}
          />
          <p className="text-sm text-gray-400 mt-2">Toque para alterar</p>
        </div>

        {/* Form */}
        <div className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1.5">Nome</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-2.5 bg-gray-800 border border-gray-600 rounded-lg text-white focus:border-neon-cyan focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1.5">Email</label>
            <input
              type="email"
              value={email}
              disabled
              className="w-full px-4 py-2.5 bg-gray-800/50 border border-gray-700 rounded-lg text-gray-400 cursor-not-allowed"
            />
            <p className="text-xs text-gray-500 mt-1">Email não pode ser alterado</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1.5">Nova Senha</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Deixe vazio para manter a atual"
              className="w-full px-4 py-2.5 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:border-neon-cyan focus:outline-none"
            />
          </div>

          {/* Info */}
          <div className="glass-card p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">User ID</span>
              <span className="text-white font-mono text-xs">{tokenUser.user_id}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Role</span>
              <span className="text-neon-cyan">{tokenUser.role}</span>
            </div>
          </div>

          {/* Buttons */}
          <div className="flex gap-3">
            <button
              onClick={() => router.push('/public-feed')}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gray-700/20 text-gray-300 border border-gray-600/30 rounded-lg hover:bg-gray-700/40 transition-colors"
            >
              Descartar
            </button>
            <button
              onClick={async () => {
                await handleSave()
                router.push('/public-feed')
              }}
              disabled={saving}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-neon-cyan border border-neon-cyan/50 rounded-lg hover:from-cyan-500/30 hover:to-purple-500/30 transition-all font-medium disabled:opacity-50"
            >
              <Save className="w-4 h-4" />
              {saving ? 'Salvando...' : 'Salvar'}
            </button>
          </div>
        </div>
      </main>

      {/* Logout Modal */}
      <ConfirmModal
        isOpen={logoutModal}
        onClose={() => setLogoutModal(false)}
        onConfirm={handleLogout}
        title="Sair da conta"
        message="Deseja realmente sair? Você precisará fazer login novamente."
        confirmText="Sair"
        confirmColor="red"
      />
    </div>
  )
}
