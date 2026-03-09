#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("1. Localizando arquivo EPORNER.COM_-_DfHQR...")

# Buscar arquivo
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/Corporativo/')

found = None
for page in pages:
    for obj in page.get('Contents', []):
        if 'EPORNER.COM_-_DfHQR' in obj['Key']:
            found = obj['Key']
            print(f"   Encontrado: {found}")
            break
    if found:
        break

if not found:
    print("   Arquivo nao encontrado!")
    exit(1)

# Copiar para nova pasta
new_key = found.replace('litle_dragon', 'emillya_Bunny')
print(f"\n2. Copiando para: {new_key}")

s3.copy_object(
    Bucket=bucket,
    CopySource={'Bucket': bucket, 'Key': found},
    Key=new_key
)

# Deletar original
print(f"\n3. Deletando original: {found}")
s3.delete_object(Bucket=bucket, Key=found)

print("\n✓ Arquivo movido com sucesso!")
