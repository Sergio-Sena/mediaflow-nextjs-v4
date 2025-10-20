'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

import DirectUpload from '@/components/modules/DirectUpload'
import FileList from '@/components/modules/FileList'
import VideoPlayer from '@/components/modules/VideoPlayer'
import ImageViewer from '@/components/modules/ImageViewer'
import PDFViewer from '@/components/modules/PDFViewer'
import Analytics from '@/components/modules/Analytics'
import FolderManager from '@/components/modules/FolderManager'
import AvatarUpload from '@/components/AvatarUpload'
import HeroSection from '@/components/modules/HeroSection'
import VideoCarousel from '@/components/modules/VideoCarousel'


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
  const [activeTab, setActiveTab] = useState<'home' | 'files' | 'upload' | 'manager' | 'analytics'>('home')
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
    
    if (!token) {
      router.push('/login')
      return
    }

    // Verificar sessão 2FA apenas para admin (30 minutos = 1800000ms)
    const session = localStorage.getItem('2fa_session')
    const isAdmin = currentUserData ? 
      JSON.parse(currentUserData).role === 'admin' || 
      JSON.parse(currentUserData).user_id === 'user_admin' : false
    
    if (isAdmin && (!session || (Date.now() - parseInt(session)) > 1800000)) {
      router.push('/2fa')
      return
    }

    // Priorizar current_user (multi-usuário) sobre user (legado)
    if (currentUserData) {
      const user = JSON.parse(currentUserData)
      setCurrentUser(user)
      // Recarregar dados do usuário para pegar avatar atualizado
      fetchUserData(user.user_id || user.id)
    }
    
    if (userData) {
      setUser(JSON.parse(userData))
    }
    
    setLoading(false)
  }, [router])

  const fetchUserData = async (userId: string) => {
    try {
      const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users')
      const data = await res.json()
      if (data.success) {
        const updatedUser = data.users.find((u: any) => u.user_id === userId)
        if (updatedUser) {
          console.log('User data loaded:', updatedUser)
          setCurrentUser(updatedUser)
          localStorage.setItem('current_user', JSON.stringify(updatedUser))
        }
      }
    } catch (error) {
      console.error('Error fetching user data:', error)
    }
  }

  const handleRefresh = () => {
    setRefreshTrigger(prev => prev + 1)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/')
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
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="loading-shimmer w-16 h-16 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-400">Carregando...</p>
        </div>
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
                    }}
                  />
                  <div className="text-sm">
                    <div className="text-neon-cyan font-semibold truncate max-w-[100px]">
                      {currentUser.role === 'admin' || currentUser.user_id === 'user_admin' ? 'Admin' : currentUser.name}
                    </div>
                  </div>
                </div>
              )}
              {!currentUser && user && (
                <div className="text-sm text-gray-300">
                  Olá, <span className="text-neon-cyan">{user?.name}</span>
                </div>
              )}
              {(currentUser?.user_id === 'admin' || currentUser?.user_id === 'user_admin' || currentUser?.id === 'user_admin') && (
                <button
                  onClick={() => router.push('/admin')}
                  className="btn-neon px-4 py-2 text-sm flex items-center gap-2"
                >
                  <span>👥</span>
                  Gerenciamento
                </button>
              )}
              <button
                onClick={logout}
                className="btn-secondary px-4 py-2 text-sm"
              >
                Sair
              </button>
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
                    }}
                  />
                  <div className="text-sm">
                    <div className="text-neon-cyan font-semibold">{currentUser.name}</div>
                  </div>
                </div>
              )}
              {(currentUser?.user_id === 'admin' || currentUser?.user_id === 'user_admin' || currentUser?.id === 'user_admin') && (
                <button
                  onClick={() => {
                    router.push('/admin')
                    setMobileMenuOpen(false)
                  }}
                  className="btn-neon w-full px-4 py-3 text-sm flex items-center justify-center gap-2"
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
                </button>
              )}
              <button
                onClick={() => {
                  logout()
                  setMobileMenuOpen(false)
                }}
                className="btn-secondary w-full px-4 py-3 text-sm"
              >
                🚪 Sair do Sistema
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-dark-800/30 backdrop-blur-sm border-b border-neon-cyan/10 overflow-x-auto">
        <div className="max-w-7xl mx-auto px-2 sm:px-4">
          <div className="flex space-x-2 sm:space-x-4 md:space-x-8 min-w-max">
            {[
              { id: 'home', label: '🏠 Início', count: 0 },
              { id: 'files', label: '📁 Biblioteca', count: 0 },
              { id: 'upload', label: '📤 Upload', count: 0 },
              { id: 'manager', label: '🗂️ Gerenciador', count: 0 },
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
        {activeTab === 'home' && (
          <div className="space-y-8">
            {/* Hero Section */}
            <HeroSection
              video={allFiles.find(f => f.type === 'video') ? {
                name: allFiles.find(f => f.type === 'video')!.name,
                url: allFiles.find(f => f.type === 'video')!.url,
                description: 'Continue de onde parou'
              } : undefined}
              onPlay={() => {
                // Buscar último vídeo assistido ou primeiro disponível
                const lastWatched = localStorage.getItem('last_watched_video')
                let videoToPlay = allFiles.find(f => f.type === 'video')
                
                if (lastWatched) {
                  const lastVideo = allFiles.find(f => f.key === lastWatched)
                  if (lastVideo) videoToPlay = lastVideo
                }
                
                if (videoToPlay) {
                  setSelectedVideo(videoToPlay)
                  setVideoPlaylist(allFiles.filter(f => f.type === 'video'))
                }
              }}
            />

            {/* Carrosséis */}
            <VideoCarousel
              title="Adicionados Recentemente"
              videos={allFiles
                .filter(f => f.type === 'video')
                .sort((a, b) => new Date(b.lastModified).getTime() - new Date(a.lastModified).getTime())
                .slice(0, 10)
                .map(f => ({
                  key: f.key,
                  name: f.name,
                  url: f.url
                }))}
              onVideoClick={(video) => {
                const fileItem = allFiles.find(f => f.key === video.key)
                if (fileItem) {
                  setSelectedVideo(fileItem)
                  setVideoPlaylist(allFiles.filter(f => f.type === 'video'))
                }
              }}
            />

            {/* Por Pasta */}
            {Array.from(new Set(allFiles.filter(f => f.type === 'video').map(f => f.folder))).map(folder => (
              <VideoCarousel
                key={folder}
                title={`Pasta: ${folder || 'Root'}`}
                videos={allFiles
                  .filter(f => f.type === 'video' && f.folder === folder)
                  .slice(0, 10)
                  .map(f => ({
                    key: f.key,
                    name: f.name,
                    url: f.url
                  }))}
                onVideoClick={(video) => {
                  const fileItem = allFiles.find(f => f.key === video.key)
                  if (fileItem) {
                    setSelectedVideo(fileItem)
                    setVideoPlaylist(allFiles.filter(f => f.type === 'video' && f.folder === folder))
                  }
                }}
              />
            ))}
          </div>
        )}

        {activeTab === 'files' && (
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
        )}

        {activeTab === 'upload' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-white">Upload de Arquivos</h2>
              <button
                onClick={() => setActiveTab('files')}
                className="btn-secondary px-4 py-3 text-sm min-h-[44px]"
              >
                📁 Ver Arquivos
              </button>
            </div>
            
            <DirectUpload
              maxFiles={100}
              maxSize={10240}
              onUploadComplete={(uploadedFiles) => {
                console.log('Upload concluído:', uploadedFiles)
                handleRefresh()
                setActiveTab('files')
              }}
            />
          </div>
        )}

        {activeTab === 'manager' && (
          <div className="space-y-6">
            <FolderManager 
              onNavigateToFolder={(folderPath) => {
                // Switch to files tab and navigate to folder
                setCurrentFolderPath(folderPath)
                setActiveTab('files')
              }}
              onFilesLoaded={setAllFiles}
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
        <VideoPlayer
          src={selectedVideo.url}
          title={selectedVideo.name}
          currentVideo={selectedVideo}
          playlist={videoPlaylist}
          onClose={() => setSelectedVideo(null)}
          onVideoChange={(video) => {
            // Convert VideoFile to FileItem
            const fileItem: FileItem = {
              key: video.key,
              name: video.name,
              url: video.url,
              folder: video.folder,
              size: 0, // Will be updated from allFiles if needed
              lastModified: new Date().toISOString(),
              type: 'video'
            }
            setSelectedVideo(fileItem)
          }}
        />
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