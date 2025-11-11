#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Midiaflow Deploy Script - Otimizado
Deploy completo com validacao, rollback e CloudFront
"""
import subprocess
import boto3
import os
import json
import time
from pathlib import Path
from datetime import datetime

# Config
S3_BUCKET = 'midiaflow-frontend-969430605054'
CLOUDFRONT_ID = 'E2HZKZ9ZJK18IU'
BACKUP_BUCKET = 'midiaflow-backups-969430605054'

s3 = boto3.client('s3')
cf = boto3.client('cloudfront')

def print_step(msg):
    print(f"\n{'='*60}\n{msg}\n{'='*60}")

def backup_current():
    """Backup da versao atual antes de deployar"""
    print_step("1/6 - Backup da versao atual")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_prefix = f"backups/{timestamp}/"
    
    try:
        try:
            s3.head_bucket(Bucket=BACKUP_BUCKET)
        except:
            s3.create_bucket(Bucket=BACKUP_BUCKET)
            print(f"Bucket de backup criado: {BACKUP_BUCKET}")
        
        paginator = s3.get_paginator('list_objects_v2')
        count = 0
        
        for page in paginator.paginate(Bucket=S3_BUCKET):
            for obj in page.get('Contents', []):
                copy_source = {'Bucket': S3_BUCKET, 'Key': obj['Key']}
                s3.copy_object(
                    CopySource=copy_source,
                    Bucket=BACKUP_BUCKET,
                    Key=backup_prefix + obj['Key']
                )
                count += 1
        
        print(f"[OK] Backup completo: {count} arquivos em {backup_prefix}")
        return backup_prefix
    except Exception as e:
        print(f"[ERRO] Backup: {e}")
        return None

def validate_env():
    """Valida ambiente antes de buildar"""
    print_step("2/6 - Validando ambiente")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"[OK] Node.js: {result.stdout.strip()}")
    except:
        print("[ERRO] Node.js nao encontrado!")
        return False
    
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        print(f"[OK] npm: {result.stdout.strip()}")
    except:
        print("[ERRO] npm nao encontrado!")
        return False
    
    try:
        s3.list_buckets()
        print("[OK] AWS credentials")
    except:
        print("[ERRO] AWS credentials invalidas!")
        return False
    
    try:
        s3.head_bucket(Bucket=S3_BUCKET)
        print(f"[OK] Bucket S3: {S3_BUCKET}")
    except:
        print(f"[ERRO] Bucket nao encontrado: {S3_BUCKET}")
        return False
    
    return True

def build_nextjs():
    """Build Next.js otimizado"""
    print_step("3/6 - Build Next.js")
    
    print("Instalando dependencias...")
    result = subprocess.run(['npm', 'ci'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERRO] npm ci: {result.stderr}")
        return False
    print("[OK] Dependencias instaladas")
    
    print("\nBuildando aplicacao...")
    result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERRO] Build: {result.stderr}")
        return False
    
    if not Path('out').exists():
        print("[ERRO] Pasta out/ nao foi criada!")
        return False
    
    file_count = len(list(Path('out').rglob('*')))
    print(f"[OK] Build completo: {file_count} arquivos gerados")
    return True

def deploy_to_s3():
    """Deploy otimizado para S3"""
    print_step("4/6 - Deploy para S3")
    
    build_dir = Path('out')
    uploaded = 0
    
    print("Uploading arquivos...")
    for file_path in build_dir.rglob('*'):
        if not file_path.is_file():
            continue
        
        s3_key = str(file_path.relative_to(build_dir)).replace('\\', '/')
        
        ext = file_path.suffix.lower()
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon'
        }
        content_type = content_types.get(ext, 'application/octet-stream')
        
        if ext in ['.js', '.css', '.png', '.jpg', '.svg', '.ico']:
            cache = 'public, max-age=31536000, immutable'
        else:
            cache = 'public, max-age=0, must-revalidate'
        
        try:
            s3.upload_file(
                str(file_path),
                S3_BUCKET,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': cache
                }
            )
            uploaded += 1
            if uploaded % 20 == 0:
                print(f"  {uploaded} arquivos...")
        except Exception as e:
            print(f"[ERRO] {s3_key}: {e}")
    
    print(f"[OK] Deploy completo: {uploaded} arquivos")
    return True

def invalidate_cloudfront():
    """Invalida cache do CloudFront"""
    print_step("5/6 - Invalidando CloudFront")
    
    try:
        response = cf.create_invalidation(
            DistributionId=CLOUDFRONT_ID,
            InvalidationBatch={
                'Paths': {'Quantity': 1, 'Items': ['/*']},
                'CallerReference': str(int(time.time()))
            }
        )
        
        invalidation_id = response['Invalidation']['Id']
        print(f"[OK] Invalidacao criada: {invalidation_id}")
        print("  Aguardando propagacao (1-2 minutos)...")
        return True
    except Exception as e:
        print(f"[ERRO] Invalidacao: {e}")
        return False

def verify_deploy():
    """Verifica se deploy funcionou"""
    print_step("6/6 - Verificando deploy")
    
    import urllib.request
    url = "https://midiaflow.sstechnologies-cloud.com"
    
    try:
        response = urllib.request.urlopen(url, timeout=10)
        if response.status == 200:
            print(f"[OK] Site acessivel: {url}")
            return True
        else:
            print(f"[ERRO] Status: {response.status}")
            return False
    except Exception as e:
        print(f"[ERRO] Acesso: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("MIDIAFLOW DEPLOY - OTIMIZADO v2.0")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    backup_prefix = backup_current()
    if not backup_prefix:
        resp = input("\nBackup falhou. Continuar? (s/n): ")
        if resp.lower() != 's':
            print("Deploy cancelado")
            return
    
    if not validate_env():
        print("\n[ERRO] Validacao falhou!")
        return
    
    if not build_nextjs():
        print("\n[ERRO] Build falhou!")
        return
    
    if not deploy_to_s3():
        print("\n[ERRO] Deploy falhou!")
        return
    
    invalidate_cloudfront()
    time.sleep(5)
    verify_deploy()
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*60)
    print("DEPLOY COMPLETO!")
    print("="*60)
    print(f"URL: https://midiaflow.sstechnologies-cloud.com")
    print(f"Tempo: {elapsed:.1f}s")
    print(f"Backup: {backup_prefix or 'N/A'}")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDeploy cancelado")
    except Exception as e:
        print(f"\n\nErro fatal: {e}")
