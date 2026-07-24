import json
import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('mediaflow-users')
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
        # Suportar GET /users/{user_id}
        user_id = event.get('pathParameters', {}).get('user_id') or event.get('pathParameters', {}).get('userId')
        
        if not user_id:
            return cors_response(400, {'success': False, 'message': 'userId required'})
        
        response = users_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return cors_response(404, {'success': False, 'message': 'User not found'})
        
        user = response['Item']
        user.pop('password', None)
        
        return cors_response(200, {'success': True, 'user': user})
        
    except Exception as e:
        print(f"Get user error: {str(e)}")
        return cors_response(500, {'success': False, 'message': 'Internal server error'})

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
