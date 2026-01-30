import boto3
import json

client = boto3.client('apigateway')
api_id = 'gdb962d234'

# Encontrar resource /update-user
resources = client.get_resources(restApiId=api_id)

update_resource = None
for resource in resources['items']:
    if resource['path'] == '/update-user':
        update_resource = resource
        break

if not update_resource:
    print("[ERROR] Resource /update-user nao encontrado")
    exit(1)

resource_id = update_resource['id']
print(f"[OK] Resource ID: {resource_id}")

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
    print("[WARN] Metodo OPTIONS ja existe")

# Configurar integração OPTIONS
client.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)
print("[OK] Integracao OPTIONS configurada")

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
    print("[OK] Method Response OPTIONS configurado")
except:
    print("[WARN] Method Response OPTIONS ja existe")

# Configurar integration response OPTIONS
try:
    client.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
            'method.response.header.Access-Control-Allow-Methods': "'GET,POST,PUT,PATCH,DELETE,OPTIONS'",
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        }
    )
    print("[OK] Integration Response OPTIONS configurado")
except:
    print("[WARN] Integration Response OPTIONS ja existe")

# Configurar CORS para método POST/PUT
for method in ['POST', 'PUT', 'PATCH']:
    try:
        # Method Response
        client.put_method_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Origin': True
            }
        )
        
        # Integration Response
        client.put_integration_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=method,
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            }
        )
        print(f"[OK] CORS configurado para {method}")
    except Exception as e:
        print(f"[WARN] {method}: {e}")

# Deploy
client.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='Fix CORS for /users/update'
)
print("[OK] Deploy realizado!")
print("\n[SUCCESS] CORS corrigido para /update-user")
