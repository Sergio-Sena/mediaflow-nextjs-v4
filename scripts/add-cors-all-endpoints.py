import boto3

apigw = boto3.client('apigateway', region_name='us-east-1')
api_id = 'gdb962d234'

# Get all resources
resources = apigw.get_resources(restApiId=api_id)

print("Adicionando CORS aos endpoints...\n")

for resource in resources['items']:
    path = resource['path']
    resource_id = resource['id']
    
    # Skip root
    if path == '/':
        continue
    
    # Check if OPTIONS method exists
    methods = resource.get('resourceMethods', {})
    
    if 'OPTIONS' not in methods:
        print(f"[{path}] Criando OPTIONS...")
        try:
            # Create OPTIONS method
            apigw.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            
            # Create mock integration
            apigw.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={'application/json': '{"statusCode": 200}'}
            )
            
            # Create method response
            apigw.put_method_response(
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
            
            # Create integration response
            apigw.put_integration_response(
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
            
            print(f"  [OK] OPTIONS criado")
        except Exception as e:
            print(f"  [ERRO] {e}")
    else:
        print(f"[{path}] OPTIONS ja existe")

print("\nDeployando mudancas...")
apigw.create_deployment(restApiId=api_id, stageName='prod')
print("[OK] Deploy concluido!")
