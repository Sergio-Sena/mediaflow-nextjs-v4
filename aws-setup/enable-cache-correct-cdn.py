#!/usr/bin/env python3
import boto3

client = boto3.client('cloudfront')
DISTRIBUTION_ID = 'E2HZKZ9ZJK18IU'

print(f"Reativando cache do CloudFront {DISTRIBUTION_ID}...")

response = client.get_distribution_config(Id=DISTRIBUTION_ID)
config = response['DistributionConfig']
etag = response['ETag']

# Reativar cache (valores otimizados)
config['DefaultCacheBehavior']['MinTTL'] = 0
config['DefaultCacheBehavior']['DefaultTTL'] = 86400  # 1 dia
config['DefaultCacheBehavior']['MaxTTL'] = 31536000  # 1 ano

print("Atualizando...")

client.update_distribution(
    Id=DISTRIBUTION_ID,
    DistributionConfig=config,
    IfMatch=etag
)

print("Cache reativado!")
print("Performance maxima restaurada.")
