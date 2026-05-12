'use client'

import { useState, useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { getApiUrl } from '@/lib/aws-config'
import { getUserFromToken } from '@/lib/auth-utils'
import VideoPlayer from '@/components/modules/VideoPlayer'
import ImageViewer from '@/components/modules/ImageViewer'

function ShareContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [content, setContent] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [notLoggedIn, setNotLoggedIn] = useState(false)

  useEffect(() => {
    const v = searchParams.get('v') || ''

    const user = getUserFromToken()
    if (!user) {
      setNotLoggedIn(true)
      setLoading(false)
      return
    }
    if (v) findContent(v)
    else setLoading(false)
  }, [searchParams])

  const findContent = async (s: string) => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(getApiUrl('PUBLIC_CONTENT'), {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const data = await res.json()
      if (data.success) {
        const found = data.content.find((item: any) => {
          const nameWithoutExt = item.title.replace(/\.[^.]+$/, '')
          const itemSlug = nameWithoutExt
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '')
          return itemSlug === s
        })
        if (found) setContent(found)
      }
    } catch (e) {
      console.error('Error:', e)
    } finally {
      setLoading(false)
    }
  }

  if (notLoggedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
        <div className="max-w-md w-full text-center">
          <div className="glass-card p-8 border border-neon-cyan/20">
            <div className="text-5xl mb-4">🔒</div>
            <h1 className="text-2xl font-bold text-white mb-3">
              Conteúdo Exclusivo
            </h1>
            <p className="text-gray-400 mb-6">
              Este conteúdo está disponível apenas para membros cadastrados do <span className="text-neon-cyan font-semibold">Mídiaflow</span>.
            </p>
            <p className="text-gray-500 text-sm mb-8">
              Crie sua conta gratuitamente para acessar vídeos, imagens e interagir com a comunidade.
            </p>
            <div className="space-y-3">
              <button
                onClick={() => router.push('/register')}
                className="w-full px-6 py-3 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-neon-cyan border border-neon-cyan/50 rounded-lg hover:from-cyan-500/30 hover:to-purple-500/30 transition-all font-medium"
              >
                🚀 Criar Conta Grátis
              </button>
              <button
                onClick={() => router.push('/login')}
                className="w-full px-6 py-3 bg-gray-700/20 text-gray-300 border border-gray-600/30 rounded-lg hover:bg-gray-700/40 transition-colors"
              >
                Já tenho conta → Entrar
              </button>
            </div>
          </div>
          <p className="text-gray-600 text-xs mt-4">
            🎬 Mídiaflow — Plataforma de streaming modular
          </p>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="loading-shimmer w-16 h-16 rounded-full mx-auto mb-4"></div>
        <p className="text-gray-400">Carregando...</p>
      </div>
    )
  }

  if (!content) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="text-center">
          <div className="text-5xl mb-4">😕</div>
          <h1 className="text-xl font-bold text-white mb-2">Conteúdo não encontrado</h1>
          <p className="text-gray-400 mb-6">Este link pode ter expirado ou o conteúdo foi removido.</p>
          <button
            onClick={() => router.push('/public-feed')}
            className="px-6 py-3 bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/50 rounded-lg hover:bg-neon-cyan/30 transition-colors"
          >
            Ir para o Feed Público
          </button>
        </div>
      </div>
    )
  }

  if (content.type === 'video') {
    return (
      <VideoPlayer
        src={content.file_key}
        title={content.title}
        onClose={() => router.push('/public-feed')}
      />
    )
  }

  return <ImageRedirect content={content} onClose={() => router.push('/public-feed')} />
}

function ImageRedirect({ content, onClose }: { content: any; onClose: () => void }) {
  const [imageUrl, setImageUrl] = useState<string | null>(null)

  useEffect(() => {
    const fetchUrl = async () => {
      const token = localStorage.getItem('token')
      const res = await fetch(`https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/view/${encodeURIComponent(content.file_key)}`, {
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
      })
      if (res.ok) {
        const data = await res.json()
        if (data.success && data.viewUrl) setImageUrl(data.viewUrl)
      }
    }
    fetchUrl()
  }, [content])

  if (!imageUrl) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="loading-shimmer w-16 h-16 rounded-full"></div>
      </div>
    )
  }

  return <ImageViewer src={imageUrl} title={content.title} onClose={onClose} />
}

export default function SharePage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="loading-shimmer w-16 h-16 rounded-full"></div>
      </div>
    }>
      <ShareContent />
    </Suspense>
  )
}
