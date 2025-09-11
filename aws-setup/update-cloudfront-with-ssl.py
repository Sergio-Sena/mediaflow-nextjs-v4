#!/usr/bin/env python3
import boto3
import json

def update_cloudfront_with_ssl():
    """Update CloudFront distribution with SSL certificate and custom domain"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    cloudfront = boto3.client('cloudfront')
    distribution_id = config['cloudfront']['distribution_id']
    domain = "mediaflow.sstechnologies-cloud.com"
    cert_arn = "arn:aws:acm:us-east-1:969430605054:certificate/5da53d3b-4f07-4aeb-9654-0b1bfea7bc0a"
    
    print(f"Updating CloudFront distribution {distribution_id}")
    print(f"Domain: {domain}")
    print(f"Certificate: {cert_arn}")
    
    # Get current distribution config
    response = cloudfront.get_distribution_config(Id=distribution_id)
    distribution_config = response['DistributionConfig']
    etag = response['ETag']
    
    # Add custom domain alias
    distribution_config['Aliases'] = {
        'Quantity': 1,
        'Items': [domain]
    }
    
    # Add SSL certificate
    distribution_config['ViewerCertificate'] = {
        'ACMCertificateArn': cert_arn,
        'SSLSupportMethod': 'sni-only',
        'MinimumProtocolVersion': 'TLSv1.2_2021',
        'CertificateSource': 'acm'
    }
    
    # Update distribution
    response = cloudfront.update_distribution(
        Id=distribution_id,
        DistributionConfig=distribution_config,
        IfMatch=etag
    )
    
    print(f"CloudFront updated successfully!")
    print(f"Status: {response['Distribution']['Status']}")
    
    # Update config
    config['cloudfront']['custom_domain'] = domain
    config['cloudfront']['ssl_certificate'] = cert_arn
    config['production_url'] = f"https://{domain}"
    
    with open('mediaflow-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\nConfiguration Complete!")
    print(f"Production URL: https://{domain}")
    print(f"DNS propagation: 5-10 minutes")
    print(f"CloudFront deployment: 15-20 minutes")
    
    return domain

if __name__ == "__main__":
    update_cloudfront_with_ssl()