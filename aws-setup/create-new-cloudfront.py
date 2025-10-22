#!/usr/bin/env python3
"""
Script para criar novo CloudFront distribution
Uso: python create-new-cloudfront.py
"""

import boto3
import json
import time

def create_cloudfront_distribution():
    client = boto3.client('cloudfront')
    
    # Configuração idêntica ao atual
    config = {
        'CallerReference': f'midiaflow-v2-{int(time.time())}',
        'Comment': 'Mídiaflow v4.7 - Nova distribuição',
        'Enabled': True,
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': 'S3-mediaflow-frontend',
                    'DomainName': 'mediaflow-frontend-969430605054.s3-website-us-east-1.amazonaws.com',
                    'CustomOriginConfig': {
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'http-only',
                        'OriginSslProtocols': {
                            'Quantity': 1,
                            'Items': ['TLSv1.2']
                        }
                    }
                }
            ]
        },
        'DefaultRootObject': 'index.html',
        'DefaultCacheBehavior': {
            'TargetOriginId': 'S3-mediaflow-frontend',
            'ViewerProtocolPolicy': 'redirect-to-https',
            'AllowedMethods': {
                'Quantity': 7,
                'Items': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE'],
                'CachedMethods': {
                    'Quantity': 2,
                    'Items': ['GET', 'HEAD']
                }
            },
            'Compress': True,
            'MinTTL': 0,
            'DefaultTTL': 86400,  # 1 dia
            'MaxTTL': 31536000,   # 1 ano
            'ForwardedValues': {
                'QueryString': True,
                'Cookies': {'Forward': 'all'},
                'Headers': {
                    'Quantity': 0
                }
            },
            'TrustedSigners': {
                'Enabled': False,
                'Quantity': 0
            }
        },
        'CustomErrorResponses': {
            'Quantity': 2,
            'Items': [
                {
                    'ErrorCode': 404,
                    'ResponsePagePath': '/404.html',
                    'ResponseCode': '404',
                    'ErrorCachingMinTTL': 300
                },
                {
                    'ErrorCode': 403,
                    'ResponsePagePath': '/index.html',
                    'ResponseCode': '200',
                    'ErrorCachingMinTTL': 300
                }
            ]
        },
        'Aliases': {
            'Quantity': 1,
            'Items': ['midiaflow.sstechnologies-cloud.com']
        },
        'ViewerCertificate': {
            'ACMCertificateArn': 'arn:aws:acm:us-east-1:969430605054:certificate/5da53d3b-4f07-4aeb-9654-0b1bfea7bc0a',
            'SSLSupportMethod': 'sni-only',
            'MinimumProtocolVersion': 'TLSv1.2_2021'
        },
        'PriceClass': 'PriceClass_All',
        'HttpVersion': 'http2'
    }
    
    print("Criando nova distribuicao CloudFront...")
    print("Isso levara 15-30 minutos para propagar...")
    
    try:
        response = client.create_distribution(DistributionConfig=config)
        
        distribution_id = response['Distribution']['Id']
        domain_name = response['Distribution']['DomainName']
        
        print(f"\nDistribuicao criada com sucesso!")
        print(f"ID: {distribution_id}")
        print(f"Domain: {domain_name}")
        print(f"\nProximos passos:")
        print(f"1. Aguarde 15-30 min para status 'Deployed'")
        print(f"2. Atualize Route 53 para apontar para: {domain_name}")
        print(f"3. Teste: https://midiaflow.sstechnologies-cloud.com")
        print(f"4. Delete distribuição antiga: E3ODIUY4LXU8TH")
        
        return distribution_id
        
    except Exception as e:
        print(f"Erro: {e}")
        return None

if __name__ == '__main__':
    create_cloudfront_distribution()
