# 🌐 Área Pública Multi-Mídia - Midiaflow v4.10

**Data:** 22/01/2026  
**Status:** 📋 PLANEJADO  
**Executor:** @Maestro  
**Revisor:** @Lyra

---

## 🎯 Objetivo

Criar área pública onde usuários podem compartilhar **vídeos, fotos e arquivos** (PDFs, documentos) com acesso livre, sem necessidade de autenticação.

---

## 📊 Requisitos Funcionais

### 1. Marcação de Mídias como Públicas
- ✅ Toggle "Tornar Público" em cada arquivo do dashboard
- ✅ Suporte para: vídeos, fotos, PDFs, documentos
- ✅ Confirmação antes de tornar público
- ✅ Opção de remover de público a qualquer momento

### 2. Área Pública Multi-Mídia
- ✅ Rota `/public` ou `/explore` (acesso livre)
- ✅ Filtros por tipo: Todos | Vídeos | Fotos | Documentos
- ✅ Grid responsivo adaptado ao tipo de mídia
- ✅ Busca por título/descrição

### 3. Visualização por Tipo
- **Vídeos:** Player integrado com controles
- **Fotos:** Lightbox/galeria com zoom
- **PDFs:** Visualizador inline (iframe)
- **Documentos:** Download direto com preview

---

## 🏗️ Arquitetura

### DynamoDB - Nova Tabela: `mediaflow-public-media`

```json
{
  "mediaId": "uuid-v4",
  "userId": "sergio_sena",
  "userName": "Sergio Sena",
  "mediaType": "video|image|pdf|document",
  "originalKey": "users/sergio_sena/file.mp4",
  "title": "Título da Mídia",
  "description": "Descrição opcional",
  "thumbnail": "url-thumbnail",
  "fileSize": 1024000,
  "mimeType": "video/mp4",
  "extension": "mp4",
  "views": 0,
  "downloads": 0,
  "likes": 0,
  "createdAt": "2026-01-22T10:00:00Z",
  "updatedAt": "2026-01-22T10:00:00Z",
  "isPublic": true
}
```

**Índices:**
- Primary Key: `mediaId`
- GSI1: `userId-createdAt` (listar mídias públicas do usuário)
- GSI2: `mediaType-createdAt` (filtrar por tipo)
- GSI3: `isPublic-views` (trending)

### Tipos de Mídia Suportados

```javascript
const MEDIA_TYPES = {
  video: {
    extensions: ['mp4', 'webm', 'mov', 'avi', 'mkv'],
    mimeTypes: ['video/mp4', 'video/webm', 'video/quicktime'],
    icon: '🎬',
    viewer: 'VideoPlayer'
  },
  image: {
    extensions: ['jpg', 'jpeg', 'png', 'gif', 'webp'],
    mimeTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    icon: '📷',
    viewer: 'ImageViewer'
  },
  pdf: {
    extensions: ['pdf'],
    mimeTypes: ['application/pdf'],
    icon: '📄',
    viewer: 'PDFViewer'
  },
  document: {
    extensions: ['doc', 'docx', 'txt', 'xlsx', 'pptx', 'csv'],
    mimeTypes: ['application/msword', 'text/plain', 'application/vnd.ms-excel'],
    icon: '📝',
    viewer: 'DocumentDownload'
  }
}
```

---

## 🔧 Componentes Backend

### Lambda Functions

#### 1. `toggle-public-media`
**Rota:** `POST /api/media/toggle-public`  
**Auth:** Requerida (JWT)

```python
def lambda_handler(event, context):
    # Validar usuário
    # Verificar se arquivo existe e pertence ao usuário
    # Criar/atualizar registro em mediaflow-public-media
    # Retornar status
```

**Request:**
```json
{
  "fileKey": "users/sergio_sena/video.mp4",
  "isPublic": true,
  "title": "Meu Vídeo",
  "description": "Descrição opcional"
}
```

**Response:**
```json
{
  "success": true,
  "mediaId": "uuid",
  "isPublic": true
}
```

#### 2. `list-public-media`
**Rota:** `GET /api/public/media?type=video&limit=20&offset=0`  
**Auth:** Não requerida

```python
def lambda_handler(event, context):
    # Buscar em mediaflow-public-media
    # Filtrar por tipo (opcional)
    # Ordenar por views/data
    # Retornar lista paginada
```

