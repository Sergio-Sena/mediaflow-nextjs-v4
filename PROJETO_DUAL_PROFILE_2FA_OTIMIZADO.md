# 🔐 MEDIAFLOW DUAL PROFILE - IMPLEMENTAÇÃO OTIMIZADA

> **Adicionar perfis público/privado com 2FA SEM duplicar código**

---

## 🎯 ESTRATÉGIA: REUTILIZAR TUDO

### **O que JÁ existe e será REAPROVEITADO:**
```
✅ Dashboard atual → vira Dashboard Privado (admin)
✅ VideoPlayer → adiciona prop readOnly
✅ FileList → adiciona prop readOnly
✅ DirectUpload → só renderiza se admin
✅ FolderManager → só renderiza se admin
✅ Lambda files-handler → adiciona filtro de prefix
✅ Lambda upload-handler → adiciona validação 2FA
✅ API Gateway → adiciona 2 rotas novas apenas
```

### **O que será ADICIONADO (mínimo):**
```
➕ 1 Lambda nova: 2fa-verify
➕ 2 páginas: /2fa e /2fa/setup
➕ 1 componente: TwoFactorInput
➕ 1 hook: useProfile (public/private)
➕ Reorganizar S3: mover arquivos para public/ ou private/
```

---

## 📋 IMPLEMENTAÇÃO MÍNIMA

### **FASE 1: Backend (2h)**

#### **1.1 - Reorganizar S3 (Script Python)**
```python
# aws-setup/reorganize-s3-profiles.py
import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

# Criar pastas
s3.put_object(Bucket=BUCKET, Key='public/')
s3.put_object(Bucket=BUCKET, Key='private/')

# Mover tudo atual para private/ (seguro por padrão)
objects = s3.list_objects_v2(Bucket=BUCKET)
for obj in objects.get('Contents', []):
    key = obj['Key']
    if not key.startswith(('public/', 'private/')):
        new_key = f'private/{key}'
        s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': key}, Key=new_key)
        s3.delete_object(Bucket=BUCKET, Key=key)
        print(f'Moved: {key} → {new_key}')

print('✅ S3 reorganizado!')
```

#### **1.2 - Atualizar auth-handler (adicionar 2FA)**
```python
# aws-setup/lambda-functions/auth-handler/lambda_function.py
import pyotp

USERS = {
    'viewer@mediaflow.com': {
        'password': 'hash_viewer',
        'role': 'public',
        'totp_secret': None
    },
    'admin@mediaflow.com': {
        'password': 'hash_admin',
        'role': 'admin',
        'totp_secret': 'JBSWY3DPEHPK3PXP'  # Base32
    }
}

def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body['email']
    password = body['password']
    
    user = USERS.get(email)
    if not user or user['password'] != password:
        return cors_response(401, {'error': 'Invalid credentials'})
    
    # Público: JWT direto
    if user['role'] == 'public':
        token = jwt.encode({'email': email, 'role': 'public', 'exp': ...}, SECRET)
        return cors_response(200, {'token': token, 'role': 'public'})
    
    # Admin: requer 2FA
    temp_token = jwt.encode({'email': email, 'role': 'admin', 'exp': ...}, SECRET)
    return cors_response(200, {'temp_token': temp_token, 'requires_2fa': True})
```

#### **1.3 - Criar 2fa-verify Lambda**
```python
# aws-setup/lambda-functions/2fa-verify/lambda_function.py
import pyotp
import jwt

def lambda_handler(event, context):
    body = json.loads(event['body'])
    temp_token = body['temp_token']
    code = body['code']
    
    decoded = jwt.decode(temp_token, SECRET, algorithms=['HS256'])
    email = decoded['email']
    
    # Validar TOTP
    totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')  # Pegar do DynamoDB depois
    if not totp.verify(code):
        return cors_response(401, {'error': 'Invalid code'})
    
    # JWT admin completo
    token = jwt.encode({
        'email': email,
        'role': 'admin',
        '2fa_verified': True,
        'exp': ...
    }, SECRET)
    
    return cors_response(200, {'token': token, 'role': 'admin'})
```

