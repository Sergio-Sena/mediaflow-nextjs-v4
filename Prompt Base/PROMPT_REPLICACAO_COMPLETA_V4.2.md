# 🎬 PROMPT COMPLETO - REPLICAÇÃO MEDIAFLOW v4.2

> **Sistema de Streaming Profissional com AWS, CDN Global e Upload Inteligente**

## 🎯 **OBJETIVO PRINCIPAL**

Replicar completamente o **Mediaflow v4.2** - plataforma profissional de streaming com:
- Upload direto S3 até 5GB
- Conversão automática H.264 1080p
- Player sequencial com navegação Previous/Next
- CDN CloudFront global (400+ edge locations)
- Gerenciador hierárquico de pastas
- Design neon cyberpunk responsivo

---

## 🏗️ **ARQUITETURA AWS COMPLETA**

### **Frontend (S3 + CloudFront)**
```yaml
CDN: CloudFront Distribution
  - Edge Locations: 400+ globalmente
  - SSL: Certificado wildcard
  - Domínio: mediaflow.sstechnologies-cloud.com
  - Cache: Otimizado para streaming

Hosting: S3 Static Website
  - Bucket: mediaflow-frontend
  - Build: Next.js export estático
  - CORS: Configurado para uploads
```

### **Backend (API Gateway + Lambda)**
```yaml
API Gateway: REST API
  - Endpoint: gdb962d234.execute-api.us-east-1.amazonaws.com
  - CORS: Habilitado
  - Auth: JWT Bearer Token

Lambda Functions (6 funções):
  1. auth-handler: Autenticação JWT
  2. upload-handler: Upload multipart S3
  3. files-handler: Listagem e gerenciamento
  4. view-handler: URLs presigned para visualização
  5. convert-handler: Trigger MediaConvert
  6. cleanup-handler: Limpeza automática órfãos
```

### **Storage (S3 Buckets)**
```yaml
Buckets (3 principais):
  1. mediaflow-uploads: Arquivos originais
  2. mediaflow-processed: Vídeos convertidos
  3. mediaflow-frontend: Build estático

Estrutura S3:
  /Star/                    # Pasta principal organizada
    /SubPasta1/
      video1.mp4
      video1.ts
    /SubPasta2/
      video2.mp4
```

### **Conversão (MediaConvert)**
```yaml
MediaConvert Job:
  - Input: S3 uploads bucket
  - Output: S3 processed bucket
  - Formato: H.264 1080p
  - Trigger: Automático via S3 Event
  - Queue: Default
```

---

## 💻 **STACK TECNOLÓGICO**

### **Frontend**
```json
{
  "framework": "Next.js 14 (App Router)",
  "language": "TypeScript 5.6",
  "styling": "Tailwind CSS + CSS Modules",
  "components": "React 18 com hooks",
  "icons": "Lucide React",
  "build": "Static Export para S3"
}
```

### **Backend**
```json
{
  "runtime": "Node.js 22+",
  "api": "Next.js API Routes + AWS Lambda",
  "auth": "JWT com bcrypt",
  "aws": "@aws-sdk/client-s3 v3",
  "validation": "Zod schemas"
}
```

---

## 📁 **ESTRUTURA COMPLETA DO PROJETO**

