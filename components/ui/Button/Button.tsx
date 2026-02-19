import { ButtonProps } from '@/types/components';

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  children,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles = 'font-medium transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variantStyles = {
    primary: 'bg-gradient-to-br from-[var(--neon-cyan)] to-[#0080ff] text-[var(--dark-900)] font-semibold shadow-[0_4px_20px_rgba(0,255,255,0.3)] hover:shadow-[0_6px_30px_rgba(0,255,255,0.5)] hover:-translate-y-0.5',
    secondary: 'bg-white/[0.08] text-white border border-white/[0.15] backdrop-blur-[10px] hover:bg-white/[0.12] hover:border-[var(--neon-cyan)]',
    ghost: 'bg-transparent text-[var(--gray-300)] border border-white/[0.1] hover:bg-white/[0.05] hover:text-white',
    danger: 'bg-gradient-to-br from-[var(--error)] to-[#cc0066] text-white font-semibold hover:shadow-[0_4px_20px_rgba(239,68,68,0.4)]'
  };

  const sizeStyles = {
    sm: 'text-[var(--text-sm)] px-[var(--spacing-4)] py-[var(--spacing-2)] rounded-[var(--radius-md)]',
    md: 'text-[var(--text-base)] px-[var(--spacing-6)] py-[var(--spacing-3)] rounded-[var(--radius-lg)]',
    lg: 'text-[var(--text-lg)] px-[var(--spacing-8)] py-[var(--spacing-4)] rounded-[var(--radius-xl)]'
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="flex items-center justify-center gap-2">
          <span className="animate-spin">⏳</span>
          {children}
        </span>
      ) : (
        children
      )}
    </button>
  );
}
