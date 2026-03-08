import boto3
import json

client = boto3.client('apigateway')
api_id = 'gdb962d234'

# Recursos que precisam de CORS
resources_to_fix = [
    '/upload/presigned',
    '/users',
    '/multipart/init',
    '/multipart/part',
    '/multipart/complete'
]

# Obter todos os recursos
resources = client.get_resources(restApiId=api_id, limit=500)

for resource in resources['items']:
    path = resource.get('path', '')
    
    if any(path.endswith(r) for r in resources_to_fix):
        resource_id = resource['id']
        print(f"\nConfigurando CORS para: {path} ({resource_id})")
        
        # Criar método OPTIONS se não existir
        try:
            client.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            print(f"  OK Metodo OPTIONS criado")
        except client.exceptions.ConflictException:
            print(f"  INFO Metodo OPTIONS ja existe")
        
        # Configurar resposta OPTIONS
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
            print(f"  OK Method Response configurado")
        except Exception as e:
            print(f"  WARN Method Response: {e}")
        
        # Configurar integração OPTIONS
        try:
            client.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={
                    'application/json': '{"statusCode": 200}'
                }
            )
            print(f"  OK Integration configurado")
        except Exception as e:
            print(f"  WARN Integration: {e}")
        
        # Configurar resposta da integração
        try:
            client.put_integration_response(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                    'method.response.header.Access-Control-Allow-Methods': "'GET,POST,PUT,DELETE,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            print(f"  OK Integration Response configurado")
        except Exception as e:
            print(f"  WARN Integration Response: {e}")

print("\n\nFazendo deploy...")
client.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='CORS fix for CloudFront'
)
print("Deploy concluido!")
