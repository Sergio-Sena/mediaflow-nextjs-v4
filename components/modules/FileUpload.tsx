'use client'

import { useState, useCallback, useRef } from 'react'
import { Upload, X, CheckCircle, AlertCircle, File, Video, Image } from 'lucide-react'

interface UploadFile {
  id: string
  file: File
  progress: number
  status: 'pending' | 'uploading' | 'success' | 'error'
  error?: string
  url?: string
  folder?: string
  relativePath?: string
}

interface FileUploadProps {
  onUploadComplete?: (files: UploadFile[]) => void
  maxFiles?: number
  maxSize?: number // MB
  acceptedTypes?: string[]
}

export default function FileUpload({ 
  onUploadComplete, 
  maxFiles = 50, 
  maxSize = 5120, // 5GB máximo (limite S3)
  acceptedTypes = ['video/*', 'image/*', 'application/pdf']
}: FileUploadProps) {
  const [files, setFiles] = useState<UploadFile[]>([])
  const [currentBatch, setCurrentBatch] = useState(0)
  const [totalBatches, setTotalBatches] = useState(0)
  const [isDragging, setIsDragging] = useState(false)
  const [uploadMode, setUploadMode] = useState<'files' | 'folder'>('files')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const folderInputRef = useRef<HTMLInputElement>(null)

  const getFileIcon = (type: string) => {
    if (type.startsWith('video/')) return <Video className="w-5 h-5 text-neon-purple" />
    if (type.startsWith('image/')) return <Image className="w-5 h-5 text-neon-cyan" />
    return <File className="w-5 h-5 text-gray-400" />
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
  }

  const sanitizeFilename = (filename: string): string => {
    // Remove caracteres especiais e limita tamanho
    let sanitized = filename.replace(/[^a-zA-Z0-9.-À-ſ\s]/g, '_')
    
    // Se nome muito longo, trunca mantendo extensão
    if (sanitized.length > 100) {
      const ext = sanitized.split('.').pop() || ''
      const name = sanitized.substring(0, 90 - ext.length)
      sanitized = `${name}...${ext ? '.' + ext : ''}`
    }
    
    return sanitized
  }

  const validateFile = (file: File): string | null => {
    if (file.size > maxSize * 1024 * 1024) {
      return `Arquivo muito grande. Máximo: ${maxSize}MB`
    }
    
    const isValidType = acceptedTypes.some(type => {
      if (type.endsWith('/*')) {
        return file.type.startsWith(type.slice(0, -1))
      }
      return file.type === type
    })
    
    if (!isValidType) {
      return 'Tipo de arquivo não suportado'
    }
    
    return null
  }

  const addFiles = useCallback((newFiles: FileList | File[], isFolder = false) => {
    const validFiles: UploadFile[] = []
    
    Array.from(newFiles).forEach(file => {
      if (files.length + validFiles.length >= maxFiles) return
      
      const error = validateFile(file)
      const relativePath = isFolder ? (file as any).webkitRelativePath || file.name : undefined
      const folder = relativePath ? relativePath.split('/')[0] : undefined
      
      validFiles.push({
        id: Math.random().toString(36).substr(2, 9),
        file,
        progress: 0,
        status: error ? 'error' : 'pending',
        error: error || undefined,
        folder,
        relativePath
      })
    })
    
    setFiles(prev => [...prev, ...validFiles])
  }, [files.length, maxFiles, maxSize, acceptedTypes])

  const uploadFile = async (uploadFile: UploadFile) => {
    try {
      setFiles(prev => prev.map(f => 
        f.id === uploadFile.id ? { ...f, status: 'uploading', progress: 0 } : f
      ))

      // v4.1: Upload modular com estratégias por tamanho
      return await uploadWithStrategy(uploadFile)

    } catch (error) {
      setFiles(prev => prev.map(f => 
        f.id === uploadFile.id 
          ? { ...f, status: 'error', error: error instanceof Error ? error.message : 'Erro no upload' }
          : f
      ))
    }
  }



  const uploadWithStrategy = async (uploadFile: UploadFile) => {
    console.log('=== UPLOAD STRATEGY DEBUG ===')
    console.log('File:', uploadFile.file.name, uploadFile.file.size, 'bytes')
    console.log('Size MB:', Math.round(uploadFile.file.size / 1024 / 1024))
    
    try {
      const { UploadFactory } = await import('../upload/strategies/UploadFactory')
      console.log('UploadFactory imported successfully')
      
      // Preparar filename com estrutura de pasta
      let uploadFilename = uploadFile.file.name
      if (uploadFile.relativePath) {
        uploadFilename = uploadFile.relativePath
      } else if (uploadFile.folder) {
        uploadFilename = `${uploadFile.folder}/${uploadFile.file.name}`
      }
      
      console.log('Upload filename with path:', uploadFilename)
      
      // Selecionar estratégia baseada no tamanho
      const strategy = UploadFactory.createStrategy(uploadFile.file.size)
      const info = UploadFactory.getStrategyInfo(uploadFile.file.size)
      
      console.log(`🚀 MODULAR UPLOAD - Strategy: ${info.type} (${info.timeout}, ${info.retries} retries)`)
      
      // Upload usando estratégia modular
      const result = await strategy.upload(
        uploadFile.file,
        uploadFilename,
        (progress) => {
          setFiles(prev => prev.map(f => 
            f.id === uploadFile.id ? { ...f, progress: progress.percentage } : f
          ))
        }
      )
      
      if (result.success) {
        setFiles(prev => prev.map(f => 
          f.id === uploadFile.id 
            ? { ...f, status: 'success', progress: 100, url: result.url }
            : f
        ))
        console.log('✅ MODULAR UPLOAD SUCCESS:', result.url)
      } else {
        console.error('❌ MODULAR UPLOAD FAILED:', result.error)
        throw new Error(result.error || 'Upload failed')
      }
    } catch (error) {
      console.error('❌ STRATEGY IMPORT ERROR:', error)
      throw error
    }
  }



  const uploadAll = async () => {
    const pendingFiles = files.filter(f => f.status === 'pending')
    const batchSize = 5
    const batches = []
    
    // Dividir em lotes de 5
    for (let i = 0; i < pendingFiles.length; i += batchSize) {
      batches.push(pendingFiles.slice(i, i + batchSize))
    }
    
    setTotalBatches(batches.length)
    
    // Processar lotes sequencialmente
    for (let i = 0; i < batches.length; i++) {
      setCurrentBatch(i + 1)
      const batch = batches[i]
      
      // Upload paralelo dentro do lote
      await Promise.all(batch.map(file => uploadFile(file)))
    }
    
    setCurrentBatch(0)
    setTotalBatches(0)
    
    const completedFiles = files.filter(f => f.status === 'success')
    onUploadComplete?.(completedFiles)
  }

  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id))
  }

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const droppedFiles = Array.from(e.dataTransfer.files)
    const hasFolder = droppedFiles.some(file => (file as any).webkitRelativePath)
    
    console.log('Drop detected:', droppedFiles.length, 'files, hasFolder:', hasFolder)
    addFiles(e.dataTransfer.files, hasFolder)
  }, [addFiles])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  return (
    <div className="space-y-6">
      {/* Drop Zone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          glass-card p-6 text-center border-2 border-dashed transition-all duration-300
          ${isDragging 
            ? 'border-neon-cyan bg-neon-cyan/5 scale-105' 
            : 'border-gray-600 hover:border-neon-cyan/50 hover:bg-neon-cyan/5'
          }
        `}
      >
        <Upload className={`w-10 h-10 mx-auto mb-3 transition-colors ${
          isDragging ? 'text-neon-cyan' : 'text-gray-400'
        }`} />
        
        <h3 className="text-lg font-semibold text-white mb-2">
          {isDragging ? 'Solte os arquivos aqui' : 'Área de Drag & Drop'}
        </h3>
        
        <p className="text-gray-400 text-sm">
          Arraste arquivos ou pastas aqui
        </p>
      </div>

      {/* Selection Buttons */}
      <div className="glass-card p-6">
        <h4 className="text-lg font-semibold text-white mb-4">Ou selecione manualmente</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={(e) => {
              e.stopPropagation()
              setUploadMode('files')
              fileInputRef.current?.click()
            }}
            className="btn-neon p-4 text-sm flex items-center justify-center gap-2"
          >
            📄 Selecionar Arquivos
          </button>
          
          <button
            onClick={(e) => {
              e.stopPropagation()
              setUploadMode('folder')
              folderInputRef.current?.click()
            }}
            className="btn-secondary p-4 text-sm flex items-center justify-center gap-2"
          >
            📁 Selecionar Pasta
          </button>
        </div>
        
        <p className="text-gray-400 text-xs mt-3 text-center">
          Máximo {maxFiles} arquivos • Até 5GB cada • Vídeos, imagens e PDFs<br/>
          <span className="text-neon-cyan text-xs">
🚀 Upload em lotes de 5 - Otimizado para pastas grandes
          </span>
        </p>
      </div>
      
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept={acceptedTypes.join(',')}
        onChange={(e) => e.target.files && addFiles(e.target.files, false)}
        className="hidden"
      />
      
      <input
        ref={folderInputRef}
        type="file"
        multiple
        {...({ webkitdirectory: '' } as any)}
        onChange={(e) => e.target.files && addFiles(e.target.files, true)}
        className="hidden"
      />

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="text-lg font-semibold text-white">
              Arquivos ({files.length})
              {totalBatches > 0 && (
                <span className="text-sm text-neon-cyan ml-2">
                  - Lote {currentBatch}/{totalBatches}
                </span>
              )}
            </h4>
            
            <div className="flex gap-2">
              <button
                onClick={() => setFiles([])}
                className="btn-secondary px-4 py-2 text-sm"
              >
                Limpar
              </button>
              
              {files.some(f => f.status === 'pending') && (
                <button
                  onClick={uploadAll}
                  className="btn-neon px-6 py-2"
                >
                  📤 Upload Todos
                </button>
              )}
            </div>
          </div>

          <div className="space-y-3">
            {files.map((file) => (
              <div key={file.id} className="glass-card p-4">
                <div className="flex items-center gap-4">
                  {getFileIcon(file.file.type)}
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-start mb-1">
                      <div className="flex-1 min-w-0">
                        <h5 className="font-medium text-white truncate">
                          {file.folder && (
                            <span className="text-neon-cyan text-xs mr-2">
                              📁 {file.folder}/
                            </span>
                          )}
                          {file.file.name}
                        </h5>
                        {file.relativePath && (
                          <p className="text-xs text-gray-500 truncate">
                            {file.relativePath}
                          </p>
                        )}
                      </div>
                      
                      <button
                        onClick={() => removeFile(file.id)}
                        className="text-gray-400 hover:text-red-400 transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                    
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-gray-400">
                        {formatFileSize(file.file.size)}
                      </span>
                      
                      <div className="flex items-center gap-2">
                        {file.status === 'success' && (
                          <CheckCircle className="w-4 h-4 text-green-400" />
                        )}
                        {file.status === 'error' && (
                          <AlertCircle className="w-4 h-4 text-red-400" />
                        )}
                        
                        <span className={`
                          ${file.status === 'success' ? 'text-green-400' : ''}
                          ${file.status === 'error' ? 'text-red-400' : ''}
                          ${file.status === 'uploading' ? 'text-neon-cyan' : ''}
                          ${file.status === 'pending' ? 'text-gray-400' : ''}
                        `}>
                          {file.status === 'pending' && 'Aguardando'}
                          {file.status === 'uploading' && `${file.progress}%`}
                          {file.status === 'success' && 'Concluído'}
                          {file.status === 'error' && 'Erro'}
                        </span>
                      </div>
                    </div>
                    
                    {file.status === 'uploading' && (
                      <div className="mt-2 bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-neon-cyan to-neon-purple h-2 rounded-full transition-all duration-300"
                          style={{ width: `${file.progress}%` }}
                        />
                      </div>
                    )}
                    
                    {file.error && (
                      <p className="mt-1 text-xs text-red-400">{file.error}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}