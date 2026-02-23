import boto3
import json

dynamodb = boto3.resource('dynamodb')

print("=" * 80)
print("ESTRUTURA DA TABELA DYNAMODB")
print("=" * 80)

# ETAPA 1: Informações da tabela
print("\n[1/2] Informacoes da tabela mediaflow-users...")
try:
    table = dynamodb.Table('mediaflow-users')
    
    print(f"Nome: {table.table_name}")
    print(f"Status: {table.table_status}")
    print(f"Item Count: {table.item_count}")
    print(f"Tamanho: {table.table_size_bytes / 1024:.2f} KB")
    
    print(f"\nChave Primaria:")
    for key in table.key_schema:
        print(f"  - {key['AttributeName']} ({key['KeyType']})")
    
    print(f"\nAtributos:")
    for attr in table.attribute_definitions:
        print(f"  - {attr['AttributeName']} ({attr['AttributeType']})")
    
except Exception as e:
    print(f"[ERRO] {e}")

# ETAPA 2: Listar todos os usuários com TODOS os campos
print("\n[2/2] Usuarios cadastrados (todos os campos)...")
try:
    table = dynamodb.Table('mediaflow-users')
    response = table.scan()
    users = response.get('Items', [])
    
    print(f"\n[OK] Total: {len(users)} usuarios\n")
    
    for i, user in enumerate(users, 1):
        print(f"\n--- Usuario {i} ---")
        for key, value in sorted(user.items()):
            # Não mostrar senha
            if 'password' in key.lower():
                print(f"  {key}: [OCULTO]")
            else:
                print(f"  {key}: {value}")
    
except Exception as e:
    print(f"[ERRO] {e}")

print("\n" + "=" * 80)
print("VERIFICACAO CONCLUIDA")
print("=" * 80)
