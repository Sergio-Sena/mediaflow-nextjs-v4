# 🔐 GitHub Secrets Configuration

## Required Secrets for CI/CD

Configure these secrets in: **Settings → Secrets and variables → Actions**

### AWS Credentials
```
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
```

### Production Environment
```
JWT_SECRET=<production-jwt-secret>
NEXT_PUBLIC_API_URL=https://your-api-gateway.execute-api.us-east-1.amazonaws.com/prod
S3_BUCKET_FRONTEND=midiaflow-frontend
CLOUDFRONT_DISTRIBUTION_ID=<your-cloudfront-id>
```

### Staging Environment (Optional)
```
STAGING_JWT_SECRET=<staging-jwt-secret>
STAGING_API_URL=https://your-api-gateway.execute-api.us-east-1.amazonaws.com/staging
S3_BUCKET_STAGING=midiaflow-staging-frontend
```

## How to Add Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the exact name above
5. Save

## Security Notes

- ⚠️ Never commit secrets to the repository
- ✅ Use different secrets for staging/production
- 🔄 Rotate secrets regularly (every 90 days)
- 🔒 Use AWS IAM roles with minimal permissions

## IAM Policy for GitHub Actions

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
      "Action": [
        "cloudfront:CreateInvalidation"
      ],
      "Resource": "arn:aws:cloudfront::*:distribution/*"
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

## Verification

After adding secrets, trigger a workflow to verify:

```bash
# Push to develop branch (triggers staging)
git checkout -b develop
git push origin develop

# Or manually trigger from GitHub Actions tab
```
