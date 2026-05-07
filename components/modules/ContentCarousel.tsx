'use client'

import { useState, useRef, useEffect } from 'react'
import { ChevronLeft, ChevronRight, Play, Image, FileText, Trash2, CheckSquare, Square } from 'lucide-react'

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
  onItemDelete?: (item: ContentItem) => void
  onDeleteAll?: (items: ContentItem[]) => void
  selectionMode: boolean
  selectedKeys: Set<string>
  onToggleSelect?: (key: string) => void
}

function ContentRow({ title, items, onItemClick, onItemDelete, onDeleteAll, selectionMode, selectedKeys, onToggleSelect }: ContentRowProps) {
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

  const selectedInRow = items.filter(i => selectedKeys.has(i.key)).length

  return (
    <div className="mb-5">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm sm:text-base font-bold text-white">
          {title} <span className="text-gray-500 text-xs font-normal">({items.length})</span>
        </h3>
        {onDeleteAll && (
          <button
            onClick={() => {
              if (confirm(`Excluir todos os ${items.length} arquivos de "${title.replace('📁 ', '')}"?`)) {
                onDeleteAll(items)
              }
            }}
            className="p-1.5 text-gray-500 hover:text-red-400 hover:bg-red-600/10 rounded transition-colors"
            title={`Excluir pasta ${title}`}
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}
      </div>

      <div className="flex items-center gap-0.5">
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
          {items.map((item) => {
            const isSelected = selectedKeys.has(item.key)
            return (
              <div
                key={item.key}
                onClick={() => {
                  if (selectionMode) {
                    onToggleSelect?.(item.key)
                  } else {
                    onItemClick?.(item)
                  }
                }}
                className={`flex-shrink-0 w-[140px] sm:w-[170px] md:w-[190px] lg:w-[210px] cursor-pointer group ${isSelected ? 'ring-2 ring-neon-cyan rounded-lg' : ''}`}
              >
                <div className={`relative aspect-video rounded-lg overflow-hidden bg-gradient-to-br ${getGradient(item.type)} border border-white/5 transition-all duration-300 group-hover:scale-105 group-hover:border-neon-cyan/50 group-hover:shadow-lg group-hover:shadow-neon-cyan/20`}>
                  <div className="absolute inset-0 flex items-center justify-center text-white/60 group-hover:text-white/90 transition-colors">
                    {getIcon(item.type)}
                  </div>
                  {!selectionMode && (
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <div className="bg-neon-cyan/90 rounded-full p-1.5 sm:p-2">
                        <Play className="w-4 h-4 sm:w-5 sm:h-5 text-black" fill="black" />
                      </div>
                    </div>
                  )}
                  <div className="absolute top-1.5 right-1.5 px-1.5 py-0.5 rounded text-[9px] sm:text-[10px] font-bold bg-black/60 text-white/80">
                    {formatSize(item.size)}
                  </div>
                  {/* Delete button on hover (non-selection mode) */}
                  {!selectionMode && onItemDelete && (
                    <button
                      onClick={(e) => { e.stopPropagation(); onItemDelete(item) }}
                      className="absolute top-1.5 left-1.5 p-1.5 rounded bg-red-600/80 hover:bg-red-600 text-white transition-colors opacity-0 group-hover:opacity-100"
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  )}
                  {/* Checkbox in selection mode */}
                  {selectionMode && (
                    <div className="absolute top-1.5 left-1.5">
                      {isSelected
                        ? <CheckSquare className="w-5 h-5 text-neon-cyan" />
                        : <Square className="w-5 h-5 text-white/60" />
                      }
                    </div>
                  )}
                </div>
                <p className="mt-1.5 text-xs sm:text-sm text-white truncate font-medium group-hover:text-neon-cyan transition-colors" title={item.name}>
                  {item.name}
                </p>
              </div>
            )
          })}
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
  onItemDelete?: (file: ContentItem) => void
  onBulkDelete?: (files: ContentItem[]) => void
  selectedKeys?: Set<string>
  onToggleSelect?: (key: string) => void
  selectionMode?: boolean
}

export default function ContentCarousel({ files, onItemClick, onItemDelete, onBulkDelete, selectedKeys = new Set(), onToggleSelect, selectionMode = false }: ContentCarouselProps) {
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
          onItemDelete={onItemDelete}
          onDeleteAll={onBulkDelete}
          selectionMode={selectionMode}
          selectedKeys={selectedKeys}
          onToggleSelect={onToggleSelect}
        />
      ))}
    </div>
  )
}
