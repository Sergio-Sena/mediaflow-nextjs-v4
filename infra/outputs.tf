output "cloudfront_domain" {
  value = module.cdn.cloudfront_domain
}

output "api_gateway_url" {
  value = module.api.api_url
}

output "frontend_bucket" {
  value = module.storage.frontend_bucket_name
}

output "uploads_bucket" {
  value = module.storage.uploads_bucket_name
}

output "dynamodb_table" {
  value = module.database.table_name
}
