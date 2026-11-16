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

        {/* Right — Player mockup */}
        <div className="hidden lg:block relative">
          <div className="rounded-2xl overflow-hidden border border-white/10" style={{ background: 'rgba(255,255,255,0.03)', boxShadow: '0 40px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.05)' }}>
            {/* Fake player */}
            <div className="aspect-video relative flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 100%)' }}>
              <div className="absolute inset-0 opacity-20" style={{ background: 'radial-gradient(ellipse at center, #667eea 0%, transparent 70%)' }}></div>
              <div className="w-16 h-16 rounded-full flex items-center justify-center border border-white/20 relative z-10" style={{ background: 'rgba(102,126,234,0.2)', backdropFilter: 'blur(10px)' }}>
                <svg className="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
              {/* Progress bar */}
              <div className="absolute bottom-0 left-0 right-0 p-4">
                <div className="h-1 rounded-full bg-white/10 mb-3">
                  <div className="h-full w-2/5 rounded-full" style={{ background: 'linear-gradient(90deg, #667eea, #764ba2)' }}></div>
                </div>
                <div className="flex justify-between text-xs text-white/40">
                  <span>12:34</span><span>31:20</span>
                </div>
              </div>
            </div>
            {/* File list */}
            <div className="p-4 space-y-2">
              {['Anime / Stellar Blade', 'Anime / Final Fantasy', 'Anime / 2B Nier'].map((name, i) => (
                <div key={i} className={`flex items-center gap-3 px-3 py-2 rounded-lg ${i === 0 ? 'border border-white/10' : ''}`} style={{ background: i === 0 ? 'rgba(102,126,234,0.1)' : 'transparent' }}>
                  <div className="w-8 h-8 rounded flex items-center justify-center flex-shrink-0" style={{ background: 'rgba(102,126,234,0.2)' }}>
                    <svg className="w-4 h-4" style={{ color: '#667eea' }} fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                  </div>
                  <span className="text-sm text-white/70 truncate">{name}</span>
                  {i === 0 && <span className="ml-auto text-xs px-2 py-0.5 rounded-full" style={{ background: 'rgba(102,126,234,0.2)', color: '#a5b4fc' }}>Ativo</span>}
                </div>
              ))}
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
