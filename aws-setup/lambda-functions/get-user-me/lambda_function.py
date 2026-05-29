import json
import boto3
import jwt
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('mediaflow-users')
secrets_client = boto3.client('secretsmanager', region_name='us-east-1')

def get_jwt_secret():
    try:
        response = secrets_client.get_secret_value(SecretId='midiaflow/jwt-secret')
        return response['SecretString']
    except Exception as e:
        print(f"Error fetching secret: {e}")
        raise Exception("Failed to retrieve JWT secret")

JWT_SECRET = get_jwt_secret()
_request_origin = None

def get_allowed_origin(event):
    allowed = os.environ.get('ALLOWED_ORIGINS', 'https://midiaflow.sstechnologies-cloud.com').split(',')
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in allowed else allowed[0]

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': _request_origin or 'https://midiaflow.sstechnologies-cloud.com',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps(body, default=str)
    }

def lambda_handler(event, context):
    global _request_origin
    _request_origin = get_allowed_origin(event)
    try:
        auth_header = event.get('headers', {}).get('Authorization') or event.get('headers', {}).get('authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return cors_response(401, {'success': False, 'message': 'Missing token'})
        
        token = auth_header.replace('Bearer ', '')
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_id = payload.get('user_id')
        except:
            return cors_response(401, {'success': False, 'message': 'Invalid token'})
        
        response = users_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return cors_response(404, {'success': False, 'message': 'User not found'})
        
        user = response['Item']
        user.pop('password', None)
        
        return cors_response(200, {'success': True, 'user': user})
        
    except Exception as e:
        print(f"Get user me error: {str(e)}")
        return cors_response(500, {'success': False, 'message': 'Internal server error'})
