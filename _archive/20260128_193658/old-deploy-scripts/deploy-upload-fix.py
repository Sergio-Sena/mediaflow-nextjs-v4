#!/usr/bin/env python3
import boto3
import zipfile
import os

lambda_client = boto3.client('lambda', region_name='us-east-1')

# Lambdas a fazer deploy
lambdas = [
    {
        'name': 'mediaflow-upload-handler',
        'path': 'aws-setup/lambda-functions/upload-handler'
    },
    {
        'name': 'mediaflow-multipart-handler',
        'path': 'aws-setup/lambda-functions/multipart-handler'
    }
]

for lambda_info in lambdas:
    lambda_name = lambda_info['name']
    lambda_path = lambda_info['path']
    
    print(f"\nDeployando {lambda_name}...")
    
    # Criar ZIP
    zip_path = f"{lambda_path}/lambda_function.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(f"{lambda_path}/lambda_function.py", "lambda_function.py")
        
        # Incluir lib se existir
        lib_path = f"{lambda_path}/../lib"
        if os.path.exists(lib_path):
            for file in os.listdir(lib_path):
                if file.endswith('.py'):
                    zipf.write(f"{lib_path}/{file}", f"lib/{file}")
    
    # Upload para Lambda
    with open(zip_path, 'rb') as f:
        response = lambda_client.update_function_code(
            FunctionName=lambda_name,
            ZipFile=f.read()
        )
    
    print(f"  Status: {response['State']}")
    print(f"  LastModified: {response['LastModified']}")
    print(f"  CodeSha256: {response['CodeSha256'][:16]}...")

print("\nDeploy completed successfully!")
