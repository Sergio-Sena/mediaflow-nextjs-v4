# 🎬 MidiaFlow - Plataforma Profissional de Hospedagem de Vídeos

[![Status](https://img.shields.io/badge/Status-✅%20Online-brightgreen)](https://midiaflow.sstechnologies-cloud.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![AWS](https://img.shields.io/badge/AWS-Serverless-orange)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Hospede, converta e distribua seus vídeos com CDN global. Simples, rápido e seguro.

**[🚀 Ver Demo](https://midiaflow.sstechnologies-cloud.com)** | **[📖 Documentação](docs/)** | **[🐛 Reportar Bug](issues)**

---

## ✨ Features

### 🎥 **Player de Vídeo Premium** (v4.9.0)
- Player moderno com controles avançados
- Barra de volume expansível horizontal com indicador visual
- Barra de progresso em 3 camadas (fundo, buffer, reprodução)
- Controles responsivos (mobile, tablet, desktop)
- Atalhos de teclado (Space, K, F, M, setas)
- Gestos touch para mobile (swipe vertical para volume, horizontal para seek)
- Fullscreen com double-click
- Velocidade de reprodução ajustável
- WCAG AA compliant (acessibilidade)
- Cross-browser support (Chrome, Firefox, Safari, Edge)

### 📤 **Upload Inteligente**
- Upload multipart para arquivos grandes (até 5GB)
- Barra de progresso em tempo real
- Suporte a múltiplos formatos (MP4, AVI, MOV, MKV, WebM)
- Thumbnails geradas automaticamente
- Organização por pastas

### 🔐 **Autenticação & Segurança**
- JWT + 2FA (Two-Factor Authentication)
- Controle de acesso por usuário
- Vídeos privados por padrão
- Presigned URLs com expiração
- CORS configurado

### 📊 **Analytics & Gestão**
- Dashboard administrativo completo
- Gestão de usuários (admin/user roles)
- Listagem e busca de vídeos
- Estatísticas de uso
- Logs de atividades

### ☁️ **Infraestrutura AWS**
- **S3**: Armazenamento escalável
- **CloudFront**: CDN global (400+ POPs)
- **Lambda**: Processamento serverless
- **API Gateway**: REST API
- **DynamoDB**: Banco de dados NoSQL

---

## 🛠️ Tech Stack

### **Frontend**
- **Next.js 14** - Framework React com SSR/SSG
- **TypeScript** - Type safety
- **TailwindCSS** - Utility-first CSS
- **Lucide Icons** - Ícones modernos

### **Backend**
- **Node.js 18+** - Runtime
- **Python 3.11** - Lambda functions
- **AWS SDK** - Integração AWS
- **JWT** - Autenticação

### **AWS Services**
- **S3** - Uploads & Processed buckets
- **CloudFront** - CDN (E1O4R8P5BGZTMW)
- **Lambda** - Upload handler, conversão
- **API Gateway** - REST endpoints
- **DynamoDB** - Usuários, logs

---

## 🚀 Quick Start

### **Pré-requisitos**
- Node.js 18+
- AWS Account
- Git

### **1. Clone o repositório**
```bash
git clone https://github.com/Sergio-Sena/mediaflow-nextjs-v4.git
cd mediaflow-nextjs-v4
```

### **2. Instale as dependências**
```bash
npm install
```

### **3. Configure as variáveis de ambiente**
```bash
cp .env.example .env.local
```

Edite `.env.local`:
```env
# AWS
NEXT_PUBLIC_AWS_REGION=us-east-1
NEXT_PUBLIC_S3_UPLOADS_BUCKET=mediaflow-uploads-969430605054
NEXT_PUBLIC_S3_PROCESSED_BUCKET=mediaflow-processed-969430605054
NEXT_PUBLIC_CLOUDFRONT_DOMAIN=d2komwe8ylb0dt.cloudfront.net

# API
NEXT_PUBLIC_API_URL=https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod

# Auth
JWT_SECRET=your-super-secret-key-here
```

### **4. Execute em desenvolvimento**
```bash
npm run dev
```

Acesse: http://localhost:3000

---

## 📦 Deploy

### **Build de Produção**
```bash
npm run build
```

### **Deploy na AWS**
```bash
# Sync static files
aws s3 sync .next/static s3://mediaflow-frontend-969430605054/_next/static --delete

# Sync HTML
aws s3 sync out s3://mediaflow-frontend-969430605054 --delete --exclude "_next/*"

# Invalidate CloudFront
aws cloudfront create-invalidation --distribution-id E1O4R8P5BGZTMW --paths "/*"
```

---

## 📁 Estrutura do Projeto

```
mediaflow-nextjs-v4/
├── app/                      # Next.js App Router
│   ├── api/                  # API Routes (proxies)
│   ├── (auth)/              # Páginas de autenticação
│   ├── dashboard/           # Dashboard principal
│   └── globals.css          # Estilos globais
├── components/
│   ├── modules/             # Componentes principais
│   │   ├── VideoPlayer.tsx  # Player premium
│   │   ├── FileList.tsx     # Lista de vídeos
│   │   └── UploadForm.tsx   # Upload multipart
│   └── ui/                  # Componentes UI
├── lib/
│   ├── aws-client.ts        # Cliente AWS
│   └── auth.ts              # Autenticação JWT
├── aws-setup/               # Infraestrutura AWS
│   └── lambda-functions/    # Funções Lambda
├── public/                  # Assets estáticos
└── types/                   # TypeScript types
```

---

## 🎯 Funcionalidades Principais

### **Upload de Vídeos**
```typescript
// Upload multipart com progresso
const uploadVideo = async (file: File) => {
  const presignedUrl = await getPresignedUrl(file.name);
  await uploadToS3(presignedUrl, file, onProgress);
};
```

### **Player de Vídeo**
```typescript
// Player com controles avançados
<VideoPlayer
  src={videoKey}
  title={videoName}
  playlist={videos}
  onVideoChange={handleVideoChange}
/>
```

### **Autenticação**
```typescript
// Login com JWT + 2FA
const login = async (email: string, password: string, code?: string) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password, code })
  });
  return response.json();
};
```

---

## 🔒 Segurança

### **Boas Práticas Implementadas**
- ✅ JWT com expiração
- ✅ 2FA obrigatório para admin
- ✅ Presigned URLs com TTL
- ✅ CORS configurado
- ✅ Validação de input
- ✅ Rate limiting (recomendado)
- ✅ HTTPS em produção

### **Variáveis Sensíveis**
Nunca commite:
- `.env.local`
- Credenciais AWS
- JWT secrets
- API keys

---

## 📊 Performance

- **Lighthouse Score**: 95+
- **Lighthouse Accessibility**: 90+
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **CDN**: 400+ POPs globais
- **Uptime**: 99.9%
- **WCAG**: AA Compliant

---

## 🐛 Troubleshooting

### **Vídeo não carrega**
- Verificar presigned URL válida
- Confirmar bucket S3 acessível
- Checar CORS configurado

### **Upload falha**
- Verificar tamanho do arquivo (< 5GB)
- Confirmar formato suportado
- Checar credenciais AWS

### **Erro 403 ao deletar**
- Usar endpoint `/files/bulk-delete`
- Verificar permissões IAM
- Confirmar token JWT válido

---

## 🗺️ Roadmap

### ⚠️ Correções Prioritárias (v4.8.6)
- [ ] Corrigir upload de arquivos pequenos
- [ ] Corrigir foto de perfil que não aparece
- [ ] Corrigir delete de arquivos

### Área Pública (v4.10)
- [ ] Conversão automática para múltiplas resoluções
- [ ] Legendas e closed captions
- [ ] Live streaming
- [ ] Analytics avançado
- [ ] API pública
- [ ] Mobile app (React Native)

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Sergio Sena**
- GitHub: [@Sergio-Sena](https://github.com/Sergio-Sena)
- LinkedIn: [Sergio Sena](https://linkedin.com/in/sergio-sena)
- Portfolio: [dev-cloud.sstechnologies-cloud.com](https://dev-cloud.sstechnologies-cloud.com)

---

## 🙏 Agradecimentos

- AWS pela infraestrutura robusta
- Next.js team pelo framework incrível
- Comunidade open source

---

<div align="center">

**⭐ Se este projeto foi útil, deixe uma estrela!**

[🚀 Ver Demo](https://midiaflow.sstechnologies-cloud.com) • [📖 Docs](docs/) • [🐛 Issues](issues)

</div>
