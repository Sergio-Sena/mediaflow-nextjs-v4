@echo off
echo ========================================
echo  DEPLOY TO GREEN (STAGING)
echo ========================================
echo.

echo [1/4] Building Next.js...
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    exit /b 1
)

echo.
echo [2/4] Syncing static files to GREEN...
aws s3 sync .next/static s3://midiaflow-green-969430605054/_next/static --delete

echo.
echo [3/4] Syncing HTML pages to GREEN...
aws s3 sync out s3://midiaflow-green-969430605054 --delete --exclude "_next/*"

echo.
echo [4/4] Deploy complete!
echo.
echo GREEN URL: http://midiaflow-green-969430605054.s3-website-us-east-1.amazonaws.com
echo.
echo ========================================
echo  TEST ON GREEN BEFORE DEPLOYING TO BLUE
echo ========================================
exit /b 0
