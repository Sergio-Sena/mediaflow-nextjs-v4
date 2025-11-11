import json
import boto3
import os
import jwt
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))
from logger import Logger
from urllib.parse import unquote

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')
SECRET_KEY = 'mediaflow_super_secret_key_2025'

def lambda_handler(event, context):
    correlation_id = event.get('headers', {}).get('x-correlation-id', None)
    logger = Logger('files-handler', correlation_id)
    
    try:
        method = event['httpMethod']
        path = event.get('path', '')
        logger.info("Files request received", method=method, path=path)
        
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
            
            logger.info("List files request", context=view_context, has_auth=bool(auth_header))
            
            if auth_header:
                try:
                    token = auth_header.replace('Bearer ', '')
                    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                    user_prefix = decoded.get('s3_prefix', '')
                    user_role = decoded.get('role', 'user')
                    logger.info("JWT decoded", s3_prefix=user_prefix, role=user_role)
                except Exception as e:
                    logger.warn("JWT decode failed", error=str(e))
                    pass
            
            # admin vê tudo, users veem apenas sua pasta
            if user_role == 'admin':
                user_prefix = ''  # Admin vê tudo
                logger.info("Admin access - full access")
            elif user_prefix:
                logger.info("User access", prefix=user_prefix)
            
            return list_files(user_prefix, view_context, logger)
        elif method == 'DELETE' and 'bulk-delete' not in path:
            # Try pathParameters first, then body
            if event.get('pathParameters') and event['pathParameters'].get('key'):
                key = unquote(event['pathParameters']['key'])
            else:
                body = json.loads(event['body'])
                key = body.get('key')
            logger.info("Delete file request", key=key)
            return delete_file(key, logger)
        elif method == 'POST' and 'bulk-delete' in path:
            body = json.loads(event['body'])
            keys = body.get('keys', [])
            logger.info("Bulk delete request", count=len(keys))
            return bulk_delete(keys, logger)
            
    except Exception as e:
        logger.error("Files handler error", error=str(e))
        return cors_response(500, {'success': False, 'message': str(e)})

def list_files(user_prefix='', context='dashboard', logger=None):
    files = []
    if logger:
        logger.info("Listing files", prefix=user_prefix, context=context)
    
    for bucket, bucket_type in [(UPLOADS_BUCKET, 'uploads'), (PROCESSED_BUCKET, 'processed')]:
        try:
            # Usar paginator para listar TODOS os arquivos
            paginator = s3.get_paginator('list_objects_v2')
            
            if user_prefix:
                page_iterator = paginator.paginate(Bucket=bucket, Prefix=user_prefix)
            else:
                page_iterator = paginator.paginate(Bucket=bucket)
            
            # Iterar por TODAS as páginas
            for page in page_iterator:
                for obj in page.get('Contents', []):
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
                        folder_path = 'root'
                        filename = key
                    
                    files.append({
                        'key': key,
                        'name': filename,
                        'folder': folder_path,
                        'size': obj['Size'],
                        'lastModified': obj['LastModified'].isoformat(),
                        'bucket': bucket_type,
                        'url': f"https://{bucket}.s3.amazonaws.com/{obj['Key']}"
                    })
        except Exception as e:
            if logger:
                logger.warn("Bucket list error", bucket=bucket, error=str(e))
            pass
    
    if logger:
        logger.info("Files listed", total=len(files))
        logger.metric("files_listed", len(files))
    return cors_response(200, {'success': True, 'files': files})

def delete_file(key, logger=None):
    try:
        s3.delete_object(Bucket=UPLOADS_BUCKET, Key=key)
        s3.delete_object(Bucket=PROCESSED_BUCKET, Key=key)
        if logger:
            logger.info("File deleted", key=key)
            logger.metric("file_deleted", 1)
        return cors_response(200, {'success': True})
    except Exception as e:
        if logger:
            logger.error("Delete failed", key=key, error=str(e))
        return cors_response(404, {'success': False, 'message': 'File not found'})

def bulk_delete(keys, logger=None):
    deleted = []
    for key in keys:
        try:
            s3.delete_object(Bucket=UPLOADS_BUCKET, Key=key)
            s3.delete_object(Bucket=PROCESSED_BUCKET, Key=key)
            deleted.append(key)
        except:
            pass
    
    if logger:
        logger.info("Bulk delete completed", requested=len(keys), deleted=len(deleted))
        logger.metric("bulk_delete", len(deleted))
    
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