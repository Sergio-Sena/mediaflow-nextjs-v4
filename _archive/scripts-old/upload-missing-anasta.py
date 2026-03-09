#!/usr/bin/env python3
import boto3
from pathlib import Path
import unicodedata
import re

def sanitize_filename(filename):
    nfkd = unicodedata.normalize('NFKD', filename)
    filename = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    filename = re.sub(r'[^\w\s\.\-]', '', filename)
    filename = re.sub(r'\s+', ' ', filename)
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    if len(name) > 200:
        name = name[:200]
    return f"{name}.{ext}" if ext else name

local_path = Path(r"C:\Users\dell 5557\Videos\IDM\Corporativo\Anasta_angel")
s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/Corporativo/Anasta_angel/'

print("Enviando arquivos faltantes...")
for file_path in local_path.glob('*.mp4'):
    sanitized = sanitize_filename(file_path.name)
    s3_key = f"{prefix}{sanitized}"
    
    try:
        s3.head_object(Bucket=bucket, Key=s3_key)
        print(f"[OK] {sanitized}")
    except:
        try:
            print(f"[UP] {file_path.name} -> {sanitized}")
        except:
            print(f"[UP] [arquivo especial] -> {sanitized}")
        s3.upload_file(
            str(file_path), bucket, s3_key,
            ExtraArgs={'StorageClass': 'INTELLIGENT_TIERING', 'ContentType': 'video/mp4'}
        )
        print(f"     Enviado!")

print("\nConcluido!")