```
mediaflow-v4.2/
├── app/                           # Next.js 14 App Router
│   ├── (auth)/
│   │   └── login/
│   │       └── page.tsx          # Página de login JWT
│   ├── api/
│   │   ├── auth/
│   │   │   └── route.ts          # Autenticação JWT
│   │   ├── upload/
│   │   │   └── route.ts          # Upload multipart S3
│   │   └── videos/
│   │       ├── route.ts          # Listagem de vídeos
│   │       └── convert/
│   │           └── route.ts      # Trigger conversão
│   ├── dashboard/
│   │   └── page.tsx              # Dashboard principal
│   ├── globals.css               # Estilos neon cyberpunk
│   ├── layout.tsx                # Layout raiz
│   └── page.tsx                  # Página inicial
├── components/
│   ├── modules/
│   │   ├── Analytics.tsx         # Métricas em tempo real
│   │   ├── DirectUpload.tsx      # Upload direto S3 (5GB)
│   │   ├── FileList.tsx          # Lista hierárquica
│   │   ├── FolderManager.tsx     # Gerenciador avançado
│   │   ├── VideoPlayer.tsx       # Player sequencial
│   │   └── HLSPlayer.tsx         # Player .ts files
│   └── ui/                       # Componentes base
├── lib/
│   ├── aws-client.ts             # Cliente AWS S3
│   ├── aws-config.ts             # Configurações AWS
│   └── multipart-upload.ts       # Upload inteligente
├── aws-setup/                    # Scripts de deploy
│   ├── lambda-functions/         # 6 funções Lambda
│   │   ├── auth-handler/
│   │   ├── upload-handler/
│   │   ├── files-handler/
│   │   ├── view-handler/
│   │   ├── convert-handler/
│   │   └── cleanup-handler/
│   ├── setup-buckets.py          # Criação S3 buckets
│   ├── create-api-gateway.py     # API Gateway
│   ├── create-cloudfront-cdn.py  # CDN global
│   └── deploy.sh                 # Deploy completo
├── public/
│   └── upload_direto.html        # Upload direto (bypass)
├── .env.local                    # Variáveis ambiente
├── package.json                  # Dependências
├── tailwind.config.js            # Config Tailwind
├── next.config.js                # Config Next.js
└── README.md                     # Documentação
```

---

## 🎨 **DESIGN SYSTEM NEON CYBERPUNK**

### **Paleta de Cores**
```css
:root {
  --neon-cyan: #00ffff;
  --neon-purple: #bf00ff;
  --neon-pink: #ff00bf;
  --dark-900: #0a0a0f;
  --dark-800: #1a1a2e;
  --glass-bg: rgba(26, 26, 46, 0.4);
}
```

### **Componentes Base**
```css
.btn-neon {
  background: linear-gradient(to right, #00ffff, #bf00ff);
  color: #0a0a0f;
  border-radius: 12px;
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
  min-height: 44px; /* Touch-friendly */
}

.glass-card {
  background: rgba(26, 26, 46, 0.4);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 16px;
}

.neon-text {
  background: linear-gradient(to right, #00ffff, #bf00ff);
  -webkit-background-clip: text;
  color: transparent;
}
```

---

## 🚀 **FUNCIONALIDADES CORE**

### **1. Upload Direto S3 (DirectUpload)**
```typescript
// components/modules/DirectUpload.tsx
interface DirectUploadProps {
  maxSize: number; // 5GB = 5 * 1024 * 1024 * 1024
  allowedTypes: string[];
  onUploadComplete: (file: UploadedFile) => void;
}

// Funcionalidades:
- Drag & drop visual
- Progress tracking em tempo real
- Upload multipart para arquivos grandes
- Validação de tipo e tamanho
- Preview de arquivos
- Cancelamento de upload
```

### **2. Player Sequencial (VideoPlayer)**
```typescript
// components/modules/VideoPlayer.tsx
interface VideoPlayerProps {
  src: string;
  playlist: VideoFile[];
  currentIndex: number;
  onVideoChange: (video: VideoFile) => void;
}

// Funcionalidades:
- Navegação Previous/Next
- Controles touch-friendly
- Fullscreen nativo
- Keyboard shortcuts (ESC, ←, →, Space)
- Auto-play próximo vídeo
- Suporte .ts e .mp4
- Progress bar interativa
```

### **3. Gerenciador Hierárquico (FolderManager)**
```typescript
// components/modules/FolderManager.tsx
interface FolderManagerProps {
  currentPath: string;
  onPathChange: (path: string) => void;
}

// Funcionalidades:
- Navegação breadcrumbs
- Seleção em lote (checkboxes)
- Delete múltiplo com confirmação
- Busca global em todas as pastas
- Contagem inteligente (subpastas + arquivos)
- Duplo clique para navegar
- Filtros por tipo de arquivo
```

