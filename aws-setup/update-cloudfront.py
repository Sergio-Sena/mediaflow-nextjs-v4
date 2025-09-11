#!/usr/bin/env python3
import boto3
import json
import time

def update_cloudfront_domain():
    """Update CloudFront distribution with custom domain"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    cloudfront = boto3.client('cloudfront')
    distribution_id = config['cloudfront']['distribution_id']
    domain = "mediaflow.sstechnologies-cloud.com"
    
    print(f"Updating CloudFront distribution {distribution_id}")
    
    # Get current distribution config
    response = cloudfront.get_distribution_config(Id=distribution_id)
    distribution_config = response['DistributionConfig']
    etag = response['ETag']
    
    # Add custom domain alias
    distribution_config['Aliases'] = {
        'Quantity': 1,
        'Items': [domain]
    }
    
    # Update distribution
    cloudfront.update_distribution(
        Id=distribution_id,
        DistributionConfig=distribution_config,
        IfMatch=etag
    )
    
    print(f"CloudFront updated with domain: {domain}")
    print("Distribution is being deployed (15-20 minutes)")
    
    return domain

if __name__ == "__main__":
    update_cloudfront_domain()