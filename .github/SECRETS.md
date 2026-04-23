# 🔐 GitHub Secrets Configuration

## Required Secrets for CI/CD

Configure em: **Settings → Secrets and variables → Actions**

### AWS Credentials
```
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
```

### Application
```
JWT_SECRET=<production-jwt-secret>
```

## How to Add Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the exact name above

## Security Notes

- ⚠️ Never commit secrets to the repository
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
        "s3:ListBucket",
        "s3:ListObjectsV2"
      ],
      "Resource": [
        "arn:aws:s3:::mediaflow-frontend-969430605054/*",
        "arn:aws:s3:::mediaflow-frontend-969430605054",
        "arn:aws:s3:::midiaflow-green-969430605054/*",
        "arn:aws:s3:::midiaflow-green-969430605054"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudfront:CreateInvalidation"
      ],
      "Resource": "arn:aws:cloudfront::969430605054:distribution/E1A2CZM0WKF6LX"
    },
    {
      "Effect": "Allow",
      "Action": [
        "lambda:UpdateFunctionCode",
        "lambda:GetFunction",
        "lambda:GetFunctionConfiguration"
      ],
      "Resource": [
        "arn:aws:lambda:us-east-1:969430605054:function:mediaflow-*",
        "arn:aws:lambda:us-east-1:969430605054:function:approve-user"
      ]
    }
  ]
}
```
