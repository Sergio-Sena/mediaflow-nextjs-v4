import { useState, useCallback } from 'react'

interface ThumbnailState {
  [key: string]: {
    url?: string
    loading: boolean
    error?: string
  }
}

export function useThumbnails() {
  const [thumbnails, setThumbnails] = useState<ThumbnailState>({})

  const generateThumbnail = useCallback(async (videoFile: File, s3Key: string) => {
    const thumbnailKey = s3Key.replace(/\.[^.]+$/, '_thumb.jpg')
    
    setThumbnails(prev => ({
      ...prev,
      [s3Key]: { loading: true }
    }))

    try {
      // Check if running in browser (client-side)
      if (typeof window === 'undefined') {
        throw new Error('Thumbnail generation only available on client-side')
      }

      // For now, we'll use a placeholder approach since FFMPEG requires server-side
      // In a real implementation, this would call an API endpoint that runs FFMPEG
      const placeholderUrl = await generatePlaceholderThumbnail(videoFile)
      
      setThumbnails(prev => ({
        ...prev,
        [s3Key]: { 
          loading: false, 
          url: placeholderUrl 
        }
      }))

      return { success: true, url: placeholderUrl }

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      
      setThumbnails(prev => ({
        ...prev,
        [s3Key]: { 
          loading: false, 
          error: errorMessage 
        }
      }))

      return { success: false, error: errorMessage }
    }
  }, [])

  const getThumbnailUrl = useCallback((s3Key: string): string | null => {
    // Check for existing thumbnail
    const thumbnailKey = s3Key.replace(/\.[^.]+$/, '_thumb.jpg')
    const thumbnailUrl = `https://mediaflow-uploads-969430605054.s3.amazonaws.com/${thumbnailKey}`
    
    // For now, return a placeholder or the potential thumbnail URL
    return thumbnailUrl
  }, [])

  const clearThumbnail = useCallback((s3Key: string) => {
    setThumbnails(prev => {
      const newState = { ...prev }
      delete newState[s3Key]
      return newState
    })
  }, [])

  return {
    thumbnails,
    generateThumbnail,
    getThumbnailUrl,
    clearThumbnail
  }
}

// Placeholder thumbnail generation using canvas
async function generatePlaceholderThumbnail(videoFile: File): Promise<string> {
  return new Promise((resolve) => {
    const video = document.createElement('video')
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')!
    
    video.onloadedmetadata = () => {
      canvas.width = 320
      canvas.height = 180
      
      // Seek to 5 seconds or 10% of video duration
      const seekTime = Math.min(5, video.duration * 0.1)
      video.currentTime = seekTime
    }
    
    video.onseeked = () => {
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      const thumbnailUrl = canvas.toDataURL('image/jpeg', 0.8)
      resolve(thumbnailUrl)
    }
    
    video.onerror = () => {
      // Generate a placeholder thumbnail with video info
      ctx.fillStyle = '#1a1a1a'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      
      ctx.fillStyle = '#00ffff'
      ctx.font = '16px Arial'
      ctx.textAlign = 'center'
      ctx.fillText('🎥', canvas.width / 2, canvas.height / 2 - 10)
      ctx.font = '12px Arial'
      ctx.fillText(videoFile.name.substring(0, 25), canvas.width / 2, canvas.height / 2 + 15)
      
      const thumbnailUrl = canvas.toDataURL('image/jpeg', 0.8)
      resolve(thumbnailUrl)
    }
    
    video.src = URL.createObjectURL(videoFile)
    video.load()
  })
}