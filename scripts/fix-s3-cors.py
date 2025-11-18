import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
BUCKET = 'mediaflow-uploads-969430605054'

cors_config = {
    'CORSRules': [{
        'AllowedHeaders': ['*'],
        'AllowedMethods': ['GET', 'HEAD'],
        'AllowedOrigins': ['*'],
        'ExposeHeaders': ['ETag', 'Content-Length', 'Content-Type'],
        'MaxAgeSeconds': 3600
    }]
}

s3.put_bucket_cors(Bucket=BUCKET, CORSConfiguration=cors_config)
print(f"[OK] CORS configurado no bucket {BUCKET}")
