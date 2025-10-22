# 🏗️ Roadmap de Infraestrutura - Mídiaflow

> **Priorização técnica para robustez e escalabilidade**

---

## 🔥 **PRIORIDADE 1: CRÍTICO (v4.8)**

### **1.1 Sistema de Controle de Acesso** 🆕
**Tempo**: 2-3 dias | **Impacto**: CRÍTICO | **Custo**: $0

**Problema Atual:**
- ❌ Cadastro público aberto (qualquer um pode se registrar)
- ❌ Admin paga storage/processamento de todos os usuários
- ❌ Sem controle de custos ou receita
- ❌ Risco financeiro crescente

**Solução:**
```typescript
// Sistema híbrido: Códigos de convite + Aprovação manual

1. Códigos de Convite:
   - Admin gera: "CONV-2025-ABC123"
   - User usa no cadastro → aprovado automaticamente
   - Código expira após uso ou prazo

2. Aprovação Manual:
   - User se cadastra sem código → status "pending"
   - Admin aprova/rejeita no painel
   - Notificações automáticas

3. Status de Usuário:
   - pending: Aguardando aprovação
   - approved: Acesso liberado
   - rejected: Cadastro negado
   - suspended: Bloqueado temporariamente
```

**Implementação:**
- [ ] Nova tabela DynamoDB: `mediaflow-invites`
- [ ] Atualizar tabela: `mediaflow-users` (campo status)
- [ ] Nova Lambda: `invite-manager`
- [ ] Nova Lambda: `user-approval`
- [ ] Frontend: campo código no cadastro
- [ ] Admin panel: aba "Controle de Acesso"
- [ ] Middleware: verificação de status

**Benefícios:**
- ✅ Controle total de novos usuários
- ✅ Economia imediata de custos
- ✅ Base para monetização futura
- ✅ Rastreabilidade completa

**Documentação**: `memoria/ROADMAP_MONETIZACAO.md`

---

### **1.2 Logs Estruturados CloudWatch**
**Tempo**: 3 horas | **Impacto**: CRÍTICO | **Custo**: $0

**Problema Atual:**
- ❌ Debugging difícil (logs desorganizados)
- ❌ Não detecta erros em produção
- ❌ Sem métricas de performance
- ❌ Usuários reportam bugs invisíveis

**Solução:**
```python
# Implementar em TODAS as 8 Lambdas:
import json
import time

def lambda_handler(event, context):
    request_id = context.request_id
    start_time = time.time()
    
    try:
        result = process_request(event)
        
        # Log estruturado de sucesso
        print(json.dumps({
            "level": "INFO",
            "request_id": request_id,
            "user_id": event.get("user_id"),
            "action": "nome_acao",
            "duration_ms": (time.time() - start_time) * 1000,
            "status": "success"
        }))
        
        return result
        
    except Exception as e:
        # Log estruturado de erro
        print(json.dumps({
            "level": "ERROR",
            "request_id": request_id,
            "user_id": event.get("user_id"),
            "action": "nome_acao",
            "error": str(e),
            "stack_trace": traceback.format_exc(),
            "duration_ms": (time.time() - start_time) * 1000,
            "status": "error"
        }))
        raise
```

**Lambdas a modificar:**
1. ✅ `upload` - Logs de upload com tamanho de arquivo
2. ✅ `multipart-upload` - Logs de partes e progresso
3. ✅ `list-files` - Logs de queries S3
4. ✅ `delete-file` - Logs de deleção com path
5. ✅ `convert-video` - Logs de MediaConvert jobs
6. ✅ `auth` - Logs de login/JWT (SEM senhas)
7. ✅ `create-user` - Logs de cadastro
8. ✅ `folder-operations` - Logs de CRUD de pastas

**Benefícios:**
- ✅ CloudWatch Insights funciona 10x melhor
- ✅ Rastreamento de requests (correlation ID)
- ✅ Métricas de performance automáticas
- ✅ Alertas de erro em tempo real

