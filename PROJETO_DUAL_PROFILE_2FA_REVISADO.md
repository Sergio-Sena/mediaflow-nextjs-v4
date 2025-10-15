# 🔐 MEDIAFLOW DUAL PROFILE - PLANO REVISADO v2

> **Implementação otimizada de perfis público/privado com Google Authenticator 2FA**

---

## ✅ STATUS ATUAL DO PROJETO

### **Já Implementado:**
- ✅ Upload com organização automática (Vídeos → raiz/, Imagens → Fotos/, Docs → Documentos/)
- ✅ Verificação de arquivos duplicados antes do upload
- ✅ Feedback visual melhorado para duplicatas
- ✅ Lambda upload-handler com check_file_exists()
- ✅ Estrutura S3 organizada (Star/, Anime/, Fotos/, Documentos/, raiz/)

### **Estrutura S3 Atual:**
```
mediaflow-uploads-969430605054/
├── Anime/                  # Conteúdo anime
├── Documentos/             # PDFs, DOCs, etc
├── Fotos/                  # Imagens JPG, PNG, etc
├── Lara_Croft/            # Pasta específica
├── Seart/                 # Pasta específica
├── Star/                  # Pasta principal
│   ├── Comatozze/
│   └── Diversos/
├── Video/                 # Pasta de vídeos
└── raiz/                  # Vídeos soltos (vazia após reorganização)
```

---

## 🎯 OBJETIVO DO PROJETO

Criar **dois perfis isolados** sem duplicar código:

### **PERFIL PÚBLICO (Viewer)**
- Login simples (email + senha)
- Acesso apenas a pasta `/public/` no S3
- View only (sem upload, delete, gerenciamento)
- Tema Azul/Cyan

### **PERFIL PRIVADO (Admin)**
- Login + Google Authenticator (2FA obrigatório)
- Acesso a `/public/` + `/private/` + todas pastas atuais
- Full access (upload, delete, gerenciamento)
- Tema Purple/Pink

---

## 📋 PLANO DE IMPLEMENTAÇÃO REVISADO

### **FASE 1: Reorganização S3 (30min)**

#### **1.1 - Criar estrutura public/private**
```python
# aws-setup/reorganize-s3-dual-profile.py
import boto3

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

# Criar pastas
s3.put_object(Bucket=BUCKET, Key='public/')
s3.put_object(Bucket=BUCKET, Key='private/')

# Decisão: O que vai para public/ e o que vai para private/?
# Sugestão:
# - public/ → Anime/, Video/ (conteúdo compartilhável)
# - private/ → Star/, Lara_Croft/, Seart/ (conteúdo pessoal)
# - Manter: Fotos/, Documentos/, raiz/ (uploads automáticos)

# Mover Anime para public/
objects = s3.list_objects_v2(Bucket=BUCKET, Prefix='Anime/')
for obj in objects.get('Contents', []):
    key = obj['Key']
    new_key = f"public/{key}"
    s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': key}, Key=new_key)
    s3.delete_object(Bucket=BUCKET, Key=key)

# Mover Video para public/
objects = s3.list_objects_v2(Bucket=BUCKET, Prefix='Video/')
for obj in objects.get('Contents', []):
    key = obj['Key']
    new_key = f"public/{key}"
    s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': key}, Key=new_key)
    s3.delete_object(Bucket=BUCKET, Key=key)

# Mover Star para private/
objects = s3.list_objects_v2(Bucket=BUCKET, Prefix='Star/')
for obj in objects.get('Contents', []):
    key = obj['Key']
    new_key = f"private/{key}"
    s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': key}, Key=new_key)
    s3.delete_object(Bucket=BUCKET, Key=key)

# Mover Lara_Croft para private/
objects = s3.list_objects_v2(Bucket=BUCKET, Prefix='Lara_Croft/')
for obj in objects.get('Contents', []):
    key = obj['Key']
    new_key = f"private/{key}"
    s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': key}, Key=new_key)
    s3.delete_object(Bucket=BUCKET, Key=key)

# Mover Seart para private/
objects = s3.list_objects_v2(Bucket=BUCKET, Prefix='Seart/')
for obj in objects.get('Contents', []):
    key = obj['Key']
    new_key = f"private/{key}"
    s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': key}, Key=new_key)
    s3.delete_object(Bucket=BUCKET, Key=key)

print('✅ S3 reorganizado com public/ e private/')
```

**Resultado:**
```
mediaflow-uploads-969430605054/
├── public/                 # Conteúdo público (viewer pode ver)
│   ├── Anime/
│   └── Video/
├── private/                # Conteúdo privado (só admin com 2FA)
│   ├── Star/
│   ├── Lara_Croft/
│   └── Seart/
├── Fotos/                  # Uploads automáticos (admin)
├── Documentos/             # Uploads automáticos (admin)
└── raiz/                   # Uploads automáticos (admin)
```

