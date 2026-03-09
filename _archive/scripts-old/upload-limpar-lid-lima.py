#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload e limpeza para lid lima (SEM conversão)
"""

import boto3
import os
import sys
import io
from pathlib import Path

# Fix encoding Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuração AWS
s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='AKIA6DNURDT7MO5EXHLQ',
    aws_secret_access_key='9wmyrw4365OTX+hwZ2ZZXjE+lbEUxn3INY4tu0Ir'
)

BUCKET = 'mediaflow-uploads-969430605054'
USER_ID = 'lid-lima'

def upload_pasta(pasta_base, pasta_nome):
    """Faz upload da pasta para S3"""
    print(f"\n[UPLOAD] {pasta_nome}")
    print("-" * 60)
    
    pasta = Path(pasta_base)
    arquivos = [f for f in pasta.rglob('*') if f.is_file()]
    
    print(f"Total: {len(arquivos)} arquivos")
    
    uploaded = 0
    skipped = 0
    
    for i, file_path in enumerate(arquivos, 1):
        relative_path = file_path.relative_to(pasta)
        s3_key = f"users/{USER_ID}/{pasta_nome}/{relative_path}".replace('\\', '/')
        
        try:
            # Verificar se já existe
            try:
                s3_client.head_object(Bucket=BUCKET, Key=s3_key)
                print(f"[{i}/{len(arquivos)}] Ja existe: {relative_path}")
                skipped += 1
                continue
            except:
                pass
            
            print(f"[{i}/{len(arquivos)}] Enviando: {relative_path}")
            s3_client.upload_file(str(file_path), BUCKET, s3_key)
            uploaded += 1
            
        except Exception as e:
            print(f"ERRO: {e}")
    
    print(f"\nOK: {uploaded} enviados | {skipped} ja existiam")

def limpar_nao_mp4(pasta_base, pasta_nome):
    """Remove arquivos não-MP4 (local e S3)"""
    print(f"\n[LIMPEZA] {pasta_nome}")
    print("-" * 60)
    
    # Limpar local
    pasta = Path(pasta_base)
    nao_mp4 = [f for f in pasta.rglob('*') if f.is_file() and f.suffix.lower() != '.mp4']
    
    print(f"Local: {len(nao_mp4)} arquivos nao-MP4")
    for arquivo in nao_mp4:
        try:
            print(f"Removendo: {arquivo.name}")
            arquivo.unlink()
        except Exception as e:
            print(f"ERRO: {e}")
    
    # Limpar S3
    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET,
            Prefix=f"users/{USER_ID}/{pasta_nome}/"
        )
        
        if 'Contents' in response:
            nao_mp4_s3 = [obj for obj in response['Contents'] if not obj['Key'].lower().endswith('.mp4')]
            
            print(f"S3: {len(nao_mp4_s3)} arquivos nao-MP4")
            for obj in nao_mp4_s3:
                try:
                    nome = obj['Key'].split('/')[-1]
                    print(f"Removendo S3: {nome}")
                    s3_client.delete_object(Bucket=BUCKET, Key=obj['Key'])
                except Exception as e:
                    print(f"ERRO: {e}")
    except Exception as e:
        print(f"ERRO S3: {e}")

def main():
    print("=" * 60)
    print("UPLOAD E LIMPEZA - LID LIMA")
    print("=" * 60)
    
    base_path = r"C:\Users\dell 5557\Videos"
    
    # Processar Carros
    print("\n>>> CARROS")
    upload_pasta(os.path.join(base_path, "Carros"), "Carros")
    limpar_nao_mp4(os.path.join(base_path, "Carros"), "Carros")
    
    # Processar Lilo & Stitch
    print("\n>>> LILO & STITCH")
    upload_pasta(os.path.join(base_path, "Lilo & Stitch"), "Lilo & Stitch")
    limpar_nao_mp4(os.path.join(base_path, "Lilo & Stitch"), "Lilo & Stitch")
    
    print("\n" + "=" * 60)
    print("CONCLUIDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()
