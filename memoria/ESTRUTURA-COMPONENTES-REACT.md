# 📋 ESTRUTURA DETALHADA - COMPONENTES REACT ATUAL

## 🏗️ **MAPEAMENTO COMPLETO DOS MÓDULOS**

### **📁 Estrutura Atual (React + Vite)**
```
src/
├── modules/
│   ├── auth/                     # 🔐 Módulo de Autenticação
│   │   ├── components/
│   │   │   ├── LoginPage.tsx     # Página de login principal
│   │   │   └── ProtectedRoute.tsx # HOC para proteção de rotas
│   │   └── services/
│   │       └── authService.ts    # Serviços de autenticação
│   │
│   ├── files/                    # 📁 Módulo de Gerenciamento de Arquivos
│   │   ├── components/
│   │   │   ├── FileUpload/       # 📤 Submodulo Upload
│   │   │   │   ├── DropZone.tsx  # Zona de drag & drop
│   │   │   │   ├── FileUpload.tsx # Componente principal upload
│   │   │   │   └── ProgressBar.tsx # Barra de progresso
│   │   │   ├── AdvancedSearch.tsx # 🔍 Busca avançada
│   │   │   ├── FileList.tsx      # 📋 Lista de arquivos
│   │   │   ├── FileManager.tsx   # 🗂️ Gerenciador completo
│   │   │   ├── FolderNavigation.tsx # 📂 Navegação pastas
│   │   │   └── StorageStats.tsx  # 📊 Estatísticas storage
│   │   └── services/
│   │       ├── fileService.ts    # CRUD arquivos
│   │       ├── uploadService.ts  # Serviços upload
│   │       ├── folderService.ts  # Gerenciamento pastas
│   │       ├── conversionService.ts # Conversão vídeos
│   │       ├── cleanupService.ts # Limpeza automática
│   │       └── folderManagerService.ts # Gerenciador pastas
│   │
│   ├── dashboard/                # 🏠 Módulo Dashboard
│   │   └── components/
│   │       └── Dashboard.tsx     # Dashboard principal
│   │
│   ├── player/                   # 🎥 Módulo Player
│   │   └── components/
│   │       └── VideoPlayer.tsx   # Player modal
│   │
│   └── shared/                   # 🔧 Módulo Compartilhado
│       └── services/
│           └── apiClient.ts      # Cliente API genérico
│
├── App.tsx                       # Componente raiz
├── main.tsx                      # Entry point
└── index.css                     # Estilos globais
```

---

## 🔐 **MÓDULO AUTH - DETALHAMENTO**

### **LoginPage.tsx**
```typescript
// Funcionalidades:
- ✅ Formulário de login responsivo
- ✅ Validação de campos
- ✅ Estados de loading
- ✅ Tratamento de erros
- ✅ Design neon/cyberpunk
- ✅ Integração com authService

// Props: Nenhuma (página standalone)
// Estado: email, password, loading, error
// Hooks: useState para form state
```

### **ProtectedRoute.tsx**
```typescript
// Funcionalidades:
- ✅ HOC para proteção de rotas
- ✅ Verificação de token JWT
- ✅ Redirecionamento automático
- ✅ Loading state durante verificação

// Props: { children: ReactNode }
// Lógica: Verifica authService.isAuthenticated()
```

### **authService.ts**
```typescript
// Funcionalidades:
- ✅ login(email, password) → Promise<AuthResponse>
- ✅ logout() → void
- ✅ isAuthenticated() → boolean
- ✅ getToken() → string | null
- ✅ getUser() → User | null
- ✅ Gerenciamento localStorage
- ✅ Integração API AWS Lambda
```

---

## 📁 **MÓDULO FILES - DETALHAMENTO**

### **FileUpload/DropZone.tsx**
```typescript
// Funcionalidades:
- ✅ Drag & drop de arquivos/pastas
- ✅ Seleção manual (botões)
- ✅ Validação de tipos/tamanhos
- ✅ Preview visual durante drag
- ✅ Suporte webkitdirectory (pastas)
- ✅ Estados visuais (hover, drop)

// Props: 
interface DropZoneProps {
  onFilesSelected: (files: File[]) => void
  disabled?: boolean
}

// Estado: isDragOver
// Eventos: onDragOver, onDragLeave, onDrop, onChange
```

