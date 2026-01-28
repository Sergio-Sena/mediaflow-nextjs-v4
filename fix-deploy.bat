@echo off
echo ========================================
echo CORRIGINDO DEPLOY - LIMPANDO CHUNKS ANTIGOS
echo ========================================
echo.

echo [1/4] Limpando bucket S3...
aws s3 rm s3://mediaflow-frontend-969430605054/ --recursive

echo.
echo [2/4] Fazendo build limpo...
rmdir /s /q .next 2>nul
rmdir /s /q out 2>nul
call npm run build

echo.
echo [3/4] Fazendo upload para S3...
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --cache-control "public, max-age=31536000, immutable" --exclude "*.html" --exclude "*.json"
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --exclude "*" --include "*.html" --include "*.json" --cache-control "public, max-age=0, must-revalidate"

echo.
echo [4/4] Invalidando CloudFront...
aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"

echo.
echo ========================================
echo DEPLOY CORRIGIDO COM SUCESSO!
echo ========================================
echo.
echo Aguarde 2-3 minutos para invalidacao do CloudFront
echo URL: https://midiaflow.sstechnologies-cloud.com
pause
