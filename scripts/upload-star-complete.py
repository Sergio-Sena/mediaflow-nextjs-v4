#!/usr/bin/env python3
"""
Upload completo da pasta Star com sanitizacao e verificacao
Padrao para uploads via CLI
"""

import boto3
from pathlib import Path
import unicodedata
import re

# Configuracoes
LOCAL_PATH = Path(r"C:\Users\dell 5557\Videos\IDM\Star")
S3_BUCKET = 'mediaflow-uploads-969430605054'
S3_PREFIX = 'users/user_admin/Star/'

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

def analyze_files():
    """Contar e analisar arquivos"""
    print("=" * 60)
    print("ETAPA 1: ANALISE DE ARQUIVOS")
    print("=" * 60)
    
    files = list(LOCAL_PATH.rglob('*'))
    files = [f for f in files if f.is_file()]
    
    total_size = sum(f.stat().st_size for f in files) / (1024**3)
    
    # Verificar quais precisam sanitizacao
    need_sanitize = []
    for f in files:
        original = f.name
        sanitized = sanitize_filename(original)
        if original != sanitized:
            need_sanitize.append((original, sanitized))
    
    print(f"Total de arquivos: {len(files)}")
    print(f"Tamanho total: {total_size:.2f} GB")
    print(f"Arquivos que precisam sanitizacao: {len(need_sanitize)}")
    
    if need_sanitize:
        print("\nExemplos de sanitizacao:")
        for orig, san in need_sanitize[:5]:
            try:
                print(f"  {orig}")
                print(f"  -> {san}")
            except:
                print(f"  [arquivo especial] -> {san}")
        if len(need_sanitize) > 5:
            print(f"  ... e mais {len(need_sanitize) - 5}")
    
    print()
    return files

def upload_files(files):
    """Upload com sanitizacao mantendo estrutura"""
    print("=" * 60)
    print("ETAPA 2: UPLOAD COM SANITIZACAO")
    print("=" * 60)
    
    s3 = boto3.client('s3', region_name='us-east-1')
    
    uploaded = 0
    skipped = 0
    errors = 0
    
    for file_path in files:
        try:
            # Caminho relativo mantendo estrutura de pastas
            rel_path = file_path.relative_to(LOCAL_PATH)
            rel_dir = rel_path.parent
            
            # Sanitizar apenas o nome do arquivo, manter estrutura de pastas
            original_name = file_path.name
            sanitized_name = sanitize_filename(original_name)
            
            # Construir key S3 mantendo estrutura
            if str(rel_dir) != '.':
                s3_key = f"{S3_PREFIX}{rel_dir}/{sanitized_name}".replace('\\', '/')
            else:
                s3_key = f"{S3_PREFIX}{sanitized_name}"
            
            # Verificar se ja existe
            try:
                s3.head_object(Bucket=S3_BUCKET, Key=s3_key)
                print(f"[SKIP] {rel_path}")
                skipped += 1
                continue
            except:
                pass
            
            # Upload
            size_mb = file_path.stat().st_size / (1024**2)
            try:
                print(f"[UP] {rel_path} ({size_mb:.1f} MB)")
            except:
                print(f"[UP] {rel_dir}/[especial] ({size_mb:.1f} MB)")
            
            s3.upload_file(
                str(file_path),
                S3_BUCKET,
                s3_key,
                ExtraArgs={
                    'StorageClass': 'INTELLIGENT_TIERING',
                    'ContentType': 'video/mp4' if file_path.suffix.lower() in ['.mp4', '.mkv', '.avi'] else 'application/octet-stream'
                }
            )
            uploaded += 1
            
        except Exception as e:
            print(f"[ERRO] {file_path.name}: {e}")
            errors += 1
    
    print()
    print(f"Enviados: {uploaded}")
    print(f"Pulados (ja existem): {skipped}")
    print(f"Erros: {errors}")
    print()
    
    return uploaded, skipped, errors

def verify_upload(files):
    """Verificar se todos os arquivos foram enviados"""
    print("=" * 60)
    print("ETAPA 3: VERIFICACAO DE UPLOAD")
    print("=" * 60)
    
    s3 = boto3.client('s3', region_name='us-east-1')
    
    # Mapear arquivos locais (sanitizados) com seus caminhos
    local_files = {}
    for file_path in files:
        rel_path = file_path.relative_to(LOCAL_PATH)
        rel_dir = rel_path.parent
        sanitized_name = sanitize_filename(file_path.name)
        
        if str(rel_dir) != '.':
            s3_key = f"{S3_PREFIX}{rel_dir}/{sanitized_name}".replace('\\', '/')
        else:
            s3_key = f"{S3_PREFIX}{sanitized_name}"
        
        local_files[s3_key] = file_path
    
    # Verificar no S3
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX)
    
    s3_keys = set()
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                if not obj['Key'].endswith('/'):
                    s3_keys.add(obj['Key'])
    
    # Comparar
    missing = []
    for key, file_path in local_files.items():
        if key not in s3_keys:
            missing.append(file_path.relative_to(LOCAL_PATH))
    
    print(f"Arquivos locais: {len(local_files)}")
    print(f"Arquivos no S3: {len(s3_keys)}")
    print()
    
    if missing:
        print(f"ARQUIVOS FALTANDO ({len(missing)}):")
        for m in missing[:10]:
            try:
                print(f"  - {m}")
            except:
                print(f"  - [arquivo especial]")
        if len(missing) > 10:
            print(f"  ... e mais {len(missing) - 10}")
        print("\nVERIFICACAO: FALHOU")
        return False
    else:
        print("Todos os arquivos foram enviados com sucesso!")
        print("\nVERIFICACAO: PASSOU")
        return True

def main():
    """Executar upload completo"""
    print("\n")
    print("*" * 60)
    print("UPLOAD COMPLETO - PASTA STAR")
    print("*" * 60)
    print(f"Origem: {LOCAL_PATH}")
    print(f"Destino: s3://{S3_BUCKET}/{S3_PREFIX}")
    print(f"Storage: INTELLIGENT_TIERING")
    print("*" * 60)
    print("\n")
    
    # Etapa 1: Analisar
    files = analyze_files()
    
    # Etapa 2: Upload
    uploaded, skipped, errors = upload_files(files)
    
    # Etapa 3: Verificar
    success = verify_upload(files)
    
    # Resumo final
    print("\n")
    print("=" * 60)
    print("RESUMO FINAL")
    print("=" * 60)
    print(f"Total de arquivos: {len(files)}")
    print(f"Enviados: {uploaded}")
    print(f"Pulados: {skipped}")
    print(f"Erros: {errors}")
    print(f"Verificacao: {'PASSOU' if success else 'FALHOU'}")
    print("=" * 60)
    
    if success:
        print("\nUPLOAD COMPLETO E VERIFICADO!")
    else:
        print("\nALERTA: Alguns arquivos nao foram enviados!")
    
    return success

if __name__ == "__main__":
    main()
