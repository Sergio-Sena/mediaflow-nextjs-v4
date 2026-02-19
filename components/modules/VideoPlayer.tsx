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
  const hideControlsTimeout = useRef<NodeJS.Timeout | null>(null)

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

    const updateTime = () => setCurrentTime(video.currentTime)
    const updateDuration = () => {
      if (video.duration && !isNaN(video.duration)) {
        setDuration(video.duration)
      }
    }
    const handlePlay = () => setIsPlaying(true)
    const handlePause = () => setIsPlaying(false)

    video.addEventListener('timeupdate', updateTime)
    video.addEventListener('loadedmetadata', updateDuration)
    video.addEventListener('durationchange', updateDuration)
    video.addEventListener('play', handlePlay)
    video.addEventListener('pause', handlePause)

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
  }

  const toggleMute = () => {
    const video = videoRef.current
    if (!video) return

    setShowVolumeSlider(!showVolumeSlider)

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
      // 5s no mobile, 3s no desktop
      const isMobile = window.innerWidth < 640
      hideControlsTimeout.current = setTimeout(() => {
        setShowControls(false)
      }, isMobile ? 5000 : 3000)
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
      }, 1000) // Esconde mais rápido quando sai da área
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

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (hideControlsTimeout.current) {
        clearTimeout(hideControlsTimeout.current)
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
            className="text-white hover:text-neon-cyan p-1.5 sm:p-2 rounded-full bg-gray-800/50"
          >
            <X className="w-5 h-5 sm:w-6 sm:h-6" />
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
              />

              {/* Controls */}
              <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 to-transparent p-3 sm:p-4 transition-opacity duration-300 ${
                showControls ? 'opacity-100' : 'opacity-0'
              }`}>
                <div className="flex items-center gap-1 sm:gap-4 mb-2">
                  {playlist && playlist.length > 1 && (
                    <button 
                      onClick={handlePrevious} 
                      disabled={!hasPrevious}
                      className="text-white hover:text-neon-cyan disabled:opacity-30 disabled:cursor-not-allowed p-2 active:scale-95 transition-transform"
                    >
                      <SkipBack className="w-5 h-5" />
                    </button>
                  )}

                  <button onClick={togglePlay} className="bg-white hover:bg-gray-200 rounded-full p-3 transition-all active:scale-95">
                    {isPlaying ? (
                      <Pause className="w-5 h-5 sm:w-6 sm:h-6 text-black" />
                    ) : (
                      <Play className="w-5 h-5 sm:w-6 sm:h-6 text-black" style={{ marginLeft: '2px' }} />
                    )}
                  </button>

                  {playlist && playlist.length > 1 && (
                    <button 
                      onClick={handleNext} 
                      disabled={!hasNext}
                      className="text-white hover:text-neon-cyan disabled:opacity-30 disabled:cursor-not-allowed p-2 active:scale-95 transition-transform"
                    >
                      <SkipForward className="w-5 h-5" />
                    </button>
                  )}

                  <button onClick={toggleMute} className="text-white hover:text-neon-cyan p-2 active:scale-95 transition-transform">
                    {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
                  </button>

                  {showVolumeSlider && (
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={isMuted ? 0 : volume}
                      onChange={handleVolumeChange}
                      className="w-16 sm:w-20 h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer"
                    />
                  )}

                  <span className="text-gray-300 text-xs sm:text-sm whitespace-nowrap">
                    {formatTime(currentTime)} / {formatTime(duration)}
                  </span>

                  <button 
                    onClick={changePlaybackRate}
                    className="text-white hover:text-neon-cyan px-2 py-1 bg-gray-800/50 rounded text-xs sm:text-sm font-mono active:scale-95 transition-transform"
                    title="Velocidade de reprodução"
                  >
                    {playbackRate}x
                  </button>

                  <button 
                    onClick={togglePictureInPicture}
                    className="hidden sm:block text-white hover:text-neon-cyan p-2 active:scale-95 transition-transform"
                    title="Picture-in-Picture"
                  >
                    <PictureInPicture className="w-5 h-5" />
                  </button>

                  {playlist && playlist.length > 1 && (
                    <button 
                      onClick={() => setShowPlaylist(!showPlaylist)} 
                      className="text-white hover:text-neon-cyan p-2 active:scale-95 transition-transform"
                    >
                      <List className="w-5 h-5" />
                    </button>
                  )}

                  <button onClick={toggleFullscreen} className="text-white hover:text-neon-cyan ml-auto p-2 active:scale-95 transition-transform">
                    <Maximize className="w-5 h-5" />
                  </button>
                </div>

                <input
                  type="range"
                  min="0"
                  max={duration || 0}
                  value={currentTime}
                  onChange={handleSeek}
                  className="w-full h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer"
                />
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
                <button onClick={() => setShowPlaylist(false)} className="text-gray-400 hover:text-white p-2 active:scale-95 transition-transform">
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
