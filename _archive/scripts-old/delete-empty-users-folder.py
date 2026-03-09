#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/users/'

print("Deletando pasta vazia /users/user_admin/users/...")
print("=" * 60)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

deleted = 0
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            key = obj['Key']
            print(f"Deletando: {key}")
            s3.delete_object(Bucket=bucket, Key=key)
            deleted += 1

print(f"\nObjetos deletados: {deleted}")
print("Pasta removida!")
