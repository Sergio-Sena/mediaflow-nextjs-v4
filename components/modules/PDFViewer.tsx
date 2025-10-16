'use client'

import { X, Download, ExternalLink } from 'lucide-react'

interface PDFViewerProps {
  src: string
  title: string
  onClose?: () => void
}

export default function PDFViewer({ src, title, onClose }: PDFViewerProps) {
  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = src
    link.download = title
    link.click()
  }

  const handleOpenNew = () => {
    window.open(src, '_blank')
  }

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="relative w-full max-w-6xl h-[90vh] bg-dark-900 rounded-lg overflow-hidden">
        {/* Header */}
        <div className="flex justify-between items-center p-4 bg-dark-800/50 border-b border-neon-cyan/20">
          <h3 className="text-lg font-semibold text-white truncate flex-1 min-w-0 mr-4" title={title}>{title}</h3>
          <div className="flex gap-2 flex-shrink-0">
            <button onClick={handleOpenNew} className="p-2 text-gray-400 hover:text-white" title="Abrir em nova aba">
              <ExternalLink className="w-4 h-4" />
            </button>
            <button onClick={handleDownload} className="p-2 text-gray-400 hover:text-white" title="Download">
              <Download className="w-4 h-4" />
            </button>
            <button onClick={onClose} className="p-2 text-gray-400 hover:text-white">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* PDF Container */}
        <div className="relative h-full bg-gray-100">
          <iframe
            src={src}
            className="w-full h-full border-0"
            title={title}
          />
        </div>
      </div>
    </div>
  )
}