#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teste S3"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

s3 = boto3.client(
    's3',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

print("Listando buckets S3:")
try:
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f"  - {bucket['Name']}")
except Exception as e:
    print(f"Erro: {e}")
