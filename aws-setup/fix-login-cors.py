import boto3

client = boto3.client('apigateway', region_name='us-east-1')
api_id = 'gdb962d234'

# Encontrar resource /auth/login
resources = client.get_resources(restApiId=api_id)
auth_resource = None
for resource in resources['items']:
    if resource['path'] == '/auth/login':
        auth_resource = resource
        break

if not auth_resource:
    print("[ERRO] Resource /auth/login nao encontrado")
    exit(1)

resource_id = auth_resource['id']
print(f"[OK] Resource encontrado: {resource_id}")

# Adicionar método OPTIONS se não existir
try:
    client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    print("[OK] Metodo OPTIONS criado")
except:
    print("[AVISO] Metodo OPTIONS ja existe")

# Configurar integração MOCK para OPTIONS
client.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)

# Configurar response OPTIONS
try:
    client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': True,
            'method.response.header.Access-Control-Allow-Methods': True,
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
except:
    print("[AVISO] Method response OPTIONS ja existe")

try:
    client.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
            'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        }
    )
except:
    print("[AVISO] Integration response OPTIONS ja existe")

# Configurar CORS no método POST
try:
    client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
except:
    print("[AVISO] Method response POST ja existe")

# Deploy
client.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='Fix CORS login'
)

print("[OK] CORS configurado e API deployada")
