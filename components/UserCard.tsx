interface UserCardProps {
  userId: string
  name: string
  avatar?: string
  onClick: () => void
}

export default function UserCard({ userId, name, avatar, onClick }: UserCardProps) {
  return (
    <div
      onClick={onClick}
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
        {/* Futuristic Profile Cards */}
        <div className="mb-6 relative group-hover:scale-110 transition-transform duration-500">
          {userId === 'admin' ? (
            // Admin Card: Futuristic user-gear/user-shield icon
            <div className="relative inline-block w-32 h-40 sm:w-36 sm:h-44">
              <div 
                className="w-full h-full rounded-xl relative"
                style={{
                  background: 'linear-gradient(135deg, #0a0a1f 0%, #1a1a2e 50%, #16213e 100%)',
                  border: '2px solid transparent',
                  backgroundImage: 'linear-gradient(135deg, #0a0a1f, #1a1a2e, #16213e), linear-gradient(90deg, #00bfff, #8a2be2)',
                  backgroundOrigin: 'border-box',
                  backgroundClip: 'content-box, border-box',
                  boxShadow: '0 0 20px rgba(0, 191, 255, 0.4), 0 0 40px rgba(138, 43, 226, 0.3)'
                }}
              >
                {/* Admin icon implementation */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="relative">
                    <div 
                      className="w-16 h-16 relative"
                      style={{
                        background: 'linear-gradient(135deg, rgba(0, 191, 255, 0.3), rgba(138, 43, 226, 0.3))',
                        clipPath: 'polygon(50% 0%, 90% 25%, 90% 75%, 50% 100%, 10% 75%, 10% 25%)',
                        filter: 'drop-shadow(0 0 15px rgba(0, 191, 255, 0.8))'
                      }}
                    >
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div 
                          className="w-8 h-8 rounded-full border-2"
                          style={{
                            borderColor: '#00bfff',
                            boxShadow: '0 0 10px rgba(0, 191, 255, 0.8)'
                          }}
                        >
                          <div className="absolute -top-1 left-1/2 w-1 h-2 bg-cyan-400 transform -translate-x-1/2"></div>
                          <div className="absolute -bottom-1 left-1/2 w-1 h-2 bg-cyan-400 transform -translate-x-1/2"></div>
                          <div className="absolute -left-1 top-1/2 h-1 w-2 bg-cyan-400 transform -translate-y-1/2"></div>
                          <div className="absolute -right-1 top-1/2 h-1 w-2 bg-cyan-400 transform -translate-y-1/2"></div>
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-2 h-2 rounded-full bg-purple-400"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            // Generic User Card
            <div className="relative inline-block w-32 h-40 sm:w-36 sm:h-44">
              <div 
                className="w-full h-full rounded-xl relative"
                style={{
                  background: 'linear-gradient(135deg, #0a0a1f 0%, #1a1a2e 50%, #16213e 100%)',
                  border: '2px solid transparent',
                  backgroundImage: 'linear-gradient(135deg, #0a0a1f, #1a1a2e, #16213e), linear-gradient(90deg, #00bfff, #8a2be2)',
                  backgroundOrigin: 'border-box',
                  backgroundClip: 'content-box, border-box',
                  boxShadow: '0 0 20px rgba(0, 191, 255, 0.4), 0 0 40px rgba(138, 43, 226, 0.3)'
                }}
              >
                {/* Generic user icon implementation */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="relative">
                    <div className="flex flex-col items-center">
                      <div 
                        className="w-12 h-12 rounded-full mb-2 relative"
                        style={{
                          background: 'linear-gradient(135deg, rgba(0, 191, 255, 0.4), rgba(138, 43, 226, 0.4))',
                          border: '2px solid rgba(0, 191, 255, 0.8)',
                          boxShadow: '0 0 15px rgba(0, 191, 255, 0.8)'
                        }}
                      ></div>
                      <div 
                        className="w-16 h-12 relative"
                        style={{
                          background: 'linear-gradient(180deg, rgba(0, 191, 255, 0.4), rgba(138, 43, 226, 0.4))',
                          clipPath: 'polygon(25% 0%, 75% 0%, 100% 100%, 0% 100%)',
                          border: '2px solid rgba(0, 191, 255, 0.8)',
                          boxShadow: '0 0 15px rgba(0, 191, 255, 0.8)'
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* User Name */}
        <h3 
          className="text-xl sm:text-2xl font-bold mb-3 truncate"
          style={{
            fontFamily: 'Inter, Montserrat, sans-serif',
            color: '#FFFFFF',
            textShadow: '0 0 10px rgba(0, 255, 255, 0.6), 0 0 20px rgba(139, 92, 246, 0.4)'
          }}
        >
          {name}
        </h3>
        
        {/* Action Text */}
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
          <div 
            className="text-sm"
            style={{
              filter: 'drop-shadow(0 0 8px #FFD700) drop-shadow(0 0 12px #FFA500)'
            }}
          >
            🔒
          </div>
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
    </div>
  )
}
