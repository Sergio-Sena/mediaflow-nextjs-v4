import json
import boto3
import os

s3 = boto3.client('s3', region_name='us-east-1')

ALLOWED_ORIGINS = ['https://midiaflow.sstechnologies-cloud.com', 'http://localhost:3000']

_current_event = None

def get_origin():
    event = _current_event
    if not event:
        return ALLOWED_ORIGINS[0]
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]

def cors_headers(event):
    return {
        'Access-Control-Allow-Origin': get_origin(),
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'POST,OPTIONS'
    }

def lambda_handler(event, context):
    global _current_event
    _current_event = event
    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        user_id = body.get('userId')
        file_ext = body.get('fileExt', 'png')
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': cors_headers(event),
                'body': json.dumps({'success': False, 'error': 'userId required'})
            }
        
        key = f'avatars/avatar_{user_id}.{file_ext}'
        bucket = 'mediaflow-uploads-969430605054'

        try:
            old = s3.list_objects_v2(Bucket=bucket, Prefix=f'avatars/avatar_{user_id}.')
            for obj in old.get('Contents', []):
                if obj['Key'] != key:
                    s3.delete_object(Bucket=bucket, Key=obj['Key'])
        except:
            pass
        
        content_type_map = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        content_type = content_type_map.get(file_ext.lower(), 'image/jpeg')
        
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket,
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=300
        )
        
        presigned_url = presigned_url.replace('&amp;', '&')
        avatar_url = f'https://{bucket}.s3.amazonaws.com/{key}'
        
        return {
            'statusCode': 200,
            'headers': cors_headers(event),
            'body': json.dumps({
                'success': True,
                'presignedUrl': presigned_url,
                'avatarUrl': avatar_url
            })
        }
        
    except Exception as e:
        print(f"Avatar presigned error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers(event),
            'body': json.dumps({'success': False, 'error': 'Internal server error'})
        }
