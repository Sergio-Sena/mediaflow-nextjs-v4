# 🚀 Plano Próximo Nível - v4.6

**Data**: 20/10/2025  
**Versão Atual**: v4.5  
**Próxima Versão**: v4.6

---

## 🎯 Objetivos Principais

### 1. **Remover Tab "🏠 Início" e Criar Nova Home** 🎬

**Problema Atual**:
- Tab "Início" demora a carregar
- Hero Section com carrosséis pesados
- Experiência não otimizada

**Solução Proposta**:
- Remover tab "🏠 Início" do dashboard
- Criar nova página inicial em `/` (raiz)
- Seguir padrão Netflix/Prime Video
- Usar imagens da pasta `public/`
- Design orientado pelo usuário

**Referências**:
- Netflix: Hero grande + carrosséis horizontais
- Prime Video: Destaque principal + categorias
- Disney+: Banner rotativo + seções temáticas

**Estrutura Sugerida**:
```
/ (Home Pública)
├── Hero Section (imagem de destaque)
├── Destaques (3-4 cards grandes)
├── Categorias (carrosséis por pasta)
└── CTA Login/Cadastro

/dashboard (Área Logada)
├── 📁 Biblioteca (lista completa)
├── 📤 Upload
├── 🗂️ Gerenciador
└── 📊 Analytics
```

**Imagens Disponíveis**:
- Verificar pasta `public/` para assets
- Criar hero banner atraente
- Cards de destaque com thumbnails

---

### 2. **Implementar Multipart Upload S3** ⚡

**Problema Atual**:
- Upload de arquivos grandes é lento
- Sem paralelização
- Falha = reiniciar tudo

**Solução: AWS S3 Multipart Upload**

#### **Como Funciona**:

1. **Inicialização**:
   - Requisição ao S3 para iniciar Multipart Upload
   - Recebe `UploadId` único

2. **Segmentação**:
   - Divide arquivo em partes (5MB+ cada)
   - Cada parte recebe um número sequencial

3. **Upload Paralelo**:
   - Envia múltiplas partes simultaneamente
   - Usa múltiplas conexões HTTP
   - Se uma parte falha, reenvia só ela

4. **Conclusão**:
   - Requisição final para "completar" upload
   - S3 remonta todas as partes na ordem correta

#### **Vantagens**:

✅ **Aceleração**: Múltiplas conexões = máxima largura de banda  
✅ **Resiliência**: Falha em uma parte não afeta outras  
✅ **Retomada**: Pode pausar e continuar upload  
✅ **Recomendado AWS**: Para arquivos > 100MB  
✅ **Similar ao IDM**: Paralelização de downloads/uploads

#### **Implementação Técnica Detalhada**:

**Estratégia de Tamanhos**:
```typescript
| Tamanho Arquivo | Método         | Chunk Size | Paralelos |
|-----------------|----------------|------------|----------|
| < 100MB         | Upload Normal  | N/A        | 1        |
| 100MB - 1GB     | Multipart      | 50MB       | 4        |
| 1GB - 5GB       | Multipart      | 50MB       | 6        |
| > 5GB           | Multipart      | 100MB      | 6        |
```

