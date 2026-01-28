import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

response = table.scan()
for user in response['Items']:
    user_id = user.get('user_id')
    role = user.get('role')
    s3_prefix = user.get('s3_prefix', 'N/A')
    email = user.get('email', 'N/A')
    print(f"{user_id:20} | role: {role:10} | s3_prefix: {s3_prefix:30} | email: {email}")
