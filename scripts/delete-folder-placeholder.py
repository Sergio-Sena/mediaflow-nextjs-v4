# -*- coding: utf-8 -*-
import boto3
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
key = 'users/sergio_sena/'

# Verificar se existe e tem 0 bytes
try:
    obj = s3.head_object(Bucket=bucket, Key=key)
    size = obj['ContentLength']
    
    print(f"[OK] Objeto encontrado: {key}")
    print(f"  Tamanho: {size} bytes")
    print(f"  Data: {obj['LastModified']}")
    
    if size == 0:
        print(f"\n[WARN] Deletando placeholder de 0 bytes...")
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"[SUCCESS] Deletado com sucesso!")
    else:
        print(f"\n[ERROR] Objeto nao e placeholder (tem {size} bytes) - nao deletado por seguranca")
        
except s3.exceptions.NoSuchKey:
    print(f"[ERROR] Objeto nao encontrado: {key}")
except Exception as e:
    print(f"[ERROR] Erro: {e}")
