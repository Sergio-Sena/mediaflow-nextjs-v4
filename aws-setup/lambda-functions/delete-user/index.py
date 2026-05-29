import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')
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
            'Access-Control-Allow-Origin': _request_origin or 'https://midiaflow.sstechnologies-cloud.com',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