#### **1.4 - Atualizar files-handler (filtro prefix)**
```python
# Adicionar no files-handler existente
def lambda_handler(event, context):
    token = event['headers']['Authorization'].replace('Bearer ', '')
    decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    role = decoded['role']
    
    prefix = event['queryStringParameters'].get('prefix', '')
    
    # Filtro por role
    if role == 'public':
        if not prefix.startswith('public/'):
            prefix = 'public/'
    elif role == 'admin' and decoded.get('2fa_verified'):
        # Admin pode acessar tudo
        pass
    else:
        return cors_response(403, {'error': 'Forbidden'})
    
    # Resto do código existente...
```

#### **1.5 - Deploy Lambdas**
```bash
# Atualizar auth-handler
cd aws-setup/lambda-functions/auth-handler
zip -r auth-handler.zip lambda_function.py
aws lambda update-function-code --function-name mediaflow-auth-handler --zip-file fileb://auth-handler.zip

# Criar 2fa-verify
cd ../2fa-verify
zip -r 2fa-verify.zip lambda_function.py
aws lambda create-function \
  --function-name mediaflow-2fa-verify \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::969430605054:role/mediaflow-lambda-role \
  --zip-file fileb://2fa-verify.zip

# Atualizar files-handler
cd ../files-handler
zip -r files-handler.zip lambda_function.py
aws lambda update-function-code --function-name mediaflow-files-handler --zip-file fileb://files-handler.zip
```

---

### **FASE 2: Frontend (3h)**

#### **2.1 - Hook useProfile (compartilhado)**
```typescript
// lib/useProfile.ts
import { useEffect, useState } from 'react'
import jwt from 'jsonwebtoken'

export function useProfile() {
  const [profile, setProfile] = useState<'public' | 'admin' | null>(null)
  const [is2FAVerified, setIs2FAVerified] = useState(false)
  
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      const decoded = jwt.decode(token) as any
      setProfile(decoded.role)
      setIs2FAVerified(decoded['2fa_verified'] || false)
    }
  }, [])
  
  return { profile, is2FAVerified, isPublic: profile === 'public', isAdmin: profile === 'admin' }
}
```

#### **2.2 - Atualizar Login (adicionar fluxo 2FA)**
```typescript
// app/(auth)/login/page.tsx - MODIFICAR APENAS handleLogin
const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault()
  
  const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  
  const data = await response.json()
  
  if (data.requires_2fa) {
    // Admin → 2FA
    localStorage.setItem('temp_token', data.temp_token)
    router.push('/2fa')
  } else {
    // Público → Dashboard direto
    localStorage.setItem('token', data.token)
    router.push('/dashboard')
  }
}
```

#### **2.3 - Criar página 2FA (nova)**
```typescript
// app/(auth)/2fa/page.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function TwoFactorPage() {
  const [code, setCode] = useState('')
  const router = useRouter()
  
  const handleVerify = async () => {
    const tempToken = localStorage.getItem('temp_token')
    
    const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/2fa/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ temp_token: tempToken, code })
    })
    
    const data = await res.json()
    
    if (data.token) {
      localStorage.setItem('token', data.token)
      localStorage.removeItem('temp_token')
      router.push('/dashboard')
    } else {
      alert('Código inválido')
    }
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-dark-900 to-dark-800">
      <div className="glass-card p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold neon-text mb-6">🔐 Autenticação 2FA</h1>
        <p className="text-gray-400 mb-6">Insira o código do Google Authenticator</p>
        
        <input
          type="text"
          maxLength={6}
          value={code}
          onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
          placeholder="000000"
          className="w-full px-4 py-3 bg-dark-800 border border-gray-700 rounded-lg text-center text-2xl tracking-widest"
        />
        
        <button onClick={handleVerify} className="btn-neon w-full mt-6">
          Verificar
        </button>
      </div>
    </div>
  )
}
```

