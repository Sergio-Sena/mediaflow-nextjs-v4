# 🔧 README Desenvolvimento - Mídiaflow

**Documentação técnica para desenvolvedores**

---

## 🏗️ Arquitetura

### Stack Tecnológico

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React 18

**Backend:**
- AWS Lambda (Node.js 18)
- API Gateway (REST)
- DynamoDB (NoSQL)
- S3 (Storage)

**CDN & Media:**
- CloudFront (CDN Global)
- MediaConvert (Transcodificação)
- Presigned URLs (Upload direto)

**Autenticação:**
- JWT (JSON Web Tokens)
- 2FA (TOTP)
- SHA-256 (Hash de senhas)

---

## 📁 Estrutura do Projeto

```
drive-online-clean-NextJs/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Rotas de autenticação
│   ├── dashboard/         # Dashboard principal
│   ├── pricing/           # Página de preços
│   └── admin/             # Painel administrativo
├── components/            # Componentes React
├── lib/                   # Utilitários
├── aws-setup/             # Configurações AWS
│   └── lambda-functions/  # Funções Lambda
├── scripts/               # Scripts de deploy
└── docs/                  # Documentação
```

---

## 🔐 Autenticação

### JWT Token
```javascript
const token = jwt.sign(
  { user_id, email, role },
  process.env.JWT_SECRET,
  { expiresIn: '24h' }
)
```

### 2FA (TOTP)
```javascript
const secret = pyotp.random_base32()
const totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
  name=user_id,
  issuer_name='Mídiaflow'
)
```

---

## 📤 Upload de Arquivos

### Fluxo
1. Frontend solicita presigned URL
2. Lambda gera URL do S3
3. Upload direto para S3
4. Conversão automática (se vídeo)
5. Notificação de conclusão

### Estrutura S3
```
users/
├── {user_id}/
│   ├── videos/
│   ├── images/
│   ├── documents/
│   └── converted/
```

---

## 🗄️ Banco de Dados (DynamoDB)

### Tabela: mediaflow-users
```
Partition Key: user_id (String)
Attributes:
  - email, name, password
  - role, status, plan
  - s3_prefix, avatar_url
  - totp_secret
  - limits, usage
  - created_at, trial_end
```

---

## 🔌 API Endpoints

### Autenticação
- `POST /users/create` - Criar usuário
- `POST /users/login` - Login
- `POST /users/approve` - Aprovar usuário (admin)

### Arquivos
- `GET /files` - Listar arquivos
- `POST /upload` - Upload de arquivo
- `DELETE /files/{id}` - Deletar arquivo

### Administração
- `GET /users` - Listar usuários (admin)
- `PUT /users/{id}` - Atualizar usuário (admin)

---

## 🚀 Deploy

### Frontend
```bash
npm run build
aws s3 sync out/ s3://mediaflow-frontend-969430605054/
aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"
```

### Backend
```bash
cd aws-setup/lambda-functions/{function-name}
zip -r function.zip .
aws lambda update-function-code --function-name {function-name} --zip-file fileb://function.zip
```

---

## 📊 Monitoramento

### CloudWatch Alarms
- Lambda errors (> 5%)
- API Gateway 5xx (> 1%)
- S3 errors (> 10 em 5min)

### Logs
- Estruturados em JSON
- Correlation IDs
- Retenção: 90 dias

---

## 🔒 Segurança

### Implementado
- HTTPS/TLS 1.3
- JWT com expiração
- 2FA opcional
- CORS configurado
- Input validation
- Rate limiting

### Conformidade
- LGPD
- Termos de Serviço
- Política de Privacidade

---

## 🧪 Desenvolvimento Local

```bash
# Setup
git clone [repo]
npm install
cp .env.example .env.local

# Desenvolvimento
npm run dev

# Build
npm run build
npm start
```

---

## 📚 Recursos

- [AWS Documentation](https://docs.aws.amazon.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Projeto no GitHub](https://github.com/...)

---

**Versão:** 4.9.0  
**Última atualização:** 31 de janeiro de 2025