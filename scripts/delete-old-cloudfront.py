#!/usr/bin/env python3
import boto3

cf = boto3.client('cloudfront', region_name='us-east-1')
old_distributions = ['E1O4R8P5BGZTMW', 'EFJXJ07BDK7UF']

for dist_id in old_distributions:
    try:
        response = cf.get_distribution_config(Id=dist_id)
        config = response['DistributionConfig']
        etag = response['ETag']
        status = cf.get_distribution(Id=dist_id)['Distribution']['Status']
        
        if not config['Enabled'] and status == 'Deployed':
            cf.delete_distribution(Id=dist_id, IfMatch=etag)
            print(f'[OK] {dist_id} deletada!')
        else:
            print(f'[WAIT] {dist_id} - Status: {status}, Enabled: {config["Enabled"]}')
    except Exception as e:
        if 'NoSuchDistribution' in str(e):
            print(f'[OK] {dist_id} ja deletada')
        else:
            print(f'[ERROR] {dist_id}: {e}')
