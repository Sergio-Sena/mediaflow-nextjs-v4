variable "project_name" { type = string }
variable "lambda_role_arn" { type = string }

variable "jwt_secret" {
  type      = string
  sensitive = true
}

variable "uploads_bucket" { type = string }
variable "processed_bucket" { type = string }
variable "lambda_runtime" { type = string }

locals {
  prefix = lower(var.project_name)

  functions = {
    auth-handler      = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret } }
    files-handler     = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret, UPLOADS_BUCKET = var.uploads_bucket, PROCESSED_BUCKET = var.processed_bucket } }
    upload-handler    = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret, ALLOWED_ORIGINS = "*" } }
    view-handler      = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret, UPLOADS_BUCKET = var.uploads_bucket, PROCESSED_BUCKET = var.processed_bucket } }
    multipart-handler = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret, UPLOADS_BUCKET = var.uploads_bucket } }
    convert-handler   = { handler = "lambda_function.lambda_handler", timeout = 300, memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret, UPLOADS_BUCKET = var.uploads_bucket, PROCESSED_BUCKET = var.processed_bucket } }
    cleanup-handler   = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret, UPLOADS_BUCKET = var.uploads_bucket, PROCESSED_BUCKET = var.processed_bucket } }
    create-user       = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 256, runtime = "python3.12",      env = { JWT_SECRET = var.jwt_secret } }
    list-users        = { handler = "lambda_function.lambda_handler", timeout = 3,   memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret } }
    get-user          = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret } }
    get-user-me       = { handler = "lambda_function.lambda_handler", timeout = 10,  memory = 256, runtime = "python3.9",        env = { JWT_SECRET = var.jwt_secret } }
    update-user       = { handler = "index.lambda_handler",          timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret } }
    avatar-presigned  = { handler = "index.lambda_handler",          timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret } }
    verify-user-2fa   = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret } }
    check-limits      = { handler = "lambda_function.lambda_handler", timeout = 10,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret } }
    send-trial-emails = { handler = "lambda_function.lambda_handler", timeout = 30,  memory = 128, runtime = var.lambda_runtime, env = { JWT_SECRET = var.jwt_secret } }
  }
}

resource "aws_lambda_function" "functions" {
  for_each = local.functions

  function_name = "${local.prefix}-${each.key}"
  role          = var.lambda_role_arn
  handler       = each.value.handler
  runtime       = each.value.runtime
  timeout       = each.value.timeout
  memory_size   = each.value.memory

  # Placeholder - will be replaced by terraform import
  filename         = "${path.module}/placeholder.zip"
  source_code_hash = filebase64sha256("${path.module}/placeholder.zip")

  environment {
    variables = each.value.env
  }
}

# approve-user (different naming convention)
resource "aws_lambda_function" "approve_user" {
  function_name = "approve-user"
  role          = var.lambda_role_arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = 30
  memory_size   = 256

  filename         = "${path.module}/placeholder.zip"
  source_code_hash = filebase64sha256("${path.module}/placeholder.zip")

  environment {
    variables = { JWT_SECRET = var.jwt_secret }
  }
}

output "lambda_arns" {
  value = merge(
    { for k, v in aws_lambda_function.functions : k => v.arn },
    { "approve-user" = aws_lambda_function.approve_user.arn }
  )
}

output "lambda_function_names" {
  value = merge(
    { for k, v in aws_lambda_function.functions : k => v.function_name },
    { "approve-user" = aws_lambda_function.approve_user.function_name }
  )
}
