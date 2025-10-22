#!/usr/bin/env python3
import boto3

client = boto3.client('cloudfront')

DISTRIBUTIONS = ['E3ODIUY4LXU8TH', 'E12GJ6BBJXZML5']

for dist_id in DISTRIBUTIONS:
    print(f"Desabilitando {dist_id}...")
    
    response = client.get_distribution_config(Id=dist_id)
    config = response['DistributionConfig']
    etag = response['ETag']
    
    config['Enabled'] = False
    
    client.update_distribution(
        Id=dist_id,
        DistributionConfig=config,
        IfMatch=etag
    )
    
    print(f"OK - {dist_id} desabilitado!")

print("\nAguarde 15-30 min para status 'Deployed', depois delete com:")
print("aws cloudfront delete-distribution --id E3ODIUY4LXU8TH --if-match ETAG")
print("aws cloudfront delete-distribution --id E12GJ6BBJXZML5 --if-match ETAG")
