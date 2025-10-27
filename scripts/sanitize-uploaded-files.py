#!/usr/bin/env python3
import boto3
import unicodedata
import re

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/Star/'

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
print("SANITIZANDO ARQUIVOS")
print("=" * 60)

# Contar total primeiro
print("\n1. Contando arquivos...")
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

all_files = []
for page in pages:
    for obj in page.get('Contents', []):
        all_files.append(obj)

print(f"   Total: {len(all_files)} arquivos")

print("\n2. Sanitizando...")
renamed = 0
for idx, obj in enumerate(all_files, 1):
        old_key = obj['Key']
        parts = old_key.split('/')
        old_filename = parts[-1]
        
        # Sanitizar
        new_filename = sanitize_filename(old_filename)
        
        if new_filename != old_filename:
            new_key = '/'.join(parts[:-1] + [new_filename])
            
            print(f"\n[{idx}/{len(all_files)}] Renomeando:")
            print(f"  DE: {old_filename[:70]}")
            print(f"  PARA: {new_filename[:70]}")
            
            try:
                # Copiar com novo nome
                s3.copy_object(
                    Bucket=bucket,
                    CopySource={'Bucket': bucket, 'Key': old_key},
                    Key=new_key
                )
                
                # Deletar antigo
                s3.delete_object(Bucket=bucket, Key=old_key)
                renamed += 1
            except Exception as e:
                print(f"  ERRO: {str(e)[:50]}... (pulando)")
                continue

print("\n" + "=" * 60)
print(f"Concluido! {renamed} arquivos renomeados de {len(all_files)} totais")
