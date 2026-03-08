@echo off
REM Deploy de Teste - UniversalUpload
REM Testa build de produção SEM afetar produção real

echo ========================================
echo DEPLOY DE TESTE - UniversalUpload
echo ========================================
echo.

REM 1. Build de produção
echo [1/4] Build de producao...
call npm run build
if errorlevel 1 (
    echo ERRO: Build falhou!
    exit /b 1
)
echo Build OK
echo.

REM 2. Verificar se UniversalUpload está no build
echo [2/4] Verificando UniversalUpload no build...
findstr /c:"UniversalUpload" .next\server\app\dashboard.html >nul
if errorlevel 1 (
    echo AVISO: UniversalUpload nao encontrado no build
) else (
    echo UniversalUpload encontrado no build
)
echo.

REM 3. Testar build localmente
echo [3/4] Iniciando servidor de producao local...
echo Teste em: http://localhost:3000
echo.
echo Pressione Ctrl+C para parar o servidor apos testar
echo.
call npm start

REM 4. Perguntar se deploy em prod
echo.
echo ========================================
echo TESTES LOCAIS CONCLUIDOS
echo ========================================
echo.
echo Se tudo funcionou, voce pode fazer deploy:
echo   1. git checkout main
echo   2. git merge feature/modularizacao-upload
echo   3. npm run build
echo   4. Deploy para S3
echo.
echo Se algo quebrou:
echo   git checkout main (rollback instantaneo)
echo.
