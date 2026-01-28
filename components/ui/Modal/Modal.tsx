'use client';

import { useEffect } from 'react';
import { ModalProps } from '@/types/components';

export function Modal({ isOpen, onClose, title, children, className = '' }: ModalProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      
      const handleEscape = (e: KeyboardEvent) => {
        if (e.key === 'Escape') onClose();
      };
      
      document.addEventListener('keydown', handleEscape);
      return () => {
        document.body.style.overflow = 'unset';
        document.removeEventListener('keydown', handleEscape);
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/80 backdrop-blur-[4px] z-[9998]"
        onClick={onClose}
        aria-hidden="true"
      />
      
      {/* Modal */}
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? 'modal-title' : undefined}
        className={`
          fixed
          top-1/2
          left-1/2
          -translate-x-1/2
          -translate-y-1/2
          bg-[var(--dark-800)]
          border
          border-[var(--gray-700)]
          rounded-[var(--radius-xl)]
          p-[var(--spacing-8)]
          max-w-[500px]
          w-[90%]
          max-h-[90vh]
          overflow-y-auto
          shadow-[var(--shadow-xl)]
          z-[9999]
          animate-fade-in
          ${className}
        `}
      >
        {title && (
          <h2 id="modal-title" className="text-[var(--text-2xl)] font-bold text-white mb-[var(--spacing-4)]">
            {title}
          </h2>
        )}
        
        {children}
        
        <button
          onClick={onClose}
          className="absolute top-[var(--spacing-4)] right-[var(--spacing-4)] text-[var(--gray-400)] hover:text-white text-2xl"
          aria-label="Fechar modal"
        >
          ×
        </button>
      </div>
    </>
  );
}
