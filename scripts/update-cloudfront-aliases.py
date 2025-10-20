#!/usr/bin/env python3
"""
Remove mediaflow alias from CloudFront (keep only midiaflow)
"""
import boto3
import json

cloudfront = boto3.client('cloudfront', region_name='us-east-1')
DISTRIBUTION_ID = 'E2HZKZ9ZJK18IU'

def update_aliases():
    # Get current config
    response = cloudfront.get_distribution_config(Id=DISTRIBUTION_ID)
    config = response['DistributionConfig']
    etag = response['ETag']
    
    print("Current aliases:", config['Aliases']['Items'])
    
    # Update aliases - keep only midiaflow
    config['Aliases']['Items'] = ['midiaflow.sstechnologies-cloud.com']
    config['Aliases']['Quantity'] = 1
    
    # Update distribution
    cloudfront.update_distribution(
        Id=DISTRIBUTION_ID,
        DistributionConfig=config,
        IfMatch=etag
    )
    
    print("Updated aliases:", config['Aliases']['Items'])
    print("Distribution updated successfully!")

if __name__ == '__main__':
    try:
        update_aliases()
    except Exception as e:
        print(f"Error: {e}")
