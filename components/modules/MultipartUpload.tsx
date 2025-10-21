'use client'

import { useState } from 'react'
import { Upload, X, CheckCircle, AlertCircle } from 'lucide-react'

interface MultipartUploadProps {
  file: File
  onComplete: (key: string) => void
  onCancel: () => void
}

export default function MultipartUpload({ file, onComplete, onCancel }: MultipartUploadProps) {
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState<'uploading' | 'completed' | 'error'>('uploading')
  const [error, setError] = useState<string | null>(null)
  const [uploadId, setUploadId] = useState<string | null>(null)
  const [key, setKey] = useState<string | null>(null)

  const CHUNK_SIZE = 50 * 1024 * 1024 // 50MB
  const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod'

  const uploadChunk = async (
    chunk: Blob,
    key: string,
    uploadId: string,
    partNumber: number,
    retries = 3
  ): Promise<{ PartNumber: number; ETag: string }> => {
    for (let i = 0; i < retries; i++) {
      try {
        // Obter presigned URL
        const token = localStorage.getItem('token')
        const partResponse = await fetch(`${API_URL}/multipart/part`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
          },
          body: JSON.stringify({ key, uploadId, partNumber })
        })

        const { uploadUrl } = await partResponse.json()

        // Upload do chunk
        const uploadResponse = await fetch(uploadUrl, {
          method: 'PUT',
          body: chunk
        })

        if (!uploadResponse.ok) throw new Error('Upload failed')

        const etag = uploadResponse.headers.get('ETag')
        if (!etag) throw new Error('No ETag received')

        return { PartNumber: partNumber, ETag: etag.replace(/"/g, '') }
      } catch (err) {
        if (i === retries - 1) throw err
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)))
      }
    }
    throw new Error('Upload failed after retries')
  }

  const startUpload = async () => {
    try {
      const token = localStorage.getItem('token')
      const chunks = Math.ceil(file.size / CHUNK_SIZE)

      console.log(`🚀 Iniciando multipart upload: ${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB, ${chunks} chunks)`)

      // 1. Iniciar multipart
      console.log('📡 Chamando /multipart/init...')
      const initResponse = await fetch(`${API_URL}/multipart/init`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({
          filename: file.name,
          fileSize: file.size
        })
      })

      const { uploadId: newUploadId, key: newKey } = await initResponse.json()
      setUploadId(newUploadId)
      setKey(newKey)

      // 2. Upload chunks em paralelo (4 simultâneos)
      const parts: { PartNumber: number; ETag: string }[] = []
      
      for (let i = 0; i < chunks; i += 4) {
        const batch = []
        
        for (let j = 0; j < 4 && i + j < chunks; j++) {
          const partNumber = i + j + 1
          const start = (i + j) * CHUNK_SIZE
          const end = Math.min(start + CHUNK_SIZE, file.size)
          const chunk = file.slice(start, end)
          
          batch.push(uploadChunk(chunk, newKey, newUploadId, partNumber))
        }

        const batchResults = await Promise.all(batch)
        parts.push(...batchResults)

        // Atualizar progress
        setProgress(Math.round((parts.length / chunks) * 100))
      }

      // 3. Completar upload
      await fetch(`${API_URL}/multipart/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({
          key: newKey,
          uploadId: newUploadId,
          parts: parts.sort((a, b) => a.PartNumber - b.PartNumber)
        })
      })

      setStatus('completed')
      setProgress(100)
      onComplete(newKey)
    } catch (err) {
      setStatus('error')
      setError(err instanceof Error ? err.message : 'Upload failed')
    }
  }

  const handleCancel = async () => {
    if (uploadId && key) {
      try {
        const token = localStorage.getItem('token')
        await fetch(`${API_URL}/multipart/abort`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
          },
          body: JSON.stringify({ key, uploadId })
        })
      } catch (err) {
        console.error('Error aborting upload:', err)
      }
    }
    onCancel()
  }

  // Auto-start upload
  useState(() => {
    startUpload()
  })

  return (
    <div className="glass-card p-6">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {status === 'uploading' && <Upload className="w-5 h-5 text-neon-cyan animate-pulse" />}
          {status === 'completed' && <CheckCircle className="w-5 h-5 text-green-400" />}
          {status === 'error' && <AlertCircle className="w-5 h-5 text-red-400" />}
          
          <div>
            <p className="text-white font-medium truncate max-w-xs">{file.name}</p>
            <p className="text-sm text-gray-400">
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </p>
          </div>
        </div>

        {status === 'uploading' && (
          <button
            onClick={handleCancel}
            className="text-gray-400 hover:text-red-400 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Progress Bar */}
      <div className="mb-2">
        <div className="w-full bg-gray-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              status === 'completed' ? 'bg-green-400' :
              status === 'error' ? 'bg-red-400' :
              'bg-neon-cyan'
            }`}
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Status */}
      <div className="flex justify-between items-center text-sm">
        <span className="text-gray-400">
          {status === 'uploading' && `Enviando... ${progress}%`}
          {status === 'completed' && 'Upload concluído!'}
          {status === 'error' && 'Erro no upload'}
        </span>
        
        {status === 'uploading' && (
          <span className="text-neon-cyan">Multipart Upload</span>
        )}
      </div>

      {error && (
        <p className="text-red-400 text-sm mt-2">{error}</p>
      )}
    </div>
  )
}
