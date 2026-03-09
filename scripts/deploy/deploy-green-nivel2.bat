@echo off
echo ========================================
echo  DEPLOY GREEN - Nivel 2 (Testes + UX)
echo ========================================
echo.

echo [1/5] Rodando testes...
call npm test
if %errorlevel% neq 0 (
    echo ❌ Testes falharam! Deploy cancelado.
    exit /b 1
)
echo ✅ Testes passaram
echo.

echo [2/5] Build de producao...
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Build falhou! Deploy cancelado.
    exit /b 1
)
echo ✅ Build completo
echo.

echo [3/5] Sync para S3 Green...
aws s3 sync .next/static s3://mediaflow-frontend-green/_next/static --delete
aws s3 sync out s3://mediaflow-frontend-green --delete --exclude "_next/*"
echo ✅ Arquivos sincronizados
echo.

echo [4/5] Invalidando CloudFront...
aws cloudfront create-invalidation --distribution-id E1O4R8P5BGZTMW --paths "/*"
echo ✅ Cache invalidado
echo.

echo [5/5] Configurando Rate Limiting...
python aws-setup/configure-rate-limiting.py
echo ✅ Rate limiting configurado
echo.

echo ========================================
echo  ✅ DEPLOY GREEN COMPLETO!
echo ========================================
echo.
echo Teste em: https://midiaflow.sstechnologies-cloud.com
echo.
pause
