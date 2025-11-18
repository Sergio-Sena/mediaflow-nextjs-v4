import boto3

client = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')

API_ID = 'gdb962d234'
LAMBDA_ARN = 'arn:aws:lambda:us-east-1:969430605054:function:mediaflow-view-handler'

# Get /view/{key+} resource
resources = client.get_resources(restApiId=API_ID)
view_resource = None

for resource in resources['items']:
    if resource.get('path') == '/view/{key+}':
        view_resource = resource
        break

if not view_resource:
    print("[ERRO] Resource /view/{key+} nao encontrado")
    exit(1)

resource_id = view_resource['id']
print(f"[OK] Resource encontrado: {view_resource['path']} (ID: {resource_id})")

# Update GET integration to point to correct Lambda
client.put_integration(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{LAMBDA_ARN}/invocations'
)
print("[OK] Integration GET atualizada para mediaflow-view-handler")

# Add Lambda permission
try:
    lambda_client.add_permission(
        FunctionName='mediaflow-view-handler',
        StatementId='apigateway-view-invoke',
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
    description='Fix Lambda integration for view endpoint'
)
print("[OK] Deploy realizado!")
print("\n[SUCESSO] API Gateway agora aponta para mediaflow-view-handler!")
