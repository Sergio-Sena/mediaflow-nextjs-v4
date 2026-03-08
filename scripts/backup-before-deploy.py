#!/usr/bin/env python3
"""
Backup completo antes de qualquer deploy
"""
import boto3
import subprocess
import json
from datetime import datetime
import os

# Config
ACCOUNT_ID = '969430605054'
REGION = 'us-east-1'
CLOUDFRONT_ID = 'E1A2CZM0WKF6LX'
S3_FRONTEND = f'midiaflow-frontend-{ACCOUNT_ID}'
S3_BACKUP = f'midiaflow-backups-{ACCOUNT_ID}'

def create_backup():
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Get current version
    try:
        version = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
    except:
        version = 'unknown'
    
    backup_name = f'backup-{version}-{timestamp}'
    print(f'\n=== CRIANDO BACKUP: {backup_name} ===\n')
    
    # 1. Backup do código (Git)
    print('[1/4] Backup do codigo Git...')
    os.makedirs('backups', exist_ok=True)
    subprocess.run(['git', 'archive', '--format=zip', 'HEAD', '-o', f'backups/{backup_name}.zip'])
    print(f'  [OK] Codigo salvo em: backups/{backup_name}.zip')
    
    # 2. Criar bucket de backup se não existir
    print('[2/4] Verificando bucket de backup...')
    s3 = boto3.client('s3', region_name=REGION)
    try:
        s3.head_bucket(Bucket=S3_BACKUP)
        print(f'  [OK] Bucket existe: {S3_BACKUP}')
    except:
        print(f'  Criando bucket: {S3_BACKUP}...')
        s3.create_bucket(Bucket=S3_BACKUP)
        s3.put_bucket_versioning(
            Bucket=S3_BACKUP,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print(f'  [OK] Bucket criado com versionamento')
    
    # 3. Backup do S3 frontend
    print('[3/4] Backup do S3 frontend...')
    subprocess.run([
        'aws', 's3', 'sync',
        f's3://{S3_FRONTEND}',
        f's3://{S3_BACKUP}/{backup_name}/',
        '--storage-class', 'STANDARD_IA'
    ])
    print(f'  [OK] S3 copiado para: s3://{S3_BACKUP}/{backup_name}/')
    
    # 4. Backup da config CloudFront
    print('[4/4] Backup da configuracao CloudFront...')
    cf = boto3.client('cloudfront', region_name=REGION)
    config = cf.get_distribution_config(Id=CLOUDFRONT_ID)
    
    with open(f'backups/{backup_name}-cloudfront.json', 'w') as f:
        json.dump(config, f, indent=2, default=str)
    print(f'  [OK] CloudFront salvo em: backups/{backup_name}-cloudfront.json')
    
    # Salvar info do backup
    backup_info = {
        'name': backup_name,
        'version': version,
        'timestamp': timestamp,
        'cloudfront_id': CLOUDFRONT_ID,
        's3_frontend': S3_FRONTEND,
        's3_backup': S3_BACKUP,
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    }
    
    with open(f'backups/{backup_name}-info.json', 'w') as f:
        json.dump(backup_info, f, indent=2)
    
    print(f'\n[SUCCESS] BACKUP COMPLETO: {backup_name}')
    print(f'\nPara restaurar, execute:')
    print(f'  python scripts/rollback.py {backup_name}')
    
    return backup_name

if __name__ == '__main__':
    create_backup()