**Frontend (components/modules/MultipartUpload.tsx)**:
```typescript
const uploadLargeFile = async (file: File) => {
  const CHUNK_SIZE = 50 * 1024 * 1024; // 50MB
  const chunks = Math.ceil(file.size / CHUNK_SIZE);
  
  // 1. Iniciar multipart
  const { uploadId, key } = await fetch('/api/upload/multipart/init', {
    method: 'POST',
    body: JSON.stringify({ 
      filename: file.name, 
      fileSize: file.size 
    })
  }).then(r => r.json());
  
  // 2. Upload chunks em paralelo (4 simultâneos)
  const parts = [];
  for (let i = 0; i < chunks; i += 4) {
    const batch = [];
    for (let j = 0; j < 4 && i + j < chunks; j++) {
      const partNumber = i + j + 1;
      const start = (i + j) * CHUNK_SIZE;
      const end = Math.min(start + CHUNK_SIZE, file.size);
      const chunk = file.slice(start, end);
      
      batch.push(uploadChunk(chunk, key, uploadId, partNumber));
    }
    const batchResults = await Promise.all(batch);
    parts.push(...batchResults);
    
    // Progress preciso
    setProgress((i + batch.length) / chunks * 100);
  }
  
  // 3. Completar
  await fetch('/api/upload/multipart/complete', {
    method: 'POST',
    body: JSON.stringify({ key, uploadId, parts })
  });
};

// Retry inteligente com backoff exponencial
const uploadChunk = async (
  chunk, key, uploadId, partNumber, retries = 3
) => {
  for (let i = 0; i < retries; i++) {
    try {
      const { uploadUrl } = await getPresignedUrl(
        key, uploadId, partNumber
      );
      const response = await fetch(uploadUrl, {
        method: 'PUT',
        body: chunk
      });
      return { 
        PartNumber: partNumber, 
        ETag: response.headers.get('ETag') 
      };
    } catch (error) {
      if (i === retries - 1) throw error;
      await sleep(1000 * (i + 1)); // Backoff: 1s, 2s, 3s
    }
  }
};

// Detecção automática
const shouldUseMultipart = file.size > 100 * 1024 * 1024;

if (shouldUseMultipart) {
  await uploadLargeFile(file);
} else {
  await uploadNormal(file);
}
```

**Backend (aws-setup/lambda-functions/multipart-handler/lambda_function.py)**:
```python
import boto3
import json
import jwt
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
SECRET_KEY = 'your-secret-key-here-change-in-production'

def lambda_handler(event, context):
    path = event.get('path', '')
    body = json.loads(event.get('body', '{}'))
    
    # Extrair username do JWT
    username = extract_username(event)
    
    # INIT - Iniciar multipart upload
    if path.endswith('/init'):
        filename = body['filename']
        key = f"users/{username}/{filename}"
        
        response = s3.create_multipart_upload(
            Bucket=BUCKET,
            Key=key,
            Metadata={
                'original_name': filename,
                'upload_timestamp': datetime.now().isoformat()
            }
        )
        return cors_response(200, {
            'success': True,
            'uploadId': response['UploadId'],
            'key': key
        })
    
    # PART - Gerar presigned URL para upload de parte
    if path.endswith('/part'):
        url = s3.generate_presigned_url(
            'upload_part',
            Params={
                'Bucket': BUCKET,
                'Key': body['key'],
                'UploadId': body['uploadId'],
                'PartNumber': body['partNumber']
            },
            ExpiresIn=3600  # 1 hora
        )
        return cors_response(200, {
            'success': True,
            'uploadUrl': url
        })
    
    # COMPLETE - Finalizar multipart upload
    if path.endswith('/complete'):
        s3.complete_multipart_upload(
            Bucket=BUCKET,
            Key=body['key'],
            UploadId=body['uploadId'],
            MultipartUpload={'Parts': body['parts']}
        )
        return cors_response(200, {
            'success': True,
            'message': 'Upload completed'
        })
    
    # ABORT - Cancelar multipart upload
    if path.endswith('/abort'):
        s3.abort_multipart_upload(
            Bucket=BUCKET,
            Key=body['key'],
            UploadId=body['uploadId']
        )
        return cors_response(200, {
            'success': True,
            'message': 'Upload aborted'
        })

def extract_username(event):
    auth_header = event.get('headers', {}).get('Authorization', '')
    if auth_header:
        try:
            token = auth_header.replace('Bearer ', '')
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded.get('username', 'anonymous')
        except:
            pass
    return 'anonymous'

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
```

