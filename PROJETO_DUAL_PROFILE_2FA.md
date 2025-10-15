# 🔐 MEDIAFLOW DUAL PROFILE - PÚBLICO + PRIVADO COM 2FA

> **Sistema de Streaming com Separação Total de Perfis e Autenticação Google Authenticator**

---

## 📋 METODOLOGIA C.E.R.T.O

### **C - CONTEXTO**

**Situação Atual:**
- Mediaflow v4.2 em produção com acesso único
- Todos usuários têm acesso total (upload, delete, gerenciamento)
- Todo conteúdo está misturado no S3

**Problema:**
- Impossível compartilhar conteúdo sem expor área administrativa
- Sem separação entre conteúdo público e privado
- Falta camada extra de segurança para operações críticas

**Objetivo:**
Criar sistema com **dois perfis completamente isolados**:
1. **PERFIL PÚBLICO** - Conteúdo visível a todos (view only)
2. **PERFIL PRIVADO** - Conteúdo restrito + admin (requer Google Authenticator)

---

### **E - ESPECIFICAÇÃO**

#### **🌐 PERFIL PÚBLICO**
```yaml
Acesso: Login simples (email + senha)
Conteúdo: Pasta /public/ no S3
Usuários: Qualquer pessoa com credenciais públicas

Permissões:
  ✅ Ver vídeos públicos
  ✅ Navegar pastas públicas
  ✅ Buscar conteúdo público
  ✅ Player com controles básicos
  ❌ Upload
  ❌ Delete
  ❌ Gerenciamento
  ❌ Ver conteúdo privado
  ❌ Acessar área admin

UI/UX:
  - Tema: Azul/Cyan (visualização)
  - Header: "Mediaflow - Biblioteca Pública"
  - Sem botões de ação
  - Player read-only
  - Indicador: "Modo Público 🌐"
```

#### **🔒 PERFIL PRIVADO**
```yaml
Acesso: Login + Google Authenticator (2FA obrigatório)
Conteúdo: Pasta /private/ no S3 + acesso a /public/
Usuários: Apenas administradores com 2FA configurado

Permissões:
  ✅ Tudo do perfil público +
  ✅ Ver conteúdo privado
  ✅ Upload até 5GB
  ✅ Delete arquivos/pastas
  ✅ Mover entre public/private
  ✅ Gerenciamento completo
  ✅ Analytics e logs
  ✅ Configurações do sistema

UI/UX:
  - Tema: Purple/Pink (administração)
  - Header: "Mediaflow - Admin Panel 🔐"
  - Todos controles visíveis
  - Indicador: "Modo Privado 🔐 2FA Ativo"
  - Toggle para alternar visualização public/private
```

---

### **R - REQUISITOS TÉCNICOS**

#### **1. Estrutura S3 Isolada**
```
mediaflow-uploads-969430605054/
├── public/                     # Conteúdo público (todos veem)
│   ├── Movies/
│   │   ├── Action/
│   │   └── Comedy/
│   ├── Series/
│   └── Documentaries/
│
└── private/                    # Conteúdo privado (2FA required)
    ├── Personal/
    ├── Work/
    ├── Archive/
    └── Sensitive/
```

#### **2. Fluxo de Autenticação**

**Perfil Público:**
```
1. /login → email + senha
2. Lambda auth-handler valida
3. Retorna JWT com role: "public"
4. Redireciona para /dashboard/public
5. Acesso apenas a /public/* no S3
```

**Perfil Privado:**
```
1. /login → email + senha
2. Lambda auth-handler valida
3. Se role: "admin" → redireciona para /2fa
4. /2fa → usuário insere código Google Authenticator (6 dígitos)
5. Lambda 2fa-verify valida TOTP
6. Retorna JWT com role: "admin" + flag "2fa_verified: true"
7. Redireciona para /dashboard/private
8. Acesso total a /public/* e /private/* no S3
```

#### **3. Lambda Functions (7 funções)**

