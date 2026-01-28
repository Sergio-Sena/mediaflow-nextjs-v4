import boto3
import os
from pathlib import Path
import mimetypes

s3 = boto3.client('s3')
cloudfront = boto3.client('cloudfront')

BUCKET = 'mediaflow-frontend-969430605054'
DISTRIBUTION_ID = 'E2HZKZ9ZJK18IU'  # midiaflow.sstechnologies-cloud.com
BUILD_DIR = '.next/static'

print("Uploading static files...")

uploaded = 0
for file_path in Path(BUILD_DIR).rglob('*'):
    if file_path.is_file():
        key = str(file_path.relative_to('.next')).replace('\\', '/')
        content_type = mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream'
        
        s3.upload_file(
            str(file_path),
            BUCKET,
            f'_next/{key}',
            ExtraArgs={'ContentType': content_type, 'CacheControl': 'public,max-age=31536000,immutable'}
        )
        uploaded += 1
        if uploaded % 50 == 0:
            print(f"  {uploaded} files...")

print(f"Uploaded {uploaded} files")
print("Invalidating CloudFront cache...")

try:
    cloudfront.create_invalidation(
        DistributionId=DISTRIBUTION_ID,
        InvalidationBatch={
            'Paths': {'Quantity': 1, 'Items': ['/*']},
            'CallerReference': str(os.urandom(16).hex())
        }
    )
    print("Cache invalidated!")
except:
    print("Note: Update DISTRIBUTION_ID in script")
