import boto3

apigateway = boto3.client('apigateway', region_name='us-east-1')

API_ID = 'gdb962d234'
RESOURCE_ID = 'tgsaw4'  # /folders resource

# Fix POST method response
try:
    apigateway.put_method_response(
        restApiId=API_ID,
        resourceId=RESOURCE_ID,
        httpMethod='POST',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
    print('POST method response configurado')
except Exception as e:
    print(f'POST method response: {e}')

# Fix DELETE method response
try:
    apigateway.put_method_response(
        restApiId=API_ID,
        resourceId=RESOURCE_ID,
        httpMethod='DELETE',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
    print('DELETE method response configurado')
except Exception as e:
    print(f'DELETE method response: {e}')

# Fix OPTIONS method response
try:
    apigateway.put_method_response(
        restApiId=API_ID,
        resourceId=RESOURCE_ID,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': True,
            'method.response.header.Access-Control-Allow-Methods': True,
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
    print('OPTIONS method response configurado')
except Exception as e:
    print(f'OPTIONS method response: {e}')

# Fix OPTIONS integration response
try:
    apigateway.put_integration_response(
        restApiId=API_ID,
        resourceId=RESOURCE_ID,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
            'method.response.header.Access-Control-Allow-Methods': "'POST,DELETE,OPTIONS'",
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        },
        responseTemplates={'application/json': ''}
    )
    print('OPTIONS integration response configurado')
except Exception as e:
    print(f'OPTIONS integration response: {e}')

# Deploy
try:
    apigateway.create_deployment(
        restApiId=API_ID,
        stageName='prod',
        description='Fix CORS for folders'
    )
    print('Deploy realizado')
except Exception as e:
    print(f'Deploy: {e}')

print('\nCORS corrigido!')
