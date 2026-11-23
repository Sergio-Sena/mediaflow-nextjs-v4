# -*- coding: utf-8 -*-
import sys, os, subprocess, boto3
sys.stdout.reconfigure(encoding='utf-8')

BUCKET = 'mediaflow-uploads-969430605054'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
TEMP_DIR = os.path.join(os.environ['TEMP'], 'midiaflow_thumbs')
os.makedirs(TEMP_DIR, exist_ok=True)

s3 = boto3.client('s3', region_name='us-east-1')
paginator = s3.get_paginator('list_objects_v2')

# Carrega todos os thumbs
thumbs = set()
for page in paginator.paginate(Bucket=BUCKET, Prefix='public/thumbnails/'):
    for o in page.get('Contents', []):
        thumbs.add(o['Key'])

# Encontra vídeos sem thumb
missing = []
for page in paginator.paginate(Bucket=BUCKET, Prefix='users/sergio_sena/'):
    for o in page.get('Contents', []):
        k = o['Key']
        if not k.lower().endswith(('.mp4','.mkv','.avi','.webm','.ts','.mov','.wmv','.flv')):
            continue
        parts = k.split('/')
        thumb = 'public/thumbnails/' + '/'.join(parts[1:]).rsplit('.', 1)[0] + '.jpg'
        if thumb not in thumbs:
            missing.append((k, thumb))

print(f"Videos sem thumbnail: {len(missing)}")
for v, _ in missing:
    print(f"  {v}")

print("\n--- Gerando ---")
for video_key, thumb_key in missing:
    filename = video_key.split('/')[-1]
    print(f"\n[{filename}]")

    url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': video_key}, ExpiresIn=1800)
    local_thumb = os.path.join(TEMP_DIR, filename.rsplit('.', 1)[0] + '.jpg')

    # Tenta seek 10s
    cmd = [FFMPEG, '-ss', '10', '-i', url, '-vframes', '1', '-q:v', '3', '-vf', 'scale=320:-1', '-y', local_thumb]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

    if not (os.path.exists(local_thumb) and os.path.getsize(local_thumb) > 0):
        print(f"  seek 10s falhou, tentando frame 0...")
        print(f"  stderr: {r.stderr[-300:]}")
        cmd2 = [FFMPEG, '-i', url, '-vframes', '1', '-q:v', '3', '-vf', 'scale=320:-1', '-y', local_thumb]
        r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=90)
        if not (os.path.exists(local_thumb) and os.path.getsize(local_thumb) > 0):
            print(f"  FALHOU: {r2.stderr[-200:]}")
            continue

    s3.upload_file(local_thumb, BUCKET, thumb_key, ExtraArgs={'ContentType': 'image/jpeg'})
    os.remove(local_thumb)
    print(f"  OK -> {thumb_key}")
