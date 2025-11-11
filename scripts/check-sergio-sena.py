import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mediaflow-users')

response = table.get_item(Key={'user_id': 'sergio_sena'})

if 'Item' in response:
    user = response['Item']
    print("="*80)
    print("SERGIO SENA - DADOS ATUAIS")
    print("="*80)
    print(json.dumps(user, indent=2, default=str))
else:
    print("Usuario nao encontrado!")
