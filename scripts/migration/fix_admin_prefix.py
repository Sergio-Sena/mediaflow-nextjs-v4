import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

# Adicionar s3_prefix para admin_sistema
table.update_item(
    Key={'user_id': 'admin_sistema'},
    UpdateExpression='SET s3_prefix = :prefix',
    ExpressionAttributeValues={':prefix': 'admin/'}
)

print("admin_sistema agora tem s3_prefix: admin/")
