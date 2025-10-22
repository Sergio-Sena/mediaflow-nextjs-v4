import boto3
import json
import base64
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = 'mediaflow-uploads-969430605054'

def lambda_handler(event, context):
    method = event['httpMethod']
    body = json.loads(event.get('body', '{}'))
    
    print(f"Method: {method}, Body: {body}")
    
    # Extract user_id from JWT
    token = event['headers'].get('Authorization', '').replace('Bearer ', '')
    try:
        payload = json.loads(base64.b64decode(token.split('.')[1] + '=='))
        user_id = payload['user_id']
        role = payload.get('role', 'user')
        print(f"User: {user_id}, Role: {role}")
    except:
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'success': False, 'message': 'Unauthorized'})
        }
    
    if method == 'POST':
        folder_path = body['folderPath'].strip('/')
        print(f"Creating folder: {folder_path}")
        
        # Validate permission
        expected_prefix = f'users/{user_id}'
        print(f"Checking: {folder_path} starts with {expected_prefix}? {folder_path.startswith(expected_prefix)}")
        
        if role != 'admin' and not folder_path.startswith(expected_prefix):
            return {
                'statusCode': 403,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'success': False, 'message': 'Forbidden'})
            }
        
        # Create placeholder
        s3.put_object(
            Bucket=BUCKET,
            Key=f'{folder_path}/.folder_placeholder',
            Body=b'',
            Metadata={'created_by': user_id, 'created_at': datetime.now().isoformat()}
        )
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'success': True, 'folder': folder_path})
        }
    
    elif method == 'DELETE':
        folder_path = body['folderPath'].strip('/')
        
        # Validate permission
        if role != 'admin' and not folder_path.startswith(f'users/{user_id}'):
            return {
                'statusCode': 403,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'success': False, 'message': 'Forbidden'})
            }
        
        # List objects in folder
        response = s3.list_objects_v2(Bucket=BUCKET, Prefix=f'{folder_path}/')
        
        # Only delete if empty (safety)
        if 'Contents' in response and len(response['Contents']) > 1:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'success': False, 'message': 'Folder not empty'})
            }
        
        # Delete placeholder
        try:
            s3.delete_object(Bucket=BUCKET, Key=f'{folder_path}/.folder_placeholder')
        except:
            pass
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'success': True})
        }
    
    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'success': False, 'message': 'Method Not Allowed'})
    }
