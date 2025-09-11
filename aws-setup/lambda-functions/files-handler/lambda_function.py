import json
import boto3
import os
from urllib.parse import unquote

s3 = boto3.client('s3')
UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')

def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        path = event.get('path', '')
        
        if method == 'OPTIONS':
            return cors_response(200, {})
        elif method == 'GET':
            return list_files()
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

def list_files():
    files = []
    
    for bucket, bucket_type in [(UPLOADS_BUCKET, 'uploads'), (PROCESSED_BUCKET, 'processed')]:
        try:
            response = s3.list_objects_v2(Bucket=bucket)
            for obj in response.get('Contents', []):
                # Preserve full path structure
                key = obj['Key']
                
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