### **FileUpload/FileUpload.tsx**
```typescript
// Funcionalidades:
- ✅ Gerenciamento fila de upload
- ✅ Upload paralelo com progress
- ✅ Retry automático em falhas
- ✅ Validação pré-upload
- ✅ Integração uploadService
- ✅ Estados por arquivo (pending, uploading, completed, error)

// Props:
interface FileUploadProps {
  onUploadComplete?: () => void
  onClose?: () => void
}

// Estado: uploadFiles[], isUploading
// Tipos: UploadFile interface
```

### **FileUpload/ProgressBar.tsx**
```typescript
// Funcionalidades:
- ✅ Barra de progresso animada
- ✅ Estados visuais por status
- ✅ Informações do arquivo (nome, tamanho)
- ✅ Detecção de pasta de destino
- ✅ Tratamento de erros

// Props:
interface ProgressBarProps {
  progress: number
  status: 'pending' | 'uploading' | 'completed' | 'error'
  fileName: string
  fileSize: number
  error?: string
  destination?: string
}
```

### **FileList.tsx**
```typescript
// Funcionalidades:
- ✅ Listagem de arquivos com paginação
- ✅ Filtros por tipo/pasta
- ✅ Busca em tempo real
- ✅ Ordenação (nome, tamanho, data)
- ✅ Seleção múltipla
- ✅ Ações em lote (delete)
- ✅ Preview de imagens
- ✅ Player modal para vídeos
- ✅ Status de conversão
- ✅ Integração com todos os services

// Props:
interface FileListProps {
  onRefresh?: () => void
  onOpenFileManager?: () => void
  onCleanupStuckFiles?: () => void
  isCleaningUp?: boolean
}

// Estado: allFiles[], filteredFiles[], folders[], currentFolder, searchTerm, loading, error, selectedVideo
```

### **FileManager.tsx**
```typescript
// Funcionalidades:
- ✅ Navegação hierárquica de pastas
- ✅ Breadcrumb navigation
- ✅ Visualização lista/grade
- ✅ Seleção múltipla avançada
- ✅ Ordenação customizável
- ✅ Ações em lote
- ✅ Modal fullscreen
- ✅ Integração folderManagerService

// Props:
interface FileManagerProps {
  onClose?: () => void
  files?: any[]
}

// Estado: currentPath, items[], selectedItems, loading, viewMode, sortBy, sortOrder
```

### **FolderNavigation.tsx**
```typescript
// Funcionalidades:
- ✅ Abas de navegação por pasta
- ✅ Contadores de arquivos
- ✅ Botão gerenciador avançado
- ✅ Estados ativos/inativos
- ✅ Design responsivo

// Props:
interface SimpleFolderTabsProps {
  folders: Array<{name: string, count: number}>
  currentFolder: string
  onFolderChange: (folder: string) => void
  onOpenFileManager?: () => void
  allFiles?: any[]
}
```

### **StorageStats.tsx**
```typescript
// Funcionalidades:
- ✅ Métricas de armazenamento
- ✅ Gráficos de uso
- ✅ Breakdown por tipo de arquivo
- ✅ Alertas de limite
- ✅ Atualização em tempo real

// Props: Nenhuma (busca dados internamente)
// Estado: storageInfo, loading, error
```

---

## 🎥 **MÓDULO PLAYER - DETALHAMENTO**

### **VideoPlayer.tsx**
```typescript
// Funcionalidades:
- ✅ Player HTML5 customizado
- ✅ Controles personalizados
- ✅ Fullscreen modal
- ✅ Progress bar interativa
- ✅ Controle de volume
- ✅ Play/pause com overlay
- ✅ Auto-hide controles
- ✅ Keyboard shortcuts
- ✅ Responsive design

// Props:
interface VideoPlayerProps {
  src: string
  title?: string
  onClose: () => void
}

// Estado: isPlaying, currentTime, duration, volume, showControls
// Refs: videoRef, containerRef, controlsTimeoutRef
```

