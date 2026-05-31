# MidiaFlow - Procedimentos de Mídia

## 1. Remux (.ts → .mp4)

### Comando padrão (com faststart para thumbnails)
```bash
chcp 65001
"C:\ffmpeg\bin\ffmpeg.exe" -i "arquivo.ts" -c copy -movflags +faststart "arquivo_sanitizado.mp4"
```

### Regras de sanitização de nomes
- Remover acentos, emojis, caracteres especiais
- Substituir espaços/hífens por `_`
- Remover referências a sites (Pornhub.com, etc)
- Remover nome do canal
- Limitar a 60 caracteres
- Extensão sempre `.mp4`

### Upload para S3
```bash
aws s3 sync "PASTA_LOCAL" s3://mediaflow-uploads-969430605054/users/sergio_sena/CATEGORIA/SUBCATEGORIA/ --exclude "*.py" --exclude "*.bat" --exclude "*.zip"
```

### Configuração de velocidade (internet 240+ Mbps upload)
```bash
aws configure set default.s3.max_concurrent_requests 20
aws configure set default.s3.multipart_chunksize 64MB
aws configure set default.s3.max_bandwidth 200MB/s
```

---

## 2. Geração de Thumbnails

### Automático (novos uploads)
- S3 trigger dispara `mediaflow-thumbnail-generator` para qualquer `.mp4` em `users/`
- Funciona via frontend e CLI
- Limitação: vídeos grandes com moov atom no final podem falhar (Lambda baixa só 30MB)

### Manual (batch - todos os vídeos)
```bash
python "C:\Projetos Git\MidiaFlow\scripts\generate_thumbnails.py"
```

**Como funciona:**
- Lista todos os .mp4 em `users/`
- Pula os que já têm thumbnail
- Gera presigned URL → ffmpeg faz seek aos 10s via HTTP streaming (não baixa o vídeo)
- 10 workers paralelos
- Fallback para primeiro frame se 10s falhar
- Upload do .jpg para `public/thumbnails/`

**Vantagens sobre a Lambda:**
- Sem limite de tempo ou disco
- Sem problema com moov atom (ffmpeg faz seek HTTP nativo)
- Processa todos de uma vez (~10-15 min para 700 vídeos)

### Regenerar todas as thumbnails
```bash
aws s3 rm s3://mediaflow-uploads-969430605054/public/thumbnails/ --recursive
python "C:\Projetos Git\MidiaFlow\scripts\generate_thumbnails.py"
```

### Auto-delete de thumbnail
- Quando um vídeo é deletado (via frontend ou API), a thumbnail correspondente é removida automaticamente pelo `files-handler`

---

## 3. Estrutura de paths no S3

| Tipo | Path |
|---|---|
| Vídeos privados | `users/{user_id}/{categoria}/{subcategoria}/arquivo.mp4` |
| Thumbnails | `public/thumbnails/{user_id}/{categoria}/{subcategoria}/arquivo.jpg` |
| Avatares | `avatars/avatar_{user_id}.{ext}` |

### Bucket principal: `mediaflow-uploads-969430605054` (us-east-1)
### Bucket backup: `backup-midia-smartphone` (sa-east-1)

---

## 4. CORS Multi-Origin

### Status: Implementado e funcionando em produção + localhost
- Todas as 18 Lambdas atualizadas com padrão `_request_origin`
- Env var `ALLOWED_ORIGINS` (comma-separated) em cada Lambda
- Valores: `https://midiaflow.sstechnologies-cloud.com,http://localhost:3000`
- Branch `dev` tem o código, produção deployada manualmente

### Padrão usado em cada Lambda:
```python
_request_origin = None

def get_allowed_origin(event):
    allowed = os.environ.get('ALLOWED_ORIGINS', 'https://midiaflow.sstechnologies-cloud.com').split(',')
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in allowed else allowed[0]

def lambda_handler(event, context):
    global _request_origin
    _request_origin = get_allowed_origin(event)
    ...

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': _request_origin or 'https://midiaflow.sstechnologies-cloud.com',
            ...
        },
        'body': json.dumps(body)
    }
```

### Lambdas com dependências externas (precisam zip com pacotes):
- `files-handler`, `view-handler`, `list-users`, `get-user-me` → PyJWT
- `verify-user-2fa` → PyJWT + pyotp
- `create-user` → pyotp

### Deploy manual de Lambda individual:
```bash
cd aws-setup/lambda-functions/NOME/
pip install PACOTE -t package --quiet
copy lambda_function.py package\
cd package && powershell -Command "Compress-Archive -Path * -DestinationPath ..\function.zip -Force"
cd .. && aws lambda update-function-code --function-name mediaflow-NOME --zip-file fileb://function.zip --region us-east-1
rmdir /S /Q package
```

