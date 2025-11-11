import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

# Atualizar sergio_sena para role 'user'
response = table.update_item(
    Key={'user_id': 'sergio_sena'},
    UpdateExpression='SET #role = :role',
    ExpressionAttributeNames={'#role': 'role'},
    ExpressionAttributeValues={':role': 'user'}
)

print("=" * 80)
print("SERGIO SENA ATUALIZADO")
print("=" * 80)
print("Role: media_owner -> user")
print()
print("Agora:")
print("  - Admin: Vê TUDO")
print("  - Sergio Sena: Vê apenas users/sergio_sena/")
print("  - Outros users: Veem apenas suas pastas")
print("=" * 80)
