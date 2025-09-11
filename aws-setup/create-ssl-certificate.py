#!/usr/bin/env python3
import boto3
import json
import time

def create_ssl_certificate():
    """Create SSL certificate for custom domain"""
    
    # Load config
    with open('mediaflow-config.json', 'r') as f:
        config = json.load(f)
    
    # ACM must be in us-east-1 for CloudFront
    acm = boto3.client('acm', region_name='us-east-1')
    domain = "mediaflow.sstechnologies-cloud.com"
    
    print(f"Requesting SSL certificate for {domain}")
    
    # Request certificate
    response = acm.request_certificate(
        DomainName=domain,
        ValidationMethod='DNS',
        SubjectAlternativeNames=[f'*.sstechnologies-cloud.com']
    )
    
    cert_arn = response['CertificateArn']
    print(f"Certificate ARN: {cert_arn}")
    
    # Get validation records
    print("Getting DNS validation records...")
    time.sleep(5)  # Wait for certificate to be processed
    
    cert_details = acm.describe_certificate(CertificateArn=cert_arn)
    
    if 'DomainValidationOptions' in cert_details['Certificate']:
        validation_options = cert_details['Certificate']['DomainValidationOptions']
        
        route53 = boto3.client('route53')
        hosted_zone_id = "/hostedzone/Z07937031ROGP6XAEMPWJ"
        
        for option in validation_options:
            if 'ResourceRecord' in option:
                record = option['ResourceRecord']
                
                print(f"Adding DNS validation record for {option['DomainName']}")
                
                # Add DNS validation record
                route53.change_resource_record_sets(
                    HostedZoneId=hosted_zone_id,
                    ChangeBatch={
                        'Changes': [{
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': record['Name'],
                                'Type': record['Type'],
                                'TTL': 300,
                                'ResourceRecords': [{'Value': record['Value']}]
                            }
                        }]
                    }
                )
                
                print(f"DNS validation record added: {record['Name']}")
    
    # Update config
    config['ssl_certificate'] = {
        'arn': cert_arn,
        'domain': domain,
        'status': 'PENDING_VALIDATION'
    }
    
    with open('mediaflow-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\nSSL Certificate requested!")
    print(f"Certificate ARN: {cert_arn}")
    print(f"Validation records added to DNS")
    print(f"Validation will complete in 5-10 minutes")
    
    return cert_arn

if __name__ == "__main__":
    create_ssl_certificate()