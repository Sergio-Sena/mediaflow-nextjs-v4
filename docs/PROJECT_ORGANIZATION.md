# 🗂️ Organização do Projeto - Mídiaflow

## 📋 Estrutura Atual vs Recomendada

### ✅ Estrutura Atual (Boa)

```
drive-online-clean-NextJs/
├── app/                    # ✅ Next.js 14 App Router
├── components/             # ✅ Componentes React
│   ├── modules/           # ✅ Componentes de funcionalidade
│   ├── ui/                # ✅ Componentes de UI
│   └── upload/            # ✅ Componentes de upload
├── lib/                    # ✅ Utilitários e clientes
├── types/                  # ✅ TypeScript types
├── public/                 # ✅ Assets estáticos
├── docs/                   # ✅ Documentação técnica
├── memoria/                # ✅ Documentação de desenvolvimento
└── content/                # ✅ Conteúdo markdown
```

### ⚠️ Áreas que Precisam Organização

```
drive-online-clean-NextJs/
├── scripts/                # ⚠️ 200+ arquivos desorganizados
├── aws-setup/              # ⚠️ Scripts de setup misturados
├── _archive/               # ✅ Arquivos arquivados (OK)
├── temp/                   # ⚠️ Pasta temporária vazia
└── *.py, *.js (raiz)      # ⚠️ Scripts soltos na raiz
```

---

## 🎯 Plano de Organização

### 1. Scripts (Prioridade Alta)

#### Estrutura Proposta
```
scripts/
├── aws/
│   ├── deploy/           # Scripts de deploy
│   ├── setup/            # Scripts de configuração inicial
│   ├── maintenance/      # Scripts de manutenção
│   └── monitoring/       # Scripts de monitoramento
├── database/
│   ├── migrations/       # Migrações de dados
│   ├── cleanup/          # Limpeza de dados
│   └── backup/           # Backup e restore
├── media/
│   ├── upload/           # Scripts de upload em massa
│   ├── conversion/       # Scripts de conversão
│   └── organization/     # Organização de arquivos
├── testing/              # Scripts de teste
├── utils/                # Utilitários gerais
└── README.md             # Documentação dos scripts
```

#### Categorização dos Scripts Atuais

**Deploy e Setup (aws/deploy/)**
- deploy-*.py
- setup-*.py
- configure-*.py
- create-*.py
- enable-*.py
- fix-*.py

**Manutenção (aws/maintenance/)**
- cleanup-*.py
- delete-*.py
- remove-*.py
- update-*.py
- invalidate-*.py

**Monitoramento (aws/monitoring/)**
- monitor-*.py
- check-*.py
- verify-*.py
- test-*.py
- list-*.py

**Upload e Mídia (media/upload/)**
- upload-*.py
- move-*.py
- copy-*.py
- sync-*.py

**Conversão (media/conversion/)**
- convert-*.py
- remux-*.py
- replace-*.py

**Organização (media/organization/)**
- organize-*.py
- sanitize-*.py
- unify-*.py

**Duplicados e Limpeza (database/cleanup/)**
- find-duplicates-*.py
- scan-duplicates-*.py
- delete-duplicates-*.py

**Testes (testing/)**
- test-*.py
- test-*.js

### 2. AWS Setup (Prioridade Média)

#### Estrutura Proposta
```
aws-setup/
├── lambda-functions/     # ✅ Já organizado
├── cloudfront/
│   ├── configs/          # Configurações CloudFront
│   └── scripts/          # Scripts CloudFront
├── api-gateway/
│   └── scripts/          # Scripts API Gateway
├── s3/
│   ├── configs/          # Configurações S3
│   └── scripts/          # Scripts S3
├── mediaconvert/
│   └── scripts/          # Scripts MediaConvert
├── dns/
│   └── scripts/          # Scripts DNS/Route53
└── README.md             # Documentação de setup
```

### 3. Raiz do Projeto (Prioridade Alta)

#### Arquivos a Mover/Organizar

