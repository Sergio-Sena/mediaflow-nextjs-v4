#!/usr/bin/env python3
import boto3
import unicodedata
from tqdm import tqdm

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/'

print("=" * 60)
print("VERIFICANDO ARQUIVOS DO ADMINISTRADOR")
print("=" * 60)

# 1. Contar total
print("\n1. Contando arquivos...")
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

all_files = []
for page in pages:
    for obj in page.get('Contents', []):
        all_files.append(obj['Key'])

print(f"   Total: {len(all_files)} arquivos")

# 2. Verificar problemas
print("\n2. Verificando problemas...")
needs_sanitize = []

with tqdm(total=len(all_files), unit='arquivo') as pbar:
    for key in all_files:
        filename = key.split('/')[-1]
        
        # Verificar problemas
        has_special = any(c in filename for c in ['á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'ç', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ã', 'Õ', 'Ç'])
        too_long = len(filename) > 100
        double_space = '  ' in filename
        
        if has_special or too_long or double_space:
            issues = []
            if has_special: issues.append('ACENTOS')
            if too_long: issues.append(f'LONGO({len(filename)})')
            if double_space: issues.append('ESPACOS')
            
            needs_sanitize.append({
                'key': key,
                'filename': filename,
                'issues': issues
            })
        
        pbar.update(1)

# 3. Resultado
print("\n" + "=" * 60)
print("RESULTADO:")
print("=" * 60)
print(f"Total verificado: {len(all_files)}")
print(f"Precisam sanitizar: {len(needs_sanitize)}")
print(f"OK: {len(all_files) - len(needs_sanitize)}")

if needs_sanitize:
    print(f"\nPrimeiros 20 arquivos com problemas:")
    for item in needs_sanitize[:20]:
        issues_str = ', '.join(item['issues'])
        print(f"  [{issues_str}] {item['filename'][:70]}")
    
    if len(needs_sanitize) > 20:
        print(f"\n  ... e mais {len(needs_sanitize) - 20} arquivos")
