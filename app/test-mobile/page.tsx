'use client'

import { useState, useEffect } from 'react'
import VideoPlayer from '@/components/modules/VideoPlayer'

interface VideoFile {
  key: string
  name: string
  url: string
  folder: string
}

export default function TestRealVideos() {
  const [videos, setVideos] = useState<VideoFile[]>([])
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchVideos()
  }, [])

  const fetchVideos = async () => {
    try {
      const response = await fetch('/api/videos/list', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.files) {
          setVideos(data.files.slice(0, 5))
        }
      }
    } catch (error) {
      console.error('Erro ao buscar vídeos:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-900 p-4 sm:p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">🎬 Teste Mobile - Vídeos Reais</h1>
        <p className="text-gray-400 mb-8 text-sm sm:text-base">
          Teste os controles mobile com vídeos reais do S3
        </p>

        {loading ? (
          <div className="text-center text-white py-12">
            <div className="loading-shimmer w-16 h-16 rounded-full mx-auto mb-4"></div>
            <p>Carregando vídeos...</p>
          </div>
        ) : videos.length === 0 ? (
          <div className="text-center text-gray-400 py-12">
            <p>Nenhum vídeo encontrado. Faça upload primeiro.</p>
          </div>
        ) : (
          <>
            <div className="grid gap-3 sm:gap-4">
              {videos.map((video) => (
                <button
                  key={video.key}
                  onClick={() => setSelectedVideo(video.key)}
                  className="bg-dark-800 hover:bg-dark-700 p-4 sm:p-6 rounded-lg text-left transition-all"
                >
                  <h3 className="text-white font-semibold mb-1 text-sm sm:text-base">{video.name}</h3>
                  <p className="text-gray-400 text-xs sm:text-sm truncate">{video.folder}</p>
                </button>
              ))}
            </div>

            <div className="mt-6 sm:mt-8 p-4 sm:p-6 bg-neon-cyan/10 border border-neon-cyan/30 rounded-lg">
              <h3 className="text-neon-cyan font-semibold mb-3 text-sm sm:text-base">📱 Controles Mobile (Poco F7):</h3>
              <div className="text-gray-300 space-y-2 text-xs sm:text-sm">
                <div className="flex items-start gap-2">
                  <span className="text-neon-cyan">◄</span>
                  <div>
                    <strong>Laterais (30%):</strong> Swipe horizontal = Avançar/Retroceder 10s
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-neon-cyan">▶</span>
                  <div>
                    <strong>Centro (40%):</strong> Tap = Play/Pause
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-neon-cyan">🔄</span>
                  <div>
                    <strong>Landscape:</strong> Melhor experiência em modo horizontal
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {selectedVideo && (
        <VideoPlayer
          src={selectedVideo}
          title={videos.find(v => v.key === selectedVideo)?.name || 'Teste'}
          currentVideo={videos.find(v => v.key === selectedVideo)}
          playlist={videos}
          onClose={() => setSelectedVideo(null)}
          onVideoChange={(video) => setSelectedVideo(video.key)}
        />
      )}
    </div>
  )
}
