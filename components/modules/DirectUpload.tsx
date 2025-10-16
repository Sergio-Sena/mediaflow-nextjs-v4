'use client'

import { useState, useRef } from 'react'
import { Upload, X, CheckCircle, AlertCircle } from 'lucide-react'

interface DirectUploadProps {
  onUploadComplete?: (files: any[]) => void
  maxFiles?: number
  maxSize?: number
}

export default function DirectUpload({ 
  onUploadComplete, 
  maxFiles = 50, 
  maxSize = 5120
}: DirectUploadProps) {
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState<{[key: string]: number}>({})
  const [results, setResults] = useState<{[key: string]: 'success' | 'error'}>({})
  const fileInputRef = useRef<HTMLInputElement>(null)
  const folderInputRef = useRef<HTMLInputElement>(null)

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
  }

  const uploadFile = async (file: File) => {
    try {
      // Usar webkitRelativePath se disponível (para pastas)
      const filename = (file as any).webkitRelativePath || file.name
      
      // 1. Obter URL presigned diretamente da AWS API
      const urlResponse = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/presigned', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: filename,
          contentType: file.type,
          fileSize: file.size
        })
      })

      const urlData = await urlResponse.json()
      
      if (!urlData.success) {
        throw new Error(urlData.message || 'Falha ao obter URL')
      }

      // 2. Upload direto para S3 com progress tracking
      await new Promise<void>((resolve, reject) => {
        const xhr = new XMLHttpRequest()

        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const percentage = Math.round((e.loaded / e.total) * 100)
            setProgress(prev => ({ ...prev, [file.name]: percentage }))
          }
        })

        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            setResults(prev => ({ ...prev, [file.name]: 'success' }))
            setProgress(prev => ({ ...prev, [file.name]: 100 }))
            resolve()
          } else {
            setResults(prev => ({ ...prev, [file.name]: 'error' }))
            reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`))
          }
        })

        xhr.addEventListener('error', () => {
          setResults(prev => ({ ...prev, [file.name]: 'error' }))
          reject(new Error('Erro de rede'))
        })

        xhr.open('PUT', urlData.uploadUrl)
        xhr.setRequestHeader('Content-Type', file.type)
        xhr.send(file)
      })

    } catch (error) {
      console.error(`Upload failed for ${file.name}:`, error)
      setResults(prev => ({ ...prev, [file.name]: 'error' }))
    }
  }

  const handleUpload = async () => {
    if (files.length === 0) return

    setUploading(true)
    setProgress({})
    setResults({})

    // Upload em paralelo (máximo 3 simultâneos)
    const batchSize = 3
    for (let i = 0; i < files.length; i += batchSize) {
      const batch = files.slice(i, i + batchSize)
      await Promise.all(batch.map(file => uploadFile(file)))
    }

    setUploading(false)
    
    const successCount = Object.values(results).filter(r => r === 'success').length
    if (successCount > 0) {
      onUploadComplete?.(files.slice(0, successCount))
    }
  }

  const handleFileSelect = async (selectedFiles: FileList) => {
    const validFiles = Array.from(selectedFiles).filter(file => {
      if (file.size > maxSize * 1024 * 1024) {
        alert(`${file.name} é muito grande. Máximo: ${maxSize}MB`)
        return false
      }
      return true
    }).slice(0, maxFiles)

    // Check which files already exist
    try {
      const filenames = validFiles.map(f => (f as any).webkitRelativePath || f.name)
      const checkResponse = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filenames })
      })
      
      const checkData = await checkResponse.json()
      
      if (checkData.success) {
        const existingFiles = checkData.files.filter((f: any) => f.exists)
        const newFiles = validFiles.filter((file, index) => !checkData.files[index].exists)
        
        if (existingFiles.length > 0) {
          const existingNames = existingFiles.map((f: any) => `• ${f.original}`).join('\n')
          const message = `⚠️ ARQUIVOS JÁ EXISTENTES\n\n${existingFiles.length} arquivo(s) já existe(m) no destino e foram removidos da lista:\n\n${existingNames}\n\n✅ ${newFiles.length} arquivo(s) novo(s) serão enviados.`
          alert(message)
        }
        
        setFiles(newFiles)
      } else {
        setFiles(validFiles)
      }
    } catch (error) {
      console.error('Error checking files:', error)
      setFiles(validFiles)
    }

    setProgress({})
    setResults({})
  }

  return (
    <div className="space-y-6">
      {/* Drop Zone */}
      <div
        onClick={() => fileInputRef.current?.click()}
        onDrop={(e) => {
          e.preventDefault()
          if (e.dataTransfer.files) handleFileSelect(e.dataTransfer.files)
        }}
        onDragOver={(e) => e.preventDefault()}
        className="glass-card p-8 text-center border-2 border-dashed border-gray-600 hover:border-neon-cyan cursor-pointer transition-colors"
      >
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        <h3 className="text-xl font-semibold text-white mb-2">
          🚀 Upload Direto AWS (Sem Proxy)
        </h3>
        <p className="text-gray-400 mb-4">
          Arraste arquivos aqui ou clique para selecionar
        </p>
        <div className="flex gap-4 justify-center mt-4">
          <button
            onClick={(e) => {
              e.stopPropagation()
              fileInputRef.current?.click()
            }}
            className="btn-secondary px-4 py-2 text-sm"
          >
            📄 Selecionar Arquivos
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation()
              folderInputRef.current?.click()
            }}
            className="btn-secondary px-4 py-2 text-sm"
          >
            📁 Selecionar Pasta
          </button>
        </div>
        <p className="text-sm text-gray-500 mt-2">
          Máximo: {maxFiles} arquivos, {maxSize}MB cada
        </p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        onChange={(e) => e.target.files && handleFileSelect(e.target.files)}
        className="hidden"
      />
      
      <input
        ref={folderInputRef}
        type="file"
        {...({ webkitdirectory: '' } as any)}
        multiple
        onChange={(e) => e.target.files && handleFileSelect(e.target.files)}
        className="hidden"
      />

      {/* File List */}
      {files.length > 0 && (
        <div className="glass-card p-6">
          <div className="flex justify-between items-center mb-4">
            <h4 className="text-lg font-semibold text-white">
              Arquivos ({files.length})
            </h4>
            <div className="flex gap-2">
              <button
                onClick={() => setFiles([])}
                className="btn-secondary px-4 py-2 text-sm"
                disabled={uploading}
              >
                Limpar
              </button>
              <button
                onClick={handleUpload}
                className="btn-neon px-6 py-2"
                disabled={uploading || files.length === 0}
              >
                {uploading ? '📤 Enviando...' : '📤 Upload Todos'}
              </button>
            </div>
          </div>

          <div className="space-y-3">
            {files.map((file, index) => (
              <div key={index} className="flex items-center gap-4 p-3 bg-gray-800/50 rounded-lg">
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-center mb-1 gap-2">
                    <span className="font-medium text-white truncate flex-1 min-w-0" title={(file as any).webkitRelativePath || file.name}>
                      {(file as any).webkitRelativePath || file.name}
                    </span>
                    <span className="text-sm text-gray-400 flex-shrink-0">
                      {formatFileSize(file.size)}
                    </span>
                  </div>
                  
                  {progress[file.name] !== undefined && results[file.name] !== 'success' && results[file.name] !== 'error' && (
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-neon-cyan to-neon-purple h-2 rounded-full transition-all duration-300"
                        style={{ width: `${progress[file.name]}%` }}
                      />
                    </div>
                  )}
                </div>

                <div className="flex items-center">
                  {results[file.name] === 'success' && (
                    <CheckCircle className="w-5 h-5 text-green-400" />
                  )}
                  {results[file.name] === 'error' && (
                    <AlertCircle className="w-5 h-5 text-red-400" />
                  )}
                  {!results[file.name] && progress[file.name] !== undefined && progress[file.name] < 100 && (
                    <span className="text-sm text-neon-cyan">
                      {progress[file.name]}%
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}