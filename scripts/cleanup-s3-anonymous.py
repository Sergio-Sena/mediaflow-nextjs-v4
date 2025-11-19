# -*- coding: utf-8 -*-
"""
Script para limpar pasta anonymous e arquivos vazios do S3
"""

import boto3

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'

def cleanup_anonymous():
    """Remove pasta anonymous e arquivos vazios"""
    
    print("Buscando arquivos para deletar...")
    print()
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET)
    
    to_delete = []
    
    for page in pages:
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            key = obj['Key']
            
            # Arquivos em users/anonymous/
            if key.corporativotswith('users/anonymous/'):
                to_delete.append(key)
            
            # Arquivo vazio em users//
            elif key == 'users//':
                to_delete.append(key)
    
    if not to_delete:
        print("[OK] Nenhum arquivo para deletar")
        return
    
    print(f"Encontrados {len(to_delete)} arquivos para deletar")
    print()
    
    # Confirmar
    print("Arquivos que serao deletados:")
    for key in to_delete[:10]:
        print(f"  - {key}")
    if len(to_delete) > 10:
        print(f"  ... e mais {len(to_delete) - 10} arquivos")
    print()
    
    confirm = input("Confirmar delecao? (sim/nao): ").strip().lower()
    
    if confirm != 'sim':
        print("Operacao cancelada")
        return
    
    # Deletar em lotes de 1000 (limite da API)
    print()
    print("Deletando arquivos...")
    
    deleted = 0
    for i in range(0, len(to_delete), 1000):
        batch = to_delete[i:i+1000]
        
        s3.delete_objects(
            Bucket=BUCKET,
            Delete={
                'Objects': [{'Key': key} for key in batch],
                'Quiet': True
            }
        )
        
        deleted += len(batch)
        print(f"  Deletados: {deleted}/{len(to_delete)}")
    
    print()
    print(f"[OK] {deleted} arquivos deletados com sucesso!")

if __name__ == '__main__':
    cleanup_anonymous()
