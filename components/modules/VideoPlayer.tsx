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
  const containerRef = useRef<HTMLDivElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  const [isMuted, setIsMuted] = useState(true)
  const [videoUrl, setVideoUrl] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [showPlaylist, setShowPlaylist] = useState(false)
  const [showControls, setShowControls] = useState(true)
  const [playbackRate, setPlaybackRate] = useState(1)
  const [showVolumeSlider, setShowVolumeSlider] = useState(false)
  const [isBuffering, setIsBuffering] = useState(false)
  const [showCenterIcon, setShowCenterIcon] = useState(false)
  const [seekFeedback, setSeekFeedback] = useState<{ side: 'left' | 'right', secs: number } | null>(null)
  const [isLandscapeMobile, setIsLandscapeMobile] = useState(false)
  const hideControlsTimeout = useRef<NodeJS.Timeout | null>(null)
  const hideVolumeTimeout = useRef<NodeJS.Timeout | null>(null)
  const hideCenterIconTimeout = useRef<NodeJS.Timeout | null>(null)
  const seekFeedbackTimeout = useRef<NodeJS.Timeout | null>(null)
  const lastTapTime = useRef<number>(0)
  const lastTapSide = useRef<'left' | 'right' | null>(null)

  // Detectar landscape mobile
  useEffect(() => {
    const check = () => {
      const landscape = window.innerWidth > window.innerHeight
      const mobile = window.innerWidth < 1024
      setIsLandscapeMobile(landscape && mobile)
    }
    check()
    window.addEventListener('resize', check)
    window.addEventListener('orientationchange', check)
    return () => {
      window.removeEventListener('resize', check)
      window.removeEventListener('orientationchange', check)
    }
  }, [])

  // Auto-fullscreen em landscape mobile ao carregar o vídeo
  useEffect(() => {
    if (!videoUrl || !isLandscapeMobile) return
    const container = containerRef.current
    if (!container || document.fullscreenElement) return
    const timer = setTimeout(() => {
      container.requestFullscreen().catch(() => {})
    }, 300)
    return () => clearTimeout(timer)
  }, [videoUrl, isLandscapeMobile])

  // Cleanup seekFeedback timeout
  useEffect(() => {
    return () => {
      if (seekFeedbackTimeout.current) clearTimeout(seekFeedbackTimeout.current)
    }
  }, [])

  // Fetch presigned URL
  useEffect(() => {
    const fetchPresignedUrl = async () => {
      setLoading(true)
      setError('')
      
      try {
        const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
        console.log('🔑 Token:', token ? '[present]' : 'MISSING')
        if (!token) {
          setError('🔒 Sessão expirada. Faça login novamente para continuar.')
          setLoading(false)
          return
        }
        
        const isDev = process.env.NODE_ENV === 'development'
        const encodedSrc = encodeURIComponent(src)
        const response = isDev 
          ? await fetch('/api/proxy-view', {
              method: 'POST',
              headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify({ key: src })
            })
          : await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodedSrc}`, {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            })

        if (response.ok) {
          const data = await response.json()
          if (data.success && data.viewUrl) {
            setVideoUrl(data.viewUrl)
          } else {
            setError('📡 Não foi possível carregar o vídeo. Tente novamente.')
          }
        } else {
          setError(`⚠️ Falha na conexão (${response.status}). Verifique sua internet.`)
        }
      } catch (err) {
        setError('🌐 Sem conexão com o servidor. Verifique sua internet.')
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

  // Double-tap seek (YouTube mobile style)
  const handleVideoTap = (e: React.TouchEvent<HTMLDivElement>) => {
    const video = videoRef.current
    if (!video) return
    const now = Date.now()
    const rect = e.currentTarget.getBoundingClientRect()
    const tapX = e.changedTouches[0].clientX - rect.left
    const side = tapX < rect.width / 2 ? 'left' : 'right'
    const isDoubleTap = now - lastTapTime.current < 300 && lastTapSide.current === side

    if (isDoubleTap) {
      const secs = 10
      if (side === 'left') {
        video.currentTime = Math.max(0, video.currentTime - secs)
      } else {
        video.currentTime = Math.min(duration, video.currentTime + secs)
      }
      setSeekFeedback({ side, secs })
      if (seekFeedbackTimeout.current) clearTimeout(seekFeedbackTimeout.current)
      seekFeedbackTimeout.current = setTimeout(() => setSeekFeedback(null), 800)
      lastTapTime.current = 0
    } else {
      lastTapTime.current = now
      lastTapSide.current = side
      // single tap — toggle controls
      resetControlsTimer()
    }
  }

  const togglePlay = () => {
    const video = videoRef.current
    if (!video) return

    if (isPlaying) {
      video.pause()
    } else {
      video.play()
    }
    setIsPlaying(!isPlaying)
    
    // Show center icon
    setShowCenterIcon(true)
    if (hideCenterIconTimeout.current) {
      clearTimeout(hideCenterIconTimeout.current)
    }
    hideCenterIconTimeout.current = setTimeout(() => {
      setShowCenterIcon(false)
    }, 600)
    
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
      video.muted = false
      video.volume = volume || 1
      setIsMuted(false)
    } else {
      video.muted = true
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
      // 4s para mobile, 6s para desktop
      const hideDelay = window.innerWidth < 768 ? 4000 : 6000
      hideControlsTimeout.current = setTimeout(() => {
        setShowControls(false)
      }, hideDelay)
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
      if (hideCenterIconTimeout.current) {
        clearTimeout(hideCenterIconTimeout.current)
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
    <div className="fixed inset-0 bg-black z-50 flex items-center justify-center">
      <div ref={containerRef} className="relative w-full h-full md:h-auto md:max-w-6xl md:bg-dark-900 md:rounded-lg md:overflow-hidden md:m-4">
        {/* Botão fechar — sempre visível, fora do fade dos controles */}
        {!isLandscapeMobile && (
          <button
            onClick={onClose}
            aria-label="Fechar player"
            className="absolute top-3 right-3 z-20 flex items-center justify-center w-9 h-9 rounded-lg bg-black/60 border border-white/10 text-gray-300 hover:bg-black/80 hover:text-white transition-all active:scale-95"
          >
            <X className="w-4 h-4" />
          </button>
        )}

        {/* Título overlay — desktop */}
        {!isLandscapeMobile && (
          <div className="absolute top-0 left-0 right-14 px-3 py-3 pointer-events-none">
            <p className="text-sm font-semibold text-white truncate drop-shadow">{title}</p>
          </div>
        )}

        {/* Video Container */}
        <div
          className="relative bg-black"
          style={{ height: isLandscapeMobile ? '100vh' : '100%', maxHeight: isLandscapeMobile ? '100vh' : '90vh' }}
          onMouseMove={handleMouseMove}
          onMouseEnter={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          onTouchStart={handleMouseMove}
          onTouchEnd={handleVideoTap}
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
            <div className="absolute inset-0 flex items-center justify-center bg-black/80">
              <div className="text-center text-white max-w-sm px-6">
                <div className="text-4xl mb-3">📹</div>
                <p className="text-gray-200 mb-4 text-sm">{error}</p>
                <div className="flex gap-3 justify-center">
                  <button onClick={() => { setError(''); setLoading(true); }} className="px-4 py-2 bg-cyan-600/20 text-cyan-300 border border-cyan-500/30 rounded-lg hover:bg-cyan-600/40 transition-colors text-sm">
                    🔄 Tentar novamente
                  </button>
                  <button onClick={onClose} className="px-4 py-2 bg-gray-700/50 text-gray-300 border border-gray-600/30 rounded-lg hover:bg-gray-700 transition-colors text-sm">
                    Fechar
                  </button>
                </div>
              </div>
            </div>
          )}

          {videoUrl && !loading && !error && (
            <>
              <video
                ref={videoRef}
                className="w-full h-full object-contain"
                onClick={togglePlay}
                onDoubleClick={toggleFullscreen}
                src={videoUrl}
                preload="auto"
                playsInline
                crossOrigin="anonymous"
                autoPlay
                muted={isMuted}
              />

              {/* Seek feedback double-tap */}
              {seekFeedback && (
                <div className={`absolute top-1/2 -translate-y-1/2 pointer-events-none flex flex-col items-center gap-1 ${
                  seekFeedback.side === 'left' ? 'left-8' : 'right-8'
                }`}>
                  <div className="bg-black/60 rounded-full px-4 py-2 text-white text-sm font-bold">
                    {seekFeedback.side === 'left' ? `⏪ -${seekFeedback.secs}s` : `+${seekFeedback.secs}s ⏩`}
                  </div>
                </div>
              )}

              {/* Fechar overlay — landscape mobile */}
              {isLandscapeMobile && (
                <button
                  onClick={onClose}
                  className={`absolute top-3 right-3 z-10 flex items-center justify-center w-8 h-8 rounded-full bg-black/50 text-white/80 hover:text-white transition-all ${
                    showControls ? 'opacity-100' : 'opacity-0 pointer-events-none'
                  }`}
                >
                  <X className="w-4 h-4" />
                </button>
              )}

              {/* Título overlay — landscape mobile */}
              {isLandscapeMobile && (
                <div className={`absolute top-3 left-3 right-14 pointer-events-none transition-opacity duration-300 ${
                  showControls ? 'opacity-100' : 'opacity-0'
                }`}>
                  <p className="text-white text-xs font-medium truncate drop-shadow">{title}</p>
                </div>
              )}

              {/* Buffer Indicator */}
              {isBuffering && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="bg-black/70 rounded-full p-4">
                    <div className="animate-spin text-neon-cyan text-4xl">⏳</div>
                  </div>
                </div>
              )}

              {/* Center Play/Pause Icon */}
              {showCenterIcon && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none animate-fade-out">
                  <div className="bg-black/60 rounded-full p-6 sm:p-8">
                    {isPlaying ? (
                      <Play className="w-16 h-16 sm:w-20 sm:h-20 text-white" />
                    ) : (
                      <Pause className="w-16 h-16 sm:w-20 sm:h-20 text-white" />
                    )}
                  </div>
                </div>
              )}

              {/* Controls */}
              <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent px-3 pt-8 pb-3 md:px-4 md:pb-4 transition-opacity duration-300 ${
                showControls ? 'opacity-100' : 'opacity-0 pointer-events-none'
              }`}>
                {/* Progress Bar */}
                <div className="mb-2">
                  <input
                    type="range"
                    min="0"
                    max={duration || 0}
                    value={currentTime}
                    onChange={handleSeek}
                    className="w-full h-1.5 bg-white/25 rounded-full appearance-none cursor-pointer"
                    style={{
                      background: `linear-gradient(to right, #667eea 0%, #667eea ${(currentTime / duration) * 100}%, rgba(255,255,255,0.25) ${(currentTime / duration) * 100}%, rgba(255,255,255,0.25) 100%)`
                    }}
                  />
                </div>

                <div className="flex items-center justify-between gap-2">
                  {/* Left controls */}
                  <div className="flex items-center gap-2">
                    {/* Play/Pause — sempre visível */}
                    <button
                      onClick={togglePlay}
                      aria-label={isPlaying ? 'Pausar' : 'Reproduzir'}
                      className="flex items-center justify-center w-9 h-9 rounded-full bg-white/15 border border-white/20 text-white hover:bg-white/25 transition-all active:scale-95"
                    >
                      {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" style={{ marginLeft: '1px' }} />}
                    </button>

                    {/* Anterior/Próximo — se playlist */}
                    {playlist && playlist.length > 1 && (
                      <>
                        <button onClick={handlePrevious} disabled={!hasPrevious} aria-label="Anterior" className="flex items-center justify-center w-8 h-8 rounded-full text-white/70 hover:text-white disabled:opacity-30 transition-all active:scale-95">
                          <SkipBack className="w-4 h-4" />
                        </button>
                        <button onClick={handleNext} disabled={!hasNext} aria-label="Próximo" className="flex items-center justify-center w-8 h-8 rounded-full text-white/70 hover:text-white disabled:opacity-30 transition-all active:scale-95">
                          <SkipForward className="w-4 h-4" />
                        </button>
                      </>
                    )}

                    {/* Volume — só desktop */}
                    <div
                      className="hidden md:flex items-center gap-1.5"
                      onMouseEnter={() => { setShowVolumeSlider(true); if (hideVolumeTimeout.current) clearTimeout(hideVolumeTimeout.current) }}
                      onMouseLeave={() => { hideVolumeTimeout.current = setTimeout(() => setShowVolumeSlider(false), 300) }}
                    >
                      <button onClick={toggleMute} aria-label={isMuted ? 'Ativar som' : 'Silenciar'} className="text-white/80 hover:text-white transition-colors">
                        {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                      </button>
                      <input
                        type="range" min="0" max="1" step="0.1"
                        value={isMuted ? 0 : volume}
                        onChange={handleVolumeChange}
                        className={`h-1 bg-white/30 rounded-full appearance-none cursor-pointer transition-all duration-200 ${
                          showVolumeSlider ? 'w-20 opacity-100' : 'w-0 opacity-0'
                        }`}
                        style={{ background: `linear-gradient(to right, #667eea 0%, #667eea ${volume * 100}%, rgba(255,255,255,0.3) ${volume * 100}%, rgba(255,255,255,0.3) 100%)` }}
                      />
                    </div>

                    {/* Timer — sempre visível */}
                    <span className="text-white/70 text-xs font-mono whitespace-nowrap">
                      {formatTime(currentTime)} / {formatTime(duration)}
                    </span>
                  </div>

                  {/* Right controls */}
                  <div className="flex items-center gap-1.5">
                    {/* Velocidade — desktop */}
                    <button
                      onClick={changePlaybackRate}
                      aria-label={`Velocidade ${playbackRate}x`}
                      className="hidden md:flex items-center justify-center h-7 px-2 rounded text-white/70 hover:text-white text-xs font-semibold bg-white/10 hover:bg-white/20 transition-all"
                    >
                      {playbackRate}x
                    </button>

                    {/* Playlist */}
                    {playlist && playlist.length > 1 && (
                      <button
                        onClick={() => setShowPlaylist(!showPlaylist)}
                        aria-label="Playlist"
                        className={`flex items-center justify-center w-8 h-8 rounded-full transition-all active:scale-95 ${
                          showPlaylist ? 'bg-[#667eea]/40 text-white' : 'text-white/70 hover:text-white bg-white/10 hover:bg-white/20'
                        }`}
                      >
                        <List className="w-4 h-4" />
                      </button>
                    )}

                    {/* PiP — desktop */}
                    <button
                      onClick={togglePictureInPicture}
                      aria-label="Picture in Picture"
                      className="hidden md:flex items-center justify-center w-8 h-8 rounded-full text-white/70 hover:text-white bg-white/10 hover:bg-white/20 transition-all active:scale-95"
                    >
                      <PictureInPicture className="w-4 h-4" />
                    </button>

                    {/* Fullscreen */}
                    <button
                      onClick={toggleFullscreen}
                      aria-label="Tela cheia"
                      className="flex items-center justify-center w-8 h-8 rounded-full text-white/70 hover:text-white bg-white/10 hover:bg-white/20 transition-all active:scale-95"
                    >
                      <Maximize className="w-4 h-4" />
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
