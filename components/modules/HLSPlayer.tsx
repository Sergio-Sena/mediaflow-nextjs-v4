'use client'

import { useEffect, useRef, useState } from 'react'

interface HLSPlayerProps {
  src: string
  title: string
  onClose?: () => void
}

export default function HLSPlayer({ src, title, onClose }: HLSPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [hlsSupported, setHlsSupported] = useState(false)

  useEffect(() => {
    console.log('=== HLS PLAYER DEBUG ===')
    console.log('Source:', src)
    console.log('Is .ts file:', src.endsWith('.ts'))

    const video = videoRef.current
    if (!video) return

    // Verificar suporte HLS nativo
    if (video.canPlayType('application/vnd.apple.mpegurl')) {
      console.log('✅ HLS nativo suportado')
      setHlsSupported(true)
      video.src = src
      setIsLoading(false)
      return
    }

    // Tentar carregar HLS.js dinamicamente
    const loadHLS = async () => {
      try {
        console.log('📦 Carregando HLS.js...')
        
        // Carregar HLS.js via CDN
        const script = document.createElement('script')
        script.src = 'https://cdn.jsdelivr.net/npm/hls.js@latest'
        document.head.appendChild(script)
        
        script.onload = () => {
          const Hls = (window as any).Hls
          
          if (Hls && Hls.isSupported()) {
            console.log('✅ HLS.js carregado e suportado')
            setHlsSupported(true)
            
            const hls = new Hls({
              debug: true,
              enableWorker: true
            })
            
            hls.loadSource(src)
            hls.attachMedia(video)
            
            hls.on(Hls.Events.MANIFEST_PARSED, () => {
              console.log('✅ Manifest parsed, ready to play')
              setIsLoading(false)
            })
            
            hls.on(Hls.Events.ERROR, (event: any, data: any) => {
              console.error('❌ HLS Error:', data)
              setError(`Erro HLS: ${data.type} - ${data.details}`)
              setIsLoading(false)
            })
            
          } else {
            console.error('❌ HLS.js não suportado')
            setError('HLS não suportado neste navegador')
            setIsLoading(false)
          }
        }
        
        script.onerror = () => {
          console.error('❌ Falha ao carregar HLS.js')
          setError('Falha ao carregar player HLS')
          setIsLoading(false)
        }
        
      } catch (err) {
        console.error('❌ Erro ao inicializar HLS:', err)
        setError('Erro ao inicializar player')
        setIsLoading(false)
      }
    }

    // Se for arquivo .ts, tentar HLS
    if (src.endsWith('.ts')) {
      loadHLS()
    } else {
      // Para outros formatos, usar player nativo
      video.src = src
      setIsLoading(false)
    }

  }, [src])

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="relative w-full max-w-6xl bg-dark-900 rounded-lg overflow-hidden">
        
        {/* Header */}
        <div className="flex justify-between items-center p-4 bg-dark-800/50 border-b border-neon-cyan/20">
          <h3 className="text-lg font-semibold text-white truncate">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Video Container */}
        <div className="relative bg-black min-h-[400px] flex items-center justify-center">
          
          {isLoading && (
            <div className="text-center text-white">
              <div className="animate-spin w-8 h-8 border-2 border-neon-cyan border-t-transparent rounded-full mx-auto mb-4"></div>
              <p>Carregando player...</p>
              <p className="text-sm text-gray-400 mt-2">
                {src.endsWith('.ts') ? 'Inicializando HLS para arquivo .ts' : 'Carregando vídeo'}
              </p>
            </div>
          )}

          {error && (
            <div className="text-center text-white">
              <p className="text-red-400 mb-2">❌ {error}</p>
              <p className="text-sm text-gray-400 mb-4">
                Arquivo: {src.split('/').pop()}
              </p>
              
              {src.endsWith('.ts') && (
                <div className="space-y-3">
                  <p className="text-yellow-400 text-sm">
                    🔄 Arquivo .ts não suportado nativamente
                  </p>
                  <button 
                    onClick={() => {
                      console.log('🚀 Iniciando conversão automática...')
                      fetch('/api/videos/convert', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ key: src.split('/').pop() })
                      }).then(res => res.json())
                        .then(data => {
                          console.log('✅ Conversão iniciada:', data)
                          alert('Conversão iniciada! Aguarde alguns minutos e recarregue a página.')
                        })
                        .catch(err => {
                          console.error('❌ Erro na conversão:', err)
                          alert('Erro ao iniciar conversão')
                        })
                    }}
                    className="px-6 py-3 bg-neon-purple text-white rounded hover:bg-neon-purple/80 transition-colors"
                  >
                    🔄 Converter para MP4
                  </button>
                </div>
              )}
              
              <button 
                onClick={() => window.open(src, '_blank')}
                className="mt-4 px-4 py-2 bg-neon-cyan text-black rounded hover:bg-neon-cyan/80"
              >
                📥 Baixar Arquivo
              </button>
            </div>
          )}

          <video
            ref={videoRef}
            className={`w-full max-h-[70vh] ${isLoading || error ? 'hidden' : 'block'}`}
            controls
            preload="metadata"
            onLoadStart={() => console.log('📦 Video load started')}
            onCanPlay={() => console.log('✅ Video can play')}
            onError={(e) => {
              console.error('❌ Video error:', e)
              setError('Erro ao reproduzir vídeo')
            }}
          />
        </div>

        {/* Info */}
        <div className="p-4 bg-dark-800/30 text-sm text-gray-400">
          <p>
            <span className="text-neon-cyan">Formato:</span> {src.endsWith('.ts') ? 'Transport Stream (.ts)' : 'Vídeo padrão'}
          </p>
          <p>
            <span className="text-neon-cyan">Player:</span> {hlsSupported ? 'HLS.js' : 'Nativo'}
          </p>
          <div className="mt-3 p-3 bg-neon-cyan/10 border border-neon-cyan/30 rounded">
            <p className="text-neon-cyan font-medium mb-1">🔍 Debug Info:</p>
            <p className="text-xs">
              Pressione <kbd className="px-1 py-0.5 bg-gray-700 rounded text-white">F12</kbd> e vá na aba <strong>Console</strong> para ver logs detalhados do player.
            </p>
            <p className="text-xs mt-1">
              Procure por: "HLS PLAYER DEBUG", "✅ HLS.js carregado" ou "❌ HLS Error"
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}