export function VideoPlayerSkeleton() {
  return (
    <div className="relative w-full aspect-video bg-gray-900 rounded-lg overflow-hidden animate-pulse">
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-gray-700 border-t-gray-500 rounded-full animate-spin" />
      </div>
      <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-black/50 to-transparent" />
    </div>
  )
}
