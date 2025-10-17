import boto3
import requests
import json

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'mediaflow-uploads-969430605054'

print("=== SINCRONIZANDO AVATARES ===\n")

# 1. Listar avatares no S3
s3_avatars = {}
response = s3.list_objects_v2(Bucket=bucket, Prefix='avatars/')
if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        user_id = key.replace('avatars/avatar_', '').rsplit('.', 1)[0]
        s3_avatars[user_id] = f"https://{bucket}.s3.amazonaws.com/{key}"
        print(f"S3: {user_id} -> {key}")

print(f"\nTotal S3: {len(s3_avatars)}")

# 2. Listar usuários no DynamoDB
response = requests.get('https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users')
users = response.json()['users']

print(f"\n=== CORRIGINDO DYNAMODB ===\n")

for user in users:
    user_id = user['user_id']
    db_avatar = user.get('avatar_url')
    s3_avatar = s3_avatars.get(user_id)
    
    if db_avatar != s3_avatar:
        print(f"\n{user_id}:")
        print(f"  DynamoDB: {db_avatar}")
        print(f"  S3:       {s3_avatar}")
        
        if s3_avatar:
            # Atualizar DynamoDB
            update_res = requests.post(
                'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/update-user',
                json={'user_id': user_id, 'avatar_url': s3_avatar}
            )
            if update_res.json().get('success'):
                print(f"  ✓ Atualizado!")
            else:
                print(f"  ✗ Erro ao atualizar")
        else:
            print(f"  ! Sem avatar no S3")

print("\n=== SINCRONIZAÇÃO COMPLETA ===")
