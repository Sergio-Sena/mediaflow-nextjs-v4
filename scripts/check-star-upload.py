#!/usr/bin/env python3
"""
Verificar upload da pasta Corporativo no S3
"""

import boto3
from datetime import datetime

def check_s3_folder():
    """Verificar conteúdo da pasta Corporativo no S3"""
    try:
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket = 'mediaflow-uploads-969430605054'
        prefix = 'users/user_admin/Corporativo/'
        
        print("Verificando upload da pasta Corporativo...")
        print("=" * 50)
        
        # Licorporativo objetos
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        
        total_size = 0
        file_count = 0
        folders = set()
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    size = obj['Size']
                    modified = obj['LastModified']
                    
                    # Contar arquivos (não pastas vazias)
                    if not key.endswith('/'):
                        file_count += 1
                        total_size += size
                        
                        # Extrair pasta
                        folder_path = '/'.join(key.split('/')[:-1])
                        if folder_path != prefix.rstrip('/'):
                            folders.add(folder_path.replace(prefix, ''))
        
        # Converter para GB
        total_gb = total_size / (1024**3)
        
        print(f"Total de arquivos: {file_count}")
        print(f"Tamanho total: {total_gb:.2f} GB")
        print(f"Subpastas encontradas: {len(folders)}")
        
        if folders:
            print("\nSubpastas:")
            for folder in sorted(folders):
                if folder:  # Ignorar string vazia
                    print(f"  - {folder}")
        
        print(f"\nPrefixo S3: {prefix}")
        print("Upload verificado com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"Erro ao verificar S3: {e}")
        return False

if __name__ == "__main__":
    check_s3_folder()