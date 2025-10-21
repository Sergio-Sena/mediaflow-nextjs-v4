# -*- coding: utf-8 -*-
"""
Script para verificar estrutura S3 e identificar problemas
"""

import boto3
from collections import defaultdict

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'

def analyze_s3_structure():
    """Analisa estrutura S3 e identifica problemas"""
    
    print("Analisando estrutura S3...")
    print()
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET)
    
    users_files = defaultdict(int)
    root_files = []
    anonymous_files = []
    total_size = 0
    
    for page in pages:
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            key = obj['Key']
            size = obj['Size']
            total_size += size
            
            # Arquivos na raiz (fora de users/)
            if not key.startswith('users/'):
                root_files.append((key, size))
            
            # Arquivos em users/anonymous/
            elif key.startswith('users/anonymous/'):
                anonymous_files.append((key, size))
            
            # Arquivos em users/{username}/
            elif key.startswith('users/'):
                parts = key.split('/')
                if len(parts) >= 2:
                    username = parts[1]
                    users_files[username] += 1
    
    # Relatorio
    print("=" * 80)
    print("RELATORIO DE ESTRUTURA S3")
    print("=" * 80)
    print()
    
    print(f"Tamanho total: {total_size / (1024**3):.2f} GB")
    print()
    
    # Usuarios
    print("USUARIOS:")
    for username, count in sorted(users_files.items()):
        status = "[OK]" if username != "anonymous" else "[PROBLEMA]"
        print(f"  {status} users/{username}/ - {count} arquivos")
    print()
    
    # Arquivos na raiz
    if root_files:
        print(f"[PROBLEMA] ARQUIVOS NA RAIZ (fora de users/): {len(root_files)} arquivos")
        root_size = sum(size for _, size in root_files)
        print(f"  Tamanho total: {root_size / (1024**3):.2f} GB")
        print("  Primeiros 10:")
        for key, size in root_files[:10]:
            print(f"    - {key} ({size / (1024**2):.1f} MB)")
        if len(root_files) > 10:
            print(f"    ... e mais {len(root_files) - 10} arquivos")
        print()
    
    # Arquivos anonymous
    if anonymous_files:
        print(f"[PROBLEMA] ARQUIVOS EM users/anonymous/: {len(anonymous_files)} arquivos")
        anon_size = sum(size for _, size in anonymous_files)
        print(f"  Tamanho total: {anon_size / (1024**3):.2f} GB")
        print("  Primeiros 10:")
        for key, size in anonymous_files[:10]:
            print(f"    - {key} ({size / (1024**2):.1f} MB)")
        if len(anonymous_files) > 10:
            print(f"    ... e mais {len(anonymous_files) - 10} arquivos")
        print()
    
    # Resumo
    print("=" * 80)
    print("RESUMO:")
    print(f"  - Total de usuarios: {len(users_files)}")
    print(f"  - Arquivos na raiz: {len(root_files)}")
    print(f"  - Arquivos em anonymous: {len(anonymous_files)}")
    print(f"  - Status: {'[OK]' if not root_files and not anonymous_files else '[PROBLEMAS ENCONTRADOS]'}")
    print("=" * 80)

if __name__ == '__main__':
    analyze_s3_structure()
