import boto3

client = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')

API_ID = 'gdb962d234'
LAMBDA_ARN = 'arn:aws:lambda:us-east-1:969430605054:function:view-handler'

# Get resources
resources = client.get_resources(restApiId=API_ID)

# Find /view and /view/{key}
view_resource = None
old_key_resource = None

for resource in resources['items']:
    if resource.get('path') == '/view':
        view_resource = resource
    elif resource.get('path') == '/view/{key}':
        old_key_resource = resource

if not view_resource:
    print("[ERRO] Resource /view nao encontrado")
    exit(1)

print(f"[OK] Resource /view encontrado (ID: {view_resource['id']})")

# Delete old {key} resource if exists
if old_key_resource:
    client.delete_resource(
        restApiId=API_ID,
        resourceId=old_key_resource['id']
    )
    print(f"[OK] Resource /view/{{key}} deletado")

# Create {key+} resource
greedy_resource = client.create_resource(
    restApiId=API_ID,
    parentId=view_resource['id'],
    pathPart='{key+}'
)
print(f"[OK] Resource /view/{{key+}} criado (ID: {greedy_resource['id']})")

resource_id = greedy_resource['id']

# Add GET method
client.put_method(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)
print("[OK] Metodo GET criado")

# Add GET integration
client.put_integration(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{LAMBDA_ARN}/invocations'
)
print("[OK] Integration GET configurada")

# Add OPTIONS method
client.put_method(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)
print("[OK] Metodo OPTIONS criado")

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

# Add Lambda permission
try:
    lambda_client.add_permission(
        FunctionName='view-handler',
        StatementId='apigateway-view-greedy',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:us-east-1:969430605054:{API_ID}/*/GET/view/*'
    )
    print("[OK] Permissao Lambda adicionada")
except lambda_client.exceptions.ResourceConflictException:
    print("[INFO] Permissao Lambda ja existe")

# Deploy
client.create_deployment(
    restApiId=API_ID,
    stageName='prod',
    description='Replace {key} with {key+} for /view endpoint'
)
print("[OK] Deploy realizado!")
print("\n[SUCESSO] Endpoint /view/{key+} configurado!")
