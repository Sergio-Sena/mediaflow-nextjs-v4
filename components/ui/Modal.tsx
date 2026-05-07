'use client'

import { useState } from 'react'
import { X } from 'lucide-react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-md bg-dark-900 border border-neon-cyan/20 rounded-xl shadow-2xl shadow-neon-cyan/10 animate-fade-in">
        <div className="flex items-center justify-between px-5 py-4 border-b border-white/5">
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          <button onClick={onClose} className="p-1 text-gray-400 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="px-5 py-4">
          {children}
        </div>
      </div>
    </div>
  )
}

interface ConfirmModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title: string
  message: string
  confirmText?: string
  confirmColor?: 'red' | 'cyan'
}

export function ConfirmModal({ isOpen, onClose, onConfirm, title, message, confirmText = 'Confirmar', confirmColor = 'red' }: ConfirmModalProps) {
  const colorClasses = confirmColor === 'red'
    ? 'bg-red-600/20 hover:bg-red-600/40 text-red-300 border-red-500/30'
    : 'bg-cyan-600/20 hover:bg-cyan-600/40 text-cyan-300 border-cyan-500/30'

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title}>
      <p className="text-gray-300 mb-6">{message}</p>
      <div className="flex gap-3 justify-end">
        <button
          onClick={onClose}
          className="px-4 py-2 bg-gray-700/30 hover:bg-gray-700/50 text-gray-300 border border-gray-600/30 rounded-lg transition-colors"
        >
          Cancelar
        </button>
        <button
          onClick={() => { onConfirm(); onClose() }}
          className={`px-4 py-2 border rounded-lg transition-colors ${colorClasses}`}
        >
          {confirmText}
        </button>
      </div>
    </Modal>
  )
}

interface InputModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: (value: string) => void
  title: string
  message?: string
  placeholder?: string
  defaultValue?: string
  options?: string[]
  confirmText?: string
}

export function InputModal({ isOpen, onClose, onConfirm, title, message, placeholder, defaultValue = '', options, confirmText = 'Confirmar' }: InputModalProps) {
  const [value, setValue] = useState(defaultValue)

  const handleConfirm = () => {
    if (value.trim()) {
      onConfirm(value.trim())
      setValue(defaultValue)
      onClose()
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title}>
      {message && <p className="text-gray-300 mb-4">{message}</p>}
      {options ? (
        <select
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="w-full px-4 py-2.5 bg-gray-800 border border-gray-600 rounded-lg text-white focus:border-neon-cyan focus:outline-none mb-4"
        >
          {options.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      ) : (
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleConfirm()}
          placeholder={placeholder}
          className="w-full px-4 py-2.5 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-neon-cyan focus:outline-none mb-4"
          autoFocus
        />
      )}
      <div className="flex gap-3 justify-end">
        <button
          onClick={onClose}
          className="px-4 py-2 bg-gray-700/30 hover:bg-gray-700/50 text-gray-300 border border-gray-600/30 rounded-lg transition-colors"
        >
          Cancelar
        </button>
        <button
          onClick={handleConfirm}
          className="px-4 py-2 bg-cyan-600/20 hover:bg-cyan-600/40 text-cyan-300 border border-cyan-500/30 rounded-lg transition-colors"
        >
          {confirmText}
        </button>
      </div>
    </Modal>
  )
}
