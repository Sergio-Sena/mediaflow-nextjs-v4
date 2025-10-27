#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
prefix = 'users/user_admin/Star/'

print("Pastas que comecam com 404 em Star/:")
print("=" * 50)

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/')

folders_404 = []
for page in pages:
    if 'CommonPrefixes' in page:
        for prefix_obj in page['CommonPrefixes']:
            folder = prefix_obj['Prefix'].replace(prefix, '').rstrip('/')
            if folder.startswith('404'):
                folders_404.append(folder)
                
                # Contar arquivos
                folder_prefix = f"{prefix}{folder}/"
                count = 0
                size = 0
                for obj_page in paginator.paginate(Bucket=bucket, Prefix=folder_prefix):
                    if 'Contents' in obj_page:
                        for obj in obj_page['Contents']:
                            if not obj['Key'].endswith('/'):
                                count += 1
                                size += obj['Size']
                
                print(f"\n{folder}/")
                print(f"  Arquivos: {count}")
                print(f"  Tamanho: {size / (1024**3):.2f} GB")

print(f"\n\nTotal de pastas 404: {len(folders_404)}")
if len(folders_404) == 2:
    print(f"\nUnificar: {folders_404[0]}/ + {folders_404[1]}/ -> 404HotFound/")
