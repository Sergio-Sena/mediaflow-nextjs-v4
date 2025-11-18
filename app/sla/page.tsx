'use client'

import Link from 'next/link'

export default function SLAPage() {
  return (
    <div className="min-h-screen bg-dark-950">
      <header className="bg-dark-900/50 backdrop-blur-md border-b border-neon-cyan/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            🎬 <span className="neon-text">Mídiaflow</span>
          </Link>
          <div className="flex gap-4">
            <Link href="/pricing" className="btn-secondary px-6 py-2">Ver Planos</Link>
            <Link href="/register" className="btn-neon px-6 py-2">Começar Grátis</Link>
          </div>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          🛡️ <span className="neon-text">Garantias e SLA</span>
        </h1>
        <p className="text-xl text-gray-400">
          Transparência total sobre nossos compromissos de disponibilidade e qualidade.
        </p>
      </section>

      <article className="max-w-4xl mx-auto px-4 pb-16">
        <section className="glass-card p-8 mb-8">
          <h2 className="text-3xl font-bold mb-6 text-neon-cyan">⏱️ Uptime Garantido por Plano</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-dark-800/50 p-6 rounded-lg border border-gray-700">
              <h3 className="text-xl font-bold mb-3">Trial (Grátis - 15 dias)</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li><strong>Disponibilidade:</strong> 99.5%</li>
                <li><strong>Downtime máximo:</strong> 3h 36min/mês</li>
                <li><strong>Suporte:</strong> Email 48h</li>
                <li><strong>Compensação:</strong> Não aplicável</li>
              </ul>
            </div>

            <div className="bg-dark-800/50 p-6 rounded-lg border border-neon-cyan/30">
              <h3 className="text-xl font-bold mb-3">Basic (R$ 49,90/mês)</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li><strong>Disponibilidade:</strong> 99.9%</li>
                <li><strong>Downtime máximo:</strong> 43 min/mês</li>
                <li><strong>Suporte:</strong> Email 24h</li>
                <li><strong>Compensação:</strong> 10% crédito</li>
              </ul>
            </div>

            <div className="bg-dark-800/50 p-6 rounded-lg border border-neon-purple/30">
              <h3 className="text-xl font-bold mb-3">Pro (R$ 99,90/mês)</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li><strong>Disponibilidade:</strong> 99.95%</li>
                <li><strong>Downtime máximo:</strong> 21 min/mês</li>
                <li><strong>Suporte:</strong> Prioritário 4h</li>
                <li><strong>Compensação:</strong> 15% crédito</li>
              </ul>
            </div>

            <div className="bg-dark-800/50 p-6 rounded-lg border border-neon-pink/30">
              <h3 className="text-xl font-bold mb-3">Enterprise</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li><strong>Disponibilidade:</strong> 99.99%</li>
                <li><strong>Downtime máximo:</strong> 4 min/mês</li>
                <li><strong>Suporte:</strong> 24/7 dedicado</li>
                <li><strong>Compensação:</strong> 25% crédito</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="glass-card p-8 mb-8 border-2 border-green-500/30 bg-green-500/5">
          <h2 className="text-3xl font-bold mb-4 text-green-400">🛡️ Garantia de 30 Dias</h2>
          <p className="text-xl text-gray-300 mb-6">Teste sem riscos. Se não gostar, devolvemos tudo.</p>
          <ul className="space-y-2 text-gray-300 mb-6">
            <li>✅ Reembolso de 100% do valor pago</li>
            <li>✅ Sem perguntas ou justificativas</li>
            <li>✅ Processamento em até 7 dias úteis</li>
          </ul>
          <div className="bg-dark-800/50 p-4 rounded-lg text-sm">
            <p className="text-gray-300 mb-2"><strong>Como solicitar:</strong></p>
            <p className="text-gray-400">Email: <span className="text-neon-cyan">suporte@midiaflow.com</span> | Assunto: "Solicitação de Reembolso"</p>
          </div>
        </section>

        <section className="glass-card p-8 mb-8">
          <h2 className="text-3xl font-bold mb-6 text-neon-cyan">❓ Perguntas Frequentes</h2>
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-bold text-neon-cyan mb-2">O que acontece se ficarem offline mais que o prometido?</h3>
              <p className="text-gray-300">Você recebe créditos automaticamente na próxima fatura.</p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-neon-cyan mb-2">Como sei se houve problema?</h3>
              <p className="text-gray-300">Acesse <strong>status.midiaflow.com</strong> ou receba notificações por email.</p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-neon-cyan mb-2">Posso cancelar quando quiser?</h3>
              <p className="text-gray-300">Sim! Sem multas, sem taxas. Cancele direto no dashboard.</p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-neon-cyan mb-2">A garantia de 30 dias é real?</h3>
              <p className="text-gray-300">Sim! Reembolso de 100% sem perguntas.</p>
            </div>
          </div>
        </section>
      </article>

      <section className="max-w-4xl mx-auto px-4 pb-16">
        <div className="glass-card p-12 text-center">
          <h2 className="text-3xl font-bold mb-4">Pronto para <span className="neon-text">começar</span>?</h2>
          <p className="text-xl text-gray-400 mb-8">15 dias grátis. Sem cartão. Cancele quando quiser.</p>
          <div className="flex gap-4 justify-center">
            <Link href="/register" className="btn-neon px-8 py-4 text-lg">🚀 Começar Grátis</Link>
            <Link href="/pricing" className="btn-secondary px-8 py-4 text-lg">Ver Planos</Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-400">
          <p>© 2025 Mídiaflow. Todos os direitos reservados.</p>
          <div className="flex justify-center gap-6 mt-4">
            <Link href="/termos" className="hover:text-neon-cyan">Termos</Link>
            <Link href="/privacidade" className="hover:text-neon-cyan">Privacidade</Link>
            <Link href="/sla" className="hover:text-neon-cyan">SLA</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
