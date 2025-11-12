import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-dark-900/50 backdrop-blur-md border-b border-neon-cyan/20">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold">
            🎬 <span className="neon-text">Mídiaflow</span>
          </div>
          <div className="flex gap-4">
            <Link href="/pricing" className="btn-secondary px-6 py-2">
              Preços
            </Link>
            <Link href="/login" className="btn-secondary px-6 py-2">
              Login
            </Link>
            <Link href="/register" className="btn-neon px-6 py-2">
              Começar Grátis
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative py-20 px-4">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-neon-cyan/5 to-transparent" />
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Hospede e Distribua Vídeos <span className="neon-text">Profissionais</span>
          </h1>
          <p className="text-xl text-gray-400 mb-8">
            Upload, conversão automática e CDN global. Usado por criadores, empresas e agências.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register" className="btn-neon px-8 py-4 text-lg">
              🚀 Começar Grátis - 14 dias
            </Link>
            <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">
              Ver Preços
            </Link>
          </div>
          <p className="text-sm text-gray-500 mt-4">
            Sem cartão de crédito • Cancele quando quiser
          </p>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="glass-card p-6 text-center">
            <div className="text-4xl mb-4">📤</div>
            <h3 className="text-xl font-bold mb-2">Upload Inteligente</h3>
            <p className="text-gray-400">Até 5GB por arquivo com drag & drop</p>
          </div>
          <div className="glass-card p-6 text-center">
            <div className="text-4xl mb-4">🔄</div>
            <h3 className="text-xl font-bold mb-2">Conversão 4K</h3>
            <p className="text-gray-400">H.264 automático em 1080p e 4K</p>
          </div>
          <div className="glass-card p-6 text-center">
            <div className="text-4xl mb-4">🌍</div>
            <h3 className="text-xl font-bold mb-2">CDN Global</h3>
            <p className="text-gray-400">400+ edge locations, 99.9% uptime</p>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="bg-dark-800/30 py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="text-3xl font-bold text-neon-cyan mb-2">99.9%</div>
              <div className="text-gray-400">Uptime garantido</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-neon-purple mb-2">50%</div>
              <div className="text-gray-400">Mais barato que Vimeo</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-neon-cyan mb-2">14 dias</div>
              <div className="text-gray-400">Trial grátis</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl font-bold mb-4">
          Pronto para <span className="neon-text">começar</span>?
        </h2>
        <p className="text-xl text-gray-400 mb-8">
          14 dias grátis. Sem cartão de crédito. Cancele quando quiser.
        </p>
        <Link href="/register" className="btn-neon px-8 py-4 text-lg inline-block">
          🚀 Começar Grátis Agora
        </Link>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-400">
          <p>© 2025 Mídiaflow. Desenvolvido por SSTechnologies - Sergio Sena</p>
          <div className="flex justify-center gap-6 mt-4">
            <Link href="/pricing" className="hover:text-neon-cyan">Preços</Link>
            <Link href="/docs" className="hover:text-neon-cyan">Docs</Link>
            <Link href="#" className="hover:text-neon-cyan">Contato</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}