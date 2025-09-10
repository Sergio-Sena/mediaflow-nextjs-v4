#!/usr/bin/env python3
"""
Mediaflow AWS Setup - Create S3 Buckets and Basic Infrastructure
"""

import boto3
import json
import sys
from datetime import datetime

def create_bucket(s3_client, bucket_name, region='us-east-1'):
    """Create S3 bucket with proper configuration"""
    try:
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        # Configure CORS
        cors_config = {
            'CORSRules': [
                {
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET', 'POST', 'PUT', 'DELETE', 'HEAD'],
                    'AllowedOrigins': ['*'],
                    'MaxAgeSeconds': 3600
                }
            ]
        }
        s3_client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_config)
        
        print(f"Created bucket: {bucket_name}")
        return True
    except Exception as e:
        print(f"Error creating bucket {bucket_name}: {str(e)}")
        return False

def main():
    print("Mediaflow AWS Setup - Phase 1")
    print("=" * 50)
    
    # Initialize AWS clients
    try:
        session = boto3.Session()
        s3_client = session.client('s3')
        sts_client = session.client('sts')
        
        # Get account info
        identity = sts_client.get_caller_identity()
        account_id = identity['Account']
        print(f"AWS Account: {account_id}")
        print(f"User: {identity['Arn']}")
        
    except Exception as e:
        print(f"AWS Configuration Error: {str(e)}")
        sys.exit(1)
    
    # Define bucket names
    buckets = [
        f"mediaflow-frontend-{account_id}",
        f"mediaflow-uploads-{account_id}",
        f"mediaflow-processed-{account_id}"
    ]
    
    print(f"\nCreating {len(buckets)} S3 buckets...")
    
    # Create buckets
    success_count = 0
    for bucket_name in buckets:
        if create_bucket(s3_client, bucket_name):
            success_count += 1
    
    print(f"\nResults: {success_count}/{len(buckets)} buckets created")
    
    if success_count == len(buckets):
        print("Phase 1 Complete - All buckets created successfully!")
        
        # Save configuration
        config = {
            "account_id": account_id,
            "region": "us-east-1",
            "buckets": {
                "frontend": buckets[0],
                "uploads": buckets[1],
                "processed": buckets[2]
            },
            "created_at": datetime.now().isoformat()
        }
        
        with open('mediaflow-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("Configuration saved to mediaflow-config.json")
        
        # Test bucket access
        print("\nTesting bucket access...")
        for bucket_name in buckets:
            try:
                s3_client.head_bucket(Bucket=bucket_name)
                print(f"{bucket_name} - accessible")
            except Exception as e:
                print(f"{bucket_name} - error: {str(e)}")
    else:
        print("Phase 1 Incomplete - Some buckets failed to create")
        sys.exit(1)

if __name__ == "__main__":
    main()