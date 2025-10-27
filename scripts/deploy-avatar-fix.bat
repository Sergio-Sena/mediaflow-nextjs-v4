@echo off
echo ========================================
echo  Deploy Avatar Fix - Midiaflow v4.7.2
echo ========================================
echo.

echo [1/3] Building frontend...
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo.

echo [2/3] Syncing to S3...
aws s3 sync out/ s3://mediaflow-frontend-969430605054/ --delete
if %errorlevel% neq 0 (
    echo ERROR: S3 sync failed!
    pause
    exit /b 1
)
echo.

echo [3/3] Invalidating CloudFront cache...
aws cloudfront create-invalidation --distribution-id E2HZKZ9ZJK18IU --paths "/*"
if %errorlevel% neq 0 (
    echo ERROR: CloudFront invalidation failed!
    pause
    exit /b 1
)
echo.

echo ========================================
echo  Deploy completed successfully!
echo ========================================
echo.
echo Avatar fix is now live at:
echo https://midiaflow.sstechnologies-cloud.com
echo.
pause
