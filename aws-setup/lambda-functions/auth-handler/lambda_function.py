import json
import hashlib
import hmac
import base64
import boto3
from datetime import datetime, timedelta

JWT_SECRET = "17b8312c72fdcffbff89f2f4a564fb26e936002d344717ab7753a237fcd57aea"

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
        print(f"Event: {json.dumps(event)}")
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        password = body.get('password')
        print(f"Login attempt: email={email}")
        
        # Check DynamoDB users
        print("Scanning DynamoDB table...")
        response = table.scan()
        users = response.get('Items', [])
        print(f"Found {len(users)} users")
        
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
        print(f"Error in lambda_handler: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
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