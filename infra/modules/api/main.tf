variable "project_name" { type = string }
variable "aws_region" { type = string }
variable "account_id" { type = string }
variable "lambda_arns" { type = map(string) }

resource "aws_api_gateway_rest_api" "main" {
  name = "${lower(var.project_name)}-api"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = "prod"
}

output "api_url" {
  value = aws_api_gateway_stage.prod.invoke_url
}

output "api_id" {
  value = aws_api_gateway_rest_api.main.id
}
