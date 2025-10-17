'use client'

import { useState, useRef } from 'react'

interface AvatarUploadProps {
  userId: string
  currentAvatar?: string
  onAvatarUpdate?: (avatarUrl: string) => void
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export default function AvatarUpload({ 
  userId, 
  currentAvatar, 
  onAvatarUpdate,
  size = 'md',
  className = ''
}: AvatarUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [preview, setPreview] = useState<string | null>(currentAvatar || null)
  const [imageError, setImageError] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const sizeClasses = {
    sm: 'w-12 h-12',
    md: 'w-20 h-20', 
    lg: 'w-32 h-32'
  }

  const handleFileSelect = async (file: File) => {
    if (!file.type.startsWith('image/')) return

    // Preview
    const reader = new FileReader()
    reader.onload = (e) => setPreview(e.target?.result as string)
    reader.readAsDataURL(file)

    // Upload via presigned URL
    setUploading(true)
    try {
      const ext = file.name.split('.').pop()
      
      // Obter presigned URL
      const presignedRes = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/avatar-presigned', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, fileExt: ext })
      })
      
      const presignedData = await presignedRes.json()
      
      if (!presignedData.success) throw new Error('Failed to get presigned URL')
      
      // Upload para S3 usando presigned URL
      await fetch(presignedData.presignedUrl, {
        method: 'PUT',
        body: file,
        headers: { 'Content-Type': file.type }
      })
      
      // Atualizar preview com cache-busting
      const avatarUrlWithCache = `${presignedData.avatarUrl}?t=${Date.now()}`
      setPreview(avatarUrlWithCache)
      
      // Atualizar DynamoDB
      await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/update-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          avatar_url: presignedData.avatarUrl
        })
      })
      
      onAvatarUpdate?.(presignedData.avatarUrl)
    } catch (error) {
      console.error('Avatar upload failed:', error)
      alert('Erro ao fazer upload. Verifique as credenciais AWS.')
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
          border-2 border-cyan-400/50 hover:border-cyan-400
          transition-all duration-300 group relative
          bg-gradient-to-br from-purple-900/30 to-blue-900/30
        `}
        style={{
          boxShadow: '0 0 15px rgba(6, 182, 212, 0.3)'
        }}
      >
        {preview && !imageError ? (
          <img 
            src={preview} 
            alt="Avatar"
            className="w-full h-full object-cover"
            onError={() => {
              console.warn(`Failed to load avatar: ${preview}`)
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

        {/* Upload Overlay */}
        <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
        </div>

        {/* Loading */}
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