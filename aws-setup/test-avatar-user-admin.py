import boto3
import requests
import json

s3 = boto3.client('s3', region_name='us-east-1')

# Upload para user_admin
bucket = 'mediaflow-uploads-969430605054'
key = 'avatars/avatar_user_admin.png'
file_path = '../Avatar/card administrador.png'

print(f"Uploading {file_path} to S3...")
s3.upload_file(file_path, bucket, key, ExtraArgs={'ContentType': 'image/png'})
print(f"Uploaded: s3://{bucket}/{key}")

avatar_url = f"https://{bucket}.s3.amazonaws.com/{key}"
print(f"Avatar URL: {avatar_url}")

# Atualizar DynamoDB
print("\nUpdating DynamoDB...")
response = requests.post(
    'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/update-user',
    json={
        'user_id': 'user_admin',
        'avatar_url': avatar_url
    }
)

print(f"Lambda response: {response.status_code}")
print(f"Body: {response.json()}")

# Verificar
print("\nVerifying...")
response = requests.get('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users')
data = response.json()

user_admin = [u for u in data['users'] if u['user_id'] == 'user_admin'][0]
print(f"\nuser_admin data:")
print(json.dumps(user_admin, indent=2))

if user_admin.get('avatar_url') == avatar_url:
    print("\n✓ Avatar salvo com sucesso!")
else:
    print(f"\n✗ Erro: avatar_url = {user_admin.get('avatar_url')}")
