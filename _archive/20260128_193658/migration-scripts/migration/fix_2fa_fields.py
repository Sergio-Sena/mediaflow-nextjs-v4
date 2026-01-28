#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adicionar campos necessários para 2FA"""

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
print("  [CORRECAO] Adicionar campos 2FA")
print("="*60)

# Buscar user_admin para pegar totp_secret
print("\n[1/3] Buscando totp_secret do user_admin...")
resp = table.get_item(Key={'user_id': 'user_admin'})
user_admin = resp['Item']
totp_secret = user_admin.get('totp_secret', 'JBSWY3DPEHPK3PXP')
print(f"TOTP Secret: {totp_secret}")

# Atualizar admin_sistema
print("\n[2/3] Atualizando admin_sistema...")
table.update_item(
    Key={'user_id': 'admin_sistema'},
    UpdateExpression='SET totp_secret = :totp, #n = :name',
    ExpressionAttributeNames={'#n': 'name'},
    ExpressionAttributeValues={
        ':totp': totp_secret,
        ':name': 'Administrador'
    }
)
print("[OK] admin_sistema.totp_secret = " + totp_secret)
print("[OK] admin_sistema.name = Administrador")

# Atualizar sergio_sena
print("\n[3/3] Atualizando sergio_sena...")
table.update_item(
    Key={'user_id': 'sergio_sena'},
    UpdateExpression='SET totp_secret = :totp, #n = :name',
    ExpressionAttributeNames={'#n': 'name'},
    ExpressionAttributeValues={
        ':totp': totp_secret,  # Mesmo secret (mesmo Google Authenticator)
        ':name': 'Sergio Sena'
    }
)
print("[OK] sergio_sena.totp_secret = " + totp_secret)
print("[OK] sergio_sena.name = Sergio Sena")

print("\n" + "="*60)
print("  [SUCESSO] Campos 2FA adicionados!")
print("="*60)

print("\nAmbos usam o MESMO Google Authenticator!")
print("Teste login novamente.")