---

## 🏠 **MÓDULO DASHBOARD - DETALHAMENTO**

### **Dashboard.tsx**
```typescript
// Funcionalidades:
- ✅ Layout principal da aplicação
- ✅ Header com navegação
- ✅ Tabs dinâmicas (Arquivos, Upload, Storage)
- ✅ Gerenciamento de estado global
- ✅ Integração com todos os módulos
- ✅ Logout functionality
- ✅ User info display
- ✅ Responsive layout

// Props: Nenhuma (componente raiz)
// Estado: user, activeTab, isLoading, showFileManager, fileManagerData, isCleaningUp
```

---

## 🔧 **SERVIÇOS - DETALHAMENTO**

### **fileService.ts**
```typescript
// Funcionalidades:
- ✅ getFiles() → Promise<FileResponse>
- ✅ getDownloadUrl(fileName) → Promise<string>
- ✅ deleteFile(fileName) → Promise<void>
- ✅ getStorageInfo() → Promise<StorageInfo>
- ✅ formatFileSize(bytes) → string
- ✅ Tratamento de erros HTTP
- ✅ Integração API Gateway

// Interfaces:
interface StorageInfo {
  used: number
  total: number
  percentage: number
  files: number
  project_total: number
}
```

### **uploadService.ts**
```typescript
// Funcionalidades:
- ✅ validateFile(file) → ValidationResult
- ✅ detectFolder(mimeType, fileName) → string
- ✅ getUploadUrl(fileName, fileSize?, fileType?) → Promise<UploadResponse>
- ✅ uploadLargeFile(file, uploadUrl, onProgress) → Promise<void>
- ✅ confirmUpload(fileId) → Promise<void>
- ✅ Multipart upload com progress
- ✅ Retry logic

// Interfaces:
interface UploadFile {
  file: File
  id: string
  name: string
  size: number
  progress: number
  status: 'pending' | 'uploading' | 'completed' | 'error'
  error?: string
}
```

### **folderService.ts**
```typescript
// Funcionalidades:
- ✅ extractFoldersFromFiles(files) → SimpleFolder[]
- ✅ getFilesInFolder(files, folderName) → File[]
- ✅ formatSize(bytes) → string
- ✅ Organização automática por tipo
- ✅ Contagem de arquivos por pasta

// Interfaces:
interface SimpleFolder {
  name: string
  count: number
}
```

### **conversionService.ts**
```typescript
// Funcionalidades:
- ✅ getStatusIcon(fileName, fileSize) → string
- ✅ getStatusTooltip(fileName, fileSize) → string
- ✅ needsConversion(fileName) → boolean
- ✅ Detecção automática de formatos
- ✅ Status visual por tipo

// Lógica: Detecta .ts, .avi, .mov → precisa conversão
```

### **cleanupService.ts**
```typescript
// Funcionalidades:
- ✅ cleanStuckFiles() → Promise<CleanupResult>
- ✅ Identificação de arquivos travados
- ✅ Limpeza automática pós-conversão
- ✅ Relatório de limpeza

// Interface:
interface CleanupResult {
  success: boolean
  cleaned: number
  files: string[]
}
```

### **folderManagerService.ts**
```typescript
// Funcionalidades:
- ✅ organizeFolderStructure(files) → FolderStructure[]
- ✅ getFilesInFolder(files, folderName) → File[]
- ✅ getBreadcrumb(path) → Breadcrumb[]
- ✅ isValidPath(path, folders) → boolean
- ✅ Navegação hierárquica completa

// Interfaces:
interface FolderStructure {
  name: string
  path: string
  fileCount: number
  files: File[]
}
```

### **apiClient.ts**
```typescript
// Funcionalidades:
- ✅ get(endpoint) → Promise<Response>
- ✅ post(endpoint, data?) → Promise<Response>
- ✅ delete(endpoint) → Promise<Response>
- ✅ Interceptors de request/response
- ✅ Tratamento automático de auth
- ✅ Logs detalhados
- ✅ Error handling centralizado

// Configuração: API_BASE_URL, IS_LOCAL, headers automáticos
```