**auth-handler.py** - Login inicial
```python
import pyotp
import jwt
import bcrypt

USERS = {
    'viewer@mediaflow.com': {
        'password_hash': bcrypt.hashpw(b'viewer123', bcrypt.gensalt()),
        'role': 'public',
        'totp_secret': None
    },
    'admin@mediaflow.com': {
        'password_hash': bcrypt.hashpw(b'admin123', bcrypt.gensalt()),
        'role': 'admin',
        'totp_secret': 'JBSWY3DPEHPK3PXP'  # Base32 secret
    }
}

def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body['email']
    password = body['password']
    
    user = USERS.get(email)
    if not user or not bcrypt.checkpw(password.encode(), user['password_hash']):
        return {'statusCode': 401, 'body': json.dumps({'error': 'Invalid credentials'})}
    
    # Se público, retorna JWT direto
    if user['role'] == 'public':
        token = jwt.encode({
            'email': email,
            'role': 'public',
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, JWT_SECRET)
        return {'statusCode': 200, 'body': json.dumps({'token': token, 'role': 'public'})}
    
    # Se admin, retorna flag para 2FA
    if user['role'] == 'admin':
        temp_token = jwt.encode({
            'email': email,
            'role': 'admin',
            'requires_2fa': True,
            'exp': datetime.utcnow() + timedelta(minutes=5)
        }, JWT_SECRET)
        return {'statusCode': 200, 'body': json.dumps({
            'temp_token': temp_token,
            'requires_2fa': True
        })}
```

**2fa-verify.py** - Validação Google Authenticator
```python
import pyotp
import jwt

def lambda_handler(event, context):
    body = json.loads(event['body'])
    temp_token = body['temp_token']
    totp_code = body['totp_code']  # 6 dígitos do Google Authenticator
    
    # Decodifica temp_token
    try:
        decoded = jwt.decode(temp_token, JWT_SECRET, algorithms=['HS256'])
    except:
        return {'statusCode': 401, 'body': json.dumps({'error': 'Invalid token'})}
    
    email = decoded['email']
    user = USERS.get(email)
    
    # Valida TOTP
    totp = pyotp.TOTP(user['totp_secret'])
    if not totp.verify(totp_code, valid_window=1):
        return {'statusCode': 401, 'body': json.dumps({'error': 'Invalid 2FA code'})}
    
    # Gera JWT admin completo
    admin_token = jwt.encode({
        'email': email,
        'role': 'admin',
        '2fa_verified': True,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, JWT_SECRET)
    
    return {'statusCode': 200, 'body': json.dumps({
        'token': admin_token,
        'role': 'admin'
    })}
```

**2fa-setup.py** - Configurar Google Authenticator (primeira vez)
```python
import pyotp
import qrcode
import io
import base64

def lambda_handler(event, context):
    email = event['email']  # Do JWT
    
    # Gera secret único
    secret = pyotp.random_base32()
    
    # Gera URI para QR Code
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name='Mediaflow'
    )
    
    # Gera QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Converte para base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Salva secret no DynamoDB
    dynamodb.put_item(
        TableName='mediaflow-users',
        Item={'email': email, 'totp_secret': secret}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'secret': secret,
            'qr_code': f'data:image/png;base64,{qr_base64}'
        })
    }
```

**files-handler.py** - Listagem com filtro por perfil
```python
def lambda_handler(event, context):
    # Extrai JWT do header
    token = event['headers']['Authorization'].replace('Bearer ', '')
    decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    role = decoded['role']
    
    # Filtro por perfil
    if role == 'public':
        # Apenas /public/
        objects = s3.list_objects_v2(
            Bucket=UPLOADS_BUCKET,
            Prefix='public/'
        )
    elif role == 'admin' and decoded.get('2fa_verified'):
        # /public/ + /private/
        prefix = event['queryStringParameters'].get('prefix', '')
        objects = s3.list_objects_v2(
            Bucket=UPLOADS_BUCKET,
            Prefix=prefix
        )
    else:
        return {'statusCode': 403, 'body': json.dumps({'error': 'Forbidden'})}
    
    return {'statusCode': 200, 'body': json.dumps(objects)}
```

**upload-handler.py** - Upload apenas para admin 2FA
```python
def lambda_handler(event, context):
    token = event['headers']['Authorization'].replace('Bearer ', '')
    decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    
    # Apenas admin com 2FA
    if decoded['role'] != 'admin' or not decoded.get('2fa_verified'):
        return {'statusCode': 403, 'body': json.dumps({'error': 'Admin 2FA required'})}
    
    # Processa upload...
```

#### **4. API Gateway - Rotas Protegidas**
```yaml
Rotas Públicas (role: public):
  GET /files?prefix=public/
  GET /view/{key}  # Valida que key começa com public/

Rotas Privadas (role: admin + 2fa_verified: true):
  GET /files?prefix=*
  POST /upload/*
  DELETE /files/*
  POST /files/move
  POST /cleanup
  GET /analytics

Rotas 2FA:
  POST /auth/2fa/verify
  POST /auth/2fa/setup
  GET /auth/2fa/qrcode
```

