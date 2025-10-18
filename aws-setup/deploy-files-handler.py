#!/usr/bin/env python3

import boto3
import zipfile
import os

# Configurações
REGION = 'us-east-1'
FUNCTION_NAME = 'mediaflow-files-handler'

# Cliente Lambda
lambda_client = boto3.client('lambda', region_name=REGION)

def create_zip():
    """Criar ZIP da função Lambda"""
    zip_path = f'lambda-functions/files-handler/{FUNCTION_NAME}.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(f'lambda-functions/files-handler/lambda_function.py', 'lambda_function.py')
    
    return zip_path

def deploy_lambda():
    """Deploy função Lambda"""
    print(f"Deploying {FUNCTION_NAME}...")
    
    zip_path = create_zip()
    
    try:
        # Atualizar código da função
        with open(zip_path, 'rb') as zip_file:
            response = lambda_client.update_function_code(
                FunctionName=FUNCTION_NAME,
                ZipFile=zip_file.read()
            )
        
        print(f"SUCCESS: {FUNCTION_NAME} updated successfully!")
        print(f"Version: {response['Version']}")
        print(f"Last Modified: {response['LastModified']}")
        
    except Exception as e:
        print(f"ERROR deploying {FUNCTION_NAME}: {str(e)}")

if __name__ == '__main__':
    deploy_lambda()