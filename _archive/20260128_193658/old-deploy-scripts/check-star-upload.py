import os
import boto3

AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = 'AKIA6DNURDT7MO5EXHLQ'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'mediaflow-uploads-969430605054'

LOCAL_PATH = r'C:\Users\dell 5557\Videos\IDM\Star'
S3_PREFIX = 'sergio/Star/'

s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def get_local_files():
    files = {}
    for root, dirs, filenames in os.walk(LOCAL_PATH):
        for filename in filenames:
            if filename.endswith('.mp4'):
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, LOCAL_PATH).replace('\\', '/')
                size = os.path.getsize(full_path)
                files[relative_path] = size
    return files

def get_s3_files():
    files = {}
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=S3_PREFIX)
    
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                if key.endswith('.mp4'):
                    relative_key = key.replace(S3_PREFIX, '')
                    files[relative_key] = obj['Size']
    return files

print('Verificando uploads...\n')

local_files = get_local_files()
s3_files = get_s3_files()

print(f'Arquivos locais: {len(local_files)}')
print(f'Arquivos no S3: {len(s3_files)}\n')

missing = []
incomplete = []

for file_path, local_size in local_files.items():
    if file_path not in s3_files:
        missing.append(file_path)
    elif s3_files[file_path] != local_size:
        incomplete.append((file_path, local_size, s3_files[file_path]))

if missing:
    print(f'FALTANDO ({len(missing)}):')
    for f in missing:
        print(f'  - {f}')
    print()

if incomplete:
    print(f'INCOMPLETOS ({len(incomplete)}):')
    for f, local, s3 in incomplete:
        print(f'  - {f}')
        print(f'    Local: {local:,} bytes | S3: {s3:,} bytes')
    print()

if not missing and not incomplete:
    print('TODOS OS ARQUIVOS FORAM ENVIADOS CORRETAMENTE!')
else:
    print(f'TOTAL COM PROBLEMAS: {len(missing) + len(incomplete)}')
