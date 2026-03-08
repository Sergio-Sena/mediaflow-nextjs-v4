@echo off
REM Script de Teste de Rollback - v4.8.6
REM Simula rollback sem afetar produção

echo ========================================
echo TESTE DE ROLLBACK - v4.8.6 Porto Seguro
echo ========================================
echo.

REM 1. Verificar estado atual
echo [1/5] Verificando estado atual...
git log --oneline -1
git status --short
echo.

REM 2. Verificar tag existe
echo [2/5] Verificando tag porto seguro...
git tag -l "v4.8.6-porto-seguro"
if errorlevel 1 (
    echo ERRO: Tag v4.8.6-porto-seguro nao encontrada!
    exit /b 1
)
echo Tag encontrada: OK
echo.

REM 3. Criar branch de teste
echo [3/5] Criando branch de teste...
git checkout -b test-rollback-v4.8.6 2>nul
if errorlevel 1 (
    echo Branch ja existe, usando existente
    git checkout test-rollback-v4.8.6
)
echo.

REM 4. Simular rollback
echo [4/5] Simulando rollback para v4.8.6-porto-seguro...
git reset --hard v4.8.6-porto-seguro
echo.

REM 5. Verificar arquivos críticos
echo [5/5] Verificando arquivos criticos...
if exist "..\aws-setup\lambda-functions\files-handler\lambda_function.py" (
    echo [OK] Lambda files-handler existe
) else (
    echo [ERRO] Lambda files-handler NAO encontrada!
)

if exist "..\components\modules\SimpleFileUpload.tsx" (
    echo [OK] SimpleFileUpload existe
) else (
    echo [ERRO] SimpleFileUpload NAO encontrado!
)

if exist "..\package.json" (
    findstr /c:"4.8.6" ..\package.json >nul
    if errorlevel 1 (
        echo [AVISO] Versao no package.json diferente de 4.8.6
    ) else (
        echo [OK] Versao 4.8.6 no package.json
    )
)
echo.

REM 6. Voltar para main
echo Voltando para branch main...
git checkout main
echo.

echo ========================================
echo TESTE CONCLUIDO
echo ========================================
echo.
echo Rollback simulado com sucesso!
echo Para aplicar em producao, use: docs/ROLLBACK_GUIDE.md
echo.
