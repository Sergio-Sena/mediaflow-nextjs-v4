# 🚀 Estratégia de Ambientes e Deploy - MidiaFlow

**Data**: 2026-03-07  
**Objetivo**: Garantir zero downtime e segurança em deploys  
**Metodologia**: Blue/Green Deployment + Ambientes Isolados

---

## 🎯 PROBLEMA IDENTIFICADO

**Situação Atual**:
- ❌ Deploy direto em produção (sem testes online)
- ❌ Um único ambiente (produção)
- ❌ Impossível testar features que dependem de AWS (CloudFront, Lambda, S3)
- ❌ Risco alto de quebrar produção

**Impacto**:
- 🔴 Bug em produção = downtime
- 🔴 Usuários afetados imediatamente
- 🔴 Sem rollback rápido

---

## 🏗️ ARQUITETURA PROPOSTA

### 3 Ambientes Isolados

```
┌─────────────────────────────────────────────────────────┐
│                    DESENVOLVIMENTO                       │
├─────────────────────────────────────────────────────────┤
│ Branch: develop                                          │
│ URL: dev.midiaflow.sstechnologies-cloud.com             │
│ CloudFront: E_DEV_XXXXXXX                               │
│ S3: mediaflow-frontend-dev-969430605054                 │
│ API: .../dev                                            │
│ DynamoDB: mediaflow-users-dev                           │
│ Uso: Testes de features novas                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                      STAGING                             │
├─────────────────────────────────────────────────────────┤
│ Branch: staging                                          │
│ URL: staging.midiaflow.sstechnologies-cloud.com         │
│ CloudFront: E_STAGING_XXXXXXX                           │
│ S3: mediaflow-frontend-staging-969430605054             │
│ API: .../staging                                        │
│ DynamoDB: mediaflow-users-staging                       │
│ Uso: Testes finais antes de produção                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     PRODUÇÃO                             │
├─────────────────────────────────────────────────────────┤
│ Branch: main                                             │
│ URL: midiaflow.sstechnologies-cloud.com                 │
│ CloudFront: E1O4R8P5BGZTMW (atual)                      │
│ S3: mediaflow-frontend-969430605054                     │
│ API: .../prod                                           │
│ DynamoDB: mediaflow-users                               │
│ Uso: Usuários reais                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🔵🟢 BLUE/GREEN DEPLOYMENT

### Conceito

```
BLUE (Versão Atual)          GREEN (Nova Versão)
┌──────────────────┐         ┌──────────────────┐
│  CloudFront A    │         │  CloudFront B    │
│  v4.8.5          │         │  v4.9.0          │
│  100% tráfego    │         │  0% tráfego      │
└──────────────────┘         └──────────────────┘
         │                            │
         └────────┬───────────────────┘
                  │
         ┌────────▼────────┐
         │   Route 53      │
         │   DNS Switch    │
         └─────────────────┘
```

### Fluxo de Deploy

**1. Preparação (GREEN)**
```bash
# Deploy nova versão em ambiente GREEN
aws s3 sync .next/static s3://mediaflow-frontend-green/_next/static
aws cloudfront create-distribution --config green-config.json
```

**2. Testes em GREEN**
```bash
# Testar via URL temporária
https://d3xxxxxxx.cloudfront.net (GREEN)

# Validações:
- ✅ Login funciona
- ✅ Upload funciona
- ✅ Dashboard carrega
- ✅ Player funciona
- ✅ Delete funciona
```

**3. Switch de Tráfego (Gradual)**
```bash
# Route 53 Weighted Routing
BLUE:  90% tráfego
GREEN: 10% tráfego (canary)

# Monitorar por 30 minutos
# Se OK, aumentar gradualmente
BLUE:  50% tráfego
GREEN: 50% tráfego

# Se OK, switch completo
BLUE:  0% tráfego
GREEN: 100% tráfego
```

**4. Rollback (Se Necessário)**
```bash
# Reverter DNS para BLUE
# Tempo de rollback: < 5 minutos
```

---

## 📋 IMPLEMENTAÇÃO PRÁTICA

### FASE 1: Criar Ambiente DEV (1 dia)

**1.1 Criar Buckets S3**
```bash
# Frontend DEV
aws s3 mb s3://mediaflow-frontend-dev-969430605054

# Uploads DEV
aws s3 mb s3://mediaflow-uploads-dev-969430605054

# Processed DEV
aws s3 mb s3://mediaflow-processed-dev-969430605054
```

**1.2 Criar CloudFront DEV**
```bash
python aws-setup/create-cloudfront-dev.py
# Output: E_DEV_XXXXXXX
```

**1.3 Criar DynamoDB DEV**
```bash
aws dynamodb create-table \
  --table-name mediaflow-users-dev \
  --attribute-definitions AttributeName=user_id,AttributeType=S \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

**1.4 Criar API Gateway Stage DEV**
```bash
aws apigateway create-deployment \
  --rest-api-id gdb962d234 \
  --stage-name dev
```

**1.5 Configurar DNS**
```bash
# Route 53
dev.midiaflow.sstechnologies-cloud.com → d_dev_xxxxx.cloudfront.net
```

