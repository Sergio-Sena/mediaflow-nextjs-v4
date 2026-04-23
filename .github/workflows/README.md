# 🚀 CI/CD Pipeline

## Pipeline: Deploy Production

**Trigger:** Push to `main` or manual dispatch

### Jobs

```
test → build → deploy-frontend ──→ health-check → finops → notify
                deploy-lambdas ──↗
```

| Job | O que faz | Tempo |
|---|---|---|
| test | `npm test` | ~2 min |
| build | `npm run build` + upload artifacts | ~3 min |
| deploy-frontend | S3 sync + CloudFront invalidation | ~1 min |
| deploy-lambdas | Deploy 17 Lambdas (paralelo) | ~2 min |
| health-check | Verifica frontend e API | ~30s |
| finops | Relatório de custos + AI insights + email | ~30s |
| notify | Status do deploy | ~10s |

**Total: ~8-10 minutos**

### Rollback

```bash
git revert HEAD
git push origin main
```

### Secrets necessários

| Secret | Descrição |
|---|---|
| `AWS_ACCESS_KEY_ID` | Credencial AWS |
| `AWS_SECRET_ACCESS_KEY` | Credencial AWS |
| `JWT_SECRET` | Secret para tokens JWT |
| `S3_BUCKET_FRONTEND` | Nome do bucket S3 |
| `CLOUDFRONT_DISTRIBUTION_ID` | ID da distribuição CloudFront |
| `NEXT_PUBLIC_API_URL` | URL da API Gateway |
