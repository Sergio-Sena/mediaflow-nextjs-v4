import boto3
import hashlib
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

# Dados do usuário teste
username = 'user_teste'
email = 'teste@example.com'
password = 'teste123'

# Hash da senha
password_hash = hashlib.sha256(password.encode()).hexdigest()

# Criar usuário
table.put_item(Item={
    'user_id': username,
    'username': username,
    'email': email,
    'password': password_hash,
    'role': 'user',
    's3_prefix': f'users/{username}/',
    'created_at': datetime.now().isoformat(),
    'requires_2fa': False
})

print(f"✅ Usuário criado: {username}")
print(f"📧 Email: {email}")
print(f"🔑 Senha: {password}")
print(f"📁 S3 Prefix: users/{username}/")
