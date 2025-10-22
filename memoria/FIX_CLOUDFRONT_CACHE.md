# 🔧 Fix CloudFront Cache - v4.7

## 🐛 Problema Identificado

**Sintoma:**
- Deploy realizado no S3
- Invalidação executada
- Versão nova NÃO aparecia no domínio
- Celular mostrava versão nova, PC mostrava antiga
- S3 direto funcionava, CloudFront não

**Causa Raiz:**
Estávamos invalidando o CloudFront **ERRADO**!

```
❌ Invalidando: E3ODIUY4LXU8TH (não usado)
✅ Correto:      E2HZKZ9ZJK18IU (domínio aponta para este)
```

## 🔍 Diagnóstico

### 1. Verificar qual CloudFront o domínio usa:
```bash
nslookup midiaflow.sstechnologies-cloud.com
# Resultado: d2x90cv3rb5hoa.cloudfront.net
```

### 2. Listar todas as distribuições:
```bash
aws cloudfront list-distributions --query "DistributionList.Items[*].[Id,DomainName,Aliases.Items[0]]" --output table
```

**Resultado:**
```
E2HZKZ9ZJK18IU | d2x90cv3rb5hoa.cloudfront.net | midiaflow.sstechnologies-cloud.com ✅
E3ODIUY4LXU8TH | d2ixahsnqs7kxv.cloudfront.net | None ❌
```

### 3. Verificar origem do CloudFront correto:
```bash
aws cloudfront get-distribution-config --id E2HZKZ9ZJK18IU
```

**Configuração encontrada:**
- ✅ 3 origens: `api-origin`, `media-origin`, `frontend-origin`
- ✅ DefaultCacheBehavior → `frontend-origin`
- ✅ `frontend-origin` → `mediaflow-frontend-969430605054.s3-website-us-east-1.amazonaws.com`
- ✅ Domínio: `midiaflow.sstechnologies-cloud.com`
- ✅ SSL: Certificado wildcard configurado

## ✅ Solução Aplicada

### 1. Invalidação no CloudFront correto:
```bash
aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"
```

### 2. Desabilitar cache temporariamente (TTL = 0):
```python
# Script: disable-cache-correct-cdn.py
config['DefaultCacheBehavior']['MinTTL'] = 0
config['DefaultCacheBehavior']['DefaultTTL'] = 0
config['DefaultCacheBehavior']['MaxTTL'] = 0
```

### 3. Aguardar 5-10 minutos para propagação

### 4. Reativar cache (performance):
```python
# Script: enable-cache-correct-cdn.py
config['DefaultCacheBehavior']['MinTTL'] = 0
config['DefaultCacheBehavior']['DefaultTTL'] = 86400  # 1 dia
config['DefaultCacheBehavior']['MaxTTL'] = 31536000  # 1 ano
```

## 📝 Scripts Criados

### `aws-setup/disable-cache-correct-cdn.py`
Desabilita cache do CloudFront E2HZKZ9ZJK18IU (TTL = 0)

### `aws-setup/enable-cache-correct-cdn.py`
Reativa cache com valores otimizados (1 dia default)

### `aws-setup/fix-cloudfront-origin.py`
Script para atualizar origem (não foi necessário usar)

## 🎯 Workflow de Deploy Correto

### Deploy padrão (com cache):
```bash
# 1. Build
npm run build

# 2. Deploy S3
aws s3 sync out/ s3://mediaflow-frontend-969430605054 --delete

# 3. Invalidar CloudFront CORRETO
aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"

# 4. Aguardar 2-5 minutos
```

### Deploy urgente (sem cache):
```bash
# 1. Build + Deploy S3 (igual acima)

# 2. Desabilitar cache
python aws-setup/disable-cache-correct-cdn.py

# 3. Aguardar 5-10 minutos

# 4. Reativar cache
python aws-setup/enable-cache-correct-cdn.py
```

## 📊 Métricas

**Antes do fix:**
- ❌ Deploy não aparecia
- ❌ Invalidação ineficaz
- ❌ Confusão entre múltiplos CloudFronts

**Depois do fix:**
- ✅ Deploy aparece em 5-10 min
- ✅ Invalidação funciona
- ✅ CloudFront correto identificado
- ✅ Cache otimizado (1 dia)

## 🔮 Prevenção Futura

### Atualizar README com CloudFront correto:
```markdown
CloudFront ID: E2HZKZ9ZJK18IU
Domain: d2x90cv3rb5hoa.cloudfront.net
Alias: midiaflow.sstechnologies-cloud.com
```

### Criar alias no script de deploy:
```bash
# .bashrc ou .zshrc
alias deploy-midiaflow='npm run build && aws s3 sync out/ s3://mediaflow-frontend-969430605054 --delete && aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"'
```

### CI/CD (v4.8):
Automatizar deploy com CloudFront ID correto no GitHub Actions

## 🎓 Lições Aprendidas

1. **Sempre verificar qual CloudFront o domínio usa** (`nslookup`)
2. **Listar todas as distribuições** antes de invalidar
3. **Testar S3 direto** para isolar problema (CloudFront vs S3)
4. **Cache em múltiplas camadas**: CloudFront edge + navegador local
5. **Celular vs PC**: Diferentes edge locations podem ter cache diferente

## ✅ Status Final

- ✅ v4.7 deployado e funcionando
- ✅ CloudFront correto identificado (E2HZKZ9ZJK18IU)
- ✅ Cache reativado (performance máxima)
- ✅ Scripts criados para futuras emergências
- ✅ Documentação completa

---

**Data:** 21/01/2025 23:50 BRT  
**Versão:** v4.7.0  
**CloudFront:** E2HZKZ9ZJK18IU  
**Status:** ✅ RESOLVIDO
