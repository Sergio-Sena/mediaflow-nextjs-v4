'use client'

import Link from 'next/link'
import { Check } from 'lucide-react'

export default function PricingPage() {
  const plans = [
    {
      name: 'Trial',
      price: 'Grátis',
      period: '15 dias',
      description: 'Teste todas as funcionalidades',
      features: [
        '10 GB de armazenamento',
        'Vídeos ilimitados',
        'Conversão 1080p',
        'Upload até 1 GB',
        '20 GB bandwidth/mês',
        'Player profissional',
      ],
      cta: 'Começar Grátis',
      href: '/register',
      popular: false,
    },
    {
      name: 'Basic',
      price: 'R$ 49,90',
      period: '/mês',
      description: 'Para criadores e pequenas empresas',
      features: [
        '25 GB de armazenamento',
        'Vídeos ilimitados',
        'Conversão 1080p ilimitada',
        'Sem marca d\'água',
        'Download habilitado',
        '🎁 Bônus: Armazene qualquer arquivo',
        '🎁 Bônus: Gerenciador de pastas',
      ],
      cta: 'Escolher Basic',
      href: '/register',
      popular: false,
    },
    {
      name: 'Pro',
      price: 'R$ 99,90',
      period: '/mês',
      description: 'Para profissionais e agências',
      features: [
        '200 GB de armazenamento',
        'Vídeos ilimitados',
        'Conversão 4K (30 min/mês)',
        'API completa',
        'Analytics avançado',
        'White-label (sem logo)',
        'Suporte prioritário',
        '🎁 Bônus: Backup profissional',
        '🎁 Bônus: Compartilhamento seguro',
      ],
      cta: 'Escolher Pro',
      href: '/register',
      popular: true,
    },
    {
      name: 'Enterprise',
      price: 'Sob consulta',
      period: '',
      description: 'Para grandes empresas',
      features: [
        'Storage customizado',
        'Multi-tenancy',
        'SLA 99.99%',
        'Suporte 24/7',
        'Gerente de conta dedicado',
        'Integração personalizada',
        'Treinamento da equipe',
      ],
      cta: 'Falar com Vendas',
      href: '#contato',
      popular: false,
    },
  ]

  const faqs = [
    {
      q: 'Posso cancelar a qualquer momento?',
      a: 'Sim! Sem multas ou taxas. Cancele quando quiser pelo dashboard.',
    },
    {
      q: 'Preciso de cartão de crédito no trial?',
      a: 'Não! 15 dias grátis sem precisar de cartão.',
    },
    {
      q: 'Quais formas de pagamento aceitam?',
      a: 'Cartão de crédito, boleto e PIX (planos anuais).',
    },
    {
      q: 'Tem desconto para pagamento anual?',
      a: 'Sim! 20% de desconto pagando anualmente.',
    },
    {
      q: 'O que acontece se eu ultrapassar o limite?',
      a: 'Você recebe um alerta por email. Pode fazer upgrade ou aguardar o próximo ciclo.',
    },
  ]

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-dark-900/50 backdrop-blur-md border-b border-neon-cyan/20">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            🎬 <span className="neon-text">Mídiaflow</span>
          </Link>
          <div className="flex gap-4">
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
      <section className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Planos <span className="neon-text">Simples e Transparentes</span>
        </h1>
        <p className="text-xl text-gray-400 mb-8">
          Hospede vídeos profissionais com CDN global. Cancele quando quiser.
        </p>
        <div className="inline-flex items-center gap-2 glass-card px-4 py-2 text-sm">
          <span className="text-green-400">✓</span>
          <span>15 dias grátis • Sem cartão de crédito • Cancele quando quiser</span>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="max-w-7xl mx-auto px-4 pb-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`glass-card p-6 relative ${
                plan.popular ? 'border-2 border-neon-cyan' : ''
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-neon-cyan to-neon-purple px-4 py-1 rounded-full text-xs font-bold">
                  MAIS POPULAR
                </div>
              )}
              
              <div className="text-center mb-6">
                <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                <div className="text-3xl font-bold text-neon-cyan mb-1">
                  {plan.price}
                </div>
                <div className="text-sm text-gray-400">{plan.period}</div>
                <p className="text-sm text-gray-400 mt-2">{plan.description}</p>
              </div>

              <ul className="space-y-3 mb-6">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <Check className="w-5 h-5 text-neon-cyan flex-shrink-0 mt-0.5" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              <Link
                href={plan.href}
                className={`block text-center py-3 rounded-lg font-semibold transition-all ${
                  plan.popular
                    ? 'btn-neon'
                    : 'btn-secondary'
                }`}
              >
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* Garantia de 30 Dias */}
      <section className="max-w-4xl mx-auto px-4 pb-16">
        <div className="glass-card p-8 border-2 border-green-500/30 bg-green-500/5">
          <div className="flex items-center justify-center gap-4 mb-4">
            <div className="text-4xl">🛡️</div>
            <h2 className="text-2xl font-bold">
              Garantia de <span className="text-green-400">30 Dias</span>
            </h2>
          </div>
          <p className="text-center text-gray-300 mb-6">
            Não gostou? Devolvemos <span className="font-bold text-green-400">100% do seu dinheiro</span>. Sem perguntas, sem burocracia.
          </p>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="text-center">
              <div className="text-green-400 font-bold mb-1">✓ Reembolso Total</div>
              <div className="text-gray-400">100% do valor pago</div>
            </div>
            <div className="text-center">
              <div className="text-green-400 font-bold mb-1">✓ Sem Perguntas</div>
              <div className="text-gray-400">Processo simples e rápido</div>
            </div>
            <div className="text-center">
              <div className="text-green-400 font-bold mb-1">✓ 7 Dias Úteis</div>
              <div className="text-gray-400">Dinheiro de volta</div>
            </div>
          </div>
          <div className="text-center mt-6">
            <Link href="/sla" className="text-neon-cyan hover:underline text-sm">
              Ver detalhes da garantia e SLA →
            </Link>
          </div>
        </div>
      </section>

      {/* Comparison */}
      <section className="max-w-7xl mx-auto px-4 pb-16">
        <h2 className="text-3xl font-bold text-center mb-8">
          Por que <span className="neon-text">Mídiaflow</span>?
        </h2>
        
        <div className="glass-card p-6 overflow-x-auto">
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

        <div className="grid md:grid-cols-3 gap-6 mt-8">
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

      {/* FAQ */}
      <section className="max-w-4xl mx-auto px-4 pb-16">
        <h2 className="text-3xl font-bold text-center mb-8">
          Perguntas <span className="neon-text">Frequentes</span>
        </h2>
        
        <div className="space-y-4">
          {faqs.map((faq, i) => (
            <div key={i} className="glass-card p-6">
              <h3 className="font-bold mb-2 text-neon-cyan">{faq.q}</h3>
              <p className="text-gray-400">{faq.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Final */}
      <section className="max-w-4xl mx-auto px-4 pb-16 text-center">
        <div className="glass-card p-12">
          <h2 className="text-3xl font-bold mb-4">
            Pronto para <span className="neon-text">começar</span>?
          </h2>
          <p className="text-xl text-gray-400 mb-8">
            15 dias grátis. Sem cartão de crédito. Cancele quando quiser.
          </p>
          <Link href="/register" className="btn-neon px-8 py-4 text-lg inline-block">
            🚀 Começar Grátis Agora
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-400">
          <p>© 2025 Mídiaflow. Todos os direitos reservados.</p>
          <div className="flex justify-center gap-6 mt-4">
            <Link href="#" className="hover:text-neon-cyan">Termos</Link>
            <Link href="#" className="hover:text-neon-cyan">Privacidade</Link>
            <Link href="#contato" className="hover:text-neon-cyan">Contato</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
