# 🗂️ Infraestrutura de Buckets S3 - Mediaflow

**Data:** 2025-01-31  
**Região:** us-east-1  
**Account ID:** 969430605054

---

## 📦 Buckets Existentes (3 Total)

### 1. **mediaflow-frontend-969430605054** 
**Função:** Hospedagem do frontend (Next.js estático)  
**Tamanho:** 4.12 MB  
**Objetos:** 89 arquivos  
**CloudFront:** E2HZKZ9ZJK18IU  
**Domínio:** midiaflow.sstechnologies-cloud.com

**Estrutura:**
```
/
├── _next/              # Build Next.js
├── 2fa/                # Página 2FA
├── admin/              # Painel admin
├── dashboard/          # Dashboard usuário
├── login/              # Login
├── register/           # Registro
├── docs/               # Documentação
├── pricing/            # Preços
├── termos/             # Termos
├── privacidade/        # Privacidade
└── sla/                # SLA
```

**Uso:** Deploy automático via GitHub Actions

---

### 2. **mediaflow-uploads-969430605054**
**Função:** Armazenamento de arquivos dos usuários  
**Tamanho:** ~109 GB (106.5 GB)  
**Objetos:** 1000+ arquivos  
**Acesso:** Privado (presigned URLs)

**Estrutura:**
```
/
├── avatars/            # Avatares públicos
│   ├── avatar_sergio_sena.jpeg
│   ├── avatar_lid_lima.jpg
│   └── avatar_user_admin.png
├── users/              # Arquivos privados por usuário
│   ├── sergio_sena/    # 1000 arquivos, 71 GB
│   │   ├── Category/
│   │   │   └── FolderA/  (76 vídeos)
│   │   └── [outros arquivos]
│   ├── lid_lima/       # 9 arquivos, 28 GB
│   │   ├── Folder1/ (3 vídeos)
│   │   ├── Folder2/ (2 vídeos)
│   │   └── [outros arquivos]
│   └── gabriel/        # Vazio (sem uploads)
└── public/             # Área pública (novo)
    ├── videos/
    ├── images/
    ├── documents/
    └── thumbnails/
```

**Tipos de Arquivo:**
- Vídeos: MP4, WebM, MOV, AVI, MKV
- Imagens: JPG, PNG, GIF, WebP
- Documentos: PDF, DOC, DOCX, TXT, XLSX
- Outros: CSV, PPTX

**Observação:** Contém 109 GB de dados. Verificar se pasta `sergio/` é duplicada de `users/sergio_sena/`

---

### 3. **midiaflow-backups-969430605054**
**Função:** Backups do frontend  
**Tamanho:** 3.75 MB  
**Objetos:** 59 arquivos  
**Último Backup:** 2025-11-11

**Estrutura:**
```
/backups/
└── 20251111_132637/    # Backup do frontend
    ├── _next/
    ├── 2fa/
    ├── admin/
    └── [outros arquivos]
```

**Observação:** Apenas 1 backup antigo. Considerar lifecycle policy para backups automáticos.

---

## 🎯 Resumo de Uso

| Bucket | Função | Tamanho | Status | Custo/Mês Estimado |
|--------|--------|---------|--------|-------------------|
| **frontend** | Site estático | 4 MB | ✅ Ativo | $0.01 |
| **uploads** | Arquivos usuários | 99 GB | ✅ Ativo | $2.28 |
| **backups** | Backups frontend | 4 MB | ⚠️ Desatualizado | $0.01 |
| **TOTAL** | | **~99 GB** | | **~$2.30/mês** |

---

## 🔧 Ações Realizadas

### ✅ Concluído (2025-01-31)
1. ✅ **Pasta sergio/ migrada** para `users/sergio_sena/` (13 arquivos)
2. ✅ **Pastas organizadas** em estrutura hierárquica (76 vídeos)
3. ✅ **Arquivos movidos** para raiz de `users/lid_lima/` (5 arquivos)
4. ✅ **Bucket processed deletado** (estava vazio)
5. ✅ **Estrutura public/ criada** para área pública multi-mídia

### Prioridade MÉDIA
6. ⚠️ **Tags:** Adicionar tags de custo/ambiente em todos os buckets
7. ⚠️ **Monitoramento:** CloudWatch para alertas de custo
8. ⚠️ **Lifecycle policy:** Configurar backup automático do frontend

### Prioridade BAIXA
7. 📝 **Organizar uploads:** Considerar subpastas por tipo (videos/, images/, docs/)
8. 📝 **Compressão:** Habilitar compressão automática de imagens

---

## 🚀 Para Área Pública Multi-Mídia

**Opção 1: Usar bucket existente (RECOMENDADO)**
- Criar pasta `public/` dentro de `mediaflow-uploads-969430605054`
- Estrutura: `public/{mediaId}/file.ext`
- Vantagem: Simplicidade, sem custo adicional
- Desvantagem: Mistura público/privado

**Opção 2: Criar novo bucket**
- Nome: `mediaflow-public-969430605054`
- Apenas conteúdo público
- Vantagem: Separação clara, políticas diferentes
- Desvantagem: Mais um bucket para gerenciar

**Decisão:** Usar Opção 1 (pasta `public/` no bucket uploads)

---

## 📊 Estrutura Proposta para Área Pública

```
mediaflow-uploads-969430605054/
├── avatars/              # Existente
├── users/                # Existente (privado)
└── public/               # NOVO (público)
    ├── videos/
    │   └── {mediaId}.mp4
    ├── images/
    │   └── {mediaId}.jpg
    ├── documents/
    │   └── {mediaId}.pdf
    └── thumbnails/
        └── {mediaId}.jpg
```

**Acesso:**
- `users/*` → Presigned URLs (privado)
- `public/*` → Presigned URLs com TTL longo (24h)
- `avatars/*` → Público direto

---

**Documento criado por:** Amazon Q  
**Última atualização:** 2025-01-31  
**Status:** ✅ Infraestrutura organizada e pronta para área pública
