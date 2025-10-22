# 🚀 Comandos de Deploy - v4.7

## 📦 1. Lambda upload-handler

```bash
cd aws-setup/lambda-functions/upload-handler

aws lambda update-function-code \
  --function-name mediaflow-upload-handler \
  --zip-file fileb://upload-handler.zip \
  --region us-east-1
```

## 🌐 2. Frontend (Next.js → S3)

```bash
cd out

aws s3 sync . s3://mediaflow-frontend-969430605054 \
  --delete \
  --cache-control "public, max-age=31536000, immutable" \
  --exclude "*.html" \
  --region us-east-1

aws s3 sync . s3://mediaflow-frontend-969430605054 \
  --delete \
  --cache-control "public, max-age=0, must-revalidate" \
  --exclude "*" \
  --include "*.html" \
  --region us-east-1
```

## ⚡ 3. Invalidar CloudFront

```bash
aws cloudfront create-invalidation \
  --distribution-id E1YJHABTI1CW0M \
  --paths "/*"
```

## ✅ Checklist

- [x] Build Next.js concluído
- [x] ZIP Lambda criado
- [ ] Lambda atualizada
- [ ] Frontend sincronizado
- [ ] CloudFront invalidado
- [ ] Teste em produção

## 🧪 Teste

1. Login: https://midiaflow.sstechnologies-cloud.com
2. Selecionar dropdown: `📁 Minha pasta (Admin)`
3. Selecionar pasta: `C:\Users\dell 5557\Videos\IDM\Anime`
4. Upload
5. Verificar S3: `users/user_admin/Anime/`
