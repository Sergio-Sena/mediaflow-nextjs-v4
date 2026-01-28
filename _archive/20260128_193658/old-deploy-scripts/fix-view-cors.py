import boto3

apigw = boto3.client('apigateway')
API_ID = 'gdb962d234'

# Buscar resource /view/{key+}
resources = apigw.get_resources(restApiId=API_ID, limit=500)
view_resource = None
for r in resources['items']:
    if r.get('pathPart') == '{key+}' and '/view' in r.get('path', ''):
        view_resource = r
        break

if not view_resource:
    print("Resource /view/{key+} não encontrado")
    exit(1)

resource_id = view_resource['id']
print(f"Resource ID: {resource_id}")

# Adicionar método OPTIONS
try:
    apigw.put_method(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    print("Método OPTIONS criado")
except:
    print("Método OPTIONS já existe")

# Configurar integração MOCK
apigw.put_integration(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)

# Response do método
try:
    apigw.put_method_response(
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
except:
    print("Method response já existe")

# Response da integração
apigw.put_integration_response(
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

# Deploy
apigw.create_deployment(restApiId=API_ID, stageName='prod')

print("CORS configurado e API deployada!")
