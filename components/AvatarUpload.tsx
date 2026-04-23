'use client'

import { useState, useRef, useEffect } from 'react'
import { getApiUrl } from '@/lib/aws-config'
import { getUserFromToken } from '@/lib/auth-utils'

interface AvatarUploadProps {
  currentAvatar?: string
  onAvatarUpdate?: (avatarUrl: string) => void
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export default function AvatarUpload({ 
  currentAvatar, 
  onAvatarUpdate,
  size = 'md',
  className = ''
}: AvatarUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [preview, setPreview] = useState<string | null>(currentAvatar || null)
  const [imageError, setImageError] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (currentAvatar) setPreview(currentAvatar)
  }, [currentAvatar])

  const sizeClasses = {
    sm: 'w-12 h-12',
    md: 'w-20 h-20', 
    lg: 'w-32 h-32'
  }

  const handleFileSelect = async (file: File) => {
    if (!file.type.startsWith('image/')) return

    const token = localStorage.getItem('token')
    const user = getUserFromToken()

    if (!token || !user) {
      alert('Sessão expirada. Faça login novamente.')
      return
    }

    // Preview imediato
    const reader = new FileReader()
    reader.onload = (e) => setPreview(e.target?.result as string)
    reader.readAsDataURL(file)

    setUploading(true)
    try {
      const ext = file.name.split('.').pop()

      // 1. Obter presigned URL
      const presignedRes = await fetch(getApiUrl('AVATAR_PRESIGNED'), {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ userId: user.user_id, fileExt: ext })
      })
      
      const presignedData = await presignedRes.json()
      if (!presignedData.success) throw new Error('Falha ao obter URL de upload')
      
      // 2. Upload para S3
      const cleanUrl = presignedData.presignedUrl.replace(/&amp;/g, '&')
      await fetch(cleanUrl, {
        method: 'PUT',
        body: file,
        headers: { 'Content-Type': file.type }
      })
      
      // 3. Atualizar DynamoDB
      await fetch(getApiUrl('UPDATE_USER'), {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          user_id: user.user_id,
          avatar_url: presignedData.avatarUrl
        })
      })

      // 4. Atualizar UI e localStorage
      const avatarUrlWithCache = `${presignedData.avatarUrl}?t=${Date.now()}`
      setPreview(avatarUrlWithCache)
      setImageError(false)

      const saved = JSON.parse(localStorage.getItem('current_user') || '{}')
      localStorage.setItem('current_user', JSON.stringify({ ...saved, avatar_url: presignedData.avatarUrl }))

      onAvatarUpdate?.(presignedData.avatarUrl)
    } catch (error) {
      console.error('Avatar upload failed:', error)
      alert(error instanceof Error ? error.message : 'Erro ao fazer upload do avatar')
    } finally {
      setUploading(false)
    }
  }

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation()
    fileInputRef.current?.click()
  }
  
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    const file = e.dataTransfer.files[0]
    if (file) handleFileSelect(file)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  return (
    <div className={`relative ${className}`}>
      <div
        onClick={handleClick}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className={`
          ${sizeClasses[size]} 
          rounded-full overflow-hidden cursor-pointer
          border-2 border-cyan-400/50 hover:border-cyan-400 hover:scale-110
          transition-all duration-300 group relative
          bg-gradient-to-br from-purple-900/30 to-blue-900/30
        `}
        style={{
          boxShadow: '0 0 15px rgba(6, 182, 212, 0.3)'
        }}
        title="Clique para alterar foto de perfil"
      >
        {preview && !imageError ? (
          <img 
            src={preview} 
            alt="Avatar"
            className="w-full h-full object-cover"
            onError={() => {
              setImageError(true)
              setPreview(null)
            }}
            onLoad={() => setImageError(false)}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-cyan-400">
            <svg className="w-1/2 h-1/2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
        )}

        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-1">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span className="text-xs text-white font-semibold">Alterar</span>
        </div>

        {uploading && (
          <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
            <div className="w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={(e) => {
          e.stopPropagation()
          e.target.files?.[0] && handleFileSelect(e.target.files[0])
        }}
        onClick={(e) => e.stopPropagation()}
        className="hidden"
      />
    </div>
  )
}
