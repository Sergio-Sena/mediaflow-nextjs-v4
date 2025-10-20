#!/usr/bin/env python3
import boto3

client = boto3.client('apigateway', region_name='us-east-1')
API_ID = 'gdb962d234'

# Get all resources
resources = client.get_resources(restApiId=API_ID)

for resource in resources['items']:
    path = resource.get('path', '')
    resource_id = resource['id']
    methods = resource.get('resourceMethods', {})
    
    # Skip root
    if path == '/':
        continue
    
    print(f"\nProcessing: {path}")
    
    # Add OPTIONS if not exists
    if 'OPTIONS' not in methods:
        try:
            client.put_method(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                authorizationType='NONE'
            )
            
            client.put_integration(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                type='MOCK',
                requestTemplates={'application/json': '{"statusCode": 200}'}
            )
            
            client.put_method_response(
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
            
            client.put_integration_response(
                restApiId=API_ID,
                resourceId=resource_id,
                httpMethod='OPTIONS',
                statusCode='200',
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
                    'method.response.header.Access-Control-Allow-Methods': "'GET,POST,PUT,DELETE,OPTIONS'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'"
                }
            )
            print(f"  [OK] OPTIONS added")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print(f"  [SKIP] OPTIONS exists")

# Deploy
print("\nDeploying...")
client.create_deployment(restApiId=API_ID, stageName='prod')
print("[OK] Deployed!")
