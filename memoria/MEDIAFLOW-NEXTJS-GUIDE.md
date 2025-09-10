# 🎬 MEDIAFLOW NEXT.JS - GUIA COMPLETO DE MIGRAÇÃO

## 📋 **ÍNDICE**
1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Configuração Inicial](#configuração-inicial)
4. [Módulos e Componentes](#módulos-e-componentes)
5. [Serviços e APIs](#serviços-e-apis)
6. [Autenticação](#autenticação)
7. [Deploy AWS](#deploy-aws)
8. [Scripts de Automação](#scripts-de-automação)

---

## 🎯 **VISÃO GERAL**

### **Projeto Original (React + Vite)**
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: Python 3.12 + AWS Lambda (6 serviços)
- **Infraestrutura**: AWS Serverless (S3 + CloudFront + API Gateway)
- **Arquitetura**: Modular com componentes reutilizáveis

### **Migração para Next.js 14**
- **Framework**: Next.js 14 + App Router
- **Styling**: Tailwind CSS (mantido)
- **Backend**: Manter AWS Lambda Python (proxy via API Routes)
- **Deploy**: Vercel + AWS ou AWS Amplify
- **Arquitetura**: Modular preservada + Server Components

---

## 🏗️ **ESTRUTURA DO PROJETO**

### **Estrutura Next.js Modular**
```
mediaflow-nextjs/
├── app/                          # App Router (Next.js 14)
│   ├── (auth)/                   # Grupo de rotas auth
│   │   ├── login/
│   │   │   └── page.tsx          # Página de login
│   │   └── layout.tsx            # Layout auth
│   ├── dashboard/                # Dashboard principal
│   │   ├── page.tsx              # Dashboard home
│   │   ├── upload/
│   │   │   └── page.tsx          # Página upload
│   │   ├── files/
│   │   │   └── page.tsx          # Gerenciador arquivos
│   │   └── layout.tsx            # Layout dashboard
│   ├── api/                      # API Routes (Proxy AWS)
│   │   ├── auth/
│   │   │   └── route.ts          # Proxy auth Lambda
│   │   ├── files/
│   │   │   └── route.ts          # Proxy files Lambda
│   │   ├── upload/
│   │   │   └── route.ts          # Proxy upload Lambda
│   │   └── stream/
│   │       └── [id]/route.ts     # Proxy streaming
│   ├── globals.css               # Estilos globais
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Home page
│   └── middleware.ts             # Auth middleware
├── components/                   # Componentes modulares
│   ├── modules/                  # Módulos específicos
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── ProtectedRoute.tsx
│   │   │   └── AuthProvider.tsx
│   │   ├── files/
│   │   │   ├── FileList.tsx
│   │   │   ├── FileUpload/
│   │   │   │   ├── DropZone.tsx
│   │   │   │   ├── FileUpload.tsx
│   │   │   │   └── ProgressBar.tsx
│   │   │   ├── FileManager.tsx
│   │   │   ├── FolderNavigation.tsx
│   │   │   └── StorageStats.tsx
│   │   ├── player/
│   │   │   └── VideoPlayer.tsx
│   │   └── dashboard/
│   │       └── Dashboard.tsx
│   └── ui/                       # Componentes base
│       ├── Button.tsx
│       ├── Modal.tsx
│       ├── Input.tsx
│       └── LoadingSpinner.tsx
├── lib/                          # Utilitários e serviços
│   ├── auth.ts                   # Auth utilities
│   ├── aws.ts                    # AWS SDK config
│   ├── api-client.ts             # API client
│   ├── utils.ts                  # Utilities gerais
│   └── constants.ts              # Constantes
├── types/                        # TypeScript types
│   ├── auth.ts
│   ├── files.ts
│   └── api.ts
├── public/                       # Assets estáticos
├── next.config.js                # Configuração Next.js
├── tailwind.config.js            # Configuração Tailwind
├── tsconfig.json                 # TypeScript config
└── package.json                  # Dependencies
```

---

## ⚙️ **CONFIGURAÇÃO INICIAL**

### **1. Criar Projeto Next.js**
```bash
# Criar projeto
npx create-next-app@latest mediaflow-nextjs --typescript --tailwind --eslint --app

# Navegar para pasta
cd mediaflow-nextjs

# Instalar dependências adicionais
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
npm install lucide-react class-variance-authority clsx tailwind-merge
npm install @types/node
```

### **2. Configuração Next.js**
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true,
  },
  images: {
    domains: ['videos.sstechnologies-cloud.com'],
  },
  env: {
    AWS_REGION: process.env.AWS_REGION,
    AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY,
    API_BASE_URL: process.env.API_BASE_URL,
  },
}

module.exports = nextConfig
```

### **3. Variáveis de Ambiente**
```bash
# .env.local
NEXT_PUBLIC_API_BASE_URL=https://g1laj6w194.execute-api.us-east-1.amazonaws.com/prod
NEXT_PUBLIC_ENVIRONMENT=production

# AWS Config (para API Routes)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### **4. Tailwind Config**
```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'neon-cyan': '#00ffff',
        'neon-purple': '#8b5cf6',
        'dark-900': '#0f0f23',
        'dark-800': '#1a1a2e',
        'dark-700': '#16213e',
      },
      animation: {
        'pulse-neon': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}
```

---

## 🧩 **MÓDULOS E COMPONENTES**

### **1. Módulo de Autenticação**

#### **AuthProvider.tsx**
```typescript
// components/modules/auth/AuthProvider.tsx
'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { User } from '@/types/auth'

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const login = async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
      throw new Error('Login failed')
    }

    const data = await response.json()
    setUser(data.user)
    localStorage.setItem('token', data.token)
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('token')
  }

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      // Verificar token válido
      fetch('/api/auth/verify', {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then(res => res.json())
        .then(data => {
          if (data.valid) {
            setUser(data.user)
          }
        })
        .finally(() => setIsLoading(false))
    } else {
      setIsLoading(false)
    }
  }, [])

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      isAuthenticated: !!user,
      isLoading,
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

#### **LoginForm.tsx**
```typescript
// components/modules/auth/LoginForm.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from './AuthProvider'

export function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      await login(email, password)
      router.push('/dashboard')
    } catch (err) {
      setError('Credenciais inválidas')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-dark-900 via-dark-800 to-dark-700">
      <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl border border-cyan-500/20 p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            🎬 <span className="text-neon-cyan">Mediaflow</span>
          </h1>
          <p className="text-gray-400">Sistema de Streaming Completo</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-cyan-500 focus:outline-none"
              placeholder="seu@email.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Senha
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-cyan-500 focus:outline-none"
              placeholder="••••••••"
              required
            />
          </div>

          {error && (
            <div className="text-red-400 text-sm text-center">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 text-white rounded-lg transition-colors font-medium disabled:cursor-not-allowed"
          >
            {isLoading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

### **2. Módulo de Arquivos**

#### **FileUpload.tsx**
```typescript
// components/modules/files/FileUpload/FileUpload.tsx
'use client'

import { useState } from 'react'
import { DropZone } from './DropZone'
import { ProgressBar } from './ProgressBar'

interface UploadFile {
  file: File
  id: string
  name: string
  size: number
  progress: number
  status: 'pending' | 'uploading' | 'completed' | 'error'
  error?: string
}

interface FileUploadProps {
  onUploadComplete?: () => void
}

export function FileUpload({ onUploadComplete }: FileUploadProps) {
  const [uploadFiles, setUploadFiles] = useState<UploadFile[]>([])
  const [isUploading, setIsUploading] = useState(false)

  const handleFilesSelected = (files: File[]) => {
    const newUploadFiles: UploadFile[] = files.map(file => ({
      file,
      id: `${Date.now()}-${Math.random()}`,
      name: file.name,
      size: file.size,
      progress: 0,
      status: 'pending',
    }))

    setUploadFiles(prev => [...prev, ...newUploadFiles])
  }

  const startUpload = async () => {
    setIsUploading(true)
    
    const validFiles = uploadFiles.filter(f => f.status === 'pending')
    
    for (const uploadFile of validFiles) {
      try {
        // Atualizar status
        setUploadFiles(prev => 
          prev.map(f => 
            f.id === uploadFile.id 
              ? { ...f, status: 'uploading' }
              : f
          )
        )

        // Obter URL de upload
        const urlResponse = await fetch('/api/upload/presigned-url', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filename: uploadFile.file.name }),
        })

        const { uploadUrl } = await urlResponse.json()

        // Upload com progress
        await uploadWithProgress(uploadFile.file, uploadUrl, (progress) => {
          setUploadFiles(prev => 
            prev.map(f => 
              f.id === uploadFile.id 
                ? { ...f, progress }
                : f
            )
          )
        })

        // Marcar como completo
        setUploadFiles(prev => 
          prev.map(f => 
            f.id === uploadFile.id 
              ? { ...f, status: 'completed', progress: 100 }
              : f
          )
        )

      } catch (error) {
        setUploadFiles(prev => 
          prev.map(f => 
            f.id === uploadFile.id 
              ? { ...f, status: 'error', error: 'Erro no upload' }
              : f
          )
        )
      }
    }
    
    setIsUploading(false)
    onUploadComplete?.()
  }

  const uploadWithProgress = (file: File, url: string, onProgress: (progress: number) => void) => {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const progress = Math.round((e.loaded / e.total) * 100)
          onProgress(progress)
        }
      })
      
      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(xhr.response)
        } else {
          reject(new Error(`Upload failed: ${xhr.status}`))
        }
      })
      
      xhr.addEventListener('error', () => {
        reject(new Error('Network error'))
      })
      
      xhr.open('PUT', url)
      xhr.setRequestHeader('Content-Type', file.type)
      xhr.setRequestHeader('X-Filename', encodeURIComponent(file.name))
      xhr.send(file)
    })
  }

  return (
    <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl border border-cyan-500/20 p-6">
      <h2 className="text-xl font-semibold text-white mb-6">Upload de Arquivos</h2>
      
      <DropZone onFilesSelected={handleFilesSelected} disabled={isUploading} />
      
      {uploadFiles.length > 0 && (
        <div className="mt-6 space-y-4">
          <div className="space-y-3">
            {uploadFiles.map((uploadFile) => (
              <ProgressBar
                key={uploadFile.id}
                progress={uploadFile.progress}
                status={uploadFile.status}
                fileName={uploadFile.name}
                fileSize={uploadFile.size}
                error={uploadFile.error}
              />
            ))}
          </div>
          
          {uploadFiles.some(f => f.status === 'pending') && (
            <button
              onClick={startUpload}
              disabled={isUploading}
              className="w-full py-3 bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 text-white rounded-lg transition-colors font-medium"
            >
              {isUploading ? 'Enviando...' : 'Enviar Arquivos'}
            </button>
          )}
        </div>
      )}
    </div>
  )
}
```

### **3. API Routes (Proxy AWS)**

#### **Auth API Route**
```typescript
// app/api/auth/login/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Proxy para AWS Lambda
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/login`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }
    )

    const data = await response.json()

    if (!response.ok) {
      return NextResponse.json(data, { status: response.status })
    }

    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

#### **Files API Route**
```typescript
// app/api/files/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const token = request.headers.get('authorization')?.replace('Bearer ', '')
    
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/videos`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    )

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch files' },
      { status: 500 }
    )
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const fileId = searchParams.get('id')
    const token = request.headers.get('authorization')?.replace('Bearer ', '')
    
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/files/${fileId}`,
      {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    )

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to delete file' },
      { status: 500 }
    )
  }
}
```

### **4. Middleware de Autenticação**
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value
  const isAuthPage = request.nextUrl.pathname.startsWith('/login')
  const isDashboard = request.nextUrl.pathname.startsWith('/dashboard')

  // Redirecionar para login se não autenticado
  if (isDashboard && !token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Redirecionar para dashboard se já autenticado
  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login']
}
```

---

## 📱 **PÁGINAS PRINCIPAIS**

### **1. Página de Login**
```typescript
// app/(auth)/login/page.tsx
import { LoginForm } from '@/components/modules/auth/LoginForm'

export default function LoginPage() {
  return <LoginForm />
}
```

### **2. Layout do Dashboard**
```typescript
// app/dashboard/layout.tsx
import { AuthProvider } from '@/components/modules/auth/AuthProvider'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-700">
        {children}
      </div>
    </AuthProvider>
  )
}
```

### **3. Dashboard Principal**
```typescript
// app/dashboard/page.tsx
'use client'

import { useState } from 'react'
import { useAuth } from '@/components/modules/auth/AuthProvider'
import { FileList } from '@/components/modules/files/FileList'
import { FileUpload } from '@/components/modules/files/FileUpload/FileUpload'
import { StorageStats } from '@/components/modules/files/StorageStats'

export default function DashboardPage() {
  const { user, logout } = useAuth()
  const [activeTab, setActiveTab] = useState<'files' | 'upload' | 'storage'>('files')

  const renderContent = () => {
    switch (activeTab) {
      case 'files':
        return <FileList />
      case 'upload':
        return <FileUpload onUploadComplete={() => setActiveTab('files')} />
      case 'storage':
        return <StorageStats />
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-neon-cyan/20">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-neon-cyan">
              🎬 Mediaflow
            </h1>
            <div className="flex items-center space-x-4">
              <span className="text-gray-300">Olá, {user?.name}</span>
              <button
                onClick={logout}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-black/10 backdrop-blur-sm border-b border-neon-cyan/10">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-8">
            {[
              { id: 'files', label: '📁 Arquivos' },
              { id: 'upload', label: '📤 Upload' },
              { id: 'storage', label: '💾 Armazenamento' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-neon-cyan text-neon-cyan'
                    : 'border-transparent text-gray-400 hover:text-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {renderContent()}
      </main>
    </div>
  )
}
```

---

## 🚀 **DEPLOY E CONFIGURAÇÃO**

### **1. Deploy Vercel**
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Configurar variáveis de ambiente no dashboard Vercel
```

### **2. Deploy AWS Amplify**
```bash
# Instalar Amplify CLI
npm install -g @aws-amplify/cli

# Configurar
amplify configure

# Inicializar
amplify init

# Deploy
amplify push
```

### **3. Scripts Package.json**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "deploy:vercel": "vercel --prod",
    "deploy:amplify": "amplify push"
  }
}
```

---

## 📊 **COMPARAÇÃO DE FUNCIONALIDADES**

| Funcionalidade | React + Vite | Next.js 14 | Status |
|----------------|--------------|------------|--------|
| **Autenticação** | ✅ JWT + localStorage | ✅ JWT + cookies + middleware | ✅ Melhorado |
| **Upload Arquivos** | ✅ Multipart + drag&drop | ✅ Mantido + Server Actions | ✅ Otimizado |
| **Player Vídeo** | ✅ Modal responsivo | ✅ Mantido + otimizações | ✅ Mantido |
| **Gerenciador** | ✅ Navegação hierárquica | ✅ Mantido + SSR | ✅ Melhorado |
| **Busca Avançada** | ✅ Filtros + ordenação | ✅ Mantido + debounce | ✅ Otimizado |
| **Conversão Vídeo** | ✅ MediaConvert automático | ✅ Mantido (AWS Lambda) | ✅ Mantido |
| **Storage Stats** | ✅ Métricas em tempo real | ✅ Mantido + cache | ✅ Otimizado |
| **Deploy** | ✅ S3 + CloudFront | ✅ Vercel + AWS | ✅ Melhorado |
| **Performance** | ✅ Vite fast reload | ✅ Next.js optimizations | ✅ Melhorado |
| **SEO** | ❌ SPA limitations | ✅ SSR + meta tags | ✅ Novo |

---

## 🎯 **CRONOGRAMA DE MIGRAÇÃO**

### **Fase 1: Setup (2 horas)**
- [ ] Criar projeto Next.js
- [ ] Configurar Tailwind CSS
- [ ] Setup TypeScript
- [ ] Configurar variáveis ambiente

### **Fase 2: Autenticação (3 horas)**
- [ ] Migrar AuthProvider
- [ ] Criar LoginForm
- [ ] Implementar middleware
- [ ] Configurar API routes auth

### **Fase 3: Módulo Files (4 horas)**
- [ ] Migrar FileUpload
- [ ] Migrar FileList
- [ ] Migrar FileManager
- [ ] Configurar API routes files

### **Fase 4: Player e Dashboard (2 horas)**
- [ ] Migrar VideoPlayer
- [ ] Migrar Dashboard
- [ ] Configurar layouts
- [ ] Testes integração

### **Fase 5: Deploy (1 hora)**
- [ ] Configurar Vercel
- [ ] Deploy produção
- [ ] Testes finais
- [ ] Documentação

**Total Estimado: 12 horas**

---

## 💡 **MELHORIAS EXCLUSIVAS NEXT.JS**

### **1. Server Components**
```typescript
// Componente que roda no servidor
async function ServerFileList() {
  const files = await fetch(`${process.env.API_BASE_URL}/videos`, {
    cache: 'no-store' // ou 'force-cache' para cache
  })
  
  return <FileListClient files={files} />
}
```

### **2. Server Actions**
```typescript
// app/dashboard/upload/actions.ts
'use server'

export async function uploadFile(formData: FormData) {
  const file = formData.get('file') as File
  
  // Processar upload no servidor
  const result = await processUpload(file)
  
  return result
}
```

### **3. Streaming UI**
```typescript
// Loading.js automático
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
      <div className="h-4 bg-gray-300 rounded w-1/2"></div>
    </div>
  )
}
```

### **4. Metadata API**
```typescript
// app/dashboard/page.tsx
export const metadata = {
  title: 'Dashboard - Mediaflow',
  description: 'Sistema de streaming completo',
  openGraph: {
    title: 'Mediaflow Dashboard',
    description: 'Gerencie seus arquivos de mídia',
    images: ['/og-image.jpg'],
  },
}
```

---

## 🔧 **UTILITÁRIOS E HELPERS**

### **1. API Client**
```typescript
// lib/api-client.ts
class ApiClient {
  private baseUrl: string
  
  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || ''
  }
  
  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const token = localStorage.getItem('token')
    
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options?.headers,
      },
      ...options,
    })
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    
    return response.json()
  }
  
  get<T>(endpoint: string) {
    return this.request<T>(endpoint)
  }
  
  post<T>(endpoint: string, data?: any) {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }
  
  delete<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

