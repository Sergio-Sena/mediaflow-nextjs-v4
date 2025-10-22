import json
import boto3
import base64
import pyotp
import hashlib
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('mediaflow-users')
BUCKET = 'mediaflow-uploads-969430605054'

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'OPTIONS':
            return cors_response(200, {})
        
        if event['httpMethod'] == 'POST':
            body = json.loads(event['body'])
            
            user_id = body.get('user_id')
            name = body.get('name')
            email = body.get('email')
            password = body.get('password')
            role = body.get('role', 'user')
            s3_prefix = body.get('s3_prefix', f"users/{user_id}/")
            avatar_base64 = body.get('avatar_image')
            
            if not user_id or not name or not email or not password:
                return cors_response(400, {
                    'success': False,
                    'message': 'user_id, name, email e password são obrigatórios'
                })
            
            # Verificar se usuário já existe
            existing = table.get_item(Key={'user_id': user_id})
            if 'Item' in existing:
                return cors_response(400, {
                    'success': False,
                    'message': 'Usuário já existe'
                })
            
            # Upload avatar para S3 se fornecido
            avatar_url = None
            if avatar_base64:
                try:
                    # Remover prefixo data:image/...;base64,
                    if ',' in avatar_base64:
                        avatar_base64 = avatar_base64.split(',')[1]
                    
                    image_data = base64.b64decode(avatar_base64)
                    avatar_key = f"avatars/{user_id}.jpg"
                    
                    s3.put_object(
                        Bucket=BUCKET,
                        Key=avatar_key,
                        Body=image_data,
                        ContentType='image/jpeg'
                    )
                    
                    avatar_url = f"https://{BUCKET}.s3.amazonaws.com/{avatar_key}"
                except Exception as e:
                    print(f"Error uploading avatar: {str(e)}")
            
            # Gerar TOTP secret
            totp_secret = pyotp.random_base32()
            
            # Hash da senha
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Criar usuário
            user = {
                'user_id': user_id,
                'name': name,
                'email': email,
                'password': password_hash,
                'role': role,
                's3_prefix': s3_prefix,
                'avatar_url': avatar_url,
                'totp_secret': totp_secret,
                'created_at': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=user)
            
            # Gerar QR Code URI para 2FA
            totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
                name=user_id,
                issuer_name='Mídiaflow'
            )
            
            return cors_response(200, {
                'success': True,
                'user': {
                    'user_id': user_id,
                    'name': name,
                    's3_prefix': s3_prefix,
                    'avatar_url': avatar_url,
                    'totp_uri': totp_uri
                }
            })
        
        elif event['httpMethod'] == 'DELETE':
            user_id = event['pathParameters']['user_id']
            
            # Buscar usuário para pegar avatar_url
            user = table.get_item(Key={'user_id': user_id})
            if 'Item' in user and user['Item'].get('avatar_url'):
                # Deletar avatar do S3
                try:
                    avatar_key = f"avatars/{user_id}.jpg"
                    s3.delete_object(Bucket=BUCKET, Key=avatar_key)
                except:
                    pass
            
            # Deletar usuário do DynamoDB
            table.delete_item(Key={'user_id': user_id})
            
            return cors_response(200, {
                'success': True,
                'message': 'Usuário deletado'
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
            'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
