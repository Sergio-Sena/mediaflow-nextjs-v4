#!/usr/bin/env python3
import boto3
import json

cf = boto3.client('cloudfront', region_name='us-east-1')
dist_id = 'E1A2CZM0WKF6LX'

print('Obtendo configuracao atual...')
response = cf.get_distribution_config(Id=dist_id)
config = response['DistributionConfig']
etag = response['ETag']

print('\n=== OTIMIZACOES ===')

# 1. Habilitar compressão
if not config['DefaultCacheBehavior'].get('Compress', False):
    config['DefaultCacheBehavior']['Compress'] = True
    print('[OK] Compressao habilitada (Gzip/Brotli)')
else:
    print('[SKIP] Compressao ja habilitada')

# 2. Otimizar TTL
default_ttl = config['DefaultCacheBehavior'].get('DefaultTTL', 0)
if default_ttl < 86400:  # 24 horas
    config['DefaultCacheBehavior']['MinTTL'] = 0
    config['DefaultCacheBehavior']['DefaultTTL'] = 86400  # 24h
    config['DefaultCacheBehavior']['MaxTTL'] = 31536000  # 1 ano
    print(f'[OK] TTL otimizado: {default_ttl}s -> 86400s (24h)')
else:
    print(f'[SKIP] TTL ja otimizado ({default_ttl}s)')

# 3. HTTP/2 e HTTP/3
if config.get('HttpVersion') != 'http2and3':
    config['HttpVersion'] = 'http2and3'
    print('[OK] HTTP/2 e HTTP/3 habilitados')
else:
    print('[SKIP] HTTP/2 e HTTP/3 ja habilitados')

# 4. IPv6
if not config.get('IsIPV6Enabled', False):
    config['IsIPV6Enabled'] = True
    print('[OK] IPv6 habilitado')
else:
    print('[SKIP] IPv6 ja habilitado')

# Aplicar mudanças
print('\nAplicando configuracoes...')
try:
    cf.update_distribution(
        Id=dist_id,
        DistributionConfig=config,
        IfMatch=etag
    )
    print('[SUCCESS] CloudFront atualizado! (Status: InProgress)')
    print('Aguarde 5-10 minutos para propagacao.')
except Exception as e:
    print(f'[ERROR] {e}')
