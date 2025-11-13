#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teste de conexão DynamoDB"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_REGION', 'us-east-1')

print(f"Region: {REGION}")
print(f"Access Key: {AWS_ACCESS_KEY[:10]}...")

# Listar tabelas
dynamodb = boto3.client(
    'dynamodb',
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

print("\nListando tabelas DynamoDB:")
try:
    response = dynamodb.list_tables()
    print(f"Tabelas encontradas: {response['TableNames']}")
except Exception as e:
    print(f"Erro: {e}")

# Tentar acessar a tabela
print("\nTentando acessar drive-online-users:")
try:
    dynamodb_resource = boto3.resource(
        'dynamodb',
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    table = dynamodb_resource.Table('drive-online-users')
    
    # Tentar buscar user_admin
    response = table.get_item(Key={'user_id': 'user_admin'})
    if 'Item' in response:
        print(f"user_admin encontrado!")
        print(f"  user_id: {response['Item']['user_id']}")
        print(f"  role: {response['Item'].get('role', 'N/A')}")
    else:
        print("user_admin NAO encontrado")
        
except Exception as e:
    print(f"Erro: {e}")
