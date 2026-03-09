#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/'

print("Pastas dentro de /users/user_admin/:")
print("=" * 60)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/')

folders = []
for page in pages:
    if 'CommonPrefixes' in page:
        for p in page['CommonPrefixes']:
            folder = p['Prefix'].replace(prefix, '').rstrip('/')
            folders.append(folder)

for folder in sorted(folders):
    # Contar arquivos
    count = 0
    size = 0
    folder_prefix = f"{prefix}{folder}/"
    for obj_page in paginator.paginate(Bucket=bucket, Prefix=folder_prefix):
        if 'Contents' in obj_page:
            for obj in obj_page['Contents']:
                if not obj['Key'].endswith('/'):
                    count += 1
                    size += obj['Size']
    
    print(f"{folder}/ - {count} arquivos, {size / (1024**3):.2f} GB")

print(f"\nTotal de pastas: {len(folders)}")
