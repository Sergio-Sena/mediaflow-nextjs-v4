'use client'

import { useState } from 'react'
import VideoPlayer from '@/components/modules/VideoPlayer'

export default function TestLocalVideos() {
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null)

  const testVideos = [
    { key: 'local:video1.mp4', name: 'Vídeo Teste 1', folder: 'Local', url: '' },
    { key: 'local:video2.mp4', name: 'Vídeo Teste 2', folder: 'Local', url: '' },
    { key: 'local:sample.mp4', name: 'Sample Video', folder: 'Local', url: '' }
  ]

  return (
    <div className="min-h-screen bg-dark-900 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">🎬 Teste de Vídeos Locais</h1>
        <p className="text-gray-400 mb-8">
          Coloque seus vídeos em <code className="bg-dark-800 px-2 py-1 rounded">public/test-videos/</code>
        </p>

        <div className="grid gap-4">
          {testVideos.map((video) => (
            <button
              key={video.key}
              onClick={() => setSelectedVideo(video.key)}
              className="bg-dark-800 hover:bg-dark-700 p-6 rounded-lg text-left transition-all"
            >
              <h3 className="text-white font-semibold mb-1">{video.name}</h3>
              <p className="text-gray-400 text-sm">{video.key}</p>
            </button>
          ))}
        </div>

        <div className="mt-8 p-6 bg-neon-cyan/10 border border-neon-cyan/30 rounded-lg">
          <h3 className="text-neon-cyan font-semibold mb-2">📝 Como usar:</h3>
          <ol className="text-gray-300 space-y-2 text-sm">
            <li>1. Coloque seus vídeos MP4 em <code className="bg-dark-800 px-2 py-1 rounded">public/test-videos/</code></li>
            <li>2. Clique em um dos botões acima para testar</li>
            <li>3. Teste os controles mobile (toque, swipe, etc)</li>
            <li>4. Ajustes não afetam produção (apenas local)</li>
          </ol>
        </div>
      </div>

      {selectedVideo && (
        <VideoPlayer
          src={selectedVideo}
          title={testVideos.find(v => v.key === selectedVideo)?.name || 'Teste'}
          currentVideo={testVideos.find(v => v.key === selectedVideo)}
          playlist={testVideos}
          onClose={() => setSelectedVideo(null)}
          onVideoChange={(video) => setSelectedVideo(video.key)}
        />
      )}
    </div>
  )
}