**Response:**
```json
{
  "success": true,
  "items": [
    {
      "mediaId": "uuid",
      "title": "Título",
      "mediaType": "video",
      "thumbnail": "url",
      "userName": "Sergio Sena",
      "views": 100,
      "createdAt": "2026-01-22T10:00:00Z"
    }
  ],
  "total": 150,
  "hasMore": true
}
```

#### 3. `view-public-media`
**Rota:** `GET /api/public/media/{mediaId}`  
**Auth:** Não requerida

```python
def lambda_handler(event, context):
    # Buscar mídia por mediaId
    # Gerar presigned URL (TTL baseado no tipo)
    # Incrementar contador de views
    # Retornar dados + URL
```

**Response:**
```json
{
  "success": true,
  "media": {
    "mediaId": "uuid",
    "title": "Título",
    "description": "Descrição",
    "mediaType": "video",
    "viewUrl": "https://s3.presigned.url",
    "thumbnail": "url",
    "userName": "Sergio Sena",
    "views": 101,
    "fileSize": 1024000
  }
}
```

#### 4. `increment-media-stats`
**Rota:** `POST /api/public/media/{mediaId}/stats`  
**Auth:** Não requerida

```python
def lambda_handler(event, context):
    # Incrementar views ou downloads
    # Rate limiting por IP (evitar spam)
    # Atualizar DynamoDB
```

---

## 🎨 Componentes Frontend

### Páginas

#### 1. `/app/public/page.tsx`
Galeria pública com filtros

```tsx
export default function PublicPage() {
  // Listar mídias públicas
  // Filtros: Todos, Vídeos, Fotos, Documentos
  // Grid responsivo
  // Paginação infinita
}
```

#### 2. `/app/public/[mediaId]/page.tsx`
Visualizador universal

```tsx
export default function MediaViewPage({ params }) {
  // Buscar mídia por ID
  // Renderizar visualizador apropriado
  // Incrementar views
  // Mostrar informações do criador
}
```

### Componentes

#### 1. `PublicMediaToggle.tsx`
Toggle no dashboard

```tsx
interface Props {
  fileKey: string
  fileName: string
  isPublic: boolean
  onToggle: (isPublic: boolean) => void
}

export default function PublicMediaToggle({ ... }) {
  // Toggle com confirmação
  // Modal para título/descrição
  // Feedback visual
}
```

#### 2. `MediaViewer.tsx`
Visualizador universal

```tsx
interface Props {
  media: PublicMedia
}

export default function MediaViewer({ media }) {
  // Switch por mediaType
  // Renderizar VideoPlayer, ImageViewer, PDFViewer ou DocumentDownload
}
```

#### 3. `PublicMediaCard.tsx`
Card na galeria

```tsx
interface Props {
  media: PublicMedia
}

export default function PublicMediaCard({ media }) {
  // Thumbnail
  // Título
  // Tipo (ícone)
  // Views/Downloads
  // Link para visualização
}
```

---

## 🔐 Segurança

### Presigned URLs por Tipo

```javascript
const TTL_CONFIG = {
  video: 24 * 60 * 60,      // 24 horas
  image: 24 * 60 * 60,      // 24 horas
  pdf: 1 * 60 * 60,         // 1 hora
  document: 1 * 60 * 60     // 1 hora
}
```

### Rate Limiting
- **Views:** Máximo 1 view por IP a cada 5 minutos
- **Downloads:** Máximo 10 downloads por IP por hora
- **Toggle Public:** Máximo 50 operações por usuário por dia

### Validações
- ✅ Verificar propriedade do arquivo antes de tornar público
- ✅ Validar tipo MIME do arquivo
- ✅ Limitar tamanho de título/descrição
- ✅ Sanitizar inputs (XSS prevention)

---

## 📈 Funcionalidades Futuras (v4.11+)

### Fase 2
- [ ] Sistema de likes/favoritos
- [ ] Comentários em mídias públicas
- [ ] Compartilhamento social (Twitter, Facebook)
- [ ] Embed code para sites externos

### Fase 3
- [ ] Categorias/tags
- [ ] Busca avançada
- [ ] Trending/mais vistos
- [ ] Perfil público do usuário

### Fase 4
- [ ] Monetização (vídeos premium)
- [ ] Analytics detalhado
- [ ] Playlists públicas
- [ ] API pública para desenvolvedores

---

## 💰 Estimativa de Custo

### AWS Services

