#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/users/'

print("Verificando TUDO em /users/user_admin/users/:")
print("=" * 60)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

total_size = 0
count = 0

for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            key = obj['Key']
            size = obj['Size']
            size_mb = size / (1024**2)
            total_size += size
            count += 1
            
            print(f"{key}")
            print(f"  Tamanho: {size_mb:.2f} MB")
            print()

print("=" * 60)
print(f"Total de objetos: {count}")
print(f"Tamanho total: {total_size / (1024**3):.2f} GB")
