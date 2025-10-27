#!/usr/bin/env python3
"""
Comparar pasta local vs S3 - Anasta_angel
"""

import boto3
import os
from pathlib import Path

def check_local_vs_s3():
    """Comparar arquivos locais vs S3"""
    try:
        # Pasta local
        local_path = Path(r"C:\Users\dell 5557\Videos\IDM\Star\Anasta_angel")
        
        # S3
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket = 'mediaflow-uploads-969430605054'
        prefix = 'users/user_admin/Star/Anasta_angel/'
        
        print("Comparando Local vs S3...")
        print("=" * 50)
        
        # Arquivos locais
        local_files = []
        local_size = 0
        if local_path.exists():
            for file_path in local_path.rglob('*'):
                if file_path.is_file():
                    rel_path = file_path.relative_to(local_path)
                    size = file_path.stat().st_size
                    local_files.append((str(rel_path), size))
                    local_size += size
        
        # Arquivos S3
        s3_files = []
        s3_size = 0
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    size = obj['Size']
                    if not key.endswith('/'):  # Ignorar "pastas"
                        rel_key = key.replace(prefix, '')
                        s3_files.append((rel_key, size))
                        s3_size += size
        
        # Resultados
        print(f"LOCAL:")
        print(f"  Arquivos: {len(local_files)}")
        print(f"  Tamanho: {local_size / (1024**3):.2f} GB")
        
        print(f"\nS3:")
        print(f"  Arquivos: {len(s3_files)}")
        print(f"  Tamanho: {s3_size / (1024**3):.2f} GB")
        
        # Arquivos que estão no local mas não no S3
        local_names = {name for name, size in local_files}
        s3_names = {name for name, size in s3_files}
        
        missing_in_s3 = local_names - s3_names
        if missing_in_s3:
            print(f"\nArquivos NÃO enviados para S3 ({len(missing_in_s3)}):")
            for name in sorted(missing_in_s3):
                print(f"  - {name}")
        
        # Arquivos extras no S3
        extra_in_s3 = s3_names - local_names
        if extra_in_s3:
            print(f"\nArquivos EXTRAS no S3 ({len(extra_in_s3)}):")
            for name in sorted(extra_in_s3):
                print(f"  + {name}")
        
        if not missing_in_s3 and not extra_in_s3:
            print("\n✅ Todos os arquivos foram enviados corretamente!")
        
        return True
        
    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    check_local_vs_s3()