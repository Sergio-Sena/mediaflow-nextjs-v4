import json
import boto3
import jwt
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('mediaflow-users')
secrets_client = boto3.client('secretsmanager', region_name='us-east-1')

def get_jwt_secret():
    try:
        response = secrets_client.get_secret_value(SecretId='midiaflow/jwt-secret')
        return response['SecretString']
    except Exception as e:
        print(f"Error fetching secret: {e}")
        raise Exception("Failed to retrieve JWT secret")

JWT_SECRET = get_jwt_secret()

def lambda_handler(event, context):
    try:
        auth_header = event.get('headers', {}).get('Authorization') or event.get('headers', {}).get('authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'success': False, 'message': 'Missing token'})
            }
        
        token = auth_header.replace('Bearer ', '')
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_id = payload.get('user_id')
        except:
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'success': False, 'message': 'Invalid token'})
            }
        
        response = users_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'success': False, 'message': 'User not found'})
            }
        
        user = response['Item']
        user.pop('password', None)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': True, 'user': user}, default=str)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': False, 'message': str(e)})
        }