**1.6 Variáveis de Ambiente**
```env
# .env.development
NEXT_PUBLIC_ENV=development
NEXT_PUBLIC_API_URL=https://gdb962d234.execute-api.us-east-1.amazonaws.com/dev
NEXT_PUBLIC_S3_UPLOADS_BUCKET=mediaflow-uploads-dev-969430605054
NEXT_PUBLIC_CLOUDFRONT_DOMAIN=d_dev_xxxxx.cloudfront.net
```

---

### FASE 2: Criar Ambiente STAGING (1 dia)

**Repetir passos da Fase 1, substituindo "dev" por "staging"**

---

### FASE 3: Implementar Blue/Green em PROD (2 dias)

**3.1 Criar CloudFront GREEN**
```bash
python aws-setup/create-cloudfront-green.py
# Output: E_GREEN_XXXXXXX
```

**3.2 Script de Deploy Blue/Green**
```bash
#!/bin/bash
# deploy-blue-green.sh

BLUE_DIST_ID="E1O4R8P5BGZTMW"
GREEN_DIST_ID="E_GREEN_XXXXXXX"
DOMAIN="midiaflow.sstechnologies-cloud.com"

echo "🔵 BLUE (atual): $BLUE_DIST_ID"
echo "🟢 GREEN (nova): $GREEN_DIST_ID"

# 1. Build
npm run build

# 2. Deploy para GREEN
aws s3 sync .next/static s3://mediaflow-frontend-green/_next/static --delete
for file in .next/server/app/*.html; do
  aws s3 cp "$file" s3://mediaflow-frontend-green/$(basename "$file" .html) \
    --cache-control "max-age=0,no-cache,no-store,must-revalidate" \
    --content-type "text/html"
done

# 3. Invalidar GREEN
aws cloudfront create-invalidation --distribution-id $GREEN_DIST_ID --paths "/*"

# 4. Testar GREEN
echo "🧪 Teste GREEN: https://d_green_xxxxx.cloudfront.net"
read -p "Testes OK? (y/n): " confirm

if [ "$confirm" = "y" ]; then
  # 5. Switch DNS (Canary 10%)
  echo "🔄 Switching 10% traffic to GREEN..."
  python aws-setup/switch-traffic.py --blue 90 --green 10
  
  # 6. Monitorar
  echo "⏳ Monitorando por 30 minutos..."
  sleep 1800
  
  # 7. Switch completo
  read -p "Switch 100% para GREEN? (y/n): " confirm_full
  if [ "$confirm_full" = "y" ]; then
    python aws-setup/switch-traffic.py --blue 0 --green 100
    echo "✅ Deploy completo! GREEN é a nova BLUE"
  fi
else
  echo "❌ Deploy cancelado. BLUE mantido."
fi
```

**3.3 Script de Rollback**
```bash
#!/bin/bash
# rollback.sh

BLUE_DIST_ID="E1O4R8P5BGZTMW"

echo "🔙 Rollback para BLUE: $BLUE_DIST_ID"
python aws-setup/switch-traffic.py --blue 100 --green 0
echo "✅ Rollback completo!"
```

---

## 🧪 ESTRATÉGIA DE TESTES

### Testes Locais (Antes de Deploy)
```bash
npm run dev
# Testar manualmente:
- Login
- Upload
- Dashboard
- Player
- Delete
```

### Testes em DEV (Após Deploy)
```bash
# Testes automatizados
npm run test:e2e -- --env=dev

# Testes manuais
https://dev.midiaflow.sstechnologies-cloud.com
```

### Testes em STAGING (Antes de PROD)
```bash
# Smoke tests
npm run test:smoke -- --env=staging

# Testes de carga
npm run test:load -- --env=staging

# Testes manuais críticos
- Login com usuário real
- Upload arquivo 1GB
- Delete em lote
```

### Testes em GREEN (Antes de Switch)
```bash
# Testes de sanidade
curl https://d_green_xxxxx.cloudfront.net/api/health

# Testes manuais
- Login
- Upload pequeno
- Dashboard
```

---

## 📊 MONITORAMENTO

### CloudWatch Alarms

**DEV**:
- Lambda errors > 5/min → Email
- API latency > 5s → Email

**STAGING**:
- Lambda errors > 3/min → Email
- API latency > 3s → Email

**PROD (BLUE/GREEN)**:
- Lambda errors > 1/min → PagerDuty
- API latency > 2s → PagerDuty
- 5xx errors > 0.1% → PagerDuty

### Métricas de Deploy

```bash
# Antes do switch
- Error rate BLUE: 0.01%
- Latency BLUE: 150ms

# Após switch 10% GREEN
- Error rate GREEN: 0.01% (OK)
- Latency GREEN: 160ms (OK)

# Critérios de sucesso:
✅ Error rate GREEN <= Error rate BLUE
✅ Latency GREEN <= Latency BLUE * 1.2
✅ Sem erros críticos por 30 min
```

---

## 💰 CUSTOS ESTIMADOS

