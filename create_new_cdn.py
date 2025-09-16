#!/usr/bin/env python3
import boto3
import json
import time

def create_new_cdn():
    cloudfront = boto3.client('cloudfront')
    
    # Configuração do novo CDN
    config = {
        'CallerReference': f'mediaflow-v2-{int(time.time())}',
        'Comment': 'Mediaflow v4.1 - Upload Modular',
        'DefaultRootObject': 'index.html',
        'Origins': {
            'Quantity': 1,
            'Items': [{
                'Id': 'S3-mediaflow-frontend',
                'DomainName': 'mediaflow-frontend-969430605054.s3.amazonaws.com',
                'S3OriginConfig': {
                    'OriginAccessIdentity': ''
                }
            }]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'S3-mediaflow-frontend',
            'ViewerProtocolPolicy': 'redirect-to-https',
            'MinTTL': 0,
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {'Forward': 'none'}
            }
        },
        'Enabled': True,
        'PriceClass': 'PriceClass_100'
    }
    
    print("Criando novo CDN CloudFront...")
    
    try:
        response = cloudfront.create_distribution(DistributionConfig=config)
        
        distribution_id = response['Distribution']['Id']
        domain_name = response['Distribution']['DomainName']
        
        print("CDN Criado!")
        print(f"ID: {distribution_id}")
        print(f"Domain: {domain_name}")
        print(f"Status: {response['Distribution']['Status']}")
        
        # Salvar configuração
        new_config = {
            'new_cdn': {
                'distribution_id': distribution_id,
                'domain_name': domain_name,
                'status': 'Deploying'
            }
        }
        
        with open('new-cdn-config.json', 'w') as f:
            json.dump(new_config, f, indent=2)
        
        print(f"\nNovo CDN em deploy (5-10 min)")
        print(f"URL temporaria: https://{domain_name}")
        
        return distribution_id, domain_name
        
    except Exception as e:
        print(f"Erro: {e}")
        return None, None

if __name__ == "__main__":
    create_new_cdn()