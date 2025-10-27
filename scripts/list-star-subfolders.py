#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/Star/'

print(f"Listando subpastas em {prefix}")
print("=" * 60)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/')

subfolders = []
for page in pages:
    if 'CommonPrefixes' in page:
        for p in page['CommonPrefixes']:
            folder = p['Prefix'].replace(prefix, '').rstrip('/')
            subfolders.append(folder)

for folder in sorted(subfolders):
    print(f"  {folder}/")

print(f"\nTotal: {len(subfolders)} subpastas")
