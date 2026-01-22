@echo off
setlocal enabledelayedexpansion

set "FOLDER=C:\Users\dell 5557\Videos\IDM\Star\Kate Kuray"

echo ========================================
echo RENOMEANDO ARQUIVOS
echo ========================================
echo.
echo Pasta: %FOLDER%
echo.
echo Removendo:
echo - "EPORNER.COM - "
echo - "[...]" (colchetes e conteudo)
echo.

cd /d "%FOLDER%"

set COUNT=0

for %%F in (*.*) do (
    set "ORIGINAL=%%F"
    set "NOVO=%%F"
    
    REM Remove "EPORNER.COM - "
    set "NOVO=!NOVO:EPORNER.COM - =!"
    
    REM Remove tudo entre colchetes incluindo os colchetes
    set "NOVO=!NOVO:[=!"
    for /f "tokens=1* delims=]" %%A in ("!NOVO!") do set "NOVO=%%A%%B"
    
    REM Remove espacos duplos
    set "NOVO=!NOVO:  = !"
    
    REM Remove espacos no inicio
    for /f "tokens=* delims= " %%A in ("!NOVO!") do set "NOVO=%%A"
    
    if not "!ORIGINAL!"=="!NOVO!" (
        echo [!COUNT!] Renomeando:
        echo     DE: !ORIGINAL!
        echo     PARA: !NOVO!
        ren "!ORIGINAL!" "!NOVO!"
        set /a COUNT+=1
        echo.
    )
)

echo.
echo ========================================
echo CONCLUIDO: !COUNT! arquivos renomeados
echo ========================================
pause
