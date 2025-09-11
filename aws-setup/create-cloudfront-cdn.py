#!/usr/bin/env python3
import boto3
import json
import time

def create_cloudfront_cdn():
    """Create CloudFront distribution for Mediaflow"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    cloudfront = boto3.client('cloudfront')
    
    print("Creating CloudFront CDN...")
    
    # Get domain from user
    domain = input("Digite seu domínio (ex: mediaflow.seudominio.com): ").strip()
    
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
                    'DomainName': config['api_gateway']['api_url'].replace('https://', ''),
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
        'Aliases': {
            'Quantity': 1,
            'Items': [domain]
        },
        'ViewerCertificate': {
            'ACMCertificateArn': 'REQUEST_CERTIFICATE',  # Will be replaced
            'SSLSupportMethod': 'sni-only',
            'MinimumProtocolVersion': 'TLSv1.2_2021'
        },
        'PriceClass': 'PriceClass_100'  # US, Canada, Europe
    }
    
    print(f"Requesting SSL certificate for {domain}...")
    
    # Request SSL certificate
    acm = boto3.client('acm', region_name='us-east-1')  # CloudFront requires us-east-1
    
    cert_response = acm.request_certificate(
        DomainName=domain,
        ValidationMethod='DNS',
        SubjectAlternativeNames=[f'*.{domain}'] if not domain.startswith('*.') else []
    )
    
    cert_arn = cert_response['CertificateArn']
    print(f"Certificate ARN: {cert_arn}")
    
    # Update distribution config with certificate
    distribution_config['ViewerCertificate']['ACMCertificateArn'] = cert_arn
    del distribution_config['ViewerCertificate']['REQUEST_CERTIFICATE']
    
    print("Waiting for certificate validation...")
    print(f"Please add the DNS validation records for {domain}")
    
    # Wait for certificate validation
    waiter = acm.get_waiter('certificate_validated')
    try:
        waiter.wait(
            CertificateArn=cert_arn,
            WaiterConfig={'Delay': 30, 'MaxAttempts': 40}
        )
        print("Certificate validated!")
    except:
        print("Certificate validation timeout. Continuing anyway...")
    
    # Create CloudFront distribution
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
        'custom_domain': domain,
        'certificate_arn': cert_arn
    }
    
    with open('mediaflow-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\nNext Steps:")
    print(f"1. Add CNAME record: {domain} -> {domain_name}")
    print(f"2. Wait 15-20 minutes for distribution deployment")
    print(f"3. Access your site at: https://{domain}")
    
    return distribution_id, domain_name

def create_route53_record():
    """Create Route 53 DNS record"""
    
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    if 'cloudfront' not in config:
        print("CloudFront not configured yet")
        return
    
    route53 = boto3.client('route53')
    
    # List hosted zones
    zones = route53.list_hosted_zones()
    
    domain = config['cloudfront']['custom_domain']
    root_domain = '.'.join(domain.split('.')[-2:])
    
    hosted_zone_id = None
    for zone in zones['HostedZones']:
        if zone['Name'].rstrip('.') == root_domain:
            hosted_zone_id = zone['Id']
            break
    
    if not hosted_zone_id:
        print(f"Hosted zone for {root_domain} not found")
        print("Please create the DNS record manually:")
        print(f"CNAME: {domain} -> {config['cloudfront']['domain_name']}")
        return
    
    # Create CNAME record
    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': domain,
                    'Type': 'CNAME',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': config['cloudfront']['domain_name']}]
                }
            }]
        }
    )
    
    print(f"DNS record created for {domain}")

if __name__ == "__main__":
    print("Mediaflow CloudFront CDN Setup")
    print("=" * 40)
    
    choice = input("1. Create CloudFront distribution\n2. Create Route 53 DNS record\nChoice (1-2): ")
    
    if choice == "1":
        create_cloudfront_cdn()
    elif choice == "2":
        create_route53_record()
    else:
        print("Invalid choice")