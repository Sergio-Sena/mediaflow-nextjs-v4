# MidiaFlow - Project Rules

## Architecture
- 100% serverless AWS (S3, CloudFront, Lambda, API Gateway, DynamoDB)
- Frontend: Next.js 14 Static Export
- Backend: 17 Lambda Functions (Python 3.11)
- Auth: JWT HMAC-SHA256 via environment variable JWT_SECRET
- All resources tagged with Project=MidiaFlow

## Security Rules
- NEVER use fallback values for JWT_SECRET. Use `os.environ['JWT_SECRET']` (fail-fast)
- NEVER hardcode credentials, ARNs, or secrets
- All Lambda functions MUST validate JWT token
- All API endpoints MUST have CORS configured
- S3 uploads MUST use presigned URLs with TTL

## Code Standards
- Lambda handler: `lambda_function.lambda_handler` or `index.lambda_handler`
- Always include error handling with proper HTTP status codes
- Always return CORS headers in Lambda responses
- Use `getUserFromToken()` from `lib/auth-utils.ts` for frontend auth
- AvatarUpload is self-contained (extracts userId from JWT internally)

## CI/CD
- Pipeline: test → ai-audit → build → deploy → health-check → finops → notify
- Push to main triggers automatic deploy
- Rollback: `git revert HEAD && git push`
- All Lambdas deployed in parallel via matrix strategy

## FinOps
- Cost Explorer filtered by tag Project=MidiaFlow
- Bedrock Claude 3 Haiku for AI insights
- Report sent via SES after each deploy
- Target: < $2/month

## When creating new Lambda functions:
1. Add JWT_SECRET to environment variables
2. Tag with Project=MidiaFlow
3. Add to CI/CD pipeline matrix
4. Add to Terraform modules/lambda/main.tf
