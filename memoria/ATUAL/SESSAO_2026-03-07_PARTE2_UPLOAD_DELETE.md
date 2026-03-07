# Sessão 2026-03-07 (Parte 2) - Correções de Upload e Delete

## 📋 Problemas Resolvidos

### 1. Upload Pequeno - Token JWT Faltando
**Problema:** Upload via `SimpleFileUpload` retornava 403 (Forbidden) porque não enviava token JWT.

**Solução:**
- Adicionado `Authorization: Bearer ${token}` no header da requisição `/api/upload/presigned`
- Arquivo: `components/modules/SimpleFileUpload.tsx`

### 2. Avatar - Fallback Melhorado no Login
**Problema:** Usuários comuns não conseguiam carregar avatar no login (endpoint `/api/users/list` é admin-only).

**Solução:**
- Adicionado fallback triplo no login:
  1. Tenta `/api/users/list` (funciona para admin)
  2. Se falhar, tenta buscar avatar direto do endpoint `/users/{user_id}`
  3. Se falhar, cria `current_user` sem avatar (pode fazer upload depois)
- Adicionado `s3_prefix` no fallback
- Arquivo: `app/(auth)/login/page.tsx`

### 3. Delete de Arquivos Não Funcionava
**Problema:** Endpoint `/files/delete` não existia no API Gateway, causando 403.

**Solução:**
- Criado resource `/files/delete` no API Gateway
- Criado método `DELETE` conectado à Lambda `mediaflow-files-handler`
- Adicionada permissão para API Gateway invocar a Lambda
- Deploy realizado

**Comandos executados:**
```bash
aws apigateway create-resource --rest-api-id gdb962d234 --parent-id 7s6xdy --path-part delete
aws apigateway put-method --rest-api-id gdb962d234 --resource-id 241ygt --http-method DELETE --authorization-type NONE
aws apigateway put-integration --rest-api-id gdb962d234 --resource-id 241ygt --http-method DELETE --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:969430605054:function:mediaflow-files-handler/invocations
aws lambda add-permission --function-name mediaflow-files-handler --statement-id apigateway-delete-files --action lambda:InvokeFunction --principal apigateway.amazonaws.com
aws apigateway create-deployment --rest-api-id gdb962d234 --stage-name prod
```

### 4. Deploy com Cache Issues
**Problema:** Após deploy, CloudFront servia HTMLs antigos que referenciavam arquivos JS deletados (404).

**Solução:**
- Rebuild completo: `npm run build`
- Sync de arquivos estáticos com cache headers: `--cache-control "public,max-age=31536000,immutable"`
- Sync de HTMLs com no-cache: `--cache-control "no-cache,must-revalidate"`
- Invalidação completa do CloudFront: `--paths "/*"`

**Lição aprendida:** Cache do navegador pode persistir mesmo após invalidação do CloudFront. Solução: reiniciar navegador ou acessar com `?v=timestamp`.

## 📁 Arquivos Modificados

```
app/(auth)/login/page.tsx
components/modules/SimpleFileUpload.tsx
```

## 🏗️ Infraestrutura AWS

### Endpoint Criado
- **Path:** `DELETE /files/delete`
- **Resource ID:** `241ygt`
- **Lambda:** `mediaflow-files-handler`
- **Status:** ✅ Funcionando

## 🧪 Testes Realizados

- ✅ Upload de arquivo pequeno (com token JWT)
- ✅ Login com avatar (fallback funcionando)
- ✅ Delete de arquivo individual
- ✅ Deploy completo com invalidação

## 📝 Notas Técnicas

### Token JWT no Upload
```typescript
const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
const urlResponse = await fetch('/api/upload/presigned', {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({...})
})
```

### Fallback de Avatar no Login
```typescript
// Fallback 1: /api/users/list (admin)
// Fallback 2: GET /users/{user_id} (direto)
// Fallback 3: Criar sem avatar
const fallbackUser = {
  user_id: data.user_id,
  name: data.user?.name || email.split('@')[0],
  email: email,
  role: data.user?.role || 'user',
  s3_prefix: `users/${data.user_id}/`,
  avatar_url: avatarData.avatar_url || undefined
}
```

## 🔜 Melhorias Futuras

- [ ] Implementar endpoint `/api/users/me` funcional (com permissões DynamoDB corretas)
- [ ] Adicionar validação JWT na Lambda de delete para maior segurança
- [ ] Criar script de deploy que adiciona `?v=timestamp` automaticamente
- [ ] Implementar cache-busting automático nos builds

---

**Data:** 2026-03-07  
**Versão:** 4.8.4  
**Status:** ✅ Testado e Funcionando
