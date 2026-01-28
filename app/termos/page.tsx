'use client'

import Link from 'next/link'
import { Button, Card } from '@/components/ui'

export default function TermosPage() {
  return (
    <div className="min-h-screen bg-dark-950">
      <header className="bg-dark-900/50 backdrop-blur-md border-b border-neon-cyan/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            🎬 <span className="neon-text">Mídiaflow</span>
          </Link>
          <div className="flex gap-4">
            <Link href="/pricing">
              <Button variant="secondary" size="md">Ver Planos</Button>
            </Link>
            <Link href="/register">
              <Button variant="primary" size="md">Começar Grátis</Button>
            </Link>
          </div>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          📜 <span className="neon-text">Termos de Serviço</span>
        </h1>
        <p className="text-gray-400">Última atualização: 30 de janeiro de 2025</p>
      </section>

      <article className="max-w-4xl mx-auto px-4 pb-16 space-y-8">
        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">1. O que é o Mídiaflow</h2>
          <p className="text-gray-300">O Mídiaflow é uma plataforma de hospedagem e distribuição de vídeos via CDN global. Oferecemos conversão automática, player profissional e armazenamento seguro na nuvem.</p>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">2. Quem pode usar</h2>
          <ul className="list-disc list-inside space-y-2 text-gray-300">
            <li>Pessoas com 18 anos ou mais</li>
            <li>Menores de 18 anos com autorização de responsável legal</li>
            <li>Empresas e organizações legalmente constituídas</li>
          </ul>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">3. Planos e Pagamentos</h2>
          <div className="space-y-4 text-gray-300">
            <div>
              <h3 className="font-bold text-white mb-2">Planos disponíveis</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Trial: 14 dias grátis, sem cartão</li>
                <li>Basic: R$ 49,90/mês</li>
                <li>Pro: R$ 99,90/mês</li>
                <li>Enterprise: Sob consulta</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">Reembolso</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>30 dias de garantia na primeira assinatura</li>
                <li>Renovações não têm direito a reembolso</li>
                <li>Processamento em até 7 dias úteis</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">4. Uso Aceitável</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-bold text-green-400 mb-3">✅ Você pode</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-300 text-sm">
                <li>Hospedar vídeos próprios</li>
                <li>Compartilhar vídeos</li>
                <li>Integrar via API</li>
                <li>Fazer download</li>
                <li>Usar comercialmente</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-red-400 mb-3">❌ Você não pode</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-300 text-sm">
                <li>Conteúdo ilegal</li>
                <li>Spam ou phishing</li>
                <li>Violar direitos autorais</li>
                <li>Mineração de cripto</li>
                <li>Revender sem autorização</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">5. Seu Conteúdo</h2>
          <div className="space-y-4 text-gray-300">
            <p><strong className="text-white">Você mantém os direitos:</strong> Você é dono dos vídeos que envia. Nós não reivindicamos propriedade.</p>
            <p><strong className="text-white">Licença para nós:</strong> Você nos dá permissão para armazenar, processar, converter e distribuir via CDN.</p>
            <p className="text-sm text-gray-400">Esta licença termina quando você deleta o conteúdo ou cancela a conta.</p>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">6. Privacidade</h2>
          <p className="text-gray-300 mb-4">Seus dados são tratados conforme nossa <Link href="/privacidade" className="text-neon-cyan hover:underline">Política de Privacidade</Link>.</p>
          <ul className="list-disc list-inside space-y-2 text-gray-300">
            <li>Coletamos apenas dados necessários</li>
            <li>Não vendemos suas informações</li>
            <li>Conformidade com LGPD</li>
            <li>Você tem direito a acessar, corrigir e deletar</li>
          </ul>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">7. Disponibilidade e SLA</h2>
          <p className="text-gray-300 mb-4">Garantimos uptime conforme seu plano:</p>
          <ul className="list-disc list-inside space-y-1 text-gray-300">
            <li>Trial: 99.5%</li>
            <li>Basic: 99.9%</li>
            <li>Pro: 99.95%</li>
            <li>Enterprise: 99.99%</li>
          </ul>
          <p className="text-gray-400 mt-4 text-sm">Veja detalhes em <Link href="/sla" className="text-neon-cyan hover:underline">Garantias e SLA</Link>.</p>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">8. Cancelamento</h2>
          <div className="space-y-4 text-gray-300">
            <p><strong className="text-white">Você pode cancelar:</strong> A qualquer momento, sem multas. Dados mantidos por 30 dias.</p>
            <p><strong className="text-white">Nós podemos suspender se:</strong> Violação dos termos, não pagamento, uso abusivo ou atividade ilegal.</p>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">9. Contato</h2>
          <div className="space-y-2 text-gray-300">
            <p><strong>Dúvidas sobre os termos?</strong></p>
            <p>Email: <span className="text-neon-cyan">juridico@midiaflow.com</span></p>
            <p>Suporte: <span className="text-neon-cyan">suporte@midiaflow.com</span></p>
            <p className="text-sm text-gray-400">Horário: Segunda a Sexta, 9h às 18h</p>
          </div>
        </div>

        <div className="glass-card p-8 bg-neon-cyan/5 border-neon-cyan/30">
          <p className="text-center text-gray-300">
            <strong>Ao usar o Mídiaflow, você confirma que leu e concorda com estes Termos de Serviço.</strong>
          </p>
          <div className="flex justify-center gap-6 mt-4">
            <Link href="/privacidade" className="text-neon-cyan hover:underline">Ver Política de Privacidade</Link>
            <Link href="/sla" className="text-neon-cyan hover:underline">Ver Garantias e SLA</Link>
          </div>
        </div>
      </article>

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
