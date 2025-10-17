# 🎬 Mediaflow v4.3 - Context Prompt para Continuação

## 📋 Estado Atual do Projeto

**Versão**: 4.3.0 | **Status**: ✅ PRODUÇÃO  
**URL**: https://mediaflow.sstechnologies-cloud.com  
**Admin**: https://mediaflow.sstechnologies-cloud.com/admin

---

## 🏗️ Arquitetura AWS

### **S3 Buckets**
- `mediaflow-uploads-969430605054` - Uploads originais + avatares + QR codes
- `mediaflow-processed-969430605054` - Vídeos convertidos H.264
- `mediaflow-frontend-969430605054` - Build Next.js estático

### **Lambda Functions (7 ativas)**
1. `mediaflow-auth-handler` - Autenticação JWT + validação DynamoDB
2. `mediaflow-list-files` - Listagem de arquivos/pastas S3
3. `mediaflow-delete-files` - Exclusão em lote
4. `mediaflow-presigned-url` - Upload direto S3
5. `mediaflow-avatar-presigned` - Upload de avatares
6. `mediaflow-update-user` - Atualização DynamoDB
7. `mediaflow-create-user` - Criação de usuários

### **DynamoDB**
- Tabela: `mediaflow-users`
- Partition Key: `user_id` (String)
- Atributos: email, password_hash, role, totp_secret, avatar_url, created_at

### **CloudFront**
- Distribution ID: `E3VQZJY8X9KQZM`
- Domínio: `mediaflow.sstechnologies-cloud.com`
- SSL: Certificado wildcard ativo
- Cache: Invalidação via `invalidate-cache.py`

---

## 👥 Sistema Multi-Usuário (v4.3)

### **Usuários Ativos**
1. **Admin** (DynamoDB)
   - User ID: `user_admin`
   - Email: `sergiosenaadmin@sstech`
   - Senha: `admin123` (hash SHA256 no DynamoDB)
   - Role: `admin`
   - S3 Prefix: `` (vazio - vê todos os arquivos)
   - TOTP: Secret único em DynamoDB
   - Avatar: S3 `avatars/avatar_user_admin.png`

2. **Lid** (DynamoDB)
   - User ID: `Lid`
   - Email: `lid@sstech`
   - Senha: `lid123`
   - Role: `user`
   - S3 Prefix: `Lid/`
   - TOTP: Secret único
   - Avatar: S3 `avatars/avatar_Lid.jpg`

3. **Sergio Sena** (DynamoDB)
   - User ID: `Sergio_sena`
   - Email: `sena@sstech`
   - Senha: `sena123`
   - Role: `user`
   - S3 Prefix: `Sergio Sena/`
   - TOTP: Secret único
   - Avatar: S3 `avatars/avatar_Sergio_sena.jpeg`

### **Fluxo de Navegação**
```
/ (initial) → /users (seleção) → /login (credenciais) → /2fa (TOTP) → /dashboard
```

### **Controle de Visibilidade**
- **Tela /users**: Sempre mostra todos os 3 usuários (useMemo removido)
- **Filtro de arquivos**: Admin vê tudo, users veem apenas seu s3_prefix
- **Botão Trocar**: Apenas em /admin (removido do /dashboard)

---

## 🔐 Sistema de Autenticação

### **JWT Payload**
```json
{
  "user_id": "user_admin",
  "email": "sergiosenaadmin@sstech",
  "role": "admin",
  "s3_prefix": "",
  "exp": 1234567890
}
```

### **LocalStorage Keys**
- `token` - JWT token
- `currentUser` - JSON com user_id, email, role, avatar_url
- `2fa_session` - Timestamp (expira em 30 minutos)

### **Lambda auth-handler**
- Valida email/password contra DynamoDB (sem hardcoded)
- Retorna JWT com user_id, role e s3_prefix
- Hash: SHA256
- SECRET_KEY: mediaflow_super_secret_key_2025

---

## 🖼️ Sistema de Avatar

### **Fluxo de Upload**
1. Frontend chama `/api/avatar-presigned` com userId e fileType
2. Lambda gera presigned URL com ACL public-read
3. Frontend faz PUT direto no S3
4. Frontend chama `/api/update-user` com avatar_url
5. Lambda atualiza DynamoDB
6. Callback atualiza estado + localStorage

### **S3 Bucket Policy**
```json
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": [
    "arn:aws:s3:::mediaflow-uploads-969430605054/avatars/*",
    "arn:aws:s3:::mediaflow-uploads-969430605054/qrcodes/*"
  ]
}
```

### **CORS Configuration**
```json
{
  "AllowedOrigins": ["*"],
  "AllowedMethods": ["GET", "PUT", "POST"],
  "AllowedHeaders": ["*"],
  "ExposeHeaders": ["ETag"]
}
```

