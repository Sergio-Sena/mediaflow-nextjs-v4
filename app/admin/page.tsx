'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { Upload, Trash2, X, Edit } from 'lucide-react'

interface User {
  user_id: string
  name: string
  email?: string
  role?: string
  avatar_url?: string
  s3_prefix: string
  created_at?: string
}

export default function AdminPage() {
  const [users, setUsers] = useState<User[]>([])
  const [pendingUsers, setPendingUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [newUser, setNewUser] = useState({ user_id: '', email: '', password: '', confirmPassword: '', name: '', s3_prefix: '', role: 'user' })
  const [editUser, setEditUser] = useState({ user_id: '', email: '', password: '', confirmPassword: '', role: 'user' })
  const [createLoading, setCreateLoading] = useState(false)
  const [editLoading, setEditLoading] = useState(false)
  const [createError, setCreateError] = useState('')
  const [editError, setEditError] = useState('')

  const generateUserId = (name: string) => {
    return name
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s]/g, '')
      .trim()
      .replace(/\s+/g, '_')
  }
  const [avatarFile, setAvatarFile] = useState<File | null>(null)
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null)
  const [qrCodeUri, setQrCodeUri] = useState<string | null>(null)
  const [show2FAModal, setShow2FAModal] = useState(false)
  const [twoFACode, setTwoFACode] = useState('')
  const [twoFAError, setTwoFAError] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }
    
    const session = localStorage.getItem('2fa_session')
    if (!session || (Date.now() - parseInt(session)) > 1800000) {
      setShow2FAModal(true)
      return
    }
    
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users')
      const data = await res.json()
      if (data.success) {
        const approved = data.users.filter((u: User & {status?: string}) => u.status !== 'pending')
        const pending = data.users.filter((u: User & {status?: string}) => u.status === 'pending')
        setUsers(approved)
        setPendingUsers(pending)
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
        role: newUser.role,
        s3_prefix: `${userId}/`
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
        setNewUser({ user_id: '', email: '', password: '', confirmPassword: '', name: '', s3_prefix: '', role: 'user' })
        setAvatarFile(null)
        setAvatarPreview(null)
      } else {
        setCreateError(data.message || 'Erro ao criar usuário')
      }
    } catch (error) {
      setCreateError('Erro ao criar usuário')
    } finally {
      setCreateLoading(false)
    }
  }

  const handleEditUser = async () => {
    setEditError('')

    if (!editUser.email) {
      setEditError('Email obrigatório')
      return
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(editUser.email)) {
      setEditError('Email inválido')
      return
    }

    if (editUser.password && editUser.password.length < 6) {
      setEditError('Senha deve ter no mínimo 6 caracteres')
      return
    }

    if (editUser.password && editUser.password !== editUser.confirmPassword) {
      setEditError('As senhas não coincidem')
      return
    }

    setEditLoading(true)
    try {
      const body: any = {
        user_id: editUser.user_id,
        email: editUser.email,
        role: editUser.role
      }

      if (editUser.password) {
        body.password = editUser.password
      }

      const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })

      const data = await res.json()
      
      if (data.success) {
        fetchUsers()
        setShowEditModal(false)
        setEditUser({ user_id: '', email: '', password: '', confirmPassword: '', role: 'user' })
      } else {
        setEditError(data.message || 'Erro ao atualizar usuário')
      }
    } catch (error) {
      setEditError('Erro ao atualizar usuário')
    } finally {
      setEditLoading(false)
    }
  }

  const handleApproveUser = async (userId: string, action: 'approve' | 'reject') => {
    try {
      const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, action })
      })
      const data = await res.json()
      if (data.success) {
        fetchUsers()
      }
    } catch (error) {
      alert('Erro ao processar aprovação')
    }
  }

  const handleDeleteUser = async (userId: string) => {
    if (!confirm(`Deletar usuário ${userId}?`)) return

    try {
      const res = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/${userId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const data = await res.json()
      if (data.success) {
        fetchUsers()
      }
    } catch (error) {
      alert('Erro ao deletar usuário')
    }
  }

  const handle2FAVerify = async () => {
    if (twoFACode.length !== 6) {
      setTwoFAError('Código deve ter 6 dígitos')
      return
    }

    try {
      const currentUser = JSON.parse(localStorage.getItem('current_user') || '{}')
      const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/verify-2fa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: currentUser.user_id, code: twoFACode })
      })

      const data = await res.json()
      if (data.success) {
        localStorage.setItem('2fa_session', Date.now().toString())
        setShow2FAModal(false)
        setTwoFACode('')
        setTwoFAError('')
        fetchUsers()
      } else {
        setTwoFAError(data.message || 'Código inválido')
      }
    } catch (error) {
      setTwoFAError('Erro ao verificar código')
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
          <h1 className="text-2xl sm:text-4xl font-bold neon-text">
            <span className="text-neon-cyan">👥</span> Gerenciar Usuários
          </h1>
          <div className="flex gap-2 sm:gap-4 w-full sm:w-auto">
            <button
              onClick={() => {
                localStorage.removeItem('token')
                localStorage.removeItem('current_user')
                localStorage.removeItem('2fa_session')
                router.push('/users')
              }}
              className="btn-secondary px-4 sm:px-6 py-3 flex-1 sm:flex-none"
            >
              <span className="hidden sm:inline">🔄 Trocar</span>
              <span className="sm:hidden">🔄</span>
            </button>
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

        {pendingUsers.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-yellow-400 mb-4">⏳ Aprovações Pendentes ({pendingUsers.length})</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
              {pendingUsers.map(user => (
                <div key={user.user_id} className="glass-card p-6 border-2 border-yellow-500/50">
                  <div className="flex justify-between items-start mb-4">
                    {user.avatar_url ? (
                      <img 
                        src={user.avatar_url} 
                        alt={user.name}
                        className="w-16 h-16 rounded-full object-cover border-2 border-yellow-400"
                      />
                    ) : (
                      <div className="w-16 h-16 rounded-full bg-gray-700 flex items-center justify-center text-2xl">
                        👤
                      </div>
                    )}
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">{user.name}</h3>
                  <p className="text-sm text-gray-400 mb-1">Email: {user.email || 'N/A'}</p>
                  <p className="text-sm text-gray-400 mb-4">ID: {user.user_id}</p>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleApproveUser(user.user_id, 'approve')}
                      className="flex-1 px-4 py-2 bg-green-500/20 hover:bg-green-500/30 text-green-400 rounded-lg transition-colors font-semibold"
                    >
                      ✅ Aprovar
                    </button>
                    <button
                      onClick={() => handleApproveUser(user.user_id, 'reject')}
                      className="flex-1 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors font-semibold"
                    >
                      ❌ Rejeitar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <h2 className="text-2xl font-bold text-white mb-4">✅ Usuários Aprovados ({users.length})</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {users.map(user => (
            <div key={user.user_id} className="glass-card p-6 min-h-[200px] flex flex-col">
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
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      setEditUser({ 
                        user_id: user.user_id, 
                        email: user.email || '', 
                        password: '', 
                        confirmPassword: '', 
                        role: user.role || 'user' 
                      })
                      setShowEditModal(true)
                    }}
                    className="p-2 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 rounded-lg transition-colors"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteUser(user.user_id)}
                    className="p-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{user.name}</h3>
              <p className="text-sm text-gray-400 mb-1">ID: {user.user_id}</p>
              <p className="text-sm text-gray-400 mb-1">Email: {user.email || 'N/A'}</p>
              <p className="text-sm text-gray-400 mb-1">Role: {user.role === 'admin' ? '👑 Admin' : '👤 User'}</p>
              <p className="text-sm text-gray-400 mb-1">Pasta: {user.s3_prefix || 'Todas'}</p>
              {user.created_at && (
                <p className="text-xs text-gray-500">Criado: {new Date(user.created_at).toLocaleDateString('pt-BR')}</p>
              )}
            </div>
          ))}
        </div>

        {/* Modal 2FA */}
        {show2FAModal && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="glass-card p-8 max-w-md w-full">
              <div className="text-center mb-6">
                <h2 className="text-2xl font-bold neon-text mb-2">🔐 Verificação 2FA</h2>
                <p className="text-gray-400">Insira o código do Google Authenticator</p>
              </div>
              
              <div className="mb-6">
                <input
                  type="text"
                  maxLength={6}
                  value={twoFACode}
                  onChange={(e) => setTwoFACode(e.target.value.replace(/\D/g, ''))}
                  onKeyPress={(e) => e.key === 'Enter' && twoFACode.length === 6 && handle2FAVerify()}
                  placeholder="000000"
                  className="w-full px-4 py-4 bg-dark-800 border border-gray-700 rounded-lg text-center text-2xl tracking-widest text-white focus:border-neon-cyan focus:outline-none"
                  autoFocus
                />
                
                {twoFAError && (
                  <p className="text-red-400 text-sm mt-3 text-center">{twoFAError}</p>
                )}
              </div>
              
              <button 
                onClick={handle2FAVerify}
                className="btn-neon w-full mb-3"
                disabled={twoFACode.length !== 6}
              >
                Verificar Código
              </button>
              
              <button 
                onClick={() => router.push('/users')}
                className="btn-secondary w-full"
              >
                ← Voltar aos Perfis
              </button>
            </div>
          </div>
        )}

        {/* Modal Editar Usuário */}
        {showEditModal && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
            <div className="glass-card p-4 sm:p-8 max-w-md w-full my-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">Editar Usuário</h2>
                <button onClick={() => {
                  setShowEditModal(false)
                  setEditError('')
                }} className="text-gray-400 hover:text-white">
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-4">
                {editError && (
                  <div className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg">
                    <p className="text-red-400 text-sm text-center">{editError}</p>
                  </div>
                )}

                <div>
                  <label className="block text-sm text-gray-400 mb-2">User ID (não editável)</label>
                  <input
                    type="text"
                    value={editUser.user_id}
                    className="input-neon bg-gray-800 cursor-not-allowed text-gray-400"
                    disabled
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">Email *</label>
                  <input
                    type="email"
                    value={editUser.email}
                    onChange={(e) => setEditUser({...editUser, email: e.target.value})}
                    className="input-neon"
                    placeholder="usuario@email.com"
                    disabled={editLoading}
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">Role *</label>
                  <select
                    value={editUser.role}
                    onChange={(e) => setEditUser({...editUser, role: e.target.value})}
                    className="input-neon"
                    disabled={editLoading}
                  >
                    <option value="user">👤 User (vê apenas sua pasta)</option>
                    <option value="admin">👑 Admin (vê tudo)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">Nova Senha (deixe vazio para não alterar)</label>
                  <input
                    type="password"
                    value={editUser.password}
                    onChange={(e) => setEditUser({...editUser, password: e.target.value})}
                    className="input-neon"
                    placeholder="••••••••"
                    disabled={editLoading}
                  />
                  {editUser.password && editUser.password.length < 6 && (
                    <p className="text-xs text-yellow-400 mt-1">⚠️ Senha muito curta</p>
                  )}
                </div>

                {editUser.password && (
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Confirmar Nova Senha</label>
                    <input
                      type="password"
                      value={editUser.confirmPassword}
                      onChange={(e) => setEditUser({...editUser, confirmPassword: e.target.value})}
                      className="input-neon"
                      placeholder="••••••••"
                      disabled={editLoading}
                    />
                    {editUser.confirmPassword && editUser.password !== editUser.confirmPassword && (
                      <p className="text-xs text-red-400 mt-1">❌ Senhas não coincidem</p>
                    )}
                    {editUser.confirmPassword && editUser.password === editUser.confirmPassword && editUser.password.length >= 6 && (
                      <p className="text-xs text-green-400 mt-1">✅ Senhas coincidem</p>
                    )}
                  </div>
                )}

                <button 
                  onClick={handleEditUser} 
                  className="btn-neon w-full"
                  disabled={editLoading || !editUser.email}
                >
                  {editLoading ? (
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-4 h-4 border-2 border-dark-900 border-t-transparent rounded-full animate-spin"></div>
                      Atualizando...
                    </div>
                  ) : (
                    'Atualizar Usuário'
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

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
                  <div className="mb-4 p-4 bg-green-500/20 border border-green-500/50 rounded-lg">
                    <p className="text-green-400 font-semibold">✅ Usuário criado com sucesso!</p>
                  </div>
                  <p className="text-white mb-4">Escaneie o QR Code no Google Authenticator:</p>
                  <img 
                    src={`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrCodeUri)}`}
                    alt="QR Code 2FA"
                    className="mx-auto mb-4"
                  />
                  <button onClick={() => {
                    setShowCreateModal(false)
                    setQrCodeUri(null)
                    setCreateError('')
                  }} className="btn-neon w-full">
                    Fechar
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {createError && (
                    <div className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg">
                      <p className="text-red-400 text-sm text-center">{createError}</p>
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
                    <label className="block text-sm text-gray-400 mb-2">Nome *</label>
                    <input
                      type="text"
                      value={newUser.name}
                      onChange={(e) => {
                        const name = e.target.value
                        const userId = generateUserId(name)
                        setNewUser({...newUser, name, user_id: userId, s3_prefix: `${userId}/`})
                      }}
                      className="input-neon"
                      placeholder="João Silva"
                      disabled={createLoading}
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">
                      User ID (gerado automaticamente)
                      <span className="ml-2 text-xs text-neon-cyan" title="Gerado automaticamente a partir do nome">ℹ️</span>
                    </label>
                    <input
                      type="text"
                      value={newUser.user_id || 'Digite o nome acima...'}
                      className="input-neon bg-gray-800 cursor-not-allowed text-gray-400"
                      placeholder="joao_silva"
                      disabled
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Email *</label>
                    <input
                      type="email"
                      value={newUser.email}
                      onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                      className="input-neon"
                      placeholder="joao@email.com"
                      disabled={createLoading}
                    />
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Senha * (mínimo 6 caracteres)</label>
                    <input
                      type="password"
                      value={newUser.password}
                      onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                      className="input-neon"
                      placeholder="••••••••"
                      disabled={createLoading}
                    />
                    {newUser.password && newUser.password.length < 6 && (
                      <p className="text-xs text-yellow-400 mt-1">⚠️ Senha muito curta</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Confirmar Senha *</label>
                    <input
                      type="password"
                      value={newUser.confirmPassword}
                      onChange={(e) => setNewUser({...newUser, confirmPassword: e.target.value})}
                      className="input-neon"
                      placeholder="••••••••"
                      disabled={createLoading}
                    />
                    {newUser.confirmPassword && newUser.password !== newUser.confirmPassword && (
                      <p className="text-xs text-red-400 mt-1">❌ Senhas não coincidem</p>
                    )}
                    {newUser.confirmPassword && newUser.password === newUser.confirmPassword && newUser.password.length >= 6 && (
                      <p className="text-xs text-green-400 mt-1">✅ Senhas coincidem</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Role *</label>
                    <select
                      value={newUser.role}
                      onChange={(e) => setNewUser({...newUser, role: e.target.value})}
                      className="input-neon"
                      disabled={createLoading}
                    >
                      <option value="user">👤 User (vê apenas sua pasta)</option>
                      <option value="admin">👑 Admin (vê tudo)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">
                      Pasta S3 (gerada automaticamente)
                      <span className="ml-2 text-xs text-neon-cyan" title="Usuário verá apenas arquivos desta pasta">ℹ️</span>
                    </label>
                    <input
                      type="text"
                      value={newUser.s3_prefix || 'Digite o nome acima...'}
                      className="input-neon bg-gray-800 cursor-not-allowed text-gray-400"
                      placeholder="joao_silva/"
                      disabled
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      {newUser.role === 'admin' ? 'Admin vê todos os arquivos' : 'User vê apenas arquivos da sua pasta'}
                    </p>
                  </div>

                  <button 
                    onClick={handleCreateUser} 
                    className="btn-neon w-full"
                    disabled={createLoading || !newUser.name || !newUser.email || !newUser.password || !newUser.confirmPassword}
                  >
                    {createLoading ? (
                      <div className="flex items-center justify-center gap-2">
                        <div className="w-4 h-4 border-2 border-dark-900 border-t-transparent rounded-full animate-spin"></div>
                        Criando...
                      </div>
                    ) : (
                      'Criar Usuário'
                    )}
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
