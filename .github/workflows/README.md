# 🚀 CI/CD Workflows

## Available Workflows

### 1. **Deploy to Production** (`deploy-production.yml`)
- **Trigger**: Push to `main` branch or manual dispatch
- **Steps**:
  1. Run tests (lint + type-check)
  2. Build Next.js application
  3. Deploy frontend to S3
  4. Deploy all 9 Lambda functions
  5. Invalidate CloudFront cache
  6. Health check
  7. Notify status

### 2. **Deploy to Staging** (`deploy-staging.yml`)
- **Trigger**: Push to `develop` branch or manual dispatch
- **Steps**: Same as production but deploys to staging environment

### 3. **Pull Request Check** (`pr-check.yml`)
- **Trigger**: Pull request to `main` or `develop`
- **Steps**: Lint, type-check, and build verification

### 4. **Rollback** (`rollback.yml`)
- **Trigger**: Manual dispatch only
- **Inputs**:
  - Environment (production/staging)
  - Git commit SHA or tag
- **Use case**: Emergency rollback to previous version

## Branch Strategy

```
main (production)
  ↑
  PR + review
  ↑
develop (staging)
  ↑
  PR + review
  ↑
feature/* (local dev)
```

## Deployment Flow

### Normal Flow
```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Develop and commit
git add .
git commit -m "feat: add new feature"

# 3. Push and create PR to develop
git push origin feature/new-feature
# Create PR on GitHub → develop

# 4. After merge to develop → auto-deploy to staging
# Test on staging environment

# 5. Create PR from develop → main
# After merge → auto-deploy to production
```

### Emergency Rollback
```bash
# 1. Go to GitHub Actions tab
# 2. Select "Rollback Deployment" workflow
# 3. Click "Run workflow"
# 4. Select environment and commit SHA
# 5. Confirm
```

## Monitoring Deployments

### GitHub Actions UI
1. Go to **Actions** tab
2. See all workflow runs
3. Click on a run to see details
4. Check logs for each step

### Deployment Status
- ✅ Green checkmark = Success
- ❌ Red X = Failed
- 🟡 Yellow dot = In progress

## Secrets Required

See [SECRETS.md](../SECRETS.md) for complete list.

**Critical secrets:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `JWT_SECRET`
- `NEXT_PUBLIC_API_URL`
- `S3_BUCKET_FRONTEND`
- `CLOUDFRONT_DISTRIBUTION_ID`

## Troubleshooting

### Build fails
```bash
# Run locally first
npm ci
npm run lint
npm run type-check
npm run build
```

### Lambda deployment fails
- Check IAM permissions
- Verify Lambda function names match
- Check Lambda runtime (Python 3.12)

### S3 sync fails
- Verify bucket name
- Check IAM S3 permissions
- Ensure bucket exists

### CloudFront invalidation fails
- Check distribution ID
- Verify IAM CloudFront permissions
- Wait for previous invalidation to complete

## Performance

### Typical deployment times:
- **Tests**: ~2 minutes
- **Build**: ~3 minutes
- **Deploy Frontend**: ~1 minute
- **Deploy Lambdas**: ~2 minutes (parallel)
- **Health Check**: ~30 seconds
- **Total**: ~8-10 minutes

## Cost Optimization

- Artifacts retained for 7 days (production) / 3 days (staging)
- Parallel Lambda deployments
- Cached npm dependencies
- Only invalidate CloudFront on production

## Next Steps

1. ✅ Configure GitHub Secrets
2. ✅ Create `develop` branch
3. ✅ Test PR workflow
4. ✅ Test staging deployment
5. ✅ Test production deployment
6. ✅ Document rollback procedure
