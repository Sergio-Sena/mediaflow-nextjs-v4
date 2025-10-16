'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { Upload, Trash2, X } from 'lucide-react'

interface User {
  user_id: string
  name: string
  avatar_url?: string
  s3_prefix: string
  created_at?: string
}

export default function AdminPage() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newUser, setNewUser] = useState({ user_id: '', name: '', s3_prefix: '' })
  const [avatarFile, setAvatarFile] = useState<File | null>(null)
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null)
  const [qrCodeUri, setQrCodeUri] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users')
      const data = await res.json()
      if (data.success) {
        setUsers(data.users)
      }
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
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
    if (!newUser.user_id || !newUser.name) {
      alert('Preencha user_id e nome')
      return
    }

    try {
      const body: any = {
        user_id: newUser.user_id,
        name: newUser.name,
        s3_prefix: newUser.s3_prefix || `${newUser.user_id}/`
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
        fetchUsers()
        setNewUser({ user_id: '', name: '', s3_prefix: '' })
        setAvatarFile(null)
        setAvatarPreview(null)
      } else {
        alert(data.message)
      }
    } catch (error) {
      alert('Erro ao criar usuário')
    }
  }

  const handleDeleteUser = async (userId: string) => {
    if (!confirm(`Deletar usuário ${userId}?`)) return

    try {
      const res = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/${userId}`, {
        method: 'DELETE'
      })

      const data = await res.json()
      if (data.success) {
        fetchUsers()
      }
    } catch (error) {
      alert('Erro ao deletar usuário')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Carregando...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 to-dark-800 p-4 sm:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-4xl font-bold neon-text">👥 Gerenciar Usuários</h1>
          <div className="flex gap-2 sm:gap-4 w-full sm:w-auto">
            <button onClick={() => setShowCreateModal(true)} className="btn-neon px-4 sm:px-6 py-3 flex-1 sm:flex-none">
              <span className="hidden sm:inline">➕ Novo Usuário</span>
              <span className="sm:hidden">➕ Novo</span>
            </button>
            <button onClick={() => router.push('/dashboard')} className="btn-secondary px-4 sm:px-6 py-3 flex-1 sm:flex-none">
              <span className="hidden sm:inline">← Dashboard</span>
              <span className="sm:hidden">←</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {users.map(user => (
            <div key={user.user_id} className="glass-card p-6">
              <div className="flex justify-between items-start mb-4">
                {user.avatar_url ? (
                  <img 
                    src={user.avatar_url} 
                    alt={user.name}
                    className="w-16 h-16 rounded-full object-cover border-2 border-neon-cyan"
                  />
                ) : (
                  <div className="w-16 h-16 rounded-full bg-gray-700 flex items-center justify-center text-2xl">
                    👤
                  </div>
                )}
                <button
                  onClick={() => handleDeleteUser(user.user_id)}
                  className="p-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{user.name}</h3>
              <p className="text-sm text-gray-400 mb-1">ID: {user.user_id}</p>
              <p className="text-sm text-gray-400 mb-1">Pasta: {user.s3_prefix || 'Todas'}</p>
              {user.created_at && (
                <p className="text-xs text-gray-500">Criado: {new Date(user.created_at).toLocaleDateString('pt-BR')}</p>
              )}
            </div>
          ))}
        </div>

        {/* Modal Criar Usuário */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
            <div className="glass-card p-4 sm:p-8 max-w-md w-full my-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">Novo Usuário</h2>
                <button onClick={() => {
                  setShowCreateModal(false)
                  setQrCodeUri(null)
                }} className="text-gray-400 hover:text-white">
                  <X className="w-6 h-6" />
                </button>
              </div>

              {qrCodeUri ? (
                <div className="text-center">
                  <p className="text-green-400 mb-4">✅ Usuário criado com sucesso!</p>
                  <p className="text-white mb-4">Escaneie o QR Code no Google Authenticator:</p>
                  <img 
                    src={`https://api.qrserver.net/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrCodeUri)}`}
                    alt="QR Code 2FA"
                    className="mx-auto mb-4"
                  />
                  <button onClick={() => {
                    setShowCreateModal(false)
                    setQrCodeUri(null)
                  }} className="btn-neon w-full">
                    Fechar
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Avatar Upload */}
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
                      className="w-20 h-20 sm:w-24 sm:h-24 mx-auto rounded-full bg-gray-700 flex items-center justify-center cursor-pointer hover:bg-gray-600 transition-colors border-2 border-dashed border-gray-500 overflow-hidden touch-manipulation"
                    >
                      {avatarPreview ? (
                        <img src={avatarPreview} alt="Preview" className="w-full h-full object-cover" />
                      ) : (
                        <Upload className="w-8 h-8 text-gray-400" />
                      )}
                    </div>
                    <p className="text-xs text-gray-400 mt-2">Clique para enviar avatar</p>
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">User ID *</label>
                    <input
                      type="text"
                      value={newUser.user_id}
                      onChange={(e) => setNewUser({...newUser, user_id: e.target.value})}
                      className="input-neon"
                      placeholder="admin, user1, etc"
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Nome *</label>
                    <input
                      type="text"
                      value={newUser.name}
                      onChange={(e) => setNewUser({...newUser, name: e.target.value})}
                      className="input-neon"
                      placeholder="Administrador"
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Pasta S3 (opcional)</label>
                    <input
                      type="text"
                      value={newUser.s3_prefix}
                      onChange={(e) => setNewUser({...newUser, s3_prefix: e.target.value})}
                      className="input-neon"
                      placeholder="Deixe vazio para ver tudo"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Vazio = vê todos os arquivos | Ex: "user1/" = vê apenas pasta user1
                    </p>
                  </div>

                  <button onClick={handleCreateUser} className="btn-neon w-full">
                    Criar Usuário
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
