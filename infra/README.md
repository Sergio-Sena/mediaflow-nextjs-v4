# MidiaFlow - Infrastructure as Code (Terraform)

## Estrutura

```
infra/
├── main.tf                    # Provider + Backend
├── variables.tf               # Variáveis globais
├── outputs.tf                 # Outputs
├── modules.tf                 # Wiring dos módulos
├── modules/
│   ├── iam/main.tf            # IAM Role + Policies
│   ├── storage/main.tf        # S3 Buckets (frontend + uploads)
│   ├── database/main.tf       # DynamoDB
│   ├── lambda/main.tf         # 17 Lambda Functions
│   ├── api/main.tf            # API Gateway
│   ├── cdn/main.tf            # CloudFront
│   └── ses/main.tf            # SES Email
├── environments/
│   ├── production/terraform.tfvars
│   └── dr/terraform.tfvars
└── INVENTORY.md               # Inventário completo
```

## Uso

### Fase 3 - Import (produção existente)
```bash
cd infra
terraform init
terraform import -var-file=environments/production/terraform.tfvars \
  module.storage.aws_s3_bucket.frontend mediaflow-frontend-969430605054
# ... (repetir para cada recurso)
terraform plan -var-file=environments/production/terraform.tfvars
```

### Fase 4 - Deploy DR (nova região)
```bash
terraform plan -var-file=environments/dr/terraform.tfvars
terraform apply -var-file=environments/dr/terraform.tfvars
```

### Fase 5 - Destruir DR (após teste)
```bash
terraform destroy -var-file=environments/dr/terraform.tfvars
```
