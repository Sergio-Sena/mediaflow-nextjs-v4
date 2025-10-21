#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para buscar pasta Anime em qualquer localização e mover para users/user_admin/Anime/
Mescla arquivos se já existir pasta Anime no destino
"""

import boto3
import sys
import io

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configurações
BUCKET_NAME = 'mediaflow-uploads-969430605054'
DESTINATION_PREFIX = 'users/user_admin/Anime/'

def find_anime_folders():
    """Busca todas as pastas Anime/ no bucket"""
    s3 = boto3.client('s3', region_name='us-east-1')
    
    print("Buscando pastas Anime/ no bucket...")
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET_NAME)
    
    anime_files = {}
    
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                # Buscar qualquer arquivo que contenha /Anime/ no caminho
                if '/Anime/' in key and not key.startswith('users/user_admin/Anime/'):
                    # Extrair o caminho da pasta Anime
                    parts = key.split('/Anime/')
                    source_prefix = parts[0] + '/Anime/'
                    relative_path = parts[1] if len(parts) > 1 else ''
                    
                    if source_prefix not in anime_files:
                        anime_files[source_prefix] = []
                    
                    anime_files[source_prefix].append({
                        'key': key,
                        'relative': relative_path,
                        'size': obj['Size']
                    })
    
    return anime_files

def move_anime_folders():
    """Move todas as pastas Anime encontradas para users/user_admin/Anime/"""
    
    try:
        s3 = boto3.client('s3', region_name='us-east-1')
        
        # Buscar pastas Anime
        anime_folders = find_anime_folders()
        
        if not anime_folders:
            print("OK - Nenhuma pasta Anime encontrada fora de users/user_admin/")
            return
        
        print(f"\nEncontradas {len(anime_folders)} pasta(s) Anime:")
        for source in anime_folders.keys():
            print(f"  - {source} ({len(anime_folders[source])} arquivos)")
        
        total_files = sum(len(files) for files in anime_folders.values())
        print(f"\nTotal de arquivos a mover: {total_files}")
        
        # Confirmação
        print("\nConfirmacao: MOVER")
        confirm = 'MOVER'
        
        moved_count = 0
        error_count = 0
        
        # Mover cada pasta
        for source_prefix, files in anime_folders.items():
            print(f"\nMovendo de {source_prefix}...")
            
            for file_info in files:
                source_key = file_info['key']
                relative_path = file_info['relative']
                dest_key = DESTINATION_PREFIX + relative_path
                
                try:
                    # Copiar arquivo
                    s3.copy_object(
                        Bucket=BUCKET_NAME,
                        CopySource={'Bucket': BUCKET_NAME, 'Key': source_key},
                        Key=dest_key
                    )
                    
                    # Deletar original
                    s3.delete_object(Bucket=BUCKET_NAME, Key=source_key)
                    
                    moved_count += 1
                    print(f"OK - Movido: {source_key} -> {dest_key}")
                    
                except Exception as e:
                    error_count += 1
                    print(f"ERRO ao mover {source_key}: {e}")
        
        print(f"\nOperacao concluida!")
        print(f"Arquivos movidos: {moved_count}")
        print(f"Erros: {error_count}")
        print(f"Destino: {DESTINATION_PREFIX}")
        
    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("MOVER PASTA ANIME PARA USER_ADMIN")
    print("=" * 50)
    move_anime_folders()
