'use client';

import { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { ToastProps, ToastContextType, ToastType } from '@/types/components';

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastProps[]>([]);

  const addToast = useCallback((type: ToastType, message: string, duration = 5000) => {
    const id = Math.random().toString(36).substr(2, 9);
    const toast: ToastProps = { id, type, message, duration };
    
    setToasts((prev) => [...prev, toast]);

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
      {children}
      <div className="fixed top-[var(--spacing-4)] right-[var(--spacing-4)] z-[9999] flex flex-col gap-[var(--spacing-2)]">
        {toasts.map((toast) => (
          <Toast key={toast.id} {...toast} onClose={() => removeToast(toast.id)} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
}

function Toast({ type, message, onClose }: ToastProps & { onClose: () => void }) {
  const typeStyles = {
    success: 'bg-[var(--success)] text-white border-l-[#059669]',
    error: 'bg-[var(--error)] text-white border-l-[#dc2626]',
    warning: 'bg-[var(--warning)] text-[var(--dark-900)] border-l-[#d97706]',
    info: 'bg-[var(--info)] text-white border-l-[#2563eb]'
  };

  return (
    <div
      role="alert"
      aria-live="polite"
      aria-atomic="true"
      className={`
        ${typeStyles[type]}
        px-[var(--spacing-6)]
        py-[var(--spacing-4)]
        rounded-[var(--radius-lg)]
        shadow-[var(--shadow-lg)]
        border-l-4
        min-w-[300px]
        max-w-[500px]
        animate-slide-down
        flex
        items-center
        justify-between
        gap-[var(--spacing-4)]
      `}
    >
      <span className="text-[var(--text-base)]">{message}</span>
      <button
        onClick={onClose}
        className="text-xl hover:opacity-70 transition-opacity"
        aria-label="Fechar notificação"
      >
        ×
      </button>
    </div>
  );
}
