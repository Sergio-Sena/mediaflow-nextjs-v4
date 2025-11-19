#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
source_prefix = 'users/user_admin/Corporativo/404 Hot Found/'
dest_prefix = 'users/user_admin/Corporativo/404HotFound/'

print("Unificando pastas 404...")
print("=" * 50)
print(f"De: {source_prefix}")
print(f"Para: {dest_prefix}")
print()

# Licorporativo arquivos da pasta origem
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=source_prefix)

moved = 0
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            source_key = obj['Key']
            if source_key.endswith('/'):
                continue
            
            # Nome do arquivo
            filename = source_key.replace(source_prefix, '')
            dest_key = f"{dest_prefix}{filename}"
            
            print(f"Movendo: {filename}")
            
            # Copiar
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': source_key},
                Key=dest_key,
                StorageClass='INTELLIGENT_TIERING'
            )
            
            # Deletar original
            s3.delete_object(Bucket=bucket, Key=source_key)
            
            moved += 1
            print(f"  OK")

print(f"\nArquivos movidos: {moved}")
print("Unificacao concluida!")
