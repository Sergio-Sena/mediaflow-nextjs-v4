// Tipos base para todos os componentes UI
import { ReactNode, ButtonHTMLAttributes, InputHTMLAttributes } from 'react';

// Tipos comuns
export type Size = 'sm' | 'md' | 'lg';
export type Variant = 'primary' | 'secondary' | 'ghost' | 'danger';
export type ToastType = 'success' | 'error' | 'warning' | 'info';
export type CardVariant = 'elevated' | 'glass' | 'flat';
export type BadgeVariant = 'default' | 'success' | 'error' | 'warning';

// Base props
export interface BaseComponentProps {
  className?: string;
  children?: ReactNode;
}

// Button
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  loading?: boolean;
  children: ReactNode;
}

// Input
export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

// Card
export interface CardProps extends BaseComponentProps {
  variant?: CardVariant;
  padding?: Size;
}

// Toast
export interface ToastProps {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

export interface ToastContextType {
  toasts: ToastProps[];
  addToast: (type: ToastType, message: string, duration?: number) => void;
  removeToast: (id: string) => void;
}

// Modal
export interface ModalProps extends BaseComponentProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
}

// Skeleton
export interface SkeletonProps {
  variant?: 'text' | 'card' | 'avatar' | 'video';
  width?: string;
  height?: string;
  className?: string;
}

// Badge
export interface BadgeProps extends BaseComponentProps {
  variant?: BadgeVariant;
}
