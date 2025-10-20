'use client'

import { useState, useEffect, useRef } from 'react'
import { Play } from 'lucide-react'

interface VideoThumbnailProps {
  videoUrl: string
  videoKey: string
  alt: string
}

export default function VideoThumbnail({ videoUrl, videoKey, alt }: VideoThumbnailProps) {
  const [thumbnail, setThumbnail] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    // Verificar cache
    const cached = localStorage.getItem(`thumb_${videoKey}`)
    if (cached) {
      setThumbnail(cached)
      setLoading(false)
      return
    }

    // Gerar thumbnail com delay (evitar sobrecarga)
    const timer = setTimeout(() => {
      generateThumbnail()
    }, Math.random() * 1000) // Delay aleatório 0-1s

    return () => clearTimeout(timer)
  }, [videoUrl, videoKey])

  const generateThumbnail = () => {
    const video = videoRef.current
    const canvas = canvasRef.current
    
    if (!video || !canvas) return

    video.addEventListener('loadeddata', () => {
      // Ir para segundo 1
      video.currentTime = 1
    })

    video.addEventListener('seeked', () => {
      try {
        const ctx = canvas.getContext('2d')
        if (!ctx) return

        // Definir tamanho do canvas
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight

        // Desenhar frame
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

        // Converter para imagem
        const dataUrl = canvas.toDataURL('image/jpeg', 0.7)
        
        // Salvar no cache
        try {
          localStorage.setItem(`thumb_${videoKey}`, dataUrl)
        } catch (e) {
          // Cache cheio, ignorar
        }

        setThumbnail(dataUrl)
        setLoading(false)
      } catch (error) {
        console.error('Erro ao gerar thumbnail:', error)
        setLoading(false)
      }
    })

    video.addEventListener('error', () => {
      setLoading(false)
    })
  }

  return (
    <>
      {/* Vídeo invisível para captura */}
      <video
        ref={videoRef}
        src={videoUrl}
        crossOrigin="anonymous"
        className="hidden"
        muted
        playsInline
      />
      
      {/* Canvas invisível */}
      <canvas ref={canvasRef} className="hidden" />

      {/* Thumbnail ou Placeholder */}
      {thumbnail ? (
        <img
          src={thumbnail}
          alt={alt}
          className="w-full h-full object-cover"
        />
      ) : loading ? (
        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-900/30 to-blue-900/30">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-white border-t-transparent" />
        </div>
      ) : (
        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-900/30 to-blue-900/30">
          <Play className="w-16 h-16 text-white/50" />
        </div>
      )}
    </>
  )
}
