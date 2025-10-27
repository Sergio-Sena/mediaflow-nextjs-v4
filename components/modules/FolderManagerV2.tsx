'use client'

import { useState, useEffect } from 'react'
import { Folder, FolderPlus, Trash2, ChevronRight, Home, RefreshCw, Search, ChevronUp, ChevronDown } from 'lucide-react'

interface FolderItem {
  name: string
  path: string
  fileCount: number
  subfolderCount: number
  isOwned: boolean
  lastModified: string
}

interface FolderManagerV2Props {
  onNavigate?: (path: string) => void
  currentPath?: string
}

type SortField = 'name' | 'fileCount' | 'subfolderCount' | 'lastModified'
type SortOrder = 'asc' | 'desc'

export default function FolderManagerV2({ onNavigate, currentPath = '' }: FolderManagerV2Props) {
  const [folders, setFolders] = useState<FolderItem[]>([])
  const [filteredFolders, setFilteredFolders] = useState<FolderItem[]>([])
  const [loading, setLoading] = useState(true)
  const [currentUser, setCurrentUser] = useState<any>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newFolderName, setNewFolderName] = useState('')
  const [breadcrumbs, setBreadcrumbs] = useState<string[]>([''])
  const [currentFolderPath, setCurrentFolderPath] = useState<string>('')
  const [searchTerm, setSearchTerm] = useState('')
  const [sortField, setSortField] = useState<SortField>('name')
  const [sortOrder, setSortOrder] = useState<SortOrder>('asc')
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage] = useState(100)

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
        const allFolderPaths = new Set<string>()

        // Primeiro, coletar TODAS as pastas do S3 (incluindo vazias)
        data.files.forEach((file: any) => {
          const folder = file.folder || 'root'
          
          if (folder === 'root') return

          // Admin vê tudo, user só vê suas pastas
          if (userRole !== 'admin' && userPrefix && !folder.startsWith(userPrefix.replace(/\/$/, ''))) {
            return
          }

          // Adicionar TODAS as pastas no caminho (incluindo intermediárias)
          const parts = folder.split('/')
          for (let i = 1; i <= parts.length; i++) {
            const folderPath = parts.slice(0, i).join('/')
            allFolderPaths.add(folderPath)
          }
        })
        
        console.log('Total unique folders found:', allFolderPaths.size, Array.from(allFolderPaths).filter(p => p.startsWith('users/user_admin/Star/')).length, 'in Star/')

        // Inicializar todas as pastas no mapa
        allFolderPaths.forEach(path => {
          if (!folderMap.has(path)) {
            folderMap.set(path, { files: 0, subfolders: new Set() })
          }
        })

        // Agora contar arquivos e construir hierarquia
        data.files.forEach((file: any) => {
          const folder = file.folder || 'root'
          
          // Detectar placeholders de pastas vazias
          if (file.name === '.folder_placeholder') {
            return // Já foi adicionada acima
          }
          
          if (folder === 'root') return

          // Admin vê tudo, user só vê suas pastas
          if (userRole !== 'admin' && userPrefix && !folder.startsWith(userPrefix.replace(/\/$/, ''))) {
            return
          }

          // Contar arquivo na pasta final
          if (folderMap.has(folder)) {
            folderMap.get(folder)!.files++
          }
        })

        // Construir hierarquia de subpastas - TODAS as subpastas diretas
        allFolderPaths.forEach(path => {
          const parts = path.split('/')
          if (parts.length > 1) {
            const parentPath = parts.slice(0, -1).join('/')
            if (folderMap.has(parentPath)) {
              folderMap.get(parentPath)!.subfolders.add(path)
            }
          }
        })

        // Subpastas já foram adicionadas no loop anterior

        // Get folders at current level
        const currentFolders: FolderItem[] = []
        const currentDepth = currentFolderPath ? currentFolderPath.split('/').length : 0
        
        allFolderPaths.forEach(path => {
          const pathParts = path.split('/')
          const parentPath = pathParts.slice(0, -1).join('/')
          
          // Mostrar apenas pastas do nível atual
          if (parentPath === currentFolderPath) {
            const name = pathParts[pathParts.length - 1]
            const isOwned = userRole === 'admin' || path.startsWith(userPrefix.replace(/\/$/, ''))
            
            // Contar subpastas DIRETAS
            let directSubfolderCount = 0
            allFolderPaths.forEach(otherPath => {
              const otherParts = otherPath.split('/')
              if (otherParts.length === pathParts.length + 1 && 
                  otherPath.startsWith(path + '/')) {
                directSubfolderCount++
              }
            })
            
            const folderData = folderMap.get(path)
            currentFolders.push({
              name,
              path,
              fileCount: folderData?.files || 0,
              subfolderCount: directSubfolderCount,
              isOwned,
              lastModified: 'Recente'
            })
          }
        })

        console.log('DEBUG FolderManagerV2:', {
          currentPath: currentFolderPath,
          totalFoldersFound: currentFolders.length,
          folderNames: currentFolders.map(f => f.name)
        })
        
        setFolders(currentFolders)
        setFilteredFolders(currentFolders)
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
      
      // Get user prefix from JWT
      let userPrefix = ''
      let userRole = 'user'
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]))
          const userId = payload.user_id || ''
          userRole = payload.role || 'user'
          userPrefix = userRole === 'admin' ? '' : `users/${userId}`
        } catch (e) {}
      }
      
      // Build full path with user prefix
      let folderPath = ''
      if (currentFolderPath) {
        folderPath = `${currentFolderPath}/${newFolderName}`
      } else if (userPrefix) {
        folderPath = `${userPrefix}/${newFolderName}`
      } else {
        folderPath = newFolderName
      }

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

  // Filtrar e ordenar pastas
  useEffect(() => {
    let filtered = folders.filter(folder => 
      folder.name.toLowerCase().includes(searchTerm.toLowerCase())
    )

    // Ordenar
    filtered.sort((a, b) => {
      let aVal: any = a[sortField]
      let bVal: any = b[sortField]
      
      if (sortField === 'name') {
        aVal = aVal.toLowerCase()
        bVal = bVal.toLowerCase()
      }
      
      if (sortOrder === 'asc') {
        return aVal > bVal ? 1 : -1
      } else {
        return aVal < bVal ? 1 : -1
      }
    })

    setFilteredFolders(filtered)
    setCurrentPage(1)
  }, [folders, searchTerm, sortField, sortOrder])

  const navigateTo = (index: number) => {
    const newPath = breadcrumbs.slice(1, index + 1).join('/')
    setCurrentFolderPath(newPath)
  }

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortOrder('asc')
    }
  }

  const handleDoubleClick = (folder: FolderItem) => {
    console.log('Double click:', folder.name, 'fileCount:', folder.fileCount, 'subfolderCount:', folder.subfolderCount)
    
    // Se tem subpastas, SEMPRE navegar (prioridade)
    if (folder.subfolderCount > 0) {
      setCurrentFolderPath(folder.path)
    } else if (folder.fileCount > 0) {
      // Só ir para biblioteca se NÃO tiver subpastas
      if (onNavigate) {
        onNavigate(folder.path)
      }
    }
  }

  // Mostrar todas as pastas sem paginação
  const paginatedFolders = filteredFolders

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return null
    return sortOrder === 'asc' ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />
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
        <div className="flex items-center gap-2 text-sm flex-wrap mb-4">
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

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar pastas..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-neon-cyan focus:outline-none"
          />
        </div>
      </div>

      {/* Table */}
      {loading ? (
        <div className="glass-card p-8 text-center">
          <RefreshCw className="w-8 h-8 text-neon-cyan animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Carregando pastas...</p>
        </div>
      ) : filteredFolders.length === 0 ? (
        <div className="glass-card p-8 text-center">
          <Folder className="w-12 h-12 text-gray-500 mx-auto mb-4" />
          <p className="text-gray-400">
            {searchTerm ? 'Nenhuma pasta encontrada' : 'Nenhuma pasta neste nível'}
          </p>
          {!searchTerm && (
            <button onClick={() => setShowCreateModal(true)} className="btn-secondary mt-4">
              Criar Primeira Pasta
            </button>
          )}
        </div>
      ) : (
        <div className="glass-card overflow-hidden">
          {/* Table Header */}
          <div className="bg-gray-800/50 border-b border-gray-700">
            <div className="grid grid-cols-12 gap-4 p-4 text-sm font-medium text-gray-300">
              <button 
                onClick={() => handleSort('name')}
                className="col-span-5 flex items-center gap-2 text-left hover:text-neon-cyan transition-colors"
              >
                Nome <SortIcon field="name" />
              </button>
              <div className="col-span-2 text-center">Tipo</div>
              <button 
                onClick={() => handleSort('fileCount')}
                className="col-span-2 flex items-center justify-center gap-1 hover:text-neon-cyan transition-colors"
              >
                Arquivos <SortIcon field="fileCount" />
              </button>
              <button 
                onClick={() => handleSort('subfolderCount')}
                className="col-span-2 flex items-center justify-center gap-1 hover:text-neon-cyan transition-colors"
              >
                Subpastas <SortIcon field="subfolderCount" />
              </button>
              <div className="col-span-1"></div>
            </div>
          </div>

          {/* Table Body */}
          <div className="divide-y divide-gray-700">
            {paginatedFolders.map((folder) => (
              <div
                key={folder.path}
                className="grid grid-cols-12 gap-4 p-4 hover:bg-gray-800/30 cursor-pointer transition-colors group"
                onDoubleClick={() => handleDoubleClick(folder)}
              >
                <div className="col-span-5 flex items-center gap-3 min-w-0">
                  <Folder className="w-5 h-5 text-neon-cyan flex-shrink-0" />
                  <span className="text-white truncate" title={folder.fileCount > 0 ? `${folder.name}/ - Duplo clique para ver arquivos` : `${folder.name}/ - Duplo clique para abrir`}>
                    {folder.name}/
                  </span>
                  {folder.fileCount > 0 && (
                    <span className="text-xs text-green-400">▶</span>
                  )}
                  {folder.subfolderCount > 0 && folder.fileCount === 0 && (
                    <span className="text-xs text-neon-purple">→</span>
                  )}
                </div>
                <div className="col-span-2 text-center text-gray-400 text-sm">
                  Pasta
                </div>
                <div className="col-span-2 text-center text-gray-300">
                  {folder.fileCount}
                </div>
                <div className="col-span-2 text-center text-gray-300">
                  {folder.subfolderCount}
                </div>
                <div className="col-span-1 flex justify-end">
                  {folder.isOwned && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDeleteFolder(folder)
                      }}
                      className="opacity-0 group-hover:opacity-100 btn-danger p-1 transition-opacity"
                      title="Excluir"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Total */}
          <div className="bg-gray-800/30 border-t border-gray-700 p-4 text-center text-sm text-gray-400">
            Total: {filteredFolders.length} pastas
          </div>
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
