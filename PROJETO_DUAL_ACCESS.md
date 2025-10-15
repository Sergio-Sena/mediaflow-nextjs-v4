# 🔐 PROJETO: MEDIAFLOW DUAL PROFILE - PÚBLICO + PRIVADO

> **Sistema de Streaming com Separação Total de Perfis e Autenticação 2FA**

---

## 📋 METODOLOGIA C.E.R.T.O

### **C - CONTEXTO**
**Situação Atual:**
- Mediaflow v4.2 em produção com acesso único
- Todos os usuários têm acesso total (upload, delete, gerenciamento)
- Necessidade de compartilhar conteúdo sem expor controles administrativos

**Problema:**
- Não há separação entre conteúdo público e privado
- Risco de usuários externos acessarem área administrativa
- Falta de camada extra de segurança para operações críticas

**Objetivo:**
Criar sistema com **dois perfis isolados**:
1. **PERFIL PÚBLICO** - Conteúdo visível a todos (apenas visualização)
2. **PERFIL PRIVADO** - Conteúdo restrito + controles admin (requer 2FA)

---

### **E - ESPECIFICAÇÃO**

#### **Perfil Público (Public Profile)**
```yaml
Acesso: Login simples (email + senha)
Conteúdo: Pasta /public/ no S3
Permissões:
  - ✅ Visualizar vídeos públicos
  - ✅ Navegar por pastas públicas
  - ✅ Buscar conteúdo público
  - ❌ Upload
  - ❌ Delete
  - ❌ Gerenciamento
  - ❌ Ver conteúdo privado

UI:
  - Tema: Azul/Cyan (visualização)
  - Header: "Mediaflow - Biblioteca Pública"
  - Sem botões de ação (upload/delete)
  - Player read-only
```

#### **Perfil Privado (Private Profile)**
```yaml
Acesso: Login + Google Authenticator (2FA)
Conteúdo: Pasta /private/ no S3
Permissões:
  - ✅ Tudo do perfil público +
  - ✅ Visualizar conteúdo privado
  - ✅ Upload até 5GB
  - ✅ Delete arquivos/pastas
  - ✅ Gerenciamento completo
  - ✅ Mover arquivos entre público/privado
  - ✅ Analytics e logs

UI:
  - Tema: Purple/Pink (administração)
  - Header: "Mediaflow - Admin Panel 🔐"
  - Todos os controles visíveis
  - Indicador 2FA ativo
```

---

### **R - REQUISITOS TÉCNICOS**

#### **1. Estrutura S3 Separada**
```
mediaflow-uploads-969430605054/
├── public/                    # Conteúdo público
│   ├── Movies/
│   ├── Series/
│   └── Documentaries/
└── private/                   # Conteúdo privado (2FA)
    ├── Personal/
    ├── Work/
    └── Archive/
```

#### **2. Sistema de Autenticação**
```typescript
// Fluxo Público
Login → JWT (role: public) → Dashboard Público

// Fluxo Privado  
Login → JWT (role: admin) → 2FA Google Authenticator → JWT Admin → Dashboard Privado
```

#### **3. Lambda Functions Atualizadas**
```python
# auth-handler: Login inicial
USERS = {
    'public@mediaflow.com': {
        'password': 'hash_public',
        'role': 'public',
        'totp_secret': None
    },
    'admin@mediaflow.com': {
        'password': 'hash_admin', 
        'role': 'admin',
        'totp_secret': 'BASE32_SECRET'  # Google Authenticator
    }
}

# files-handler: Filtro por perfil
def list_files(role, path):
    if role == 'public':
        # Apenas /public/
        return s3.list_objects(Prefix='public/')
    elif role == 'admin':
        # /public/ + /private/
        return s3.list_objects(Prefix=path)
```

#### **4. API Gateway - Rotas Protegidas**
```yaml
Público (role: public):
  - GET /files?prefix=public/
  - GET /view/{key}  # Apenas public/*

Privado (role: admin + 2FA verified):
  - GET /files?prefix=*
  - POST /upload/*
  - DELETE /files/*
  - POST /files/move
  - POST /cleanup
```

---

### **T - TECNOLOGIAS**

