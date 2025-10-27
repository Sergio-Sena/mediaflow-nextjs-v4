#!/usr/bin/env python3
import boto3
import os
import json
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')
cloudfront = boto3.client('cloudfront', region_name='us-east-1')

BUCKET = 'mediaflow-frontend-969430605054'
DISTRIBUTION_ID = 'E2HZKZ9ZJK18IU'
OUT_DIR = '../out'

print("=" * 60)
print("Deploy Mídiaflow v4.7.4 - Paginação Frontend")
print("=" * 60)

# Upload out/ para S3
print("\n1. Uploading files to S3...")
for root, dirs, files in os.walk(OUT_DIR):
    for file in files:
        local_path = os.path.join(root, file)
        s3_key = os.path.relpath(local_path, OUT_DIR).replace('\\', '/')
        
        content_type = 'text/html'
        if file.endswith('.js'):
            content_type = 'application/javascript'
        elif file.endswith('.css'):
            content_type = 'text/css'
        elif file.endswith('.json'):
            content_type = 'application/json'
        elif file.endswith('.png'):
            content_type = 'image/png'
        elif file.endswith('.jpg') or file.endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif file.endswith('.svg'):
            content_type = 'image/svg+xml'
        
        s3.upload_file(
            local_path,
            BUCKET,
            s3_key,
            ExtraArgs={'ContentType': content_type}
        )
        print(f"  + {s3_key}")

print("\n2. Invalidating CloudFront cache...")
cloudfront.create_invalidation(
    DistributionId=DISTRIBUTION_ID,
    InvalidationBatch={
        'Paths': {'Quantity': 1, 'Items': ['/*']},
        'CallerReference': str(hash('v4.7.4'))
    }
)

print("\n" + "=" * 60)
print("✅ Deploy v4.7.4 concluído!")
print("=" * 60)
print("\n🌐 URL: https://midiaflow.sstechnologies-cloud.com")
print("\n📊 Mudanças:")
print("  - Paginação frontend (50 itens/página)")
print("  - Performance 10x mais rápida")
print("  - Navegação hierárquica completa")
print("  - Autoplay ao navegar")
