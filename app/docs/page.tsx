'use client'

import { useRouter } from 'next/navigation'

export default function DocsPage() {
  const router = useRouter()
  
  return (
    <div className="min-h-screen p-4 sm:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
              Documentação
            </span>
          </h1>
          <p className="text-gray-400">Guia completo para usar o Mídiaflow</p>
        </div>

        {/* Content */}
        <div className="glass-card p-6 sm:p-8 space-y-8">
          
          {/* O que é */}
          <section>
            <h2 className="text-2xl font-bold text-cyan-400 mb-4">
              🎬 O que é o Mídiaflow?
            </h2>
            <p className="text-gray-300 leading-relaxed">
              Mídiaflow é uma plataforma de streaming profissional multi-usuário que permite fazer upload 
              de até 5GB, organizar e assistir seus vídeos de qualquer lugar. Com conversão automática 
              H.264 1080p e CDN global com 400+ edge locations para performance mundial.
            </p>
          </section>

          {/* Como começar */}
          <section>
            <h2 className="text-2xl font-bold text-purple-400 mb-4">
              🚀 Como começar
            </h2>
            <div className="space-y-4">
              <div className="bg-dark-800/50 p-4 rounded-lg border border-cyan-500/20">
                <h3 className="font-semibold text-cyan-300 mb-2">1. Faça login</h3>
                <p className="text-gray-400 text-sm">
                  Acesse a página inicial e clique em "Acessar Sistema". 
                  Selecione seu perfil e insira o código 2FA do aplicativo autenticador.
                </p>
              </div>
              
              <div className="bg-dark-800/50 p-4 rounded-lg border border-purple-500/20">
                <h3 className="font-semibold text-purple-300 mb-2">2. Navegue pelas pastas</h3>
                <p className="text-gray-400 text-sm">
                  Use o menu lateral ou os breadcrumbs para navegar entre suas pastas. 
                  Clique duas vezes em uma pasta para abrir.
                </p>
              </div>
              
              <div className="bg-dark-800/50 p-4 rounded-lg border border-cyan-500/20">
                <h3 className="font-semibold text-cyan-300 mb-2">3. Faça upload de vídeos</h3>
                <p className="text-gray-400 text-sm">
                  Clique no botão "Upload" e arraste seus vídeos (até 5GB). 
                  Use o botão "Converter" quando desejar otimizar para streaming.
                </p>
              </div>
            </div>
          </section>

          {/* Funcionalidades */}
          <section>
            <h2 className="text-2xl font-bold text-cyan-400 mb-4">
              ✨ Funcionalidades
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-cyan-300 mb-2 flex items-center gap-2">
                  <span>📤</span> Upload até 5GB
                </h3>
                <p className="text-gray-400 text-sm">
                  DirectUpload component com drag & drop. Suporta MP4, AVI, MOV e mais.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-300 mb-2 flex items-center gap-2">
                  <span>🔄</span> Conversão H.264 1080p
                </h3>
                <p className="text-gray-400 text-sm">
                  AWS MediaConvert automático para qualidade profissional.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-cyan-300 mb-2 flex items-center gap-2">
                  <span>🎥</span> Player Sequencial
                </h3>
                <p className="text-gray-400 text-sm">
                  Navegação Previous/Next entre vídeos da pasta.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-300 mb-2 flex items-center gap-2">
                  <span>🔐</span> 2FA + Multi-usuário
                </h3>
                <p className="text-gray-400 text-sm">
                  Autenticação 2FA obrigatória com isolamento de dados.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-cyan-300 mb-2 flex items-center gap-2">
                  <span>⚡</span> Next.js 14 + Tailwind
                </h3>
                <p className="text-gray-400 text-sm">
                  Frontend moderno com design neon cyberpunk.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-300 mb-2 flex items-center gap-2">
                  <span>☁️</span> AWS CloudFront
                </h3>
                <p className="text-gray-400 text-sm">
                  CDN global com 400+ edge locations e SSL.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-cyan-300 mb-2 flex items-center gap-2">
                  <span>⚡</span> Lighthouse 95+
                </h3>
                <p className="text-gray-400 text-sm">
                  Performance otimizada em todas as categorias.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-300 mb-2 flex items-center gap-2">
                  <span>🎯</span> Uptime 99.9%
                </h3>
                <p className="text-gray-400 text-sm">
                  Alta disponibilidade com monitoramento CloudWatch.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-cyan-300 mb-2 flex items-center gap-2">
                  <span>💰</span> ~$20/mês AWS
                </h3>
                <p className="text-gray-400 text-sm">
                  Custo otimizado com arquitetura serverless.
                </p>
              </div>
            </div>
          </section>

          {/* Como usar */}
          <section>
            <h2 className="text-2xl font-bold text-purple-400 mb-4">
              📖 Como usar
            </h2>
            <div className="space-y-6">
              
              <div>
                <h3 className="font-semibold text-cyan-300 mb-3">📤 Fazer Upload</h3>
                <ol className="list-decimal list-inside space-y-2 text-gray-400 text-sm ml-4">
                  <li>Navegue até a pasta desejada</li>
                  <li>Clique no botão "Upload" no canto superior direito</li>
                  <li>Arraste seus vídeos ou clique para selecionar</li>
                  <li>Aguarde o upload completar</li>
                  <li>Use o botão "Converter" se desejar otimizar para streaming</li>
                  <li>Pronto! Seu vídeo está disponível</li>
                </ol>
              </div>

              <div>
                <h3 className="font-semibold text-purple-300 mb-3">🎥 Assistir Vídeos</h3>
                <ol className="list-decimal list-inside space-y-2 text-gray-400 text-sm ml-4">
                  <li>Clique no card do vídeo que deseja assistir</li>
                  <li>Use os controles do player (play, pause, volume)</li>
                  <li>Navegue entre vídeos com os botões Previous/Next</li>
                  <li>Ajuste a velocidade de reprodução se desejar</li>
                  <li>Use fullscreen para melhor experiência</li>
                </ol>
              </div>

              <div>
                <h3 className="font-semibold text-cyan-300 mb-3">📁 Gerenciar Pastas</h3>
                <ol className="list-decimal list-inside space-y-2 text-gray-400 text-sm ml-4">
                  <li>Clique em "Gerenciar Pastas" no menu</li>
                  <li>Crie novas pastas com o botão "Nova Pasta"</li>
                  <li>Renomeie clicando no ícone de edição</li>
                  <li>Delete pastas vazias com o ícone de lixeira</li>
                  <li>Use seleção em lote para operações múltiplas</li>
                </ol>
              </div>

              <div>
                <h3 className="font-semibold text-purple-300 mb-3">🔍 Buscar Vídeos</h3>
                <ol className="list-decimal list-inside space-y-2 text-gray-400 text-sm ml-4">
                  <li>Use a barra de busca no topo do dashboard</li>
                  <li>Digite o nome do vídeo que procura</li>
                  <li>A busca procura em todas as pastas automaticamente</li>
                  <li>Clique no resultado para abrir o vídeo</li>
                  <li>Use "Limpar Filtros" para voltar à visualização normal</li>
                </ol>
              </div>

            </div>
          </section>

          {/* Dicas */}
          <section>
            <h2 className="text-2xl font-bold text-cyan-400 mb-4">
              💡 Dicas úteis
            </h2>
            <div className="space-y-3">
              <div className="flex items-start gap-3 bg-cyan-500/10 p-3 rounded-lg border border-cyan-500/20">
                <span className="text-cyan-400 text-xl">⚡</span>
                <p className="text-gray-300 text-sm">
                  <strong className="text-cyan-300">Upload rápido:</strong> Arquivos menores que 100MB são enviados diretamente. 
                  Arquivos maiores usam upload em partes para maior confiabilidade.
                </p>
              </div>
              
              <div className="flex items-start gap-3 bg-purple-500/10 p-3 rounded-lg border border-purple-500/20">
                <span className="text-purple-400 text-xl">🎯</span>
                <p className="text-gray-300 text-sm">
                  <strong className="text-purple-300">Qualidade:</strong> Use o botão "Converter" para otimizar vídeos 
                  para H.264 1080p, garantindo compatibilidade e qualidade de streaming.
                </p>
              </div>
              
              <div className="flex items-start gap-3 bg-cyan-500/10 p-3 rounded-lg border border-cyan-500/20">
                <span className="text-cyan-400 text-xl">📱</span>
                <p className="text-gray-300 text-sm">
                  <strong className="text-cyan-300">Mobile:</strong> O sistema é totalmente responsivo. 
                  Use gestos de swipe para navegar entre vídeos no celular.
                </p>
              </div>
              
              <div className="flex items-start gap-3 bg-purple-500/10 p-3 rounded-lg border border-purple-500/20">
                <span className="text-purple-400 text-xl">🌐</span>
                <p className="text-gray-300 text-sm">
                  <strong className="text-purple-300">CDN Global:</strong> Seus vídeos são distribuídos em 400+ localizações 
                  ao redor do mundo para carregamento ultra-rápido.
                </p>
              </div>
            </div>
          </section>

          {/* Suporte */}
          <section>
            <h2 className="text-2xl font-bold text-purple-400 mb-4">
              🆘 Precisa de ajuda?
            </h2>
            <div className="bg-gradient-to-r from-cyan-500/10 to-purple-500/10 p-6 rounded-lg border border-cyan-500/30 text-center">
              <p className="text-gray-300 mb-4">
                Se encontrar algum problema ou tiver dúvidas, entre em contato:
              </p>
              <div className="space-y-2 text-sm">
                <p className="text-cyan-300">
                  <strong>Desenvolvedor:</strong> SSTechnologies (Sergio Sena)
                </p>
                <p className="text-gray-400 flex items-center justify-center gap-2">
                  <span>📧</span>
                  <a href="mailto:senanetworker@gmail.com" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                    senanetworker@gmail.com
                  </a>
                </p>
                <p className="text-gray-400">
                  Sistema 100% funcional em produção com uptime de 99.9% e Lighthouse 95+
                </p>
              </div>
            </div>
          </section>

        </div>

        {/* Back Button */}
        <div className="mt-8 text-center">
          <button
            onClick={() => router.push('/')}
            className="btn-secondary px-6 py-3 inline-flex items-center gap-2"
          >
            <span>←</span>
            <span>Voltar ao Início</span>
          </button>
        </div>
      </div>
    </div>
  )
}
