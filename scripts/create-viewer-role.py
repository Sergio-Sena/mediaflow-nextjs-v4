import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

# Atualizar sergio_sena para role 'viewer'
response = table.update_item(
    Key={'user_id': 'sergio_sena'},
    UpdateExpression='SET #role = :role, s3_prefix = :prefix',
    ExpressionAttributeNames={'#role': 'role'},
    ExpressionAttributeValues={
        ':role': 'viewer',
        ':prefix': 'users/user_admin/'
    }
)

print("="*80)
print("SERGIO SENA ATUALIZADO PARA VIEWER")
print("="*80)
print("Role: user -> viewer")
print("S3 Prefix: users/user_admin/")
print()
print("Permissoes:")
print("  - Ve apenas midias de user_admin")
print("  - NAO ve outros usuarios")
print("  - NAO tem acesso ao painel admin")
print("="*80)
