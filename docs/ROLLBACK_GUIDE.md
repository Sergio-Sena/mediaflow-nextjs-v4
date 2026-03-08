# 🔄 Guia de Rollback - Porto Seguro v4.8.6

**Data**: 2026-03-08  
**Commit**: 0cef81a0  
**Tag**: v4.8.6-porto-seguro  
**Status**: ✅ TESTADO E FUNCIONANDO

---

## 📊 Estado Atual (Porto Seguro)

### Git
- **Commit**: 0cef81a0 (docs: atualizar documentação v4.8.6 - porto seguro)
- **Tag**: v4.8.6-porto-seguro
- **Branch**: main
- **GitHub**: ✅ Sincronizado

### Infraestrutura AWS
- **CloudFront**: E1O4R8P5BGZTMW (d2komwe8ylb0dt.cloudfront.net)
- **API Gateway**: gdb962d234 (prod)
- **Lambda files-handler**: Atualizada (2026-03-08T14:17:07)
- **S3 Frontend**: mediaflow-frontend-969430605054
- **DynamoDB**: mediaflow-users

### Funcionalidades Testadas
- ✅ Upload: Funcionando
- ✅ Delete: Funcionando (corrigido)
- ✅ Avatar: Funcionando
- ✅ Login: Funcionando
- ✅ Dashboard: Funcionando

---

## 🔄 ROLLBACK COMPLETO

### Opção 1: Rollback via Git (RECOMENDADO)

```bash
# 1. Verificar estado atual
git status
git log --oneline -3

# 2. Voltar para porto seguro
git checkout v4.8.6-porto-seguro

# 3. Criar branch de rollback
git checkout -b rollback-from-$(date +%Y%m%d)

# 4. Forçar main para porto seguro (SE NECESSÁRIO)
git checkout main
git reset --hard v4.8.6-porto-seguro
git push origin main --force

# 5. Rebuild e deploy
npm run build
aws s3 sync .next/static s3://mediaflow-frontend-969430605054/_next/static --delete
aws cloudfront create-invalidation --distribution-id E1O4R8P5BGZTMW --paths "/*"
```

### Opção 2: Rollback Apenas Frontend

```bash
# 1. Checkout do commit porto seguro
git checkout 0cef81a0 -- .next/

# 2. Rebuild
npm run build

# 3. Deploy
aws s3 sync .next/static s3://mediaflow-frontend-969430605054/_next/static --delete --cache-control "public,max-age=31536000,immutable"

# 4. Invalidar cache
aws cloudfront create-invalidation --distribution-id E1O4R8P5BGZTMW --paths "/*"
```

### Opção 3: Rollback Lambda files-handler

```bash
# 1. Recriar zip da versão porto seguro
cd aws-setup/lambda-functions/files-handler
powershell -Command "Compress-Archive -Path 'lambda_function.py' -DestinationPath '../files-handler-rollback.zip' -Force"

# 2. Deploy
aws lambda update-function-code \
  --function-name mediaflow-files-handler \
  --zip-file fileb://../files-handler-rollback.zip \
  --region us-east-1

# 3. Verificar
aws lambda get-function --function-name mediaflow-files-handler --query 'Configuration.LastModified'
```

---

## 🧪 TESTES PÓS-ROLLBACK

### 1. Teste de Upload
```bash
curl -X POST http://localhost:3000/api/upload/presigned \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"filename":"test.txt","contentType":"text/plain","fileSize":100}'
```

**Esperado**: `{"success":true,"uploadUrl":"..."}`

### 2. Teste de Delete
```bash
curl -X DELETE https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/files/delete \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"key":"users/sergio_sena/test.txt"}'
```

**Esperado**: `{"success":true}` ou `{"success":false,"message":"File not found"}`

### 3. Teste de Avatar
```bash
curl https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/me \
  -H "Authorization: Bearer <TOKEN>"
```

**Esperado**: `{"success":true,"user":{...,"avatar_url":"..."}}`

### 4. Teste de Login
```bash
curl -X POST https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sergio@midiaflow.com","password":"admin123"}'
```

**Esperado**: `{"success":true,"token":"..."}`

---

## 📋 CHECKLIST DE VALIDAÇÃO

### Antes do Rollback
- [ ] Documentar motivo do rollback
- [ ] Criar branch de backup das mudanças
- [ ] Notificar usuários (se necessário)
- [ ] Backup do DynamoDB (se houver mudanças)

### Durante o Rollback
- [ ] Executar rollback escolhido
- [ ] Aguardar propagação CloudFront (2-5 min)
- [ ] Verificar logs Lambda
- [ ] Verificar API Gateway

### Após o Rollback
- [ ] Executar todos os 4 testes acima
- [ ] Testar no browser (login, upload, delete)
- [ ] Verificar dashboard
- [ ] Confirmar com usuário final

---

## 🚨 PROBLEMAS CONHECIDOS E SOLUÇÕES

### Problema 1: CloudFront Cache Persistente
**Sintoma**: Mudanças não aparecem após deploy  
**Solução**:
```bash
# Invalidação agressiva
aws cloudfront create-invalidation --distribution-id E1O4R8P5BGZTMW --paths "/*"

# Aguardar 5 minutos
# Testar em modo anônimo (Ctrl+Shift+N)
```

### Problema 2: Lambda Não Atualiza
**Sintoma**: Código antigo ainda executando  
**Solução**:
```bash
# Verificar versão
aws lambda get-function --function-name mediaflow-files-handler --query 'Configuration.[LastModified,CodeSha256]'

# Forçar atualização
aws lambda update-function-configuration \
  --function-name mediaflow-files-handler \
  --description "Rollback to v4.8.6 - $(date)"
```

### Problema 3: API Gateway Não Responde
**Sintoma**: 403/500 em endpoints  
**Solução**:
```bash
# Redeployar stage
aws apigateway create-deployment \
  --rest-api-id gdb962d234 \
  --stage-name prod \
  --description "Rollback deployment"
```

---

## 📦 BACKUP MANUAL (Última Opção)

Se Git falhar, use backup manual:

### 1. Backup Código
```bash
# Criar backup completo
cd "c:\Projetos Git"
powershell -Command "Compress-Archive -Path 'MidiaFlow' -DestinationPath 'MidiaFlow-backup-$(Get-Date -Format yyyyMMdd-HHmmss).zip'"
```

### 2. Backup Lambda
```bash
# Download código Lambda atual
aws lambda get-function --function-name mediaflow-files-handler --query 'Code.Location' --output text > lambda-url.txt

# Baixar zip
curl -o files-handler-backup.zip $(cat lambda-url.txt)
```

### 3. Backup DynamoDB
```bash
# Scan completo
aws dynamodb scan --table-name mediaflow-users --output json > dynamodb-backup-$(date +%Y%m%d).json
```

---

## 🎯 CONTATOS DE EMERGÊNCIA

**Desenvolvedor**: Sergio Sena  
**AWS Account**: 969430605054  
**Region**: us-east-1  
**Suporte AWS**: https://console.aws.amazon.com/support/

---

## 📝 HISTÓRICO DE ROLLBACKS

| Data | Versão De | Versão Para | Motivo | Sucesso |
|------|-----------|-------------|--------|---------|
| - | - | - | - | - |

---

**Criado em**: 2026-03-08  
**Última atualização**: 2026-03-08  
**Versão**: 1.0
