import json
import boto3
import os
import jwt
from urllib.parse import unquote

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')
SECRET_KEY = os.environ['JWT_SECRET']
_request_origin = None

def get_allowed_origin(event):
    allowed = os.environ.get('ALLOWED_ORIGINS', 'https://midiaflow.sstechnologies-cloud.com').split(',')
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

            return list_files(user_prefix, view_context)
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
        print(f"Files handler error: {str(e)}")
        return cors_response(500, {'success': False, 'message': 'Internal server error'})


def get_duration_endpoint(key):
    try:
        head = s3.head_object(Bucket=UPLOADS_BUCKET, Key=key)
        duration = int(head.get('Metadata', {}).get('duration', 0))
        return cors_response(200, {'success': True, 'duration': duration})
    except:
        return cors_response(200, {'success': True, 'duration': 0})


def list_files(user_prefix='', context='dashboard'):
    files = []

    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(
            Bucket=UPLOADS_BUCKET,
            Prefix=user_prefix,
            PaginationConfig={'MaxItems': 2000}
        )

        for page in pages:
            for obj in page.get('Contents', []):
                key = obj['Key']

                if context == 'dashboard':
                    if key.startswith('avatars/') or key.startswith('qrcodes/') or key.startswith('public/'):
                        continue

                if '/' in key:
                    folder_path = '/'.join(key.split('/')[:-1])
                    filename = key.split('/')[-1]
                else:
                    folder_path = 'root'
                    filename = key

                duration = int(obj.get('Metadata', {}).get('duration', 0)) if obj.get('Metadata') else 0

                files.append({
                    'key': key,
                    'name': filename,
                    'folder': folder_path,
                    'size': obj['Size'],
                    'lastModified': obj['LastModified'].isoformat(),
                    'duration': duration
                })
    except Exception as e:
        print(f"list_files error: {str(e)}")

    return cors_response(200, {'success': True, 'files': files})


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
