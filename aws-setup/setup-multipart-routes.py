import boto3
import json

apigateway = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')

API_ID = 'gdb962d234'
LAMBDA_ARN = 'arn:aws:lambda:us-east-1:969430605054:function:mediaflow-multipart-handler'

# Obter root resource
resources = apigateway.get_resources(restApiId=API_ID)
root_id = [r for r in resources['items'] if r['path'] == '/'][0]['id']

print("Criando rotas multipart...")

# 1. Criar /multipart
try:
    multipart_resource = apigateway.create_resource(
        restApiId=API_ID,
        parentId=root_id,
        pathPart='multipart'
    )
    multipart_id = multipart_resource['id']
    print(f"OK /multipart criado: {multipart_id}")
except:
    # Já existe
    multipart_id = [r for r in resources['items'] if r['path'] == '/multipart'][0]['id']
    print(f"OK /multipart ja existe: {multipart_id}")

# 2. Criar /{action} sob /multipart
try:
    action_resource = apigateway.create_resource(
        restApiId=API_ID,
        parentId=multipart_id,
        pathPart='{action}'
    )
    action_id = action_resource['id']
    print(f"OK /multipart/{{action}} criado: {action_id}")
except:
    resources = apigateway.get_resources(restApiId=API_ID)
    action_id = [r for r in resources['items'] if r['path'] == '/multipart/{action}'][0]['id']
    print(f"OK /multipart/{{action}} ja existe: {action_id}")

# 3. Adicionar métodos POST e OPTIONS
for method in ['POST', 'OPTIONS']:
    try:
        apigateway.put_method(
            restApiId=API_ID,
            resourceId=action_id,
            httpMethod=method,
            authorizationType='NONE'
        )
        print(f"OK Metodo {method} adicionado")
        
        # Integração com Lambda
        apigateway.put_integration(
            restApiId=API_ID,
            resourceId=action_id,
            httpMethod=method,
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{LAMBDA_ARN}/invocations'
        )
        print(f"OK Integracao {method} configurada")
        
    except Exception as e:
        print(f"AVISO {method} ja existe ou erro: {e}")

# 4. Deploy
try:
    apigateway.create_deployment(
        restApiId=API_ID,
        stageName='prod',
        description='Add multipart routes'
    )
    print("\nOK Deploy realizado!")
    print(f"Endpoints disponiveis:")
    print(f"   POST https://{API_ID}.execute-api.us-east-1.amazonaws.com/prod/multipart/init")
    print(f"   POST https://{API_ID}.execute-api.us-east-1.amazonaws.com/prod/multipart/part")
    print(f"   POST https://{API_ID}.execute-api.us-east-1.amazonaws.com/prod/multipart/complete")
    print(f"   POST https://{API_ID}.execute-api.us-east-1.amazonaws.com/prod/multipart/abort")
except Exception as e:
    print(f"ERRO no deploy: {e}")
