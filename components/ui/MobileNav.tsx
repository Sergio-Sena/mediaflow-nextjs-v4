'use client'

import { useState } from 'react'
import { X, Menu, Home, Upload, Folder, BarChart3, Settings, LogOut } from 'lucide-react'

interface MobileNavProps {
  activeTab: string
  onTabChange: (tab: string) => void
  user?: any
  onLogout: () => void
  onAdminPanel?: () => void
}

export default function MobileNav({ activeTab, onTabChange, user, onLogout, onAdminPanel }: MobileNavProps) {
  const [isOpen, setIsOpen] = useState(false)

  const menuItems = [
    { id: 'files', label: 'Biblioteca', icon: Home, show: user?.role !== 'admin' },
    { id: 'folders', label: 'Pastas', icon: Folder, show: true },
    { id: 'upload', label: 'Upload', icon: Upload, show: true },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, show: true },
  ].filter(item => item.show)

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="lg:hidden touch-target btn-ghost p-3"
        aria-label="Abrir menu"
      >
        <Menu className="w-6 h-6" />
      </button>

      {/* Mobile Overlay */}
      {isOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Sidebar */}
          <div className="absolute right-0 top-0 h-full w-80 max-w-[85vw] bg-dark-900/95 backdrop-blur-xl border-l border-neon-cyan/20">
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-neon-cyan/20">
              <h2 className="text-lg font-semibold text-white">Menu</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="touch-target btn-ghost p-2"
                aria-label="Fechar menu"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* User Info */}
            {user && (
              <div className="p-6 border-b border-neon-cyan/10">
                <div className="flex items-center gap-3">
                  {user.avatar_url ? (
                    <img 
                      src={user.avatar_url} 
                      alt={user.name}
                      className="w-12 h-12 rounded-full object-cover border-2 border-neon-cyan/30"
                    />
                  ) : (
                    <div className="w-12 h-12 rounded-full bg-neon-cyan/20 flex items-center justify-center">
                      <span className="text-neon-cyan font-semibold text-lg">
                        {user.name?.charAt(0)?.toUpperCase() || '?'}
                      </span>
                    </div>
                  )}
                  <div>
                    <p className="text-white font-medium">{user.name}</p>
                    <p className="text-gray-400 text-sm">{user.role === 'admin' ? 'Administrador' : 'Usuário'}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Navigation */}
            <nav className="p-4 space-y-2">
              {menuItems.map((item) => {
                const Icon = item.icon
                const isActive = activeTab === item.id
                
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      onTabChange(item.id)
                      setIsOpen(false)
                    }}
                    className={`w-full flex items-center gap-3 p-4 rounded-xl transition-all touch-target ${
                      isActive
                        ? 'bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/30'
                        : 'text-gray-300 hover:bg-white/5 hover:text-white'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                  </button>
                )
              })}
            </nav>

            {/* Actions */}
            <div className="absolute bottom-0 left-0 right-0 p-4 space-y-2 border-t border-neon-cyan/10">
              {user?.role === 'admin' && onAdminPanel && (
                <button
                  onClick={() => {
                    onAdminPanel()
                    setIsOpen(false)
                  }}
                  className="w-full flex items-center gap-3 p-4 rounded-xl text-gray-300 hover:bg-white/5 hover:text-white transition-all touch-target"
                >
                  <Settings className="w-5 h-5" />
                  <span className="font-medium">Painel Admin</span>
                </button>
              )}
              
              <button
                onClick={() => {
                  onLogout()
                  setIsOpen(false)
                }}
                className="w-full flex items-center gap-3 p-4 rounded-xl text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-all touch-target"
              >
                <LogOut className="w-5 h-5" />
                <span className="font-medium">Sair</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}