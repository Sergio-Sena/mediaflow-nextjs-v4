import boto3
import time

client = boto3.client('cloudfront', region_name='us-east-1')

# Criar nova distribuição SEM alias
print("Criando nova distribuicao CloudFront SEM alias...")
new_config = {
    'CallerReference': f'midiaflow-v3-{int(time.time())}',
    'Aliases': {'Quantity': 0},  # SEM ALIAS
    'DefaultRootObject': 'index.html',
    'Origins': {
        'Quantity': 1,
        'Items': [{
            'Id': 'S3-mediaflow-frontend',
            'DomainName': 'mediaflow-frontend-969430605054.s3.us-east-1.amazonaws.com',
            'S3OriginConfig': {'OriginAccessIdentity': ''},
            'ConnectionAttempts': 3,
            'ConnectionTimeout': 10,
            'OriginShield': {'Enabled': False},
            'OriginAccessControlId': ''
        }]
    },
    'DefaultCacheBehavior': {
        'TargetOriginId': 'S3-mediaflow-frontend',
        'ViewerProtocolPolicy': 'redirect-to-https',
        'AllowedMethods': {
            'Quantity': 2,
            'Items': ['HEAD', 'GET'],
            'CachedMethods': {'Quantity': 2, 'Items': ['HEAD', 'GET']}
        },
        'Compress': True,
        'CachePolicyId': '658327ea-f89d-4fab-a63d-7e88639e58f6',
        'OriginRequestPolicyId': '88a5eaf4-2fd4-4709-b370-b4c650ea3fcf'
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
                    'Items': ['HEAD', 'GET'],
                    'CachedMethods': {'Quantity': 2, 'Items': ['HEAD', 'GET']}
                },
                'Compress': True,
                'CachePolicyId': '4135ea2d-6df8-44a3-9df3-4b5a84be39ad',
                'OriginRequestPolicyId': '88a5eaf4-2fd4-4709-b370-b4c650ea3fcf'
            },
            {
                'PathPattern': '_next/static/*',
                'TargetOriginId': 'S3-mediaflow-frontend',
                'ViewerProtocolPolicy': 'redirect-to-https',
                'AllowedMethods': {
                    'Quantity': 2,
                    'Items': ['HEAD', 'GET'],
                    'CachedMethods': {'Quantity': 2, 'Items': ['HEAD', 'GET']}
                },
                'Compress': True,
                'CachePolicyId': '658327ea-f89d-4fab-a63d-7e88639e58f6',
                'OriginRequestPolicyId': '88a5eaf4-2fd4-4709-b370-b4c650ea3fcf'
            }
        ]
    },
    'CustomErrorResponses': {
        'Quantity': 2,
        'Items': [
            {'ErrorCode': 403, 'ResponsePagePath': '/index.html', 'ResponseCode': '200', 'ErrorCachingMinTTL': 300},
            {'ErrorCode': 404, 'ResponsePagePath': '/index.html', 'ResponseCode': '200', 'ErrorCachingMinTTL': 300}
        ]
    },
    'Comment': 'MidiaFlow CDN v3 - Cache limpo',
    'PriceClass': 'PriceClass_All',
    'Enabled': True,
    'ViewerCertificate': {
        'CloudFrontDefaultCertificate': True  # Usar certificado padrão por enquanto
    },
    'HttpVersion': 'http2',
    'IsIPV6Enabled': True
}

response = client.create_distribution(DistributionConfig=new_config)

dist_id = response['Distribution']['Id']
domain = response['Distribution']['DomainName']

print(f"\n=== SUCESSO ===")
print(f"Novo ID: {dist_id}")
print(f"Domain: {domain}")
print(f"Status: {response['Distribution']['Status']}")
print(f"\nTeste agora em: https://{domain}/login")
print(f"\nDepois de testar, adicione o alias manualmente:")
print(f"  aws cloudfront get-distribution-config --id {dist_id} > new-config.json")
print(f"  # Editar new-config.json para adicionar alias")
print(f"  aws cloudfront update-distribution --id {dist_id} --if-match ETAG --distribution-config file://new-config.json")
