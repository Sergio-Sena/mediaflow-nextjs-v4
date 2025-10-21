import boto3

apigateway = boto3.client('apigateway', region_name='us-east-1')
API_ID = 'gdb962d234'

print("Habilitando CORS para /multipart/{action}...")

# Obter resource ID
resources = apigateway.get_resources(restApiId=API_ID)
action_id = [r for r in resources['items'] if r['path'] == '/multipart/{action}'][0]['id']

# Configurar response do OPTIONS
try:
    apigateway.put_method_response(
        restApiId=API_ID,
        resourceId=action_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': True,
            'method.response.header.Access-Control-Allow-Methods': True,
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
    print("OK Method response OPTIONS configurado")
except Exception as e:
    print(f"AVISO: {e}")

# Configurar integration response do OPTIONS
try:
    apigateway.put_integration_response(
        restApiId=API_ID,
        resourceId=action_id,
        httpMethod='OPTIONS',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
            'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        }
    )
    print("OK Integration response OPTIONS configurado")
except Exception as e:
    print(f"AVISO: {e}")

# Configurar response do POST
try:
    apigateway.put_method_response(
        restApiId=API_ID,
        resourceId=action_id,
        httpMethod='POST',
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Origin': True
        }
    )
    print("OK Method response POST configurado")
except Exception as e:
    print(f"AVISO: {e}")

# Deploy
apigateway.create_deployment(
    restApiId=API_ID,
    stageName='prod',
    description='Enable CORS for multipart'
)

print("\nOK CORS habilitado!")
print("Teste novamente em http://localhost:3000")
