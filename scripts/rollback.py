#!/usr/bin/env python3
"""
Rollback para backup anterior em caso de problema
"""
import boto3
import subprocess
import json
import sys
import os

def rollback(backup_name):
    print(f'\n=== INICIANDO ROLLBACK: {backup_name} ===\n')
    
    # Carregar info do backup
    info_file = f'backups/{backup_name}-info.json'
    if not os.path.exists(info_file):
        print(f'❌ Backup não encontrado: {backup_name}')
        print(f'\nBackups disponíveis:')
        for f in os.listdir('backups'):
            if f.endswith('-info.json'):
                print(f'  - {f.replace("-info.json", "")}')
        return
    
    with open(info_file) as f:
        info = json.load(f)
    
    print(f'Versão: {info["version"]}')
    print(f'Data: {info["timestamp"]}')
    print(f'Commit: {info["git_commit"][:8]}')
    
    confirm = input('\n⚠️  Confirma rollback? (sim/não): ')
    if confirm.lower() != 'sim':
        print('Rollback cancelado.')
        return
    
    # 1. Rollback do código
    print('\n[1/3] Restaurando codigo...')
    subprocess.run(['git', 'checkout', info['git_commit']])
    print(f'  [OK] Codigo restaurado para commit {info["git_commit"][:8]}')
    
    # 2. Rollback do S3
    print('[2/3] Restaurando S3 frontend...')
    subprocess.run([
        'aws', 's3', 'sync',
        f's3://{info["s3_backup"]}/{backup_name}/',
        f's3://{info["s3_frontend"]}',
        '--delete'
    ])
    print(f'  [OK] S3 restaurado')
    
    # 3. Invalidar CloudFront
    print('[3/3] Invalidando CloudFront...')
    cf = boto3.client('cloudfront', region_name='us-east-1')
    cf.create_invalidation(
        DistributionId=info['cloudfront_id'],
        InvalidationBatch={
            'Paths': {'Quantity': 1, 'Items': ['/*']},
            'CallerReference': f'rollback-{backup_name}'
        }
    )
    print(f'  [OK] CloudFront invalidado')
    
    print(f'\n[SUCCESS] ROLLBACK COMPLETO!')
    print(f'\nAplicação restaurada para: {info["version"]}')
    print(f'Aguarde 2-3 minutos para propagação do CloudFront.')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python rollback.py <backup_name>')
        print('\nBackups disponíveis:')
        if os.path.exists('backups'):
            for f in os.listdir('backups'):
                if f.endswith('-info.json'):
                    print(f'  - {f.replace("-info.json", "")}')
        sys.exit(1)
    
    rollback(sys.argv[1])
