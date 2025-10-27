#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/users/'

print("Conteudo de /users/user_admin/users/:")
print("=" * 60)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            key = obj['Key']
            size_mb = obj['Size'] / (1024**2)
            print(f"{key} - {size_mb:.2f} MB")
