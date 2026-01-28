import boto3

AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = 'AKIA6DNURDT7MO5EXHLQ'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'mediaflow-uploads-969430605054'

s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

print('Calculando uso do bucket...\n')

total_size = 0
total_files = 0

paginator = s3_client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=BUCKET_NAME)

for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            total_size += obj['Size']
            total_files += 1

gb = total_size / (1024**3)
tb = total_size / (1024**4)

print(f'Total de arquivos: {total_files:,}')
print(f'Tamanho total: {gb:.2f} GB ({tb:.3f} TB)')
print(f'\nNOTA: S3 nao tem limite de espaco, e ilimitado!')
print('O problema pode ser:')
print('  - Memoria RAM do navegador')
print('  - Cache do navegador cheio')
print('  - Espaco em disco local (temp files)')
