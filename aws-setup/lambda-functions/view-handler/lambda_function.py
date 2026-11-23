import json
import boto3
import os
import jwt
from urllib.parse import unquote, unquote_plus
from boto3.dynamodb.conditions import Attr

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('mediaflow-users')
public_table = dynamodb.Table('mediaflow-public-content')

UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')
CDN_DOMAIN = os.environ.get('CDN_DOMAIN', 'midiaflow.sstechnologies-cloud.com')
JWT_SECRET = os.environ['JWT_SECRET']
_request_origin = None

def get_allowed_origin(event):
    allowed = os.environ.get('ALLOWED_ORIGINS', 'https://midiaflow.sstechnologies-cloud.com').split(',')
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in allowed else allowed[0]

def lambda_handler(event, context):
    global _request_origin
    _request_origin = get_allowed_origin(event)
    print(f"Event method: {event.get('httpMethod')}")
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        # Verificar autenticação
        headers = event.get('headers', {})
        # API Gateway pode enviar headers em lowercase
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            print(f"Auth header missing or invalid: {auth_header}")
            return cors_response(401, {'success': False, 'message': 'Token de acesso necessário'})
        
        token = auth_header.replace('Bearer ', '')
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user_role = payload.get('role', 'user')
        except jwt.InvalidTokenError as e:
            print(f"JWT decode error: {str(e)}")
            return cors_response(401, {'success': False, 'message': 'Token inválido'})
        
        # Decodificar key com tratamento para caracteres especiais
        raw_key = event['pathParameters']['key']
        # Tentar unquote_plus primeiro (trata + como espaço)
        key = unquote_plus(raw_key)
        print(f"Raw key: {raw_key}")
        print(f"Decoded key: {key}")
        
        # Verificar permissões
        if user_role != 'admin' and not key.startswith(f'users/{user_id}/'):
            resp = public_table.scan(
                FilterExpression=Attr('file_key').eq(key) & Attr('is_active').eq(True)
            )
            if not resp.get('Items'):
                return cors_response(403, {'success': False, 'message': 'Acesso negado'})

        # URL via CloudFront CDN (cache + performance)
        view_url = f'https://{CDN_DOMAIN}/media/{key}'
        
        return cors_response(200, {
            'success': True,
            'viewUrl': view_url,
            'user_id': user_id
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'success': False, 'message': 'Internal server error'})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': _request_origin or 'https://midiaflow.sstechnologies-cloud.com',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps(body)
    }