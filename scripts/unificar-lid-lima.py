#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unifica lid-lima para lid_lima (mantém a mais antiga)
"""

import boto3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

s3 = boto3.client('s3', region_name='us-east-1',
    aws_access_key_id='AKIA6DNURDT7MO5EXHLQ',
    aws_secret_access_key='9wmyrw4365OTX+hwZ2ZZXjE+lbEUxn3INY4tu0Ir')

BUCKET = 'mediaflow-uploads-969430605054'

print("=== UNIFICANDO LID LIMA ===\n")

# Listar arquivos de lid-lima
resp = s3.list_objects_v2(Bucket=BUCKET, Prefix='users/lid-lima/')

if 'Contents' not in resp:
    print("Nenhum arquivo em lid-lima/")
    exit()

arquivos = resp['Contents']
print(f"Encontrados: {len(arquivos)} arquivos em lid-lima/\n")

# Copiar para lid_lima
for obj in arquivos:
    old_key = obj['Key']
    new_key = old_key.replace('lid-lima', 'lid_lima')
    
    print(f"Copiando: {old_key.split('/')[-1]}")
    
    try:
        # Copiar
        s3.copy_object(
            Bucket=BUCKET,
            CopySource={'Bucket': BUCKET, 'Key': old_key},
            Key=new_key
        )
        
        # Deletar original
        s3.delete_object(Bucket=BUCKET, Key=old_key)
        print("  -> OK\n")
        
    except Exception as e:
        print(f"  -> ERRO: {e}\n")

print("=== CONCLUIDO ===")
print("Todos os arquivos movidos para users/lid_lima/")
