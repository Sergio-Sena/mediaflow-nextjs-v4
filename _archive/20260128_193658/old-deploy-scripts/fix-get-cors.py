import boto3

apigw = boto3.client('apigateway')
API_ID = 'gdb962d234'
RESOURCE_ID = 'zct1na'

print("Adicionando CORS headers no método GET...")

# Adicionar method response com headers CORS
try:
    apigw.put_method_response(
        restApiId=API_ID,
        resourceId=RESOURCE_ID,
        httpMethod='GET',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin': True,
            'method.response.header.Access-Control-Allow-Headers': True,
            'method.response.header.Access-Control-Allow-Methods': True
        }
    )
    print("Method response 200 criado")
except Exception as e:
    print(f"Method response: {e}")

# Adicionar para 403
try:
    apigw.put_method_response(
        restApiId=API_ID,
        resourceId=RESOURCE_ID,
        httpMethod='GET',
        statusCode='403',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
    print("Method response 403 criado")
except Exception as e:
    print(f"Method response 403: {e}")

# Atualizar integration response
try:
    apigw.put_integration_response(
        restApiId=API_ID,
        resourceId=RESOURCE_ID,
        httpMethod='GET',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin': "'*'",
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
            'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'"
        }
    )
    print("Integration response 200 atualizado")
except Exception as e:
    print(f"Integration response: {e}")

# Deploy
apigw.create_deployment(restApiId=API_ID, stageName='prod')
print("API deployada!")
