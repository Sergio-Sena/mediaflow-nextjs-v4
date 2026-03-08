'use client'

import { useState, useRef } from 'react'
import { Upload, X, CheckCircle, AlertCircle, File, Video, Image } from 'lucide-react'
import { UploadFactory } from '../upload/strategies/UploadFactory'

interface UploadFile {
  id: string
  file: File
  progress: number
  status: 'pending' | 'uploading' | 'success' | 'error'
  error?: string
  url?: string
}

interface UniversalUploadProps {
  onUploadComplete?: (files: UploadFile[]) => void
  maxFiles?: number
  maxSize?: number
  accept?: string
}

export default function UniversalUpload({ 
  onUploadComplete, 
  maxFiles = 50, 
  maxSize = 5120,
  accept = 'video/*,image/*,application/pdf'
}: UniversalUploadProps) {
  const [files, setFiles] = useState<UploadFile[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

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

  const addFiles = (newFiles: FileList) => {
    const validFiles: UploadFile[] = []
    
    Array.from(newFiles).forEach(file => {
      if (files.length + validFiles.length >= maxFiles) return
      
      const error = file.size > maxSize * 1024 * 1024 ? `Arquivo muito grande. Máximo: ${maxSize}MB` : null
      
      validFiles.push({
        id: Math.random().toString(36).substr(2, 9),
        file,
        progress: 0,
        status: error ? 'error' : 'pending',
        error: error || undefined
      })
    })
    
    setFiles(prev => [...prev, ...validFiles])
  }

  const uploadFile = async (uploadFile: UploadFile) => {
    try {
      setFiles(prev => prev.map(f => 
        f.id === uploadFile.id ? { ...f, status: 'uploading', progress: 0 } : f
      ))

      // Obter URL presigned
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
      const urlResponse = await fetch('/api/upload/presigned', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          filename: uploadFile.file.name,
          contentType: uploadFile.file.type,
          fileSize: uploadFile.file.size
        })
      })

      const urlData = await urlResponse.json()
      
      if (!urlData.success) {
        throw new Error(urlData.message || 'Falha ao obter URL')
      }

      // Upload para S3 com progresso
      await new Promise<void>((resolve, reject) => {
        const xhr = new XMLHttpRequest()

        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const percentage = Math.round((e.loaded / e.total) * 100)
            setFiles(prev => prev.map(f => 
              f.id === uploadFile.id ? { ...f, progress: percentage } : f
            ))
          }
        })

        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve()
          } else {
            reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`))
          }
        })

        xhr.addEventListener('error', () => reject(new Error('Erro de rede')))

        xhr.open('PUT', urlData.uploadUrl)
        xhr.setRequestHeader('Content-Type', uploadFile.file.type)
        xhr.send(uploadFile.file)
      })

      setFiles(prev => prev.map(f => 
        f.id === uploadFile.id 
          ? { ...f, status: 'success', progress: 100, url: `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${urlData.key}` }
          : f
      ))
      
      // Notificar conclusão
      setTimeout(() => {
        onUploadComplete?.([{ ...uploadFile, status: 'success', progress: 100 }])
      }, 500)

    } catch (error) {
      setFiles(prev => prev.map(f => 
        f.id === uploadFile.id 
          ? { ...f, status: 'error', error: error instanceof Error ? error.message : 'Erro no upload' }
          : f
      ))
    }
  }

  const uploadAll = async () => {
    const pendingFiles = files.filter(f => f.status === 'pending')
    
    // Upload em paralelo (máximo 3 simultâneos)
    const batchSize = 3
    for (let i = 0; i < pendingFiles.length; i += batchSize) {
      const batch = pendingFiles.slice(i, i + batchSize)
      await Promise.all(batch.map(file => uploadFile(file)))
    }
    
    // Notificar conclusão em lote
    setTimeout(() => {
      const completedFiles = files.filter(f => f.status === 'success')
      if (completedFiles.length > 0) {
        onUploadComplete?.(completedFiles)
      }
    }, 1000)
  }

  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id))
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    addFiles(e.dataTransfer.files)
  }

  return (
    <div className="space-y-6">
      {/* Drop Zone */}
      <div
        onDrop={handleDrop}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
        onDragLeave={(e) => { e.preventDefault(); setIsDragging(false) }}
        className={`glass-card p-6 text-center border-2 border-dashed transition-all duration-300 ${
          isDragging 
            ? 'border-neon-cyan bg-neon-cyan/5 scale-105' 
            : 'border-gray-600 hover:border-neon-cyan/50 hover:bg-neon-cyan/5'
        }`}
      >
        <Upload className={`w-10 h-10 mx-auto mb-3 transition-colors ${
          isDragging ? 'text-neon-cyan' : 'text-gray-400'
        }`} />
        
        <h3 className="text-lg font-semibold text-white mb-2">
          {isDragging ? 'Solte os arquivos aqui' : '🚀 Upload Universal'}
        </h3>
        
        <p className="text-gray-400 text-sm mb-4">
          Arraste arquivos aqui ou clique para selecionar
        </p>

        <button
          onClick={() => fileInputRef.current?.click()}
          className="btn-neon px-6 py-2"
        >
          📁 Selecionar Arquivos
        </button>
      </div>
      
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept={accept}
        onChange={(e) => e.target.files && addFiles(e.target.files)}
        className="hidden"
      />

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="text-lg font-semibold text-white">
              Arquivos ({files.length})
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
                      <h5 className="font-medium text-white truncate">
                        {file.file.name}
                      </h5>
                      
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
