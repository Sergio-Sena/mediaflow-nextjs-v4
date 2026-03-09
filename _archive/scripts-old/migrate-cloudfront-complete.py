import boto3
import time

client = boto3.client('cloudfront', region_name='us-east-1')

# 1. Remover alias da distribuição antiga
print("1. Removendo alias da distribuicao antiga...")
response = client.get_distribution_config(Id='E1O4R8P5BGZTMW')
config = response['DistributionConfig']
etag = response['ETag']

config['Aliases'] = {'Quantity': 0}
config['Enabled'] = False

client.update_distribution(
    Id='E1O4R8P5BGZTMW',
    DistributionConfig=config,
    IfMatch=etag
)
print("   Alias removido e distribuicao desabilitada!")
print("   Aguardando 3 minutos para propagacao...")
time.sleep(180)

# 2. Criar nova distribuição
print("\n2. Criando nova distribuicao CloudFront...")
new_config = {
    'CallerReference': f'midiaflow-v3-{int(time.time())}',
    'Aliases': {
        'Quantity': 1,
        'Items': ['midiaflow.sstechnologies-cloud.com']
    },
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
        'ACMCertificateArn': 'arn:aws:acm:us-east-1:969430605054:certificate/5da53d3b-4f07-4aeb-9654-0b1bfea7bc0a',
        'SSLSupportMethod': 'sni-only',
        'MinimumProtocolVersion': 'TLSv1.2_2021',
        'CertificateSource': 'acm'
    },
    'HttpVersion': 'http2',
    'IsIPV6Enabled': True
}

response = client.create_distribution(DistributionConfig=new_config)

dist_id = response['Distribution']['Id']
domain = response['Distribution']['DomainName']

print(f"   Nova distribuicao criada!")
print(f"\n=== SUCESSO ===")
print(f"Novo ID: {dist_id}")
print(f"Domain: {domain}")
print(f"Status: {response['Distribution']['Status']}")
print(f"\nAguarde 5-10 minutos para propagacao completa.")
print(f"\nProximo passo: Atualizar README.md com: {dist_id}")
