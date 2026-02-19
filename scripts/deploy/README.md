# 🚀 Scripts de Deploy Manual

## ⚠️ Quando Usar

**Use deploy manual APENAS em casos de emergência:**

1. **CI/CD quebrado** - GitHub Actions fora do ar
2. **Hotfix urgente** - Não pode esperar pipeline completa
3. **Rollback emergencial** - Reverter versão rapidamente
4. **Teste local** - Deploy de branch não commitada

## 📋 Deploy Normal (Recomendado)

```bash
# Push para main → Deploy automático via GitHub Actions
git push origin main
```

## 🆘 Deploy Manual (Emergência)

### Windows

```bash
cd scripts/deploy
deploy-production.bat
```

### Pré-requisitos

- AWS CLI configurado
- Credenciais com permissões S3 + CloudFront
- Build gerado (`npm run build`)

## 📊 O que o script faz

1. Sync arquivos estáticos para S3 (cache longo)
2. Sync HTML para S3 (sem cache)
3. Invalida cache do CloudFront
4. Verifica URL de produção

## ⏱️ Tempo estimado

- Build: ~3 minutos
- Upload S3: ~1 minuto
- Invalidação CloudFront: ~2-5 minutos
- **Total: ~6-9 minutos**

## 🔒 Segurança

- Script usa credenciais AWS locais
- Não commitar credenciais no código
- Usar IAM roles com permissões mínimas

## 📞 Suporte

Se precisar usar deploy manual frequentemente, algo está errado com CI/CD.

**Contate o time DevOps.**