---

### **T - TECNOLOGIAS**

#### **Frontend**
```json
{
  "framework": "Next.js 14 App Router",
  "language": "TypeScript 5.6",
  "2fa_client": "speakeasy + qrcode.react",
  "styling": "Tailwind CSS",
  "icons": "Lucide React",
  "state": "React Context API"
}
```

#### **Backend**
```json
{
  "runtime": "Python 3.11 (AWS Lambda)",
  "2fa_server": "pyotp (Google Authenticator compatible)",
  "auth": "JWT (HS256) + TOTP",
  "storage": "AWS S3 (prefixes isolados)",
  "database": "DynamoDB (TOTP secrets)",
  "api": "API Gateway REST"
}
```

#### **Dependências**
```bash
# Frontend
npm install speakeasy qrcode.react @types/speakeasy

# Backend (Lambda Layer)
pip install pyotp qrcode pillow pyjwt bcrypt -t python/
```

---

### **O - OPERACIONALIZAÇÃO**

## 🏗️ ESTRUTURA DO PROJETO

```
mediaflow-dual-profile/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx              # Login único
│   │   └── 2fa/
│   │       ├── page.tsx              # Validação Google Authenticator
│   │       └── setup/
│   │           └── page.tsx          # Configurar 2FA (primeira vez)
│   ├── dashboard/
│   │   ├── public/
│   │   │   └── page.tsx              # Dashboard público (view only)
│   │   └── private/
│   │       └── page.tsx              # Dashboard privado (full access)
│   └── api/
│       ├── auth/
│       │   ├── login/route.ts
│       │   └── 2fa/
│       │       ├── verify/route.ts
│       │       └── setup/route.ts
│       └── files/route.ts
│
├── components/
│   ├── public/                       # Componentes read-only
│   │   ├── PublicVideoPlayer.tsx
│   │   ├── PublicFileList.tsx
│   │   └── PublicNavigation.tsx
│   ├── private/                      # Componentes full access
│   │   ├── PrivateVideoPlayer.tsx
│   │   ├── DirectUpload.tsx
│   │   ├── FolderManager.tsx
│   │   └── Analytics.tsx
│   └── auth/
│       ├── TwoFactorInput.tsx        # Input 6 dígitos
│       └── QRCodeDisplay.tsx         # QR Code setup
│
├── lib/
│   ├── auth.ts                       # JWT + role check
│   ├── totp.ts                       # TOTP client
│   └── s3-client.ts                  # S3 com prefix filter
│
├── aws-setup/
│   ├── lambda-functions/
│   │   ├── auth-handler/
│   │   ├── 2fa-verify/
│   │   ├── 2fa-setup/
│   │   ├── files-handler/
│   │   ├── upload-handler/
│   │   ├── view-handler/
│   │   └── cleanup-handler/
│   ├── create-dynamodb-table.py      # Tabela para TOTP secrets
│   ├── reorganize-s3.py              # Mover arquivos para public/private
│   └── deploy-2fa.py                 # Deploy completo
│
└── middleware.ts                     # Proteção de rotas
```

---

## 🎨 DESIGN SYSTEM

### **Tema Público (Azul/Cyan)**
```css
/* globals.css - Public Theme */
.theme-public {
  --primary: #00b4d8;
  --secondary: #0077b6;
  --accent: #00ffff;
  --bg: #001219;
}

.public-header {
  background: linear-gradient(135deg, #00b4d8, #0077b6);
}

.public-card {
  border: 1px solid rgba(0, 180, 216, 0.3);
  background: rgba(0, 18, 25, 0.6);
}
```

### **Tema Privado (Purple/Pink)**
```css
/* globals.css - Private Theme */
.theme-private {
  --primary: #bf00ff;
  --secondary: #7209b7;
  --accent: #ff00bf;
  --bg: #10002b;
}

.private-header {
  background: linear-gradient(135deg, #bf00ff, #ff00bf);
}

.private-card {
  border: 1px solid rgba(191, 0, 255, 0.3);
  background: rgba(16, 0, 43, 0.6);
}
```

---

## 🚀 IMPLEMENTAÇÃO PASSO A PASSO

### **FASE 1: Backend (AWS)**

**1.1 - Criar DynamoDB para TOTP Secrets**
```python
# aws-setup/create-dynamodb-table.py
import boto3

dynamodb = boto3.client('dynamodb')

dynamodb.create_table(
    TableName='mediaflow-users',
    KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
    AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],
    BillingMode='PAY_PER_REQUEST'
)
```

