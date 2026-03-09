# 📁 Scripts Ativos - MidiaFlow

**Data**: 2026-03-09  
**Limpeza**: 150+ scripts obsoletos movidos para `_archive/scripts-old/`

---

## 🚀 Scripts de Deploy

### `deploy-green.bat`
Deploy para ambiente de staging (GREEN)
```bash
scripts\deploy-green.bat
```

### `deploy-blue.bat`
Deploy para produção (BLUE) - requer confirmação
```bash
scripts\deploy-blue.bat
```

### `rollback.bat`
Rollback de emergência (GREEN → BLUE)
```bash
scripts\rollback.bat
```

### `backup-before-deploy.py`
Criar backup antes de deploy
```bash
python scripts\backup-before-deploy.py
```

---

## 🔧 Scripts AWS

### `aws/deploy.py`
Deploy genérico de recursos AWS

### `aws/monitoring/monitor-upload-live.py`
Monitorar uploads em tempo real

### `aws/monitoring/get-lambda-errors.py`
Buscar erros em Lambdas

### `aws/monitoring/get-multipart-errors.py`
Buscar erros em multipart uploads

---

## 🧪 Scripts de Teste

### `test-production.js`
Testar produção (login, upload, delete)
```bash
node scripts\test-production.js
```

### `test-midiaflow-production.js`
Teste completo de produção

---

## 🛠️ Scripts Utilitários

### `utils/backup-before-deploy.py`
Backup automático

### `utils/organize-project.py`
Organizar estrutura do projeto

### `utils/audit-users-vs-s3.py`
Auditar usuários vs S3

### `utils/check-dynamodb-structure.py`
Verificar estrutura DynamoDB

### `utils/map-bucket-structure.py`
Mapear estrutura dos buckets

---

## 📊 Scripts de Análise

### `measure-performance.py`
Medir performance da aplicação

### `monitor-performance.py`
Monitorar performance em tempo real

---

## 🧹 Scripts de Manutenção

### `cleanup-obsolete.bat`
Limpar scripts obsoletos (já executado)

### `sanitize-docs.py`
Sanitizar documentação

---

## ⚠️ Scripts Arquivados

**Localização**: `_archive/scripts-old/`

**Categorias arquivadas**:
- Upload específicos (kate-kuray, star, comatozze, etc)
- Check específicos (sergio, admin, etc)
- Rename/move obsoletos
- Verificação obsoletos
- Compare obsoletos
- Unify/organize obsoletos
- Find/list obsoletos
- Convert obsoletos
- Delete/cleanup obsoletos
- Fix obsoletos
- Replace obsoletos
- Scan/duplicates obsoletos
- Migrate obsoletos
- Test obsoletos
- Scripts JS obsoletos
- Scripts BAT obsoletos

**Total arquivado**: ~150 arquivos

---

## 📝 Notas

- Scripts mantidos: **~20 de 200** (90% redução)
- Critério: Uso atual ou genérico
- Scripts específicos de conteúdo foram arquivados
- Scripts de teste antigos foram arquivados
- Manter apenas ferramentas de deploy, monitoring e utils

---

**Última atualização**: 2026-03-09
