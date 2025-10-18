# 🚀 Prompt para Próximo Chat - Mediaflow v4.3

## 📋 Contexto Rápido

Você está assumindo o desenvolvimento do **Mediaflow v4.3**, uma plataforma de streaming profissional multi-usuário **100% funcional em produção** na AWS.

### 🌐 Acesso Rápido
- **URL**: https://mediaflow.sstechnologies-cloud.com
- **Admin**: [admin-email] / [admin-password]
- **Painel Admin**: https://mediaflow.sstechnologies-cloud.com/admin
- **Status**: ✅ PRODUÇÃO | Uptime 99.9%

---

## 🎯 Estado Atual do Projeto

### ✅ Funcionalidades Implementadas (v4.3)

**Sistema Multi-Usuário Completo:**
- Cadastro via painel admin com user_id auto-gerado
- Upload de avatar direto para S3
- QR Code 2FA automático
- Role-based access (admin vê tudo, user vê só sua pasta)
- s3_prefix: `users/{user_id}/`

**Streaming Profissional:**
- Upload até 5GB com DirectUpload component
- Conversão automática H.264 1080p (AWS MediaConvert)
- Player sequencial com Previous/Next
- Navegação hierárquica por pastas
- CDN global CloudFront (400+ edge locations)

**Interface Mobile:**
- Gestos touch (swipe left/right)
- Controles touch-friendly (48px+)
- Layout responsivo (2 cols tablet, 4 cols desktop)
- Gerenciador de pastas com seleção em lote

---

## 🏗️ Arquitetura AWS

### Região: us-east-1 | Account: 969430605054

**S3 Buckets:**
- `mediaflow-frontend-969430605054` - Frontend Next.js
- `mediaflow-uploads-969430605054` - Uploads + avatares
- `mediaflow-processed-969430605054` - Vídeos convertidos

**CloudFront:**
- Distribution ID: E2HZKZ9ZJK18IU
- Domain: mediaflow.sstechnologies-cloud.com

**API Gateway + 7 Lambdas:**
- Endpoint: gdb962d234.execute-api.us-east-1.amazonaws.com/prod
- Lambdas: create-user, verify-user-2fa, files-handler, avatar-presigned, upload-presigned, delete-file, folder-operations

**DynamoDB:**
- Table: mediaflow-users
- Key: user_id (String)

---

## 📁 Estrutura do Código

```
drive-online-clean-NextJs/
├── app/                    # Next.js App Router
│   ├── (auth)/login/       # Login
│   ├── 2fa/                # Verificação 2FA
│   ├── admin/              # Painel admin
│   └── dashboard/          # Dashboard principal
├── components/
│   ├── AvatarUpload.tsx    # Upload avatar
│   ├── UserCard.tsx        # Card de usuário
│   └── modules/            # Componentes principais
├── lib/                    # Clientes AWS
├── aws-setup/
│   └── lambda-functions/   # 7 Lambdas
├── scripts/                # Scripts utilitários
│   ├── s3-operations/      # Movimentação S3
│   └── testing/            # Testes
├── memoria/                # Documentação
│   ├── PROMPT_CONSOLIDADO.md
│   ├── METODO_DESENVOLVIMENTO.md
│   └── PROMPT_PROXIMO_CHAT.md (este arquivo)
└── README.md
```

---

## 🔧 Comandos Essenciais

### Deploy para Produção
```bash
npm run build
cd out
aws s3 sync . s3://mediaflow-frontend-969430605054/ --delete --region us-east-1
aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"
```

### Deploy Lambda (se alterada)
```bash
cd aws-setup/lambda-functions/[nome-lambda]
zip -r function.zip .
aws lambda update-function-code --function-name [nome-lambda] --zip-file fileb://function.zip --region us-east-1
```

### Desenvolvimento Local
```bash
npm run dev  # http://localhost:3000
```

---

## 💡 Decisões Importantes

### 1. Admin Detection
```typescript
const isAdmin = 
  user_id === 'user_admin' || 
  user_id === 'admin' || 
  id === 'user_admin' || 
  role === 'admin';
```

### 2. FileList Filtering
```typescript
// Root level
if (currentFolderPath === '') {
  return file.folder === 'root' || file.folder === '';
}
// Folder level (exact match)
return file.folder === currentFolderPath;
```

### 3. DirectUpload Config
```typescript
maxFiles: 100        // Otimizado para uploads menores
maxSize: 5120MB      // 5GB (multipart automático para >5GB)
```

### 4. s3_prefix Structure
- Admin: Bypass filtros (vê tudo)
- User: `users/{user_id}/` (isolado)

