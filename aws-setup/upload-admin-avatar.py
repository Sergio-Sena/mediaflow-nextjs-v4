import boto3
import requests
import json

s3 = boto3.client('s3', region_name='us-east-1')

# Upload imagem para S3
bucket = 'mediaflow-uploads-969430605054'
key = 'avatars/avatar_admin.png'
file_path = '../Avatar/card administrador.png'

print(f"Uploading {file_path} to S3...")
s3.upload_file(file_path, bucket, key, ExtraArgs={'ContentType': 'image/png'})
print(f"Uploaded to s3://{bucket}/{key}")

avatar_url = f"https://{bucket}.s3.amazonaws.com/{key}"
print(f"Avatar URL: {avatar_url}")

# Chamar Lambda update-user
print("\nCalling Lambda update-user...")
response = requests.post(
    'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/update-user',
    json={
        'user_id': 'admin',
        'avatar_url': avatar_url
    }
)

print(f"Lambda response: {response.status_code}")
print(f"Response body: {response.json()}")

# Verificar DynamoDB
print("\nVerifying DynamoDB...")
response = requests.get('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users')
data = response.json()

if data['success']:
    admin_users = [u for u in data['users'] if u['user_id'] == 'admin']
    if admin_users:
        admin_user = admin_users[0]
        print(f"\nAdmin user data:")
        print(json.dumps(admin_user, indent=2))
        
        if admin_user.get('avatar_url') == avatar_url:
            print("\nLambda funcionou! Avatar salvo no DynamoDB")
        else:
            print(f"\nAvatar URL diferente:")
            print(f"  Expected: {avatar_url}")
            print(f"  Got: {admin_user.get('avatar_url', 'NOT SET')}")
    else:
        print("\nAdmin user not found in response")