**1.2 - Reorganizar S3**
```python
# aws-setup/reorganize-s3.py
import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

# Criar estrutura
s3.put_object(Bucket=BUCKET, Key='public/')
s3.put_object(Bucket=BUCKET, Key='private/')

# Mover arquivos existentes para private/ (padrão seguro)
objects = s3.list_objects_v2(Bucket=BUCKET)
for obj in objects.get('Contents', []):
    key = obj['Key']
    if not key.startswith('public/') and not key.startswith('private/'):
        # Move para private/
        s3.copy_object(
            Bucket=BUCKET,
            CopySource={'Bucket': BUCKET, 'Key': key},
            Key=f'private/{key}'
        )
        s3.delete_object(Bucket=BUCKET, Key=key)
```

**1.3 - Deploy Lambdas**
```bash
cd aws-setup/lambda-functions

# auth-handler
cd auth-handler && zip -r ../auth-handler.zip . && cd ..
aws lambda update-function-code --function-name mediaflow-auth-handler --zip-file fileb://auth-handler.zip

# 2fa-verify (nova)
cd 2fa-verify && zip -r ../2fa-verify.zip . && cd ..
aws lambda create-function \
  --function-name mediaflow-2fa-verify \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::969430605054:role/mediaflow-lambda-role \
  --zip-file fileb://2fa-verify.zip

# 2fa-setup (nova)
cd 2fa-setup && zip -r ../2fa-setup.zip . && cd ..
aws lambda create-function \
  --function-name mediaflow-2fa-setup \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::969430605054:role/mediaflow-lambda-role \
  --zip-file fileb://2fa-setup.zip
```

**1.4 - Atualizar API Gateway**
```bash
# Criar rotas 2FA
aws apigateway create-resource --rest-api-id gdb962d234 --parent-id xa5za2 --path-part 2fa
aws apigateway create-resource --rest-api-id gdb962d234 --parent-id <2fa-id> --path-part verify
aws apigateway create-resource --rest-api-id gdb962d234 --parent-id <2fa-id> --path-part setup

# Integrar com Lambdas
# ... (comandos similares aos existentes)
```

---

### **FASE 2: Frontend**

**2.1 - Página de Login**
```typescript
// app/(auth)/login/page.tsx
'use client'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  
  const handleLogin = async () => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    })
    
    const data = await res.json()
    
    if (data.requires_2fa) {
      // Admin precisa de 2FA
      localStorage.setItem('temp_token', data.temp_token)
      router.push('/2fa')
    } else {
      // Público vai direto
      localStorage.setItem('token', data.token)
      router.push('/dashboard/public')
    }
  }
  
  return (
    <div className="login-container">
      <h1>🎬 Mediaflow Login</h1>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Entrar</button>
    </div>
  )
}
```

**2.2 - Página 2FA**
```typescript
// app/(auth)/2fa/page.tsx
'use client'

export default function TwoFactorPage() {
  const [code, setCode] = useState('')
  
  const handleVerify = async () => {
    const tempToken = localStorage.getItem('temp_token')
    
    const res = await fetch('/api/auth/2fa/verify', {
      method: 'POST',
      body: JSON.stringify({ temp_token: tempToken, totp_code: code })
    })
    
    const data = await res.json()
    
    if (data.token) {
      localStorage.setItem('token', data.token)
      router.push('/dashboard/private')
    }
  }
  
  return (
    <div className="2fa-container theme-private">
      <h1>🔐 Autenticação 2FA</h1>
      <p>Insira o código do Google Authenticator</p>
      <input 
        type="text" 
        maxLength={6}
        value={code}
        onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
        placeholder="000000"
      />
      <button onClick={handleVerify}>Verificar</button>
    </div>
  )
}
```

**2.3 - Dashboard Público**
```typescript
// app/dashboard/public/page.tsx
'use client'

export default function PublicDashboard() {
  const [files, setFiles] = useState([])
  
  useEffect(() => {
    fetchFiles('public/')
  }, [])
  
  return (
    <div className="theme-public">
      <header className="public-header">
        <h1>Mediaflow - Biblioteca Pública 🌐</h1>
      </header>
      
      <PublicFileList files={files} />
      <PublicVideoPlayer />
      
      {/* SEM botões de upload/delete */}
    </div>
  )
}
```

