#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migração automática sem aprovações"""

import boto3
import os
import sys
import json
from datetime import datetime
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
print("  MIGRACAO AUTOMATICA")
print("="*60)

# ETAPA 1: Backup
print("\n[1/5] Backup...")
resp = table.get_item(Key={'user_id': 'user_admin'})
backup = resp['Item']
filename = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(backup, f, indent=2, default=str)
print(f"[OK] {filename}")

# ETAPA 2: Criar admin_sistema
print("\n[2/5] Criando admin_sistema...")
table.put_item(Item={
    'user_id': 'admin_sistema',
    'password': backup['password'],
    'role': 'admin',
    'avatar': backup.get('avatar', ''),
    'created_at': datetime.now().isoformat()
})
print("[OK] admin_sistema criado (role admin, sem midias)")

# ETAPA 3: Criar sergio_sena
print("\n[3/5] Criando sergio_sena...")
table.put_item(Item={
    'user_id': 'sergio_sena',
    'password': backup['password'],
    'role': 'user',
    'avatar': backup.get('avatar', ''),
    'created_at': backup.get('created_at', datetime.now().isoformat())
})
print("[OK] sergio_sena criado (role user)")

# ETAPA 4: Mover arquivos S3
print("\n[4/5] Movendo arquivos S3...")
print("Contando arquivos...")
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/')

all_files = []
for page in pages:
    if 'Contents' in page:
        all_files.extend(page['Contents'])

total = len(all_files)
print(f"Total: {total} arquivos\n")

for i, obj in enumerate(all_files, 1):
    old_key = obj['Key']
    new_key = old_key.replace('users/user_admin/', 'users/sergio_sena/')
    size = obj['Size']
    
    if size < 5 * 1024**3:
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': old_key},
            Key=new_key
        )
    else:
        mpu = s3.create_multipart_upload(Bucket=bucket, Key=new_key)
        upload_id = mpu['UploadId']
        
        try:
            parts = []
            part_size = 100 * 1024**2
            part_num = 1
            
            for corporativot in range(0, size, part_size):
                end = min(corporativot + part_size - 1, size - 1)
                part = s3.upload_part_copy(
                    Bucket=bucket,
                    Key=new_key,
                    CopySource={'Bucket': bucket, 'Key': old_key},
                    CopySourceRange=f'bytes={corporativot}-{end}',
                    PartNumber=part_num,
                    UploadId=upload_id
                )
                parts.append({
                    'ETag': part['CopyPartResult']['ETag'],
                    'PartNumber': part_num
                })
                part_num += 1
            
            s3.complete_multipart_upload(
                Bucket=bucket,
                Key=new_key,
                UploadId=upload_id,
                MultipartUpload={'Parts': parts}
            )
        except:
            s3.abort_multipart_upload(Bucket=bucket, Key=new_key, UploadId=upload_id)
            raise
    
    percent = (i / total) * 100
    bar_length = 40
    filled = int(bar_length * i / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\r[{bar}] {percent:.1f}% ({i}/{total})", end='', flush=True)

print(f"\n[OK] {total} arquivos movidos")

# ETAPA 5: Deletar user_admin antigo
print("\n[5/5] Deletando user_admin antigo...")
table.delete_item(Key={'user_id': 'user_admin'})
print("[OK] user_admin deletado do DynamoDB")

print("\n" + "="*60)
print("  MIGRACAO CONCLUIDA!")
print("="*60)
print("\n[OK] admin_sistema: role admin, sem midias")
print("[OK] sergio_sena: role user, com todas as midias")
print("[OK] user_admin: deletado")
print(f"\n[BACKUP] {filename}")