#### **Frontend**
```json
{
  "framework": "Next.js 14",
  "language": "TypeScript 5.6",
  "2fa": "speakeasy (TOTP)",
  "qrcode": "qrcode.react",
  "styling": "Tailwind CSS",
  "icons": "Lucide React"
}
```

#### **Backend**
```json
{
  "runtime": "Python 3.11 (Lambda)",
  "2fa": "pyotp (Google Authenticator)",
  "auth": "JWT + TOTP",
  "storage": "AWS S3",
  "api": "API Gateway REST"
}
```

#### **Segurança**
```json
{
  "jwt": "HS256 com role",
  "2fa": "TOTP (Time-based OTP)",
  "session": "JWT refresh token",
  "encryption": "TOTP secrets em DynamoDB"
}
```

---

### **O - OPERACIONALIZAÇÃO**

## 🏗️ Arquitetura Completa

### **Fluxo de Autenticação**
```
1. Login Inicial → JWT com role (public/admin)
2. Dashboard Público → Visualização de vídeos
3. Botão "Área Admin" → Segunda autenticação (PIN/Senha)
4. Dashboard Privado → Acesso completo
```

### **Estrutura de Pastas**
```
app/
├── (auth)/
│   ├── login/              # Login inicial (público)
│   └── admin-auth/         # Segunda autenticação (admin)
├── dashboard/              # Área pública (view only)
└── admin/                  # Área privada (full access)
    ├── upload/
    ├── manager/
    └── settings/
```

---

## 📋 Implementação

### **1. Sistema de Roles**

#### Lambda auth-handler atualizada:
```python
# Dois tipos de usuários
USERS = {
    'user@mediaflow.com': {
        'password': 'hash_senha_publica',
        'role': 'public'
    },
    'admin@mediaflow.com': {
        'password': 'hash_senha_admin',
        'role': 'admin'
    }
}

# JWT com role
token = jwt.encode({
    'email': email,
    'role': user['role'],
    'exp': datetime.utcnow() + timedelta(hours=24)
}, SECRET_KEY)
```

#### Middleware de verificação:
```typescript
// lib/auth.ts
export function checkRole(token: string): 'public' | 'admin' | null {
  const decoded = jwt.verify(token, SECRET_KEY)
  return decoded.role
}
```

---

### **2. Componentes por Área**

#### Dashboard Público (View Only):
- ✅ VideoPlayer (sem delete)
- ✅ FolderNavigation (sem criar/deletar pastas)
- ✅ Search
- ❌ Upload
- ❌ Manager
- ❌ Bulk Delete

#### Dashboard Admin (Full Access):
- ✅ Tudo do público +
- ✅ DirectUpload
- ✅ FolderManager
- ✅ Bulk Operations
- ✅ Analytics
- ✅ Settings

---

### **3. Segunda Autenticação Admin**

#### Página /admin-auth:
```typescript
// app/(auth)/admin-auth/page.tsx
export default function AdminAuth() {
  const [pin, setPin] = useState('')
  
  const handleAuth = async () => {
    const response = await fetch('/api/auth/admin-verify', {
      method: 'POST',
      body: JSON.stringify({ pin })
    })
    
    if (response.ok) {
      // Atualiza token com flag admin_verified
      router.push('/admin')
    }
  }
  
  return (
    <div className="admin-auth-container">
      <h1>🔐 Acesso Administrativo</h1>
      <input 
        type="password" 
        placeholder="PIN Admin"
        value={pin}
        onChange={(e) => setPin(e.target.value)}
      />
      <button onClick={handleAuth}>Verificar</button>
    </div>
  )
}
```

#### Lambda admin-verify:
```python
ADMIN_PIN = os.environ.get('ADMIN_PIN', '1234')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    pin = body.get('pin')
    
    if pin == ADMIN_PIN:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'admin_token': generate_admin_token()
            })
        }
    
    return {
        'statusCode': 401,
        'body': json.dumps({'success': False})
    }
```

---

### **4. Proteção de Rotas**

#### Middleware Next.js:
```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')
  const adminToken = request.cookies.get('admin_token')
  
  // Rotas admin requerem admin_token
  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (!adminToken) {
      return NextResponse.redirect(new URL('/admin-auth', request.url))
    }
  }
  
  // Rotas públicas requerem apenas token
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }
  
  return NextResponse.next()
}
```

---

### **5. UI Diferenciada**