**API Routes (app/api/upload/multipart/[action]/route.ts)**:
```typescript
// Proxy para Lambda multipart-handler
export async function POST(request: NextRequest) {
  const action = request.nextUrl.pathname.split('/').pop();
  const body = await request.json();
  
  const response = await fetch(
    `https://API_GATEWAY_URL/prod/multipart/${action}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('Authorization') || ''
      },
      body: JSON.stringify(body)
    }
  );
  
  return NextResponse.json(await response.json());
}
```

#### **Configuração Otimizada**:

- **Tamanho do Chunk**: 50MB (ótimo para 100MB-5GB)
- **Chunks Paralelos**: 4 simultâneos (não sobrecarrega)
- **Timeout**: 60s por chunk (50MB em conexão lenta)
- **Retry**: 3 tentativas com backoff exponencial (1s, 2s, 3s)
- **Progress**: Atualizar a cada chunk completo (precisão de 2%)
- **Detecção**: Automática para arquivos > 100MB
- **Cancelamento**: Botão para abortar upload
- **Cleanup**: AWS remove partes órfãs após 7 dias

#### **Fluxo de Implementação**:

```
1. User seleciona arquivo grande (>100MB)
2. Frontend divide em chunks de 5MB
3. Chama /multipart/init → recebe UploadId
4. Loop paralelo:
   - Upload chunk 1, 2, 3, 4 simultaneamente
   - Recebe ETag de cada parte
   - Atualiza progress bar
5. Todas partes completas → /multipart/complete
6. S3 remonta arquivo final
7. Trigger conversão MediaConvert (se vídeo)
```

#### **Comparação com Upload Atual**:

| Recurso | Upload Atual | Multipart Upload |
|---------|--------------|------------------|
| Velocidade | 1 conexão | 4-6 conexões paralelas |
| Resiliência | Falha = reiniciar | Falha = reenviar chunk |
| Tamanho Max | 5GB | Ilimitado (até 5TB) |
| Progress | Arquivo inteiro | Por chunk (mais preciso) |
| Retomada | ❌ Não | ✅ Sim |

---

## 📋 Checklist de Implementação

### Fase 1: Nova Home Page
- [ ] Criar `app/page.tsx` (home pública)
- [ ] Remover tab "🏠 Início" do dashboard
- [ ] Design hero section com imagem
- [ ] Cards de destaque (3-4)
- [ ] CTA para login/cadastro
- [ ] Responsivo mobile

### Fase 2: Multipart Upload
- [ ] **Criar Lambda `multipart-handler`**
  - [ ] Endpoint `/init` - Iniciar upload e retornar uploadId
  - [ ] Endpoint `/part` - Gerar presigned URL para chunk
  - [ ] Endpoint `/complete` - Finalizar e juntar partes
  - [ ] Endpoint `/abort` - Cancelar upload
  - [ ] Extrair username do JWT
  - [ ] Salvar em `users/{username}/`
  - [ ] Deploy Lambda
  - [ ] Configurar API Gateway routes
- [ ] **Criar componente `MultipartUpload.tsx`**
  - [ ] Dividir arquivo em chunks de 50MB
  - [ ] Upload paralelo (4 simultâneos)
  - [ ] Progress tracking preciso por chunk
  - [ ] Retry logic com backoff exponencial
  - [ ] Botão cancelar upload
  - [ ] Estimativa de tempo restante
  - [ ] Tratamento de erros
- [ ] **Atualizar `DirectUpload.tsx`**
  - [ ] Detectar arquivo > 100MB
  - [ ] Usar multipart automaticamente
  - [ ] Fallback para upload normal se falhar
  - [ ] UI diferenciada para multipart
  - [ ] Mostrar velocidade de upload
- [ ] **Criar API Routes Next.js**
  - [ ] `/api/upload/multipart/init`
  - [ ] `/api/upload/multipart/part`
  - [ ] `/api/upload/multipart/complete`
  - [ ] `/api/upload/multipart/abort`
- [ ] **Testes com arquivos grandes**
  - [ ] 100MB (limite mínimo)
  - [ ] 500MB (chunk único)
  - [ ] 1GB (2 chunks)
  - [ ] 2.5GB (5 chunks)
  - [ ] 5GB (10 chunks)
  - [ ] Teste de falha e retry
  - [ ] Teste de cancelamento

### Fase 3: Deploy
- [ ] Deploy Lambda multipart
- [ ] Build frontend
- [ ] Sync S3
- [ ] Invalidate CloudFront
- [ ] Testes em produção

---

## 🎨 Mockup Nova Home

```
┌─────────────────────────────────────────────┐
│  🎬 Mídiaflow                    [Login]    │
├─────────────────────────────────────────────┤
│                                             │
│     ╔═══════════════════════════════╗      │
│     ║                               ║      │
│     ║   HERO IMAGE / VIDEO          ║      │
│     ║   "Seu streaming pessoal"     ║      │
│     ║                               ║      │
│     ║   [▶ Começar Agora]           ║      │
│     ╚═══════════════════════════════╝      │
│                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │ Card 1  │ │ Card 2  │ │ Card 3  │      │
│  │ Feature │ │ Feature │ │ Feature │      │
│  └─────────┘ └─────────┘ └─────────┘      │
│                                             │
│  📁 Suas Pastas                             │
│  ← [Pasta 1] [Pasta 2] [Pasta 3] →        │
│                                             │
│  🎥 Vídeos Recentes                         │
│  ← [Video 1] [Video 2] [Video 3] →        │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 📊 Métricas Esperadas

