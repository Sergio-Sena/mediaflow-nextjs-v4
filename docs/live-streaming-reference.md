# 📡 Live Streaming - Referência para Implementação (v4.10)

## Arquitetura Proposta

```
Câmera/OBS → MediaLive → MediaStore → CloudFront → Player HLS
```

## Serviços AWS Necessários

### AWS MediaLive
- Codifica o stream de entrada (RTMP/RTP)
- Converte para HLS/DASH
- Output para MediaStore

### AWS MediaStore
- Armazenamento otimizado para live streaming
- Latência consistente (milissegundos)
- Custo: ~$0.036/GB armazenamento
- Ideal para conteúdo ao vivo (não para VOD)

### CloudFront
- Distribuição global do stream
- Já temos configurado

## Arquitetura Atual vs Futura

| Funcionalidade | Atual (v4.9) | Futuro (v4.10) |
|---|---|---|
| VOD | S3 + CloudFront ✅ | S3 + CloudFront (mantém) |
| Arquivos estáticos | S3 + CloudFront ✅ | S3 + CloudFront (mantém) |
| Live Streaming | ❌ | MediaLive + MediaStore + CloudFront |

## Notas
- MediaStore NÃO substitui S3 para VOD e arquivos estáticos
- MediaStore NÃO suporta presigned URLs nem multipart upload
- Usar MediaStore APENAS para live streaming
- S3 continua sendo a melhor opção para todo o resto
