import requests
import json

# Exemplo: Criar novo usuario "Maria"
new_user = {
    'user_id': 'Maria',
    'name': 'Maria Silva',
    'email': 'maria@sstech',
    'password': 'maria123',
    's3_prefix': 'Maria/'
}

print("=== CRIANDO NOVO USUARIO ===\n")

# 1. Criar usuario via Lambda
response = requests.post(
    'https://gdb962d234.execute-api.us-east-1.amazonaws.com/prod/users/create',
    json=new_user
)

print(f"Status: {response.status_code}")
result = response.json()
print(f"Response: {json.dumps(result, indent=2)}")

if result.get('success'):
    print(f"\n✓ Usuario criado!")
    print(f"  User ID: {new_user['user_id']}")
    print(f"  Email: {new_user['email']}")
    print(f"  Senha: {new_user['password']}")
    print(f"  QR Code: {result.get('qr_code_url')}")
    print(f"\n2. Proximo passo: Fazer upload do avatar em /users")
    print(f"3. Avatar sera salvo em: avatars/avatar_Maria.ext")
    print(f"4. Lambda update-user atualizara DynamoDB automaticamente")
else:
    print(f"\n✗ Erro: {result.get('error')}")
