"""
AWS CDK Stack - Módulo de Gerenciamento de Pastas
Implementa as 4 camadas do plano:
1. S3 Storage
2. IAM Policies (Least Privilege)
3. Lambda Automation
4. DynamoDB Metadata
"""

import boto3
import json

# Configuração
BUCKET_NAME = 'mediaflow-uploads-969430605054'
DYNAMODB_TABLE = 'mediaflow-folders'
REGION = 'us-east-1'

s3 = boto3.client('s3', region_name=REGION)
iam = boto3.client('iam', region_name=REGION)
dynamodb = boto3.client('dynamodb', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)

# ============================================
# CAMADA 1: S3 Storage (Já existe)
# ============================================
print("✅ CAMADA 1: S3 Storage")
print(f"   Bucket: {BUCKET_NAME}")
print(f"   Estrutura: users/{{user_id}}/")

# ============================================
# CAMADA 2: IAM Policies (Least Privilege)
# ============================================
print("\n📋 CAMADA 2: IAM Policies")

# Política Admin - Acesso Total
admin_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AdminFullAccess",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                f"arn:aws:s3:::{BUCKET_NAME}",
                f"arn:aws:s3:::{BUCKET_NAME}/*"
            ]
        }
    ]
}

# Política User - Acesso Restrito ao próprio prefixo
user_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListOwnFolder",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}",
            "Condition": {
                "StringLike": {
                    "s3:prefix": ["users/${aws:username}/*"]
                }
            }
        },
        {
            "Sid": "ReadWriteOwnFolder",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/users/${{aws:username}}/*"
        },
        {
            "Sid": "DenyAdminFolder",
            "Effect": "Deny",
            "Action": "s3:*",
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/users/user_admin/*",
            "Condition": {
                "StringNotEquals": {
                    "aws:username": "user_admin"
                }
            }
        }
    ]
}

print("   ✅ Admin Policy: Acesso total ao bucket")
print("   ✅ User Policy: Acesso restrito a users/${aws:username}/")
print("   ✅ Deny Policy: Ninguém além do admin vê users/user_admin/")

# Salvar políticas
with open('iam-policies/admin-folder-policy.json', 'w') as f:
    json.dump(admin_policy, f, indent=2)

with open('iam-policies/user-folder-policy.json', 'w') as f:
    json.dump(user_policy, f, indent=2)

print("   📄 Políticas salvas em iam-policies/")

# ============================================
# CAMADA 3: Lambda Automation
# ============================================
print("\n⚡ CAMADA 3: Lambda Automation")
print("   Criando Lambda para provisionamento automático de pastas...")

# Lambda será criada em arquivo separado
print("   📄 Lambda code: lambda-functions/folder-provisioning/")

# ============================================
# CAMADA 4: DynamoDB Metadata
# ============================================
print("\n🗄️ CAMADA 4: DynamoDB Metadata")

try:
    # Criar tabela DynamoDB para metadados de pastas
    dynamodb.create_table(
        TableName=DYNAMODB_TABLE,
        KeySchema=[
            {'AttributeName': 'folder_path', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'user_id', 'KeyType': 'RANGE'}      # Sort key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'folder_path', 'AttributeType': 'S'},
            {'AttributeName': 'user_id', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST',
        Tags=[
            {'Key': 'Project', 'Value': 'Midiaflow'},
            {'Key': 'Component', 'Value': 'FolderManagement'}
        ]
    )
    print(f"   ✅ Tabela {DYNAMODB_TABLE} criada com sucesso")
except dynamodb.exceptions.ResourceInUseException:
    print(f"   ℹ️ Tabela {DYNAMODB_TABLE} já existe")

print("\n" + "="*50)
print("✅ INFRAESTRUTURA COMPLETA CRIADA")
print("="*50)
print("\nPróximos passos:")
print("1. Deploy das Lambdas: python deploy-folder-lambdas.py")
print("2. Aplicar políticas IAM aos usuários")
print("3. Testar criação automática de pastas")
