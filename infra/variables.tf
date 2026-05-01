variable "aws_region" {
  description = "AWS region to deploy"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for tagging"
  type        = string
  default     = "MidiaFlow"
}

variable "environment" {
  description = "Environment (production, dr)"
  type        = string
  default     = "production"
}

variable "account_id" {
  description = "AWS Account ID"
  type        = string
  default     = "969430605054"
}

variable "jwt_secret" {
  description = "JWT secret for authentication"
  type        = string
  sensitive   = true
}

variable "domain_name" {
  description = "Custom domain for CloudFront"
  type        = string
  default     = "midiaflow.sstechnologies-cloud.com"
}

variable "ses_email" {
  description = "Email for SES (FinOps reports)"
  type        = string
  default     = "senanetworker@gmail.com"
}

variable "lambda_runtime" {
  description = "Default Lambda runtime"
  type        = string
  default     = "python3.11"
}
