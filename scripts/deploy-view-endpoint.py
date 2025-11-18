import boto3

client = boto3.client('apigateway', region_name='us-east-1')
API_ID = 'gdb962d234'

client.create_deployment(
    restApiId=API_ID,
    stageName='prod',
    description='Deploy view endpoint with greedy path'
)
print("[OK] Deploy realizado!")
