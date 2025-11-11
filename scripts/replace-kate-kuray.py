import boto3
import os
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star\kate kuray'
S3_PREFIX = 'users/user_admin/Star/kate kuray/'

def get_local_files():
    """Lista arquivos locais"""
    files = {}
    for file in Path(LOCAL_PATH).rglob('*'):
        if file.is_file():
            files[file.name.lower()] = str(file)
    return files

def get_s3_files():
    """Lista arquivos no S3"""
    files = {}
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=BUCKET, Prefix=S3_PREFIX):
        for obj in page.get('Contents', []):
            filename = obj['Key'].split('/')[-1]
            if filename:
                files[filename.lower()] = obj['Key']
    
    return files

print("="*60)
print("VERIFICANDO KATE KURAY")
print("="*60)

local_files = get_local_files()
s3_files = get_s3_files()

print(f"\nLocal: {len(local_files)} arquivos")
print(f"S3: {len(s3_files)} arquivos")

# Comparar
matched = []
not_in_s3 = []
not_in_local = []

for name, path in local_files.items():
    if name in s3_files:
        matched.append((name, path, s3_files[name]))
    else:
        not_in_s3.append(name)

for name in s3_files:
    if name not in local_files:
        not_in_local.append(name)

print("\n" + "="*60)
print("RESULTADO")
print("="*60)
print(f"Arquivos correspondentes: {len(matched)}")
print(f"Apenas local: {len(not_in_s3)}")
print(f"Apenas S3: {len(not_in_local)}")

if not_in_s3:
    print("\nApenas local (primeiros 10):")
    for name in not_in_s3[:10]:
        print(f"  - {name}")

if not_in_local:
    print("\nApenas S3 (primeiros 10):")
    for name in not_in_local[:10]:
        print(f"  - {name}")

if matched:
    print("\n" + "="*60)
    print(f"SUBSTITUIR {len(matched)} ARQUIVOS NO S3?")
    print("="*60)
    resp = input("Digite 'SIM' para confirmar: ")
    
    if resp.upper() == 'SIM':
        print("\nSubstituindo arquivos...")
        replaced = 0
        
        for name, local_path, s3_key in matched:
            try:
                print(f"[{replaced+1}/{len(matched)}] {name}")
                s3.upload_file(local_path, BUCKET, s3_key)
                replaced += 1
            except Exception as e:
                print(f"  [ERRO] {e}")
        
        print(f"\n{replaced} arquivos substituidos com sucesso!")
    else:
        print("Cancelado")
else:
    print("\nNenhum arquivo correspondente encontrado!")
