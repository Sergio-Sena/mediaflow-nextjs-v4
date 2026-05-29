import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

ALLOWED_ORIGINS = ['https://midiaflow.sstechnologies-cloud.com', 'http://localhost:3000']

_current_event = None

def get_origin():
    event = _current_event
    if not event:
        return ALLOWED_ORIGINS[0]
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]

def lambda_handler(event, context):
    global _current_event
    _current_event = event
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        user_id = event.get('pathParameters', {}).get('user_id')
        
        if not user_id:
            return cors_response(400, {'success': False, 'message': 'user_id obrigatório'})
        
        user = table.get_item(Key={'user_id': user_id})
        if 'Item' not in user:
            return cors_response(404, {'success': False, 'message': 'Usuário não encontrado'})
        
        table.delete_item(Key={'user_id': user_id})
        
        return cors_response(200, {'success': True, 'message': 'Usuário deletado'})
        
    except Exception as e:
        print(f"Delete user error: {str(e)}")
        return cors_response(500, {'success': False, 'message': 'Internal server error'})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': get_origin() if event else ALLOWED_ORIGINS[0],
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
