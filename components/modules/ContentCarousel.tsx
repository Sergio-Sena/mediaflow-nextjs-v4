'use client'

import { useState, useRef, useEffect } from 'react'
import { ChevronLeft, ChevronRight, Play, Image, FileText } from 'lucide-react'

interface ContentItem {
  key: string
  name: string
  size: number
  type: string
  folder: string
}

interface ContentRowProps {
  title: string
  items: ContentItem[]
  onItemClick?: (item: ContentItem) => void
}

function ContentRow({ title, items, onItemClick }: ContentRowProps) {
  const scrollRef = useRef<HTMLDivElement>(null)
  const [showLeft, setShowLeft] = useState(false)
  const [showRight, setShowRight] = useState(false)

  const checkArrows = () => {
    if (!scrollRef.current) return
    const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current
    setShowLeft(scrollLeft > 0)
    setShowRight(scrollLeft < scrollWidth - clientWidth - 10)
  }

  useEffect(() => {
    checkArrows()
    const el = scrollRef.current
    if (el) el.addEventListener('scroll', checkArrows)
    window.addEventListener('resize', checkArrows)
    return () => {
      if (el) el.removeEventListener('scroll', checkArrows)
      window.removeEventListener('resize', checkArrows)
    }
  }, [items])

  const scroll = (direction: 'left' | 'right') => {
    if (!scrollRef.current) return
    const amount = scrollRef.current.clientWidth * 0.75
    scrollRef.current.scrollBy({ left: direction === 'left' ? -amount : amount, behavior: 'smooth' })
  }

  if (items.length === 0) return null

  const getGradient = (type: string) => {
    switch (type) {
      case 'video': return 'from-purple-900/80 to-purple-600/40'
      case 'image': return 'from-emerald-900/80 to-emerald-600/40'
      case 'document': return 'from-blue-900/80 to-blue-600/40'
      default: return 'from-gray-900/80 to-gray-600/40'
    }
  }

  const getIcon = (type: string) => {
    switch (type) {
      case 'video': return <Play className="w-6 h-6 sm:w-8 sm:h-8" />
      case 'image': return <Image className="w-6 h-6 sm:w-8 sm:h-8" />
      default: return <FileText className="w-6 h-6 sm:w-8 sm:h-8" />
    }
  }

  const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`
  }

  return (
    <div className="mb-5">
      <h3 className="text-sm sm:text-base font-bold text-white mb-2">
        {title} <span className="text-gray-500 text-xs font-normal">({items.length})</span>
      </h3>

      <div className="flex items-center gap-1">
        {/* Left Arrow */}
        <button
          onClick={() => scroll('left')}
          className={`flex-shrink-0 w-7 h-7 sm:w-9 sm:h-9 rounded-full bg-dark-800/80 border border-cyan-400/30 flex items-center justify-center text-cyan-300 hover:bg-cyan-400/20 transition-all ${showLeft ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
        >
          <ChevronLeft className="w-4 h-4 sm:w-5 sm:h-5" />
        </button>

        {/* Scroll area */}
        <div
          ref={scrollRef}
          className="flex gap-2 sm:gap-3 overflow-x-auto flex-1 py-1"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {items.map((item) => (
            <div
              key={item.key}
              onClick={() => onItemClick?.(item)}
              className="flex-shrink-0 w-[140px] sm:w-[170px] md:w-[190px] lg:w-[210px] cursor-pointer group"
            >
              <div className={`relative aspect-video rounded-lg overflow-hidden bg-gradient-to-br ${getGradient(item.type)} border border-white/5 transition-all duration-300 group-hover:scale-105 group-hover:border-neon-cyan/50 group-hover:shadow-lg group-hover:shadow-neon-cyan/20`}>
                <div className="absolute inset-0 flex items-center justify-center text-white/60 group-hover:text-white/90 transition-colors">
                  {getIcon(item.type)}
                </div>
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div className="bg-neon-cyan/90 rounded-full p-1.5 sm:p-2">
                    <Play className="w-4 h-4 sm:w-5 sm:h-5 text-black" fill="black" />
                  </div>
                </div>
                <div className="absolute top-1.5 right-1.5 px-1.5 py-0.5 rounded text-[9px] sm:text-[10px] font-bold bg-black/60 text-white/80">
                  {formatSize(item.size)}
                </div>
              </div>
              <p className="mt-1.5 text-xs sm:text-sm text-white truncate font-medium group-hover:text-neon-cyan transition-colors" title={item.name}>
                {item.name}
              </p>
            </div>
          ))}
        </div>

        {/* Right Arrow */}
        <button
          onClick={() => scroll('right')}
          className={`flex-shrink-0 w-7 h-7 sm:w-9 sm:h-9 rounded-full bg-dark-800/80 border border-cyan-400/30 flex items-center justify-center text-cyan-300 hover:bg-cyan-400/20 transition-all ${showRight ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
        >
          <ChevronRight className="w-4 h-4 sm:w-5 sm:h-5" />
        </button>
      </div>
    </div>
  )
}

interface ContentCarouselProps {
  files: ContentItem[]
  onItemClick?: (file: ContentItem) => void
}

export default function ContentCarousel({ files, onItemClick }: ContentCarouselProps) {
  // Group by folder
  const grouped: Record<string, ContentItem[]> = {}
  files.forEach(file => {
    const folder = file.folder || 'Raiz'
    if (!grouped[folder]) grouped[folder] = []
    grouped[folder].push(file)
  })

  // Sort by item count descending
  const sorted = Object.entries(grouped).sort((a, b) => b[1].length - a[1].length)

  return (
    <div className="mt-4">
      {sorted.map(([folder, items]) => (
        <ContentRow
          key={folder}
          title={folder === 'root' ? '📁 Raiz' : `📁 ${folder.split('/').pop()}`}
          items={items}
          onItemClick={onItemClick}
        />
      ))}
    </div>
  )
}
