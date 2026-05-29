import json
import boto3
import jwt
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

SECRET_KEY = os.environ['JWT_SECRET']
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
        
        # Validar JWT
        auth_header = event.get('headers', {}).get('Authorization', '') or \
                      event.get('headers', {}).get('authorization', '')
        
        if not auth_header:
            return cors_response(401, {'success': False, 'message': 'Unauthorized'})
        
        try:
            token = auth_header.replace('Bearer ', '').strip()
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_role = decoded.get('role', 'user')
            
            # Apenas admin pode listar usuários
            if user_role != 'admin':
                return cors_response(403, {'success': False, 'message': 'Forbidden: Admin only'})
        except jwt.ExpiredSignatureError:
            return cors_response(401, {'success': False, 'message': 'Token expired'})
        except jwt.InvalidTokenError:
            return cors_response(401, {'success': False, 'message': 'Invalid token'})
        
        # Listar todos os usuários
        response = table.scan()
        users = response['Items']
        
        # Remover secrets da resposta (segurança)
        for user in users:
            user.pop('totp_secret', None)
            user.pop('password', None)
        
        return cors_response(200, {
            'success': True,
            'users': users
        })
        
    except Exception as e:
        print(f"List users error: {str(e)}")
        return cors_response(500, {
            'success': False,
            'message': 'Internal server error'
        })

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': _request_origin or 'https://midiaflow.sstechnologies-cloud.com',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
