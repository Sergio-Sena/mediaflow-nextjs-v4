'use client'

import { useState, useEffect } from 'react'
import { Folder, FolderPlus, Edit2, Trash2, ChevronRight, Home, RefreshCw } from 'lucide-react'

interface FolderItem {
  name: string
  path: string
  fileCount: number
  subfolderCount: number
  isOwned: boolean
}

interface FolderManagerV2Props {
  onNavigate?: (path: string) => void
  currentPath?: string
}

export default function FolderManagerV2({ onNavigate, currentPath = '' }: FolderManagerV2Props) {
  const [folders, setFolders] = useState<FolderItem[]>([])
  const [loading, setLoading] = useState(true)
  const [currentUser, setCurrentUser] = useState<any>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showRenameModal, setShowRenameModal] = useState(false)
  const [newFolderName, setNewFolderName] = useState('')
  const [selectedFolder, setSelectedFolder] = useState<FolderItem | null>(null)
  const [breadcrumbs, setBreadcrumbs] = useState<string[]>([''])
  const [currentFolderPath, setCurrentFolderPath] = useState<string>('')

  useEffect(() => {
    const userData = localStorage.getItem('current_user')
    if (userData) {
      setCurrentUser(JSON.parse(userData))
    }
    fetchFolders()
  }, [currentFolderPath])

  useEffect(() => {
    const parts = currentFolderPath ? currentFolderPath.split('/').filter(Boolean) : []
    setBreadcrumbs(['', ...parts])
  }, [currentFolderPath])

  const fetchFolders = async () => {
    try {
      setLoading(true)
      const { mediaflowClient } = await import('@/lib/aws-client')
      const data = await mediaflowClient.getFiles()

      if (data.success) {
        const token = localStorage.getItem('token')
        let userPrefix = ''
        let userRole = 'user'

        if (token) {
          try {
            const payload = JSON.parse(atob(token.split('.')[1]))
            userPrefix = payload.s3_prefix || ''
            userRole = payload.role || 'user'
          } catch (e) {
            console.error('Error parsing JWT:', e)
          }
        }

        // Build folder structure
        const folderMap = new Map<string, { files: number; subfolders: Set<string> }>()

        data.files.forEach((file: any) => {
          const folder = file.folder || 'root'
          if (folder === 'root') return

          // Admin vê tudo, user só vê suas pastas
          if (userRole !== 'admin' && userPrefix && !folder.startsWith(userPrefix.replace(/\/$/, ''))) {
            return
          }

          const parts = folder.split('/')
          let currentLevel = ''

          parts.forEach((part: string, index: number) => {
            const parentPath = parts.slice(0, index).join('/')
            const fullPath = parts.slice(0, index + 1).join('/')

            if (!folderMap.has(fullPath)) {
              folderMap.set(fullPath, { files: 0, subfolders: new Set() })
            }

            if (index === parts.length - 1) {
              folderMap.get(fullPath)!.files++
            }

            if (parentPath && folderMap.has(parentPath)) {
              folderMap.get(parentPath)!.subfolders.add(fullPath)
            }
          })
        })

        // Get folders at current level
        const currentFolders: FolderItem[] = []
        folderMap.forEach((value, path) => {
          const parentPath = path.split('/').slice(0, -1).join('/')
          if (parentPath === currentFolderPath) {
            const name = path.split('/').pop() || path
            const isOwned = userRole === 'admin' || path.startsWith(userPrefix.replace(/\/$/, ''))
            
            currentFolders.push({
              name,
              path,
              fileCount: value.files,
              subfolderCount: value.subfolders.size,
              isOwned
            })
          }
        })

        setFolders(currentFolders.sort((a, b) => a.name.localeCompare(b.name)))
      }
    } catch (error) {
      console.error('Error fetching folders:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateFolder = async () => {
    if (!newFolderName.trim()) return

    try {
      const token = localStorage.getItem('token')
      const folderPath = currentFolderPath ? `${currentFolderPath}/${newFolderName}` : newFolderName

      const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/folders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({ folderPath })
      })

      if (response.ok) {
        setShowCreateModal(false)
        setNewFolderName('')
        fetchFolders()
      }
    } catch (error) {
      console.error('Error creating folder:', error)
      alert('Erro ao criar pasta')
    }
  }

  const handleDeleteFolder = async (folder: FolderItem) => {
    if (!confirm(`Deseja excluir a pasta "${folder.name}" e todo seu conteúdo?`)) return

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/folders', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({ folderPath: folder.path })
      })

      if (response.ok) {
        fetchFolders()
      }
    } catch (error) {
      console.error('Error deleting folder:', error)
      alert('Erro ao excluir pasta')
    }
  }

  const navigateTo = (index: number) => {
    const newPath = breadcrumbs.slice(1, index + 1).join('/')
    onNavigate?.(newPath)
  }

  if (loading) {
    return (
      <div className="glass-card p-8 text-center">
        <RefreshCw className="w-8 h-8 text-neon-cyan animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Carregando pastas...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-white">📁 Gerenciador de Pastas</h2>
          <div className="flex gap-2">
            <button onClick={fetchFolders} className="btn-refresh" title="Atualizar">
              <RefreshCw className="w-4 h-4" />
            </button>
            <button onClick={() => setShowCreateModal(true)} className="btn-neon px-4 py-2 text-sm">
              <FolderPlus className="w-4 h-4 mr-2 inline" />
              Nova Pasta
            </button>
          </div>
        </div>

        {/* Breadcrumbs */}
        <div className="flex items-center gap-2 text-sm flex-wrap">
          <button
            onClick={() => navigateTo(0)}
            className="flex items-center gap-1 text-neon-cyan hover:text-neon-purple transition-colors"
          >
            <Home className="w-4 h-4" />
            Raiz
          </button>
          {breadcrumbs.slice(1).map((crumb, index) => (
            <div key={index} className="flex items-center gap-2">
              <ChevronRight className="w-4 h-4 text-gray-500" />
              <button
                onClick={() => navigateTo(index + 1)}
                className="text-gray-300 hover:text-neon-cyan transition-colors"
              >
                {crumb}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Folder Grid */}
      {folders.length === 0 ? (
        <div className="glass-card p-8 text-center">
          <Folder className="w-12 h-12 text-gray-500 mx-auto mb-4" />
          <p className="text-gray-400">Nenhuma pasta neste nível</p>
          <button onClick={() => setShowCreateModal(true)} className="btn-secondary mt-4">
            Criar Primeira Pasta
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {folders.map((folder) => (
            <div
              key={folder.path}
              className="glass-card p-4 hover:border-neon-cyan/50 transition-all cursor-pointer group"
              onDoubleClick={() => onNavigate?.(folder.path)}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <Folder className="w-8 h-8 text-neon-cyan flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-white truncate" title={folder.name}>
                      {folder.name}
                    </h3>
                    <p className="text-xs text-gray-400">
                      {folder.fileCount} arquivo(s) • {folder.subfolderCount} subpasta(s)
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    setCurrentFolderPath(folder.path)
                    fetchFolders()
                  }}
                  className="btn-secondary flex-1 py-2 text-sm"
                >
                  Abrir
                </button>
                {folder.isOwned && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDeleteFolder(folder)
                    }}
                    className="btn-danger p-2"
                    title="Excluir"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Folder Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-card p-6 max-w-md w-full">
            <h3 className="text-xl font-bold text-white mb-4">📁 Nova Pasta</h3>
            <input
              type="text"
              value={newFolderName}
              onChange={(e) => setNewFolderName(e.target.value)}
              placeholder="Nome da pasta"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white mb-4"
              onKeyPress={(e) => e.key === 'Enter' && handleCreateFolder()}
              autoFocus
            />
            <div className="flex gap-2">
              <button onClick={handleCreateFolder} className="btn-neon flex-1">
                Criar
              </button>
              <button onClick={() => setShowCreateModal(false)} className="btn-secondary flex-1">
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