export const apiClient = new ApiClient()
```

### **2. Utilities**
```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('pt-BR')
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}
```

---

## 📝 **CHECKLIST FINAL**

### **Funcionalidades Core**
- [ ] ✅ Autenticação JWT
- [ ] ✅ Upload multipart
- [ ] ✅ Conversão automática
- [ ] ✅ Player modal
- [ ] ✅ Gerenciador arquivos
- [ ] ✅ Busca avançada
- [ ] ✅ Storage stats
- [ ] ✅ Limpeza automática

### **Melhorias Next.js**
- [ ] ✅ SSR/SSG
- [ ] ✅ Server Components
- [ ] ✅ API Routes
- [ ] ✅ Middleware auth
- [ ] ✅ Image optimization
- [ ] ✅ SEO metadata
- [ ] ✅ Performance optimizations

### **Deploy e Produção**
- [ ] ✅ Build otimizado
- [ ] ✅ Variáveis ambiente
- [ ] ✅ Deploy Vercel/AWS
- [ ] ✅ Monitoramento
- [ ] ✅ Backup e rollback

---

## 🎬 **CONCLUSÃO**

Este guia fornece uma migração completa e detalhada do Mediaflow de React+Vite para Next.js 14, mantendo toda a funcionalidade existente e adicionando melhorias significativas de performance, SEO e developer experience.

A arquitetura modular é preservada e otimizada, garantindo que o projeto continue escalável e maintível.

**Resultado esperado**: Sistema mais rápido, melhor SEO, deploy mais simples e developer experience superior.