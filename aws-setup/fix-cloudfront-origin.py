#!/usr/bin/env python3
"""
Atualiza origem do CloudFront para apontar para S3 correto
"""

import boto3

client = boto3.client('cloudfront')

DISTRIBUTION_ID = 'E2HZKZ9ZJK18IU'
S3_BUCKET = 'mediaflow-frontend-969430605054.s3-website-us-east-1.amazonaws.com'

print(f"Atualizando CloudFront {DISTRIBUTION_ID}...")

# Get config
response = client.get_distribution_config(Id=DISTRIBUTION_ID)
config = response['DistributionConfig']
etag = response['ETag']

print(f"Origem atual: {config['Origins']['Items'][0]['DomainName']}")

# Atualizar origem para S3
config['Origins']['Items'][0]['DomainName'] = S3_BUCKET
config['Origins']['Items'][0]['Id'] = 'frontend-origin'  # Manter ID original

# Remover S3OriginConfig se existir (usar CustomOrigin para website)
if 'S3OriginConfig' in config['Origins']['Items'][0]:
    del config['Origins']['Items'][0]['S3OriginConfig']

# Adicionar CustomOriginConfig
config['Origins']['Items'][0]['CustomOriginConfig'] = {
    'HTTPPort': 80,
    'HTTPSPort': 443,
    'OriginProtocolPolicy': 'http-only',
    'OriginSslProtocols': {
        'Quantity': 1,
        'Items': ['TLSv1.2']
    },
    'OriginReadTimeout': 30,
    'OriginKeepaliveTimeout': 5
}

# TargetOriginId já está correto (frontend-origin)

# Desabilitar cache temporariamente
config['DefaultCacheBehavior']['MinTTL'] = 0
config['DefaultCacheBehavior']['DefaultTTL'] = 0
config['DefaultCacheBehavior']['MaxTTL'] = 0

print(f"Nova origem: {S3_BUCKET}")
print("Atualizando...")

# Update
client.update_distribution(
    Id=DISTRIBUTION_ID,
    DistributionConfig=config,
    IfMatch=etag
)

print("CloudFront atualizado!")
print("Aguarde 5-10 minutos para propagar.")
print("Teste: https://midiaflow.sstechnologies-cloud.com/dashboard")
