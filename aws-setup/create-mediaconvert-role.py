#!/usr/bin/env python3
import boto3
import json

iam = boto3.client('iam')

# Create MediaConvert service role
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "mediaconvert.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

try:
    # Create role
    response = iam.create_role(
        RoleName='MediaConvertRole',
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description='Role for MediaConvert to access S3'
    )
    print(f"Created role: {response['Role']['Arn']}")
    
    # Attach S3 policy
    iam.attach_role_policy(
        RoleName='MediaConvertRole',
        PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
    )
    print("Attached S3 policy")
    
except Exception as e:
    if 'EntityAlreadyExists' in str(e):
        print("Role already exists")
    else:
        print(f"Error: {e}")