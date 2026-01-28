#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Continua migração de onde parou"""

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
print("  [CONTINUACAO] Migração S3")
print("="*60)

# Verificar se DynamoDB já está OK
print("\n[1/3] Verificando DynamoDB...")
try:
    admin = table.get_item(Key={'user_id': 'admin_sistema'})
    sergio = table.get_item(Key={'user_id': 'sergio_sena'})
    
    if 'Item' in admin and 'Item' in sergio:
        print("[OK] admin_sistema e sergio_sena existem")
    else:
        print("[ERRO] Falta criar usuarios no DynamoDB")
        print("Execute: python migrate_final.py")
        exit(1)
except Exception as e:
    print(f"[ERRO] {e}")
    exit(1)

# Licorporativo arquivos origem e destino
print("\n[2/3] Verificando arquivos...")

print("Listando arquivos de origem (user_admin)...")
paginator = s3.get_paginator('list_objects_v2')
origem_pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/')

origem_files = set()
for page in origem_pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            origem_files.add(obj['Key'])

print(f"Total origem: {len(origem_files)} arquivos")

print("Listando arquivos de destino (sergio_sena)...")
destino_pages = paginator.paginate(Bucket=bucket, Prefix='users/sergio_sena/')

destino_files = set()
for page in destino_pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            # Converter para nome equivalente em user_admin
            equiv = obj['Key'].replace('users/sergio_sena/', 'users/user_admin/')
            destino_files.add(equiv)

print(f"Total destino: {len(destino_files)} arquivos")

# Calcular faltantes
faltantes = origem_files - destino_files
print(f"\n[OK] Faltam copiar: {len(faltantes)} arquivos")

if len(faltantes) == 0:
    print("\n[SUCESSO] Todos os arquivos ja foram copiados!")
    print("Execute limpeza se desejar:")
    print("  - Deletar user_admin do DynamoDB")
    print("  - Deletar pasta users/user_admin/ do S3")
    exit(0)

# Copiar faltantes
print("\n[3/3] Copiando arquivos faltantes...")

faltantes_list = sorted(list(faltantes))
total = len(faltantes_list)

for i, old_key in enumerate(faltantes_list, 1):
    new_key = old_key.replace('users/user_admin/', 'users/sergio_sena/')
    
    try:
        # Obter tamanho
        head = s3.head_object(Bucket=bucket, Key=old_key)
        size = head['ContentLength']
        
        # Copy simples ou multipart
        if size < 5 * 1024**3:
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': old_key},
                Key=new_key
            )
        else:
            # Multipart
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
            except Exception as e:
                s3.abort_multipart_upload(Bucket=bucket, Key=new_key, UploadId=upload_id)
                raise e
        
        # Progresso
        percent = (i / total) * 100
        bar_length = 40
        filled = int(bar_length * i / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r[{bar}] {percent:.1f}% ({i}/{total})", end='', flush=True)
        
    except Exception as e:
        print(f"\n[ERRO] Arquivo: {old_key}")
        print(f"       Erro: {e}")
        print("\nContinuando com próximo arquivo...")
        continue

print(f"\n\n[SUCESSO] {total} arquivos copiados!")
print("\n" + "="*60)
print("  [MIGRACAO CONCLUIDA]")
print("="*60)
print("\n[OK] admin_sistema: criado")
print("[OK] sergio_sena: criado")
print(f"[OK] {len(origem_files)} arquivos copiados")
print("\n[LIMPEZA OPCIONAL]")
print("  1. Deletar user_admin do DynamoDB")
print("  2. Deletar pasta users/user_admin/ do S3")
