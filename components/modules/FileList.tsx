'use client'

import { useState, useEffect } from 'react'
import { Play, Download, Trash2, Search, Filter, Grid, List, RefreshCw } from 'lucide-react'

interface S3File {
  key: string
  name: string
  size: number
  lastModified: string
  url: string
  type: 'video' | 'image' | 'document' | 'other'
  folder: string
}

interface FileListProps {
  onPlayVideo?: (file: S3File) => void
  onViewImage?: (file: S3File) => void
  onViewPDF?: (file: S3File) => void
  refreshTrigger?: number
}

export default function FileList({ onPlayVideo, onViewImage, onViewPDF, refreshTrigger }: FileListProps) {
  const [files, setFiles] = useState<S3File[]>([])
  const [folders, setFolders] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFolder, setSelectedFolder] = useState<string>('all')
  const [selectedType, setSelectedType] = useState<string>('all')
  const [viewMode, setViewMode] = useState<'list' | 'grid'>('list')
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set())

  const fetchFiles = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const { mediaflowClient } = await import('@/lib/aws-client')
      const data = await mediaflowClient.getFiles()
      
      if (data.success) {
        // Transform AWS response to match component expectations
        const transformedFiles = data.files.map((file: any) => {
          const pathParts = file.key.split('/')
          const fileName = pathParts.pop() || file.key
          const folderName = pathParts.length > 0 ? pathParts[0] : 'root'
          const fileType = getFileTypeFromName(file.key)
          
          return {
            key: file.key,
            name: fileName,
            size: file.size,
            lastModified: file.lastModified,
            url: `https://${file.bucket === 'uploads' ? 'mediaflow-uploads-969430605054' : 'mediaflow-processed-969430605054'}.s3.amazonaws.com/${encodeURIComponent(file.key)}`,
            type: fileType,
            folder: folderName,
            bucket: file.bucket
          }
        })
        
        setFiles(transformedFiles)
        
        // Extract unique folders (only real folders + root)
        const realFolders = transformedFiles.map((f: any) => f.folder as string).filter((f: string) => f !== 'root')
        const uniqueRealFolders = Array.from(new Set(realFolders)) as string[]
        
        // Check if there are files in root
        const hasRootFiles = transformedFiles.some((f: any) => f.folder === 'root')
        
        // Build folder list (no virtual type folders)
        const rootFolder = hasRootFiles ? ['📁 Raiz'] : []
        const realFoldersWithIcon = uniqueRealFolders.map(f => `📁 ${f}`)
        
        const allFolders = [...rootFolder, ...realFoldersWithIcon]
        
        setFolders(allFolders)
      } else {
        throw new Error(data.message || 'Erro ao carregar arquivos')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido')
    } finally {
      setLoading(false)
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
    fetchFiles()
  }, [refreshTrigger])

  const filteredFiles = files.filter(file => {
    const matchesSearch = file.name.toLowerCase().includes(searchTerm.toLowerCase())
    
    // Handle real folders only
    let matchesFolder = true
    if (selectedFolder !== 'all') {
      if (selectedFolder === '📁 Raiz') {
        matchesFolder = file.folder === 'root'
      } else if (selectedFolder.startsWith('📁 ')) {
        // Real folder with icon prefix
        const folderName = selectedFolder.replace('📁 ', '')
        matchesFolder = file.folder === folderName
      } else {
        matchesFolder = file.folder === selectedFolder
      }
    }
    
    const matchesType = selectedType === 'all' || file.type === selectedType
    
    return matchesSearch && matchesFolder && matchesType
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

  const getConversionStatus = (filename: string) => {
    if (filename.endsWith('.mp4')) return { icon: '🎯', tooltip: 'Otimizado' }
    if (filename.endsWith('.ts') || filename.endsWith('.avi')) return { icon: '⏳', tooltip: 'Processando' }
    return { icon: '🎥', tooltip: 'Original' }
  }

  const handleDownload = (file: S3File) => {
    const link = document.createElement('a')
    link.href = file.url
    link.download = file.name
    link.click()
  }

  const handleDelete = async (file: S3File) => {
    if (!confirm(`Deseja excluir "${file.name}"?`)) return

    try {
      // Direct API call to avoid client issues
      const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key: file.key })
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setFiles(prev => prev.filter(f => f.key !== file.key))
        } else {
          throw new Error(data.message || 'Erro ao excluir arquivo')
        }
      } else {
        throw new Error(`Delete failed: ${response.status}`)
      }
    } catch (err) {
      console.error('Delete error:', err)
      alert('Erro ao excluir arquivo')
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

  const handleBulkDelete = async () => {
    if (selectedFiles.size === 0) return
    if (!confirm(`Deseja excluir ${selectedFiles.size} arquivo(s)?`)) return

    try {
      // Delete files one by one
      const promises = Array.from(selectedFiles).map(key =>
        fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ key })
        })
      )

      await Promise.all(promises)
      setFiles(prev => prev.filter(f => !selectedFiles.has(f.key)))
      setSelectedFiles(new Set())
    } catch (err) {
      console.error('Bulk delete error:', err)
      alert('Erro ao excluir arquivos')
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
        <button onClick={fetchFiles} className="btn-neon">
          Tentar Novamente
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-6">
        <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">
              🎬 Arquivos ({filteredFiles.length})
            </h2>
            <p className="text-gray-400">
              {selectedFiles.size > 0 && `${selectedFiles.size} selecionado(s) • `}
              Total: {formatFileSize(files.reduce((acc, f) => acc + f.size, 0))}
            </p>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={fetchFiles}
              className="btn-secondary p-2"
              title="Atualizar"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
            
            <button
              onClick={() => setViewMode(viewMode === 'list' ? 'grid' : 'list')}
              className="btn-secondary p-2"
              title={viewMode === 'list' ? 'Visualização em Grade' : 'Visualização em Lista'}
            >
              {viewMode === 'list' ? <Grid className="w-4 h-4" /> : <List className="w-4 h-4" />}
            </button>
            
            {selectedFiles.size > 0 && (
              <button
                onClick={handleBulkDelete}
                className="btn-danger p-2"
                title="Excluir Selecionados"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Buscar arquivos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-neon-cyan focus:outline-none"
            />
          </div>

          {/* Folder Filter */}
          <select
            value={selectedFolder}
            onChange={(e) => setSelectedFolder(e.target.value)}
            className="px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:border-neon-cyan focus:outline-none"
          >
            <option value="all">📁 Todas as pastas</option>
            {folders.map(folder => (
              <option key={folder} value={folder}>{folder}</option>
            ))}
          </select>

          {/* Type Filter */}
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:border-neon-cyan focus:outline-none"
          >
            <option value="all">Todos os tipos</option>
            <option value="video">Vídeos</option>
            <option value="image">Imagens</option>
            <option value="document">Documentos</option>
            <option value="other">Outros</option>
          </select>

          {/* Clear Filters */}
          <button
            onClick={() => {
              setSearchTerm('')
              setSelectedFolder('all')
              setSelectedType('all')
            }}
            className="btn-secondary"
          >
            <Filter className="w-4 h-4 mr-2" />
            Limpar Filtros
          </button>
        </div>
      </div>

      {/* File List */}
      {filteredFiles.length === 0 ? (
        <div className="glass-card p-8 text-center">
          <p className="text-gray-400">Nenhum arquivo encontrado</p>
        </div>
      ) : (
        <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-3'}>
          {filteredFiles.map((file) => {
            const status = getConversionStatus(file.name)
            const isSelected = selectedFiles.has(file.key)
            
            return (
              <div
                key={file.key}
                className={`glass-card p-4 transition-all duration-200 ${
                  isSelected ? 'ring-2 ring-neon-cyan' : ''
                }`}
              >
                <div className="flex items-center gap-4">
                  {/* Checkbox */}
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => toggleFileSelection(file.key)}
                    className="w-4 h-4 text-neon-cyan bg-gray-800 border-gray-600 rounded focus:ring-neon-cyan"
                  />

                  {/* File Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-lg">{getFileIcon(file.type)}</span>
                      <span 
                        className="text-lg cursor-help" 
                        title={status.tooltip}
                      >
                        {status.icon}
                      </span>
                      <h3 className="font-medium text-white truncate flex-1">
                        {file.name}
                      </h3>
                    </div>
                    
                    <div className="flex items-center gap-4 text-sm text-gray-400">
                      <span>{formatFileSize(file.size)}</span>
                      <span>{formatDate(file.lastModified)}</span>
                      {file.folder !== 'root' && (
                        <span className="text-neon-cyan">📁 {file.folder}</span>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    {file.type === 'video' && (
                      <button
                        onClick={async () => {
                          try {
                            const response = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(file.key)}`, {
                              method: 'GET',
                              headers: { 'Content-Type': 'application/json' }
                            })
                            
                            if (response.ok) {
                              const data = await response.json()
                              if (data.success) {
                                onPlayVideo?.({ ...file, url: data.viewUrl })
                              }
                            }
                          } catch (error) {
                            onPlayVideo?.(file)
                          }
                        }}
                        className="p-2 bg-neon-purple/20 hover:bg-neon-purple/30 text-neon-purple rounded-lg transition-colors"
                        title="Reproduzir"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                    )}
                    
                    {file.type === 'image' && (
                      <button
                        onClick={async () => {
                          try {
                            const response = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(file.key)}`, {
                              method: 'GET',
                              headers: { 'Content-Type': 'application/json' }
                            })
                            
                            if (response.ok) {
                              const data = await response.json()
                              if (data.success) {
                                onViewImage?.({ ...file, url: data.viewUrl })
                              }
                            }
                          } catch (error) {
                            onViewImage?.(file)
                          }
                        }}
                        className="p-2 bg-green-500/20 hover:bg-green-500/30 text-green-400 rounded-lg transition-colors"
                        title="Visualizar"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                    )}
                    
                    {file.type === 'document' && (
                      <button
                        onClick={async () => {
                          try {
                            const response = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(file.key)}`, {
                              method: 'GET',
                              headers: { 'Content-Type': 'application/json' }
                            })
                            
                            if (response.ok) {
                              const data = await response.json()
                              if (data.success) {
                                onViewPDF?.({ ...file, url: data.viewUrl })
                              }
                            }
                          } catch (error) {
                            onViewPDF?.(file)
                          }
                        }}
                        className="p-2 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 rounded-lg transition-colors"
                        title="Visualizar PDF"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                    )}
                    
                    <button
                      onClick={() => handleDownload(file)}
                      className="p-2 bg-neon-cyan/20 hover:bg-neon-cyan/30 text-neon-cyan rounded-lg transition-colors"
                      title="Download"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                    
                    <button
                      onClick={() => handleDelete(file)}
                      className="p-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
                      title="Excluir"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}