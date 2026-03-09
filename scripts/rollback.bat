@echo off
echo ========================================
echo  EMERGENCY ROLLBACK
echo ========================================
echo.
echo This will copy GREEN (staging) to BLUE (production)
echo.

set /p confirm="Are you sure? This will overwrite production! (yes/no): "
if /i not "%confirm%"=="yes" (
    echo Rollback cancelled.
    exit /b 1
)

echo.
echo [1/3] Copying GREEN to BLUE...
aws s3 sync s3://midiaflow-green-969430605054 s3://mediaflow-frontend-969430605054 --delete

echo.
echo [2/3] Invalidating CloudFront...
aws cloudfront create-invalidation --distribution-id E1A2CZM0WKF6LX --paths "/*"

echo.
echo [3/3] Rollback complete!
echo.
echo Production now matches GREEN staging environment.
echo.
echo ========================================
exit /b 0
