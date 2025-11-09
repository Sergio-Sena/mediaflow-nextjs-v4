# ⚡ CI/CD Quick Start

## 🚀 Setup em 5 Minutos

### 1️⃣ Configure GitHub Secrets
```
Settings → Secrets and variables → Actions → New repository secret
```

**Adicione:**
- `AWS_ACCESS_KEY_ID` - Sua AWS access key
- `AWS_SECRET_ACCESS_KEY` - Sua AWS secret key
- `JWT_SECRET` - Seu JWT secret (do .env.local)
- `NEXT_PUBLIC_API_URL` - URL da sua API Gateway
- `S3_BUCKET_FRONTEND` - Nome do bucket S3 (ex: midiaflow-frontend)
- `CLOUDFRONT_DISTRIBUTION_ID` - ID da distribuição CloudFront

### 2️⃣ Crie Branch Develop
```bash
git checkout -b develop
git push -u origin develop
```

### 3️⃣ Teste Deploy Staging
```bash
git checkout develop
echo "# Test" >> test.txt
git add test.txt
git commit -m "test: CI/CD"
git push origin develop
```

✅ Vai para **GitHub → Actions** e veja o deploy acontecendo!

### 4️⃣ Deploy Production
```bash
# Criar PR de develop → main no GitHub
# Após merge → deploy automático para produção
```

## 📊 Workflows Disponíveis

| Workflow | Trigger | Ambiente |
|----------|---------|----------|
| Deploy Production | Push `main` | Produção |
| Deploy Staging | Push `develop` | Staging |
| PR Check | Pull Request | Validação |
| Rollback | Manual | Prod/Staging |
| Health Check | A cada 6h | Monitoramento |

## 🔄 Fluxo de Trabalho

```
1. Criar feature branch
   git checkout -b feature/nova-feature

2. Desenvolver e commitar
   git add .
   git commit -m "feat: nova feature"

3. Push e criar PR para develop
   git push origin feature/nova-feature
   # Criar PR no GitHub → develop

4. Após merge → auto-deploy staging
   # Testar em staging

5. Criar PR de develop → main
   # Após merge → auto-deploy produção
```

## 🆘 Rollback de Emergência

```
1. GitHub → Actions tab
2. Rollback Deployment → Run workflow
3. Selecionar:
   - Environment: production
   - Version: abc123 (commit SHA anterior)
4. Run workflow
```

## 📚 Documentação Completa

- **DEPLOYMENT.md** - Guia completo de deployment
- **.github/SECRETS.md** - Configuração de secrets
- **.github/workflows/README.md** - Documentação dos workflows
- **memoria/CICD_IMPLEMENTATION.md** - Detalhes técnicos

## ✅ Checklist

- [ ] Secrets configurados no GitHub
- [ ] Branch `develop` criada
- [ ] Primeiro deploy staging testado
- [ ] PR workflow testado
- [ ] Deploy production testado
- [ ] Rollback testado (opcional)

## 🎯 Pronto!

Seu CI/CD está configurado. Agora todo push para `main` ou `develop` faz deploy automático! 🚀
