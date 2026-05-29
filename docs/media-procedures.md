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

---

## 3. Estrutura de paths no S3

| Tipo | Path |
|---|---|
| Vídeos privados | `users/{user_id}/{categoria}/{subcategoria}/arquivo.mp4` |
| Thumbnails | `public/thumbnails/{user_id}/{categoria}/{subcategoria}/arquivo.jpg` |
| Avatares | `avatars/avatar_{user_id}.{ext}` |

---

## 4. Notas importantes

- `-movflags +faststart` no remux garante que a Lambda consiga gerar thumbnail (moov atom no início)
- Thumbnails são públicas (preview de 320px), vídeos são privados (presigned URL com JWT)
- O script local é a solução definitiva para batch; a Lambda é para novos uploads individuais
