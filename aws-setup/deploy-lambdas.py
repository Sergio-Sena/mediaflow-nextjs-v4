#!/usr/bin/env python3
import boto3
import json
import zipfile
import os
from pathlib import Path

def create_lambda_zip(function_dir):
    """Create ZIP file for Lambda deployment"""
    zip_path = f"{function_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for file_path in Path(function_dir).rglob('*'):
            if file_path.is_file():
                zip_file.write(file_path, file_path.relative_to(function_dir))
    return zip_path

def deploy_lambda(lambda_client, function_name, zip_path, role_arn, env_vars=None):
    """Deploy or update Lambda function"""
    try:
        with open(zip_path, 'rb') as zip_file:
            zip_content = zip_file.read()
        
        # Try to update existing function
        try:
            lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            print(f"Updated: {function_name}")
        except lambda_client.exceptions.ResourceNotFoundException:
            # Create new function
            lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.11',
                Role=role_arn,
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_content},
                Environment={'Variables': env_vars or {}},
                Timeout=30
            )
            print(f"Created: {function_name}")
        
        return True
    except Exception as e:
        print(f"Error deploying {function_name}: {str(e)}")
        return False

def main():
    print("Deploying Mediaflow Lambda Functions...")
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    lambda_client = boto3.client('lambda')
    iam_client = boto3.client('iam')
    
    # Create IAM role for Lambda
    role_name = 'mediaflow-lambda-role'
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        role_response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = role_response['Role']['Arn']
        
        # Attach policies
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
        )
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AWSElementalMediaConvertFullAccess'
        )
        print(f"Created IAM role: {role_arn}")
        
    except iam_client.exceptions.EntityAlreadyExistsException:
        role_arn = f"arn:aws:iam::{config['account_id']}:role/{role_name}"
        print(f"Using existing IAM role: {role_arn}")
    
    # Deploy functions
    functions = [
        {
            'name': 'mediaflow-auth-handler',
            'dir': 'lambda-functions/auth-handler',
            'env': {}
        },
        {
            'name': 'mediaflow-files-handler', 
            'dir': 'lambda-functions/files-handler',
            'env': {
                'UPLOADS_BUCKET': config['buckets']['uploads'],
                'PROCESSED_BUCKET': config['buckets']['processed']
            }
        },
        {
            'name': 'mediaflow-upload-handler',
            'dir': 'lambda-functions/upload-handler', 
            'env': {
                'UPLOADS_BUCKET': config['buckets']['uploads']
            }
        },
        {
            'name': 'mediaflow-cleanup-handler',
            'dir': 'lambda-functions/cleanup-handler',
            'env': {
                'UPLOADS_BUCKET': config['buckets']['uploads'],
                'PROCESSED_BUCKET': config['buckets']['processed']
            }
        },
        {
            'name': 'mediaflow-view-handler',
            'dir': 'lambda-functions/view-handler',
            'env': {
                'UPLOADS_BUCKET': config['buckets']['uploads']
            }
        },
        {
            'name': 'mediaflow-convert-handler',
            'dir': 'lambda-functions/convert-handler',
            'env': {
                'UPLOADS_BUCKET': config['buckets']['uploads'],
                'PROCESSED_BUCKET': config['buckets']['processed']
            }
        }
    ]
    
    success_count = 0
    for func in functions:
        print(f"Deploying {func['name']}...")
        zip_path = create_lambda_zip(func['dir'])
        
        if deploy_lambda(lambda_client, func['name'], zip_path, role_arn, func['env']):
            success_count += 1
        
        os.remove(zip_path)  # Cleanup
    
    print(f"Deployment complete: {success_count}/{len(functions)} functions deployed")
    
    # Update config
    config['lambda_functions'] = [f['name'] for f in functions]
    config['lambda_role_arn'] = role_arn
    
    with open('mediaflow-config.json', 'w') as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()