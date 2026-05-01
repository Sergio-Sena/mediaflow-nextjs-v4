variable "ses_email" { type = string }

resource "aws_ses_email_identity" "finops" {
  email = var.ses_email
}

output "ses_email" {
  value = aws_ses_email_identity.finops.email
}
