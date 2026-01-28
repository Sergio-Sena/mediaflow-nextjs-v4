import { InputProps } from '@/types/components';

export function Input({
  label,
  error,
  className = '',
  ...props
}: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-[var(--text-sm)] font-medium text-[var(--gray-300)] mb-[var(--spacing-2)]">
          {label}
        </label>
      )}
      <input
        className={`
          w-full
          text-[var(--text-base)]
          px-[var(--spacing-4)]
          py-[var(--spacing-3)]
          bg-[rgba(26,26,26,0.8)]
          border
          ${error ? 'border-[var(--error)]' : 'border-[var(--gray-700)]'}
          rounded-[var(--radius-md)]
          text-white
          transition-all
          duration-200
          focus:outline-none
          focus:border-[var(--neon-cyan)]
          focus:shadow-[0_0_0_3px_rgba(0,255,255,0.1)]
          disabled:opacity-50
          disabled:cursor-not-allowed
          ${className}
        `}
        aria-invalid={!!error}
        aria-describedby={error ? 'input-error' : undefined}
        {...props}
      />
      {error && (
        <p id="input-error" className="text-[var(--text-sm)] text-[var(--error)] mt-[var(--spacing-1)]">
          {error}
        </p>
      )}
    </div>
  );
}
