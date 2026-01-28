@echo off
echo ========================================
echo BACKUP VERSAO ESTAVEL - v4.9.1
echo ========================================
echo.

set BACKUP_DIR=backup-v4.9.1-%date:~-4,4%%date:~-10,2%%date:~-7,2%-%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%

echo [1/5] Criando diretorio de backup...
mkdir "%BACKUP_DIR%"

echo.
echo [2/5] Backup de configuracoes Lambda...
aws lambda get-function-configuration --function-name mediaflow-view-handler > "%BACKUP_DIR%\lambda-view-handler-config.json"
aws lambda get-function-configuration --function-name midiaflow-auth-handler > "%BACKUP_DIR%\lambda-auth-handler-config.json"

echo.
echo [3/5] Backup de codigo Lambda...
aws lambda get-function --function-name mediaflow-view-handler --query "Code.Location" --output text > "%BACKUP_DIR%\lambda-view-handler-url.txt"
aws lambda get-function --function-name midiaflow-auth-handler --query "Code.Location" --output text > "%BACKUP_DIR%\lambda-auth-handler-url.txt"

echo.
echo [4/5] Backup de arquivos locais criticos...
copy "next.config.js" "%BACKUP_DIR%\"
copy "package.json" "%BACKUP_DIR%\"
copy ".env.local" "%BACKUP_DIR%\" 2>nul
copy "backup-view-handler-config.json" "%BACKUP_DIR%\" 2>nul

echo.
echo [5/5] Criando arquivo de informacoes...
(
echo BACKUP VERSAO ESTAVEL v4.9.1
echo Data: %date% %time%
echo.
echo CORRECOES INCLUIDAS:
echo - JWT_SECRET sincronizado entre auth-handler e view-handler
echo - Sanitizacao de nomes de arquivos ativada no upload
echo - Documentacao atualizada
echo.
echo LAMBDAS:
echo - mediaflow-view-handler: JWT_SECRET=17b8312c72f...
echo - midiaflow-auth-handler: JWT_SECRET=17b8312c72f...
echo.
echo STATUS: PRODUCAO ESTAVEL
) > "%BACKUP_DIR%\README.txt"

echo.
echo ========================================
echo BACKUP CONCLUIDO!
echo ========================================
echo.
echo Diretorio: %BACKUP_DIR%
echo.
pause
