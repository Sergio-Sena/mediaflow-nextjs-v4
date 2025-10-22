#!/usr/bin/env python3
"""
Desabilita cache do CloudFront temporariamente (TTL = 0)
"""

import boto3
import json

client = boto3.client('cloudfront')

# CloudFront que está servindo o domínio
DISTRIBUTION_ID = 'E3ODIUY4LXU8TH'

print(f"Desabilitando cache do CloudFront {DISTRIBUTION_ID}...")

# Get config
response = client.get_distribution_config(Id=DISTRIBUTION_ID)
config = response['DistributionConfig']
etag = response['ETag']

# Desabilitar cache (TTL = 0)
config['DefaultCacheBehavior']['MinTTL'] = 0
config['DefaultCacheBehavior']['DefaultTTL'] = 0
config['DefaultCacheBehavior']['MaxTTL'] = 0

print("Atualizando configuracao...")

# Update
client.update_distribution(
    Id=DISTRIBUTION_ID,
    DistributionConfig=config,
    IfMatch=etag
)

print("Cache desabilitado! Aguarde 5-10 minutos para propagar.")
print("Teste novamente: https://midiaflow.sstechnologies-cloud.com/dashboard")
print("\nPara reativar cache depois, rode: enable-cloudfront-cache.py")
