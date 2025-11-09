@echo off
REM Setup CI/CD for Midiaflow (Windows)

echo.
echo ================================
echo Midiaflow CI/CD Setup (Windows)
echo ================================
echo.

REM Check if git is initialized
if not exist .git (
    echo [ERROR] Not a git repository. Run 'git init' first.
    exit /b 1
)

REM Check if remote is configured
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No remote 'origin' configured.
    set /p repo_url="Enter GitHub repository URL: "
    git remote add origin %repo_url%
    echo [OK] Remote added: %repo_url%
)

REM Create develop branch if it doesn't exist
git show-ref --verify --quiet refs/heads/develop >nul 2>&1
if errorlevel 1 (
    echo [INFO] Creating develop branch...
    git checkout -b develop
    git push -u origin develop
    git checkout main
    echo [OK] Develop branch created
) else (
    echo [OK] Develop branch already exists
)

echo.
echo ================================
echo Required GitHub Secrets
echo ================================
echo.
echo Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions
echo.
echo Add these secrets:
echo.
echo 1. AWS_ACCESS_KEY_ID
echo 2. AWS_SECRET_ACCESS_KEY
echo 3. JWT_SECRET
echo 4. NEXT_PUBLIC_API_URL
echo 5. S3_BUCKET_FRONTEND
echo 6. CLOUDFRONT_DISTRIBUTION_ID
echo.
echo Optional (for staging):
echo 7. STAGING_JWT_SECRET
echo 8. STAGING_API_URL
echo 9. S3_BUCKET_STAGING
echo.

REM Check if .env.local exists
if exist .env.local (
    echo [INFO] Found .env.local - Use these values for secrets:
    echo.
    findstr /C:"JWT_SECRET" /C:"NEXT_PUBLIC_API_URL" .env.local
    echo.
)

echo [OK] Setup complete!
echo.
echo Next steps:
echo 1. Configure GitHub Secrets (see above)
echo 2. Push to develop branch to test staging deployment
echo 3. Create PR from develop to main for production deployment
echo.
echo See DEPLOYMENT.md for detailed instructions
echo.
pause
