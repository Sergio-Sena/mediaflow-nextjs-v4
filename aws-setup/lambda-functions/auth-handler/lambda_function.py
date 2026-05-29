import json
import hashlib
import hmac
import base64
import boto3
import os
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

JWT_SECRET = os.environ['JWT_SECRET']

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_jwt(payload, secret):
    """Simple JWT creation without external libraries"""
    header = {"alg": "HS256", "typ": "JWT"}
    
    # Encode header and payload
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    
    # Create signature
    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{message}.{signature_encoded}"

def lambda_handler(event, context):
    try:
        print(f"Login request received: {event['httpMethod']}")
        
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {}, event)
        
        body = json.loads(event.get('body', '{}'))
        email = body.get('email', '').strip().lower()
        password = body.get('password', '')
        
        if not email or not password:
            return cors_response(400, {'success': False, 'error': 'Email e senha são obrigatórios'}, event)
        
        # Query by email instead of scan
        response = table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        users = response.get('Items', [])
        
        for user in users:
            if user.get('email') == email and user.get('password') == hash_password(password):
                status = user.get('status', 'approved')
                if status == 'pending':
                    print(f"Login blocked - pending: {email}")
                    return cors_response(403, {'success': False, 'error': 'Conta aguardando aprovação do administrador'}, event)
                if status == 'rejected':
                    print(f"Login blocked - rejected: {email}")
                    return cors_response(403, {'success': False, 'error': 'Conta rejeitada pelo administrador'}, event)
                
                s3_prefix = user.get('s3_prefix', '')
                role = user.get('role', 'user')
                payload = {
                    'email': email,
                    'user_id': user['user_id'],
                    's3_prefix': s3_prefix,
                    'role': role,
                    'exp': int((datetime.utcnow() + timedelta(hours=24)).timestamp())
                }
                token = create_jwt(payload, JWT_SECRET)
                print(f"Login successful: {email}, role: {role}, user_id: {user['user_id']}")
                return cors_response(200, {
                    'success': True,
                    'token': token,
                    'user_id': user['user_id'],
                    'user': {
                        'user_id': user['user_id'],
                        'email': email,
                        'name': user.get('name', email),
                        'role': role,
                        's3_prefix': s3_prefix,
                        'avatar_url': user.get('avatar_url', '')
                    }
                }, event)
        
        print(f"Login failed - invalid credentials: {email}")
        return cors_response(401, {'success': False, 'error': 'Invalid credentials'}, event)
            
    except Exception as e:
        print(f"Lambda error: {str(e)}")
        return cors_response(500, {'success': False, 'message': 'Internal server error'}, event)

ALLOWED_ORIGINS = ['https://midiaflow.sstechnologies-cloud.com', 'http://localhost:3000']

def get_origin(event=None):
    if not event:
        return ALLOWED_ORIGINS[0]
    headers = event.get('headers') or {}
    origin = headers.get('origin') or headers.get('Origin') or ''
    return origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]

def cors_response(status_code, body, event=None):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': get_origin(event) if event else ALLOWED_ORIGINS[0],
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': json.dumps(body)
    }