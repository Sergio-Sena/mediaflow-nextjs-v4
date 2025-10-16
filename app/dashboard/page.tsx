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
  const [activeTab, setActiveTab] = useState<'files' | 'upload' | 'manager' | 'analytics'>('files')
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

  useEffect(() => {
    // Verificar autenticação
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    const currentUserData = localStorage.getItem('current_user')
    
    if (!token) {
      router.push('/login')
      return
    }

    // Priorizar current_user (multi-usuário) sobre user (legado)
    if (currentUserData) {
      setCurrentUser(JSON.parse(currentUserData))
    }
    
    if (userData) {
      setUser(JSON.parse(userData))
    }
    
    setLoading(false)
  }, [router])

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
                🎬 <span className="neon-text">Mediaflow</span>
              </h1>
              <div className="hidden md:block text-sm text-gray-400">
                Dashboard v4.3
              </div>
            </div>
            
            <div className="flex items-center gap-1 sm:gap-2 md:gap-4">
              {currentUser && (
                <div className="flex items-center gap-2 glass-card px-2 sm:px-4 py-2">
                  {currentUser.avatar_url ? (
                    <img 
                      src={currentUser.avatar_url} 
                      alt={currentUser.name}
                      className="w-8 h-8 sm:w-10 sm:h-10 rounded-full object-cover border-2 border-neon-cyan"
                    />
                  ) : (
                    <span className="text-xl sm:text-2xl">{currentUser.avatar || '👤'}</span>
                  )}
                  <div className="text-xs sm:text-sm hidden sm:block">
                    <div className="text-neon-cyan font-semibold truncate max-w-[100px]">{currentUser.name}</div>
                    <div className="text-xs text-gray-400">🔒 2FA</div>
                  </div>
                </div>
              )}
              {!currentUser && user && (
                <div className="text-sm text-gray-300">
                  Olá, <span className="text-neon-cyan">{user?.name}</span>
                </div>
              )}
              {currentUser && (
                <button
                  onClick={() => {
                    localStorage.removeItem('token')
                    localStorage.removeItem('current_user')
                    router.push('/users')
                  }}
                  className="btn-secondary px-2 sm:px-4 py-2 text-xs sm:text-sm hidden sm:inline-block"
                >
                  🔄 Trocar
                </button>
              )}
              {currentUser?.user_id === 'admin' && (
                <button
                  onClick={() => router.push('/admin')}
                  className="btn-neon px-2 sm:px-4 py-2 text-xs sm:text-sm"
                >
                  <span className="hidden sm:inline">👥 Admin</span>
                  <span className="sm:hidden">👥</span>
                </button>
              )}
              <button
                onClick={logout}
                className="btn-secondary px-2 sm:px-4 py-2 text-xs sm:text-sm"
              >
                <span className="hidden sm:inline">Sair</span>
                <span className="sm:hidden">🚪</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-dark-800/30 backdrop-blur-sm border-b border-neon-cyan/10 overflow-x-auto">
        <div className="max-w-7xl mx-auto px-2 sm:px-4">
          <div className="flex space-x-2 sm:space-x-4 md:space-x-8 min-w-max">
            {[
              { id: 'files', label: '📁 Arquivos', count: 0 },
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
                className="btn-secondary px-4 py-2 text-sm"
              >
                📁 Ver Arquivos
              </button>
            </div>
            
            <DirectUpload
              maxFiles={100}
              maxSize={5120}
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