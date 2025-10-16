'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

interface User {
  user_id: string
  name: string
  avatar?: string
  avatar_url?: string
  s3_prefix: string
}

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  
  useEffect(() => {
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
  
  const handleSelectUser = (userId: string) => {
    localStorage.setItem('selected_user', userId)
    router.push('/2fa')
  }
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-dark-900 to-dark-800">
        <div className="text-white text-xl">Carregando usuários...</div>
      </div>
    )
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 to-dark-800 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold neon-text mb-2 text-center">
          👥 Selecione um Perfil
        </h1>
        <p className="text-gray-400 text-center mb-8">
          Escolha o perfil que deseja acessar
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {users.map(user => (
            <div
              key={user.user_id}
              onClick={() => handleSelectUser(user.user_id)}
              className="glass-card p-8 text-center cursor-pointer hover:scale-105 hover:border-neon-cyan transition-all duration-300"
            >
              {user.avatar_url ? (
                <img 
                  src={user.avatar_url} 
                  alt={user.name}
                  className="w-24 h-24 rounded-full object-cover border-4 border-neon-cyan mx-auto mb-4"
                />
              ) : (
                <div className="text-7xl mb-4">{user.avatar || '👤'}</div>
              )}
              <h3 className="text-2xl font-semibold text-white mb-2">{user.name}</h3>
              <p className="text-sm text-gray-400">Clique para acessar</p>
              <div className="mt-4 text-xs text-gray-500">
                🔐 Requer 2FA
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-8 text-center">
          <button
            onClick={() => router.push('/login')}
            className="btn-secondary px-6 py-3"
          >
            ← Voltar ao Login
          </button>
        </div>
      </div>
    </div>
  )
}
