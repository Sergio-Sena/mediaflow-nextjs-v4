'use client'

import { useState, useEffect } from 'react'
import { Folder, ChevronRight, Home, RefreshCw, Play } from 'lucide-react'

interface S3File {
  key: string
  name: string
  size: number
  lastModified: string
  url: string
  type: 'video' | 'image' | 'document' | 'other'
  folder: string
}

interface FolderManagerProps {
  onNavigateToFolder?: (folderPath: string) => void
  onFilesLoaded?: (files: S3File[]) => void
}

export default function FolderManager({ onNavigateToFolder, onFilesLoaded }: FolderManagerProps) {
  const [files, setFiles] = useState<S3File[]>([])
  const [folderStructure, setFolderStructure] = useState<{[key: string]: string[]}>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPath, setCurrentPath] = useState<string[]>([''])
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set())
  const [selectAll, setSelectAll] = useState(false)

  const fetchFiles = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const { mediaflowClient } = await import('@/lib/aws-client')
      const data = await mediaflowClient.getFiles()
      
      if (data.success) {
        const transformedFiles = data.files.map((file: any) => {
          const folderName = file.folder || (
            file.key.includes('/') ? file.key.split('/').slice(0, -1).join('/') : 'root'
          )
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
            bucket: file.bucket
          }
        })
        
        setFiles(transformedFiles)
        onFilesLoaded?.(transformedFiles)
        
        // Build folder structure
        const structure: {[key: string]: string[]} = {}
        transformedFiles.forEach((file: any) => {
          if (file.folder && file.folder !== 'root') {
            const parts = file.folder.split('/')
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
  }, [])

  const navigateToFolder = (folderPath: string) => {
    const pathParts = folderPath ? folderPath.split('/') : ['']
    setCurrentPath(['', ...pathParts])
  }
  
  const navigateUp = (index: number) => {
    setCurrentPath(currentPath.slice(0, index + 1))
  }
  
  const getCurrentFolderPath = () => {
    return currentPath.slice(1).join('/')
  }
  
  const getCurrentFolders = () => {
    const currentFolderPath = getCurrentFolderPath()
    return folderStructure[currentFolderPath] || []
  }

  const getCurrentFiles = () => {
    const currentFolderPath = getCurrentFolderPath()
    return files.filter(file => {
      if (currentFolderPath === '') {
        return file.folder === 'root' || !file.folder.includes('/')
      }
      return file.folder === currentFolderPath
    })
  }

  const handleFolderClick = (folderPath: string) => {
    onNavigateToFolder?.(folderPath)
  }

  if (loading) {
    return (
      <div className="glass-card p-8 text-center">
        <RefreshCw className="w-8 h-8 text-neon-cyan animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Carregando pastas...</p>
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
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">
              🗂️ Gerenciador de Pastas
            </h2>
            <p className="text-gray-400">
              Navegue pela estrutura hierárquica de pastas
            </p>
          </div>
          <button
            onClick={fetchFiles}
            className="btn-refresh mt-1"
            title="Atualizar"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Breadcrumb Navigation */}
      <div className="glass-card p-4">
        <div className="flex items-center gap-2 text-sm">
          <button
            onClick={() => setCurrentPath([''])}
            className="flex items-center gap-1 px-3 py-1 rounded-lg hover:bg-neon-cyan/20 text-neon-cyan transition-colors"
          >
            <Home className="w-4 h-4" />
            Raiz
          </button>
          {currentPath.slice(1).map((folder, index) => (
            <div key={index} className="flex items-center gap-2">
              <ChevronRight className="w-4 h-4 text-gray-400" />
              <button
                onClick={() => navigateUp(index + 1)}
                className="px-3 py-1 rounded-lg hover:bg-neon-cyan/20 text-white transition-colors"
              >
                📁 {folder}
              </button>
            </div>
          ))}
        </div>
      </div>
      
      {/* Folders and Files */}
      <div className="glass-card p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-white">
            {getCurrentFolders().length > 0 ? `📁 Pastas (${getCurrentFolders().length})` : `📄 ${getCurrentFolderPath() || 'Raiz'} (${getCurrentFiles().length} arquivos)`}
          </h3>
          {getCurrentFiles().length > 0 && (
            <div className="flex gap-2">
              {selectedFiles.size > 0 && (
                <button
                  onClick={async () => {
                    if (!confirm(`Deseja excluir ${selectedFiles.size} arquivo(s)?`)) return
                    try {
                      const promises = Array.from(selectedFiles).map(key =>
                        fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files', {
                          method: 'DELETE',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ key })
                        })
                      )
                      await Promise.all(promises)
                      setFiles(prev => prev.filter(f => !selectedFiles.has(f.key)))
                      setSelectedFiles(new Set())
                      setSelectAll(false)
                    } catch (err) {
                      alert('Erro ao excluir arquivos')
                    }
                  }}
                  className="p-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors font-bold"
                  title="Excluir Selecionados"
                >
                  🗑️
                </button>
              )}
              <button
                onClick={() => {
                  if (selectAll) {
                    setSelectedFiles(new Set())
                    setSelectAll(false)
                  } else {
                    setSelectedFiles(new Set(getCurrentFiles().map(f => f.key)))
                    setSelectAll(true)
                  }
                }}
                className={`btn-secondary p-2 ${selectAll ? 'bg-neon-cyan/20 text-neon-cyan' : ''}`}
                title={selectAll ? 'Desmarcar Todos' : 'Selecionar Todos'}
              >
                {selectAll ? '☑️' : '☐'}
              </button>
            </div>
          )}
        </div>
        
        {getCurrentFolders().length === 0 ? (
          getCurrentFiles().length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {getCurrentFiles().map((file) => {
                const getFileIcon = (type: string) => {
                  switch (type) {
                    case 'video': return '🎥'
                    case 'image': return '🖼️'
                    case 'document': return '📄'
                    default: return '📁'
                  }
                }
                
                const formatFileSize = (bytes: number) => {
                  if (bytes === 0) return '0 B'
                  const k = 1024
                  const sizes = ['B', 'KB', 'MB', 'GB']
                  const i = Math.floor(Math.log(bytes) / Math.log(k))
                  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
                }
                
                const isSelected = selectedFiles.has(file.key)
                
                return (
                  <div 
                    key={file.key} 
                    className={`flex items-center gap-3 p-3 rounded-lg bg-gray-800/50 hover:bg-gray-700/50 transition-colors cursor-pointer ${isSelected ? 'ring-2 ring-neon-cyan' : ''}`}
                    onDoubleClick={() => onNavigateToFolder?.(file.folder)}
                  >
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => {
                        const newSelected = new Set(selectedFiles)
                        if (newSelected.has(file.key)) {
                          newSelected.delete(file.key)
                        } else {
                          newSelected.add(file.key)
                        }
                        setSelectedFiles(newSelected)
                        setSelectAll(newSelected.size === getCurrentFiles().length)
                      }}
                      onClick={(e) => e.stopPropagation()}
                      className="w-4 h-4 text-neon-cyan bg-gray-800 border-gray-600 rounded focus:ring-neon-cyan"
                    />
                    <span className="text-2xl flex-shrink-0">{getFileIcon(file.type)}</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-white text-sm font-medium truncate" title={file.name}>{file.name}</p>
                      <p className="text-gray-400 text-xs flex-shrink-0">{formatFileSize(file.size)}</p>
                    </div>
                    <button
                      onClick={async () => {
                        if (!confirm(`Deseja excluir "${file.name}"?`)) return
                        try {
                          const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files', {
                            method: 'DELETE',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ key: file.key })
                          })
                          if (response.ok) {
                            setFiles(prev => prev.filter(f => f.key !== file.key))
                            setSelectedFiles(prev => {
                              const newSet = new Set(prev)
                              newSet.delete(file.key)
                              return newSet
                            })
                          }
                        } catch (err) {
                          alert('Erro ao excluir arquivo')
                        }
                      }}
                      className="p-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
                      title="Excluir"
                    >
                      🗑️
                    </button>
                  </div>
                )
              })}
            </div>
          ) : (
            <div className="text-center py-8">
              <Folder className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">Pasta vazia</p>
            </div>
          )
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 justify-items-center">
            {getCurrentFolders().map(folderPath => {
              const folderName = folderPath.split('/').pop() || folderPath
              
              // Contar arquivos diretos na pasta
              const directFileCount = files.filter(f => f.folder === folderPath).length
              
              // Contar subpastas
              const subFolderCount = folderStructure[folderPath]?.length || 0
              
              // Contar total de arquivos (incluindo subpastas)
              const totalFileCount = files.filter(f => f.folder.startsWith(folderPath + '/') || f.folder === folderPath).length
              
              return (
                <button
                  key={folderPath}
                  onClick={() => navigateToFolder(folderPath)}
                  className="w-full flex flex-col items-center gap-2 p-4 rounded-lg bg-gray-800/50 hover:bg-neon-cyan/20 transition-colors group"
                >
                  <span className="text-3xl group-hover:scale-110 transition-transform flex-shrink-0">📁</span>
                  <span className="text-sm text-white truncate w-full text-center font-medium px-1" title={folderName}>
                    {folderName}
                  </span>
                  <div className="text-xs text-gray-400 text-center">
                    {subFolderCount > 0 && (
                      <div>📁 {subFolderCount} pasta{subFolderCount !== 1 ? 's' : ''}</div>
                    )}
                    <div>📄 {totalFileCount} arquivo{totalFileCount !== 1 ? 's' : ''}</div>
                  </div>
                </button>
              )
            })}
          </div>
        )}
      </div>

    </div>
  )
}