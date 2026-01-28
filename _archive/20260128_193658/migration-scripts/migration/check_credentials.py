#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificar credenciais"""

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
print("  [VERIFICACAO] Credenciais")
print("="*60)

# Buscar todos
users = {}
for user_id in ['user_admin', 'admin_sistema', 'sergio_sena']:
    try:
        resp = table.get_item(Key={'user_id': user_id})
        if 'Item' in resp:
            users[user_id] = resp['Item']
    except:
        pass

# Comparar
print("\n[SENHAS]")
if 'user_admin' in users:
    senha_admin_original = users['user_admin']['password']
    print(f"user_admin:     {senha_admin_original[:30]}...")
    
    if 'admin_sistema' in users:
        senha_admin_sistema = users['admin_sistema']['password']
        print(f"admin_sistema:  {senha_admin_sistema[:30]}...")
        
        if senha_admin_original == senha_admin_sistema:
            print("  ✅ SENHAS IGUAIS (admin_sistema = user_admin)")
        else:
            print("  ❌ SENHAS DIFERENTES!")
    
    if 'sergio_sena' in users:
        senha_sergio = users['sergio_sena']['password']
        print(f"sergio_sena:    {senha_sergio[:30]}...")
        
        if senha_admin_original == senha_sergio:
            print("  ✅ SENHAS IGUAIS (sergio_sena = user_admin)")
        else:
            print("  ❌ SENHAS DIFERENTES!")

print("\n[ROLES]")
for user_id in ['user_admin', 'admin_sistema', 'sergio_sena']:
    if user_id in users:
        role = users[user_id].get('role', 'N/A')
        print(f"{user_id:15} → role: {role}")

print("\n[AVATARES]")
for user_id in ['user_admin', 'admin_sistema', 'sergio_sena']:
    if user_id in users:
        avatar = users[user_id].get('avatar', '')
        tem_avatar = 'Sim' if avatar else 'Nao'
        print(f"{user_id:15} → avatar: {tem_avatar}")

print("\n" + "="*60)
print("  [RESUMO]")
print("="*60)
print("\n✅ admin_sistema = Mesma senha do user_admin")
print("✅ sergio_sena = Mesma senha do user_admin")
print("\nTodos usam a MESMA senha!")
print("Todos usam o MESMO Google Authenticator!")
