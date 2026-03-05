# 🎬 Ambiente de Teste Local - MidiaFlow

## Como usar vídeos locais para testes

### 1. Adicione seus vídeos
Coloque arquivos MP4 na pasta:
```
public/test-videos/
├── video1.mp4
├── video2.mp4
└── sample.mp4
```

### 2. Acesse a página de teste
```
http://localhost:3000/test-local
```

### 3. Teste os controles
- ✅ Toque no centro: Play/Pause
- ✅ Swipe lateral: Avançar/Retroceder
- ✅ Controles mobile (Poco F7)
- ✅ Fullscreen
- ✅ Volume

### 4. Não afeta produção
- Vídeos locais usam prefixo `local:`
- Produção continua usando S3 + CloudFront
- Apenas para desenvolvimento

## Exemplo de vídeo de teste
Baixe um sample gratuito:
- https://sample-videos.com/
- https://test-videos.co.uk/

Renomeie para `video1.mp4` e coloque em `public/test-videos/`
