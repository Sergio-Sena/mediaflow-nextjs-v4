#!/usr/bin/env python3
"""
Verificar arquivos kate kuray no S3 sergio_sena vs pasta local Star
"""

import boto3
import os

def get_kate_kuray_local():
    """Obter arquivos kate kuray da pasta Star local"""
    star_path = r"C:\Users\dell 5557\Videos\IDM\Star\kate kuray"
    local_files = []
    
    if not os.path.exists(star_path):
        return local_files
    
    for filename in os.listdir(star_path):
        if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            full_path = os.path.join(star_path, filename)
            try:
                normalized_name = filename.lower().replace(' ', '').replace('_', '').replace('-', '')
                normalized_name = ''.join(c for c in normalized_name if c.isalnum() or c == '.')
                
                local_files.append({
                    'filename': filename,
                    'normalized': normalized_name,
                    'size': os.path.getsize(full_path) / (1024 * 1024)
                })
            except:
                continue
    
    return local_files

def get_kate_kuray_s3():
    """Obter arquivos kate kuray do S3 sergio_sena"""
    s3_client = boto3.client('s3')
    bucket_name = 'mediaflow-uploads-969430605054'
    s3_files = []
    
    try:
        # Buscar em todas as pastas do sergio_sena que contenham kate kuray
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix='users/sergio_sena/')
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    filename = key.split('/')[-1]
                    
                    # Verificar se é arquivo kate kuray
                    if ('kate' in key.lower() or 'kuray' in key.lower()) and filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
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

def main():
    print("Verificando arquivos Kate Kuray: Local vs S3 sergio_sena")
    print("=" * 60)
    
    # Obter arquivos
    print("Carregando arquivos locais (Star/kate kuray)...")
    local_files = get_kate_kuray_local()
    
    print("Carregando arquivos S3 sergio_sena (kate kuray)...")
    s3_files = get_kate_kuray_s3()
    
    print(f"Kate Kuray local: {len(local_files)} arquivos")
    print(f"Kate Kuray S3: {len(s3_files)} arquivos")
    print()
    
    # Criar indices
    s3_normalized = {f['normalized'] for f in s3_files}
    local_normalized = {f['normalized'] for f in local_files}
    
    # Analise
    already_in_s3 = local_normalized.intersection(s3_normalized)
    missing_in_s3 = local_normalized - s3_normalized
    only_in_s3 = s3_normalized - local_normalized
    
    print("ANALISE KATE KURAY:")
    print("-" * 40)
    print(f"Ja no S3: {len(already_in_s3)} arquivos")
    print(f"Faltando no S3: {len(missing_in_s3)} arquivos")
    print(f"Apenas no S3: {len(only_in_s3)} arquivos")
    print()
    
    # Mostrar arquivos faltantes
    if missing_in_s3:
        print("ARQUIVOS KATE KURAY FALTANDO NO S3:")
        print("-" * 50)
        
        missing_files = [f for f in local_files if f['normalized'] in missing_in_s3]
        total_size = 0
        
        for i, file in enumerate(missing_files, 1):
            safe_name = file['filename'][:60] + "..." if len(file['filename']) > 60 else file['filename']
            try:
                print(f"{i:2d}. {safe_name} ({file['size']:.1f} MB)")
            except:
                print(f"{i:2d}. [arquivo com caracteres especiais] ({file['size']:.1f} MB)")
            
            total_size += file['size']
        
        print(f"\nTOTAL FALTANDO: {len(missing_in_s3)} arquivos ({total_size:.1f} MB / {total_size/1024:.2f} GB)")
    else:
        print("TODOS OS ARQUIVOS KATE KURAY JA ESTAO NO S3!")
    
    # Resumo
    if local_files:
        coverage = (len(already_in_s3) / len(local_files) * 100)
        print(f"\nCOBERTURA KATE KURAY: {coverage:.1f}%")
        print(f"Sincronizados: {len(already_in_s3)}/{len(local_files)}")

if __name__ == "__main__":
    main()