'use client'

import { useState, useEffect } from 'react'
import { BarChart3, TrendingUp, Video, HardDrive, Clock, Users, Folder } from 'lucide-react'

interface RealAnalytics {
  totalFiles: number
  totalSize: number
  videoFiles: number
  imageFiles: number
  documentFiles: number
  otherFiles: number
  folders: number
  avgFileSize: number
  largestFile: { name: string; size: number }
  oldestFile: { name: string; date: string }
  newestFile: { name: string; date: string }
}

export default function Analytics() {
  const [stats, setStats] = useState<RealAnalytics>({
    totalFiles: 0,
    totalSize: 0,
    videoFiles: 0,
    imageFiles: 0,
    documentFiles: 0,
    otherFiles: 0,
    folders: 0,
    avgFileSize: 0,
    largestFile: { name: '', size: 0 },
    oldestFile: { name: '', date: '' },
    newestFile: { name: '', date: '' }
  })
  const [loading, setLoading] = useState(true)

  const fetchRealStats = async () => {
    try {
      const { mediaflowClient } = await import('@/lib/aws-client')
      const data = await mediaflowClient.getFiles()
      
      if (data.success) {
        // Filtrar arquivos por usuário
        const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
        let userRole = 'user'
        let userId = ''
        
        if (token) {
          try {
            const payload = JSON.parse(atob(token.split('.')[1]))
            userRole = payload.role || 'user'
            userId = payload.user_id || ''
          } catch (e) {}
        }
        
        // Admin vê tudo, user só vê seus arquivos
        const files = userRole === 'admin' 
          ? data.files 
          : data.files.filter((f: any) => {
              const folder = f.folder || (f.key.includes('/') ? f.key.split('/').slice(0, -1).join('/') : 'root')
              return folder.startsWith(`users/${userId}`) || folder === 'root'
            })
        
        const totalFiles = files.length
        const totalSize = files.reduce((acc: number, file: any) => acc + file.size, 0)
        
        const videoFiles = files.filter((f: any) => f.key.match(/\.(mp4|avi|mov|mkv|webm|ts)$/i)).length
        const imageFiles = files.filter((f: any) => f.key.match(/\.(jpg|jpeg|png|gif|webp)$/i)).length
        const documentFiles = files.filter((f: any) => f.key.match(/\.(pdf|doc|docx|txt)$/i)).length
        const otherFiles = totalFiles - videoFiles - imageFiles - documentFiles
        
        const folders = new Set(files.map((f: any) => f.key.includes('/') ? f.key.split('/')[0] : 'root')).size - 1
        const avgFileSize = totalFiles > 0 ? totalSize / totalFiles : 0
        
        const largestFile = files.reduce((largest: any, file: any) => 
          file.size > largest.size ? file : largest, { size: 0, key: '' })
        
        const sortedByDate = [...files].sort((a: any, b: any) => 
          new Date(a.lastModified).getTime() - new Date(b.lastModified).getTime())
        
        const oldestFile = sortedByDate[0] || { key: '', lastModified: '' }
        const newestFile = sortedByDate[sortedByDate.length - 1] || { key: '', lastModified: '' }
        
        setStats({
          totalFiles,
          totalSize,
          videoFiles,
          imageFiles,
          documentFiles,
          otherFiles,
          folders,
          avgFileSize,
          largestFile: { 
            name: largestFile.key?.split('/').pop() || '', 
            size: largestFile.size || 0 
          },
          oldestFile: { 
            name: oldestFile.key?.split('/').pop() || '', 
            date: oldestFile.lastModified || '' 
          },
          newestFile: { 
            name: newestFile.key?.split('/').pop() || '', 
            date: newestFile.lastModified || '' 
          }
        })
      }
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchRealStats()
  }, [])

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
  }

  const formatPercentage = (value: number, total: number) => {
    return total > 0 ? ((value / total) * 100).toFixed(1) : '0'
  }

  const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit', 
      year: 'numeric'
    })
  }

  if (loading) {
    return (
      <div className="glass-card p-8 text-center">
        <div className="loading-shimmer w-16 h-16 rounded-full mx-auto mb-4"></div>
        <p className="text-gray-400">Carregando analytics...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Main Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Total de Arquivos</p>
              <p className="text-2xl font-bold text-white">{stats.totalFiles}</p>
            </div>
            <HardDrive className="w-8 h-8 text-neon-cyan" />
          </div>
          <p className="text-xs text-gray-500 mt-2">{formatFileSize(stats.totalSize)}</p>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Vídeos</p>
              <p className="text-2xl font-bold text-white">{stats.videoFiles}</p>
            </div>
            <Video className="w-8 h-8 text-neon-purple" />
          </div>
          <p className="text-xs text-gray-500 mt-2">{formatPercentage(stats.videoFiles, stats.totalFiles)}% do total</p>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Imagens</p>
              <p className="text-2xl font-bold text-white">{stats.imageFiles}</p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-400" />
          </div>
          <p className="text-xs text-gray-500 mt-2">{formatPercentage(stats.imageFiles, stats.totalFiles)}% do total</p>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Pastas</p>
              <p className="text-2xl font-bold text-white">{stats.folders}</p>
            </div>
            <Folder className="w-8 h-8 text-blue-400" />
          </div>
          <p className="text-xs text-gray-500 mt-2">Organizadas</p>
        </div>
      </div>

      {/* Detailed Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">📊 Estatísticas Detalhadas</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">📄 Documentos:</span>
              <span className="text-white">{stats.documentFiles}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">📁 Outros arquivos:</span>
              <span className="text-white">{stats.otherFiles}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">📏 Tamanho médio:</span>
              <span className="text-white">{formatFileSize(stats.avgFileSize)}</span>
            </div>
          </div>
        </div>

        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">🏆 Recordes</h3>
          <div className="space-y-3">
            <div>
              <span className="text-gray-400 text-sm">📦 Maior arquivo:</span>
              <p className="text-white truncate">{stats.largestFile.name || 'N/A'}</p>
              <p className="text-neon-cyan text-sm">{formatFileSize(stats.largestFile.size)}</p>
            </div>
            <div>
              <span className="text-gray-400 text-sm">⏰ Mais antigo:</span>
              <p className="text-white truncate">{stats.oldestFile.name || 'N/A'}</p>
              <p className="text-gray-500 text-sm">{formatDate(stats.oldestFile.date)}</p>
            </div>
            <div>
              <span className="text-gray-400 text-sm">🆕 Mais recente:</span>
              <p className="text-white truncate">{stats.newestFile.name || 'N/A'}</p>
              <p className="text-neon-cyan text-sm">{formatDate(stats.newestFile.date)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* File Type Distribution */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-6">📈 Distribuição por Tipo</h3>
        
        <div className="space-y-4">
          {stats.videoFiles > 0 && (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 bg-neon-purple rounded"></div>
                <span className="text-gray-300">Vídeos</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-white">{stats.videoFiles}</span>
                <div className="w-24 bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-neon-purple h-2 rounded-full transition-all duration-500" 
                    style={{ width: `${formatPercentage(stats.videoFiles, stats.totalFiles)}%` }}
                  ></div>
                </div>
                <span className="text-gray-400 text-sm w-12">{formatPercentage(stats.videoFiles, stats.totalFiles)}%</span>
              </div>
            </div>
          )}
          
          {stats.imageFiles > 0 && (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 bg-green-400 rounded"></div>
                <span className="text-gray-300">Imagens</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-white">{stats.imageFiles}</span>
                <div className="w-24 bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-green-400 h-2 rounded-full transition-all duration-500" 
                    style={{ width: `${formatPercentage(stats.imageFiles, stats.totalFiles)}%` }}
                  ></div>
                </div>
                <span className="text-gray-400 text-sm w-12">{formatPercentage(stats.imageFiles, stats.totalFiles)}%</span>
              </div>
            </div>
          )}
          
          {stats.documentFiles > 0 && (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 bg-blue-400 rounded"></div>
                <span className="text-gray-300">Documentos</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-white">{stats.documentFiles}</span>
                <div className="w-24 bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-blue-400 h-2 rounded-full transition-all duration-500" 
                    style={{ width: `${formatPercentage(stats.documentFiles, stats.totalFiles)}%` }}
                  ></div>
                </div>
                <span className="text-gray-400 text-sm w-12">{formatPercentage(stats.documentFiles, stats.totalFiles)}%</span>
              </div>
            </div>
          )}
          
          {stats.otherFiles > 0 && (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 bg-gray-400 rounded"></div>
                <span className="text-gray-300">Outros</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-white">{stats.otherFiles}</span>
                <div className="w-24 bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-gray-400 h-2 rounded-full transition-all duration-500" 
                    style={{ width: `${formatPercentage(stats.otherFiles, stats.totalFiles)}%` }}
                  ></div>
                </div>
                <span className="text-gray-400 text-sm w-12">{formatPercentage(stats.otherFiles, stats.totalFiles)}%</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}