---

## 🎨 **DESIGN SYSTEM - COMPONENTES UI**

### **Cores e Temas**
```css
/* Paleta Neon/Cyberpunk */
--neon-cyan: #00ffff
--neon-purple: #8b5cf6
--dark-900: #0f0f23
--dark-800: #1a1a2e
--dark-700: #16213e

/* Gradientes */
bg-gradient-to-br from-dark-900 via-dark-800 to-dark-700
bg-gradient-to-r from-neon-cyan/5 via-transparent to-neon-purple/5
```

### **Componentes Reutilizáveis**
```typescript
// Padrões de componentes:
- ✅ Modal com backdrop blur
- ✅ Buttons com estados hover/disabled
- ✅ Inputs com focus states
- ✅ Cards com border neon
- ✅ Loading spinners animados
- ✅ Progress bars customizadas
- ✅ Tooltips informativos
- ✅ Breadcrumbs navegáveis
```

### **Animações e Transições**
```css
/* Animações customizadas */
.animate-pulse-neon { /* Pulse com cor neon */ }
.animate-spin { /* Loading spinners */ }
.transition-all { /* Transições suaves */ }
.backdrop-blur-sm { /* Blur effects */ }
.hover:scale-105 { /* Hover effects */ }
```

---

## 📱 **RESPONSIVIDADE**

### **Breakpoints**
```css
/* Mobile First Design */
sm: 640px   /* Tablets */
md: 768px   /* Desktop pequeno */
lg: 1024px  /* Desktop médio */
xl: 1280px  /* Desktop grande */
2xl: 1536px /* Desktop extra grande */
```

### **Componentes Responsivos**
- ✅ **FileList**: Grid adaptativo (1-5 colunas)
- ✅ **FileManager**: Layout flex responsivo
- ✅ **Dashboard**: Navigation collapse em mobile
- ✅ **VideoPlayer**: Fullscreen em mobile
- ✅ **DropZone**: Touch-friendly em tablets

---

## 🔄 **FLUXOS DE DADOS**

### **Fluxo de Upload**
```
1. DropZone → FileUpload (files selection)
2. FileUpload → uploadService.getUploadUrl()
3. uploadService → AWS Lambda (presigned URL)
4. FileUpload → uploadService.uploadLargeFile()
5. uploadService → S3 Direct Upload
6. FileUpload → Dashboard (onUploadComplete)
7. Dashboard → FileList (refresh)
```

### **Fluxo de Autenticação**
```
1. LoginPage → authService.login()
2. authService → AWS Lambda Auth
3. authService → localStorage (token)
4. ProtectedRoute → authService.isAuthenticated()
5. Dashboard → authService.getUser()
```

### **Fluxo de Conversão**
```
1. Upload → S3 Event Trigger
2. S3 → Lambda Conversion Service
3. Lambda → MediaConvert Job
4. MediaConvert → S3 (converted file)
5. S3 → Lambda Cleanup Service
6. FileList → Status Update (polling)
```

---

## 🧪 **TESTES E VALIDAÇÃO**

### **Cenários de Teste**
- ✅ **Upload**: Arquivos grandes (>1GB)
- ✅ **Upload**: Pastas com estrutura complexa
- ✅ **Upload**: Múltiplos arquivos simultâneos
- ✅ **Conversão**: Formatos diversos (.ts, .avi, .mov)
- ✅ **Player**: Vídeos de diferentes resoluções
- ✅ **Auth**: Login/logout/token expiration
- ✅ **Responsivo**: Mobile/tablet/desktop
- ✅ **Performance**: Loading states/error handling

### **Validações Implementadas**
- ✅ **Tamanho**: Máximo 5GB por arquivo
- ✅ **Tipos**: Whitelist de MIME types
- ✅ **Nomes**: Sanitização automática
- ✅ **Auth**: Token JWT validation
- ✅ **Network**: Retry logic + timeouts

---

## 📊 **MÉTRICAS E PERFORMANCE**