**2.4 - Dashboard Privado**
```typescript
// app/dashboard/private/page.tsx
'use client'

export default function PrivateDashboard() {
  const [view, setView] = useState<'public' | 'private'>('private')
  const [files, setFiles] = useState([])
  
  useEffect(() => {
    fetchFiles(view === 'public' ? 'public/' : 'private/')
  }, [view])
  
  return (
    <div className="theme-private">
      <header className="private-header">
        <h1>Mediaflow - Admin Panel 🔐</h1>
        <span className="2fa-badge">2FA Ativo ✓</span>
      </header>
      
      <div className="view-toggle">
        <button onClick={() => setView('public')}>Ver Público</button>
        <button onClick={() => setView('private')}>Ver Privado</button>
      </div>
      
      <DirectUpload />
      <FolderManager />
      <PrivateVideoPlayer />
      <Analytics />
    </div>
  )
}
```

**2.5 - Middleware de Proteção**
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import jwt from 'jsonwebtoken'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value
  
  // Rotas públicas
  if (request.nextUrl.pathname.startsWith('/dashboard/public')) {
    if (!token) return NextResponse.redirect(new URL('/login', request.url))
    
    const decoded = jwt.decode(token) as any
    if (decoded.role !== 'public' && decoded.role !== 'admin') {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }
  
  // Rotas privadas
  if (request.nextUrl.pathname.startsWith('/dashboard/private')) {
    if (!token) return NextResponse.redirect(new URL('/login', request.url))
    
    const decoded = jwt.decode(token) as any
    if (decoded.role !== 'admin' || !decoded['2fa_verified']) {
      return NextResponse.redirect(new URL('/2fa', request.url))
    }
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*']
}
```

---

### **FASE 3: Deploy**

```bash
# 1. Build frontend
npm run build

# 2. Upload para S3
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --delete

# 3. Invalidar CloudFront
aws cloudfront create-invalidation --distribution-id E12GJ6BBJXZML5 --paths "/*"

# 4. Testar
echo "✅ Deploy completo!"
echo "🌐 Público: https://mediaflow.sstechnologies-cloud.com/dashboard/public"
echo "🔐 Privado: https://mediaflow.sstechnologies-cloud.com/dashboard/private"
```

---

## 🔒 SEGURANÇA

### **Camadas de Proteção**
```yaml
Camada 1: JWT com role (public/admin)
Camada 2: Google Authenticator (TOTP) para admin
Camada 3: Prefixes S3 isolados (public/ vs private/)
Camada 4: Middleware Next.js (proteção de rotas)
Camada 5: Lambda authorizer (validação server-side)
Camada 6: API Gateway (CORS + rate limiting)
```

### **Fluxo de Tokens**
```
Login → temp_token (5min) → 2FA → admin_token (24h) → refresh_token (7d)
```

---

## 📊 RESULTADO FINAL

### **Usuários de Teste**
```json
{
  "public": {
    "email": "viewer@mediaflow.com",
    "password": "viewer123",
    "acesso": "Apenas /public/"
  },
  "admin": {
    "email": "admin@mediaflow.com",
    "password": "admin123",
    "2fa": "Google Authenticator",
    "acesso": "/public/ + /private/"
  }
}
```

### **URLs**
```
Login: https://mediaflow.sstechnologies-cloud.com/login
2FA: https://mediaflow.sstechnologies-cloud.com/2fa
Público: https://mediaflow.sstechnologies-cloud.com/dashboard/public
Privado: https://mediaflow.sstechnologies-cloud.com/dashboard/private
```

---

## 🎯 CHECKLIST DE IMPLEMENTAÇÃO

### **Backend**
- [ ] DynamoDB table criada
- [ ] S3 reorganizado (public/ + private/)
- [ ] Lambda auth-handler atualizada
- [ ] Lambda 2fa-verify criada
- [ ] Lambda 2fa-setup criada
- [ ] Lambda files-handler com filtro
- [ ] API Gateway rotas 2FA
- [ ] Testes de integração

### **Frontend**
- [ ] Página login única
- [ ] Página 2FA com input 6 dígitos
- [ ] Página setup 2FA (QR Code)
- [ ] Dashboard público (read-only)
- [ ] Dashboard privado (full access)
- [ ] Componentes públicos
- [ ] Componentes privados
- [ ] Middleware de proteção
- [ ] Temas diferenciados

### **Deploy**
- [ ] Build Next.js
- [ ] Upload S3
- [ ] Invalidação CloudFront
- [ ] Testes E2E
- [ ] Documentação atualizada

---

**🎬 "De acesso único para perfis isolados com 2FA enterprise!" - Mediaflow Team** 🚀🔐
