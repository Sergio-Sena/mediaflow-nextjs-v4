#!/usr/bin/env python3
"""
Verificar todas as pastas Corporativo vs S3 sergio_sena para evitar uploads desnecessarios
"""

import boto3
import os
from collections import defaultdict

def get_s3_files():
    """Obter todos os arquivos do S3 sergio_sena"""
    s3_client = boto3.client('s3')
    bucket_name = 'mediaflow-uploads-969430605054'
    s3_files = []
    
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix='users/sergio_sena/')
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    filename = key.split('/')[-1]
                    
                    if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                        try:
                            normalized_name = filename.lower().replace(' ', '').replace('_', '').replace('-', '')
                            normalized_name = ''.join(c for c in normalized_name if c.isalnum() or c == '.')
                            
                            s3_files.append({
                                'key': key,
                                'filename': filename,
                                'normalized': normalized_name,
                                'size': obj['Size'] / (1024 * 1024)
                            })
                        except:
                            continue
    except Exception as e:
        print(f"Erro ao acessar S3: {e}")
        return []
    
    return s3_files

def get_local_files_by_folder(corporativo_path):
    """Obter arquivos locais organizados por pasta"""
    folders = {}
    
    if not os.path.exists(corporativo_path):
        return folders
    
    for item in os.listdir(corporativo_path):
        folder_path = os.path.join(corporativo_path, item)
        if os.path.isdir(folder_path):
            files = []
            
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                    full_path = os.path.join(folder_path, filename)
                    try:
                        normalized_name = filename.lower().replace(' ', '').replace('_', '').replace('-', '')
                        normalized_name = ''.join(c for c in normalized_name if c.isalnum() or c == '.')
                        
                        files.append({
                            'filename': filename,
                            'normalized': normalized_name,
                            'size': os.path.getsize(full_path) / (1024 * 1024)
                        })
                    except:
                        continue
            
            if files:
                folders[item] = files
    
    return folders

def main():
    print("Verificando TODAS as pastas Corporativo vs S3 sergio_sena")
    print("=" * 60)
    
    corporativo_path = r"C:\Users\dell 5557\Videos\IDM\Corporativo"
    
    # Obter arquivos
    print("Carregando arquivos S3 sergio_sena...")
    s3_files = get_s3_files()
    s3_normalized = {f['normalized'] for f in s3_files}
    
    print("Carregando pastas locais Corporativo...")
    local_folders = get_local_files_by_folder(corporativo_path)
    
    print(f"S3 sergio_sena: {len(s3_files)} arquivos")
    print(f"Pastas Corporativo: {len(local_folders)} pastas")
    print()
    
    # Analisar cada pasta
    total_missing_size = 0
    total_missing_count = 0
    folder_summary = []
    
    for folder_name, files in local_folders.items():
        local_normalized = {f['normalized'] for f in files}
        missing_in_s3 = local_normalized - s3_normalized
        already_in_s3 = local_normalized.intersection(s3_normalized)
        
        missing_files = [f for f in files if f['normalized'] in missing_in_s3]
        missing_size = sum(f['size'] for f in missing_files)
        
        coverage = (len(already_in_s3) / len(files) * 100) if files else 0
        
        folder_summary.append({
            'name': folder_name,
            'total': len(files),
            'synced': len(already_in_s3),
            'missing': len(missing_in_s3),
            'missing_size': missing_size,
            'coverage': coverage,
            'missing_files': missing_files
        })
        
        total_missing_count += len(missing_in_s3)
        total_missing_size += missing_size
    
    # Ordenar por cobertura (menor primeiro = mais critico)
    folder_summary.sort(key=lambda x: x['coverage'])
    
    print("RESUMO POR PASTA (ordenado por prioridade):")
    print("-" * 60)
    
    for folder in folder_summary:
        status = "CRITICO" if folder['coverage'] < 50 else "PARCIAL" if folder['coverage'] < 95 else "OK"
        print(f"{folder['name']:<20} | {folder['synced']:2d}/{folder['total']:2d} | {folder['coverage']:5.1f}% | {folder['missing_size']:6.1f}MB | {status}")
    
    print()
    print("DETALHES DOS ARQUIVOS FALTANTES:")
    print("-" * 50)
    
    for folder in folder_summary:
        if folder['missing'] > 0:
            print(f"\n{folder['name']} - {folder['missing']} arquivos faltando ({folder['missing_size']:.1f} MB):")
            
            for i, file in enumerate(folder['missing_files'], 1):
                safe_name = file['filename'][:50] + "..." if len(file['filename']) > 50 else file['filename']
                try:
                    print(f"  {i:2d}. {safe_name} ({file['size']:.1f} MB)")
                except:
                    print(f"  {i:2d}. [arquivo com caracteres especiais] ({file['size']:.1f} MB)")
    
    print(f"\nRESUMO GERAL:")
    print("-" * 30)
    print(f"Total de pastas: {len(local_folders)}")
    print(f"Arquivos faltantes: {total_missing_count}")
    print(f"Tamanho total faltante: {total_missing_size:.1f} MB ({total_missing_size/1024:.2f} GB)")
    
    # Recomendacoes
    critical_folders = [f for f in folder_summary if f['coverage'] < 50]
    partial_folders = [f for f in folder_summary if 50 <= f['coverage'] < 95]
    ok_folders = [f for f in folder_summary if f['coverage'] >= 95]
    
    print(f"\nRECOMENDACAO DE UPLOAD:")
    print(f"Pastas CRITICAS (< 50%): {len(critical_folders)} pastas")
    print(f"Pastas PARCIAIS (50-95%): {len(partial_folders)} pastas") 
    print(f"Pastas OK (>= 95%): {len(ok_folders)} pastas")
    
    if critical_folders:
        critical_size = sum(f['missing_size'] for f in critical_folders)
        print(f"\nPRIORIDADE 1 - Pastas criticas: {critical_size:.1f} MB")
        for f in critical_folders:
            print(f"  {f['name']}: {f['missing']} arquivos ({f['missing_size']:.1f} MB)")

if __name__ == "__main__":
    main()