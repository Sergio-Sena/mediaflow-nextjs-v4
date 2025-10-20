'use client'

import { useState, useRef } from 'react'
import { ChevronLeft, ChevronRight, Play, Clock } from 'lucide-react'
import VideoThumbnail from './VideoThumbnail'

interface Video {
  key: string
  name: string
  url: string
  thumbnail?: string
  duration?: string
  progress?: number
}

interface VideoCarouselProps {
  title: string
  videos: Video[]
  onVideoClick: (video: Video) => void
}

export default function VideoCarousel({ title, videos, onVideoClick }: VideoCarouselProps) {
  const scrollRef = useRef<HTMLDivElement>(null)
  const [showLeftArrow, setShowLeftArrow] = useState(false)
  const [showRightArrow, setShowRightArrow] = useState(true)

  const scroll = (direction: 'left' | 'right') => {
    if (scrollRef.current) {
      const scrollAmount = 400
      scrollRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      })
    }
  }

  const handleScroll = () => {
    if (scrollRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current
      setShowLeftArrow(scrollLeft > 0)
      setShowRightArrow(scrollLeft < scrollWidth - clientWidth - 10)
    }
  }

  if (videos.length === 0) return null

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-white mb-4 px-4">{title}</h2>
      
      <div className="relative group">
        {/* Left Arrow */}
        {showLeftArrow && (
          <button
            onClick={() => scroll('left')}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-dark-900/80 hover:bg-dark-900 p-2 rounded-r-lg opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <ChevronLeft className="w-8 h-8 text-white" />
          </button>
        )}

        {/* Carousel */}
        <div
          ref={scrollRef}
          onScroll={handleScroll}
          className="flex gap-4 overflow-x-auto scrollbar-hide px-4 scroll-smooth"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {videos.map((video) => (
            <div
              key={video.key}
              onClick={() => onVideoClick(video)}
              className="flex-shrink-0 w-64 cursor-pointer group/card"
            >
              <div className="relative aspect-video rounded-lg overflow-hidden bg-gradient-to-br from-purple-900/30 to-blue-900/30 transform transition-all duration-300 group-hover/card:scale-105 group-hover/card:z-10">
                {/* Thumbnail */}
                <VideoThumbnail
                  videoUrl={video.url}
                  videoKey={video.key}
                  alt={video.name}
                />

                {/* Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover/card:opacity-100 transition-opacity">
                  <div className="absolute bottom-0 left-0 right-0 p-4">
                    <div className="flex items-center gap-2 text-white">
                      <Play className="w-5 h-5" fill="white" />
                      <span className="text-sm font-semibold">Assistir</span>
                    </div>
                  </div>
                </div>

                {/* Duration */}
                {video.duration && (
                  <div className="absolute top-2 right-2 bg-black/70 px-2 py-1 rounded text-xs text-white flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {video.duration}
                  </div>
                )}

                {/* Progress Bar */}
                {video.progress && video.progress > 0 && (
                  <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-700">
                    <div
                      className="h-full bg-neon-cyan"
                      style={{ width: `${video.progress}%` }}
                    />
                  </div>
                )}
              </div>

              {/* Title */}
              <h3 className="text-white text-sm font-medium mt-2 line-clamp-2 group-hover/card:text-neon-cyan transition-colors">
                {video.name}
              </h3>
            </div>
          ))}
        </div>

        {/* Right Arrow */}
        {showRightArrow && (
          <button
            onClick={() => scroll('right')}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-dark-900/80 hover:bg-dark-900 p-2 rounded-l-lg opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <ChevronRight className="w-8 h-8 text-white" />
          </button>
        )}
      </div>
    </div>
  )
}
