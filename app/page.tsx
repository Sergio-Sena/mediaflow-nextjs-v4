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

      {/* Comparison Table */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-8">
          Por que <span className="neon-text">Mídiaflow</span>?
        </h2>
        
        <div className="glass-card p-6 overflow-x-auto mb-8">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left py-3 px-4">Recurso</th>
                <th className="text-center py-3 px-4">Mídiaflow</th>
                <th className="text-center py-3 px-4">Vimeo</th>
                <th className="text-center py-3 px-4">Wistia</th>
                <th className="text-center py-3 px-4">YouTube</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-gray-800">
                <td className="py-3 px-4">Preço (50GB)</td>
                <td className="text-center text-neon-cyan font-bold">R$ 49,90</td>
                <td className="text-center text-gray-400">R$ 60+</td>
                <td className="text-center text-gray-400">R$ 95+</td>
                <td className="text-center text-gray-400">Grátis</td>
              </tr>
              <tr className="border-b border-gray-800">
                <td className="py-3 px-4">Conversão 4K</td>
                <td className="text-center text-green-400">✓ Incluída</td>
                <td className="text-center text-red-400">✗ Paga extra</td>
                <td className="text-center text-red-400">✗</td>
                <td className="text-center text-green-400">✓</td>
              </tr>
              <tr className="border-b border-gray-800">
                <td className="py-3 px-4">Sem anúncios</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-red-400">✗</td>
              </tr>
              <tr className="border-b border-gray-800">
                <td className="py-3 px-4">White-label</td>
                <td className="text-center text-green-400">✓ Pro</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-red-400">✗</td>
              </tr>
              <tr className="border-b border-gray-800">
                <td className="py-3 px-4">API Completa</td>
                <td className="text-center text-green-400">✓ Pro</td>
                <td className="text-center text-gray-400">Planos caros</td>
                <td className="text-center text-green-400">✓</td>
                <td className="text-center text-green-400">✓</td>
              </tr>
              <tr>
                <td className="py-3 px-4">🎁 Storage de arquivos</td>
                <td className="text-center text-neon-cyan font-bold">✓ Bônus</td>
                <td className="text-center text-red-400">✗</td>
                <td className="text-center text-red-400">✗</td>
                <td className="text-center text-red-400">✗</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="glass-card p-6 text-center">
            <div className="text-3xl mb-2">💰</div>
            <h3 className="font-bold mb-2">50% mais barato</h3>
            <p className="text-sm text-gray-400">que Vimeo com mesmas features</p>
          </div>
          <div className="glass-card p-6 text-center">
            <div className="text-3xl mb-2">🎁</div>
            <h3 className="font-bold mb-2">Storage bônus</h3>
            <p className="text-sm text-gray-400">Armazene qualquer arquivo, não só vídeos</p>
          </div>
          <div className="glass-card p-6 text-center">
            <div className="text-3xl mb-2">🚀</div>
            <h3 className="font-bold mb-2">CDN Global</h3>
            <p className="text-sm text-gray-400">400+ edge locations, 99.9% uptime</p>
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
            <Link href="/termos" className="hover:text-neon-cyan">Termos</Link>
            <Link href="/privacidade" className="hover:text-neon-cyan">Privacidade</Link>
            <Link href="/sla" className="hover:text-neon-cyan">SLA</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}