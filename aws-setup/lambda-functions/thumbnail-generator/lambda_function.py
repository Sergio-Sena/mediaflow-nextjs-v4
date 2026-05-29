import json
import os
import subprocess
import tempfile
import boto3
import jwt

ALLOWED_ORIGINS = ['https://midiaflow.sstechnologies-cloud.com', 'http://localhost:3000']

def get_origin(event=None):
    if not event:
        return ALLOWED_ORIGINS[0]
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]



s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
THUMB_PREFIX = 'public/thumbnails/'
JWT_SECRET = os.environ['JWT_SECRET']
def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except Exception:
        return None


def generate_thumbnail(video_key, output_key):
    """Download video from S3, extract first frame, upload thumbnail."""
    with tempfile.TemporaryDirectory() as tmp:
        video_path = os.path.join(tmp, 'video.mp4')
        thumb_path = os.path.join(tmp, 'thumb.jpg')

        # Download video (only first 5MB for speed - enough for first frame)
        obj = s3.get_object(Bucket=BUCKET, Key=video_key, Range='bytes=0-5242880')
        with open(video_path, 'wb') as f:
            f.write(obj['Body'].read())

        # Extract first frame with ffmpeg
        ffmpeg = '/opt/bin/ffmpeg'
        cmd = [ffmpeg, '-i', video_path, '-vframes', '1', '-q:v', '5',
               '-vf', 'scale=320:-1', '-y', thumb_path]
        result = subprocess.run(cmd, capture_output=True, timeout=30)

        if result.returncode != 0 or not os.path.exists(thumb_path):
            # Retry with full file if partial download failed
            s3.download_file(BUCKET, video_key, video_path)
            result = subprocess.run(cmd, capture_output=True, timeout=60)

        if not os.path.exists(thumb_path):
            return False

        # Upload thumbnail
        s3.upload_file(thumb_path, BUCKET, output_key,
                       ExtraArgs={'ContentType': 'image/jpeg'})
        return True


def lambda_handler(event, context):
    # Mode 1: S3 trigger (auto-generate on upload)
    if 'Records' in event:
        for record in event['Records']:
            key = record['s3']['object']['key']
            if not key.endswith('.mp4'):
                continue
            # Generate thumbnail path: users/x/folder/file.mp4 -> public/thumbnails/x/folder/file.jpg
            parts = key.split('/')
            if len(parts) >= 3 and parts[0] == 'users':
                thumb_key = THUMB_PREFIX + '/'.join(parts[1:]).rsplit('.', 1)[0] + '.jpg'
                generate_thumbnail(key, thumb_key)
        return {'statusCode': 200, 'body': json.dumps({'message': 'Thumbnails generated'})}

    # Mode 2: API call (batch generate or single)
    headers = event.get('headers', {})
    token = (headers.get('Authorization') or headers.get('authorization', '')).replace('Bearer ', '')
    user = verify_token(token)
    if not user or user.get('role') != 'admin':
        return {
            'statusCode': 403,
            'headers': {'Access-Control-Allow-Origin': get_origin(event)},
            'body': json.dumps({'error': 'Admin only'})
        }

    body = json.loads(event.get('body', '{}'))
    action = body.get('action', 'batch')

    if action == 'single':
        video_key = body.get('video_key')
        if not video_key:
            return {'statusCode': 400, 'body': json.dumps({'error': 'video_key required'})}
        parts = video_key.split('/')
        thumb_key = THUMB_PREFIX + '/'.join(parts[1:]).rsplit('.', 1)[0] + '.jpg'
        ok = generate_thumbnail(video_key, thumb_key)
        return {
            'statusCode': 200 if ok else 500,
            'headers': {'Access-Control-Allow-Origin': get_origin(event)},
            'body': json.dumps({'thumbnail': thumb_key if ok else None})
        }

    # Batch: generate for all videos that don't have thumbnails yet
    if action == 'batch':
        # List all videos
        paginator = s3.get_paginator('list_objects_v2')
        videos = []
        for page in paginator.paginate(Bucket=BUCKET, Prefix='users/'):
            for obj in page.get('Contents', []):
                if obj['Key'].endswith('.mp4'):
                    videos.append(obj['Key'])

        # List existing thumbnails
        existing = set()
        for page in paginator.paginate(Bucket=BUCKET, Prefix=THUMB_PREFIX):
            for obj in page.get('Contents', []):
                existing.add(obj['Key'])

        generated = 0
        errors = 0
        for video_key in videos:
            parts = video_key.split('/')
            if len(parts) < 3:
                continue
            thumb_key = THUMB_PREFIX + '/'.join(parts[1:]).rsplit('.', 1)[0] + '.jpg'
            if thumb_key in existing:
                continue
            try:
                if generate_thumbnail(video_key, thumb_key):
                    generated += 1
                else:
                    errors += 1
            except Exception:
                errors += 1
            # Lambda timeout safety (14 min max)
            if context.get_remaining_time_in_millis() < 60000:
                break

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': get_origin(event)},
            'body': json.dumps({
                'generated': generated,
                'errors': errors,
                'total_videos': len(videos)
            })
        }

    return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': get_origin(event)},
        'body': json.dumps({'error': 'Invalid action'})
    }
