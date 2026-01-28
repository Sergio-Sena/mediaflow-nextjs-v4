'use client'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'primary' | 'secondary' | 'minimal'
  text?: string
  fullScreen?: boolean
}

export default function LoadingSpinner({ 
  size = 'md', 
  variant = 'primary', 
  text,
  fullScreen = false 
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8', 
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  }

  const textSizes = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base', 
    xl: 'text-lg'
  }

  const Spinner = () => (
    <div className="relative">
      {variant === 'primary' && (
        <div className={`${sizeClasses[size]} relative`}>
          <div className="absolute inset-0 rounded-full border-2 border-neon-cyan/20"></div>
          <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-neon-cyan animate-spin"></div>
          <div className="absolute inset-2 rounded-full border border-neon-purple/40 border-t-transparent animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
        </div>
      )}
      
      {variant === 'secondary' && (
        <div className={`${sizeClasses[size]} relative`}>
          <div className="absolute inset-0 rounded-full bg-gradient-to-r from-neon-cyan via-neon-purple to-neon-pink opacity-20"></div>
          <div className="absolute inset-0 rounded-full bg-gradient-to-r from-neon-cyan via-neon-purple to-neon-pink animate-spin" 
               style={{ 
                 background: 'conic-gradient(from 0deg, #00ffff, #bf00ff, #ff0080, #00ffff)',
                 mask: 'radial-gradient(circle at center, transparent 60%, black 65%)',
                 WebkitMask: 'radial-gradient(circle at center, transparent 60%, black 65%)'
               }}>
          </div>
        </div>
      )}
      
      {variant === 'minimal' && (
        <div className={`${sizeClasses[size]} grid grid-cols-2 gap-1`}>
          <div className="bg-neon-cyan rounded-sm animate-pulse" style={{ animationDelay: '0ms' }}></div>
          <div className="bg-neon-purple rounded-sm animate-pulse" style={{ animationDelay: '150ms' }}></div>
          <div className="bg-neon-pink rounded-sm animate-pulse" style={{ animationDelay: '300ms' }}></div>
          <div className="bg-neon-blue rounded-sm animate-pulse" style={{ animationDelay: '450ms' }}></div>
        </div>
      )}
    </div>
  )

  const content = (
    <div className="flex flex-col items-center gap-4">
      <Spinner />
      {text && (
        <p className={`text-gray-300 font-medium ${textSizes[size]} animate-pulse`}>
          {text}
        </p>
      )}
    </div>
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-dark-900/80 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="card-elevated p-8">
          {content}
        </div>
      </div>
    )
  }

  return content
}

// Skeleton Loader Component
interface SkeletonProps {
  className?: string
  variant?: 'text' | 'rectangular' | 'circular'
  animation?: 'pulse' | 'wave'
}

export function Skeleton({ 
  className = '', 
  variant = 'rectangular',
  animation = 'pulse' 
}: SkeletonProps) {
  const baseClasses = 'bg-gradient-to-r from-gray-700 via-gray-600 to-gray-700 bg-[length:200%_100%]'
  
  const variantClasses = {
    text: 'h-4 rounded',
    rectangular: 'rounded-lg',
    circular: 'rounded-full'
  }
  
  const animationClasses = {
    pulse: 'animate-pulse',
    wave: 'animate-shimmer'
  }

  return (
    <div 
      className={`${baseClasses} ${variantClasses[variant]} ${animationClasses[animation]} ${className}`}
    />
  )
}