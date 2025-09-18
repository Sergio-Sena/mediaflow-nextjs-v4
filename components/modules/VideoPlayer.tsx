'use client'

import { useState, useRef, useEffect } from 'react'
import { Play, Pause, Volume2, VolumeX, Maximize, SkipBack, SkipForward } from 'lucide-react'

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
  
  // Update current index when currentVideo changes
  useEffect(() => {
    if (currentVideo && playlist.length > 0) {
      const index = playlist.findIndex(v => v.key === currentVideo.key)
      if (index !== -1) setCurrentIndex(index)
    }
  }, [currentVideo, playlist])

  // Debug do tipo de arquivo
  console.log('=== VIDEO PLAYER DEBUG ===')
  console.log('Source:', src)
  console.log('Is .ts file:', src.endsWith('.ts'))
  console.log('Title:', title)
  console.log('Playlist:', playlist.length, 'videos')
  console.log('Current index:', currentIndex)

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
  
  const playNext = () => {
    if (playlist.length === 0) return
    
    const nextIndex = currentIndex + 1
    if (nextIndex < playlist.length) {
      const nextVideo = playlist[nextIndex]
      setCurrentIndex(nextIndex)
      onVideoChange?.(nextVideo)
    }
  }
  
  const playPrevious = () => {
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
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="relative w-full max-w-6xl bg-dark-900 rounded-lg overflow-hidden">
        {/* Header */}
        <div className="flex justify-between items-center p-4 bg-dark-800/50 border-b border-neon-cyan/20">
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
            className="text-gray-400 hover:text-white transition-colors ml-4"
          >
            ✕
          </button>
        </div>

        {/* Video Container */}
        <div 
          className="relative bg-black group max-h-[70vh] overflow-hidden"
          onMouseEnter={() => setShowControls(true)}
          onMouseLeave={() => setShowControls(false)}
        >
          <video
            ref={videoRef}
            className="w-full h-full max-h-[70vh] object-contain"
            onClick={togglePlay}
            crossOrigin="anonymous"
            preload="metadata"
          >
            {/* Priorizar .ts nativo primeiro */}
            {src.endsWith('.ts') ? (
              <>
                <source src={src} type="video/mp2t" />
                <source src={src.replace('.ts', '.mp4')} type="video/mp4" />
              </>
            ) : (
              <>
                <source src={src} type="video/mp4" />
                <source src={src} type="video/webm" />
                <source src={src} type="video/ogg" />
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

          {/* Play/Pause Overlay */}
          {!isPlaying && (
            <div className="absolute inset-0 flex items-center justify-center">
              <button
                onClick={togglePlay}
                className="bg-neon-cyan/20 hover:bg-neon-cyan/30 rounded-full p-6 transition-all duration-300 hover:scale-110"
              >
                <Play className="w-12 h-12 text-neon-cyan ml-1" />
              </button>
            </div>
          )}

          {/* Controls */}
          <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4 transition-opacity duration-300 ${
            showControls ? 'opacity-100' : 'opacity-0'
          }`}>
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
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                {/* Previous Video */}
                <button
                  onClick={playPrevious}
                  disabled={currentIndex === 0 || playlist.length === 0}
                  className="text-white hover:text-neon-cyan transition-colors disabled:text-gray-600 disabled:cursor-not-allowed"
                  title="Vídeo Anterior"
                >
                  ⏮️
                </button>
                
                <button
                  onClick={() => skip(-10)}
                  className="text-white hover:text-neon-cyan transition-colors"
                  title="Voltar 10s"
                >
                  <SkipBack className="w-5 h-5" />
                </button>

                <button
                  onClick={togglePlay}
                  className="bg-neon-cyan hover:bg-neon-cyan/80 rounded-full p-2 transition-colors"
                >
                  {isPlaying ? (
                    <Pause className="w-5 h-5 text-black" />
                  ) : (
                    <Play className="w-5 h-5 text-black ml-0.5" />
                  )}
                </button>

                <button
                  onClick={() => skip(10)}
                  className="text-white hover:text-neon-cyan transition-colors"
                  title="Avançar 10s"
                >
                  <SkipForward className="w-5 h-5" />
                </button>
                
                {/* Next Video */}
                <button
                  onClick={playNext}
                  disabled={currentIndex >= playlist.length - 1 || playlist.length === 0}
                  className="text-white hover:text-neon-cyan transition-colors disabled:text-gray-600 disabled:cursor-not-allowed"
                  title="Próximo Vídeo"
                >
                  ⏭️
                </button>

                <div className="flex items-center gap-2">
                  <button
                    onClick={toggleMute}
                    className="text-white hover:text-neon-cyan transition-colors"
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
              </div>

              <button
                onClick={toggleFullscreen}
                className="text-white hover:text-neon-cyan transition-colors"
              >
                <Maximize className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
        
        {/* Playlist */}
        {playlist.length > 1 && (
          <div className="p-4 bg-dark-800/30 border-t border-neon-cyan/20 max-h-48 overflow-y-auto">
            <h4 className="text-sm font-semibold text-white mb-3">📋 Playlist ({playlist.length} vídeos)</h4>
            <div className="space-y-2">
              {playlist.map((video, index) => (
                <button
                  key={video.key}
                  onClick={() => {
                    setCurrentIndex(index)
                    onVideoChange?.(video)
                  }}
                  className={`w-full text-left p-2 rounded-lg transition-colors ${
                    index === currentIndex
                      ? 'bg-neon-cyan/20 text-neon-cyan'
                      : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-gray-400 w-6">{index + 1}</span>
                    <span className="text-sm truncate flex-1">{video.name}</span>
                    {index === currentIndex && <span className="text-xs">▶️</span>}
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