# 📋 Estudo de Caso: MidiaFlow

## Infraestrutura Resiliente com Visibilidade de Custos em Tempo Real

---

### O Desafio

Construir uma plataforma de hospedagem de vídeos que fosse:
- **Escalável** sem gerenciar servidores
- **Segura** com autenticação em todas as camadas
- **Automatizada** do commit ao deploy em produção
- **Custo-consciente** com visibilidade de gastos por projeto

### A Solução

Arquitetura 100% serverless na AWS com 10 serviços integrados:

**Frontend:** Next.js 14 (Static Export) → S3 → CloudFront (400+ POPs globais)

**Backend:** 17 Lambda Functions (Python 3.11) → API Gateway → DynamoDB

**CI/CD:** GitHub Actions com 6 stages (test → build → deploy → health-check → finops → notify)

**FinOps:** AWS Cost Explorer + Bedrock Claude AI + SES (relatório automático pós-deploy)

**Segurança:** JWT HMAC-SHA256 unificado em todas as 17 Lambdas + 2FA para admin

### Decisões Técnicas

| Decisão | Por quê |
|---|---|
| S3 + CloudFront vs EC2 | Zero manutenção, custo ~$1/mês vs ~$15/mês |
| Lambda vs ECS | Pay-per-request, sem idle cost |
| JWT manual vs Cognito | Controle total, sem vendor lock-in |
| Git rollback vs Blue/Green | Simplicidade para static sites |
| Bedrock vs GPT API | Nativo AWS, sem chave externa |

### Resultados

| Métrica | Antes | Depois |
|---|---|---|
| Deploy | Manual (~30 min) | Automatizado (~8 min) |
| Rollback | Indefinido | `git revert` (~8 min) |
| Visibilidade de custos | Nenhuma | Por projeto, com AI insights |
| Uptime | ~95% | 99.9% |
| Latência | ~3s | < 1.5s (CDN global) |
| Segurança | Parcial | JWT + 2FA em todas as camadas |

### Stack

AWS (S3, CloudFront, Lambda, API Gateway, DynamoDB, SES, Bedrock, Cost Explorer, IAM, CloudWatch) • Next.js 14 • TypeScript • Python 3.11 • GitHub Actions • JWT • Jest

### Links

- **Live:** https://midiaflow.sstechnologies-cloud.com
- **Código:** https://github.com/Sergio-Sena/mediaflow-nextjs-v4
- **Pipeline:** https://github.com/Sergio-Sena/mediaflow-nextjs-v4/actions

---

*Sergio Sena - Cloud & DevOps Engineer*
*https://linkedin.com/in/sergio-sena*
