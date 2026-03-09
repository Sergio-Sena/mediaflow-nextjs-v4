#!/usr/bin/env python3
import boto3
import os

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
local_dir = r'C:\Users\dell 5557\Videos\IDM\Corporativo'

folders_to_check = ['Little Angel', 'MIRARI HUB']

print("=" * 60)
print("ARQUIVOS FALTANTES")
print("=" * 60)

for folder in folders_to_check:
    print(f"\n{folder}:")
    print("-" * 60)
    
    # Arquivos locais
    local_path = os.path.join(local_dir, folder)
    local_files = set(os.listdir(local_path))
    
    # Arquivos S3
    s3_files = set()
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=f'users/user_admin/Corporativo/{folder}/')
    
    for page in pages:
        for obj in page.get('Contents', []):
            filename = obj['Key'].split('/')[-1]
            s3_files.add(filename)
    
    # Comparar
    missing = local_files - s3_files
    
    print(f"Local: {len(local_files)} arquivos")
    print(f"S3: {len(s3_files)} arquivos")
    print(f"Faltando: {len(missing)} arquivos")
    
    if missing:
        print("\nArquivos faltando:")
        for f in sorted(missing):
            print(f"  - {f}")
