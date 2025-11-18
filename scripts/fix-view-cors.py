import boto3

client = boto3.client('apigateway', region_name='us-east-1')
API_ID = 'gdb962d234'

# Get resources
resources = client.get_resources(restApiId=API_ID)

# Find /view/{key} resource
view_resource = None
for resource in resources['items']:
    if resource.get('path') == '/view/{key}':
        view_resource = resource
        break

if not view_resource:
    print("[ERRO] Resource /view/{key} nao encontrado")
    exit(1)

resource_id = view_resource['id']
print(f"[OK] Resource encontrado: {view_resource['path']} (ID: {resource_id})")

# Add OPTIONS method
try:
    client.put_method(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    print("[OK] Metodo OPTIONS criado")
except client.exceptions.ConflictException:
    print("[INFO] Metodo OPTIONS ja existe")

# Add OPTIONS integration
client.put_integration(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)
print("[OK] Integration OPTIONS configurada")

# Add OPTIONS method response
client.put_method_response(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Methods': True,
        'method.response.header.Access-Control-Allow-Origin': True
    }
)
print("[OK] Method response OPTIONS configurada")

# Add OPTIONS integration response
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
print("[OK] Integration response OPTIONS configurada")

# Update GET method response
try:
    client.put_method_response(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='GET',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
    print("[OK] Method response GET atualizada")
except:
    pass

# Deploy
client.create_deployment(
    restApiId=API_ID,
    stageName='prod',
    description='Fix CORS for /view endpoint'
)
print("[OK] Deploy realizado!")
print("\n[SUCESSO] CORS configurado com sucesso!")
