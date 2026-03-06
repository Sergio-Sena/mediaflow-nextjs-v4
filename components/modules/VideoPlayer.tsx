'use client'

import { useState, useRef, useEffect } from 'react'
import { Play, Pause, Volume2, VolumeX, Maximize, X, SkipBack, SkipForward, List, PictureInPicture } from 'lucide-react'

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
  const [showVolumeSlider, setShowVolumeSlider] = useState(false)
  const [isBuffering, setIsBuffering] = useState(false)
  const hideControlsTimeout = useRef<NodeJS.Timeout | null>(null)
  const hideVolumeTimeout = useRef<NodeJS.Timeout | null>(null)

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

    // Throttle timeupdate para reduzir re-renders
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
    
    // Sincroniza volume quando alterado por botões físicos
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

    // Força atualização da duração se já estiver carregada
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
    
    // Resetar timer ao ajustar volume (2s)
    if (hideVolumeTimeout.current) {
      clearTimeout(hideVolumeTimeout.current)
    }
    hideVolumeTimeout.current = setTimeout(() => {
      setShowVolumeSlider(false)
    }, 2000)
  }

  const toggleMute = () => {
    const video = videoRef.current
    if (!video) return

    setShowVolumeSlider(!showVolumeSlider)

    // Auto-hide volume slider após 2s (padrão YouTube/Netflix)
    if (hideVolumeTimeout.current) {
      clearTimeout(hideVolumeTimeout.current)
    }
    if (!showVolumeSlider) {
      hideVolumeTimeout.current = setTimeout(() => {
        setShowVolumeSlider(false)
      }, 2000)
    }

    if (isMuted) {
      video.volume = volume
      setIsMuted(false)
    } else {
      video.volume = 0
      setIsMuted(true)
    }
  }

  const toggleFullscreen = () => {
    const video = videoRef.current
    if (!video) return

    const container = video.parentElement
    if (!container) return

    if (document.fullscreenElement) {
      document.exitFullscreen()
    } else {
      container.requestFullscreen()
    }
  }

  const togglePictureInPicture = async () => {
    const video = videoRef.current
    if (!video) return

    try {
      if (document.pictureInPictureElement) {
        await document.exitPictureInPicture()
      } else {
        await video.requestPictureInPicture()
      }
    } catch (err) {
      console.error('PiP error:', err)
    }
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
      // 3s para esconder controles (padrão da indústria)
      hideControlsTimeout.current = setTimeout(() => {
        setShowControls(false)
      }, 3000)
    }
  }

  const handleMouseMove = () => {
    resetControlsTimer()
  }

  const handleMouseLeave = () => {
    if (isPlaying && hideControlsTimeout.current) {
      clearTimeout(hideControlsTimeout.current)
      hideControlsTimeout.current = setTimeout(() => {
        setShowControls(false)
      }, 500)
    }
  }

  // Auto-hide quando o vídeo começa a tocar
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

  // Cleanup timers on unmount
  useEffect(() => {
    return () => {
      if (hideControlsTimeout.current) {
        clearTimeout(hideControlsTimeout.current)
      }
      if (hideVolumeTimeout.current) {
        clearTimeout(hideVolumeTimeout.current)
      }
    }
  }, [])

  // Keyboard shortcuts
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
          video.currentTime = Math.max(0, video.currentTime - 5)
          break
        case 'ArrowRight':
          e.preventDefault()
          video.currentTime = Math.min(duration, video.currentTime + 5)
          break
        case 'ArrowUp':
          e.preventDefault()
          video.volume = Math.min(1, video.volume + 0.1)
          setVolume(video.volume)
          break
        case 'ArrowDown':
          e.preventDefault()
          video.volume = Math.max(0, video.volume - 0.1)
          setVolume(video.volume)
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
  }, [isPlaying, duration])

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
    <div className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4">
      <div className="relative w-full max-w-6xl bg-dark-900 rounded-lg overflow-hidden">
        {/* Header */}
        <div className={`flex items-center justify-between p-2 sm:p-4 bg-dark-800/50 border-b border-neon-cyan/20 transition-opacity duration-300 ${
          showControls ? 'opacity-100' : 'opacity-0'
        }`}>
          <h3 className="text-sm sm:text-lg font-semibold text-white truncate">{title}</h3>
          <button
            onClick={onClose}
            className="flex items-center justify-center w-10 h-10 rounded-lg bg-black/45 backdrop-blur-md text-white/90 hover:text-white transition-all duration-200 active:scale-95"
          >
            <X className="w-[18px] h-[18px]" />
          </button>
        </div>

        {/* Video Container */}
        <div 
          className="relative bg-black fullscreen:h-screen" 
          style={{ maxHeight: '80vh' }}
          onMouseMove={handleMouseMove}
          onMouseEnter={handleMouseMove}
          onMouseLeave={handleMouseLeave}
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
                className="w-full h-full object-contain fullscreen:object-cover"
                style={{ maxHeight: '80vh' }}
                onClick={resetControlsTimer}
                src={videoUrl}
                preload="metadata"
                playsInline
                crossOrigin="anonymous"
              />

              {/* Buffer Indicator */}
              {isBuffering && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="bg-black/70 rounded-full p-4">
                    <div className="animate-spin text-neon-cyan text-4xl">⏳</div>
                  </div>
                </div>
              )}

              {/* Controls */}
              <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-2 sm:p-3 md:p-4 transition-opacity duration-300 ${
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
                    className="w-full h-1.5 bg-white/25 rounded-full appearance-none cursor-pointer"
                    style={{
                      background: `linear-gradient(to right, #FF3B30 0%, #FF3B30 ${(currentTime / duration) * 100}%, rgba(255,255,255,0.25) ${(currentTime / duration) * 100}%, rgba(255,255,255,0.25) 100%)`
                    }}
                  />
                </div>

                <div className="flex items-center gap-1.5 sm:gap-2 md:gap-3 flex-wrap">
                  {/* Playlist Controls Group */}
                  {playlist && playlist.length > 1 ? (
                    <div className="flex items-center gap-1 sm:gap-1.5 md:gap-2 h-9 sm:h-10 md:h-12 px-1 sm:px-1.5 md:px-2 rounded-full bg-white/[0.18] border border-white/25 transition-all duration-300">
                      <button 
                        onClick={handlePrevious} 
                        disabled={!hasPrevious}
                        className="text-white/90 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 active:scale-95"
                      >
                        <SkipBack className="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5" />
                      </button>

                      <button 
                        onClick={togglePlay} 
                        className="flex items-center justify-center w-7 h-7 sm:w-8 sm:h-8 md:w-10 md:h-10 rounded-full bg-white/90 hover:bg-white transition-all duration-200 active:scale-95 shadow-lg"
                      >
                        {isPlaying ? (
                          <Pause className="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5 text-[#2F2F2F]" fill="#2F2F2F" />
                        ) : (
                          <Play className="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5 text-[#2F2F2F]" fill="#2F2F2F" style={{ marginLeft: '1px' }} />
                        )}
                      </button>

                      <button 
                        onClick={handleNext} 
                        disabled={!hasNext}
                        className="text-white/90 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 active:scale-95"
                      >
                        <SkipForward className="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5" />
                      </button>
                    </div>
                  ) : (
                    <button 
                      onClick={togglePlay} 
                      className="flex items-center justify-center w-9 h-9 sm:w-10 sm:h-10 md:w-12 md:h-12 rounded-full bg-white/90 hover:bg-white border border-white/25 transition-all duration-200 active:scale-95 shadow-lg"
                    >
                      {isPlaying ? (
                        <Pause className="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5 text-[#2F2F2F]" fill="#2F2F2F" />
                      ) : (
                        <Play className="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5 text-[#2F2F2F]" fill="#2F2F2F" style={{ marginLeft: '1px' }} />
                      )}
                    </button>
                  )}

                  {/* Volume Control */}
                  <div 
                    className="flex items-center gap-1 sm:gap-1.5 md:gap-2 h-7 sm:h-7 md:h-8 px-1.5 sm:px-2 md:px-3 rounded-full bg-white/[0.18] border border-white/25 transition-all duration-300"
                    onMouseEnter={() => {
                      setShowVolumeSlider(true)
                      if (hideVolumeTimeout.current) {
                        clearTimeout(hideVolumeTimeout.current)
                      }
                    }}
                    onMouseLeave={() => {
                      if (hideVolumeTimeout.current) {
                        clearTimeout(hideVolumeTimeout.current)
                      }
                      hideVolumeTimeout.current = setTimeout(() => {
                        setShowVolumeSlider(false)
                      }, 300)
                    }}
                  >
                    <button onClick={toggleMute} className="text-white/85 hover:text-white transition-all duration-200 active:scale-95">
                      {isMuted ? <VolumeX className="w-3 h-3 sm:w-3.5 sm:h-3.5 md:w-4 md:h-4" /> : <Volume2 className="w-3 h-3 sm:w-3.5 sm:h-3.5 md:w-4 md:h-4" />}
                    </button>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={isMuted ? 0 : volume}
                      onChange={handleVolumeChange}
                      className={`h-1 bg-white/35 rounded-full appearance-none cursor-pointer transition-all duration-300 ${
                        showVolumeSlider ? 'w-12 sm:w-16 md:w-20 opacity-100' : 'w-0 opacity-0'
                      }`}
                      style={{
                        background: `linear-gradient(to right, #FFFFFF 0%, #FFFFFF ${volume * 100}%, rgba(255,255,255,0.35) ${volume * 100}%, rgba(255,255,255,0.35) 100%)`
                      }}
                    />
                  </div>

                  {/* Timer */}
                  <span className="text-white/85 text-[10px] sm:text-xs md:text-sm font-medium whitespace-nowrap px-1.5 sm:px-2 md:px-3 py-1 sm:py-1 md:py-1.5 rounded-full bg-white/[0.18] border border-white/25 transition-all duration-300">
                    {formatTime(currentTime)} / {formatTime(duration)}
                  </span>

                  {/* Right Controls Group */}
                  <div className="flex items-center gap-1 sm:gap-1.5 md:gap-2 h-7 sm:h-8 md:h-10 px-1 sm:px-1.5 md:px-2 rounded-full bg-white/[0.18] border border-white/25 ml-auto transition-all duration-300">
                    <button 
                      onClick={changePlaybackRate}
                      className="text-white/85 hover:text-white px-1 sm:px-1.5 md:px-2 text-[10px] sm:text-xs md:text-sm font-medium transition-all duration-200 active:scale-95"
                      title="Velocidade de reprodução"
                    >
                      {playbackRate}x
                    </button>

                    <button 
                      onClick={togglePictureInPicture}
                      className="hidden sm:flex items-center justify-center text-white/90 hover:text-white transition-all duration-200 active:scale-95"
                      title="Picture-in-Picture"
                    >
                      <PictureInPicture className="w-4 h-4 md:w-[18px] md:h-[18px]" />
                    </button>

                    {playlist && playlist.length > 1 && (
                      <button 
                        onClick={() => setShowPlaylist(!showPlaylist)} 
                        className="flex items-center justify-center text-white/90 hover:text-white transition-all duration-200 active:scale-95"
                      >
                        <List className="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-[18px] md:h-[18px]" />
                      </button>
                    )}

                    <button 
                      onClick={toggleFullscreen} 
                      className="flex items-center justify-center text-white/90 hover:text-white transition-all duration-200 active:scale-95"
                    >
                      <Maximize className="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-[18px] md:h-[18px]" />
                    </button>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Playlist Sidebar */}
        {showPlaylist && playlist && playlist.length > 1 && (
          <div className="absolute right-0 top-0 bottom-0 w-full max-w-xs sm:w-80 bg-dark-900/95 backdrop-blur-sm border-l border-neon-cyan/20 overflow-y-auto">
            <div className="p-3 sm:p-4">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <h4 className="text-sm sm:text-base text-white font-semibold">Playlist ({playlist.length})</h4>
                <button onClick={() => setShowPlaylist(false)} className="text-gray-400 hover:text-white p-2 transition-all duration-200 active:scale-95">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="space-y-2">
                {playlist.map((video, index) => (
                  <button
                    key={video.key}
                    onClick={() => onVideoChange && onVideoChange(video)}
                    className={`w-full text-left p-3 rounded-lg transition-all duration-200 ${
                      currentVideo?.key === video.key
                        ? 'bg-neon-cyan/20 border border-neon-cyan/50'
                        : 'bg-dark-800/50 hover:bg-dark-800 border border-transparent'
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
