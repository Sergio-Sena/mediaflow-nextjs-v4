@echo off
echo ==========================================
echo   MidiaFlow - Terraform Import
echo ==========================================
echo.

set TFVARS=-var-file=environments/production/terraform.tfvars -var="jwt_secret=17b8312c72fdcffbff89f2f4a564fb26e936002d344717ab7753a237fcd57aea"

echo [1/7] Importing IAM...
terraform import %TFVARS% module.iam.aws_iam_role.lambda mediaflow-lambda-role
terraform import %TFVARS% module.iam.aws_iam_role_policy_attachment.lambda_basic mediaflow-lambda-role/arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
terraform import %TFVARS% module.iam.aws_iam_role_policy_attachment.s3_full mediaflow-lambda-role/arn:aws:iam::aws:policy/AmazonS3FullAccess
terraform import %TFVARS% module.iam.aws_iam_role_policy_attachment.dynamodb_full mediaflow-lambda-role/arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
terraform import %TFVARS% module.iam.aws_iam_role_policy_attachment.mediaconvert mediaflow-lambda-role/arn:aws:iam::aws:policy/AWSElementalMediaConvertFullAccess
terraform import %TFVARS% module.iam.aws_iam_role_policy_attachment.secrets mediaflow-lambda-role/arn:aws:iam::aws:policy/SecretsManagerReadWrite
echo.

echo [2/7] Importing S3 Buckets...
terraform import %TFVARS% module.storage.aws_s3_bucket.frontend mediaflow-frontend-969430605054
terraform import %TFVARS% module.storage.aws_s3_bucket.uploads mediaflow-uploads-969430605054
echo.

echo [3/7] Importing DynamoDB...
terraform import %TFVARS% module.database.aws_dynamodb_table.users mediaflow-users
echo.

echo [4/7] Importing Lambda Functions...
for %%f in (auth-handler files-handler upload-handler view-handler multipart-handler convert-handler cleanup-handler create-user list-users get-user get-user-me update-user avatar-presigned verify-user-2fa check-limits send-trial-emails) do (
    echo   Importing mediaflow-%%f...
    terraform import %TFVARS% "module.lambda.aws_lambda_function.functions[\"%%f\"]" mediaflow-%%f
)
echo   Importing approve-user...
terraform import %TFVARS% module.lambda.aws_lambda_function.approve_user approve-user
echo.

echo [5/7] Importing API Gateway...
terraform import %TFVARS% module.api.aws_api_gateway_rest_api.main gdb962d234
echo.

echo [6/7] Importing CloudFront...
terraform import %TFVARS% module.cdn.aws_cloudfront_distribution.main E1A2CZM0WKF6LX
echo.

echo [7/7] Importing SES...
terraform import %TFVARS% module.ses.aws_ses_email_identity.finops senanetworker@gmail.com
echo.

echo ==========================================
echo   Import concluido! Rode terraform plan
echo ==========================================
