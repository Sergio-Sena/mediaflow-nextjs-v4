#!/usr/bin/env python3
import boto3
import os
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
local_dir = r'C:\Users\dell 5557\Videos\IDM\Star'
s3_prefix = 'users/user_admin/Star/'

print("=" * 60)
print("VERIFICACAO COMPLETA: LOCAL vs S3")
print("=" * 60)

# 1. Contar arquivos locais por pasta
print("\n1. Contando arquivos locais...")
local_files = {}
for root, dirs, files in os.walk(local_dir):
    folder = os.path.basename(root)
    if folder == 'Star':
        continue
    local_files[folder] = len(files)

print(f"   Total de pastas: {len(local_files)}")
for folder, count in sorted(local_files.items()):
    print(f"   {folder}: {count} arquivos")

# 2. Contar arquivos no S3 por pasta
print("\n2. Contando arquivos no S3...")
s3_files = {}
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=s3_prefix)

for page in pages:
    for obj in page.get('Contents', []):
        key = obj['Key']
        parts = key.replace(s3_prefix, '').split('/')
        if len(parts) >= 2:
            folder = parts[0]
            if folder not in s3_files:
                s3_files[folder] = 0
            s3_files[folder] += 1

print(f"   Total de pastas: {len(s3_files)}")
for folder, count in sorted(s3_files.items()):
    print(f"   {folder}: {count} arquivos")

# 3. Comparar
print("\n3. Comparacao:")
print("-" * 60)
all_folders = set(local_files.keys()) | set(s3_files.keys())

missing = []
duplicated = []
ok = []

for folder in sorted(all_folders):
    local_count = local_files.get(folder, 0)
    s3_count = s3_files.get(folder, 0)
    
    if local_count == 0:
        print(f"   {folder}: S3={s3_count}, Local=0 (EXTRA NO S3)")
    elif s3_count == 0:
        print(f"   {folder}: Local={local_count}, S3=0 (FALTANDO)")
        missing.append(folder)
    elif s3_count > local_count:
        print(f"   {folder}: Local={local_count}, S3={s3_count} (DUPLICADOS?)")
        duplicated.append(folder)
    elif s3_count < local_count:
        print(f"   {folder}: Local={local_count}, S3={s3_count} (FALTANDO)")
        missing.append(folder)
    else:
        print(f"   {folder}: {local_count} arquivos (OK)")
        ok.append(folder)

print("\n" + "=" * 60)
print("RESUMO:")
print("=" * 60)
print(f"OK: {len(ok)} pastas")
print(f"Faltando: {len(missing)} pastas")
print(f"Duplicados: {len(duplicated)} pastas")

if duplicated:
    print("\nPASTAS COM DUPLICADOS:")
    for folder in duplicated:
        print(f"  - {folder}: Local={local_files[folder]}, S3={s3_files[folder]}")