**Entregáveis:**
- [ ] Script `add-structured-logging.py` (atualiza todas as Lambdas)
- [ ] CloudWatch Dashboard com métricas
- [ ] Alertas SNS para erros críticos
- [ ] Documentação de logs em `memoria/LOGS.md`

---

## ⚡ **PRIORIDADE 2: ALTA (v4.8)**

### **2.1 CI/CD com GitHub Actions**
**Tempo**: 1 dia | **Impacto**: ALTO | **Custo**: $0

**Problema Atual:**
- ❌ Deploy manual (propenso a erros)
- ❌ Testa em produção (arriscado)
- ❌ Rollback manual (lento)
- ❌ Sem histórico de deploys

**Solução:**
```yaml
# .github/workflows/deploy.yml
name: Deploy Mídiaflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '22'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run build

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      
      - uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy Frontend
        run: |
          aws s3 sync out/ s3://mediaflow-frontend-969430605054 --delete
          aws cloudfront create-invalidation --distribution-id E3ODIUY4LXU8TH --paths "/*"
      
      - name: Deploy Lambdas
        run: |
          cd aws-setup/lambda-functions
          for dir in */; do
            cd "$dir"
            zip -r function.zip .
            aws lambda update-function-code --function-name "mediaflow-${dir%/}" --zip-file fileb://function.zip
            cd ..
          done
```

**Benefícios:**
- ✅ Deploy automático (git push = produção)
- ✅ Testes antes de deploy
- ✅ Rollback com `git revert`
- ✅ Histórico completo de mudanças
- ✅ Prepara para ambientes dev/staging

**Entregáveis:**
- [ ] `.github/workflows/deploy.yml`
- [ ] `.github/workflows/test.yml`
- [ ] Secrets configurados no GitHub
- [ ] Badge de status no README
- [ ] Documentação em `memoria/CI_CD.md`

---

### **2.2 Ambientes Separados (dev/staging/prod)**
**Tempo**: 1 dia | **Impacto**: ALTO | **Custo**: +$15/mês

**Problema Atual:**
- ❌ Testa features em produção
- ❌ Bug pode derrubar sistema
- ❌ Usuários veem features incompletas

**Solução:**
```yaml
# Estratégia de Branches:
main → Produção (midiaflow.sstechnologies-cloud.com)
dev  → Staging (dev.midiaflow.sstechnologies-cloud.com)

# API Gateway Stages:
/prod → Lambdas com alias 'prod'
/dev  → Lambdas com alias 'dev'

# S3 Buckets:
mediaflow-frontend-969430605054      → Produção
mediaflow-frontend-dev-969430605054  → Staging

# DynamoDB Tables:
mediaflow-users      → Produção
mediaflow-users-dev  → Staging
```

**Workflow:**
1. Desenvolve em branch `dev`
2. Push → Deploy automático em staging
3. Testa em `dev.midiaflow.sstechnologies-cloud.com`
4. Merge para `main` → Deploy em produção

**Benefícios:**
- ✅ Testa sem afetar usuários
- ✅ Rollback instantâneo
- ✅ Features em beta antes de produção
- ✅ Dados de teste separados

**Entregáveis:**
- [ ] CloudFront distribution para dev
- [ ] API Gateway stage 'dev'
- [ ] Lambda aliases (prod/dev)
- [ ] DynamoDB table dev
- [ ] Script `setup-dev-environment.py`
- [ ] Documentação em `memoria/AMBIENTES.md`

---

## 🛡️ **PRIORIDADE 3: MÉDIA (v4.9)**

### **3.1 Rate Limiting no API Gateway**
**Tempo**: 15 minutos | **Impacto**: MÉDIO | **Custo**: $0

**Problema Atual:**
- ❌ Sem proteção contra abuso
- ❌ Custos podem explodir
- ❌ DDoS pode derrubar API

