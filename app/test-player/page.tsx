'use client'

import { useState, useEffect } from 'react'
import VideoPlayer from '@/components/modules/VideoPlayer'
import { Trash2 } from 'lucide-react'

interface VideoFile {
  key: string
  name: string
  url: string
  folder: string
}

export default function TestPlayerPage() {
  const [videos, setVideos] = useState<VideoFile[]>([])
  const [selectedVideo, setSelectedVideo] = useState<VideoFile | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchVideos()
  }, [])

  const fetchVideos = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/videos/list', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setVideos(data.files.filter((f: any) => f.type === 'video'))
        }
      }
    } catch (err) {
      console.error('Error fetching videos:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (video: VideoFile) => {
    if (!confirm(`Deletar "${video.name}"?`)) return

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/videos/delete', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ key: video.key })
      })

      if (response.ok) {
        alert('Vídeo deletado!')
        fetchVideos()
      } else {
        const data = await response.json()
        alert(`Erro: ${data.message || response.status}`)
      }
    } catch (err) {
      alert('Erro ao deletar')
      console.error(err)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-950 flex items-center justify-center">
        <p className="text-white">Carregando...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-dark-950 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">🎬 Test Player & Delete</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {videos.map((video) => (
            <div key={video.key} className="glass-card p-4">
              <h3 className="text-white font-medium mb-2 truncate">{video.name}</h3>
              <p className="text-gray-400 text-sm mb-4 truncate">{video.folder}</p>
              
              <div className="flex gap-2">
                <button
                  onClick={() => setSelectedVideo(video)}
                  className="flex-1 btn-neon py-2"
                >
                  ▶ Play
                </button>
                <button
                  onClick={() => handleDelete(video)}
                  className="btn-danger p-2"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {videos.length === 0 && (
          <div className="glass-card p-8 text-center">
            <p className="text-gray-400">Nenhum vídeo encontrado</p>
          </div>
        )}
      </div>

      {selectedVideo && (
        <VideoPlayer
          src={selectedVideo.key}
          title={selectedVideo.name}
          currentVideo={selectedVideo}
          playlist={videos}
          onClose={() => setSelectedVideo(null)}
          onVideoChange={setSelectedVideo}
        />
      )}
    </div>
  )
}
