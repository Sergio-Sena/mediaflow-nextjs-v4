#!/usr/bin/env python3
"""
Upload de pasta completa com sanitizacao automatica
USO: python upload-folder-sanitized.py "C:\caminho\pasta" "destino/s3/"
"""

import boto3
import sys
from pathlib import Path
import unicodedata
import re

def sanitize_filename(filename):
    """Sanitizar nome do arquivo"""
    nfkd = unicodedata.normalize('NFKD', filename)
    filename = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    filename = re.sub(r'[^\w\s\.\-]', '', filename)
    filename = re.sub(r'\s+', ' ', filename)
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    if len(name) > 200:
        name = name[:200]
    return f"{name}.{ext}" if ext else name

def upload_folder(local_path, s3_prefix):
    """Upload pasta com sanitizacao"""
    local_path = Path(local_path)
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket = 'mediaflow-uploads-969430605054'
    
    if not s3_prefix.endswith('/'):
        s3_prefix += '/'
    
    print(f"Upload com sanitizacao")
    print("=" * 50)
    print(f"Local: {local_path}")
    print(f"S3: s3://{bucket}/{s3_prefix}")
    print(f"Storage: INTELLIGENT_TIERING")
    print()
    
    if not local_path.exists():
        print("ERRO: Pasta nao encontrada!")
        return False
    
    files = list(local_path.rglob('*'))
    files = [f for f in files if f.is_file()]
    
    print(f"Total: {files} arquivos")
    total_size = sum(f.stat().st_size for f in files) / (1024**3)
    print(f"Tamanho: {total_size:.2f} GB")
    print()
    
    uploaded = 0
    skipped = 0
    
    for file_path in files:
        try:
            original = file_path.name
            sanitized = sanitize_filename(original)
            
            rel_path = file_path.relative_to(local_path)
            rel_dir = rel_path.parent
            
            if str(rel_dir) != '.':
                s3_key = f"{s3_prefix}{rel_dir}/{sanitized}".replace('\\', '/')
            else:
                s3_key = f"{s3_prefix}{sanitized}"
            
            # Verificar se existe
            try:
                s3.head_object(Bucket=bucket, Key=s3_key)
                print(f"[SKIP] {sanitized}")
                skipped += 1
                continue
            except:
                pass
            
            # Upload
            size_mb = file_path.stat().st_size / (1024**2)
            try:
                print(f"[UP] {sanitized} ({size_mb:.1f} MB)")
            except:
                print(f"[UP] [arquivo especial] ({size_mb:.1f} MB)")
            
            s3.upload_file(
                str(file_path), bucket, s3_key,
                ExtraArgs={
                    'StorageClass': 'INTELLIGENT_TIERING',
                    'ContentType': 'video/mp4' if file_path.suffix.lower() in ['.mp4', '.mkv', '.avi'] else 'application/octet-stream'
                }
            )
            uploaded += 1
            
        except Exception as e:
            print(f"[ERRO] {e}")
    
    print()
    print("=" * 50)
    print(f"Enviados: {uploaded}")
    print(f"Pulados: {skipped}")
    print(f"Total: {len(files)}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USO: python upload-folder-sanitized.py \"C:\\caminho\\pasta\" \"users/user_admin/destino/\"")
        sys.exit(1)
    
    upload_folder(sys.argv[1], sys.argv[2])