---

### **FASE 2: Backend - Lambdas (1h30min)**

#### **2.1 - Atualizar auth-handler (adicionar 2FA)**

**Arquivo:** `aws-setup/lambda-functions/auth-handler/lambda_function.py`

```python
import json
import jwt
import bcrypt
from datetime import datetime, timedelta

SECRET_KEY = 'seu_secret_jwt'

USERS = {
    'viewer@mediaflow.com': {
        'password_hash': '$2b$12$...hash_bcrypt...',  # viewer123
        'role': 'public',
        'totp_secret': None
    },
    'admin@mediaflow.com': {
        'password_hash': '$2b$12$...hash_bcrypt...',  # admin123
        'role': 'admin',
        'totp_secret': 'JBSWY3DPEHPK3PXP'  # Google Authenticator secret
    }
}

def lambda_handler(event, context):
    if event['httpMethod'] == 'OPTIONS':
        return cors_response(200, {})
    
    body = json.loads(event['body'])
    email = body.get('email')
    password = body.get('password')
    
    user = USERS.get(email)
    if not user:
        return cors_response(401, {'success': False, 'message': 'Invalid credentials'})
    
    # Verificar senha
    if not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return cors_response(401, {'success': False, 'message': 'Invalid credentials'})
    
    # Perfil público: JWT direto
    if user['role'] == 'public':
        token = jwt.encode({
            'email': email,
            'role': 'public',
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        
        return cors_response(200, {
            'success': True,
            'token': token,
            'role': 'public'
        })
    
    # Perfil admin: requer 2FA
    if user['role'] == 'admin':
        temp_token = jwt.encode({
            'email': email,
            'role': 'admin',
            'requires_2fa': True,
            'exp': datetime.utcnow() + timedelta(minutes=5)
        }, SECRET_KEY, algorithm='HS256')
        
        return cors_response(200, {
            'success': True,
            'temp_token': temp_token,
            'requires_2fa': True
        })

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
```

#### **2.2 - Criar 2fa-verify Lambda (NOVA)**

**Arquivo:** `aws-setup/lambda-functions/2fa-verify/lambda_function.py`

```python
import json
import jwt
import pyotp
from datetime import datetime, timedelta

SECRET_KEY = 'seu_secret_jwt'
ADMIN_TOTP_SECRET = 'JBSWY3DPEHPK3PXP'

def lambda_handler(event, context):
    if event['httpMethod'] == 'OPTIONS':
        return cors_response(200, {})
    
    body = json.loads(event['body'])
    temp_token = body.get('temp_token')
    code = body.get('code')
    
    # Decodificar temp_token
    try:
        decoded = jwt.decode(temp_token, SECRET_KEY, algorithms=['HS256'])
    except:
        return cors_response(401, {'success': False, 'message': 'Invalid token'})
    
    email = decoded['email']
    
    # Validar código TOTP (Google Authenticator)
    totp = pyotp.TOTP(ADMIN_TOTP_SECRET)
    if not totp.verify(code, valid_window=1):
        return cors_response(401, {'success': False, 'message': 'Invalid 2FA code'})
    
    # Gerar JWT admin completo
    admin_token = jwt.encode({
        'email': email,
        'role': 'admin',
        '2fa_verified': True,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    
    return cors_response(200, {
        'success': True,
        'token': admin_token,
        'role': 'admin'
    })

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
```

#### **2.3 - Atualizar files-handler (filtro por perfil)**

**Modificar:** `aws-setup/lambda-functions/files-handler/lambda_function.py`

```python
# ADICIONAR no início da função lambda_handler, após extrair token

# Extrair e validar JWT
token = event['headers'].get('Authorization', '').replace('Bearer ', '')
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    role = decoded['role']
except:
    return cors_response(401, {'error': 'Unauthorized'})

# Filtro por perfil
prefix = event['queryStringParameters'].get('prefix', '')

if role == 'public':
    # Público só acessa public/
    if not prefix.startswith('public/'):
        prefix = 'public/'
elif role == 'admin' and decoded.get('2fa_verified'):
    # Admin com 2FA acessa tudo
    pass
else:
    return cors_response(403, {'error': 'Forbidden'})

# Continuar com listagem usando prefix filtrado...
```

#### **2.4 - Atualizar upload-handler (apenas admin)**

**Modificar:** `aws-setup/lambda-functions/upload-handler/lambda_function.py`

