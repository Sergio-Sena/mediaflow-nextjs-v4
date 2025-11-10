@echo off
echo ================================================================================
echo CONFIGURANDO GITHUB SECRETS
echo ================================================================================
echo.

REM Pegar AWS credentials do ambiente
for /f "tokens=2 delims==" %%a in ('aws configure get aws_access_key_id') do set AWS_KEY=%%a
for /f "tokens=2 delims==" %%a in ('aws configure get aws_secret_access_key') do set AWS_SECRET=%%a

echo Configurando secrets...
echo.

echo [1/6] AWS_ACCESS_KEY_ID
echo %AWS_KEY% | gh secret set AWS_ACCESS_KEY_ID
if %errorlevel% equ 0 (echo ✓ OK) else (echo ✗ ERRO)

echo [2/6] AWS_SECRET_ACCESS_KEY
echo %AWS_SECRET% | gh secret set AWS_SECRET_ACCESS_KEY
if %errorlevel% equ 0 (echo ✓ OK) else (echo ✗ ERRO)

echo [3/6] JWT_SECRET
echo 17b8312c72fdcffbff89f2f4a564fb26e936002d344717ab7753a237fcd57aea | gh secret set JWT_SECRET
if %errorlevel% equ 0 (echo ✓ OK) else (echo ✗ ERRO)

echo [4/6] NEXT_PUBLIC_API_URL
echo https://api.midiaflow.sstechnologies-cloud.com | gh secret set NEXT_PUBLIC_API_URL
if %errorlevel% equ 0 (echo ✓ OK) else (echo ✗ ERRO)

echo [5/6] S3_BUCKET_FRONTEND
echo midiaflow-frontend-969430605054 | gh secret set S3_BUCKET_FRONTEND
if %errorlevel% equ 0 (echo ✓ OK) else (echo ✗ ERRO)

echo [6/6] CLOUDFRONT_DISTRIBUTION_ID
echo E2HZKZ9ZJK18IU | gh secret set CLOUDFRONT_DISTRIBUTION_ID
if %errorlevel% equ 0 (echo ✓ OK) else (echo ✗ ERRO)

echo.
echo ================================================================================
echo SECRETS CONFIGURADOS
echo ================================================================================
echo.
echo Verificando...
gh secret list
echo.
echo ✓ Pronto para CI/CD!
