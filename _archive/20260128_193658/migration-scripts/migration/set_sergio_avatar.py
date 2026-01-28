#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configurar avatar do sergio_sena"""

import boto3
import os
import sys
from dotenv import load_dotenv

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv('.env.local')

s3 = boto3.client(
    's3',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

table = dynamodb.Table('mediaflow-users')
bucket = 'mediaflow-uploads-969430605054'

print("\n" + "="*60)
print("  [AVATAR] Configurar avatar sergio_sena")
print("="*60)

# Upload imagem para S3
print("\n[1/2] Fazendo upload da imagem...")
local_file = 'public/LoginDevagem.jpeg'
s3_key = 'avatars/sergio_sena.jpeg'

try:
    s3.upload_file(
        local_file,
        bucket,
        s3_key,
        ExtraArgs={'ContentType': 'image/jpeg'}
    )
    avatar_url = f'https://{bucket}.s3.amazonaws.com/{s3_key}'
    print(f"[OK] Upload concluido: {s3_key}")
    print(f"     URL: {avatar_url}")
except Exception as e:
    print(f"[ERRO] {e}")
    sys.exit(1)

# Atualizar DynamoDB
print("\n[2/2] Atualizando DynamoDB...")
table.update_item(
    Key={'user_id': 'sergio_sena'},
    UpdateExpression='SET avatar = :avatar',
    ExpressionAttributeValues={
        ':avatar': avatar_url
    }
)
print("[OK] Avatar atualizado no DynamoDB")

print("\n" + "="*60)
print("  [SUCESSO] Avatar configurado!")
print("="*60)
print(f"\nsergio_sena agora tem avatar: {avatar_url}")
