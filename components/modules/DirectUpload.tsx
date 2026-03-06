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

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch('/api/users/list', {
          headers: {
            'Authorization': token ? `Bearer ${token}` : ''
          }
        })
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

  const uploadFile = async (file: File, retryCount = 0) => {
    try {
      let filename = (file as any).webkitRelativePath || file.name
      
      // Auto-adicionar pasta do usuário se não for admin
      if (!destination && currentUser && currentUser.role !== 'admin') {
        const userPrefix = currentUser.s3_prefix || `users/${currentUser.user_id}/`
        filename = userPrefix + filename
      } else if (destination) {
        filename = destination + filename
      }
      
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('Token de autenticação não encontrado')
      }
      
      const { getApiUrl } = await import('@/lib/aws-config')
      const apiUrl = getApiUrl('UPLOAD')
      
      const urlResponse = await fetch('/api/upload/presigned', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          filename: filename,
          contentType: file.type,
          fileSize: file.size
        })
      })

      const urlData = await urlResponse.json()
      
      if (!urlResponse.ok || !urlData.success) {
        throw new Error(urlData.message || 'Falha ao obter URL')
      }

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
            // Delay mínimo de 500ms para mostrar 100%
            setTimeout(() => {
              setResults(prev => ({ ...prev, [file.name]: 'success' }))
              setProgress(prev => ({ ...prev, [file.name]: 100 }))
            }, 500)
            resolve()
          } else if (xhr.status === 503 && retryCount < 3) {
            const delay = Math.pow(2, retryCount) * 1000
            setTimeout(() => {
              uploadFile(file, retryCount + 1).then(resolve).catch(reject)
            }, delay)
          } else {
            setResults(prev => ({ ...prev, [file.name]: 'error' }))
            reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`))
          }
        })

        xhr.addEventListener('error', () => {
          if (retryCount < 3) {
            const delay = Math.pow(2, retryCount) * 1000
            setTimeout(() => {
              uploadFile(file, retryCount + 1).then(resolve).catch(reject)
            }, delay)
          } else {
            setResults(prev => ({ ...prev, [file.name]: 'error' }))
            reject(new Error('Erro de rede'))
          }
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

    // Inicializar progresso em 0% para todos os arquivos
    const initialProgress: {[key: string]: number} = {}
    normalFiles.forEach(f => initialProgress[f.name] = 0)
    setProgress(initialProgress)

    try {
      const batchSize = 2
      for (let i = 0; i < normalFiles.length; i += batchSize) {
        const batch = normalFiles.slice(i, i + batchSize)
        await Promise.all(batch.map(file => uploadFile(file)))
        if (i + batchSize < normalFiles.length) {
          await new Promise(resolve => setTimeout(resolve, 500))
        }
      }
      
      const successCount = Object.values(results).filter(r => r === 'success').length
      if (successCount > 0 && onUploadComplete) {
        setTimeout(() => onUploadComplete(normalFiles.slice(0, successCount)), 100)
      }
    } finally {
      setUploading(false)
    }
  }

  const convertTsToMp4 = async (file: File): Promise<File> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch('/api/convert-ts', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) throw new Error('Conversão falhou')
    
    const blob = await response.blob()
    return new File([blob], file.name.replace('.ts', '.mp4'), { type: 'video/mp4' })
  }

  const handleFileSelect = async (selectedFiles: FileList) => {
    let allFiles = Array.from(selectedFiles)
    
    const tsFiles = allFiles.filter(f => f.name.endsWith('.ts'))
    if (tsFiles.length > 0) {
      setNotification({
        type: 'info',
        message: `🔄 Convertendo ${tsFiles.length} arquivo(s) .ts para .mp4...`
      })
      
      try {
        const convertedFiles = await Promise.all(
          tsFiles.map(f => convertTsToMp4(f))
        )
        
        allFiles = allFiles.filter(f => !f.name.endsWith('.ts')).concat(convertedFiles)
        
        setNotification({
          type: 'info',
          message: `✅ ${tsFiles.length} arquivo(s) convertido(s) com sucesso!`
        })
      } catch (error) {
        console.error('Erro na conversão:', error)
        setNotification({
          type: 'error',
          message: `❌ Erro ao converter arquivos .ts`
        })
        return
      }
    }
    
    if (allFiles.length > maxFiles) {
      setNotification({
        type: 'warning',
        message: `⚠️ Limite de ${maxFiles} arquivos excedido! Selecionados: ${allFiles.length}, serão enviados: ${maxFiles}.`
      })
    }
    
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

    const normalFiles = validFiles.filter(f => f.size <= 100 * 1024 * 1024)
    const multipartFiles = validFiles.filter(f => f.size > 100 * 1024 * 1024)
    
    let finalNormalFiles = normalFiles
    if (normalFiles.length > 1) {
      try {
        const filenames = normalFiles.map(f => (f as any).webkitRelativePath || f.name)
        const checkResponse = await fetch('/api/upload/check-exists', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filenames })
        })
        
        const checkData = await checkResponse.json()
        
        if (checkData.success) {
          const existingFiles = checkData.files.filter((f: any) => f.exists)
          finalNormalFiles = normalFiles.filter((file, index) => !checkData.files[index].exists)
          
          if (existingFiles.length > 0) {
            const existingNames = existingFiles.map((f: any) => f.original).slice(0, 5).join(', ')
            const more = existingFiles.length > 5 ? ` e mais ${existingFiles.length - 5}` : ''
            setNotification({
              type: 'warning',
              message: `⚠️ ${existingFiles.length} arquivo(s) já existe(m): ${existingNames}${more}.`
            })
          }
        }
      } catch (error) {
        console.error('Error checking files:', error)
      }
    }
    
    setFiles([...finalNormalFiles, ...multipartFiles])
    setProgress({})
    setResults({})
  }

  return (
    <div className="space-y-6">
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
                  setProgress({})
                  setResults({})
                  setMultipartUploading(false)
                  setUploading(false)
                }}
                className="btn-secondary px-4 py-2 text-sm"
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
                    <>
                      <div className="w-full bg-gray-700 rounded-full h-2 mb-1">
                        <div 
                          className="bg-gradient-to-r from-neon-cyan to-neon-purple h-2 rounded-full transition-all duration-300"
                          style={{ width: `${progress[file.name]}%` }}
                        />
                      </div>
                      <div className="text-xs text-neon-cyan text-right">
                        {progress[file.name]}%
                      </div>
                    </>
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
