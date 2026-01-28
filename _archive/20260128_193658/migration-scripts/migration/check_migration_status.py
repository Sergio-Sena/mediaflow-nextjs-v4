#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificar status da migração"""

import boto3
import os
import sys
from dotenv import load_dotenv

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
print("  [STATUS] VERIFICACAO POS-MIGRACAO")
print("="*60)

# Verificar DynamoDB
print("\n[DYNAMODB]")
for user_id in ['user_admin', 'admin_sistema', 'sergio_sena']:
    try:
        resp = table.get_item(Key={'user_id': user_id})
        if 'Item' in resp:
            user = resp['Item']
            print(f"  [OK] {user_id}")
            print(f"       Role: {user.get('role', 'N/A')}")
            print(f"       Avatar: {'Sim' if user.get('avatar') else 'Nao'}")
        else:
            print(f"  [--] {user_id}: Nao existe")
    except Exception as e:
        print(f"  [ERRO] {user_id}: {e}")

# Verificar S3
print("\n[S3]")
for prefix in ['users/user_admin/', 'users/sergio_sena/', 'users/admin_sistema/']:
    try:
        resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1000)
        count = len(resp.get('Contents', []))
        print(f"  {prefix}: {count} arquivos")
    except Exception as e:
        print(f"  {prefix}: Erro - {e}")

print("\n" + "="*60)
print("  Verificacao concluida!")
print("="*60)
