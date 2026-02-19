@echo off
REM Script de Rollback para v4.8.5
echo ========================================
echo  ROLLBACK PARA v4.8.5
echo ========================================
echo.

echo [1/3] Voltando para tag v4.8.5-backup...
git checkout v4.8.5-backup

echo.
echo [2/3] Criando branch de rollback...
git checkout -b rollback-v4.8.5-%date:~-4,4%%date:~-10,2%%date:~-7,2%

echo.
echo [3/3] Status atual:
git log -1 --oneline

echo.
echo ========================================
echo  ROLLBACK CONCLUIDO
echo ========================================
echo.
echo Commit atual: 3fb0d200
echo Branch: rollback-v4.8.5-[data]
echo.
echo Para voltar ao main:
echo   git checkout main
echo.
pause