---

## 🔧 **CONFIGURAÇÃO AWS**

### **1. S3 Buckets**
```python
# aws-setup/setup-buckets.py
import boto3

def create_buckets():
    s3 = boto3.client('s3')
    
    buckets = [
        'mediaflow-uploads',
        'mediaflow-processed', 
        'mediaflow-frontend'
    ]
    
    for bucket in buckets:
        s3.create_bucket(Bucket=bucket)
        
        # CORS para uploads
        s3.put_bucket_cors(
            Bucket=bucket,
            CORSConfiguration={
                'CORSRules': [{
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET', 'POST', 'PUT'],
                    'AllowedOrigins': ['*']
                }]
            }
        )
```

### **2. Lambda Functions**
```python
# aws-setup/deploy-lambdas.py
lambda_functions = {
    'auth-handler': {
        'runtime': 'nodejs22.x',
        'handler': 'index.handler',
        'environment': {
            'JWT_SECRET': 'your-secret-key'
        }
    },
    'upload-handler': {
        'runtime': 'nodejs22.x', 
        'handler': 'index.handler',
        'timeout': 300,
        'memory': 1024
    }
    # ... outras 4 funções
}
```

### **3. CloudFront CDN**
```python
# aws-setup/create-cloudfront-cdn.py
def create_cdn():
    cloudfront = boto3.client('cloudfront')
    
    distribution = {
        'Origins': [{
            'Id': 'S3-mediaflow-frontend',
            'DomainName': 'mediaflow-frontend.s3.amazonaws.com',
            'S3OriginConfig': {
                'OriginAccessIdentity': ''
            }
        }],
        'DefaultCacheBehavior': {
            'TargetOriginId': 'S3-mediaflow-frontend',
            'ViewerProtocolPolicy': 'redirect-to-https',
            'Compress': True
        },
        'Aliases': ['mediaflow.sstechnologies-cloud.com'],
        'ViewerCertificate': {
            'AcmCertificateArn': 'arn:aws:acm:us-east-1:...',
            'SSLSupportMethod': 'sni-only'
        }
    }
```

---

## 📱 **RESPONSIVIDADE MOBILE**

