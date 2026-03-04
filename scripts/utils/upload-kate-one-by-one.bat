@echo off
setlocal enabledelayedexpansion

set FOLDER=C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray
set S3_PATH=s3://mediaflow-uploads-969430605054/users/sergio_sena/Star/Kate Kuray/

echo ================================================================================
echo UPLOAD UM POR UM VIA AWS CLI
echo ================================================================================
echo.
echo [AUTO] Confirmacao automatica ativada
echo.

set COUNT=0
set SUCCESS=0
set ERRORS=0

for %%F in ("%FOLDER%\*.mp4") do (
    set /a COUNT+=1
    echo [!COUNT!] Uploading: %%~nxF
    
    aws s3 cp "%%F" "%S3_PATH%%%~nxF"
    
    if !ERRORLEVEL! EQU 0 (
        set /a SUCCESS+=1
        echo   [OK] Upload concluido
    ) else (
        set /a ERRORS+=1
        echo   [ERRO] Falha no upload
    )
    echo.
)

echo ================================================================================
echo CONCLUIDO: !SUCCESS! uploads, !ERRORS! erros
echo ================================================================================
echo.
echo Fechando em 3 segundos...
timeout /t 3 /nobreak >nul
exit
