#!/bin/bash

# Setup CI/CD for Mídiaflow
# This script helps configure GitHub repository and secrets

set -e

echo "🚀 Mídiaflow CI/CD Setup"
echo "========================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Not a git repository. Run 'git init' first."
    exit 1
fi

# Check if remote is configured
if ! git remote get-url origin &> /dev/null; then
    echo "⚠️  No remote 'origin' configured."
    read -p "Enter GitHub repository URL: " repo_url
    git remote add origin "$repo_url"
    echo "✅ Remote added: $repo_url"
fi

# Create develop branch if it doesn't exist
if ! git show-ref --verify --quiet refs/heads/develop; then
    echo "📝 Creating develop branch..."
    git checkout -b develop
    git push -u origin develop
    git checkout main || git checkout master
    echo "✅ Develop branch created"
else
    echo "✅ Develop branch already exists"
fi

# Display secrets that need to be configured
echo ""
echo "🔐 Required GitHub Secrets"
echo "=========================="
echo ""
echo "Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions"
echo ""
echo "Add these secrets:"
echo ""
echo "1. AWS_ACCESS_KEY_ID"
echo "2. AWS_SECRET_ACCESS_KEY"
echo "3. JWT_SECRET"
echo "4. NEXT_PUBLIC_API_URL"
echo "5. S3_BUCKET_FRONTEND"
echo "6. CLOUDFRONT_DISTRIBUTION_ID"
echo ""
echo "Optional (for staging):"
echo "7. STAGING_JWT_SECRET"
echo "8. STAGING_API_URL"
echo "9. S3_BUCKET_STAGING"
echo ""

# Check if .env.local exists
if [ -f .env.local ]; then
    echo "📄 Found .env.local - Use these values for secrets:"
    echo ""
    grep -E "JWT_SECRET|NEXT_PUBLIC_API_URL" .env.local || echo "⚠️  No matching variables found"
    echo ""
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure GitHub Secrets (see above)"
echo "2. Push to develop branch to test staging deployment"
echo "3. Create PR from develop to main for production deployment"
echo ""
echo "📚 See DEPLOYMENT.md for detailed instructions"
