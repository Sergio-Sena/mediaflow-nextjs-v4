#!/usr/bin/env python3
import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', region_name='us-east-1')

# Criar ZIP
zip_path = '../aws-setup/lambda-functions/files-handler/files-handler-folders.zip'
os.chdir('../aws-setup/lambda-functions/files-handler')

with zipfile.ZipFile('files-handler-folders.zip', 'w') as zipf:
    zipf.write('lambda_function.py')

# Deploy
with open('files-handler-folders.zip', 'rb') as f:
    lambda_client.update_function_code(
        FunctionName='mediaflow-files-handler',
        ZipFile=f.read()
    )

print("Lambda files-handler atualizada com paginacao completa!")
