#!/usr/bin/env python3
import boto3
import unicodedata
import re
from tqdm import tqdm

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/'

def sanitize_filename(filename):
    # Remover acentos
    nfkd = unicodedata.normalize('NFKD', filename)
    filename = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    
    # Remover espaços duplos
    filename = re.sub(r'\s+', ' ', filename)
    
    # Truncar se muito longo (max 95 chars + extensão)
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    if len(name) > 95:
        name = name[:95]
    
    return f"{name}.{ext}" if ext else name

print("=" * 60)
print("SANITIZANDO 26 ARQUIVOS")
print("=" * 60)

# Buscar arquivos com problemas
print("\n1. Buscando arquivos...")
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

to_sanitize = []
for page in pages:
    for obj in page.get('Contents', []):
        key = obj['Key']
        filename = key.split('/')[-1]
        
        has_special = any(c in filename for c in ['á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'ç', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ã', 'Õ', 'Ç'])
        too_long = len(filename) > 100
        double_space = '  ' in filename
        
        if has_special or too_long or double_space:
            to_sanitize.append(key)

print(f"   Encontrados: {len(to_sanitize)} arquivos")

# Sanitizar
print("\n2. Sanitizando...")
renamed = 0

with tqdm(total=len(to_sanitize), unit='arquivo') as pbar:
    for old_key in to_sanitize:
        parts = old_key.split('/')
        old_filename = parts[-1]
        new_filename = sanitize_filename(old_filename)
        
        if new_filename != old_filename:
            new_key = '/'.join(parts[:-1] + [new_filename])
            
            try:
                s3.copy_object(
                    Bucket=bucket,
                    CopySource={'Bucket': bucket, 'Key': old_key},
                    Key=new_key
                )
                s3.delete_object(Bucket=bucket, Key=old_key)
                renamed += 1
            except Exception as e:
                pass
        
        pbar.update(1)

print("\n" + "=" * 60)
print(f"Concluido! {renamed} arquivos sanitizados")
