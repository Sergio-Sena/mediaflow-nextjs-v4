import requests
import json

API_URL = 'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod'

# Login lid_lima
response = requests.post(f'{API_URL}/auth', json={
    'email': 'lidlima@sstech.com',
    'password': 'Ss@123456'
})

print('Status:', response.status_code)
data = response.json()
print(json.dumps(data, indent=2))

if data.get('success'):
    token = data['token']
    print(f'\nToken gerado com sucesso!')
    print(f'User ID: {data["user"]["user_id"]}')
    print(f'S3 Prefix: {data["user"]["s3_prefix"]}')
