# 🎬 MidiaFlow - Plataforma Profissional de Hospedagem de Vídeos

[![Status](https://img.shields.io/badge/Status-✅%20Online-brightgreen)](https://midiaflow.sstechnologies-cloud.com)
[![Version](https://img.shields.io/badge/Version-4.9.1-blue)]()
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![AWS](https://img.shields.io/badge/AWS-Serverless-orange)](https://aws.amazon.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF)](https://github.com/Sergio-Sena/mediaflow-nextjs-v4/actions)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Hospede, converta e distribua seus vídeos com CDN global. Simples, rápido e seguro.

**[🚀 Ver Demo](https://midiaflow.sstechnologies-cloud.com)** | **[📖 Documentação](docs/)** | **[🐛 Reportar Bug](issues)**

---

## ✨ Features

### 💰 **FinOps & AI Insights** (v4.9.1) - NOVO
- Relatório de custos AWS por projeto (filtrado por tags)
- AI Insights via AWS Bedrock (Claude 3 Haiku)
- Email automático via SES após cada deploy
- Tags de custo em todos os recursos AWS

### 🚀 **CI/CD Pipeline** (v4.9.1) - NOVO
- GitHub Actions: test → build → deploy → health-check → finops
- Deploy automático de frontend (S3 + CloudFront) e 17 Lambdas
- Rollback via `git revert`
- Health check automático pós-deploy

### 🧪 **Qualidade & Confiabilidade** (v4.9.0)
- Testes unitários automatizados (Jest + Testing Library)
- Error Boundaries para captura de erros
- Loading Skeletons para melhor UX
- Rate Limiting para proteção contra abuso

### 🎥 **Player de Vídeo Premium**
- Player moderno com controles avançados
- Barra de volume expansível horizontal com indicador visual
- Barra de progresso em 3 camadas (fundo, buffer, reprodução)
- Controles responsivos (mobile, tablet, desktop)
- Atalhos de teclado (Space, K, F, M, setas)
- Gestos touch para mobile
- Fullscreen com double-click
- Velocidade de reprodução ajustável
- WCAG AA compliant

### 📤 **Upload Inteligente**
- Upload multipart para arquivos grandes (até 5GB)
- Barra de progresso em tempo real
- Suporte a múltiplos formatos (MP4, AVI, MOV, MKV, WebM)
- Organização por pastas

### 🖼️ **Visualizador de Imagens**
- Galeria com navegação por setas e swipe
- Zoom, rotação e download
- Presigned URLs com autenticação JWT

### 🔐 **Autenticação & Segurança**
- JWT com expiração (24h)
- 2FA obrigatório para admin
- Controle de acesso por usuário
- Presigned URLs com TTL
- JWT_SECRET unificado em todas as Lambdas

### 👤 **Avatar Upload**
- Módulo autossuficiente (extrai userId do JWT)
- Auto-delete de avatares antigos
- Persistência via DynamoDB

### 📊 **Analytics & Gestão**
- Dashboard administrativo completo
- Gestão de usuários (admin/user roles)
- Listagem e busca de vídeos
- Estatísticas de uso

---

## 🛠️ Tech Stack

### **Frontend**
- **Next.js 14** - Framework React com SSR/SSG
- **TypeScript** - Type safety
- **TailwindCSS** - Utility-first CSS
- **Lucide Icons** - Ícones modernos

### **Backend**
- **Python 3.11** - 17 Lambda functions
- **AWS SDK** - Integração AWS
- **JWT (HMAC-SHA256)** - Autenticação

### **AWS Services**
- **S3** - Armazenamento (mediaflow-uploads-969430605054)
- **CloudFront** - CDN (E1A2CZM0WKF6LX)
- **Lambda** - 17 funções serverless
- **API Gateway** - REST API (gdb962d234)
- **DynamoDB** - Banco de dados (mediaflow-users)
- **SES** - Email (relatórios FinOps)
- **Bedrock** - AI Insights (Claude 3 Haiku)
- **Cost Explorer** - Monitoramento de custos

### **CI/CD**
- **GitHub Actions** - Pipeline automatizado
- **Git tags** - Versionamento e rollback

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
AWS_REGION=us-east-1
JWT_SECRET=your-secret-key
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### **4. Execute em desenvolvimento**
```bash
npm run dev
```

### **5. Rodar testes**
```bash
npm test
npm run test:coverage
```

---

## 📦 Deploy

### **Automático (recomendado)**
Push para `main` dispara o pipeline:
```bash
git push origin main
```

### **Manual**
```bash
npm run build
aws s3 sync .next/static s3://mediaflow-frontend-969430605054/_next/static --delete
aws s3 sync out s3://mediaflow-frontend-969430605054 --delete --exclude "_next/*"
aws cloudfront create-invalidation --distribution-id E1A2CZM0WKF6LX --paths "/*"
```

### **Rollback**
```bash
git revert HEAD
git push origin main
```

Ou para uma versão específica:
```bash
git revert HEAD~3..HEAD
git push origin main
```

---

## 📁 Estrutura do Projeto

```
midiaflow/
├── .github/workflows/        # CI/CD Pipeline
│   └── deploy-production.yml
├── app/                      # Next.js App Router
│   ├── api/                  # API Routes (proxies)
│   ├── (auth)/               # Login, Register
│   ├── dashboard/            # Dashboard principal
│   ├── admin/                # Painel admin
│   └── users/                # Gestão de usuários
├── components/
│   ├── modules/              # Componentes principais
│   │   ├── VideoPlayer.tsx   # Player premium
│   │   ├── ImageViewer.tsx   # Visualizador de imagens
│   │   ├── FileList.tsx      # Lista de arquivos
│   │   └── DirectUpload.tsx  # Upload multipart
│   ├── AvatarUpload.tsx      # Avatar (autossuficiente)
│   └── ui/                   # Componentes UI
├── lib/
│   ├── aws-client.ts         # Cliente AWS
│   ├── aws-config.ts         # Configuração endpoints
│   └── auth-utils.ts         # Utilitários JWT
├── aws-setup/
│   └── lambda-functions/     # 17 Funções Lambda
├── scripts/
│   └── finops/               # Relatório de custos + AI
│       └── cost-report.py
├── docs/                     # Documentação
└── types/                    # TypeScript types
```

---

## 🔒 Segurança

- ✅ JWT com expiração (24h)
- ✅ 2FA obrigatório para admin
- ✅ Presigned URLs com TTL
- ✅ CORS configurado
- ✅ JWT_SECRET via variáveis de ambiente
- ✅ Rate limiting
- ✅ HTTPS em produção

**Nunca commite:** `.env.local`, credenciais AWS, JWT secrets

---

## 💰 FinOps

Relatório automático após cada deploy:
- Custos filtrados por tag `Project=MidiaFlow`
- Comparação com mês anterior
- 3 insights de otimização via AI (Bedrock Claude)
- Email via SES

---

## 📊 Performance

- **Lighthouse Score**: 95+
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **CDN**: 400+ POPs globais
- **Uptime**: 99.9%
- **WCAG**: AA Compliant

---

## 🗺️ Roadmap

### ✅ v4.9.0 - Qualidade & Confiabilidade - COMPLETO
- ✅ Testes unitários (Jest + Testing Library)
- ✅ Error Boundaries
- ✅ Loading Skeletons
- ✅ Rate Limiting

### ✅ v4.9.1 - CI/CD & FinOps - COMPLETO
- ✅ Pipeline CI/CD (GitHub Actions)
- ✅ FinOps + AI Insights (Bedrock + SES)
- ✅ JWT unificado em todas as Lambdas
- ✅ AvatarUpload refatorado (autossuficiente)
- ✅ ImageViewer com autenticação JWT
- ✅ Auto-delete avatares antigos
- ✅ Limpeza S3 (undefined/, anonymous/)
- ✅ Tags de custo em todos os recursos

### 🔜 v4.10 - Área Pública
- [ ] Área pública para conteúdo compartilhável
- [ ] Conversão automática para múltiplas resoluções
- [ ] Legendas e closed captions
- [ ] Analytics avançado

### 🔮 Futuro
- [ ] Live streaming (MediaStore + MediaLive)
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

<div align="center">

**⭐ Se este projeto foi útil, deixe uma estrela!**

[🚀 Ver Demo](https://midiaflow.sstechnologies-cloud.com) • [📖 Docs](docs/) • [🐛 Issues](issues)

</div>
