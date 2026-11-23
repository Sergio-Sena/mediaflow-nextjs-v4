import json
import boto3
import os
import jwt
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor, as_completed

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')
SECRET_KEY = os.environ['JWT_SECRET']
DEFAULT_ORIGIN = 'https://midiaflow.sstechnologies-cloud.com'
DEV_ORIGINS = ['http://localhost:3000', 'http://localhost:3001']
_request_origin = DEFAULT_ORIGIN

def get_allowed_origin(event):
    allowed = os.environ.get('ALLOWED_ORIGINS', DEFAULT_ORIGIN).split(',') + DEV_ORIGINS
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in allowed else allowed[0]

def lambda_handler(event, context):
    global _request_origin
    _request_origin = get_allowed_origin(event)
    try:
        method = event['httpMethod']
        path = event.get('path', '')

        if method == 'OPTIONS':
            return cors_response(200, {})
        elif method == 'GET':
            query_params = event.get('queryStringParameters') or {}
            view_context = query_params.get('context', 'dashboard')

            # Endpoint de duration: GET /files/duration?key=...
            if query_params.get('key'):
                return get_duration_endpoint(query_params['key'])

            user_prefix = ''
            user_role = 'user'
            auth_header = event.get('headers', {}).get('Authorization', '') or event.get('headers', {}).get('authorization', '')

            if auth_header:
                try:
                    token = auth_header.replace('Bearer ', '')
                    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                    user_prefix = decoded.get('s3_prefix', '')
                    user_role = decoded.get('role', 'user')
                except:
                    pass

            if user_role == 'admin':
                if view_context == 'dashboard':
                    user_prefix = user_prefix or 'admin/'
                else:
                    user_prefix = ''
            elif user_role == 'viewer':
                user_prefix = 'users/user_admin/'

            page = int(query_params.get('page') or 1)
            limit = min(int(query_params.get('limit') or 50), 200)
            return list_files(user_prefix, view_context, page, limit)
        elif method == 'DELETE' and 'bulk-delete' not in path:
            if event.get('pathParameters') and event['pathParameters'].get('key'):
                key = unquote(event['pathParameters']['key'])
            else:
                body = json.loads(event['body'])
                key = body.get('key')
            return delete_file(key)
        elif method == 'POST' and 'bulk-delete' in path:
            body = json.loads(event['body'])
            keys = body.get('keys', [])
            return bulk_delete(keys)

    except Exception as e:
        import traceback
        print(f"Files handler error: {str(e)}")
        print(traceback.format_exc())
        return cors_response(500, {'success': False, 'message': 'Internal server error'})


def get_duration_endpoint(key):
    try:
        head = s3.head_object(Bucket=UPLOADS_BUCKET, Key=key)
        duration = int(head.get('Metadata', {}).get('duration', 0))
        return cors_response(200, {'success': True, 'duration': duration})
    except:
        return cors_response(200, {'success': True, 'duration': 0})


def get_duration(key):
    try:
        head = s3.head_object(Bucket=UPLOADS_BUCKET, Key=key)
        return int(head.get('Metadata', {}).get('duration', 0))
    except:
        return 0


def list_files(user_prefix='', context='dashboard', page_num=1, limit=50):
    files = []

    try:
        paginator = s3.get_paginator('list_objects_v2')
        s3_pages = paginator.paginate(
            Bucket=UPLOADS_BUCKET,
            Prefix=user_prefix,
            PaginationConfig={'MaxItems': 2000}
        )

        for s3_page in s3_pages:
            for obj in s3_page.get('Contents', []):
                key = obj['Key']

                if context == 'dashboard':
                    if key.startswith('avatars/') or key.startswith('qrcodes/') or key.startswith('public/'):
                        continue

                folder_path = '/'.join(key.split('/')[:-1]) if '/' in key else 'root'
                filename = key.split('/')[-1]

                files.append({
                    'key': key,
                    'name': filename,
                    'folder': folder_path,
                    'size': obj['Size'],
                    'lastModified': obj['LastModified'].isoformat(),
                    'duration': 0
                })
    except Exception as e:
        print(f"list_files error: {str(e)}")
        return cors_response(500, {'success': False, 'message': 'Internal server error'})

    total = len(files)
    start = (page_num - 1) * limit
    page_files = files[start:start + limit]

    # Buscar duration em paralelo apenas para vídeos da página atual
    video_exts = ('.mp4', '.mkv', '.avi', '.mov', '.webm', '.ts')
    video_files = [f for f in page_files if f['name'].lower().endswith(video_exts)]

    if video_files:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(get_duration, f['key']): f['key'] for f in video_files}
            durations = {}
            for future in as_completed(futures):
                key = futures[future]
                try:
                    durations[key] = future.result()
                except:
                    durations[key] = 0

        for f in page_files:
            if f['key'] in durations:
                f['duration'] = durations[f['key']]

    return cors_response(200, {
        'success': True,
        'files': page_files,
        'total': total,
        'page': page_num,
        'limit': limit,
        'hasMore': (start + limit) < total
    })


def delete_thumbnail(key):
    if not key.endswith('.mp4'):
        return
    parts = key.split('/')
    if len(parts) >= 3 and parts[0] == 'users':
        thumb_key = 'public/thumbnails/' + '/'.join(parts[1:]).rsplit('.', 1)[0] + '.jpg'
        try:
            s3.delete_object(Bucket=UPLOADS_BUCKET, Key=thumb_key)
        except:
            pass


def delete_file(key):
    try:
        found = False
        try:
            s3.head_object(Bucket=UPLOADS_BUCKET, Key=key)
            s3.delete_object(Bucket=UPLOADS_BUCKET, Key=key)
            found = True
        except:
            pass
        try:
            s3.head_object(Bucket=PROCESSED_BUCKET, Key=key)
            s3.delete_object(Bucket=PROCESSED_BUCKET, Key=key)
            found = True
        except:
            pass
        if found:
            delete_thumbnail(key)
            return cors_response(200, {'success': True})
        else:
            return cors_response(404, {'success': False, 'message': 'File not found'})
    except Exception as e:
        print(f"Delete error: {str(e)}")
        return cors_response(500, {'success': False, 'message': 'Internal server error'})


def bulk_delete(keys):
    deleted = []
    for key in keys:
        try:
            s3.delete_object(Bucket=UPLOADS_BUCKET, Key=key)
            s3.delete_object(Bucket=PROCESSED_BUCKET, Key=key)
            delete_thumbnail(key)
            deleted.append(key)
        except:
            pass
    return cors_response(200, {'success': True, 'deleted': deleted})


def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': _request_origin or 'https://midiaflow.sstechnologies-cloud.com',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization,x-correlation-id',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body) if body else '{}'
    }
