import boto3
import json

cloudfront = boto3.client('cloudfront', region_name='us-east-1')

response = cloudfront.get_distribution_config(Id='E2HZKZ9ZJK18IU')
config = response['DistributionConfig']
etag = response['ETag']

api_origin = {
    'Id': 'api-gateway',
    'DomainName': 'gdb962d234.execute-api.us-east-1.amazonaws.com',
    'CustomOriginConfig': {
        'HTTPPort': 80,
        'HTTPSPort': 443,
        'OriginProtocolPolicy': 'https-only',
        'OriginSSLProtocols': {
            'Quantity': 1,
            'Items': ['TLSv1.2']
        }
    }
}

origins_list = config['Origins']['Items']
if not any(o['Id'] == 'api-gateway' for o in origins_list):
    origins_list.append(api_origin)
    config['Origins']['Quantity'] = len(origins_list)

api_behavior = {
    'PathPattern': '/api/*',
    'TargetOriginId': 'api-gateway',
    'ViewerProtocolPolicy': 'https-only',
    'AllowedMethods': {
        'Quantity': 7,
        'Items': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE']
    },
    'CachedMethods': {
        'Quantity': 2,
        'Items': ['GET', 'HEAD']
    },
    'ForwardedValues': {
        'QueryString': True,
        'Cookies': {'Forward': 'all'},
        'Headers': {
            'Quantity': 5,
            'Items': ['Authorization', 'Content-Type', 'Host', 'Accept', 'Accept-Encoding']
        }
    },
    'MinTTL': 0,
    'DefaultTTL': 0,
    'MaxTTL': 0,
    'Compress': True
}

if not any(b['PathPattern'] == '/api/*' for b in config['CacheBehaviors']):
    config['CacheBehaviors'].append(api_behavior)

try:
    cloudfront.update_distribution(
        Id='E2HZKZ9ZJK18IU',
        DistributionConfig=config,
        IfMatch=etag
    )
    print("OK: CloudFront atualizado com API Gateway")
except Exception as e:
    print(f"ERRO: {e}")