| Serviço | Uso Estimado | Custo/Mês |
|---------|--------------|-----------|
| DynamoDB | 2000 itens, 20k reads | $0.30 |
| Lambda | 20k invocações | $0.15 |
| S3 GET | 20k requests | $0.08 |
| CloudFront | 50GB transfer | $4.25 |
| **TOTAL** | | **~$4.80/mês** |

### Escalabilidade

| Usuários Ativos | Mídias Públicas | Custo/Mês |
|-----------------|-----------------|-----------|
| 100 | 500 | $2.50 |
| 1.000 | 5.000 | $12.00 |
| 10.000 | 50.000 | $85.00 |

---

## 🚀 Plano de Implementação

### Fase 1: Backend (3-4 horas)
1. ✅ Criar tabela DynamoDB `mediaflow-public-media`
2. ✅ Implementar Lambda `toggle-public-media`
3. ✅ Implementar Lambda `list-public-media`
4. ✅ Implementar Lambda `view-public-media`
5. ✅ Implementar Lambda `increment-media-stats`
6. ✅ Configurar API Gateway (rotas públicas)
7. ✅ Testes unitários

### Fase 2: Frontend (4-5 horas)
1. ✅ Criar página `/app/public/page.tsx`
2. ✅ Criar página `/app/public/[mediaId]/page.tsx`
3. ✅ Implementar `PublicMediaToggle.tsx`
4. ✅ Implementar `MediaViewer.tsx`
5. ✅ Implementar `PublicMediaCard.tsx`
6. ✅ Integrar toggle no dashboard
7. ✅ Testes E2E

### Fase 3: Otimizações (2-3 horas)
1. ✅ Thumbnails automáticos (vídeos)
2. ✅ Compressão de imagens
3. ✅ Cache de listagens
4. ✅ SEO (meta tags dinâmicas)
5. ✅ Performance testing

### Fase 4: Deploy (1 hora)
1. ✅ Deploy Lambdas
2. ✅ Deploy Frontend
3. ✅ Testes em produção
4. ✅ Monitoramento

**Tempo Total Estimado:** 10-13 horas

---

## 📝 Checklist de Execução

### Pré-requisitos
- [ ] Backup da versão atual
- [ ] Commit no GitHub
- [ ] Ambiente de desenvolvimento pronto
- [ ] Credenciais AWS configuradas

### Backend
- [ ] Tabela DynamoDB criada
- [ ] Lambda `toggle-public-media` deployada
- [ ] Lambda `list-public-media` deployada
- [ ] Lambda `view-public-media` deployada
- [ ] Lambda `increment-media-stats` deployada
- [ ] API Gateway configurado
- [ ] Testes backend OK

### Frontend
- [ ] Página `/public` criada
- [ ] Página `/public/[mediaId]` criada
- [ ] Componente `PublicMediaToggle` criado
- [ ] Componente `MediaViewer` criado
- [ ] Componente `PublicMediaCard` criado
- [ ] Integração no dashboard
- [ ] Testes frontend OK

### Deploy
- [ ] Build Next.js
- [ ] Upload S3
- [ ] Invalidação CloudFront
- [ ] Testes em produção
- [ ] Documentação atualizada

---

## 🎯 Prompt para @Maestro

```
@Maestro: Implementar Área Pública Multi-Mídia - Midiaflow v4.10

Objetivo: Criar área pública onde usuários podem compartilhar vídeos, fotos e 
arquivos (PDFs, documentos) com acesso livre.

Referência: docs/AREA_PUBLICA_MULTIMIDIA.md

Tarefas:
1. Criar infraestrutura backend (DynamoDB + 4 Lambdas)
2. Implementar frontend (2 páginas + 3 componentes)
3. Integrar toggle no dashboard existente
4. Testes e deploy

Arquitetura: Seguir especificação completa no documento
Tempo estimado: 10-13 horas
Prioridade: MÉDIA (após backup e commit da versão atual)

Executar após confirmação de backup v4.9.1 completo.
```

---

## 📚 Referências

- [Next.js Dynamic Routes](https://nextjs.org/docs/app/building-your-application/routing/dynamic-routes)
- [AWS DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [S3 Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)
- [React Video Player](https://www.npmjs.com/package/react-player)

---

**Documento criado por:** @Lyra  
**Aprovado por:** Sergio Sena  
**Data:** 22/01/2026  
**Versão:** 1.0
