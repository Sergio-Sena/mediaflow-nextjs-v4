import boto3
import json
import base64
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))
from logger import Logger
from datetime import datetime

ALLOWED_ORIGINS = ['https://midiaflow.sstechnologies-cloud.com', 'http://localhost:3000']

def get_origin(event):
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]



s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'
def cors_headers():
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': get_origin(event),
        'Access-Control-Allow-Headers': 'Content-Type,Authorization,x-correlation-id',
        'Access-Control-Allow-Methods': 'POST,DELETE,OPTIONS'
    }

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': cors_headers(),
        'body': json.dumps(body)
    }

def lambda_handler(event, context):
    correlation_id = event.get('headers', {}).get('x-correlation-id', None)
    logger = Logger('folder-operations', correlation_id)
    
    method = event['httpMethod']
    
    if method == 'OPTIONS':
        return cors_response(200, {})
    
    body = json.loads(event.get('body', '{}'))
    logger.info("Folder operation request", method=method)
    
    token = event['headers'].get('Authorization', '').replace('Bearer ', '')
    try:
        payload = json.loads(base64.b64decode(token.split('.')[1] + '=='))
        user_id = payload['user_id']
        role = payload.get('role', 'user')
        logger.info("User authenticated", user_id=user_id, role=role)
    except Exception as e:
        logger.warn("Authentication failed", error=str(e))
        return cors_response(401, {'success': False, 'message': 'Unauthorized'})
    
    if method == 'POST':
        folder_path = body['folderPath'].strip('/')
        logger.info("Creating folder", path=folder_path, user_id=user_id)
        
        expected_prefix = f'users/{user_id}'
        if role != 'admin' and not folder_path.startswith(expected_prefix):
            logger.warn("Folder creation forbidden", path=folder_path, user_id=user_id)
            return cors_response(403, {'success': False, 'message': 'Forbidden'})
        
        s3.put_object(
            Bucket=BUCKET,
            Key=f'{folder_path}/.folder_placeholder',
            Body=b'',
            Metadata={'created_by': user_id, 'created_at': datetime.now().isoformat()}
        )
        
        logger.info("Folder created", path=folder_path)
        logger.metric("folder_created", 1)
        return cors_response(200, {'success': True, 'folder': folder_path})
    
    elif method == 'DELETE':
        folder_path = body['folderPath'].strip('/')
        logger.info("Deleting folder", path=folder_path, user_id=user_id)
        
        if role != 'admin' and not folder_path.startswith(f'users/{user_id}'):
            logger.warn("Folder deletion forbidden", path=folder_path, user_id=user_id)
            return cors_response(403, {'success': False, 'message': 'Forbidden'})
        
        response = s3.list_objects_v2(Bucket=BUCKET, Prefix=f'{folder_path}/')
        
        if 'Contents' in response and len(response['Contents']) > 1:
            logger.warn("Folder not empty", path=folder_path, files=len(response['Contents']))
            return cors_response(400, {'success': False, 'message': 'Folder not empty'})
        
        try:
            s3.delete_object(Bucket=BUCKET, Key=f'{folder_path}/.folder_placeholder')
        except:
            pass
        
        logger.info("Folder deleted", path=folder_path)
        logger.metric("folder_deleted", 1)
        return cors_response(200, {'success': True})
    
    return cors_response(405, {'success': False, 'message': 'Method Not Allowed'})
