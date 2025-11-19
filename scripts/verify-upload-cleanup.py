# -*- coding: utf-8 -*-
import os
import boto3
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
MP4_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\MP4'
S3_FOLDER = 'users/sergio_sena/Corporativo'

def check_s3_exists(s3_key):
    """Verifica se arquivo já existe no S3"""
    try:
        s3.head_object(Bucket=BUCKET, Key=s3_key)
        return True
    except:
        return False

def upload_to_s3(local_file, s3_key):
    """Upload arquivo para S3 com progresso"""
    file_size = os.path.getsize(local_file)
    uploaded = 0
    
    def callback(bytes_transferred):
        nonlocal uploaded
        uploaded = bytes_transferred
        percent = (uploaded / file_size) * 100
        mb = uploaded / (1024 * 1024)
        print(f'\r  Upload: {mb:.2f} MB ({percent:.1f}%)', end='', flush=True)
    
    s3.upload_file(local_file, BUCKET, s3_key, Callback=callback)
    print()

def delete_from_s3(s3_key):
    """Deleta arquivo do S3"""
    try:
        s3.delete_object(Bucket=BUCKET, Key=s3_key)
        return True
    except:
        return False

def verify_ts_in_s3():
    """Verifica se há arquivos .ts no S3 em sergio_sena/Corporativo"""
    print("[VERIFICAÇÃO] Procurando arquivos .ts em sergio_sena/Corporativo...\n")
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET, Prefix=S3_FOLDER)
    
    ts_files = []
    for page in pages:
        if 'Contents' not in page:
            continue
        
        for obj in page['Contents']:
            if obj['Key'].lower().endswith('.ts'):
                ts_files.append(obj['Key'])
    
    if ts_files:
        print(f"[AVISO] Encontrados {len(ts_files)} arquivos .ts:\n")
        for ts_file in ts_files:
            print(f"  - {ts_file}")
        print()
    else:
        print("[OK] Nenhum arquivo .ts encontrado em sergio_sena/Corporativo\n")
    
    return ts_files

def process_mp4_files():
    """Processa arquivos MP4 locais"""
    print("[PROCESSAMENTO] Iniciando upload de arquivos MP4...\n")
    
    mp4_files = list(Path(MP4_DIR).glob('*.mp4'))
    
    if not mp4_files:
        print("[ERRO] Nenhum arquivo .mp4 encontrado em MP4_DIR!")
        return 0, 0, 0
    
    print(f"Encontrados {len(mp4_files)} arquivos .mp4\n")
    print("=" * 60)
    
    uploaded = 0
    skipped = 0
    errors = 0
    uploaded_files = []
    
    for idx, mp4_file in enumerate(mp4_files, 1):
        mp4_name = mp4_file.name
        s3_key = f"{S3_FOLDER}/{mp4_name}"
        
        print(f"\n[{idx}/{len(mp4_files)}] {mp4_name}")
        
        # Verificar se já existe no S3
        if check_s3_exists(s3_key):
            print(f"  SKIP - Já existe no S3")
            skipped += 1
            continue
        
        # Upload
        print(f"  Enviando para S3...")
        try:
            upload_to_s3(str(mp4_file), s3_key)
            uploaded += 1
            uploaded_files.append((mp4_file, mp4_name))
            print(f"  ✓ Upload concluído!")
            
        except Exception as e:
            print(f"  ✗ ERRO no upload: {str(e)}")
            errors += 1
    
    print("\n" + "=" * 60)
    return uploaded, skipped, errors, uploaded_files

def cleanup(uploaded_files):
    """Deleta arquivos locais .mp4 e .ts do S3 após upload bem-sucedido"""
    print("\n[LIMPEZA] Removendo arquivos...\n")
    
    deleted_local = 0
    deleted_s3 = 0
    
    for mp4_file, mp4_name in uploaded_files:
        # Deletar arquivo local .mp4
        try:
            os.remove(str(mp4_file))
            print(f"  ✓ Deletado local: {mp4_name}")
            deleted_local += 1
        except Exception as e:
            print(f"  ✗ Erro ao deletar local {mp4_name}: {e}")
        
        # Deletar arquivo .ts do S3
        ts_name = mp4_name.replace('.mp4', '.ts')
        ts_key = f"{S3_FOLDER}/{ts_name}"
        
        if delete_from_s3(ts_key):
            print(f"  ✓ Deletado S3: {ts_name}")
            deleted_s3 += 1
        else:
            print(f"  - Não encontrado S3: {ts_name}")
    
    return deleted_local, deleted_s3

if __name__ == "__main__":
    print("=" * 60)
    print("VERIFICAÇÃO, UPLOAD E LIMPEZA DE ARQUIVOS")
    print("=" * 60 + "\n")
    
    # 1. Verificar .ts no S3
    ts_in_s3 = verify_ts_in_s3()
    
    # 2. Processar e fazer upload dos .mp4
    uploaded, skipped, errors, uploaded_files = process_mp4_files()
    
    # 3. Limpeza
    if uploaded_files:
        deleted_local, deleted_s3 = cleanup(uploaded_files)
    else:
        deleted_local = 0
        deleted_s3 = 0
    
    # Resumo final
    print("\n" + "=" * 60)
    print("[RESUMO FINAL]")
    print(f"  Arquivos .ts encontrados no S3: {len(ts_in_s3)}")
    print(f"  Arquivos .mp4 enviados: {uploaded}")
    print(f"  Arquivos .mp4 pulados (já existem): {skipped}")
    print(f"  Erros no upload: {errors}")
    print(f"  Arquivos locais deletados: {deleted_local}")
    print(f"  Arquivos .ts deletados do S3: {deleted_s3}")
    print("=" * 60)
