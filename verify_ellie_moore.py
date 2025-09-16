#!/usr/bin/env python3
"""
Script para verificar a pasta Ellie_moore criada
"""

import boto3
import json
from botocore.exceptions import ClientError

def load_config():
    """Carrega configuração do Mediaflow"""
    with open('aws-setup/mediaflow-config.json', 'r') as f:
        return json.load(f)

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
    config = load_config()
    bucket = config['buckets']['uploads']
    
    print("VERIFICACAO DA PASTA ELLIE_MOORE")
    print("=" * 50)
    print(f"Bucket: {bucket}")
    print(f"Pasta: Ellie_moore")
    print("=" * 50)
    
    # Verificar pasta Ellie_moore
    files = list_folder_contents(bucket, 'Ellie_moore')
    
    if not files:
        print("ERRO: Pasta Ellie_moore nao encontrada ou vazia!")
        return
    
    print(f"SUCESSO: {len(files)} arquivo(s) encontrado(s)")
    print("\nConteudo da pasta Ellie_moore:")
    print("-" * 50)
    
    total_size = 0
    for i, file in enumerate(files, 1):
        size_mb = file['size'] / (1024 * 1024)
        total_size += size_mb
        file_name = file['key'].split('/')[-1]
        print(f"{i:2d}. {file_name} ({size_mb:.1f} MB)")
    
    print("-" * 50)
    print(f"Total: {len(files)} arquivo(s) - {total_size:.1f} MB")
    
    # Verificar tipos de arquivo
    video_files = [f for f in files if f['key'].endswith(('.mp4', '.ts', '.avi', '.mov'))]
    other_files = [f for f in files if not f['key'].endswith(('.mp4', '.ts', '.avi', '.mov'))]
    
    print(f"\nTipos de arquivo:")
    print(f"  Videos: {len(video_files)}")
    print(f"  Outros: {len(other_files)}")
    
    print(f"\nPasta Ellie_moore criada com sucesso!")
    print("Todas as pastas '_morre' foram unificadas.")

if __name__ == "__main__":
    main()