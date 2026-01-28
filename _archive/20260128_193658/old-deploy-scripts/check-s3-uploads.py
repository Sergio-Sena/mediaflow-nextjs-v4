#!/usr/bin/env python3
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("\nArquivos no S3 (users/sergio_sena/):\n")

response = s3.list_objects_v2(
    Bucket=bucket,
    Prefix='users/sergio_sena/',
    MaxKeys=50
)

if 'Contents' in response:
    for obj in response['Contents']:
        size_mb = obj['Size'] / (1024 * 1024)
        print(f"  {obj['Key']} ({size_mb:.2f} MB)")
    print(f"\nTotal: {len(response['Contents'])} arquivos")
else:
    print("  Nenhum arquivo encontrado")
