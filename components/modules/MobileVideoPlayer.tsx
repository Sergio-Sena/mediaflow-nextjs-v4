'use client'

import { useState, useRef, useEffect } from 'react'
import { Play, Pause, Volume2, VolumeX, Maximize, SkipBack, SkipForward, ChevronLeft, ChevronRight, X } from 'lucide-react'

interface VideoFile {
  key: string
  name: string
  url: string
  folder: string
}

interface MobileVideoPlayerProps {
  src: string
  title: string
  currentVideo?: VideoFile
  playlist?: VideoFile[]
  onClose?: () => void
  onVideoChange?: (video: VideoFile) => void
}

export default function MobileVideoPlayer({ src, title, currentVideo, playlist = [], onClose, onVideoChange }: MobileVideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  const [isMuted, setIsMuted] = useState(false)
  const [showControls, setShowControls] = useState(true)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [videoUrl, setVideoUrl] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [touchStart, setTouchStart] = useState<{ x: number; y: number; time: number } | null>(null)
  const [isFullscreen, setIsFullscreen] = useState(false)
  
  // Auto-hide controls timer
  const controlsTimeoutRef = useRef<NodeJS.Timeout>()
  
  useEffect(() => {
    const fetchPresignedUrl = async () => {
      setLoading(true)
      setError('')
      
      try {
        const isDev = process.env.NODE_ENV === 'development'
        const encodedSrc = encodeURIComponent(src)
        const response = isDev 
          ? await fetch('/api/proxy-view', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ key: src })
            })
          : await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodedSrc}`, {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
              }
            })

        if (response.ok) {
          const data = await response.json()
          if (data.success && data.viewUrl) {
            setVideoUrl(data.viewUrl)
          } else {
            setError('Erro ao obter URL do vídeo')
          }
        } else {
          setError(`Erro ${response.status}: ${response.statusText}`)
        }
      } catch (err) {
        setError('Erro ao conectar com servidor')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    if (src) {
      fetchPresignedUrl()
    }
  }, [src])

  // Update current index when currentVideo changes
  useEffect(() => {
    if (currentVideo && playlist.length > 0) {
      const index = playlist.findIndex(v => v.key === currentVideo.key)
      if (index !== -1) {
        setCurrentIndex(index)
        setCurrentTime(0)
        setIsPlaying(false)
      }
    }
  }, [currentVideo, playlist])
  
  // Auto-hide controls after 3 seconds
  const resetControlsTimer = () => {
    if (controlsTimeoutRef.current) {
      clearTimeout(controlsTimeoutRef.current)
    }
    
    setShowControls(true)
    
    if (isPlaying) {
      controlsTimeoutRef.current = setTimeout(() => {
        setShowControls(false)
      }, 3000)
    }
  }
  
  // Auto-hide when playing starts
  useEffect(() => {
    if (isPlaying) {
      resetControlsTimer()
    } else {
      setShowControls(true)
      if (controlsTimeoutRef.current) {
        clearTimeout(controlsTimeoutRef.current)
      }
    }
  }, [isPlaying])
  
  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (controlsTimeoutRef.current) {
        clearTimeout(controlsTimeoutRef.current)
      }
    }
  }, [])
  
  // Touch gesture handling
  const handleTouchStart = (e: React.TouchEvent) => {
    const touch = e.touches[0]
    setTouchStart({ 
      x: touch.clientX, 
      y: touch.clientY, 
      time: Date.now() 
    })
  }
  
  const handleTouchEnd = (e: React.TouchEvent) => {
    if (!touchStart) return
    
    const touch = e.changedTouches[0]
    const deltaX = touch.clientX - touchStart.x
    const deltaY = touch.clientY - touchStart.y
    const deltaTime = Date.now() - touchStart.time
    
    // Quick tap (< 200ms) = toggle controls
    if (deltaTime < 200 && Math.abs(deltaX) < 10 && Math.abs(deltaY) < 10) {
      resetControlsTimer()
      return
    }
    
    // Swipe gestures (minimum 80px)
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 80) {
      if (deltaX > 0) {
        playPrevious() // Swipe right = previous
      } else {
        playNext() // Swipe left = next
      }
    }
    
    // Double tap = toggle play/pause
    if (deltaTime < 300 && Math.abs(deltaX) < 20 && Math.abs(deltaY) < 20) {
      togglePlay()
    }
    
    setTouchStart(null)
  }
  
  // Video event handlers
  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const updateTime = () => setCurrentTime(video.currentTime)
    const updateDuration = () => setDuration(video.duration)
    const handleEnded = () => {
      setIsPlaying(false)
      playNext()
    }

    video.addEventListener('timeupdate', updateTime)
    video.addEventListener('loadedmetadata', updateDuration)
    video.addEventListener('ended', handleEnded)
    video.addEventListener('play', () => setIsPlaying(true))
    video.addEventListener('pause', () => setIsPlaying(false))

    return () => {
      video.removeEventListener('timeupdate', updateTime)
      video.removeEventListener('loadedmetadata', updateDuration)
      video.removeEventListener('ended', handleEnded)
    }
  }, [])
  
  // Fullscreen detection
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement)
    }
    
    document.addEventListener('fullscreenchange', handleFullscreenChange)
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange)
  }, [])

  const togglePlay = () => {
    const video = videoRef.current
    if (!video) return

    if (isPlaying) {
      video.pause()
    } else {
      video.play()
    }
    resetControlsTimer()
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const video = videoRef.current
    if (!video) return

    const time = parseFloat(e.target.value)
    video.currentTime = time
    setCurrentTime(time)
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const video = videoRef.current
    if (!video) return

    const vol = parseFloat(e.target.value)
    video.volume = vol
    setVolume(vol)
    setIsMuted(vol === 0)
  }

  const toggleMute = () => {
    const video = videoRef.current
    if (!video) return

    if (isMuted) {
      video.volume = volume
      setIsMuted(false)
    } else {
      video.volume = 0
      setIsMuted(true)
    }
  }

  const skip = (seconds: number) => {
    const video = videoRef.current
    if (!video) return

    video.currentTime = Math.max(0, Math.min(duration, video.currentTime + seconds))
    resetControlsTimer()
  }
  
  const playNext = async () => {
    if (playlist.length === 0) return
    
    const nextIndex = currentIndex + 1
    if (nextIndex < playlist.length) {
      const nextVideo = playlist[nextIndex]
      setCurrentIndex(nextIndex)
      onVideoChange?.(nextVideo)
    }
  }
  
  const playPrevious = async () => {
    if (playlist.length === 0) return
    
    const prevIndex = currentIndex - 1
    if (prevIndex >= 0) {
      const prevVideo = playlist[prevIndex]
      setCurrentIndex(prevIndex)
      onVideoChange?.(prevVideo)
    }
  }

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  const toggleFullscreen = () => {
    const video = videoRef.current
    if (!video) return

    if (document.fullscreenElement) {
      document.exitFullscreen()
    } else {
      video.requestFullscreen()
    }
  }

  return (
    <div className="fixed inset-0 bg-black z-50 flex flex-col overflow-hidden">
      {/* Video Container */}
      <div 
        className="relative w-full h-full bg-black flex items-center justify-center"
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        {/* Header - Only show when not fullscreen */}
        {!isFullscreen && (
          <div className={`absolute top-0 left-0 right-0 z-20 bg-gradient-to-b from-black/80 to-transparent p-4 transition-opacity duration-300 ${
            showControls ? 'opacity-100' : 'opacity-0'
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-semibold text-white truncate">{title}</h3>
                {playlist.length > 0 && (
                  <p className="text-sm text-gray-400">
                    {currentIndex + 1} de {playlist.length} • 📁 {currentVideo?.folder || 'Pasta'}
                  </p>
                )}
              </div>
              <button
                onClick={onClose}
                className="text-white hover:text-neon-cyan p-3 rounded-full bg-gray-800/50 backdrop-blur-sm min-h-[48px] min-w-[48px]"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>
        )}

        {loading && (
          <div className="absolute inset-0 flex items-center justify-center z-30">
            <div className="text-center text-white">
              <div className="loading-shimmer w-16 h-16 rounded-full mx-auto mb-4"></div>
              <p>Carregando vídeo...</p>
            </div>
          </div>
        )}

        {error && (
          <div className="absolute inset-0 flex items-center justify-center z-30">
            <div className="text-center text-white">
              <p className="text-red-400 mb-2">{error}</p>
              <button onClick={onClose} className="bg-neon-cyan text-black px-4 py-2 rounded">Fechar</button>
            </div>
          </div>
        )}

        {/* Video Element */}
        {videoUrl && !loading && !error && (
          <video
            ref={videoRef}
            className="absolute inset-0 w-full h-full object-contain"
            onClick={resetControlsTimer}
            src={videoUrl}
            crossOrigin="anonymous"
            preload="metadata"
            playsInline
          />
        )}



        {/* Bottom Controls - Fixed Footer */}
        <div className={`fixed bottom-0 left-0 right-0 z-50 bg-gradient-to-t from-black via-black/95 to-transparent transition-all duration-300 ${
          showControls ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-full pointer-events-none'
        }`}>
          {/* Progress Bar */}
          <div className="px-4 pt-4 pb-3">
            <input
              type="range"
              min="0"
              max={duration || 0}
              value={currentTime}
              onChange={handleSeek}
              className="w-full h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
            />
            <div className="flex justify-between text-xs text-gray-400 mt-2">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(duration)}</span>
            </div>
          </div>

          {/* Main Controls - Centered at bottom */}
          <div className="flex items-center justify-center gap-3 px-4 pb-2">
            <button
              onClick={playPrevious}
              disabled={currentIndex === 0 || playlist.length === 0}
              className="text-white hover:text-neon-cyan transition-colors disabled:text-gray-500 p-2 rounded-full bg-gray-800/50 min-h-[48px] min-w-[48px] touch-feedback"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
            
            <button
              onClick={() => skip(-10)}
              className="text-white hover:text-neon-cyan transition-colors p-2 rounded-full bg-gray-800/30 min-h-[48px] min-w-[48px] touch-feedback"
            >
              <SkipBack className="w-6 h-6" />
            </button>

            <button
              onClick={togglePlay}
              className="bg-neon-cyan hover:bg-neon-cyan/80 rounded-full p-3 transition-colors min-h-[64px] min-w-[64px] touch-feedback"
            >
              {isPlaying ? (
                <Pause className="w-8 h-8 text-black" />
              ) : (
                <Play className="w-8 h-8 text-black ml-1" />
              )}
            </button>

            <button
              onClick={() => skip(10)}
              className="text-white hover:text-neon-cyan transition-colors p-2 rounded-full bg-gray-800/30 min-h-[48px] min-w-[48px] touch-feedback"
            >
              <SkipForward className="w-6 h-6" />
            </button>
            
            <button
              onClick={playNext}
              disabled={currentIndex >= playlist.length - 1 || playlist.length === 0}
              className="text-white hover:text-neon-cyan transition-colors disabled:text-gray-500 p-2 rounded-full bg-gray-800/50 min-h-[48px] min-w-[48px] touch-feedback"
            >
              <ChevronRight className="w-6 h-6" />
            </button>
          </div>

          {/* Secondary Controls */}
          <div className="flex items-center justify-between px-4 pb-3">
            <div className="flex items-center gap-3 flex-1">
              <button
                onClick={toggleMute}
                className="text-white hover:text-neon-cyan transition-colors p-2 rounded-full bg-gray-800/50 min-h-[44px] min-w-[44px] touch-feedback"
              >
                {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
              </button>
              
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={isMuted ? 0 : volume}
                onChange={handleVolumeChange}
                className="flex-1 h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>

            <button
              onClick={toggleFullscreen}
              className="text-white hover:text-neon-cyan transition-colors p-2 rounded-full bg-gray-800/50 min-h-[44px] min-w-[44px] ml-3 touch-feedback"
            >
              <Maximize className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Playlist - Only show when not fullscreen */}
      {!isFullscreen && playlist.length > 1 && (
        <div className="fixed bottom-0 left-0 right-0 bg-dark-800/95 backdrop-blur-sm border-t border-neon-cyan/20 max-h-48 overflow-y-auto z-40" style={{ paddingBottom: '180px' }}>
          <div className="p-4">
            <h4 className="text-sm font-semibold text-white mb-3">📋 Playlist ({playlist.length} vídeos)</h4>
            <div className="space-y-1">
              {playlist.map((video, index) => (
                <button
                  key={video.key}
                  onClick={() => {
                    setCurrentIndex(index)
                    onVideoChange?.(video)
                  }}
                  className={`w-full text-left p-3 rounded-lg transition-colors touch-manipulation min-h-[48px] touch-feedback ${
                    index === currentIndex
                      ? 'bg-neon-cyan/20 text-neon-cyan'
                      : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-gray-400 w-6">{index + 1}</span>
                    <span className="text-base truncate flex-1">{video.name}</span>
                    {index === currentIndex && <span className="text-sm">▶️</span>}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}