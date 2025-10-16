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
              className="group relative p-6 sm:p-8 text-center cursor-pointer transition-all duration-500 touch-manipulation rounded-xl"
            >
              {/* Card Background - Dark with Transparency */}
              <div className="absolute inset-0 rounded-xl bg-[#0A0A1F] opacity-80 backdrop-blur-[5px]"></div>
              
              {/* Neon Border - Pulsing Cyan/Magenta */}
              <div 
                className="absolute inset-0 rounded-xl border-2 animate-neon-pulse"
                style={{
                  borderColor: '#00FFFF',
                  boxShadow: '0 0 10px #00FFFF, 0 0 20px #FF00FF, inset 0 0 10px rgba(0,255,255,0.1)'
                }}
              ></div>
              
              {/* Content */}
              <div className="relative z-10">
                {/* 3D Abstract Avatar Icons */}
                <div className="mb-6 relative group-hover:scale-110 transition-transform duration-500">
                  {user.avatar_url ? (
                    <div className="relative inline-block w-28 h-28 sm:w-32 sm:h-32">
                      <div className="absolute inset-0 rounded-full blur-xl opacity-70 animate-pulse" style={{
                        background: 'radial-gradient(circle, #FF66CC, #8B5CF6)'
                      }}></div>
                      <div className="relative w-full h-full rounded-full overflow-hidden" style={{
                        background: 'linear-gradient(135deg, rgba(255, 102, 204, 0.3), rgba(139, 92, 246, 0.3))',
                        boxShadow: 'inset 0 0 20px rgba(255, 102, 204, 0.5), 0 0 30px rgba(255, 102, 204, 0.3)'
                      }}>
                        <img 
                          src={user.avatar_url} 
                          alt={user.name}
                          className="w-full h-full object-cover opacity-90"
                          style={{ filter: 'brightness(1.1) contrast(1.1)' }}
                        />
                      </div>
                    </div>
                  ) : (
                    user.user_id === 'admin' ? (
                      // Admin: Geometric Complex Structure (Cyan Electric)
                      <div className="relative inline-block w-28 h-28 sm:w-32 sm:h-32">
                        <div className="absolute inset-0 blur-2xl opacity-70 animate-pulse" style={{
                          background: 'radial-gradient(circle, #00FFFF, #00CCCC)'
                        }}></div>
                        <div className="relative w-full h-full animate-spin-slow">
                          {/* Outer Hexagon */}
                          <div className="absolute inset-0" style={{
                            clipPath: 'polygon(50% 0%, 93% 25%, 93% 75%, 50% 100%, 7% 75%, 7% 25%)',
                            border: '3px solid #00FFFF',
                            boxShadow: '0 0 15px #00FFFF, inset 0 0 15px rgba(0,255,255,0.3)'
                          }}></div>
                          {/* Inner Diamond */}
                          <div className="absolute inset-4 rotate-45" style={{
                            border: '2px solid #FF00FF',
                            boxShadow: '0 0 10px #FF00FF, inset 0 0 10px rgba(255,0,255,0.3)'
                          }}></div>
                          {/* Center Glow */}
                          <div className="absolute inset-8 rounded-full" style={{
                            background: 'radial-gradient(circle, rgba(0,255,255,0.4), rgba(255,0,255,0.4))'
                          }}></div>
                        </div>
                      </div>
                    ) : (
                      // Maria Santos / João Silva: Abstract Human Silhouette
                      <div className="relative inline-block w-28 h-28 sm:w-32 sm:h-32">
                        <div className="absolute inset-0 rounded-full blur-xl opacity-70 animate-pulse" style={{
                          background: user.name.includes('Maria') 
                            ? 'radial-gradient(circle, #FF66CC, #FF1493)'
                            : 'radial-gradient(circle, #FFD700, #FFA500)'
                        }}></div>
                        <div className="relative w-full h-full rounded-full" style={{
                          background: user.name.includes('Maria')
                            ? 'linear-gradient(135deg, rgba(255, 102, 204, 0.4), rgba(255, 20, 147, 0.4))'
                            : 'linear-gradient(135deg, rgba(255, 215, 0, 0.4), rgba(255, 165, 0, 0.4))',
                          boxShadow: user.name.includes('Maria')
                            ? 'inset 0 0 20px rgba(255, 102, 204, 0.5), 0 0 30px rgba(255, 102, 204, 0.4)'
                            : 'inset 0 0 20px rgba(255, 215, 0, 0.5), 0 0 30px rgba(255, 215, 0, 0.4)'
                        }}>
                          {/* Abstract Human Shape */}
                          <div className="absolute inset-0 flex flex-col items-center justify-center">
                            {/* Head */}
                            <div className="w-10 h-10 rounded-full mb-1" style={{
                              background: user.name.includes('Maria')
                                ? 'linear-gradient(135deg, #FF66CC, #FF1493)'
                                : 'linear-gradient(135deg, #FFD700, #FFA500)',
                              opacity: 0.9
                            }}></div>
                            {/* Body */}
                            <div className="w-16 h-14 rounded-t-full" style={{
                              background: user.name.includes('Maria')
                                ? 'linear-gradient(180deg, #FF66CC, #FF1493)'
                                : 'linear-gradient(180deg, #FFD700, #FFA500)',
                              opacity: 0.9
                            }}></div>
                          </div>
                        </div>
                      </div>
                    )
                  )}
                </div>
                
                {/* User Name - Bold Sans-serif with Blue/Purple Glow */}
                <h3 
                  className="text-xl sm:text-2xl font-bold mb-3 truncate"
                  style={{
                    fontFamily: 'Inter, Montserrat, sans-serif',
                    color: '#FFFFFF',
                    textShadow: '0 0 10px rgba(0, 255, 255, 0.6), 0 0 20px rgba(139, 92, 246, 0.4)'
                  }}
                >
                  {user.name}
                </h3>
                
                {/* Action Text - Regular Sans-serif, Neutral White */}
                <p 
                  className="text-sm mb-4"
                  style={{
                    fontFamily: 'Inter, sans-serif',
                    color: '#FFFFFF'
                  }}
                >
                  Clique para acessar
                </p>
                
                {/* 2FA Security Indicator */}
                <div className="inline-flex items-center gap-2 px-3 py-1.5">
                  {/* Lock Icon with Yellow Neon Glow */}
                  <div 
                    className="text-sm"
                    style={{
                      filter: 'drop-shadow(0 0 8px #FFD700) drop-shadow(0 0 12px #FFA500)'
                    }}
                  >
                    🔒
                  </div>
                  {/* Text with Yellow Glow */}
                  <span 
                    className="text-xs"
                    style={{
                      fontFamily: 'Inter, sans-serif',
                      color: '#FFFACD',
                      textShadow: '0 0 8px rgba(255, 215, 0, 0.8), 0 0 12px rgba(255, 165, 0, 0.6)'
                    }}
                  >
                    Requer 2FA
                  </span>
                </div>
              </div>
              
              {/* Hover Effect Lines */}
              <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-purple-500 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            </div>
          ))}
        </div>
        
        {/* Back Button - Purple to Cyan Gradient with Neon Glow */}
        <div className="mt-8 sm:mt-12 text-center">
          <button
            onClick={() => router.push('/login')}
            className="group relative px-8 py-4 w-full sm:w-auto rounded-xl transition-all duration-300 hover:scale-105"
            style={{
              background: 'linear-gradient(90deg, #8B5CF6 0%, #00FFFF 100%)',
              boxShadow: '0 0 20px rgba(139, 92, 246, 0.5), 0 0 30px rgba(0, 255, 255, 0.3)',
              border: 'none'
            }}
          >
            <span 
              className="relative flex items-center justify-center gap-2 font-semibold"
              style={{
                fontFamily: 'Inter, sans-serif',
                color: '#FFFFFF',
                fontSize: '1rem'
              }}
            >
              <span className="text-lg">←</span>
              <span>Voltar ao Login</span>
            </span>
          </button>
        </div>
      </div>
    </div>
  )
}
