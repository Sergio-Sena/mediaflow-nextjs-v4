# Roadmap v4.9 Ajustado - Infraestrutura Primeiro

**Data**: 27/01/2025  
**Estrategia**: Infraestrutura → Features  
**Duracao**: 30 dias

---

## Filosofia

**Infraestrutura primeiro, features depois**

Por que?
- CI/CD = Deploy seguro para todas as proximas features
- Logs = Debug 10x mais rapido
- Planos = Features com base solida

---

## Semana 1: CI/CD Pipeline (Dias 1-7)

### Objetivo
Deploy automatico, seguro e rapido

### Implementacao

**Dia 1-2: GitHub Actions**
```yaml
Workflow:
- Push para main → Testes → Deploy
- Push para staging → Testes → Deploy staging
- Push para dev → Testes → Deploy dev

Jobs:
1. test: Lint + testes
2. deploy-lambdas: 9 Lambdas
3. deploy-frontend: Build + S3 + CloudFront
```

**Dia 3-4: Ambientes**
```
dev:
  - S3: mediaflow-frontend-dev
  - API: api-dev.sstechnologies-cloud.com
  - DynamoDB: mediaflow-users-dev

staging:
  - S3: mediaflow-frontend-staging
  - API: api-staging.sstechnologies-cloud.com
  - DynamoDB: mediaflow-users-staging

prod:
  - S3: mediaflow-frontend-969430605054
  - API: gdb962d234.execute-api.us-east-1.amazonaws.com
  - DynamoDB: mediaflow-users
```

**Dia 5: Secrets & Docs**
```
GitHub Secrets:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- JWT_SECRET

Documentacao:
- README atualizado
- Guia de deploy
- Troubleshooting
```

### Resultado
- git push → Deploy automatico
- Rollback em 1 minuto
- Zero downtime

---

## Semana 2: Logs + Monitoring (Dias 8-14)

### Objetivo
Debug 10x mais rapido + alertas proativos

### Implementacao

**Dia 8-9: CloudWatch Logs JSON**
```python
# Estrutura padrao
{
  "timestamp": "2025-01-27T10:30:00Z",
  "level": "INFO",
  "correlation_id": "req_abc123",
  "function": "auth-handler",
  "user_id": "user_admin",
  "action": "login",
  "duration_ms": 245,
  "status": "success"
}

# Implementar em 9 Lambdas:
1. auth-handler
2. create-user
3. approve-user
4. files-handler
5. upload-handler
6. multipart-handler
7. list-users
8. update-user
9. verify-user-2fa
```

**Dia 10-11: CloudWatch Alarms**
```
Alertas criticos:
- Lambda errors > 5% (5 min)
- API latency > 3s (5 min)
- S3 storage > 300 GB (1 dia)
- Custos AWS > $100/mes (1 dia)

Alertas warning:
- Lambda duration > 2s (15 min)
- DynamoDB throttling (5 min)
- CloudFront 5xx > 1% (10 min)
```

**Dia 12-13: Dashboard CloudWatch**
```
Widgets:
- Lambda invocations (ultimas 24h)
- Error rate por funcao
- Latencia media
- Storage S3 (GB)
- Custos estimados
- Usuarios ativos
```

**Dia 14: SNS Notifications**
```
Email para admin:
- Alertas criticos (imediato)
- Relatorio diario (8h)
- Relatorio semanal (segunda 8h)
```

### Resultado
- Detecta problemas antes dos usuarios
- Debug em minutos (nao horas)
- Controle de custos em tempo real

---

## Semana 3-4: Sistema de Planos (Dias 15-30)

### Objetivo
Controle de custos + base para monetizacao

### Implementacao

**Semana 3 (Dias 15-21): Backend**

**Dia 15-16: DynamoDB Schema**
```json
{
  "user_id": "user_123",
  "plan": "pro",
  "plan_limits": {
    "storage_gb": 500,
    "uploads_per_month": -1,
    "conversion_minutes": 30,
    "conversion_quality": "4k"
  },
  "usage_current_month": {
    "storage_used_gb": 125.5,
    "uploads_count": 45,
    "conversion_minutes_used": 12
  },
  "billing_cycle_start": "2025-01-01",
  "next_reset": "2025-02-01"
}
```

**Dia 17-18: Lambda Middleware**
```python
def check_limits(user_id, action):
    user = get_user(user_id)
    usage = user['usage_current_month']
    limits = user['plan_limits']
    
    if action == 'upload':
        if limits['uploads_per_month'] != -1:
            if usage['uploads_count'] >= limits['uploads_per_month']:
                return {'allowed': False, 'reason': 'Upload limit reached'}
    
    if action == 'convert':
        if usage['conversion_minutes_used'] >= limits['conversion_minutes']:
            return {'allowed': False, 'reason': 'Conversion limit reached'}
    
    return {'allowed': True}
```

