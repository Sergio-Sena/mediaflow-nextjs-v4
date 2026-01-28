import { SkeletonProps } from '@/types/components';

export function Skeleton({
  variant = 'text',
  width,
  height,
  className = ''
}: SkeletonProps) {
  const variantStyles = {
    text: 'h-[var(--text-base)] w-full',
    card: 'h-[200px] w-full rounded-[var(--radius-xl)]',
    avatar: 'h-12 w-12 rounded-[var(--radius-full)]',
    video: 'aspect-video w-full rounded-[var(--radius-lg)]'
  };

  return (
    <div
      className={`
        loading-shimmer
        rounded-[var(--radius-md)]
        ${variantStyles[variant]}
        ${className}
      `}
      style={{ width, height }}
      aria-busy="true"
      aria-live="polite"
    />
  );
}
