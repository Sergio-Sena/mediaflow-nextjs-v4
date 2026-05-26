'use client'

import { usePathname, useRouter } from 'next/navigation'
import { Library, Globe, Upload, User } from 'lucide-react'

export default function MobileNav() {
  const pathname = usePathname()
  const router = useRouter()

  // Hide on public pages (landing, login, register, share)
  const hiddenPages = ['/', '/login', '/register', '/p', '/pricing', '/privacidade', '/termos', '/sla', '/docs']
  if (hiddenPages.includes(pathname)) return null

  const tabs = [
    { id: '/dashboard', icon: Library, label: 'Biblioteca' },
    { id: '/public-feed', icon: Globe, label: 'Público' },
    { id: '/dashboard', icon: Upload, label: 'Upload', query: 'upload' },
    { id: '/profile', icon: User, label: 'Perfil' },
  ]

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 md:hidden bg-dark-900/95 backdrop-blur-md border-t border-neon-cyan/20">
      <div className="flex justify-around items-center h-14">
        {tabs.map(tab => {
          const isActive = pathname === tab.id || (tab.id === '/public-feed' && pathname === '/public-feed')
          const Icon = tab.icon
          return (
            <button
              key={tab.label}
              onClick={() => router.push(tab.query ? `${tab.id}?${tab.query}=true` : tab.id)}
              className={`flex flex-col items-center justify-center w-full h-full transition-colors ${
                isActive ? 'text-neon-cyan' : 'text-gray-500'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px] mt-0.5">{tab.label}</span>
            </button>
          )
        })}
      </div>
    </nav>
  )
}
