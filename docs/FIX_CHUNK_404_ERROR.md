# 🔧 Correção: Erro 404 em Chunks do Next.js

## 🐛 Problema

```
GET http://mediaflow-frontend-969430605054.s3-website-us-east-1.amazonaws.com/_next/static/chunks/874-2054d9fa2d919d20.js 
net::ERR_ABORTED 404 (Not Found)

ChunkLoadError: Loading chunk 874 failed.
```

## 🔍 Causa Raiz

**Chunks de builds diferentes misturados no S3**

1. Build local gerou: `874-2054d9fa2d919d20.js`
2. HTML referencia esse chunk
3. Mas o arquivo não existe no S3 (build anterior tinha outro hash)

### Por que aconteceu?

- O workflow usava `--delete` no `aws s3 sync`, mas isso **não garante limpeza total**
- Arquivos órfãos de builds anteriores permaneciam no bucket
- Next.js gera hashes diferentes a cada build (`874-ABC123.js` → `874-XYZ789.js`)
- HTML novo referencia chunks novos, mas S3 tem chunks velhos

## ✅ Solução Implementada

### 1. Limpeza Total do Bucket Antes do Deploy

```yaml
# .github/workflows/deploy-production.yml
- name: Clear S3 bucket (prevent stale chunks)
  run: |
    aws s3 rm s3://${{ secrets.S3_BUCKET_FRONTEND }}/ --recursive
```

**Por quê?**
- Garante que APENAS os arquivos do build atual existam
- Elimina qualquer chunk órfão de builds anteriores
- Previne incompatibilidade de hashes

### 2. Upload Apenas do `out/`

```yaml
- name: Upload build artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: out/  # Apenas out/, não .next/
```

**Por quê?**
- Next.js com `output: 'export'` gera tudo em `out/`
- `.next/` é apenas cache de build, não deve ir para produção
- Reduz tamanho do artifact e tempo de deploy

## 🚀 Como Corrigir Agora

### Opção 1: Script Automático (Recomendado)

```bash
fix-deploy.bat
```

Este script:
1. ✅ Limpa todo o bucket S3
2. ✅ Faz build limpo (remove .next e out)
3. ✅ Faz upload correto
4. ✅ Invalida CloudFront

### Opção 2: Manual

```bash
# 1. Limpar S3
aws s3 rm s3://mediaflow-frontend-969430605054/ --recursive

# 2. Build limpo
rmdir /s /q .next
rmdir /s /q out
npm run build

# 3. Upload
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --cache-control "public, max-age=31536000, immutable" --exclude "*.html" --exclude "*.json"
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --exclude "*" --include "*.html" --include "*.json" --cache-control "public, max-age=0, must-revalidate"

# 4. Invalidar CloudFront
aws cloudfront create-invalidation --distribution-id E2H9YJWVZ8YZQO --paths "/*"
```

## 🛡️ Prevenção Futura

### ✅ Workflow Corrigido

O workflow agora:
1. Limpa o bucket ANTES do upload
2. Faz upload apenas do `out/`
3. Garante consistência entre HTML e chunks

### ✅ Cache Strategy

```yaml
# Chunks JS/CSS: cache longo (imutáveis por hash)
--cache-control "public, max-age=31536000, immutable"

# HTML/JSON: sem cache (sempre busca novo)
--cache-control "public, max-age=0, must-revalidate"
```

## 📊 Checklist de Deploy

Antes de cada deploy:

- [ ] Build limpo (`rm -rf .next out`)
- [ ] Bucket S3 limpo (`aws s3 rm --recursive`)
- [ ] Upload completo do `out/`
- [ ] Invalidação do CloudFront
- [ ] Aguardar 2-3 minutos
- [ ] Testar em navegador anônimo (Ctrl+Shift+N)

## 🔍 Como Verificar se Está Correto

### 1. Verificar Chunks no S3

```bash
aws s3 ls s3://mediaflow-frontend-969430605054/_next/static/chunks/ --recursive
```

Deve listar APENAS chunks do build atual.

### 2. Verificar HTML

```bash
curl https://midiaflow.sstechnologies-cloud.com/ | grep -o "chunks/[^\"]*\.js"
```

Todos os chunks referenciados devem existir no S3.

### 3. Testar no Navegador

1. Abrir em aba anônima (Ctrl+Shift+N)
2. Abrir DevTools (F12) → Network
3. Recarregar (Ctrl+F5)
4. Verificar se todos os chunks carregam com 200 OK

## 🎯 Resultado Esperado

```
✅ Todos os chunks carregam com 200 OK
✅ Sem erros de ChunkLoadError
✅ Aplicação funciona normalmente
✅ Mesmo comportamento local e produção
```

## 📝 Notas Técnicas

### Por que Next.js gera hashes diferentes?

```javascript
// Build 1
874-2054d9fa2d919d20.js  // Hash baseado no conteúdo

// Build 2 (mesmo código, mas timestamp diferente)
874-abc123def4567890.js  // Hash diferente!
```

Next.js usa **content hashing** para cache busting. Qualquer mudança (até timestamp) gera novo hash.

### Por que `--delete` não é suficiente?

```bash
# aws s3 sync com --delete
# ❌ Só deleta arquivos que não existem no source
# ❌ Não deleta arquivos com nomes diferentes (chunks com hash diferente)

# aws s3 rm --recursive
# ✅ Deleta TUDO antes do upload
# ✅ Garante estado limpo
```

## 🔗 Referências

- [Next.js Static Export](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [AWS S3 Sync vs Rm](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html)
- [CloudFront Cache Invalidation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)

---

**Data da Correção:** 2025-01-30  
**Versão:** v4.9.1  
**Status:** ✅ Resolvido