### **Componente AvatarUpload**
- Props: userId, currentAvatarUrl, size (sm/md/lg), onAvatarUpdate
- Drag & drop support
- Fallback: User/UserCircle icons
- onError handler para imagens quebradas

---

## 📁 Estrutura de Arquivos Críticos

### **Frontend**
```
app/
├── users/page.tsx          # Seleção de usuário (filtro role-based)
├── login/page.tsx          # Credenciais
├── 2fa/page.tsx            # TOTP validation
├── dashboard/page.tsx      # Dashboard com avatar
└── admin/page.tsx          # Gerenciamento de usuários

components/
└── AvatarUpload.tsx        # Upload component reutilizável

lib/
├── s3Client.ts             # AWS SDK S3
└── dynamoClient.ts         # AWS SDK DynamoDB
```

### **Backend**
```
aws-setup/lambda-functions/
├── auth-handler/           # Autenticação
├── avatar-presigned/       # Presigned URLs
├── update-user/            # Update DynamoDB
└── create-user/            # Criar usuários
```

---

## 🐛 Problemas Resolvidos Recentemente

### **Visibilidade de Cards (v4.4)**
- **Problema**: Logout mostrava apenas último usuário logado
- **Causa**: useMemo guardava estado anterior
- **Solução**: Removido useMemo, sempre mostra todos os usuários

### **Avatar não Carregava**
- **Problema**: 403 Forbidden no S3
- **Causa**: Bucket policy não permitia acesso público
- **Solução**: Bucket policy para `avatars/*` + CORS + ACL public-read

### **Auth Multi-User (v4.4)**
- **Problema**: Senha hardcoded na Lambda (má prática)
- **Causa**: Admin tinha credenciais no código
- **Solução**: Removido hardcoded, senha hash no DynamoDB

---

## 🚀 Deploy Workflow

```bash
# Build
npm run build

# Deploy frontend
cd aws-setup
python upload-frontend.py

# Invalidar cache CloudFront
python invalidate-cache.py

# Aguardar 2-3 minutos
# Testar com Ctrl+Shift+R (hard refresh)
```

---

## 📊 Próximos Passos (v4.5)

### **Prioridade Alta**
- [ ] Editar usuários existentes (email, senha, role)
- [ ] Deletar usuários via admin panel
- [ ] Validação de email único no create-user
- [ ] Reset de senha via email
- [ ] Logs de auditoria (quem fez o quê)

### **Prioridade Média**
- [ ] Thumbnails automáticos para vídeos
- [ ] Compressão de imagens no upload
- [ ] Notificações push
- [ ] PWA offline support

### **Prioridade Baixa**
- [ ] Modo picture-in-picture
- [ ] Compartilhamento de vídeos
- [ ] Comentários em vídeos

---

## 🔧 Comandos Úteis

```bash
# Desenvolvimento local
npm run dev                 # http://localhost:3000

# Build e deploy
npm run build
python aws-setup/upload-frontend.py
python aws-setup/invalidate-cache.py

# Verificar tipos
npm run type-check

# Lint
npm run lint

# Testar Lambda localmente
cd aws-setup/lambda-functions/auth-handler
python lambda_function.py
```

---

## 📝 Notas Importantes

1. **Cache CloudFront**: Sempre invalidar após deploy (`invalidate-cache.py`)
2. **Hard Refresh**: Ctrl+Shift+R para limpar cache do browser
3. **2FA Session**: Expira em 30 minutos (1800000ms)
4. **Avatar Size**: Recomendado 512x512px, max 5MB
5. **TOTP Secret**: Gerado automaticamente no create-user
6. **QR Codes**: Armazenados em `qrcodes/qr_${userId}.png`
7. **Role-Based**: Admin vê tudo, user vê apenas próprio conteúdo
8. **S3 Folders**: `avatars/` e `qrcodes/` são públicos, resto privado

---

## 🎯 Como Usar Este Prompt

**Cole este prompt no início do próximo chat:**

```
Estou continuando o desenvolvimento do Mediaflow v4.3, um sistema de streaming profissional com AWS.

Leia o contexto completo em @CONTEXT_PROMPT.md para entender:
- Arquitetura AWS atual (S3, Lambda, DynamoDB, CloudFront)
- Sistema multi-usuário com avatares
- Fluxo de autenticação (JWT + 2FA)
- Problemas já resolvidos
- Próximos passos planejados

O sistema está 100% funcional em produção. Preciso continuar implementando as features da v4.4.
```

---

## 📚 Documentação Adicional

- **README.md**: Overview geral do projeto
- **DOCUMENTACAO_COMPLETA.md**: Arquitetura detalhada e troubleshooting
- **aws-setup/README.md**: Setup AWS e deploy

---

**✅ Sistema 100% funcional com multi-usuário e avatares!**  
**🚀 Pronto para v4.4!**
