import json
import boto3
import os
import jwt
from urllib.parse import unquote, unquote_plus

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('mediaflow-users')

UPLOADS_BUCKET = os.environ.get('UPLOADS_BUCKET', 'mediaflow-uploads-969430605054')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'mediaflow-processed-969430605054')
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key')

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
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
        if user_role != 'admin':
            # Usuários só podem acessar seus próprios arquivos
            if not key.startswith(f'users/{user_id}/'):
                return cors_response(403, {'success': False, 'message': 'Acesso negado'})
        
        # Try processed bucket first (optimized videos), then uploads
        bucket_to_use = UPLOADS_BUCKET
        
        # Check if optimized version exists in processed bucket
        try:
            # Look for converted version (with _1080p suffix)
            base_name = key.rsplit('.', 1)[0]
            converted_key = f"{base_name}_1080p.mp4"
            s3.head_object(Bucket=PROCESSED_BUCKET, Key=converted_key)
            bucket_to_use = PROCESSED_BUCKET
            key = converted_key
        except:
            # If no converted version, check original in processed bucket
            try:
                s3.head_object(Bucket=PROCESSED_BUCKET, Key=key)
                bucket_to_use = PROCESSED_BUCKET
            except:
                # Fall back to uploads bucket
                pass
        
        # Generate presigned URL
        view_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_to_use, 'Key': key},
            ExpiresIn=3600
        )
        
        return cors_response(200, {
            'success': True,
            'viewUrl': view_url,
            'user_id': user_id
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'success': False, 'message': str(e)})

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps(body)
    }