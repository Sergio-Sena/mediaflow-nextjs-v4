# Prompt para Próximo Chat - Mídiaflow v4.7

## Contexto do Sistema

**Mídiaflow** é uma plataforma de streaming profissional multi-usuário em produção na AWS.

- **URL Produção**: https://midiaflow.sstechnologies-cloud.com
- **Versão Atual**: v4.7.0 (Gerenciador de Pastas)
- **Status**: ✅ 100% FUNCIONAL EM PRODUÇÃO

## Arquitetura AWS

### Frontend
- **Hosting**: S3 bucket `mediaflow-frontend-969430605054` (static export Next.js)
- **CDN**: CloudFront distribution `E3ODIUY4LXU8TH`
- **SSL**: Certificado wildcard ativo
- **Build**: `npm run build` → `aws s3 sync out/ s3://mediaflow-frontend-969430605054 --delete`
- **Cache**: Invalidar com `aws cloudfront create-invalidation --distribution-id E3ODIUY4LXU8TH --paths "/*"`

### Backend
- **API Gateway**: 8 Lambda Functions (Python 3.12)
- **Storage**: 3 S3 buckets (uploads/processed/frontend)
- **Auth**: JWT com campo `user_id` (NÃO `username`)
- **Database**: DynamoDB table `mediaflow-users`
- **Região**: us-east-1

### Lambdas Principais
1. **auth-handler**: Login/JWT generation (campo `user_id` no payload)
2. **upload-handler**: Upload direto S3 para `users/{user_id}/`
3. **multipart-handler**: Upload >100MB para `users/{user_id}/`
4. **list-files**: Lista arquivos do usuário
5. **delete-file**: Deleta arquivos
6. **get-video-url**: Gera URLs assinadas
7. **create-user**: Cadastro de novos usuários
8. **folder-operations**: CRUD de pastas (POST/DELETE /folders)

## Estrutura S3 Correta

```
mediaflow-uploads/
└── users/
    ├── gabriel/          # user_id: "gabriel"
    ├── joao_silva/       # user_id: "joao_silva"
    ├── user_admin/       # user_id: "user_admin" (admin)
    ├── lid_lima/         # user_id: "lid_lima"
    └── sergio_sena/      # user_id: "sergio_sena"
```

**IMPORTANTE**: Uploads SEMPRE vão para `users/{user_id}/`, extraído do JWT payload.

## JWT Structure (CRÍTICO)

```json
{
  "user_id": "gabriel",        // ← ESTE campo (NÃO "username")
  "email": "gabriel@example.com",
  "s3_prefix": "users/gabriel/",
  "role": "user",
  "exp": 1234567890
}
```

**Lambdas devem usar**: `jwt_payload.get('user_id')` (NÃO `username`)

## Usuários DynamoDB

| user_id | email | role | s3_prefix |
|---------|-------|------|-----------|
| user_admin | admin@example.com | admin | users/user_admin/ |
| gabriel | gabriel@example.com | user | users/gabriel/ |
| joao_silva | joao@example.com | user | users/joao_silva/ |
| lid_lima | lid@example.com | user | users/lid_lima/ |
| sergio_sena | sergio@example.com | user | users/sergio_sena/ |

## Stack Tecnológico

- **Frontend**: Next.js 14.2.32 (static export), React 18, TypeScript 5.6
- **Styling**: Tailwind CSS (tema neon cyberpunk)
- **Backend**: AWS Lambda (Python 3.12), API Gateway
- **Storage**: S3 + CloudFront CDN (400+ edge locations)
- **Video**: AWS MediaConvert (H.264 1080p)
- **Auth**: JWT (sem refresh token)

## Funcionalidades Ativas

✅ Upload até 5GB (DirectUpload component)
✅ Sistema híbrido: <100MB direto, >100MB multipart
✅ Conversão automática H.264 1080p
✅ Player sequencial (Previous/Next)
✅ Navegação hierárquica por pastas
✅ Sistema multi-usuário com avatares S3
✅ Upload de avatar com preview
✅ Continue assistindo (retoma último vídeo)
✅ Thumbnails client-side (geração gratuita)
✅ Analytics em tempo real
✅ Cleanup automático de órfãos
✅ Busca global em todas as pastas
✅ Mobile-friendly (gestos touch)
✅ **Tab Pastas** (gerenciador visual hierárquico)
✅ **Upload consolidado** (botão único multipart + normal)
✅ **Busca inteligente** (encontra com underscore)
✅ **Player otimizado** (auto-hide + autoplay)

## Estrutura do Projeto

```
drive-online-clean-NextJs/
├── app/
│   ├── (auth)/              # Login/Register
│   ├── admin/               # Painel admin (apenas user_admin)
│   │   └── dashboard/
│   └── dashboard/           # Dashboard principal (4 tabs)
│       └── page.tsx         # files, folders, upload, analytics
├── components/
│   ├── modules/
│   │   ├── DirectUpload.tsx       # Upload (botão consolidado)
│   │   ├── MultipartUpload.tsx    # Upload >100MB (autoStart)
│   │   ├── FileList.tsx           # Lista (busca melhorada)
│   │   ├── VideoPlayer.tsx        # Player (auto-hide + autoplay)
│   │   ├── FolderManagerV2.tsx    # Gerenciador pastas (NOVO)
│   │   └── Analytics.tsx          # Métricas
│   ├── AvatarUpload.tsx     # Upload de avatar
│   └── UserCard.tsx         # Card de usuário
├── aws-setup/
│   └── lambda-functions/    # 8 Lambdas Python
│       └── folder-operations/  # CRUD pastas (NOVO)
├── scripts/
│   ├── s3-operations/       # Scripts S3
│   └── testing/             # Scripts de teste
└── memoria/
    ├── PROMPT_CONSOLIDADO.md
    ├── METODO_DESENVOLVIMENTO.md
    ├── FIX_PATH_DUPLICADO.md
    ├── CHANGELOG_v4.7.md          # Novidades v4.7 (NOVO)
    └── FOLDER_MANAGER_V2.md       # Docs técnica (NOVO)
```

