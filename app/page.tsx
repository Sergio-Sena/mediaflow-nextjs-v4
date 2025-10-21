import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-20"
        style={{ backgroundImage: 'url(/Gemini_Generated_Image_2fjorj2fjorj2fjo.png)' }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/70" />
      <div className="relative z-10 text-center">
        <div className="mb-8">
          <div className="mb-6">
            <h1 className="text-4xl md:text-6xl lg:text-7xl mb-6 font-black">
              <span className="animate-float inline-block">🎬</span> <span className="text-blue-300 relative">
                Mídiaflow
                <div className="absolute inset-0 bg-blue-400/20 rounded-lg blur-md animate-pulse -z-10"></div>
              </span>
            </h1>
          </div>
          <div className="space-y-2">
            <p className="text-2xl md:text-3xl text-gradient font-bold">
              Sistema de Streaming Modular
            </p>
          </div>
        </div>

        <div className="space-y-16">
          {/* Hero Stats */}
          <div className="glass-card p-6 md:p-8 hover:scale-105 transition-transform duration-300">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div className="space-y-2">
                <div className="text-2xl md:text-3xl font-bold text-neon-cyan">🟢 99.9%</div>
                <div className="text-sm text-gray-400">Uptime</div>
              </div>
              <div className="space-y-2">
                <div className="text-2xl md:text-3xl font-bold text-neon-purple">🚀 Ilimitado</div>
                <div className="text-sm text-gray-400">Upload Multipart</div>
              </div>
              <div className="space-y-2">
                <div className="text-2xl md:text-3xl font-bold text-neon-cyan">🌍 400+</div>
                <div className="text-sm text-gray-400">Edge Locations</div>
              </div>
              <div className="space-y-2">
                <div className="text-2xl md:text-3xl font-bold text-neon-purple">⚡ 95+</div>
                <div className="text-sm text-gray-400">Lighthouse Score</div>
              </div>
            </div>
          </div>
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-4xl mx-auto">
              <div className="glass-card p-4 text-center hover:scale-105 transition-all duration-300 bg-gradient-to-r from-cyan-500/10 to-cyan-500/5">
                <div className="text-2xl mb-2">📤</div>
                <div className="text-neon-cyan font-semibold">Upload Inteligente</div>
              </div>
              <div className="glass-card p-4 text-center hover:scale-105 transition-all duration-300 bg-gradient-to-r from-purple-500/10 to-purple-500/5">
                <div className="text-2xl mb-2">🔄</div>
                <div className="text-neon-purple font-semibold">Conversão H.264</div>
              </div>
              <div className="glass-card p-4 text-center hover:scale-105 transition-all duration-300 bg-gradient-to-r from-cyan-500/10 to-cyan-500/5">
                <div className="text-2xl mb-2">🎥</div>
                <div className="text-neon-cyan font-semibold">Player Sequencial</div>
              </div>
              <div className="glass-card p-4 text-center hover:scale-105 transition-all duration-300 bg-gradient-to-r from-purple-500/10 to-purple-500/5">
                <div className="text-2xl mb-2">🔐</div>
                <div className="text-neon-purple font-semibold">Multi-usuário 2FA</div>
              </div>
              <div className="glass-card p-4 text-center hover:scale-105 transition-all duration-300 bg-gradient-to-r from-cyan-500/10 to-cyan-500/5">
                <div className="text-2xl mb-2">☁️</div>
                <div className="text-neon-cyan font-semibold">CDN Global</div>
              </div>
            </div>

          {/* Feature Highlights */}
          <div className="text-left space-y-6">
            <h2 className="text-2xl md:text-3xl font-bold text-gradient">
              Filmes, fotos, vídeos, ae em nuvem e mais.
            </h2>
            <p className="text-lg text-gray-300 mt-2">
              Comece agora
            </p>
           
          </div>

          <div className="space-y-6">
            <div className="flex justify-center">
              <Link 
                href="/login" 
                className="btn-neon text-lg px-8 py-4 no-underline inline-flex items-center gap-2 group transform hover:scale-105 transition-all duration-300"
              >
                <span className="group-hover:animate-pulse-neon-fast">🚀</span>
                Acessar Sistema
              </Link>
            </div>
            
            <div className="border-t border-neon-cyan/20 pt-6 mt-8">
              <div className="text-center space-y-4">
                <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                  <div className="inline-block px-6 py-3 bg-gradient-to-r from-cyan-500/10 to-purple-500/10 border border-cyan-500/30 rounded-lg">
                    <p className="text-base font-semibold">
                      <span className="text-cyan-400">Desenvolvido por </span>
                      <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">SSTechnologies</span>
                    </p>
                    <p className="text-sm text-gray-400 mt-1">Sergio Sena</p>
                  </div>
                  
                  <Link 
                    href="/docs" 
                    className="btn-secondary px-6 py-3 inline-flex items-center gap-2 no-underline transform hover:scale-105 transition-all duration-300"
                  >
                    <span>📚</span>
                    Documentação
                  </Link>
                </div>
                <div className="flex items-center justify-center gap-2 text-xs text-neon-cyan">
                  <div className="w-2 h-2 bg-neon-cyan rounded-full animate-pulse"></div>
                  <span>Sistema Online</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Elementos decorativos */}
        <div className="absolute -top-4 -right-4 w-24 h-24 bg-neon-cyan/5 rounded-full blur-xl animate-pulse opacity-50"></div>
        <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-neon-purple/5 rounded-full blur-xl animate-pulse opacity-50"></div>
      </div>
    </div>
  )
}