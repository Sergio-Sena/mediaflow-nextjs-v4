import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

# Buscar avatar do user_admin
response = table.get_item(Key={'user_id': 'user_admin'})
old_avatar = response['Item'].get('avatar_url', '')

print(f"Avatar do user_admin: {old_avatar}")

# Atualizar admin_sistema com mesmo avatar
table.update_item(
    Key={'user_id': 'admin_sistema'},
    UpdateExpression='SET avatar_url = :avatar',
    ExpressionAttributeValues={':avatar': old_avatar}
)

print(f"Avatar copiado para admin_sistema: {old_avatar}")