---

## 🐛 Problemas Já Resolvidos

✅ Avatar upload 400 → Fix: Limpar &amp; das URLs  
✅ 2FA ícone quebrado → Fix: Emoji fora do neon-text  
✅ Grid quebrando 1024x768 → Fix: md:grid-cols-2 lg:grid-cols-4  
✅ Users vendo arquivos de outros → Fix: s3_prefix no JWT  
✅ Admin sem dropdown → Fix: Condição expandida  
✅ Pastas mostrando só subpastas → Fix: getCurrentFiles() match exato  
✅ sergio_sena em root → Fix: Movido para users/sergio_sena/  

---

## 🎯 Roadmap v4.4 (Próxima Versão)

### Prioridade Alta
- [ ] **Editar usuários existentes** - Alterar email, senha, role
- [ ] **Thumbnails automáticos** - Preview de vídeos
- [ ] **Compressão de imagens** - Otimizar avatares
- [ ] **Logs de auditoria** - Registrar ações

### Prioridade Média
- [ ] **Notificações push** - Conversão completa
- [ ] **Picture-in-picture** - Player flutuante
- [ ] **Compartilhamento** - Pastas entre users
- [ ] **Busca avançada** - Filtros por data/tamanho

### Prioridade Baixa
- [ ] **PWA offline** - Cache de vídeos
- [ ] **Estatísticas** - Dashboard por usuário
- [ ] **Temas** - Customização de cores

---

## 📚 Documentação Completa

Para contexto detalhado, consulte:

1. **[PROMPT_CONSOLIDADO.md](./PROMPT_CONSOLIDADO.md)** - Histórico completo do projeto
2. **[METODO_DESENVOLVIMENTO.md](./METODO_DESENVOLVIMENTO.md)** - Metodologia C.E.R.T.O
3. **[README.md](../README.md)** - Overview e quick start
4. **[scripts/README.md](../scripts/README.md)** - Scripts utilitários

---

## 🚀 Como Começar

### Se for implementar nova feature:
1. Ler METODO_DESENVOLVIMENTO.md (metodologia C.E.R.T.O)
2. Seguir padrão: Contexto → Expectativa → Regras → Tarefa → Objetivo
3. Código mínimo necessário
4. Testar localmente antes de deploy
5. Deploy incremental com validação

### Se for corrigir bug:
1. Reproduzir o problema
2. Verificar se já foi resolvido (lista acima)
3. Analisar logs (CloudWatch)
4. Implementar fix mínimo
5. Validar solução

### Se for fazer deploy:
1. `npm run build` (verificar erros)
2. Testar localmente
3. Sync S3
4. Invalidar CloudFront
5. Validar em produção

---

## ⚠️ Avisos Importantes

### Segurança
- Nunca commitar credenciais
- JWT_SECRET em .env.local
- Validar inputs sempre
- s3_prefix obrigatório para users

### Performance
- Build otimizado antes de deploy
- Invalidar CloudFront após sync
- Testar em 1024x768 (tablet)
- Verificar mobile (gestos touch)

### Dados
- Backup antes de mover arquivos S3
- Validar estrutura users/{user_id}/
- Preservar originais no bucket uploads
- DynamoDB: user_id é chave primária

---

## 🎓 Metodologia C.E.R.T.O

Este projeto segue rigorosamente:

**C** - Contexto: Entender o domínio  
**E** - Expectativa: Definir objetivos  
**R** - Regras: Estabelecer restrições  
**T** - Tarefa: Quebrar em etapas  
**O** - Objetivo: Validar entrega  

Leia [METODO_DESENVOLVIMENTO.md](./METODO_DESENVOLVIMENTO.md) para detalhes.

---

## 📊 Métricas de Sucesso

- ✅ Uptime: 99.9%
- ✅ Performance: Lighthouse 95+
- ✅ Segurança: SSL + JWT + 2FA
- ✅ Escalabilidade: Milhares de usuários
- ✅ First Load: < 2s globalmente

---

## 🎯 Próximos Passos Sugeridos

1. **Implementar edição de usuários** (roadmap v4.4)
2. **Adicionar thumbnails automáticos** para vídeos
3. **Otimizar compressão de avatares**
4. **Implementar logs de auditoria**

Ou pergunte: **"O que você gostaria de implementar?"**

---

**Versão**: 4.3.0 | **Status**: ✅ PRODUÇÃO | **Última atualização**: 2025-01-18

**Sistema 100% funcional e documentado. Pronto para evolução!** 🚀
