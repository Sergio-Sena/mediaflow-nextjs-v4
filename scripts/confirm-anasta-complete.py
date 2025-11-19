#!/usr/bin/env python3
"""
Confirmar se todos os arquivos locais estao no S3 (considerando sanitizacao)
"""

import boto3
import os
from pathlib import Path
import unicodedata
import re

def sanitize_filename(filename):
    """Sanitizar nome do arquivo"""
    nfkd = unicodedata.normalize('NFKD', filename)
    filename = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    filename = re.sub(r'[^\w\s\.\-]', '', filename)
    filename = re.sub(r'\s+', ' ', filename)
    name, ext = os.path.splitext(filename)
    if len(name) > 200:
        name = name[:200]
    return name + ext

def confirm_upload():
    """Confirmar upload completo"""
    try:
        local_path = Path(r"C:\Users\dell 5557\Videos\IDM\Corporativo\Anasta_angel")
        
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket = 'mediaflow-uploads-969430605054'
        prefix = 'users/user_admin/Corporativo/Anasta_angel/'
        
        print("Confirmando upload completo...")
        print("=" * 50)
        
        # Arquivos locais (sanitizados)
        local_files = {}
        for file_path in local_path.rglob('*'):
            if file_path.is_file():
                sanitized = sanitize_filename(file_path.name)
                local_files[sanitized] = file_path.name
        
        # Arquivos S3
        s3_files = set()
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    if not key.endswith('/'):
                        filename = key.split('/')[-1]
                        s3_files.add(filename)
        
        # Verificar se todos os arquivos locais (sanitizados) estao no S3
        missing = []
        for sanitized, original in local_files.items():
            if sanitized not in s3_files:
                missing.append(f"{original} -> {sanitized}")
        
        print(f"Arquivos locais: {len(local_files)}")
        print(f"Arquivos S3: {len(s3_files)}")
        print()
        
        if missing:
            print(f"Arquivos FALTANDO no S3 ({len(missing)}):")
            for m in missing:
                try:
                    print(f"  - {m}")
                except:
                    print(f"  - [arquivo com caracteres especiais]")
            print("\nUpload INCOMPLETO")
            return False
        else:
            print("Todos os arquivos locais estao no S3!")
            print("\nUpload COMPLETO")
            return True
        
    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    confirm_upload()
