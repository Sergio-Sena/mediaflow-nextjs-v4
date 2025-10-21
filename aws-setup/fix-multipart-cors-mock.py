import boto3

apigateway = boto3.client('apigateway', region_name='us-east-1')
API_ID = 'gdb962d234'

print("Configurando CORS com MOCK integration...")

# Obter resource ID
resources = apigateway.get_resources(restApiId=API_ID)
action_id = [r for r in resources['items'] if r['path'] == '/multipart/{action}'][0]['id']

# Deletar integração OPTIONS existente
try:
    apigateway.delete_integration(
        restApiId=API_ID,
        resourceId=action_id,
        httpMethod='OPTIONS'
    )
    print("OK Integracao OPTIONS antiga removida")
except:
    pass

# Criar MOCK integration para OPTIONS
apigateway.put_integration(
    restApiId=API_ID,
    resourceId=action_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)
print("OK MOCK integration criada")

# Configurar integration response
apigateway.put_integration_response(
    restApiId=API_ID,
    resourceId=action_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
        'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    },
    responseTemplates={
        'application/json': ''
    }
)
print("OK Integration response configurada")

# Deploy
apigateway.create_deployment(
    restApiId=API_ID,
    stageName='prod',
    description='Fix CORS with MOCK'
)

print("\nOK CORS corrigido com MOCK!")
print("Aguarde 5 segundos e teste novamente")
