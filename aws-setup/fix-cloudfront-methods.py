#!/usr/bin/env python3
import boto3
import json

def fix_cloudfront_methods():
    """Fix CloudFront to allow all HTTP methods"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    cloudfront = boto3.client('cloudfront')
    distribution_id = config['cloudfront']['distribution_id']
    
    print(f"Fixing CloudFront methods for {distribution_id}")
    
    # Get current distribution config
    response = cloudfront.get_distribution_config(Id=distribution_id)
    distribution_config = response['DistributionConfig']
    etag = response['ETag']
    
    # Fix default cache behavior to allow all methods
    distribution_config['DefaultCacheBehavior']['AllowedMethods'] = {
        'Quantity': 7,
        'Items': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE'],
        'CachedMethods': {
            'Quantity': 2,
            'Items': ['GET', 'HEAD']
        }
    }
    
    # Fix API cache behavior
    for behavior in distribution_config['CacheBehaviors']['Items']:
        if behavior['PathPattern'] == '/api/*':
            behavior['AllowedMethods'] = {
                'Quantity': 7,
                'Items': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE'],
                'CachedMethods': {
                    'Quantity': 2,
                    'Items': ['GET', 'HEAD']
                }
            }
    
    # Update distribution
    response = cloudfront.update_distribution(
        Id=distribution_id,
        DistributionConfig=distribution_config,
        IfMatch=etag
    )
    
    print(f"CloudFront updated to allow all HTTP methods!")
    print(f"Status: {response['Distribution']['Status']}")
    print("Deployment will take 15-20 minutes")
    
    return True

if __name__ == "__main__":
    fix_cloudfront_methods()