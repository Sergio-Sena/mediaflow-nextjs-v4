#!/usr/bin/env python3
import boto3
import json

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

cors_config = {
    'CORSRules': [
        {
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
            'AllowedOrigins': ['https://midiaflow.sstechnologies-cloud.com', 'https://*.midiaflow.sstechnologies-cloud.com'],
            'ExposeHeaders': ['ETag', 'x-amz-version-id'],
            'MaxAgeSeconds': 3000
        }
    ]
}

try:
    s3.put_bucket_cors(Bucket=bucket, CORSConfiguration=cors_config)
    print(f"CORS configurado com sucesso no bucket {bucket}")
    
    # Verificar
    result = s3.get_bucket_cors(Bucket=bucket)
    print(f"\nConfiguracao atual:\n{json.dumps(result['CORSRules'], indent=2)}")
except Exception as e:
    print(f"Erro: {str(e)}")
