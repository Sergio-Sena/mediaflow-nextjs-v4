#!/usr/bin/env python3
"""
Comparar arquivos locais com usuario sergio_sena no S3 - versao simples
"""

import boto3
import os
from collections import defaultdict

def get_local_files(local_path):
    """Obter lista de arquivos locais"""
    local_files = []
    
    for dirpath, dirnames, filenames in os.walk(local_path):
        for filename in filenames:
            if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, local_path)
                
                # Normalizar nome para comparacao (apenas caracteres basicos)
                try:
                    normalized_name = filename.lower().replace(' ', '').replace('_', '').replace('-', '')
                    # Remover caracteres especiais
                    normalized_name = ''.join(c for c in normalized_name if c.isalnum() or c == '.')
                    
                    local_files.append({
                        'path': relative_path,
                        'filename': filename,
                        'normalized': normalized_name,
                        'size': os.path.getsize(full_path) / (1024 * 1024)  # MB
                    })
                except:
                    # Pular arquivos com nomes problematicos
                    continue
    
    return local_files

def get_s3_files(bucket_name, prefix):
    """Obter lista de arquivos do S3"""
    s3_client = boto3.client('s3')
    s3_files = []
    
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    filename = key.split('/')[-1]
                    
                    if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                        # Normalizar nome para comparacao
                        try:
                            normalized_name = filename.lower().replace(' ', '').replace('_', '').replace('-', '')
                            normalized_name = ''.join(c for c in normalized_name if c.isalnum() or c == '.')
                            
                            s3_files.append({
                                'key': key,
                                'filename': filename,
                                'normalized': normalized_name,
                                'size': obj['Size'] / (1024 * 1024)  # MB
                            })
                        except:
                            continue
    except Exception as e:
        print(f"Erro ao acessar S3: {e}")
        return []
    
    return s3_files

def main():
    print("Comparando arquivos locais com usuario sergio_sena")
    print("=" * 60)
    
    # Configuracoes
    local_path = r"C:\Users\dell 5557\Videos\IDM"
    bucket_name = 'mediaflow-uploads-969430605054'
    s3_prefix = 'users/sergio_sena/'
    
    # Obter arquivos
    print("Carregando arquivos locais...")
    local_files = get_local_files(local_path)
    
    print("Carregando arquivos do S3 (sergio_sena)...")
    s3_files = get_s3_files(bucket_name, s3_prefix)
    
    print(f"Arquivos locais: {len(local_files)}")
    print(f"Arquivos S3 sergio_sena: {len(s3_files)}")
    print()
    
    # Criar indices para comparacao rapida
    s3_normalized = {f['normalized'] for f in s3_files}
    
    # Encontrar arquivos que estao no local mas nao no S3
    missing_in_s3 = []
    
    for local_file in local_files:
        if local_file['normalized'] not in s3_normalized:
            missing_in_s3.append(local_file)
    
    # Agrupar por pasta
    missing_by_folder = defaultdict(list)
    for file in missing_in_s3:
        folder = os.path.dirname(file['path'])
        if not folder:
            folder = 'root'
        missing_by_folder[folder].append(file)
    
    # Relatorio
    if missing_in_s3:
        print("ARQUIVOS LOCAIS NAO ENCONTRADOS EM SERGIO_SENA:")
        print("-" * 50)
        
        total_size = 0
        total_count = 0
        
        for folder, files in missing_by_folder.items():
            print(f"\nPasta: {folder} ({len(files)} arquivos)")
            folder_size = 0
            
            for file in files:
                # Usar nome simplificado para evitar problemas de encoding
                safe_name = file['filename'][:50] + "..." if len(file['filename']) > 50 else file['filename']
                try:
                    print(f"  {safe_name} ({file['size']:.1f} MB)")
                except:
                    print(f"  [arquivo com caracteres especiais] ({file['size']:.1f} MB)")
                
                folder_size += file['size']
                total_size += file['size']
                total_count += 1
            
            print(f"  Subtotal: {folder_size:.1f} MB")
        
        print(f"\nTOTAL FALTANDO: {total_count} arquivos ({total_size:.1f} MB / {total_size/1024:.2f} GB)")
        
    else:
        print("TODOS OS ARQUIVOS LOCAIS JA EXISTEM EM SERGIO_SENA!")
    
    # Estatisticas
    print(f"\nESTATISTICAS:")
    if local_files:
        coverage = ((len(local_files) - len(missing_in_s3)) / len(local_files) * 100)
        print(f"Cobertura: {coverage:.1f}%")
        print(f"Arquivos sincronizados: {len(local_files) - len(missing_in_s3)}")
        print(f"Arquivos pendentes: {len(missing_in_s3)}")

if __name__ == "__main__":
    main()