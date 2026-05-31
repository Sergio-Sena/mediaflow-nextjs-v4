import os
import subprocess
import boto3

BUCKET = 'mediaflow-uploads-969430605054'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
TEMP_DIR = os.path.join(os.environ['TEMP'], 'midiaflow_thumbs')
VIDEO_KEY = 'users/sergio_sena/10000_Anos_Depois.mp4'
THUMB_KEY = 'public/thumbnails/sergio_sena/10000_Anos_Depois.jpg'

s3 = boto3.client('s3', region_name='us-east-1')

def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    local_thumb = os.path.join(TEMP_DIR, '10000_Anos_Depois.jpg')

    url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': VIDEO_KEY}, ExpiresIn=1800)

    print(f"Gerando thumbnail para: {VIDEO_KEY}")
    cmd = [FFMPEG, '-ss', '10', '-i', url, '-vframes', '1', '-q:v', '3', '-vf', 'scale=320:-1', '-y', local_thumb]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=120)

    if result.returncode != 0 or not os.path.exists(local_thumb):
        print("Fallback: primeiro frame...")
        cmd_fb = [FFMPEG, '-i', url, '-vframes', '1', '-q:v', '3', '-vf', 'scale=320:-1', '-y', local_thumb]
        subprocess.run(cmd_fb, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=120)

    if os.path.exists(local_thumb) and os.path.getsize(local_thumb) > 0:
        s3.upload_file(local_thumb, BUCKET, THUMB_KEY, ExtraArgs={'ContentType': 'image/jpeg'})
        os.remove(local_thumb)
        print(f"✅ Thumbnail gerado e enviado: s3://{BUCKET}/{THUMB_KEY}")
    else:
        print(f"❌ Falha ao gerar thumbnail. Stderr: {result.stderr.decode()[:200]}")

if __name__ == '__main__':
    main()
