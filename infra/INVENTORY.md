# MidiaFlow - Inventário de Infraestrutura AWS

**Região:** us-east-1
**Account ID:** 969430605054
**Projeto:** MidiaFlow
**Tag:** Project=MidiaFlow
**Data:** 2026-04-23

---

## 1. Lambda Functions (17)

| Nome | ARN | Runtime | Memory | Timeout | Env Vars |
|---|---|---|---|---|---|
| mediaflow-auth-handler | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-auth-handler | python3.11 | 128MB | 30s | JWT_SECRET |
| mediaflow-files-handler | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-files-handler | python3.11 | 128MB | 30s | UPLOADS_BUCKET, PROCESSED_BUCKET, JWT_SECRET |
| mediaflow-upload-handler | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-upload-handler | python3.11 | 128MB | 30s | ALLOWED_ORIGINS, JWT_SECRET |
| mediaflow-view-handler | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-view-handler | python3.11 | 128MB | 30s | UPLOADS_BUCKET, PROCESSED_BUCKET, JWT_SECRET |
| mediaflow-multipart-handler | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-multipart-handler | python3.11 | 128MB | 30s | UPLOADS_BUCKET, JWT_SECRET |
| mediaflow-convert-handler | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-convert-handler | python3.11 | 128MB | 300s | UPLOADS_BUCKET, PROCESSED_BUCKET, JWT_SECRET |
| mediaflow-cleanup-handler | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-cleanup-handler | python3.11 | 128MB | 30s | UPLOADS_BUCKET, PROCESSED_BUCKET, JWT_SECRET |
| mediaflow-create-user | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-create-user | python3.12 | 256MB | 30s | JWT_SECRET |
| mediaflow-list-users | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-list-users | python3.11 | 128MB | 3s | JWT_SECRET |
| mediaflow-get-user | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-get-user | python3.11 | 128MB | 30s | JWT_SECRET |
| mediaflow-get-user-me | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-get-user-me | python3.9 | 256MB | 10s | JWT_SECRET |
| mediaflow-update-user | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-update-user | python3.11 | 128MB | 30s | JWT_SECRET |
| mediaflow-avatar-presigned | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-avatar-presigned | python3.11 | 128MB | 30s | JWT_SECRET |
| mediaflow-verify-user-2fa | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-verify-user-2fa | python3.11 | 128MB | 30s | JWT_SECRET |
| mediaflow-check-limits | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-check-limits | python3.11 | 128MB | 10s | JWT_SECRET |
| mediaflow-send-trial-emails | arn:aws:lambda:us-east-1:969430605054:function:mediaflow-send-trial-emails | python3.11 | 128MB | 30s | JWT_SECRET |
| approve-user | arn:aws:lambda:us-east-1:969430605054:function:approve-user | python3.11 | 256MB | 30s | JWT_SECRET |

---

## 2. S3 Buckets (2)

| Nome | Uso | Tag |
|---|---|---|
| mediaflow-frontend-969430605054 | Frontend (Static Hosting) | Project=MidiaFlow |
| mediaflow-uploads-969430605054 | Uploads (Videos, Images, Avatars) | Project=MidiaFlow |

---

## 3. CloudFront (1)

| ID | Domain | Alias | Origin | Status |
|---|---|---|---|---|
| E1A2CZM0WKF6LX | dau2z7fot0cqr.cloudfront.net | midiaflow.sstechnologies-cloud.com | mediaflow-frontend-969430605054.s3-website-us-east-1.amazonaws.com | Deployed |

---

## 4. API Gateway (1)

| ID | Nome | Tipo | URL |
|---|---|---|---|
| gdb962d234 | mediaflow-api | REGIONAL | https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod |

### Endpoints (27 rotas)
```
/auth/login
/users
/users/me
/users/create
/users/approve
/users/verify-2fa
/users/{user_id}
/update-user
/files
/files/{key}
/files/delete
/files/bulk-delete
/view/{key+}
/upload
/upload/presigned
/upload/check
/multipart
/multipart/{action}
/avatar-presigned
/convert
/cleanup
/folders
```

---

## 5. DynamoDB (1)

| Tabela | ARN | Modo | Items | Tamanho |
|---|---|---|---|---|
| mediaflow-users | arn:aws:dynamodb:us-east-1:969430605054:table/mediaflow-users | PAY_PER_REQUEST | 3 | 1.1 KB |

---

## 6. IAM Role (1)

| Nome | ARN |
|---|---|
| mediaflow-lambda-role | arn:aws:iam::969430605054:role/mediaflow-lambda-role |

### Policies Attached
- AWSLambdaBasicExecutionRole
- AmazonS3FullAccess
- AmazonDynamoDBFullAccess
- AWSElementalMediaConvertFullAccess
- SecretsManagerReadWrite

---

## 7. SES (1)

| Identidade | Status |
|---|---|
| senanetworker@gmail.com | Verified |

---

## 8. Mapa de Dependências

```
CloudFront → S3 Frontend
API Gateway → 17 Lambdas → DynamoDB
                         → S3 Uploads
CI/CD (GitHub Actions) → S3 Frontend + 17 Lambdas
FinOps: Cost Explorer → Bedrock → SES
```

---

## 9. Resumo para Terraform

| Recurso | Quantidade | Terraform Resource Type |
|---|---|---|
| Lambda | 17 | aws_lambda_function |
| S3 | 2 | aws_s3_bucket |
| CloudFront | 1 | aws_cloudfront_distribution |
| API Gateway | 1 + 27 rotas | aws_api_gateway_rest_api + resources + methods |
| DynamoDB | 1 | aws_dynamodb_table |
| IAM Role | 1 | aws_iam_role |
| IAM Policy Attachment | 5 | aws_iam_role_policy_attachment |
| SES | 1 | aws_ses_email_identity |

**Total: ~55 recursos Terraform**
