# -*- coding: utf-8 -*-
import os
import re
import subprocess
import boto3
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'
TS_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\arquivos TS'
MP4_DIR = r'C:\Users\dell 5557\Videos\IDM\Corporativo\MP4'

def sanitize_filename(filename):
    """Remove emojis e caracteres especiais"""
    # Remove extensão
    name, ext = os.path.splitext(filename)
    
    # Remove emojis e caracteres especiais
    sanitized = re.sub(r'[^\w\s.-]', '_', name)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized)
    sanitized = sanitized.strip('_')
    
    if not sanitized:
        sanitized = 'video'
    
    return sanitized + ext

def check_s3_exists(s3_key):
    """Verifica se arquivo já existe no S3"""
    try:
        s3.head_object(Bucket=BUCKET, Key=s3_key)
        return True
    except:
        return False

def convert_ts_to_mp4(ts_file, mp4_file):
    """Converte .ts para .mp4 usando ffmpeg"""
    cmd = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        '-i', ts_file,
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+fastcorporativot',
        '-y',
        mp4_file
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    for line in process.stdout:
        if 'time=' in line:
            print(f'\r  {line.strip()}', end='', flush=True)
    
    process.wait()
    print()
    return process.returncode == 0

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

def delete_ts_from_s3(s3_folder, mp4_name):
    """Deleta arquivo .ts do S3 após conversão bem-sucedida"""
    ts_name = mp4_name.replace('.mp4', '.ts')
    ts_key = f"{s3_folder}/{ts_name}"
    
    try:
        s3.head_object(Bucket=BUCKET, Key=ts_key)
        s3.delete_object(Bucket=BUCKET, Key=ts_key)
        print(f"  ✓ Deletado do S3: {ts_key}")
        return True
    except:
        return False

def find_all_ts_in_s3():
    """Procura todos os arquivos .ts em qualquer user no S3"""
    print("\n[VERIFICAÇÃO] Procurando arquivos .ts em todos os users...")
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET, Prefix='users/')
    
    ts_files = []
    for page in pages:
        if 'Contents' not in page:
            continue
        
        for obj in page['Contents']:
            if obj['Key'].lower().endswith('.ts'):
                ts_files.append(obj['Key'])
    
    return ts_files

# Criar diretório de saída
Path(MP4_DIR).mkdir(parents=True, exist_ok=True)

# Licorporativo arquivos .ts
ts_files = list(Path(TS_DIR).glob('*.ts'))
print(f"[INFO] Encontrados {len(ts_files)} arquivos .ts\n")

if not ts_files:
    print("[ERRO] Nenhum arquivo .ts encontrado!")
    exit(1)

# Processar cada arquivo
converted = 0
uploaded = 0
skipped = 0

for idx, ts_file in enumerate(ts_files, 1):
    print(f"[{idx}/{len(ts_files)}] Processando: {ts_file.name}")
    
    # Sanitizar nome
    sanitized_name = sanitize_filename(ts_file.name)
    mp4_name = sanitized_name.replace('.ts', '.mp4')
    mp4_file = os.path.join(MP4_DIR, mp4_name)
    
    if sanitized_name != ts_file.name:
        print(f"  Nome sanitizado: {mp4_name}")
    
    # Determinar pasta no S3 baseado no nome original
    original_name = ts_file.name
    if 'Creamy_Spot' in original_name:
        s3_folder = 'users/sergio_sena/Corporativo/Creamy_Spot'
    elif 'Lisinha' in original_name or 'BRANQUINHA' in original_name or 'Brincando' in original_name or 'Cindel' in original_name or 'Garota' in original_name or 'Que_Tal' in original_name or 'Universit' in original_name or 'cindel' in original_name:
        s3_folder = 'users/sergio_sena/Corporativo/Lisinha'
    elif 'angel' in original_name or 'Garota_Perfeita' in original_name:
        s3_folder = 'users/sergio_sena/Corporativo/angel'
    else:
        s3_folder = 'users/sergio_sena/Corporativo'
    
    s3_key = f"{s3_folder}/{mp4_name}"
    
    # Verificar se já existe no S3
    if check_s3_exists(s3_key):
        print(f"  SKIP - Ja existe no S3: {s3_key}\n")
        skipped += 1
        continue
    
    # Converter
    print(f"  Convertendo para MP4...")
    if convert_ts_to_mp4(str(ts_file), mp4_file):
        converted += 1
        
        # Upload para S3
        print(f"  Enviando para S3: {s3_key}")
        try:
            upload_to_s3(mp4_file, s3_key)
            uploaded += 1
            print(f"  OK - Upload concluido!")
            
            # Deletar .ts do S3 após upload bem-sucedido
            delete_ts_from_s3(s3_folder, mp4_name)
            
            # Remover arquivo local após upload
            os.remove(mp4_file)
            print()
            
        except Exception as e:
            print(f"  ERRO no upload: {str(e)}\n")
    else:
        print(f"  ERRO na conversao\n")

print(f"\n[RESUMO]")
print(f"  Total de arquivos: {len(ts_files)}")
print(f"  Convertidos: {converted}")
print(f"  Enviados para S3: {uploaded}")
print(f"  Pulados (ja existem): {skipped}")
print(f"  Falhas: {len(ts_files) - converted - skipped}")

# Verificar se há mais arquivos .ts em qualquer user
ts_remaining = find_all_ts_in_s3()

if ts_remaining:
    print(f"\n[AVISO] Encontrados {len(ts_remaining)} arquivos .ts no S3:")
    for ts_file in ts_remaining:
        print(f"  - {ts_file}")
else:
    print(f"\n[OK] Nenhum arquivo .ts encontrado no S3!")
