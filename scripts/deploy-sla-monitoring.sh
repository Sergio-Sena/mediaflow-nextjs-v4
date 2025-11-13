#!/bin/bash
# deploy-sla-monitoring.sh
# Script para configurar monitoramento SLA do Mídiaflow

set -e

echo "🔧 Configurando monitoramento SLA Mídiaflow..."

# Variáveis
REGION="us-east-1"
ACCOUNT_ID="969430605054"
CLOUDFRONT_ID="E2HZKZ9ZJK18IU"
DOMAIN="midiaflow.sstechnologies-cloud.com"

# 1. Criar SNS Topic
echo "📧 Criando SNS Topic..."
SNS_ARN=$(aws sns create-topic \
  --name midiaflow-alerts \
  --region $REGION \
  --output text 2>/dev/null || echo "arn:aws:sns:$REGION:$ACCOUNT_ID:midiaflow-alerts")
echo "✅ SNS Topic: $SNS_ARN"

# 2. Adicionar assinantes
echo "📬 Adicionando assinantes..."
aws sns subscribe \
  --topic-arn $SNS_ARN \
  --protocol email \
  --notification-endpoint suporte@midiaflow.com \
  --region $REGION \
  --no-cli-pager 2>/dev/null || echo "⚠️ Assinante já existe"

# 3. Criar alarmes CloudFront
echo "☁️ Criando alarmes CloudFront..."

# Alarme 5xx
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
  --dimensions Name=DistributionId,Value=$CLOUDFRONT_ID \
  --alarm-actions $SNS_ARN \
  --region $REGION \
  --no-cli-pager

# Alarme 4xx
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
  --dimensions Name=DistributionId,Value=$CLOUDFRONT_ID \
  --alarm-actions $SNS_ARN \
  --region $REGION \
  --no-cli-pager

echo "✅ Alarmes CloudFront criados"

# 4. Criar alarmes Lambda
echo "⚡ Criando alarmes Lambda..."

LAMBDAS=("create-user" "list-files" "get-upload-url" "convert-video")

for lambda in "${LAMBDAS[@]}"; do
  # Alarme de erros
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
    --alarm-actions $SNS_ARN \
    --region $REGION \
    --no-cli-pager
  
  # Alarme de throttling
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
    --alarm-actions $SNS_ARN \
    --region $REGION \
    --no-cli-pager
done

echo "✅ Alarmes Lambda criados"

# 5. Criar alarme S3
echo "💾 Criando alarmes S3..."

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
  --dimensions Name=BucketName,Value=midiaflow-videos-$ACCOUNT_ID \
  --alarm-actions $SNS_ARN \
  --region $REGION \
  --no-cli-pager

echo "✅ Alarmes S3 criados"

# 6. Criar health check Route 53
echo "🏥 Criando health check..."

HEALTH_CHECK_ID=$(aws route53 create-health-check \
  --caller-reference "midiaflow-homepage-$(date +%s)" \
  --health-check-config \
    Type=HTTPS,ResourcePath=/,FullyQualifiedDomainName=$DOMAIN,Port=443,RequestInterval=30,FailureThreshold=3,MeasureLatency=true,EnableSNI=true \
  --query 'HealthCheck.Id' \
  --output text 2>/dev/null || echo "existing")

if [ "$HEALTH_CHECK_ID" != "existing" ]; then
  echo "✅ Health check criado: $HEALTH_CHECK_ID"
else
  echo "⚠️ Health check já existe"
fi

# 7. Resumo
echo ""
echo "✅ Monitoramento SLA configurado com sucesso!"
echo ""
echo "📊 Recursos criados:"
echo "  - SNS Topic: $SNS_ARN"
echo "  - Alarmes CloudFront: 2"
echo "  - Alarmes Lambda: 8 (4 funções × 2 tipos)"
echo "  - Alarmes S3: 1"
echo "  - Health Check: 1"
echo ""
echo "📧 IMPORTANTE: Confirme a assinatura do SNS no email: suporte@midiaflow.com"
echo "📈 Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=$REGION#dashboards:"
echo ""
echo "🧪 Para testar os alarmes:"
echo "  aws cloudwatch set-alarm-state --alarm-name Midiaflow-CloudFront-5xx-Errors --state-value ALARM --state-reason 'Testing'"
