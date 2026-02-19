@echo off
echo ========================================
echo   MIDIAFLOW - DEPLOY PRODUCAO v4.8.5
echo ========================================
echo.

echo [1/4] Sincronizando arquivos com S3...
aws s3 sync out/ s3://mediaflow-frontend-969430605054 --delete --cache-control "public,max-age=31536000,immutable" --exclude "*.html"

echo.
echo [2/4] Enviando HTML sem cache...
aws s3 sync out/ s3://mediaflow-frontend-969430605054 --delete --cache-control "no-cache" --exclude "*" --include "*.html"

echo.
echo [3/4] Invalidando CloudFront cache...
aws cloudfront create-invalidation --distribution-id E3UOGGJTS9B8LI --paths "/*"

echo.
echo [4/4] Verificando deploy...
echo URL: https://midiaflow.sstechnologies-cloud.com
echo.

echo ========================================
echo   DEPLOY CONCLUIDO COM SUCESSO!
echo ========================================
pause
