import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="glass-card p-8 md:p-12 text-center w-4/5 mx-auto">
        <div className="mb-8">
          <div className="mb-6">
            <h1 className="text-4xl md:text-7xl lg:text-8xl mb-4">
              <span className="animate-float inline-block">🎬</span> <span className="neon-text-large">Mídiaflow</span>
            </h1>
          </div>
          <div className="space-y-2">
            <p className="text-xl md:text-2xl text-gradient font-medium">
              Sistema de Streaming Modular
            </p>

            <div className="inline-block px-3 py-1 bg-neon-cyan/10 border border-neon-cyan/30 rounded-full">
              <span className="text-xs text-neon-cyan font-medium">v4.0.0 - Arquitetura Modular</span>
            </div>
          </div>
        </div>

        <div className="space-y-8">
          {/* Hero Stats */}
          <div className="glass-card p-6 mb-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div className="space-y-2">
                <div className="text-2xl font-bold text-neon-cyan">99.9%</div>
                <div className="text-sm text-gray-400">Uptime</div>
              </div>
              <div className="space-y-2">
                <div className="text-2xl font-bold text-neon-purple">5GB</div>
                <div className="text-sm text-gray-400">Upload Máximo</div>
              </div>
              <div className="space-y-2">
                <div className="text-2xl font-bold text-neon-cyan">400+</div>
                <div className="text-sm text-gray-400">Edge Locations</div>
              </div>
              <div className="space-y-2">
                <div className="text-2xl font-bold text-neon-purple">95+</div>
                <div className="text-sm text-gray-400">Lighthouse Score</div>
              </div>
            </div>
          </div>

          {/* Feature Highlights */}
          <div className="text-center space-y-6">
            <h2 className="text-2xl md:text-3xl font-bold text-gradient">
              Plataforma Profissional de Streaming
            </h2>
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <span className="glass-card px-4 py-2 text-neon-cyan">
                📤 Upload Inteligente
              </span>
              <span className="glass-card px-4 py-2 text-neon-purple">
                🔄 Conversão H.264
              </span>
              <span className="glass-card px-4 py-2 text-neon-cyan">
                🎥 Player Sequencial
              </span>
              <span className="glass-card px-4 py-2 text-neon-purple">
                🔐 Multi-usuário 2FA
              </span>
              <span className="glass-card px-4 py-2 text-neon-cyan">
                ☁️ CDN Global
              </span>
            </div>
          </div>

          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link 
                href="/login" 
                className="btn-neon text-lg px-8 py-4 no-underline inline-flex items-center gap-2 group"
              >
                <span className="group-hover:animate-pulse-neon-fast">🚀</span>
                Acessar Sistema
              </Link>
              
              <Link 
                href="/docs" 
                className="btn-secondary px-6 py-3 inline-flex items-center gap-2 no-underline"
              >
                <span>📚</span>
                Documentação
              </Link>
            </div>
            
            <div className="border-t border-neon-cyan/20 pt-6 mt-8">
              <div className="text-center space-y-3">
                <div className="inline-block px-6 py-3 bg-gradient-to-r from-cyan-500/10 to-purple-500/10 border border-cyan-500/30 rounded-lg">
                  <p className="text-base font-semibold">
                    <span className="text-cyan-400">Desenvolvido por </span>
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">SSTechnologies</span>
                  </p>
                  <p className="text-sm text-gray-400 mt-1">Sergio Sena</p>
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