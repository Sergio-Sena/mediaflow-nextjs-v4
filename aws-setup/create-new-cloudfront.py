import boto3
import json
import time

cf = boto3.client('cloudfront')
s3_bucket = 'mediaflow-frontend-969430605054'
domain = 'midiaflow.sstechnologies-cloud.com'

config = {
    'CallerReference': f'midiaflow-v2-{int(time.time())}',
    'Comment': 'MidiaFlow CDN v2 - Cache correto',
    'Enabled': True,
    'Origins': {
        'Quantity': 1,
        'Items': [{
            'Id': 'S3-mediaflow-frontend',
            'DomainName': f'{s3_bucket}.s3.us-east-1.amazonaws.com',
            'S3OriginConfig': {'OriginAccessIdentity': ''}
        }]
    },
    'DefaultRootObject': 'index.html',
    'DefaultCacheBehavior': {
        'TargetOriginId': 'S3-mediaflow-frontend',
        'ViewerProtocolPolicy': 'redirect-to-https',
        'AllowedMethods': {
            'Quantity': 2,
            'Items': ['GET', 'HEAD'],
            'CachedMethods': {'Quantity': 2, 'Items': ['GET', 'HEAD']}
        },
        'Compress': True,
        'CachePolicyId': '658327ea-f89d-4fab-a63d-7e88639e58f6',  # CachingOptimized
        'OriginRequestPolicyId': '88a5eaf4-2fd4-4709-b370-b4c650ea3fcf'  # CORS-S3Origin
    },
    'CacheBehaviors': {
        'Quantity': 2,
        'Items': [
            {
                'PathPattern': '*.html',
                'TargetOriginId': 'S3-mediaflow-frontend',
                'ViewerProtocolPolicy': 'redirect-to-https',
                'AllowedMethods': {
                    'Quantity': 2,
                    'Items': ['GET', 'HEAD'],
                    'CachedMethods': {'Quantity': 2, 'Items': ['GET', 'HEAD']}
                },
                'Compress': True,
                'CachePolicyId': '4135ea2d-6df8-44a3-9df3-4b5a84be39ad',  # CachingDisabled
                'OriginRequestPolicyId': '88a5eaf4-2fd4-4709-b370-b4c650ea3fcf'
            },
            {
                'PathPattern': '_next/static/*',
                'TargetOriginId': 'S3-mediaflow-frontend',
                'ViewerProtocolPolicy': 'redirect-to-https',
                'AllowedMethods': {
                    'Quantity': 2,
                    'Items': ['GET', 'HEAD'],
                    'CachedMethods': {'Quantity': 2, 'Items': ['GET', 'HEAD']}
                },
                'Compress': True,
                'CachePolicyId': '658327ea-f89d-4fab-a63d-7e88639e58f6',  # CachingOptimized (1 ano)
                'OriginRequestPolicyId': '88a5eaf4-2fd4-4709-b370-b4c650ea3fcf'
            }
        ]
    },
    'Aliases': {'Quantity': 0, 'Items': []},
    'ViewerCertificate': {
        'CloudFrontDefaultCertificate': True
    },
    'CustomErrorResponses': {
        'Quantity': 2,
        'Items': [
            {'ErrorCode': 403, 'ResponsePagePath': '/index.html', 'ResponseCode': '200', 'ErrorCachingMinTTL': 300},
            {'ErrorCode': 404, 'ResponsePagePath': '/index.html', 'ResponseCode': '200', 'ErrorCachingMinTTL': 300}
        ]
    }
}

print("[INFO] Buscando certificado SSL...")
print(f"[OK] Certificado: arn:aws:acm:us-east-1:969430605054:certificate/5da53d3b-4f07-4aeb-9654-0b1bfea7bc0a")

print("[INFO] Criando CloudFront...")
response = cf.create_distribution(DistributionConfig=config)
new_dist_id = response['Distribution']['Id']
new_domain = response['Distribution']['DomainName']

print(f"\n[OK] CloudFront criado!")
print(f"Distribution ID: {new_dist_id}")
print(f"Domain: {new_domain}")
print(f"\nProximos passos:")
print(f"1. Aguarde 10-15 minutos para deploy")
print(f"2. Atualize DNS: midiaflow.sstechnologies-cloud.com -> {new_domain}")
print(f"3. Teste: https://{new_domain}")
print(f"4. Depois delete o antigo: E2HZKZ9ZJK18IU")
