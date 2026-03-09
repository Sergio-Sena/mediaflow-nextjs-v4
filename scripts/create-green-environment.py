import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
cf = boto3.client('cloudfront', region_name='us-east-1')

ACCOUNT_ID = '969430605054'

print("=== CRIANDO AMBIENTE BLUE/GREEN ===\n")

# 1. Criar bucket GREEN (testes)
green_bucket = f'midiaflow-green-{ACCOUNT_ID}'
print(f"[1/3] Criando bucket GREEN: {green_bucket}")

try:
    s3.create_bucket(Bucket=green_bucket)
    print("  [OK] Bucket criado")
except Exception as e:
    if 'BucketAlreadyOwnedByYou' in str(e):
        print("  [OK] Bucket ja existe")
    else:
        print(f"  [ERRO] {e}")

# 2. Configurar bucket como website
print("\n[2/3] Configurando website...")
try:
    s3.put_bucket_website(
        Bucket=green_bucket,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': '404.html'}
        }
    )
    print("  [OK] Website configurado")
except Exception as e:
    print(f"  [ERRO] {e}")

# 3. Configurar politica publica
print("\n[3/3] Configurando acesso publico...")
policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{green_bucket}/*"
    }]
}

try:
    s3.put_bucket_policy(Bucket=green_bucket, Policy=json.dumps(policy))
    print("  [OK] Acesso publico configurado")
except Exception as e:
    print(f"  [ERRO] {e}")

print("\n" + "="*60)
print("AMBIENTE GREEN CRIADO!")
print("="*60)
print(f"\nBucket: {green_bucket}")
print(f"URL: http://{green_bucket}.s3-website-us-east-1.amazonaws.com")
print("\nProximo passo:")
print("  1. Deploy no GREEN para testar")
print("  2. Se OK, swap BLUE <-> GREEN")
print("  3. Se erro, manter BLUE ativo")
