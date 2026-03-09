#!/usr/bin/env python3
import boto3
import os
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
local_dir = r'C:\Users\dell 5557\Videos\IDM\Star'
s3_prefix = 'users/sergio_sena/Star/'

print("Verificando arquivos locais vs S3...")
print("=" * 80)

# Listar todos os arquivos locais
local_files = {}
for root, dirs, files in os.walk(local_dir):
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, local_dir)
        s3_key = s3_prefix + relative_path.replace('\\', '/')
        local_files[s3_key] = {
            'local_path': local_path,
            'relative_path': relative_path,
            'size': os.path.getsize(local_path)
        }

print(f"Total de arquivos locais: {len(local_files)}")
print()

# Listar todos os arquivos no S3
print("Listando arquivos no S3...")
s3_files = {}
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket=bucket, Prefix=s3_prefix):
    if 'Contents' in page:
        for obj in page['Contents']:
            s3_files[obj['Key']] = obj['Size']

print(f"Total de arquivos no S3: {len(s3_files)}")
print()

# Comparar
missing = []
size_mismatch = []

for s3_key, info in local_files.items():
    if s3_key not in s3_files:
        missing.append(info['relative_path'])
    elif s3_files[s3_key] != info['size']:
        size_mismatch.append({
            'path': info['relative_path'],
            'local_size': info['size'],
            's3_size': s3_files[s3_key]
        })

# Resultados
print("=" * 80)
print("RESULTADO DA VERIFICAÇÃO")
print("=" * 80)

if not missing and not size_mismatch:
    print("✓ SUCESSO! Todos os arquivos foram enviados corretamente!")
    print(f"  Total: {len(local_files)} arquivos")
else:
    if missing:
        print(f"\n❌ ARQUIVOS FALTANDO NO S3 ({len(missing)}):")
        print("-" * 80)
        for file in missing:
            print(f"  - {file}")
    
    if size_mismatch:
        print(f"\n⚠ ARQUIVOS COM TAMANHO DIFERENTE ({len(size_mismatch)}):")
        print("-" * 80)
        for item in size_mismatch:
            print(f"  - {item['path']}")
            print(f"    Local: {item['local_size']:,} bytes")
            print(f"    S3:    {item['s3_size']:,} bytes")

print("\n" + "=" * 80)
