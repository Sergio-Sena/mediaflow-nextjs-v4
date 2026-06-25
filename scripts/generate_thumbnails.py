import os
import subprocess
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed

BUCKET = 'mediaflow-uploads-969430605054'
VIDEO_PREFIX = 'users/'
THUMB_PREFIX = 'public/thumbnails/'
FFMPEG = r'C:\Program Files\FormatFactory5.22.0.0\ffmpeg.exe'
TEMP_DIR = os.path.join(os.environ['TEMP'], 'midiaflow_thumbs')
MAX_WORKERS = 10

session = boto3.Session(profile_name='default')
s3 = session.client('s3', region_name='us-east-1')

def get_thumb_key(video_key):
    """users/sergio_sena/Anime/file.mp4 -> public/thumbnails/sergio_sena/Anime/file.jpg"""
    parts = video_key.split('/')
    if len(parts) >= 3 and parts[0] == 'users':
        return THUMB_PREFIX + '/'.join(parts[1:]).rsplit('.', 1)[0] + '.jpg'
    return None

def thumb_exists(thumb_key):
    try:
        s3.head_object(Bucket=BUCKET, Key=thumb_key)
        return True
    except:
        return False

def process_video(video_key):
    thumb_key = get_thumb_key(video_key)
    if not thumb_key:
        return 'skip'

    if thumb_exists(thumb_key):
        return 'exists'

    # Presigned URL para streaming
    url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': video_key}, ExpiresIn=1800)

    local_thumb = os.path.join(TEMP_DIR, os.path.basename(video_key).rsplit('.', 1)[0] + '.jpg')

    # FFmpeg: seek 10s via streaming, extrai 1 frame
    cmd = [FFMPEG, '-ss', '10', '-i', url, '-vframes', '1', '-q:v', '3', '-vf', 'scale=320:-1', '-y', local_thumb]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)

    if result.returncode != 0 or not os.path.exists(local_thumb):
        # Fallback: primeiro frame
        cmd_fb = [FFMPEG, '-i', url, '-vframes', '1', '-q:v', '3', '-vf', 'scale=320:-1', '-y', local_thumb]
        subprocess.run(cmd_fb, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)

    if os.path.exists(local_thumb) and os.path.getsize(local_thumb) > 0:
        s3.upload_file(local_thumb, BUCKET, thumb_key, ExtraArgs={'ContentType': 'image/jpeg'})
        os.remove(local_thumb)
        return 'ok'

    return 'error'

def main():
    os.makedirs(TEMP_DIR, exist_ok=True)

    print("Listando videos no S3...")
    paginator = s3.get_paginator('list_objects_v2')
    videos = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix=VIDEO_PREFIX):
        for obj in page.get('Contents', []):
            if obj['Key'].lower().endswith(('.mp4', '.mkv', '.avi', '.webm', '.ts', '.mov', '.wmv', '.flv')):
                videos.append(obj['Key'])

    print(f"Total videos: {len(videos)}")
    print(f"Workers: {MAX_WORKERS}")
    print("=" * 60)

    stats = {'ok': 0, 'exists': 0, 'error': 0, 'skip': 0}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_video, v): v for v in videos}
        for i, future in enumerate(as_completed(futures), 1):
            video = futures[future]
            try:
                result = future.result()
                stats[result] += 1
                if result == 'ok':
                    print(f"[{i}/{len(videos)}] [OK] {video.split('/')[-1][:50]}")
                elif result == 'error':
                    print(f"[{i}/{len(videos)}] [ERR] {video.split('/')[-1][:50]}")
            except Exception as e:
                stats['error'] += 1
                print(f"[{i}/{len(videos)}] [EXCEPTION] {video.split('/')[-1][:30]} - {str(e)[:50]}")

    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL")
    print(f"  Geradas:  {stats['ok']}")
    print(f"  Existiam: {stats['exists']}")
    print(f"  Erros:    {stats['error']}")
    print(f"  Puladas:  {stats['skip']}")
    print("=" * 60)

if __name__ == '__main__':
    main()
