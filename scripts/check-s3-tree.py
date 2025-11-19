#!/usr/bin/env python3
"""
Verificar arvore de pastas no S3
"""

import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("Arvore de pastas no S3:")
print("=" * 60)

# Licorporativo pastas no nivel raiz
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Delimiter='/')

root_folders = []
for page in pages:
    if 'CommonPrefixes' in page:
        for prefix in page['CommonPrefixes']:
            folder = prefix['Prefix'].rstrip('/')
            root_folders.append(folder)

print(f"\nPastas na RAIZ do bucket:")
for folder in sorted(root_folders):
    print(f"  /{folder}/")

# Verificar estrutura users/
print(f"\n\nEstrutura de /users/:")
print("-" * 60)

pages = paginator.paginate(Bucket=bucket, Prefix='users/', Delimiter='/')
users_folders = []
for page in pages:
    if 'CommonPrefixes' in page:
        for prefix in page['CommonPrefixes']:
            folder = prefix['Prefix'].replace('users/', '').rstrip('/')
            users_folders.append(folder)

for folder in sorted(users_folders):
    print(f"  /users/{folder}/")
    
    # Contar arquivos
    count = 0
    size = 0
    for obj_page in paginator.paginate(Bucket=bucket, Prefix=f"users/{folder}/"):
        if 'Contents' in obj_page:
            for obj in obj_page['Contents']:
                if not obj['Key'].endswith('/'):
                    count += 1
                    size += obj['Size']
    
    print(f"    Arquivos: {count}, Tamanho: {size / (1024**3):.2f} GB")

# Verificar se existe user_admin duplicado
print(f"\n\nVerificando duplicacao:")
print("-" * 60)

if 'user_admin' in users_folders and 'user' in users_folders:
    print("ALERTA: Encontradas pastas duplicadas!")
    print("  /users/user_admin/")
    print("  /users/user/")
    
    # Verificar se user/ tem user_admin/ dentro
    pages = paginator.paginate(Bucket=bucket, Prefix='users/user/', Delimiter='/')
    for page in pages:
        if 'CommonPrefixes' in page:
            for prefix in page['CommonPrefixes']:
                subfolder = prefix['Prefix'].replace('users/user/', '').rstrip('/')
                print(f"    /users/user/{subfolder}/")