## Dashboard Tabs (4 tabs)

1. **📁 Biblioteca**: FileList component (navegação por pastas)
2. **🗂️ Pastas**: FolderManagerV2 component (gerenciador visual)
3. **📤 Upload**: DirectUpload component (botão consolidado)
4. **📊 Analytics**: Métricas em tempo real

## Deploy Workflow

```bash
# 1. Build frontend
npm run build

# 2. Deploy para S3
aws s3 sync out/ s3://mediaflow-frontend-969430605054 --delete

# 3. Invalidar CloudFront
aws cloudfront create-invalidation --distribution-id E3ODIUY4LXU8TH --paths "/*"

# 4. Deploy Lambda (exemplo)
cd aws-setup/lambda-functions/upload-handler
zip -r lambda.zip .
aws lambda update-function-code --function-name upload-handler --zip-file fileb://lambda.zip
```

## Problemas Conhecidos e Soluções

### 1. Cache CloudFront Persistente
**Problema**: Mudanças não aparecem após deploy
**Solução**: 
- Invalidar cache: `aws cloudfront create-invalidation --distribution-id E3ODIUY4LXU8TH --paths "/*"`
- Hard refresh no browser: `Ctrl+Shift+R` (Windows) ou `Cmd+Shift+R` (Mac)
- Aguardar 5-10 minutos para propagação global

### 2. Path Duplicado (RESOLVIDO v4.6.1)
**Problema**: Arquivos iam para `users/anonymous/users/user_admin/`
**Causa**: Lambdas buscavam `username` ao invés de `user_id` no JWT
**Solução**: Corrigido em upload-handler e multipart-handler

### 3. Usuário Vê Conteúdo de Outros
**Causa**: Lambda list-files não filtra por `s3_prefix`
**Solução**: Adicionar filtro `Prefix=user['s3_prefix']` no `s3.list_objects_v2()`

## Padrões de Código

- **TypeScript**: Tipagem forte, interfaces explícitas
- **React**: Functional components, hooks
- **Naming**: camelCase (JS/TS), snake_case (Python)
- **Imports**: Absolutos quando possível
- **Error Handling**: Try-catch com logs detalhados
- **Comments**: Apenas quando necessário (código auto-explicativo)

## Comandos Úteis

```bash
# Desenvolvimento
npm run dev                  # Localhost:3000
npm run build               # Build produção
npm run lint                # ESLint

# AWS CLI
aws s3 ls s3://mediaflow-uploads/users/ --recursive --human-readable --summarize
aws lambda list-functions --query 'Functions[?starts_with(FunctionName, `mediaflow`)].FunctionName'
aws cloudfront get-invalidation --distribution-id E3ODIUY4LXU8TH --id <INVALIDATION_ID>

# Scripts S3
node scripts/s3-operations/analyze-structure.js
node scripts/s3-operations/cleanup-anonymous.js
```

## Credenciais e Acesso

- **Login Admin**: Veja README.md (credenciais redacted)
- **AWS Region**: us-east-1
- **DynamoDB Table**: mediaflow-users
- **S3 Buckets**: mediaflow-uploads, mediaflow-processed, mediaflow-frontend-969430605054

## Próximos Passos Sugeridos (v4.8)

- [ ] Renomear pastas
- [ ] Mover arquivos entre pastas
- [ ] DynamoDB para cache de metadados
- [ ] Editar usuários existentes (admin)
- [ ] OAuth Google login
- [ ] PWA offline support

## Documentação Completa

- **README.md**: Visão geral e setup
- **memoria/PROMPT_CONSOLIDADO.md**: Histórico completo
- **memoria/METODO_DESENVOLVIMENTO.md**: Metodologia C.E.R.T.O
- **memoria/FIX_PATH_DUPLICADO.md**: Hotfix v4.6.1
- **memoria/CHANGELOG_v4.7.md**: Novidades v4.7
- **memoria/FOLDER_MANAGER_V2.md**: Docs técnica gerenciador

---

## Instruções para o Próximo Chat

1. **Leia este arquivo primeiro** para entender o contexto completo
2. **Sempre use `user_id`** do JWT (nunca `username`)
3. **Teste localmente** antes de deploy em produção
4. **Invalide CloudFront** após cada deploy frontend
5. **Documente mudanças** em memoria/ para continuidade
6. **Siga padrões** de código e nomenclatura existentes
7. **Priorize segurança**: Validação de permissões, sanitização de inputs

**Sistema 100% funcional. Qualquer mudança deve manter compatibilidade com arquitetura existente.**

🎬 **Mídiaflow v4.7** - Sistema de Streaming Profissional Multi-Usuário
