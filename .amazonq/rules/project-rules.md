# MidiaFlow - Project Rules

## Architecture
- 100% serverless AWS (S3, CloudFront, Lambda, API Gateway, DynamoDB, SES, Bedrock)
- Frontend: Next.js 14 Static Export → S3 → CloudFront (CDN unificado)
- Backend: 18 Lambda Functions (Python 3.11)
- Auth: JWT HMAC-SHA256 via environment variable JWT_SECRET
- All resources tagged with Project=MidiaFlow
- CDN unificado: E9ZQJ3RPSA04N (bucket sstech-cdn-unified, path /midiaflow/)
- DynamoDB: mediaflow-users (auth) + mediaflow-public-content (social)

## Security Rules
- NEVER use fallback values for JWT_SECRET. Use `os.environ['JWT_SECRET']` (fail-fast)
- NEVER hardcode credentials, ARNs, or secrets
- All Lambda functions MUST validate JWT token
- All API endpoints MUST have CORS configured
- S3 uploads MUST use presigned URLs with TTL
- Public feed requires login (JWT) - no anonymous access

## Code Standards
- Lambda handler: `lambda_function.lambda_handler` or `index.lambda_handler`
- Always include error handling with proper HTTP status codes
- Always return CORS headers in Lambda responses
- Use `getUserFromToken()` from `lib/auth-utils.ts` for frontend auth
- AvatarUpload is self-contained (extracts userId from JWT internally)
- Use custom Modal components (never native alert/confirm/prompt)
- ContentCarousel is reusable (dashboard + public feed)

## CI/CD
- Pipeline: test → ai-audit → build → deploy → health-check → finops → notify
- Push to main triggers automatic deploy
- Deploy path: sstech-cdn-unified/midiaflow/
- CloudFront invalidation: /midiaflow/*
- Rollback: `git revert HEAD && git push`
- All Lambdas deployed in parallel via matrix strategy
- Branch strategy: dev (development) → main (production)

## FinOps
- Cost Explorer filtered by tag Project=MidiaFlow
- Bedrock Claude 3 Haiku for AI insights
- Report sent via SES (senanetworker@gmail.com) after each deploy
- Target: < $2/month

## AI Agents (6 Bedrock Agents)
- Security Auditor: secrets, IAM, encryption
- FinOps Auditor: right-sizing, storage, idle resources
- Code Quality: error handling, hardcoded values
- Compliance (LGPD/GDPR): personal data, retention
- Performance: cold starts, connection reuse, N+1
- Leader: orchestrates all, decides APPROVED/BLOCKED

## Public Feed (/public-feed)
- Social features: likes, comments, share link
- Feed organized by user → category → carousel
- Owner can share/remove own content
- Admin can moderate (deactivate) any content
- Lambda: mediaflow-share-content (actions: share, like, comment, deactivate)

## When creating new Lambda functions:
1. Add JWT_SECRET to environment variables
2. Tag with Project=MidiaFlow
3. Add to CI/CD pipeline matrix in deploy-production.yml
4. Add to Terraform modules/lambda/main.tf
5. Configure CORS in response headers
