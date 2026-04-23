'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button, Card, Skeleton } from '@/components/ui'
import { DashboardSkeleton, FileListSkeleton, VideoPlayerSkeleton } from '@/components/ui/Skeleton'
import { ErrorBoundary } from '@/components/ui/ErrorBoundary'
import { getUserApiUrl } from '@/lib/aws-config'

import DirectUpload from '@/components/modules/DirectUpload'
import FileList from '@/components/modules/FileList'
import VideoPlayer from '@/components/modules/VideoPlayer'
import ImageViewer from '@/components/modules/ImageViewer'
import PDFViewer from '@/components/modules/PDFViewer'
import Analytics from '@/components/modules/Analytics'
import FolderManagerV2 from '@/components/modules/FolderManagerV2'

import AvatarUpload from '@/components/AvatarUpload'



interface User {
  email: string
  name: string
  role: string
}

interface FileItem {
  key: string
  name: string
  size: number
  lastModified: string
  url: string
  type: string
  folder: string
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'files' | 'folders' | 'upload' | 'analytics'>('files')
  const [selectedVideo, setSelectedVideo] = useState<FileItem | null>(null)
  const [selectedImage, setSelectedImage] = useState<FileItem | null>(null)
  const [selectedPDF, setSelectedPDF] = useState<FileItem | null>(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const [allFiles, setAllFiles] = useState<FileItem[]>([])
  const [videoPlaylist, setVideoPlaylist] = useState<FileItem[]>([])
  const [imagePlaylist, setImagePlaylist] = useState<FileItem[]>([])
  const [currentFolderPath, setCurrentFolderPath] = useState<string>('')
  const router = useRouter()

  const [currentUser, setCurrentUser] = useState<any>(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    // Verificar autenticação
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    const currentUserData = localStorage.getItem('current_user')
    
    // Validar token - se tiver caracteres HTML encoded, limpar
    if (token && (token.includes('&#') || token.includes('&amp;') || token.includes('&lt;') || token.includes('&gt;'))) {
      console.error('❌ Token corrompido detectado! Limpando...')
      localStorage.clear()
      router.push('/login')
      return
    }
    
    // Construir current_user a partir do JWT (fonte confiável)
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        const saved = currentUserData ? JSON.parse(currentUserData) : {}
        const fullUser = {
          user_id: payload.user_id,
          name: saved.name || payload.email?.split('@')[0] || 'Usuário',
          email: payload.email,
          role: payload.role || 'user',
          s3_prefix: payload.s3_prefix || '',
          avatar_url: saved.avatar_url || ''
        }
        localStorage.setItem('current_user', JSON.stringify(fullUser))
        setCurrentUser(fullUser)
        if (fullUser.role !== 'admin') {
          setCurrentFolderPath(fullUser.s3_prefix || '')
        }
        // Buscar avatar atualizado do DynamoDB
        fetchUserData(payload.user_id)
      } catch (e) {
        console.error('Erro ao decodificar JWT:', e)
      }
    }
    
    if (!token) {
      window.location.href = '/login'
      return
    }

    // Verificar sessão 2FA apenas para admin (30 minutos = 1800000ms)
    const session = localStorage.getItem('2fa_session')
    const isAdmin = currentUserData ? 
      JSON.parse(currentUserData).role === 'admin' || 
      JSON.parse(currentUserData).user_id === 'user_admin' ||
      JSON.parse(currentUserData).user_id === 'admin_sistema' : false
    
    if (isAdmin && (!session || (Date.now() - parseInt(session)) > 1800000)) {
      window.location.href = '/2fa'
      return
    }
    
    if (userData) {
      setUser(JSON.parse(userData))
    }
    