### **Bundle Size (Atual)**
```
- index.html: 0.63 kB
- CSS: 30.39 kB (gzip: 5.66 kB)
- JS: 210.16 kB (gzip: 65.78 kB)
- Total: ~241 kB (gzip: ~72 kB)
```

### **Performance Otimizações**
- ✅ **Code Splitting**: Lazy loading de módulos
- ✅ **Tree Shaking**: Remoção de código não usado
- ✅ **Compression**: Gzip automático
- ✅ **Caching**: Service Worker + Cache API
- ✅ **Images**: Lazy loading + WebP
- ✅ **API**: Debounce em buscas

---

## 🔧 **CONFIGURAÇÕES E SETUP**

### **Vite Config**
```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  build: {
    target: 'esnext',
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        }
      }
    }
  }
})
```

### **TypeScript Config**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### **Environment Variables**
```bash
# .env.local (desenvolvimento)
VITE_API_BASE_URL=http://localhost:3001
VITE_ENVIRONMENT=local
VITE_DEBUG=true

# .env.production (produção)
VITE_API_BASE_URL=https://g1laj6w194.execute-api.us-east-1.amazonaws.com/prod
VITE_ENVIRONMENT=production
VITE_DEBUG=false
```

---

## 📚 **DEPENDÊNCIAS**

### **Core Dependencies**
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.8.1"
}
```

### **Dev Dependencies**
```json
{
  "@types/react": "^18.2.43",
  "@types/react-dom": "^18.2.17",
  "@typescript-eslint/eslint-plugin": "^6.14.0",
  "@typescript-eslint/parser": "^6.14.0",
  "@vitejs/plugin-react": "^4.2.1",
  "autoprefixer": "^10.4.16",
  "concurrently": "^8.2.2",
  "eslint": "^8.55.0",
  "eslint-plugin-react-hooks": "^4.6.0",
  "eslint-plugin-react-refresh": "^0.4.5",
  "postcss": "^8.4.32",
  "tailwindcss": "^3.3.6",
  "typescript": "^5.2.2",
  "vite": "^5.0.8"
}
```

---

## 🎯 **PONTOS DE ATENÇÃO PARA MIGRAÇÃO**

### **Complexidades Identificadas**
1. **Estado Global**: Não usa Redux/Zustand (useState local)
2. **Routing**: React Router v6 → Next.js App Router
3. **API Calls**: Fetch direto → API Routes proxy
4. **Auth**: localStorage → Cookies + middleware
5. **File Upload**: XMLHttpRequest → Fetch API + Server Actions
6. **Styling**: Tailwind classes → Mantido igual

### **Dependências Críticas**
- ✅ **AWS SDK**: Para S3 operations
- ✅ **File API**: Para upload progress
- ✅ **Drag & Drop API**: Para DropZone
- ✅ **Video API**: Para VideoPlayer
- ✅ **LocalStorage**: Para auth tokens

### **Funcionalidades Únicas**
- ✅ **Sanitização inteligente**: Preserva estrutura de pastas
- ✅ **Conversão automática**: MediaConvert integration
- ✅ **Player customizado**: Controles personalizados
- ✅ **Upload robusto**: Retry + progress + validation
- ✅ **Gerenciador avançado**: Navegação hierárquica

---

## 📋 **CHECKLIST DE MIGRAÇÃO**

### **Preparação**
- [ ] Análise completa da estrutura atual ✅
- [ ] Mapeamento de dependências ✅
- [ ] Identificação de breaking changes ✅
- [ ] Planejamento de testes ✅

### **Execução**
- [ ] Setup Next.js project
- [ ] Migração de componentes core
- [ ] Configuração de API routes
- [ ] Implementação de middleware
- [ ] Testes de integração
- [ ] Deploy e validação

### **Validação**
- [ ] Funcionalidades mantidas 100%
- [ ] Performance igual ou melhor
- [ ] SEO implementado
- [ ] Responsividade preservada
- [ ] Testes end-to-end passando

---

**📝 Este documento serve como blueprint completo para recriar o Mediaflow em Next.js mantendo 100% das funcionalidades e melhorando a arquitetura.**