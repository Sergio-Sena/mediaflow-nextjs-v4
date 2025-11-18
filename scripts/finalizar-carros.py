#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import boto3
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

s3 = boto3.client('s3', region_name='us-east-1',
    aws_access_key_id='AKIA6DNURDT7MO5EXHLQ',
    aws_secret_access_key='9wmyrw4365OTX+hwZ2ZZXjE+lbEUxn3INY4tu0Ir')

BUCKET = 'mediaflow-uploads-969430605054'
USER = 'lid-lima'

print("=== FINALIZANDO CARROS ===\n")

# 1. Upload arquivos faltantes
pasta = Path(r"C:\Users\dell 5557\Videos\Carros")
for mp4 in pasta.glob("*.mp4"):
    s3_key = f"users/{USER}/Carros/{mp4.name}"
    
    try:
        s3.head_object(Bucket=BUCKET, Key=s3_key)
        print(f"OK: {mp4.name} ja existe")
    except:
        print(f"Enviando: {mp4.name} ({mp4.stat().st_size/(1024**3):.2f} GB)")
        s3.upload_file(str(mp4), BUCKET, s3_key)
        print("  -> Enviado!\n")

# 2. Limpar MKV do S3
print("\n=== LIMPANDO MKV S3 ===")
resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=f"users/{USER}/Carros/")
if 'Contents' in resp:
    for obj in resp['Contents']:
        if obj['Key'].endswith('.mkv'):
            print(f"Removendo S3: {obj['Key'].split('/')[-1]}")
            s3.delete_object(Bucket=BUCKET, Key=obj['Key'])

# 3. Limpar MKV local
print("\n=== LIMPANDO MKV LOCAL ===")
for mkv in pasta.rglob("*.mkv"):
    print(f"Removendo: {mkv.name}")
    mkv.unlink()

print("\n=== CONCLUIDO ===")
