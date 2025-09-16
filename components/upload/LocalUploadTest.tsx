'use client'

import { useState } from 'react'
import { Upload, CheckCircle, AlertCircle } from 'lucide-react'

export default function LocalUploadTest() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle')
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState('')

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      setStatus('idle')
      setError('')
    }
  }

  const uploadFile = async () => {
    if (!file) return

    setStatus('uploading')
    setProgress(0)

    try {
      // 1. Obter URL presigned
      const urlResponse = await fetch('/api/upload/presigned-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          contentType: file.type,
          fileSize: file.size
        })
      })

      const urlData = await urlResponse.json()
      
      if (!urlData.success) {
        throw new Error(urlData.error || 'Falha ao obter URL')
      }

      // 2. Upload direto para S3
      const xhr = new XMLHttpRequest()

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          setProgress(Math.round((e.loaded / e.total) * 100))
        }
      })

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          setStatus('success')
        } else {
          setStatus('error')
          setError(`HTTP ${xhr.status}: ${xhr.statusText}`)
        }
      })

      xhr.addEventListener('error', () => {
        setStatus('error')
        setError('Erro de rede')
      })

      xhr.open('PUT', urlData.uploadUrl)
      xhr.setRequestHeader('Content-Type', file.type)
      xhr.send(file)

    } catch (err) {
      setStatus('error')
      setError(err instanceof Error ? err.message : 'Erro desconhecido')
    }
  }

  return (
    <div className="glass-card p-6 max-w-md mx-auto">
      <h3 className="text-lg font-semibold text-white mb-4">
        🧪 Teste Upload Local
      </h3>

      <input
        type="file"
        onChange={handleFileSelect}
        className="mb-4 text-white"
        accept="*/*"
      />

      {file && (
        <div className="mb-4 text-sm text-gray-300">
          <p>📄 {file.name}</p>
          <p>📊 {Math.round(file.size / 1024)}KB</p>
        </div>
      )}

      <button
        onClick={uploadFile}
        disabled={!file || status === 'uploading'}
        className="btn-neon w-full mb-4"
      >
        {status === 'uploading' ? `Enviando ${progress}%` : 'Enviar'}
      </button>

      {status === 'uploading' && (
        <div className="mb-4 bg-gray-700 rounded-full h-2">
          <div 
            className="bg-neon-cyan h-2 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {status === 'success' && (
        <div className="flex items-center gap-2 text-green-400">
          <CheckCircle className="w-4 h-4" />
          Upload realizado com sucesso!
        </div>
      )}

      {status === 'error' && (
        <div className="flex items-center gap-2 text-red-400">
          <AlertCircle className="w-4 h-4" />
          {error}
        </div>
      )}
    </div>
  )
}