**Solução:**
```python
# Script: setup-rate-limiting.py
import boto3

client = boto3.client('apigateway')

# Criar Usage Plan
usage_plan = client.create_usage_plan(
    name='midiaflow-standard',
    throttle={
        'rateLimit': 10.0,      # 10 req/segundo sustentado
        'burstLimit': 100       # 100 req/segundo burst
    },
    quota={
        'limit': 10000,         # 10k requests/dia
        'period': 'DAY'
    }
)

# Associar ao API Gateway
client.create_usage_plan_key(
    usagePlanId=usage_plan['id'],
    keyId='API_KEY_ID',
    keyType='API_KEY'
)
```

**Limites Sugeridos:**
- **Usuário Normal**: 10 req/s, 10k req/dia
- **Admin**: 50 req/s, 100k req/dia
- **Upload**: 1 req/s (arquivos grandes)

**Benefícios:**
- ✅ Protege contra abuso
- ✅ Controla custos AWS
- ✅ Mitiga DDoS básico
- ✅ Sem impacto em uso normal

**Entregáveis:**
- [ ] Script `setup-rate-limiting.py`
- [ ] Usage Plans configurados
- [ ] Documentação em README

---

### **3.2 Monitoramento e Alertas**
**Tempo**: 2 horas | **Impacto**: MÉDIO | **Custo**: $5/mês

**Problema Atual:**
- ❌ Não sabe quando sistema cai
- ❌ Descobre bugs por usuários
- ❌ Sem métricas de saúde

**Solução:**
```python
# CloudWatch Alarms
alarms = [
    {
        'name': 'Lambda-Errors-High',
        'metric': 'Errors',
        'threshold': 10,        # 10 erros em 5 min
        'period': 300,
        'action': 'SNS_TOPIC_ARN'
    },
    {
        'name': 'API-Latency-High',
        'metric': 'Latency',
        'threshold': 3000,      # 3 segundos
        'period': 60,
        'action': 'SNS_TOPIC_ARN'
    },
    {
        'name': 'S3-Upload-Failures',
        'metric': '4xxErrors',
        'threshold': 5,
        'period': 300,
        'action': 'SNS_TOPIC_ARN'
    }
]
```

**Alertas via:**
- 📧 Email (SNS)
- 📱 SMS (opcional, +$0.50/alerta)
- 💬 Slack/Discord (webhook)

**Benefícios:**
- ✅ Detecta problemas em minutos
- ✅ Resolve antes de usuários reclamarem
- ✅ Métricas de uptime
- ✅ Dashboard de saúde

**Entregáveis:**
- [ ] CloudWatch Dashboard
- [ ] 5 alarmes críticos
- [ ] SNS topic configurado
- [ ] Script `setup-monitoring.py`

---

## 📚 **PRIORIDADE 4: BAIXA (v5.0+)**

### **4.1 Versionamento de API (v1, v2)**
**Quando**: Abrir API pública  
**Tempo**: 1 dia | **Impacto**: BAIXO | **Custo**: $0

**Necessário apenas quando:**
- ✅ API pública para terceiros
- ✅ Múltiplos clientes (mobile, web, etc)
- ✅ Breaking changes frequentes

**Solução:**
```
/api/v1/files     → Versão estável
/api/v2/files     → Versão nova (breaking changes)
/api/v1/upload    → Mantém compatibilidade
```

---

### **4.2 API Keys para Terceiros**
**Quando**: API pública  
**Tempo**: 2 horas | **Impacto**: BAIXO | **Custo**: $0

**Necessário apenas quando:**
- ✅ Integrações externas (Zapier, etc)
- ✅ Webhooks para terceiros
- ✅ Rate limiting por cliente

---

### **4.3 Documentação OpenAPI/Swagger**
**Quando**: Contratar devs ou API pública  
**Tempo**: 1 dia | **Impacto**: BAIXO | **Custo**: $0

**Necessário apenas quando:**
- ✅ Equipe com 3+ desenvolvedores
- ✅ API pública documentada
- ✅ 20+ endpoints

---

## 📊 **Resumo de Prioridades**