### Ambiente DEV
- S3: $0.50/mês (10 GB)
- CloudFront: $1.00/mês (10 GB transfer)
- DynamoDB: $0.25/mês (on-demand)
- **Total**: ~$1.75/mês

### Ambiente STAGING
- S3: $1.00/mês (20 GB)
- CloudFront: $2.00/mês (20 GB transfer)
- DynamoDB: $0.50/mês (on-demand)
- **Total**: ~$3.50/mês

### Blue/Green PROD (Temporário)
- CloudFront GREEN: $5.00/mês (durante deploy)
- S3 duplicado: $2.00/mês (temporário)
- **Total**: ~$7.00/mês (apenas durante deploy)

### TOTAL MENSAL
- DEV + STAGING: $5.25/mês (permanente)
- Blue/Green: $7.00/mês (1-2 dias/mês)
- **Média**: ~$6.00/mês adicional

**ROI**: Evitar 1 bug em produção = economia de horas de trabalho + reputação

---

## 🎯 WORKFLOW DE DESENVOLVIMENTO

### 1. Feature Nova
```bash
# Criar branch
git checkout -b feature/nova-funcionalidade

# Desenvolver localmente
npm run dev

# Commit
git commit -m "feat: nova funcionalidade"

# Push para DEV
git push origin feature/nova-funcionalidade

# Deploy automático para DEV (GitHub Actions)
# Testar em: https://dev.midiaflow.sstechnologies-cloud.com
```

### 2. Pull Request
```bash
# Criar PR: feature/nova-funcionalidade → develop
# CI/CD roda testes automatizados
# Code review
# Merge para develop
```

### 3. Deploy STAGING
```bash
# Merge develop → staging
git checkout staging
git merge develop
git push origin staging

# Deploy automático para STAGING
# Testes finais em: https://staging.midiaflow.sstechnologies-cloud.com
```

### 4. Deploy PROD (Blue/Green)
```bash
# Merge staging → main
git checkout main
git merge staging
git push origin main

# Deploy manual Blue/Green
./deploy-blue-green.sh

# Monitorar
# Switch gradual
# Confirmar sucesso
```

---

## 📋 CHECKLIST DE DEPLOY

### Antes do Deploy
- [ ] Testes locais passando
- [ ] Testes em DEV passando
- [ ] Testes em STAGING passando
- [ ] Code review aprovado
- [ ] Documentação atualizada
- [ ] Changelog atualizado
- [ ] Backup de produção criado

### Durante o Deploy
- [ ] Build sem erros
- [ ] Deploy GREEN completo
- [ ] Testes em GREEN passando
- [ ] Monitoramento ativo
- [ ] Switch gradual (10% → 50% → 100%)
- [ ] Métricas dentro do esperado

### Após o Deploy
- [ ] Testes de sanidade em PROD
- [ ] Monitorar por 1 hora
- [ ] Confirmar métricas estáveis
- [ ] Desabilitar BLUE (após 24h)
- [ ] Atualizar documentação
- [ ] Comunicar time/usuários

---

## 🚨 PLANO DE ROLLBACK

### Cenários de Rollback

**1. Erro Crítico Detectado**
```bash
# Rollback imediato (< 5 min)
./rollback.sh
```

**2. Performance Degradada**
```bash
# Rollback se latency > 2x baseline
./rollback.sh
```

**3. Erro de Funcionalidade**
```bash
# Rollback se feature crítica quebrada
./rollback.sh
```

### Tempo de Rollback
- **DNS Switch**: 5 minutos
- **CloudFront Propagation**: 10-15 minutos
- **Total**: < 20 minutos

---

## 🎯 PRÓXIMOS PASSOS

### Prioridade MÁXIMA (Antes de Refatoração)
1. ✅ Corrigir bugs críticos (v4.8.6)
2. 🔴 Criar ambiente DEV
3. 🔴 Criar ambiente STAGING
4. 🔴 Implementar Blue/Green

### Prioridade ALTA (Após Ambientes)
5. 🟡 Configurar CI/CD (GitHub Actions)
6. 🟡 Implementar testes automatizados
7. 🟡 Configurar monitoramento

### Prioridade MÉDIA (Melhoria Contínua)
8. 🟢 Documentar processo de deploy
9. 🟢 Treinar time em Blue/Green
10. 🟢 Otimizar custos de ambientes

---

## 💡 CONCLUSÃO

**Benefícios**:
- ✅ Zero downtime em deploys
- ✅ Testes em ambiente real (AWS)
- ✅ Rollback rápido (< 20 min)
- ✅ Confiança para fazer mudanças
- ✅ Redução de bugs em produção

**Investimento**:
- **Tempo**: 4 dias (setup inicial)
- **Custo**: $6/mês adicional
- **ROI**: Evitar 1 bug = economia de horas + reputação

**Recomendação**: IMPLEMENTAR ANTES de iniciar refatoração (Fase 1-5)

---

**Status**: 📋 PLANEJADO  
**Prioridade**: 🔴 ALTA  
**Bloqueio**: Correções críticas (v4.8.6)  
**Próximo Passo**: Criar ambiente DEV
