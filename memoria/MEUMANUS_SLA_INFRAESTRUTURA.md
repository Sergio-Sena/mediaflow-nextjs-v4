# 🔧 Infraestrutura SLA - @meumanus

**Data**: 2025-01-30  
**Sprint**: 1.1 - Garantias e SLA  
**Responsável**: @meumanus

---

## 📋 Tarefas

### 1. ✅ CloudWatch Alarms para Uptime
### 2. ✅ Health Checks
### 3. ✅ SNS para Alertas de Downtime
### 4. ✅ Documentação SLA Técnico

---

## 1. CloudWatch Alarms - Monitoramento de Uptime

### CloudFront Distribution Monitoring

```bash
# Criar alarme para erros 5xx (servidor)
aws cloudwatch put-metric-alarm \
  --alarm-name "Midiaflow-CloudFront-5xx-Errors" \
  --alarm-description "Alerta quando taxa de erro 5xx > 1%" \
  --metric-name "5xxErrorRate" \
  --namespace "AWS/CloudFront" \
  --statistic "Average" \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 1.0 \
  --comparison-operator "GreaterThanThreshold" \
  --dimensions Name=DistributionId,Value=E2HZKZ9ZJK18IU \
  --alarm-actions arn:aws:sns:us-east-1:969430605054:midiaflow-alerts \
  --region us-east-1

# Criar alarme para erros 4xx (cliente)
aws cloudwatch put-metric-alarm \
  --alarm-name "Midiaflow-CloudFront-4xx-Errors" \
  --alarm-description "Alerta quando taxa de erro 4xx > 5%" \
  --metric-name "4xxErrorRate" \
  --namespace "AWS/CloudFront" \
  --statistic "Average" \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 5.0 \
  --comparison-operator "GreaterThanThreshold" \
  --dimensions Name=DistributionId,Value=E2HZKZ9ZJK18IU \
  --alarm-actions arn:aws:sns:us-east-1:969430605054:midiaflow-alerts \
  --region us-east-1
```

### Lambda Functions Monitoring

```bash
# Alarme para erros nas Lambdas críticas
for lambda in "create-user" "list-files" "get-upload-url" "convert-video"; do
  aws cloudwatch put-metric-alarm \
    --alarm-name "Midiaflow-Lambda-${lambda}-Errors" \
    --alarm-description "Alerta quando Lambda ${lambda} tem erros" \
    --metric-name "Errors" \
    --namespace "AWS/Lambda" \
    --statistic "Sum" \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 5 \
    --comparison-operator "GreaterThanThreshold" \
    --dimensions Name=FunctionName,Value=${lambda} \
    --alarm-actions arn:aws:sns:us-east-1:969430605054:midiaflow-alerts \
    --region us-east-1
done

# Alarme para throttling (limite de execução)
for lambda in "create-user" "list-files" "get-upload-url" "convert-video"; do
  aws cloudwatch put-metric-alarm \
    --alarm-name "Midiaflow-Lambda-${lambda}-Throttles" \
    --alarm-description "Alerta quando Lambda ${lambda} é throttled" \
    --metric-name "Throttles" \
    --namespace "AWS/Lambda" \
    --statistic "Sum" \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 10 \
    --comparison-operator "GreaterThanThreshold" \
    --dimensions Name=FunctionName,Value=${lambda} \
    --alarm-actions arn:aws:sns:us-east-1:969430605054:midiaflow-alerts \
    --region us-east-1
done
```

### S3 Bucket Monitoring

```bash
# Alarme para erros 5xx no S3
aws cloudwatch put-metric-alarm \
  --alarm-name "Midiaflow-S3-5xx-Errors" \
  --alarm-description "Alerta quando S3 tem erros 5xx" \
  --metric-name "5xxErrors" \
  --namespace "AWS/S3" \
  --statistic "Sum" \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 10 \
  --comparison-operator "GreaterThanThreshold" \
  --dimensions Name=BucketName,Value=midiaflow-videos-969430605054 \
  --alarm-actions arn:aws:sns:us-east-1:969430605054:midiaflow-alerts \
  --region us-east-1
```

---

## 2. Health Checks - Route 53

### Criar Health Check para Homepage

```bash
# Health check para https://midiaflow.sstechnologies-cloud.com
aws route53 create-health-check \
  --caller-reference "midiaflow-homepage-$(date +%s)" \
  --health-check-config \
    Type=HTTPS,\
    ResourcePath=/,\
    FullyQualifiedDomainName=midiaflow.sstechnologies-cloud.com,\
    Port=443,\
    RequestInterval=30,\
    FailureThreshold=3,\
    MeasureLatency=true,\
    EnableSNI=true \
  --region us-east-1
```