| # | Item | Versão | Tempo | Custo | Impacto | Status |
|---|------|--------|-------|-------|---------|--------|
| 1 | **Logs Estruturados** | v4.8 | 3h | $0 | 🔥 CRÍTICO | ⏳ Pendente |
| 2 | **CI/CD GitHub Actions** | v4.8 | 1d | $0 | ⚡ ALTO | ⏳ Pendente |
| 3 | **Ambientes dev/prod** | v4.8 | 1d | +$15/mês | ⚡ ALTO | ⏳ Pendente |
| 4 | **Rate Limiting** | v4.9 | 15m | $0 | 🛡️ MÉDIO | ⏳ Pendente |
| 5 | **Monitoramento** | v4.9 | 2h | +$5/mês | 🛡️ MÉDIO | ⏳ Pendente |
| 6 | Versionamento API | v5.0+ | 1d | $0 | 📚 BAIXO | 🔮 Futuro |
| 7 | API Keys | v5.0+ | 2h | $0 | 📚 BAIXO | 🔮 Futuro |
| 8 | OpenAPI/Swagger | v5.0+ | 1d | $0 | 📚 BAIXO | 🔮 Futuro |

---

## 🎯 **Plano de Execução v4.8**

### **Sprint 1: Observabilidade (3 horas)**
```bash
Dia 1:
- [ ] Implementar logs estruturados em 8 Lambdas
- [ ] Criar CloudWatch Dashboard
- [ ] Configurar alertas SNS básicos
- [ ] Testar em produção
- [ ] Deploy + documentação
```

### **Sprint 2: CI/CD (1 dia)**
```bash
Dia 2:
- [ ] Criar .github/workflows/deploy.yml
- [ ] Configurar secrets no GitHub
- [ ] Testar workflow em branch test
- [ ] Merge para main (primeiro deploy automático)
- [ ] Documentar processo
```

### **Sprint 3: Ambientes (1 dia)**
```bash
Dia 3:
- [ ] Criar infraestrutura dev (S3, CloudFront, API Gateway)
- [ ] Configurar Lambda aliases
- [ ] Criar DynamoDB table dev
- [ ] Atualizar CI/CD para deploy em dev
- [ ] Testar fluxo completo dev → prod
```

---

## 💰 **Impacto Financeiro**

```
Custo Atual (v4.7):           $20/mês
+ Logs estruturados:          $0
+ CI/CD GitHub Actions:       $0
+ Ambiente dev:               +$15/mês
+ Rate limiting:              $0
+ Monitoramento:              +$5/mês
────────────────────────────────────
Total v4.9:                   $40/mês

ROI:
- Debugging 10x mais rápido
- Zero downtime em deploys
- Bugs detectados antes de usuários
- Economia de tempo: ~10h/mês
```

---

## 📈 **Métricas de Sucesso**

### **Após v4.8:**
- ✅ Deploy time: 15min → 3min (automático)
- ✅ Bug detection: 24h → 5min (alertas)
- ✅ Rollback time: 30min → 1min (git revert)
- ✅ Debugging time: 2h → 15min (logs estruturados)

### **Após v4.9:**
- ✅ Uptime: 99.9% → 99.95%
- ✅ Zero deploys quebrados
- ✅ Features testadas antes de produção
- ✅ Custos controlados (rate limiting)

---

## 🚀 **Próximos Passos**

Implementar em ordem:
1. **Logs estruturados** (3h) - Impacto imediato
2. **CI/CD** (1d) - Automação crítica
3. **Ambientes dev/prod** (1d) - Segurança
4. **Rate limiting** (15m) - Proteção
5. **Monitoramento** (2h) - Visibilidade

**Total v4.8**: 2.5 dias de trabalho  
**Benefício**: Sistema robusto para escalar

---

*Última atualização: 22/01/2025*  
*Versão atual: v4.7.1*  
*Próxima versão: v4.8.0 (Infraestrutura + Controle de Acesso)*
