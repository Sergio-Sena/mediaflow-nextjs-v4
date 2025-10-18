import json
import jwt
import pyotp
import boto3
from datetime import datetime, timedelta

SECRET_KEY = 'your-secret-key-here-change-in-production'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mediaflow-users')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        body = json.loads(event['body'])
        user_id = body.get('user_id')
        code = body.get('code')
        
        if not user_id or not code:
            return cors_response(400, {
                'success': False,
                'message': 'user_id and code required'
            })
        
        # Buscar usuário no DynamoDB
        response = table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return cors_response(404, {
                'success': False,
                'message': 'User not found'
            })
        
        user = response['Item']
        
        # Validar TOTP (Google Authenticator)
        totp = pyotp.TOTP(user['totp_secret'])
        if not totp.verify(code, valid_window=1):
            return cors_response(401, {
                'success': False,
                'message': 'Invalid 2FA code'
            })
        
        # Gerar JWT com informações do usuário
        token = jwt.encode({
            'user_id': user_id,
            'user_name': user['name'],
            's3_prefix': user.get('s3_prefix', ''),
            'role': user.get('role', 'user'),
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')
        
        return cors_response(200, {
            'success': True,
            'token': token,
            'user': {
                'id': user_id,
                'name': user['name'],
                'avatar': user.get('avatar', '👤')
            }
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
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
