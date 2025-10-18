#!/usr/bin/env python3

import boto3
import zipfile
import json

# Configurações
REGION = 'us-east-1'
FUNCTION_NAME = 'delete-user'
ROLE_ARN = 'arn:aws:iam::969430605054:role/lambda-execution-role'

# Clientes AWS
lambda_client = boto3.client('lambda', region_name=REGION)

def create_zip():
    """Criar ZIP da função Lambda"""
    zip_path = f'lambda-functions/delete-user/function.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(f'lambda-functions/delete-user/index.py', 'index.py')
    
    return zip_path

def create_lambda():
    """Criar função Lambda"""
    print(f"Creating {FUNCTION_NAME}...")
    
    zip_path = create_zip()
    
    try:
        with open(zip_path, 'rb') as zip_file:
            response = lambda_client.create_function(
                FunctionName=FUNCTION_NAME,
                Runtime='python3.9',
                Role=ROLE_ARN,
                Handler='index.lambda_handler',
                Code={'ZipFile': zip_file.read()},
                Description='Delete user from DynamoDB',
                Timeout=30,
                Environment={
                    'Variables': {
                        'DYNAMODB_TABLE': 'mediaflow-users'
                    }
                }
            )
        
        print(f"SUCCESS: {FUNCTION_NAME} created successfully!")
        print(f"ARN: {response['FunctionArn']}")
        
        return response['FunctionArn']
        
    except Exception as e:
        print(f"ERROR creating {FUNCTION_NAME}: {str(e)}")
        return None

if __name__ == '__main__':
    create_lambda()