# -*- coding: utf-8 -*-
import os
import re
import boto3
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
TS_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\arquivos TS'

def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    sanitized = re.sub(r'[^\w\s.-]', '_', name)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    return (sanitized or 'video') + ext

def check_s3_exists(s3_key):
    try:
        s3.head_object(Bucket=BUCKET, Key=s3_key)
        return True
    except:
        return False

def upload_to_s3(local_file, s3_key):
    file_size = os.path.getsize(local_file)
    uploaded = 0
    
    def callback(bytes_transferred):
        nonlocal uploaded
        uploaded = bytes_transferred
        mb = uploaded / (1024 * 1024)
        percent = (uploaded / file_size) * 100
        print(f'\r  Upload: {mb:.2f} MB ({percent:.1f}%)', end='', flush=True)
    
    s3.upload_file(local_file, BUCKET, s3_key, Callback=callback)
    print()

ts_files = list(Path(TS_DIR).glob('*.ts'))
print(f"[INFO] Encontrados {len(ts_files)} arquivos .ts\n")

if not ts_files:
    print("[ERRO] Nenhum arquivo .ts encontrado!")
    exit(1)

uploaded = 0
skipped = 0

for idx, ts_file in enumerate(ts_files, 1):
    print(f"[{idx}/{len(ts_files)}] {ts_file.name}")
    
    sanitized_name = sanitize_filename(ts_file.name)
    
    original_name = ts_file.name
    if 'Creamy_Spot' in original_name:
        s3_folder = 'users/sergio_sena/Corporativo/Creamy_Spot'
    elif 'Lisinha' in original_name or 'BRANQUINHA' in original_name or 'Brincando' in original_name or 'Cindel' in original_name or 'Garota' in original_name or 'Que_Tal' in original_name or 'Universit' in original_name or 'cindel' in original_name:
        s3_folder = 'users/sergio_sena/Corporativo/Lisinha'
    elif 'angel' in original_name or 'Garota_Perfeita' in original_name:
        s3_folder = 'users/sergio_sena/Corporativo/angel'
    else:
        s3_folder = 'users/sergio_sena/Corporativo'
    
    s3_key = f"{s3_folder}/{sanitized_name}"
    
    if check_s3_exists(s3_key):
        print(f"  SKIP - Ja existe: {s3_key}\n")
        skipped += 1
        continue
    
    print(f"  Enviando para: {s3_key}")
    try:
        upload_to_s3(str(ts_file), s3_key)
        uploaded += 1
        print(f"  OK!\n")
    except Exception as e:
        print(f"  ERRO: {e}\n")

print(f"\n[RESUMO]")
print(f"  Total: {len(ts_files)}")
print(f"  Enviados: {uploaded}")
print(f"  Pulados: {skipped}")
print(f"  Falhas: {len(ts_files) - uploaded - skipped}")