#### **2.4 - Atualizar Dashboard (adicionar lógica de perfil)**
```typescript
// app/dashboard/page.tsx - ADICIONAR no início
'use client'

import { useProfile } from '@/lib/useProfile'

export default function DashboardPage() {
  const { profile, isPublic, isAdmin } = useProfile()
  const [currentPrefix, setCurrentPrefix] = useState('')
  
  useEffect(() => {
    // Público: força prefix public/
    if (isPublic) {
      setCurrentPrefix('public/')
    }
  }, [isPublic])
  
  return (
    <div className={isPublic ? 'theme-public' : 'theme-private'}>
      <header className={isPublic ? 'public-header' : 'private-header'}>
        <h1>
          {isPublic ? '🌐 Biblioteca Pública' : '🔐 Admin Panel'}
        </h1>
      </header>
      
      {/* Admin pode alternar entre public/private */}
      {isAdmin && (
        <div className="flex gap-2 mb-4">
          <button onClick={() => setCurrentPrefix('public/')}>Ver Público</button>
          <button onClick={() => setCurrentPrefix('private/')}>Ver Privado</button>
        </div>
      )}
      
      <FileList prefix={currentPrefix} readOnly={isPublic} />
      <VideoPlayer readOnly={isPublic} />
      
      {/* Upload só para admin */}
      {isAdmin && <DirectUpload />}
      {isAdmin && <FolderManager />}
    </div>
  )
}
```

#### **2.5 - Atualizar VideoPlayer (adicionar readOnly)**
```typescript
// components/modules/VideoPlayer.tsx - ADICIONAR prop
interface VideoPlayerProps {
  // ... props existentes
  readOnly?: boolean
}

export default function VideoPlayer({ readOnly = false, ...props }: VideoPlayerProps) {
  // ... código existente
  
  return (
    <div>
      <video ... />
      
      {/* Esconder botão delete se readOnly */}
      {!readOnly && (
        <button onClick={handleDelete}>🗑️ Deletar</button>
      )}
    </div>
  )
}
```

#### **2.6 - Atualizar FileList (adicionar readOnly)**
```typescript
// components/modules/FileList.tsx - ADICIONAR prop
interface FileListProps {
  prefix: string
  readOnly?: boolean
}

export default function FileList({ prefix, readOnly = false }: FileListProps) {
  // Buscar arquivos com prefix
  useEffect(() => {
    fetch(`/api/videos/list?prefix=${prefix}`)
  }, [prefix])
  
  return (
    <div>
      {files.map(file => (
        <div key={file.key}>
          <span>{file.name}</span>
          
          {/* Esconder ações se readOnly */}
          {!readOnly && (
            <button onClick={() => handleDelete(file)}>Delete</button>
          )}
        </div>
      ))}
    </div>
  )
}
```

#### **2.7 - Adicionar temas CSS**
```css
/* app/globals.css - ADICIONAR */

/* Tema Público */
.theme-public {
  --primary: #00b4d8;
  --accent: #00ffff;
}

.public-header {
  background: linear-gradient(135deg, #00b4d8, #0077b6);
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

/* Tema Privado */
.theme-private {
  --primary: #bf00ff;
  --accent: #ff00bf;
}

.private-header {
  background: linear-gradient(135deg, #bf00ff, #ff00bf);
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}
```

---

### **FASE 3: Deploy (30min)**

```bash
# 1. Reorganizar S3
python aws-setup/reorganize-s3-profiles.py

# 2. Build frontend
npm run build

# 3. Upload
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --delete

# 4. Invalidar cache
aws cloudfront create-invalidation --distribution-id E12GJ6BBJXZML5 --paths "/*"
```

---

## 📊 RESUMO: O QUE MUDA

### **Arquivos NOVOS (3):**
```
✅ app/(auth)/2fa/page.tsx                    # Página 2FA
✅ lib/useProfile.ts                          # Hook compartilhado
✅ aws-setup/lambda-functions/2fa-verify/     # Lambda 2FA
```

### **Arquivos MODIFICADOS (6):**
```
✅ app/(auth)/login/page.tsx                  # +10 linhas (fluxo 2FA)
✅ app/dashboard/page.tsx                     # +20 linhas (lógica perfil)
✅ components/modules/VideoPlayer.tsx         # +5 linhas (prop readOnly)
✅ components/modules/FileList.tsx            # +5 linhas (prop readOnly)
✅ app/globals.css                            # +30 linhas (temas)
✅ lambda-functions/auth-handler/             # +15 linhas (2FA)
✅ lambda-functions/files-handler/            # +10 linhas (filtro)
```

### **Total de código novo: ~200 linhas**

---

## 🎯 RESULTADO

**Antes:**
- 1 perfil único
- Acesso total para todos
- Sem 2FA

**Depois:**
- 2 perfis (público/privado)
- Público: view only em /public/
- Admin: full access em /public/ + /private/ com 2FA
- **95% do código reaproveitado**

---

**Quer que eu comece a implementar?** 🚀
