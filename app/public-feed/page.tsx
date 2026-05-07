'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { getApiUrl } from '@/lib/aws-config'
import { getUserFromToken } from '@/lib/auth-utils'
import VideoPlayer from '@/components/modules/VideoPlayer'
import ImageViewer from '@/components/modules/ImageViewer'
import { ConfirmModal } from '@/components/ui/Modal'
import { Heart, MessageCircle, Trash2, Send, ChevronLeft, ChevronRight, Play, Share2 } from 'lucide-react'

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
  liked_by: string[]
  comments: Comment[]
  is_active: boolean
}

interface Comment {
  comment_id: string
  user_id: string
  user_name: string
  text: string
  created_at: string
}

function CategoryRow({ title, items, currentUserId, currentUserRole, onPlay, onLike, onComment, onRemove }: {
  title: string
  items: PublicItem[]
  currentUserId: string
  currentUserRole: string
  onPlay: (item: PublicItem) => void
  onLike: (id: string) => void
  onComment: (id: string, text: string) => void
  onRemove: (id: string) => void
}) {
  const scrollRef = useRef<HTMLDivElement>(null)
  const [showLeft, setShowLeft] = useState(false)
  const [showRight, setShowRight] = useState(false)
  const [commentingOn, setCommentingOn] = useState<string | null>(null)
  const [commentText, setCommentText] = useState('')

  const checkArrows = () => {
    if (!scrollRef.current) return
    const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current
    setShowLeft(scrollLeft > 0)
    setShowRight(scrollLeft < scrollWidth - clientWidth - 10)
  }

  useEffect(() => {
    checkArrows()
    const el = scrollRef.current
    if (el) el.addEventListener('scroll', checkArrows)
    window.addEventListener('resize', checkArrows)
    return () => {
      if (el) el.removeEventListener('scroll', checkArrows)
      window.removeEventListener('resize', checkArrows)
    }
  }, [items])

  const scroll = (direction: 'left' | 'right') => {
    if (!scrollRef.current) return
    scrollRef.current.scrollBy({ left: direction === 'left' ? -300 : 300, behavior: 'smooth' })
  }

  if (items.length === 0) return null

  return (
    <div className="mb-6">
      <h4 className="text-sm font-semibold text-gray-300 mb-2 px-1">
        {title} <span className="text-gray-600 text-xs">({items.length})</span>
      </h4>

      <div className="flex items-start gap-0.5">
        <button
          onClick={() => scroll('left')}
          className={`flex-shrink-0 w-7 h-7 mt-16 rounded-full bg-dark-800/80 border border-cyan-400/30 flex items-center justify-center text-cyan-300 hover:bg-cyan-400/20 transition-all ${showLeft ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        <div
          ref={scrollRef}
          className="flex gap-3 overflow-x-auto flex-1 py-1"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {items.map(item => {
            const isLiked = (item.liked_by || []).includes(currentUserId)
            const canRemove = item.owner_id === currentUserId || currentUserRole === 'admin'

            return (
              <div key={item.content_id} className="flex-shrink-0 w-[200px] sm:w-[230px] md:w-[260px]">
                {/* Preview */}
                <div
                  onClick={() => onPlay(item)}
                  className="relative aspect-video rounded-lg overflow-hidden bg-gradient-to-br from-purple-900/60 to-blue-900/40 border border-white/5 cursor-pointer group transition-all duration-300 hover:scale-[1.03] hover:border-neon-cyan/50 hover:shadow-lg hover:shadow-neon-cyan/10"
                >
                  <div className="absolute inset-0 flex items-center justify-center text-white/50 group-hover:text-white/80 transition-colors">
                    <span className="text-3xl">{item.type === 'video' ? '🎬' : '🖼️'}</span>
                  </div>
                  <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-r from-cyan-500/20 to-purple-500/20 backdrop-blur-sm flex items-center justify-center">
                      <Play className="w-5 h-5 text-cyan-300" fill="currentColor" />
                    </div>
                  </div>
                  {/* Remove button */}
                  {canRemove && (
                    <button
                      onClick={(e) => { e.stopPropagation(); onRemove(item.content_id) }}
                      className="absolute top-1.5 right-1.5 p-1 rounded bg-red-600/70 hover:bg-red-600 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                      title={item.owner_id === currentUserId ? 'Remover' : 'Moderar'}
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  )}
                </div>

                {/* Info */}
                <div className="mt-2 px-0.5">
                  <p className="text-sm text-white font-medium truncate" title={item.title}>{item.title}</p>

                  {/* Like + Comment + Share */}
                  <div className="flex items-center gap-4 mt-2">
                    <button
                      onClick={() => onLike(item.content_id)}
                      className={`flex items-center gap-1.5 text-sm transition-colors ${isLiked ? 'text-red-400' : 'text-gray-500 hover:text-red-400'}`}
                    >
                      <Heart className={`w-5 h-5 ${isLiked ? 'fill-current' : ''}`} />
                      <span>{item.likes || 0}</span>
                    </button>
                    <button
                      onClick={() => setCommentingOn(commentingOn === item.content_id ? null : item.content_id)}
                      className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-neon-cyan transition-colors"
                    >
                      <MessageCircle className="w-5 h-5" />
                      <span>{(item.comments || []).length}</span>
                    </button>
                    <button
                      onClick={() => {
                        const url = `${window.location.origin}/public-feed?play=${item.content_id}`
                        navigator.clipboard.writeText(url)
                        const btn = document.activeElement as HTMLButtonElement
                        const original = btn.innerHTML
                        btn.innerHTML = '<span class="text-xs">Copiado!</span>'
                        setTimeout(() => { btn.innerHTML = original }, 1500)
                      }}
                      className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-cyan-400 transition-colors"
                      title="Copiar link"
                    >
                      <Share2 className="w-4 h-4" />
                    </button>
                  </div>

                  {/* Last comment preview */}
                  {(item.comments || []).length > 0 && commentingOn !== item.content_id && (
                    <p className="text-xs text-gray-500 mt-1 truncate">
                      <span className="text-gray-400">{item.comments[item.comments.length - 1].user_name}:</span> {item.comments[item.comments.length - 1].text}
                    </p>
                  )}

                  {/* Comment input */}
                  {commentingOn === item.content_id && (
                    <div className="mt-2">
                      {(item.comments || []).length > 0 && (
                        <div className="space-y-1 mb-2 max-h-20 overflow-y-auto">
                          {item.comments.slice(-3).map(c => (
                            <p key={c.comment_id} className="text-xs">
                              <span className="text-neon-cyan">{c.user_name}</span>{' '}
                              <span className="text-gray-400">{c.text}</span>
                            </p>
                          ))}
                        </div>
                      )}
                      <div className="flex gap-1">
                        <input
                          type="text"
                          value={commentText}
                          onChange={(e) => setCommentText(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' && commentText.trim()) {
                              onComment(item.content_id, commentText)
                              setCommentText('')
                            }
                          }}
                          placeholder="Comentar..."
                          className="flex-1 px-2 py-1 bg-gray-800 border border-gray-700 rounded text-xs text-white placeholder-gray-500 focus:border-neon-cyan focus:outline-none"
                        />
                        <button
                          onClick={() => {
                            if (commentText.trim()) {
                              onComment(item.content_id, commentText)
                              setCommentText('')
                            }
                          }}
                          className="p-1 text-neon-cyan hover:bg-neon-cyan/10 rounded transition-colors"
                        >
                          <Send className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        <button
          onClick={() => scroll('right')}
          className={`flex-shrink-0 w-7 h-7 mt-16 rounded-full bg-dark-800/80 border border-cyan-400/30 flex items-center justify-center text-cyan-300 hover:bg-cyan-400/20 transition-all ${showRight ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}

export default function PublicFeedPage() {
  const [content, setContent] = useState<PublicItem[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedVideo, setSelectedVideo] = useState<any>(null)
  const [selectedImage, setSelectedImage] = useState<any>(null)
  const [removeModal, setRemoveModal] = useState<string | null>(null)
  const router = useRouter()
  const currentUser = getUserFromToken()

  useEffect(() => {
    if (!currentUser) {
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
      if (data.success) setContent(data.content)
    } catch (e) {
      console.error('Error:', e)
    } finally {
      setLoading(false)
    }
  }

  const handleLike = async (contentId: string) => {
    const token = localStorage.getItem('token')
    const res = await fetch(getApiUrl('PUBLIC_CONTENT'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ action: 'like', content_id: contentId })
    })
    const data = await res.json()
    if (data.success) {
      setContent(prev => prev.map(item =>
        item.content_id === contentId
          ? { ...item, likes: data.likes, liked_by: data.liked ? [...(item.liked_by || []), currentUser!.user_id] : (item.liked_by || []).filter(id => id !== currentUser!.user_id) }
          : item
      ))
    }
  }

  const handleComment = async (contentId: string, text: string) => {
    const token = localStorage.getItem('token')
    const res = await fetch(getApiUrl('PUBLIC_CONTENT'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ action: 'comment', content_id: contentId, text })
    })
    const data = await res.json()
    if (data.success) {
      setContent(prev => prev.map(item =>
        item.content_id === contentId
          ? { ...item, comments: [...(item.comments || []), data.comment] }
          : item
      ))
    }
  }

  const handleRemove = async (contentId: string) => {
    const token = localStorage.getItem('token')
    const res = await fetch(getApiUrl('PUBLIC_CONTENT'), {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ content_id: contentId })
    })
    const data = await res.json()
    if (data.success) setContent(prev => prev.filter(item => item.content_id !== contentId))
  }

  const handlePlay = async (item: PublicItem) => {
    if (item.type === 'video') {
      setSelectedVideo({ key: item.file_key, name: item.title })
    } else if (item.type === 'image') {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(item.file_key)}`, {
          headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
        })
        if (res.ok) {
          const data = await res.json()
          if (data.success && data.viewUrl) {
            setSelectedImage({ url: data.viewUrl, name: item.title })
          }
        }
      } catch (e) {
        console.error('Error getting image URL:', e)
      }
    }
  }

  // Group by user, then by category
  const groupedByUser: Record<string, { name: string; categories: Record<string, PublicItem[]> }> = {}
  content.forEach(item => {
    if (!groupedByUser[item.owner_id]) {
      groupedByUser[item.owner_id] = { name: item.owner_name, categories: {} }
    }
    const cat = item.category || 'Geral'
    if (!groupedByUser[item.owner_id].categories[cat]) {
      groupedByUser[item.owner_id].categories[cat] = []
    }
    groupedByUser[item.owner_id].categories[cat].push(item)
  })

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
          <div className="space-y-8">
            {Object.entries(groupedByUser).map(([userId, userData]) => {
              const totalItems = Object.values(userData.categories).flat().length
              return (
                <div key={userId}>
                  {/* User header */}
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-500 to-purple-500 flex items-center justify-center text-white font-bold">
                      {userData.name?.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <p className="text-base font-semibold text-white">{userData.name}</p>
                      <p className="text-xs text-gray-500">{totalItems} conteúdo(s)</p>
                    </div>
                  </div>

                  {/* Category carousels */}
                  {Object.entries(userData.categories).map(([category, items]) => (
                    <CategoryRow
                      key={`${userId}-${category}`}
                      title={`📁 ${category}`}
                      items={items}
                      currentUserId={currentUser?.user_id || ''}
                      currentUserRole={currentUser?.role || 'user'}
                      onPlay={handlePlay}
                      onLike={handleLike}
                      onComment={handleComment}
                      onRemove={(id) => setRemoveModal(id)}
                    />
                  ))}
                </div>
              )
            })}
          </div>
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
          src={selectedImage.url}
          title={selectedImage.name}
          onClose={() => setSelectedImage(null)}
        />
      )}

      {/* Remove Modal */}
      <ConfirmModal
        isOpen={!!removeModal}
        onClose={() => setRemoveModal(null)}
        onConfirm={() => { if (removeModal) handleRemove(removeModal) }}
        title="Remover conteúdo"
        message="Tem certeza que deseja remover este conteúdo da área pública? O arquivo original não será deletado."
        confirmText="Remover"
        confirmColor="red"
      />
    </div>
  )
}
