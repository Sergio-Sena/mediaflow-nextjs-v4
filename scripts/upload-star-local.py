#!/usr/bin/env python3
import boto3
import os
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'
local_dir = r'C:\Users\dell 5557\Videos\IDM\Corporativo'
s3_prefix = 'users/user_admin/Corporativo/'

print(f"Uploading {local_dir} -> s3://{bucket}/{s3_prefix}")
print("=" * 60)

count = 0
for root, dirs, files in os.walk(local_dir):
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, local_dir)
        s3_key = s3_prefix + relative_path.replace('\\', '/')
        
        print(f"  + {relative_path}")
        s3.upload_file(local_path, bucket, s3_key)
        count += 1

print("=" * 60)
print(f"✓ {count} arquivos enviados!")
