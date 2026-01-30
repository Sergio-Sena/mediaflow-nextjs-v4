# 🔧 Sessão 2025-01-29: Correção Upload com JWT

## ✅ Problema Resolvido

**Erro**: Upload não salvava em `users/{user_id}/`, salvava na raiz do bucket.

**Causa**: Lambda `midiaflow-upload-handler` (nome errado) não tinha biblioteca PyJWT instalada.

---

## 🛠️ Correções Implementadas

### 1. Lambda Upload Handler
- ✅ Identificado Lambda correto: `mediaflow-upload-handler` (com "e")
- ✅ Instalado PyJWT no Lambda
- ✅ Lambda agora extrai `user_id` do JWT corretamente
- ✅ Arquivos salvos automaticamente em `users/{user_id}/`
- ✅ Deletado Lambda duplicado `midiaflow-upload-handler` (com "i")

### 2. Frontend DirectUpload
- ✅ Chama Lambda diretamente via `aws-config.ts`
- ✅ Envia JWT no `Authorization: Bearer {token}`
- ✅ Auto-adiciona pasta do usuário se não for admin
- ✅ Barra de progresso melhorada:
  - Inicia em 0% (visível desde o início)
  - Mostra percentual numérico (ex: "45%")
  - Delay de 500ms em 100% antes de marcar sucesso

### 3. API Gateway
- ✅ Atualizado para usar `mediaflow-upload-handler` correto
- ✅ Permissão de invocação configurada
- ✅ Endpoint: `/prod/upload/presigned`

---

## 📊 Testes Realizados

### Upload Pequeno (<100MB)
```bash
curl -X POST "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/presigned" \
  -H "Authorization: Bearer {jwt}" \
  -d '{"filename":"test.mp4","contentType":"video/mp4","fileSize":1000}'

# Resultado: key: "users/sergio_sena/test.mp4" ✅
```

### Upload Frontend
- ✅ Sergio: Upload funcionando
- ✅ Lid: Upload funcionando
- ✅ Multipart (>100MB): Funcionando
- ✅ Player: Reproduz corretamente

---

## 🔑 Arquivos Modificados

1. **DirectUpload.tsx**
   - Chama Lambda direto via `aws-config.ts`
   - Barra de progresso melhorada
   - Auto-adiciona `users/{user_id}/`

2. **Lambda mediaflow-upload-handler**
   - PyJWT instalado
   - Extrai `user_id` do JWT
   - Salva em `users/{user_id}/{filename}`

3. **API Gateway**
   - Integração atualizada para Lambda correto
   - Permissão de invocação adicionada

---

## 🎯 Resultado Final

✅ **Upload pequeno**: Funciona  
✅ **Multipart (>100MB)**: Funciona  
✅ **Player**: Funciona  
✅ **Arquivos salvos em**: `users/{user_id}/`  
✅ **Barra de progresso**: Visível e com percentual  

---

## 📝 Comandos Úteis

### Testar Lambda
```bash
curl -X POST "https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/upload/presigned" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"filename":"test.mp4","contentType":"video/mp4","fileSize":1000}'
```

### Deploy Lambda
```bash
cd aws-setup/lambda-functions/upload-handler
pip install PyJWT -t .
powershell Compress-Archive -Force -Path lambda_function.py,../lib/logger.py,jwt,PyJWT-2.10.1.dist-info -DestinationPath function.zip
aws lambda update-function-code --function-name mediaflow-upload-handler --zip-file fileb://function.zip
```

### Deploy Frontend
```bash
npm run build
aws s3 sync out s3://mediaflow-frontend-969430605054 --delete
aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"
```

---

## 🎉 Status: COMPLETO ✅
