'use client'

import { Play, Info } from 'lucide-react'
import VideoThumbnail from './VideoThumbnail'

interface HeroSectionProps {
  video?: {
    name: string
    url: string
    thumbnail?: string
    description?: string
  }
  onPlay: () => void
}

export default function HeroSection({ video, onPlay }: HeroSectionProps) {
  if (!video) return null

  return (
    <div className="relative h-[70vh] w-full overflow-hidden rounded-lg mb-8">
      {/* Background */}
      <div className="absolute inset-0">
        <VideoThumbnail
          videoUrl={video.url}
          videoKey={video.name}
          alt={video.name}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark-900 via-dark-900/60 to-transparent" />
      </div>

      {/* Content */}
      <div className="relative h-full flex flex-col justify-end p-8 md:p-12">
        <div className="max-w-2xl">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 drop-shadow-lg">
            {video.name}
          </h1>
          
          {video.description && (
            <p className="text-lg text-gray-200 mb-6 line-clamp-3">
              {video.description}
            </p>
          )}

          <div className="flex gap-4">
            <button
              onClick={onPlay}
              className="flex items-center gap-2 bg-white text-dark-900 px-8 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-all transform hover:scale-105"
            >
              <Play className="w-6 h-6" fill="currentColor" />
              Assistir
            </button>
            
            <button className="flex items-center gap-2 bg-gray-500/50 backdrop-blur-sm text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-500/70 transition-all">
              <Info className="w-6 h-6" />
              Mais Info
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
