#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contar TODOS os arquivos (sem limite)"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

s3 = boto3.client(
    's3',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

bucket = 'mediaflow-uploads-969430605054'

print("\n" + "="*60)
print("  [CONTAGEM COMPLETA] Todos os Arquivos")
print("="*60)

for prefix in ['users/sergio_sena/', 'users/user_admin/']:
    print(f"\n[{prefix}]")
    print("Contando... (pode demorar 10-20 segundos)")
    
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    
    total = 0
    for page in pages:
        if 'Contents' in page:
            total += len(page['Contents'])
    
    print(f"Total: {total} arquivos")

print("\n" + "="*60)
print("  [RESULTADO]")
print("="*60)
print("\nSe sergio_sena tem 1728 arquivos = SUCESSO TOTAL!")
