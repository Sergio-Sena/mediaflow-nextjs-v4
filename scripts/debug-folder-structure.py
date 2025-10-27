#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/'

print("Debug: Estrutura de pastas para user_admin")
print("=" * 60)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

# Agrupar por pasta
folders = {}
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            key = obj['Key']
            if key.endswith('/'):
                continue
            
            # Extrair pasta
            parts = key.replace(prefix, '').split('/')
            if len(parts) > 1:
                folder = parts[0]
                if folder not in folders:
                    folders[folder] = []
                folders[folder].append(key)

print(f"\nPastas encontradas: {len(folders)}")
print()

for folder in sorted(folders.keys()):
    print(f"{folder}/")
    print(f"  Arquivos: {len(folders[folder])}")
    print(f"  Exemplo: {folders[folder][0] if folders[folder] else 'vazio'}")
    print()
