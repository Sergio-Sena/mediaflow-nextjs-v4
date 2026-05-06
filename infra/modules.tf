module "iam" {
  source       = "./modules/iam"
  project_name = var.project_name
}

module "storage" {
  source       = "./modules/storage"
  project_name = var.project_name
  account_id   = var.account_id
  aws_region   = var.aws_region
}

module "database" {
  source       = "./modules/database"
  project_name = var.project_name
}

module "lambda" {
  source            = "./modules/lambda"
  project_name      = var.project_name
  lambda_role_arn   = module.iam.lambda_role_arn
  jwt_secret        = var.jwt_secret
  uploads_bucket    = module.storage.uploads_bucket_name
  processed_bucket  = "${var.project_name}-processed-${var.account_id}"
  lambda_runtime    = var.lambda_runtime
}

module "api" {
  source       = "./modules/api"
  project_name = var.project_name
  aws_region   = var.aws_region
  account_id   = var.account_id
  lambda_arns  = module.lambda.lambda_arns
}

module "cdn" {
  source              = "./modules/cdn"
  project_name        = var.project_name
  frontend_bucket     = module.storage.frontend_bucket_website_endpoint
  domain_name         = var.domain_name
  acm_certificate_arn = var.acm_certificate_arn
}

module "ses" {
  source    = "./modules/ses"
  ses_email = var.ses_email
}
