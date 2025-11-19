# -*- coding: utf-8 -*-
import os
import sys
import io
import re
import subprocess
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
TS_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\arquivos TS'
STAR_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo'
S3_FOLDER = 'users/sergio_sena/Corporativo'

def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    sanitized = re.sub(r'[^\w\s.-]', '_', name)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized)
    sanitized = sanitized.strip('_')
    return (sanitized or 'video') + ext

def convert_ts_to_mp4_fast(ts_file, mp4_file):
    cmd = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        '-i', ts_file,
        '-c', 'copy',
        '-y',
        mp4_file
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                              universal_newlines=True, encoding='utf-8', errors='ignore')
    for line in process.stdout:
        if 'time=' in line:
            print(f'\r  {line.strip()}', end='', flush=True)
    process.wait()
    print()
    return process.returncode == 0

def upload_to_s3(local_file, s3_key):
    try:
        file_size = os.path.getsize(local_file)
        s3.upload_file(local_file, BUCKET, s3_key, 
                      Config=boto3.s3.transfer.TransferConfig(max_concurrency=1))
        return True
    except Exception as e:
        print(f"  [ERRO] {str(e)[:50]}")
        return False

def get_s3_files():
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET, Prefix=S3_FOLDER)
        
        files = set()
        for page in pages:
            if 'Contents' not in page:
                continue
            for obj in page['Contents']:
                filename = os.path.basename(obj['Key'])
                if filename:
                    files.add(filename)
        return files
    except Exception as e:
        print(f"[ERRO] Nao conseguiu licorporativo S3: {e}")
        return set()

print("=" * 70)
print("CONVERTER E SINCRONIZAR COM S3 (ROBUSTO)")
print("=" * 70 + "\n")

# 1. Converter .ts
print("[1/3] CONVERTENDO ARQUIVOS .TS\n")
ts_files = list(Path(TS_DIR).glob('*.ts'))
converted = 0

for idx, ts_file in enumerate(ts_files, 1):
    sanitized = sanitize_filename(ts_file.name)
    mp4_name = sanitized.replace('.ts', '.mp4')
    mp4_file = os.path.join(STAR_DIR, mp4_name)
    
    print(f"[{idx}/{len(ts_files)}] {ts_file.name}")
    
    if os.path.exists(mp4_file):
        print(f"  [SKIP] Ja existe\n")
        continue
    
    if convert_ts_to_mp4_fast(str(ts_file), mp4_file):
        converted += 1
        print(f"  [OK]\n")
        try:
            os.remove(str(ts_file))
        except:
            pass
    else:
        print(f"  [ERRO]\n")

print(f"Total convertido: {converted}\n")

# 2. Comparar com S3
print("[2/3] COMPARANDO COM S3\n")
s3_files = get_s3_files()
local_mp4 = {f.name for f in Path(STAR_DIR).glob('*.mp4')}

missing = local_mp4 - s3_files
print(f"Locais: {len(local_mp4)} | S3: {len(s3_files)} | Faltando: {len(missing)}\n")

# 3. Upload
if missing:
    print("[3/3] UPLOAD DOS FALTANTES\n")
    uploaded = 0
    failed = 0
    
    for idx, filename in enumerate(sorted(missing), 1):
        local_path = os.path.join(STAR_DIR, filename)
        s3_key = f"{S3_FOLDER}/{filename}"
        
        print(f"[{idx}/{len(missing)}] {filename}")
        
        if upload_to_s3(local_path, s3_key):
            uploaded += 1
            print(f"  [OK]\n")
        else:
            failed += 1
            print(f"  [FALHOU]\n")
    
    print(f"Enviados: {uploaded} | Falhados: {failed}\n")
else:
    print("[3/3] Nenhum faltando\n")

print("=" * 70)
print("[CONCLUIDO]")
print("=" * 70)
