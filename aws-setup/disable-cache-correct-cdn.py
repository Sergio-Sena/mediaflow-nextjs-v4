#!/usr/bin/env python3
import boto3
import json

client = boto3.client('cloudfront')
DISTRIBUTION_ID = 'E2HZKZ9ZJK18IU'

print(f"Desabilitando cache do CloudFront {DISTRIBUTION_ID}...")

response = client.get_distribution_config(Id=DISTRIBUTION_ID)
config = response['DistributionConfig']
etag = response['ETag']

# Desabilitar cache
config['DefaultCacheBehavior']['MinTTL'] = 0
config['DefaultCacheBehavior']['DefaultTTL'] = 0
config['DefaultCacheBehavior']['MaxTTL'] = 0

print("Atualizando...")

client.update_distribution(
    Id=DISTRIBUTION_ID,
    DistributionConfig=config,
    IfMatch=etag
)

print("Cache desabilitado!")
print("Aguarde 5-10 minutos.")
print("Teste: https://midiaflow.sstechnologies-cloud.com/dashboard")
