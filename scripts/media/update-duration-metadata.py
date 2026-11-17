# -*- coding: utf-8 -*-
"""
Atualiza metadata 'duration' nos arquivos .mp4 já existentes no S3.
- Lista todos os .mp4 sem duration no metadata
- ffprobe lê duração via presigned URL (sem baixar o arquivo)
- copy-object atualiza o metadata no S3
"""
import boto3
import subprocess
import sys
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

BUCKET  = 'mediaflow-uploads-969430605054'
PREFIX  = 'users/sergio_sena/'
FFPROBE = r'C:\ffmpeg\bin\ffprobe.exe'
REGION  = 'us-east-1'

s3 = boto3.client('s3', region_name=REGION)


def get_duration_from_url(url):
    """ffprobe lê duração via URL sem baixar o arquivo inteiro."""
    cmd = [
        FFPROBE, '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0',
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=30)
    if result.returncode != 0 or not result.stdout.strip():
        return 0
    try:
        return int(float(result.stdout.strip().splitlines()[0]))
    except:
        return 0


def get_presigned_url(key):
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET, 'Key': key},
        ExpiresIn=300
    )


def get_existing_metadata(key):
    try:
        head = s3.head_object(Bucket=BUCKET, Key=key)
        return head.get('Metadata', {}), head.get('ContentType', 'video/mp4')
    except:
        return {}, 'video/mp4'


def update_metadata(key, duration, existing_meta, content_type):
    """copy-object para si mesmo com metadata atualizado."""
    new_meta = {**existing_meta, 'duration': str(duration)}
    s3.copy_object(
        Bucket=BUCKET,
        CopySource={'Bucket': BUCKET, 'Key': key},
        Key=key,
        Metadata=new_meta,
        MetadataDirective='REPLACE',
        ContentType=content_type,
    )


def process_key(key):
    existing_meta, content_type = get_existing_metadata(key)

    # Já tem duration válida — skip
    if int(existing_meta.get('duration', 0)) > 0:
        return key, 'skip', 0

    url = get_presigned_url(key)
    duration = get_duration_from_url(url)

    if duration <= 0:
        return key, 'error', 0

    update_metadata(key, duration, existing_meta, content_type)
    return key, 'ok', duration


def main():
    print(f'Listando .mp4 em s3://{BUCKET}/{PREFIX}\n')

    paginator = s3.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.mp4'):
                keys.append(obj['Key'])

    if not keys:
        print('Nenhum arquivo .mp4 encontrado.')
        return

    print(f'Total: {len(keys)} arquivos\n')
    print('=' * 60)

    updated = skipped = errors = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_key, k): k for k in keys}
        for i, future in enumerate(as_completed(futures), 1):
            key = futures[future]
            name = key.split('/')[-1]
            try:
                _, status, duration = future.result()
                if status == 'ok':
                    updated += 1
                    print(f'[{i}/{len(keys)}] OK  {name[:55]} → {duration}s')
                elif status == 'skip':
                    skipped += 1
                    print(f'[{i}/{len(keys)}] SKIP {name[:55]}')
                else:
                    errors += 1
                    print(f'[{i}/{len(keys)}] ERR  {name[:55]}')
            except Exception as e:
                errors += 1
                print(f'[{i}/{len(keys)}] ERR  {name[:55]} — {e}')

    print(f'\n{"="*60}')
    print(f'RESUMO')
    print(f'{"="*60}')
    print(f'  Atualizados: {updated}')
    print(f'  Já tinham:   {skipped}')
    print(f'  Erros:       {errors}')


if __name__ == '__main__':
    main()
