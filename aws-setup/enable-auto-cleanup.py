#!/usr/bin/env python3
import boto3
import zipfile
import os

def enable_auto_cleanup():
    """Enable automatic cleanup of original files after conversion"""
    
    lambda_client = boto3.client('lambda')
    function_name = 'mediaflow-convert-handler'
    
    print("Enabling auto-cleanup for convert handler...")
    
    # Create zip file with updated code
    zip_path = 'convert-handler-auto-cleanup.zip'
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write(
            'lambda-functions/convert-handler/lambda_function_auto_cleanup.py',
            'lambda_function.py'
        )
    
    # Read zip file
    with open(zip_path, 'rb') as zip_file:
        zip_content = zip_file.read()
    
    # Update Lambda function
    response = lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_content
    )
    
    # Update timeout to handle cleanup operations
    lambda_client.update_function_configuration(
        FunctionName=function_name,
        Timeout=900,  # 15 minutes
        Description='MediaConvert handler with auto-cleanup of originals'
    )
    
    # Clean up
    os.remove(zip_path)
    
    print(f"✅ Auto-cleanup enabled for {function_name}")
    print("📋 Features:")
    print("  - Automatic original file deletion after successful conversion")
    print("  - Safety checks (file size validation)")
    print("  - Preserves originals if conversion fails")
    print("  - 15-minute timeout for long conversions")
    
    return True

if __name__ == "__main__":
    enable_auto_cleanup()