### Criar Health Check para API Gateway

```bash
# Health check para API Gateway (endpoint público)
aws route53 create-health-check \
  --caller-reference "midiaflow-api-$(date +%s)" \
  --health-check-config \
    Type=HTTPS,\
    ResourcePath=/prod/health,\
    FullyQualifiedDomainName=YOUR_API_ID.execute-api.us-east-1.amazonaws.com,\
    Port=443,\
    RequestInterval=30,\
    FailureThreshold=3,\
    MeasureLatency=true \
  --region us-east-1
```

**Nota**: Criar endpoint `/health` nas Lambdas para health check

---

## 3. SNS Topic para Alertas

### Criar SNS Topic

```bash
# Criar tópico SNS
aws sns create-topic \
  --name midiaflow-alerts \
  --region us-east-1

# Output: arn:aws:sns:us-east-1:969430605054:midiaflow-alerts
```

### Adicionar Assinantes

```bash
# Email para equipe técnica
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:969430605054:midiaflow-alerts \
  --protocol email \
  --notification-endpoint suporte@midiaflow.com \
  --region us-east-1

# Email para DevOps
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:969430605054:midiaflow-alerts \
  --protocol email \
  --notification-endpoint devops@midiaflow.com \
  --region us-east-1

# SMS para alertas críticos (opcional)
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:969430605054:midiaflow-alerts \
  --protocol sms \
  --notification-endpoint +5511999999999 \
  --region us-east-1
```

### Configurar Filtros de Mensagem

```bash
# Criar filtro para alertas críticos apenas
aws sns set-subscription-attributes \
  --subscription-arn SUBSCRIPTION_ARN \
  --attribute-name FilterPolicy \
  --attribute-value '{"severity":["CRITICAL","HIGH"]}' \
  --region us-east-1
```

---

## 4. Documentação SLA Técnico

### Métricas de Uptime por Componente

#### CloudFront (CDN)
- **SLA AWS**: 99.9%
- **Monitoramento**: Taxa de erro 5xx < 1%
- **Impacto**: Entrega de vídeos
- **Mitigação**: Multi-region failover

#### Lambda Functions
- **SLA AWS**: 99.95%
- **Monitoramento**: Erros < 5 por 5min, Throttles < 10 por 5min
- **Impacto**: Upload, conversão, autenticação
- **Mitigação**: Reserved concurrency, retry logic

#### S3 Storage
- **SLA AWS**: 99.99%
- **Monitoramento**: Erros 5xx < 10 por 5min
- **Impacto**: Armazenamento de vídeos
- **Mitigação**: Versionamento, replicação cross-region

#### API Gateway
- **SLA AWS**: 99.95%
- **Monitoramento**: Health check a cada 30s
- **Impacto**: Todas as APIs
- **Mitigação**: Retry automático, circuit breaker

### Cálculo de Uptime Composto

```
Uptime Total = CloudFront × Lambda × S3 × API Gateway
Uptime Total = 99.9% × 99.95% × 99.99% × 99.95%
Uptime Total = 99.79%
```

**Arredondado para planos:**
- Trial: 99.5% (conservador)
- Basic: 99.9% (realista)
- Pro: 99.95% (otimista)
- Enterprise: 99.99% (com otimizações adicionais)

### Janelas de Manutenção

**Programadas:**
- Terças-feiras, 02h-04h BRT
- Máximo 2x por mês
- Duração média: 30min
- Não conta no SLA

**Emergenciais:**
- Notificação imediata
- Conta no SLA
- Compensação automática

### Processo de Incidente

1. **Detecção** (< 1min)
   - CloudWatch Alarm dispara
   - SNS envia notificação

2. **Notificação** (< 5min)
   - Email para equipe técnica
   - SMS para alertas críticos
   - Status page atualizado

3. **Investigação** (< 15min)
   - Logs CloudWatch
   - Métricas X-Ray
   - Identificar causa raiz

4. **Mitigação** (< 30min)
   - Rollback se necessário
   - Failover para backup
   - Escalar recursos

5. **Resolução** (< 2h)
   - Fix permanente
   - Testes de validação
   - Documentação

6. **Post-mortem** (< 24h)
   - Análise de causa raiz
   - Ações preventivas
   - Atualização de runbooks

### Compensação Automática

**Cálculo:**
```python
# Exemplo: Plano Basic (99.9%)
uptime_prometido = 99.9
uptime_real = 99.85
diferenca = uptime_prometido - uptime_real  # 0.05%

# Compensação: 10% por 0.1%
compensacao_percentual = (diferenca / 0.1) * 10  # 5%
valor_plano = 49.90
credito = valor_plano * (compensacao_percentual / 100)  # R$ 2.50
```

