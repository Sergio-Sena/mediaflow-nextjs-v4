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
    <div className="min-h-screen relative overflow-hidden p-4 sm:p-8">
      {/* Cyberpunk Background */}
      <div className="fixed inset-0 bg-gradient-to-br from-[#0a0a1f] via-[#1a0a2e] to-[#0f0520] -z-10">
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-0 left-1/4 w-1 h-full bg-gradient-to-b from-cyan-500 via-purple-500 to-transparent animate-pulse" style={{animationDuration: '3s'}}></div>
          <div className="absolute top-0 left-1/2 w-1 h-full bg-gradient-to-b from-purple-500 via-pink-500 to-transparent animate-pulse" style={{animationDuration: '4s', animationDelay: '1s'}}></div>
          <div className="absolute top-0 left-3/4 w-1 h-full bg-gradient-to-b from-blue-500 via-cyan-500 to-transparent animate-pulse" style={{animationDuration: '3.5s', animationDelay: '0.5s'}}></div>
        </div>
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent"></div>
      </div>

      <div className="max-w-6xl mx-auto relative z-10">
        {/* Floating Title */}
        <div className="text-center mb-8 sm:mb-12 animate-float">
          <h1 className="text-3xl sm:text-5xl font-bold mb-3 relative inline-block">
            <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent drop-shadow-[0_0_30px_rgba(0,255,255,0.5)]">
              Selecione um Perfil
            </span>
            <div className="absolute -bottom-2 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-50 blur-sm"></div>
          </h1>
          <p className="text-sm sm:text-lg text-cyan-300/70 mt-4 drop-shadow-[0_0_10px_rgba(0,255,255,0.3)]">
            Escolha o perfil que deseja acessar
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {users.map(user => (
            <div
              key={user.user_id}
              onClick={() => handleSelectUser(user.user_id)}
              className="group relative p-6 sm:p-8 text-center cursor-pointer transition-all duration-500 touch-manipulation"
            >
              {/* Neon Border */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-cyan-500/20 via-purple-500/20 to-pink-500/20 opacity-50 group-hover:opacity-100 transition-opacity duration-500 animate-pulse-slow"></div>
              <div className="absolute inset-0 rounded-2xl border border-cyan-500/30 group-hover:border-cyan-400/60 group-hover:shadow-[0_0_30px_rgba(0,255,255,0.3)] transition-all duration-500"></div>
              
              {/* Glass Effect */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-gray-900/40 via-purple-900/20 to-gray-900/40 backdrop-blur-xl"></div>
              
              {/* Content */}
              <div className="relative z-10">
                {/* Avatar with Glow */}
                <div className="mb-6 relative group-hover:scale-110 transition-transform duration-500">
                  {user.avatar_url ? (
                    <div className="relative inline-block">
                      <div className="absolute inset-0 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 blur-xl opacity-50 group-hover:opacity-100 transition-opacity duration-500 animate-pulse"></div>
                      <img 
                        src={user.avatar_url} 
                        alt={user.name}
                        className="relative w-24 h-24 sm:w-28 sm:h-28 rounded-full object-cover border-2 border-cyan-400/50 shadow-[0_0_20px_rgba(0,255,255,0.3)]"
                      />
                    </div>
                  ) : (
                    <div className="relative inline-block">
                      <div className="absolute inset-0 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 blur-xl opacity-50 group-hover:opacity-100 transition-opacity duration-500 animate-pulse"></div>
                      <div className="relative text-6xl sm:text-7xl drop-shadow-[0_0_20px_rgba(0,255,255,0.5)]">{user.avatar || '👤'}</div>
                    </div>
                  )}
                </div>
                
                {/* Name with Glow */}
                <h3 className="text-xl sm:text-2xl font-bold mb-3 truncate bg-gradient-to-r from-cyan-300 to-purple-300 bg-clip-text text-transparent drop-shadow-[0_0_10px_rgba(0,255,255,0.3)]">
                  {user.name}
                </h3>
                
                {/* Action Text */}
                <p className="text-sm text-cyan-400/70 mb-4 group-hover:text-cyan-300 transition-colors duration-300">
                  Clique para acessar
                </p>
                
                {/* 2FA Badge */}
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/30 group-hover:border-purple-400/50 transition-all duration-300">
                  <div className="w-4 h-4 rounded-full bg-gradient-to-r from-cyan-400 to-purple-400 flex items-center justify-center shadow-[0_0_10px_rgba(0,255,255,0.5)]">
                    <span className="text-[10px]">🔒</span>
                  </div>
                  <span className="text-xs text-purple-300">Requer 2FA</span>
                </div>
              </div>
              
              {/* Hover Effect Lines */}
              <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-purple-500 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            </div>
          ))}
        </div>
        
        {/* Back Button */}
        <div className="mt-8 sm:mt-12 text-center">
          <button
            onClick={() => router.push('/login')}
            className="group relative px-8 py-4 w-full sm:w-auto overflow-hidden rounded-xl transition-all duration-300 hover:scale-105"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 to-purple-600 opacity-80 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-purple-500 blur-xl opacity-50 group-hover:opacity-75 transition-opacity duration-300"></div>
            <span className="relative flex items-center justify-center gap-2 text-white font-semibold">
              <span className="text-lg">←</span>
              <span>Voltar ao Login</span>
            </span>
          </button>
        </div>
      </div>
    </div>
  )
}