**Mover para scripts/**
- `get-lambda-errors.py` → `scripts/aws/monitoring/`
- `get-multipart-errors.py` → `scripts/aws/monitoring/`
- `monitor-upload-live.py` → `scripts/aws/monitoring/`
- `move_files.py` → `scripts/utils/`
- `upload_and_rename.py` → `scripts/media/upload/`
- `organize-*.py` → `scripts/utils/`
- `sanitize-*.py` → `scripts/utils/`
- `remove-codes.py` → `scripts/utils/`

**Mover para docs/**
- `DEPLOY_FINAL.md` → `docs/`
- `DEPLOY_SUMMARY.md` → `docs/`
- `MANUAL_DEPLOY_SUCCESS.md` → `docs/`
- `ROLLBACK_GUIDE.md` → `docs/`
- `SANITIZACAO_COMPLETA.md` → `docs/`

**Manter na Raiz (Arquivos de Configuração)**
- ✅ `package.json`
- ✅ `tsconfig.json`
- ✅ `next.config.js`
- ✅ `tailwind.config.js`
- ✅ `postcss.config.js`
- ✅ `.gitignore`
- ✅ `.env.example`
- ✅ `README.md`
- ✅ `CHANGELOG.md`
- ✅ `vercel.json`

**Remover/Arquivar**
- `dashboard-s3.html` → `_archive/`
- `test-payload.json` → `_archive/`
- `backup-view-handler-config.json` → `_archive/`
- `next.config.aws.js` → `_archive/` (se não usado)

### 4. Temp (Prioridade Baixa)

```
temp/
└── .gitkeep  # Manter pasta vazia no git
```

Adicionar ao `.gitignore`:
```
temp/*
!temp/.gitkeep
```

---

## 📝 .gitignore Recomendado

```gitignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Next.js
.next/
out/
build/
dist/

# Production
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Vercel
.vercel/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary
temp/*
!temp/.gitkeep

# Archives (opcional - manter no git ou não)
_archive/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# AWS
.aws/

# Sensitive
*.pem
*.key
secrets/
```

---

## 🚀 Script de Organização Automática

Criar `scripts/organize-project.py`:

```python
#!/usr/bin/env python3
"""
Script para organizar automaticamente o projeto Mídiaflow
"""

import os
import shutil
from pathlib import Path

# Mapeamento de arquivos para destinos
MAPPINGS = {
    'scripts/aws/monitoring/': [
        'get-lambda-errors.py',
        'get-multipart-errors.py',
        'monitor-upload-live.py',
    ],
    'scripts/utils/': [
        'move_files.py',
        'organize-for-performance.py',
        'organize-now.py',
        'organize-project-v2.py',
        'sanitize-and-clean.py',
        'remove-codes.py',
    ],
    'scripts/media/upload/': [
        'upload_and_rename.py',
    ],
    'docs/': [
        'DEPLOY_FINAL.md',
        'DEPLOY_SUMMARY.md',
        'MANUAL_DEPLOY_SUCCESS.md',
        'ROLLBACK_GUIDE.md',
        'SANITIZACAO_COMPLETA.md',
    ],
    '_archive/old-configs/': [
        'dashboard-s3.html',
        'test-payload.json',
        'backup-view-handler-config.json',
    ],
}

def organize():
    root = Path.cwd()
    
    for dest_dir, files in MAPPINGS.items():
        dest_path = root / dest_dir
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            src = root / file
            if src.exists():
                dst = dest_path / file
                print(f"Moving {file} -> {dest_dir}")
                shutil.move(str(src), str(dst))
            else:
                print(f"⚠️  {file} not found")
    
    print("✅ Organization complete!")

if __name__ == '__main__':
    organize()
```

---

## 📚 README.md Atualizado (Raiz)

Criar estrutura clara:

```markdown
# 🎬 Mídiaflow - Plataforma de Hospedagem de Vídeos

## 📁 Estrutura do Projeto

- `app/` - Next.js 14 App Router
- `components/` - Componentes React
- `lib/` - Utilitários e clientes
- `docs/` - Documentação técnica
- `memoria/` - Documentação de desenvolvimento
- `scripts/` - Scripts de automação
- `aws-setup/` - Configuração AWS

## 🚀 Quick Start

[... instruções de instalação ...]

## 📖 Documentação

- [Documentação Técnica](./docs/)
- [Memória de Desenvolvimento](./memoria/)
- [Changelog](./CHANGELOG.md)

## 🛠️ Scripts Úteis

Ver [scripts/README.md](./scripts/README.md)
```

---

## ✅ Checklist de Organização

### Fase 1: Preparação
- [x] Criar documentação de organização
- [ ] Criar script de organização automática
- [ ] Backup do projeto atual
- [ ] Revisar .gitignore

### Fase 2: Execução
- [ ] Executar script de organização
- [ ] Mover arquivos manualmente (se necessário)
- [ ] Atualizar imports quebrados
- [ ] Testar build do projeto

### Fase 3: Documentação
- [ ] Atualizar README.md
- [ ] Criar scripts/README.md
- [ ] Atualizar docs/
- [ ] Commit das mudanças

### Fase 4: Validação
- [ ] Build sem erros
- [ ] Testes passando
- [ ] Deploy de teste
- [ ] Validação em produção

---

## 🎯 Benefícios da Organização

### Desenvolvimento
- ✅ Encontrar arquivos rapidamente
- ✅ Entender estrutura do projeto
- ✅ Onboarding de novos devs mais fácil

### Manutenção
- ✅ Scripts organizados por categoria
- ✅ Documentação centralizada
- ✅ Menos arquivos na raiz

### Deploy
- ✅ CI/CD mais limpo
- ✅ Build mais rápido
- ✅ Menos arquivos desnecessários

---

**Criado por:** Amazon Q  
**Data:** 31/01/2025  
**Versão:** 1.0
