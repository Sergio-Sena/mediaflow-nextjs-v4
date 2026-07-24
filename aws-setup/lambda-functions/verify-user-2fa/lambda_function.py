import json
import jwt
import pyotp
import boto3
import os
from datetime import datetime, timedelta

JWT_SECRET = os.environ['JWT_SECRET']
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
        
        body = json.loads(event['body'])
        user_id = body.get('user_id')
        code = body.get('code')
        
        if not user_id or not code:
            return cors_response(400, {
                'success': False,
                'message': 'user_id and code required'
            })
        
        response = table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return cors_response(404, {
                'success': False,
                'message': 'User not found'
            })
        
        user = response['Item']
        
        totp = pyotp.TOTP(user['totp_secret'])
        if not totp.verify(code, valid_window=1):
            return cors_response(401, {
                'success': False,
                'message': 'Invalid 2FA code'
            })
        
        token = jwt.encode({
            'user_id': user_id,
            'user_name': user['name'],
            's3_prefix': user.get('s3_prefix', ''),
            'role': user.get('role', 'user'),
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, JWT_SECRET, algorithm='HS256')
        
        return cors_response(200, {
            'success': True,
            'token': token,
            'user': {
                'id': user_id,
                'name': user['name'],
                'avatar': user.get('avatar', '')
            }
        })
        
    except Exception as e:
        print(f"Verify 2FA error: {str(e)}")
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
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
