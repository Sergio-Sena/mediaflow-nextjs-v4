#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrigir migração - adicionar emails e ajustar campos"""

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
print("  [CORRECAO] Ajustar admin_sistema e sergio_sena")
print("="*60)

# Buscar user_admin para pegar dados
print("\n[1/3] Buscando dados do user_admin...")
resp = table.get_item(Key={'user_id': 'user_admin'})
user_admin = resp['Item']

email_admin = user_admin.get('email', 'sergiosenaadmin@sstech')
avatar_admin = user_admin.get('avatar', '')

print(f"Email: {email_admin}")
print(f"Avatar: {'Sim' if avatar_admin else 'Nao'}")

# Atualizar admin_sistema
print("\n[2/3] Atualizando admin_sistema...")
table.update_item(
    Key={'user_id': 'admin_sistema'},
    UpdateExpression='SET email = :email, avatar = :avatar',
    ExpressionAttributeValues={
        ':email': email_admin,
        ':avatar': avatar_admin
    }
)
print("[OK] admin_sistema atualizado")
print(f"     Email: {email_admin}")
print(f"     Avatar: Sim")

# Atualizar sergio_sena
print("\n[3/3] Atualizando sergio_sena...")
table.update_item(
    Key={'user_id': 'sergio_sena'},
    UpdateExpression='SET email = :email',
    ExpressionAttributeValues={
        ':email': email_admin  # Mesmo email por enquanto
    }
)
print("[OK] sergio_sena atualizado")
print(f"     Email: {email_admin}")

print("\n" + "="*60)
print("  [SUCESSO] Correções aplicadas!")
print("="*60)

print("\n[PROXIMO PASSO]")
print("Testar login novamente:")
print("  1. admin_sistema (email: sergiosenaadmin@sstech)")
print("  2. sergio_sena (email: sergiosenaadmin@sstech)")
print("\n[NOTA]")
print("Ambos usam mesmo email temporariamente.")
print("Você pode criar email diferente para sergio_sena depois.")
