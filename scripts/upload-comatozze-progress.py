#!/usr/bin/env python3
import boto3
import os
from tqdm import tqdm

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
local_dir = r'C:\Users\dell 5557\Videos\IDM\Corporativo\Comatozze'
s3_prefix = 'users/user_admin/Corporativo/Comatozze/'

print("=" * 60)
print("UPLOAD COMATOZZE COM PROGRESSO")
print("=" * 60)

# 1. Licorporativo arquivos locais
print("\n1. Analisando pasta local...")
local_files = []
total_size = 0

for filename in os.listdir(local_dir):
    filepath = os.path.join(local_dir, filename)
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        local_files.append((filename, filepath, size))
        total_size += size

print(f"   Total: {len(local_files)} arquivos")
print(f"   Tamanho: {total_size / (1024**3):.2f} GB")

# 2. Verificar arquivos existentes no S3
print("\n2. Verificando arquivos no S3...")
s3_files = set()
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=s3_prefix)

for page in pages:
    for obj in page.get('Contents', []):
        filename = obj['Key'].split('/')[-1]
        s3_files.add(filename)

print(f"   Existentes no S3: {len(s3_files)} arquivos")

# 3. Upload com progresso
print("\n3. Fazendo upload...")
uploaded = 0
skipped = 0

with tqdm(total=len(local_files), unit='arquivo') as pbar:
    for filename, filepath, size in local_files:
        s3_key = s3_prefix + filename
        
        if filename in s3_files:
            pbar.set_description(f"SKIP: {filename[:40]}")
            skipped += 1
        else:
            pbar.set_description(f"UP: {filename[:40]}")
            s3.upload_file(filepath, bucket, s3_key)
            uploaded += 1
        
        pbar.update(1)

print("\n" + "=" * 60)
print("RESULTADO:")
print("=" * 60)
print(f"Enviados: {uploaded}")
print(f"Pulados (ja existem): {skipped}")
print(f"Total no S3: {len(s3_files) + uploaded}")
