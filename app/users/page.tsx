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
      {/* Cyberpunk Data Tunnel Background */}
      <div className="fixed inset-0 bg-[#0a0a1f] -z-10 overflow-hidden">
        {/* Moving Neon Lines - Data Tunnel Effect */}
        <div className="absolute inset-0">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 bg-gradient-to-b opacity-40"
              style={{
                left: `${i * 5}%`,
                height: '200%',
                top: '-50%',
                background: i % 2 === 0 
                  ? 'linear-gradient(to bottom, #0ea5e9, #a855f7, transparent)'
                  : 'linear-gradient(to bottom, #8b5cf6, #ec4899, transparent)',
                animation: `moveDown ${3 + (i % 3)}s linear infinite`,
                animationDelay: `${i * 0.2}s`
              }}
            />
          ))}
        </div>
        {/* Depth Glow */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/30 via-blue-900/20 to-transparent"></div>
      </div>

      <div className="max-w-6xl mx-auto relative z-10">
        {/* Pulsing Neon Title */}
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="text-3xl sm:text-5xl font-bold mb-3 relative inline-block animate-pulse-text">
            <span className="bg-gradient-to-r from-cyan-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent" style={{
              textShadow: '0 0 20px rgba(6, 182, 212, 0.6), 0 0 40px rgba(139, 92, 246, 0.4)'
            }}>
              Selecione um Perfil
            </span>
          </h1>
          <p className="text-sm sm:text-lg animate-pulse-text" style={{
            color: '#67e8f9',
            textShadow: '0 0 10px rgba(103, 232, 249, 0.5)'
          }}>
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
                {/* 3D Abstract Avatar */}
                <div className="mb-6 relative group-hover:scale-110 transition-transform duration-500">
                  {user.avatar_url ? (
                    <div className="relative inline-block">
                      <div className="absolute inset-0 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 blur-2xl opacity-60 group-hover:opacity-100 transition-opacity duration-500 animate-pulse"></div>
                      <div className="relative w-24 h-24 sm:w-28 sm:h-28 rounded-full overflow-hidden border-2 border-cyan-400/50 shadow-[0_0_30px_rgba(0,255,255,0.5)]" style={{
                        background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2))',
                        backdropFilter: 'blur(10px)'
                      }}>
                        <img 
                          src={user.avatar_url} 
                          alt={user.name}
                          className="w-full h-full object-cover opacity-80 mix-blend-luminosity"
                        />
                      </div>
                    </div>
                  ) : (
                    user.user_id === 'admin' ? (
                      // Geometric Abstract Icon for Admin
                      <div className="relative inline-block w-24 h-24 sm:w-28 sm:h-28">
                        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-magenta-500 blur-2xl opacity-60 group-hover:opacity-100 transition-opacity duration-500 animate-pulse"></div>
                        <div className="relative w-full h-full animate-spin-slow">
                          <div className="absolute inset-0 border-4 border-cyan-400/50 rotate-45" style={{
                            clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)'
                          }}></div>
                          <div className="absolute inset-2 border-4 border-magenta-400/50 -rotate-45" style={{
                            clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)'
                          }}></div>
                          <div className="absolute inset-4 bg-gradient-to-br from-cyan-500/30 to-magenta-500/30 backdrop-blur-sm"></div>
                        </div>
                      </div>
                    ) : (
                      // Abstract Human Silhouette for Users
                      <div className="relative inline-block">
                        <div className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 blur-2xl opacity-60 group-hover:opacity-100 transition-opacity duration-500 animate-pulse"></div>
                        <div className="relative w-24 h-24 sm:w-28 sm:h-28 rounded-full border-2 border-purple-400/50 shadow-[0_0_30px_rgba(168,85,247,0.5)]" style={{
                          background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(236, 72, 153, 0.3))',
                          backdropFilter: 'blur(10px)'
                        }}>
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 opacity-80"></div>
                            <div className="absolute bottom-4 w-16 h-12 rounded-t-full bg-gradient-to-br from-purple-400 to-pink-400 opacity-80"></div>
                          </div>
                        </div>
                      </div>
                    )
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
