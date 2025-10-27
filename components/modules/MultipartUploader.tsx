'use client'

import { useState } from 'react'
import { CheckCircle, AlertCircle } from 'lucide-react'

const CHUNK_SIZE = 10 * 1024 * 1024 // 10MB
const API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/multipart'

interface MultipartUploaderProps {
  file: File
  destination?: string
  onComplete: () => void
  onError?: (error: string) => void
}

export default function MultipartUploader({ file, destination = '', onComplete, onError }: MultipartUploaderProps) {
  const [progress, setProgress] = useState(0)
  const [uploading, setUploading] = useState(false)
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle')
  const [currentPart, setCurrentPart] = useState(0)
  const [totalParts, setTotalParts] = useState(0)
  const [uploadId, setUploadId] = useState<string | null>(null)
  const [uploadKey, setUploadKey] = useState<string | null>(null)

  const uploadMultipart = async () => {
    setUploading(true)
    setStatus('uploading')
    
    try {
      const filename = destination + file.name
      const chunks = Math.ceil(file.size / CHUNK_SIZE)
      setTotalParts(chunks)
      
      // 1. Iniciar multipart
      const initRes = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'initiate',
          filename,
          contentType: file.type || 'application/octet-stream'
        })
      })
      
      const initData = await initRes.json()
      if (!initData.success) throw new Error('Falha ao iniciar upload')
      
      const uploadId = initData.uploadId
      setUploadId(uploadId)
      setUploadKey(filename)
      const parts: {PartNumber: number, ETag: string}[] = []
      
      // 2. Upload paralelo (3 chunks por vez)
      for (let i = 0; i < chunks; i += 3) {
        const batch = []
        
        for (let j = 0; j < 3 && (i + j) < chunks; j++) {
          const partNumber = i + j + 1
          batch.push(uploadPart(file, uploadId, filename, partNumber))
        }
        
        const batchResults = await Promise.all(batch)
        parts.push(...batchResults)
        
        setCurrentPart(parts.length)
        setProgress(Math.round((parts.length / chunks) * 100))
      }
      
      // 3. Completar upload
      const completeRes = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'complete',
          uploadId,
          key: filename,
          parts: parts.sort((a, b) => a.PartNumber - b.PartNumber)
        })
      })
      
      const completeData = await completeRes.json()
      if (!completeData.success) throw new Error('Falha ao completar upload')
      
      setStatus('success')
      setUploadId(null)
      setUploadKey(null)
      onComplete()
      
    } catch (error) {
      console.error('Multipart upload failed:', error)
      setStatus('error')
      onError?.(error instanceof Error ? error.message : 'Erro desconhecido')
    } finally {
      setUploading(false)
    }
  }

  const abortUpload = async () => {
    if (!uploadId || !uploadKey) return
    
    try {
      const token = localStorage.getItem('token')
      await fetch(`${API_URL}/abort`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          uploadId,
          key: uploadKey
        })
      })
      
      setStatus('idle')
      setProgress(0)
      setCurrentPart(0)
      setUploadId(null)
      setUploadKey(null)
      onError?.('Upload cancelado pelo usuário')
    } catch (error) {
      console.error('Erro ao abortar upload:', error)
    }
  }

  const uploadPart = async (file: File, uploadId: string, key: string, partNumber: number): Promise<{PartNumber: number, ETag: string}> => {
    const start = (partNumber - 1) * CHUNK_SIZE
    const end = Math.min(start + CHUNK_SIZE, file.size)
    const chunk = file.slice(start, end)
    
    // Retry até 3 vezes
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        // Obter presigned URL
        const urlRes = await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: 'get-url',
            uploadId,
            key,
            partNumber
          })
        })
        
        const urlData = await urlRes.json()
        if (!urlData.success) throw new Error('Falha ao obter URL')
        
        // Upload chunk
        const uploadRes = await fetch(urlData.presignedUrl, {
          method: 'PUT',
          body: chunk
        })
        
        if (!uploadRes.ok) throw new Error(`Upload falhou: ${uploadRes.status}`)
        
        const etag = uploadRes.headers.get('ETag')?.replace(/"/g, '')
        if (!etag) throw new Error('ETag não retornado')
        
        return { PartNumber: partNumber, ETag: etag }
        
      } catch (error) {
        if (attempt === 2) throw error
        await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)))
      }
    }
    
    throw new Error(`Falha após 3 tentativas: parte ${partNumber}`)
  }

  return (
    <div className="glass-card p-6 mb-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-white truncate">{file.name}</h3>
          <p className="text-sm text-gray-400">
            {(file.size / 1024 / 1024 / 1024).toFixed(2)} GB
            {totalParts > 0 && ` • ${currentPart}/${totalParts} partes`}
          </p>
        </div>
        
        {status === 'success' && <CheckCircle className="w-6 h-6 text-green-400 flex-shrink-0" />}
        {status === 'error' && <AlertCircle className="w-6 h-6 text-red-400 flex-shrink-0" />}
      </div>
      
      {status === 'idle' && (
        <button onClick={uploadMultipart} className="btn-neon w-full">
          🚀 Iniciar Upload Multipart
        </button>
      )}
      
      {status === 'uploading' && (
        <div>
          <div className="w-full bg-gray-700 rounded-full h-4 mb-2">
            <div 
              className="bg-gradient-to-r from-neon-cyan to-neon-purple h-4 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-center text-neon-cyan text-sm mb-3">
            {progress}% • Enviando parte {currentPart}/{totalParts}
          </p>
          <button 
            onClick={abortUpload}
            className="btn-secondary w-full"
          >
            ❌ Cancelar Upload
          </button>
        </div>
      )}
      
      {status === 'success' && (
        <p className="text-green-400 text-center">✅ Upload concluído com sucesso!</p>
      )}
      
      {status === 'error' && (
        <div className="text-center">
          <p className="text-red-400 mb-2">❌ Erro no upload</p>
          <button onClick={uploadMultipart} className="btn-secondary">
            🔄 Tentar Novamente
          </button>
        </div>
      )}
    </div>
  )
}