```python
# ADICIONAR validação no início

# Extrair e validar JWT
token = event['headers'].get('Authorization', '').replace('Bearer ', '')
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    role = decoded['role']
except:
    return cors_response(401, {'error': 'Unauthorized'})

# Apenas admin com 2FA pode fazer upload
if role != 'admin' or not decoded.get('2fa_verified'):
    return cors_response(403, {'error': 'Admin with 2FA required'})

# Continuar com lógica de upload...
```

#### **2.5 - Deploy Lambdas**

```bash
# Atualizar auth-handler
cd aws-setup/lambda-functions/auth-handler
powershell Compress-Archive -Path lambda_function.py -DestinationPath auth-handler.zip -Force
aws lambda update-function-code --function-name mediaflow-auth-handler --zip-file fileb://auth-handler.zip --profile default

# Criar 2fa-verify (NOVA)
cd ../2fa-verify
powershell Compress-Archive -Path lambda_function.py -DestinationPath 2fa-verify.zip -Force
aws lambda create-function \
  --function-name mediaflow-2fa-verify \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::969430605054:role/mediaflow-lambda-role \
  --zip-file fileb://2fa-verify.zip \
  --profile default

# Atualizar files-handler
cd ../files-handler
powershell Compress-Archive -Path lambda_function.py -DestinationPath files-handler.zip -Force
aws lambda update-function-code --function-name mediaflow-files-handler --zip-file fileb://files-handler.zip --profile default

# Atualizar upload-handler
cd ../upload-handler
powershell Compress-Archive -Path lambda_function.py -DestinationPath upload-handler.zip -Force
aws lambda update-function-code --function-name mediaflow-upload-handler --zip-file fileb://upload-handler.zip --profile default
```

#### **2.6 - Adicionar rota 2FA no API Gateway**

```bash
# Criar recurso /auth/2fa
aws apigateway create-resource --rest-api-id gdb962d234 --parent-id xa5za2 --path-part 2fa --profile default

# Criar recurso /auth/2fa/verify
aws apigateway create-resource --rest-api-id gdb962d234 --parent-id <2fa-id> --path-part verify --profile default

# Adicionar método POST
aws apigateway put-method --rest-api-id gdb962d234 --resource-id <verify-id> --http-method POST --authorization-type NONE --profile default

# Integrar com Lambda
aws apigateway put-integration --rest-api-id gdb962d234 --resource-id <verify-id> --http-method POST --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:969430605054:function:mediaflow-2fa-verify/invocations --profile default

# Deploy
aws apigateway create-deployment --rest-api-id gdb962d234 --stage-name prod --profile default
```

---

### **FASE 3: Frontend (2h)**

#### **3.1 - Criar hook useProfile**

**Arquivo:** `lib/useProfile.ts` (NOVO)

```typescript
import { useEffect, useState } from 'react'

export function useProfile() {
  const [profile, setProfile] = useState<'public' | 'admin' | null>(null)
  const [is2FAVerified, setIs2FAVerified] = useState(false)
  
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        setProfile(payload.role)
        setIs2FAVerified(payload['2fa_verified'] || false)
      } catch (e) {
        console.error('Invalid token')
      }
    }
  }, [])
  
  return { 
    profile, 
    is2FAVerified, 
    isPublic: profile === 'public', 
    isAdmin: profile === 'admin' 
  }
}
```

#### **3.2 - Atualizar Login**

**Modificar:** `app/(auth)/login/page.tsx`

```typescript
// SUBSTITUIR função handleLogin

const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault()
  setLoading(true)
  
  const response = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  
  const data = await response.json()
  setLoading(false)
  
  if (!data.success) {
    setError(data.message || 'Login falhou')
    return
  }
  
  if (data.requires_2fa) {
    // Admin → redireciona para 2FA
    localStorage.setItem('temp_token', data.temp_token)
    router.push('/2fa')
  } else {
    // Público → vai direto para dashboard
    localStorage.setItem('token', data.token)
    router.push('/dashboard')
  }
}
```

#### **3.3 - Criar página 2FA**

**Arquivo:** `app/(auth)/2fa/page.tsx` (NOVO)

```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function TwoFactorPage() {
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()
  
  const handleVerify = async () => {
    if (code.length !== 6) {
      setError('Código deve ter 6 dígitos')
      return
    }
    
    setLoading(true)
    setError('')
    
    const tempToken = localStorage.getItem('temp_token')
    
    const res = await fetch('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/2fa/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ temp_token: tempToken, code })
    })
    
    const data = await res.json()
    setLoading(false)
    
    if (data.success) {
      localStorage.setItem('token', data.token)
      localStorage.removeItem('temp_token')
      router.push('/dashboard')
    } else {
      setError(data.message || 'Código inválido')
    }
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-dark-900 to-dark-800">
      <div className="glass-card p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold neon-text mb-2">🔐 Autenticação 2FA</h1>
        <p className="text-gray-400 mb-6">Insira o código do Google Authenticator</p>
        
        <input
          type="text"
          maxLength={6}
          value={code}
          onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
          placeholder="000000"
          className="w-full px-4 py-3 bg-dark-800 border border-gray-700 rounded-lg text-center text-2xl tracking-widest mb-4"
          autoFocus
        />
        
        {error && (
          <p className="text-red-400 text-sm mb-4">{error}</p>
        )}
        
        <button 
          onClick={handleVerify} 
          className="btn-neon w-full"
          disabled={loading || code.length !== 6}
        >
          {loading ? 'Verificando...' : 'Verificar'}
        </button>
      </div>
    </div>
  )
}
```

