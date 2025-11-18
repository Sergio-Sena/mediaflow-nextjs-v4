import boto3

client = boto3.client('apigateway', region_name='us-east-1')
API_ID = 'gdb962d234'

resources = client.get_resources(restApiId=API_ID)

view_resource = None
for resource in resources['items']:
    if resource.get('path') == '/view/{key+}':
        view_resource = resource
        break

if not view_resource:
    print("[ERRO] Resource nao encontrado")
    exit(1)

resource_id = view_resource['id']

# Update OPTIONS integration response to allow localhost
client.put_integration_response(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
        'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)

client.create_deployment(
    restApiId=API_ID,
    stageName='prod',
    description='Allow localhost CORS'
)
print("[OK] CORS atualizado para permitir localhost")
