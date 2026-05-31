import boto3
import os
import re
import unicodedata

BACKUP_BUCKET = 'backup-midia-smartphone'
MIDIAFLOW_BUCKET = 'mediaflow-uploads-969430605054'
REGION_BACKUP = 'sa-east-1'
REGION_MIDIAFLOW = 'us-east-1'

s3_backup = boto3.client('s3', region_name=REGION_BACKUP)
s3_mf = boto3.client('s3', region_name=REGION_MIDIAFLOW)

VIDEO_EXT = ('.mp4', '.mkv', '.avi', '.mov', '.ts')

def normalize_name(name):
    """Normalize filename for comparison (lowercase, no accents, no special chars)."""
    n = os.path.splitext(name)[0].lower()
    n = unicodedata.normalize('NFD', n)
    n = re.sub(r'[\u0300-\u036f]', '', n)
    n = re.sub(r'[^a-z0-9]', '', n)
    return n

def list_videos(client, bucket, prefix=''):
    paginator = client.get_paginator('list_objects_v2')
    videos = []
    kwargs = {'Bucket': bucket}
    if prefix:
        kwargs['Prefix'] = prefix
    for page in paginator.paginate(**kwargs):
        for obj in page.get('Contents', []):
            if obj['Key'].lower().endswith(VIDEO_EXT):
                videos.append(obj['Key'])
    return videos

def main():
    print("Listando videos do backup...")
    backup_videos = list_videos(s3_backup, BACKUP_BUCKET, 'Videos/')
    print(f"  Backup: {len(backup_videos)} videos")

    print("Listando videos do MidiaFlow...")
    mf_videos = list_videos(s3_mf, MIDIAFLOW_BUCKET, 'users/sergio_sena/')
    print(f"  MidiaFlow: {len(mf_videos)} videos")

    # Build normalized name set for MidiaFlow
    mf_names = set()
    for v in mf_videos:
        filename = v.split('/')[-1]
        mf_names.add(normalize_name(filename))

    # Compare
    already_in = []
    missing = []

    for v in backup_videos:
        filename = v.split('/')[-1]
        normalized = normalize_name(filename)
        if normalized in mf_names:
            already_in.append(v)
        else:
            missing.append(v)

    print(f"\n{'=' * 60}")
    print(f"RESULTADO")
    print(f"  Ja no MidiaFlow: {len(already_in)}")
    print(f"  Faltam migrar:   {len(missing)}")
    print(f"{'=' * 60}")

    if missing:
        print(f"\nVideos que FALTAM no MidiaFlow ({len(missing)}):")
        for v in sorted(missing):
            size_label = ''
            name = v.split('/')[-1]
            folder = '/'.join(v.split('/')[:-1])
            print(f"  [{folder}] {name}")

    # Save to file
    with open('missing_videos.txt', 'w', encoding='utf-8') as f:
        for v in sorted(missing):
            f.write(v + '\n')
    print(f"\nLista salva em: missing_videos.txt")

if __name__ == '__main__':
    main()
