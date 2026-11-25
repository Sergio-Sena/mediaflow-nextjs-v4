'use client'

import { useState, useEffect } from 'react'
import { Play, Download, Trash2, Search, Filter, Grid, List, RefreshCw, Settings, X, ListChecks, Share2 } from 'lucide-react'
import { getApiUrl } from '@/lib/aws-config'
import ContentCarousel from './ContentCarousel'
import { InputModal, ConfirmModal } from '@/components/ui/Modal'

interface S3File {
  key: string
  name: string
  size: number
  lastModified: string
  url: string
  type: 'video' | 'image' | 'document' | 'other'
  folder: string
  duration?: number
}

interface FileListProps {
  onPlayVideo?: (file: S3File) => void
  onViewImage?: (file: S3File) => void
  onViewPDF?: (file: S3File) => void
  refreshTrigger?: number
  onFilesLoaded?: (files: S3File[]) => void
  targetFolder?: string
}

export default function FileList({ onPlayVideo, onViewImage, onViewPDF, refreshTrigger, onFilesLoaded, targetFolder }: FileListProps) {
  const [files, setFiles] = useState<S3File[]>([])
  const [folders, setFolders] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFolder, setSelectedFolder] = useState<string>('all')
  const [selectedType, setSelectedType] = useState<string>('all')
  const [viewMode, setViewMode] = useState<'list' | 'grid'>('list')
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set())
  const [selectAll, setSelectAll] = useState(false)
  const [converting, setConverting] = useState<Set<string>>(new Set())
  const [currentPath, setCurrentPath] = useState<string[]>([])
  const [initialPathSet, setInitialPathSet] = useState(false)
  const [folderStructure, setFolderStructure] = useState<{[key: string]: string[]}>({})
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage] = useState(50)
  const [hasMore, setHasMore] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)
  const [totalFiles, setTotalFiles] = useState(0)
  const [deleting, setDeleting] = useState<Set<string>>(new Set())
  const [deleteModal, setDeleteModal] = useState<{type: 'single' | 'bulk' | 'folder', file?: any, items?: any[]} | null>(null)
  const [shareModal, setShareModal] = useState<any>(null)
  const [sortBy, setSortBy] = useState<'name' | 'size' | 'date'>('name')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')
  const [mobileFolderOpen, setMobileFolderOpen] = useState(false)
  const [mobileSortOpen, setMobileSortOpen] = useState(false)
  const [filtersOpen, setFiltersOpen] = useState(false)
  const [folderDropOpen, setFolderDropOpen] = useState(false)
  const [typeDropOpen, setTypeDropOpen] = useState(false)
  const [sortDropOpen, setSortDropOpen] = useState(false)

  const fetchDurationsInBackground = async (filesToCheck: S3File[]) => {
    const { durationCache } = await import('@/lib/duration-cache')
    const token = localStorage.getItem('token')
    const missing = filesToCheck.filter(f => f.type === 'video' && durationCache.get(f.key) === null)
    if (missing.length === 0) return

    // Limita a 50 por sessão para não sobrecarregar
    const toFetch = missing.slice(0, 50)
    const results: Record<string, number> = {}
    const BATCH = 5

    for (let i = 0; i < toFetch.length; i += BATCH) {
      const batch = toFetch.slice(i, i + BATCH)
      await Promise.all(batch.map(async (file) => {
        try {
          const res = await fetch(
            `${getApiUrl('FILES')}?key=${encodeURIComponent(file.key)}`,
            { headers: { Authorization: `Bearer ${token}` } }
          )
          if (res.ok) {
            const data = await res.json()
            if (data.duration !== undefined) results[file.key] = data.duration
          }
        } catch {}
      }))
      durationCache.setMany(results)
      setFiles(prev => prev.map(f => results[f.key] !== undefined ? { ...f, duration: results[f.key] } : f))
    }
  }

  const applyDurationCache = async (fileList: S3File[]): Promise<S3File[]> => {
    const { durationCache } = await import('@/lib/duration-cache')
    const cache = durationCache.getAll()
    return fileList.map(f => ({
      ...f,
      duration: cache[f.key] ?? f.duration ?? 0
    }))
  }

  const fetchFiles = async (page = 1, append = false) => {
    try {
      if (!append) setLoading(true)
      else setLoadingMore(true)
      setError(null)

      // Cache apenas para página 1
      if (page === 1) {
        const { filesCache } = await import('@/lib/files-cache')
        const cached = filesCache.get()
        if (cached) {
          const withDuration = await applyDurationCache(cached.files)
          setFiles(withDuration)
          setFolders(cached.folders)
          setFolderStructure(cached.folderStructure)
          setTotalFiles(cached.total || withDuration.length)
          setHasMore(cached.hasMore || false)
          onFilesLoaded?.(withDuration)
          setLoading(false)
          return
        }
      }
      
      const { mediaflowClient } = await import('@/lib/aws-client')
      const data = await mediaflowClient.getFiles(page)
      
      // Obter informações do usuário do JWT
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
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
      
      if (data.success) {
        // Transform AWS response to match component expectations
        const transformedFiles = data.files.map((file: any) => {
          // Use folder from backend if available, otherwise extract from key
          let folderName = file.folder
          if (!folderName) {
            if (file.key.includes('/')) {
              folderName = file.key.split('/').slice(0, -1).join('/')
            } else {
              folderName = 'root'
            }
          }
          // Normalize: empty string or null should be 'root'
          if (!folderName || folderName === '') {
            folderName = 'root'
          }
          const fileName = file.name || file.key.split('/').pop() || file.key
          const fileType = getFileTypeFromName(file.key)
          
          return {
            key: file.key,
            name: fileName,
            size: file.size,
            lastModified: file.lastModified,
            url: `https://${file.bucket === 'uploads' ? 'mediaflow-uploads-969430605054' : 'mediaflow-processed-969430605054'}.s3.amazonaws.com/${encodeURIComponent(file.key)}`,
            type: fileType,
            folder: folderName,
            bucket: file.bucket,
            duration: file.duration || 0
          }
        })
        
        const withDuration = await applyDurationCache(transformedFiles)

        if (append) {
          setFiles(prev => {
            const merged = [...prev, ...withDuration]
            onFilesLoaded?.(merged)
            return merged
          })
        } else {
          setFiles(withDuration)
          onFilesLoaded?.(withDuration)
        }

        setTotalFiles(data.total || transformedFiles.length)
        setHasMore(data.hasMore || false)
        
        // Build folder structure for navigation
        const structure: {[key: string]: string[]} = {}
        transformedFiles.forEach((file: any) => {
          if (file.folder && file.folder !== 'root') {
            const parts = file.folder.split('/')
            let currentLevel = ''
            parts.forEach((part: string, index: number) => {
              const parentPath = parts.slice(0, index).join('/')
              if (!structure[parentPath]) structure[parentPath] = []
              const fullPath = parts.slice(0, index + 1).join('/')
              if (!structure[parentPath].includes(fullPath)) {
                structure[parentPath].push(fullPath)
              }
            })
          }
        })
        setFolderStructure(structure)
        
        // Extract unique folders (preserve full folder paths)
        const allFolderPaths = transformedFiles
          .map((f: any) => f.folder as string)
          .filter((f: string) => f && f !== 'root')
        
        const uniqueFolderPaths = Array.from(new Set(allFolderPaths)) as string[]
        
        // Check if there are files in root
        const hasRootFiles = transformedFiles.some((f: any) => f.folder === 'root')
        
        // Build folder list - ALWAYS include root if there are root files
        const allFolders = []
        if (hasRootFiles) {
          allFolders.push('📁 Raiz')
        }
        // Add other folders (filtradas por userPrefix)
        uniqueFolderPaths.forEach(f => {
          // Admin vê apenas admin/, user vê apenas suas pastas
          if (userRole === 'admin') {
            if (f.startsWith('admin/') || f === 'admin') {
              allFolders.push(`📁 ${f}`)
            }
          } else if (userPrefix && f.startsWith(userPrefix.replace(/\/$/, ''))) {
            allFolders.push(`📁 ${f}`)
          }
        })
        
        setFolders(allFolders)
        
        // Salvar no cache apenas página 1
        if (page === 1) {
          const { filesCache } = await import('@/lib/files-cache')
          filesCache.set({
            files: withDuration,
            folders: allFolders,
            folderStructure: structure,
            total: data.total,
            hasMore: data.hasMore
          })
        }
      } else {
        throw new Error(data.message || 'Erro ao carregar arquivos')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido')
    } finally {
      setLoading(false)
      setLoadingMore(false)
    }
  }
  
  const getFileTypeFromName = (filename: string): 'video' | 'image' | 'document' | 'other' => {
    const ext = filename.split('.').pop()?.toLowerCase()
    
    if (['mp4', 'avi', 'mov', 'mkv', 'webm', 'ts'].includes(ext || '')) {
      return 'video'
    }
    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext || '')) {
      return 'image'
    }
    if (['pdf', 'doc', 'docx', 'txt'].includes(ext || '')) {
      return 'document'
    }
    return 'other'
  }

  useEffect(() => {
    setCurrentPage(1)
    fetchFiles(1, false)
  }, [refreshTrigger])

  // Carrega próximas páginas em background
  useEffect(() => {
    if (!hasMore || loadingMore) return
    const timer = setTimeout(() => {
      const next = currentPage + 1
      setCurrentPage(next)
      fetchFiles(next, true)
    }, 500)
    return () => clearTimeout(timer)
  }, [hasMore, currentPage, loadingMore])

  // Set initial path based on user role
  useEffect(() => {
    if (files.length > 0 && !initialPathSet) {
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]))
          const userRole = payload.role || 'user'
          const userId = payload.user_id || ''
          
          if (userRole === 'user' && userId) {
            // User: navigate to users/{user_id}/
            const userFolder = `users/${userId}`
            setCurrentPath(['', 'users', userId])
          } else {
            // Admin: stay at root
            setCurrentPath([''])
          }
          setInitialPathSet(true)
        } catch (e) {
          setCurrentPath([''])
          setInitialPathSet(true)
        }
      } else {
        setCurrentPath([''])
        setInitialPathSet(true)
      }
    }
  }, [files, initialPathSet])

  useEffect(() => {
    if (targetFolder !== undefined) {
      const pathParts = targetFolder ? targetFolder.split('/') : ['']
      setCurrentPath(['', ...pathParts])
    }
  }, [targetFolder])

  // Navigation functions
  const navigateToFolder = (folderPath: string) => {
    const pathParts = folderPath ? folderPath.split('/') : ['']
    setCurrentPath(['', ...pathParts])
  }
  
  const navigateUp = (index: number) => {
    setCurrentPath(currentPath.slice(0, index + 1))
  }
  
  // Get current folder content
  const getCurrentFolderPath = () => {
    return currentPath.slice(1).join('/')
  }
  
  const getCurrentFolders = () => {
    const currentFolderPath = getCurrentFolderPath()
    return folderStructure[currentFolderPath] || []
  }
  
  const getCurrentFiles = () => {
    const currentFolderPath = getCurrentFolderPath()
    
    // Obter role do JWT
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    let userRole = 'user'
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        userRole = payload.role || 'user'
      } catch (e) {}
    }
    
    return files.filter(file => {
      // Obter userPrefix do JWT
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
      let userPrefix = ''
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]))
          userPrefix = payload.s3_prefix || ''
        } catch (e) {}
      }
      
      if (currentFolderPath === '' || currentFolderPath === 'Raiz') {
        // Admin na raiz vê apenas admin/, user vê apenas root
        if (userRole === 'admin') {
          return file.folder.startsWith('admin/') || file.folder === 'admin'
        }
        // User na raiz vê apenas arquivos root
        return file.folder === 'root' || file.folder === ''
      }
      // Show files that are EXACTLY in this folder (not in subfolders)
      // E que o usuário tem permissão
      const inCurrentFolder = file.folder === currentFolderPath
      const hasPermission = userRole === 'admin' 
        ? file.folder.startsWith('admin/') || file.folder === 'admin'
        : !userPrefix || file.folder.startsWith(userPrefix.replace(/\/$/, ''))
      return inCurrentFolder && hasPermission
    })
  }
  
  // Reset page when filters change
  useEffect(() => {
    setCurrentPage(1)
  }, [searchTerm, selectedType, currentPath])

  const filteredFiles = files.filter(file => {
    // Normalizar busca: remover _ e espaços para comparação
    const normalizedFileName = file.name.toLowerCase().replace(/[_\s]/g, '')
    const normalizedSearch = searchTerm.toLowerCase().replace(/[_\s]/g, '')
    const matchesSearch = !searchTerm || normalizedFileName.includes(normalizedSearch)
    const matchesType = selectedType === 'all' || file.type === selectedType
    
    // Filtrar por permissão do usuário
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    let userRole = 'user'
    let userPrefix = ''
    
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        userRole = payload.role || 'user'
        const userId = payload.user_id || ''
        userPrefix = `users/${userId}`
      } catch (e) {}
    }
    
    // Admin vê apenas admin/, user vê apenas suas pastas
    const normalizedPrefix = userPrefix.replace(/\/$/, '')
    const hasPermission = userRole === 'admin' 
      ? (file.folder.startsWith('admin/') || file.folder === 'admin')
      : (file.folder.startsWith(normalizedPrefix) || file.folder === 'root')
    
    // Filtrar por pasta selecionada (se não for raiz)
    const currentFolderPath = getCurrentFolderPath()
    const matchesFolder = !currentFolderPath || file.folder.startsWith(currentFolderPath)
    
    return matchesSearch && matchesType && hasPermission && matchesFolder
  })

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'video': return '🎥'
      case 'image': return '🖼️'
      case 'document': return '📄'
      default: return '📁'
    }
  }

  const getConversionStatus = (filename: string, key: string) => {
    if (converting.has(key)) return { icon: '🔄', tooltip: 'Convertendo...', canConvert: false }
    if (filename.endsWith('.mp4')) return { icon: '🎯', tooltip: 'Otimizado', canConvert: false }
    if (filename.endsWith('.ts') || filename.endsWith('.avi') || filename.endsWith('.mov') || filename.endsWith('.mkv')) {
      return { icon: '🎥', tooltip: 'Pode ser convertido', canConvert: true }
    }
    return { icon: '📁', tooltip: 'Não conversível', canConvert: false }
  }

  const handleDownload = (file: S3File) => {
    alert('📥 Função de download estará disponível em breve!')
  }

  const handleDelete = async (file: S3File) => {
    setDeleteModal({ type: 'single', file })
  }

  const executeDelete = async (file: S3File) => {
    if (deleting.has(file.key)) return

    setDeleting(prev => new Set(prev).add(file.key))
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('Token de autenticação não encontrado. Faça login novamente.')
      }
      
      // Usar bulk-delete com array de 1 item
      const response = await fetch(getApiUrl('BULK_DELETE'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ keys: [file.key] })
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setFiles(prev => prev.filter(f => f.key !== file.key))
          // Limpar cache
          const { filesCache } = await import('@/lib/files-cache')
          filesCache.clear()
        } else {
          throw new Error(data.message || 'Erro ao excluir arquivo')
        }
      } else if (response.status === 403) {
        throw new Error('Sessão expirada. Faça login novamente.')
      } else {
        throw new Error(`Delete failed: ${response.status}`)
      }
    } catch (err) {
      console.error('Delete error:', err)
      alert(err instanceof Error ? err.message : 'Erro ao excluir arquivo')
    } finally {
      setDeleting(prev => {
        const next = new Set(prev)
        next.delete(file.key)
        return next
      })
    }
  }

  const toggleFileSelection = (key: string) => {
    const newSelected = new Set(selectedFiles)
    if (newSelected.has(key)) {
      newSelected.delete(key)
    } else {
      newSelected.add(key)
    }
    setSelectedFiles(newSelected)
  }

  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedFiles(new Set())
      setSelectAll(false)
    } else {
      setSelectedFiles(new Set(filteredFiles.map(f => f.key)))
      setSelectAll(true)
    }
  }

  const handleBulkDelete = async () => {
    if (selectedFiles.size === 0 || deleting.size > 0) return
    setDeleteModal({ type: 'bulk' })
  }

  const executeBulkDelete = async () => {

    const keysToDelete = Array.from(selectedFiles)
    setDeleting(new Set(keysToDelete))
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('Token de autenticação não encontrado. Faça login novamente.')
      }
      
      const response = await fetch(getApiUrl('BULK_DELETE'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ keys: keysToDelete })
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setFiles(prev => prev.filter(f => !selectedFiles.has(f.key)))
          setSelectedFiles(new Set())
          // Limpar cache
          const { filesCache } = await import('@/lib/files-cache')
          filesCache.clear()
        } else {
          throw new Error(data.message || 'Erro ao excluir arquivos')
        }
      } else if (response.status === 403) {
        throw new Error('Sessão expirada. Faça login novamente.')
      } else {
        throw new Error(`Bulk delete failed: ${response.status}`)
      }
    } catch (err) {
      console.error('Bulk delete error:', err)
      alert(err instanceof Error ? err.message : 'Erro ao excluir arquivos')
    } finally {
      setDeleting(new Set())
    }
  }

  const handleConvertFiles = async () => {
    if (selectedFiles.size === 0) return
    
    const convertibleFiles = files.filter(f => {
      const status = getConversionStatus(f.name, f.key)
      return selectedFiles.has(f.key) && status.canConvert
    })
    
    if (convertibleFiles.length === 0) {
      alert('Nenhum arquivo selecionado pode ser convertido')
      return
    }
    
    if (!confirm(`Converter ${convertibleFiles.length} arquivo(s) para MP4 720p?\n\nCusto estimado: ~$${(convertibleFiles.length * 0.75).toFixed(2)} USD`)) return

    try {
      const newConverting = new Set(converting)
      convertibleFiles.forEach(f => newConverting.add(f.key))
      setConverting(newConverting)
      
      // Start conversions using direct Lambda API (same as successful ones)
      const promises = convertibleFiles.map(file =>
        fetch(getApiUrl('CONVERT'), {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ key: file.key })
        })
      )

      const results = await Promise.all(promises)
      
      let successCount = 0
      for (const result of results) {
        if (result.ok) successCount++
      }
      
      alert(`${successCount}/${convertibleFiles.length} conversões iniciadas com sucesso!\n\nOs arquivos serão substituídos automaticamente quando a conversão terminar.`)
      
      setSelectedFiles(new Set())
      
      // Remove from converting state after 2 minutes (conversions should be done)
      setTimeout(() => {
        setConverting(new Set())
        // Don't auto-refresh - let user refresh manually
      }, 120000)
      
    } catch (err) {
      console.error('Conversion error:', err)
      alert('Erro ao iniciar conversões')
      setConverting(new Set())
    }
  }

  if (loading) {
    return (
      <div className="glass-card p-8 text-center">
        <RefreshCw className="w-8 h-8 text-neon-cyan animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Carregando arquivos...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="glass-card p-8 text-center">
        <p className="text-red-400 mb-4">{error}</p>
        <button onClick={() => fetchFiles(1, false)} className="btn-neon">
          Tentar Novamente
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-4">



      {/* Header + Filters sticky */}
      <div className="sticky top-[52px] z-40 bg-dark-900/95 backdrop-blur-md border-b border-white/5 px-3 sm:px-8 py-2 -mx-4 sm:-mx-8">
        {/* Mobile portrait: busca full-width + ícones */}
        <div className="flex md:hidden items-center gap-2">
          {/* Busca */}
          <div className="relative flex items-center flex-1">
            <Search className="absolute left-2.5 w-3.5 h-3.5 text-gray-500 pointer-events-none" />
            <input
              type="text"
              placeholder="Buscar..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full h-[38px] pl-8 pr-7 bg-white/5 border border-white/10 rounded-xl text-white text-sm placeholder-gray-500 focus:border-[#667eea]/60 focus:outline-none transition-colors"
            />
            {searchTerm && (
              <button onClick={() => setSearchTerm('')} className="absolute right-2 p-1 text-gray-500 hover:text-white">
                <X className="w-3 h-3" />
              </button>
            )}
          </div>

          {/* Pasta dropdown */}
          <div className="relative flex-shrink-0">
            <button
              onClick={() => { setMobileFolderOpen(v => !v); setMobileSortOpen(false) }}
              className={`h-[38px] w-[38px] flex items-center justify-center rounded-xl border transition-colors ${
                getCurrentFolderPath() ? 'bg-[#667eea]/20 border-[#667eea]/40 text-[#a5b4fc]' : 'bg-white/5 border-white/10 text-gray-400'
              }`}
            >
              <span className="text-base">📁</span>
            </button>
            {mobileFolderOpen && (
              <>
                <div className="fixed inset-0 z-40" onClick={() => setMobileFolderOpen(false)} />
                <div className="absolute right-0 top-full mt-1 w-52 rounded-xl border border-white/10 shadow-xl z-50 overflow-hidden" style={{ background: 'rgba(8,8,18,0.98)', backdropFilter: 'blur(20px)' }}>
                  <button
                    onClick={() => { setCurrentPath(['']); setInitialPathSet(false); setMobileFolderOpen(false) }}
                    className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${
                      !getCurrentFolderPath() ? 'text-white bg-[#667eea]/15' : 'text-gray-400 hover:text-white hover:bg-white/5'
                    }`}
                  >Todas as pastas</button>
                  {folders.map(folder => {
                    const f = folder.replace('📁 ', '')
                    const label = f.split('/').pop() || f
                    return (
                      <button
                        key={folder}
                        onClick={() => { navigateToFolder(f === 'Raiz' ? '' : f); setMobileFolderOpen(false) }}
                        className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${
                          getCurrentFolderPath() === f ? 'text-white bg-[#667eea]/15' : 'text-gray-400 hover:text-white hover:bg-white/5'
                        }`}
                      >📁 {label}</button>
                    )
                  })}
                </div>
              </>
            )}
          </div>

          {/* Ordenação dropdown */}
          <div className="relative flex-shrink-0">
            <button
              onClick={() => { setMobileSortOpen(v => !v); setMobileFolderOpen(false) }}
              className="h-[38px] w-[38px] flex items-center justify-center rounded-xl border bg-white/5 border-white/10 text-gray-400 transition-colors"
            >
              <Filter className="w-3.5 h-3.5" />
            </button>
            {mobileSortOpen && (
              <>
                <div className="fixed inset-0 z-40" onClick={() => setMobileSortOpen(false)} />
                <div className="absolute right-0 top-full mt-1 w-44 rounded-xl border border-white/10 shadow-xl z-50 overflow-hidden" style={{ background: 'rgba(8,8,18,0.98)', backdropFilter: 'blur(20px)' }}>
                  {[
                    { v: 'name-asc', l: 'Nome A→Z' },
                    { v: 'name-desc', l: 'Nome Z→A' },
                    { v: 'size-desc', l: 'Maior primeiro' },
                    { v: 'date-desc', l: 'Mais recente' },
                  ].map(opt => (
                    <button
                      key={opt.v}
                      onClick={() => {
                        const [by, order] = opt.v.split('-') as ['name'|'size'|'date','asc'|'desc']
                        setSortBy(by); setSortOrder(order); setMobileSortOpen(false)
                      }}
                      className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${
                        `${sortBy}-${sortOrder}` === opt.v ? 'text-white bg-[#667eea]/15' : 'text-gray-400 hover:text-white hover:bg-white/5'
                      }`}
                    >{opt.l}</button>
                  ))}
                </div>
              </>
            )}
          </div>

          {/* Refresh */}
          <button
            onClick={() => { const { filesCache } = require('@/lib/files-cache'); filesCache.clear(); fetchFiles() }}
            className="h-[38px] w-[38px] flex items-center justify-center rounded-xl border bg-white/5 border-white/10 text-gray-400 flex-shrink-0 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>

          {/* Delete bulk */}
          {selectedFiles.size > 0 && (
            <button onClick={handleBulkDelete} className="h-[38px] w-[38px] flex items-center justify-center rounded-xl border bg-red-600/20 border-red-500/30 text-red-400 flex-shrink-0">
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Desktop: linha única */}
        <div className="hidden md:flex items-center gap-2">
          {/* Contador */}
          <span className="hidden lg:flex items-center text-xs text-gray-500 flex-shrink-0 min-w-[60px]">
            <span className="text-white font-semibold mr-1">{filteredFiles.length}</span> arquivos
          </span>

          {/* Busca */}
          <div className="relative flex items-center flex-1 min-w-0 max-w-xs">
            <Search className="absolute left-2.5 w-3.5 h-3.5 text-gray-500 pointer-events-none" />
            <input
              type="text"
              placeholder="Buscar..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full h-[34px] pl-8 pr-7 bg-white/5 border border-white/10 rounded-lg text-white text-sm placeholder-gray-500 focus:border-[#667eea]/60 focus:bg-white/8 focus:outline-none transition-colors"
            />
            {searchTerm && (
              <button onClick={() => setSearchTerm('')} className="absolute right-2 p-0.5 text-gray-500 hover:text-white">
                <X className="w-3 h-3" />
              </button>
            )}
          </div>

          {/* Toggle filtros */}
          <button
            onClick={() => setFiltersOpen(v => !v)}
            className={`h-[34px] px-3 flex items-center gap-1.5 rounded-lg border text-sm transition-colors flex-shrink-0 ${
              filtersOpen
                ? 'bg-[#667eea]/20 border-[#667eea]/40 text-[#a5b4fc]'
                : 'bg-white/5 border-white/10 text-gray-400 hover:text-white'
            }`}
          >
            <Filter className="w-3.5 h-3.5" />
            <span>Filtros</span>
            {(!!getCurrentFolderPath() || selectedType !== 'all') && (
              <span className="w-1.5 h-1.5 rounded-full bg-[#667eea]" />
            )}
          </button>

          {/* Filtros colapsáveis */}
          {filtersOpen && (
            <>
              {/* Pasta */}
              <div className="relative flex-shrink-0">
                <button
                  onClick={() => { setFolderDropOpen(v => !v); setTypeDropOpen(false); setSortDropOpen(false) }}
                  className={`h-[34px] px-3 flex items-center gap-1.5 bg-white/5 border rounded-lg text-sm transition-colors ${
                    getCurrentFolderPath() ? 'text-white border-[#667eea]/40' : 'text-gray-400 border-white/10 hover:text-white'
                  }`}
                >
                  <span className="max-w-[120px] truncate">
                    {getCurrentFolderPath() ? getCurrentFolderPath().split('/').pop() : 'Pasta'}
                  </span>
                  <svg className={`w-3 h-3 transition-transform ${folderDropOpen ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {folderDropOpen && (
                  <>
                    <div className="fixed inset-0 z-40" onClick={() => setFolderDropOpen(false)} />
                    <div className="absolute left-0 top-full mt-1 w-52 rounded-xl border border-white/10 shadow-xl z-50 overflow-hidden" style={{ background: 'rgba(8,8,18,0.98)', backdropFilter: 'blur(20px)' }}>
                      <button
                        onClick={() => { setCurrentPath(['']); setInitialPathSet(false); setFolderDropOpen(false) }}
                        className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${!getCurrentFolderPath() ? 'text-white bg-[#667eea]/15' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
                      >
                        Todas as pastas
                      </button>
                      {folders.map(folder => {
                        const f = folder.replace('📁 ', '')
                        const label = f.split('/').pop() || f
                        return (
                          <button
                            key={folder}
                            onClick={() => { navigateToFolder(f === 'Raiz' ? '' : f); setFolderDropOpen(false) }}
                            className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${getCurrentFolderPath() === f ? 'text-white bg-[#667eea]/15' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
                          >
                            📁 {label}
                          </button>
                        )
                      })}
                    </div>
                  </>
                )}
              </div>

              {/* Tipo */}
              <div className="relative flex-shrink-0">
                <button
                  onClick={() => { setTypeDropOpen(v => !v); setFolderDropOpen(false); setSortDropOpen(false) }}
                  className={`h-[34px] px-3 flex items-center gap-1.5 bg-white/5 border rounded-lg text-sm transition-colors ${
                    selectedType !== 'all' ? 'text-white border-[#667eea]/40' : 'text-gray-400 border-white/10 hover:text-white'
                  }`}
                >
                  <span>
                    {selectedType === 'all' ? 'Tipo' : selectedType === 'video' ? 'Vídeos' : selectedType === 'image' ? 'Imagens' : 'Docs'}
                  </span>
                  <svg className={`w-3 h-3 transition-transform ${typeDropOpen ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {typeDropOpen && (
                  <>
                    <div className="fixed inset-0 z-40" onClick={() => setTypeDropOpen(false)} />
                    <div className="absolute left-0 top-full mt-1 w-36 rounded-xl border border-white/10 shadow-xl z-50 overflow-hidden" style={{ background: 'rgba(8,8,18,0.98)', backdropFilter: 'blur(20px)' }}>
                      {[{ v: 'all', l: 'Todos' }, { v: 'video', l: 'Vídeos' }, { v: 'image', l: 'Imagens' }, { v: 'document', l: 'Docs' }].map(opt => (
                        <button
                          key={opt.v}
                          onClick={() => { setSelectedType(opt.v); setTypeDropOpen(false) }}
                          className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${selectedType === opt.v ? 'text-white bg-[#667eea]/15' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
                        >
                          {opt.l}
                        </button>
                      ))}
                    </div>
                  </>
                )}
              </div>

              {/* Ordenação */}
              <div className="relative flex-shrink-0">
                <button
                  onClick={() => { setSortDropOpen(v => !v); setFolderDropOpen(false); setTypeDropOpen(false) }}
                  className="h-[34px] px-3 flex items-center gap-1.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-400 hover:text-white transition-colors"
                >
                  <span>
                    {sortBy === 'name' && sortOrder === 'asc' ? 'Nome A→Z' :
                     sortBy === 'name' && sortOrder === 'desc' ? 'Nome Z→A' :
                     sortBy === 'size' && sortOrder === 'asc' ? 'Menor' :
                     sortBy === 'size' && sortOrder === 'desc' ? 'Maior' :
                     sortBy === 'date' && sortOrder === 'desc' ? 'Recente' : 'Antigo'}
                  </span>
                  <svg className={`w-3 h-3 transition-transform ${sortDropOpen ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {sortDropOpen && (
                  <>
                    <div className="fixed inset-0 z-40" onClick={() => setSortDropOpen(false)} />
                    <div className="absolute left-0 top-full mt-1 w-40 rounded-xl border border-white/10 shadow-xl z-50 overflow-hidden" style={{ background: 'rgba(8,8,18,0.98)', backdropFilter: 'blur(20px)' }}>
                      {[
                        { v: 'name-asc', l: 'Nome A→Z' }, { v: 'name-desc', l: 'Nome Z→A' },
                        { v: 'size-asc', l: 'Menor' }, { v: 'size-desc', l: 'Maior' },
                        { v: 'date-desc', l: 'Recente' }, { v: 'date-asc', l: 'Antigo' },
                      ].map(opt => (
                        <button
                          key={opt.v}
                          onClick={() => { const [by, order] = opt.v.split('-') as ['name'|'size'|'date','asc'|'desc']; setSortBy(by); setSortOrder(order); setSortDropOpen(false) }}
                          className={`w-full text-left px-4 py-2.5 text-sm transition-colors ${`${sortBy}-${sortOrder}` === opt.v ? 'text-white bg-[#667eea]/15' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
                        >
                          {opt.l}
                        </button>
                      ))}
                    </div>
                  </>
                )}
              </div>
            </>
          )}

          {/* Ações */}
          <div className="flex gap-1 flex-shrink-0 ml-auto">
            <button
              onClick={() => { const { filesCache } = require('@/lib/files-cache'); filesCache.clear(); fetchFiles() }}
              className="h-[34px] w-[34px] flex items-center justify-center bg-white/5 hover:bg-white/10 text-gray-400 hover:text-cyan-300 rounded-lg border border-white/10 transition-colors"
              title="Atualizar"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => { if (selectAll) { setSelectedFiles(new Set()); setSelectAll(false) } else { setSelectAll(true) } }}
              className={`h-[34px] w-[34px] flex items-center justify-center rounded-lg border transition-colors ${
                selectAll ? 'bg-[#667eea]/20 text-[#a5b4fc] border-[#667eea]/40' : 'bg-white/5 text-gray-400 border-white/10 hover:bg-white/10'
              }`}
              title={selectAll ? 'Sair da seleção' : 'Selecionar'}
            >
              <ListChecks className="w-3.5 h-3.5" />
            </button>
            {selectedFiles.size > 0 && (
              <>
                <button
                  onClick={() => { const selectedItems = filteredFiles.filter(f => selectedFiles.has(f.key)); setShareModal({ key: 'bulk', name: `${selectedItems.length} arquivo(s)`, type: 'video', items: selectedItems }) }}
                  className="h-[34px] w-[34px] flex items-center justify-center bg-white/5 hover:bg-[#667eea]/20 text-gray-400 hover:text-[#a5b4fc] rounded-lg border border-white/10 transition-colors"
                  title="Compartilhar"
                >
                  <Share2 className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={handleBulkDelete}
                  className="h-[34px] w-[34px] flex items-center justify-center bg-white/5 hover:bg-red-600/20 text-gray-400 hover:text-red-400 rounded-lg border border-white/10 transition-colors"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
                <span className="flex items-center text-xs text-[#a5b4fc] font-semibold px-1">{selectedFiles.size}</span>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Carousel View */}
      <ContentCarousel
        files={filteredFiles}
        sortBy={sortBy}
        sortOrder={sortOrder}
        onItemClick={(file) => {
          if (file.type === 'video') onPlayVideo?.(file as any)
          else if (file.type === 'image') onViewImage?.(file as any)
          else if (file.type === 'document') onViewPDF?.(file as any)
        }}
        onItemDelete={(file) => handleDelete(file as any)}
        onItemShare={(file) => setShareModal(file)}
        onBulkDelete={(items) => {
          setDeleteModal({ type: 'folder', items })
        }}
        selectionMode={selectAll}
        selectedKeys={selectedFiles}
        onToggleSelect={(key) => toggleFileSelection(key)}
      />

      {/* Share Modal */}
      <InputModal
        isOpen={!!shareModal}
        onClose={() => setShareModal(null)}
        onConfirm={async (category) => {
          if (!shareModal) return
          try {
            const token = localStorage.getItem('token')
            if (shareModal.items) {
              // Bulk share
              for (const item of shareModal.items) {
                await fetch(getApiUrl('PUBLIC_CONTENT'), {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                  body: JSON.stringify({ file_key: item.key, title: item.name, type: item.type, category, duration: item.duration || 0 })
                })
              }
              setSelectedFiles(new Set())
              setSelectAll(false)
            } else {
              // Single share
              await fetch(getApiUrl('PUBLIC_CONTENT'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ file_key: shareModal.key, title: shareModal.name, type: shareModal.type, category, duration: shareModal.duration || 0 })
              })
            }
            setShareModal(null)
          } catch (e) {
            console.error('Share error:', e)
          }
        }}
        title="Compartilhar na Área Pública"
        message={shareModal ? `Compartilhar "${shareModal.name}" publicamente?` : ''}
        options={['Geral', 'Filmes', 'Séries', 'Anime', 'Música', 'Documentos', 'Fotos']}
        defaultValue="Geral"
        confirmText="Compartilhar"
      />

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={!!deleteModal}
        onClose={() => setDeleteModal(null)}
        onConfirm={() => {
          if (deleteModal?.type === 'single' && deleteModal.file) {
            executeDelete(deleteModal.file)
          } else if (deleteModal?.type === 'bulk') {
            executeBulkDelete()
          } else if (deleteModal?.type === 'folder' && deleteModal.items) {
            const keys = deleteModal.items.map((i: any) => i.key)
            setSelectedFiles(new Set(keys))
            setTimeout(() => executeBulkDelete(), 100)
          }
        }}
        title={deleteModal?.type === 'folder' ? 'Excluir pasta' : 'Excluir arquivo(s)'}
        message={
          deleteModal?.type === 'single'
            ? `Deseja excluir "${deleteModal?.file?.name}"?`
            : deleteModal?.type === 'folder'
            ? `Deseja excluir ${deleteModal?.items?.length} arquivo(s) desta pasta?`
            : `Deseja excluir ${selectedFiles.size} arquivo(s) selecionado(s)?`
        }
        confirmText="Excluir"
        confirmColor="red"
      />
    </div>
  )
}