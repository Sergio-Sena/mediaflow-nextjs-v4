import json
import boto3
import os

ALLOWED_ORIGINS = ['https://midiaflow.sstechnologies-cloud.com', 'http://localhost:3000']

_current_event = None

def get_origin():
    event = _current_event
    if not event:
        return ALLOWED_ORIGINS[0]
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]



dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('mediaflow-users')

def lambda_handler(event, context):
    global _current_event
    _current_event = event
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
            'Access-Control-Allow-Origin': get_origin(),
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps(body, default=str)
    }
