#!/usr/bin/env python3
import boto3

apigateway = boto3.client('apigateway', region_name='us-east-1')

API_ID = 'gdb962d234'
LAMBDA_ARN = 'arn:aws:lambda:us-east-1:969430605054:function:mediaflow-multipart-handler'

# 1. Obter root resource
resources = apigateway.get_resources(restApiId=API_ID)
root_id = [r for r in resources['items'] if r['path'] == '/'][0]['id']

# 2. Criar resource /multipart
try:
    multipart_resource = apigateway.create_resource(
        restApiId=API_ID,
        parentId=root_id,
        pathPart='multipart'
    )
    resource_id = multipart_resource['id']
    print(f"OK Resource /multipart criado: {resource_id}")
except Exception as e:
    # Já existe, pegar ID
    existing = [r for r in resources['items'] if r['path'] == '/multipart']
    if existing:
        resource_id = existing[0]['id']
        print(f"INFO Resource /multipart ja existe: {resource_id}")
    else:
        print(f"ERRO: {str(e)}")
        raise

# 3. Criar método POST
try:
    apigateway.put_method(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='POST',
        authorizationType='NONE'
    )
    print("OK Metodo POST criado")
except:
    print("INFO Metodo POST ja existe")

# 4. Integrar com Lambda
apigateway.put_integration(
    restApiId=API_ID,
    resourceId=resource_id,
    httpMethod='POST',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{LAMBDA_ARN}/invocations'
)
print("OK Integracao Lambda configurada")

# 5. Criar método OPTIONS (CORS)
try:
    apigateway.put_method(
        restApiId=API_ID,
        resourceId=resource_id,
        httpMethod='OPTIONS',
        authorizationType='NONE'
    )
    print("OK Metodo OPTIONS criado")
except:
    print("INFO Metodo OPTIONS ja existe")

# 6. Configurar method response primeiro
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

# 7. Integrar OPTIONS com MOCK
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
        'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)
print("OK CORS configurado")

# 8. Deploy para stage 'prod'
apigateway.create_deployment(
    restApiId=API_ID,
    stageName='prod',
    description='Deploy multipart endpoint'
)
print("OK Deploy realizado")

print("\nSUCESSO: API Gateway configurado!")
print(f"Endpoint: https://{API_ID}.execute-api.us-east-1.amazonaws.com/prod/multipart")
