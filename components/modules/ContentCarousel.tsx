'use client'

import { useState, useRef, useEffect } from 'react'
import { ChevronLeft, ChevronRight, Play, Trash2, Share2, CheckSquare, Square } from 'lucide-react'

const BUCKET_URL = process.env.NEXT_PUBLIC_S3_BUCKET_URL || 'https://mediaflow-uploads-969430605054.s3.amazonaws.com'

function getThumbnailUrl(key: string): string {
  // key: users/sergio_sena/Star/Kate Kuray/file.mp4
  // thumb: public/thumbnails/sergio_sena/Star/Kate Kuray/file.jpg
  const parts = key.split('/')
  if (parts.length >= 3 && parts[0] === 'users') {
    const thumbPath = 'public/thumbnails/' + parts.slice(1).join('/').replace(/\.[^.]+$/, '.jpg')
    return `${BUCKET_URL}/${thumbPath}`
  }
  return ''
}

function ThumbnailImage({ itemKey }: { itemKey: string }) {
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState(false)
  const [visible, setVisible] = useState(false)
  const ref = useRef<HTMLDivElement>(null)
  const thumbUrl = getThumbnailUrl(itemKey)

  useEffect(() => {
    if (!ref.current) return
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.disconnect() } },
      { rootMargin: '200px' }
    )
    observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={ref} className="absolute inset-0">
      {visible && thumbUrl && !error && (
        <img
          src={thumbUrl}
          alt=""
          loading="lazy"
          className={`absolute inset-0 w-full h-full object-cover transition-opacity ${loaded ? 'opacity-100' : 'opacity-0'}`}
          onLoad={() => setLoaded(true)}
          onError={() => setError(true)}
        />
      )}
    </div>
  )
}

interface ContentItem {
  key: string
  name: string
  size: number
  type: string
  folder: string
  lastModified?: string
  duration?: number
}

interface ContentRowProps {
  title: string
  items: ContentItem[]
  onItemClick?: (item: ContentItem) => void
  onItemDelete?: (item: ContentItem) => void
  onItemShare?: (item: ContentItem) => void
  onDeleteAll?: (items: ContentItem[]) => void
  selectionMode: boolean
  selectedKeys: Set<string>
  onToggleSelect?: (key: string) => void
}

