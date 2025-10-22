'use client'

import { useState, useRef, useEffect } from 'react'
import { Upload, X, CheckCircle, AlertCircle, AlertTriangle } from 'lucide-react'
import MultipartUpload from './MultipartUpload'

interface DirectUploadProps {
  onUploadComplete?: (files: any[]) => void
  maxFiles?: number
  maxSize?: number
}

export default function DirectUpload({ 
  onUploadComplete, 
  maxFiles = 100, 
  maxSize = 10240
}: DirectUploadProps) {
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState<{[key: string]: number}>({})
  const [results, setResults] = useState<{[key: string]: 'success' | 'error'}>({})
  const [destination, setDestination] = useState('')
  const [multipartUploading, setMultipartUploading] = useState(false)
  const [users, setUsers] = useState<any[]>([])
  const [currentUser, setCurrentUser] = useState<any>(null)
  const [notification, setNotification] = useState<{type: 'warning' | 'error' | 'info', message: string} | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const folderInputRef = useRef<HTMLInputElement>(null)

  // Fetch users for destination selector
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users')
        const data = await res.json()
        if (data.success) {
          setUsers(data.users)
        }
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    }
    
    const userData = localStorage.getItem('current_user')
    if (userData) {
      setCurrentUser(JSON.parse(userData))
    }
    
    fetchUsers()
  }, [])

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
  }

  const uploadFile = async (file: File) => {
    const startTime = Date.now()
    console.log(`📤 Iniciando upload: ${file.name} (${formatFileSize(file.size)})`)
    
    try {
      // Usar webkitRelativePath se disponível (para pastas)
      let filename = (file as any).webkitRelativePath || file.name
      
      // Adicionar prefixo de destino se selecionado
      if (destination) {
        // Se tem webkitRelativePath, manter estrutura completa da pasta selecionada
        // Ex: C:\Users\dell\Videos\IDM\Anime\video.mp4 → Anime/video.mp4
        // Ex: C:\Users\dell\Videos\Star\Anime\video.mp4 → Star/Anime/video.mp4
        filename = destination + filename
      }
      
      // 1. Obter URL presigned diretamente da AWS API
      console.log(`🔑 Solicitando presigned URL para: ${filename}`)
      const presignedStart = Date.now()
      const token = localStorage.getItem('token')
      const urlResponse = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/presigned', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({
          filename: filename,
          contentType: file.type,
          fileSize: file.size
        })
      })

      const urlData = await urlResponse.json()
      console.log(`⏱️ Presigned URL obtida em ${Date.now() - presignedStart}ms`)
      
      if (!urlData.success) {
        throw new Error(urlData.message || 'Falha ao obter URL')
      }

      // 2. Upload direto para S3 com progress tracking
      console.log(`🚀 Iniciando upload S3...`)
      const uploadStart = Date.now()
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
            const totalTime = Date.now() - startTime
            const uploadTime = Date.now() - uploadStart
            console.log(`✅ Upload concluído: ${file.name} em ${totalTime}ms (S3: ${uploadTime}ms)`)
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
    const normalFiles = files.filter(f => f.size <= 100 * 1024 * 1024)
    if (normalFiles.length === 0) return

    setUploading(true)
    setProgress({})
    setResults({})

    // Upload em paralelo (máximo 3 simultâneos) - apenas arquivos normais
    const batchSize = 3
    for (let i = 0; i < normalFiles.length; i += batchSize) {
      const batch = normalFiles.slice(i, i + batchSize)
      await Promise.all(batch.map(file => uploadFile(file)))
    }

    setUploading(false)
    
    const successCount = Object.values(results).filter(r => r === 'success').length
    if (successCount > 0 && onUploadComplete) {
      setTimeout(() => onUploadComplete(normalFiles.slice(0, successCount)), 100)
    }
  }

  const handleFileSelect = async (selectedFiles: FileList) => {
    const selectStart = Date.now()
    console.log(`📁 Processando ${selectedFiles.length} arquivos selecionados...`)
    
    const allFiles = Array.from(selectedFiles)
    console.log(`⏱️ Array.from concluído em ${Date.now() - selectStart}ms`)
    
    // Avisar se exceder limite
    if (allFiles.length > maxFiles) {
      setNotification({
        type: 'warning',
        message: `⚠️ Limite de ${maxFiles} arquivos excedido! Selecionados: ${allFiles.length}, serão enviados: ${maxFiles}. Após o upload, selecione os próximos ${allFiles.length - maxFiles} arquivos.`
      })
    }
    
    const filterStart = Date.now()
    const validFiles = allFiles.filter(file => {
      if (file.size > maxSize * 1024 * 1024) {
        setNotification({
          type: 'error',
          message: `❌ ${file.name} é muito grande. Máximo: ${maxSize}MB`
        })
        return false
      }
      return true
    }).slice(0, maxFiles)
    console.log(`⏱️ Filtro de arquivos concluído em ${Date.now() - filterStart}ms`)

    // Separar arquivos por tamanho
    const separateStart = Date.now()
    const normalFiles = validFiles.filter(f => f.size <= 100 * 1024 * 1024)
    const multipartFiles = validFiles.filter(f => f.size > 100 * 1024 * 1024)
    console.log(`⏱️ Separação concluída em ${Date.now() - separateStart}ms - Normal: ${normalFiles.length}, Multipart: ${multipartFiles.length}`)
    
    // Skip check para uploads rápidos (apenas 1 arquivo pequeno)
    let finalNormalFiles = normalFiles
    if (normalFiles.length > 1) {
      try {
        console.log(`🔍 Verificando ${normalFiles.length} arquivos normais existentes...`)
        const checkStart = Date.now()
        const filenames = normalFiles.map(f => (f as any).webkitRelativePath || f.name)
        const checkResponse = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filenames })
        })
        
        const checkData = await checkResponse.json()
        console.log(`⏱️ Check concluído em ${Date.now() - checkStart}ms`)
        
        if (checkData.success) {
          const existingFiles = checkData.files.filter((f: any) => f.exists)
          finalNormalFiles = normalFiles.filter((file, index) => !checkData.files[index].exists)
          
          if (existingFiles.length > 0) {
            const existingNames = existingFiles.map((f: any) => f.original).slice(0, 5).join(', ')
            const more = existingFiles.length > 5 ? ` e mais ${existingFiles.length - 5}` : ''
            setNotification({
              type: 'warning',
              message: `⚠️ ${existingFiles.length} arquivo(s) já existe(m): ${existingNames}${more}. Serão enviados ${finalNormalFiles.length} novo(s).`
            })
          }
        }
      } catch (error) {
        console.error('Error checking files:', error)
      }
    } else if (normalFiles.length === 1) {
      console.log(`⚡ Skip check - apenas 1 arquivo pequeno`)
    }
    
    // Combinar arquivos finais
    const combineStart = Date.now()
    setFiles([...finalNormalFiles, ...multipartFiles])
    console.log(`⏱️ setFiles concluído em ${Date.now() - combineStart}ms`)
    console.log(`✅ handleFileSelect TOTAL: ${Date.now() - selectStart}ms`)

    setProgress({})
    setResults({})
  }

  return (
    <div className="space-y-6">
      {/* Notification Toast */}
      {notification && (
        <div className={`glass-card p-4 border-l-4 ${
          notification.type === 'error' ? 'border-red-500 bg-red-500/10' :
          notification.type === 'warning' ? 'border-yellow-500 bg-yellow-500/10' :
          'border-blue-500 bg-blue-500/10'
        }`}>
          <div className="flex items-start gap-3">
            <AlertTriangle className={`w-5 h-5 flex-shrink-0 ${
              notification.type === 'error' ? 'text-red-400' :
              notification.type === 'warning' ? 'text-yellow-400' :
              'text-blue-400'
            }`} />
            <div className="flex-1">
              <p className="text-sm text-white">{notification.message}</p>
            </div>
            <button
              onClick={() => setNotification(null)}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Drop Zone */}
      <div
        onDrop={(e) => {
          e.preventDefault()
          if (e.dataTransfer.files) handleFileSelect(e.dataTransfer.files)
        }}
        onDragOver={(e) => e.preventDefault()}
        className="glass-card p-8 text-center border-2 border-dashed border-gray-600 hover:border-neon-cyan transition-colors"
      >
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        <h3 className="text-xl font-semibold text-white mb-2">
          🚀 Upload Direto AWS (Sem Proxy)
        </h3>
        <p className="text-gray-400 mb-4">
          Arraste arquivos aqui ou clique para selecionar
        </p>
        
        {/* Destination Selector - Only for Admin */}
        {(currentUser?.user_id === 'user_admin' || currentUser?.user_id === 'admin' || currentUser?.id === 'user_admin' || currentUser?.role === 'admin') && (
          <div className="mb-4">
            <label className="block text-sm text-gray-400 mb-2">📁 Pasta de Destino:</label>
            <select
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              className="px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:border-neon-cyan focus:outline-none"
            >
              <option value="">Raiz do sistema</option>
              <option value="users/user_admin/">📁 Minha pasta (Admin)</option>
              {users.filter(user => user.user_id !== 'user_admin').map(user => (
                <option key={user.user_id} value={`${user.s3_prefix}`}>
                  📁 {user.name} ({user.user_id})
                </option>
              ))}
            </select>
          </div>
        )}
        
        <div className="flex gap-4 justify-center mt-4">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn-secondary px-4 py-2 text-sm"
          >
            📄 Selecionar Arquivos
          </button>
          <button
            onClick={() => folderInputRef.current?.click()}
            className="btn-secondary px-4 py-2 text-sm"
          >
            📁 Selecionar Pasta
          </button>
        </div>
        <p className="text-sm text-gray-500 mt-2">
          Máximo: {maxFiles} arquivos, {maxSize}MB cada
          {destination && (
            <span className="block text-neon-cyan mt-1">
              📍 Destino: {destination || 'raiz'}
            </span>
          )}
        </p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        onChange={(e) => {
          e.preventDefault()
          if (e.target.files) handleFileSelect(e.target.files)
        }}
        className="hidden"
      />
      
      <input
        ref={folderInputRef}
        type="file"
        {...({ webkitdirectory: '' } as any)}
        multiple
        onChange={(e) => {
          e.preventDefault()
          if (e.target.files) handleFileSelect(e.target.files)
        }}
        className="hidden"
      />

      {/* Botões Globais */}
      {files.length > 0 && (
        <div className="glass-card p-6">
          <div className="flex justify-between items-center">
            <div>
              <h4 className="text-lg font-semibold text-white">
                📦 {files.length} arquivo(s) selecionado(s)
              </h4>
              <p className="text-sm text-gray-400">
                {files.filter(f => f.size > 100 * 1024 * 1024).length} grande(s) • {files.filter(f => f.size <= 100 * 1024 * 1024).length} pequeno(s)
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => {
                  setFiles([])
                  setMultipartUploading(false)
                  setUploading(false)
                }}
                className="btn-secondary px-4 py-2 text-sm"
                disabled={uploading || multipartUploading}
              >
                Limpar Todos
              </button>
              <button
                onClick={() => {
                  setMultipartUploading(true)
                  handleUpload()
                }}
                className="btn-neon px-6 py-2"
                disabled={uploading || multipartUploading}
              >
                {(uploading || multipartUploading) ? '📤 Enviando...' : '📤 Upload Todos'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Multipart Uploads (>100MB) */}
      {files.filter(f => f.size > 100 * 1024 * 1024).length > 0 && (
        <div className="glass-card p-6">
          <div className="mb-4">
            <h4 className="text-lg font-semibold text-white">
              ⚡ Arquivos Grandes ({files.filter(f => f.size > 100 * 1024 * 1024).length})
            </h4>
          </div>
          <p className="text-sm text-gray-400 mb-4">
            Arquivos maiores que 100MB usam upload paralelo em chunks de 50MB
          </p>
          <div className="space-y-4">
            {files.filter(f => f.size > 100 * 1024 * 1024).map((file, i) => (
              <MultipartUpload
                key={i}
                file={file}
                destination={destination}
                autoStart={multipartUploading}
                onComplete={(key) => {
                  setFiles(prev => prev.filter(f => f !== file))
                  setResults(prev => ({ ...prev, [file.name]: 'success' }))
                  if (onUploadComplete) {
                    setTimeout(() => onUploadComplete([file]), 100)
                  }
                  if (files.filter(f => f.size > 100 * 1024 * 1024).length === 1) {
                    setMultipartUploading(false)
                  }
                }}
                onCancel={() => {
                  setFiles(prev => prev.filter(f => f !== file))
                  setMultipartUploading(false)
                }}
              />
            ))}
          </div>
        </div>
      )}

      {/* File List (<=100MB) */}
      {files.filter(f => f.size <= 100 * 1024 * 1024).length > 0 && (
        <div className="glass-card p-6">
          <div className="mb-4">
            <h4 className="text-lg font-semibold text-white">
              📄 Arquivos Pequenos ({files.filter(f => f.size <= 100 * 1024 * 1024).length})
            </h4>
          </div>

          <div className="space-y-3">
            {files.filter(f => f.size <= 100 * 1024 * 1024).map((file, index) => (
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