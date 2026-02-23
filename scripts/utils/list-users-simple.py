import boto3
import json

dynamodb = boto3.resource('dynamodb')

print("=" * 80)
print("ESTRUTURA DA TABELA DYNAMODB")
print("=" * 80)

# Listar todos os usuarios
print("\nUsuarios cadastrados...")
try:
    table = dynamodb.Table('mediaflow-users')
    response = table.scan()
    users = response.get('Items', [])
    
    print(f"\nTotal: {len(users)} usuarios\n")
    
    for i, user in enumerate(users, 1):
        print(f"\n--- Usuario {i} ---")
        print(f"  user_id: {user.get('user_id', 'N/A')}")
        print(f"  email: {user.get('email', 'N/A')}")
        print(f"  name: {user.get('name', 'N/A')}")
        print(f"  role: {user.get('role', 'N/A')}")
        print(f"  status: {user.get('status', 'N/A')}")
        print(f"  s3_prefix: {user.get('s3_prefix', 'N/A')}")
        print(f"  created_at: {user.get('created_at', 'N/A')}")
    
except Exception as e:
    print(f"[ERRO] {e}")

print("\n" + "=" * 80)
