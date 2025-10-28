import boto3
import json

cf = boto3.client('cloudfront', region_name='us-east-1')

DIST_ID = 'E2HZKZ9ZJK18IU'

print('[1/3] Obtendo configuracao atual...')
response = cf.get_distribution_config(Id=DIST_ID)
config = response['DistributionConfig']
etag = response['ETag']

print('[2/3] Habilitando compressao...')
config['DefaultCacheBehavior']['Compress'] = True

print('[3/3] Atualizando distribuicao...')
cf.update_distribution(
    Id=DIST_ID,
    DistributionConfig=config,
    IfMatch=etag
)

print('Compressao habilitada!')
print('Aguarde ~5min para propagar nas edge locations')
print('Reducao esperada: ~70% no tamanho dos arquivos')
