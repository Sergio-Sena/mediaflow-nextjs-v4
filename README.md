# 🎬 MidiaFlow - Video Hosting Platform

[![Status](https://img.shields.io/badge/Status-✅%20Production-brightgreen)](https://midiaflow.sstechnologies-cloud.com)
[![Version](https://img.shields.io/badge/Version-4.9.1-blue)]()
[![Pipeline](https://img.shields.io/github/actions/workflow/status/Sergio-Sena/mediaflow-nextjs-v4/deploy-production.yml?label=CI%2FCD)](https://github.com/Sergio-Sena/mediaflow-nextjs-v4/actions)
[![AWS](https://img.shields.io/badge/AWS-Serverless-FF9900?logo=amazonaws)](https://aws.amazon.com/)
[![IaC](https://img.shields.io/badge/Infra-17%20Lambdas-purple)]()
[![FinOps](https://img.shields.io/badge/FinOps-AI%20Insights-00FFFF)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Plataforma serverless de hospedagem de vídeos com CDN global, CI/CD automatizado e camada FinOps com AI insights.

**[🚀 Live Demo](https://midiaflow.sstechnologies-cloud.com)** | **[📐 Arquitetura](#-arquitetura)** | **[📊 Métricas](#-observabilidade--métricas)** | **[💰 FinOps](#-finops--ai-insights)**

---

## 🎯 Problema → Solução → Resultado

| | Descrição |
|---|---|
| **Problema** | Como automatizar deploys de uma plataforma de vídeo garantindo escalabilidade, segurança e controle de gastos? |
| **Solução** | Arquitetura 100% serverless na AWS com pipeline CI/CD, autenticação JWT unificada e camada FinOps com AI para otimização de custos |
| **Resultado** | Deploy automatizado em ~8 min, 99.9% uptime, latência < 1.5s (CDN global), visibilidade de custos em tempo real por projeto |

---

## 📐 Arquitetura

```
                                    ┌─────────────────────────────────────────┐
                                    │           GitHub Actions CI/CD          │
                                    │  test → build → deploy → health → finops│
                                    └──────────┬──────────────┬───────────────┘
                                               │              │
                                    ┌──────────▼──────┐ ┌─────▼──────────┐
                                    │   S3 (Frontend)  │ │  17 Lambdas    │
                                    │   Static Export  │ │  Python 3.11   │
                                    └──────────┬──────┘ └─────┬──────────┘
                                               │              │
┌──────────┐    ┌──────────────┐    ┌──────────▼──────┐ ┌─────▼──────────┐
│  Client  │───▶│  CloudFront  │───▶│   S3 Website    │ │  API Gateway   │
│ (Browser)│    │  CDN Global  │    │   Hosting       │ │  REST API      │
└──────────┘    │  400+ POPs   │    └─────────────────┘ └─────┬──────────┘
                └──────────────┘                              │
                                                    ┌─────────▼─────────┐
                                              ┌─────┤   Lambda Functions ├─────┐
                                              │     └───────────────────┘     │
                                    ┌─────────▼──┐  ┌──────▼──────┐  ┌───────▼────┐
                                    │  DynamoDB   │  │  S3 Uploads │  │  Bedrock   │
                                    │  Users/Auth │  │  5GB/file   │  │  Claude AI │
                                    └─────────────┘  └─────────────┘  └────────────┘
                                                                      ┌────────────┐
                                                                      │    SES      │
                                                                      │FinOps Email│
                                                                      └────────────┘
```

### Decisões de Arquitetura

| Decisão | Alternativa | Por que escolhi |
|---|---|---|
| **S3 + CloudFront** (static hosting) | EC2/ECS | Zero manutenção, escala infinita, custo ~$1/mês |
| **Lambda** (17 funções) | ECS Fargate | Pay-per-request, sem idle cost, escala automática |
| **DynamoDB** (on-demand) | RDS/Aurora | Serverless, sem provisioning, latência < 10ms |
| **JWT manual** (HMAC-SHA256) | Cognito | Controle total, sem vendor lock-in, custo zero |
| **Git rollback** | Blue/Green | Simplicidade para static sites, sem custo extra |
| **Bedrock Claude** (FinOps AI) | GPT API | Nativo AWS, pay-per-token, sem chave externa |

---

## 🚀 CI/CD Pipeline

```
┌────────┐    ┌────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────┐    ┌────────┐
│  Test  │───▶│ Build  │───▶│Deploy Frontend│───▶│ Health Check │───▶│ FinOps │───▶│ Notify │
│ Jest   │    │Next.js │    │  S3 + CDN    │    │  HTTP 200?   │    │Cost+AI │    │ Status │
└────────┘    └────────┘    │              │    └──────────────┘    │Bedrock │    └────────┘
                            │Deploy Lambdas│                       │  +SES  │
                            │  17x parallel│                       └────────┘
                            └──────────────┘
```

| Métrica | Valor |
|---|---|
| **Tempo total** | ~8 minutos |
| **Trigger** | Push to `main` |
| **Lambdas deployadas** | 17 (paralelo) |
| **Rollback** | `git revert HEAD && git push` (~8 min) |
| **Health check** | Frontend + API automático |

### Rollback

```bash
# Reverter último deploy
git revert HEAD
git push origin main

# Voltar para versão específica
git checkout v4.9.1
```

---

## 💰 FinOps & AI Insights

Após cada deploy, o pipeline gera automaticamente:

1. **Coleta** custos via AWS Cost Explorer (filtrado por tag `Project=MidiaFlow`)
2. **Analisa** com Bedrock Claude 3 Haiku (3 insights acionáveis)
3. **Envia** relatório HTML por email via SES

### Exemplo de relatório

```
📊 MidiaFlow FinOps - Deploy ec7a1f7b

💰 Custos (30 dias)
┌─────────────────────┬──────────┐
│ Serviço             │ Custo    │
├─────────────────────┼──────────┤
│ S3 Storage          │ $0.12    │
│ CloudFront          │ $0.85    │
│ Lambda              │ $0.03    │
│ DynamoDB            │ $0.25    │
│ API Gateway         │ $0.15    │
├─────────────────────┼──────────┤
│ TOTAL               │ $1.40    │
└─────────────────────┴──────────┘

🤖 AI Insights (Bedrock Claude):
1. CloudFront: restringir geo para South America (-30% custo)
2. Lambda: 3 funções com 256MB executariam mais rápido e barato
3. DynamoDB: padrão de uso sugere provisioned mode (-40%)
```

**Custo do FinOps:** ~$0.005/relatório (Bedrock) + $0.00 (SES)

---

## 📊 Observabilidade & Métricas

| Métrica | Valor | Ferramenta |
|---|---|---|
| **Uptime** | 99.9% | CloudFront |
| **Latência (P50)** | < 50ms | CloudFront CDN |
| **First Contentful Paint** | < 1.5s | Lighthouse |
| **Time to Interactive** | < 3s | Lighthouse |
| **Lighthouse Score** | 95+ | Chrome DevTools |
| **CDN POPs** | 400+ globais | CloudFront |
| **Lambda Cold Start** | < 500ms | CloudWatch |
| **WCAG** | AA Compliant | Accessibility Audit |

### Monitoramento

- **CloudWatch**: Logs de todas as 17 Lambdas
- **Cost Explorer**: Custos por tag `Project=MidiaFlow`
- **GitHub Actions**: Pipeline status e histórico
- **Health Check**: Automático pós-deploy

---

## 🔐 Segurança

| Controle | Implementação |
|---|---|
| **Autenticação** | JWT HMAC-SHA256 (24h expiry) |
| **2FA** | TOTP obrigatório para admin |
| **Autorização** | Role-based (admin/user) |
| **Dados em trânsito** | HTTPS (CloudFront TLS 1.3) |
| **Dados em repouso** | S3 SSE (AES-256) |
| **URLs temporárias** | Presigned URLs com TTL |
| **Secrets** | GitHub Secrets + Lambda env vars |
| **CORS** | Configurado por endpoint |
| **Rate Limiting** | Implementado no frontend |

---

## 🛠️ Tech Stack

### Frontend
| Tecnologia | Versão | Uso |
|---|---|---|
| Next.js | 14 | Framework (Static Export) |
| TypeScript | 5.0 | Type safety |
| TailwindCSS | 4.x | Styling |
| Jest | 30.x | Testes unitários |

### Backend
| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.11 | 17 Lambda functions |
| JWT | HMAC-SHA256 | Autenticação |
| Boto3 | latest | AWS SDK |

### AWS Services (10 serviços)
| Serviço | Recurso | Uso |
|---|---|---|
| S3 | 2 buckets | Storage + Hosting |
| CloudFront | 1 distribuição | CDN global |
| Lambda | 17 funções | Backend serverless |
| API Gateway | 1 REST API | Endpoints |
| DynamoDB | 1 tabela | Users/Auth |
| SES | 1 identidade | Email FinOps |
| Bedrock | Claude 3 Haiku | AI Insights |
| Cost Explorer | Tags | Monitoramento custos |
| IAM | Roles + Policies | Segurança |
| CloudWatch | Logs | Observabilidade |

---

## 📁 Estrutura do Projeto

```
midiaflow/
├── .github/workflows/         # CI/CD Pipeline
│   └── deploy-production.yml  # test → build → deploy → finops
├── app/                       # Next.js App Router
│   ├── (auth)/                # Login, Register, 2FA
│   ├── dashboard/             # Dashboard principal
│   ├── admin/                 # Painel administrativo
│   └── users/                 # Gestão de usuários
├── components/
│   ├── modules/               # Componentes de negócio
│   │   ├── VideoPlayer.tsx    # Player premium (JWT auth)
│   │   ├── ImageViewer.tsx    # Galeria (JWT auth)
│   │   └── DirectUpload.tsx   # Upload multipart (5GB)
│   ├── AvatarUpload.tsx       # Avatar autossuficiente
│   └── ui/                    # Design system
├── lib/
│   ├── auth-utils.ts          # getUserFromToken() - JWT utils
│   ├── aws-client.ts          # Cliente API
│   └── aws-config.ts          # Endpoints config
├── aws-setup/
│   └── lambda-functions/      # 17 Lambdas (Python)
│       ├── auth-handler/      # Login + JWT
│       ├── view-handler/      # Presigned URLs
│       ├── files-handler/     # CRUD arquivos
│       ├── upload-handler/    # Upload presigned
│       ├── avatar-presigned/  # Avatar + auto-delete
│       └── ...                # +12 funções
├── scripts/
│   └── finops/
│       └── cost-report.py     # Cost Explorer + Bedrock + SES
└── docs/
    └── live-streaming-reference.md
```

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/Sergio-Sena/mediaflow-nextjs-v4.git
cd mediaflow-nextjs-v4

# Install
npm install

# Configure
cp .env.example .env.local
# Edit .env.local with your AWS credentials

# Dev
npm run dev

# Test
npm test

# Build
npm run build
```

---

## 🗺️ Roadmap

### ✅ v4.9.0 - Qualidade & Confiabilidade
Testes unitários, Error Boundaries, Loading Skeletons, Rate Limiting

### ✅ v4.9.1 - CI/CD & FinOps (atual)
Pipeline GitHub Actions, FinOps + Bedrock AI, JWT unificado, AvatarUpload refatorado

### 🔜 v4.10 - Área Pública
Conteúdo compartilhável, conversão multi-resolução, legendas, analytics avançado

### 🔮 Futuro
Live streaming (MediaStore + MediaLive), API pública, Mobile app (React Native)

---

## 👨‍💻 Autor

**Sergio Sena** - Cloud & DevOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-Sergio--Sena-181717?logo=github)](https://github.com/Sergio-Sena)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sergio%20Sena-0A66C2?logo=linkedin)](https://linkedin.com/in/sergio-sena)
[![Portfolio](https://img.shields.io/badge/Portfolio-dev--cloud-00FFFF)](https://dev-cloud.sstechnologies-cloud.com)

---

<div align="center">

**⭐ Se este projeto foi útil, deixe uma estrela!**

</div>
