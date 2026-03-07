# 🧠 CONTEXTO ATUAL - MidiaFlow (Fixar como Pinned Context)

## 📦 Projeto
- **Next.js 14** + TypeScript + TailwindCSS
- **AWS**: S3, CloudFront, Lambda, API Gateway, DynamoDB
- **API Gateway**: `https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod`
- **CloudFront**: `E2HZKZ9ZJK18IU`
- **Buckets**: `mediaflow-uploads-969430605054` / `mediaflow-processed-969430605054`
- **Account**: `969430605054` / **Region**: `us-east-1`

---

## ✅ STATUS ATUAL (última sessão)

### Funcionando 100%
- ✅ Biblioteca de arquivos (FileList.tsx)
- ✅ Pastas / FolderManager
- ✅ Upload multipart (MultipartUploader.tsx)
- ✅ Analytics
- ✅ Video Player Premium (v4.9.0)
- ✅ Delete de arquivos
- ✅ CORS resolvido via proxy Next.js (`/api/upload/presigned`)
- ✅ Autenticação JWT

### Corrigido nesta sessão
- ✅ `SimpleFileUpload.tsx`: agora chama `onUploadComplete` após upload individual E em lote
- ✅ `AvatarUpload.tsx`: agora envia token JWT nas requisições (avatar-presigned e update-user)

### Pendente / Em investigação
- ❌ Upload pequeno (SimpleFileUpload) não atualizava lista após upload → **CORRIGIDO AGORA**
- ❌ Foto de perfil não carregava (sem token JWT) → **CORRIGIDO AGORA**
- ❓ Pasta `users/sergio_sena/` aparece com 0b no S3 → **INVESTIGANDO**

---

## 🔍 Investigação Pendente: Pasta 0b

**Hipótese**: A pasta `users/sergio_sena/` é um objeto "folder placeholder" (0 bytes) criado pelo S3 quando se cria pasta manualmente no console.

**Para verificar**:
```bash
aws s3api list-objects-v2 --bucket mediaflow-uploads-969430605054 \
  --prefix "users/sergio_sena/" --max-items 5
```

**Solução provável**: Deletar o objeto `users/sergio_sena/` (0b) — não afeta os arquivos dentro da pasta.

---

## 🏗️ Arquitetura de Autenticação

- JWT armazenado em `localStorage` com chave `token`
- Payload JWT contém: `user_id`, `role` (admin/user), `s3_prefix`
- Admin: acessa pasta `admin/`
- User: acessa pasta `users/{user_id}/`
- `s3_prefix` = `users/{user_id}/`

---

## 📁 Arquivos Principais

| Arquivo | Função |
|---------|--------|
| `components/modules/FileList.tsx` | Lista de arquivos com navegação por pastas |
| `components/modules/SimpleFileUpload.tsx` | Upload pequeno via presigned URL |
| `components/modules/MultipartUploader.tsx` | Upload multipart para arquivos grandes |
| `components/modules/VideoPlayer.tsx` | Player premium v4.9.0 |
| `components/AvatarUpload.tsx` | Upload de foto de perfil |
| `app/api/upload/presigned/route.ts` | Proxy Next.js → API Gateway (evita CORS) |
| `app/dashboard/page.tsx` | Dashboard principal |
| `lib/aws-client.ts` | Cliente AWS centralizado |

---

## 🔗 Endpoints Lambda (API Gateway)

| Endpoint | Lambda | Função |
|----------|--------|--------|
| `POST /upload/presigned` | `upload-handler` | Gera presigned URL |
| `POST /avatar-presigned` | `avatar-presigned` | Presigned URL para avatar |
| `POST /update-user` | `update-user` | Atualiza dados do usuário |
| `GET /files` | `files-handler` | Lista arquivos do usuário |
| `DELETE /files` | `files-handler` | Deleta arquivo |
| `POST /auth/login` | `auth-handler` | Login JWT |
| `POST /convert` | `convert-handler` | Converte vídeo para MP4 |

---

## ⚠️ Notas Importantes

1. **CORS**: Nunca chamar API Gateway direto do frontend — usar sempre proxy `/api/*` do Next.js
2. **Token**: Sempre incluir `Authorization: Bearer {token}` nas chamadas às Lambdas
3. **Pasta 0b**: Objeto `users/sergio_sena/` (0 bytes) é placeholder — pode deletar sem risco
4. **Backups VideoPlayer**: Existem 4 backups em `components/modules/VideoPlayer.tsx.backup*`
5. **Deploy**: `npm run build` → sync S3 → invalidar CloudFront `E2HZKZ9ZJK18IU`
