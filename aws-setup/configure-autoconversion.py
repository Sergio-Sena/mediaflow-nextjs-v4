#!/usr/bin/env python3
import boto3
import json

def configure_s3_autoconversion():
    """Configure S3 events for automatic video conversion"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    s3_client = boto3.client('s3')
    lambda_client = boto3.client('lambda')
    
    bucket_name = config['buckets']['uploads']
    convert_function = 'mediaflow-convert-handler'
    
    print(f"Configuring S3 autoconversion for: {bucket_name}")
    
    # 1. Add Lambda permission for S3 to invoke
    try:
        lambda_client.add_permission(
            FunctionName=convert_function,
            StatementId='s3-trigger-autoconvert',
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f'arn:aws:s3:::{bucket_name}'
        )
        print("[OK] Lambda permission added")
    except lambda_client.exceptions.ResourceConflictException:
        print("[OK] Lambda permission already exists")
    
    # 2. Configure S3 notification
    notification_config = {
        'LambdaFunctionConfigurations': [
            {
                'Id': 'video-autoconvert-trigger',
                'LambdaFunctionArn': f'arn:aws:lambda:us-east-1:{config["account_id"]}:function:{convert_function}',
                'Events': ['s3:ObjectCreated:*'],
                'Filter': {
                    'Key': {
                        'FilterRules': [
                            {
                                'Name': 'suffix',
                                'Value': '.ts'
                            }
                        ]
                    }
                }
            },
            {
                'Id': 'video-autoconvert-avi',
                'LambdaFunctionArn': f'arn:aws:lambda:us-east-1:{config["account_id"]}:function:{convert_function}',
                'Events': ['s3:ObjectCreated:*'],
                'Filter': {
                    'Key': {
                        'FilterRules': [
                            {
                                'Name': 'suffix',
                                'Value': '.avi'
                            }
                        ]
                    }
                }
            },
            {
                'Id': 'video-autoconvert-mov',
                'LambdaFunctionArn': f'arn:aws:lambda:us-east-1:{config["account_id"]}:function:{convert_function}',
                'Events': ['s3:ObjectCreated:*'],
                'Filter': {
                    'Key': {
                        'FilterRules': [
                            {
                                'Name': 'suffix',
                                'Value': '.mov'
                            }
                        ]
                    }
                }
            }
        ]
    }
    
    try:
        s3_client.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration=notification_config
        )
        print("[OK] S3 notification configured")
        
        # Verify configuration
        response = s3_client.get_bucket_notification_configuration(Bucket=bucket_name)
        lambda_configs = response.get('LambdaConfigurations', [])
        print(f"[OK] Configured {len(lambda_configs)} Lambda triggers")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error configuring S3 notification: {str(e)}")
        return False

if __name__ == "__main__":
    success = configure_s3_autoconversion()
    if success:
        print("\n[SUCCESS] Autoconversion configured successfully!")
        print("[INFO] Test: Upload a .ts/.avi/.mov file to trigger conversion")
    else:
        print("\n[FAILED] Configuration failed!")