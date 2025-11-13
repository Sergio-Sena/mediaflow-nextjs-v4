#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adicionar s3_prefix para sergio_sena"""

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

table = dynamodb.Table('mediaflow-users')

print("\n" + "="*60)
print("  [CORRECAO] Adicionar s3_prefix")
print("="*60)

# Atualizar sergio_sena
print("\n[1/2] Atualizando sergio_sena...")
table.update_item(
    Key={'user_id': 'sergio_sena'},
    UpdateExpression='SET s3_prefix = :prefix',
    ExpressionAttributeValues={
        ':prefix': 'users/sergio_sena/'
    }
)
print("[OK] sergio_sena.s3_prefix = 'users/sergio_sena/'")

# Verificar admin_sistema (não precisa de s3_prefix pois é admin)
print("\n[2/2] Verificando admin_sistema...")
resp = table.get_item(Key={'user_id': 'admin_sistema'})
if 'Item' in resp:
    user = resp['Item']
    if 's3_prefix' in user:
        print(f"[INFO] admin_sistema.s3_prefix = '{user['s3_prefix']}'")
        print("[INFO] Admin não precisa de s3_prefix (vê tudo)")
    else:
        print("[OK] admin_sistema sem s3_prefix (correto para admin)")

print("\n" + "="*60)
print("  [SUCESSO] s3_prefix configurado!")
print("="*60)

print("\n[RESULTADO]")
print("  sergio_sena agora verá apenas: users/sergio_sena/")
print("  admin_sistema verá: Tudo (sem filtro)")

print("\n[PROXIMO PASSO]")
print("  1. Fazer deploy da Lambda files-handler")
print("  2. Testar login novamente")
