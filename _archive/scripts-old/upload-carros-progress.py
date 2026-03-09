#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload Carros com barra de progresso
"""

import boto3
import sys
import io
from pathlib import Path
from tqdm import tqdm

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

print(f"Carros: {len(arquivos)} arquivos")
print("-" * 60)

uploaded = 0
skipped = 0

with tqdm(total=len(arquivos), desc="Upload", unit="arquivo") as pbar:
    for file_path in arquivos:
        relative_path = file_path.relative_to(pasta)
        s3_key = f"users/{USER_ID}/Carros/{relative_path}".replace('\\', '/')
        
        try:
            # Verificar se existe
            try:
                s3_client.head_object(Bucket=BUCKET, Key=s3_key)
                skipped += 1
                pbar.set_postfix({"OK": uploaded, "Skip": skipped})
                pbar.update(1)
                continue
            except:
                pass
            
            s3_client.upload_file(str(file_path), BUCKET, s3_key)
            uploaded += 1
            pbar.set_postfix({"OK": uploaded, "Skip": skipped})
            pbar.update(1)
            
        except Exception as e:
            pbar.write(f"ERRO: {relative_path} - {e}")
            pbar.update(1)

print(f"\nOK: {uploaded} enviados | {skipped} ja existiam")