### Performance:
- **Upload 1GB**: 
  - Atual: ~15min (1 conexão)
  - Multipart: ~5min (4 conexões paralelas = 3x mais rápido)
- **Upload 5GB**:
  - Atual: ~75min (1 conexão)
  - Multipart: ~20min (6 conexões paralelas = 3.75x mais rápido)
- **Resiliência**: 
  - Atual: 0% (falha = reiniciar tudo)
  - Multipart: 95%+ (reenvio apenas do chunk que falhou)
- **Largura de Banda**:
  - Atual: ~1.1 MB/s (subutilizada)
  - Multipart: ~4.2 MB/s (utilização máxima)
- **Experiência**:
  - Progress preciso (2% por chunk em 5GB)
  - Estimativa de tempo confiável
  - Possibilidade de pausar/retomar

### UX:
- **Home Load**: < 1s (sem carrosséis pesados)
- **First Paint**: < 500ms
- **Interactive**: < 2s

---

## 🔗 Referências

### AWS Multipart Upload:
- [AWS S3 Multipart Upload Docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)
- [AWS SDK v3 Examples](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/s3-example-creating-buckets.html)
- [Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html#mpu-best-practices)

### Design Inspiration:
- Netflix Homepage
- Amazon Prime Video
- Disney+ Landing Page
- Spotify Web Player

---

## ⚠️ Considerações

### Multipart Upload:
- Mínimo 5MB por parte (exceto última)
- Máximo 10.000 partes por upload
- Custo: Mesmo que upload normal
- Limpeza: Abortar uploads incompletos após 7 dias

### Nova Home:
- Não carregar vídeos automaticamente
- Lazy load de imagens
- Cache agressivo
- SEO otimizado

---

## 🎯 Resultado Final v4.6

**Home Pública**:
- ✅ Rápida (< 1s load)
- ✅ Atraente (design Netflix-like)
- ✅ Conversão (CTA claro)

**Upload Otimizado**:
- ✅ 3x mais rápido
- ✅ Resiliente a falhas
- ✅ Progress preciso
- ✅ Retomada de upload

**Experiência**:
- ✅ Profissional
- ✅ Performática
- ✅ Escalável

---

**Status**: 📝 Planejamento  
**Prioridade**: 🔥 Alta  
**Complexidade**: ⭐⭐⭐ Média-Alta  
**Tempo Estimado**: 4-6 horas
