import boto3
import json

apigateway = boto3.client('apigateway', region_name='us-east-1')

with open('mediaflow-config.json', 'r') as f:
    config = json.load(f)

api_id = config['api_gateway']['api_id']

# Recursos que precisam de CORS
resources_to_fix = ['avatar-presigned', 'update-user']

resources = apigateway.get_resources(restApiId=api_id)

for resource_name in resources_to_fix:
    resource = [r for r in resources['items'] if r.get('pathPart') == resource_name]
    
    if not resource:
        print(f"Resource {resource_name} not found")
        continue
    
    resource_id = resource[0]['id']
    
    print(f"\nConfiguring CORS for /{resource_name}...")
    
    # Add OPTIONS method
    try:
        apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            authorizationType='NONE'
        )
        print("  OPTIONS method created")
    except:
        print("  OPTIONS method exists")
    
    # Add MOCK integration
    try:
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={'application/json': '{"statusCode": 200}'}
        )
        print("  MOCK integration created")
    except:
        print("  MOCK integration exists")
    
    # Add method response
    try:
        apigateway.put_method_response(
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
        print("  Method response created")
    except:
        print("  Method response exists")
    
    # Add integration response
    try:
        apigateway.put_integration_response(
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
        print("  Integration response created")
    except:
        print("  Integration response exists")

# Deploy
apigateway.create_deployment(restApiId=api_id, stageName='prod')
print("\n\nAPI Gateway deployed with CORS!")
