# 🚀 Setup CI/CD - Guia Rápido

## Pré-requisitos

1. **GitHub CLI instalado**
   ```bash
   # Windows (winget)
   winget install GitHub.cli
   
   # Ou baixe: https://cli.github.com/
   ```

2. **Login no GitHub CLI**
   ```bash
   gh auth login
   ```

## Opção 1: Setup Automático (Recomendado)

```bash
python scripts/setup-github-cicd.py
```

O script vai pedir:
- AWS Access Key ID
- AWS Secret Access Key  
- CloudFront Distribution ID

## Opção 2: Setup Manual

### 1. Configure Secrets no GitHub

Vá em: `Settings → Secrets and variables → Actions → New repository secret`

Adicione:

| Secret | Valor |
|--------|-------|
| `AWS_ACCESS_KEY_ID` | Sua AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Sua AWS secret key |
| `JWT_SECRET` | `17b8312c72fdcffbff89f2f4a564fb26e936002d344717ab7753a237fcd57aea` |
| `NEXT_PUBLIC_API_URL` | `https://api.midiaflow.sstechnologies-cloud.com` |
| `S3_BUCKET_FRONTEND` | `midiaflow-frontend-969430605054` |
| `CLOUDFRONT_DISTRIBUTION_ID` | Seu CloudFront ID (veja abaixo) |

### 2. Encontre seu CloudFront Distribution ID

```bash
aws cloudfront list-distributions --query "DistributionList.Items[?Aliases.Items[?contains(@, 'midiaflow')]].Id" --output text
```

### 3. Crie branch develop

```bash
git checkout -b develop
git push -u origin develop
```

## Testando o CI/CD

### Teste 1: Deploy Staging

```bash
git checkout develop
echo "# Test CI/CD" >> test.txt
git add test.txt
git commit -m "test: CI/CD staging"
git push origin develop
```

Vá em: `GitHub → Actions` e veja o deploy!

### Teste 2: Deploy Production

```bash
# No GitHub, crie PR de develop → main
# Após merge → deploy automático
```

## Estrutura dos Workflows

```
.github/workflows/
├── deploy-production.yml    # Push main → Deploy produção
├── deploy-staging.yml       # Push develop → Deploy staging  
├── pr-check.yml            # PR → Testes
├── rollback.yml            # Manual → Rollback
└── health-check.yml        # Cron → Monitoramento
```

## Fluxo de Trabalho

```
1. Feature branch
   git checkout -b feature/nova-feature
   
2. Desenvolver
   git add .
   git commit -m "feat: nova feature"
   
3. PR para develop
   git push origin feature/nova-feature
   # Criar PR no GitHub
   
4. Merge → Auto-deploy staging
   
5. PR develop → main
   # Merge → Auto-deploy produção
```

## Rollback de Emergência

```
1. GitHub → Actions
2. Rollback Deployment → Run workflow
3. Selecionar:
   - Environment: production
   - Version: [commit SHA anterior]
4. Run workflow
```

## Verificar Status

```bash
# Ver último deploy
gh run list --limit 5

# Ver logs do último deploy
gh run view --log

# Ver status dos workflows
gh workflow list
```

## Troubleshooting

### Erro: "AWS credentials not found"
- Verifique se os secrets AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY estão configurados

### Erro: "CloudFront distribution not found"
- Verifique o CLOUDFRONT_DISTRIBUTION_ID

### Erro: "Lambda function not found"
- Verifique se os nomes das Lambdas estão corretos (prefixo `midiaflow-`)

## Próximos Passos

- [ ] Configurar secrets
- [ ] Criar branch develop
- [ ] Testar deploy staging
- [ ] Testar deploy production
- [ ] Configurar notificações (opcional)

## Documentação Completa

- **CICD_QUICKSTART.md** - Guia rápido
- **DEPLOYMENT.md** - Deploy manual
- **.github/workflows/README.md** - Detalhes dos workflows
- **memoria/CICD_IMPLEMENTATION.md** - Implementação técnica

---

✅ **Pronto! Seu CI/CD está configurado.**

Todo push para `main` ou `develop` faz deploy automático! 🚀
