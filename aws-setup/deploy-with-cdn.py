#!/usr/bin/env python3
import boto3
import json
import subprocess
import os

def deploy_frontend_with_cdn():
    """Deploy frontend with CDN configuration"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    print("Building frontend with CDN configuration...")
    
    # Build frontend
    os.chdir('..')
    result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Build failed:", result.stderr)
        return False
    
    print("Build completed successfully!")
    
    # Deploy to S3
    s3 = boto3.client('s3')
    bucket = config['buckets']['frontend']
    
    print(f"Deploying to S3 bucket: {bucket}")
    
    # Upload build files
    subprocess.run([
        'aws', 's3', 'sync', 'out/', f's3://{bucket}/',
        '--delete', '--cache-control', 'max-age=31536000'
    ])
    
    print("Frontend deployed successfully!")
    
    # Invalidate CloudFront cache
    if 'cloudfront' in config:
        cloudfront = boto3.client('cloudfront')
        distribution_id = config['cloudfront']['distribution_id']
        
        print("Invalidating CloudFront cache...")
        
        cloudfront.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': ['/*']
                },
                'CallerReference': str(int(time.time()))
            }
        )
        
        print("Cache invalidation started!")
    
    print("\nDeployment completed!")
    print(f"CDN URL: https://{config['cloudfront']['domain_name']}")
    print(f"Custom Domain: https://{config['cloudfront']['custom_domain']} (after DNS setup)")
    
    return True

if __name__ == "__main__":
    import time
    deploy_frontend_with_cdn()