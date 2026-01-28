import boto3
import json

client = boto3.client('apigateway', region_name='us-east-1')

# API Gateway ID (extraído da URL)
api_id = 'gdb962d234'

# Licorporativo recursos
resources = client.get_resources(restApiId=api_id)

print("Recursos encontrados:")
for resource in resources['items']:
    print(f"  {resource['path']} - {resource['id']}")
    
    # Verificar se tem OPTIONS
    methods = resource.get('resourceMethods', {})
    if 'OPTIONS' not in methods:
        print(f"    [X] OPTIONS nao configurado em {resource['path']}")
        
        # Adicionar OPTIONS se for /files
        if resource['path'] == '/files':
            print(f"    [+] Adicionando OPTIONS em /files...")
            
            # Criar método OPTIONS
            client.put_method(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            
            # Criar integração MOCK
            client.put_integration(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={
                    'application/json': '{"statusCode": 200}'
                }
            )
            
            # Criar resposta do método
            client.put_method_response(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': True,
                    'method.response.header.Access-Control-Allow-Methods': True,
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            )
            
            # Criar resposta da integração
            client.put_integration_response(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization,x-correlation-id'",
                    'method.response.header.Access-Control-Allow-Methods': "'GET,POST,DELETE,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            
            print(f"    [OK] OPTIONS configurado!")
    else:
        print(f"    [OK] OPTIONS ja existe em {resource['path']}")

# Deploy
print("\n[DEPLOY] Fazendo deploy...")
client.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='Fix CORS OPTIONS'
)
print("[OK] Deploy concluido!")
