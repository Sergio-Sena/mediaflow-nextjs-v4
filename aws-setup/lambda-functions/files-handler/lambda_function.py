import json
import boto3
import os
import jwt
from urllib.parse import unquote

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')
SECRET_KEY = 'mediaflow_super_secret_key_2025'

def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        path = event.get('path', '')
        
        if method == 'OPTIONS':
            return cors_response(200, {})
        elif method == 'GET':
            # Extrair context (dashboard ou admin)
            query_params = event.get('queryStringParameters') or {}
            view_context = query_params.get('context', 'dashboard')
            
            # Extrair e validar JWT para filtro por usuário
            user_prefix = ''
            user_role = 'user'
            auth_header = event.get('headers', {}).get('Authorization', '') or event.get('headers', {}).get('authorization', '')
            
            print(f"Auth header: {auth_header}, context: {view_context}")
            
            if auth_header:
                try:
                    token = auth_header.replace('Bearer ', '')
                    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                    user_prefix = decoded.get('s3_prefix', '')
                    user_role = decoded.get('role', 'user')
                    print(f"Decoded JWT - s3_prefix: '{user_prefix}', role: '{user_role}'")
                except Exception as e:
                    print(f"JWT decode error: {str(e)}")
                    pass
            
            # Admin vê tudo (sem filtro)
            if user_role == 'admin':
                user_prefix = ''
            
            return list_files(user_prefix, view_context)
        elif method == 'DELETE' and 'bulk-delete' not in path:
            # Try pathParameters first, then body
            if event.get('pathParameters') and event['pathParameters'].get('key'):
                key = unquote(event['pathParameters']['key'])
            else:
                body = json.loads(event['body'])
                key = body.get('key')
            return delete_file(key)
        elif method == 'POST' and 'bulk-delete' in path:
            body = json.loads(event['body'])
            return bulk_delete(body.get('keys', []))
            
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

def list_files(user_prefix='', context='dashboard'):
    files = []
    print(f"Listing files with prefix: '{user_prefix}', context: '{context}'")
    
    for bucket, bucket_type in [(UPLOADS_BUCKET, 'uploads'), (PROCESSED_BUCKET, 'processed')]:
        try:
            # Aplicar filtro de usuário se existir
            if user_prefix:
                print(f"Filtering bucket {bucket} with prefix: {user_prefix}")
                response = s3.list_objects_v2(Bucket=bucket, Prefix=user_prefix)
            else:
                print(f"Listing all files in bucket {bucket}")
                response = s3.list_objects_v2(Bucket=bucket)
            for obj in response.get('Contents', []):
                # Preserve full path structure
                key = obj['Key']
                
                # Filtrar pastas especiais no dashboard
                if context == 'dashboard':
                    if key.startswith('avatars/') or key.startswith('qrcodes/'):
                        continue
                
                # Extract folder and filename
                if '/' in key:
                    folder_path = '/'.join(key.split('/')[:-1])
                    filename = key.split('/')[-1]
                else:
                    folder_path = 'root'  # Changed from '' to 'root'
                    filename = key
                
                print(f"File: {key} -> folder: '{folder_path}', name: '{filename}'")
                
                files.append({
                    'key': key,  # Full path preserved
                    'name': filename,
                    'folder': folder_path,
                    'size': obj['Size'],
                    'lastModified': obj['LastModified'].isoformat(),
                    'bucket': bucket_type,
                    'url': f"https://{bucket}.s3.amazonaws.com/{obj['Key']}"
                })
        except Exception as e:
            print(f"Error listing bucket {bucket}: {str(e)}")
            pass
    
    return cors_response(200, {'success': True, 'files': files})

def delete_file(key):
    try:
        s3.delete_object(Bucket=UPLOADS_BUCKET, Key=key)
        s3.delete_object(Bucket=PROCESSED_BUCKET, Key=key)
        return cors_response(200, {'success': True})
    except:
        return cors_response(404, {'success': False, 'message': 'File not found'})

def bulk_delete(keys):
    deleted = []
    for key in keys:
        try:
            s3.delete_object(Bucket=UPLOADS_BUCKET, Key=key)
            s3.delete_object(Bucket=PROCESSED_BUCKET, Key=key)
            deleted.append(key)
        except:
            pass
    
    return cors_response(200, {'success': True, 'deleted': deleted})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }