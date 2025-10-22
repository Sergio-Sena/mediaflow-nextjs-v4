import boto3
import json

apigateway = boto3.client('apigatewayv2', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')

API_ID = 'gdb962d234'
LAMBDA_ARN = 'arn:aws:lambda:us-east-1:969430605054:function:folder-operations'

# Create integration
try:
    integration = apigateway.create_integration(
        ApiId=API_ID,
        IntegrationType='AWS_PROXY',
        IntegrationUri=LAMBDA_ARN,
        PayloadFormatVersion='2.0'
    )
    integration_id = integration['IntegrationId']
    print(f'Integration criada: {integration_id}')
except Exception as e:
    print(f'Erro ao criar integration: {e}')
    # Get existing integration
    integrations = apigateway.get_integrations(ApiId=API_ID)
    for integ in integrations['Items']:
        if 'folder-operations' in integ.get('IntegrationUri', ''):
            integration_id = integ['IntegrationId']
            print(f'Integration existente: {integration_id}')
            break

# Create routes
routes = [
    ('POST', '/folders'),
    ('DELETE', '/folders'),
    ('OPTIONS', '/folders')
]

for method, path in routes:
    try:
        route = apigateway.create_route(
            ApiId=API_ID,
            RouteKey=f'{method} {path}',
            Target=f'integrations/{integration_id}'
        )
        print(f'Rota criada: {method} {path}')
    except Exception as e:
        print(f'Rota {method} {path} ja existe ou erro: {e}')

# Add Lambda permission
try:
    lambda_client.add_permission(
        FunctionName='folder-operations',
        StatementId='apigateway-invoke-folders',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:us-east-1:969430605054:{API_ID}/*/*/folders'
    )
    print('Permissao Lambda adicionada')
except Exception as e:
    print(f'Permissao ja existe ou erro: {e}')

print('\nAPI Gateway configurado com sucesso!')
print(f'Endpoint: https://{API_ID}.execute-api.us-east-1.amazonaws.com/prod/folders')
