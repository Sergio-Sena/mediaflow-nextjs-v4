import json
import boto3
import jwt
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

SECRET_KEY = os.environ.get('JWT_SECRET', 'your-secret-key')

def lambda_handler(event, context):
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
        return cors_response(500, {
            'success': False,
            'message': str(e)
        })

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
