@echo off
echo Preparando commit...
echo.

git add .
git status

echo.
echo Arquivos prontos para commit. Execute:
echo git commit -m "v4.9: Limpeza duplicados, organizacao e uploads (30/01/2025)"
echo git push origin main
echo.
pause
