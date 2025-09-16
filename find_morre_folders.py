#!/usr/bin/env python3
"""
Script para localizar e unificar pastas com "_morre" no Mediaflow
"""

import boto3
import json
from botocore.exceptions import ClientError

def load_config():
    """Carrega configuração do Mediaflow"""
    with open('aws-setup/mediaflow-config.json', 'r') as f:
        return json.load(f)

def list_s3_folders(bucket_name, prefix=""):
    """Lista pastas no bucket S3"""
    s3 = boto3.client('s3')
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
        
        folders = []
        for page in pages:
            if 'CommonPrefixes' in page:
                for prefix_info in page['CommonPrefixes']:
                    folder_name = prefix_info['Prefix'].rstrip('/')
                    folders.append(folder_name)
        
        return folders
    except ClientError as e:
        print(f"Erro ao acessar bucket {bucket_name}: {e}")
        return []

def find_morre_folders():
    """Encontra pastas que terminam com '_morre'"""
    config = load_config()
    
    print("Procurando pastas com '_morre' nos buckets S3...")
    print("=" * 60)
    
    morre_folders = []
    
    # Verificar bucket uploads
    uploads_bucket = config['buckets']['uploads']
    print(f"\nVerificando bucket: {uploads_bucket}")
    
    folders = list_s3_folders(uploads_bucket)
    for folder in folders:
        if folder.endswith('_morre'):
            morre_folders.append({
                'bucket': uploads_bucket,
                'folder': folder,
                'type': 'uploads'
            })
            print(f"  Encontrado: {folder}")
    
    # Verificar bucket processed
    processed_bucket = config['buckets']['processed']
    print(f"\nVerificando bucket: {processed_bucket}")
    
    folders = list_s3_folders(processed_bucket)
    for folder in folders:
        if folder.endswith('_morre'):
            morre_folders.append({
                'bucket': processed_bucket,
                'folder': folder,
                'type': 'processed'
            })
            print(f"  Encontrado: {folder}")
    
    return morre_folders

def list_folder_contents(bucket_name, folder_name):
    """Lista conteúdo de uma pasta"""
    s3 = boto3.client('s3')
    
    try:
        response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=f"{folder_name}/"
        )
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):  # Não incluir a própria pasta
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'modified': obj['LastModified']
                    })
        
        return files
    except ClientError as e:
        print(f"Erro ao listar conteúdo: {e}")
        return []

def main():
    print("MEDIAFLOW - Localizador de Pastas '_morre'")
    print("=" * 60)
    
    # Encontrar pastas
    morre_folders = find_morre_folders()
    
    if not morre_folders:
        print("\nNenhuma pasta com '_morre' encontrada.")
        return
    
    print(f"\nResumo: {len(morre_folders)} pasta(s) encontrada(s)")
    print("=" * 60)
    
    # Mostrar detalhes de cada pasta
    for i, folder_info in enumerate(morre_folders, 1):
        print(f"\nPasta {i}: {folder_info['folder']}")
        print(f"   Bucket: {folder_info['bucket']}")
        print(f"   Tipo: {folder_info['type']}")
        
        # Listar arquivos
        files = list_folder_contents(folder_info['bucket'], folder_info['folder'])
        print(f"   Arquivos: {len(files)}")
        
        if files:
            print("   Conteudo:")
            for file in files[:5]:  # Mostrar apenas os primeiros 5
                size_mb = file['size'] / (1024 * 1024)
                print(f"     - {file['key']} ({size_mb:.1f} MB)")
            
            if len(files) > 5:
                print(f"     ... e mais {len(files) - 5} arquivo(s)")
    
    # Sugerir ação
    print("\nProximos passos:")
    print("1. Confirme se essas sao as pastas que deseja unificar")
    print("2. Execute o script de unificacao para renomear para 'Ellie_moore'")
    print("3. Verifique se nao ha conflitos de nomes de arquivos")

if __name__ == "__main__":
    main()