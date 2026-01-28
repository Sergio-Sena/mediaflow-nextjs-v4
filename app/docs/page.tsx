'use client'

import Link from 'next/link'
import { useState } from 'react'
import { Book, Upload, Share2, HelpCircle, FileText } from 'lucide-react'
import { Button, Card } from '@/components/ui'

export default function DocsPage() {
  const [activeSection, setActiveSection] = useState('inicio-rapido')

  const sections = [
    { id: 'inicio-rapido', title: 'Início Rápido', icon: Book },
    { id: 'upload', title: 'Como Fazer Upload', icon: Upload },
    { id: 'compartilhar', title: 'Como Compartilhar', icon: Share2 },
    { id: 'faq', title: 'FAQ', icon: HelpCircle },
    { id: 'tecnico', title: 'Documentação Técnica', icon: FileText },
  ]

  const content: Record<string, { title: string; sections: { title: string; content: string }[] }> = {
    'inicio-rapido': {
      title: '🚀 Início Rápido',
      sections: [
        {
          title: 'Passo 1: Criar Conta (1 minuto)',
          content: `1. Acesse midiaflow.sstechnologies-cloud.com/register
2. Preencha nome, email e senha
3. Marque "Aceito os Termos de Serviço"
4. Clique em "Criar Conta"

Você ganhou 14 dias grátis com 10 GB de armazenamento!`
        },
        {
          title: 'Passo 2: Fazer Login (30 segundos)',
          content: `1. Acesse midiaflow.sstechnologies-cloud.com/login
2. Digite seu email e senha
3. (Opcional) Configure 2FA para mais segurança`
        },
        {
          title: 'Passo 3: Fazer Primeiro Upload (2 minutos)',
          content: `Método 1: Arrastar e Soltar
- Arraste seu vídeo para a área de upload
- Aguarde o upload (barra de progresso)
- Conversão automática inicia

Método 2: Clique para Selecionar
- Clique em "Escolher Arquivo"
- Selecione o vídeo
- Upload inicia automaticamente`
        },
        {
          title: 'Passo 4: Compartilhar Vídeo (1 minuto)',
          content: `Opção 1: Link Direto
- Clique no vídeo
- Copie o link direto
- Compartilhe onde quiser

Opção 2: Código Embed
- Clique em "Embed"
- Copie o código HTML
- Cole no seu site`
        }
      ]
    },
    'upload': {
      title: '📤 Como Fazer Upload',
      sections: [
        {
          title: 'Métodos de Upload',
          content: `Método 1: Arrastar e Soltar (Recomendado)
✅ Suporta múltiplos arquivos
✅ Barra de progresso em tempo real
✅ Não precisa clicar em nada

Método 2: Clique para Selecionar
✅ Familiar para todos
✅ Seleção múltipla (Ctrl/Cmd + clique)
✅ Funciona em qualquer navegador`
        },
        {
          title: 'Limites por Plano',
          content: `Trial: 1 GB/arquivo | 10 GB storage | 20 GB bandwidth
Basic: 5 GB/arquivo | 25 GB storage | Ilimitado
Pro: 5 GB/arquivo | 200 GB storage | Ilimitado
Enterprise: Customizado`
        },
        {
          title: 'Formatos Suportados',
          content: `Vídeos (Conversão Automática):
✅ MP4 (recomendado)
✅ MOV (Apple)
✅ AVI (Windows)
✅ MKV (alta qualidade)
✅ WebM (web)

Outros Arquivos (Bônus Basic/Pro):
📄 Documentos: PDF, DOC, XLS, PPT
🖼️ Imagens: JPG, PNG, GIF, SVG
📦 Compactados: ZIP, RAR, 7Z`
        },
        {
          title: 'Tempo de Conversão',
          content: `Até 5 minutos: 2-5 minutos
5-30 minutos: 5-10 minutos
30-60 minutos: 10-15 minutos
Mais de 1 hora: 15-30 minutos`
        }
      ]
    },
    'compartilhar': {
      title: '📤 Como Compartilhar Vídeos',
      sections: [
        {
          title: 'Método 1: Link Direto',
          content: `Melhor para: Redes sociais, WhatsApp, email

Como fazer:
1. Clique no vídeo no dashboard
2. Copie o link direto
3. Cole onde quiser

Onde usar:
✅ WhatsApp, Telegram
✅ Email, newsletter
✅ Facebook, Twitter, LinkedIn
✅ Instagram bio`
        },
        {
          title: 'Método 2: Código Embed',
          content: `Melhor para: Sites, blogs, plataformas de curso

Como fazer:
1. Clique no vídeo
2. Clique em "Embed"
3. Copie o código HTML
4. Cole no seu site

Onde usar:
✅ WordPress, Wix, Squarespace
✅ Hotmart, Eduzz, Monetizze
✅ Landing pages
✅ Plataformas de EAD`
        },
        {
          title: 'Controle de Privacidade',
          content: `Vídeos Privados (Padrão):
- Apenas você vê
- Link não funciona para outros

Vídeos Públicos:
- Qualquer pessoa com link pode ver
- Não aparece em buscas

Vídeos com Senha (Pro/Enterprise):
- Protegido por senha
- Você define a senha`
        }
      ]
    },
    'faq': {
      title: '❓ Perguntas Frequentes',
      sections: [
        {
          title: 'Conta e Planos',
          content: `Como funciona o trial de 14 dias?
Totalmente grátis, sem cartão de crédito! 10 GB storage, 20 GB bandwidth.

Posso cancelar quando quiser?
Sim! Sem multas, sem taxas. Cancele direto no dashboard.

Como faço upgrade de plano?
Dashboard → Configurações → Planos. Pagamento proporcional.

Tem desconto para pagamento anual?
Sim! 20% de desconto pagando anualmente.`
        },
        {
          title: 'Upload e Conversão',
          content: `Qual o tamanho máximo de upload?
Trial: 1 GB | Basic/Pro: 5 GB | Enterprise: Customizado

Quanto tempo demora a conversão?
Vídeos curtos: 2-5 min | Médios: 5-10 min | Longos: 10-15 min

Quais formatos são suportados?
MP4, MOV, AVI, MKV, WebM (conversão automática para H.264)

Posso fazer upload de outros arquivos?
Sim! Bônus dos planos Basic e Pro. Use como storage na nuvem.`
        },
        {
          title: 'Compartilhamento',
          content: `Como compartilho meus vídeos?
Link direto (copiar e colar) ou Código embed (para sites)

Meus vídeos são públicos?
Não, privados por padrão. Você controla quem vê.

Posso usar meu próprio domínio?
Sim, em planos Pro e Enterprise (ex: videos.suaempresa.com)`
        },
        {
          title: 'Técnico',
          content: `Onde os vídeos são armazenados?
AWS S3 (Amazon) com CDN CloudFront (400+ edge locations)

Qual o uptime garantido?
Trial: 99.5% | Basic: 99.9% | Pro: 99.95% | Enterprise: 99.99%

Como funciona o suporte?
Trial: Email 48h | Basic: Email 24h | Pro: Email 4h + Chat | Enterprise: 24/7`
        }
      ]
    },
    'tecnico': {
      title: '🔧 Documentação Técnica',
      sections: [
        {
          title: 'Arquitetura',
          content: `Frontend: Next.js 14 + TypeScript + Tailwind CSS
Backend: AWS Lambda (Node.js 18)
Storage: S3 + CloudFront CDN
Conversão: MediaConvert
Auth: JWT + 2FA (TOTP)`
        },
        {
          title: 'API Endpoints (Pro/Enterprise)',
          content: `POST /prod/get-upload-url - Upload de vídeo
GET /prod/list-files - Listar vídeos
GET /prod/video/:id - Detalhes do vídeo
DELETE /prod/video/:id - Deletar vídeo

Autenticação: Bearer Token (JWT)
Rate Limits: Trial: 10 req/min | Basic: 60 | Pro: 300`
        },
        {
          title: 'Deploy',
          content: `Frontend (S3 + CloudFront):
npm run build
cd out
aws s3 sync . s3://bucket/ --delete
aws cloudfront create-invalidation --distribution-id ID --paths "/*"

Backend (Lambda):
cd lambda/function-name
npm install
zip -r function.zip .
aws lambda update-function-code --function-name NAME --zip-file fileb://function.zip`
        },
        {
          title: 'Segurança',
          content: `✅ HTTPS em tudo (TLS 1.3)
✅ Senhas com hash SHA-256
✅ JWT com expiração (7 dias)
✅ 2FA obrigatório
✅ Presigned URLs (5 min)
✅ CORS configurado
✅ Rate limiting
✅ Conformidade LGPD`
        }
      ]
    }
  }

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

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">
            📚 <span className="neon-text">Documentação</span>
          </h1>
          <p className="text-gray-400">Guias completos para usar o Mídiaflow</p>
        </div>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <aside className="lg:col-span-1">
            <nav className="glass-card p-4 sticky top-24">
              <div className="space-y-2">
                {sections.map((section) => {
                  const Icon = section.icon
                  return (
                    <button
                      key={section.id}
                      onClick={() => setActiveSection(section.id)}
                      className={`w-full text-left px-4 py-3 rounded-lg transition-all flex items-center gap-3 ${
                        activeSection === section.id
                          ? 'bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/30'
                          : 'hover:bg-dark-800/50 text-gray-400'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="text-sm font-medium">{section.title}</span>
                    </button>
                  )
                })}
              </div>
            </nav>
          </aside>

          {/* Content */}
          <main className="lg:col-span-3">
            <article className="glass-card p-8">
              <h2 className="text-3xl font-bold mb-8">{content[activeSection].title}</h2>
              
              <div className="space-y-8">
                {content[activeSection].sections.map((section, idx) => (
                  <div key={idx} className="border-l-4 border-neon-cyan/30 pl-6">
                    <h3 className="text-xl font-bold mb-4 text-neon-cyan">{section.title}</h3>
                    <div className="text-gray-300 whitespace-pre-line leading-relaxed">
                      {section.content}
                    </div>
                  </div>
                ))}
              </div>

              {/* Navigation */}
              <div className="mt-12 pt-8 border-t border-gray-700 flex justify-between">
                <div>
                  {sections.findIndex(s => s.id === activeSection) > 0 && (
                    <Button
                      onClick={() => setActiveSection(sections[sections.findIndex(s => s.id === activeSection) - 1].id)}
                      variant="secondary"
                    >
                      ← Anterior
                    </Button>
                  )}
                </div>
                <div>
                  {sections.findIndex(s => s.id === activeSection) < sections.length - 1 && (
                    <Button
                      onClick={() => setActiveSection(sections[sections.findIndex(s => s.id === activeSection) + 1].id)}
                      variant="primary"
                    >
                      Próximo →
                    </Button>
                  )}
                </div>
              </div>
            </article>

            {/* Help CTA */}
            <div className="glass-card p-6 mt-8 text-center">
              <h3 className="text-xl font-bold mb-2">Ainda tem dúvidas?</h3>
              <p className="text-gray-400 mb-4">Nossa equipe está pronta para ajudar</p>
              <div className="flex gap-4 justify-center">
                <a href="mailto:suporte@midiaflow.com" className="btn-secondary px-6 py-3">
                  📧 Email
                </a>
                <Link href="/pricing" className="btn-neon px-6 py-3">
                  Ver Planos
                </Link>
              </div>
            </div>
          </main>
        </div>
      </div>

      <footer className="border-t border-gray-800 py-8 mt-16">
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
