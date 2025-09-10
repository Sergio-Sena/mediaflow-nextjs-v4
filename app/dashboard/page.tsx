'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

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
  const [files, setFiles] = useState<FileItem[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'files' | 'upload'>('files')
  const router = useRouter()

  useEffect(() => {
    // Verificar autenticação
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (!token || !userData) {
      router.push('/login')
      return
    }

    setUser(JSON.parse(userData))
    loadFiles()
  }, [router])

  const loadFiles = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/videos/list', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        setFiles(data.files || [])
      }
    } catch (error) {
      console.error('Erro ao carregar arquivos:', error)
    } finally {
      setLoading(false)
    }
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
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <h1 className="text-2xl font-bold">
                🎬 <span className="neon-text">Mediaflow</span>
              </h1>
              <div className="hidden md:block text-sm text-gray-400">
                Dashboard v4.0
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-300">
                Olá, <span className="text-neon-cyan">{user?.name}</span>
              </div>
              <button
                onClick={logout}
                className="btn-secondary px-4 py-2 text-sm"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-dark-800/30 backdrop-blur-sm border-b border-neon-cyan/10">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-8">
            {[
              { id: 'files', label: '📁 Arquivos', count: files.length },
              { id: 'upload', label: '📤 Upload', count: 0 },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-2 border-b-2 font-medium text-sm transition-all duration-300 ${
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
      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'files' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-white">
                Seus Arquivos ({files.length})
              </h2>
              <button
                onClick={loadFiles}
                className="btn-secondary px-4 py-2 text-sm"
              >
                🔄 Atualizar
              </button>
            </div>

            {files.length === 0 ? (
              <div className="glass-card p-12 text-center">
                <div className="text-6xl mb-4">📁</div>
                <h3 className="text-xl font-semibold text-gray-300 mb-2">
                  Nenhum arquivo encontrado
                </h3>
                <p className="text-gray-400 mb-6">
                  Faça upload de seus primeiros arquivos
                </p>
                <button
                  onClick={() => setActiveTab('upload')}
                  className="btn-neon"
                >
                  📤 Fazer Upload
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {files.map((file) => (
                  <div key={file.key} className="glass-card-hover p-4">
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-2xl">{getFileIcon(file.type)}</span>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-white truncate">
                          {file.name}
                        </h3>
                        <p className="text-xs text-gray-400">
                          {formatFileSize(file.size)}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex gap-2">
                      {file.type === 'video' && (
                        <button className="btn-secondary flex-1 py-2 text-xs">
                          ▶️ Play
                        </button>
                      )}
                      <a
                        href={file.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-secondary flex-1 py-2 text-xs text-center"
                      >
                        📥 Download
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'upload' && (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-white">Upload de Arquivos</h2>
            
            <div className="glass-card p-8 text-center">
              <div className="text-6xl mb-4">📤</div>
              <h3 className="text-xl font-semibold text-gray-300 mb-2">
                Upload em Desenvolvimento
              </h3>
              <p className="text-gray-400 mb-6">
                Funcionalidade será implementada na próxima etapa
              </p>
              <button
                onClick={() => setActiveTab('files')}
                className="btn-neon"
              >
                📁 Ver Arquivos
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}