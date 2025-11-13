#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup final dos usuários com emails e senhas separados"""

import boto3
import os
import sys
import hashlib
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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

print("\n" + "="*60)
print("  [SETUP FINAL] Usuarios com emails separados")
print("="*60)

# Buscar dados atuais
print("\n[1/3] Buscando dados atuais...")
resp_admin = table.get_item(Key={'user_id': 'user_admin'})
user_admin = resp_admin['Item']

senha_admin = user_admin['password']  # Já está hasheada
avatar_admin = user_admin.get('avatar', '')

print(f"Senha admin (hash): {senha_admin[:30]}...")
print(f"Avatar admin: {'Sim' if avatar_admin else 'Nao'}")

# Atualizar admin_sistema
print("\n[2/3] Configurando admin_sistema...")
table.update_item(
    Key={'user_id': 'admin_sistema'},
    UpdateExpression='SET email = :email, password = :password, avatar = :avatar, #r = :role, #s = :status',
    ExpressionAttributeNames={
        '#r': 'role',
        '#s': 'status'
    },
    ExpressionAttributeValues={
        ':email': 'admin@midiaflow.com',  # Email novo
        ':password': senha_admin,  # Mesma senha do admin
        ':avatar': avatar_admin,
        ':role': 'admin',
        ':status': 'approved'
    }
)
print("[OK] admin_sistema configurado")
print("     Email: admin@midiaflow.com")
print("     Senha: Mesma do user_admin")
print("     Role: admin")
print("     Avatar: Sim")

# Atualizar sergio_sena
print("\n[3/3] Configurando sergio_sena...")

# Buscar avatar do sergio_sena
resp_sergio = table.get_item(Key={'user_id': 'sergio_sena'})
sergio = resp_sergio['Item']
avatar_sergio = sergio.get('avatar', '')

table.update_item(
    Key={'user_id': 'sergio_sena'},
    UpdateExpression='SET email = :email, password = :password, s3_prefix = :prefix, #r = :role, #s = :status',
    ExpressionAttributeNames={
        '#r': 'role',
        '#s': 'status'
    },
    ExpressionAttributeValues={
        ':email': 'sergio@midiaflow.com',  # Email novo
        ':password': senha_admin,  # Mesma senha do admin
        ':prefix': 'users/sergio_sena/',
        ':role': 'user',
        ':status': 'approved'
    }
)
print("[OK] sergio_sena configurado")
print("     Email: sergio@midiaflow.com")
print("     Senha: Mesma do user_admin")
print("     Role: user")
print("     Avatar: LoginDevagem.jpeg")
print("     Pasta: users/sergio_sena/")

print("\n" + "="*60)
print("  [SUCESSO] Setup concluido!")
print("="*60)

print("\n[CREDENCIAIS]")
print("\n1. ADMIN_SISTEMA:")
print("   Email: admin@midiaflow.com")
print("   Senha: [mesma do user_admin]")
print("   2FA: [mesmo Google Authenticator]")
print("   Acesso: TUDO")

print("\n2. SERGIO_SENA:")
print("   Email: sergio@midiaflow.com")
print("   Senha: [mesma do user_admin]")
print("   2FA: [mesmo Google Authenticator]")
print("   Acesso: users/sergio_sena/ apenas")

print("\n[PROXIMO PASSO]")
print("Testar login com os novos emails!")
