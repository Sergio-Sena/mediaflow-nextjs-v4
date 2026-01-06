import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

response = table.scan()
users = response['Items']

print(f'Total de usuarios: {len(users)}\n')
print('=' * 100)

admin_password = None

for user in users:
    print(f"\nUser ID: {user['user_id']}")
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Role: {user['role']}")
    print(f"Status: {user.get('status', 'N/A')}")
    print(f"S3 Prefix: {user['s3_prefix']}")
    print(f"Password Hash: {user['password'][:20]}...")
    
    if user['user_id'] == 'user_admin':
        admin_password = user['password']
    
    # Verifica se s3_prefix esta correto
    if not user['s3_prefix'].startswith('users/'):
        print(f"  [!] PROBLEMA: s3_prefix deveria ser 'users/{user['user_id']}/'")
    
    print('-' * 100)

# Verifica se lid_lima tem mesma senha do admin
print('\n' + '=' * 100)
print('VERIFICACAO DE SENHAS:')
for user in users:
    if user['user_id'] == 'lid_lima':
        if user['password'] == admin_password:
            print(f"[!] ALERTA: lid_lima tem a MESMA senha do administrador!")
        else:
            print(f"[OK] lid_lima tem senha diferente do administrador")