    setLoading(false)
  }, [router])

  const fetchUserData = async (userId: string) => {
    try {
      const token = localStorage.getItem('token')
      if (!token) return
      
      const response = await fetch(getUserApiUrl(userId), {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.user) {
          const updated = { ...currentUser, avatar_url: data.user.avatar_url }
          setCurrentUser(updated)
          localStorage.setItem('current_user', JSON.stringify(updated))
        }
      }
    } catch (error) {
      console.error('Erro ao buscar dados do usuário:', error)
    }
  }

  const handleRefresh = () => {
    setRefreshTrigger(prev => prev + 1)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/'
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
  }

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'video': return '🎥'
      case 'image': return '📸'
      case 'document': return '📄'
      default: return '📁'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen p-8">
        <DashboardSkeleton />
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-dark-900/50 backdrop-blur-md border-b border-neon-cyan/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-2 sm:px-4 py-3 sm:py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2 sm:gap-4">
              <h1 
                className="text-lg sm:text-2xl font-bold cursor-pointer hover:scale-105 transition-transform duration-300"
                onClick={() => window.location.reload()}
              >
                🎬 <span className="neon-text">Mídiaflow</span>
              </h1>
              <div className="hidden md:block text-sm text-gray-400">
                Dashboard v4.3
              </div>
            </div>
            
            {/* Desktop Menu */}
            <div className="hidden lg:flex items-center gap-2 md:gap-4">
              {currentUser?.plan === 'trial' && (
                <div className="glass-card px-3 py-1.5 border border-yellow-500/50 bg-yellow-500/10">
                  <div className="text-xs text-yellow-400 font-semibold">
                    ⏱️ Trial - {Math.max(0, Math.ceil((new Date(currentUser.trial_end).getTime() - Date.now()) / (1000 * 60 * 60 * 24)))} dias
                  </div>
                </div>
              )}
              {currentUser && (
                <div className="flex items-center gap-2 glass-card px-4 py-2">
                  <AvatarUpload
                    userId={currentUser.user_id || currentUser.id}
                    currentAvatar={currentUser.avatar_url}
                    size="sm"
                    className="flex-shrink-0"
                    onAvatarUpdate={(avatarUrl) => {
                      const updated = { ...currentUser, avatar_url: avatarUrl }
                      setCurrentUser(updated)
                      localStorage.setItem('current_user', JSON.stringify(updated))
                      setTimeout(() => fetchUserData(currentUser.user_id || currentUser.id), 500)
                    }}
                  />
                  <div className="text-sm">
                    <div className="text-neon-cyan font-semibold truncate max-w-[100px]">
                      {currentUser.role === 'admin' ? 'Admin' : currentUser.name}
                    </div>
                  </div>
                </div>
              )}
              {!currentUser && user && (
                <div className="text-sm text-gray-300">
                  Olá, <span className="text-neon-cyan">{user?.name}</span>
                </div>
              )}
              {(currentUser?.role === 'admin') && (
                <Button
                  onClick={() => router.push('/admin')}
                  variant="primary"
                  size="sm"
                >
                  <span>👥</span>
                  Gerenciamento
                </Button>
              )}
              <Button
                onClick={logout}
                variant="secondary"
                size="sm"
              >
                Sair
              </Button>
            </div>

            {/* Mobile Hamburger */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden btn-secondary p-3 text-xl min-h-[44px] min-w-[44px]"
            >
              {mobileMenuOpen ? '✕' : '☰'}
            </button>
          </div>

          {/* Mobile Menu Dropdown */}
          {mobileMenuOpen && (
            <div className="lg:hidden mt-4 space-y-3 pb-4 border-t border-neon-cyan/20 pt-4">
              {currentUser && (
                <div className="flex items-center gap-3 glass-card px-4 py-3">
                  <AvatarUpload
                    userId={currentUser.user_id || currentUser.id}
                    currentAvatar={currentUser.avatar_url}
                    size="sm"
                    className="flex-shrink-0"
                    onAvatarUpdate={(avatarUrl) => {
                      const updated = { ...currentUser, avatar_url: avatarUrl }
                      setCurrentUser(updated)
                      localStorage.setItem('current_user', JSON.stringify(updated))
                      setTimeout(() => fetchUserData(currentUser.user_id || currentUser.id), 500)
                    }}
                  />
                  <div className="text-sm">
                    <div className="text-neon-cyan font-semibold">{currentUser.name}</div>
                  </div>
                </div>
              )}
              {(currentUser?.role === 'admin') && (
                <Button
                  onClick={() => {
                    router.push('/admin')
                    setMobileMenuOpen(false)
                  }}
                  variant="primary"
                  size="md"
                  className="w-full"
                >
                  {currentUser.avatar_url ? (
                    <img 
                      src={currentUser.avatar_url} 
                      alt="Admin"
                      className="w-5 h-5 rounded-full object-cover border border-neon-cyan/50"
                    />
                  ) : (
                    <span>👥</span>
                  )}
                  Painel Admin
                </Button>
              )}
              <Button
                onClick={() => {
                  logout()
                  setMobileMenuOpen(false)
                }}
                variant="secondary"
                size="md"
                className="w-full"
              >
                🚪 Sair do Sistema
              </Button>
            </div>
          )}
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-dark-800/30 backdrop-blur-sm border-b border-neon-cyan/10 overflow-x-auto">
        <div className="max-w-7xl mx-auto px-2 sm:px-4">
          <div className="flex space-x-2 sm:space-x-4 md:space-x-8 min-w-max">
            {[
              ...(currentUser?.role !== 'admin' ? [{ id: 'files', label: '📁 Biblioteca', count: 0 }] : []),
              { id: 'folders', label: '🗂️ Pastas', count: 0 },
              { id: 'upload', label: '📤 Upload', count: 0 },
              { id: 'analytics', label: '📊 Analytics', count: 0 },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-3 sm:py-4 px-2 sm:px-3 border-b-2 font-medium text-xs sm:text-sm whitespace-nowrap transition-all duration-300 ${
                  activeTab === tab.id
                    ? 'border-neon-cyan text-neon-cyan'
                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-neon-cyan/30'
                }`}
              >
                {tab.label}
                {tab.count > 0 && (
                  <span className="ml-2 px-2 py-1 bg-neon-cyan/20 text-neon-cyan text-xs rounded-full">
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-2 sm:px-4 py-4 sm:py-8">
        {/* Trial Progress */}
        {currentUser?.plan === 'trial' && (
          <Card variant="glass" padding="md" className="mb-6 border border-yellow-500/30">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-yellow-400">📊 Uso do Trial</h3>
              <Button variant="primary" size="sm">Fazer Upgrade</Button>
            </div>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-400">Storage</span>
                  <span className="text-white">{((currentUser.storage_used || 0) / 1024 / 1024 / 1024).toFixed(2)} GB / {(currentUser.storage_limit / 1024 / 1024 / 1024).toFixed(0)} GB</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-neon-cyan to-neon-purple h-2 rounded-full transition-all duration-300"
                    style={{ width: `${Math.min(100, ((currentUser.storage_used || 0) / currentUser.storage_limit) * 100)}%` }}
                  />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-400">Bandwidth</span>
                  <span className="text-white">{((currentUser.bandwidth_used || 0) / 1024 / 1024 / 1024).toFixed(2)} GB / {(currentUser.bandwidth_limit / 1024 / 1024 / 1024).toFixed(0)} GB</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-neon-purple to-neon-pink h-2 rounded-full transition-all duration-300"
                    style={{ width: `${Math.min(100, ((currentUser.bandwidth_used || 0) / currentUser.bandwidth_limit) * 100)}%` }}
                  />
                </div>
              </div>
            </div>
          </Card>
        )}


        {activeTab === 'files' && (
          <ErrorBoundary fallback={<FileListSkeleton />}>
            <FileList 
            onPlayVideo={(video) => {
              setSelectedVideo(video)
              // Create playlist from videos in same folder
              const videosInFolder = allFiles.filter(f => 
                f.type === 'video' && f.folder === video.folder
              )
              setVideoPlaylist(videosInFolder)
            }}
            onViewImage={(image) => {
              setSelectedImage(image)
              // Create playlist from images in same folder
              const imagesInFolder = allFiles.filter(f => 
                f.type === 'image' && f.folder === image.folder
              )
              setImagePlaylist(imagesInFolder)
            }}
            onViewPDF={setSelectedPDF}
            refreshTrigger={refreshTrigger}
            onFilesLoaded={setAllFiles}
            targetFolder={currentFolderPath}
          />
          </ErrorBoundary>
        )}

        {activeTab === 'folders' && (
          <FolderManagerV2
            currentPath={currentFolderPath}
            onNavigate={async (path) => {
              setCurrentFolderPath(path)
              setActiveTab('files')
              // Aguardar FileList carregar e abrir primeiro vídeo com URL assinada
              setTimeout(async () => {
                const firstVideo = allFiles.find(f => f.type === 'video' && f.folder === path)
                if (firstVideo) {
                  // Buscar URL assinada
                  try {
                    const response = await fetch(`/api/videos/view?key=${encodeURIComponent(firstVideo.key)}`, {
                      method: 'GET',
                      headers: { 'Content-Type': 'application/json' }
                    })
                    
                    if (response.ok) {
                      const data = await response.json()
                      if (data.success) {
                        setSelectedVideo({ ...firstVideo, url: data.viewUrl })
                        const videosInFolder = allFiles.filter(f => f.type === 'video' && f.folder === path)
                        setVideoPlaylist(videosInFolder)
                      }
                    }
                  } catch (error) {
                    console.error('Erro ao buscar URL assinada:', error)
                    setSelectedVideo(firstVideo)
                    const videosInFolder = allFiles.filter(f => f.type === 'video' && f.folder === path)
                    setVideoPlaylist(videosInFolder)
                  }
                }
              }, 500)
            }}
          />
        )}

        {activeTab === 'upload' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-white">Upload de Arquivos</h2>
              <Button
                onClick={() => setActiveTab('files')}
                variant="secondary"
                size="md"
              >
                📁 Ver Arquivos
              </Button>
            </div>
            
            <DirectUpload
              maxFiles={100}
              maxSize={10240}
              onUploadComplete={(uploadedFiles) => {
                console.log('✅ Todos os uploads concluídos:', uploadedFiles)
                handleRefresh()
                setActiveTab('files')
              }}
            />
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-white">Analytics & Relatórios</h2>
            </div>
            
            <Analytics />
          </div>
        )}
      </main>

      {/* Viewers */}
      {selectedVideo && (
        <ErrorBoundary fallback={<VideoPlayerSkeleton />}>
          <VideoPlayer
            src={selectedVideo.key}
            title={selectedVideo.name}
            currentVideo={selectedVideo}
            playlist={videoPlaylist}
            onClose={() => setSelectedVideo(null)}
            onVideoChange={(video) => {
              const fileItem: FileItem = {
                key: video.key,
                name: video.name,
                url: video.url,
                folder: video.folder,
                size: 0,
                lastModified: new Date().toISOString(),
                type: 'video'
              }
              setSelectedVideo(fileItem)
            }}
          />
        </ErrorBoundary>
      )}
      
      {selectedImage && (
        <ImageViewer
          src={selectedImage.url}
          title={selectedImage.name}
          currentImage={selectedImage}
          playlist={imagePlaylist}
          onClose={() => setSelectedImage(null)}
          onImageChange={(image) => {
            // Convert ImageFile to FileItem
            const fileItem: FileItem = {
              key: image.key,
              name: image.name,
              url: image.url,
              folder: image.folder,
              size: 0, // Will be updated from allFiles if needed
              lastModified: new Date().toISOString(),
              type: 'image'
            }
            setSelectedImage(fileItem)
          }}
        />
      )}
      
      {selectedPDF && (
        <PDFViewer
          src={selectedPDF.url}
          title={selectedPDF.name}
          onClose={() => setSelectedPDF(null)}
        />
      )}
    </div>
  )
}
