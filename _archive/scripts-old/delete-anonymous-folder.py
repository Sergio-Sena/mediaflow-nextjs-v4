#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para deletar completamente a pasta users/anonymous/ do S3
"""

import boto3
import sys
import io

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurações
BUCKET_NAME = 'mediaflow-uploads-969430605054'
ANONYMOUS_PREFIX = 'users/anonymous/'

def delete_anonymous_folder():
    """Deleta todos os arquivos da pasta users/anonymous/"""
    
    try:
        s3 = boto3.client('s3', region_name='us-east-1')
        
        print(f"Listando arquivos em {ANONYMOUS_PREFIX}...")
        
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=ANONYMOUS_PREFIX)
        
        objects_to_delete = []
        total_files = 0
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    objects_to_delete.append({'Key': obj['Key']})
                    total_files += 1
                    print(f"Encontrado: {obj['Key']}")
        
        if not objects_to_delete:
            print("OK - Pasta anonymous ja esta vazia ou nao existe")
            return
        
        print(f"\nDeletando {total_files} arquivos...")
        
        batch_size = 1000
        deleted_count = 0
        
        for i in range(0, len(objects_to_delete), batch_size):
            batch = objects_to_delete[i:i + batch_size]
            
            response = s3.delete_objects(
                Bucket=BUCKET_NAME,
                Delete={
                    'Objects': batch,
                    'Quiet': False
                }
            )
            
            if 'Deleted' in response:
                deleted_count += len(response['Deleted'])
                for deleted in response['Deleted']:
                    print(f"OK - Deletado: {deleted['Key']}")
            
            if 'Errors' in response:
                for error in response['Errors']:
                    print(f"ERRO ao deletar {error['Key']}: {error['Message']}")
        
        print(f"\nOperacao concluida!")
        print(f"Total de arquivos deletados: {deleted_count}")
        print(f"Pasta users/anonymous/ removida completamente")
        
    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("DELETAR PASTA ANONYMOUS")
    print("=" * 50)
    print(f"Confirmacao: DELETAR")
    delete_anonymous_folder()
