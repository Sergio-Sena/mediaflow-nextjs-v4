@echo off
echo ========================================
echo  DEPLOY TO BLUE (PRODUCTION)
echo ========================================
echo.

set /p confirm="Have you tested on GREEN? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo.
    echo Deploy cancelled. Please test on GREEN first!
    echo Run: scripts\deploy-green.bat
    exit /b 1
)

echo.
echo [1/4] Syncing static files to BLUE...
aws s3 sync .next/static s3://mediaflow-frontend-969430605054/_next/static --delete

echo.
echo [2/4] Syncing HTML pages to BLUE...
aws s3 sync out s3://mediaflow-frontend-969430605054 --delete --exclude "_next/*"

echo.
echo [3/4] Invalidating CloudFront cache...
aws cloudfront create-invalidation --distribution-id E1A2CZM0WKF6LX --paths "/*"

echo.
echo [4/4] Deploy complete!
echo.
echo PRODUCTION URL: https://midiaflow.sstechnologies-cloud.com
echo.
echo ========================================
echo  PRODUCTION DEPLOY SUCCESSFUL
echo ========================================
echo.
echo Wait 2-3 minutes for CloudFront invalidation to complete.
exit /b 0
