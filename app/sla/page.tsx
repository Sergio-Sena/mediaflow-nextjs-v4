'use client'

import Link from 'next/link'
import { Button } from '@/components/ui'

export default function SLAPage() {
  return (
    <div className="min-h-screen bg-dark-950">
      <header className="sticky top-0 z-50 backdrop-blur-md border-b border-white/10" style={{background:'rgba(0,0,0,0.7)'}}>
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            <span style={{background:'linear-gradient(135deg,#667eea,#764ba2)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>Mídia</span><span className="text-white">flow</span>
          </Link>
          <Link href="/login">
            <Button variant="primary" size="md">Entrar</Button>
          </Link>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span style={{background:'linear-gradient(135deg,#667eea,#764ba2)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>Garantias e SLA</span>
        </h1>
        <p className="text-xl text-gray-400">
          Transparência total sobre nossos compromissos de disponibilidade e qualidade.
        </p>
      </section>

      <article className="max-w-4xl mx-auto px-4 pb-16 space-y-8">
        <section className="glass-card p-8">
          <h2 className="text-3xl font-bold mb-6 text-[#667eea]">⏱️ Uptime Garantido</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-dark-800/50 p-6 rounded-lg border border-[#667eea]/30">
              <h3 className="text-xl font-bold mb-3">Plataforma</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li><strong>Disponibilidade:</strong> 99.9%</li>
                <li><strong>Downtime máximo:</strong> 43 min/mês</li>
                <li><strong>CDN:</strong> 400+ POPs globais</li>
                <li><strong>Suporte:</strong> Email 24h</li>
              </ul>
            </div>
            <div className="bg-dark-800/50 p-6 rounded-lg border border-[#764ba2]/30">
              <h3 className="text-xl font-bold mb-3">Infraestrutura</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li><strong>CloudFront:</strong> SLA AWS 99.9%</li>
                <li><strong>Lambda:</strong> SLA AWS 99.95%</li>
                <li><strong>DynamoDB:</strong> SLA AWS 99.999%</li>
                <li><strong>S3:</strong> Durabilidade 99.999999999%</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="glass-card p-8">
          <h2 className="text-3xl font-bold mb-6 text-[#667eea]">❓ Perguntas Frequentes</h2>
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-bold text-[#a5b4fc] mb-2">O que acontece se ficarem offline mais que o prometido?</h3>
              <p className="text-gray-300">Você recebe créditos automaticamente na próxima fatura.</p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-[#a5b4fc] mb-2">Como sei se houve problema?</h3>
              <p className="text-gray-300">Acesse <strong>status.midiaflow.com</strong> ou receba notificações por email.</p>
            </div>
            <div>
              <h3 className="text-lg font-bold text-[#a5b4fc] mb-2">Posso cancelar quando quiser?</h3>
              <p className="text-gray-300">Sim! Sem multas, sem taxas. Cancele direto no dashboard.</p>
            </div>
          </div>
        </section>

        <div className="glass-card p-8 border-[#667eea]/30" style={{background:'rgba(102,126,234,0.05)'}}>
          <p className="text-center text-gray-300 mb-4">
            <strong>Dúvidas sobre o SLA? Entre em contato.</strong>
          </p>
          <div className="flex justify-center gap-6">
            <Link href="/termos" className="text-[#a5b4fc] hover:underline">Ver Termos de Serviço</Link>
            <Link href="/privacidade" className="text-[#a5b4fc] hover:underline">Ver Política de Privacidade</Link>
          </div>
        </div>
      </article>

      <footer className="border-t border-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-400">
          <p>© 2025 Mídiaflow. Todos os direitos reservados.</p>
          <div className="flex justify-center gap-6 mt-4">
            <Link href="/termos" className="hover:text-[#a5b4fc]">Termos</Link>
            <Link href="/privacidade" className="hover:text-[#a5b4fc]">Privacidade</Link>
            <Link href="/sla" className="hover:text-[#a5b4fc]">SLA</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
