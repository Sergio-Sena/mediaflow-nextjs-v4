# Contexto — MidiaFlow

Leia este arquivo antes de implementar qualquer mudança neste projeto.

---

## Sobre o Projeto

- **Produto:** Plataforma serverless de hospedagem de vídeos com CDN global, CI/CD automatizado e FinOps com AI insights
- **URL produção:** https://midiaflow.sstechnologies-cloud.com
- **Versão atual:** 4.9.1
- **Autor:** Sergio Sena — SS Technologies (senanetworker@gmail.com)

---

## Arquitetura

- **100% serverless AWS** — S3, CloudFront, Lambda, API Gateway, DynamoDB, SES, Bedrock
- **Frontend:** Next.js 14 Static Export → S3 → CloudFront (CDN unificado `E9ZQJ3RPSA04N`)
- **Backend:** 17 Lambda Functions (Python 3.11)
- **Auth:** JWT HMAC-SHA256 via `JWT_SECRET` (env var — nunca fallback)
- **CDN path:** `sstech-cdn-unified/midiaflow/`
- **DynamoDB:** `mediaflow-users` (auth) + `mediaflow-public-content` (social)
- **Tag de todos os recursos:** `Project=MidiaFlow`

### Lambdas principais:
- `auth-handler` — login + JWT
- `view-handler` — presigned URLs
- `files-handler` — CRUD arquivos
- `upload-handler` — upload presigned (até 5GB)
- `avatar-presigned` — avatar + auto-delete
- +12 funções em `aws-setup/lambda-functions/`

---

## Regras Críticas de Segurança

- NUNCA usar fallback para `JWT_SECRET` — usar `os.environ['JWT_SECRET']` (fail-fast)
- NUNCA hardcodar credentials, ARNs ou secrets
- Toda Lambda DEVE validar JWT
- Todo endpoint DEVE ter CORS configurado
- Uploads S3 DEVEM usar presigned URLs com TTL
- Feed público exige login (JWT) — sem acesso anônimo

---

## Regras Críticas de CDN

- Bucket `sstech-cdn-unified` é COMPARTILHADO por múltiplos projetos
- Deploy APENAS em `s3://sstech-cdn-unified/midiaflow/`
- `--delete` APENAS dentro do prefixo
- Invalidação APENAS: `--paths "/midiaflow/*"`
- NUNCA alterar distribution, CloudFront Function ou DNS

---

## CI/CD

- Pipeline: `test → build → deploy frontend → deploy lambdas (paralelo) → health-check → finops → notify`
- Push para `main` dispara deploy automático (~8 min)
- Rollback: `git revert HEAD && git push`
- Branch strategy: `dev` (desenvolvimento) → `main` (produção)

---

## Padrões de Código

- Handler Lambda: `lambda_function.lambda_handler` ou `index.lambda_handler`
- Sempre incluir error handling com HTTP status codes corretos
- Sempre retornar CORS headers nas respostas Lambda
- Usar `getUserFromToken()` de `lib/auth-utils.ts` para auth no frontend
- `AvatarUpload` é autossuficiente — não modificar sem necessidade
- `ContentCarousel` é reutilizável — não duplicar
- Usar Modal customizado — nunca `alert/confirm/prompt` nativo

### Ao criar nova Lambda:
1. Adicionar `JWT_SECRET` nas env vars
2. Taggear com `Project=MidiaFlow`
3. Adicionar ao pipeline em `deploy-production.yml`
4. Adicionar ao Terraform `modules/lambda/main.tf`
5. Configurar CORS nos headers de resposta

### Scripts de mídia (`scripts/media/`):
- Path local: `C:\Users\dell 5557\Videos\IDM`
- Prefixo S3: `users/sergio_sena`
- Estrutura local mapeia diretamente para S3
- FFmpeg: `C:\ffmpeg\bin\ffmpeg.exe`

---

## Gestão de Tarefas e Entregas

- Toda tarefa importante tem **Issue no GitHub** antes do código:
  - `correção` — bug fix
  - `melhoria` — aprimoramento existente
  - `nova função` — funcionalidade nova
- Todo **Pull Request** deve:
  - Mencionar a Issue (`Closes #N`)
  - Explicar o que mudou e por quê
  - Descrever como foi validado
  - Registrar riscos, limitações e próximos passos
- Branch `main` só recebe código após lint, testes e revisão aprovada

---

## Interface e UX

Toda interface deve ter:
- Skeleton screens durante carregamento (já implementado em v4.9.0)
- Lazy loading em listas e vídeos
- Animações suaves de entrada/saída
- Feedback visual para ações do usuário
- Estados de progresso em uploads e formulários
- Transições consistentes entre telas e modais

Referência: https://github.com/kylezantos/design-principles

---

## Observabilidade

- **CloudWatch** — logs de todas as 17 Lambdas (já configurado)
- **Cost Explorer** — custos por tag `Project=MidiaFlow` (já configurado)
- **FinOps AI** — relatório automático pós-deploy via Bedrock + SES
- **Sentry** — recomendado para erros no frontend (pendente)

---

## Checklist antes de chamar de pronto

- [ ] Issue criada e referenciada no PR
- [ ] Lint passou (`npm run lint`)
- [ ] Testes passando (`npm test`)
- [ ] Sem secrets no código
- [ ] CORS configurado na Lambda (se aplicável)
- [ ] Tag `Project=MidiaFlow` nos recursos AWS novos
- [ ] Interface revisada (skeleton, feedback, animações)
- [ ] Este arquivo atualizado se algo estrutural mudou

---

## Roadmap

- [ ] v4.10 — Área pública (conteúdo compartilhável, multi-resolução, legendas, analytics)
- [ ] Sentry no frontend
- [ ] Live streaming (MediaStore + MediaLive)
- [ ] API pública
- [ ] Mobile app (React Native)
