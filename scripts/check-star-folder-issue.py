#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("Verificando estrutura de pastas em user_admin")
print("=" * 60)

# Listar arquivos em users/user_admin/ (nivel raiz)
paginator = s3.get_paginator('list_objects_v2')

# Verificar se existem arquivos diretos em users/user_admin/Star/
print("\n1. Arquivos DIRETOS em users/user_admin/Star/ (sem subpasta):")
print("-" * 60)
pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/Star/', Delimiter='/')

direct_files = 0
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            key = obj['Key']
            # Arquivo direto = nao tem / depois de Star/
            if key.count('/') == 3:  # users/user_admin/Star/arquivo.mp4
                direct_files += 1
                print(f"  {key}")

print(f"\nTotal de arquivos diretos: {direct_files}")

# Verificar subpastas
print("\n2. Subpastas em users/user_admin/Star/:")
print("-" * 60)
pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/Star/', Delimiter='/')

subfolders = []
for page in pages:
    if 'CommonPrefixes' in page:
        for prefix in page['CommonPrefixes']:
            folder = prefix['Prefix'].replace('users/user_admin/Star/', '').rstrip('/')
            subfolders.append(folder)

for folder in sorted(subfolders):
    print(f"  {folder}/")

print(f"\nTotal de subpastas: {len(subfolders)}")

# Verificar pastas no nivel raiz de user_admin
print("\n3. Pastas no nivel RAIZ de users/user_admin/:")
print("-" * 60)
pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/', Delimiter='/')

root_folders = []
for page in pages:
    if 'CommonPrefixes' in page:
        for prefix in page['CommonPrefixes']:
            folder = prefix['Prefix'].replace('users/user_admin/', '').rstrip('/')
            root_folders.append(folder)

for folder in sorted(root_folders):
    print(f"  {folder}/")

print(f"\nTotal de pastas raiz: {len(root_folders)}")
