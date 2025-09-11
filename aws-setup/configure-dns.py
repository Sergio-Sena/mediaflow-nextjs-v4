#!/usr/bin/env python3
import boto3
import json

def configure_dns():
    """Configure DNS for CloudFront distribution"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    route53 = boto3.client('route53')
    
    # Use the actual domain
    domain = "mediaflow.sstechnologies-cloud.com"
    hosted_zone_id = "/hostedzone/Z07937031ROGP6XAEMPWJ"
    cloudfront_domain = config['cloudfront']['domain_name']
    
    print(f"Configuring DNS for {domain}")
    print(f"Pointing to CloudFront: {cloudfront_domain}")
    
    # Create CNAME record
    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Comment': 'Mediaflow CloudFront DNS',
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': domain,
                    'Type': 'CNAME',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': cloudfront_domain}]
                }
            }]
        }
    )
    
    change_id = response['ChangeInfo']['Id']
    print(f"DNS record created! Change ID: {change_id}")
    
    # Update config with real domain
    config['cloudfront']['custom_domain'] = domain
    config['production_url'] = f"https://{domain}"
    
    with open('mediaflow-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\nDNS Configuration Complete!")
    print(f"Domain: https://{domain}")
    print(f"Propagation: 5-10 minutes")
    
    return domain

if __name__ == "__main__":
    configure_dns()