import boto3
import json

cf = boto3.client('cloudfront')
dist_id = 'E2HZKZ9ZJK18IU'

# Get config
config = cf.get_distribution_config(Id=dist_id)
etag = config['ETag']
dist_config = config['DistributionConfig']

# Criar cache policy sem cache para HTMLs
cache_policy = {
    'CachePolicyConfig': {
        'Name': 'NoCache-HTMLs-MidiaFlow',
        'MinTTL': 0,
        'MaxTTL': 0,
        'DefaultTTL': 0,
        'ParametersInCacheKeyAndForwardedToOrigin': {
            'EnableAcceptEncodingGzip': False,
            'EnableAcceptEncodingBrotli': False,
            'QueryStringsConfig': {'QueryStringBehavior': 'none'},
            'HeadersConfig': {'HeaderBehavior': 'none'},
            'CookiesConfig': {'CookieBehavior': 'none'}
        }
    }
}

try:
    policy_response = cf.create_cache_policy(**cache_policy)
    policy_id = policy_response['CachePolicy']['Id']
    print(f"[OK] Cache policy criada: {policy_id}")
except Exception as e:
    if 'already exists' in str(e):
        # Listar policies existentes
        policies = cf.list_cache_policies(Type='custom')
        for policy in policies['CachePolicyList']['Items']:
            if policy['CachePolicy']['CachePolicyConfig']['Name'] == 'NoCache-HTMLs-MidiaFlow':
                policy_id = policy['CachePolicy']['Id']
                print(f"[OK] Cache policy existente: {policy_id}")
                break
    else:
        raise

# Atualizar default behavior para usar a policy
dist_config['DefaultCacheBehavior']['CachePolicyId'] = policy_id
if 'ForwardedValues' in dist_config['DefaultCacheBehavior']:
    del dist_config['DefaultCacheBehavior']['ForwardedValues']
if 'MinTTL' in dist_config['DefaultCacheBehavior']:
    del dist_config['DefaultCacheBehavior']['MinTTL']
if 'MaxTTL' in dist_config['DefaultCacheBehavior']:
    del dist_config['DefaultCacheBehavior']['MaxTTL']
if 'DefaultTTL' in dist_config['DefaultCacheBehavior']:
    del dist_config['DefaultCacheBehavior']['DefaultTTL']

# Update distribution
cf.update_distribution(
    Id=dist_id,
    DistributionConfig=dist_config,
    IfMatch=etag
)

print("[OK] CloudFront atualizado - cache de HTMLs desabilitado")
