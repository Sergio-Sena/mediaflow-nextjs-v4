import os
import subprocess
import boto3

BUCKET = 'mediaflow-uploads-969430605054'
THUMB_PREFIX = 'public/thumbnails/'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
TEMP_DIR = os.path.join(os.environ['TEMP'], 'midiaflow_thumbs')

s3 = boto3.client('s3', region_name='us-east-1')
os.makedirs(TEMP_DIR, exist_ok=True)

# Video de teste
video_key = 'users/sergio_sena/Star/Honey_Sasha/Foda_me_Na_Cozinha_e_Cum_on_Meus_Peitos_Grandes.mp4'
thumb_key = THUMB_PREFIX + '/'.join(video_key.split('/')[1:]).rsplit('.', 1)[0] + '.jpg'

print(f"Video: {video_key}")
print(f"Thumb: {thumb_key}")

# Presigned URL
url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': video_key}, ExpiresIn=1800)
print(f"URL gerada: {url[:80]}...")

local_thumb = os.path.join(TEMP_DIR, 'test_thumb.jpg')

# FFmpeg streaming com seek 10s
cmd = [FFMPEG, '-ss', '10', '-i', url, '-vframes', '1', '-q:v', '3', '-vf', 'scale=320:-1', '-y', local_thumb]
print(f"\nExecutando ffmpeg...")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

if result.returncode == 0 and os.path.exists(local_thumb) and os.path.getsize(local_thumb) > 0:
    size = os.path.getsize(local_thumb)
    print(f"[OK] Thumbnail gerada: {size} bytes")
    
    # Upload
    s3.upload_file(local_thumb, BUCKET, thumb_key, ExtraArgs={'ContentType': 'image/jpeg'})
    print(f"[OK] Upload feito: {thumb_key}")
    os.remove(local_thumb)
else:
    print(f"[ERR] FFmpeg falhou")
    print(f"stderr: {result.stderr[:200]}")
