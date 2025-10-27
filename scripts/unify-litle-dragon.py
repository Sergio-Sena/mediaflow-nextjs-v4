#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("Unificando litle_dragon -> litle dragon")
print("=" * 60)

# Listar arquivos em litle_dragon
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix='users/user_admin/Star/litle_dragon/')

moved = 0
for page in pages:
    for obj in page.get('Contents', []):
        old_key = obj['Key']
        new_key = old_key.replace('litle_dragon', 'litle dragon')
        
        print(f"Movendo: {old_key.split('/')[-1]}")
        
        # Copiar
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': old_key},
            Key=new_key
        )
        
        # Deletar original
        s3.delete_object(Bucket=bucket, Key=old_key)
        moved += 1

print(f"\n✓ {moved} arquivo(s) movido(s)")
