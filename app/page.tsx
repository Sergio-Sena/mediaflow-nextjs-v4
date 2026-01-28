import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
      {/* Header */}
      <header className="bg-dark-900/80 backdrop-blur-xl border-b border-neon-cyan/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold flex items-center gap-2">
            <span className="text-3xl">🎬</span>
            <span className="neon-text bg-gradient-to-r from-neon-cyan to-neon-purple bg-clip-text text-transparent">
              Mídiaflow
            </span>
          </div>
          <div className="flex gap-3">
            <Link href="/pricing" className="btn-ghost px-6 py-2.5 text-sm font-medium">
              Preços
            </Link>
            <Link href="/login" className="btn-primary px-6 py-2.5 text-sm font-medium">
              Entrar
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 px-4 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-neon-cyan/10 rounded-full blur-3xl animate-float"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-neon-purple/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
        </div>
        
        <div className="max-w-6xl mx-auto text-center relative z-10">
          <div className="mb-6">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-neon-cyan/10 border border-neon-cyan/20 rounded-full text-neon-cyan text-sm font-medium">
              <span className="w-2 h-2 bg-neon-cyan rounded-full animate-pulse"></span>
              Novo: Upload até 10GB por arquivo
            </span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-8 leading-tight">
            Hospede e Distribua
            <br />
            <span className="bg-gradient-to-r from-neon-cyan via-neon-purple to-neon-pink bg-clip-text text-transparent">
              Vídeos Profissionais
            </span>
          </h1>
          
          <p className="text-xl text-gray-300 mb-10 max-w-3xl mx-auto leading-relaxed">
            Plataforma completa com upload inteligente, conversão automática 4K e CDN global. 
            Usado por criadores, empresas e agências do mundo todo.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <Link href="/register" className="btn-primary px-8 py-4 text-lg font-semibold">
              🚀 Começar Grátis - 15 dias
            </Link>
            <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg font-semibold">
              Ver Preços
            </Link>
          </div>
          
          <div className="flex items-center justify-center gap-6 text-sm text-gray-400">
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 bg-accent-success rounded-full"></span>
              Sem cartão de crédito
            </span>
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 bg-accent-success rounded-full"></span>
              Cancele quando quiser
            </span>
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 bg-accent-success rounded-full"></span>
              Suporte 24/7
            </span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 py-12 sm:py-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-8">
          <div className="glass-card p-5 sm:p-6 text-center">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">📤</div>
            <h3 className="text-lg sm:text-xl font-bold mb-2">Upload Inteligente</h3>
            <p className="text-sm sm:text-base text-gray-400">Até 5GB por arquivo com drag & drop</p>
          </div>
          <div className="glass-card p-5 sm:p-6 text-center">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">🔄</div>
            <h3 className="text-lg sm:text-xl font-bold mb-2">Conversão 4K</h3>
            <p className="text-sm sm:text-base text-gray-400">H.264 automático em 1080p e 4K</p>
          </div>
          <div className="glass-card p-5 sm:p-6 text-center sm:col-span-2 md:col-span-1">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">🌍</div>
            <h3 className="text-lg sm:text-xl font-bold mb-2">CDN Global</h3>
            <p className="text-sm sm:text-base text-gray-400">400+ edge locations, 99.9% uptime</p>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="bg-dark-800/30 py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <div className="grid grid-cols-3 gap-4 sm:gap-8">
            <div>
              <div className="text-2xl sm:text-3xl font-bold text-neon-cyan mb-1 sm:mb-2">99.9%</div>
              <div className="text-xs sm:text-base text-gray-400">Uptime garantido</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-bold text-neon-purple mb-1 sm:mb-2">50%</div>
              <div className="text-xs sm:text-base text-gray-400">Mais barato</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-bold text-neon-cyan mb-1 sm:mb-2">15 dias</div>
              <div className="text-xs sm:text-base text-gray-400">Trial grátis</div>
            </div>
          </div>
        </div>
      </section>

      {/* Comparison Table */}
      <section className="max-w-7xl mx-auto px-4 py-12 sm:py-16">
        <h2 className="text-2xl sm:text-3xl font-bold text-center mb-6 sm:mb-8">
          Por que <span className="neon-text">Mídiaflow</span>?
        </h2>
        
        <div className="glass-card p-3 sm:p-6 overflow-x-auto mb-6 sm:mb-8">
          <table className="w-full text-xs sm:text-sm min-w-[500px]">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left py-2 sm:py-3 px-2 sm:px-4">Recurso</th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4">Mídiaflow</th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4">Vimeo</th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4">Wistia</th>
                <th className="text-center py-2 sm:py-3 px-2 sm:px-4">YouTube</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-gray-800">
                <td className="py-2 sm:py-3 px-2 sm:px-4">Preço (50GB)</td>
                <td className="text-center text-neon-cyan font-bold">R$ 49,90</td>
                <td className="text-center text-gray-400">R$ 60+</td>
                <td className="text-center text-gray-400">R$ 95+</td>
                <td className="text-center text-gray-400">Grátis</td>
              </tr>
              <tr className="border-b border-gray-800">
                <td className="py-2 sm:py-3 px-2 sm:px-4">Conversão 4K</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-red-400">✗</td>
                <td className="text-center text-red-400">✗</td>
                <td className="text-center text-green-400">✓</td>
              </tr>
              <tr className="border-b border-gray-800">
                <td className="py-2 sm:py-3 px-2 sm:px-4">Sem anúncios</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-red-400">✗</td>
              </tr>
              <tr className="border-b border-gray-800">
                <td className="py-2 sm:py-3 px-2 sm:px-4">White-label</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-red-400">✗</td>
              </tr>
              <tr className="border-b border-gray-800">
                <td className="py-2 sm:py-3 px-2 sm:px-4">API Completa</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-gray-400">Caros</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
              </tr>
              <tr>
                <td className="py-2 sm:py-3 px-2 sm:px-4">Storage bônus</td>
                <td className="text-center text-neon-cyan font-bold">✓</td>
                <td className="text-center text-red-400">✗</td>
                <td className="text-center text-red-400">✗</td>
                <td className="text-center text-red-400">✗</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
          <div className="glass-card p-5 sm:p-6 text-center">
            <div className="text-2xl sm:text-3xl mb-2">💰</div>
            <h3 className="text-base sm:text-lg font-bold mb-2">50% mais barato</h3>
            <p className="text-xs sm:text-sm text-gray-400">que o concorrente com mesmas features</p>
          </div>
          <div className="glass-card p-5 sm:p-6 text-center">
            <div className="text-2xl sm:text-3xl mb-2">🎁</div>
            <h3 className="text-base sm:text-lg font-bold mb-2">Storage bônus</h3>
            <p className="text-xs sm:text-sm text-gray-400">Armazene qualquer arquivo, não só vídeos</p>
          </div>
          <div className="glass-card p-5 sm:p-6 text-center sm:col-span-2 md:col-span-1">
            <div className="text-2xl sm:text-3xl mb-2">🚀</div>
            <h3 className="text-base sm:text-lg font-bold mb-2">CDN Global</h3>
            <p className="text-xs sm:text-sm text-gray-400">400+ edge locations, 99.9% uptime</p>
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="max-w-4xl mx-auto px-4 py-12 sm:py-16 text-center">
        <h2 className="text-2xl sm:text-3xl font-bold mb-3 sm:mb-4">
          Pronto para <span className="neon-text">começar</span>?
        </h2>
        <p className="text-base sm:text-xl text-gray-400 mb-6 sm:mb-8 px-2">
          15 dias grátis. Sem cartão de crédito. Cancele quando quiser.
        </p>
        <Link href="/register" className="btn-neon px-6 sm:px-8 py-3 sm:py-4 text-base sm:text-lg inline-block">
          🚀 Começar Grátis Agora
        </Link>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-6 sm:py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-xs sm:text-sm text-gray-400">
          <p className="mb-3 sm:mb-4">© 2025 Mídiaflow. Desenvolvido por SSTechnologies - Sergio Sena</p>
          <div className="flex flex-wrap justify-center gap-3 sm:gap-6">
            <Link href="/pricing" className="hover:text-neon-cyan">Preços</Link>
            <Link href="/docs" className="hover:text-neon-cyan">Docs</Link>
            <Link href="/termos" className="hover:text-neon-cyan">Termos</Link>
            <Link href="/privacidade" className="hover:text-neon-cyan">Privacidade</Link>
            <Link href="/sla" className="hover:text-neon-cyan">SLA</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}