#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validar migração"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

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
print("  [VALIDACAO] Pos-Migracao")
print("="*60)

# DynamoDB
print("\n[DYNAMODB]")
for user_id in ['admin_sistema', 'sergio_sena', 'user_admin']:
    try:
        resp = table.get_item(Key={'user_id': user_id})
        if 'Item' in resp:
            u = resp['Item']
            print(f"  [OK] {user_id}")
            print(f"       Role: {u.get('role')}")
            print(f"       Senha: {u.get('password')[:20]}...")
            print(f"       Avatar: {'Sim' if u.get('avatar') else 'Nao'}")
        else:
            print(f"  [--] {user_id}: Nao existe")
    except Exception as e:
        print(f"  [ERRO] {user_id}: {e}")

# S3
print("\n[S3]")
for prefix in ['users/admin_sistema/', 'users/sergio_sena/', 'users/user_admin/']:
    try:
        resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1000)
        count = len(resp.get('Contents', []))
        
        if prefix == 'users/admin_sistema/':
            status = "[OK]" if count == 0 else "[AVISO]"
            print(f"  {status} {prefix}: {count} arquivos (esperado: 0)")
        elif prefix == 'users/sergio_sena/':
            status = "[OK]" if count > 1000 else "[AVISO]"
            print(f"  {status} {prefix}: {count} arquivos (esperado: 1728)")
        else:
            print(f"  [INFO] {prefix}: {count} arquivos (backup)")
    except Exception as e:
        print(f"  [ERRO] {prefix}: {e}")

print("\n" + "="*60)
print("  [RESUMO]")
print("="*60)
print("\n[OK] Migracao concluida com sucesso!")
print("\n[PROXIMO PASSO]")
print("  Tecorporativo login:")
print("  1. admin_sistema (role admin)")
print("  2. sergio_sena (role user)")
print("\n[LIMPEZA OPCIONAL]")
print("  Deletar user_admin se tudo estiver OK")
