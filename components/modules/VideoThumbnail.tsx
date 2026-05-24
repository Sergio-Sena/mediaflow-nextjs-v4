'use client'

import { useState, useEffect, useRef } from 'react'
import { Play } from 'lucide-react'

interface VideoThumbnailProps {
  videoUrl: string
  videoKey: string
  alt: string
}

const CDN_BASE = 'https://d1l5mhz0fgb5g8.cloudfront.net'
const BUCKET_URL = 'https://mediaflow-uploads-969430605054.s3.amazonaws.com'

function getS3ThumbnailUrl(videoKey: string): string {
  // videoKey: users/sergio_sena/Star/Kate Kuray/file.mp4
  // thumbnail: public/thumbnails/sergio_sena/Star/Kate Kuray/file.jpg
  const parts = videoKey.split('/')
  if (parts.length >= 3 && parts[0] === 'users') {
    const thumbPath = 'public/thumbnails/' + parts.slice(1).join('/').replace(/\.[^.]+$/, '.jpg')
    return `${BUCKET_URL}/${encodeURIComponent(thumbPath).replace(/%2F/g, '/')}`
  }
  return ''
}

export default function VideoThumbnail({ videoUrl, videoKey, alt }: VideoThumbnailProps) {
  const [thumbnail, setThumbnail] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    // 1. Check localStorage cache
    const cached = localStorage.getItem(`thumb_${videoKey}`)
    if (cached) {
      setThumbnail(cached)
      setLoading(false)
      return
    }

    // 2. Try S3 thumbnail
    const s3Url = getS3ThumbnailUrl(videoKey)
    if (s3Url) {
      const img = new Image()
      img.onload = () => {
        setThumbnail(s3Url)
        setLoading(false)
        try { localStorage.setItem(`thumb_${videoKey}`, s3Url) } catch {}
      }
      img.onerror = () => {
        // 3. Fallback: generate in browser
        generateThumbnail()
      }
      img.src = s3Url
      return
    }

    // 3. Fallback: generate in browser
    const timer = setTimeout(() => generateThumbnail(), Math.random() * 1000)
    return () => clearTimeout(timer)
  }, [videoUrl, videoKey])

  const generateThumbnail = () => {
    const video = videoRef.current
    const canvas = canvasRef.current
    if (!video || !canvas) return

    video.addEventListener('loadeddata', () => { video.currentTime = 1 })
    video.addEventListener('seeked', () => {
      try {
        const ctx = canvas.getContext('2d')
        if (!ctx) return
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
        const dataUrl = canvas.toDataURL('image/jpeg', 0.7)
        try { localStorage.setItem(`thumb_${videoKey}`, dataUrl) } catch {}
        setThumbnail(dataUrl)
        setLoading(false)
      } catch { setLoading(false) }
    })
    video.addEventListener('error', () => setLoading(false))
  }

  return (
    <>
      <video ref={videoRef} src={videoUrl} crossOrigin="anonymous" className="hidden" muted playsInline />
      <canvas ref={canvasRef} className="hidden" />
      {thumbnail ? (
        <img src={thumbnail} alt={alt} className="w-full h-full object-cover" />
      ) : loading ? (
        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-900/30 to-blue-900/30">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-white border-t-transparent" />
        </div>
      ) : (
        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-900/30 to-blue-900/30">
          <Play className="w-16 h-16 text-white/50" />
        </div>
      )}
    </>
  )
}