#### Botão de Acesso Admin no Dashboard Público:
```typescript
// components/AdminAccessButton.tsx
export default function AdminAccessButton() {
  const [role, setRole] = useState<string>('')
  
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      const decoded = jwt.decode(token)
      setRole(decoded.role)
    }
  }, [])
  
  if (role !== 'admin') return null
  
  return (
    <button 
      onClick={() => router.push('/admin-auth')}
      className="btn-admin-access"
    >
      🔐 Área Administrativa
    </button>
  )
}
```

---

## 🎨 Design System

### **Área Pública**
- Tema: Azul/Cyan (visualização)
- Botões: Apenas navegação e play
- Header: "Mediaflow - Biblioteca"

### **Área Privada**
- Tema: Purple/Pink (administração)
- Botões: Upload, delete, gerenciamento
- Header: "Mediaflow - Admin Panel"

---

## 📊 Estrutura de Dados

### **Usuários Sugeridos**
```json
{
  "public_users": [
    {
      "email": "viewer@mediaflow.com",
      "password": "viewer123",
      "role": "public"
    }
  ],
  "admin_users": [
    {
      "email": "admin@mediaflow.com",
      "password": "admin123",
      "role": "admin",
      "pin": "1234"
    }
  ]
}
```

---

## 🚀 Roadmap de Implementação

### **Fase 1: Backend (Lambda + API Gateway)**
- [ ] Atualizar auth-handler com roles
- [ ] Criar admin-verify Lambda
- [ ] Adicionar rotas /auth/admin-verify
- [ ] Atualizar JWT com role

### **Fase 2: Frontend (Páginas)**
- [ ] Criar /admin-auth page
- [ ] Criar /admin layout
- [ ] Duplicar dashboard para /admin
- [ ] Adicionar middleware de proteção

### **Fase 3: Componentes**
- [ ] Criar versão read-only dos componentes
- [ ] Adicionar AdminAccessButton
- [ ] Atualizar VideoPlayer (remover delete para público)
- [ ] Atualizar FolderNavigation (remover ações para público)

### **Fase 4: UI/UX**
- [ ] Tema diferenciado para admin
- [ ] Indicador visual de área (público/admin)
- [ ] Transição suave entre áreas
- [ ] Logout separado por área

### **Fase 5: Deploy**
- [ ] Deploy Lambdas
- [ ] Atualizar API Gateway
- [ ] Build e deploy frontend
- [ ] Testar fluxo completo

---

## 🔒 Segurança

### **Medidas Implementadas**
- ✅ JWT com role
- ✅ Segunda autenticação para admin
- ✅ Middleware de proteção de rotas
- ✅ Tokens separados (token + admin_token)
- ✅ PIN admin em variável de ambiente
- ✅ Validação server-side em todas as APIs

### **APIs Protegidas**
```
Público (role: public):
- GET /files (list)
- GET /view/{key}

Admin (role: admin + admin_token):
- POST /upload/*
- DELETE /files/*
- POST /files/bulk-delete
- POST /convert
- POST /cleanup
```

---

## 📝 Configuração

### **Variáveis de Ambiente**
```bash
# .env.local
JWT_SECRET=seu_secret_aqui
ADMIN_PIN=1234

# Lambda Environment Variables
ADMIN_PIN=1234
JWT_SECRET=mesmo_secret_do_frontend
```

---

## 🎯 Resultado Final

### **Fluxo Usuário Público**
1. Login → viewer@mediaflow.com
2. Dashboard → Visualiza vídeos
3. Sem botões de upload/delete
4. Tema azul/cyan

### **Fluxo Usuário Admin**
1. Login → admin@mediaflow.com
2. Dashboard → Visualiza vídeos + botão "Área Admin"
3. Clica "Área Admin" → Pede PIN
4. Insere PIN → Redireciona para /admin
5. Acesso completo: upload, delete, gerenciamento
6. Tema purple/pink

---

## 💡 Melhorias Futuras

- [ ] Sistema de permissões granulares
- [ ] Logs de ações admin
- [ ] Múltiplos níveis de admin
- [ ] Gestão de usuários via UI
- [ ] 2FA com autenticador
- [ ] Sessões com timeout diferenciado

---

**Status**: 📋 Planejamento Completo
**Próximo Passo**: Implementar Fase 1 (Backend)