**Dia 19-21: Lambda Usage Tracking**
```python
def track_usage(user_id, action, amount):
    # Incrementa uso
    if action == 'upload':
        increment_field('uploads_count', 1)
    elif action == 'storage':
        update_field('storage_used_gb', amount)
    elif action == 'conversion':
        increment_field('conversion_minutes_used', amount)
    
    # Verifica se atingiu 80%, 90%, 100%
    check_and_alert_limits(user_id)
```

**Semana 4 (Dias 22-30): Frontend**

**Dia 22-24: Admin Panel**
```typescript
// Modal de aprovacao com planos
<Modal title="Aprovar Usuario">
  <UserInfo user={selectedUser} />
  
  <Select value={plan} onChange={setPlan}>
    <Option value="free">Free (1 GB, sem conversao)</Option>
    <Option value="basic">Basic (50 GB, 60 min/mes)</Option>
    <Option value="pro">Pro (500 GB, 30 min 4K/mes)</Option>
    <Option value="vip">VIP (Ilimitado)</Option>
  </Select>
  
  <PlanDetails plan={plan} />
  
  <Button onClick={approveWithPlan}>Aprovar</Button>
</Modal>

// Dashboard de uso por usuario
<Table>
  <Column title="Usuario" />
  <Column title="Plano" />
  <Column title="Storage" render={(user) => 
    `${user.usage.storage_used_gb} / ${user.limits.storage_gb} GB`
  } />
  <Column title="Uploads" />
  <Column title="Conversao" />
</Table>
```

**Dia 25-27: User Dashboard**
```typescript
// Card de uso no dashboard
<Card title="Seu Plano: Pro">
  <Progress 
    percent={usage.storage_used / limits.storage_gb * 100}
    status={usage.storage_used > limits.storage_gb * 0.9 ? 'exception' : 'normal'}
  />
  <Text>Storage: {usage.storage_used} / {limits.storage_gb} GB</Text>
  
  <Progress percent={usage.uploads_count / limits.uploads_per_month * 100} />
  <Text>Uploads: {usage.uploads_count} / {limits.uploads_per_month}</Text>
  
  <Button onClick={upgrade}>Fazer Upgrade</Button>
</Card>
```

**Dia 28-30: Emails SES**
```python
# Template limite atingido
subject = "Limite de {tipo} atingido"
body = f"""
Ola {user.name},

Voce atingiu {percent}% do seu limite de {tipo}.

Plano atual: {user.plan}
Uso: {usage} / {limit}

Faca upgrade: https://midiaflow.sstechnologies-cloud.com/pricing

Equipe Midiaflow
"""

# Enviar em 80%, 90%, 100%
```

### Resultado
- Controle total de custos
- Base para cobranca futura
- UX profissional

---

## Checklist de Entrega

### Semana 1: CI/CD
- [ ] GitHub Actions configurado
- [ ] Deploy automatico funcionando
- [ ] Ambientes dev/staging/prod
- [ ] Secrets configurados
- [ ] Documentacao atualizada

### Semana 2: Logs + Monitoring
- [ ] Logs JSON em 9 Lambdas
- [ ] CloudWatch Alarms configurados
- [ ] Dashboard criado
- [ ] SNS notifications ativas
- [ ] Testes de alertas

### Semana 3-4: Planos
- [ ] DynamoDB schema atualizado
- [ ] Middleware de limites
- [ ] Usage tracking
- [ ] Admin panel com planos
- [ ] User dashboard com uso
- [ ] Emails SES configurados
- [ ] Testes end-to-end

---

## Metricas de Sucesso

### CI/CD
- Deploy time: < 5 min
- Success rate: > 95%
- Rollback time: < 2 min

### Logs + Monitoring
- Debug time: 10x mais rapido
- Alertas criticos: < 5 min deteccao
- False positives: < 10%

### Planos
- Usuarios com limites: 100%
- Alertas enviados: 100%
- Custos controlados: < $50/mes

---

## Proximos Passos (v5.0)

Apos v4.9 completo:
1. Integracao Stripe (cobranca real)
2. Billing dashboard (faturas)
3. Player avancado (legendas, qualidades)
4. Mobile PWA

---

**Status**: Planejado  
**Inicio**: 27/01/2025  
**Fim estimado**: 26/02/2025  
**Responsavel**: Equipe Midiaflow
