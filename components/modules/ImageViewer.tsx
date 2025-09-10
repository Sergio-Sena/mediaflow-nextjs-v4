'use client'

import { useState } from 'react'
import { X, Download, ZoomIn, ZoomOut, RotateCw } from 'lucide-react'

interface ImageViewerProps {
  src: string
  title: string
  onClose?: () => void
}

export default function ImageViewer({ src, title, onClose }: ImageViewerProps) {
  const [zoom, setZoom] = useState(1)
  const [rotation, setRotation] = useState(0)

  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.25, 3))
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.25, 0.25))
  const handleRotate = () => setRotation(prev => (prev + 90) % 360)
  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = src
    link.download = title
    link.click()
  }

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="relative w-full max-w-6xl bg-dark-900 rounded-lg overflow-hidden">
        {/* Header */}
        <div className="flex justify-between items-center p-4 bg-dark-800/50 border-b border-neon-cyan/20">
          <h3 className="text-lg font-semibold text-white truncate">{title}</h3>
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
        <div className="relative bg-black overflow-auto max-h-[80vh] flex items-center justify-center">
          <img
            src={src}
            alt={title}
            className="max-w-none transition-transform duration-200"
            style={{
              transform: `scale(${zoom}) rotate(${rotation}deg)`,
              maxHeight: zoom === 1 ? '80vh' : 'none',
              maxWidth: zoom === 1 ? '100%' : 'none'
            }}
          />
        </div>
      </div>
    </div>
  )
}