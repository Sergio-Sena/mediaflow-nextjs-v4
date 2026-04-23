'use client'

import { useState, useEffect } from 'react'
import { X, Download, ZoomIn, ZoomOut, RotateCw, ChevronLeft, ChevronRight } from 'lucide-react'

const getPresignedUrl = async (key: string): Promise<string | null> => {
  const token = localStorage.getItem('token')
  if (!token) return null
  try {
    const res = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(key)}`, {
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      const data = await res.json()
      if (data.success && data.viewUrl) return data.viewUrl
    }
  } catch (e) {
    console.error('Presigned URL error:', e)
  }
  return null
}

interface ImageFile {
  key: string
  name: string
  url: string
  folder: string
}

interface ImageViewerProps {
  src: string
  title: string
  currentImage?: ImageFile
  playlist?: ImageFile[]
  onClose?: () => void
  onImageChange?: (image: ImageFile) => void
}

export default function ImageViewer({ src, title, currentImage, playlist = [], onClose, onImageChange }: ImageViewerProps) {
  const [zoom, setZoom] = useState(1)
  const [rotation, setRotation] = useState(0)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [currentSrc, setCurrentSrc] = useState(src)
  const [touchStart, setTouchStart] = useState<number | null>(null)
  const [touchEnd, setTouchEnd] = useState<number | null>(null)
  
  // Update current index and source when currentImage changes
  useEffect(() => {
    if (currentImage && playlist.length > 0) {
      const index = playlist.findIndex(img => img.key === currentImage.key)
      if (index !== -1) {
        setCurrentIndex(index)
        setCurrentSrc(currentImage.url)
        // Reset zoom and rotation when changing images
        setZoom(1)
        setRotation(0)
      }
    }
  }, [currentImage, playlist])
  
  // Get presigned URL for initial image
  useEffect(() => {
    if (currentImage?.key) {
      getPresignedUrl(currentImage.key).then(url => {
        if (url) setCurrentSrc(url)
      })
    } else {
      setCurrentSrc(src)
    }
  }, [src, currentImage])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose?.()
      } else if (e.key === 'ArrowLeft') {
        goToPrevious()
      } else if (e.key === 'ArrowRight') {
        goToNext()
      }
    }
    
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [currentIndex, playlist.length])

  // Touch/Swipe support
  const minSwipeDistance = 50

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null)
    setTouchStart(e.targetTouches[0].clientX)
  }

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX)
  }

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return
    
    const distance = touchStart - touchEnd
    const isLeftSwipe = distance > minSwipeDistance
    const isRightSwipe = distance < -minSwipeDistance

    if (isLeftSwipe && playlist.length > 1) {
      goToNext()
    }
    if (isRightSwipe && playlist.length > 1) {
      goToPrevious()
    }
  }

  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.25, 3))
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.25, 0.25))
  const handleRotate = () => setRotation(prev => (prev + 90) % 360)
  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = currentSrc
    link.download = title
    link.click()
  }
  
  const goToNext = async () => {
    if (playlist.length === 0) return
    
    const nextIndex = currentIndex + 1
    if (nextIndex < playlist.length) {
      const nextImage = playlist[nextIndex]
      setCurrentIndex(nextIndex)
      
      const url = await getPresignedUrl(nextImage.key)
      if (url) {
        setCurrentSrc(url)
        onImageChange?.({ ...nextImage, url })
      } else {
        onImageChange?.(nextImage)
      }
    }
  }
  
  const goToPrevious = async () => {
    if (playlist.length === 0) return
    
    const prevIndex = currentIndex - 1
    if (prevIndex >= 0) {
      const prevImage = playlist[prevIndex]
      setCurrentIndex(prevIndex)
      
      const url = await getPresignedUrl(prevImage.key)
      if (url) {
        setCurrentSrc(url)
        onImageChange?.({ ...prevImage, url })
      } else {
        onImageChange?.(prevImage)
      }
    }
  }

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-2 sm:p-4">
      <div className="relative w-full max-w-6xl bg-dark-900 rounded-lg overflow-hidden">
        {/* Header */}
        <div className="flex justify-between items-center p-2 sm:p-4 bg-dark-800/50 border-b border-neon-cyan/20">
          <div className="flex-1 min-w-0">
            <h3 className="text-sm sm:text-lg font-semibold text-white truncate" title={title}>{title}</h3>
            {playlist.length > 0 && (
              <p className="text-sm text-gray-400 truncate" title={currentImage?.folder}>
                {currentIndex + 1} de {playlist.length} • 📁 {currentImage?.folder || 'Pasta'}
              </p>
            )}
          </div>
          <div className="flex gap-2">
            <button onClick={handleZoomOut} className="p-2 text-gray-400 hover:text-white">
              <ZoomOut className="w-4 h-4" />
            </button>
            <span className="px-2 py-1 text-sm text-gray-400">{Math.round(zoom * 100)}%</span>
            <button onClick={handleZoomIn} className="p-2 text-gray-400 hover:text-white">
              <ZoomIn className="w-4 h-4" />
            </button>
            <button onClick={handleRotate} className="p-2 text-gray-400 hover:text-white">
              <RotateCw className="w-4 h-4" />
            </button>
            <button onClick={handleDownload} className="p-2 text-gray-400 hover:text-white">
              <Download className="w-4 h-4" />
            </button>
            <button onClick={onClose} className="p-2 text-gray-400 hover:text-white">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Image Container */}
        <div 
          className="relative bg-black overflow-auto max-h-[70vh] sm:max-h-[80vh] flex items-center justify-center group"
          onTouchStart={onTouchStart}
          onTouchMove={onTouchMove}
          onTouchEnd={onTouchEnd}
        >
          {/* Previous Button - Left Side */}
          {playlist.length > 1 && currentIndex > 0 && (
            <button
              onClick={goToPrevious}
              className="absolute left-2 sm:left-4 top-1/2 -translate-y-1/2 z-10 bg-black/60 hover:bg-black/80 text-white p-2 sm:p-4 rounded-full opacity-0 group-hover:opacity-100 transition-all duration-300 hover:scale-110 border border-white/20"
              title="Imagem Anterior (←)"
            >
              <ChevronLeft className="w-4 h-4 sm:w-6 sm:h-6" />
            </button>
          )}
          
          {/* Next Button - Right Side */}
          {playlist.length > 1 && currentIndex < playlist.length - 1 && (
            <button
              onClick={goToNext}
              className="absolute right-2 sm:right-4 top-1/2 -translate-y-1/2 z-10 bg-black/60 hover:bg-black/80 text-white p-2 sm:p-4 rounded-full opacity-0 group-hover:opacity-100 transition-all duration-300 hover:scale-110 border border-white/20"
              title="Próxima Imagem (→)"
            >
              <ChevronRight className="w-4 h-4 sm:w-6 sm:h-6" />
            </button>
          )}
          
          <img
            src={currentSrc}
            alt={title}
            className="max-w-none transition-transform duration-200"
            style={{
              transform: `scale(${zoom}) rotate(${rotation}deg)`,
              maxHeight: zoom === 1 ? '80vh' : 'none',
              maxWidth: zoom === 1 ? '100%' : 'none'
            }}
            key={currentSrc}
          />
        </div>
        
        {/* Image Playlist */}
        {playlist.length > 1 && (
          <div className="p-2 sm:p-4 bg-dark-800/30 border-t border-neon-cyan/20 max-h-32 sm:max-h-48 overflow-y-auto">
            <h4 className="text-sm font-semibold text-white mb-3">📸 Galeria ({playlist.length} imagens)</h4>
            <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10 gap-1 sm:gap-2">
              {playlist.map((image, index) => (
                <button
                  key={image.key}
                  onClick={() => {
                    setCurrentIndex(index)
                    onImageChange?.(image)
                  }}
                  className={`relative aspect-square rounded-lg overflow-hidden transition-all duration-200 ${
                    index === currentIndex
                      ? 'ring-2 ring-neon-cyan scale-105'
                      : 'hover:scale-105 opacity-70 hover:opacity-100'
                  }`}
                  title={image.name}
                >
                  <img
                    src={image.url}
                    alt={image.name}
                    className="w-full h-full object-cover"
                    loading="lazy"
                  />
                  {index === currentIndex && (
                    <div className="absolute inset-0 bg-neon-cyan/20 flex items-center justify-center">
                      <span className="text-white text-xs font-bold">▶️</span>
                    </div>
                  )}
                  <div className="absolute bottom-0 left-0 right-0 bg-black/50 text-white text-xs p-1 truncate">
                    {index + 1}
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