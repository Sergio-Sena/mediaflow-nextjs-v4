import boto3

apigateway = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')

API_ID = 'gdb962d234'
LAMBDA_ARN = 'arn:aws:lambda:us-east-1:969430605054:function:folder-operations'

# Get root resource
resources = apigateway.get_resources(restApiId=API_ID)
root_id = [r for r in resources['items'] if r['path'] == '/'][0]['id']

# Create /folders resource
try:
    folder_resource = apigateway.create_resource(
        restApiId=API_ID,
        parentId=root_id,
        pathPart='folders'
    )
    resource_id = folder_resource['id']
    print(f'Resource /folders criado: {resource_id}')
except Exception as e:
    # Get existing resource
    for r in resources['items']:
        if r['path'] == '/folders':
            resource_id = r['id']
            print(f'Resource /folders existente: {resource_id}')
            break

# Create POST method
try:
    apigateway.put_method(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='POST',
        authorizationType='NONE'
    )
    print('Metodo POST criado')
except Exception as e:
    print(f'Metodo POST: {e}')

# Create DELETE method
try:
    apigateway.put_method(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='DELETE',
        authorizationType='NONE'
    )
    print('Metodo DELETE criado')
except Exception as e:
    print(f'Metodo DELETE: {e}')

# Create OPTIONS method (CORS)
try:
    apigateway.put_method(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    print('Metodo OPTIONS criado')
except Exception as e:
    print(f'Metodo OPTIONS: {e}')

# Integrate POST with Lambda
try:
    apigateway.put_integration(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{LAMBDA_ARN}/invocations'
    )
    print('Integracao POST criada')
except Exception as e:
    print(f'Integracao POST: {e}')

# Integrate DELETE with Lambda
try:
    apigateway.put_integration(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='DELETE',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{LAMBDA_ARN}/invocations'
    )
    print('Integracao DELETE criada')
except Exception as e:
    print(f'Integracao DELETE: {e}')

# CORS OPTIONS integration
try:
    apigateway.put_integration(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        type='MOCK',
        requestTemplates={'application/json': '{"statusCode": 200}'}
    )
    apigateway.put_integration_response(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
            'method.response.header.Access-Control-Allow-Methods': "'POST,DELETE,OPTIONS'",
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        }
    )
    apigateway.put_method_response(
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
    print('CORS configurado')
except Exception as e:
    print(f'CORS: {e}')

# Add Lambda permission
try:
    lambda_client.add_permission(
        FunctionName='folder-operations',
        StatementId='apigateway-invoke-folders',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:us-east-1:969430605054:{API_ID}/*/POST/folders'
    )
    print('Permissao Lambda POST adicionada')
except Exception as e:
    print(f'Permissao POST: {e}')

try:
    lambda_client.add_permission(
        FunctionName='folder-operations',
        StatementId='apigateway-invoke-folders-delete',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:us-east-1:969430605054:{API_ID}/*/DELETE/folders'
    )
    print('Permissao Lambda DELETE adicionada')
except Exception as e:
    print(f'Permissao DELETE: {e}')

# Deploy to prod stage
try:
    apigateway.create_deployment(
        restApiId=API_ID,
        stageName='prod',
        description='Deploy folder-operations'
    )
    print('Deploy realizado')
except Exception as e:
    print(f'Deploy: {e}')

print('\nAPI Gateway configurado!')
print(f'Endpoint: https://{API_ID}.execute-api.us-east-1.amazonaws.com/prod/folders')
