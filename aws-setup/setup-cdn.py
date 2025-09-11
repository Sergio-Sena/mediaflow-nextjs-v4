#!/usr/bin/env python3
import boto3
import json
import time
import sys

def create_cloudfront_cdn(domain):
    """Create CloudFront distribution for Mediaflow"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    cloudfront = boto3.client('cloudfront')
    
    print(f"Creating CloudFront CDN for {domain}...")
    
    # CloudFront distribution config
    distribution_config = {
        'CallerReference': f'mediaflow-{int(time.time())}',
        'Comment': 'Mediaflow Next.js CDN Distribution',
        'DefaultRootObject': 'index.html',
        'Origins': {
            'Quantity': 3,
            'Items': [
                {
                    'Id': 'frontend-origin',
                    'DomainName': f"{config['buckets']['frontend']}.s3-website-{config['region']}.amazonaws.com",
                    'CustomOriginConfig': {
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'http-only'
                    }
                },
                {
                    'Id': 'api-origin',
                    'DomainName': config['api_gateway']['api_url'].replace('https://', '').split('/')[0],
                    'OriginPath': '/prod',
                    'CustomOriginConfig': {
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'https-only'
                    }
                },
                {
                    'Id': 'media-origin',
                    'DomainName': f"{config['buckets']['processed']}.s3.{config['region']}.amazonaws.com",
                    'S3OriginConfig': {
                        'OriginAccessIdentity': ''
                    }
                }
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'frontend-origin',
            'ViewerProtocolPolicy': 'redirect-to-https',
            'TrustedSigners': {
                'Enabled': False,
                'Quantity': 0
            },
            'ForwardedValues': {
                'QueryString': True,
                'Cookies': {'Forward': 'all'},
                'Headers': {
                    'Quantity': 3,
                    'Items': ['Authorization', 'Content-Type', 'Origin']
                }
            },
            'MinTTL': 0,
            'DefaultTTL': 86400,
            'MaxTTL': 31536000
        },
        'CacheBehaviors': {
            'Quantity': 2,
            'Items': [
                {
                    'PathPattern': '/api/*',
                    'TargetOriginId': 'api-origin',
                    'ViewerProtocolPolicy': 'https-only',
                    'TrustedSigners': {
                        'Enabled': False,
                        'Quantity': 0
                    },
                    'ForwardedValues': {
                        'QueryString': True,
                        'Cookies': {'Forward': 'all'},
                        'Headers': {
                            'Quantity': 5,
                            'Items': ['Authorization', 'Content-Type', 'Origin', 'Accept', 'User-Agent']
                        }
                    },
                    'MinTTL': 0,
                    'DefaultTTL': 0,
                    'MaxTTL': 0
                },
                {
                    'PathPattern': '/media/*',
                    'TargetOriginId': 'media-origin',
                    'ViewerProtocolPolicy': 'https-only',
                    'TrustedSigners': {
                        'Enabled': False,
                        'Quantity': 0
                    },
                    'ForwardedValues': {
                        'QueryString': False,
                        'Cookies': {'Forward': 'none'}
                    },
                    'MinTTL': 0,
                    'DefaultTTL': 86400,
                    'MaxTTL': 31536000
                }
            ]
        },
        'Enabled': True,
        'PriceClass': 'PriceClass_100'  # US, Canada, Europe
    }
    
    # Create distribution without custom domain first
    print("Creating CloudFront distribution...")
    
    response = cloudfront.create_distribution(
        DistributionConfig=distribution_config
    )
    
    distribution_id = response['Distribution']['Id']
    domain_name = response['Distribution']['DomainName']
    
    print(f"CloudFront distribution created!")
    print(f"Distribution ID: {distribution_id}")
    print(f"CloudFront Domain: {domain_name}")
    
    # Update config
    config['cloudfront'] = {
        'distribution_id': distribution_id,
        'domain_name': domain_name,
        'custom_domain': domain
    }
    
    with open('mediaflow-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\nNext Steps:")
    print(f"1. Add CNAME record: {domain} -> {domain_name}")
    print(f"2. Wait 15-20 minutes for distribution deployment")
    print(f"3. Access your site at: https://{domain_name} (temporary)")
    print(f"4. After DNS: https://{domain}")
    
    return distribution_id, domain_name

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup-cdn.py your-domain.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    create_cloudfront_cdn(domain)