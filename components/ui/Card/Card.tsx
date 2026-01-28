import { CardProps } from '@/types/components';

export function Card({
  variant = 'elevated',
  padding = 'md',
  children,
  className = ''
}: CardProps) {
  const variantStyles = {
    elevated: 'bg-[rgba(26,26,26,0.8)] backdrop-blur-[20px] border border-[var(--gray-800)] shadow-[var(--shadow-lg)] hover:-translate-y-1 hover:shadow-[var(--shadow-xl)] hover:border-[rgba(0,255,255,0.2)]',
    glass: 'bg-[rgba(26,26,26,0.7)] backdrop-blur-[10px] border border-[rgba(0,255,255,0.1)] shadow-[0_8px_32px_rgba(0,255,255,0.1)]',
    flat: 'bg-[rgba(26,26,26,0.6)] border border-[var(--gray-800)]'
  };

  const paddingStyles = {
    sm: 'p-[var(--spacing-4)]',
    md: 'p-[var(--spacing-6)]',
    lg: 'p-[var(--spacing-8)]'
  };

  return (
    <div
      className={`
        rounded-[var(--radius-xl)]
        transition-all
        duration-300
        ${variantStyles[variant]}
        ${paddingStyles[padding]}
        ${className}
      `}
    >
      {children}
    </div>
  );
}
