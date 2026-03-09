#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload Carros - UM arquivo por vez
"""

import boto3
import sys
import io
from pathlib import Path

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='AKIA6DNURDT7MO5EXHLQ',
    aws_secret_access_key='9wmyrw4365OTX+hwZ2ZZXjE+lbEUxn3INY4tu0Ir'
)

BUCKET = 'mediaflow-uploads-969430605054'
USER_ID = 'lid-lima'

pasta = Path(r"C:\Users\dell 5557\Videos\Carros")
arquivos = [f for f in pasta.rglob('*') if f.is_file()]

print(f"Total: {len(arquivos)} arquivos\n")

for i, file_path in enumerate(arquivos, 1):
    relative_path = file_path.relative_to(pasta)
    s3_key = f"users/{USER_ID}/Carros/{relative_path}".replace('\\', '/')
    
    print(f"[{i}/{len(arquivos)}] {relative_path}")
    
    try:
        # Verificar se existe
        try:
            s3_client.head_object(Bucket=BUCKET, Key=s3_key)
            print("  -> Ja existe\n")
            continue
        except:
            pass
        
        # Upload
        tamanho = file_path.stat().st_size / (1024**2)  # MB
        print(f"  -> Enviando ({tamanho:.1f} MB)...")
        
        s3_client.upload_file(str(file_path), BUCKET, s3_key)
        print("  -> OK\n")
        
    except Exception as e:
        print(f"  -> ERRO: {e}\n")

print("CONCLUIDO!")
