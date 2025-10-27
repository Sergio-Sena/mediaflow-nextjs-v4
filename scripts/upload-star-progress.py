#!/usr/bin/env python3
import boto3
import os
from pathlib import Path
from tqdm import tqdm

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
local_dir = r'C:\Users\dell 5557\Videos\IDM\Star'
s3_prefix = 'users/user_admin/Star/'

print("=" * 60)
print("UPLOAD STAR FOLDER COM PROGRESSO")
print("=" * 60)

# 1. Calcular tamanho e contar arquivos
print("\n1. Analisando pasta local...")
total_size = 0
files_list = []

for root, dirs, files in os.walk(local_dir):
    for file in files:
        local_path = os.path.join(root, file)
        file_size = os.path.getsize(local_path)
        total_size += file_size
        relative_path = os.path.relpath(local_path, local_dir)
        files_list.append((local_path, relative_path, file_size))

print(f"   Total: {len(files_list)} arquivos")
print(f"   Tamanho: {total_size / (1024**3):.2f} GB")

# 2. Upload com barra de progresso
print("\n2. Fazendo upload...")
uploaded = []
failed = []

with tqdm(total=len(files_list), unit='arquivo') as pbar:
    for local_path, relative_path, file_size in files_list:
        s3_key = s3_prefix + relative_path.replace('\\', '/')
        try:
            s3.upload_file(local_path, bucket, s3_key)
            uploaded.append(s3_key)
            pbar.set_description(f"Upload: {relative_path[:40]}")
        except Exception as e:
            failed.append((relative_path, str(e)))
        pbar.update(1)

# 3. Verificar no S3
print("\n3. Verificando arquivos no S3...")
s3_files = set()
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=s3_prefix)

for page in pages:
    for obj in page.get('Contents', []):
        s3_files.add(obj['Key'])

# Comparar
local_keys = {s3_prefix + rel.replace('\\', '/') for _, rel, _ in files_list}
missing = local_keys - s3_files

print("\n" + "=" * 60)
print("RESULTADO:")
print("=" * 60)
print(f"Enviados: {len(uploaded)}")
print(f"Falharam: {len(failed)}")
print(f"No S3: {len(s3_files)}")
print(f"Faltando: {len(missing)}")

if failed:
    print("\nArquivos com erro:")
    for f, err in failed[:10]:
        print(f"  - {f}: {err}")

if missing:
    print("\nArquivos faltando no S3:")
    for m in list(missing)[:10]:
        print(f"  - {m}")

if not failed and not missing:
    print("\n✓ Todos os arquivos foram enviados com sucesso!")
