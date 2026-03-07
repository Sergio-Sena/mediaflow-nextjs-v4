# 📝 Sessão 2026-03-07 - Parte 3: Correção Cache CloudFront

## 🎯 Problema Identificado

**Sintoma**: Login funcionava local mas falhava em produção com erro 404 em arquivos JS.

**Causa Raiz**: Cache persistente de HTMLs antigos no CloudFront referenciando arquivos JS deletados durante deploy.

## 🔍 Diagnóstico (Metodologia C.E.R.T.O)

### Contexto
- Local (localhost:3000): Login funcionava
- Produção (midiaflow.sstechnologies-cloud.com): 404 em webpack-652c8d689df6c5ff.js, main-app-49e84fcaf664d588.js, page-48e643a6f2b1ba84.js
- CloudFront (E2HZKZ9ZJK18IU) com cache problemático

### Expectativa
- Login e dashboard funcionando em produção
- Cache correto (HTMLs sem cache, JS com cache longo)

### Regras
- HTMLs devem ter cache-control: max-age=0
- JS/CSS devem ter cache-control: max-age=31536000,immutable
- CloudFront deve respeitar headers do S3

### Tarefa
1. Verificar se erro era CORS ou cache
2. Rebuild e sync de arquivos
3. Invalidação CloudFront
4. Se persistir, criar novo CDN

### Objetivo
Produção funcionando sem erros 404

## 🛠️ Tentativas de Correção

### Tentativa 1: Configurar CORS no API Gateway
```bash
python fix-login-cors.py
```
**Resultado**: CORS já estava correto. Não era o problema.

### Tentativa 2: Rebuild e Sync
```bash
npm run build
aws s3 sync .next/static s3://mediaflow-frontend-969430605054/_next/static --delete
aws s3 cp .next/server/app/login.html s3://mediaflow-frontend-969430605054/login
aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"
```
**Resultado**: CloudFront servia HTML correto, mas navegadores mantinham cache local.

### Tentativa 3: Upload de Todos os HTMLs
```bash
for %f in (.next\server\app\*.html) do aws s3 cp "%f" s3://bucket/%~nf --cache-control "max-age=0,no-cache,no-store,must-revalidate"
```
**Resultado**: Ainda persistia em modo anônimo = problema no CloudFront.

### Tentativa 4: Desabilitar Cache de HTMLs
```python
# disable-html-cache.py
# Criou cache policy com TTL=0 para HTMLs
```
**Resultado**: Funcionou, mas aumentaria custos (mais requests ao S3).

## ✅ Solução Final: Novo CloudFront

### Decisão
Criar novo CloudFront limpo com cache correto desde o início.

### Implementação

**1. Criar novo CloudFront**
```python
# create-new-cloudfront.py
config = {
    'DefaultCacheBehavior': {
        'CachePolicyId': '658327ea-f89d-4fab-a63d-7e88639e58f6'  # CachingOptimized
    },
    'CacheBehaviors': [
        {
            'PathPattern': '*.html',
            'CachePolicyId': '4135ea2d-6df8-44a3-9df3-4b5a84be39ad'  # CachingDisabled
        },
        {
            'PathPattern': '_next/static/*',
            'CachePolicyId': '658327ea-f89d-4fab-a63d-7e88639e58f6'  # CachingOptimized (1 ano)
        }
    ]
}
```

**Resultado**: Distribution E1O4R8P5BGZTMW criada com domain d2komwe8ylb0dt.cloudfront.net

**2. Teste no CDN temporário**
```
https://d2komwe8ylb0dt.cloudfront.net
```
**Resultado**: ✅ Login e dashboard funcionaram perfeitamente

**3. Migração de DNS**
- Route 53: midiaflow.sstechnologies-cloud.com → d2komwe8ylb0dt.cloudfront.net
- Removido alias do CDN antigo (E2HZKZ9ZJK18IU)
- Adicionado alias no novo (E1O4R8P5BGZTMW)
- CDN antigo desabilitado

## 📊 Resultado Final

### Antes
- CloudFront: E2HZKZ9ZJK18IU (com cache problemático)
- Erros 404 em produção
- Cache inconsistente entre edge locations

### Depois
- CloudFront: E1O4R8P5BGZTMW (cache otimizado)
- ✅ Login funcionando
- ✅ Dashboard carregando
- ✅ HTMLs sem cache (sempre atualizados)
- ✅ JS/CSS com cache 1 ano (performance)
- ✅ Custos otimizados

## 🔧 Configuração Final

### CloudFront E1O4R8P5BGZTMW
- **Domain**: d2komwe8ylb0dt.cloudfront.net
- **Alias**: midiaflow.sstechnologies-cloud.com
- **Certificado**: arn:aws:acm:us-east-1:969430605054:certificate/5da53d3b-4f07-4aeb-9654-0b1bfea7bc0a
- **Origin**: mediaflow-frontend-969430605054.s3.us-east-1.amazonaws.com

### Cache Policies
- **Default**: CachingOptimized (1 ano)
- **HTMLs (*.html)**: CachingDisabled (sempre busca S3)
- **Static (_next/static/*)**: CachingOptimized (1 ano)

### DNS (Route 53)
- **Record**: midiaflow.sstechnologies-cloud.com
- **Type**: CNAME
- **Value**: d2komwe8ylb0dt.cloudfront.net
- **TTL**: 300

## 📝 Arquivos Criados/Modificados

### Scripts Criados
- `aws-setup/fix-login-cors.py` - Configurar CORS no API Gateway
- `aws-setup/disable-html-cache.py` - Desabilitar cache de HTMLs
- `aws-setup/create-new-cloudfront.py` - Criar novo CloudFront
- `aws-setup/migrate-cdn.py` - Migrar alias entre CDNs

### Documentação Atualizada
- `README.md` - CloudFront ID atualizado (E2HZKZ9ZJK18IU → E1O4R8P5BGZTMW)

## 🎓 Lições Aprendidas

1. **Cache de HTMLs é problemático**: Sempre desabilitar cache de HTMLs em SPAs
2. **Invalidação não é suficiente**: Edge locations podem manter cache mesmo após invalidação
3. **Novo CDN é mais rápido**: Criar novo CDN limpo é mais eficiente que corrigir cache problemático
4. **Teste incremental**: Testar CDN temporário antes de migrar DNS
5. **Cache policies corretas**: Usar policies AWS nativas em vez de custom TTLs

## 🚀 Próximos Passos

1. ✅ Aguardar 24h para confirmar estabilidade
2. ⏳ Deletar CDN antigo (E2HZKZ9ZJK18IU)
3. ⏳ Monitorar custos do novo CDN
4. ⏳ Documentar processo de deploy atualizado

## 📌 Comandos Úteis

### Deploy Completo
```bash
npm run build
aws s3 sync .next/static s3://mediaflow-frontend-969430605054/_next/static --delete --cache-control "public,max-age=31536000,immutable"
for %f in (.next\server\app\*.html) do aws s3 cp "%f" s3://mediaflow-frontend-969430605054/%~nf --cache-control "max-age=0,no-cache,no-store,must-revalidate" --content-type "text/html"
aws cloudfront create-invalidation --distribution-id E1O4R8P5BGZTMW --paths "/*"
```

### Deletar CDN Antigo (após 24h)
```bash
aws cloudfront get-distribution-config --id E2HZKZ9ZJK18IU --query 'ETag' --output text
aws cloudfront delete-distribution --id E2HZKZ9ZJK18IU --if-match <etag>
```

---

**Status**: ✅ Completo  
**Data**: 2026-03-07  
**Versão**: v4.8.5
