import { BadgeProps } from '@/types/components';

export function Badge({ variant = 'default', children, className = '' }: BadgeProps) {
  const variantStyles = {
    default: 'bg-[var(--gray-700)] text-[var(--gray-200)]',
    success: 'bg-[rgba(16,185,129,0.2)] text-[var(--success)] border border-[var(--success)]',
    error: 'bg-[rgba(239,68,68,0.2)] text-[var(--error)] border border-[var(--error)]',
    warning: 'bg-[rgba(245,158,11,0.2)] text-[var(--warning)] border border-[var(--warning)]'
  };

  return (
    <span
      className={`
        inline-flex
        items-center
        text-[var(--text-xs)]
        font-medium
        px-[var(--spacing-2)]
        py-[var(--spacing-1)]
        rounded-[var(--radius-full)]
        ${variantStyles[variant]}
        ${className}
      `}
    >
      {children}
    </span>
  );
}