function ContentRow({ title, items, onItemClick, onItemDelete, onItemShare, onDeleteAll, selectionMode, selectedKeys, onToggleSelect }: ContentRowProps) {
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



  const formatDuration = (secs: number) => {
    if (!secs) return null
    const h = Math.floor(secs / 3600)
    const m = Math.floor((secs % 3600) / 60)
    const s = secs % 60
    if (h > 0) return `${h}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`
    return `${m}:${String(s).padStart(2,'0')}`
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
      <div className="flex items-center gap-2 mb-2">
        <h3 className="text-sm sm:text-base font-bold text-white">
          {title} <span className="text-gray-500 text-xs font-normal">({items.length})</span>
        </h3>
        {onDeleteAll && (
          <button
            onClick={() => onDeleteAll(items)}
            className="p-1.5 text-gray-500 hover:text-red-400 hover:bg-red-600/10 rounded transition-colors"
            title={`Excluir pasta ${title}`}
          >
            <Trash2 className="w-5 h-5" />
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
                className={`flex-shrink-0 w-[calc(50vw-20px)] landscape:w-[calc(40vw-20px)] sm:w-48 md:w-52 lg:w-48 cursor-pointer group ${isSelected ? 'ring-2 ring-neon-cyan rounded-xl' : ''}`}
              >
                <div
                  onClick={() => {
                    if (selectionMode) {
                      onToggleSelect?.(item.key)
                    } else {
                      onItemClick?.(item)
                    }
                  }}
                  className={`relative aspect-video rounded-xl overflow-hidden bg-gradient-to-br ${getGradient(item.type)} border border-white/5 transition-all duration-300 md:group-hover:scale-105 md:group-hover:border-neon-cyan/50 md:group-hover:shadow-lg md:group-hover:shadow-neon-cyan/20`}
                >
                  <ThumbnailImage itemKey={item.key} />
                  {/* Play overlay — desktop hover only */}
                  <div className="absolute inset-0 bg-black/20 opacity-0 md:group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-r from-cyan-500/20 to-purple-500/20 backdrop-blur-sm flex items-center justify-center">
                      <Play className="w-4 h-4 text-cyan-300" fill="currentColor" />
                    </div>
                  </div>
                  {/* Size badge */}
                  <div className="absolute top-1.5 right-1.5 px-1.5 py-0.5 rounded text-[9px] font-bold bg-black/60 text-white/80">
                    {formatSize(item.size)}
                  </div>
                  {/* Duration badge */}
                  {item.duration ? (
                    <div className="absolute bottom-1.5 left-1.5 px-1.5 py-0.5 rounded text-[9px] font-bold bg-black/70 text-white/90">
                      {formatDuration(item.duration)}
                    </div>
                  ) : null}
                  {/* Checkbox selection mode */}
                  {selectionMode && (
                    <div className="absolute top-1.5 left-1.5">
                      {isSelected
                        ? <CheckSquare className="w-5 h-5 text-neon-cyan drop-shadow" />
                        : <Square className="w-5 h-5 text-white/60" />
                      }
                    </div>
                  )}
                  {/* Action buttons — always visible on mobile, hover on desktop */}
                  {!selectionMode && (
                    <div className="absolute top-1.5 left-1.5 flex gap-1 md:opacity-0 md:group-hover:opacity-100 transition-opacity">
                      {onItemShare && (
                        <button
                          onClick={(e) => { e.stopPropagation(); onItemShare(item) }}
                          className="p-1.5 rounded-lg bg-[#667eea]/80 hover:bg-[#667eea] text-white transition-colors"
                          title="Compartilhar"
                        >
                          <Share2 className="w-3 h-3" />
                        </button>
                      )}
                      {onItemDelete && (
                        <button
                          onClick={(e) => { e.stopPropagation(); onItemDelete(item) }}
                          className="p-1.5 rounded-lg bg-red-600/80 hover:bg-red-600 text-white transition-colors"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      )}
                    </div>
                  )}
                </div>
                <p className="mt-1.5 text-xs text-white truncate font-medium" title={item.name}>
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
  onItemShare?: (file: ContentItem) => void
  onBulkDelete?: (files: ContentItem[]) => void
  selectedKeys?: Set<string>
  onToggleSelect?: (key: string) => void
  selectionMode?: boolean
  sortBy?: 'name' | 'size' | 'date'
  sortOrder?: 'asc' | 'desc'
}

export default function ContentCarousel({ files, onItemClick, onItemDelete, onItemShare, onBulkDelete, selectedKeys = new Set(), onToggleSelect, selectionMode = false, sortBy = 'name', sortOrder = 'asc' }: ContentCarouselProps) {
  const sortItems = (items: ContentItem[]) => [...items].sort((a, b) => {
    let cmp = 0
    if (sortBy === 'name') cmp = a.name.localeCompare(b.name)
    else if (sortBy === 'size') cmp = a.size - b.size
    else cmp = new Date(a.lastModified ?? 0).getTime() - new Date(b.lastModified ?? 0).getTime()
    return sortOrder === 'asc' ? cmp : -cmp
  })

  // Group by folder
  const grouped: Record<string, ContentItem[]> = {}
  files.forEach(file => {
    const folder = file.folder || 'Raiz'
    if (!grouped[folder]) grouped[folder] = []
    grouped[folder].push(file)
  })

  const sorted = Object.entries(grouped).sort((a, b) => a[0].localeCompare(b[0]))

  return (
    <div className="mt-4">
      {sorted.map(([folder, items]) => (
        <ContentRow
          key={folder}
          title={folder === 'root' ? '📁 Raiz' : `📁 ${folder.split('/').pop()}`}
          items={sortItems(items)}
          onItemClick={onItemClick}
          onItemDelete={onItemDelete}
          onItemShare={onItemShare}
          onDeleteAll={onBulkDelete}
          selectionMode={selectionMode}
          selectedKeys={selectedKeys}
          onToggleSelect={onToggleSelect}
        />
      ))}
    </div>
  )
}
