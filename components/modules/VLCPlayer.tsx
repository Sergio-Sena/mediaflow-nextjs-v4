'use client'

import { useEffect, useRef, useState } from 'react'

interface VLCPlayerProps {
  src: string
  title: string
  onClose?: () => void
}

export default function VLCPlayer({ src, title, onClose }: VLCPlayerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [vlcStatus, setVlcStatus] = useState<'loading' | 'ready' | 'error' | 'not-installed'>('loading')
  const [errorMessage, setErrorMessage] = useState<string>('')

  useEffect(() => {
    console.log('=== VLC PLAYER DEBUG ===')
    console.log('Source:', src)
    console.log('Checking VLC Web Plugin...')

    const checkVLC = () => {
      // Verificar se VLC Web Plugin está disponível
      const vlcPlugin = (window as any).VLC || (navigator as any).plugins['VLC Web Plugin']
      
      if (vlcPlugin) {
        console.log('✅ VLC Web Plugin detectado')
        initVLCPlayer()
      } else {
        console.log('❌ VLC Web Plugin não encontrado')
        // Tentar carregar via embed/object
        tryEmbedVLC()
      }
    }

    const initVLCPlayer = () => {
      try {
        const container = containerRef.current
        if (!container) return

        // Criar elemento VLC
        const vlcEmbed = document.createElement('embed')
        vlcEmbed.setAttribute('type', 'application/x-vlc-plugin')
        vlcEmbed.setAttribute('pluginspage', 'http://www.videolan.org')
        vlcEmbed.setAttribute('target', src)
        vlcEmbed.setAttribute('width', '100%')
        vlcEmbed.setAttribute('height', '400')
        vlcEmbed.setAttribute('autoplay', 'yes')
        vlcEmbed.setAttribute('loop', 'no')
        vlcEmbed.setAttribute('controls', 'yes')

        container.appendChild(vlcEmbed)
        
        console.log('✅ VLC Player inicializado')
        setVlcStatus('ready')
        
      } catch (error) {
        console.error('❌ Erro ao inicializar VLC:', error)
        setErrorMessage('Erro ao inicializar VLC Player')
        setVlcStatus('error')
      }
    }

    const tryEmbedVLC = () => {
      try {
        const container = containerRef.current
        if (!container) return

        // Tentar object tag para VLC
        const vlcObject = document.createElement('object')
        vlcObject.setAttribute('classid', 'clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921')
        vlcObject.setAttribute('width', '100%')
        vlcObject.setAttribute('height', '400')
        vlcObject.setAttribute('codebase', 'http://download.videolan.org/pub/videolan/vlc/last/win32/axvlc.cab')

        // Parâmetros VLC
        const params = [
          { name: 'Src', value: src },
          { name: 'ShowDisplay', value: 'true' },
          { name: 'AutoLoop', value: 'false' },
          { name: 'AutoPlay', value: 'true' }
        ]

        params.forEach(param => {
          const paramElement = document.createElement('param')
          paramElement.setAttribute('name', param.name)
          paramElement.setAttribute('value', param.value)
          vlcObject.appendChild(paramElement)
        })

        // Fallback embed
        const embedFallback = document.createElement('embed')
        embedFallback.setAttribute('type', 'application/x-vlc-plugin')
        embedFallback.setAttribute('target', src)
        embedFallback.setAttribute('width', '100%')
        embedFallback.setAttribute('height', '400')
        vlcObject.appendChild(embedFallback)

        container.appendChild(vlcObject)
        
        // Verificar se carregou após 3 segundos
        setTimeout(() => {
          if (vlcObject.clientHeight > 0) {
            console.log('✅ VLC Object carregado')
            setVlcStatus('ready')
          } else {
            console.log('❌ VLC não disponível')
            setVlcStatus('not-installed')
            setErrorMessage('VLC Web Plugin não instalado')
          }
        }, 3000)
        
      } catch (error) {
        console.error('❌ Erro ao tentar embed VLC:', error)
        setVlcStatus('not-installed')
        setErrorMessage('VLC não disponível neste navegador')
      }
    }

    checkVLC()

    return () => {
      // Cleanup
      if (containerRef.current) {
        containerRef.current.innerHTML = ''
      }
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

        {/* VLC Container */}
        <div className="relative bg-black min-h-[400px] flex items-center justify-center">
          
          {vlcStatus === 'loading' && (
            <div className="text-center text-white">
              <div className="animate-spin w-8 h-8 border-2 border-neon-cyan border-t-transparent rounded-full mx-auto mb-4"></div>
              <p>Carregando VLC Player...</p>
              <p className="text-sm text-gray-400 mt-2">Verificando plugin VLC</p>
            </div>
          )}

          {vlcStatus === 'not-installed' && (
            <div className="text-center text-white max-w-md">
              <p className="text-red-400 mb-4">🚫 VLC Web Plugin não encontrado</p>
              <div className="space-y-3 text-sm text-gray-300">
                <p>Para reproduzir arquivos .ts, instale o VLC Media Player:</p>
                <ol className="text-left space-y-1">
                  <li>1. Baixe VLC: <a href="https://www.videolan.org/vlc/" target="_blank" className="text-neon-cyan hover:underline">videolan.org</a></li>
                  <li>2. Instale com "Web Plugin" habilitado</li>
                  <li>3. Reinicie o navegador</li>
                  <li>4. Recarregue esta página</li>
                </ol>
              </div>
              <button 
                onClick={() => window.open(src, '_blank')}
                className="mt-4 px-4 py-2 bg-neon-cyan text-black rounded hover:bg-neon-cyan/80"
              >
                📥 Baixar Arquivo
              </button>
            </div>
          )}

          {vlcStatus === 'error' && (
            <div className="text-center text-white">
              <p className="text-red-400 mb-2">❌ {errorMessage}</p>
              <button 
                onClick={() => window.open(src, '_blank')}
                className="mt-4 px-4 py-2 bg-neon-cyan text-black rounded hover:bg-neon-cyan/80"
              >
                📥 Baixar Arquivo
              </button>
            </div>
          )}

          {/* VLC Player Container */}
          <div 
            ref={containerRef}
            className={`w-full ${vlcStatus === 'ready' ? 'block' : 'hidden'}`}
            style={{ minHeight: '400px' }}
          />
        </div>

        {/* Info */}
        <div className="p-4 bg-dark-800/30 text-sm text-gray-400">
          <p>
            <span className="text-neon-cyan">Player:</span> VLC Web Plugin
          </p>
          <p>
            <span className="text-neon-cyan">Status:</span> {vlcStatus}
          </p>
          <div className="mt-3 p-3 bg-neon-cyan/10 border border-neon-cyan/30 rounded">
            <p className="text-neon-cyan font-medium mb-1">🔍 Debug Info:</p>
            <p className="text-xs">
              Pressione <kbd className="px-1 py-0.5 bg-gray-700 rounded text-white">F12</kbd> → Console para logs do VLC Player
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}