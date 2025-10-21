'use client'

import { useRouter } from 'next/navigation'

export default function DocsPage() {
  const router = useRouter()
  
  return (
    <div className="min-h-screen p-4 sm:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
              Documentacao
            </span>
          </h1>
          <p className="text-gray-400">Guia completo para usar o Midiaflow v4.6</p>
        </div>

        <div className="glass-card p-6 sm:p-8 space-y-8">
          
          <section>
            <h2 className="text-2xl font-bold text-cyan-400 mb-4">
              O que e o Midiaflow?
            </h2>
            <p className="text-gray-300 leading-relaxed">
              Midiaflow e uma plataforma de streaming profissional multi-usuario com upload multipart 
              ilimitado, sistema de avatares, autenticacao 2FA e organizacao inteligente de arquivos. 
              Com conversao automatica H.264 1080p e CDN global com 400+ edge locations.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-purple-400 mb-4">
              Como comecar
            </h2>
            <div className="space-y-4">
              <div className="bg-dark-800/50 p-4 rounded-lg border border-cyan-500/20">
                <h3 className="font-semibold text-cyan-300 mb-2">1. Faca login</h3>
                <p className="text-gray-400 text-sm">
                  Acesse a pagina inicial e clique em Acessar Sistema. 
                  Faca login direto ou cadastre-se em /register. Admin precisa de 2FA.
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
                <h3 className="font-semibold text-cyan-300 mb-2">3. Faca upload de videos</h3>
                <p className="text-gray-400 text-sm">
                  Clique no botao Upload e arraste seus arquivos. Sistema detecta 
                  automaticamente: menor que 100MB instantaneo, maior que 100MB multipart paralelo.
                </p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-cyan-400 mb-4">
              Funcionalidades
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-cyan-300 mb-2">Upload Multipart Ilimitado</h3>
                <p className="text-gray-400 text-sm">
                  Sistema hibrido: arquivos pequenos instantaneos, grandes com paralelizacao.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-300 mb-2">Conversao H.264 1080p</h3>
                <p className="text-gray-400 text-sm">
                  AWS MediaConvert automatico para qualidade profissional.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-cyan-300 mb-2">Player Sequencial</h3>
                <p className="text-gray-400 text-sm">
                  Navegacao Previous/Next entre videos da pasta.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-300 mb-2">Sistema Multi-Usuario Completo</h3>
                <p className="text-gray-400 text-sm">
                  2FA seletivo, avatares S3, painel admin e isolamento users/username.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-cyan-300 mb-2">Next.js 14 + Tailwind</h3>
                <p className="text-gray-400 text-sm">
                  Frontend moderno com design neon cyberpunk.
                </p>
              </div>
              
              <div className="bg-dark-800/30 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-300 mb-2">AWS CloudFront</h3>
                <p className="text-gray-400 text-sm">
                  CDN global com 400+ edge locations e SSL.
                </p>
              </div>
            </div>
          </section>

        </div>

        <div className="mt-8 text-center">
          <button
            onClick={() => router.push('/')}
            className="btn-secondary px-6 py-3 inline-flex items-center gap-2"
          >
            <span>Voltar ao Inicio</span>
          </button>
        </div>
      </div>
    </div>
  )
}
