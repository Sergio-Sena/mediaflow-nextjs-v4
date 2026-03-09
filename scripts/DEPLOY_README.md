# 🚀 Deploy Scripts - Blue/Green Strategy

## 📋 Fluxo de Deploy

```
LOCAL → GREEN (staging) → BLUE (production)
```

## 🟢 Deploy para GREEN (Staging)

```bash
scripts\deploy-green.bat
```

**O que faz:**
1. Build do Next.js
2. Sync para `s3://midiaflow-green-969430605054`
3. Pronto para testes

**URL:** http://midiaflow-green-969430605054.s3-website-us-east-1.amazonaws.com

---

## 🔵 Deploy para BLUE (Production)

```bash
scripts\deploy-blue.bat
```

**O que faz:**
1. Confirma que testou no GREEN
2. Sync para `s3://mediaflow-frontend-969430605054`
3. Invalida CloudFront cache

**URL:** https://midiaflow.sstechnologies-cloud.com

⚠️ **Aguarde 2-3 minutos** para invalidação do CloudFront completar.

---

## 🔄 Rollback de Emergência

```bash
scripts\rollback.bat
```

**O que faz:**
- Copia GREEN → BLUE
- Invalida CloudFront
- Restaura última versão estável

⚠️ **Use apenas em emergências!**

---

## ✅ Checklist de Deploy

### Antes de deployar para GREEN:
- [ ] Código testado localmente
- [ ] Build sem erros
- [ ] Funcionalidades principais testadas

### Antes de deployar para BLUE:
- [ ] Testado no GREEN
- [ ] Upload funcionando
- [ ] Delete funcionando
- [ ] Avatar funcionando
- [ ] Player funcionando
- [ ] Sem erros no console

### Após deploy para BLUE:
- [ ] Aguardar invalidação CloudFront (2-3 min)
- [ ] Verificar versão servida
- [ ] Testar funcionalidades críticas
- [ ] Monitorar por 10 minutos

---

## 🏗️ Ambientes

| Ambiente | Bucket | URL | CloudFront |
|----------|--------|-----|------------|
| **GREEN** (staging) | `midiaflow-green-969430605054` | http://midiaflow-green-969430605054.s3-website-us-east-1.amazonaws.com | ❌ |
| **BLUE** (production) | `mediaflow-frontend-969430605054` | https://midiaflow.sstechnologies-cloud.com | ✅ E1A2CZM0WKF6LX |

---

## 🐛 Troubleshooting

### Build falha
```bash
npm install
npm run build
```

### CloudFront serve versão antiga
```bash
# Verificar invalidação
aws cloudfront get-invalidation --distribution-id E1A2CZM0WKF6LX --id <INVALIDATION_ID>

# Forçar nova invalidação
aws cloudfront create-invalidation --distribution-id E1A2CZM0WKF6LX --paths "/*"
```

### Rollback não funciona
```bash
# Manual: copiar GREEN → BLUE
aws s3 sync s3://midiaflow-green-969430605054 s3://mediaflow-frontend-969430605054 --delete
```

---

## 📊 Histórico de Deploys

Manter log manual em `CHANGELOG.md`:

```markdown
## v4.9.0 - 2026-03-09
- ✅ Upload system fix
- ✅ Avatar upload/display
- ✅ Delete files fix
- Deploy: GREEN → BLUE
```
