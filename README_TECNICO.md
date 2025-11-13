# 🔧 README Técnico - Mídiaflow

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
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/         # Dashboard principal
│   ├── pricing/           # Página de preços
│   ├── sla/               # Garantias e SLA
│   ├── termos/            # Termos de Serviço
│   └── privacidade/       # Política de Privacidade
├── components/            # Componentes React
├── lib/                   # Utilitários
├── public/                # Assets estáticos
├── styles/                # CSS global
├── content/               # Conteúdo markdown
│   ├── docs/             # Documentação
│   ├── sla.md
│   ├── termos.md
│   └── privacidade.md
├── scripts/               # Scripts de deploy
└── memoria/               # Documentação do projeto
```

---

## 🔐 Autenticação

### JWT Token

**Geração:**
```javascript
const token = jwt.sign(
  { user_id, email, role },
  process.env.JWT_SECRET,
  { expiresIn: '7d' }
)
```

**Validação:**
```javascript
const decoded = jwt.verify(token, process.env.JWT_SECRET)
```

### 2FA (TOTP)

**Biblioteca:** `speakeasy`

**Geração do secret:**
```javascript
const secret = speakeasy.generateSecret({
  name: `Mídiaflow (${email})`
})
```

**Validação:**
```javascript
const verified = speakeasy.totp.verify({
  secret: user.totp_secret,
  encoding: 'base32',
  token: userToken
})
```

---

## 📤 Upload de Vídeos

### Fluxo

1. **Frontend** solicita presigned URL
2. **Lambda** gera URL do S3
3. **Frontend** faz upload direto para S3
4. **S3** notifica Lambda via evento
5. **Lambda** inicia conversão no MediaConvert
6. **MediaConvert** processa vídeo
7. **Lambda** atualiza DynamoDB

### Presigned URL

**Lambda: get-upload-url**
```javascript
const command = new PutObjectCommand({
  Bucket: 'midiaflow-videos-969430605054',
  Key: `${s3_prefix}${fileName}`,
  ContentType: contentType
})

const url = await getSignedUrl(s3Client, command, {
  expiresIn: 300 // 5 minutos
})
```

### Conversão

**MediaConvert Job:**
```javascript
{
  Role: 'arn:aws:iam::969430605054:role/MediaConvertRole',
  Settings: {
    OutputGroups: [{
      OutputGroupSettings: {
        Type: 'FILE_GROUP_SETTINGS',
        FileGroupSettings: {
          Destination: `s3://bucket/${s3_prefix}converted/`
        }
      },
      Outputs: [
        { VideoDescription: { Height: 1080 } }, // 1080p
        { VideoDescription: { Height: 720 } },  // 720p
        { VideoDescription: { Height: 480 } }   // 480p
      ]
    }]
  }
}
```

---

## 🗄️ Banco de Dados

### DynamoDB

**Tabela: users**
```
Partition Key: user_id (String)
Attributes:
  - email (String)
  - password_hash (String)
  - name (String)
  - role (String)
  - s3_prefix (String)
  - totp_secret (String)
  - avatar_url (String)
  - status (String) // 'trial', 'active', 'inactive'
  - trial_end_date (Number)
  - storage_used (Number)
  - bandwidth_used (Number)
  - created_at (Number)
```

**Tabela: files**
```
Partition Key: user_id (String)
Sort Key: file_id (String)
Attributes:
  - file_name (String)
  - file_size (Number)
  - file_type (String)
  - s3_key (String)
  - folder (String)
  - converted (Boolean)
  - conversion_status (String)
  - views (Number)
  - created_at (Number)
```

---

## 🔌 API Endpoints

### Autenticação

**POST /prod/users/create**
```json
{
  "user_id": "joao_silva",
  "email": "joao@email.com",
  "password": "senha123",
  "name": "João Silva",
  "s3_prefix": "users/joao_silva/"
}
```

**POST /prod/users/login**
```json
{
  "email": "joao@email.com",
  "password": "senha123",
  "totp_token": "123456"
}
```

### Upload

**POST /prod/get-upload-url**
```json
{
  "fileName": "video.mp4",
  "contentType": "video/mp4",
  "folder": "projetos/2025"
}
```

**Response:**
```json
{
  "uploadUrl": "https://s3.amazonaws.com/...",
  "fileKey": "users/joao_silva/projetos/2025/video.mp4"
}
```

### Listagem

**GET /prod/list-files?folder=projetos/2025**

**Response:**
```json
{
  "files": [
    {
      "file_id": "abc123",
      "file_name": "video.mp4",
      "file_size": 1048576,
      "converted": true,
      "views": 42,
      "created_at": 1706659200000
    }
  ]
}
```

---

## 🚀 Deploy

### Frontend (S3 + CloudFront)

```bash
# Build
npm run build