---

## 5. Backup Unificado

### Bucket: `backup-midia-smartphone` (sa-east-1)
Unificação dos antigos buckets: `pics-notebackup`, `smarthophone`, `xioami-mi6` (já deletados)

### Estrutura:
```
backup-midia-smartphone/
├── Apps/                    ← apps do Redmi Note 8
├── Fotos/
│   ├── redmi-note-8/       ← fotos pessoais
│   ├── anime-art/          ← Jiggly Girls, Seart (AI art)
│   └── redmi-note-8/xiaomi-media/
├── Videos/
│   ├── redmi-note-8/       ← VideoDownloader (Anime, Stars, etc)
│   └── xiaomi-mi6/         ← FinalFantasy, Nier, Outros
└── WhatsApp/
    ├── audio/
    ├── documents/
    ├── gifs/
    ├── stickers/
    ├── video-notes/
    ├── voice-notes/
    ├── WhatsApp_Images.zip  (2.6GB)
    └── WhatsApp_Video.zip   (20GB)
```

---

## 6. Migração smartphone → MidiaFlow

### Script: `scripts/migrate_smartphone_bucket.py`
- Copia S3→S3 com sanitização de nomes
- 10 workers paralelos
- Pula duplicados (Charming, EmillyaBunny já existiam)
- Baixa "Pequenos" (WhatsApp) para local

### Script: `scripts/reorganize_by_keywords.py`
- Escaneia `Star/Outros/` e `Anime/Outros/`
- Move arquivos para pasta correta baseado em keywords no nome
- Keywords: Tifa→Final_Fantasy, Kate Kuray→Kate_Kuray, Megan→megan, Derpixon→Dexpirion, etc

### Resultado final MidiaFlow:
- **~960 vídeos** em `users/sergio_sena/`
- **~190GB** total
- Organizados em `Anime/` e `Star/` com subcategorias

---

## 7. Notas importantes

- `-movflags +faststart` no remux garante que a Lambda consiga gerar thumbnail (moov atom no início)
- Thumbnails são públicas (preview de 320px), vídeos são privados (presigned URL com JWT)
- O script local é a solução definitiva para batch; a Lambda é para novos uploads individuais
- CORS: branch `dev` tem código atualizado, precisa merge para `main` para passar pela esteira
- WiFi Dell 5557: Qualcomm QCA61x4A configurado com roaming lowest + power management desabilitado

---

## 8. Pendências / Próximos passos

- [ ] Merge `dev` → `main` (CORS multi-origin via esteira CI/CD)
- [ ] Backup do Poco F7 via ADB (fotos, vídeos, WhatsApp) → `backup-midia-smartphone`
- [ ] Rodar `generate_thumbnails.py` para gerar thumbnails dos novos vídeos migrados
- [ ] Deletar buckets antigos (já feito: pics-notebackup, smarthophone, xioami-mi6)

---

## 9. Caminhos locais importantes

| O quê | Path |
|---|---|
| Projeto MidiaFlow | `C:\Projetos Git\MidiaFlow` |
| FFmpeg | `C:\ffmpeg\bin\ffmpeg.exe` |
| Vídeos IDM | `C:\Users\dell 5557\Videos\IDM` |
| WhatsApp local | `C:\Users\dell 5557\Videos\IDM\Wattsup` |
| Scripts utilitários | `C:\Projetos Git\MidiaFlow\scripts\` |

---

## 10. Nomes das Lambdas na AWS

| Função | Nome AWS |
|---|---|
| auth-handler | mediaflow-auth-handler |
| files-handler | mediaflow-files-handler |
| view-handler | mediaflow-view-handler |
| upload-handler | mediaflow-upload-handler |
| multipart-handler | mediaflow-multipart-handler |
| share-content | mediaflow-share-content |
| get-user | mediaflow-get-user |
| get-user-me | mediaflow-get-user-me |
| list-users | mediaflow-list-users |
| create-user | mediaflow-create-user |
| verify-user-2fa | mediaflow-verify-user-2fa |
| avatar-presigned | mediaflow-avatar-presigned |
| cleanup-handler | mediaflow-cleanup-handler |
| convert-handler | mediaflow-convert-handler |
| thumbnail-generator | mediaflow-thumbnail-generator |
| folder-operations | folder-operations |
| approve-user | approve-user |
| update-user | mediaflow-update-user |