#### **3.4 - Atualizar Dashboard**

**Modificar:** `app/dashboard/page.tsx`

```typescript
// ADICIONAR no início
'use client'

import { useProfile } from '@/lib/useProfile'
import { useEffect, useState } from 'react'

export default function DashboardPage() {
  const { profile, isPublic, isAdmin } = useProfile()
  const [currentPrefix, setCurrentPrefix] = useState('')
  
  useEffect(() => {
    // Público: força prefix public/
    if (isPublic) {
      setCurrentPrefix('public/')
    } else if (isAdmin) {
      // Admin: começa em private/
      setCurrentPrefix('private/')
    }
  }, [isPublic, isAdmin])
  
  return (
    <div className={isPublic ? 'theme-public' : 'theme-private'}>
      <header className={isPublic ? 'public-header' : 'private-header'}>
        <h1>
          {isPublic ? '🌐 Biblioteca Pública' : '🔐 Admin Panel'}
        </h1>
        {isAdmin && <span className="text-sm">2FA Ativo ✓</span>}
      </header>
      
      {/* Admin pode alternar entre public/private */}
      {isAdmin && (
        <div className="flex gap-2 mb-4">
          <button 
            onClick={() => setCurrentPrefix('public/')}
            className={currentPrefix.startsWith('public/') ? 'btn-neon' : 'btn-secondary'}
          >
            Ver Público
          </button>
          <button 
            onClick={() => setCurrentPrefix('private/')}
            className={currentPrefix.startsWith('private/') ? 'btn-neon' : 'btn-secondary'}
          >
            Ver Privado
          </button>
          <button 
            onClick={() => setCurrentPrefix('')}
            className={!currentPrefix ? 'btn-neon' : 'btn-secondary'}
          >
            Ver Tudo
          </button>
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

#### **3.5 - Adicionar temas CSS**

**Modificar:** `app/globals.css`

```css
/* ADICIONAR no final */

/* Tema Público */
.theme-public {
  --primary: #00b4d8;
  --accent: #00ffff;
}

.public-header {
  background: linear-gradient(135deg, #00b4d8, #0077b6);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Tema Privado */
.theme-private {
  --primary: #bf00ff;
  --accent: #ff00bf;
}

.private-header {
  background: linear-gradient(135deg, #bf00ff, #ff00bf);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

---

### **FASE 4: Deploy Final (30min)**

```bash
# 1. Reorganizar S3
python aws-setup/reorganize-s3-dual-profile.py

# 2. Build frontend
npm run build

# 3. Upload
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --delete --profile default

# 4. Invalidar cache
aws cloudfront create-invalidation --distribution-id E12GJ6BBJXZML5 --paths "/*" --profile default
```

---

## 📊 RESUMO FINAL

### **Arquivos NOVOS (3):**
- `lib/useProfile.ts` - Hook compartilhado
- `app/(auth)/2fa/page.tsx` - Página 2FA
- `aws-setup/lambda-functions/2fa-verify/` - Lambda 2FA

### **Arquivos MODIFICADOS (7):**
- `app/(auth)/login/page.tsx` - Fluxo 2FA
- `app/dashboard/page.tsx` - Lógica de perfil
- `app/globals.css` - Temas público/privado
- `lambda-functions/auth-handler/` - Suporte 2FA
- `lambda-functions/files-handler/` - Filtro por perfil
- `lambda-functions/upload-handler/` - Validação admin
- API Gateway - Rota /auth/2fa/verify

### **Total: ~250 linhas de código novo**

---

## 🎯 RESULTADO ESPERADO

**Perfil Público:**
- Login: viewer@mediaflow.com / viewer123
- Acesso: public/Anime/, public/Video/
- Ações: View only
- Tema: Azul/Cyan

**Perfil Privado:**
- Login: admin@mediaflow.com / admin123
- 2FA: Google Authenticator (código 6 dígitos)
- Acesso: public/ + private/ + Fotos/ + Documentos/ + raiz/
- Ações: Full access
- Tema: Purple/Pink

---

**Pronto para começar a implementação?** 🚀
