import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="glass-card p-8 md:p-12 text-center w-4/5 mx-auto">
        <div className="mb-8">
          <div className="mb-6">
            <h1 className="text-4xl md:text-7xl lg:text-8xl mb-4">
              <span className="animate-float inline-block">🎬</span> <span className="neon-text-large">Mediaflow</span>
            </h1>
          </div>
          <div className="space-y-2">
            <p className="text-xl md:text-2xl text-gradient font-medium">
              Sistema de Streaming Modular
            </p>
            <p className="text-sm md:text-base text-gray-400">
              Next.js 14 + Node.js 22 + AWS
            </p>
            <div className="inline-block px-3 py-1 bg-neon-cyan/10 border border-neon-cyan/30 rounded-full">
              <span className="text-xs text-neon-cyan font-medium">v4.0.0 - Arquitetura Modular</span>
            </div>
          </div>
        </div>

        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
            <div className="glass-card-hover p-6 group text-center">
              <div className="text-2xl md:text-3xl mb-3 group-hover:animate-pulse-neon-fast transition-all duration-300">
                ✨
              </div>
              <h3 className="text-lg font-semibold text-neon-cyan mb-3">
                Funcionalidades
              </h3>
              <ul className="text-sm text-gray-300 space-y-2 text-left mx-auto w-fit">
                <li className="flex items-center gap-2">
                  <span className="text-neon-cyan">📤</span>
                  <span>Upload inteligente</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-purple">🔄</span>
                  <span>Conversão automática</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-blue">🎥</span>
                  <span>Player híbrido</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-green">🔐</span>
                  <span>Autenticação MFA</span>
                </li>
              </ul>
            </div>

            <div className="glass-card-hover p-6 group text-center">
              <div className="text-2xl md:text-3xl mb-3 group-hover:animate-pulse-neon-fast transition-all duration-300">
                🚀
              </div>
              <h3 className="text-lg font-semibold text-neon-purple mb-3">
                Tecnologias
              </h3>
              <ul className="text-sm text-gray-300 space-y-2 text-left mx-auto w-fit">
                <li className="flex items-center gap-2">
                  <span className="text-neon-cyan">⚡</span>
                  <span>Node.js 22</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-purple">🎨</span>
                  <span>Tailwind CSS</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-blue">☁️</span>
                  <span>AWS Services</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-green">🐳</span>
                  <span>Vercel Functions</span>
                </li>
              </ul>
            </div>

            <div className="glass-card-hover p-6 group md:col-span-2 lg:col-span-1 text-center">
              <div className="text-2xl md:text-3xl mb-3 group-hover:animate-pulse-neon-fast transition-all duration-300">
                📊
              </div>
              <h3 className="text-lg font-semibold text-neon-blue mb-3">
                Performance
              </h3>
              <ul className="text-sm text-gray-300 space-y-2 text-left mx-auto w-fit">
                <li className="flex items-center gap-2">
                  <span className="text-neon-cyan">⚡</span>
                  <span>Upload 4x mais rápido</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-purple">🎯</span>
                  <span>Conversão 50% menor</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-blue">💰</span>
                  <span>Custo otimizado</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-neon-green">🌐</span>
                  <span>CDN global</span>
                </li>
              </ul>
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
              
              <button className="btn-secondary px-6 py-3 inline-flex items-center gap-2">
                <span>📚</span>
                Documentação
              </button>
            </div>
            
            <div className="border-t border-neon-cyan/20 pt-6 mt-8">
              <div className="flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-gray-500">
                <div className="flex items-center gap-4">
                  <span className="px-2 py-1 bg-dark-800/50 rounded border border-neon-cyan/20">
                    Desenvolvido por Sergio Sena
                  </span>
                  <span className="px-2 py-1 bg-dark-800/50 rounded border border-neon-purple/20">
                    SStech
                  </span>
                </div>
                <div className="flex items-center gap-2 text-neon-cyan">
                  <div className="w-2 h-2 bg-neon-cyan rounded-full animate-pulse-neon-fast"></div>
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