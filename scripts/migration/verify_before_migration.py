#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificações antes da migração"""

import boto3
import os
import sys
from dotenv import load_dotenv

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv('.env.local')

# Config AWS
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
s3 = boto3.client(
    's3',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

table = dynamodb.Table('mediaflow-users')
bucket = 'mediaflow-uploads-969430605054'

print("\n" + "="*60)
print("  [VERIFICACAO] PRE-MIGRACAO")
print("="*60)

# 1. Verificar user_admin
print("\n[1] Verificando user_admin...")
try:
    resp = table.get_item(Key={'user_id': 'user_admin'})
    if 'Item' in resp:
        user = resp['Item']
        print(f"  [OK] user_admin encontrado")
        print(f"      Role: {user.get('role', 'N/A')}")
        print(f"      Senha: {user.get('password', 'N/A')[:20]}...")
        print(f"      Avatar: {'Sim' if user.get('avatar') else 'Nao'}")
    else:
        print(f"  [ERRO] user_admin NAO encontrado!")
        exit(1)
except Exception as e:
    print(f"  [ERRO] {e}")
    exit(1)

# 2. Verificar se admin_sistema já existe
print("\n[2] Verificando admin_sistema...")
try:
    resp = table.get_item(Key={'user_id': 'admin_sistema'})
    if 'Item' in resp:
        print(f"  [AVISO] admin_sistema JA EXISTE!")
        print(f"          Precisa deletar antes de migrar")
        resp = input("  Deletar admin_sistema agora? (s/n): ")
        if resp.lower() == 's':
            table.delete_item(Key={'user_id': 'admin_sistema'})
            print(f"  [OK] admin_sistema deletado")
        else:
            print(f"  [ERRO] Migracao cancelada")
            exit(1)
    else:
        print(f"  [OK] admin_sistema nao existe (pode criar)")
except Exception as e:
    print(f"  [ERRO] {e}")

# 3. Verificar se sergio_sena já existe
print("\n[3] Verificando sergio_sena...")
try:
    resp = table.get_item(Key={'user_id': 'sergio_sena'})
    if 'Item' in resp:
        print(f"  [AVISO] sergio_sena JA EXISTE!")
        print(f"          Precisa deletar antes de migrar")
        resp = input("  Deletar sergio_sena agora? (s/n): ")
        if resp.lower() == 's':
            table.delete_item(Key={'user_id': 'sergio_sena'})
            print(f"  [OK] sergio_sena deletado")
        else:
            print(f"  [ERRO] Migracao cancelada")
            exit(1)
    else:
        print(f"  [OK] sergio_sena nao existe (pode criar)")
except Exception as e:
    print(f"  [ERRO] {e}")

# 4. Verificar arquivos S3
print("\n[4] Verificando arquivos S3...")
try:
    prefix = 'users/user_admin/'
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    
    total_files = 0
    total_size = 0
    large_files = []
    
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                total_files += 1
                total_size += obj['Size']
                
                # Arquivos > 5GB
                if obj['Size'] > 5 * 1024 * 1024 * 1024:
                    large_files.append({
                        'key': obj['Key'],
                        'size': obj['Size'] / (1024**3)
                    })
    
    print(f"  [OK] Total de arquivos: {total_files}")
    print(f"      Tamanho total: {total_size / (1024**3):.2f} GB")
    
    if large_files:
        print(f"      Arquivos grandes (>5GB): {len(large_files)}")
        for f in large_files[:3]:
            print(f"        - {f['key'].split('/')[-1][:40]}... ({f['size']:.2f} GB)")
        if len(large_files) > 3:
            print(f"        ... e mais {len(large_files) - 3} arquivos")
    
    # Estimar tempo
    avg_time_per_file = 0.5  # segundos
    estimated_time = (total_files * avg_time_per_file) / 60
    print(f"      Tempo estimado: {estimated_time:.1f} minutos")
    
except Exception as e:
    print(f"  [ERRO] {e}")
    exit(1)

# 5. Verificar se pasta sergio_sena já existe no S3
print("\n[5] Verificando pasta sergio_sena no S3...")
try:
    prefix = 'users/sergio_sena/'
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1)
    
    if 'Contents' in resp:
        print(f"  [AVISO] Pasta sergio_sena JA EXISTE no S3!")
        print(f"          Arquivos serao sobrescritos")
        resp = input("  Continuar mesmo assim? (s/n): ")
        if resp.lower() != 's':
            print(f"  [ERRO] Migracao cancelada")
            exit(1)
    else:
        print(f"  [OK] Pasta sergio_sena nao existe (pode criar)")
except Exception as e:
    print(f"  [ERRO] {e}")

# Resumo final
print("\n" + "="*60)
print("  [RESUMO] VERIFICACOES CONCLUIDAS")
print("="*60)
print(f"  [OK] user_admin: Pronto para migrar")
print(f"  [OK] admin_sistema: Pode ser criado")
print(f"  [OK] sergio_sena: Pode ser criado")
print(f"  [OK] S3: {total_files} arquivos prontos para mover")
print(f"  [OK] Tempo estimado: {estimated_time:.1f} minutos")
print("\n  Tudo pronto para migracao!")
print("="*60)

resp = input("\n  Executar migracao agora? (s/n): ")
if resp.lower() == 's':
    print("\n  Executando: python migrate_admin_to_sergio.py")
    os.system("python migrate_admin_to_sergio.py")
else:
    print("\n  Migracao cancelada pelo usuario")
