import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

response = table.scan()
for user in response['Items']:
    if user.get('role') == 'admin':
        print(f"Admin encontrado: {user.get('user_id')} - {user.get('email')} - role: {user.get('role')}")
