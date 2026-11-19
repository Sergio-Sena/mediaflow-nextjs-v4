'use client'

import { useState, useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Button, Card, Skeleton } from '@/components/ui'
import { DashboardSkeleton, FileListSkeleton, VideoPlayerSkeleton } from '@/components/ui/Skeleton'
import { ErrorBoundary } from '@/components/ui/ErrorBoundary'
import { getUserApiUrl } from '@/lib/aws-config'
import { getUserFromToken } from '@/lib/auth-utils'

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
  duration?: number
}

function DashboardContent() {
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
  const searchParams = useSearchParams()

  useEffect(() => {
    if (searchParams.get('upload') === 'true') {
      setActiveTab('upload')
    }
  }, [searchParams])

  const [currentUser, setCurrentUser] = useState<any>(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [landscapeDrawer, setLandscapeDrawer] = useState(false)

  useEffect(() => {
    // Verificar autenticação
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    const currentUserData = localStorage.getItem('current_user')
    
    // Validar token - se tiver caracteres HTML encoded, limpar
    if (token && (token.includes('&#') || token.includes('&amp;') || token.includes('&lt;') || token.includes('&gt;'))) {
          console.error('Token corrompido detectado. Limpando...')
      localStorage.clear()
      router.push('/login')
      return
    }
    
    // Construir current_user a partir do JWT (fonte confiável)
    const tokenUser = getUserFromToken()
    if (token && tokenUser) {
      const saved = currentUserData ? JSON.parse(currentUserData) : {}
      const fullUser = {
        user_id: tokenUser.user_id,
        name: saved.name || tokenUser.email?.split('@')[0] || 'Usuário',
        email: tokenUser.email,
        role: tokenUser.role,
        s3_prefix: tokenUser.s3_prefix,
        avatar_url: saved.avatar_url || ''
      }
      localStorage.setItem('current_user', JSON.stringify(fullUser))
      setCurrentUser(fullUser)
      if (fullUser.role !== 'admin') {
        setCurrentFolderPath(fullUser.s3_prefix || '')
      }
      fetchUserData(tokenUser.user_id)
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
      if (!token || !userId) return
      
      const response = await fetch(getUserApiUrl(userId), {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.user) {
          const saved = JSON.parse(localStorage.getItem('current_user') || '{}')
          const updated = { ...saved, avatar_url: data.user.avatar_url }
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
      <header className="sticky top-0 z-50 border-b border-white/5" style={{ background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(20px)' }}>
        <div className="mx-auto px-4 sm:px-8 py-1.5 landscape:py-1 sm:py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2 sm:gap-4">
              <h1 
                className="text-lg sm:text-xl font-bold cursor-pointer tracking-tight"
                onClick={() => window.location.reload()}
              >
                <span className="text-white">Mídia</span><span style={{ color: '#667eea' }}>flow</span>
              </h1>
              <div className="hidden md:block text-xs text-gray-600 font-mono">
                v4.9.1
              </div>
            </div>
            
            {/* Desktop Menu */}
            <div className="hidden lg:flex items-center gap-3">
              {currentUser?.plan === 'trial' && (
                <div className="glass-card px-3 py-1.5 border border-yellow-500/50 bg-yellow-500/10">
                  <div className="text-xs text-yellow-400 font-semibold">
                    ⏱️ Trial - {Math.max(0, Math.ceil((new Date(currentUser.trial_end).getTime() - Date.now()) / (1000 * 60 * 60 * 24)))} dias
                  </div>
                </div>
              )}
              {currentUser && (
                <div
                  onClick={() => router.push('/profile')}
                  className="flex items-center gap-2 glass-card px-4 py-2 cursor-pointer hover:border-neon-cyan/50 transition-colors"
                >
                  <AvatarUpload
                    currentAvatar={currentUser.avatar_url}
                    size="sm"
                    className="flex-shrink-0"
                    onAvatarUpdate={(avatarUrl) => {
                      const updated = { ...currentUser, avatar_url: avatarUrl }
                      setCurrentUser(updated)
                    }}
                  />
                  <div className="text-sm">
                    <div className="text-neon-cyan font-semibold truncate max-w-[140px]">
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

            {/* Portrait: avatar + nome */}
            <div className="lg:hidden landscape:hidden flex items-center gap-2 cursor-pointer" onClick={() => router.push('/profile')}>
              <AvatarUpload
                currentAvatar={currentUser?.avatar_url}
                size="sm"
                className="flex-shrink-0"
                onAvatarUpdate={(avatarUrl) => {
                  const updated = { ...currentUser, avatar_url: avatarUrl }
                  setCurrentUser(updated)
                }}
              />
              <span className="text-sm font-semibold" style={{ color: '#a5b4fc' }}>
                {currentUser?.role === 'admin' ? 'Admin' : currentUser?.name?.split(' ')[0]}
              </span>
            </div>

            {/* Landscape mobile only: hambúrguer */}
            <button
              className="hidden landscape:max-lg:flex items-center justify-center w-8 h-8 rounded-lg hover:bg-white/10 transition-colors"
              onClick={() => setLandscapeDrawer(true)}
            >
              <svg className="w-5 h-5 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* Navigation desktop */}
      <nav className="hidden md:block border-b border-white/5 overflow-x-auto sticky top-[49px] z-40" style={{ background: 'rgba(0,0,0,0.5)', backdropFilter: 'blur(10px)' }}>
        <div className="mx-auto px-4 sm:px-8">
          <div className="flex space-x-1 min-w-max">
            {[
              ...(currentUser?.role !== 'admin' ? [{ id: 'files', label: 'Biblioteca' }] : []),
              { id: 'folders', label: 'Pastas' },
              { id: 'upload', label: 'Upload' },
              { id: 'public-feed', label: 'Público' },
              { id: 'analytics', label: 'Analytics' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => tab.id === 'public-feed' ? router.push('/public-feed') : setActiveTab(tab.id as any)}
                className={`py-3 px-5 border-b-2 font-medium text-sm whitespace-nowrap transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'border-[#667eea] text-white'
                    : 'border-transparent text-gray-500 hover:text-gray-300 hover:border-white/20'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Portrait: bottom tab bar — só ícones */}
      <nav className="md:hidden landscape:hidden fixed bottom-0 left-0 right-0 z-50 border-t border-white/10" style={{ background: 'rgba(0,0,0,0.92)', backdropFilter: 'blur(20px)' }}>
        <div className="flex items-center justify-around px-4 py-2">
          {[
            ...(currentUser?.role !== 'admin' ? [{ id: 'files', icon: '📁' }] : []),
            { id: 'folders', icon: '🗂️' },
            { id: 'upload', icon: '📤' },
            { id: 'public-feed', icon: '🌐' },
            { id: 'analytics', icon: '📊' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => tab.id === 'public-feed' ? router.push('/public-feed') : setActiveTab(tab.id as any)}
              className="relative flex flex-col items-center justify-center w-12 h-12 rounded-2xl transition-all"
            >
              <span className={`text-2xl leading-none transition-transform ${
                activeTab === tab.id ? 'scale-110' : 'opacity-50'
              }`}>{tab.icon}</span>
              {activeTab === tab.id && (
                <div className="absolute bottom-1 w-1 h-1 rounded-full bg-[#667eea]" />
              )}
            </button>
          ))}
        </div>
      </nav>

      {/* Landscape mobile: drawer lateral */}
      {landscapeDrawer && (
        <>
          {/* Overlay */}
          <div
            className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm lg:hidden"
            onClick={() => setLandscapeDrawer(false)}
          />
          {/* Drawer */}
          <div
            className="fixed left-0 top-0 bottom-0 z-50 w-56 flex flex-col lg:hidden animate-slide-in-left"
            style={{ background: 'rgba(8,8,18,0.98)', backdropFilter: 'blur(24px)', borderRight: '1px solid rgba(255,255,255,0.08)', transform: 'translateX(0)', transition: 'transform 200ms ease-out' }}
          >
            {/* Header do drawer */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-white/8">
              <span className="font-bold text-base">
                <span className="text-white">Mídia</span><span style={{ color: '#667eea' }}>flow</span>
              </span>
              <button onClick={() => setLandscapeDrawer(false)} className="p-1 rounded-lg hover:bg-white/10 text-gray-400 hover:text-white transition-colors">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Avatar + info */}
            <div className="flex items-center gap-3 px-4 py-3 border-b border-white/8">
              <AvatarUpload
                currentAvatar={currentUser?.avatar_url}
                size="sm"
                className="flex-shrink-0"
                onAvatarUpdate={(avatarUrl) => {
                  const updated = { ...currentUser, avatar_url: avatarUrl }
                  setCurrentUser(updated)
                }}
              />
              <div className="min-w-0">
                <p className="text-sm font-semibold text-white truncate">
                  {currentUser?.role === 'admin' ? 'Admin' : currentUser?.name}
                </p>
                <p className="text-xs text-gray-500 truncate">{currentUser?.email}</p>
              </div>
            </div>

            {/* Navegação */}
            <div className="flex-1 py-2">
              <p className="px-4 py-1.5 text-[10px] font-semibold text-gray-600 uppercase tracking-wider">Navegação</p>
              {[
                ...(currentUser?.role !== 'admin' ? [{ id: 'files', icon: '📁', label: 'Biblioteca' }] : []),
                { id: 'folders', icon: '🗂️', label: 'Pastas' },
                { id: 'upload', icon: '📤', label: 'Upload' },
                { id: 'public-feed', icon: '🌐', label: 'Público' },
                { id: 'analytics', icon: '📊', label: 'Analytics' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setLandscapeDrawer(false)
                    tab.id === 'public-feed' ? router.push('/public-feed') : setActiveTab(tab.id as any)
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'text-white bg-[#667eea]/15 border-r-2 border-[#667eea]'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <span className="text-base">{tab.icon}</span>
                  <span className="font-medium">{tab.label}</span>
                </button>
              ))}
            </div>

            {/* Conta */}
            <div className="border-t border-white/8 py-2">
              <p className="px-4 py-1.5 text-[10px] font-semibold text-gray-600 uppercase tracking-wider">Conta</p>
              <button
                onClick={() => { setLandscapeDrawer(false); router.push('/profile') }}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
              >
                <span className="text-base">👤</span>
                <span className="font-medium">Perfil</span>
              </button>
              {currentUser?.role === 'admin' && (
                <button
                  onClick={() => { setLandscapeDrawer(false); router.push('/admin') }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
                >
                  <span className="text-base">👥</span>
                  <span className="font-medium">Gerenciamento</span>
                </button>
              )}
              <button
                onClick={() => { setLandscapeDrawer(false); logout() }}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-red-400 hover:bg-red-600/10 transition-colors"
              >
                <span className="text-base">🚪</span>
                <span className="font-medium">Sair</span>
              </button>
            </div>
          </div>
        </>
      )}

      {/* Content */}
      <main className="mx-auto px-4 sm:px-8 pt-0 pb-24 landscape:pb-4 md:pb-8">
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

export default function DashboardPage() {
  return (
    <Suspense fallback={<div className="min-h-screen p-8"><DashboardSkeleton /></div>}>
      <DashboardContent />
    </Suspense>
  )
}
