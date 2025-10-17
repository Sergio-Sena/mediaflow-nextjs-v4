import json
import hashlib
import hmac
import base64
import boto3
from datetime import datetime, timedelta

JWT_SECRET = "mediaflow_super_secret_key_2025"

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

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
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        password = body.get('password')
        
        # Check DynamoDB users
        response = table.scan()
        users = response.get('Items', [])
        
        for user in users:
            if user.get('email') == email and user.get('password') == hash_password(password):
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
                return cors_response(200, {
                    'success': True,
                    'token': token,
                    'user_id': user['user_id'],
                    'user': {
                        'email': email,
                        'name': user.get('name', email),
                        'role': role
                    }
                })
        
        return cors_response(401, {'success': False, 'error': 'Invalid credentials'})
            
    except Exception as e:
        return cors_response(500, {'success': False, 'message': str(e)})

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