# Deploy
cd out
aws s3 sync . s3://midiaflow-frontend-969430605054/ \
  --delete \
  --region us-east-1

# Invalidar cache
aws cloudfront create-invalidation \
  --distribution-id E2HZKZ9ZJK18IU \
  --paths "/*"
```

### Backend (Lambda)

```bash
# Cada Lambda tem seu próprio diretório
cd lambda/create-user

# Instalar dependências
npm install

# Zipar
zip -r function.zip .

# Deploy
aws lambda update-function-code \
  --function-name create-user \
  --zip-file fileb://function.zip \
  --region us-east-1
```

---

## 🔧 Variáveis de Ambiente

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod
NEXT_PUBLIC_CDN_URL=https://d3abc123.cloudfront.net
```

### Backend (Lambda Environment Variables)

```bash
JWT_SECRET=your-secret-key
DYNAMODB_TABLE_USERS=users
DYNAMODB_TABLE_FILES=files
S3_BUCKET=midiaflow-videos-969430605054
MEDIACONVERT_ENDPOINT=https://abc123.mediaconvert.us-east-1.amazonaws.com
MEDIACONVERT_ROLE=arn:aws:iam::969430605054:role/MediaConvertRole
```

---

## 📊 Monitoramento

### CloudWatch Alarms

**Configurados:**
- CloudFront 5xx errors (> 1%)
- CloudFront 4xx errors (> 5%)
- Lambda errors (> 5 em 5min)
- Lambda throttles (> 10 em 5min)
- S3 5xx errors (> 10 em 5min)

**Script de deploy:**
```bash
./scripts/deploy-sla-monitoring.sh
```

### Logs

**CloudWatch Logs:**
- `/aws/lambda/create-user`
- `/aws/lambda/list-files`
- `/aws/lambda/get-upload-url`
- `/aws/lambda/convert-video`

**Retenção:** 90 dias

---

## 🧪 Testes

### Local

```bash
# Instalar dependências
npm install

# Rodar dev server
npm run dev

# Build de produção
npm run build

# Testar build
npm start
```

### Testes de Carga

**Recomendado:** Artillery, k6

```bash
# Exemplo com k6
k6 run --vus 100 --duration 30s load-test.js
```

---

## 🔒 Segurança

### Boas Práticas Implementadas

- ✅ HTTPS em tudo (TLS 1.3)
- ✅ Senhas com hash SHA-256
- ✅ JWT com expiração (7 dias)
- ✅ 2FA obrigatório
- ✅ Presigned URLs com expiração (5 min)
- ✅ CORS configurado
- ✅ Rate limiting (API Gateway)
- ✅ Validação de inputs
- ✅ Sanitização de dados

### Conformidade

- ✅ LGPD (Lei Geral de Proteção de Dados)
- ✅ Termos de Serviço
- ✅ Política de Privacidade
- ✅ SLA por plano

---

## 📚 Recursos Adicionais

### Documentação AWS

- [S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [MediaConvert Documentation](https://docs.aws.amazon.com/mediaconvert/)
- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)

### Bibliotecas Principais

- [Next.js](https://nextjs.org/docs)
- [AWS SDK v3](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/)
- [jsonwebtoken](https://github.com/auth0/node-jsonwebtoken)
- [speakeasy](https://github.com/speakeasyjs/speakeasy)

---

## 🤝 Contribuindo

### Setup Local

1. Clone o repositório
2. Instale dependências: `npm install`
3. Configure `.env.local`
4. Rode dev server: `npm run dev`
5. Acesse: `http://localhost:3000`

### Padrões de Código

- TypeScript strict mode
- ESLint + Prettier
- Conventional Commits
- Código mínimo necessário

---

## 📞 Suporte Técnico

**Para desenvolvedores:**
- 📧 Email: dev@midiaflow.com
- 📚 Docs: midiaflow.com/docs
- 🐛 Issues: GitHub (privado)

---

**Versão:** 4.8.2  
**Última atualização:** 30 de janeiro de 2025
