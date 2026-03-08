# Changelog

## 🚀 [v4.8.6] - 2026-03-08

### 🔧 Fixed
- **Delete de Arquivos**: Lambda files-handler agora verifica existência antes de deletar
- **Validação**: Todos os bugs críticos testados e funcionando em produção

### 📝 Documentation
- Adicionada documentação completa da sessão de correções
- Criado script de diagnóstico para testes futuros

---

## 🚀 [v4.8.5] - 2026-03-07

### 🔧 Fixed
- **Cache CloudFront**: Resolvido problema de cache persistente causando 404 em arquivos JS
- **Login Produção**: Corrigido erro de login em produção (funcionava local mas falhava online)
- **Dashboard Loading**: Corrigido carregamento do dashboard com arquivos JS antigos

### ⚡ Changed
- **CloudFront**: Migrado de E2HZKZ9ZJK18IU para E1O4R8P5BGZTMW
- **CDN Domain**: Atualizado de d2x90cv3rb5hoa.cloudfront.net para d2komwe8ylb0dt.cloudfront.net
- **Cache Policy**: HTMLs sem cache, JS/CSS com cache 1 ano

### 📝 Infrastructure
- Novo CloudFront com cache policies otimizadas
- CORS configurado no endpoint /auth/login do API Gateway
- DNS atualizado no Route 53

### 🗑️ Deprecated
- CloudFront E2HZKZ9ZJK18IU desabilitado (será deletado em 24h)

---

## 📋 Detalhes Técnicos

### Cache Policies Implementadas
```
Default Behavior: CachingOptimized (1 ano)
*.html: CachingDisabled (sempre atualizado)
_next/static/*: CachingOptimized (1 ano)
```

### Scripts Criados
- `aws-setup/fix-login-cors.py`
- `aws-setup/disable-html-cache.py`
- `aws-setup/create-new-cloudfront.py`
- `aws-setup/migrate-cdn.py`

### Documentação Atualizada
- `README.md` - CloudFront IDs
- `memoria/ATUAL/SESSAO_2026-03-07_PARTE3_CORRECAO_CACHE_CDN.md`

---

## 🔗 Links
- **Produção**: https://midiaflow.sstechnologies-cloud.com
- **CloudFront**: E1O4R8P5BGZTMW
- **Domain**: d2komwe8ylb0dt.cloudfront.net

---

**Versão Anterior**: v4.8.4  
**Próxima Versão**: v4.9.0
