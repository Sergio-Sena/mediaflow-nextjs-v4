# 🚀 Deployment Guide - Mídiaflow v4.9

## 📋 Pre-Deployment Checklist

### 1. GitHub Repository Setup
- [ ] Repository created on GitHub
- [ ] Local repository connected to GitHub
- [ ] `.gitignore` configured
- [ ] All code committed

### 2. GitHub Secrets Configuration
Go to **Settings → Secrets and variables → Actions** and add:

#### Required Secrets
```
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
JWT_SECRET=<your-jwt-secret>
NEXT_PUBLIC_API_URL=https://your-api.execute-api.us-east-1.amazonaws.com/prod
S3_BUCKET_FRONTEND=midiaflow-frontend
CLOUDFRONT_DISTRIBUTION_ID=<your-distribution-id>
```

#### Optional (Staging)
```
STAGING_JWT_SECRET=<staging-jwt>
STAGING_API_URL=https://your-api.execute-api.us-east-1.amazonaws.com/staging
S3_BUCKET_STAGING=midiaflow-staging-frontend
```

### 3. AWS IAM Setup
Create IAM user for GitHub Actions with this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::midiaflow-frontend/*",
        "arn:aws:s3:::midiaflow-frontend"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "cloudfront:CreateInvalidation",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "lambda:UpdateFunctionCode",
        "lambda:GetFunction"
      ],
      "Resource": "arn:aws:lambda:us-east-1:*:function:midiaflow-*"
    }
  ]
}
```

## 🌿 Branch Strategy

```
main (production) ← Auto-deploy on push
  ↑
develop (staging) ← Auto-deploy on push
  ↑
feature/* (local dev)
```

## 🚀 Deployment Methods

### Method 1: Automatic (Recommended)

#### Deploy to Staging
```bash
# Create and switch to develop branch
git checkout -b develop
git push origin develop

# Make changes
git add .
git commit -m "feat: new feature"
git push origin develop
# ✅ Auto-deploys to staging
```

#### Deploy to Production
```bash
# Create PR from develop to main
# After review and merge
# ✅ Auto-deploys to production
```

### Method 2: Manual Trigger

1. Go to **Actions** tab on GitHub
2. Select workflow (Deploy to Production/Staging)
3. Click **Run workflow**
4. Select branch
5. Click **Run workflow** button

## 🔄 Rollback Procedure

### Emergency Rollback

1. Go to **Actions** tab
2. Select **Rollback Deployment**
3. Click **Run workflow**
4. Fill inputs:
   - **Environment**: production or staging
   - **Version**: Git commit SHA (e.g., `abc123def`)
5. Click **Run workflow**

### Find Commit SHA
```bash
# List recent commits
git log --oneline -10

# Output example:
# abc123d feat: new feature (current - broken)
# def456e fix: bug fix (last working version)
# ghi789f feat: another feature

# Use def456e for rollback
```

## 📊 Monitoring Deployments

### GitHub Actions UI
1. Go to **Actions** tab
2. See all workflow runs
3. Click on run for details
4. Check logs for each step

### Deployment Status
- ✅ **Success**: All green, site is live
- ❌ **Failed**: Check logs, fix issue, retry
- 🟡 **In Progress**: Wait for completion

### Health Checks
After deployment, verify:
- [ ] Frontend loads: https://midiaflow.sstechnologies-cloud.com
- [ ] Login works
- [ ] Upload works
- [ ] Video playback works
- [ ] CloudFront cache cleared

## 🐛 Troubleshooting

### Build Fails
```bash
# Test locally first
npm ci
npm run lint
npm run type-check
npm run build
```

### Lambda Deployment Fails
**Error**: `Function not found`
- Check Lambda function names in AWS Console
- Verify they match workflow (e.g., `midiaflow-login`)

**Error**: `Access denied`
- Check IAM permissions
- Verify AWS credentials in GitHub Secrets

### S3 Sync Fails
**Error**: `Bucket not found`
- Verify bucket name in secrets
- Check bucket exists in AWS Console

**Error**: `Access denied`
- Check IAM S3 permissions
- Verify bucket policy

### CloudFront Invalidation Fails
**Error**: `Distribution not found`
- Check distribution ID in secrets
- Verify distribution exists

**Error**: `Too many invalidations`
- Wait 15 minutes between invalidations
- AWS limit: 3 concurrent invalidations

## ⏱️ Deployment Timeline

| Step | Duration |
|------|----------|
| Tests (lint + type-check) | ~2 min |
| Build Next.js | ~3 min |
| Deploy Frontend to S3 | ~1 min |
| Deploy 9 Lambdas (parallel) | ~2 min |
| CloudFront Invalidation | ~1 min |
| Health Check | ~30 sec |
| **Total** | **~8-10 min** |

## 🔐 Security Best Practices

1. **Secrets Management**
   - Never commit secrets to repository
   - Use different secrets for staging/production
   - Rotate secrets every 90 days

2. **IAM Permissions**
   - Use minimal required permissions
   - Create dedicated IAM user for CI/CD
   - Enable MFA on AWS account

3. **Branch Protection**
   - Require PR reviews for main branch
   - Require status checks to pass
   - Restrict who can push to main

## 📈 Performance Optimization

1. **Caching**
   - npm dependencies cached between runs
   - Build artifacts retained 7 days (prod) / 3 days (staging)

2. **Parallel Execution**
   - Lambda deployments run in parallel
   - Reduces total deployment time

3. **Conditional Steps**
   - CloudFront invalidation only on production
   - Health checks skip if previous steps fail

## 🎯 Next Steps

1. ✅ Configure GitHub Secrets
2. ✅ Create `develop` branch
3. ✅ Test PR workflow
4. ✅ Deploy to staging
5. ✅ Test staging environment
6. ✅ Deploy to production
7. ✅ Monitor production
8. ✅ Document any issues

## 📞 Support

If deployment fails:
1. Check GitHub Actions logs
2. Verify AWS Console (S3, Lambda, CloudFront)
3. Test locally with same environment
4. Review this guide
5. Check AWS service status

## 🎉 Success Criteria

Deployment is successful when:
- ✅ All GitHub Actions steps pass
- ✅ Frontend loads without errors
- ✅ Login/authentication works
- ✅ File upload works
- ✅ Video playback works
- ✅ No console errors
- ✅ Lighthouse score 95+
