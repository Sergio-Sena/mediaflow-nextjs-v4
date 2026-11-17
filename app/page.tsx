import { Button } from '@/components/ui'
import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen" style={{ background: 'linear-gradient(315deg, #000000 0%, #0d0d1a 50%, #0a0a1f 100%)' }}>

      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-white/5" style={{ background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(20px)' }}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-xl font-bold tracking-tight">
            <span className="text-white">Mídia</span><span style={{ color: '#667eea' }}>flow</span>
          </div>
          <Link href="/login">
            <Button variant="primary" size="sm">Entrar</Button>
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-6 pt-24 pb-20 grid lg:grid-cols-2 gap-16 items-center">
        {/* Left */}
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium mb-8 border" style={{ background: 'rgba(102,126,234,0.1)', borderColor: 'rgba(102,126,234,0.3)', color: '#a5b4fc' }}>
            <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: '#667eea' }}></span>
            Plataforma privada · Acesso por convite
          </div>

          <h1 className="text-5xl lg:text-7xl font-bold leading-none tracking-tight mb-6">
            <span className="text-white">Sua mídia.</span>
            <br />
            <span style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Seu espaço.
            </span>
          </h1>

          <p className="text-lg text-gray-400 mb-10 leading-relaxed max-w-lg">
            Hospedagem de vídeos com CDN global, player premium e organização inteligente. Acesso exclusivo para membros.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <Link href="/login">
              <button className="px-8 py-4 rounded-xl font-semibold text-white transition-all duration-300 hover:-translate-y-1" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', boxShadow: '0 8px 30px rgba(102,126,234,0.4)' }}>
                Acessar Plataforma
              </button>
            </Link>
          </div>

          <div className="flex items-center gap-8 mt-12">
            <div>
              <div className="text-2xl font-bold text-white">99.9%</div>
              <div className="text-xs text-gray-500 mt-0.5">Uptime</div>
            </div>
            <div className="w-px h-8 bg-white/10"></div>
            <div>
              <div className="text-2xl font-bold text-white">400+</div>
              <div className="text-xs text-gray-500 mt-0.5">CDN POPs</div>
            </div>
            <div className="w-px h-8 bg-white/10"></div>
            <div>
              <div className="text-2xl font-bold text-white">&lt;50ms</div>
              <div className="text-xs text-gray-500 mt-0.5">Latência</div>
            </div>
          </div>
        </div>

        {/* Right — Player mockup + dashboard preview */}
        <div className="hidden lg:block relative">
          <div className="rounded-2xl overflow-hidden border border-white/10" style={{ background: 'rgba(255,255,255,0.03)', boxShadow: '0 40px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.05)' }}>

            {/* Player mockup */}
            <div className="aspect-video relative flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 50%, #0f0f2e 100%)' }}>
              {/* Ambient glow layers */}
              <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse at 30% 50%, rgba(102,126,234,0.18) 0%, transparent 60%)' }}></div>
              <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse at 70% 80%, rgba(118,75,162,0.12) 0%, transparent 50%)' }}></div>
              {/* Fake scan lines */}
              <div className="absolute inset-0 opacity-5" style={{ backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.3) 2px, rgba(255,255,255,0.3) 3px)', backgroundSize: '100% 4px' }}></div>
              {/* Play button */}
              <div className="w-16 h-16 rounded-full flex items-center justify-center border border-white/20 relative z-10 transition-transform hover:scale-110" style={{ background: 'rgba(102,126,234,0.25)', backdropFilter: 'blur(10px)', boxShadow: '0 0 40px rgba(102,126,234,0.3)' }}>
                <svg className="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              </div>
              {/* Bottom controls */}
              <div className="absolute bottom-0 left-0 right-0 p-4" style={{ background: 'linear-gradient(to top, rgba(0,0,0,0.7), transparent)' }}>
                <div className="h-1 rounded-full mb-2" style={{ background: 'rgba(255,255,255,0.1)' }}>
                  <div className="h-full rounded-full animate-pulse" style={{ width: '38%', background: 'linear-gradient(90deg, #667eea, #764ba2)' }}></div>
                </div>
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: '#667eea' }}></div>
                    <span className="text-xs" style={{ color: 'rgba(255,255,255,0.4)' }}>Reproduzindo</span>
                  </div>
                  <span className="text-xs" style={{ color: 'rgba(255,255,255,0.3)' }}>HD · CDN</span>
                </div>
              </div>
            </div>

            {/* Dashboard preview — category cards */}
            <div className="p-4">
              <p className="text-xs mb-3" style={{ color: 'rgba(255,255,255,0.3)' }}>Sua biblioteca</p>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { gradient: 'linear-gradient(135deg,#667eea,#764ba2)', label: 'Coleção A', count: '24 itens' },
                  { gradient: 'linear-gradient(135deg,#f093fb,#f5576c)', label: 'Série 01', count: '12 itens' },
                  { gradient: 'linear-gradient(135deg,#4facfe,#00f2fe)', label: 'Favoritos', count: '8 itens' },
                ].map((cat, i) => (
                  <div key={i} className="rounded-xl overflow-hidden border border-white/5">
                    <div className="h-14" style={{ background: cat.gradient, opacity: 0.7 }}></div>
                    <div className="px-2 py-1.5" style={{ background: 'rgba(255,255,255,0.03)' }}>
                      <p className="text-xs font-medium text-white/80 truncate">{cat.label}</p>
                      <p className="text-xs" style={{ color: 'rgba(255,255,255,0.3)' }}>{cat.count}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Glow */}
          <div className="absolute -inset-4 rounded-3xl opacity-20 blur-3xl -z-10" style={{ background: 'linear-gradient(135deg, #667eea, #764ba2)' }}></div>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-6 pb-24">
        <div className="grid md:grid-cols-3 gap-4">
          {[
            { icon: '▶', title: 'Player Premium', desc: 'Controles avançados, playlist automática e suporte a 4K com baixa latência.' },
            { icon: '⚡', title: 'CDN Global', desc: '400+ pontos de presença. Streaming fluido em qualquer lugar do mundo.' },
            { icon: '🗂', title: 'Organização Inteligente', desc: 'Pastas, categorias e busca instantânea para toda sua biblioteca.' },
          ].map((f, i) => (
            <div key={i} className="p-6 rounded-2xl border border-white/5 transition-all duration-300 hover:border-white/10" style={{ background: 'rgba(255,255,255,0.02)' }}>
              <div className="w-10 h-10 rounded-xl flex items-center justify-center text-lg mb-4" style={{ background: 'rgba(102,126,234,0.15)' }}>
                {f.icon}
              </div>
              <h3 className="font-semibold text-white mb-2">{f.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-2xl mx-auto px-6 pb-24 text-center">
        <div className="p-12 rounded-3xl border border-white/5" style={{ background: 'rgba(102,126,234,0.05)' }}>
          <h2 className="text-3xl font-bold text-white mb-3">Acesso exclusivo</h2>
          <p className="text-gray-400 mb-8">Esta plataforma é privada. Entre com suas credenciais ou solicite acesso ao administrador.</p>
          <Link href="/login">
            <button className="px-8 py-4 rounded-xl font-semibold text-white transition-all duration-300 hover:-translate-y-1" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', boxShadow: '0 8px 30px rgba(102,126,234,0.3)' }}>
              Entrar na Plataforma
            </button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-gray-600">
          <span><span className="text-white">Mídia</span><span style={{ color: '#667eea' }}>flow</span> · SSTechnologies</span>
          <div className="flex gap-6">
            <Link href="/termos" className="hover:text-gray-400 transition-colors">Termos</Link>
            <Link href="/privacidade" className="hover:text-gray-400 transition-colors">Privacidade</Link>
            <Link href="/sla" className="hover:text-gray-400 transition-colors">SLA</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
