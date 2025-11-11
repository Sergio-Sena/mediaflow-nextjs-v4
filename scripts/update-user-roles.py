import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

# Atualizar Sergio Sena para media_owner
print("Atualizando Sergio Sena para media_owner...")
table.update_item(
    Key={'user_id': 'sergio_sena'},
    UpdateExpression='SET #role = :role',
    ExpressionAttributeNames={'#role': 'role'},
    ExpressionAttributeValues={':role': 'media_owner'}
)
print("OK - sergio_sena agora e media_owner")

# Admin continua admin (sem mudanças)
print("\nOK - user_admin continua como admin")

print("\n=== Roles Atualizados ===")
print("sergiosena@sstech.com -> media_owner (ve todas as midias)")
print("sergiosenaadmin@sstech -> admin (tarefas administrativas apenas)")
print("\nCusto: $0.00")
print("Tempo: Instantaneo")
