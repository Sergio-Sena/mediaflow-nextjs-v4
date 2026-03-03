'use client'

import { useState, useRef, useEffect } from 'react'
import { Play, Pause, Volume2, VolumeX, X, SkipBack, SkipForward, List, ArrowLeft, Camera, Maximize2, Languages, MoreVertical, RotateCw } from 'lucide-react'

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

export default function VideoPlayer({ src, title, onClose, currentVideo, playlist, onVideoChange }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  const [isMuted, setIsMuted] = useState(false)
  const [videoUrl, setVideoUrl] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [showPlaylist, setShowPlaylist] = useState(false)
  const [showControls, setShowControls] = useState(true)
  const [playbackRate, setPlaybackRate] = useState(1)
  const [isBuffering, setIsBuffering] = useState(false)
  const [showVolumeIndicator, setShowVolumeIndicator] = useState(false)
  const [showSeekIndicator, setShowSeekIndicator] = useState<{show: boolean, text: string}>({show: false, text: ''})
  const [showClickFeedback, setShowClickFeedback] = useState(false)
  const [showKeyboardHelp, setShowKeyboardHelp] = useState(false)
  const [touchStart, setTouchStart] = useState<number | null>(null)
  const hideControlsTimeout = useRef<NodeJS.Timeout | null>(null)
  const volumeIndicatorTimeout = useRef<NodeJS.Timeout | null>(null)
  const seekIndicatorTimeout = useRef<NodeJS.Timeout | null>(null)
  const clickFeedbackTimeout = useRef<NodeJS.Timeout | null>(null)
  const keyboardHelpTimeout = useRef<NodeJS.Timeout | null>(null)

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

  useEffect(() => {
    const video = videoRef.current
    if (!video || !videoUrl) return

    let lastUpdate = 0
    const updateTime = () => {
      const now = Date.now()
      if (now - lastUpdate > 500) {
        setCurrentTime(video.currentTime)
        lastUpdate = now
      }
    }

    const updateDuration = () => {
      if (video.duration && !isNaN(video.duration)) {
        setDuration(video.duration)
      }
    }
    const handlePlay = () => setIsPlaying(true)
    const handlePause = () => setIsPlaying(false)
    const handleWaiting = () => setIsBuffering(true)
    const handleCanPlay = () => setIsBuffering(false)
    const handlePlaying = () => setIsBuffering(false)
    const handleVolumeChange = () => {
      setVolume(video.volume)
      setIsMuted(video.muted || video.volume === 0)
    }

    video.addEventListener('timeupdate', updateTime)
    video.addEventListener('loadedmetadata', updateDuration)
    video.addEventListener('durationchange', updateDuration)
    video.addEventListener('play', handlePlay)
    video.addEventListener('pause', handlePause)
    video.addEventListener('waiting', handleWaiting)
    video.addEventListener('canplay', handleCanPlay)
    video.addEventListener('playing', handlePlaying)
    video.addEventListener('volumechange', handleVolumeChange)

    if (video.duration && !isNaN(video.duration)) {
      setDuration(video.duration)
    }

    return () => {
      video.removeEventListener('timeupdate', updateTime)
      video.removeEventListener('loadedmetadata', updateDuration)
      video.removeEventListener('durationchange', updateDuration)
      video.removeEventListener('play', handlePlay)
      video.removeEventListener('pause', handlePause)
      video.removeEventListener('waiting', handleWaiting)
      video.removeEventListener('canplay', handleCanPlay)
      video.removeEventListener('playing', handlePlaying)
      video.removeEventListener('volumechange', handleVolumeChange)
    }
  }, [videoUrl])

  const togglePlay = () => {
    const video = videoRef.current
    if (!video) return
    if (isPlaying) {
      video.pause()
    } else {
      video.play()
    }
    setIsPlaying(!isPlaying)
    
    // Feedback visual
    setShowClickFeedback(true)
    if (clickFeedbackTimeout.current) clearTimeout(clickFeedbackTimeout.current)
    clickFeedbackTimeout.current = setTimeout(() => setShowClickFeedback(false), 500)
    
    resetControlsTimer()
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const video = videoRef.current
    if (!video) return
    const time = parseFloat(e.target.value)
    video.currentTime = time
    setCurrentTime(time)
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
    
    // Mostrar indicador de volume
    setShowVolumeIndicator(true)
    if (volumeIndicatorTimeout.current) clearTimeout(volumeIndicatorTimeout.current)
    volumeIndicatorTimeout.current = setTimeout(() => setShowVolumeIndicator(false), 1500)
  }

  const toggleFullscreen = () => {
    const video = videoRef.current
    if (!video) return
    const container = video.parentElement?.parentElement
    if (!container) return
    if (document.fullscreenElement) {
      document.exitFullscreen()
    } else {
      container.requestFullscreen()
    }
  }

  const handleDoubleClick = () => {
    toggleFullscreen()
  }

  const changePlaybackRate = () => {
    const video = videoRef.current
    if (!video) return
    const rates = [0.5, 0.75, 1, 1.25, 1.5, 2]
    const currentIndex = rates.indexOf(playbackRate)
    const nextRate = rates[(currentIndex + 1) % rates.length]
    video.playbackRate = nextRate
    setPlaybackRate(nextRate)
  }

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  const resetControlsTimer = () => {
    setShowControls(true)
    if (hideControlsTimeout.current) {
      clearTimeout(hideControlsTimeout.current)
    }
    if (isPlaying) {
      hideControlsTimeout.current = setTimeout(() => {
        setShowControls(false)
      }, 3000)
    }
  }

  const handleMouseMove = () => {
    resetControlsTimer()
    if (!showKeyboardHelp) {
      setShowKeyboardHelp(true)
      if (keyboardHelpTimeout.current) clearTimeout(keyboardHelpTimeout.current)
      keyboardHelpTimeout.current = setTimeout(() => setShowKeyboardHelp(false), 3000)
    }
  }

  const handleTouchStart = (e: React.TouchEvent) => {
    setTouchStart(e.touches[0].clientX)
  }

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (!touchStart) return
    const touchEnd = e.changedTouches[0].clientX
    const diff = touchStart - touchEnd
    if (Math.abs(diff) > 50) {
      const video = videoRef.current
      if (!video) return
      if (diff > 0) {
        video.currentTime = Math.min(duration, video.currentTime + 10)
        showSeekFeedback('+10s')
      } else {
        video.currentTime = Math.max(0, video.currentTime - 10)
        showSeekFeedback('-10s')
      }
    }
    setTouchStart(null)
  }

  const showSeekFeedback = (text: string) => {
    setShowSeekIndicator({show: true, text})
    if (seekIndicatorTimeout.current) clearTimeout(seekIndicatorTimeout.current)
    seekIndicatorTimeout.current = setTimeout(() => setShowSeekIndicator({show: false, text: ''}), 800)
  }

  useEffect(() => {
    if (isPlaying) {
      resetControlsTimer()
    } else {
      setShowControls(true)
      if (hideControlsTimeout.current) {
        clearTimeout(hideControlsTimeout.current)
      }
    }
  }, [isPlaying])

  useEffect(() => {
    return () => {
      if (hideControlsTimeout.current) {
        clearTimeout(hideControlsTimeout.current)
      }
    }
  }, [])

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      const video = videoRef.current
      if (!video) return

      switch(e.key) {
        case ' ':
        case 'k':
          e.preventDefault()
          togglePlay()
          break
        case 'ArrowLeft':
          e.preventDefault()
          video.currentTime = Math.max(0, video.currentTime - 10)
          showSeekFeedback('-10s')
          break
        case 'ArrowRight':
          e.preventDefault()
          video.currentTime = Math.min(duration, video.currentTime + 10)
          showSeekFeedback('+10s')
          break
        case 'ArrowUp':
          e.preventDefault()
          const newVolumeUp = Math.min(1, video.volume + 0.1)
          video.volume = newVolumeUp
          setVolume(newVolumeUp)
          setShowVolumeIndicator(true)
          if (volumeIndicatorTimeout.current) clearTimeout(volumeIndicatorTimeout.current)
          volumeIndicatorTimeout.current = setTimeout(() => setShowVolumeIndicator(false), 1500)
          break
        case 'ArrowDown':
          e.preventDefault()
          const newVolumeDown = Math.max(0, video.volume - 0.1)
          video.volume = newVolumeDown
          setVolume(newVolumeDown)
          setShowVolumeIndicator(true)
          if (volumeIndicatorTimeout.current) clearTimeout(volumeIndicatorTimeout.current)
          volumeIndicatorTimeout.current = setTimeout(() => setShowVolumeIndicator(false), 1500)
          break
        case 'f':
          e.preventDefault()
          toggleFullscreen()
          break
        case 'm':
          e.preventDefault()
          toggleMute()
          break
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [isPlaying, duration, volume])

  const handlePrevious = () => {
    if (!playlist || !currentVideo || !onVideoChange) return
    const currentIndex = playlist.findIndex(v => v.key === currentVideo.key)
    if (currentIndex > 0) {
      onVideoChange(playlist[currentIndex - 1])
    }
  }

  const handleNext = () => {
    if (!playlist || !currentVideo || !onVideoChange) return
    const currentIndex = playlist.findIndex(v => v.key === currentVideo.key)
    if (currentIndex < playlist.length - 1) {
      onVideoChange(playlist[currentIndex + 1])
    }
  }

  const currentIndex = playlist && currentVideo ? playlist.findIndex(v => v.key === currentVideo.key) : -1
  const hasPrevious = currentIndex > 0
  const hasNext = playlist && currentIndex < playlist.length - 1

  return (
    <div className="fixed inset-0 bg-black z-50 flex items-center justify-center">
      <div className="relative w-full h-full">
        {/* Video Container */}
        <div 
          className="relative w-full h-full bg-black" 
          onMouseMove={handleMouseMove}
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
        >
          {loading && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center text-white">
                <div className="loading-shimmer w-16 h-16 rounded-full mx-auto mb-4"></div>
                <p>Carregando vídeo...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center text-white">
                <p className="text-red-400 mb-2">{error}</p>
                <button onClick={onClose} className="btn-secondary">Fechar</button>
              </div>
            </div>
          )}

          {videoUrl && !loading && !error && (
            <>
              <video
                ref={videoRef}
                className="w-full h-full object-contain"
                onClick={togglePlay}
                onDoubleClick={handleDoubleClick}
                src={videoUrl}
                preload="metadata"
                playsInline
                crossOrigin="anonymous"
              />

              {/* Header Premium */}
              <div className={`absolute top-0 left-0 right-0 z-10 bg-gradient-to-b from-black/80 via-black/40 to-transparent backdrop-blur-sm transition-opacity duration-300 ${
                showControls ? 'opacity-100' : 'opacity-0'
              }`}>
                <div className="flex items-center justify-between p-2 sm:p-4">
                  <button
                    onClick={onClose}
                    className="text-white hover:text-neon-cyan p-1.5 sm:p-2 rounded-full hover:bg-white/10 transition-all active:scale-95"
                  >
                    <ArrowLeft className="w-5 h-5 sm:w-6 sm:h-6" strokeWidth={1.5} />
                  </button>
                  
                  <h3 className="flex-1 text-center text-white text-xs sm:text-sm font-medium truncate px-2 sm:px-4">{title}</h3>
                  
                  <div className="flex items-center gap-1 sm:gap-2">
                    <button 
                      onClick={toggleFullscreen}
                      className="text-white hover:text-neon-cyan p-1.5 sm:p-2 rounded-full hover:bg-white/10 transition-all active:scale-95"
                    >
                      <Maximize2 className="w-4 h-4 sm:w-5 sm:h-5" strokeWidth={1.5} />
                    </button>
                    <button 
                      onClick={toggleMute}
                      className="text-white hover:text-neon-cyan p-1.5 sm:p-2 rounded-full hover:bg-white/10 transition-all active:scale-95"
                    >
                      {isMuted ? <VolumeX className="w-4 h-4 sm:w-5 sm:h-5" strokeWidth={1.5} /> : <Volume2 className="w-4 h-4 sm:w-5 sm:h-5" strokeWidth={1.5} />}
                    </button>
                  </div>
                </div>
              </div>

              {/* Buffer Indicator */}
              {isBuffering && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="bg-black/70 rounded-full p-4">
                    <div className="animate-spin text-neon-cyan text-4xl">⏳</div>
                  </div>
                </div>
              )}

              {/* Click Feedback */}
              {showClickFeedback && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="bg-black/70 rounded-full p-6 animate-ping">
                    {isPlaying ? (
                      <Pause className="w-12 h-12 text-white" strokeWidth={2} />
                    ) : (
                      <Play className="w-12 h-12 text-white" strokeWidth={2} />
                    )}
                  </div>
                </div>
              )}

              {/* Seek Indicator */}
              {showSeekIndicator.show && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="bg-black/80 rounded-lg px-4 py-2 sm:px-6 sm:py-3">
                    <span className="text-white text-xl sm:text-2xl font-bold">{showSeekIndicator.text}</span>
                  </div>
                </div>
              )}



              {/* Volume Indicator */}
              {showVolumeIndicator && (
                <div className="absolute top-16 sm:top-20 right-2 sm:right-4 bg-black/80 rounded-lg p-2 sm:p-4 backdrop-blur-sm">
                  <div className="flex items-center gap-2 sm:gap-3">
                    {isMuted ? <VolumeX className="w-4 h-4 sm:w-6 sm:h-6 text-white" /> : <Volume2 className="w-4 h-4 sm:w-6 sm:h-6 text-white" />}
                    <div className="w-16 sm:w-24 h-1.5 sm:h-2 bg-gray-600 rounded-full">
                      <div 
                        className="h-full bg-white rounded-full transition-all"
                        style={{ width: `${isMuted ? 0 : volume * 100}%` }}
                      />
                    </div>
                    <span className="text-white text-xs sm:text-sm font-medium w-6 sm:w-8">{Math.round((isMuted ? 0 : volume) * 100)}%</span>
                  </div>
                </div>
              )}

              {/* Controls Premium */}
              <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 via-black/60 to-transparent backdrop-blur-sm p-3 sm:p-4 transition-opacity duration-300 ${
                showControls ? 'opacity-100' : 'opacity-0'
              }`}>
                {/* Progress Bar */}
                <div className="mb-2 sm:mb-3">
                  <input
                    type="range"
                    min="0"
                    max={duration || 0}
                    value={currentTime}
                    onChange={handleSeek}
                    className="w-full h-1 bg-gray-600/50 rounded-full appearance-none cursor-pointer"
                    style={{
                      background: `linear-gradient(to right, #00A8FF 0%, #00A8FF ${(currentTime / duration) * 100}%, rgba(255,255,255,0.2) ${(currentTime / duration) * 100}%, rgba(255,255,255,0.2) 100%)`
                    }}
                  />
                </div>

                {/* Center Play Button */}
                <div className="flex items-center justify-center mb-1 sm:mb-4">
                  <div className="flex items-center gap-1.5 sm:gap-8">
                    {playlist && playlist.length > 1 && hasPrevious && (
                      <button 
                        onClick={handlePrevious}
                        className="text-white hover:text-neon-cyan p-0.5 sm:p-4 landscape:!p-0.5 rounded-full hover:bg-white/10 transition-all active:scale-95"
                      >
                        <SkipBack className="w-3 h-3 sm:w-8 sm:h-8 landscape:!w-3 landscape:!h-3" strokeWidth={1.5} fill="currentColor" />
                      </button>
                    )}
                    
                    <button 
                      onClick={togglePlay} 
                      className="bg-white/90 hover:bg-white rounded-full p-1.5 sm:p-6 landscape:!p-1.5 transition-all active:scale-95 shadow-2xl"
                    >
                      {isPlaying ? (
                        <Pause className="w-4 h-4 sm:w-10 sm:h-10 landscape:!w-4 landscape:!h-4 text-black" strokeWidth={2} fill="currentColor" />
                      ) : (
                        <Play className="w-4 h-4 sm:w-10 sm:h-10 landscape:!w-4 landscape:!h-4 text-black" strokeWidth={2} fill="currentColor" style={{ marginLeft: '1px' }} />
                      )}
                    </button>
                    
                    {playlist && playlist.length > 1 && hasNext && (
                      <button 
                        onClick={handleNext}
                        className="text-white hover:text-neon-cyan p-0.5 sm:p-4 landscape:!p-0.5 rounded-full hover:bg-white/10 transition-all active:scale-95"
                      >
                        <SkipForward className="w-3 h-3 sm:w-8 sm:h-8 landscape:!w-3 landscape:!h-3" strokeWidth={1.5} fill="currentColor" />
                      </button>
                    )}
                  </div>
                </div>

                {/* Bottom Controls */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5 sm:gap-3">
                    <span className="text-white text-xs sm:text-sm font-medium">
                      {formatTime(currentTime)}
                    </span>
                    <span className="text-gray-400 text-xs sm:text-sm">/</span>
                    <span className="text-gray-400 text-xs sm:text-sm">
                      {formatTime(duration)}
                    </span>
                  </div>

                  <div className="flex items-center gap-1 sm:gap-3">
                    <button 
                      onClick={changePlaybackRate}
                      className="text-white hover:text-neon-cyan text-xs sm:text-sm font-medium px-2 py-1 sm:px-3 rounded-full hover:bg-white/10 transition-all active:scale-95"
                    >
                      {playbackRate}x
                    </button>
                    
                    {playlist && playlist.length > 1 && (
                      <button 
                        onClick={() => setShowPlaylist(!showPlaylist)} 
                        className="text-white hover:text-neon-cyan p-1.5 sm:p-2 rounded-full hover:bg-white/10 transition-all active:scale-95"
                      >
                        <List className="w-4 h-4 sm:w-5 sm:h-5" strokeWidth={1.5} />
                      </button>
                    )}
                    
                    <button className="hidden sm:block text-white hover:text-neon-cyan p-2 rounded-full hover:bg-white/10 transition-all active:scale-95">
                      <RotateCw className="w-5 h-5" strokeWidth={1.5} />
                    </button>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Playlist Sidebar */}
        {showPlaylist && playlist && playlist.length > 1 && (
          <div className="absolute right-0 top-0 bottom-0 w-full sm:w-80 bg-dark-900/95 backdrop-blur-sm border-l border-neon-cyan/20 overflow-y-auto z-20">
            <div className="p-3 sm:p-4">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <h4 className="text-white font-semibold text-sm sm:text-base">Playlist ({playlist.length})</h4>
                <button onClick={() => setShowPlaylist(false)} className="text-gray-400 hover:text-white p-2 active:scale-95 transition-all">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="space-y-2">
                {playlist.map((video, index) => (
                  <button
                    key={video.key}
                    onClick={() => onVideoChange && onVideoChange(video)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      currentVideo?.key === video.key
                        ? 'bg-neon-cyan/20 border border-neon-cyan/50'
                        : 'bg-dark-800/50 hover:bg-dark-800'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <span className={`text-sm font-mono ${
                        currentVideo?.key === video.key ? 'text-neon-cyan' : 'text-gray-400'
                      }`}>
                        {(index + 1).toString().padStart(2, '0')}
                      </span>
                      <div className="flex-1 min-w-0">
                        <p className={`text-sm truncate ${
                          currentVideo?.key === video.key ? 'text-white font-semibold' : 'text-gray-300'
                        }`}>
                          {video.name}
                        </p>
                        <p className="text-xs text-gray-500 truncate">{video.folder}</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