### **Breakpoints Tailwind**
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'xs': '475px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    }
  }
}
```

### **Componentes Touch-Friendly**
```css
/* Botões mínimo 44px para touch */
.btn-touch {
  min-height: 44px;
  min-width: 44px;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

/* Player mobile otimizado */
@media (max-width: 768px) {
  .video-controls {
    padding: 16px;
    font-size: 18px;
  }
  
  .control-button {
    min-height: 48px;
    min-width: 48px;
  }
}
```

---

## 🔐 **AUTENTICAÇÃO JWT**

### **Login Component**
```typescript
// app/(auth)/login/page.tsx
export default function LoginPage() {
  const handleLogin = async (email: string, password: string) => {
    const response = await fetch('/api/auth', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    if (response.ok) {
      const { token } = await response.json();
      localStorage.setItem('token', token);
      router.push('/dashboard');
    }
  };
}
```

### **API Route Auth**
```typescript
// app/api/auth/route.ts
import jwt from 'jsonwebtoken';

export async function POST(request: Request) {
  const { email, password } = await request.json();
  
  // Validar credenciais
  if (email === process.env.ADMIN_EMAIL && password === process.env.ADMIN_PASSWORD) {
    const token = jwt.sign(
      { email, role: 'admin' },
      process.env.JWT_SECRET!,
      { expiresIn: '24h' }
    );
    
    return Response.json({ success: true, token });
  }
  
  return Response.json({ success: false }, { status: 401 });
}
```

---

## 📊 **ANALYTICS E MONITORAMENTO**

### **Analytics Component**
```typescript
// components/modules/Analytics.tsx
export default function Analytics() {
  const [metrics, setMetrics] = useState({
    totalFiles: 0,
    totalSize: 0,
    uploadsToday: 0,
    conversionQueue: 0
  });
  
  useEffect(() => {
    // Buscar métricas da API
    fetchMetrics();
  }, []);
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <MetricCard title="Total de Arquivos" value={metrics.totalFiles} />
      <MetricCard title="Tamanho Total" value={formatBytes(metrics.totalSize)} />
      <MetricCard title="Uploads Hoje" value={metrics.uploadsToday} />
      <MetricCard title="Fila de Conversão" value={metrics.conversionQueue} />
    </div>
  );
}
```

---

## 🚀 **DEPLOY AUTOMATIZADO**

### **Script Principal**
```bash
#!/bin/bash
# aws-setup/deploy.sh

echo "🚀 Iniciando deploy Mediaflow v4.2..."

# 1. Criar buckets S3
python3 setup-buckets.py

# 2. Deploy Lambda functions
python3 deploy-lambdas.py

# 3. Criar API Gateway
python3 create-api-gateway.py

# 4. Configurar CloudFront CDN
python3 create-cloudfront-cdn.py

# 5. Build e upload frontend
npm run build
python3 upload-frontend.py

echo "✅ Deploy concluído!"
echo "🌐 URL: https://mediaflow.sstechnologies-cloud.com"
```

### **Package.json**
```json
{
  "name": "mediaflow-v4.2",
  "version": "4.2.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build && next export",
    "deploy": "npm run build && cd aws-setup && ./deploy.sh"
  },
  "dependencies": {
    "next": "^14.2.15",
    "react": "^18.3.1",
    "typescript": "^5.6.3",
    "@aws-sdk/client-s3": "^3.884.0",
    "jsonwebtoken": "^9.0.2",
    "lucide-react": "^0.460.0",
    "tailwindcss": "^3.4.14"
  }
}
```

---

## 📋 **CHECKLIST DE IMPLEMENTAÇÃO**

### **✅ Frontend (Next.js 14)**
- [ ] App Router configurado
- [ ] Componentes TypeScript
- [ ] Design system neon cyberpunk
- [ ] Responsividade mobile
- [ ] PWA ready

### **✅ Upload System**
- [ ] DirectUpload component
- [ ] Drag & drop visual
- [ ] Progress tracking
- [ ] Multipart upload (5GB)
- [ ] Validação de arquivos

### **✅ Video Player**
- [ ] Player sequencial
- [ ] Navegação Previous/Next
- [ ] Controles touch-friendly
- [ ] Suporte .ts e .mp4
- [ ] Fullscreen nativo

### **✅ Folder Management**
- [ ] Navegação hierárquica
- [ ] Breadcrumbs
- [ ] Seleção em lote
- [ ] Busca global
- [ ] Delete múltiplo

### **✅ AWS Infrastructure**
- [ ] 3 S3 buckets configurados
- [ ] 6 Lambda functions
- [ ] API Gateway REST
- [ ] CloudFront CDN global
- [ ] MediaConvert automático

### **✅ Security & Auth**
- [ ] JWT robusto
- [ ] CORS configurado
- [ ] SSL wildcard
- [ ] Validação de entrada

### **✅ Performance**
- [ ] Lighthouse 95+
- [ ] CDN global (400+ edges)
- [ ] Lazy loading
- [ ] Code splitting
- [ ] Image optimization

---

## 🎯 **RESULTADO FINAL**

**Sistema Mediaflow v4.2 100% funcional:**
- 🌍 **URL**: https://mediaflow.sstechnologies-cloud.com
- 🔑 **Login**: admin@mediaflow.com / senha123
- 📤 **Upload**: Até 5GB direto S3
- 🎥 **Player**: Sequencial com navegação
- 📁 **Gerenciador**: Hierárquico com busca global
- ⚡ **Performance**: Lighthouse 95+ | Uptime 99.9%
- 🌐 **CDN**: CloudFront global (400+ edge locations)

---

**🎬 "De conceito a produção enterprise em uma única implementação!" - Mediaflow Team** 🚀