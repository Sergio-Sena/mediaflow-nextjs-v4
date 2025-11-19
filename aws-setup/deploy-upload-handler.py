#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import boto3
import json
import zipfile
import os
import time
from pathlib import Path

def create_lambda_zip(function_dir):
    """Create ZIP file for Lambda deployment"""
    zip_path = f"{function_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for file_path in Path(function_dir).rglob('*'):
            if file_path.is_file():
                zip_file.write(file_path, file_path.relative_to(function_dir))
    return zip_path

def main():
    print("Deploying midiaflow-upload-handler Lambda Function...")
    
    # Load config
    with open('midiaflow-config.json', 'r') as f:
        config = json.load(f)
    
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    role_arn = config['lambda_role_arn']
    
    # Create ZIP
    print("Creating deployment package...")
    zip_path = create_lambda_zip('lambda-functions/upload-handler')
    
    # Deploy
    print("Deploying to AWS...")
    with open(zip_path, 'rb') as zip_file:
        zip_content = zip_file.read()
    
    try:
        response = lambda_client.update_function_code(
            FunctionName='midiaflow-upload-handler',
            ZipFile=zip_content
        )
        print("Updated: midiaflow-upload-handler")
        print(f"Version: {response['Version']}")
    except lambda_client.exceptions.ResourceNotFoundException:
        print("Creating new function...")
        time.sleep(2)  # Wait for role to be available
        response = lambda_client.create_function(
            FunctionName='midiaflow-upload-handler',
            Runtime='python3.11',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content},
            Environment={'Variables': {
                'UPLOADS_BUCKET': config['buckets']['uploads']
            }},
            Timeout=30
        )
        print("Created: midiaflow-upload-handler")
        print(f"ARN: {response['FunctionArn']}")
    
    os.remove(zip_path)
    print("Deployment complete!")

if __name__ == "__main__":
    main()