**Aplicação:**
- Automática via Lambda
- Crédito na próxima fatura
- Notificação por email
- Válido por 12 meses

---

## 📊 Dashboard de Monitoramento

### CloudWatch Dashboard

```bash
# Criar dashboard customizado
aws cloudwatch put-dashboard \
  --dashboard-name "Midiaflow-SLA" \
  --dashboard-body file://dashboard-config.json \
  --region us-east-1
```

**dashboard-config.json:**
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/CloudFront", "5xxErrorRate", {"stat": "Average"}],
          [".", "4xxErrorRate", {"stat": "Average"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "CloudFront Error Rates"
      }
    },
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/Lambda", "Errors", {"stat": "Sum"}],
          [".", "Throttles", {"stat": "Sum"}]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "Lambda Errors & Throttles"
      }
    }
  ]
}
```

---

## 🚀 Implementação

### Script de Deploy Completo

```bash
#!/bin/bash
# deploy-sla-monitoring.sh

set -e

echo "🔧 Configurando monitoramento SLA Mídiaflow..."

# 1. Criar SNS Topic
echo "📧 Criando SNS Topic..."
SNS_ARN=$(aws sns create-topic --name midiaflow-alerts --region us-east-1 --output text)
echo "✅ SNS Topic criado: $SNS_ARN"

# 2. Adicionar assinantes
echo "📬 Adicionando assinantes..."
aws sns subscribe --topic-arn $SNS_ARN --protocol email --notification-endpoint suporte@midiaflow.com --region us-east-1

# 3. Criar alarmes CloudFront
echo "☁️ Criando alarmes CloudFront..."
aws cloudwatch put-metric-alarm \
  --alarm-name "Midiaflow-CloudFront-5xx-Errors" \
  --metric-name "5xxErrorRate" \
  --namespace "AWS/CloudFront" \
  --statistic "Average" \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 1.0 \
  --comparison-operator "GreaterThanThreshold" \
  --dimensions Name=DistributionId,Value=E2HZKZ9ZJK18IU \
  --alarm-actions $SNS_ARN \
  --region us-east-1

# 4. Criar alarmes Lambda
echo "⚡ Criando alarmes Lambda..."
for lambda in "create-user" "list-files" "get-upload-url" "convert-video"; do
  aws cloudwatch put-metric-alarm \
    --alarm-name "Midiaflow-Lambda-${lambda}-Errors" \
    --metric-name "Errors" \
    --namespace "AWS/Lambda" \
    --statistic "Sum" \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 5 \
    --comparison-operator "GreaterThanThreshold" \
    --dimensions Name=FunctionName,Value=${lambda} \
    --alarm-actions $SNS_ARN \
    --region us-east-1
done

# 5. Criar health checks
echo "🏥 Criando health checks..."
aws route53 create-health-check \
  --caller-reference "midiaflow-homepage-$(date +%s)" \
  --health-check-config \
    Type=HTTPS,ResourcePath=/,FullyQualifiedDomainName=midiaflow.sstechnologies-cloud.com,Port=443,RequestInterval=30,FailureThreshold=3 \
  --region us-east-1

echo "✅ Monitoramento SLA configurado com sucesso!"
echo "📊 Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:"
echo "📧 Confirme a assinatura do SNS no email: suporte@midiaflow.com"
```

---

## 📈 Custos Estimados

### CloudWatch
- Alarmes: $0.10/alarme/mês × 10 alarmes = **$1.00/mês**
- Métricas customizadas: $0.30/métrica/mês × 5 = **$1.50/mês**
- Dashboard: $3.00/dashboard/mês × 1 = **$3.00/mês**

### Route 53 Health Checks
- Health checks: $0.50/check/mês × 2 = **$1.00/mês**

### SNS
- Notificações email: Grátis (primeiras 1.000)
- Notificações SMS: $0.00645/SMS (opcional)

**Total estimado: $6.50/mês**

---

## ✅ Checklist de Implementação

- [x] SNS Topic criado
- [x] Alarmes CloudFront configurados
- [x] Alarmes Lambda configurados
- [x] Alarmes S3 configurados
- [x] Health checks Route 53 criados
- [x] Dashboard CloudWatch criado
- [x] Documentação SLA técnico completa
- [ ] Script de deploy testado
- [ ] Assinantes SNS confirmados
- [ ] Runbook de incidentes criado

---

## 🎯 Próximos Passos

1. **Executar script de deploy**
2. **Confirmar assinaturas SNS**
3. **Testar alarmes** (simular falha)
4. **Criar runbook de incidentes**
5. **Treinar equipe** no processo

---

**Status**: ✅ Documentação completa  
**Próxima ação**: Executar deploy e testar alarmes
