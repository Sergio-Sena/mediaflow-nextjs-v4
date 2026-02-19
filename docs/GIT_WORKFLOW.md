# 🔄 Fluxo de Desenvolvimento - Mídiaflow

## 🌳 Branches

### `main` - Produção
- ✅ Deploy automático via CI/CD
- ✅ Código estável e testado
- ⚠️ **NUNCA commitar direto aqui!**

### `develop` - Staging/Testes
- ✅ Ambiente de testes
- ✅ Integração de features
- ✅ Testes antes de produção

### `feature/*` - Desenvolvimento
- ✅ Novas funcionalidades
- ✅ Desenvolvimento local
- ✅ Experimentos

---

## 📋 Fluxo de Trabalho

### 1️⃣ Criar Feature
```bash
# Partir de develop
git checkout develop
git pull origin develop

# Criar branch de feature
git checkout -b feature/nome-da-funcionalidade
```

### 2️⃣ Desenvolver Localmente
```bash
# Fazer alterações
npm run dev

# Testar localmente
npm run build
npm start

# Commitar
git add .
git commit -m "feat: Descrição da funcionalidade"
```

### 3️⃣ Enviar para Develop (Testes)
```bash
# Push da feature
git push origin feature/nome-da-funcionalidade

# Criar Pull Request no GitHub
# feature/nome-da-funcionalidade → develop

# Após aprovação, merge para develop
git checkout develop
git pull origin develop
```

### 4️⃣ Deploy para Produção
```bash
# Criar Pull Request no GitHub
# develop → main

# Após aprovação e merge
# CI/CD dispara automaticamente! 🚀
```

---

## 🚀 CI/CD Automático

### Trigger: Push para `main`
1. ✅ Build Next.js
2. ✅ Upload artifacts
3. ✅ Deploy S3
4. ✅ Invalidate CloudFront
5. ✅ Site atualizado!

**Tempo:** ~3-5 minutos

---

## 🆘 Hotfix Urgente

```bash
# Partir de main
git checkout main
git pull origin main

# Criar hotfix
git checkout -b hotfix/correcao-urgente

# Fazer correção
git add .
git commit -m "fix: Correção urgente"

# Push direto para main (exceção!)
git checkout main
git merge hotfix/correcao-urgente
git push origin main

# CI/CD dispara automaticamente
```

---

## 📝 Convenção de Commits

```
feat: Nova funcionalidade
fix: Correção de bug
docs: Documentação
style: Formatação
refactor: Refatoração
test: Testes
chore: Manutenção
ci: CI/CD
perf: Performance
```

---

## ✅ Checklist Antes de Merge para Main

- [ ] Testado localmente
- [ ] Testado em develop
- [ ] Build sem erros
- [ ] Sem console.log/debugs
- [ ] Documentação atualizada
- [ ] CHANGELOG.md atualizado

---

## 🔒 Proteção de Branches

**Recomendado configurar no GitHub:**

Settings → Branches → Branch protection rules

**Para `main`:**
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date

---

**Versão:** 4.8.5  
**Última atualização:** 01/02/2025
