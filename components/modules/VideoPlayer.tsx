'use client'

import { useState, useRef, useEffect } from 'react'
import { Play, Pause, Volume2, VolumeX, Maximize, SkipBack, SkipForward, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react'

interface VideoFile {
  key: string
  name: string
  url: string
  folder: string
}

interface VideoPlayerProps {
  src: string
  title: string
  currentVideo?: VideoFile
  playlist?: VideoFile[]
  onClose?: () => void
  onVideoChange?: (video: VideoFile) => void
}

export default function VideoPlayer({ src, title, currentVideo, playlist = [], onClose, onVideoChange }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  const [isMuted, setIsMuted] = useState(false)
  const [showControls, setShowControls] = useState(true)
  const [videoError, setVideoError] = useState<string | null>(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [currentSrc, setCurrentSrc] = useState(src)
  const [isMobile, setIsMobile] = useState(false)
  const [touchStart, setTouchStart] = useState<{ x: number; y: number } | null>(null)
  const [showMobileControls, setShowMobileControls] = useState(true)
  
  // Detectar dispositivo móvel
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768 || 'ontouchstart' in window)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])
  
  // Update current index and source when currentVideo changes
  useEffect(() => {
    if (currentVideo && playlist.length > 0) {
      const index = playlist.findIndex(v => v.key === currentVideo.key)
      if (index !== -1) {
        setCurrentIndex(index)
        setCurrentSrc(currentVideo.url)
        setVideoError(null)
        // Reset video state
        setCurrentTime(0)
        setIsPlaying(false)
      }
    }
  }, [currentVideo, playlist])
  
  // Update source when src prop changes
  useEffect(() => {
    setCurrentSrc(src)
  }, [src])

  // Keyboard shortcuts e touch gestures
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose?.()
      } else if (e.key === 'ArrowLeft') {
        playPrevious()
      } else if (e.key === 'ArrowRight') {
        playNext()
      } else if (e.key === ' ') {
        e.preventDefault()
        togglePlay()
      }
    }
    
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [currentIndex, playlist.length])
  
  // Touch gestures para mobile
  const handleTouchStart = (e: React.TouchEvent) => {
    const touch = e.touches[0]
    setTouchStart({ x: touch.clientX, y: touch.clientY })
  }
  
  const handleTouchEnd = (e: React.TouchEvent) => {
    if (!touchStart) return
    
    const touch = e.changedTouches[0]
    const deltaX = touch.clientX - touchStart.x
    const deltaY = touch.clientY - touchStart.y
    
    // Swipe horizontal para navegação (mínimo 50px)
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
      if (deltaX > 0) {
        playPrevious() // Swipe right = previous
      } else {
        playNext() // Swipe left = next
      }
    }
    
    // Tap para mostrar/esconder controles
    if (Math.abs(deltaX) < 10 && Math.abs(deltaY) < 10) {
      setShowMobileControls(!showMobileControls)
    }
    
    setTouchStart(null)
  }
  
  // Debug do tipo de arquivo
  console.log('=== VIDEO PLAYER DEBUG ===')
  console.log('Source:', src)
  console.log('Is .ts file:', src.endsWith('.ts'))
  console.log('Title:', title)
  console.log('Playlist:', playlist.length, 'videos')
  console.log('Current index:', currentIndex)
  console.log('Previous disabled:', currentIndex === 0 || playlist.length === 0)
  console.log('Next disabled:', currentIndex >= playlist.length - 1 || playlist.length === 0)

  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const updateTime = () => setCurrentTime(video.currentTime)
    const updateDuration = () => setDuration(video.duration)

    video.addEventListener('timeupdate', updateTime)
    video.addEventListener('loadedmetadata', updateDuration)
    video.addEventListener('ended', () => {
      setIsPlaying(false)
      // Auto-play next video
      playNext()
    })
    
    // Debug events
    video.addEventListener('loadstart', () => console.log('📦 Video load started'))
    video.addEventListener('canplay', () => console.log('✅ Video can play'))
    video.addEventListener('error', (e) => {
      console.error('❌ Video error:', e)
      setVideoError('Erro ao carregar vídeo')
    })
    video.addEventListener('loadeddata', () => console.log('📊 Video data loaded'))

    return () => {
      video.removeEventListener('timeupdate', updateTime)
      video.removeEventListener('loadedmetadata', updateDuration)
    }
  }, [])

  const togglePlay = () => {
    const video = videoRef.current
    if (!video) return

    if (isPlaying) {
      video.pause()
    } else {
      video.play()
    }
    setIsPlaying(!isPlaying)
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
  }
  
  const playNext = async () => {
    if (playlist.length === 0) return
    
    const nextIndex = currentIndex + 1
    if (nextIndex < playlist.length) {
      const nextVideo = playlist[nextIndex]
      setCurrentIndex(nextIndex)
      
      // Get presigned URL for next video
      try {
        const response = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(nextVideo.key)}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        })
        
        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            onVideoChange?.({ ...nextVideo, url: data.viewUrl })
            return
          }
        }
      } catch (error) {
        console.error('Error getting presigned URL:', error)
      }
      
      // Fallback to original URL
      onVideoChange?.(nextVideo)
    }
  }
  
  const playPrevious = async () => {
    if (playlist.length === 0) return
    
    const prevIndex = currentIndex - 1
    if (prevIndex >= 0) {
      const prevVideo = playlist[prevIndex]
      setCurrentIndex(prevIndex)
      
      // Get presigned URL for previous video
      try {
        const response = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(prevVideo.key)}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        })
        
        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            onVideoChange?.({ ...prevVideo, url: data.viewUrl })
            return
          }
        }
      } catch (error) {
        console.error('Error getting presigned URL:', error)
      }
      
      // Fallback to original URL
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
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-2 sm:p-4">
      <div className={`relative w-full bg-dark-900 overflow-hidden ${
        isMobile ? 'h-full rounded-none' : 'max-w-6xl rounded-lg'
      }`}>
        {/* Header */}
        <div className="flex items-center p-4 bg-dark-800/50 border-b border-neon-cyan/20">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-white truncate" title={title}>{title}</h3>
            {playlist.length > 0 && (
              <p className="text-sm text-gray-400 truncate" title={currentVideo?.folder}>
                {currentIndex + 1} de {playlist.length} • 📁 {currentVideo?.folder || 'Pasta'}
              </p>
            )}
          </div>
        </div>

        {/* Video Container */}
        <div 
          className="relative bg-black group max-h-[70vh] overflow-hidden"
          onMouseEnter={() => !isMobile && setShowControls(true)}
          onMouseLeave={() => !isMobile && setShowControls(false)}
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
        >
          {/* Close Button - Top Right */}
          <button
            onClick={onClose}
            className={`absolute top-4 right-4 z-20 text-white hover:text-neon-cyan transition-opacity duration-300 p-3 rounded-full bg-gray-800/70 backdrop-blur-sm ${
              (isMobile ? showMobileControls : showControls) ? 'opacity-100' : 'opacity-0'
            } ${isMobile ? 'text-xl min-h-[48px] min-w-[48px]' : 'text-lg'}`}
            title="Fechar (ESC)"
          >
            ✕
          </button>
          
          {/* Mobile Gesture Hint */}
          {isMobile && (
            <div className={`absolute top-4 left-4 z-20 text-white/70 text-sm bg-gray-800/70 backdrop-blur-sm rounded-lg p-2 transition-opacity duration-300 ${
              showMobileControls ? 'opacity-100' : 'opacity-0'
            }`}>
              👆 Toque para controles • 👈👉 Deslize para navegar
            </div>
          )}

          <video
            ref={videoRef}
            className="w-full h-full max-h-[70vh] object-contain"
            onClick={togglePlay}
            crossOrigin="anonymous"
            preload="metadata"
            key={currentSrc}
          >
            {/* Priorizar .ts nativo primeiro */}
            {currentSrc.endsWith('.ts') ? (
              <>
                <source src={currentSrc} type="video/mp2t" />
                <source src={currentSrc.replace('.ts', '.mp4')} type="video/mp4" />
              </>
            ) : (
              <>
                <source src={currentSrc} type="video/mp4" />
                <source src={currentSrc} type="video/webm" />
                <source src={currentSrc} type="video/ogg" />
              </>
            )}
            Seu navegador não suporta reprodução de vídeo.
          </video>

          {/* Error Message */}
          {videoError && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/50">
              <div className="text-center text-white">
                <p className="text-red-400 mb-2">{videoError}</p>
                <p className="text-sm text-gray-400">
                  {src.endsWith('.ts') ? 'Tentando reproduzir arquivo .ts nativamente' : 'Formato de vídeo não suportado'}
                </p>
              </div>
            </div>
          )}



          {/* Controls */}
          <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 to-transparent transition-opacity duration-300 ${
            (isMobile ? showMobileControls : showControls) ? 'opacity-100' : 'opacity-0'
          } ${isMobile ? 'p-3' : 'p-4'}`}>
            {/* Progress Bar */}
            <div className="mb-4">
              <input
                type="range"
                min="0"
                max={duration || 0}
                value={currentTime}
                onChange={handleSeek}
                className="w-full h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>

            {/* Control Buttons */}
            <div className={`flex items-center justify-between ${isMobile ? 'flex-col gap-3' : ''}`}>
              <div className={`flex items-center ${isMobile ? 'gap-6 justify-center w-full' : 'gap-4'}`}>
                {/* Previous Video */}
                <button
                  onClick={playPrevious}
                  disabled={currentIndex === 0 || playlist.length === 0}
                  className={`text-white hover:text-neon-cyan transition-colors disabled:text-gray-500 disabled:cursor-not-allowed rounded bg-gray-800/50 backdrop-blur-sm ${
                    isMobile ? 'p-3 min-h-[48px] min-w-[48px]' : 'p-2'
                  }`}
                  title={`Vídeo Anterior ${currentIndex === 0 ? '(Primeiro vídeo)' : ''}`}
                >
                  <ChevronLeft className={isMobile ? 'w-6 h-6' : 'w-5 h-5'} />
                </button>
                
                <button
                  onClick={() => skip(-10)}
                  className={`text-white hover:text-neon-cyan transition-colors rounded bg-gray-800/30 ${
                    isMobile ? 'p-3 min-h-[48px] min-w-[48px]' : 'p-2'
                  }`}
                  title="Voltar 10s"
                >
                  <SkipBack className={isMobile ? 'w-6 h-6' : 'w-5 h-5'} />
                </button>

                <button
                  onClick={togglePlay}
                  className={`bg-neon-cyan hover:bg-neon-cyan/80 rounded-full transition-colors ${
                    isMobile ? 'p-4 min-h-[56px] min-w-[56px]' : 'p-2'
                  }`}
                >
                  {isPlaying ? (
                    <Pause className={`text-black ${isMobile ? 'w-7 h-7' : 'w-5 h-5'}`} />
                  ) : (
                    <Play className={`text-black ${isMobile ? 'w-7 h-7 ml-1' : 'w-5 h-5 ml-0.5'}`} />
                  )}
                </button>

                <button
                  onClick={() => skip(10)}
                  className={`text-white hover:text-neon-cyan transition-colors rounded bg-gray-800/30 ${
                    isMobile ? 'p-3 min-h-[48px] min-w-[48px]' : 'p-2'
                  }`}
                  title="Avançar 10s"
                >
                  <SkipForward className={isMobile ? 'w-6 h-6' : 'w-5 h-5'} />
                </button>
                
                {/* Next Video */}
                <button
                  onClick={playNext}
                  disabled={currentIndex >= playlist.length - 1 || playlist.length === 0}
                  className={`text-white hover:text-neon-cyan transition-colors disabled:text-gray-500 disabled:cursor-not-allowed rounded bg-gray-800/50 backdrop-blur-sm ${
                    isMobile ? 'p-3 min-h-[48px] min-w-[48px]' : 'p-2'
                  }`}
                  title={`Próximo Vídeo ${currentIndex >= playlist.length - 1 ? '(Último vídeo)' : ''}`}
                >
                  <ChevronRight className={isMobile ? 'w-6 h-6' : 'w-5 h-5'} />
                </button>

                {!isMobile && (
                  <>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={toggleMute}
                        className="text-white hover:text-neon-cyan transition-colors p-2 rounded bg-gray-800/30"
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
                        className="w-20 h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
                      />
                    </div>

                    <span className="text-sm text-gray-300">
                      {formatTime(currentTime)} / {formatTime(duration)}
                    </span>
                  </>
                )}
              </div>

              {/* Mobile: Segunda linha com controles extras */}
              {isMobile && (
                <div className="flex items-center justify-between w-full">
                  <div className="flex items-center gap-4">
                    <button
                      onClick={toggleMute}
                      className="text-white hover:text-neon-cyan transition-colors p-3 rounded bg-gray-800/50 min-h-[48px] min-w-[48px]"
                    >
                      {isMuted ? <VolumeX className="w-6 h-6" /> : <Volume2 className="w-6 h-6" />}
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
                    className="text-white hover:text-neon-cyan transition-colors p-3 rounded bg-gray-800/50 min-h-[48px] min-w-[48px]"
                    title="Tela Cheia"
                  >
                    <Maximize className="w-6 h-6" />
                  </button>
                </div>
              )}
              
              {/* Desktop: Fullscreen button */}
              {!isMobile && (
                <button
                  onClick={toggleFullscreen}
                  className="text-white hover:text-neon-cyan transition-colors p-2 rounded bg-gray-800/30"
                  title="Tela Cheia"
                >
                  <Maximize className="w-5 h-5" />
                </button>
              )}
              
              {/* Mobile: Time display */}
              {isMobile && (
                <div className="text-center w-full mt-2">
                  <span className="text-sm text-gray-300 bg-gray-800/50 px-3 py-1 rounded-full">
                    {formatTime(currentTime)} / {formatTime(duration)}
                  </span>
                </div>
              )}
              

            </div>
          </div>
        </div>
        
        {/* Playlist */}
        {playlist.length > 1 && (
          <div className={`bg-dark-800/30 border-t border-neon-cyan/20 overflow-y-auto ${
            isMobile ? 'p-3 max-h-40' : 'p-4 max-h-48'
          }`}>
            <h4 className="text-sm font-semibold text-white mb-3">📋 Playlist ({playlist.length} vídeos)</h4>
            <div className={isMobile ? 'space-y-1' : 'space-y-2'}>
              {playlist.map((video, index) => (
                <button
                  key={video.key}
                  onClick={() => {
                    setCurrentIndex(index)
                    onVideoChange?.(video)
                  }}
                  className={`w-full text-left rounded-lg transition-colors touch-manipulation ${
                    isMobile ? 'p-3 min-h-[48px]' : 'p-2'
                  } ${
                    index === currentIndex
                      ? 'bg-neon-cyan/20 text-neon-cyan'
                      : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50 active:bg-gray-600/50'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className={`text-gray-400 w-6 flex-shrink-0 ${
                      isMobile ? 'text-sm' : 'text-xs'
                    }`}>{index + 1}</span>
                    <span className={`truncate flex-1 min-w-0 ${
                      isMobile ? 'text-base' : 'text-sm'
                    }`} title={video.name}>{video.name}</span>
                    {index === currentIndex && <span className="text-xs flex-shrink-0">▶️</span>}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}