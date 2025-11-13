'use client'

import Link from 'next/link'

export default function PrivacidadePage() {
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
          🔒 <span className="neon-text">Política de Privacidade</span>
        </h1>
        <p className="text-gray-400">Última atualização: 30 de janeiro de 2025</p>
        <p className="text-gray-400 mt-2">Conformidade com LGPD (Lei Geral de Proteção de Dados)</p>
      </section>

      <article className="max-w-4xl mx-auto px-4 pb-16 space-y-8">
        <div className="glass-card p-8 bg-green-500/5 border-green-500/30">
          <h2 className="text-2xl font-bold mb-4 text-green-400">Resumo em Linguagem Simples</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-bold text-white mb-3">✅ O que fazemos</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>Coletamos apenas o necessário</li>
                <li>Protegemos com criptografia forte</li>
                <li>Não vendemos seus dados</li>
                <li>Você controla suas informações</li>
                <li>Conformidade total com LGPD</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-3">❌ O que não fazemos</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>Vender ou alugar seus dados</li>
                <li>Compartilhar para marketing</li>
                <li>Usar dados além do necessário</li>
                <li>Dificultar acesso ou exclusão</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">1. Quais Dados Coletamos</h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-bold text-white mb-2">Dados que você fornece</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-300 text-sm">
                <li>Nome completo - para identificação</li>
                <li>Email - para login e comunicação</li>
                <li>Senha - criptografada (nunca em texto puro)</li>
                <li>Telefone (opcional) - para suporte e 2FA</li>
                <li>Dados de pagamento - via Stripe (não armazenamos cartões)</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">Dados coletados automaticamente</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-300 text-sm">
                <li>Endereço IP - segurança e localização</li>
                <li>Navegador e dispositivo - compatibilidade</li>
                <li>Logs de acesso - segurança</li>
                <li>Cookies - manter você logado</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">2. Como Usamos Seus Dados</h2>
          <div className="space-y-3 text-gray-300">
            <p><strong className="text-white">Para prestar o serviço:</strong> Processar uploads, entregar vídeos via CDN, autenticar login, fornecer suporte.</p>
            <p><strong className="text-white">Para melhorar:</strong> Analisar uso, estatísticas agregadas, testes A/B.</p>
            <p><strong className="text-white">Para comunicar:</strong> Emails transacionais, marketing (opt-in), notificações de serviço.</p>
            <p><strong className="text-white">Para cumprir a lei:</strong> Obrigações fiscais, prevenção de fraudes, solicitações judiciais.</p>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">3. Com Quem Compartilhamos</h2>
          <div className="space-y-4 text-gray-300">
            <p className="text-lg"><strong className="text-white">Não vendemos seus dados.</strong> Nunca vendemos ou alugamos suas informações.</p>
            <div>
              <h3 className="font-bold text-white mb-2">Compartilhamento necessário:</h3>
              <ul className="list-disc list-inside space-y-1 text-sm">
                <li><strong>AWS (Amazon):</strong> Hospedagem e CDN - DPA assinado</li>
                <li><strong>Stripe:</strong> Processamento de pagamentos - PCI-DSS certificado</li>
                <li><strong>Autoridades:</strong> Apenas quando exigido por lei</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">4. Como Protegemos</h2>
          <div className="grid md:grid-cols-2 gap-6 text-gray-300 text-sm">
            <div>
              <h3 className="font-bold text-white mb-2">Segurança técnica</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Criptografia AES-256 (padrão bancário)</li>
                <li>HTTPS/TLS 1.3 em tudo</li>
                <li>Senhas com hash SHA-256</li>
                <li>2FA obrigatório</li>
                <li>Backup a cada 6h</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">Retenção de dados</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Conta ativa: Enquanto usar</li>
                <li>Após cancelamento: 30 dias</li>
                <li>Após 120 dias inativo: Exclusão</li>
                <li>Logs: 90 dias</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="glass-card p-8 bg-neon-cyan/5 border-neon-cyan/30">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">5. Seus Direitos (LGPD)</h2>
          <div className="grid md:grid-cols-2 gap-4 text-gray-300 text-sm">
            <div>
              <h3 className="font-bold text-white mb-2">✓ Acesso</h3>
              <p>Solicitar cópia dos seus dados</p>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">✓ Correção</h3>
              <p>Atualizar informações incorretas</p>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">✓ Exclusão</h3>
              <p>Deletar conta e dados</p>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">✓ Portabilidade</h3>
              <p>Exportar seus vídeos (JSON)</p>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">✓ Revogação</h3>
              <p>Desativar emails de marketing</p>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">✓ Oposição</h3>
              <p>Opor-se ao tratamento</p>
            </div>
          </div>
          <div className="mt-6 p-4 bg-dark-800/50 rounded-lg">
            <p className="text-white mb-2"><strong>Como exercer seus direitos:</strong></p>
            <p className="text-gray-300">Email: <span className="text-neon-cyan">privacidade@midiaflow.com</span></p>
            <p className="text-gray-400 text-sm">Prazo de resposta: até 15 dias</p>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">6. Cookies</h2>
          <div className="space-y-4 text-gray-300 text-sm">
            <div>
              <h3 className="font-bold text-white mb-2">Cookies essenciais (não podem ser desativados)</h3>
              <p>Autenticação, sessão, segurança</p>
            </div>
            <div>
              <h3 className="font-bold text-white mb-2">Cookies de analytics (você pode desativar)</h3>
              <p>Google Analytics, métricas de uso, heatmaps</p>
            </div>
            <p className="text-gray-400">Gerenciar cookies: Configurações no dashboard</p>
          </div>
        </div>

        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold mb-4 text-neon-cyan">7. Contato</h2>
          <div className="space-y-3 text-gray-300">
            <div>
              <p className="font-bold text-white">Dúvidas sobre privacidade?</p>
              <p>Email: <span className="text-neon-cyan">privacidade@midiaflow.com</span></p>
              <p className="text-sm text-gray-400">Prazo de resposta: 15 dias</p>
            </div>
            <div>
              <p className="font-bold text-white">Encarregado de Dados (DPO)</p>
              <p>Email: <span className="text-neon-cyan">dpo@midiaflow.com</span></p>
              <p className="text-sm text-gray-400">Responsável pela conformidade com LGPD</p>
            </div>
          </div>
        </div>

        <div className="glass-card p-8 bg-neon-cyan/5 border-neon-cyan/30">
          <p className="text-center text-gray-300 mb-4">
            <strong>Ao usar o Mídiaflow, você confirma que leu e concorda com esta Política de Privacidade.</strong>
          </p>
          <div className="flex justify-center gap-6">
            <Link href="/termos" className="text-neon-cyan hover:underline">Ver Termos de Serviço</Link>
            <Link href="/sla" className="text-neon-cyan hover:underline">Ver Garantias e SLA</Link>
          </div>
          <p className="text-center text-gray-400 text-xs mt-4">
            Base legal (LGPD): Art. 7º, I (Consentimento) | Art. 7º, V (Execução de contrato) | Art. 7º, IX (Legítimo interesse)
          </p>
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
