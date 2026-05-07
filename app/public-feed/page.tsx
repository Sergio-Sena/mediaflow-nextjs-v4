'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { getApiUrl } from '@/lib/aws-config'
import { getUserFromToken } from '@/lib/auth-utils'
import VideoPlayer from '@/components/modules/VideoPlayer'
import ImageViewer from '@/components/modules/ImageViewer'
import ContentCarousel from '@/components/modules/ContentCarousel'
import { ArrowLeft } from 'lucide-react'

interface PublicItem {
  content_id: string
  owner_id: string
  owner_name: string
  file_key: string
  title: string
  type: string
  category: string
  shared_at: string
  likes: number
  is_active: boolean
}

export default function PublicFeedPage() {
  const [content, setContent] = useState<PublicItem[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedVideo, setSelectedVideo] = useState<any>(null)
  const [selectedImage, setSelectedImage] = useState<any>(null)
  const router = useRouter()

  useEffect(() => {
    const user = getUserFromToken()
    if (!user) {
      window.location.href = '/login'
      return
    }
    fetchPublicContent()
  }, [])

  const fetchPublicContent = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(getApiUrl('PUBLIC_CONTENT'), {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const data = await res.json()
      if (data.success) {
        setContent(data.content)
      }
    } catch (e) {
      console.error('Error fetching public content:', e)
    } finally {
      setLoading(false)
    }
  }

  // Transform public items to carousel format
  const carouselFiles = content.map(item => ({
    key: item.file_key,
    name: item.title,
    size: 0,
    lastModified: item.shared_at,
    url: '',
    type: item.type,
    folder: item.category
  }))

  const handleItemClick = (file: any) => {
    if (file.type === 'video') {
      setSelectedVideo({ key: file.key, name: file.name, folder: file.folder })
    } else if (file.type === 'image') {
      setSelectedImage({ key: file.key, name: file.name, folder: file.folder })
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="loading-shimmer w-16 h-16 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-400">Carregando conteúdo público...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-dark-900/50 backdrop-blur-md border-b border-neon-cyan/20 sticky top-0 z-50">
        <div className="mx-auto px-4 sm:px-8 py-3 sm:py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <h1
                className="text-lg sm:text-2xl font-bold cursor-pointer hover:scale-105 transition-transform duration-300"
                onClick={() => router.push('/dashboard')}
              >
                🎬 <span className="neon-text">Mídiaflow</span>
              </h1>
              <span className="text-gray-600">|</span>
              <span className="text-sm sm:text-lg font-semibold text-white">🌐 Área Pública</span>
            </div>
            <button
              onClick={() => router.push('/dashboard')}
              className="px-3 py-1.5 bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border border-purple-500/30 rounded-lg transition-colors text-sm font-medium"
            >
              🔒 Minha Biblioteca
            </button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="mx-auto px-4 sm:px-8 py-6">
        {content.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">📭</div>
            <h2 className="text-xl font-bold text-white mb-2">Nenhum conteúdo público ainda</h2>
            <p className="text-gray-400 mb-6">Compartilhe vídeos e imagens do seu dashboard para aparecerem aqui.</p>
            <button
              onClick={() => router.push('/dashboard')}
              className="px-6 py-3 bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/50 rounded-lg hover:bg-neon-cyan/30 transition-colors"
            >
              Ir para Dashboard
            </button>
          </div>
        ) : (
          <ContentCarousel
            files={carouselFiles}
            onItemClick={handleItemClick}
            selectionMode={false}
            selectedKeys={new Set()}
          />
        )}
      </main>

      {/* Video Player */}
      {selectedVideo && (
        <VideoPlayer
          src={selectedVideo.key}
          title={selectedVideo.name}
          onClose={() => setSelectedVideo(null)}
        />
      )}

      {/* Image Viewer */}
      {selectedImage && (
        <ImageViewer
          src={selectedImage.key}
          title={selectedImage.name}
          onClose={() => setSelectedImage(null)}
        />
      )}
    </div>
  )
}
