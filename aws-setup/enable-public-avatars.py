import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("=== CONFIGURANDO ACESSO PUBLICO PARA AVATARS ===\n")

# 1. Desabilitar Block Public Access apenas para policies
print("1. Ajustando Block Public Access...")
s3.put_public_access_block(
    Bucket=bucket,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': False,  # Permitir bucket policies publicas
        'RestrictPublicBuckets': False
    }
)
print("   OK - Block Public Access ajustado")

# 2. Aplicar Bucket Policy
print("\n2. Aplicando Bucket Policy...")
policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'PublicReadAvatars',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': 's3:GetObject',
        'Resource': f'arn:aws:s3:::{bucket}/avatars/*'
    }]
}

s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
print("   OK - Policy aplicada")

# 3. Testar acesso
print("\n3. Testando acesso...")
import requests
test_url = f"https://{bucket}.s3.amazonaws.com/avatars/avatar_Lid.jpg"
response = requests.head(test_url)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    print("\n=== SUCESSO! Avatars sao publicos ===")
else:
    print(f"\n=== ERRO: Status {response.status_code} ===")
