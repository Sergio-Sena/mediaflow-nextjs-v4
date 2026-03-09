import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

# Corrigir user_admin
table.update_item(
    Key={'user_id': 'user_admin'},
    UpdateExpression='SET s3_prefix = :prefix',
    ExpressionAttributeValues={':prefix': 'users/user_admin/'}
)
print('[OK] user_admin corrigido: s3_prefix = users/user_admin/')

# Corrigir lid_lima
table.update_item(
    Key={'user_id': 'lid_lima'},
    UpdateExpression='SET s3_prefix = :prefix',
    ExpressionAttributeValues={':prefix': 'users/lid_lima/'}
)
print('[OK] lid_lima corrigido: s3_prefix = users/lid_lima/')

print('\nCorrecoes concluidas!')
