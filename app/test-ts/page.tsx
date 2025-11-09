'use client'

import { useState } from 'react'
import VideoPlayer from '@/components/modules/VideoPlayer'

export default function TestTSPage() {
  const [showPlayer, setShowPlayer] = useState(false)

  return (
    <div className="min-h-screen bg-dark-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-4">Teste de Arquivo .TS</h1>
        
        <div className="bg-dark-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl text-white mb-2">Arquivo de Teste</h2>
          <p className="text-gray-400 mb-4">Uma Pequena Colagem.ts (18 MB)</p>
          
          <button
            onClick={() => setShowPlayer(true)}
            className="bg-neon-cyan hover:bg-neon-cyan/80 text-black px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            ▶️ Reproduzir Vídeo .TS
          </button>
        </div>

        <div className="bg-dark-800 rounded-lg p-6">
          <h3 className="text-lg text-white mb-2">ℹ️ Informações</h3>
          <ul className="text-gray-400 space-y-2 text-sm">
            <li>✅ Usando Hls.js para reprodução de .ts</li>
            <li>✅ Suporte nativo em navegadores modernos</li>
            <li>✅ Sem necessidade de conversão</li>
            <li>✅ Compatível com streaming HLS</li>
          </ul>
        </div>
      </div>

      {showPlayer && (
        <VideoPlayer
          src="/Uma Pequena Colagem.mp4"
          title="Uma Pequena Colagem (convertido de .ts)"
          onClose={() => setShowPlayer(false)}
        />
      )}
    </div>
  )
}
